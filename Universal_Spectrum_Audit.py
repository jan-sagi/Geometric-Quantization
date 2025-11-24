import math

# =============================================================================
# THE GEOMETRIC UNIVERSE: MULTI-ATOM SPECTRAL AUDIT (FIXED)
# =============================================================================

class Constants:
    # TVÉ AXIOMY
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV

    # FYZIKA
    C = 299792458
    H = 6.62607015e-34
    ME = 9.10938356e-31

    # GEOMETRICKÝ PROTON (Základní kámen hmoty)
    GEOM_PROTON_MASS = 6 * (PI**5) * ME

class Dataset:
    TARGETS = [
        {"name": "Hydrogen (H)",   "Z": 1, "A": 1, "nu": 3, "nl": 2, "real": 656.279},
        {"name": "Deuterium (D)",  "Z": 1, "A": 2, "nu": 3, "nl": 2, "real": 656.101},
        {"name": "Helium+ (He II)", "Z": 2, "A": 4, "nu": 4, "nl": 3, "real": 468.570},
        {"name": "Lithium+2 (Li III)", "Z": 3, "A": 7, "nu": 5, "nl": 4, "real": 449.913}
    ]

def run_audit():
    print(f"==================================================================================")
    print(f" UNIVERSAL SPECTRAL AUDIT (Isotope & Ion Test)")
    print(f" Hypothesis: Spectrum derives solely from Alpha (1/{Constants.ALPHA_INV:.3f}) and Pi.")
    print(f"==================================================================================")
    print(f" {'ELEMENT':<18} | {'TRANSITION':<8} | {'THEORY (nm)':<12} | {'NIST (nm)':<12} | {'ERROR':<10}")
    print(f"-" * 82)

    R_inf = (Constants.ALPHA**2 * Constants.ME * Constants.C) / (2 * Constants.H)
    RESET = "\033[0m"
    average_error = 0

    for atom in Dataset.TARGETS:
        Z = atom["Z"]
        A = atom["A"]
        ni = atom["nu"]
        nf = atom["nl"]

        # 1. Hmotnost jádra z geometrie
        mass_nucleus = A * Constants.GEOM_PROTON_MASS

        # 2. Redukovaná hmotnost
        reduced_mass_factor = mass_nucleus / (Constants.ME + mass_nucleus)

        # 3. Vlnová délka
        R_eff = R_inf * (Z**2) * reduced_mass_factor
        inv_lambda = R_eff * ((1.0/nf**2) - (1.0/ni**2))
        lambda_nm = (1.0 / inv_lambda) * 1e9

        # 4. Chyba
        error_abs = abs(lambda_nm - atom["real"])
        error_rel = (error_abs / atom["real"]) * 100
        average_error += error_rel

        # Barvy
        color = RESET
        if error_rel < 0.05: color = "\033[92m" # Zelená
        elif error_rel < 0.1: color = "\033[93m" # Žlutá
        else: color = "\033[91m" # Červená

        # ZDE BYLA CHYBA - NYNÍ OPRAVENO:
        print(f" {atom['name']:<18} | {ni}->{nf:<5} | {color}{lambda_nm:<12.4f}{RESET} | {atom['real']:<12.4f} | {color}{error_rel:.4f} %{RESET}")

    print(f"-" * 82)
    print(f" AVERAGE GEOMETRIC DEVIATION: {average_error / len(Dataset.TARGETS):.4f} %")
    print(f"==================================================================================")

if __name__ == "__main__":
    run_audit()