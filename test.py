import math
from decimal import Decimal, getcontext

# --- KONFIGURACE PŘESNOSTI ---
# Nastavíme přesnost na 110 platných číslic, jak požaduješ v paperu.
getcontext().prec = 110

class GeometricQuantization:
    def __init__(self):
        print("=== GEOMETRIC QUANTIZATION OF MATTER: VERIFICATION ENGINE ===\n")

        # 1. Základní konstanty (Vstupy)
        # Používáme Decimal("string") pro zachování absolutní přesnosti bez float chyb.

        # Jemná struktura (alfa) - z PDF: 137.035999
        self.alpha_inv = Decimal("137.035999")
        self.alpha = Decimal(1) / self.alpha_inv

        # Pi (vypočítáme s vysokou přesností pomocí knihovny nebo vložíme dlouhý string)
        # Pro nezávislost zde vkládám pi na 60 míst, což pro ověření stačí.
        self.pi = Decimal("3.14159265358979323846264338327950288419716939937510582097494")

        # Logaritmická báze časoprostoru: N = ln(4pi)
        self.N = (Decimal(4) * self.pi).ln()

        # Fyzikální konstanty pro výpočet G (CODATA 2018/2022 values)
        # Potřebujeme je pro převedení geometrických poměrů na jednotky SI.
        self.c = Decimal("299792458")                  # m/s
        self.h = Decimal("6.62607015e-34")             # J*s
        self.hbar = self.h / (Decimal(2) * self.pi)
        self.me_kg = Decimal("9.10938356e-31")         # Hmotnost elektronu v kg

        # Experimentální hodnoty pro porovnání (CODATA)
        self.muon_exp_ratio = Decimal("206.768283")    # m_mu / m_e
        self.proton_exp_ratio = Decimal("1836.152673") # m_p / m_e (CODATA 2018)
        self.G_exp = Decimal("6.67430e-11")            # m^3 kg^-1 s^-2

    def verify_muon(self):
        """
        Verifikace Sekce 3.1: Lepton Sector (Muon)
        Vzorec (Eq 5): m_mu = m_e * (4*pi*N^3) / (1 - 2*alpha)
        """
        print("--- 1. VERIFIKACE MUONU (k=1, n=2) ---")

        # Lepton Scale S_L = 4*pi*N^3
        S_L = Decimal(4) * self.pi * (self.N ** 3)

        # Topological correction (sphere): 1 - 2*alpha
        correction = Decimal(1) - (Decimal(2) * self.alpha)

        # Výpočet
        muon_ratio_calc = S_L / correction

        print(f"Vstupní vzorec: 4*pi*N^3 / (1 - 2*alpha)")
        print(f"Vypočtená hodnota (m_mu/m_e): {muon_ratio_calc:.6f}")
        print(f"Experimentální hodnota      : {self.muon_exp_ratio:.6f}")

        error = abs(muon_ratio_calc - self.muon_exp_ratio) / self.muon_exp_ratio
        print(f"Relativní chyba             : {error * 100:.8f} %")
        print("------------------------------------------\n")
        return muon_ratio_calc

    def verify_proton(self):
        """
        Verifikace Sekce 3.2: Nuclear Sector (Proton)
        Vzorec (Eq 6): m_p = m_e * 6*pi^5
        """
        print("--- 2. VERIFIKACE PROTONU (k=6, n=0) ---")

        # Baryon Scale S_B = pi^5, Node k=6
        proton_ratio_calc = Decimal(6) * (self.pi ** 5)

        print(f"Vstupní vzorec: 6 * pi^5")
        print(f"Vypočtená hodnota (m_p/m_e): {proton_ratio_calc:.6f}")
        print(f"Experimentální hodnota      : {self.proton_exp_ratio:.6f}")

        error = abs(proton_ratio_calc - self.proton_exp_ratio) / self.proton_exp_ratio
        print(f"Relativní chyba             : {error * 100:.6f} %")
        print("------------------------------------------\n")
        return proton_ratio_calc

    def verify_gravity(self, proton_ratio):
            """
            Verifikace Sekce 3.3: Gravitační konstanta G
            OPRAVENO: Interpretace clenu sqrt(2)*alpha^2
            """
            print("--- 3. VERIFIKACE GRAVITACE (G) ---")

            # Exponent X (Eq 7)
            # X = 10pi/3 + alpha/4pi + sqrt(2) * alpha^2

            term1 = (Decimal(10) * self.pi) / Decimal(3)
            term2 = self.alpha / (Decimal(4) * self.pi)

            # ZDE BYLA CHYBA: Musí to být sqrt(2) * (alpha^2), nikoliv sqrt(2*alpha^2)
            term3 = Decimal(2).sqrt() * (self.alpha ** 2)

            X = term1 + term2 + term3
            print(f"Dimenzionální exponent X     : {X:.5f}")

            # Výpočet G (Eq 8)
            m_p_kg = self.me_kg * proton_ratio
            Gamma_p = proton_ratio

            prefactor = (self.hbar * self.c) / (m_p_kg ** 2)
            geometry_part = (Gamma_p ** 2) * (self.alpha ** (Decimal(2) * X))

            G_calc = prefactor * geometry_part

            print(f"Vypočtené G                  : {G_calc:.5e}")
            print(f"CODATA G                     : {self.G_exp:.5e}")

            error = abs(G_calc - self.G_exp) / self.G_exp
            print(f"Relativní chyba              : {error * 100:.6f} %")
            print("------------------------------------------\n")

# Spuštění verifikace
if __name__ == "__main__":
    engine = GeometricQuantization()
    engine.verify_muon()
    proton_dim = engine.verify_proton()
    engine.verify_gravity(proton_dim)