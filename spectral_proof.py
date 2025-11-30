import math
from decimal import Decimal

class FractalPhysics:
    """
    JÁDRO SIMULACE: ČISTÁ GEOMETRIE (DECIMAL SAFE EDICE)
    ====================================================
    Verze 2.0:
    - Implementován zákon rozpadu 1/k^5 (Baryon Scale Dimension)
    - Implementována rovnice Alpha Wall (Attraction vs Repulsion)
    """

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
        """
        UNIVERZÁLNÍ ZÁKON ROZPADU (k^5)
        Baryonová škála je Pi^5, což implikuje 5D fázový prostor pro rezonanci.
        Pravděpodobnost úniku energie (rozpadu) roste s k^5.
        """
        if beta == 0:
            return float('inf')

        epsilon = 1e-15
        beta_sq = max(beta**2, epsilon)

        # ZMĚNA: Exponent 4 -> 5
        score = 1.0 / ((float(k)**5) * beta_sq)
        return score

    @staticmethod
    def calculate_nucleus_mass(A, Z, proton_mass, alpha, pi):
        """
        ROVNICE ZÁNIKU (THE DOOMSDAY EQUATION)
        Vypočítá hmotnost jádra jako souboj soudržnosti a náboje.
        """
        DA = Decimal(A)
        DZ = Decimal(Z)

        # 1. SOUDRŽNOST (Strong Force Geometry)
        # Každý nukleon dává vazbu Alpha.
        # Mřížka dává bonus Alpha^2 (vrstvení).
        attraction_term = alpha + (alpha ** 2)

        # 2. ODPUZOVÁNÍ (Charge Stress Geometry)
        # Interakce Z*(Z-1). Geometrie pole je PI. Síla je Alpha^2.
        # Rozředěno v objemu A.
        repulsion_term = (DZ * (DZ - 1) / DA) * (alpha ** 2) * pi

        # Čistá vazba na nukleon
        binding_per_nucleon = attraction_term - repulsion_term

        # Pokud je vazba záporná, jádro neexistuje (rozpadne se během vzniku)
        if binding_per_nucleon < 0:
            binding_per_nucleon = Decimal(0)

        # Celková hmotnost = Součet protonů - Vazebná energie
        total_mass = (DA * proton_mass) * (Decimal(1) - binding_per_nucleon)

        return total_mass

    @staticmethod
    def calculate_charge_stress(Z, alpha):
        symmetry_factor = Decimal(FractalPhysics._get_divisors_count(Z))
        if FractalPhysics._is_prime(Z): symmetry_factor = Decimal("0.5")
        stress = (Decimal(Z) * alpha) / symmetry_factor
        if Z % 2 == 0: stress *= Decimal("0.8")
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