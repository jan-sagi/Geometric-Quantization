import math
import random
import sys
import re
from decimal import Decimal, getcontext

# =============================================================================
# GEOMETRIC UNIVERSE: THE STRESS TEST (Devil's Advocate Edition)
# =============================================================================
# GOAL:   Attempt to FALSIFY the theory by finding "Blind Spots".
# METHOD 1: Isobar Test (Does the theory distinguish Beta Decay?)
# METHOD 2: Lattice Density Test (Is the high-energy match just a coincidence?)
# OUTPUT: Console (Color) + File 'Stress_Test_Report.txt'
# =============================================================================

# Precision settings
getcontext().prec = 100

# --- LOGGER CLASS ---
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Remove ANSI color codes for clean text file
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV
    N = math.log(4 * PI)

    ME_MEV = 0.510998950
    # Geometric Proton (Theory Definition)
    PROTON_GEOM_MEV = (6 * (PI**5)) * ME_MEV
    # Unit Binding Energy
    UNIT_ALPHA = PROTON_GEOM_MEV * ALPHA

    U_TO_MEV = 931.49410242

class IsobarDataset:
    # Triplets: Stable vs Unstable with SAME nucleon count (A)
    # The theory uses 'A' for base geometry calculation. Can it see the difference?
    ISOBARS = [
        # A=40: Argon (Stable), Potassium (Unstable), Calcium (Stable)
        {"id": "GROUP A=40", "data": [
            ("Ar-40", 40, 39.962383, "STABLE"),
            ("K-40",  40, 39.963998, "UNSTABLE"), # Beta decay
            ("Ca-40", 40, 39.962591, "STABLE")
        ]},
        # A=50: Titanium (Stable), Vanadium (Unstable), Chromium (Stable)
        {"id": "GROUP A=50", "data": [
            ("Ti-50", 50, 49.944791, "STABLE"),
            ("V-50",  50, 49.947158, "UNSTABLE"), # Very long half-life but unstable
            ("Cr-50", 50, 49.946044, "STABLE")
        ]},
        # A=87: Rubidium (Unstable), Strontium (Stable)
        {"id": "GROUP A=87", "data": [
            ("Rb-87", 87, 86.909180, "UNSTABLE"),
            ("Sr-87", 87, 86.908877, "STABLE")
        ]}
    ]

class Formatting:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def run_isobar_stress_test():
    print(f"\n{Formatting.BOLD}TEST 1: ISOBAR BLINDNESS (The Weak Force Attack){Formatting.RESET}")
    print("Hypothesis: Geometry based solely on 'A' cannot distinguish Proton from Neutron.")
    print("If the theory assigns equal efficiency to stable and unstable isobars, it fails.")
    print("-" * 80)
    print(f"{'ISOTOPE':<8} | {'STATUS':<10} | {'EFFICIENCY (Alpha)':<20} | {'RESULT'}")
    print("-" * 80)

    for group in IsobarDataset.ISOBARS:
        print(f"{Formatting.YELLOW}--- {group['id']} ---{Formatting.RESET}")
        efficiencies = []

        for name, A, mass_u, status in group['data']:
            # Theory Calculation
            mass_theory = A * Constants.PROTON_GEOM_MEV
            mass_real = mass_u * Constants.U_TO_MEV
            binding = mass_theory - mass_real
            eff = (binding / A) / Constants.UNIT_ALPHA

            efficiencies.append((name, status, eff))

            # Output
            print(f"{name:<8} | {status:<10} | {eff:.6f} alpha")

        # ANALYSIS OF DIFFERENCE
        # Can the theory distinguish K-40 (Unstable) from Ca-40 (Stable)?
        stable_effs = [e for n, s, e in efficiencies if s == "STABLE"]
        unstable_effs = [e for n, s, e in efficiencies if s == "UNSTABLE"]

        if stable_effs and unstable_effs:
            avg_stable = sum(stable_effs)/len(stable_effs)
            avg_unstable = sum(unstable_effs)/len(unstable_effs)
            diff = abs(avg_stable - avg_unstable)

            print(f" > Resolution Power (Delta Eff): {diff:.6f}")
            if diff < 0.0005:
                print(f" > {Formatting.RED}[CRITICAL FAIL] Theory is 'blind' to Beta Decay.{Formatting.RESET}")
                print(f"   It cannot explain why {group['data'][1][0]} decays into its neighbor.")
            else:
                print(f" > {Formatting.GREEN}[PASS] Theory detects geometric difference.{Formatting.RESET}")
        print("")

def run_lattice_density_test():
    print(f"\n{Formatting.BOLD}TEST 2: LATTICE SATURATION (The Statistical Attack){Formatting.RESET}")
    print("Hypothesis: At high energies, the geometric lattice is so dense anything fits.")
    print("Method: Generate 1000 RANDOM 'particles' (2000 - 10000 MeV) and measure hit rate.")
    print("-" * 80)

    # 1. Generate Lattice (Simplified version of the core algorithm)
    lattice_nodes = []
    bases = [
        4 * Constants.PI * (Constants.N**3) * Constants.ME_MEV, # Lepton
        Constants.ALPHA_INV * Constants.ME_MEV,                 # Meson
        (Constants.PI**5) * Constants.ME_MEV                    # Baryon
    ]

    # Generate nodes up to 10 GeV
    for base in bases:
        for k in range(1, 100):
            val = base * k
            if 2000 < val < 10000:
                lattice_nodes.append(val)

    lattice_nodes.sort()

    # 2. Test Random Particles
    hits = 0
    trials = 1000
    tolerance = 0.015 # 1.5% tolerance (same as in the main audit)

    for _ in range(trials):
        random_mass = random.uniform(2000, 10000)

        # Find nearest node
        best_err = float('inf')
        for node in lattice_nodes:
            err = abs(random_mass - node) / random_mass
            if err < best_err: best_err = err

        if best_err < tolerance:
            hits += 1

    hit_rate = (hits / trials) * 100
    print(f"Number of geometric nodes in 2-10 GeV band: {len(lattice_nodes)}")
    print(f"Success rate of RANDOM numbers (Noise Floor):  {hit_rate:.2f} %")

    print("-" * 80)
    print("VERDICT:")
    if hit_rate > 20:
        print(f"{Formatting.RED}[DANGER] Lattice is saturated!{Formatting.RESET}")
        print("More than 20% of random numbers hit the theory. Prediction power >2 GeV is low.")
    else:
        print(f"{Formatting.GREEN}[ROBUST] Lattice is sparse.{Formatting.RESET}")
        print("Random numbers do not hit. If real particles hit, it is significant.")

if __name__ == "__main__":
    # Redirect output to file and console
    sys.stdout = DualLogger("Stress_Test_Report.txt")

    print("INITIATING THEORY DESTRUCTION TESTS...")
    run_isobar_stress_test()
    run_lattice_density_test()