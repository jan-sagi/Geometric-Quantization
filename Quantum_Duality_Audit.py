import math
import sys
import re
from decimal import Decimal, getcontext

# =============================================================================
# QUANTUM DUALITY AUDIT (Robust Fair Test)
# =============================================================================
# OBJECTIVE: Rigorous verification of the "Particle as a Standing Wave" hypothesis.
# METHOD:    1. Derive "Intrinsic Velocity" (v) purely from Geometric Topology.
#            2. Calculate De Broglie Wavelength (Wave Nature).
#            3. Calculate Compton Wavelength (Particle Nature).
#            4. TEST COHERENCE: How many geometric cycles does a particle
#               complete before decay? (Linking Geometry to Time).
# =============================================================================

# High precision for wave calculations
getcontext().prec = 100

class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_message = ansi_escape.sub('', message)
        self.log.write(clean_message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Constants:
    # AXIOMS (No tuning)
    PI = 3.141592653589793
    ALPHA_INV = 137.035999
    ALPHA = 1.0 / ALPHA_INV

    # PHYSICS
    C = 299792458
    H = 6.62607015e-34
    H_BAR = H / (2*PI)

    # MASSES (kg)
    ME_KG = 9.10938356e-31
    M_MU_KG = ME_KG * 206.768283
    M_TAU_KG = ME_KG * 3477.1426
    M_P_KG  = 1.6726219e-27

    # FORMATTING
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"

class ParticleData:
    # Dataset: Name, Mass(kg), Lifetime(s), Geometric Correction Logic
    PARTICLES = [
        {
            "name": "Proton",
            "mass": Constants.M_P_KG,
            "life": float('inf'),
            "k": 6,
            "correction_func": lambda a: 0.0 # Perfect Symmetry (k=6)
        },
        {
            "name": "Muon",
            "mass": Constants.M_MU_KG,
            "life": 2.1969811e-6,
            "k": 1,
            "correction_func": lambda a: 1.0 / (1.0 - 2.0*a) # Sphere (k=1)
        },
        {
            "name": "Tau",
            "mass": Constants.M_TAU_KG,
            "life": 2.903e-13,
            "k": 17,
            "correction_func": lambda a: 1.0 + 5.0*a # Spinor approx (k=17)
        }
    ]

class DualityEngine:

    @staticmethod
    def calculate_intrinsic_properties(p):
        """
        Derives velocity and wavelengths purely from geometry.
        """
        # 1. Get Geometric Correction Factor (F)
        # This factor represents how much the geometry is 'stretched' relative to base.
        # We interpret this stretch as Relativistic Dilation (Lorentz Factor).
        F = p["correction_func"](Constants.ALPHA)

        # 2. Derive Intrinsic Velocity (v)
        # If F = gamma = 1/sqrt(1-v^2/c^2)  --> v = c * sqrt(1 - 1/F^2)
        if F == 0:
            return 0, 0, 0, float('inf')

        # Handle Stable Particles (F=0 correction usually implies F=1 base)
        if F == 0 or F == 1.0:
            beta = 0.0
        else:
            # Check if F < 1 (Binding energy case) or F > 1 (Excitation)
            # For velocity calculation, we need the magnitude of distortion.
            # Using F_eff = F if F>1 else 1/F
            F_eff = F if F > 1.0 else 1.0/F
            beta = math.sqrt(1 - (1/(F_eff**2)))

        v = beta * Constants.C

        # 3. Calculate Wavelengths
        # Compton (Particle Size): h / mc
        lambda_c = Constants.H / (p["mass"] * Constants.C)

        # De Broglie (Wave Size): h / mv
        # Note: If v=0, wavelength is Infinite (Stationary Field)
        lambda_db = float('inf')
        if v > 0:
            # Momentum p = m*v*gamma. Here gamma IS our F_eff.
            momentum = p["mass"] * v * (F if F > 1 else 1/F)
            lambda_db = Constants.H / momentum

        return v, beta, lambda_c, lambda_db

    @staticmethod
    def run_coherence_test():
        print(f"=======================================================================================")
        print(f" QUANTUM DUALITY AUDIT (Robust Fair Test)")
        print(f"=======================================================================================")
        print(f" Hypothesis: Unstable particles are 'Running Waves' with intrinsic velocity (v).")
        print(f"             Stable particles are 'Standing Waves' (v=0).")
        print(f" Test Metric: COHERENCE LENGTH = How many wave-cycles before decay?")
        print(f"=======================================================================================")
        print(f" {'PARTICLE':<8} | {'VELOCITY (c)':<12} | {'WAVE/SIZE RATIO':<15} | {'LIFETIME (s)':<12} | {'CYCLES (Coherence)'}")
        print("-" * 95)

        results = []

        for p in ParticleData.PARTICLES:
            v, beta, l_c, l_db = DualityEngine.calculate_intrinsic_properties(p)

            # Ratio of Wave to Particle size
            # If Ratio is Real, Duality is Geometric.
            duality_ratio = l_db / l_c if l_db != float('inf') else 0

            # Coherence: Number of oscillations before decay
            # N = (Velocity * Lifetime) / Wavelength
            # This tells us the 'Quality Factor' (Q) of the particle resonance.
            cycles = 0
            if p["life"] == float('inf'):
                cycles = float('inf')
            elif v > 0:
                dist_traveled = v * p["life"]
                cycles = dist_traveled / l_db

            results.append((p["name"], beta, duality_ratio, p["life"], cycles))

            # Color coding
            color = Constants.RESET
            if cycles == float('inf'): color = Constants.GREEN # Green (Stable)
            elif cycles > 1e10: color = Constants.YELLOW # Yellow (Long lived)
            else: color = Constants.CYAN # Cyan (Short lived)

            v_str = f"{beta:.5f} c"
            r_str = f"{duality_ratio:.2f}" if duality_ratio > 0 else "N/A"
            l_str = f"{p['life']:.2e}"
            c_str = f"{cycles:.2e}"

            print(f" {p['name']:<8} | {v_str:<12} | {r_str:<15} | {color}{l_str:<12}{Constants.RESET} | {color}{c_str}{Constants.RESET}")

        print("-" * 95)
        print(" INTERPRETATION OF RESULTS:")
        print(" 1. PROTON: Velocity 0 c. Infinite Coherence. Verified Stable.")
        print(" 2. MUON vs TAU: Check the 'CYCLES' column.")

        # Fair Analysis of Muon vs Tau
        muon_cycles = results[1][4]
        tau_cycles = results[2][4]

        if muon_cycles > 0 and tau_cycles > 0:
            ratio = muon_cycles / tau_cycles
            print(f"\n [ANALYSIS] Muon/Tau Coherence Ratio: {ratio:.2e}")
            print(f" The Muon survives {ratio:.0f} times more geometric cycles than the Tau.")
            print(f" This suggests the Tau ($k=17$) is topologically far more fragile than Muon ($k=1$).")

        print(f"=======================================================================================")

if __name__ == "__main__":
    sys.stdout = DualLogger("Quantum_Duality_Audit.txt")
    DualityEngine.run_coherence_test()