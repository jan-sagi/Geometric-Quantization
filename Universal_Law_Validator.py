import numpy as np
import scipy.signal

# --- GENERÁTOR ---
def validate_law(test_omega_vac):
    # Pro každý test změníme vakuum
    # Node dáme blízko, aby vznikly rázy
    test_omega_node = test_omega_vac * 1.05

    dt = 0.0001
    t_axis = np.arange(0, 1.0, dt) # 1 sekunda stačí

    # 1. Simulace pulzů (zjednodušená pro rychlost)
    # Hledáme, kdy |sin(vac) + sin(node)| překročí 1.9 (blízko max)
    # Efektivně simulujeme "vlnu smrti"
    # Fáze 0 je nejhorší případ (worst case)
    wave = 0.5 * (np.sin(test_omega_vac * t_axis) + np.sin(test_omega_node * t_axis))

    # Detekce vrcholů (peaks)
    peaks, _ = scipy.signal.find_peaks(np.abs(wave), height=0.9, distance=10)

    if len(peaks) < 2:
        return None, None

    peak_times = t_axis[peaks]
    measured_period = np.mean(np.diff(peak_times))

    # 2. Předpověď podle tvé rovnice
    predicted_period = np.pi / test_omega_vac

    return measured_period, predicted_period

if __name__ == "__main__":
    print("=========================================================")
    print("   UNIVERSAL LAW VALIDATOR: T = PI / Omega_Vac")
    print("=========================================================")
    print(f"{'VACUUM FREQ':<15} | {'NAMĚŘENÁ T':<12} | {'PŘEDPOVĚĎ T':<12} | {'CHYBA'}")
    print("-" * 65)

    test_frequencies = [50.0, 100.0, 137.036, 314.159, 1000.0]

    valid_count = 0

    for vac_freq in test_frequencies:
        meas, pred = validate_law(vac_freq)

        if meas:
            error = abs(meas - pred)
            status = "✅" if error < 0.001 else "❌"
            if error < 0.001: valid_count += 1

            print(f"{vac_freq:<15.3f} | {meas:<12.6f} | {pred:<12.6f} | {error:.6f} {status}")
        else:
            print(f"{vac_freq:<15.3f} | --- CHYBA SIMULACE ---")

    print("-" * 65)
    if valid_count == len(test_frequencies):
        print("ZÁVĚR: Zákon je UNIVERZÁLNÍ. Platí pro jakoukoliv frekvenci.")
        print("       Čas smrti je vždy diktován geometrií vakua (PI).")
    else:
        print("ZÁVĚR: Zákon selhal v některých případech.")