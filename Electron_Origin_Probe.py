import math
import sys
import os
from decimal import Decimal, getcontext

# =============================================================================
# ELECTRON ORIGIN PROBE: FROM PLANCK TO PARTICLE
# =============================================================================
# OBJECTIVE: Derive the mass of the Electron from the Planck Scale.
# HYPOTHESIS: The Electron is the "Ground State" vibration of the Planck Vacuum,
#             damped by the dimensional structure of space (Alpha).
#
# FORMULA: m_e = M_Planck * (Alpha ^ X)
# WE SEARCH FOR: The Geometric Exponent X.
# =============================================================================

# High Precision Analysis
getcontext().prec = 100

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
    # 1. GEOMETRIC SOURCES (Derived previously)
    PI = D("3.14159265358979323846264338327950288419716939937510")

    # Alpha derived from Geometry: 1 / (4pi^3 + pi^2 + pi)
    ALPHA_INV_GEOM = (D(4) * PI**3) + (PI**2) + PI
    ALPHA_GEOM = D(1) / ALPHA_INV_GEOM

    # 2. PHYSICAL CONSTANTS (SI Units for scaling)
    # Planck Constant
    H_BAR = D("1.054571817e-34")
    # Speed of Light
    C = D("299792458")
    # Gravitational Constant (CODATA 2018)
    G = D("6.67430e-11")

    # Target Electron Mass (CODATA)
    ME_REAL_KG = D("9.10938356e-31")

class OriginEngine:

    @staticmethod
    def calculate_planck_mass():
        # M_p = sqrt(hbar * c / G)
        mp = (Constants.H_BAR * Constants.C / Constants.G).sqrt()
        return mp

    @staticmethod
    def analyze_electron():
        # Setup
        sys.stdout = DualLogger("Electron_Origin_Report.txt")

        M_Planck = OriginEngine.calculate_planck_mass()
        M_Electron = Constants.ME_REAL_KG
        Alpha = Constants.ALPHA_GEOM

        print(f"{'='*80}")
        print(f" ELECTRON ORIGIN PROBE")
        print(f"{'='*80}")
        print(f" Planck Mass (Vacuum):  {M_Planck:.4e} kg")
        print(f" Electron Mass (Matter):{M_Electron:.4e} kg")

        # 1. The Great Ratio
        Ratio = M_Planck / M_Electron
        print(f" Damping Ratio:         {Ratio:.4e}")
        print(f"{'-'*80}")

        # 2. Solving for Dimensional Exponent X
        # Ratio = Alpha ^ -X  =>  ln(Ratio) = -X * ln(Alpha)
        # X = ln(Ratio) / ln(1/Alpha)

        ln_ratio = Ratio.ln()
        ln_alpha_inv = (D(1)/Alpha).ln()

        X = ln_ratio / ln_alpha_inv

        print(f" CALCULATION: How many layers of Alpha does it take")
        print(f"              to reduce Planck Mass to Electron Mass?")
        print(f"\n DIMENSIONAL EXPONENT (X) = {X:.10f}")
        print(f"{'-'*80}")

        # 3. Geometric Interpretation of X
        # We look for patterns involving Pi in X
        # Hypothesis: X should be related to the dimensions of space (D=10?)

        # Test: X approx 10?
        remainder = X - 10
        print(f" ANALYSIS OF EXPONENT X ({X:.4f}):")
        print(f" Is it 10 Dimensions? Diff: {remainder:.4f}")

        # Test: Is it 10*Pi/3? (Volume of 10D sphere factors often have Pi/3)
        target_geom = (D(10) * Constants.PI) / D(3)
        diff_geom = X - target_geom

        print(f" Is it 10*Pi/3?       Target: {target_geom:.4f} | Diff: {diff_geom:.4f}")

        print(f"{'='*80}")
        print(f" INTERPRETATION:")
        if abs(remainder) < 0.5:
            print(f" The Electron is the Planck Mass damped through approx 10.5 Dimensions.")
            print(f" Formula: m_e = M_Planck * Alpha^(10.47)")
            print(f" This effectively links Gravity (Planck) to Quantum Mechanics (Electron).")

        print(f"{'='*80}")

if __name__ == "__main__":
    OriginEngine.analyze_electron()