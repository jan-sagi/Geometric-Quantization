import math
from decimal import Decimal, getcontext

getcontext().prec = 60

class GeometricUniverseFixed:
    def __init__(self):
        self.PI = Decimal(math.pi)
        # Konstanty
        self.ALPHA_EXP = Decimal("137.035999084")
        self.G_EXP = Decimal("6.67430e-11")

        # SI převodníky
        self.hbar = Decimal("1.054571817e-34")
        self.c = Decimal("299792458")
        self.me = Decimal("9.10938356e-31")

    def derive_constants(self):
        # 1. Alpha (Geometrická)
        alpha_inv = (4 * self.PI**3) + (self.PI**2) + self.PI
        alpha = 1 / alpha_inv

        # 2. Proton (Geometrický)
        proton_ratio = 6 * (self.PI ** 5)

        # 3. Exponent X (Dimenzionální tlumení)
        term1 = (10 * self.PI) / 3
        term2 = alpha / (4 * self.PI)
        term3 = Decimal(2).sqrt() * (alpha ** 2)
        X = term1 + term2 + term3

        return alpha, proton_ratio, X

    def solve_gravity_corrected(self, alpha, X):
        """
        OPRAVA: Odstraněn člen (proton_ratio ** 2), který způsobil chybu 1836^2.
        Vztah nyní zní: G ~ (hbar*c/me^2) * alpha^(2X)
        """
        # Gravitační vazba (čistě geometrická)
        alpha_G = alpha ** (2 * X)

        # Newtonova konstanta
        G_calc = (self.hbar * self.c / (self.me ** 2)) * alpha_G
        return G_calc

    def find_dark_matter_law(self, alpha):
        """
        Hledá exponent 'n' pro vztah E ~ k^n, který dá poměr ~5.47
        """
        k_max = int( (1/alpha) / self.PI )
        target_ratio = 5.47

        best_n = 0
        best_error = 100

        print(f"\n[DARK MATTER SEARCH] (k_max = {k_max})")
        print(f"Hledám disperzní relaci E(k) = k^n ...")

        # Zkoušíme exponenty od -2 do 2
        test_range = [x * 0.1 for x in range(-20, 25)] # -2.0 až 2.5

        for n in test_range:
            sum_dark = 0
            sum_baryon = 0

            for k in range(1, k_max + 1):
                # Test prvocisla
                is_prime = True
                if k <= 1: is_prime = False
                else:
                    for i in range(2, int(k**0.5) + 1):
                        if k % i == 0: is_prime = False; break

                energy = k ** n

                if is_prime: sum_dark += energy
                else: sum_baryon += energy

            if sum_baryon == 0: continue

            # Zkusíme oba směry poměru (DM/Baryon a Baryon/DM)
            ratio1 = sum_dark / sum_baryon
            ratio2 = sum_baryon / sum_dark if sum_dark > 0 else 0

            # Hledáme shodu s 5.47
            if abs(ratio1 - target_ratio) < best_error:
                best_error = abs(ratio1 - target_ratio)
                best_n = n
                best_type = "Dark/Baryon"
                best_val = ratio1

            if abs(ratio2 - target_ratio) < best_error:
                best_error = abs(ratio2 - target_ratio)
                best_n = n
                best_type = "Baryon/Dark" # Inverzní definice
                best_val = ratio2

        print(f"Nalezen nejlepší fit pro exponent n = {best_n:.1f}")
        print(f"Typ poměru: {best_type}")
        print(f"Výsledný poměr: {best_val:.4f} (Cíl: {target_ratio})")
        return best_n

def run_patch():
    uni = GeometricUniverseFixed()
    alpha, proton, X = uni.derive_constants()

    print(f"=== GEOMETRIC UNIVERSE: PATCHED RESULTS ===")

    # 1. Opravená Gravitace
    G_calc = uni.solve_gravity_corrected(alpha, X)
    print(f"\n1. GRAVITACE (OPRAVENÁ):")
    print(f"   Vstup: X = {X:.5f}")
    print(f"   Teorie: {G_calc:.5e}")
    print(f"   CODATA: {uni.G_EXP:.5e}")

    err = abs(G_calc - uni.G_EXP) / uni.G_EXP * 100
    print(f"   Chyba : {err:.4f} %")

    if err < 0.01:
        print("   >>> SUCCESS: GRAVITY SOLVED <<<")
        print("   (Chyba 1836^2 byla odstraněna)")

    # 2. Hledání zákona Temné hmoty
    uni.find_dark_matter_law(alpha)

if __name__ == "__main__":
    run_patch()