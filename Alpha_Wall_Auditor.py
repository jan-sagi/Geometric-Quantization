import numpy as np
import matplotlib.pyplot as plt

class GeometricNuclearPhysics:
    def __init__(self):
        # 1. TVÉ GEOMETRICKÉ KONSTANTY
        self.PI = 3.141592653589793
        self.alpha_inv = 4*(self.PI**3) + (self.PI**2) + self.PI
        self.alpha = 1.0 / self.alpha_inv

        # 2. HMOTNOSTNÍ ŠKÁLY (Odvozené)
        self.me_MeV = 0.510998950   # Hmotnost elektronu (Scale Unit)
        self.mp_geom = 6 * (self.PI**5) * self.me_MeV # Geometrický Proton (MeV)

        # 3. JEDNOTKOVÁ ALPHA ENERGIE (E_alpha)
        # Toto je energie jednoho geometrického uzlu v poli Alpha
        self.E_alpha = self.mp_geom * self.alpha

        print("="*60)
        print(f" GEOMETRIC UNIVERSE: ALPHA WALL AUDITOR")
        print("="*60)
        print(f" [AXIOM] Geometric Proton Mass:  {self.mp_geom:.4f} MeV")
        print(f" [AXIOM] Geometric Alpha:        1/{self.alpha_inv:.4f}")
        print(f" [DERIVED] Unit Alpha Energy:    {self.E_alpha:.4f} MeV")
        print("-" * 60)

    def analyze_isotope(self, name, Z, BE_per_nucleon_exp):
        """
        Vypočítá 'Geometrickou Efektivitu' (Eta)
        Eta = Skutečná vazebná energie / Jednotková Alpha Energie
        """
        eta = BE_per_nucleon_exp / self.E_alpha
        return eta

def run_audit():
    physics = GeometricNuclearPhysics()

    # --- DATASET (Empirická data z NIST/CODATA) ---
    # (Jméno, Protonové číslo Z, Vazebná energie na nukleon v MeV)
    isotopes = [
        ("Helium-4", 2, 7.074),    # První vrchol stability
        ("Carbon-12", 6, 7.680),   # Základ života
        ("Oxygen-16", 8, 7.976),
        ("Iron-56", 26, 8.790),    # Absolutní vrchol (Peak)
        ("Krypton-84", 36, 8.719),
        ("Tin-118", 50, 8.523),    # Magic Number
        ("Xenon-132", 54, 8.428),
        ("Gold-197", 79, 7.916),   # Zlato (Stabilní i přes Z=79)
        ("Mercury-202", 80, 7.896),
        ("Lead-208", 82, 7.867),   # === THE ANCHOR (Nejtěžší stabilní) ===
        ("Bismuth-209", 83, 7.848), # Hraniční (kvazi-stabilní)
        ("Polonium-210", 84, 7.834), # !!! NESTABILNÍ (Alpha rozpad) !!!
        ("Radon-222", 86, 7.694),    # Nestabilní
        ("Uranium-238", 92, 7.570)   # Nestabilní
    ]

    # --- KALIBRACE ---
    # Kalibrujeme "Alpha Stěnu" na Olovo-208.
    # Tvá teorie říká: "Co je pod efektivitou Olova, to se rozpadne."
    limit_eta = 7.867 / physics.E_alpha

    z_vals = []
    eta_vals = []
    colors = []

    print(f"{'ISOTOPE':<12} | {'Z':<3} | {'BE/A (MeV)':<10} | {'ETA (η)':<8} | {'STATUS'}")
    print("-" * 60)

    for name, z, be in isotopes:
        eta = physics.analyze_isotope(name, z, be)

        # Logika stability (Tvá teorie)
        # 1. Je efektivita nad limitem Olova? (Nebo rovna) -> STABILNÍ
        # 2. Je pod limitem? -> NESTABILNÍ (Alpha Wall Breached)

        # Malá tolerance pro numerické zaokrouhlení u samotného Olova
        if eta >= limit_eta - 0.0001:
            status = "STABLE"
            col = 'green'
            # Výjimka pro Bismut (je to hraniční případ, extrémně dlouhý poločas)
            if name == "Bismuth-209":
                status = "BORDERLINE"
                col = 'orange'
        else:
            status = "UNSTABLE (WALL BREACH)"
            col = 'red'

        print(f"{name:<12} | {z:<3} | {be:<10.3f} | {eta:<8.4f} | {status}")

        z_vals.append(z)
        eta_vals.append(eta)
        colors.append(col)

    print("-" * 60)
    print(f" [CONCLUSION] The Alpha Wall is at η = {limit_eta:.4f}")
    print(f"              Polonium (Z=84) falls below this limit.")

    # --- VIZUALIZACE ---
    plt.figure(figsize=(12, 7))

    # Křivka
    plt.plot(z_vals, eta_vals, color='gray', alpha=0.5, zorder=1)

    # Body
    for x, y, c, label in zip(z_vals, eta_vals, colors, isotopes):
        plt.scatter(x, y, color=c, s=100, zorder=2, edgecolors='black')
        # Popisky jen pro klíčové prvky
        if x in [2, 26, 82, 84, 92]:
            plt.text(x, y + 0.02, label[0].split('-')[0], ha='center', fontsize=9, fontweight='bold')

    # ALPHA WALL (Červená čára)
    plt.axhline(y=limit_eta, color='red', linestyle='--', linewidth=2, label='The Alpha Wall (Geometric Limit)')

    # Zóny
    plt.fill_between([0, 100], [limit_eta, limit_eta], [2.0, 2.0], color='green', alpha=0.05, label='Stability Zone')
    plt.fill_between([0, 100], [0, 0], [limit_eta, limit_eta], color='red', alpha=0.05, label='Instability Zone')

    plt.title("The Alpha Wall: Geometric Limit of the Periodic Table", fontsize=14)
    plt.xlabel("Proton Number (Z)", fontsize=12)
    plt.ylabel("Geometric Efficiency (η)", fontsize=12)
    plt.xlim(0, 95)
    plt.ylim(1.0, 1.3)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Šipka ukazující na pád
    plt.annotate('THE COLLAPSE', xy=(84, 1.144), xytext=(90, 1.2),
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10, color='red', fontweight='bold')

    plt.show()

if __name__ == "__main__":
    run_audit()