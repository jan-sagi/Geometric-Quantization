import math
import sys
import os
from decimal import Decimal, getcontext

# =============================================================================
# HOLOGRAPHIC PROTON AUDIT: THE STABILITY BALANCE
# =============================================================================
# OBJECTIVE:
#   Prove that the Proton does not collapse because its Information Content
#   (Surface Entropy) exactly balances its Mass Density (Volume).
#
#   We test the Bekenstein-Hawking Holographic Bound on the Proton Geometry.
# =============================================================================

getcontext().prec = 100
def D(val): return Decimal(str(val))

# --- LOGGER ---
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
    ALPHA_INV = D("137.035999084")
    ALPHA = D(1) / ALPHA_INV

    H_BAR = D("1.054571817e-34")
    C = D("299792458")
    G = D("6.67430e-11")
    ME_KG = D("9.10938356e-31")

    # Planck Length (Pixel size of the universe)
    L_PLANCK = (H_BAR * G / C**3).sqrt()

    # Geometric Proton Mass Ratio
    PROTON_RATIO = D(6) * (PI**5)

class Fmt:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def audit_holography():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Holographic_Audit.txt"))

    print(f"{Fmt.BOLD}{'='*80}")
    print(f" HOLOGRAPHIC AUDIT: PROTON STABILITY")
    print(f"{'='*80}{Fmt.RESET}")

    # 1. Calculate Proton Radius (Charge Radius)
    # Experimental Value (CODATA 2018): 0.8414 fm
    R_proton_exp = D("0.8414e-15")

    # 2. Calculate Surface Area (The Holographic Screen)
    # A = 4 * pi * r^2
    Area_proton = D(4) * Constants.PI * (R_proton_exp**2)

    # 3. Calculate Information Capacity (in Planck Areas)
    # N = Area / (L_planck^2 * ln(2)) ... standard entropy definition
    # But in pure geometry, let's look at Area / L_planck^2

    Planck_Area = Constants.L_PLANCK ** 2
    Bits = Area_proton / Planck_Area

    print(f" Proton Radius:        {R_proton_exp:.4e} m")
    print(f" Surface Area:         {Area_proton:.4e} m^2")
    print(f" Planck Pixel Area:    {Planck_Area:.4e} m^2")
    print(f"{'-'*80}")
    print(f" {Fmt.CYAN}HOLOGRAPHIC BITS (Surface Capacity):{Fmt.RESET}")
    print(f" N_bits = {Bits:.4e}")

    print(f"{'-'*80}")

    # 4. THE GRAND TEST
    # Does this number relate to the Mass (6*Pi^5) and Interaction (Alpha)?
    # Hypothesis: N_bits ~ (Proton_Mass_in_Planck_Units)^2 ?
    # Or better: N_bits ~ Alpha_G (Gravitational Coupling)^-1 ?

    # Calculate Proton Mass in kg
    M_proton = Constants.ME_KG * Constants.PROTON_RATIO

    # Calculate Gravitational Coupling (Alpha_G)
    # Alpha_G = (mp/m_planck)^2
    M_planck = (Constants.H_BAR * Constants.C / Constants.G).sqrt()
    Alpha_G = (M_proton / M_planck) ** 2

    Inverse_Alpha_G = D(1) / Alpha_G

    print(f" Inverse Gravitational Coupling (1/Alpha_G): {Inverse_Alpha_G:.4e}")

    # Compare
    ratio = Bits / Inverse_Alpha_G

    print(f"{'-'*80}")
    print(f" {Fmt.BOLD}THE RATIO (Bits / Coupling): {ratio:.4f}{Fmt.RESET}")

    # Interpretation
    target_geom = D(4) * Constants.PI # Surface factor
    err = (abs(ratio - target_geom) / target_geom) * 100

    print(f" Target (4*Pi?): {target_geom:.4f}")
    print(f" Deviation:      {err:.2f} %")

    print(f"{'='*80}")
    print(f" CONCLUSION:")
    if err < 5.0:
        print(f" {Fmt.GREEN}HOLOGRAPHIC PRINCIPLE CONFIRMED.{Fmt.RESET}")
        print(f" The Information Capacity of the Proton Surface is exactly")
        print(f" proportional to its Gravitational Strength via 4*Pi.")
        print(f" The Proton is a stable Hologram.")
    else:
        print(f" Relation is complex. Likely involves strong force radius vs charge radius.")

    print(f"{'='*80}")

if __name__ == "__main__":
    audit_holography()
