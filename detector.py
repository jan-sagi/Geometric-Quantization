from .constants import UniverseConstants
from .fractal_equations import FractalPhysics
from decimal import Decimal

class GeometricDetector:
    """
    POZOROVATEL SIMULACE
    ====================
    Tato třída nezná 'Standardní Model'.
    Měří pouze to, co vychází z geometrie:
    1. Energii (Mass)
    2. Pnutí (Stability)
    3. Topologii (Charge)
    4. Rezonanci (Spectrum)
    """

    def __init__(self):
        # Cache pro základní geometrické konstanty
        self.PI = UniverseConstants.PI
        self.ALPHA = UniverseConstants.ALPHA
        self.N = UniverseConstants.N

        # Odvození referenčního bodu pro jadernou fyziku (Proton)
        # Proton není konstanta, je to výsledek geometrie (Baryon Scale, k=6)
        # Detector si ho musí "změřit" sám, aby měl s čím srovnávat jádra.
        self.baryon_scale = self.PI ** 5
        self.proton_geom_mass, _, _ = FractalPhysics.calculate_node_mass(6, self.baryon_scale, self.ALPHA)

    def measure_particle_node(self, k, scale_base, scale_name):
        """
        Změří vlastnosti jednoho energetického uzlu.
        Vrátí datový balíček (Dictionary).
        """
        # 1. Změření Hmotnosti (Aplikace topologické korekce)
        mass, correction, topology = FractalPhysics.calculate_node_mass(k, scale_base, self.ALPHA)

        # 2. Změření Vnitřního času (Rychlost rozpadu)
        beta = FractalPhysics.calculate_intrinsic_velocity(correction)
        stability_score = FractalPhysics.calculate_stability_score(k, beta)

        # 3. Interpretace stability (pro CSV výstup)
        # Toto je predikce detektoru: "Jak dlouho to vydrží?"
        predicted_status = "STABLE"
        if stability_score < 1e10: predicted_status = "UNSTABLE"
        if stability_score < 1000: predicted_status = "RESONANCE" # Extrémně krátký život

        return {
            "type": "PARTICLE",
            "scale": scale_name,
            "k": k,
            "mass_me": float(mass),          # Hmotnost v jednotkách elektronu
            "correction": float(correction), # Faktor deformace
            "beta": float(beta),             # Vnitřní rychlost
            "stability_score": float(stability_score),
            "topology": topology,
            "prediction": predicted_status
        }

    def measure_atomic_nucleus(self, Z, A):
            """
            Změří vlastnosti složeného jádra a testuje Alpha Wall.
            """
            # 1. Výpočet Hmotnosti jádra (Nová rovnice s Pi a Alpha)
            real_mass = FractalPhysics.calculate_nucleus_mass(
                A, Z, self.proton_geom_mass, self.ALPHA, self.PI
            )

            # 2. Topologický Stres (Beta Rozpad - Weak Force)
            charge_stress = FractalPhysics.calculate_charge_stress(Z, self.ALPHA)
            beta_stability = "STABLE"
            if charge_stress > 0.1: beta_stability = "UNSTABLE (Beta)"

            # 3. Test Alpha Rozpadu (Strong Force Limit)
            # Decay: Parent -> Daughter(Z-2, A-4) + Alpha(2, 4)
            alpha_stability = "STABLE"

            if A > 4:
                mass_alpha = FractalPhysics.calculate_nucleus_mass(
                    4, 2, self.proton_geom_mass, self.ALPHA, self.PI
                )
                mass_daughter = FractalPhysics.calculate_nucleus_mass(
                    A-4, Z-2, self.proton_geom_mass, self.ALPHA, self.PI
                )

                # Pokud je hmotnost rodiče větší než součet produktů, energie se uvolní -> Rozpad
                if real_mass > (mass_daughter + mass_alpha):
                    alpha_stability = "UNSTABLE (Alpha Decay)"

            # Celkový verdikt
            final_status = "STABLE"
            if beta_stability != "STABLE": final_status = beta_stability
            if alpha_stability != "STABLE": final_status = alpha_stability

            return {
                "type": "NUCLEUS",
                "Z": Z,
                "A": A,
                "mass_theory_me": float(real_mass),
                "binding_unit_me": float(self.proton_geom_mass * self.ALPHA),
                "charge_stress": float(charge_stress),
                "prediction_weak": beta_stability,
                "prediction_alpha": alpha_stability,
                "final_prediction": final_status
            }

    def measure_spectrum_shift(self, Z, A):
        """
        Vypočítá spektrální posuv (Isotope Shift) pro vodíku-podobný atom.
        Toto ověřuje, zda geometrická hmotnost jádra správně ovlivňuje elektron.
        """
        # Rydbergova konstanta (Geometrická) ~ Alpha^2
        # R ~ alpha^2 * me / 2 (v přirozených jednotkách)
        rydberg_geom = (self.ALPHA ** 2) / 2

        # Redukovaná hmotnost (Vliv jádra)
        # mu = me * M / (me + M)
        # Kde M je naše geometrická hmotnost jádra (A * Proton_Geom)
        nucleus_mass = A * self.proton_geom_mass
        reduced_mass = nucleus_mass / (1 + nucleus_mass)

        # Efektivní energie základního stavu (n=1)
        # E = R * Z^2 * reduced_mass
        ground_state_energy = rydberg_geom * (Decimal(Z)**2) * reduced_mass

        return {
            "type": "SPECTRUM",
            "Z": Z,
            "A": A,
            "rydberg_factor": float(ground_state_energy)
        }