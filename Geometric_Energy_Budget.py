import math
import sys
import os
from decimal import Decimal, getcontext

# =============================================================================
# GEOMETRIC ENERGY BUDGET: DECONSTRUCTING ALPHA
# =============================================================================
# OBJECTIVE: Analyze the distinct energy layers of the Alpha Constant.
# HYPOTHESIS: The components of Alpha (Volume, Area, Line) correspond to
#             the Energy Budget of the Universe (Dark Energy, Dark Matter, Baryons).
#
# FORMULA: Alpha^-1 = 4pi^3 + pi^2 + pi
# =============================================================================

getcontext().prec = 100
def D(val): return Decimal(str(val))

# --- LOGGER CLASS ---
class DualLogger:
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
    PI = D("3.14159265358979323846264338327950288419716939937510")

    # Geometric Components
    VOL_TERM = 4 * (PI**3)
    AREA_TERM = PI**2
    LINE_TERM = PI

    TOTAL_ALPHA_INV = VOL_TERM + AREA_TERM + LINE_TERM

class Formatting:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def analyze_budget():
    # Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Geometric_Energy_Budget.txt"))

    total = Constants.TOTAL_ALPHA_INV
    vol = Constants.VOL_TERM
    area = Constants.AREA_TERM
    line = Constants.LINE_TERM

    # Calculate Ratios (Percentages)
    p_vol = (vol / total) * 100
    p_area = (area / total) * 100
    p_line = (line / total) * 100

    print(f"{Formatting.BOLD}{'='*80}")
    print(f" GEOMETRIC ENERGY BUDGET ANALYSIS")
    print(f"{'='*80}{Formatting.RESET}")
    print(f" Total Geometric Capacity (Alpha^-1): {total:.6f}")
    print(f"{'-'*80}")
    print(f" {'COMPONENT':<15} | {'VALUE':<12} | {'% OF TOTAL':<15} | {'INTERPRETATION'}")
    print(f"{'-'*80}")

    # 1. VOLUME (4pi^3)
    print(f" {Formatting.CYAN}{'4 * Pi^3':<15} | {vol:<12.4f} | {p_vol:.4f} %        | The Bulk / Vacuum Energy{Formatting.RESET}")

    # 2. AREA (Pi^2)
    print(f" {Formatting.YELLOW}{'Pi^2':<15} | {area:<12.4f} | {p_area:.4f} %         | Surface / Interaction Field{Formatting.RESET}")

    # 3. LINE (Pi)
    print(f" {Formatting.GREEN}{'Pi':<15} | {line:<12.4f} | {p_line:.4f} %         | Baryonic / Linear Matter{Formatting.RESET}")

    print(f"{'-'*80}")

    # --- COSMOLOGICAL COMPARISON ---
    # Planck 2018 Data:
    # Dark Energy ~ 68.5%
    # Dark Matter ~ 26.5%
    # Baryonic Matter ~ 5.0%

    print(f"\n{Formatting.BOLD}>>> COMPARISON WITH COSMOLOGY (Standard Model){Formatting.RESET}")
    print(f" Baryonic Matter (Visible): ~ 4.9 %")
    print(f" Geometric Line (Pi):       ~ {p_line:.1f} %")

    ratio_baryon = p_line / D("4.9")
    print(f" Deviation Factor:          {ratio_baryon:.2f}x")

    print(f"\n{Formatting.BOLD}>>> ANALYSIS OF FORCES (Coupling Strength){Formatting.RESET}")
    # Electromagnetic Coupling is 1/137 (Total)
    # Strong Force is approx 1.0 (at short range)

    # Ratio of Volume to Surface (Bulk vs Boundary)
    ratio_vol_area = vol / area
    print(f" Bulk/Boundary Ratio (4pi): {ratio_vol_area:.4f} (Approx 4*Pi)")
    print(f" This defines the geometric impedance of the vacuum.")

    print(f"{'='*80}")
    print(" CONCLUSION:")
    print(" The geometry of Alpha is dominated by the Volumetric Term (90.5%).")
    print(" This suggests that 90% of the 'structure' of space is hidden in the Bulk.")
    print(" Visible matter (Linear Pi) is just the tip of the geometric iceberg.")
    print(f"{'='*80}")

if __name__ == "__main__":
    analyze_budget()