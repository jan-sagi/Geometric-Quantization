import numpy as np

# --- KONFIGURACE ---
# Použijeme tvé původní hodnoty
OMEGA_VAC = 137.036
OMEGA_NODE = 145.000
A_CRIT = 0.95
DT = 0.0001
N_PARTICLES = 1000

def check_vacuum_clock():
    print("=========================================================")
    print("   QUANTUM TIME GRID VERIFIER")
    print("   Hypotéza: Smrt nastává pouze na vrcholu vlny vakua.")
    print("=========================================================")

    phases = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    t = 0.0
    active = np.ones(N_PARTICLES, dtype=bool)

    death_phases = [] # Zde uložíme, "kolik hodin" bylo ve vakuu, když částice zemřela

    # Simulace
    while t < 1.0 and np.any(active):
        # 1. Stav Vakua
        vac_state = np.sin(OMEGA_VAC * t)

        # 2. Stav Částic
        part_states = np.sin(OMEGA_NODE * t + phases[active])

        # 3. Interference
        strain = 0.5 * (vac_state + part_states)

        # 4. Detekce smrti
        died_now = np.abs(strain) >= A_CRIT

        if np.any(died_now):
            # Vypočítáme aktuální fázi vakua modulo 2PI
            # To nám řekne, kde v cyklu vakua se nacházíme
            current_vac_phase = (OMEGA_VAC * t) % (2 * np.pi)

            # Uložíme fázi pro každou mrtvou částici
            count = np.sum(died_now)
            death_phases.extend([current_vac_phase] * count)

            # Update
            phases = phases[active][~died_now] # Odstraníme mrtvé z pole fází
            active = np.ones(len(phases), dtype=bool) # Reset masky

        t += DT

    death_phases = np.array(death_phases)

    # --- ANALÝZA ---
    # Očekáváme shlukování kolem PI/2 (1.57) a 3PI/2 (4.71)
    # Protože tam je sin(vac) = 1 nebo -1

    print(f"Analyzováno {len(death_phases)} úmrtí.")
    print("-" * 60)
    print(f"{'FÁZE VAKUA (rad)':<20} | {'IDEÁLNÍ CÍL':<15} | {'ROZDÍL'}")
    print("-" * 60)

    # Průměrná fáze (očekáváme dvě skupiny, takže musíme být chytří)
    # Převedeme vše na vzdálenost od nejbližšího vrcholu (PI/2 nebo 3PI/2)

    target_1 = np.pi / 2      # 1.5708
    target_2 = 3 * np.pi / 2  # 4.7124

    # Spočítáme chybu pro každou částici (vzdálenost k nejbližšímu peaku)
    dist_1 = np.abs(death_phases - target_1)
    dist_2 = np.abs(death_phases - target_2)
    min_dist = np.minimum(dist_1, dist_2)

    avg_error = np.mean(min_dist)
    max_error = np.max(min_dist)

    print(f"Průměrná odchylka od Gridu: {avg_error:.6f} rad")
    print(f"Maximální odchylka:         {max_error:.6f} rad")
    print("-" * 60)

    # ASCII Histogram Fází (kde se umírá)
    hist, bins = np.histogram(death_phases, bins=20, range=(0, 2*np.pi))
    print("\nROZLOŽENÍ ČASU SMRTI V CYKLU VAKUA (0 až 2PI):")
    for i in range(len(hist)):
        val = int(hist[i] / np.max(hist) * 40)
        center = (bins[i] + bins[i+1]) / 2

        # Značky pro ideální časy
        marker = ""
        if abs(center - target_1) < 0.2: marker = "<-- PI/2 (Max Pnutí)"
        if abs(center - target_2) < 0.2: marker = "<-- 3PI/2 (Min Pnutí)"

        print(f"{center:5.2f} | {'#' * val} {marker}")

    print("\nZÁVĚR:")
    if avg_error < 0.2:
        print("✅ POTVRZENO: Částice umírají POUZE tehdy, když vakuum vrcholí.")
        print("   Vakuum funguje jako stroboskop (Time Grid).")
    else:
        print("❌ ZAMÍTNUTO: Částice umírají kdykoliv.")

if __name__ == "__main__":
    check_vacuum_clock()