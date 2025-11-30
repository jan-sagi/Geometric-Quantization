from .constants import UniverseConstants, D
from decimal import Decimal

class GeometricAccelerator:
    """
    URYCHLOVAČ A GENERÁTOR HMOTY
    ============================
    Tato třída je 'Motor'. Její úkol je systematicky procházet
    geometrickou mřížku (zvyšovat k, Z, A) a posílat tyto
    souřadnice Detektoru.

    Všechny výpočty škál probíhají v High-Precision Decimal (110+ digits).
    """

    def __init__(self, detector_instance):
        self.detector = detector_instance

        # 1. INICIALIZACE ZÁKLADNÍCH ŠKÁL (Dynamicky z Axiomů)
        # Nepoužíváme žádná předpočítaná čísla. Vše se počítá teď.

        # Leptonová škála: Základní časoprostorová excitace (4*PI*N^3)
        self.scale_lepton = D(4) * UniverseConstants.PI * (UniverseConstants.N ** 3)

        # Mezonová škála: Elektromagnetická vazba (Alpha^-1)
        self.scale_meson = UniverseConstants.ALPHA_INV

        # Baryonová škála: Objemová geometrie (Pi^5)
        self.scale_baryon = UniverseConstants.PI ** 5

        # Seznam škál pro iteraci
        self.scales = [
            ("LEPTON_SCALE", self.scale_lepton),
            ("MESON_SCALE",  self.scale_meson),
            ("BARYON_SCALE", self.scale_baryon)
        ]

    def run_collision_experiment(self, max_k=100):
        """
        Simuluje srážky částic (skenování energetických hladin).
        Prochází celá čísla k (1..max_k) na všech třech škálách.
        """
        results = []
        print(f"   -> Spouštím skenování mřížky (k=1 až {max_k}) na 3 škálách...")

        for scale_name, scale_base_value in self.scales:
            for k in range(1, max_k + 1):
                # Odeslání uzlu do detektoru k měření
                # Uzel je definován jen (Integer k) a (Base Scale)
                measurement = self.detector.measure_particle_node(
                    k=k,
                    scale_base=scale_base_value,
                    scale_name=scale_name
                )
                results.append(measurement)

        return results

    def run_nucleosynthesis(self, max_z=118):
        """
        Simuluje tvorbu atomových jader (skládání protonů a neutronů).
        Prochází Z (1..max_z) a k nim relevantní A (izotopy).
        """
        results = []
        print(f"   -> Spouštím nukleosyntézu (Z=1 až {max_z})...")

        for z in range(1, max_z + 1):
            # Heuristika pro skenování izotopů (nemá smysl skenovat A=1000 pro Vodík)
            # Skenujeme oblast od A=Z (samotné protony) až po A=3.5*Z (těžké neutronové přebytky)
            # To pokryje "Valley of Stability" i "Drip Lines".
            min_a = z
            max_a = int(z * 3.2) + 2

            for a in range(min_a, max_a):
                # 1. Měření jádra (Stabilita, Vazba, Weak Force)
                nucleus_data = self.detector.measure_atomic_nucleus(z, a)

                # 2. Měření spektra (Jako kdybychom k jádru přidali 1 elektron)
                # Toto ověřuje vliv hmotnosti jádra na elektron (Isotope Shift)
                spectrum_data = self.detector.measure_spectrum_shift(z, a)

                # Sloučení dat do jednoho záznamu
                full_atom_record = {**nucleus_data, **spectrum_data}
                results.append(full_atom_record)

        return results