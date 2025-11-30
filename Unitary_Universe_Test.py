import sys
import time
import math
import re
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: UNITARY EDITION (FIXED)
# =============================================================================
# TITLE:  Derivation of G and H0 without Proton Mass Input
# AUTHOR: Jan Sagi
# DATE:   November 2025
#
# GOAL:   To derive the Gravitational Constant (G) and Hubble Constant (H0)
#         without using the experimental proton mass as an input parameter.
#         Instead, we use the 'Baryon Scalar' (6*pi^5) as a geometric
#         complexity factor.
#
# OUTPUT: Console + File 'Unitary_Universe_Report.txt'
# =============================================================================

PRECISION_BITS = 150
getcontext().prec = PRECISION_BITS

def D(val): return Decimal(str(val))

class Formatting:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"

class DualLogger:
    """
    Redirects stdout to both the terminal (with colors) and a file (clean text).
    """
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Remove ANSI color codes for file output
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Universe:
    def __init__(self):
        # 1. GENERATE PI
        self.PI = self._compute_pi(PRECISION_BITS)

        # 2. SPACE GEOMETRY (Geometric Alpha)
        # Formula: alpha = 1 / (4pi^3 + pi^2 + pi)
        self.ALPHA_GEOM = D(1) / ((4 * self.PI**3) + (self.PI**2) + self.PI)

        # 3. UNITS (Electron and SI Constants only)
        # We remove Proton Mass from the input parameters.
        self.C = D("299792458")
        self.H_BAR = D("1.054571817e-34")
        self.ME_KG = D("9.10938356e-31")

        # 4. GEOMETRIC SCALAR (Gamma)
        # This is a pure number defining the complexity of matter (Proton).
        # It is NOT a mass in kg, but a geometric multiplier.
        self.SCALAR_BARYON = 6 * (self.PI**5)

        # 5. TARGET DATA (For Verification)
        self.G_REAL = D("6.67430e-11")
        self.H0_REAL = D("67.4")

    def _compute_pi(self, precision):
        """Compute Pi using Chudnovsky algorithm."""
        C = 426880 * Decimal(10005).sqrt()
        K, M, X, L, S = Decimal(6), Decimal(1), Decimal(1), Decimal(13591409), Decimal(13591409)
        for k in range(1, precision // 14 + 1):
            M = (K**3 - 16*K) * M // (k**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12
        return C / S

    def run_unitary_test(self):
        # Redirect output to file
        sys.stdout = DualLogger("Unitary_Universe_Report.txt")

        print(f"\n{Formatting.BOLD}=== UNITARY UNIVERSE TEST (FIXED) ==={Formatting.RESET}")
        print(f" Input: PI, Electron ($m_e$).")
        print(f" Scalar: $S_B = 6\\pi^5$ (Defines Matter Complexity)")
        print("-" * 60)

        # --- 1. GRAVITY (G) ---
        # G is derived from the electron mass and the geometric coupling.
        # Formula: G = (hc / me^2) * Alpha^(2X)

        # Dimensional Exponent X
        term1 = (10 * self.PI) / 3
        term2 = self.ALPHA_GEOM / (4 * self.PI)
        term3 = D(2).sqrt() * (self.ALPHA_GEOM**2)
        X_geom = term1 + term2 + term3

        # Pure Geometric Coupling (Electron-Space)
        alpha_G_pure = self.ALPHA_GEOM**(2 * X_geom)

        # Calculate G
        G_calc = (self.H_BAR * self.C / self.ME_KG**2) * alpha_G_pure
        err_G = (abs(G_calc - self.G_REAL) / self.G_REAL) * 100

        print(f"\n [1] GRAVITY (G)")
        print(f"     Calculated: {G_calc:.5e}")
        print(f"     CODATA:     {self.G_REAL:.5e}")
        print(f"     Error:      {Formatting.GREEN}{err_G:.4f} %{Formatting.RESET}")

        # --- 2. COSMOLOGY (H0) ---
        # We calculate the expansion rate of a "Baryonic Universe".

        # Step A: Radius of an 'Electronic Universe' (Hypothetical)
        # This represents a universe made only of light leptons.
        sphere_proj = self.ALPHA_GEOM / (2 * self.PI * (1 + 2*self.ALPHA_GEOM))
        R_univ_electronic = (self.H_BAR / (self.ME_KG * self.C)) * (1/alpha_G_pure) * sphere_proj

        # Step B: Baryonic Contraction (Real Universe)
        # The universe is filled with Baryons (Protons), which are S_B times more complex.
        # This complexity scales the fundamental ruler of the universe.
        # Resulting Scaling Factor: 1 / S_B

        R_univ_baryonic = R_univ_electronic / self.SCALAR_BARYON

        # Calculate H0 = c / R_univ
        mpc_km = D("3.08567758e19") # 1 Mpc in km
        H0_calc = (self.C / R_univ_baryonic) * mpc_km
        err_H0 = (abs(H0_calc - self.H0_REAL) / self.H0_REAL) * 100

        print(f"\n [2] COSMOLOGY (Hubble)")
        print(f"     Calculated: {Formatting.BOLD}{H0_calc:.2f}{Formatting.RESET} km/s/Mpc")
        print(f"     Planck:     {self.H0_REAL:.2f} km/s/Mpc")
        print(f"     Error:      {Formatting.GREEN}{err_H0:.2f} %{Formatting.RESET}")

        print("-" * 60)
        print(f" {Formatting.CYAN}MATHEMATICAL PROOF:{Formatting.RESET}")
        print(f" H0 is inversely proportional to 'Matter Complexity' ($6\\pi^5$).")
        print(f" The more complex the matter, the slower the expansion.")
        print("============================================================")
        print(" Report saved to 'Unitary_Universe_Report.txt'")

if __name__ == "__main__":
    test = Universe()
    test.run_unitary_test()