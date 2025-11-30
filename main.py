import yaml
import time
import math
import os
import multiprocessing as mp
import numpy as np
from typing import List, Dict, Any, Set, FrozenSet

# Import pro symbolickou matematiku
try:
    import sympy
    from sympy import symbols, simplify
except ImportError:
    print("CRITICAL: Knihovna 'sympy' neni nainstalovana. Prosim spustte 'pip install sympy'.")
    exit(1)

from src.constants_manager import ConstantsManager
from src.equation_generator import EquationGenerator
from src.calculation_engine import GpuCalculationEngine

# =============================================================================
# POMOCNÉ FUNKCE PRO SYSTÉM
# =============================================================================

def set_low_priority():
    """
    Nastaví aktuálnímu procesu nízkou prioritu (high 'nice' value),
    aby nezamrzal počítač a terminál zůstal responzivní.
    """
    try:
        # Unix/Linux: +15 je nízká priorita (šetrná k systému)
        os.nice(15)
    except Exception:
        pass

# =============================================================================
# LOGIKA FILTRŮ (Sensitivity Test + SymPy)
# =============================================================================

def evaluate_rpn_numeric(rpn_indices: List[int], constants_map: Dict[int, Any], override_values: Dict[int, float] = None) -> float:
    stack = []
    if override_values is None: override_values = {}
    try:
        for token in rpn_indices:
            if token > 0:
                val = override_values.get(token, constants_map[token]['value_float'])
                stack.append(val)
            else:
                if len(stack) < 2: return float('nan')
                b, a = stack.pop(), stack.pop()
                if token == -1: stack.append(a + b)
                elif token == -2: stack.append(a - b)
                elif token == -3: stack.append(a * b)
                elif token == -4:
                    if b == 0: return float('nan')
                    stack.append(a / b)
                elif token == -5:
                    try:
                        res = a ** b
                        # Ochrana proti komplexním číslům (odmocnina ze záporné)
                        if isinstance(res, complex): return float('nan')
                        stack.append(res)
                    except: return float('nan')

        if len(stack) != 1: return float('nan')

        # Finální kontrola výsledku na komplexnost
        res = stack[0]
        if isinstance(res, complex): return float('nan')
        return res

    except: return float('nan')

def rpn_to_sympy_expression(rpn_indices: List[int], constants_map: Dict[int, Any]):
    stack = []
    used_symbols = set()
    ops = {-1: lambda x,y: x+y, -2: lambda x,y: x-y, -3: lambda x,y: x*y, -4: lambda x,y: x/y, -5: lambda x,y: x**y}
    try:
        for token in rpn_indices:
            if token > 0:
                c = constants_map[token]
                s = symbols(c['symbol'])
                stack.append(s)
                used_symbols.add(c['symbol'])
            else:
                if len(stack) < 2: return None, None
                b, a = stack.pop(), stack.pop()
                stack.append(ops[token](a, b))
        return stack[0], used_symbols
    except: return None, None

def is_valid_discovery(rpn_indices: List[int], target_symbol: str, constants_map: Dict[int, Any], seen_clusters: Dict[str, Any]) -> bool:
    # 1. Rychlý filtr cílů - nezajímá nás, když vyjde číslo
    if target_symbol in ['one', 'two', 'three', 'half', 'pi', 'phi', 'e_math', 'alpha', 'sqrt_2', 'sqrt_3']:
        return False

    used_const_ids = [t for t in rpn_indices if t > 0]
    unique_const_ids = set(used_const_ids)

    # 2. Numerický test citlivosti (Ghost variables)
    base_result = evaluate_rpn_numeric(rpn_indices, constants_map)

    # Robustní kontrola NaN (musí být reálný float)
    if isinstance(base_result, complex) or math.isnan(base_result) or math.isinf(base_result):
        return False

    for cid in unique_const_ids:
        # Matematické konstanty netestujeme na citlivost
        if constants_map[cid]['symbol'] in ['one', 'two', 'half', 'three', 'pi', 'e_math', 'phi', 'sqrt_2', 'sqrt_3']:
            continue

        perturbed_val = constants_map[cid]['value_float'] * 1.05 # 5% změna
        new_result = evaluate_rpn_numeric(rpn_indices, constants_map, override_values={cid: perturbed_val})

        if isinstance(new_result, complex) or math.isnan(new_result):
            return False

        # Pokud se výsledek nezmění i když jsme změnili vstup, je proměnná zbytečná
        if abs(new_result - base_result) < 1e-7 * abs(base_result):
            return False

    # 3. SymPy Ratio Test (Definice a Identity)
    expr, used_symbols = rpn_to_sympy_expression(rpn_indices, constants_map)
    if expr is None: return False

    all_involved = used_symbols | {target_symbol}

    # Blacklist známých definičních skupin
    definition_groups = [
        {'c', 'mu_0', 'epsilon_0', 'Z_0'},
        {'h', 'hbar', 'e_charge', 'G_0', 'R_K', 'K_J', 'phi_0', 'two', 'half', 'pi'},
        {'k_B', 'R', 'F', 'e_charge', 'N_A'},
        {'m_P', 'l_P', 't_P', 'G', 'c', 'hbar'},
        {'m_e', 'r_e', 'alpha', 'h', 'c', 'e_charge', 'R_inf', 'a_0', 'lambda_C', 'pi', 'two', 'half'},
        {'mu_B', 'e_charge', 'h', 'm_e', 'two', 'pi'}
    ]

    for group in definition_groups:
        if len(all_involved) > 2 and all_involved.issubset(group):
            return False

    try:
        target_sym = symbols(target_symbol)
        ratio = simplify(expr / target_sym)
        if ratio.is_constant(): return False
    except: return False

    # 4. Deduplikace
    cluster_signature = frozenset(all_involved)
    if cluster_signature in seen_clusters: return False
    seen_clusters[cluster_signature] = True
    return True

# =============================================================================
# PROCESY (PRODUCER & CONSUMER)
# =============================================================================

def producer_task(queue_standard: mp.Queue, queue_gravity: mp.Queue, config: Dict[str, Any], constants: List[Dict[str, Any]]):
    """
    Generuje NÁHODNÉ rovnice (Monte Carlo) v nekonečné smyčce.
    """
    set_low_priority()
    try:
        generator = EquationGenerator(constants=constants, operators=config['generator']['operators'], max_depth=config['generator']['max_depth'])

        batch_size = config['engine']['batch_size']
        gravity_symbol = config['engine']['gravity_constant_symbol']
        const_map = {c['symbol']: i+1 for i, c in enumerate(constants)}
        g_tok = const_map.get(gravity_symbol, -999)

        print("[Producer] STARTING INFINITE RANDOM SEARCH (Monte Carlo Mode)...")
        print("[Producer] Target complexity: 3 to 6 constants (Deep Search).")

        while True:
            if queue_standard.qsize() > 4 or queue_gravity.qsize() > 4:
                time.sleep(1.0)
                continue

            # Generování - velikost dávky pro random
            current_batch_size = 50000
            raw_batch = generator.generate_random_batch(batch_size=current_batch_size, min_consts=3, max_consts=6)

            std, grav = [], []
            for eq in raw_batch:
                if g_tok in eq: grav.append(eq)
                else: std.append(eq)

            if std:
                max_l = max(len(e) for e in std)
                queue_standard.put([e + [0]*(max_l-len(e)) for e in std])
            if grav:
                max_l = max(len(e) for e in grav)
                queue_gravity.put([e + [0]*(max_l-len(e)) for e in grav])

            time.sleep(0.02)

    except Exception as e: print(f"[Producer] Error: {e}")
    finally:
        queue_standard.put(None)
        queue_gravity.put(None)

def consumer_task(queue: mp.Queue, config: Dict[str, Any], constants: List[Dict[str, Any]],
                  tolerance: float, p_type: str, log_state: Dict, stats: Dict, seen_clusters: Dict):

    set_low_priority()
    try: engine = GpuCalculationEngine(constants)
    except: return

    const_map = {i+1: c for i, c in enumerate(constants)}
    op_map = {'+':-1, '-':-2, '*':-3, '/':-4, '^':-5}
    c_lookup = {c['symbol']: i+1 for i, c in enumerate(constants)}

    # --- NASTAVENÍ TOLERANCE PRO ZÁPIS ---
    # Zde nastavujeme limit pro LOGOVÁNÍ na 1% (0.01), jak bylo požadováno.
    LOGGING_THRESHOLD = 0.01

    print(f"[{p_type}] Ready (Monte Carlo Mode). Logging threshold: {LOGGING_THRESHOLD:.0%} (1%)")
    batch_num = 0

    while True:
        if queue.empty():
            time.sleep(0.1)
            continue

        batch = queue.get()
        if batch is None: break

        batch_num += 1
        if batch_num % 20 == 0: print(f"--> [{p_type}] Processed {batch_num} random batches...")

        matches = engine.process_batch(batch, tolerance=tolerance)

        if matches:
            matches.sort(key=lambda x: (x['rpn_length'], x['deviation']))
            valid = []

            for match in matches:
                # 1. Filtr odchylky (nyní propustí vše do 1%)
                if match['deviation'] > LOGGING_THRESHOLD:
                    continue

                parts = match['equation_rpn'].split(' ')
                rpn = []
                ok = True
                for p in parts:
                    if p in op_map: rpn.append(op_map[p])
                    elif p in c_lookup: rpn.append(c_lookup[p])
                    else: ok=False; break
                if not ok: continue

                if is_valid_discovery(rpn, match['target'], const_map, seen_clusters):
                    valid.append(match)
                    time.sleep(0.01)

            if valid:
                print(f"    !!! [{p_type}] Found {len(valid)} matches within 1% deviation !!!")
                base = config['paths']['candidates_log'].replace('.log', '')
                for m in valid:
                    cnt = log_state['total_records_written']
                    f_idx = (cnt // 500) + 1
                    path = f"{base}_{f_idx}.log"
                    mode = 'a' if os.path.exists(path) else 'w'
                    with open(path, mode) as f:
                        if mode=='w': f.write(f"# Equation Explorer v3.2 (1% Tolerance)\n\n")
                        f.write(f"Match ({p_type}): '{m['equation_rpn']}' ==> {m['target']} (Dev: {m['deviation']:.4e})\n")
                    log_state['total_records_written'] = cnt + 1

        time.sleep(0.05)

    stats[f'{p_type}_processed'] = batch_num * 50000
    print(f"[{p_type}] Finished.")

def main():
    print("========================================")
    print("===   EQUATION EXPLORER v3.2         ===")
    print("===   (Monte Carlo + 1% Tolerance)   ===")
    print("========================================")

    set_low_priority()

    with open('config.yaml', 'r') as f: config = yaml.safe_load(f)
    constants = ConstantsManager(config['paths']['constants_db']).constants

    base_log = config['paths']['candidates_log'].replace('.log', '')
    if not os.path.exists('output'): os.makedirs('output')

    # Vyčistit staré logy
    for f in os.listdir('output'):
        if f.startswith(os.path.basename(base_log)): os.remove(os.path.join('output', f))

    with mp.Manager() as pm:
        log_state = pm.dict({'total_records_written': 0})
        stats = pm.dict()
        seen_clusters = pm.dict()

        q_std = mp.Queue(maxsize=5)
        q_grav = mp.Queue(maxsize=5)

        # OVERRIDE CONFIG TOLERANCE
        # Aby GPU vůbec vracelo výsledky s odchylkou 1%, musíme to vnutit enginu,
        # bez ohledu na to, co je v config.yaml (tam bývá 1e-9).
        LOOSE_TOLERANCE = 0.01

        pro = mp.Process(target=producer_task, args=(q_std, q_grav, config, constants))
        con_std = mp.Process(target=consumer_task, args=(q_std, config, constants, LOOSE_TOLERANCE, "Standard", log_state, stats, seen_clusters))
        con_grav = mp.Process(target=consumer_task, args=(q_grav, config, constants, LOOSE_TOLERANCE, "Gravity", log_state, stats, seen_clusters))

        print("Starting processes... (Press Ctrl+C to stop)")

        try:
            pro.start(); con_std.start(); con_grav.start()
            pro.join(); con_std.join(); con_grav.join()
        except KeyboardInterrupt:
            print("\n[Main] Stopping...")
            pro.terminate(); con_std.terminate(); con_grav.terminate()

        print(f"\nSession ended.")

if __name__ == '__main__':
    try: mp.set_start_method('spawn', force=True)
    except: pass
    main()