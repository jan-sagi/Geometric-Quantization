import math

def print_separator(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def calculate_percent_error(experimental, theoretical):
    return abs((theoretical - experimental) / experimental) * 100

# ==========================================
# 1. KONSTANTY (Reference Values - CODATA 2018)
# ==========================================
# Zdroj: NIST/CODATA 2018 (odpovídá tvé referenci [6])
ALPHA_INV_CODATA = 137.035999084  # Inverse fine-structure constant
MU_CODATA = 1836.15267343         # Proton-to-electron mass ratio
PI = math.pi

print_separator("INPUT DATA & CONSTANTS")
print(f"Použité PI: {PI:.15f}")
print(f"CODATA Alpha^-1: {ALPHA_INV_CODATA:.9f}")
print(f"CODATA Mu (mp/me): {MU_CODATA:.8f}")

# ==========================================
# 2. VERIFIKACE ROVNICE (5) - Alpha
# ==========================================
# Tvůj vzorec: 4*pi^3 + pi^2 + pi
alpha_geom_inv = 4 * (PI**3) + (PI**2) + PI

print_separator("VERIFIKACE SEKCE 4.1: GEOMETRIC ORIGIN OF ALPHA")
print(f"Vzorec: 4π^3 + π^2 + π")
print(f"Tvoje hodnota v papíru:  137.03630")
print(f"Vypočítaná hodnota:      {alpha_geom_inv:.5f}")

diff_alpha = alpha_geom_inv - ALPHA_INV_CODATA
error_alpha_percent = calculate_percent_error(ALPHA_INV_CODATA, alpha_geom_inv)

print(f"Rozdíl (Calc - CODATA):  {diff_alpha:.5f}")
print(f"Procentuální odchylka:   {error_alpha_percent:.6f} %")

# Kontrola tvého tvrzení v textu: "deviates by only approx 2 x 10^-4 %"
claimed_error = 2e-4
if error_alpha_percent <= claimed_error * 1.5: # Tolerance pro zaokrouhlení
    print(">> ZÁVĚR: Tvrzení o přesnosti (2e-4 %) je VALIDNÍ.")
else:
    print(f">> ZÁVĚR: Skutečná odchylka je {error_alpha_percent:.2e} %, zkontroluj text.")

# ==========================================
# 3. VERIFIKACE ROVNICE (6) - Mu (Matter Stability)
# ==========================================
# Tvůj vzorec: 6*pi^5
mu_geom = 6 * (PI**5)

print_separator("VERIFIKACE SEKCE 4.2: MATTER STABILITY (MU)")
print(f"Vzorec: 6π^5")
print(f"Tvoje hodnota v papíru:  1836.118")
print(f"Vypočítaná hodnota:      {mu_geom:.3f}")

error_mu_percent = calculate_percent_error(MU_CODATA, mu_geom)
accuracy_mu = 100 - error_mu_percent

print(f"CODATA hodnota:          {MU_CODATA:.3f}")
print(f"Procentuální odchylka:   {error_mu_percent:.4f} %")
print(f"Přesnost (Accuracy):     {accuracy_mu:.4f} %")

# Kontrola tvého tvrzení v textu: "within a 99.998% margin"
if accuracy_mu >= 99.998:
    print(">> ZÁVĚR: Tvrzení o přesnosti (99.998%) je VALIDNÍ.")
else:
    print(f">> POZOR: Vypočítaná přesnost je {accuracy_mu:.4f}%.")
    print("   Tvůj text tvrdí 99.998%, což je velmi blízko, ale stojí za kontrolu.")

# ==========================================
# 4. ROZMĚROVÁ KONZISTENCE (Eq 4)
# ==========================================
print_separator("VERIFIKACE ROVNICE (4): DIMENSIONAL CHECK")
# G_mu_nu = 8pi * l_eff * T_top
# [L^-2]  = [1] * [L]   * [L^-3]

dim_LHS = -2        # Curvature R ~ 1/L^2
dim_l_eff = 1       # Length
dim_rho_top = -3    # Density L^-3 (per Definition 1)

dim_RHS = dim_l_eff + dim_rho_top

print(f"Levá strana (Curvature) rozměr L^x, kde x = {dim_LHS}")
print(f"Pravá strana (l_eff * rho) rozměr L^x, kde x = {dim_l_eff} + ({dim_rho_top}) = {dim_RHS}")

if dim_LHS == dim_RHS:
    print(">> ZÁVĚR: Rozměrová analýza je KONZISTENTNÍ.")
else:
    print(">> CHYBA: Rozměry nesedí.")

print("\n")