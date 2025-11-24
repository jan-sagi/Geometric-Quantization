import math
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: ATOMIC FAIR TEST (v1.0)
# =============================================================================
# OBJECTIVE: Impartial verification of Nuclear Binding Energy quantization.
# HYPOTHESIS: Binding Energy corresponds to integer multiples of Alpha.
# METHOD: No parameter tuning. Raw comparison of Data vs. Geometry.
# =============================================================================

# Precision settings
getcontext().prec = 100

def D(val):
    return Decimal(str(val))

class Constants:
    # 1. Fundamental Geometric Base (Zero Tuning)
    PI = D("3.14159265358979323846264338327950288419716939937510")
    ALPHA_INV = D("137.035999084")
    ALPHA = D(1) / ALPHA_INV

    # 2. Physical Constants (CODATA 2018)
    MEV_ELECTRON = D("0.51099895000")
    U_TO_MEV = D("931.49410242")

    # 3. Theoretical Proton (The Anchor)
    # Logic: Proton is Node k=6 on Baryon Scale (pi^5)
    PROTON_GEOM_MEV = (D(6) * (PI**5)) * MEV_ELECTRON

class Dataset:
    # Unbiased list of major stable isotopes (Z=1 to Z=92)
    # Data: Isotope Name, Nucleon Count (A), Atomic Mass (u) [Source: NIST]
    ISOTOPES = [
        ("H-1", 1, D("1.007825")),      # Hydrogen
        ("H-2", 2, D("2.014102")),      # Deuterium
        ("He-4", 4, D("4.002603")),     # Helium (Magic)
        ("Li-7", 7, D("7.016003")),     # Lithium
        ("Be-9", 9, D("9.012183")),     # Beryllium
        ("B-11", 11, D("11.009305")),   # Boron
        ("C-12", 12, D("12.000000")),   # Carbon (Standard)
        ("N-14", 14, D("14.003074")),   # Nitrogen
        ("O-16", 16, D("15.994915")),   # Oxygen (Magic)
        ("F-19", 19, D("18.998403")),   # Fluorine
        ("Ne-20", 20, D("19.992439")),  # Neon
        ("Na-23", 23, D("22.989769")),  # Sodium
        ("Mg-24", 24, D("23.985042")),  # Magnesium
        ("Al-27", 27, D("26.981538")),  # Aluminum
        ("Si-28", 28, D("27.976927")),  # Silicon
        ("P-31", 31, D("30.973761")),   # Phosphorus
        ("S-32", 32, D("31.972071")),   # Sulfur
        ("Ca-40", 40, D("39.962591")),  # Calcium (Magic)
        ("Fe-56", 56, D("55.934936")),  # Iron (Peak Stability)
        ("Ni-58", 58, D("57.935343")),  # Nickel
        ("Cu-63", 63, D("62.929601")),  # Copper
        ("Ag-107", 107, D("106.905097")), # Silver
        ("Au-197", 197, D("196.966569")), # Gold
        ("Pb-208", 208, D("207.976652")), # Lead (Magic)
        ("U-238", 238, D("238.050788"))   # Uranium
    ]

class Formatting:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def run_fair_test():
    print(f"{Formatting.BOLD}{'='*100}")
    print(f" THE ATOMIC FAIR TEST (Zero-Tuning)")
    print(f" Testing Hypothesis: Nuclear Binding Energy is quantized by Alpha.")
    print(f"{'='*100}{Formatting.RESET}")

    print(f" {'ISOTOPE':<8} | {'A':<4} | {'EXP MASS (MeV)':<16} | {'THEORY BASE':<16} | {'ALPHA RATIO':<12} | {'PER NUCLEON'}")
    print("-" * 100)

    total_deviation = 0
    count = 0

    # Quantum Unit of Binding Energy (Geometric Proton * Alpha)
    # This represents the electromagnetic coupling of one geometric node.
    UNIT_ALPHA_BINDING = Constants.PROTON_GEOM_MEV * Constants.ALPHA

    for name, A, mass_u in Dataset.ISOTOPES:
        # 1. Get Experimental Mass in MeV
        mass_exp = mass_u * Constants.U_TO_MEV

        # 2. Calculate Theoretical "Raw" Mass (Sum of Geometric Protons)
        # If nuclei were just loose protons with no binding energy:
        mass_theory = D(A) * Constants.PROTON_GEOM_MEV

        # 3. Calculate the Gap (Binding Energy + Neutron Mass Diff)
        gap = mass_theory - mass_exp

        # 4. Normalize the Gap by Alpha
        # This tells us: "How many Alpha-units of energy are missing?"
        alpha_ratio = gap / UNIT_ALPHA_BINDING

        # 5. Per Nucleon Efficiency
        # ideally, this should be close to 1.0 for stable matter
        efficiency = alpha_ratio / D(A)

        # Color Coding based on "Integer Proximity"
        # We look if the efficiency is close to 1.0 (perfect Alpha resonance)
        eff_float = float(efficiency)

        color = Formatting.RESET
        if abs(eff_float - 1.0) < 0.02: color = Formatting.GREEN # Extremely close to 1.0 alpha/nucleon
        elif abs(eff_float - 1.0) < 0.05: color = Formatting.YELLOW

        print(f" {color}{name:<8} | {A:<4} | {float(mass_exp):<16.3f} | {float(mass_theory):<16.3f} | {float(alpha_ratio):<12.3f} | {eff_float:.4f} α{Formatting.RESET}")

        if A > 1: # Skip Hydrogen-1 (no binding)
            count += 1

    print("-" * 100)
    print(f"{Formatting.BOLD} INTERPRETATION OF RESULTS:{Formatting.RESET}")
    print(" 1. 'THEORY BASE' is calculated purely as: A * (6 * pi^5 * me)")
    print(" 2. 'ALPHA RATIO' shows the Binding Gap divided by (Proton_Geom * Alpha).")
    print(" 3. 'PER NUCLEON' is the key metric. If specific geometry rules the nucleus,")
    print("    this value should converge to exactly 1.0000 or simple harmonics.")
    print("-" * 100)
    print(f" {Formatting.GREEN}GREEN{Formatting.RESET} = Binding Energy is within 2% of perfect Alpha Resonance.")
    print(f" {Formatting.YELLOW}YELLOW{Formatting.RESET} = Binding Energy is within 5% of perfect Alpha Resonance.")
    print("=" * 100)

if __name__ == "__main__":
    run_fair_test()