import math
from decimal import Decimal, getcontext

# Nastavení přesnosti
getcontext().prec = 100

class DimensionalPhysics:
    """
    TOPOLOGICKÝ PRŮZKUMNÍK DIMENZÍ
    ===============================
    Cíl: Zjistit, v kolika dimenzích 'žijí' částice podle tvé teorie.
    Metoda: Porovnání objemů n-rozměrných koulí s fyzikálními konstantami.
    """

    PI = Decimal("3.14159265358979323846264338327950288419716939937510")
    ALPHA_INV = Decimal("137.035999084")

    @staticmethod
    def gamma_function(z):
        """
        Vypočítá Gamma funkci (zobecněný faktoriál) pro výpočet objemu hypersféry.
        Gamma(n) = (n-1)! pro celá čísla.
        Používáme Lanczosovu aproximaci pro Decimal.
        """
        # Pro celá a polocelá čísla (což pro dimenze stačí)
        # Gamma(n+1) = n * Gamma(n)
        # Gamma(1) = 1, Gamma(0.5) = sqrt(pi)

        z = float(z) # Pro gamma stačí float precision, jde o hledání vzorů
        return math.gamma(z)

    @staticmethod
    def hypersphere_volume(dim, radius=1.0):
        """
        Vypočítá objem n-rozměrné koule.
        V_n = (pi^(n/2) / Gamma(n/2 + 1)) * R^n
        """
        n = dim
        numerator = math.pi ** (n / 2.0)
        denominator = math.gamma((n / 2.0) + 1.0)
        return (numerator / denominator) * (radius ** n)

    @staticmethod
    def hypersphere_surface(dim, radius=1.0):
        """
        Vypočítá povrch n-rozměrné koule.
        S_n = (2 * pi^(n/2) / Gamma(n/2)) * R^(n-1)
        """
        n = dim
        numerator = 2 * (math.pi ** (n / 2.0))
        denominator = math.gamma(n / 2.0)
        return (numerator / denominator) * (radius ** (n - 1))

class DimensionScanner:
    def __init__(self):
        self.phys = DimensionalPhysics()

    def run_scan(self):
        print("===================================================================")
        print(" DIMENSIONAL TOPOLOGY SCANNER")
        print("===================================================================")
        print(f" Hledáme shodu mezi geometrií dimenzí a konstantou Alpha^-1 ({self.phys.ALPHA_INV})")
        print("-------------------------------------------------------------------")
        print(f" {'DIM (n)':<8} | {'OBJEM (Unit)':<15} | {'POVRCH (Unit)':<15} | {'RELACE K ALFA'}")
        print("-" * 70)

        # Procházíme dimenze 1 až 15
        # (Strunová teorie má ráda 10, 11, 26)
        for n in range(1, 27):
            vol = self.phys.hypersphere_volume(n)
            surf = self.phys.hypersphere_surface(n)

            # Hledáme "Alpha Match"
            # Zkoušíme, jestli Alfa není schovaná v poměru Povrch/Objem nebo v samotném objemu

            note = ""

            # Test 1: Je objem blízký nějaké škále?
            # Baryon Scale je Pi^5 (~306). Objem 10D koule je Pi^5 / 120 (~2.55).
            # Ale podívejme se na 'Reciprocal Volume' nebo jiné vztahy.

            # Test 2: Souvislost s Alfou (137.036)
            # Zkoumáme, jestli (Povrch * n) nebo (Objem * n!) nedává 137.

            # Zajímavost: 4*PI^3 + PI^2 + PI = 137.036...
            # 4*PI^3 je "Povrch koule v 4D prostoru" (skoro).
            # Povrch 4D koule (S_3) = 2 * pi^2 * R^3 -> 19.7

            print(f" {n:<8} | {vol:<15.4f} | {surf:<15.4f} | {note}")

        print("-" * 70)
        self.analyze_specific_geometries()

    def analyze_specific_geometries(self):
        print("\n HLOUBKOVÁ ANALÝZA: PROJEKCE DO 137")
        print("-" * 70)

        # 1. Analýza vzorce 4*pi^3 + pi^2 + pi
        # Jaké dimenze to reprezentuje?

        # 4*pi^3 = Objem čeho?
        # V_6 (6D koule) = pi^3 / 6. -> 4*pi^3 = 24 * V_6

        print(f" HYPOTÉZA: Alfa (137.036) je součtem 'fázových objemů'.")

        pi = math.pi
        term1 = 4 * (pi**3)
        term2 = pi**2
        term3 = pi

        print(f" 1. 4*pi^3 ({term1:.2f}) odpovídá...")
        print(f"    -> Objem toru? Povrch 5D sféry?")

        # Zkusíme najít, jestli to sedí na povrch v 7D
        s7 = self.phys.hypersphere_surface(7) # 33.07
        s8 = self.phys.hypersphere_surface(8) # 40.5

        # Zkusíme V_n * n! (Fázový prostor)
        for n in range(1, 10):
            phase_vol = self.phys.hypersphere_volume(n) * math.factorial(n)
            if abs(phase_vol - 137) < 50:
                print(f"    -> Dimenze {n}: Fázový objem = {phase_vol:.2f}")

        print("\n 2. Gravitační exponent X = 10.47")
        print("    Co znamená fraktální dimenze 10.47?")

        # Zkusme objem v dimenzi 10.47 (použitím Gamma funkce pro necelá čísla)
        x_dim = 10.472
        vol_x = self.phys.hypersphere_volume(x_dim)
        print(f"    -> Objem sféry v D={x_dim}: {vol_x:.4f}")

        # Porovnání s Alfou
        # Zkusíme: Je to logaritmus něčeho?

        print("-" * 70)

if __name__ == "__main__":
    scanner = DimensionScanner()
    scanner.run_scan()