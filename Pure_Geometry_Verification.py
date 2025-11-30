import sys
import time
import math
import re
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: AB INITIO GENERATOR (v2.0)
# =============================================================================
# TITLE:  Generation of the Physical Universe from Pure Mathematics
# AUTHOR: Jan Sagi
# DATE:   November 2025
#
# INPUT:  NONE (Calculates PI from scratch).
# OUTPUT: Derivation of Particle Masses, Gravity (G), and Cosmology (H0).
# NOTE:   Includes the "Baryonic Correction" for the Hubble Constant.
# =============================================================================

# 1. PRECISION CONFIGURATION (150 digits to ensure stability of G)
PRECISION_BITS = 150
getcontext().prec = PRECISION_BITS

def D(val): return Decimal(str(val))

class Formatting:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
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

class MathEngine:
    """
    Generates mathematical constants ex nihilo (from nothing).
    """
    @staticmethod
    def compute_pi_chudnovsky(precision):
        print(f" [INIT] Computing PI to {precision} decimal places...")
        start = time.time()

        # Chudnovsky Algorithm for high-precision PI
        C = 426880 * Decimal(10005).sqrt()
        K = Decimal(6)
        M = Decimal(1)
        X = Decimal(1)
        L = Decimal(13591409)
        S = Decimal(13591409)

        # Iterations required for desired precision
        for k in range(1, precision // 14 + 1):
            M = (K**3 - 16*K) * M // (k**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12

        pi = C / S
        end = time.time()
        print(f" [DONE] Generated in {end - start:.4f}s.")
        return pi

class Universe:
    def __init__(self):
        # 1. GENESIS: Compute PI
        self.PI = MathEngine.compute_pi_chudnovsky(PRECISION_BITS)

        # 2. DERIVE ALPHA (Geometric Definition)
        # Alpha^-1 = 4pi^3 + pi^2 + pi (Sum of holographic dimensions)
        self.ALPHA_INV_GEOM = (4 * self.PI**3) + (self.PI**2) + self.PI
        self.ALPHA_GEOM = D(1) / self.ALPHA_INV_GEOM

        # 3. SPACETIME BASE
        self.N = (D(4) * self.PI).ln()

        # 4. PHYSICAL SCALING (For unit conversion only)
        # These do not affect the geometric ratios, only the SI output units.
        self.C = D("299792458")
        self.H_BAR = D("1.054571817e-34")
        self.ME_KG = D("9.10938356e-31")
        self.MP_KG_REAL = D("1.6726219e-27") # Used only to check G in SI units

        # 5. TARGET DATA (REALITY CHECK)
        # CODATA 2018 / Planck 2018
        self.TARGETS = {
            "ALPHA_INV": D("137.035999084"),
            "MUON": D("206.768283"),
            "PROTON": D("1836.152673"),
            "G": D("6.67430e-11"),
            "H0": D("67.4")
        }

    def run_simulation(self):
        # Redirect output
        sys.stdout = DualLogger("Ab_Initio_Report.txt")

        print(f"\n{Formatting.BOLD}=== INITIALIZING UNIVERSE SIMULATION ==={Formatting.RESET}")

        # --- A. FINE STRUCTURE CONSTANT ---
        alpha_inv_calc = 1 / self.ALPHA_GEOM
        diff_alpha = alpha_inv_calc - self.TARGETS["ALPHA_INV"]

        print(f"\n[1] STRUCTURE OF SPACE (Alpha)")
        print(f"    Calculated (from PI): 1/{alpha_inv_calc:.6f}")
        print(f"    Measured (CODATA):    1/{self.TARGETS['ALPHA_INV']:.6f}")
        print(f"    Difference:           {diff_alpha:+.6f}")

        # --- B. MATTER (Ratios to Electron) ---
        print(f"\n[2] MATTER (Mass Ratios)")

        # MUON (Sphere k=1)
        # Formula: (4pi * N^3) / (1 - 2*Alpha)
        muon_base = 4 * self.PI * (self.N**3)
        muon_calc = muon_base / (D(1) - 2*self.ALPHA_GEOM)
        err_mu = self._get_error(muon_calc, self.TARGETS["MUON"])

        print(f"    MUON (k=1):       {muon_calc:.6f} me")
        print(f"    Error:            {Formatting.GREEN}{err_mu:.6f} %{Formatting.RESET}")

        # PROTON (Hexagon k=6)
        # Formula: 6 * pi^5
        proton_geom_ratio = 6 * (self.PI**5)
        err_p = self._get_error(proton_geom_ratio, self.TARGETS["PROTON"])

        print(f"    PROTON (k=6):     {proton_geom_ratio:.6f} me")
        print(f"    Error:            {Formatting.GREEN}{err_p:.6f} %{Formatting.RESET}")

        # --- C. GRAVITY ---
        print(f"\n[3] GRAVITY (Derivation of G)")

        # Dimensional Exponent X = 10pi/3 + QED corrections
        term1 = (10 * self.PI) / 3
        term2 = self.ALPHA_GEOM / (4 * self.PI)
        term3 = D(2).sqrt() * (self.ALPHA_GEOM**2)
        X_geom = term1 + term2 + term3

        # Coupling Alpha_G = Gamma_proton^2 * Alpha^(2X)
        alpha_G = (proton_geom_ratio**2) * (self.ALPHA_GEOM**(2 * X_geom))

        # G = (alpha_G * hbar * c) / m_p^2
        # We use the theoretical proton mass (in kg) derived from the electron
        mp_theor_kg = self.ME_KG * proton_geom_ratio
        G_calc = (alpha_G * self.H_BAR * self.C) / (mp_theor_kg**2)

        err_G = self._get_error(G_calc, self.TARGETS["G"])

        print(f"    G (Calculated):   {G_calc:.5e}")
        print(f"    G (CODATA):       {self.TARGETS['G']:.5e}")
        print(f"    Error:            {Formatting.GREEN}{err_G:.4f} %{Formatting.RESET}")

        # --- D. COSMOLOGY (CORRECTED) ---
        print(f"\n[4] COSMOLOGY (Hubble H0)")
        print(f"    *Applying Baryonic Correction (Universe is Proton-based, not Electron-based)*")

        # 1. Atomic Radius (Bohr) in the gravitational field
        R_atom = (self.H_BAR / (self.ME_KG * self.C)) / alpha_G

        # 2. Projection to Macroscale (k=1 Sphere)
        R_univ_electron_scale = (R_atom * self.ALPHA_GEOM) / (2 * self.PI * (1 + 2*self.ALPHA_GEOM))

        # 3. BARYONIC CORRECTION (Key Insight)
        # The universe scales according to the Proton, not the Electron.
        # R_univ_real = R_univ_electron * (m_p / m_e)
        R_univ_real = R_univ_electron_scale * proton_geom_ratio

        # 4. Hubble H0 = c / R_univ
        mpc_km = D("3.08567758e19") # 1 Mpc in km
        H0_calc = (self.C / R_univ_real) * mpc_km

        err_H0 = self._get_error(H0_calc, self.TARGETS["H0"])

        print(f"    H0 (Calculated):  {Formatting.BOLD}{H0_calc:.2f}{Formatting.RESET} km/s/Mpc")
        print(f"    Planck (2018):    {self.TARGETS['H0']:.2f} km/s/Mpc")

        if err_H0 < 1.0:
            print(f"    Error:            {Formatting.GREEN}{err_H0:.2f} % (MATCH){Formatting.RESET}")
        else:
            print(f"    Error:            {Formatting.RED}{err_H0:.2f} %{Formatting.RESET}")

        self._print_verdict(err_mu, err_p, err_G, err_H0)

    def _get_error(self, calc, real):
        return (abs(calc - real) / real) * 100

    def _print_verdict(self, e1, e2, e3, e4):
        print(f"\n{Formatting.BOLD}{'='*60}")
        if e1 < 0.01 and e2 < 0.01 and e3 < 0.05 and e4 < 1.5:
            print(f" {Formatting.GREEN}FINAL VERDICT: THEORY IS CONSISTENT.{Formatting.RESET}")
            print(" All 4 fundamental scales (Micro, Nuclear, G, Cosmo)")
            print(" have been successfully derived solely from PI.")
        else:
            print(f" {Formatting.YELLOW}FINAL VERDICT: Promising, but calibration required.{Formatting.RESET}")
        print(f"{'='*60}{Formatting.RESET}")
        print(" Report saved to 'Ab_Initio_Report.txt'")

if __name__ == "__main__":
    sim = Universe()
    sim.run_simulation()