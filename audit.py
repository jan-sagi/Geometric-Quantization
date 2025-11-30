import math
import glob
import os
import sys

# =============================================================================
# KONFIGURACE
# =============================================================================
# Název složky, kde máš uloženy .dat soubory
DATA_FOLDER = "sparc_data"

# =============================================================================
# 1. FYZIKÁLNÍ JÁDRO (Tvá Teorie)
# =============================================================================
class GeometricPhysics:
    def __init__(self):
        # Základní konstanty
        self.PI = 3.141592653589793
        self.c = 299792458.0  # Rychlost světla (m/s)

        # Hubbleova konstanta (dle tvého zadání 67.3 km/s/Mpc)
        H0_km_s_Mpc = 67.30

        # Převod H0 na SI jednotky (s^-1)
        # 1 Mpc = 3.08567758e22 m
        Mpc_in_meters = 3.08567758e22
        self.H0_si = (H0_km_s_Mpc * 1000) / Mpc_in_meters

        # VÝPOČET GEOMETRICKÉHO PRAHU ZRYCHLENÍ (Zákon II)
        # a_geom = (c * H0) / 2pi
        self.a_geom = (self.c * self.H0_si) / (2 * self.PI)

        print(f"\n>>> INICIALIZACE FYZIKY")
        print(f"    c      = {self.c:.2e} m/s")
        print(f"    H0     = {H0_km_s_Mpc} km/s/Mpc")
        print(f"    a_geom = {self.a_geom:.4e} m/s^2 (Tvůj práh tuhosti vakua)")
        print("-" * 60)

    def predict_velocity(self, r_kpc, v_bar_kms):
        """
        Vstup:
          r_kpc: Poloměr v kiloparsecích
          v_bar_kms: Baryonová rychlost (to co by platilo podle Newtona) v km/s
        Výstup:
          Predikovaná rychlost podle Geometrické teorie v km/s
        """
        if r_kpc <= 0 or v_bar_kms <= 0:
            return 0.0

        # 1. Převod na SI jednotky (metry, m/s)
        r_meters = r_kpc * 3.08567758e19
        v_bar_ms = v_bar_kms * 1000.0

        # 2. Newtonovské gravitační zrychlení (čistě z baryonové hmoty)
        # g = v^2 / r
        g_newton = (v_bar_ms**2) / r_meters

        # 3. Aplikace Zákona II: Modifikovaná odezva vakua
        # Tvůj vzorec: F = M * sqrt(a(a + a_geom))
        # V řeči zrychlení: g_newton = sqrt(g_obs * (g_obs + a_geom))
        # Musíme vyjádřit g_obs (kvadratická rovnice nebo tvůj inverzní vzorec)
        # Tvůj inverzní vzorec:
        g_geom = (g_newton + math.sqrt(g_newton**2 + 4 * g_newton * self.a_geom)) / 2

        # 4. Zpětný výpočet rychlosti z geometrického zrychlení
        # v = sqrt(g * r)
        v_geom_ms = math.sqrt(g_geom * r_meters)

        return v_geom_ms / 1000.0 # Návrat v km/s

# =============================================================================
# 2. NAČÍTÁNÍ DAT (SPARC formát)
# =============================================================================
class DataLoader:
    def load_galaxies(self, folder):
        galaxies = []
        # Hledáme všechny soubory končící na .dat
        search_path = os.path.join(folder, "*.dat")
        files = glob.glob(search_path)

        if not files:
            # Zkusíme hledat i specificky _rotmod.dat
            search_path = os.path.join(folder, "*_rotmod.dat")
            files = glob.glob(search_path)

        if not files:
            print(f"CHYBA: Ve složce '{folder}' nebyly nalezeny žádné soubory .dat!")
            print("Ujisti se, že jsi data nahrál do správné složky.")
            sys.exit()

        print(f">>> NALEZENO {len(files)} GALAXIÍ. Načítám data...")

        for filepath in files:
            galaxy_name = os.path.basename(filepath).split('_')[0]
            data_points = []

            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith("#"): continue # Přeskočit komentáře
                        parts = line.split()

                        # SPARC formát obvykle: Rad(kpc) Vobs Err Vgas Vdisk Vbul
                        if len(parts) < 6: continue

                        try:
                            r = float(parts[0])
                            v_obs = float(parts[1])
                            # Ignorujeme chybové rozpětí pro tento rychlý test
                            v_gas = float(parts[3])
                            v_disk = float(parts[4])
                            v_bul = float(parts[5])

                            # Vyloučení bodů, kde data chybí
                            if r <= 0 or v_obs <= 0: continue

                            # Výpočet celkové baryonové rychlosti (Newton)
                            # V_bar = sqrt(|V_gas|V_gas + |V_disk|V_disk + ...)
                            # Absolutní hodnota řeší případy negativních čtverců (vzácné, ale stává se v datech)
                            v_bar_sq = abs(v_gas)*v_gas + abs(v_disk)*v_disk + abs(v_bul)*v_bul
                            if v_bar_sq < 0: v_bar_sq = 0
                            v_bar = math.sqrt(v_bar_sq)

                            data_points.append({
                                'r': r,
                                'v_obs': v_obs,  # Realita
                                'v_newton': v_bar # Newton (bez temné hmoty)
                            })

                        except ValueError:
                            continue

                if data_points:
                    galaxies.append({'name': galaxy_name, 'data': data_points})

            except Exception as e:
                print(f"Chyba při čtení {galaxy_name}: {e}")

        return galaxies

# =============================================================================
# 3. AUDIT A VÝSTUP
# =============================================================================
def run_audit():
    physics = GeometricPhysics()
    loader = DataLoader()

    galaxies = loader.load_galaxies(DATA_FOLDER)

    if not galaxies: return

    print(f">>> START ANALÝZY NA {len(galaxies)} GALAXIÍCH")
    print("="*95)
    print(f"{'GALAXIE':<12} | {'BODY':<5} | {'CHYBA NEWTON':<15} | {'CHYBA TVÁ TEORIE':<18} | {'ZLEPŠENÍ'}")
    print("-" * 95)

    total_err_newton = 0
    total_err_geom = 0
    count = 0

    # Otevření souboru pro detailní zápis
    with open("VYSLEDEK_AUDITU.txt", "w", encoding="utf-8") as outfile:
        header = f"AUDIT GEOMETRICKÉ TEORIE - {len(galaxies)} GALAXIÍ\n" + "="*60 + "\n"
        outfile.write(header)

        for gal in galaxies:
            sum_err_sq_newton = 0
            sum_err_sq_geom = 0
            n = 0

            for p in gal['data']:
                r = p['r']
                v_obs = p['v_obs']
                v_bar = p['v_newton']

                # Výpočet podle tvé teorie
                v_geom = physics.predict_velocity(r, v_bar)

                # Výpočet kvadratické chyby
                sum_err_sq_newton += (v_obs - v_bar)**2
                sum_err_sq_geom += (v_obs - v_geom)**2
                n += 1

            if n == 0: continue

            # RMSE (Root Mean Square Error) - průměrná odchylka v km/s
            rmse_newton = math.sqrt(sum_err_sq_newton / n)
            rmse_geom = math.sqrt(sum_err_sq_geom / n)

            # Procentuální zlepšení
            if rmse_newton > 0:
                improve = (rmse_newton - rmse_geom) / rmse_newton * 100
            else:
                improve = 0

            # Výpis do konzole
            print(f"{gal['name']:<12} | {n:<5} | {rmse_newton:<15.2f} | {rmse_geom:<18.2f} | {improve:+.1f}%")

            # Zápis do souboru
            outfile.write(f"{gal['name']}: Newton Err={rmse_newton:.2f}, Geom Err={rmse_geom:.2f}, Zlepšení={improve:.1f}%\n")

            total_err_newton += rmse_newton
            total_err_geom += rmse_geom
            count += 1

        print("="*95)

        if count > 0:
            avg_newton = total_err_newton / count
            avg_geom = total_err_geom / count
            total_imp = (avg_newton - avg_geom) / avg_newton * 100

            summary = f"""
GLOBÁLNÍ VÝSLEDEK:
------------------
Průměrná odchylka (Klasický Newton):   {avg_newton:.2f} km/s
Průměrná odchylka (Tvá Teorie):        {avg_geom:.2f} km/s
CELKOVÉ ZLEPŠENÍ PŘESNOSTI:            {total_imp:.2f} %
"""
            print(summary)
            outfile.write(summary)
            print(f"Detailní výsledky byly uloženy do souboru 'VYSLEDEK_AUDITU.txt'.")

if __name__ == "__main__":
    run_audit()