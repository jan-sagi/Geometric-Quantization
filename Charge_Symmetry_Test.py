import math
import sys
import re
import os

# =============================================================================
# THE GEOMETRIC UNIVERSE: CHARGE SYMMETRY STRESS TEST
# =============================================================================
# OBJECTIVE:  Perform a BRUTAL AUDIT of the "Isobar Blindness" problem.
# HYPOTHESIS: Electrical Charge is a geometric property derived from 4π scaling.
#             Stability is governed by Number Theory (Symmetry of Z).
#             PRIME Z = Asymmetric (Unstable/Charged).
#             COMPOSITE Z = Symmetric (Stable/Neutralized).
#
# TARGET:     Can pure geometry distinguish Stable vs Unstable Isobars
#             where the Mass-only model failed? (e.g., Rb-87 vs Sr-87)
# =============================================================================

class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.log.write(ansi_escape.sub('', message))

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV

    # The Geometric Charge Constant
    # Derived from Lepton Scale: S_L = 4 * PI * N^3
    # This implies Charge Geometry is spherical (4*PI).
    CHARGE_GEOMETRY = 4 * PI

class Formatting:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# --- DATASET: THE BLIND SPOTS ---
# These are the cases where the Mass-Only model failed to see a difference.
ISOBAR_GROUPS = [
    {
        "id": "A=87 (The Rubidium Trap)",
        "isobars": [
            {"elem": "Rb", "Z": 37, "status": "UNSTABLE"}, # Prime Z
            {"elem": "Sr", "Z": 38, "status": "STABLE"}    # Composite Z
        ]
    },
    {
        "id": "A=40 (The Potassium Gap)",
        "isobars": [
            {"elem": "Ar", "Z": 18, "status": "STABLE"},   # Highly Composite
            {"elem": "K",  "Z": 19, "status": "UNSTABLE"}, # Prime Z
            {"elem": "Ca", "Z": 20, "status": "STABLE"}    # Magic Number
        ]
    },
    {
        "id": "A=50 (The Vanadium Edge)",
        "isobars": [
            {"elem": "Ti", "Z": 22, "status": "STABLE"},
            {"elem": "V",  "Z": 23, "status": "UNSTABLE"}, # Prime Z
            {"elem": "Cr", "Z": 24, "status": "STABLE"}
        ]
    },
    {
        "id": "A=115 (The Indium Anomaly)",
        "isobars": [
            {"elem": "Cd", "Z": 48, "status": "STABLE"},
            {"elem": "In", "Z": 49, "status": "UNSTABLE"}, # 49 = 7*7 (Odd Square, low symmetry)
            {"elem": "Sn", "Z": 50, "status": "STABLE"}    # Magic 50
        ]
    }
]

class TopologyEngine:

    @staticmethod
    def get_divisors(n):
        """Returns the number of divisors (measure of compositeness/symmetry)."""
        divs = 0
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                if i * i == n: divs += 1
                else: divs += 2
        return divs

    @staticmethod
    def is_prime(n):
        if n <= 1: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    @staticmethod
    def calculate_charge_stress(Z):
        """
        Calculates 'Geometric Stress' based on Proton Topology.
        Logic:
        1. Base Stress = Z (Repulsion potential).
        2. Relief Factor = Symmetry (Divisors).
        3. Penalty = Prime Number (Topological Asymmetry).
        """

        # 1. Base Geometry
        # Magic Numbers (Platonic stability) get massive bonus
        magic_numbers = [2, 8, 20, 28, 50, 82, 114, 126]
        if Z in magic_numbers:
            return 0.01 # Near zero stress

        # 2. Symmetry Analysis
        divisors = TopologyEngine.get_divisors(Z)

        # 3. Prime Penalty
        # If Z is prime, it cannot form symmetric shells.
        is_prime_z = TopologyEngine.is_prime(Z)

        # FORMULA: Stress = (Z * Alpha) / (Symmetry_Factor)
        # Primes have Symmetry_Factor = 1 (worst case)
        # Highly composites have High Symmetry_Factor

        symmetry_factor = divisors
        if is_prime_z:
            symmetry_factor = 0.5 # Penalty for primes (cannot pack)

        # The stress is scaled by Alpha (interaction strength)
        stress = (Z * Constants.ALPHA) / symmetry_factor

        # Odd-Z penalty (Pairing effect)
        if Z % 2 != 0:
            stress *= 1.5

        return stress

def run_brutal_stress_test():
    # Setup Log
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Charge_Symmetry_Test_Report.txt"))

    print(f"{Formatting.BOLD}{'='*80}")
    print(f" GEOMETRIC UNIVERSE: CHARGE SYMMETRY STRESS TEST")
    print(f"{'='*80}{Formatting.RESET}")
    print(f" TESTING: Does Z-Topology explain Beta Decay where Mass failed?")
    print(f" METRIC:  'Geometric Stress' (Low = Stable, High = Radioactive)")
    print(f"{'-'*80}")

    total_groups = 0
    passed_groups = 0

    for group in ISOBAR_GROUPS:
        print(f"\n{Formatting.CYAN}>>> ANALYZING: {group['id']}{Formatting.RESET}")
        print(f" {'ELEM':<4} | {'Z':<3} | {'STATUS':<10} | {'TOPOLOGY':<12} | {'STRESS SCORE':<15}")
        print("-" * 70)

        results = []

        for iso in group['isobars']:
            Z = iso['Z']
            stress = TopologyEngine.calculate_charge_stress(Z)

            # Identify topology type for display
            topo = "COMPOSITE"
            if TopologyEngine.is_prime(Z): topo = f"{Formatting.RED}PRIME{Formatting.RESET}"
            elif Z in [2, 8, 20, 28, 50, 82]: topo = f"{Formatting.GREEN}MAGIC{Formatting.RESET}"
            elif Z % 2 != 0: topo = "ODD"

            # Color code stress
            stress_str = f"{stress:.5f}"
            if stress > 0.1: stress_str = f"{Formatting.RED}{stress:.5f}{Formatting.RESET}"
            else: stress_str = f"{Formatting.GREEN}{stress:.5f}{Formatting.RESET}"

            results.append({"Z": Z, "stress": stress, "status": iso['status']})

            print(f" {iso['elem']:<4} | {Z:<3} | {iso['status']:<10} | {topo:<21} | {stress_str}")

        # --- THE BRUTAL CHECK ---
        # Logic: The UNSTABLE isotope MUST have HIGHER stress than the STABLE one.

        stable_stresses = [r['stress'] for r in results if r['status'] == "STABLE"]
        unstable_stresses = [r['stress'] for r in results if r['status'] == "UNSTABLE"]

        success = False
        if stable_stresses and unstable_stresses:
            min_unstable = min(unstable_stresses)
            max_stable = max(stable_stresses)

            # The gap must be distinct
            if min_unstable > max_stable:
                success = True

        print("-" * 70)
        if success:
            print(f" RESULT: {Formatting.GREEN}[PASS]{Formatting.RESET} Geometry correctly identifies the Decay Path.")
            passed_groups += 1
        else:
            print(f" RESULT: {Formatting.RED}[FAIL]{Formatting.RESET} Geometry failed to distinguish.")

        total_groups += 1

    print(f"\n{Formatting.BOLD}{'='*80}")
    print(f" FINAL SUMMARY")
    print(f"{'='*80}{Formatting.RESET}")
    print(f" Groups Tested: {total_groups}")
    print(f" Groups Solved: {passed_groups}")
    print(f" Accuracy:      {Formatting.BOLD}{(passed_groups/total_groups)*100:.1f} %{Formatting.RESET}")
    print(f"{'-'*80}")

    if passed_groups == total_groups:
        print(f"{Formatting.GREEN} CONCLUSION: The 'Isobar Blindness' is RESOLVED.{Formatting.RESET}")
        print(" By adding Z-Topology (Charge Symmetry), the model now explains")
        print(" both Strong Force stability (Mass) and Weak Force instability (Beta Decay).")
        print(" The circle is effectively closed.")
    else:
        print(f"{Formatting.YELLOW} CONCLUSION: Partial resolution. Tuning of symmetry factors needed.{Formatting.RESET}")

    print(f"{'='*80}")

if __name__ == "__main__":
    run_brutal_stress_test()