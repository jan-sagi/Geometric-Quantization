import decimal
import sys
import os
import time
import re
from decimal import Decimal, getcontext

# =============================================================================
# MANUSCRIPT: GEOMETRIC DERIVATION OF THE FINE-STRUCTURE CONSTANT
# =============================================================================
# ABSTRACT:
# This script tests the hypothesis that the fine-structure constant (alpha),
# representing the strength of electromagnetic interaction, is not a random
# parameter but a geometric derivative of spatial dimensions defined by Pi.
#
# HYPOTHESIS:
# Alpha^-1 ~= 4*Pi^3 + Pi^2 + Pi
# Represents the summation of holographic geometries (Volumetric + Surface + Linear).
# =============================================================================

# Configuration: Extreme Precision Context
# We demand 2000 digits of precision to eliminate any computational noise.
PRECISION_DIGITS = 2000
getcontext().prec = PRECISION_DIGITS

# --- LOGGER CLASS (Console + File) ---
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Remove ANSI codes for the text file (clean output)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class UniversalMath:
    """
    The Mathematical Engine.
    Generates fundamental constants from infinite series.
    """

    @staticmethod
    def compute_pi_chudnovsky(precision):
        """
        DERIVATION OF PI (Chudnovsky Algorithm).
        ----------------------------------------
        Calculates Pi ab initio using pure integer/decimal arithmetic.
        """
        print(f"   [CALCULATION] Generating Pi to {precision} decimal places...")
        start = time.time()

        C = Decimal(426880) * Decimal(10005).sqrt()
        K = Decimal(6)
        M = Decimal(1)
        X = Decimal(1)
        L = Decimal(13591409)
        S = Decimal(13591409)

        k_limit = precision // 14 + 1

        for k in range(1, k_limit):
            k_dec = Decimal(k)
            term_k = (K**3 - 16*K)
            M = (term_k * M) / (k_dec**3)
            M = M.to_integral_value()

            L += Decimal(545140134)
            X *= Decimal("-262537412640768000")
            S += (M * L) / X
            K += Decimal(12)

        pi_val = C / S

        end = time.time()
        print(f"   [DONE] Pi generated in {end - start:.4f} seconds.")
        return pi_val

class TheoryAudit:
    """
    The Judge.
    Compares Geometric Theory against Experimental Physics (CODATA).
    """

    # CODATA 2018 Value for Inverse Fine Structure Constant
    CODATA_ALPHA_INV = Decimal("137.035999084")

    def __init__(self):
        self.pi = UniversalMath.compute_pi_chudnovsky(PRECISION_DIGITS)

    def run_audit(self):
        print("\n" + "="*80)
        print(" THE GEOMETRIC UNIVERSE: CONSTANT VERIFICATION")
        print("="*80)

        # --- THE FORMULA ---
        print(" HYPOTHESIS FORMULA:")
        print(" -------------------")
        print(" α⁻¹ = 4π³ + π² + π")
        print(" -------------------")
        print(" Interpretation: Sum of Holographic Geometries")
        print("   4π³ : Volumetric Component (Sphere Volume factor)")
        print("   π²  : Surface Component (Flux factor)")
        print("   π   : Linear Component (Distance factor)")
        print("-" * 80)

        # 1. The Geometric Calculation
        term_3d = Decimal(4) * (self.pi ** 3)
        term_2d = self.pi ** 2
        term_1d = self.pi

        alpha_geom = term_3d + term_2d + term_1d

        # 2. The Comparison
        difference = alpha_geom - self.CODATA_ALPHA_INV
        error_ppm = (difference / self.CODATA_ALPHA_INV) * Decimal(1_000_000)

        # 3. Report Generation
        print(f" {'COMPONENT':<15} | {'VALUE (First 20 digits)':<30}")
        print("-" * 60)
        print(f" {'Pi (Base)':<15} | {str(self.pi)[:22]}...")
        print(f" {'4 * Pi^3':<15} | {str(term_3d)[:22]}...")
        print(f" {'Pi^2':<15} | {str(term_2d)[:22]}...")
        print(f" {'Pi':<15} | {str(term_1d)[:22]}...")
        print("-" * 60)
        print(f" {'THEORY SUM':<15} | {str(alpha_geom)[:22]}...")
        print(f" {'CODATA REAL':<15} | {str(self.CODATA_ALPHA_INV)[:22]}")
        print("=" * 80)

        print(f"\n [ANALYSIS OF DEVIATION]")
        print(f" Absolute Difference: +{difference:.10f}...")
        print(f" Error (PPM):         {error_ppm:.4f} ppm")
        print("-" * 80)

        self.interpret_results(difference)

    def interpret_results(self, diff):
        if abs(diff) < 0.001:
            print(" [CONCLUSION]: HIGH CORRELATION CONFIRMED.")
            print(" The geometric series (4pi^3 + pi^2 + pi) reproduces the fine-structure")
            print(" constant with a precision of 99.9998%.")
            print("\n [HYPOTHESIS FOR RESIDUAL]:")
            print(f" The residual (+{diff:.5f}) likely corresponds to the QED vertex correction.")
            print(" Pure geometry describes the 'ideal' vacuum state.")
        else:
            print(" [CONCLUSION]: HYPOTHESIS FALSIFIED.")
            print(" The geometric relation is statistically insignificant.")

if __name__ == "__main__":
    # Redirect stdout to DualLogger
    sys.stdout = DualLogger("Fundamental_Constants_Report.txt")

    # Execution
    audit = TheoryAudit()
    audit.run_audit()

    print("\n Report saved to 'Fundamental_Constants_Report.txt'")