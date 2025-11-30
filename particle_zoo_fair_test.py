import math
from decimal import Decimal, getcontext

getcontext().prec = 50

# FYZIKÁLNÍ REFERENČNÍ HODNOTY (MeV)
PARTICLES = {
    "Muon": 105.658,
    "Pion (+/-)": 139.570,
    "Kaon (+/-)": 493.677,
    "Proton": 938.272,
    "Tau": 1776.86,
    "Neutron": 939.565,
    "Omega": 782.65,   # Omega mezon
    "Eta": 547.86
}

class GeometricLattice:
    def __init__(self):
        self.PI = Decimal(math.pi)
        self.me_MeV = Decimal("0.51099895") # Hmotnost elektronu v MeV

        # 1. Výpočet konstant mřížky
        # Alpha (Geometrická)
        self.alpha_inv = (4 * self.PI**3) + (self.PI**2) + self.PI
        self.alpha = 1 / self.alpha_inv

        # Logaritmická báze N = ln(4pi)
        self.N = Decimal(math.log(4 * math.pi))

        # 2. Definice ŠKÁL (Scales)
        # Leptonová škála: 4pi * N^3
        self.Scale_L = 4 * self.PI * (self.N ** 3)

        # Baryonová škála: pi^5
        self.Scale_B = self.PI ** 5

        # Mesonová škála (z PDF): alpha^-1
        self.Scale_M = self.alpha_inv

    def scan_lattice(self, max_k=20):
        print(f"=== THE FAIR TEST: SCANNING LATTICE NODES (k=1 to {max_k}) ===")
        print(f"Electron mass: {self.me_MeV} MeV")
        print(f"Scale Lepton (4pi*N^3): {self.Scale_L:.4f} me")
        print(f"Scale Baryon (pi^5):    {self.Scale_B:.4f} me")
        print("-" * 65)
        print(f"{'k':<4} | {'Scale Type':<10} | {'Mass (MeV)':<12} | {'Candidate?':<20} | {'Error %':<8}")
        print("-" * 65)

        # Prohledáváme obě škály pro každé k
        hits = []

        for k in range(1, max_k + 1):
            # 1. Lepton Scale Check
            mass_L = self.me_MeV * Decimal(k) * self.Scale_L
            self.check_match(k, "LEPTON", mass_L, hits)

            # 2. Baryon Scale Check
            mass_B = self.me_MeV * Decimal(k) * self.Scale_B
            self.check_match(k, "BARYON", mass_B, hits)

            # 3. Meson Scale Check (Alpha scale)
            mass_M = self.me_MeV * Decimal(k) * self.Scale_M
            self.check_match(k, "MESON", mass_M, hits)

    def check_match(self, k, scale_type, mass, hits):
        # Tolerance pro "Hit" (2% - bez topologických korekcí n*alpha)
        # Hledáme hrubou shodu s celočíselným uzlem

        for p_name, p_mass in PARTICLES.items():
            diff = abs(mass - Decimal(p_mass))
            error = (diff / Decimal(p_mass)) * 100

            if error < 2.5: # 2.5% okno pro "Candidate"
                print(f"{k:<4} | {scale_type:<10} | {mass:.2f}        | {p_name:<20} | {error:.2f}%")
                hits.append((p_name, error))

if __name__ == "__main__":
    lattice = GeometricLattice()
    lattice.scan_lattice(max_k=25)