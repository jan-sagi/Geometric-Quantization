import math
import csv
import os

# =============================================================================
# THE GEOMETRIC PARTICLE ZOO: PREDICTIVE ENGINE
# =============================================================================
# AUTHOR: Jan Sagi
# GOAL:   Generate a complete catalogue of geometric resonance nodes.
#         Identify KNOWN particles and predict UNKNOWN candidates.
# =============================================================================

class Constants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999084
    ALPHA = 1.0 / ALPHA_INV
    N = math.log(4 * PI)

    # Mass Conversion (me -> MeV)
    ME_TO_MEV = 0.510998950

    # Time Anchor (Muon)
    MUON_LIFE = 2.2e-6
    MUON_BETA = 0.1702

class KnownPhysics:
    """
    Database of known particles for cross-referencing.
    Source: Particle Data Group (PDG).
    """
    DATABASE = [
        (0.511, "Electron"), (105.66, "Muon"), (1776.86, "Tau"),
        (134.98, "Pion0"), (139.57, "Pion+"), (493.67, "Kaon+"),
        (938.27, "Proton"), (939.57, "Neutron"), (1115.68, "Lambda"),
        (1869.65, "D+ Meson"), (3096.90, "J/Psi"), (5279.32, "B+ Meson"),
        (9460.30, "Upsilon(1S)"), (125100.0, "Higgs Boson"),
        (80379.0, "W Boson"), (91187.6, "Z Boson"), (173100.0, "Top Quark")
    ]

    @staticmethod
    def identify(mass_mev):
        for real_mass, name in KnownPhysics.DATABASE:
            # Tolerance 2% (Geometry is ideal, reality has binding energy noise)
            if abs(mass_mev - real_mass) / real_mass < 0.025:
                return name
        return None

class ZooGenerator:
    def __init__(self):
        self.zoo = []

        # Define the 3 Geometric Scales
        self.scales = {
            "LEPTON (4pi*N^3)": 4 * Constants.PI * (Constants.N**3),
            "MESON (Alpha^-1)": Constants.ALPHA_INV,
            "BARYON (Pi^5)":    Constants.PI**5
        }

    def calculate_properties(self, k, base_val, scale_name):
        # 1. Topology Correction
        correction = 1.0
        topo_type = "Harmonic"

        if k == 1:
            correction = 1 / (1 - 2*Constants.ALPHA)
            topo_type = "Sphere (Singularity)"
        elif k % 6 == 0:
            correction = 1.0
            topo_type = "Hexagon (Perfect)"
        elif self._is_prime(k):
            correction = 1 + 5*Constants.ALPHA
            topo_type = "Prime (Spinor)"
        else:
            correction = 1 + Constants.ALPHA
            topo_type = "Composite"

        # 2. Mass
        mass_me = k * base_val * correction
        mass_mev = mass_me * Constants.ME_TO_MEV

        # 3. Lifetime (The k^5 Law)
        # Beta calculation
        beta = 0.0
        if correction != 1.0:
            F = correction if correction > 1 else 1/correction
            try: beta = math.sqrt(1 - 1/F**2)
            except: beta = 0

        if beta < 1e-5:
            lifetime = float('inf')
        else:
            # Universal Decay Law
            lifetime = Constants.MUON_LIFE / ((k**5) * (beta/Constants.MUON_BETA)**2)
            # Penalty for Meson Scale (High instability)
            if "MESON" in scale_name: lifetime /= 100

        return mass_mev, lifetime, topo_type

    def scan_universe(self, max_mass_mev=200000):
        print(f">>> SCANNING GEOMETRIC LATTICE (0 - {max_mass_mev} MeV)...")

        for scale_name, base_val in self.scales.items():
            k = 1
            while True:
                mass, life, topo = self.calculate_properties(k, base_val, scale_name)
                if mass > max_mass_mev: break

                # Check if it exists in Standard Model
                known_name = KnownPhysics.identify(mass)

                # Determine Status
                status = "UNKNOWN"
                if known_name:
                    status = f"CONFIRMED ({known_name})"
                elif life > 1e-20:
                    status = "PREDICTION (Candidate)"
                else:
                    status = "NOISE (Short-lived)"

                # Filter: Save only interesting nodes
                # (Confirmed particles OR Long-lived Candidates)
                if status != "NOISE (Short-lived)" or (self._is_prime(k) and k < 50):
                    self.zoo.append({
                        "Mass_MeV": round(mass, 2),
                        "Lifetime_s": f"{life:.2e}",
                        "Scale": scale_name,
                        "Node_k": k,
                        "Topology": topo,
                        "Status": status
                    })

                k += 1

        # Sort by Mass
        self.zoo.sort(key=lambda x: x["Mass_MeV"])

    def save_to_csv(self):
        filename = "Particle_Zoo_Predictions.csv"
        keys = ["Mass_MeV", "Scale", "Node_k", "Topology", "Lifetime_s", "Status"]

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.zoo)

        print(f">>> DATABASE SAVED: {filename}")
        self.print_top_candidates()

    def print_top_candidates(self):
        print("\n" + "="*90)
        print(f" THE GEOMETRIC ZOO: TOP PREDICTIONS (UNKNOWN PARTICLES)")
        print("="*90)
        print(f" {'MASS (MeV)':<12} | {'SCALE':<18} | {'k':<4} | {'LIFETIME':<10} | {'TOPOLOGY'}")
        print("-" * 90)

        count = 0
        for p in self.zoo:
            if "PREDICTION" in p["Status"]:
                # Filter weak candidates to show only strong ones
                if "Prime" in p["Topology"] or "Hexagon" in p["Topology"]:
                    print(f" {p['Mass_MeV']:<12.2f} | {p['Scale']:<18} | {p['Node_k']:<4} | {p['Lifetime_s']:<10} | {p['Topology']}")
                    count += 1
                    if count >= 20: break

        print("-" * 90)
        print(f" Note: These particles should exist based on geometric laws.")
        print(f" Look for resonance peaks at these specific energies.")
        print("="*90)

    @staticmethod
    def _is_prime(n):
        if n <= 1: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

if __name__ == "__main__":
    gen = ZooGenerator()
    gen.scan_universe(200000) # Scan up to Top Quark energy
    gen.save_to_csv()