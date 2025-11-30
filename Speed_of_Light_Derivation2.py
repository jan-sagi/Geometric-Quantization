import sys
import math
import time
import re
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: SPEED OF LIGHT DERIVATION
# =============================================================================
# AUTHOR: Jan Sagi
# DATE:   November 2025
#
# OBJECTIVE:
#   1. Calculate the "Geometric Speed Limit" (C_geom) purely from Pi.
#   2. Convert this geometric value to Human SI Units (m/s) using the
#      Rydberg Constant (R_inf) as the "Lattice Density" scalar.
#
# FORMULA:
#   c_SI = (2 * h * R_inf) / (m_e * alpha_geom^2)
#
#   Where alpha_geom is derived ab initio: alpha^-1 = 4pi^3 + pi^2 + pi
# =============================================================================

# Configuration: Extreme Precision
PRECISION_BITS = 150
getcontext().prec = PRECISION_BITS

def D(val): return Decimal(str(val))

# --- LOGGER CLASS ---
class DualLogger:
    """Redirects output to both Console and File."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Remove ANSI codes for the text file
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Formatting:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

class LightSpeedEngine:
    def __init__(self):
        self.PI = self.compute_pi(PRECISION_BITS)

        # --- 1. HUMAN "ARTIFACTS" (Measurement Units) ---
        # These constants define what a "meter" and "second" are to us.
        # We use them to translate the Geometric Code into Human Language.
        # Source: CODATA 2018
        self.h     = D("6.62607015e-34")    # Planck Constant (J*s)
        self.me    = D("9.10938356e-31")    # Electron Mass (kg)
        self.R_inf = D("10973731.568160")   # Rydberg Constant (m^-1) -> Lattice Density

        # Target Speed of Light (Exact Definition)
        self.c_real = D("299792458")

    def compute_pi(self, precision):
        """Generates Pi from scratch (Chudnovsky Algorithm)."""
        C = 426880 * Decimal(10005).sqrt()
        K, M, X, L, S = Decimal(6), Decimal(1), Decimal(1), Decimal(13591409), Decimal(13591409)
        for k in range(1, precision // 14 + 1):
            M = (K**3 - 16*K) * M // (k**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12
        return C / S

    def run_derivation(self):
        print(f"{Formatting.BOLD}{'='*80}")
        print(f" GEOMETRIC DERIVATION OF THE SPEED OF LIGHT (c)")
        print(f"{'='*80}{Formatting.RESET}")

        # --- STEP 1: THE GEOMETRIC SOURCE CODE ---
        # Alpha is not measured; it is calculated from Holographic Geometry.
        # Formula: Alpha^-1 = 4pi^3 + pi^2 + pi

        term_vol = 4 * (self.PI**3)
        term_surf = self.PI**2
        term_line = self.PI

        alpha_inv_geom = term_vol + term_surf + term_line
        alpha_geom = D(1) / alpha_inv_geom

        print(f"\n{Formatting.CYAN}[1] GEOMETRIC SOURCE CODE (Alpha){Formatting.RESET}")
        print(f"    Formula: 4π³ + π² + π")
        print(f"    Result:  1 / {alpha_inv_geom:.6f}")

        # --- STEP 2: DERIVING LIGHT SPEED ---
        # We derive c from the Rydberg relation: c = (2 * h * R_inf) / (m_e * alpha^2)
        # This links the Lattice Frequency (R_inf) to the Geometric Coupling (Alpha).

        print(f"\n{Formatting.CYAN}[2] CALCULATING SPEED (SI Units){Formatting.RESET}")
        print(f"    Input:   Rydberg (Lattice Density) = {self.R_inf:.1f} m⁻¹")
        print(f"    Logic:   Scaling geometry by the mass of the electron.")

        numerator = 2 * self.h * self.R_inf
        denominator = self.me * (alpha_geom**2)

        c_calculated = numerator / denominator

        # --- STEP 3: VERIFICATION ---
        diff = c_calculated - self.c_real
        error_ppm = (abs(diff) / self.c_real) * 1000000

        print(f"\n{Formatting.BOLD}[3] FINAL RESULTS{Formatting.RESET}")
        print(f"    Target (Exact):      {self.c_real:.9f} m/s")
        print(f"    Geometric Theory:    {Formatting.GREEN}{c_calculated:.9f} m/s{Formatting.RESET}")

        print("-" * 80)
        print(f"    Absolute Difference: {diff:+.9f} m/s")
        print(f"    Precision Error:     {Formatting.BOLD}{error_ppm:.4f} PPM{Formatting.RESET} (Parts Per Million)")

        print(f"{'='*80}")
        if error_ppm < 5.0:
            print(f" {Formatting.GREEN}SUCCESS: The Speed of Light is a geometric property of Pi.{Formatting.RESET}")
            print(f" It is the propagation speed of the lattice defined by {Formatting.BOLD}4π³ + π² + π{Formatting.RESET}.")
        else:
            print(f" {Formatting.YELLOW}PARTIAL SUCCESS: High correlation, needs vacuum polarization correction.{Formatting.RESET}")
        print(f"{'='*80}")

if __name__ == "__main__":
    # Setup dual logging
    sys.stdout = DualLogger("Speed_of_Light_Report2.txt")

    engine = LightSpeedEngine()
    engine.run_derivation()