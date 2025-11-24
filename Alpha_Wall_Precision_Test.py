import math
import sys
import re

# =============================================================================
# THE GEOMETRIC UNIVERSE: HEAVY NUCLEI PRECISION AUDIT (v2.0)
# =============================================================================
# GOAL: Verify the precision of the "Alpha Wall" (Stability Limit) in heavy elements.
# OUTPUT: Console (Color) + File 'Alpha_Wall_Report.txt' (Plain Text)
# AUTHOR: Jan Šági
# DATE: November 2025
# =============================================================================

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV
    ME_MEV = 0.510998950
    # Baryon Scale Anchor (k=6) -> 6 * PI^5 * me
    PROTON_GEOM_MEV = (6 * (PI**5)) * ME_MEV
    # The Unit Alpha Binding Energy
    UNIT_ALPHA = PROTON_GEOM_MEV * ALPHA

    U_TO_MEV = 931.49410242

class Dataset:
    # Focusing on the transition STABLE -> UNSTABLE in heavy elements.
    # Source: NUBASE / NIST
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
        ("Pb-206", 206, 205.97446, "STABLE"),
        ("Pb-207", 207, 206.97589, "STABLE"),
        ("Pb-208", 208, 207.97665, "STABLE"),   # ---> THE WALL
        ("Bi-209", 209, 208.98039, "BORDER"),   # Technically unstable, but > universe age
        ("Po-210", 210, 209.98287, "UNSTABLE"), # ---> BREAKING POINT
        ("At-211", 211, 210.98749, "UNSTABLE"),
        ("Rn-222", 222, 222.01763, "UNSTABLE"),
        ("Fr-223", 223, 223.01973, "UNSTABLE"),
        ("Ra-226", 226, 226.02540, "UNSTABLE"),
        ("U-238",  238, 238.05078, "UNSTABLE"),
    ]

# --- LOGGER CLASS (Writes to both Console and File) ---
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        # 1. Write to Console (with Colors)
        self.terminal.write(message)

        # 2. Write to File (Clean Text - remove ANSI codes)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# Redirect output to DualLogger
sys.stdout = DualLogger("Alpha_Wall_Report.txt")

def analyze_wall():
    print(f"===================================================================")
    print(f" THE ALPHA WALL AUDIT: PRECISION ANALYSIS")
    print(f"===================================================================")
    print(f" Searching for the boundary where Alpha Efficiency drops below 1.0000")
    print(f" Saving record to 'Alpha_Wall_Report.txt'")
    print(f"-------------------------------------------------------------------")
    print(f" {'ISOTOPE':<8} | {'STATUS':<8} | {'ALPHA EFFICIENCY':<20} | {'GAP TO 1.0'}")
    print(f"-------------------------------------------------------------------")

    pb_eff = 0
    po_eff = 0

    RESET = "\033[0m"

    for name, A, mass_u, status in Dataset.HEAVY_ISOTOPES:
        # Calculation
        mass_theory = A * Constants.PROTON_GEOM_MEV
        mass_real = mass_u * Constants.U_TO_MEV
        binding = mass_theory - mass_real
        eff = (binding / A) / Constants.UNIT_ALPHA

        # Gap (distance from 1.0 boundary)
        gap = eff - 1.0

        # Color coding
        color = RESET
        if eff >= 1.0: color = "\033[92m" # Green (Stable)
        elif abs(eff - 1.0) < 0.002: color = "\033[93m" # Yellow (Border)
        else: color = "\033[91m" # Red (Unstable)

        print(f" {color}{name:<8} | {status:<8} | {eff:.6f} α            | {gap:+.6f}{RESET}")

        if name == "Pb-208": pb_eff = eff
        if name == "Po-210": po_eff = eff

    print(f"-------------------------------------------------------------------")
    print(f" CROSSOVER ANALYSIS:")
    print(f" Heaviest Stable Element (Pb-208):  {pb_eff:.6f} α")
    print(f" First Clearly Unstable (Po-210):   {po_eff:.6f} α")
    print(f"-------------------------------------------------------------------")

    # Critical Deviation
    # How close is Pb-208 to the mathematical limit 1.0?
    crossover_precision = abs(pb_eff - 1.0) * 100

    print(f" BOUNDARY PRECISION: \033[1m{crossover_precision:.4f} %\033[0m")
    print(f"-------------------------------------------------------------------")

    if pb_eff > 1.0 and po_eff < 1.0:
        print(f" \033[92m[VERIFIED] Stability boundary lies exactly between Pb and Po.")
        print(f" The theory successfully predicted the end of the Periodic Table.\033[0m")
    else:
        print(f" [FAILED] Boundary does not match.")

    print(f"===================================================================")

if __name__ == "__main__":
    analyze_wall()