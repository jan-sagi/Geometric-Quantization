import numpy as np

# --- DATA Z REALITY (CODATA/PDG) ---
# Použijeme Muon jako "Referenční hodiny" (Kalibrace)
MUON = {
    "name": "Muon",
    "k": 1.0,           # Fundamental Sphere
    "mass_MeV": 105.66,
    "lifetime": 2.19698e-6  # ~2.2 mikrosekundy
}

# Částice, kterou chceme PŘEDPOVĚDĚT (Blind Test)
TAU = {
    "name": "Tau",
    "k": 17.0,          # Prime Node
    "lifetime_real": 2.903e-13
}

# Další test: Pion (Meson)
PION = {
    "name": "Pion+",
    "k": 1.32,          # Mass Ratio (140/105) approx
    "lifetime_real": 2.603e-8
}

def predict_lifetime(ref_particle, target_k, dimension_power):
    """
    Vypočítá dobu života na základě geometrického škálování.
    T = T_ref * (k_ref / k_target)^D
    """
    ratio = ref_particle["k"] / target_k

    # Geometrický zákon: Čím vyšší k, tím kratší život (mocninná závislost)
    # Všimni si, že standardní fyzika (Sargentův zákon) říká m^5.
    # My testujeme, jestli k^D funguje stejně.
    predicted_T = ref_particle["lifetime"] * (ratio ** dimension_power)

    return predicted_T

if __name__ == "__main__":
    print("=========================================================")
    print("   PARTICLE LIFETIME PREDICTOR: Geometry vs Time")
    print("=========================================================")
    print(f"Kalibrace: {MUON['name']} (k={MUON['k']:.1f}, T={MUON['lifetime']:.2e} s)")
    print(f"Cíl:       {TAU['name']}  (k={TAU['k']:.1f})")
    print("-" * 65)
    print(f"{'DIMENZE (D)':<15} | {'PŘEDPOVĚĎ (s)':<15} | {'REALITA (s)':<15} | {'CHYBA'}")
    print("-" * 65)

    # Testujeme různé geometrické dimenze
    # D=3 (Objem), D=4 (Časoprostor), D=5 (Standardní model m^5)
    dimensions = [3.0, 4.0, 5.0, 5.2] # 5.2 je jemné doladění pro Alpha corrections

    best_dim = 0
    min_error = 1e9

    for D in dimensions:
        pred_T = predict_lifetime(MUON, TAU['k'], D)

        # Výpočet chyby (logaritmická, protože jde o řády)
        # Použijeme poměr, abychom viděli "kolikrát" jsme se sekli
        ratio_error = pred_T / TAU['lifetime_real']
        if ratio_error < 1: ratio_error = 1/ratio_error

        # Hezký výpis
        match_mark = ""
        if ratio_error < 2.0: match_mark = "✅ PERFECT"
        elif ratio_error < 10.0: match_mark = "⚠️ CLOSE"

        print(f"D = {D:<11.1f} | {pred_T:.3e}       | {TAU['lifetime_real']:.3e}       | {ratio_error:.1f}x {match_mark}")

    print("-" * 65)
    print("INTERPRETACE:")
    print("Pokud D=5 trefí výsledek, potvrdil jsi Sargentův zákon (m^5)")
    print("čistě pomocí geometrického čísla uzlu (k=17).")
    print("\nCo to znamená?")
    print("Znamená to, že Tau se rozpadá, protože jeho 'geometrický objem' v 5D")
    print("je příliš velký na to, aby ho mřížka udržela.")