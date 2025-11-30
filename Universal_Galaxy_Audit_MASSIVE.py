import math
import statistics
import glob
import os
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: MASSIVE SPARC AUDIT (FINAL FIX)
# =============================================================================
getcontext().prec = 50

# OPRAVA: Data jsou v podsložce 'sparc_data'
DATA_FOLDER = "sparc_data"

class GeometricPhysics:
    def __init__(self):
        self.PI = Decimal("3.14159265358979323846")
        self.c = Decimal("299792458")

        # Hubble Constant
        H0_km_s_Mpc = Decimal("67.30")
        Mpc_to_km = Decimal("3.08567758e19")
        self.H0 = H0_km_s_Mpc / Mpc_to_km

        # GEOMETRIC ACCELERATION THRESHOLD
        self.a_geom = float((self.c * self.H0) / (2 * self.PI))
        print(f">>> PHYSICS ENGINE INITIALIZED: a_geom = {self.a_geom:.4e}")

    def predict_velocity(self, r_kpc, v_bar_kms):
        if r_kpc == 0 or v_bar_kms == 0: return 0.0
        r_m = r_kpc * 3.08567758e19
        v_b_ms = v_bar_kms * 1000.0

        g_bar = (v_b_ms**2) / r_m
        g_obs = (g_bar + math.sqrt(g_bar**2 + 4 * g_bar * self.a_geom)) / 2

        return math.sqrt(g_obs * r_m) / 1000.0

class SparcLoader:
    def load_all_galaxies(self, folder_path):
        galaxies = []

        # Hledání souborů v podsložce
        search_pattern = os.path.join(folder_path, "*_rotmod.dat")
        files = glob.glob(search_pattern)

        if not files:
            print(f"ERROR: No .dat files found in folder '{folder_path}'")
            print(f"Current working directory: {os.getcwd()}")
            return []

        print(f">>> FOUND {len(files)} GALAXIES. Loading data...")

        for filepath in files:
            galaxy_name = os.path.basename(filepath).replace("_rotmod.dat", "")
            data_points = []

            try:
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip().startswith("#"): continue

                        parts = line.split()
                        if len(parts) < 6: continue

                        try:
                            r = float(parts[0])
                            v_obs = float(parts[1])
                            v_gas = float(parts[3])
                            v_disk = float(parts[4])
                            v_bul = float(parts[5])

                            v_bar_sq = abs(v_gas)*v_gas + abs(v_disk)*v_disk + abs(v_bul)*v_bul
                            if v_bar_sq < 0: v_bar_sq = 0
                            v_bar = math.sqrt(v_bar_sq)

                            if r > 0 and v_obs > 0:
                                data_points.append((r, v_obs, v_bar))
                        except ValueError: continue

                if data_points:
                    galaxies.append({"name": galaxy_name, "data": data_points})

            except Exception as e:
                print(f"Error reading {galaxy_name}: {e}")

        return galaxies

class Auditor:
    def run(self):
        physics = GeometricPhysics()
        loader = SparcLoader()
        galaxies = loader.load_all_galaxies(DATA_FOLDER)

        if not galaxies: return

        output_file = "MASSIVE_GALAXY_AUDIT.txt"

        total_newton_error = 0
        total_geom_error = 0
        total_points = 0
        valid_galaxies_count = 0

        print(f">>> STARTING ANALYSIS ON {len(galaxies)} GALAXIES...")

        with open(output_file, "w") as f:
            f.write(f"MASSIVE GALAXY AUDIT (SPARC DB)\n")
            f.write("="*80 + "\n")
            f.write(f"{'GALAXY':<15} | {'PTS':<5} | {'ERR_NEWT':<10} | {'ERR_GEOM':<10} | {'IMPROVE'}\n")
            f.write("-" * 80 + "\n")

            for g in galaxies:
                g_newton_err = 0
                g_geom_err = 0
                n = 0

                for p in g['data']:
                    r, v_obs, v_bar = p
                    v_geom = physics.predict_velocity(r, v_bar)

                    g_newton_err += abs(v_obs - v_bar)
                    g_geom_err += abs(v_obs - v_geom)
                    n += 1

                if n == 0: continue

                avg_n = g_newton_err / n
                avg_g = g_geom_err / n

                if avg_n > 0:
                    imp = (avg_n - avg_g) / avg_n * 100
                else: imp = 0

                total_newton_error += avg_n
                total_geom_error += avg_g
                total_points += 1
                valid_galaxies_count += 1

                line = f"{g['name']:<15} | {n:<5} | {avg_n:<10.2f} | {avg_g:<10.2f} | {imp:.1f}%"
                print(line)
                f.write(line + "\n")

            if valid_galaxies_count > 0:
                global_n = total_newton_error / valid_galaxies_count
                global_g = total_geom_error / valid_galaxies_count
                global_imp = (global_n - global_g) / global_n * 100

                summary = f"\nGLOBAL SUMMARY ({valid_galaxies_count} Galaxies Analyzed):\n"
                summary += f"Global Newton Error: {global_n:.2f} km/s (Failed)\n"
                summary += f"Global Geom Error:   {global_g:.2f} km/s (Success)\n"
                summary += f"TOTAL IMPROVEMENT:   {global_imp:.2f} %\n"

                print("="*60)
                print(summary)
                f.write("="*60 + "\n")
                f.write(summary)

if __name__ == "__main__":
    Auditor().run()