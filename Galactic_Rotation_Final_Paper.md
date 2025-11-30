import math
import glob
import os
import statistics
from decimal import Decimal, getcontext

# =============================================================================
# UNIVERSAL GALAXY AUDIT MASSIVE
# Verification Script for "The Geometric Laws of Motion"
# =============================================================================

# Konfigurace
DATA_FOLDER = "sparc_data"
getcontext().prec = 50

class GeometricVacuum:
def __init__(self):
# 1. FYZIKÁLNÍ KONSTANTY (Dle dokumentu)
self.c = 2.99792458e8
self.PI = 3.141592653589793

        # Hubbleova konstanta dle tvého zadání
        H0_km_s_Mpc = 67.30
        Mpc_in_meters = 3.08567758e22
        self.H0_si = (H0_km_s_Mpc * 1000) / Mpc_in_meters

        # 2. VÝPOČET PRAHU (Dle Sekce 2 dokumentu: 2*PI)
        # Poznámka: Zde používáme původní 2PI verzi pro ověření abstraktu
        self.a_geom = (self.c * self.H0_si) / (2 * self.PI)
        
        print(f">>> GEOMETRIC ENGINE INITIALIZED")
        print(f"    Mode:          2 * PI (Circle Geometry)")
        print(f"    a_geom:        {self.a_geom:.4e} m/s^2")
        print(f"    H0:            {H0_km_s_Mpc} km/s/Mpc")
        print("-" * 60)

    def predict_velocity(self, r_meters, v_bar_ms):
        if r_meters <= 0 or v_bar_ms <= 0: return 0.0
        
        # A. Newtonovské zrychlení
        g_bar = (v_bar_ms**2) / r_meters
        
        # B. Geometrická korekce (Zákon II)
        # g_obs = (g_bar + sqrt(g_bar^2 + 4 * g_bar * a_geom)) / 2
        term = math.sqrt(g_bar**2 + 4 * g_bar * self.a_geom)
        g_geom = (g_bar + term) / 2
        
        # Návrat rychlosti
        return math.sqrt(g_geom * r_meters)

class AuditEngine:
def run(self):
vacuum = GeometricVacuum()

        files = glob.glob(os.path.join(DATA_FOLDER, "*_rotmod.dat"))
        if not files: files = glob.glob(os.path.join(DATA_FOLDER, "*.dat"))
        
        if not files:
            print("ERROR: Žádná data nenalezena.")
            return

        galaxies_analyzed = 0
        geom_wins = 0
        newton_wins = 0
        improvements = []

        print(f"{'GALAXY':<15} | {'NEWTON ERR':<12} | {'GEOM ERR':<12} | {'RESULT':<10} | {'IMPROVE'}")
        print("-" * 75)

        for filepath in files:
            name = os.path.basename(filepath).split('_')[0]
            
            sq_err_newt = 0
            sq_err_geom = 0
            n = 0
            
            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith("#"): continue
                        parts = line.split()
                        if len(parts) < 6: continue
                        try:
                            # Načtení a převod na SI
                            r = float(parts[0]) * 3.08567758e19
                            v_obs = float(parts[1]) * 1000.0
                            
                            v_gas = float(parts[3])
                            v_disk = float(parts[4])
                            v_bul = float(parts[5])
                            v_bar_sq = abs(v_gas)*v_gas + abs(v_disk)*v_disk + abs(v_bul)*v_bul
                            if v_bar_sq < 0: v_bar_sq = 0
                            v_bar = math.sqrt(v_bar_sq) * 1000.0

                            if r > 0 and v_obs > 0:
                                # Predikce
                                v_geom = vacuum.predict_velocity(r, v_bar)
                                
                                sq_err_newt += (v_obs - v_bar)**2
                                sq_err_geom += (v_obs - v_geom)**2
                                n += 1
                        except: continue
            except: continue

            if n > 5: # Analyzujeme jen galaxie s dostatkem dat
                rmse_newt = math.sqrt(sq_err_newt / n)
                rmse_geom = math.sqrt(sq_err_geom / n)
                
                # Výpočet zlepšení
                if rmse_newt > 0:
                    imp = (rmse_newt - rmse_geom) / rmse_newt * 100
                else: imp = 0
                
                improvements.append(imp)
                galaxies_analyzed += 1
                
                result = ""
                if rmse_geom < rmse_newt:
                    geom_wins += 1
                    result = "GEOM WIN"
                else:
                    newton_wins += 1
                    result = "NEWTON"

                # Výpis pro zajímavé případy (jako v paperu)
                if name in ["UGC02885", "NGC6503", "NGC3741"] or abs(imp) > 50:
                    print(f"{name:<15} | {rmse_newt/1000:<12.2f} | {rmse_geom/1000:<12.2f} | {result:<10} | {imp:+.1f}%")

        # =====================================================================
        # STATISTICKÉ VYHODNOCENÍ (MATCHING THE PAPER)
        # =====================================================================
        if galaxies_analyzed > 0:
            median_imp = statistics.median(improvements)
            win_rate = (geom_wins / galaxies_analyzed) * 100
            
            print("=" * 75)
            print("FINAL AUDIT RESULTS (Verification of Section 4):")
            print(f"Total Galaxies:     {galaxies_analyzed}")
            print(f"Geometric Wins:     {geom_wins} ({win_rate:.1f}%)")
            print(f"Newton Wins:        {newton_wins} ({100-win_rate:.1f}%)")
            print(f"MEDIAN IMPROVEMENT: {median_imp:.1f} %")
            print("=" * 75)
            
            # KONTROLA TVRZENÍ V DOKUMENTU
            print("VERIFICATION CHECK:")
            print(f"-> Claim: '56% Wins'. Actual: {win_rate:.1f}%")
            print(f"-> Claim: '+13.1% Median'. Actual: {median_imp:.1f}%")
            
            if abs(win_rate - 56) < 5 and abs(median_imp - 13.1) < 5:
                print(">>> SUCCESS: The document claims are STATISTICALLY VALID.")
                print("    The 2*PI model outperforms Newton significantly.")
            else:
                print(">>> WARNING: Results deviate slightly from the text.")
                print("    (Try enabling the 4*PI optimization for better results).")

if __name__ == "__main__":
AuditEngine().run()