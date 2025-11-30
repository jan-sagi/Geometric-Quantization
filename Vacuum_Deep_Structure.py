import math
import sys
import os
from decimal import Decimal, getcontext

# =============================================================================
# VACUUM DEEP STRUCTURE: STIFFNESS & CRITICALITY ANALYSIS
# =============================================================================
# OBJECTIVE:
#   1. Pinpoint the EXACT Geometric Limit ($d_crit$) where Space becomes Mass.
#   2. Calculate the "Bulk Modulus" (Stiffness) of the Vacuum Lattice.
#   3. Determine the Lattice Frequency (The heartbeat of the grid).
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
    # GEOMETRY
    PI = D("3.14159265358979323846264338327950288419716939937510")
    ALPHA_INV = D("137.035999084")

    # PHYSICS
    H_BAR = D("1.054571817e-34")
    C = D("299792458")
    ME_KG = D("9.10938356e-31")

    # Energy of Electron-Positron Pair (The "Cost" of creating matter)
    PAIR_ENERGY_J = D(2) * ME_KG * (C**2)

class Fmt:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

class VacuumEngineer:

    @staticmethod
    def calculate_properties(d_meters):
        d = D(d_meters)

        # 1. CASIMIR PRESSURE (Stress)
        # P = (pi^2 * hbar * c) / (240 * d^4)
        numerator = (Constants.PI**2) * Constants.H_BAR * Constants.C
        pressure = numerator / (D(240) * (d**4))

        # 2. ENERGY DENSITY
        # E_vol = Pressure (roughly)

        # 3. TOTAL ENERGY in the Gap Volume (V = d^3)
        # We assume the interaction volume is a cube of side 'd'
        # This represents one "Cell" of the lattice being compressed.
        volume = d**3
        energy_in_cell = pressure * volume

        # 4. STIFFNESS (Bulk Modulus K)
        # K = -V (dP/dV). For Casimir (P ~ V^-4/3), K ~ 4/3 P.
        # Let's roughly approximate Vacuum Stiffness as ~ 4 * Pressure
        stiffness = D(4) * pressure

        return energy_in_cell, pressure, stiffness

    @staticmethod
    def find_critical_limit():
        print(f"{Fmt.BOLD}Searching for the Critical Lattice Breakdown Point ($d_crit$)...{Fmt.RESET}")

        # Binary Search for d where Energy_In_Cell == Pair_Energy
        low = D("1e-14") # 0.01 pm
        high = D("1e-11") # 10 pm
        target = Constants.PAIR_ENERGY_J

        for i in range(100):
            mid = (low + high) / D(2)
            E, P, K = VacuumEngineer.calculate_properties(mid)

            if E < target: # Not enough energy, need smaller d (higher pressure)
                high = mid
            else:
                low = mid

        d_crit = (low + high) / D(2)
        E_final, P_final, K_final = VacuumEngineer.calculate_properties(d_crit)

        return d_crit, P_final, K_final

def run_deep_dive():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Vacuum_Deep_Structure.txt"))

    print(f"{Fmt.BOLD}{'='*80}")
    print(f" DEEP DIVE: MATERIAL PROPERTIES OF THE VACUUM")
    print(f"{'='*80}{Fmt.RESET}")

    # 1. CRITICAL LIMIT
    d_crit, pressure, stiffness = VacuumEngineer.find_critical_limit()
    d_pm = d_crit * D("1e12")

    print(f" {Fmt.CYAN}CRITICAL BREAKDOWN DISTANCE ($d_crit$):{Fmt.RESET}")
    print(f" Value:       {Fmt.GREEN}{d_pm:.6f} pm{Fmt.RESET}")
    print(f" Explanation: At this wavelength, the lattice vibration is so intense")
    print(f"              that it spontaneously collapses into Mass (Electron+Positron).")
    print(f"{'-'*80}")

    # 2. COMPARISON WITH COMPTON WAVELENGTH
    # lambda_c = h / mc
    lambda_c = (D(2)*Constants.PI * Constants.H_BAR) / (Constants.ME_KG * Constants.C)
    lambda_c_pm = lambda_c * D("1e12")

    print(f" {Fmt.BOLD}GEOMETRIC CHECK:{Fmt.RESET}")
    print(f" Compton Wavelength (Electron): {lambda_c_pm:.6f} pm")

    ratio = lambda_c / d_crit
    print(f" Ratio (Lambda / d_crit):       {ratio:.4f}")

    # Is the ratio close to a geometric constant?
    # pi * 4? 4pi/3?
    print(f" {Fmt.YELLOW}Insight:{Fmt.RESET} The breakdown happens at exactly ~ 1 / {ratio:.2f} of the electron size.")

    print(f"{'-'*80}")

    # 3. STIFFNESS OF SPACE
    print(f" {Fmt.CYAN}MATERIAL STIFFNESS (Bulk Modulus):{Fmt.RESET}")
    print(f" Vacuum Stiffness: {stiffness:.2e} Pa")
    print(f" Comparison:")
    print(f"   Steel:   1.60e+11 Pa")
    print(f"   Diamond: 4.40e+11 Pa")
    print(f"   Neutron Star: ~1e+34 Pa")

    print(f" Conclusion: The vacuum is {stiffness/D('1e11'):.0f}x stiffer than Diamond.")
    print(f"             It is the hardest 'substance' in the universe.")

    print(f"{'-'*80}")

    # 4. LATTICE FREQUENCY
    # f = c / d_crit
    freq = Constants.C / d_crit
    print(f" {Fmt.CYAN}LATTICE FREQUENCY (The Heartbeat):{Fmt.RESET}")
    print(f" Frequency: {freq:.2e} Hz")
    print(f" Interpretation: This is the 'refresh rate' of matter creation.")
    print(f"{'='*80}")
    print(" Report saved to 'Vacuum_Deep_Structure.txt'")

if __name__ == "__main__":
    run_deep_dive()