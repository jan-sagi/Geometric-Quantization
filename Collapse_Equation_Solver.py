import numpy as np
import scipy.signal

# --- KONFIGURACE ---
OMEGA_VAC = 137.036
OMEGA_NODE = 145.000
A_CRIT = 0.95
DT = 0.0001           # Extrémní přesnost pro nalezení rovnice
MAX_TIME = 2.0

def get_collapse_bursts():
    """
    Simuluje a vrací přesné časy, kdy dochází k masovým rozpadům (peaks).
    """
    # Lineární fáze pro determinismus
    phases = np.linspace(0, 2*np.pi, 50000)

    # Časová osa
    t_axis = np.arange(0, MAX_TIME, DT)

    # Rychlá simulace: Počítáme jen kolik % fází překročí limit v čase t
    # Nemusíme sledovat jednotlivé částice, zajímá nás "globální vlna"
    burst_intensity = []

    print("Simuluji časovou osu a hledám pulzy...")
    for t in t_axis:
        # Tvá rovnice interference
        # Vytvoříme vlnu pro všechny fáze najednou
        wave = 0.5 * (np.sin(OMEGA_VAC * t) + np.sin(OMEGA_NODE * t + phases))

        # Kolik % překročilo práh?
        count = np.sum(np.abs(wave) >= A_CRIT)
        burst_intensity.append(count)

    burst_intensity = np.array(burst_intensity)

    # Najdeme vrcholy (peaks) - časy kdy rozpad kulminuje
    peaks, _ = scipy.signal.find_peaks(burst_intensity, height=np.max(burst_intensity)*0.1, distance=100)
    peak_times = t_axis[peaks]

    return peak_times

def brute_force_solver(observed_period):
    """
    Zkouší kombinovat konstanty, aby našel vzorec pro observed_period.
    """
    print(f"\n--- HLEDÁNÍ ROVNICE PRO PERIODU: {observed_period:.6f} s ---")

    # Konstanty k dispozici
    consts = {
        "PI": np.pi,
        "w_vac": OMEGA_VAC,
        "w_node": OMEGA_NODE,
        "w_sum": OMEGA_VAC + OMEGA_NODE,
        "w_diff": abs(OMEGA_VAC - OMEGA_NODE),
        "2_w_vac": 2 * OMEGA_VAC
    }

    # Hledáme vzorce typu: Numerator / Denominator
    # Numerator candidates: PI, 2*PI, 4*PI, 1
    numerators = {
        "1": 1.0,
        "PI": np.pi,
        "2*PI": 2 * np.pi,
        "4*PI": 4 * np.pi,
        "PI/2": np.pi / 2
    }

    best_match = None
    min_error = 1.0

    print(f"{'KANDIDÁT NA VZOREC':<40} | {'VÝSLEDEK':<12} | {'CHYBA'}")
    print("-" * 70)

    for n_name, n_val in numerators.items():
        for d_name, d_val in consts.items():
            # Test vzorce: T = n / d
            theoretical_val = n_val / d_val
            error = abs(theoretical_val - observed_period)

            if error < 0.01: # Tolerance
                print(f"{n_name} / {d_name:<30} | {theoretical_val:.6f} s | {error:.6f}")
                if error < min_error:
                    min_error = error
                    best_match = f"{n_name} / {d_name}"

    print("-" * 70)
    return best_match

if __name__ == "__main__":
    # 1. Získat data
    peak_times = get_collapse_bursts()

    if len(peak_times) < 2:
        print("Nedostatek pulzů pro určení periody.")
    else:
        # Vypočítáme průměrnou deltu mezi pulzy
        deltas = np.diff(peak_times)
        avg_period = np.mean(deltas)

        print(f"Nalezeno {len(peak_times)} pulzů.")
        print(f"První pulz v čase: {peak_times[0]:.6f} s")
        print(f"Průměrná perioda pulzů (Delta T): {avg_period:.6f} s")

        # 2. Najít rovnici
        equation = brute_force_solver(avg_period)

        print("\n=== VÍTĚZNÁ ROVNICE KOLAPSU ===")
        if equation:
            print(f"T_collapse = {equation}")
            print("Interpretace: Čas rozpadu je kvantován geometrií PI a frekvencí systému.")
        else:
            print("Žádná jednoduchá rovnice nenalezena. (Možná je to fraktální?)")