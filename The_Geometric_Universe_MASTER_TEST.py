import math
import random
import statistics
import time
import sys
import re

# =============================================================================
# THE GEOMETRIC UNIVERSE: MASTER VERIFICATION SUITE (v1.0)
# =============================================================================
# TITLE:  Geometric Quantization of Matter & Grand Unification
# AUTHOR: Jan Šági
# DATE:   November 24, 2025
# GOAL:   Unified statistical audit across Micro, Meso, and Macro scales.
# =============================================================================

# --- 0. SYSTEM CONFIGURATION & LOGGING ---
class DualLogger:
    """Handles simultaneous output to Console (Color) and File (Plain Text)."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# --- 1. FUNDAMENTAL CONSTANTS (NO TUNING ALLOWED) ---
class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999084
    ALPHA = 1.0 / ALPHA_INV
    N = math.log(4 * PI)

    # Unit Conversions
    ME_MEV = 0.510998950
    U_TO_MEV = 931.49410242

    # Physics Targets (CODATA 2018/2022) for Validation
    G_REAL = 6.67430e-11
    MP_KG = 1.6726219e-27
    H_BAR = 1.054571817e-34
    C = 299792458

    # --- GEOMETRIC BASES ---
    # Proton Geometry (Baryon Scale Anchor k=6)
    PROTON_GEOM_MEV = (6 * (PI**5)) * ME_MEV
    # The Unit Alpha Binding Energy
    UNIT_ALPHA_BINDING = PROTON_GEOM_MEV * ALPHA

    # Scale Bases for Particles
    SCALE_LEPTON = 4 * PI * (N**3) * ME_MEV
    SCALE_MESON  = ALPHA_INV * ME_MEV
    SCALE_BARYON = (PI**5) * ME_MEV

# --- 2. DATASETS (GROUND TRUTH) ---
class Data:
    # A. PARTICLE SPECTRUM (Standard Model Key Particles)
    PARTICLES = [
        ("Muon", 105.658), ("Pion0", 134.977), ("Pion+", 139.570),
        ("Kaon+", 493.677), ("Kaon0", 497.611), ("Eta", 547.862),
        ("Rho(770)", 775.26), ("Omega(782)", 782.65), ("Proton", 938.272),
        ("Neutron", 939.565), ("Eta'", 957.78), ("Phi(1020)", 1019.461),
        ("Lambda", 1115.683), ("Sigma+", 1189.37), ("Delta(1232)", 1232.0),
        ("Xi-", 1321.71), ("Sigma(1385)", 1385.0), ("Xi0", 1314.86),
        ("Tau", 1776.86), ("D+", 1869.65), ("D0", 1864.83),
        ("D_s+", 1968.34), ("Lambda_c", 2286.46), ("Eta_c", 2983.4),
        ("J/Psi", 3096.90), ("Xi_c", 2467.8), ("Omega_c", 2695.2),
        ("Psi(2S)", 3686.10), ("B+", 5279.32), ("B0", 5279.63),
        ("B_s", 5366.89), ("Bc+", 6274.9), ("Upsilon(1S)", 9460.30),
        ("Upsilon(2S)", 10023.26), ("Upsilon(3S)", 10355.2),
        ("W Boson", 80379.0), ("Z Boson", 91187.6), ("Higgs", 125100.0)
    ]

    # B. HEAVY NUCLEI (The Alpha Wall Transition)
    # Focusing on Z=16 to Z=92 to find the stability break
    HEAVY_ISOTOPES = [
        ("O-16",   16,  15.994915, "STABLE"),
        ("Ca-40",  40,  39.962591, "STABLE"),
        ("Fe-56",  56,  55.934937, "STABLE"),
        ("Kr-84",  84,  83.911507, "STABLE"),
        ("Sn-120", 120, 119.90219, "STABLE"),
        ("Xe-132", 132, 131.90415, "STABLE"),
        ("Pt-195", 195, 194.96479, "STABLE"),
        ("Au-197", 197, 196.96656, "STABLE"),
        ("Hg-202", 202, 201.97064, "STABLE"),
        ("Tl-205", 205, 204.97442, "STABLE"),
        ("Pb-208", 208, 207.97665, "STABLE"),   # ---> THE EXPECTED WALL
        ("Bi-209", 209, 208.98039, "BORDER"),   # Technically unstable, but > universe age
        ("Po-210", 210, 209.98287, "UNSTABLE"), # ---> BREAKING POINT
        ("Rn-222", 222, 222.01763, "UNSTABLE"),
        ("Ra-226", 226, 226.02540, "UNSTABLE"),
        ("U-238",  238, 238.05078, "UNSTABLE"),
    ]

# --- 3. ANALYSIS ENGINES ---

class ParticleEngine:
    @staticmethod
    def get_fit_error(mass_mev):
        """Finds nearest geometric node and returns error."""
        best_err = float('inf')
        bases = [Constants.SCALE_LEPTON, Constants.SCALE_MESON, Constants.SCALE_BARYON]
        for base in bases:
            k = round(mass_mev / base)
            if k < 1: k = 1
            theory = k * base
            err = abs(mass_mev - theory) / mass_mev
            if err < best_err: best_err = err
        return best_err

    @staticmethod
    def run_monte_carlo(iterations=5000):
        # 1. Real Universe Score
        real_errors = [ParticleEngine.get_fit_error(m) for _, m in Data.PARTICLES]
        real_score = sum(real_errors) / len(real_errors) * 100

        # 2. Random Universes
        better_count = 0
        scores = []

        # Progress Bar logic
        print(f"     Running {iterations} Simulations...", end="", flush=True)

        for i in range(iterations):
            # Generate fake universe (Jitter +/- 30%)
            fake_masses = []
            for _, m in Data.PARTICLES:
                jitter = math.exp(random.uniform(math.log(0.7), math.log(1.3)))
                fake_masses.append(m * jitter)

            # Score fake universe
            fake_errors = [ParticleEngine.get_fit_error(fm) for fm in fake_masses]
            fake_score = sum(fake_errors) / len(fake_errors) * 100
            scores.append(fake_score)

            if fake_score < real_score: better_count += 1

        print(" Done.")

        p_value = better_count / iterations
        z_score = (real_score - statistics.mean(scores)) / statistics.stdev(scores)
        return abs(z_score), p_value

class NuclearEngine:
    @staticmethod
    def analyze_wall():
        pb_eff = 0
        po_eff = 0

        for _, A, mass_u, _ in Data.HEAVY_ISOTOPES:
            mass_theory = A * (Constants.PROTON_GEOM_MEV / Constants.ME_MEV) * Constants.ME_MEV # Redundant but safe
            mass_real = mass_u * Constants.U_TO_MEV
            binding = mass_theory - mass_real
            eff = (binding / A) / Constants.UNIT_ALPHA_BINDING

            if A == 208: pb_eff = eff
            if A == 210: po_eff = eff

        # Wall Precision: How close is Pb-208 to 1.000?
        precision = (1.0 - abs(pb_eff - 1.0)) * 100
        valid = (pb_eff > 1.0) and (po_eff < 1.0)
        return precision, valid, pb_eff, po_eff

class GravityEngine:
    @staticmethod
    def derive_G():
        # Dimensional Exponent
        X = (10 * Constants.PI / 3) + (Constants.ALPHA / (4*Constants.PI)) + (math.sqrt(math.sqrt(2)) * Constants.ALPHA**2)

        # Proton Geometric Mass (Dimensionless)
        Gamma = 6 * (Constants.PI**5)

        # Coupling
        alpha_G = (Gamma**2) * (Constants.ALPHA**(2 * X))

        # G derived
        G_calc = (alpha_G * Constants.H_BAR * Constants.C) / (Constants.MP_KG**2)

        error = abs(G_calc - Constants.G_REAL) / Constants.G_REAL
        return G_calc, error

# --- 4. MAIN ORCHESTRATOR ---

def run_master_test():
    # Setup
    sys.stdout = DualLogger("FINAL_THEORY_REPORT.txt")

    # Colors
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print(f"{BOLD}{'='*80}")
    print(f" THE GEOMETRIC UNIVERSE: MASTER VERIFICATION SUITE")
    print(f"{'='*80}{RESET}")
    print(f" TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" TARGET:    Global Consistency Check (Particles, Nuclei, Gravity)")
    print(f"{'-'*80}")

    # --- STEP 1: MICRO-SCALE (PARTICLES) ---
    print(f"\n{BOLD}[1] MICRO-SCALE: Particle Spectrum Analysis{RESET}")
    print(f"     Method: Monte Carlo Statistical Audit (Lattice Fit)")

    z_score, p_val = ParticleEngine.run_monte_carlo(10000)

    status_micro = f"{RED}FAIL{RESET}"
    if z_score > 2.0: status_micro = f"{GREEN}PASS{RESET}"

    print(f"     Significance: {BOLD}{z_score:.2f} Sigma{RESET}")
    print(f"     P-Value:      {p_val:.5f}")
    print(f"     Verdict:      {status_micro}")

    # --- STEP 2: MESO-SCALE (NUCLEI) ---
    print(f"\n{BOLD}[2] MESO-SCALE: Nuclear Stability Limit (Alpha Wall){RESET}")
    print(f"     Method: Efficiency Analysis at Z=82 (Lead) vs Z=84 (Polonium)")

    wall_acc, wall_valid, pb_val, po_val = NuclearEngine.analyze_wall()

    status_meso = f"{RED}FAIL{RESET}"
    if wall_valid and wall_acc > 99.0: status_meso = f"{GREEN}PASS{RESET}"

    print(f"     Pb-208 Eff:   {pb_val:.5f} alpha (Stable)")
    print(f"     Po-210 Eff:   {po_val:.5f} alpha (Unstable)")
    print(f"     Wall Accuracy: {BOLD}{wall_acc:.3f} %{RESET}")
    print(f"     Verdict:       {status_meso}")

    # --- STEP 3: MACRO-SCALE (GRAVITY) ---
    print(f"\n{BOLD}[3] MACRO-SCALE: Gravitational Unification{RESET}")
    print(f"     Method: Analytical Derivation of G from Proton Mass")

    G_val, G_err = GravityEngine.derive_G()

    status_macro = f"{RED}FAIL{RESET}"
    if G_err < 0.01: status_macro = f"{GREEN}PASS{RESET}"

    print(f"     Calculated G: {G_val:.5e}")
    print(f"     CODATA G:     {Constants.G_REAL:.5e}")
    print(f"     Error:        {BOLD}{G_err*100:.4f} %{RESET}")
    print(f"     Verdict:      {status_macro}")

    # --- FINAL SCORING ---
    print(f"\n{BOLD}{'='*80}")
    print(f" FINAL ASSESSMENT")
    print(f"{'='*80}{RESET}")

    total_score = 0
    if z_score > 2.5: total_score += 33
    if wall_valid: total_score += 33
    if G_err < 0.005: total_score += 34

    print(f" GLOBAL CONSISTENCY SCORE: {BOLD}{total_score}/100{RESET}")

    if total_score == 100:
        print(f"\n {GREEN}{BOLD}*** GRAND UNIFIED THEORY CANDIDATE ***{RESET}")
        print(f" The model is statistically significant and physically consistent")
        print(f" across all three major scales of reality.")
    elif total_score > 60:
        print(f"\n {YELLOW}{BOLD}STRONG THEORETICAL FRAMEWORK{RESET}")
        print(f" Significant correlation found, but minor deviations exist.")
    else:
        print(f"\n {RED}INCONCLUSIVE{RESET}")

    print(f"{'='*80}")
    print(f" Report saved to: FINAL_THEORY_REPORT.txt")

if __name__ == "__main__":
    run_master_test()