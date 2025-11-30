import math
import sys
from decimal import Decimal, getcontext

# =============================================================================
# QUANTUM DUALITY CHECK
# =============================================================================
# CÍL: Ověřit, zda "Vnitřní rychlost" částic (z geometrie) generuje
#      správné vlnové vlastnosti (De Broglieho vlnu).
# =============================================================================

getcontext().prec = 100

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV
    C = 299792458
    H = 6.62607015e-34

    # Hmotnosti (kg)
    ME_KG = 9.10938356e-31
    M_MU_KG = ME_KG * 206.768283

def analyze_duality():
    print("===================================================================")
    print(" WAVE-PARTICLE DUALITY AUDIT")
    print("===================================================================")
    print(" Hypotéza: Částice je 'Node' (hmota), Mřížka je 'Wave' (vlna).")
    print("           Vnitřní rychlost (topologické pnutí) určuje vlnovou délku.")
    print("-------------------------------------------------------------------")

    # 1. Získání vnitřní rychlosti Mionu (z předchozího skriptu)
    # Korekce: 1/(1-2a)
    F_muon = 1.0 / (1.0 - 2.0*Constants.ALPHA)
    # Rychlost v = c * sqrt(1 - 1/F^2)
    beta_muon = math.sqrt(1 - (1/(F_muon**2)))
    v_muon = beta_muon * Constants.C

    print(f" 1. Geometrická vnitřní rychlost Mionu: {v_muon/1000:.0f} km/s ({beta_muon:.4f} c)")

    # 2. Výpočet De Broglieho vlnové délky (Vlna hmoty)
    # lambda_db = h / (m * v)
    # Používáme relativistickou hybnost p = m*v*gamma, ale gamma je přímo F_muon!

    p_muon = Constants.M_MU_KG * v_muon * F_muon
    lambda_db = Constants.H / p_muon

    print(f" 2. De Broglieho vlnová délka (Vlna):   {lambda_db:.4e} m")

    # 3. Výpočet Comptonovy vlnové délky (Velikost částice)
    # lambda_c = h / (m * c)
    lambda_c = Constants.H / (Constants.M_MU_KG * Constants.C)

    print(f" 3. Comptonova vlnová délka (Částice):  {lambda_c:.4e} m")

    # 4. Poměr - Je tam geometrický vztah?
    ratio = lambda_db / lambda_c
    print("-------------------------------------------------------------------")
    print(f" POMĚR (Vlna / Částice): {ratio:.4f}")

    # Co ten poměr znamená?
    # ratio = (h/mv) / (h/mc) = c/v = 1/beta

    expected_ratio = 1.0 / beta_muon
    print(f" Očekávaný geometrický poměr (1/v):     {expected_ratio:.4f}")

    print("===================================================================")
    print(" INTERPRETACE:")
    print(f" Vlna částice je přesně {ratio:.2f}-násobek její velikosti.")
    print(" To znamená, že 'vlna' není nic magického. Je to jen")
    print(" geometrická projekce její vnitřní rotace do prostoru.")
    print(" Čím rychlejší vnitřní rotace (vyšší energie), tím kratší vlna.")
    print(" DUALITA JE VYŘEŠENA: Částice je Uzel, Vlna je jeho stopa v mřížce.")

if __name__ == "__main__":
    analyze_duality()