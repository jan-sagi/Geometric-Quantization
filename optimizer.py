import math
import glob
import os
import sys

# =============================================================================
# KONFIGURACE
# =============================================================================
DATA_FOLDER = "sparc_data"

class PhysicsEngine:
    def __init__(self, a_geom_candidate):
        self.a_geom = a_geom_candidate

    def predict_velocity(self, r_meters, v_bar_ms):
        if r_meters <= 0 or v_bar_ms <= 0: return 0.0

        # 1. Newtonovské zrychlení
        g_newton = (v_bar_ms**2) / r_meters

        # 2. MECHANISMUS SATURACE (Ten, co nám zafungoval)
        # Použijeme stejný 'shielding' jako v minulém kroku
        shielding = math.exp(-g_newton / (5 * self.a_geom))
        a_geom_effective = self.a_geom * shielding

        # 3. Geometrická korekce
        g_geom = (g_newton + math.sqrt(g_newton**2 + 4 * g_newton * a_geom_effective)) / 2

        return math.sqrt(g_geom * r_meters)

# =============================================================================
# OPTIMALIZÁTOR
# =============================================================================
class Optimizer:
    def run(self):
        # Načteme data do paměti jen jednou, ať je to rychlé
        files = glob.glob(os.path.join(DATA_FOLDER, "*_rotmod.dat"))
        if not files: files = glob.glob(os.path.join(DATA_FOLDER, "*.dat"))

        all_galaxies = []
        print(f">>> NAČÍTÁM DATA Z {len(files)} GALAXIÍ...")

        for filepath in files:
            gal_data = []
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith("#"): continue
                        parts = line.split()
                        if len(parts) < 6: continue
                        try:
                            r = float(parts[0]) * 3.08567758e19 # rovnou na metry
                            v_obs = float(parts[1]) * 1000.0    # rovnou na m/s

                            v_gas = float(parts[3])
                            v_disk = float(parts[4])
                            v_bul = float(parts[5])
                            v_bar_sq = abs(v_gas)*v_gas + abs(v_disk)*v_disk + abs(v_bul)*v_bul
                            if v_bar_sq < 0: v_bar_sq = 0
                            v_bar = math.sqrt(v_bar_sq) * 1000.0 # rovnou na m/s

                            if r > 0 and v_obs > 0:
                                gal_data.append((r, v_obs, v_bar))
                        except ValueError: continue
                if gal_data:
                    all_galaxies.append(gal_data)
            except: continue

        print(f">>> DATA NAČTENA. SPUŠTĚNÍ OPTIMALIZACE KONSTANTY a_geom...")
        print("-" * 60)

        # FYZIKÁLNÍ KONSTANTY PRO REFERENCI
        PI = 3.141592653589793
        c = 299792458.0
        H0_si = (67.30 * 1000) / 3.08567758e22 # cca 2.18e-18

        # Tvůj původní odhad (z kruhu)
        a_target = (c * H0_si) / (2 * PI) # cca 1.04e-10

        print(f"Referenční hodnota (Teoretická): {a_target:.4e}")

        # Budeme hledat v rozmezí 0.5x až 2.0x kolem tvé hodnoty
        best_error = float('inf')
        best_a = 0

        # Test 100 hodnot
        steps = 100
        start_val = a_target * 0.5
        end_val = a_target * 2.0
        step_size = (end_val - start_val) / steps

        print(f"{'TESTOVANÁ HODNOTA (a_geom)':<30} | {'PRŮMĚRNÁ CHYBA (m/s)':<20}")
        print("-" * 60)

        for i in range(steps):
            current_a = start_val + i * step_size

            physics = PhysicsEngine(current_a)
            total_sq_error = 0
            total_points = 0

            for gal in all_galaxies:
                for r, v_obs, v_bar in gal:
                    v_pred = physics.predict_velocity(r, v_bar)
                    total_sq_error += (v_obs - v_pred)**2
                    total_points += 1

            if total_points == 0: continue

            rmse = math.sqrt(total_sq_error / total_points)

            # Jen pro info vypisujeme každou 10. hodnotu
            if i % 10 == 0:
                print(f"{current_a:.4e}                     | {rmse:.4f}")

            if rmse < best_error:
                best_error = rmse
                best_a = current_a

        print("-" * 60)
        print(f"NEJLEPŠÍ NALEZENÁ HODNOTA a_geom: {best_a:.5e}")
        print(f"MINIMÁLNÍ CHYBA (RMSE):           {best_error:.4f} m/s")
        print("-" * 60)

        # FINÁLNÍ ANALÝZA: ČEMU TO ODPOVÍDÁ?
        ratio_2pi = (c * H0_si) / best_a
        print(f"\nINTERPRETACE VÝSLEDKU:")
        print(f"Pokud a_geom = c * H0 / X, pak X = {ratio_2pi:.4f}")
        print(f"Tvoje teorie předpovídala X = 2*pi = {2*PI:.4f}")
        print(f"Hodnota pro hexagony (X=6):          6.0000")

        diff = abs(ratio_2pi - 2*PI)
        if diff < 0.2:
            print(">>> SHODA! Tvůj odhad 2pi byl téměř přesný.")
        elif abs(ratio_2pi - 6.0) < 0.2:
            print(">>> FASCINUJÍCÍ! Data preferují X=6 (HEXAGON) před 2pi (KRUH).")
        else:
            print(">>> ZÁHADA. Data ukazují na jinou geometrickou konstantu.")

if __name__ == "__main__":
    Optimizer().run()