import sys
import time
import math
import re
from decimal import Decimal, getcontext

# =============================================================================
# THE SPEED OF GEOMETRY (Absolute Zero-Input Derivation)
# =============================================================================
# PHILOSOPHY:
#   "Meters" and "Seconds" are human artifacts.
#   The Universe only knows RATIOS.
#   The ultimate ratio is the Speed of Light relative to Matter (Electron).
#
#   c_natural = c / v_electron = 1 / Alpha
#
# GOAL:
#   Derive this Universal Speed Limit purely from the geometry of PI.
#   NO physical constants allowed (No h, No me, No R_inf).
# =============================================================================

# 1. EXTREME PRECISION (200 digits - Pure Mathematics)
getcontext().prec = 200

def D(val): return Decimal(str(val))

# --- LOGGER CLASS (Redirects output to Console + File) ---
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        # 1. Write to Console (with Colors)
        self.terminal.write(message)

        # 2. Write to File (Clean Text - remove ANSI color codes)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Formatting:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class PureGeometryEngine:
    def __init__(self):
        self.PI = self.generate_pi()

        # Target from Reality (CODATA 2018 Inverse Fine Structure Constant)
        # This is the MEASURED speed of light in atomic units.
        self.C_NATURAL_REAL = D("137.035999084")

    def generate_pi(self):
        """Chudnovsky Algorithm: Generating the Universe form Nothing."""
        print(f"{Formatting.BOLD}GENERATING PI (Ab Initio)...{Formatting.RESET}", end="")
        C = 426880 * Decimal(10005).sqrt()
        K, M, X, L, S = Decimal(6), Decimal(1), Decimal(1), Decimal(13591409), Decimal(13591409)
        for k in range(1, 200 // 14 + 1):
            M = (K**3 - 16*K) * M // (k**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12
        print(" DONE.")
        return C / S

    def run_derivation(self):
        print(f"\n{Formatting.BOLD}{'='*80}")
        print(f" THE SPEED OF GEOMETRY: ZERO-INPUT DERIVATION")
        print(f"{'='*80}{Formatting.RESET}")
        print(f" Logic: Speed of Light is the sum of Holographic Dimensions.")
        print(f" Formula: c_geom = 4π³ + π² + π")
        print("-" * 80)

        # --- 1. THE CALCULATION (Pure Geometry) ---
        # Volumetric (4pi^3) + Superficial (pi^2) + Linear (pi)

        term_3d = 4 * (self.PI**3)
        term_2d = self.PI**2
        term_1d = self.PI

        c_geometric = term_3d + term_2d + term_1d

        print(f"\n{Formatting.CYAN}[1] DIMENSIONAL SUMMATION{Formatting.RESET}")
        print(f"    4π³ (Volume):  {term_3d:.8f}...")
        print(f"    π²  (Surface): {term_2d:.8f}...")
        print(f"    π   (Line):    {term_1d:.8f}...")
        print(f"    --------------------------------")
        print(f"    SUM (c_geom):  {Formatting.BOLD}{c_geometric:.10f}...{Formatting.RESET}")

        # --- 2. THE COMPARISON (Reality Check) ---
        # We compare our Geometric C against the Measured C (in atomic units).

        diff = c_geometric - self.C_NATURAL_REAL

        # PPM Error (Parts Per Million)
        error_ppm = (abs(diff) / self.C_NATURAL_REAL) * 1000000

        print(f"\n{Formatting.CYAN}[2] REALITY CHECK (Natural Units){Formatting.RESET}")
        print(f"    Target (1/α):  {self.C_NATURAL_REAL:.10f} (CODATA 2018)")
        print(f"    Theory (π):    {c_geometric:.10f} (Pure Math)")

        print("-" * 80)
        print(f"    DIFFERENCE:    {diff:+.10f}")
        print(f"    PRECISION:     {Formatting.GREEN}{error_ppm:.4f} PPM{Formatting.RESET}")

        print(f"{'='*80}")
        print(f" {Formatting.YELLOW}INTERPRETATION:{Formatting.RESET}")
        print(f" In natural units, the Speed of Light is exactly {Formatting.BOLD}137.036...{Formatting.RESET}")
        print(f" It is not a speed in m/s. It is a GEOMETRIC RATIO.")
        print(f" It represents the ratio between the Lattice Geometry (Light) and the Node Geometry (Matter).")
        print(f"\n This calculation used ZERO physical inputs. Only π.")
        print(f"{'='*80}")

if __name__ == "__main__":
    # Setup Output Redirection
    sys.stdout = DualLogger("The_Speed_of_Geometry_Report.txt")

    engine = PureGeometryEngine()
    engine.run_derivation()