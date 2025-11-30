import numpy as np
import matplotlib.pyplot as plt

# --- KONFIGURACE MODELU ---
# Hodnoty vycházející z tvého abstraktu
ALPHA_INV = 137.035999  # Fine structure constant inverse
OMEGA_VAC = ALPHA_INV   # Frekvence vakua
OMEGA_NODE = 17.0       # Tau-like node (k=17)
A_CRIT = 0.99           # "Alpha Wall" - práh kolapsu (blízko maxima 1.0)
DT = 0.0001             # Časový krok simulace (vysoká přesnost)
MAX_TIME = 2.0          # Maximální čas simulace

def simulate_particle(phi, omega_node, omega_vac, threshold, dt, max_time):
    """
    Simuluje jednu částici a vrací čas kolapsu.
    Rovnice: A(t) = 0.5 * (sin(w_node*t + phi) + sin(w_vac*t))
    """
    t = 0.0
    while t < max_time:
        # Výpočet okamžitého napětí mřížky
        # Používáme absolutní hodnotu, protože "breach" může být v + i - směru
        strain = 0.5 * (np.sin(omega_node * t + phi) + np.sin(omega_vac * t))

        if np.abs(strain) >= threshold:
            return t # Kolaps nastal
        t += dt

    return max_time # Částice přežila simulaci (stabilní nebo dlouhý život)

def run_causality_test():
    print("--- 1. TEST KAUZALITY (DETERMINISMUS) ---")
    phases_to_test = [0.0, 0.5, 1.0, 3.14]
    results = []

    print(f"{'Fáze (rad)':<15} | {'Čas rozpadu (s)':<15}")
    print("-" * 35)

    for phi in phases_to_test:
        decay_time = simulate_particle(phi, OMEGA_NODE, OMEGA_VAC, A_CRIT, DT, MAX_TIME)
        results.append((phi, decay_time))
        print(f"{phi:<15.4f} | {decay_time:<15.5f}")
    return results

def run_population_stats(n_particles=10000):
    print("\n--- 2. STATISTICKÁ EMERGENCE (POPULACE) ---")
    print(f"Simuluji {n_particles} částic s náhodnou fází 0 až 2pi...")

    # Generování náhodných fází
    random_phases = np.random.uniform(0, 2*np.pi, n_particles)
    decay_times = []

    for phi in random_phases:
        t_decay = simulate_particle(phi, OMEGA_NODE, OMEGA_VAC, A_CRIT, DT, MAX_TIME)
        decay_times.append(t_decay)

    decay_times = np.array(decay_times)

    # Analýza přežití
    time_axis = np.linspace(0, MAX_TIME, 100)
    survival_counts = []

    for t in time_axis:
        # Počet částic, které ještě nezkolabovaly před časem t
        alive = np.sum(decay_times > t)
        survival_counts.append(alive)

    return time_axis, survival_counts, decay_times

# --- SPUŠTĚNÍ ---
if __name__ == "__main__":
    # 1. Determinismus
    run_causality_test()

    # 2. Statistika
    t_axis, survival, all_times = run_population_stats()

    # Vykreslení výsledků
    plt.figure(figsize=(12, 6))

    # Graf přežití
    plt.subplot(1, 2, 1)
    plt.plot(t_axis, survival, label='Simulace (Deterministická)')

    # Pro porovnání proložíme teoretickou exponenciálu, která odpovídá středu dat
    # N(t) = N0 * e^(-lambda*t)
    # Odhadneme lambda z času, kdy zbývá 50% částic
    start_n = survival[0]
    half_n = start_n / 2
    # Najdeme index, kde je populace nejblíže polovině
    idx_half = (np.abs(np.array(survival) - half_n)).argmin()
    t_half = t_axis[idx_half] if t_axis[idx_half] > 0 else 0.1

    # Vypočítaná lambda pro porovnání
    if t_half > 0:
        decay_lambda = np.log(2) / t_half
        y_theoretical = start_n * np.exp(-decay_lambda * t_axis)
        plt.plot(t_axis, y_theoretical, 'r--', label=f'Teoretická Exponenciála (halflife={t_half:.3f}s)')

    plt.title("Křivka přežití (Survival Curve)")
    plt.xlabel("Čas (s)")
    plt.ylabel("Počet živých částic")
    plt.legend()
    plt.grid(True)

    # Histogram časů rozpadu
    plt.subplot(1, 2, 2)
    plt.hist(all_times, bins=50, color='skyblue', edgecolor='black', range=(0, MAX_TIME))
    plt.title("Rozdělení časů rozpadu")
    plt.xlabel("Čas rozpadu")
    plt.ylabel("Četnost")

    plt.tight_layout()
    plt.show()