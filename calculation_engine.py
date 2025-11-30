import cupy as cp
import numpy as np
import time
import math
import os
from collections import Counter

# --- CUDA KERNEL ---
# Kernel zůstává stejný, stará se o rychlý hrubý výpočet na grafické kartě
cuda_kernel_source = r'''
#define OP_ADD -1
#define OP_SUB -2
#define OP_MUL -3
#define OP_DIV -4
#define OP_POW -5

#define STACK_SIZE 16
#define NUM_DIMENSIONS 7

__device__ bool perform_dim_op(int op, const int* a, const int* b, int* result, const double b_val) {
    if (op == OP_ADD || op == OP_SUB) {
        for (int i = 0; i < NUM_DIMENSIONS; ++i) {
            if (a[i] != b[i]) return false;
            result[i] = a[i];
        }
    } else if (op == OP_POW) {
        bool is_b_dimensionless = true;
        for (int i = 0; i < NUM_DIMENSIONS; ++i) {
            if (b[i] != 0) {
                is_b_dimensionless = false;
                break;
            }
        }
        if (!is_b_dimensionless) return false;

        for (int i = 0; i < NUM_DIMENSIONS; ++i) {
            result[i] = (int)(round(a[i] * b_val));
        }

    } else {
        for (int i = 0; i < NUM_DIMENSIONS; ++i) {
            if (op == OP_MUL) result[i] = a[i] + b[i];
            else if (op == OP_DIV) result[i] = a[i] - b[i];
        }
    }
    return true;
}

extern "C" __global__
void evaluate_equations(
    const int* equations, const int max_eq_len,
    const double* const_vals, const int* const_dims,
    const double* target_vals, const int* target_dims,
    const int num_targets, const double tolerance, long* results
)
{
    int eq_idx = blockIdx.x * blockDim.x + threadIdx.x;
    int num_equations_in_grid = gridDim.x * blockDim.x;
    if (eq_idx >= num_equations_in_grid) return;

    double value_stack[STACK_SIZE];
    int dim_stack[STACK_SIZE * NUM_DIMENSIONS];
    int value_sp = 0;
    int dim_sp = 0;

    const int* rpn = &equations[eq_idx * max_eq_len];

    for (int i = 0; i < max_eq_len; ++i) {
        int token = rpn[i];
        if (token == 0) break;

        if (token > 0) {
            int const_idx = token - 1;
            value_stack[value_sp++] = const_vals[const_idx];
            for(int d=0; d<NUM_DIMENSIONS; ++d) {
                dim_stack[dim_sp++] = const_dims[const_idx * NUM_DIMENSIONS + d];
            }
        } else {
            if (value_sp < 2) continue;
            double b_val = value_stack[--value_sp];
            double a_val = value_stack[--value_sp];
            dim_sp -= NUM_DIMENSIONS;
            const int* b_dim = &dim_stack[dim_sp];
            dim_sp -= NUM_DIMENSIONS;
            const int* a_dim = &dim_stack[dim_sp];
            int res_dim[NUM_DIMENSIONS];
            if (!perform_dim_op(token, a_dim, b_dim, res_dim, b_val)) continue;
            double result_val = 0.0;
            if (token == OP_ADD) result_val = a_val + b_val;
            else if (token == OP_SUB) result_val = a_val - b_val;
            else if (token == OP_MUL) result_val = a_val * b_val;
            else if (token == OP_DIV) {
                if (b_val == 0) continue;
                result_val = a_val / b_val;
            }
            else if (token == OP_POW) result_val = pow(a_val, b_val);
            value_stack[value_sp++] = result_val;
            for(int d=0; d<NUM_DIMENSIONS; ++d) {
                dim_stack[dim_sp++] = res_dim[d];
            }
        }
    }

    if (value_sp != 1) return;

    double final_value = value_stack[0];
    const int* final_dim = &dim_stack[0];

    for (int i = 0; i < num_targets; ++i) {
        bool dim_match = true;
        for (int d = 0; d < NUM_DIMENSIONS; ++d) {
            if (final_dim[d] != target_dims[i * NUM_DIMENSIONS + d]) {
                dim_match = false;
                break;
            }
        }
        if (dim_match) {
            double target_val = target_vals[i];
            // Kontrola tolerance
            if (target_val != 0 && abs(final_value - target_val) / abs(target_val) < tolerance) {
                long result_idx = atomicAdd((unsigned long long int*)&results[0], 1);
                if (result_idx < 1000) {
                    results[2 * result_idx + 1] = eq_idx;
                    results[2 * result_idx + 2] = i;
                }
                return;
            }
        }
    }
}
'''

class GpuCalculationEngine:
    def __init__(self, constants_data):
        print("Initializing GPU Calculation Engine...")
        self.kernel = cp.RawKernel(cuda_kernel_source, 'evaluate_equations')
        self.constants = constants_data
        self.const_vals_gpu = cp.array([c['value_float'] for c in self.constants], dtype=cp.float64)
        self.const_dims_gpu = cp.array([c['dimensions'] for c in self.constants], dtype=cp.int32).flatten()
        self.target_vals_gpu = self.const_vals_gpu
        self.target_dims_gpu = self.const_dims_gpu
        print(f"Loaded {len(self.constants)} constants to GPU memory.")

    def _evaluate_rpn_cpu(self, rpn_int: list) -> float:
        """
        Přepočítá RPN rovnici na CPU pro získání přesné hodnoty.

        OPRAVA: Přidán try-except blok pro zachycení OverflowError a ValueError.
        """
        try:
            stack = []
            for token in rpn_int:
                if token > 0:
                    stack.append(self.constants[token - 1]['value_float'])
                else:
                    if len(stack) < 2: return float('nan')
                    b = stack.pop()
                    a = stack.pop()

                    if token == -1:
                        stack.append(a + b)
                    elif token == -2:
                        stack.append(a - b)
                    elif token == -3:
                        stack.append(a * b)
                    elif token == -4:
                        if b == 0: return float('nan')
                        stack.append(a / b)
                    elif token == -5:
                        # Zde nastával OverflowError při příliš velkých číslech
                        # ValueError může nastat při umocňování záporného čísla na necelé číslo
                        stack.append(a ** b)

            return stack[0] if len(stack) == 1 else float('nan')

        except (OverflowError, ValueError, ZeroDivisionError):
            # Pokud dojde k přetečení (číslo moc velké) nebo chybě domény, vrátíme NaN
            return float('nan')
        except Exception:
            # Pro jistotu zachytíme i jiné nečekané aritmetické chyby
            return float('nan')

    def _is_interesting(self, rpn_int: list, target_idx: int, deviation: float) -> bool:
        """
        Rozšířený filtr inteligence (Princip Emergence + Heuristika odchylek).

        Args:
            rpn_int: RPN rovnice jako seznam integerů.
            target_idx: Index cílové konstanty v seznamu self.constants.
            deviation: Vypočítaná relativní odchylka.
        """
        used_constant_indices = {token - 1 for token in rpn_int if token > 0}

        # --- PRAVIDLO 1: Zákaz Tautologie ---
        # Pokud se cílová konstanta vyskytuje na vstupu, je to neplatné.
        if target_idx in used_constant_indices:
            return False

        # --- PRAVIDLO 2: Zákaz Triviálních identit ---
        # Pokud je odchylka podezřele přesně 0.0, často jde o identitu.
        if deviation < 1e-15:
            return False

        # --- PRAVIDLO 3: Minimální složitost ---
        # Rovnice musí kombinovat alespoň 2 RŮZNÉ (ne-cílové) konstanty.
        if len(used_constant_indices) < 2:
            return False

        return True

    def process_batch(self, equations_rpn_list, tolerance):
        num_equations = len(equations_rpn_list)
        if num_equations == 0: return []

        max_eq_len = len(equations_rpn_list[0])
        equations_gpu = cp.array(equations_rpn_list, dtype=cp.int32)

        MAX_RESULTS_PER_BATCH = 1000
        results_gpu = cp.zeros(1 + 2 * MAX_RESULTS_PER_BATCH, dtype=cp.int64)

        threads_per_block = 256
        blocks_per_grid = (num_equations + threads_per_block - 1) // threads_per_block

        # Spuštění kernelu na GPU
        self.kernel((blocks_per_grid,), (threads_per_block,), (equations_gpu, max_eq_len, self.const_vals_gpu, self.const_dims_gpu, self.target_vals_gpu, self.target_dims_gpu, len(self.constants), tolerance, results_gpu))

        results_host = results_gpu.get()

        interesting_matches = []
        num_found_raw = min(int(results_host[0]), MAX_RESULTS_PER_BATCH)
        op_map = {'-1':'+', '-2':'-', '-3':'*', '-4':'/', '-5':'^'}

        for i in range(num_found_raw):
            eq_idx, target_idx = int(results_host[2 * i + 1]), int(results_host[2 * i + 2])

            if eq_idx >= len(equations_rpn_list): continue

            rpn_int_padded = equations_rpn_list[eq_idx]
            rpn_int = [t for t in rpn_int_padded if t != 0] # Odstraníme padding

            # Nejprve spočítáme CPU hodnotu pro přesnou odchylku
            # Zde se nyní bezpečně zavolá upravená metoda, která nespadne
            calculated_value = self._evaluate_rpn_cpu(rpn_int)

            # Zahození numericky nestabilních výsledků (NaN, Inf)
            if np.isnan(calculated_value) or np.isinf(calculated_value):
                continue

            target_value = self.constants[target_idx]['value_float']
            relative_deviation = abs(calculated_value - target_value) / abs(target_value)

            # Aplikace filtrů inteligence
            if not self._is_interesting(rpn_int, target_idx, relative_deviation):
                continue

            rpn_str = [self.constants[t-1]['symbol'] if t > 0 else op_map.get(str(t), "?") for t in rpn_int]

            match = {
                "equation_rpn": ' '.join(rpn_str),
                "target": self.constants[target_idx]['symbol'],
                "deviation": relative_deviation,
                "rpn_length": len(rpn_int)
            }
            interesting_matches.append(match)

        return interesting_matches

if __name__ == '__main__':
    print("--- Testování vylepšených filtrů a opravy OverflowError ---")

    mock_consts = [
        {'symbol': 'c', 'value_float': 299792458.0, 'dimensions': [0,1,-1,0,0,0,0]},
        {'symbol': 'huge', 'value_float': 1e300, 'dimensions': [0,0,0,0,0,0,0]}, # Testovací obří číslo
    ]

    engine = GpuCalculationEngine(mock_consts)

    # Test 1: Overflow (huge ^ 2) -> mělo by vrátit NaN a nespadnout
    rpn_overflow = [2, 2, -3] # huge * huge (alternativa k pow pro test) nebo huge ^ 2
    rpn_pow_overflow = [2, 2, -5] # huge ^ huge -> EXTRÉMNÍ PŘETEČENÍ

    print("Testování OverflowError ochrany...")
    val = engine._evaluate_rpn_cpu(rpn_pow_overflow)
    print(f"Výsledek přetečení (očekáváme nan): {val}")

    if np.isnan(val):
        print("-> ÚSPĚCH: Aplikace nespadla a vrátila NaN.")
    else:
        print("-> CHYBA: Nezachyceno správně.")