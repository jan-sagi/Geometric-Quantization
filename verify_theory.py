import math

def print_header(text):
    print("\n" + "="*70)
    print(f" {text.upper()}")
    print("="*70)

def check_value(name, calculated, reference, unit=""):
    """Pomocná funkce pro výpis a porovnání hodnot."""
    error_pct = abs((calculated - reference) / reference) * 100
    accuracy = 100 - error_pct

    print(f"--- {name} ---")
    print(f"  Calculated (Theory): {calculated:.6f} {unit}")
    print(f"  Reference (CODATA):  {reference:.6f} {unit}")
    print(f"  Deviation:           {error_pct:.6f} %")
    print(f"  Model Accuracy:      {accuracy:.6f} %")

    if accuracy > 99.9:
        print("  >> STATUS: EXCELLENT MATCH")
    elif accuracy > 99.0:
        print("  >> STATUS: GOOD MATCH")
    else:
        print("  >> STATUS: DIVERGENCE DETECTED")
    print("-" * 30)

# ---------------------------------------------------------
# CONSTANTS (CODATA 2018)
# ---------------------------------------------------------
PI = math.pi
ALPHA_INV_CODATA = 137.035999084
MU_CODATA = 1836.15267343

# ---------------------------------------------------------
# 1. ALPHA DERIVATION (Section 4.1)
# ---------------------------------------------------------
def verify_alpha():
    print_header("1. Geometric Origin of Alpha (Eq. 5)")
    print("Hypothesis: Alpha^-1 is the sum of dimensional expansion modes of PI.")
    print("Formula: 4*pi^3 + pi^2 + pi")

    # Calculation
    alpha_geom_inv = 4 * (PI**3) + (PI**2) + PI

    check_value("Inverse Fine-Structure Constant", alpha_geom_inv, ALPHA_INV_CODATA)

# ---------------------------------------------------------
# 2. PROTON-ELECTRON MASS RATIO (Section 4.2)
# ---------------------------------------------------------
def verify_mu():
    print_header("2. Matter Stability Ratio (Eq. 6)")
    print("Hypothesis: Proton is a stable knot with hexagonal symmetry (k=6) in 5D.")
    print("Formula: 6 * pi^5")

    # Calculation
    mu_geom = 6 * (PI**5)

    check_value("Proton/Electron Mass Ratio", mu_geom, MU_CODATA)

# ---------------------------------------------------------
# 3. LATTICE CAPACITY & DARK MATTER (Section 5)
# ---------------------------------------------------------
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def verify_dark_matter():
    print_header("3. Lattice Capacity & Dark Matter (Eq. 7)")

    # A. Derivation of k_max
    # Formula: k_max = floor(Alpha_inv / pi)

    alpha_geom_inv = 4 * (PI**3) + (PI**2) + PI # Consistency: use theoretical alpha
    k_ratio = alpha_geom_inv / PI
    k_max_calc = math.floor(k_ratio)
    k_max_rounded = round(k_ratio)

    print(f"Step A: Deriving Lattice Limit (k_max)")
    print(f"  Input Alpha_inv (Geom): {alpha_geom_inv:.4f}")
    print(f"  Ratio (Alpha^-1 / PI):  {k_ratio:.4f}")
    print(f"  Floor Value:            {k_max_calc}")
    print(f"  Rounded Value:          {k_max_rounded}")
    print(f"  >> Paper uses k_max approx 44 (based on rounding/boundary).")

    k_limit = 44

    # B. Mode Analysis (Prime vs Composite)
    print(f"\nStep B: Analyzing Modes up to k = {k_limit}")

    baryonic_modes = [] # Composites (Resonant)
    dark_modes = []     # Primes (Non-resonant)

    for k in range(1, k_limit + 1):
        if is_prime(k):
            dark_modes.append(k)
        else:
            baryonic_modes.append(k)

    # NOTE: The energy summation logic depends on the specific Hamiltonian of the lattice.
    # Here we demonstrate the partition of modes.

    print(f"  Total Modes: {k_limit}")
    print(f"  Resonant Nodes (Baryonic candidates):     {len(baryonic_modes)} nodes")
    print(f"  Non-Resonant Nodes (Dark Matter candidates): {len(dark_modes)} nodes")
    print(f"  Primes found: {dark_modes}")

    # Placeholder for the Ratio Calculation
    # (User needs to insert their specific energy summation function E(n) here)
    # Example hypothesis: If Energy ~ Sum of squares or similar
    print("\n  [!] To replicate the exact Ratio ~ 5.5, the specific energy weighting")
    print("      function E(n) from the full theory must be applied.")
    print("      (See full theory documentation for Hamiltonian details).")

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
if __name__ == "__main__":
    print("VERIFICATION SUITE: TOPOLOGICAL EINSTEIN REINTERPRETATION")
    print("Author: Jan Sagi, Nov 2025")

    verify_alpha()
    verify_mu()
    verify_dark_matter()

    print("\n" + "="*70)
    print(" END OF VERIFICATION")
    print("="*70)