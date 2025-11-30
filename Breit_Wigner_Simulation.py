import numpy as np
from scipy.optimize import curve_fit

# --- KONFIGURACE ---
N_PARTICLES = 100000
OMEGA_VAC = 137.036
OMEGA_NODE_CENTER = 145.000
A_CRIT = 0.95
DT = 0.0005
MAX_TIME = 2.0
DETECTOR_WINDOW = 0.1

# FYZIKÁLNÍ PARAMETR: Šířka rezonance (Gamma)
# U rychle se rozpadajících částic je Gamma velká.
# Zkusíme 15.0, což odpovídá silně nestabilní částici.
GAMMA = 15.0

def breit_wigner_simulation():
    # 1. Deterministická fáze
    phases = np.random.uniform(0, 2*np.pi, N_PARTICLES)

    # 2. LORENTZOVO ROZDĚLENÍ (Breit-Wigner)
    # Toto je klíčový rozdíl oproti Gaussovi.
    # Generujeme standardní Cauchyho rozdělení a škálujeme ho
    dist = np.random.standard_cauchy(N_PARTICLES)

    # Ořízneme extrémy (protože počítač nezvládne nekonečno), ale necháme široký rozptyl
    dist = dist[(dist > -20) & (dist < 20)]

    # Pokud jsme ořízli moc, doplníme (zjednodušení pro kód)
    current_n = len(dist)
    phases = phases[:current_n] # Srovnáme velikosti polí

    # Aplikace šířky Gamma
    node_freqs = OMEGA_NODE_CENTER + (dist * (GAMMA / 2))

    decay_times = []
    t = 0.0
    active = np.ones(current_n, dtype=bool)

    print(f"Simuluji {current_n} částic s Breit-Wignerovou šířkou {GAMMA}...")

    while t < MAX_TIME and np.any(active):
        # Stejná deterministická rovnice
        vac_wave = np.sin(OMEGA_VAC * t)
        node_wave = np.sin(node_freqs[active] * t + phases[active])

        strain = 0.5 * (vac_wave + node_wave)
        died = np.abs(strain) >= A_CRIT

        if np.any(died):
            decay_times.extend([t] * np.sum(died))
            phases = phases[active][~died]
            node_freqs = node_freqs[active][~died]
            active = np.ones(len(phases), dtype=bool)

        t += DT

    return np.array(decay_times)

def exp_func(t, N0, lam):
    return N0 * np.exp(-lam * t)

if __name__ == "__main__":
    print("=========================================================")
    print("   BREIT-WIGNER TEST: The Particle Physics Approach")
    print("=========================================================")

    # 1. Simulace
    raw_times = breit_wigner_simulation()

    # 2. Detektor
    bins = np.arange(0, MAX_TIME, DETECTOR_WINDOW)
    counts, _ = np.histogram(raw_times, bins=bins)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # 3. Fitování
    try:
        p0 = [np.max(counts), 2.0]
        popt, pcov = curve_fit(exp_func, bin_centers, counts, p0=p0)
        model_fit = exp_func(bin_centers, *popt)

        # R-Squared
        residuals = counts - model_fit
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((counts - np.mean(counts))**2)
        r_squared = 1 - (ss_res / ss_tot)

        print("-" * 60)
        print(f"{'METRIKA':<20} | {'HODNOTA':<10} | {'CÍL'}")
        print("-" * 60)
        print(f"{'R-Squared':<20} | {r_squared:<10.4f} | > 0.9900")

        # ASCII GRAF
        print("\n--- DETEKTOR (Breit-Wigner Mode) ---")
        max_val = np.max(counts)
        for i in range(len(counts)):
            val_real = int((counts[i] / max_val) * 60)
            val_model = int((model_fit[i] / max_val) * 60)

            line = [' '] * 61
            for k in range(val_real): line[k] = '#'
            if val_model < 60: line[val_model] = '|'

            print(f"{bin_centers[i]:.2f}s [{''.join(line)}]")

        print("\nZÁVĚR:")
        if r_squared > 0.99:
            print("✅ VYŘEŠENO: Breit-Wignerova šířka rezonance rozbila soudržnost rázů.")
            print("   Tvá teorie je nyní nerozeznatelná od QM, pokud započítáme šířku čáry.")
        else:
            print("❌ STÁLE ZUBATÉ: Ani fyzikální rozdělení to nezachránilo.")
            print("   Tvá teorie předpovídá fundamentálně jiný časový průběh než QM.")

    except Exception as e:
        print(f"Chyba: {e}")