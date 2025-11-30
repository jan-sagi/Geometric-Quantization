import math
import csv
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: CERN DIAGNOSTIC SUITE
# =============================================================================
# AUTHOR: Jan Sagi
# DATE:   November 2025
# GOAL:   Reverse-engineer the topological rules by comparing the
#         Geometric Lattice against High-Precision CERN/PDG Data.
# =============================================================================

# Precision Settings
getcontext().prec = 100

class Constants:
    # AXIOMS (The Source Code)
    PI = Decimal("3.14159265358979323846264338327950288419716939937510")
    ALPHA_INV = Decimal("137.035999084")
    ALPHA = Decimal(1) / ALPHA_INV
    N = (Decimal(4) * PI).ln()

    # UNITS
    ME_TO_MEV = Decimal("0.510998950") # Electron mass in MeV

    # BASE SCALES (In Electron Mass Units)
    SCALE_LEPTON = Decimal(4) * PI * (N**3)
    SCALE_MESON  = ALPHA_INV
    SCALE_BARYON = PI**5

class PDG_Database:
    """
    Ground Truth Data from Particle Data Group (2024).
    Format: (Name, Mass_MeV, Uncertainty_MeV)
    """
    PARTICLES = [
        # LEPTONS
        ("Muon",        105.6583755, 0.0000023),
        ("Tau",         1776.86,     0.12),

        # LIGHT MESONS (Quark-Antiquark)
        ("Pion0",       134.9768,    0.0005),
        ("Pion+",       139.57039,   0.00018),
        ("Kaon+",       493.677,     0.016),
        ("Kaon0",       497.611,     0.013),
        ("Eta",         547.862,     0.017),
        ("Rho(770)",    775.26,      0.25),
        ("Omega(782)",  782.65,      0.12),
        ("Eta_prime",   957.78,      0.06),
        ("Phi(1020)",   1019.461,    0.016),

        # BARYONS (3 Quarks)
        ("Proton",      938.272088,  0.000000006), # Extreme precision
        ("Neutron",     939.565420,  0.000000005),
        ("Lambda",      1115.683,    0.006),
        ("Sigma+",      1189.37,     0.07),
        ("Sigma0",      1192.642,    0.024),
        ("Delta(1232)", 1232.0,      2.0),
        ("Xi-",         1321.71,     0.07),
        ("Omega-",      1672.45,     0.29),

        # HEAVY MESONS (Charm/Bottom)
        ("D+",          1869.66,     0.05),
        ("D_s+",        1968.35,     0.07),
        ("J/Psi",       3096.900,    0.006),
        ("B+",          5279.34,     0.12),
        ("Upsilon(1S)", 9460.30,     0.26),

        # BOSONS
        ("W Boson",     80377.0,     12.0),
        ("Z Boson",     91187.6,     2.1),
        ("Higgs",       125110.0,    140.0)
    ]

class TopologyDetective:
    def __init__(self):
        self.scales = {
            "LEPTON": Constants.SCALE_LEPTON,
            "MESON":  Constants.SCALE_MESON,
            "BARYON": Constants.SCALE_BARYON
        }
        self.results = []

    def analyze_particle(self, name, real_mass_mev):
        """
        Finds the best fitting Scale and Integer (k) for a real particle.
        Then calculates the 'Residual Topology' (the error pattern).
        """
        real_mass_me = Decimal(real_mass_mev) / Constants.ME_TO_MEV

        best_fit = None
        min_error = Decimal("Infinity")

        # 1. Scan all scales to find the 'Base Node'
        for scale_name, scale_val in self.scales.items():
            # Calculate ideal k
            k_float = real_mass_me / scale_val
            k_int = round(k_float)
            if k_int < 1: k_int = 1

            # Base Mass (pure integer geometry)
            base_mass = k_int * scale_val

            # Deviation
            diff = real_mass_me - base_mass
            rel_error = abs(diff) / real_mass_me

            if rel_error < min_error:
                min_error = rel_error

                # Calculate the Correction Factor needed to fix the error
                # Mass = Base * F  ->  F = Mass / Base
                f_needed = real_mass_me / base_mass

                # Analyze the correction in terms of Alpha
                # F = 1 + x*Alpha  ->  x = (F - 1) / Alpha
                alpha_units = (f_needed - 1) / Constants.ALPHA

                best_fit = {
                    "scale": scale_name,
                    "k": k_int,
                    "base_mev": float(base_mass * Constants.ME_TO_MEV),
                    "f_needed": float(f_needed),
                    "alpha_units": float(alpha_units)
                }

        return best_fit

    def run_diagnostics(self):
        print("======================================================================================================")
        print(" CERN DIAGNOSTIC SUITE: TOPOLOGY DECODER")
        print("======================================================================================================")
        print(" We look for the 'Alpha Units' (x).")
        print(" If x is close to an integer (1, 2, 5), it confirms a geometric rule.")
        print("------------------------------------------------------------------------------------------------------")
        print(f" {'PARTICLE':<12} | {'REAL (MeV)':<10} | {'SCALE':<8} | {'k':<3} | {'BASE (MeV)':<10} | {'ERROR %':<8} | {'ALPHA UNITS (x)'}")
        print("-" * 102)

        for name, mass, _ in PDG_Database.PARTICLES:
            fit = self.analyze_particle(name, mass)

            # Formatting
            k = fit['k']
            scale = fit['scale'].replace("_SCALE", "")
            err_pct = abs(fit['base_mev'] - mass) / mass * 100
            alpha_x = fit['alpha_units']

            # Highlighting patterns
            alpha_str = f"{alpha_x:+.2f} α"
            if abs(round(alpha_x) - alpha_x) < 0.1:
                alpha_str = f"\033[92m{alpha_x:+.2f} α\033[0m" # Green if close to integer
            elif abs(alpha_x) < 0.1:
                 alpha_str = f"\033[94m{alpha_x:+.2f} α\033[0m" # Blue if nearly zero (Proton)

            print(f" {name:<12} | {mass:<10.2f} | {scale:<8} | {k:<3} | {fit['base_mev']:<10.2f} | {err_pct:<8.2f} | {alpha_str}")

        print("-" * 102)
        print(" INTERPRETATION GUIDE:")
        print(" 1. ALPHA UNITS (x): This tells us the topological correction formula F = 1 + x*Alpha.")
        print("    - If x ≈ 0.00  -> Perfect Symmetry (Proton-like).")
        print("    - If x ≈ +1.00 -> Standard Stress (Meson-like).")
        print("    - If x ≈ +5.00 -> Spinor Stress (Tau-like).")
        print("    - If x ≈ +2.00 -> Sphere Stress (Muon-like, inverse).")
        print(" 2. Use these 'x' values to update the FractalPhysics class.")
        print("======================================================================================================")

if __name__ == "__main__":
    detective = TopologyDetective()
    detective.run_diagnostics()


    "
    jan@jan-OptiPlex-5040:~/Desktop/MyUniverse$ python CERN_Diagnostic_Suite.py
    ======================================================================================================
     CERN DIAGNOSTIC SUITE: TOPOLOGY DECODER
    ======================================================================================================
     We look for the 'Alpha Units' (x).
     If x is close to an integer (1, 2, 5), it confirms a geometric rule.
    ------------------------------------------------------------------------------------------------------
     PARTICLE     | REAL (MeV) | SCALE    | k   | BASE (MeV) | ERROR %  | ALPHA UNITS (x)
    ------------------------------------------------------------------------------------------------------
     Muon         | 105.66     | LEPTON   | 1   | 104.12     | 1.46     | +2.03 α
     Tau          | 1776.86    | LEPTON   | 17  | 1769.98    | 0.39     | +0.53 α
     Pion0        | 134.98     | MESON    | 2   | 140.05     | 3.76     | -4.96 α
     Pion+        | 139.57     | MESON    | 2   | 140.05     | 0.34     | -0.47 α
     Kaon+        | 493.68     | MESON    | 7   | 490.18     | 0.71     | +0.98 α
     Kaon0        | 497.61     | MESON    | 7   | 490.18     | 1.49     | +2.08 α
     Eta          | 547.86     | MESON    | 8   | 560.20     | 2.25     | -3.02 α
     Rho(770)     | 775.26     | MESON    | 11  | 770.28     | 0.64     | +0.89 α
     Omega(782)   | 782.65     | BARYON   | 5   | 781.88     | 0.10     | +0.14 α
     Eta_prime    | 957.78     | BARYON   | 6   | 938.25     | 2.04     | +2.85 α
     Phi(1020)    | 1019.46    | LEPTON   | 10  | 1041.16    | 2.13     | -2.86 α
     Proton       | 938.27     | BARYON   | 6   | 938.25     | 0.00     | +0.00 α
     Neutron      | 939.57     | BARYON   | 6   | 938.25     | 0.14     | +0.19 α
     Lambda       | 1115.68    | MESON    | 16  | 1120.40    | 0.42     | -0.58 α
     Sigma+       | 1189.37    | MESON    | 17  | 1190.43    | 0.09     | -0.12 α
     Sigma0       | 1192.64    | MESON    | 17  | 1190.43    | 0.19     | +0.25 α
     Delta(1232)  | 1232.00    | LEPTON   | 12  | 1249.40    | 1.41     | -1.91 α
     Xi-          | 1321.71    | MESON    | 19  | 1330.48    | 0.66     | -0.90 α
     Omega-       | 1672.45    | LEPTON   | 16  | 1665.86    | 0.39     | +0.54 α
     D+           | 1869.66    | LEPTON   | 18  | 1874.09    | 0.24     | -0.32 α
     D_s+         | 1968.35    | MESON    | 28  | 1960.71    | 0.39     | +0.53 α
     J/Psi        | 3096.90    | MESON    | 44  | 3081.11    | 0.51     | +0.70 α
     B+           | 5279.34    | MESON    | 75  | 5251.89    | 0.52     | +0.72 α
     Upsilon(1S)  | 9460.30    | MESON    | 135 | 9453.41    | 0.07     | +0.10 α
     W Boson      | 80377.00   | BARYON   | 514 | 80377.13   | 0.00     | -0.00 α
     Z Boson      | 91187.60   | MESON    | 1302 | 91172.88   | 0.02     | +0.02 α
     Higgs        | 125110.00  | BARYON   | 800 | 125100.59  | 0.01     | +0.01 α
    ------------------------------------------------------------------------------------------------------
     INTERPRETATION GUIDE:
     1. ALPHA UNITS (x): This tells us the topological correction formula F = 1 + x*Alpha.
        - If x ≈ 0.00  -> Perfect Symmetry (Proton-like).
        - If x ≈ +1.00 -> Standard Stress (Meson-like).
        - If x ≈ +5.00 -> Spinor Stress (Tau-like).
        - If x ≈ +2.00 -> Sphere Stress (Muon-like, inverse).
     2. Use these 'x' values to update the FractalPhysics class.
    ======================================================================================================
    jan@jan-OptiPlex-5040:~/Desktop/MyUniverse$
    "

