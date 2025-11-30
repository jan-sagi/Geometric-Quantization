import math
import sys
import os

# =============================================================================
# WEAK FORCE HUNTER: SEARCHING FOR W/Z BOSONS
# =============================================================================
# OBJECTIVE: Determine if "Forces" (W/Z Bosons) are merely high-energy
#            nodes of the geometric lattice.
#
# TARGETS:
#   W Boson ~ 80.4 GeV (80400 MeV)
#   Z Boson ~ 91.2 GeV (91200 MeV)
#   Higgs   ~ 125.1 GeV (125100 MeV)
# =============================================================================

# --- LOGGER CLASS ---
class DualLogger:
    """Redirects stdout to both console and a log file."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV
    ME_TO_MEV = 0.510998950

    # Baryon Scale (Proton base) - Best candidate for heavy particles
    # Formula: Pi^5 * me
    SCALE_BARYON_MEV = (PI**5) * ME_TO_MEV # ~ 156.37 MeV per unit k

    # Lepton Scale
    N = math.log(4 * PI)
    SCALE_LEPTON_MEV = 4 * PI * (N**3) * ME_TO_MEV # ~ 104.12 MeV per unit k

# --- FORMATTING ---
class Fmt:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def scan_for_bosons():
    # Setup Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Weak_Force_Report.txt"))

    print(f"{Fmt.BOLD}{'='*90}")
    print(f" WEAK FORCE GEOMETRY SCAN (80 - 130 GeV)")
    print(f"{'='*90}{Fmt.RESET}")
    print(f" LATTICE BASE: Baryon Scale (Pi^5) = {Constants.SCALE_BARYON_MEV:.4f} MeV")
    print(f"{'-'*90}")
    print(f" {'TARGET':<10} | {'REAL MASS':<12} | {'NEAREST NODE (k)':<20} | {'THEORY MASS':<12} | {'ERROR'}")
    print(f"{'-'*90}")

    targets = [
        ("W Boson", 80379.0),
        ("Z Boson", 91187.6),
        ("Higgs", 125100.0)
    ]

    # Use Baryon Scale (Pi^5) as Bosons behave like heavy matter
    base = Constants.SCALE_BARYON_MEV

    for name, real_mass in targets:
        # 1. Find nearest integer node k
        k_float = real_mass / base
        k_int = round(k_float)

        # 2. Calculate Theoretical Mass
        theory_mass = k_int * base

        # 3. Calculate Error
        error = abs(theory_mass - real_mass) / real_mass * 100

        # Analyze k (Topology check)
        note = ""
        if k_int % 2 != 0: note = "(Odd)"
        else: note = "(Even)"

        k_display = f"k = {k_int} {note}"

        # Color Highlighting
        color = Fmt.RESET
        status = ""

        if error < 0.05:
            color = Fmt.GREEN
            status = "[EXACT MATCH]"
        elif error < 1.0:
            color = Fmt.YELLOW
            status = "[MATCH]"

        print(f" {color}{name:<10} | {real_mass:<12.1f} | {k_display:<20} | {theory_mass:<12.1f} | {error:.2f}% {status}{Fmt.RESET}")

    print(f"{'-'*90}")
    print(f"{Fmt.BOLD} INTERPRETATION:{Fmt.RESET}")
    print(" 1. If W/Z Bosons align with integer nodes, the 'Weak Force' is likely not a force")
    print("    but a high-frequency resonance of the vacuum lattice.")
    print(" 2. The Higgs Boson (k=800) suggests a harmonic closure of the lattice.")
    print(f"{'='*90}")
    print(f" Report saved to 'Weak_Force_Report.txt'")

if __name__ == "__main__":
    scan_for_bosons()