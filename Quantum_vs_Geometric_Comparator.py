import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# --- KONFIGURACE ---
N_PARTICLES = 100000    # Zvyšujeme počet pro přesnější RMS
OMEGA_VAC = 137.036
OMEGA_NODE = 145.000
A_CRIT = 0.95
DT = 0.0005             # Jemnější krok pro zachycení detailů
MAX_TIME = 1.0

def geometric_simulation(n):
    # (Stejná simulace jako předtím, jen optimalizovaná)
    phases = np.random.uniform(0, 2*np.pi, n)
    decay_times = np.zeros(n)
    active = np.ones(n, dtype=bool)
    t = 0.0

    while t < MAX_TIME and np.any(active):
        # Rychlý vektorový výpočet
        strain = 0.5 * (np.sin(OMEGA_VAC * t) + np.sin(OMEGA_NODE * t + phases[active]))
        died_now = np.abs(strain) >= A_CRIT

        # Zápis časů
        idx_active = np.where(active)[0]
        idx_died = idx_active[died_now]
        decay_times[idx_died] = t
        active[idx_died] = False
        t += DT

    return decay_times[decay_times > 0] # Vracíme jen ty, co zemřely

def exp_fit(t, N0, lam):
    return N0 * np.exp(-lam * t)

# --- ANALÝZA ---
if __name__ == "__main__":
    print(f"--- SPUŠTĚNÍ RMS KVANTIZACE ---")
    print(f"Simuluji {N_PARTICLES} částic...")

    # 1. Generování dat
    data_geom = geometric_simulation(N_PARTICLES)

    # Histogram (Experimentální data z tvé teorie)
    counts, bins = np.histogram(data_geom, bins=200, range=(0, MAX_TIME))
    t_centers = (bins[:-1] + bins[1:]) / 2

    # 2. Fitování Exponenciály (Standardní QM model)
    # Snažíme se proložit "hladkou křivku" skrz tvá data
    popt, _ = curve_fit(exp_fit, t_centers, counts, p0=[N_PARTICLES/50, 5.0])
    model_qm = exp_fit(t_centers, *popt)

    # 3. Výpočet Odchylek (Residua)
    residuals = counts - model_qm

    # --- VÝPOČET RMS a STATISTIK ---

    # RMSE (Absolutní chyba v počtu částic)
    rmse = np.sqrt(np.mean(residuals**2))

    # Normalized RMSE (Chyba jako procento z průměrného počtu)
    # Toto nám řekne, jak velká je ta "chyba" relativně.
    mean_count = np.mean(counts)
    nrmse_percent = (rmse / mean_count) * 100

    # Max Deviation (Největší "výkyv" od teorie)
    max_dev = np.max(np.abs(residuals))

    print("\n--- VÝSLEDKY ANALÝZY ---")
    print(f"Celkový počet rozpadů: {len(data_geom)}")
    print(f"RMSE (Root Mean Square Error): {rmse:.4f}")
    print(f"NRMSE (Relativní odchylka):    {nrmse_percent:.2f} %")
    print(f"Maximální anomálie:            {max_dev:.0f} částic")

    # Interpretace pro tebe
    print("\n--- INTERPRETACE ---")
    if nrmse_percent < 1.0:
        print("-> Rozdíl je ZANEDBATELNÝ (< 1%).")
        print("   Tvá teorie produkuje téměř dokonalou exponenciálu.")
        print("   Závěr: Geometrický determinismus je nerozeznatelný od kvantové náhody.")
    else:
        print(f"-> Rozdíl je VÝZNAMNÝ ({nrmse_percent:.2f}%).")
        print("   Tvá teorie generuje strukturu (vlny), kterou QM nepředpovídá.")
        print("   Závěr: Máš v ruce experimentálně ověřitelný rozdíl!")

    # --- GRAF ---
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t_centers, counts, 'b.', label='Geometrická Data', alpha=0.3)
    plt.plot(t_centers, model_qm, 'r-', label='QM Exponenciála', linewidth=2)
    plt.ylabel("Počet rozpadů")
    plt.legend()
    plt.title(f"Fitování modelu (NRMSE = {nrmse_percent:.2f}%)")

    plt.subplot(2, 1, 2)
    plt.plot(t_centers, residuals, 'k-')
    plt.axhline(0, color='r', linestyle='--')
    plt.fill_between(t_centers, -rmse, rmse, color='yellow', alpha=0.3, label='RMS Pásmo')
    plt.ylabel("Residua (Rozdíl)")
    plt.xlabel("Čas")
    plt.legend()

    plt.tight_layout()
    plt.show()