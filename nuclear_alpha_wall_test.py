import math
from decimal import Decimal, getcontext

getcontext().prec = 50

class AlphaWallTest:
    def __init__(self):
        self.PI = Decimal(math.pi)
        self.me = Decimal("0.51099895") # MeV

        # 1. Geometrický Proton (Základ mřížky)
        self.mass_proton_geom = self.me * 6 * (self.PI**5)

        # 2. Alpha (Geometrická)
        self.alpha_inv = (4 * self.PI**3) + (self.PI**2) + self.PI
        self.alpha = 1 / self.alpha_inv

        # 3. Unit Alpha Energy (Energie jedné alpha vazby na protonu)
        # E_alpha = Mp * alpha
        self.E_alpha = self.mass_proton_geom * self.alpha

        print(f"=== ALPHA WALL TEST ===")
        print(f"Geometric Proton Mass: {self.mass_proton_geom:.2f} MeV")
        print(f"Unit Alpha Energy (Limit): {self.E_alpha:.3f} MeV")
        print("-" * 60)

    def check_nucleus(self, element_name, A, binding_energy_per_nucleon_MeV):
        """
        Ověřuje stabilitu jádra vůči geometrickému limitu Alpha.
        Podmínka stability podle teorie: (Binding Energy / A) >= E_alpha
        """
        BE_per_A = Decimal(binding_energy_per_nucleon_MeV)

        # Alpha Efficiency Ratio
        eta = BE_per_A / self.E_alpha

        status = "STABLE" if eta >= 1.0 else "UNSTABLE (Alpha Decay)"

        print(f"{element_name:<15} (A={A:<3}) | BE/A: {BE_per_A:.3f} MeV | Ratio (eta): {eta:.4f} alpha | {status}")
        return eta

# DATA Z NIST/Jaderné fyziky (Binding Energy per Nucleon)
# Toto jsou naměřené hodnoty, které porovnáme s tvým limitem.
ISOTOPES = [
    ("Helium-4", 4, 7.07),
    ("Carbon-12", 12, 7.68),
    ("Iron-56", 56, 8.79),   # Peak stability
    ("Tin-120", 120, 8.51),
    ("Gold-197", 197, 7.91),
    ("Lead-208", 208, 7.87), # Poslední stabilní (doubly magic)
    ("Bismuth-209", 209, 7.84), # Extrémně dlouhý poločas (kvazi-stabilní)
    ("Polonium-210", 210, 7.83), # Nestabilní!
    ("Radon-222", 222, 7.69),
    ("Uranium-238", 238, 7.57)
]

if __name__ == "__main__":
    test = AlphaWallTest()

    print(f"{'Isotope':<15} {'Mass':<7} | {'Binding E':<13} | {'Efficiency':<18} | {'Prediction'}")
    print("-" * 80)

    results = []
    for name, A, be in ISOTOPES:
        eta = test.check_nucleus(name, A, be)
        results.append((name, eta))

    print("-" * 80)
    print("ANALÝZA:")
    print("Pokud teorie platí, 'Ratio' musí klesnout pod 1.0000 přesně u Polonia.")
    print("Lead-208 by měl být těsně nad 1.0000.")
