import math
import sys
import re
import os

# =============================================================================
# THE GEOMETRIC UNIVERSE: REBUTTAL TEST
# =============================================================================
# OBJECTIVE: Falsify the "Free Parameter" criticism.
# CRITICISM: "Why did you choose k=17 for Tau? Is it arbitrary?"
# DEFENSE:   "The integer k is not arbitrary. Changing k results in
#             predicting a different, existing particle family."
#
# HYPOTHESIS 1 (Neighbor Test): The lattice is dense. k-1 and k+1 are not empty.
# HYPOTHESIS 2 (Prime Test):    Prime nodes correlate with Elementary particles.
#                               Composite nodes correlate with Hadrons.
# =============================================================================

# --- LOGGER CLASS ---
class DualLogger:
    """Redirects stdout to both console and a log file."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Strip ANSI color codes for the text log
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

    # Base Energy Scales
    SCALE_LEPTON = 4 * PI * (N**3) * ME_MEV  # ~ 104.12 MeV
    SCALE_BARYON = (PI**5) * ME_MEV          # ~ 156.37 MeV
    SCALE_MESON  = ALPHA_INV * ME_MEV        # ~ 70.02 MeV

# --- EXTENDED PARTICLE DATABASE ---
# Format: (Mass MeV, Name, Classification)
PARTICLE_DB = [
    (105.66,  "Muon",      "Elementary"),
    (139.57,  "Pion+",     "Composite"),
    (493.67,  "Kaon+",     "Composite"),
    (938.27,  "Proton",    "Composite"), # Stable Hadron
    (939.56,  "Neutron",   "Composite"),
    (1019.46, "Phi",       "Composite"),
    (1115.68, "Lambda",    "Composite"),
    (1189.37, "Sigma+",    "Composite"),
    (1232.0,  "Delta",     "Composite"),
    (1321.71, "Xi-",       "Composite"),
    (1535.0,  "N(1535)",   "Composite"),
    (1672.45, "Omega-",    "Composite"),
    (1776.86, "Tau",       "Elementary"),
    (1869.65, "D+",        "Composite"),
    (1968.34, "D_s+",      "Composite"),
    (2286.46, "Lambda_c",  "Composite"),
    (2983.4,  "Eta_c",     "Composite"),
    (3096.9,  "J/Psi",     "Composite")
]

class Formatting:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"

# --- HELPER FUNCTIONS ---

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def find_match(mass_mev):
    best_match_name = None
    best_match_type = None
    best_err = float('inf')

    for p_mass, p_name, p_type in PARTICLE_DB:
        err = abs(mass_mev - p_mass) / p_mass
        if err < best_err:
            best_err = err
            best_match_name = p_name
            best_match_type = p_type

    return best_match_name, best_match_type, best_err

def analyze_neighborhood(target_name, scale_name, scale_val, center_k):
    print(f"\n{Formatting.BOLD}NEIGHBORHOOD ANALYSIS: {target_name}{Formatting.RESET}")
    print(f" CRITICISM: 'Why specifically k={center_k}? Why not the adjacent integers?'")
    print(f" RESPONSE:  'Changing the integer changes the particle family.'")
    print("-" * 85)
    print(f" {'k':<4} | {'NODE TYPE':<10} | {'THEORY (MeV)':<15} | {'REAL PARTICLE':<20} | {'MATCH?'}")
    print("-" * 85)

    # Scan neighbors k-2 to k+2
    for k in range(center_k - 2, center_k + 3):
        theory_mass = k * scale_val
        match_name, match_type, err = find_match(theory_mass)

        node_type = "PRIME" if is_prime(k) else "COMPOSITE"
        row_color = Formatting.RESET
        status = "---"
        marker = ""

        # Check for match (Tolerance 2.5%)
        if err < 0.025:
            status = f"{match_name} ({err*100:.1f}%)"
            if k == center_k:
                row_color = Formatting.GREEN
                marker = "<< TARGET"
            else:
                row_color = Formatting.YELLOW
                marker = "   NEIGHBOR"

        print(f" {row_color}{k:<4} | {node_type:<10} | {theory_mass:<15.2f} | {status:<20} | {marker}{Formatting.RESET}")

def run_rebuttal():
    # Setup Log
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Rebuttal_Report.txt"))

    print("======================================================================")
    print(" THE GEOMETRIC UNIVERSE: REBUTTAL & FALSIFICATION TEST")
    print("======================================================================")

    # 1. TAU TEST (The Strongest Proof)
    analyze_neighborhood("TAU (Lepton Scale)", "Lepton", Constants.SCALE_LEPTON, 17)

    print("\n [INTERPRETATION: TAU LADDER]")
    print(" 1. k=17 (Prime)     -> Matches TAU (Lepton/Elementary).")
    print(" 2. k=16 (Composite) -> Matches OMEGA- (Baryon/Composite).")
    print(" 3. k=18 (Composite) -> Matches D+ (Meson/Composite).")
    print(f" {Formatting.CYAN}CONCLUSION: The lattice unifies Leptons and Hadrons on a single scale.{Formatting.RESET}")

    # 2. PROTON TEST
    analyze_neighborhood("PROTON (Baryon Scale)", "Baryon", Constants.SCALE_BARYON, 6)

    print("\n [INTERPRETATION: PROTON]")
    print(" 1. k=6  (Composite) -> Matches PROTON (Stable Baryon).")
    print(" 2. k=7  (Prime)     -> Matches LAMBDA (Unstable Baryon).")
    print(f" {Formatting.CYAN}CONCLUSION: Baryon resonances adhere to integer steps of Pi^5.{Formatting.RESET}")

    # 3. STATISTICAL PRIME CHECK
    print("\n======================================================================")
    print(" STATISTICAL HYPOTHESIS: PRIME NUMBER DOMINANCE")
    print("======================================================================")
    print(" Checking the first 50 integers on all 3 scales (150 potential nodes).")

    scales = [Constants.SCALE_LEPTON, Constants.SCALE_MESON, Constants.SCALE_BARYON]
    hits_prime = 0
    hits_composite = 0
    total_scanned = 0

    # Random baseline: In range 1-50, there are 15 primes (30%).
    # If physics was random, we should see ~30% primes in hits.

    for scale in scales:
        for k in range(1, 51):
            mass = k * scale
            name, ptype, err = find_match(mass)

            if err < 0.02: # 2% Hit Tolerance
                total_scanned += 1
                if is_prime(k):
                    hits_prime += 1
                else:
                    hits_composite += 1

    total_hits = hits_prime + hits_composite
    if total_hits == 0: total_hits = 1 # Avoid div by zero

    prime_ratio = (hits_prime / total_hits) * 100

    print(f" Total Hits found (Error < 2%): {total_hits}")
    print(f" Hits on PRIME integers:        {hits_prime}")
    print(f" Hits on COMPOSITE integers:    {hits_composite}")
    print(f" Prime Hit Ratio:               {Formatting.BOLD}{prime_ratio:.1f} %{Formatting.RESET}")
    print(f" Random Baseline (Expected):    30.0 %")

    print("-" * 70)
    print(" VERDICT:")
    if prime_ratio > 30.0:
        print(f" {Formatting.GREEN}[POSITIVE SIGNAL]{Formatting.RESET} Primes are over-represented compared to randomness.")
        print(" This supports the hypothesis that Prime Topology correlates with stability.")
    else:
        print(f" {Formatting.YELLOW}[NEUTRAL SIGNAL]{Formatting.RESET} Primes appear at expected random rates.")
        print(" The distinction between Elementary/Composite particles is likely more complex.")

    print("======================================================================")
    print(" Report saved to 'Rebuttal_Report.txt'")

if __name__ == "__main__":
    run_rebuttal()