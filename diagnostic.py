import math
import glob
import os
import sys

# =============================================================================
# KONFIGURACE A FYZIKA
# =============================================================================
DATA_FOLDER = "sparc_data"

class GeometricPhysics:
    def __init__(self):
        self.PI = 3.141592653589793
        self.c = 299792458.0
        H0_km_s_Mpc = 67.30
        Mpc_in_meters = 3.08567758e22
        self.H0_si = (H0_km_s_Mpc * 1000) / Mpc_in_meters
        # Tvůj práh
        self.a_geom = (self.c * self.H0_si) / (2 * self.PI)

def predict_velocity(self, r_kpc, v_bar_kms):
        if r_kpc <= 0 or v_bar_kms <= 0: return 0.0

        r_meters = r_kpc * 3.08567758e19
        v_bar_ms = v_bar_kms * 1000.0

        # 1. Newtonovské zrychlení (čistá hmota)
        g_newton = (v_bar_ms**2) / r_meters

        # 2. MECHANISMUS SATURACE (NOVÉ!)
        # Pokud je g_newton mnohem větší než a_geom, mřížka je "napnutá" a a_geom klesá k nule.
        # Použijeme "Topologický stínící faktor":
        # Pokud g_newton >> a_geom, pak effective_a_geom -> 0

        # Zkusíme jednoduchou "Simple Interpolation" funkci, která je ostřejší než ta původní:
        # g_obs = g_newton / (1 - sqrt(a_geom / g_newton)) ... to je složité na inverzi

        # Místo toho použijeme exponenciální tlumení tvé konstanty:
        # Čím silnější je gravitace, tím menší je vliv vakua.
        shielding = math.exp(-g_newton / (5 * self.a_geom))

        a_geom_effective = self.a_geom * shielding

        # 3. Původní výpočet, ale s efektivním a_geom
        g_geom = (g_newton + math.sqrt(g_newton**2 + 4 * g_newton * a_geom_effective)) / 2

        return math.sqrt(g_geom * r_meters) / 1000.0

# =============================================================================
# DIAGNOSTICKÝ ENGINE
# =============================================================================
class DiagnosticTool:
    def run(self):
        physics = GeometricPhysics()
        files = glob.glob(os.path.join(DATA_FOLDER, "*.dat"))
        if not files: files = glob.glob(os.path.join(DATA_FOLDER, "*_rotmod.dat"))

        results = []

        print(f">>> START DIAGNOSTIKY: Hledání korelací v {len(files)} galaxiích...")

        for filepath in files:
            galaxy_name = os.path.basename(filepath).split('_')[0]

            # Statistiky pro jednu galaxii
            sum_g_newton = 0 # Součet gravitačního zrychlení (pro průměr)
            points = 0

            err_newton_sq = 0
            err_geom_sq = 0

            try:
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.startswith("#"): continue
                        parts = line.split()
                        if len(parts) < 6: continue

                        try:
                            r = float(parts[0])
                            v_obs = float(parts[1])
                            v_gas = float(parts[3])
                            v_disk = float(parts[4])
                            v_bul = float(parts[5])

                            if r <= 0 or v_obs <= 0: continue

                            # Newton (Baryonová rychlost)
                            v_bar_sq = abs(v_gas)*v_gas + abs(v_disk)*v_disk + abs(v_bul)*v_bul
                            if v_bar_sq < 0: v_bar_sq = 0
                            v_bar = math.sqrt(v_bar_sq)

                            # Tvá predikce
                            v_geom = physics.predict_velocity(r, v_bar)

                            # Ukládáme sílu gravitačního pole (g = v^2 / r) v tomto bodě
                            # Převod na m/s^2 pro fyzikální smysl
                            r_m = r * 3.08567758e19
                            g_local = (v_bar * 1000)**2 / r_m
                            sum_g_newton += g_local
                            points += 1

                            err_newton_sq += (v_obs - v_bar)**2
                            err_geom_sq += (v_obs - v_geom)**2

                        except ValueError: continue

                if points > 0:
                    avg_g = sum_g_newton / points # Průměrná síla pole v galaxii
                    rmse_newton = math.sqrt(err_newton_sq / points)
                    rmse_geom = math.sqrt(err_geom_sq / points)

                    # Kdo vyhrál?
                    # Pokud je RMSE Geometrie menší než RMSE Newtona, vyhrála Geometrie.
                    winner = "GEOM" if rmse_geom < rmse_newton else "NEWTON"

                    # O kolik % se to liší?
                    if rmse_newton > 0:
                        diff_percent = (rmse_newton - rmse_geom) / rmse_newton * 100
                    else: diff_percent = 0

                    results.append({
                        'name': galaxy_name,
                        'avg_g': avg_g,            # Klíčový parametr: Jak silná je gravitace?
                        'rmse_newton': rmse_newton,
                        'rmse_geom': rmse_geom,
                        'winner': winner,
                        'diff': diff_percent
                    })

            except Exception: continue

        # =====================================================================
        # ANALÝZA VÝSLEDKŮ - ROZDĚLENÍ DO BINŮ (KATEGORIÍ)
        # =====================================================================

        # Seřadíme galaxie podle síly gravitace (od nejslabších "duchů" po nejhustší)
        results.sort(key=lambda x: x['avg_g'])

        # Rozdělíme na 3 třetiny (Low Surface Brightness, Medium, High Surface Brightness)
        chunk_size = len(results) // 3
        groups = [results[:chunk_size], results[chunk_size:2*chunk_size], results[2*chunk_size:]]
        labels = ["SLABÁ GRAVITACE (LSB)", "STŘEDNÍ GRAVITACE", "SILNÁ GRAVITACE (HSB)"]

        print("\n" + "="*80)
        print("VÝSLEDEK DIAGNOSTIKY: KDY TVÁ TEORIE FUNGUJE?")
        print("="*80)

        for i, group in enumerate(groups):
            if not group: continue

            wins_geom = sum(1 for g in group if g['winner'] == "GEOM")
            wins_newton = sum(1 for g in group if g['winner'] == "NEWTON")
            total = len(group)

            avg_g_in_group = sum(g['avg_g'] for g in group) / total

            print(f"\nKATEGORIE {i+1}: {labels[i]}")
            print(f"Průměrné zrychlení v galaxii: {avg_g_in_group:.2e} m/s^2")
            print(f"-> Geometrie vyhrála: {wins_geom}x ({wins_geom/total*100:.1f}%)")
            print(f"-> Newton vyhrál:     {wins_newton}x ({wins_newton/total*100:.1f}%)")

            # Výpis největšího propadáku v této skupině
            worst = min(group, key=lambda x: x['diff'])
            print(f"   Nejhorší selhání: {worst['name']} (Zhoršení o {worst['diff']:.1f}%)")
            if worst['diff'] < -50:
                print(f"   DŮVOD: Newton měl chybu jen {worst['rmse_newton']:.2f} km/s, ale ty jsi to 'přepálil'.")

        print("\n" + "="*80)
        print("ZÁVĚREČNÝ VERDIKT:")

        high_g_group = groups[2]
        high_g_failures = sum(1 for g in high_g_group if g['winner'] == "NEWTON")

        if high_g_failures > len(high_g_group) / 2:
            print("Tvá teorie systematicky selhává u galaxií se SILNOU gravitací.")
            print("Doporučení: Tvůj vzorec potřebuje 'stínící efekt'.")
            print("Když je zrychlení >> a_geom, musí se korekce vypnout rychleji, než to dělá teď.")
        else:
            print("Výsledky jsou smíšené. Chyba není přímo závislá na síle gravitace.")
            print("Může jít o vliv inklinace (sklonu galaxie vůči mřížce).")

if __name__ == "__main__":
    DiagnosticTool().run()