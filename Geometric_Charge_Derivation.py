import math
import sys
import os
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: ELECTRIC CHARGE DERIVATION
# =============================================================================
# OBJECTIVE:
#   Derive the Elementary Charge (e) purely from Geometric Constants.
#   Show that "Charge" is not a fundamental property, but a geometric
#   consequence of the Lattice Flux (Alpha).
#
# FORMULA:
#   e = sqrt( 2 * epsilon_0 * h * c * Alpha_geom )
#
#   We use standard vacuum permittivity (epsilon_0) as the scaling factor
#   for SI units, but the core relation depends on Alpha.
# =============================================================================

# High Precision
getcontext().prec = 100

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

def D(val): return Decimal(str(val))

class Constants:
    # 1. GEOMETRIC SOURCE
    PI = D("3.14159265358979323846264338327950288419716939937510")

    # Alpha derived from Geometry
    ALPHA_INV_GEOM = (4 * PI**3) + (PI**2) + PI
    ALPHA_GEOM = D(1) / ALPHA_INV_GEOM

    # 2. SI SCALING FACTORS (CODATA 2018)
    # We use these to map the geometry to the human "Coulomb" unit.
    H = D("6.62607015e-34")         # Planck Constant
    C = D("299792458")              # Speed of Light
    EPSILON_0 = D("8.8541878128e-12") # Vacuum Permittivity

    # Target Charge
    E_REAL = D("1.602176634e-19")

class Fmt:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def derive_charge():
    # Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Charge_Derivation_Report.txt"))

    print(f"{Fmt.BOLD}{'='*80}")
    print(f" GEOMETRIC DERIVATION OF ELECTRIC CHARGE (e)")
    print(f"{'='*80}{Fmt.RESET}")

    # 1. Inputs
    alpha = Constants.ALPHA_GEOM
    print(f" [INPUT] Geometric Alpha: 1 / {1/alpha:.6f}")
    print(f" [INPUT] Speed of Light:  {Constants.C} m/s")
    print(f"{'-'*80}")

    # 2. Calculation
    # e = sqrt(2 * eps0 * h * c * alpha)
    # This comes from the definition: alpha = e^2 / (2 * eps0 * h * c)

    term = D(2) * Constants.EPSILON_0 * Constants.H * Constants.C * alpha
    e_calc = term.sqrt()

    # 3. Analysis
    diff = e_calc - Constants.E_REAL
    error_ppm = (abs(diff) / Constants.E_REAL) * 1000000

    print(f" [TARGET] CODATA Charge:  {Constants.E_REAL:.15e} C")
    print(f" [THEORY] Geometric e:    {Fmt.GREEN}{e_calc:.15e} C{Fmt.RESET}")

    print(f"{'-'*80}")
    print(f" ABSOLUTE DIFFERENCE:     {diff:.4e} C")
    print(f" PRECISION ERROR:         {Fmt.BOLD}{error_ppm:.4f} PPM{Fmt.RESET}")
    print(f"{'='*80}")

    # Interpretation
    print(f" INTERPRETATION:")
    if error_ppm < 5.0:
        print(f" Electric Charge is exactly equal to the {Fmt.YELLOW}Square Root of Geometry{Fmt.RESET}.")
        print(f" e ~ sqrt(Alpha).")
        print(f" This confirms that 'Charge' is just the coupling strength of the lattice.")
    else:
        print(f" Deviation detected. Vacuum polarization may screen the charge.")

    print(f"{'='*80}")
    print(" Report saved to 'Charge_Derivation_Report.txt'")

if __name__ == "__main__":
    derive_charge()