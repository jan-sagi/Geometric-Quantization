"""
THE GEOMETRIC UNIVERSE: DATA DISCOVERY (v9.0)
=============================================
High-Precision Geometric Scan with CSV Export

AUTHOR: Jan Sagi & AI Collaborator
DATE:   November 2024
LICENSE: MIT / Creative Commons (CC-BY 4.0)

OBJECTIVE:
1. Scan the geometric energy lattice (0 - MAX MeV) with 110-digit precision.
2. Compare against known particles.
3. EXPORT data to .csv for analysis in Excel/Calc.

DEPENDENCIES:
- Python 3.x
- Libraries: sys, math, decimal, csv
"""

import sys
import math
import csv
from decimal import Decimal, getcontext

# =============================================================================
# DEFAULT CONFIGURATION (Can be overridden by user input)
# =============================================================================
PRECISION_BITS = 110
DEFAULT_MAX_MEV = 30000
DEFAULT_FILENAME = "geometric_scan_results.csv"

# Apply precision settings
getcontext().prec = PRECISION_BITS

# =============================================================================
# CORE ENGINE
# =============================================================================

def D(val):
    return Decimal(str(val))

class Formatting:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"

class UniversalConstants:
    PI_STR = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647"
    PI = D(PI_STR)
    ALPHA_INV = D("137.035999084")
    ALPHA = D(1) / ALPHA_INV
    N = (D(4) * PI).ln()
    M_E_MEV = D("0.51099895000")

class GeometricScales:
    SCALES = {
        "LEPTON (N)":    lambda k: D(k) * (D(4) * UniversalConstants.PI * UniversalConstants.N**3),
        "MESON (A^-1)":  lambda k: D(k) * (D(1) / UniversalConstants.ALPHA),
        "BARYON (Pi^5)": lambda k: D(k) * (UniversalConstants.PI**5),
        "BOSON (A^-2)":  lambda k: D(k) * (UniversalConstants.PI * UniversalConstants.ALPHA**-2)
    }

class DiscoveryEngine:
    KNOWN_PARTICLES = [
        (0.511, "Electron"), (105.66, "Muon"), (1776.8, "Tau"),
        (134.98, "Pion0"), (139.57, "Pion+"), (493.67, "Kaon+"), (497.6, "Kaon0"),
        (547.86, "Eta"), (775.26, "Rho(770)"), (782.65, "Omega"), (957.78, "Eta_prime"),
        (1019.46, "Phi(1020)"), (1230, "a1(1260)"), (1275, "f2(1270)"),
        (1720, "f0(1710) Glueball?"),
        (938.27, "Proton"), (939.56, "Neutron"), (1115.68, "Lambda"),
        (1189.37, "Sigma+"), (1232.0, "Delta(1232)"), (1321.71, "Xi-"),
        (1385, "Sigma(1385)"), (1440, "Roper N(1440)"), (1520, "Lambda(1520)"),
        (1535, "N(1535)"), (1600, "Delta(1600)"), (1672.45, "Omega-"),
        (1710, "N(1710)"), (1720, "Sigma(1720)"),
        (1869.6, "D+"), (1968.3, "D_s+"), (2286.46, "Lambda_c"),
        (2645, "Xi_c(2645)"),
        (2983, "Eta_c"), (3096.9, "J/Psi"), (3686, "Psi(2S)"),
        (4430, "Z(4430) Tetraquark"),
        (5279.3, "B+"), (9460.3, "Upsilon(1S)"), (10023, "Upsilon(2S)"),
        (80379, "W Boson"), (91187, "Z Boson"), (125100, "Higgs"),
        (173000, "Top Quark")
    ]

    @staticmethod
    def is_prime(n):
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    @staticmethod
    def calculate_stability(scale, k):
        score = 0
        prime = DiscoveryEngine.is_prime(k)

        # Base Score
        if scale == "FUNDAMENTAL": return 100
        if "BARYON" in scale: score = 60
        if "MESON" in scale: score = 40
        if "LEPTON" in scale: score = 30
        if "BOSON" in scale: score = 50

        # Topology Bonus
        if prime: score += 30
        if k < 10: score += 20
        elif k > 100: score -= 40

        # Symmetry Bonus
        if k == 6 and "BARYON" in scale: score = 100
        if k == 1 and "LEPTON" in scale: score = 90

        return max(0, score)

    @staticmethod
    def scan(max_mev):
        nodes = []
        print(f"Scanning... (Limit: {max_mev} MeV, Precision: {PRECISION_BITS})")

        for scale_name, func in GeometricScales.SCALES.items():
            k = 1
            while True:
                mass_me = func(k)
                mass_mev = mass_me * UniversalConstants.M_E_MEV

                if mass_mev > max_mev: break

                stab = DiscoveryEngine.calculate_stability(scale_name, k)

                if stab > 20: # Minimum filter
                    # Check Match
                    match_name = ""
                    match_diff = 0.0
                    for km_mev, km_name in DiscoveryEngine.KNOWN_PARTICLES:
                        diff = float(abs(D(km_mev) - mass_mev) / mass_mev * 100)
                        if diff < 2.5:
                            match_name = km_name
                            match_diff = diff
                            break

                    status = "NOISE"
                    if match_name: status = "CONFIRMED"
                    elif stab >= 70: status = "PREDICTION"
                    elif stab >= 50: status = "RESONANCE"

                    nodes.append({
                        "mev": float(mass_mev),
                        "scale": scale_name,
                        "k": k,
                        "prime": DiscoveryEngine.is_prime(k),
                        "stability": stab,
                        "status": status,
                        "match": match_name,
                        "err": match_diff
                    })
                k += 1

        nodes.sort(key=lambda x: x["mev"])
        return nodes

def save_to_csv(filename, data):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Header
            writer.writerow(["Theory_MeV", "Scale_Type", "k_Node", "Is_Prime", "Stability_Score", "Status", "Match_Name", "Error_Percent"])

            # Data
            for row in data:
                writer.writerow([
                    f"{row['mev']:.4f}",
                    row['scale'],
                    row['k'],
                    row['prime'],
                    row['stability'],
                    row['status'],
                    row['match'],
                    f"{row['err']:.4f}" if row['match'] else ""
                ])
        print(f"\n{Formatting.GREEN}SUCCESS: Data saved to '{filename}'{Formatting.RESET}")
    except Exception as e:
        print(f"\n{Formatting.RED}ERROR: Could not save CSV. {e}{Formatting.RESET}")

def main():
    print(f"{Formatting.BOLD}GEOMETRIC UNIVERSE: DATA DISCOVERY ENGINE{Formatting.RESET}")
    print("-" * 50)

    # User Input
    try:
        user_max = input(f"Enter Max Energy in MeV [default {DEFAULT_MAX_MEV}]: ")
        max_scan = float(user_max) if user_max.strip() else DEFAULT_MAX_MEV

        user_file = input(f"Enter CSV Filename [default {DEFAULT_FILENAME}]: ")
        filename = user_file if user_file.strip() else DEFAULT_FILENAME
        if not filename.endswith(".csv"): filename += ".csv"

    except ValueError:
        print("Invalid input. Using defaults.")
        max_scan = DEFAULT_MAX_MEV
        filename = DEFAULT_FILENAME

    # Run Scan
    results = DiscoveryEngine.scan(max_scan)

    # Display Summary to Console (Top results only to avoid flooding)
    print(f"\n{Formatting.BLUE}--- TOP 20 SIGNIFICANT NODES (Preview) ---{Formatting.RESET}")
    print(f"{'MeV':<12} | {'Scale':<15} | {'k':<5} | {'Stab':<4} | {'Status'}")

    shown = 0
    for r in results:
        # Show confirmed or high predictions only in preview
        if r['status'] in ["CONFIRMED", "PREDICTION"] and shown < 20:
            color = Formatting.GREEN if r['status'] == "CONFIRMED" else Formatting.RED
            k_str = f"{r['k']}*" if r['prime'] else str(r['k'])
            print(f"{color}{r['mev']:<12.2f} | {r['scale']:<15} | {k_str:<5} | {r['stability']:<4} | {r['status']}{Formatting.RESET}")
            shown += 1

    print(f"... and {len(results) - shown} more records.")

    # Export
    save_to_csv(filename, results)

if __name__ == "__main__":
    main()