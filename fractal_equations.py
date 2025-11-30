import math
from decimal import Decimal

class FractalPhysics:
    """
    JÁDRO SIMULACE: ČISTÁ GEOMETRIE (FINAL REVISION)
    ================================================
    Opravy:
    1. Repulsion Term používá poloměr (A^(1/3)), ne objem (A).
    2. Charge Stress zohledňuje Magická čísla (Geometrické slupky).
    """

    # Geometricky uzavřené slupky (Platonická stabilita)
    GEOMETRIC_SHELLS = {2, 8, 20, 28, 50, 82, 126}

    @staticmethod
    def get_topology_correction(k, alpha):
        ONE = Decimal("1")
        TWO = Decimal("2")
        FIVE = Decimal("5")

        if k == 1:
            return (ONE / (ONE - TWO * alpha)), "SPHERE_SINGULARITY"
        if k % 6 == 0:
            return ONE, "PERFECT_SYMMETRY"
        if FractalPhysics._is_prime(k):
            return (ONE + FIVE * alpha), "PRIME_TOPOLOGY"
        return ONE, "COMPOSITE_HARMONIC"

    @staticmethod
    def calculate_node_mass(k, base_scale_value, alpha):
        correction, topology_type = FractalPhysics.get_topology_correction(k, alpha)
        mass = Decimal(k) * base_scale_value * correction
        return mass, correction, topology_type

    @staticmethod
    def calculate_intrinsic_velocity(correction_factor):
        cf = float(correction_factor)
        if abs(cf - 1.0) < 1e-15: return 0.0
        F = cf if cf > 1.0 else 1.0 / cf
        try:
            beta = math.sqrt(1.0 - (1.0 / (F ** 2)))
        except ValueError:
            beta = 0.0
        return beta

    @staticmethod
    def calculate_stability_score(k, beta):
        if beta == 0: return float('inf')
        epsilon = 1e-15
        beta_sq = max(beta**2, epsilon)
        score = 1.0 / ((float(k)**5) * beta_sq)
        return score

    @staticmethod
    def calculate_nucleus_mass(A, Z, proton_mass, alpha, pi):
        """
        ROVNICE ZÁNIKU (Opravená dimenzionalita)
        """
        DA = Decimal(A)
        DZ = Decimal(Z)

        # 1. SOUDRŽNOST (Objemová)
        attraction_term = alpha + (alpha ** 2)

        # 2. ODPUZOVÁNÍ (Povrchové/Radiální)
        # OPRAVA: Dělíme A^(1/3) -> Poloměr, ne Objem.
        # Používáme Decimal.pow(1/3)
        radius_geom = DA ** (Decimal("1") / Decimal("3"))

        # Repulsion = (Z*(Z-1) / Radius) * Alpha^2 * Pi
        # Pi zde reprezentuje sférickou geometrii pole
        repulsion_term = (DZ * (DZ - 1) / radius_geom) * (alpha ** 2) * pi

        binding_per_nucleon = attraction_term - repulsion_term

        if binding_per_nucleon < 0:
            binding_per_nucleon = Decimal(0)

        total_mass = (DA * proton_mass) * (Decimal(1) - binding_per_nucleon)
        return total_mass

    @staticmethod
    def calculate_charge_stress(Z, alpha):
        """
        Vypočítá stres s bonusem pro Magická čísla (Slupky).
        """
        # Základní symetrie (počet dělitelů)
        divisors = Decimal(FractalPhysics._get_divisors_count(Z))
        symmetry_factor = divisors

        # Penalizace pro prvočísla
        if FractalPhysics._is_prime(Z):
            symmetry_factor = Decimal("0.5")

        # OPRAVA: Bonus pro Magická čísla (Geometrické slupky)
        if Z in FractalPhysics.GEOMETRIC_SHELLS:
            symmetry_factor = Decimal("20.0") # Obrovská stabilita

        stress = (Decimal(Z) * alpha) / symmetry_factor

        # Bonus pro sudá čísla (Pairing) - pokud to není Magické číslo (tam už bonus je)
        if Z % 2 == 0 and Z not in FractalPhysics.GEOMETRIC_SHELLS:
            stress *= Decimal("0.8")

        return float(stress)

    @staticmethod
    def _is_prime(n):
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0 or n % 3 == 0: return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0: return False
            i += 6
        return True

    @staticmethod
    def _get_divisors_count(n):
        cnt = 0
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                if i * i == n: cnt += 1
                else: cnt += 2
        return cnt