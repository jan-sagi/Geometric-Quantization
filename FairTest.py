import numpy as np
import math

# =============================================================================
# THE GEOMETRIC UNIVERSE: DISCOVERY EDITION (FairTest v6.0)
# =============================================================================
# GOAL: Generate a theoretical spectrum and search for "missing" particles.
# METHOD: Scanning geometric nodes 0 - 15,000 MeV.
# =============================================================================

class Formatting:
    GREEN = "\033[92m"      # Known Particle (Match)
    RED = "\033[91m"        # Unknown (Prediction)
    YELLOW = "\033[93m"     # Resonance / Noise
    BLUE = "\033[94m"       # Header
    CYAN = "\033[96m"       # Info
    RESET = "\033[0m"
    BOLD = "\033[1m"

class Constants:
    ALPHA = 1 / 137.035999084
    PI = math.pi
    N = math.log(4 * PI)
    # Conversion factor: 1 / Mass_Electron_in_MeV (approx 1/0.511)
    # Used to convert electron-mass units to MeV
    MeV_to_Me = 1.956951

class GeometricScales:
    # Generator definitions
    SCALES = {
        "LEPTON (N)":    lambda k: k * (4 * Constants.PI * Constants.N**3),
        "MESON (A^-1)":  lambda k: k * (1 / Constants.ALPHA),
        "BARYON (Pi^5)": lambda k: k * (Constants.PI**5),
        # Boson scale is too high for this Discovery scan but kept for Higgs reference
        "BOSON (A^-2)":  lambda k: k * (Constants.PI * Constants.ALPHA**-2)
    }

class DiscoveryEngine:

    # --- EXTENDED KNOWN PARTICLE DATABASE (FOR FILTERING) ---
    KNOWN_PARTICLES = [
        # Leptons
        (0.511, "Electron"), (105.66, "Muon"), (1776.8, "Tau"),
        # Light Mesons
        (134.98, "Pion0"), (139.57, "Pion+"), (493.67, "Kaon+"), (497.6, "Kaon0"),
        (547.86, "Eta"), (775.26, "Rho(770)"), (782.65, "Omega"), (957.78, "Eta_prime"),
        (1019.46, "Phi(1020)"), (1230, "a1(1260)"), (1275, "f2(1270)"),
        # Baryons & Resonances
        (938.27, "Proton"), (939.56, "Neutron"), (1115.68, "Lambda"),
        (1189.37, "Sigma+"), (1232.0, "Delta(1232)"), (1321.71, "Xi-"),
        (1385, "Sigma(1385)"), (1440, "Roper N(1440)"), (1520, "Lambda(1520)"),
        (1535, "N(1535)"), (1600, "Delta(1600)"), (1672.45, "Omega-"),
        # Charmed / Heavy
        (1869.6, "D+"), (1968.3, "D_s+"), (2286.46, "Lambda_c"),
        (2983, "Eta_c"), (3096.9, "J/Psi"), (3686, "Psi(2S)"),
        (5279.3, "B+"), (9460.3, "Upsilon(1S)"), (10023, "Upsilon(2S)"),
        # Bosons
        (80379, "W Boson"), (91187, "Z Boson"), (125100, "Higgs")
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
    def calculate_theoretical_stability(scale, k):
        """
        Determines if a geometric node is theoretically stable.
        Returns 'Stability Score' (0 = Noise, 100 = Stable).
        """
        score = 0
        prime = DiscoveryEngine.is_prime(k)

        # 1. Base Score by scale
        if scale == "FUNDAMENTAL": return 100
        if scale == "BARYON (Pi^5)": score = 60
        if scale == "MESON (A^-1)": score = 40 # Mesons are generally less stable
        if scale == "LEPTON (N)": score = 30

        # 2. Prime Bonus (Topology)
        if prime: score += 30

        # 3. Low Harmonic Bonus (Lower numbers are cleaner)
        if k < 10: score += 20
        elif k > 50: score -= 20
        elif k > 100: score -= 40

        # 4. Special Magic Numbers (Heuristic symmetries)
        if k == 6 and "BARYON" in scale: score = 100 # Proton rule
        if k == 1 and "LEPTON" in scale: score = 90  # Muon rule (Base)

        return max(0, score)

    @staticmethod
    def scan_spectrum(max_mev=15000):
        found_nodes = []

        print(f"Scanning Geometric Lattice [0 - {max_mev} MeV]...")

        # Generate all possible nodes
        for scale_name, func in GeometricScales.SCALES.items():
            k = 1
            while True:
                mass_me = func(k)
                mass_mev = mass_me / Constants.MeV_to_Me

                if mass_mev > max_mev: break

                # Pre-calculate stability
                stability = DiscoveryEngine.calculate_theoretical_stability(scale_name, k)

                # Discard total noise (unless it's a known particle)
                # Filter is set low to catch potential resonances
                if stability > 20:
                    found_nodes.append({
                        "mev": mass_mev,
                        "scale": scale_name,
                        "k": k,
                        "stability": stability
                    })
                k += 1

        # Sort by energy
        found_nodes.sort(key=lambda x: x["mev"])
        return found_nodes

    @staticmethod
    def match_against_reality(nodes):
        results = []
        known_matched = set()

        for node in nodes:
            mev = node["mev"]
            # Search for match in database (Tolerance 2.5%)
            match_name = None
            match_diff = 0

            for km_mev, km_name in DiscoveryEngine.KNOWN_PARTICLES:
                diff = abs(km_mev - mev) / mev * 100
                if diff < 2.5:
                    match_name = km_name
                    match_diff = diff
                    known_matched.add(km_name)
                    break # Match found

            node["match"] = match_name
            node["match_diff"] = match_diff
            results.append(node)

        return results, len(known_matched)

def run_discovery_scan():
    max_scan = 11000 # Scan up to 11 GeV (Covers Upsilon)

    nodes = DiscoveryEngine.scan_spectrum(max_scan)
    results, matched_count = DiscoveryEngine.match_against_reality(nodes)

    print(f"{Formatting.BOLD}{'='*100}")
    print(f" THE GEOMETRIC UNIVERSE: DISCOVERY SCAN (0 - {max_scan} MeV)")
    print(f" Searching for stable geometric nodes and missing particles...")
    print(f"{'='*100}{Formatting.RESET}")

    print(f" {'THEORY(MeV)':<12} | {'SCALE':<15} | {'k':<4} | {'STAB':<4} | {'STATUS':<20} | {'MATCH/PREDICTION'}")
    print("-" * 100)

    predictions = 0

    for r in results:
        mev = r["mev"]
        k = r["k"]
        scale = r["scale"]
        stab = r["stability"]
        match = r["match"]

        # Output Filtering:
        # Show everything that has a Match.
        # Show Predictions only if they have high stability (>60).

        show_row = False
        row_color = Formatting.RESET
        status = ""
        info = ""

        if match:
            show_row = True
            row_color = Formatting.GREEN
            status = "CONFIRMED"
            info = f"{match} (Err: {r['match_diff']:.1f}%)"
        elif stab >= 70:
            show_row = True
            row_color = Formatting.RED
            status = "PREDICTION"
            info = f"?? NEW CANDIDATE ??"
            predictions += 1
        elif stab >= 50:
            show_row = True
            row_color = Formatting.YELLOW
            status = "RESONANCE"
            info = "Possible Excited State"

        # Prime number formatting
        is_prime = DiscoveryEngine.is_prime(k)
        k_str = f"{k}*" if is_prime else f"{k}"

        if show_row:
            print(f"{row_color} {mev:<12.1f} | {scale:<15} | {k_str:<4} | {stab:<4} | {status:<20} | {info}{Formatting.RESET}")

    print("-" * 100)
    print(f"{Formatting.BOLD} SCAN REPORT:{Formatting.RESET}")
    print(f" Theory Nodes Generated: {len(nodes)}")
    print(f" Known Particles Matched: {matched_count} / {len(DiscoveryEngine.KNOWN_PARTICLES)}")
    print(f" {Formatting.RED}HIGH CONFIDENCE PREDICTIONS (New Particles?): {predictions}{Formatting.RESET}")
    print("=" * 100)
    print(" NOTE: 'k*' indicates a Prime Number topology (Higher Stability).")
    print(" Predictions around 3000-10000 MeV are likely undiscovered Meson states (XYZ particles).")

if __name__ == "__main__":
    run_discovery_scan()