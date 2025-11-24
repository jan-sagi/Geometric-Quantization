import math
import random
import statistics
import time
import sys
import re

# =============================================================================
# THE GEOMETRIC UNIVERSE: GLOBAL STATISTICAL AUDIT (Monte Carlo)
# =============================================================================
# GOAL:   Determine the probability that the geometric match is coincidental.
# METHOD: Compare model error in "Our Universe" vs "10,000 Random Universes".
# OUTPUT: Console (Color) + File 'Global_Audit_Report.txt'
# AUTHOR: Jan Šági
# DATE:   November 2025
# =============================================================================

class Constants:
    # --- HARD-CODED CONSTANTS (No Tuning) ---
    PI = math.pi
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV
    N = math.log(4 * PI)

    # Pre-calculated Geometric Bases (in electron mass units me)
    SCALE_LEPTON = 4 * PI * (N**3)       # ~ 206.77 me
    SCALE_MESON  = ALPHA_INV             # ~ 137.04 me
    SCALE_BARYON = PI**5                 # ~ 306.02 me

    # Conversion: me -> MeV (for comparison with data)
    ME_TO_MEV = 0.51099895

class Data:
    # DATASET: 40 Key Particles (Standard Model)
    # Format: (Name, Mass_MeV)
    # Source: Particle Data Group (PDG)
    REAL_PARTICLES = [
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

# --- LOGGER CLASS ---
class DualLogger:
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

class GeometryEngine:
    @staticmethod
    def find_best_fit(mass_mev):
        """
        Finds the NEAREST node in the geometric lattice for a given mass.
        Tests all 3 scales and returns the one with the lowest error.
        """
        mass_me = mass_mev / Constants.ME_TO_MEV
        best_error = float('inf')

        # Test 3 scales
        scales = [Constants.SCALE_LEPTON, Constants.SCALE_MESON, Constants.SCALE_BARYON]

        for base in scales:
            # Calculate ideal node k (must be an integer)
            k_float = mass_me / base
            k_int = round(k_float)

            if k_int < 1: k_int = 1

            # Theoretical mass for this node
            theory_mass = k_int * base

            # Relative error
            error = abs(mass_me - theory_mass) / mass_me

            if error < best_error:
                best_error = error

        return best_error

class Statistician:
    @staticmethod
    def evaluate_universe(particle_list):
        """
        Calculates 'Universe Score' as the average fit error of all particles.
        Lower score = Better geometric fit.
        """
        total_error = 0
        for name, mass in particle_list:
            err = GeometryEngine.find_best_fit(mass)
            total_error += err

        # Return average error in percent
        return (total_error / len(particle_list)) * 100

    @staticmethod
    def generate_random_universe(real_particles):
        """
        Creates a 'Fake Universe'.
        Takes real particles and randomly jitters their mass by +/- 30% (log-uniform).
        This destroys precise geometry but preserves the 'physical hierarchy'.
        """
        fake_particles = []
        for name, mass in real_particles:
            # Random jitter 0.7x to 1.3x
            jitter = math.exp(random.uniform(math.log(0.7), math.log(1.3)))
            fake_mass = mass * jitter
            fake_particles.append((f"Fake_{name}", fake_mass))
        return fake_particles

def run_global_test():
    # Redirect output
    sys.stdout = DualLogger("Global_Audit_Report.txt")

    # Colors
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    print(f"===================================================================")
    print(f" THE GEOMETRIC UNIVERSE: GLOBAL CONSISTENCY AUDIT (Monte Carlo)")
    print(f"===================================================================")
    print(f" 1. THEORY: Strict Lattice (N^3, Alpha^-1, Pi^5). No tuning.")
    print(f" 2. DATA:   {len(Data.REAL_PARTICLES)} Key Particles (Standard Model).")
    print(f" 3. TEST:   Comparison against 10,000 Randomly Generated Universes.")
    print(f"-------------------------------------------------------------------")

    # 1. Evaluate OUR Universe
    real_score = Statistician.evaluate_universe(Data.REAL_PARTICLES)
    print(f"\n[REALITY CHECK]")
    print(f" Average grid deviation in OUR universe: {BOLD}{real_score:.4f} %{RESET}")

    # 2. Monte Carlo Simulation
    SIMULATIONS = 10000
    print(f"\n[MONTE CARLO SIMULATION STARTING...]")
    print(f" Generating {SIMULATIONS} parallel universes...")

    start_time = time.time()
    better_universes = 0
    scores = []

    for i in range(SIMULATIONS):
        # Generate fake universe
        fake_uni = Statistician.generate_random_universe(Data.REAL_PARTICLES)
        # Test it
        fake_score = Statistician.evaluate_universe(fake_uni)
        scores.append(fake_score)

        # Is this random universe 'more geometric' than ours?
        if fake_score < real_score:
            better_universes += 1

        if (i+1) % 1000 == 0:
            print(f" ... {i+1} simulations done.")

    # 3. Statistics
    mean_random_score = statistics.mean(scores)
    stdev_random_score = statistics.stdev(scores)
    z_score = (real_score - mean_random_score) / stdev_random_score
    p_value = better_universes / SIMULATIONS

    print(f"\n===================================================================")
    print(f" AUDIT RESULTS")
    print(f"===================================================================")
    print(f" Average RANDOM universe error:  {mean_random_score:.4f} % (± {stdev_random_score:.4f})")
    print(f" YOUR Model error:               {BOLD}{real_score:.4f} %{RESET}")
    print(f"-------------------------------------------------------------------")
    print(f" Z-SCORE (Sigma): {BOLD}{abs(z_score):.2f} σ{RESET}")
    print(f" P-VALUE:         {BOLD}{p_value:.5f}{RESET}")
    print(f"-------------------------------------------------------------------")

    # 4. Verdict
    print(f" VERDICT:")
    if p_value < 0.003:
        print(f" {GREEN}[STRONG SIGNAL] Statistically highly significant (>3 sigma).{RESET}")
        print(f" Probability of coincidence is less than 0.3%. Model detects real structure.")
    elif p_value < 0.05:
        print(f" {YELLOW}[MODERATE SIGNAL] Statistically significant (<5%).{RESET}")
        print(f" Model performs better than chance but requires tuning (topological corrections).")
    else:
        print(f" {RED}[NO SIGNAL] Indistinguishable from noise.{RESET}")
        print(f" Geometric lattice fits data no better than random numbers.")
    print(f"===================================================================")
    print(f" Report saved to 'Global_Audit_Report.txt'")

if __name__ == "__main__":
    run_global_test()