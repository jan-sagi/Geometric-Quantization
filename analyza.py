import glob
import re
import os
import json
from mpmath import mp

# --- KONFIGURACE ---
mp.dps = 50
MAX_ODCHYLKA = 1e-4

# Zapnout filtrování dimenzí? (True = vyhodí rovnice typu "metr + sekunda")
FILTER_DIMENSIONS = True

CESTA_K_JSON = os.path.join("..", "data", "constants.json")
VSTUPNI_LOGY = "candidates_*.log"
VYSTUPNI_SLOZKA = "vysledky_high_precision_dim"

# --- 1. DEFINICE DIMENZÍ (SI JEDNOTKY) ---
# Formát: [Mass (kg), Length (m), Time (s), Current (A), Temp (K), Mole (mol), Intensity (cd)]
DIM_MAP = {
    # Základní
    'c':         [0, 1, -1, 0, 0, 0, 0],  # m/s
    'G':         [-1, 3, -2, 0, 0, 0, 0], # m^3 kg^-1 s^-2
    'h':         [1, 2, -1, 0, 0, 0, 0],  # J.s
    'hbar':      [1, 2, -1, 0, 0, 0, 0],
    'm_Pl':      [1, 0, 0, 0, 0, 0, 0],   # kg
    'l_p':       [0, 1, 0, 0, 0, 0, 0],   # m
    't_p':       [0, 0, 1, 0, 0, 0, 0],   # s
    'e_charge':  [0, 0, 1, 1, 0, 0, 0],   # C = A.s
    'e':         [0, 0, 1, 1, 0, 0, 0],
    'm_e':       [1, 0, 0, 0, 0, 0, 0],   # kg
    'm_p':       [1, 0, 0, 0, 0, 0, 0],   # kg
    'm_n':       [1, 0, 0, 0, 0, 0, 0],   # kg
    'mu_0':      [1, 1, -2, -2, 0, 0, 0], # N/A^2
    'epsilon_0': [-1, -3, 4, 2, 0, 0, 0], # F/m
    'Z_0':       [1, 2, -3, -2, 0, 0, 0], # Ohm
    'k_B':       [1, 2, -2, 0, -1, 0, 0], # J/K
    'R':         [1, 2, -2, 0, -1, -1, 0],# J/(K.mol)
    'F':         [0, 0, 1, 1, 0, 1, 0],   # C/mol
    'N_A':       [0, 0, 0, 0, 0, -1, 0],  # 1/mol
    'sigma_SB':  [1, 0, -3, 0, -4, 0, 0], # W m^-2 K^-4
    'alpha':     [0, 0, 0, 0, 0, 0, 0],   # Bezrozměrné
    'R_K':       [1, 2, -3, -2, 0, 0, 0], # Ohm
    'G_0':       [-1, -2, 3, 2, 0, 0, 0], # Siemens
    'K_J':       [-1, -2, 2, 1, 0, 0, 0], # Hz/V
    'phi_0':     [1, 2, -2, -1, 0, 0, 0], # Weber
    'mu_B':      [0, 2, 0, 1, 0, 0, 0],   # J/T
    'mu_pe':     [0, 0, 0, 0, 0, 0, 0],   # Poměr hmotností
    'b_wien':    [0, 1, 0, 0, 1, 0, 0],   # m.K
    'R_inf':     [0, -1, 0, 0, 0, 0, 0],  # 1/m
    'a_0':       [0, 1, 0, 0, 0, 0, 0],   # m
    'r_e':       [0, 1, 0, 0, 0, 0, 0],   # m
    'lambda_C':  [0, 1, 0, 0, 0, 0, 0],   # m
    'H_0':       [0, 0, -1, 0, 0, 0, 0],  # 1/s
    'u':         [1, 0, 0, 0, 0, 0, 0],   # kg
    'M_sol':     [1, 0, 0, 0, 0, 0, 0],   # kg
    'g_e':       [0, 0, 0, 0, 0, 0, 0],   # Bezrozměrné
    'g_p':       [0, 0, 0, 0, 0, 0, 0],   # Bezrozměrné
    'E_h':       [1, 2, -2, 0, 0, 0, 0],  # J
}

# --- 2. HODNOTY KONSTANT ---
C = {
    'one': mp.mpf(1), 'two': mp.mpf(2), 'three': mp.mpf(3),
    'half': mp.mpf(0.5), 'sqrt_2': mp.sqrt(2), 'sqrt_3': mp.sqrt(3),
    'pi': mp.pi, 'e_math': mp.e, 'phi': mp.phi
}
SKIP_JSON_MATH = set(C.keys())

# Rozměry matematických konstant jsou nuly
D = {k: [0]*7 for k in C}

def nacti_konstanty(cesta):
    if not os.path.exists(cesta):
        print(f"CHYBA: Soubor {cesta} nenalezen.")
        exit(1)
    with open(cesta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        sym = item.get('symbol')
        val = item.get('value')
        if sym and val and sym not in SKIP_JSON_MATH:
            C[sym] = mp.mpf(val)

            if sym in DIM_MAP:
                D[sym] = DIM_MAP[sym]
            else:
                D[sym] = [0]*7

            if sym == 'e_charge':
                C['e'] = C[sym]
                D['e'] = D[sym]

def dopocitat_chybejici():
    # hbar
    if 'h' in C:
        C['hbar'] = C['h'] / (2 * mp.pi)
        D['hbar'] = D['h']
    # m_Pl
    if all(k in C for k in ['hbar', 'c', 'G']):
        C['m_Pl'] = mp.sqrt(C['hbar'] * C['c'] / C['G'])
        D['m_Pl'] = [1, 0, 0, 0, 0, 0, 0]
    # Z_0
    if all(k in C for k in ['mu_0', 'c']):
        C['Z_0'] = C['mu_0'] * C['c']
        D['Z_0'] = DIM_MAP['Z_0']
    # G_0
    if 'h' in C and 'e_charge' in C:
        C['G_0'] = 2 * C['e_charge']**2 / C['h']
        D['G_0'] = DIM_MAP['G_0']

def rpn_calculator_full(equation_str):
    stack = []
    tokens = equation_str.split()

    try:
        for token in tokens:
            if token in C:
                stack.append((C[token], D[token]))
            elif token in ['+', '-', '*', '/']:
                if len(stack) < 2: return None
                (val_b, dim_b), (val_a, dim_a) = stack.pop(), stack.pop()

                if token == '+':
                    if FILTER_DIMENSIONS and dim_a != dim_b: return None
                    res_val = val_a + val_b
                    res_dim = dim_a
                elif token == '-':
                    if FILTER_DIMENSIONS and dim_a != dim_b: return None
                    res_val = val_a - val_b
                    res_dim = dim_a
                elif token == '*':
                    res_val = val_a * val_b
                    res_dim = [a + b for a, b in zip(dim_a, dim_b)]
                elif token == '/':
                    if val_b == 0: return None
                    res_val = val_a / val_b
                    res_dim = [a - b for a, b in zip(dim_a, dim_b)]

                stack.append((res_val, res_dim))

            elif token == '^':
                if len(stack) < 2: return None
                (val_b, dim_b), (val_a, dim_a) = stack.pop(), stack.pop()

                # 1. Exponent musí být bezrozměrný
                if FILTER_DIMENSIONS and any(x != 0 for x in dim_b):
                    return None

                # 2. Výpočet nové dimenze
                try:
                    exp_float = float(val_b)
                    res_dim = [d * exp_float for d in dim_a]
                except:
                    return None

                try:
                    res_val = mp.power(val_a, val_b)
                    if isinstance(res_val, mp.mpc): return None
                except:
                    return None

                stack.append((res_val, res_dim))
            else:
                return None

        if len(stack) == 1:
            return stack[0]
        return None
    except Exception as e:
        return None

def zpracovat():
    nacti_konstanty(CESTA_K_JSON)
    dopocitat_chybejici()

    if not os.path.exists(VYSTUPNI_SLOZKA): os.makedirs(VYSTUPNI_SLOZKA)
    soubory = glob.glob(VSTUPNI_LOGY)
    print(f"Zpracovávám {len(soubory)} souborů. Filtr dimenzí: {FILTER_DIMENSIONS}")

    vysledky = []
    regex = re.compile(r"Match.*?: '(.*?)' ==> (\w+)")

    for soubor in soubory:
        with open(soubor, 'r') as f:
            for radek in f:
                m = regex.search(radek)
                if m:
                    eq, target = m.group(1), m.group(2)
                    if target not in C: continue

                    res = rpn_calculator_full(eq)
                    if res is None: continue

                    val_calc, dim_calc = res
                    val_target = C[target]
                    dim_target = D[target]

                    # 1. Kontrola DIMENZE
                    dim_ok = True
                    if FILTER_DIMENSIONS:
                        for d1, d2 in zip(dim_calc, dim_target):
                            if abs(d1 - d2) > 1e-5:
                                dim_ok = False; break

                    if not dim_ok: continue

                    # 2. Kontrola HODNOTY
                    diff = abs(val_calc - val_target)
                    dev = diff / abs(val_target) if val_target != 0 else diff

                    if dev <= MAX_ODCHYLKA:
                        # SPOČÍTAT SLOŽITOST (počet mezer + 1 = počet tokenů)
                        complexity = eq.count(' ') + 1
                        vysledky.append((float(dev), complexity, target, eq))

    # ŘAZENÍ: 1. Podle cílové proměnné (abecedně), 2. Podle odchylky (vzestupně)
    # Tím se seskupí všechny rovnice pro stejnou konstantu k sobě.
    vysledky.sort(key=lambda x: (x[2], x[0]))

    out_file = os.path.join(VYSTUPNI_SLOZKA, "vysledky_dim_check.txt")
    with open(out_file, 'w') as f:
        f.write(f"DIMENSIONALLY CORRECT EQUATIONS (dps={mp.dps})\n")
        f.write(f"Sorted by: Target Variable -> Lowest Error\n")
        f.write("-" * 120 + "\n")
        # Upravený výpis s Complexity/Len
        for dev, comp, tar, eq in vysledky:
            f.write(f"{dev:.3e} | Len: {comp:02d} | {tar:<10} | {eq}\n")

    print(f"Hotovo. Nalezeno {len(vysledky)} platných rovnic. Uloženo do {out_file}")

if __name__ == "__main__":
    zpracovat()