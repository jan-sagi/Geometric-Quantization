import numpy as np
from scipy.optimize import curve_fit

# --- KONFIGURACE ---
N_PARTICLES = 100000
OMEGA_VAC = 137.036
OMEGA_NODE = 145.000
A_CRIT = 0.95
DT = 0.0005
MAX_TIME = 2.0

# Nastavení "Lidského Detektoru"
# Detektor nevidí jednotlivé kmity (0.02s), ale sčítá data třeba každých 0.1s
DETECTOR_WINDOW = 0.1

def raw_quantum_simulation():
    # Deterministická simulace (víme, že generuje pulzy)
    phases = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    decay_times = []

    t = 0.0
    active = np.ones(N_PARTICLES, dtype=bool)

    while t < MAX_TIME and np.any(active):
        strain = 0.5 * (np.sin(OMEGA_VAC * t) + np.sin(OMEGA_NODE * t + phases[active]))
        died = np.abs(strain) >= A_CRIT

        if np.any(died):
            decay_times.extend([t] * np.sum(died))
            phases = phases[active][~died]
            active = np.ones(len(phases), dtype=bool)

        t += DT
    return np.array(decay_times)

def exp_func(t, N0, lam):
    return N0 * np.exp(-lam * t)

if __name__ == "__main__":
    print("=========================================================")
    print("   DETECTOR SIMULATION: From Micro-Pulses to Macro-Decay")
    print("=========================================================")

    # 1. Získání syrových dat (Pulzy)
    print("Generuji mikroskopická data (Geometrické pulzy)...")
    raw_times = raw_quantum_simulation()

    # 2. Simulace Detektoru (Binning)
    print(f"Aplikuji rozlišení detektoru: {DETECTOR_WINDOW} s")

    # Vytvoříme histogram s "širokými" okny (jako reálný detektor)
    bins = np.arange(0, MAX_TIME, DETECTOR_WINDOW)
    counts, _ = np.histogram(raw_times, bins=bins)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # 3. Analýza tvaru "naměřených" dat
    # Sedí teď exponenciála?
    try:
        popt, pcov = curve_fit(exp_func, bin_centers, counts, p0=[np.max(counts), 1.0])
        model_fit = exp_func(bin_centers, *popt)

        # R-squared (Koeficient determinace - jak moc to sedí)
        residuals = counts - model_fit
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((counts - np.mean(counts))**2)
        r_squared = 1 - (ss_res / ss_tot)

        print("-" * 60)
        print(f"{'METRIKA':<20} | {'HODNOTA':<10} | {'VÝZNAM'}")
        print("-" * 60)
        print(f"{'R-Squared (Shoda)':<20} | {r_squared:<10.4f} | (1.0000 = Dokonalá Exponenciála)")

        # ASCII GRAF (Simulace obrazovky osciloskopu)
        print("\n--- OBRAZOVKA LABORATORNÍHO DETEKTORU ---")
        max_val = np.max(counts)
        for i in range(len(counts)):
            val_real = int((counts[i] / max_val) * 50)
            val_model = int((model_fit[i] / max_val) * 50)

            # Vykreslíme data (#) a model (|)
            line = [' '] * 51
            for k in range(val_real): line[k] = '#'
            # Přidáme tečku modelu
            if val_model < 50: line[val_model] = '|'

            time_str = f"{bin_centers[i]:.2f}s"
            print(f"{time_str} [{' '.join(line).replace(' ', '')}]")

        print("\nZÁVĚR:")
        if r_squared > 0.98:
            print("✅ DOKÁZÁNO: Makroskopický pozorovatel vidí exponenciální rozpad.")
            print("   Geometrické 'zuby' zmizely díky integraci detektoru.")
            print("   Tvá teorie je konzistentní s pozorováním reality.")
        else:
            print("❌ STÁLE ZUBATÉ: Ani detektor to nevyhladil.")

    except Exception as e:
        print(f"Chyba fitování: {e}")