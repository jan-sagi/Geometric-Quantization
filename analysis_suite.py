import csv
import math
import os

class DataAuditor:
    """
    NEZÁVISLÝ AUDITOR DAT
    =====================
    Tento skript načte vygenerované CSV soubory a porovná je
    s 'Ground Truth' (známou fyzikou).
    """

    # Převodní konstanta (pouze pro zobrazení, neovlivňuje simulaci)
    # Hmotnost elektronu v MeV
    ME_TO_MEV = 0.510998950

    # ZNÁMÉ ČÁSTICE (Cíle, které chceme v datech najít)
    # (Název, Hmotnost MeV, Tolerance %)
    KNOWN_PARTICLES = [
        ("Muon", 105.66, 1.0),
        ("Pion+/-", 139.57, 1.5),
        ("Kaon+/-", 493.67, 1.5),
        ("Proton", 938.27, 0.5),   # Přísná tolerance
        ("Neutron", 939.57, 0.5),
        ("Lambda", 1115.68, 2.0),
        ("Tau", 1776.86, 1.0),
        ("D-Meson", 1869.65, 1.5),
        ("J/Psi", 3096.90, 1.5),
        ("Upsilon", 9460.30, 1.5),
        ("Higgs", 125100.0, 2.0) # Bonus
    ]

    def __init__(self):
        self.particles = []
        self.atoms = []
        self.path_particles = "universal_particles.csv"
        self.path_atoms = "universal_atoms.csv"

    def load_data(self):
        """Načte vygenerovaná data z CSV."""
        print(">>> NAČÍTÁM DATA Z DISKU...")

        if os.path.exists(self.path_particles):
            with open(self.path_particles, 'r') as f:
                self.particles = list(csv.DictReader(f))
            print(f"   -> Načteno {len(self.particles)} částic.")
        else:
            print("   [CHYBA] Nenalezen soubor particles.csv")

        if os.path.exists(self.path_atoms):
            with open(self.path_atoms, 'r') as f:
                self.atoms = list(csv.DictReader(f))
            print(f"   -> Načteno {len(self.atoms)} atomů.")
        else:
            print("   [CHYBA] Nenalezen soubor atoms.csv")

    def audit_particle_spectrum(self):
        """
        Hledá shody mezi vygenerovanou mřížkou a realitou.
        """
        print("\n" + "="*80)
        print(" AUDIT 1: HLEDÁNÍ ZNÁMÝCH ČÁSTIC V MŘÍŽCE")
        print("="*80)
        print(f" {'CÍL':<12} | {'REAL (MeV)':<10} | {'GEN (MeV)':<10} | {'CHYBA %':<8} | {'SCALE':<15} | {'k':<4} | {'STABILITA'}")
        print("-" * 80)

        hits = 0

        for name, real_mev, tol in self.KNOWN_PARTICLES:
            best_match = None
            best_error = float('inf')

            # Prohledat všechny vygenerované uzly
            for p in self.particles:
                # Převod simulované hmotnosti (me) na MeV
                sim_mev = float(p['mass_me']) * self.ME_TO_MEV

                error = abs(sim_mev - real_mev) / real_mev * 100.0

                if error < best_error:
                    best_error = error
                    best_match = p
                    best_match['mev_calc'] = sim_mev

            # Vyhodnocení
            if best_error < tol:
                hits += 1
                color_code = "" # V konzoli bez barev pro kompatibilitu, nebo ANSI
                status = "MATCH"
            else:
                status = "MISS"

            if status == "MATCH":
                k_str = str(best_match['k'])
                # Zjistit, jestli detektor předpověděl stabilitu správně
                # (např. Proton by měl být STABLE, Muon UNSTABLE nebo RESONANCE)
                stab = best_match['prediction']

                print(f" {name:<12} | {real_mev:<10.2f} | {best_match['mev_calc']:<10.2f} | {best_error:<8.3f} | {best_match['scale']:<15} | {k_str:<4} | {stab}")

        print("-" * 80)
        print(f" VÝSLEDEK: Nalezeno {hits} z {len(self.KNOWN_PARTICLES)} částic uvnitř tolerance.")

    def audit_nuclear_stability(self):
        """
        Hledá 'Alpha Wall' v datech. Kde končí stabilita?
        """
        print("\n" + "="*80)
        print(" AUDIT 2: HRANICE JADERNÉ STABILITY (ALPHA WALL)")
        print("="*80)

        # 1. Seskupit data podle Z (hledáme nejtěžší stabilní izotop pro každé Z)
        elements = {} # Z -> {max_mass_efficiency, prediction}

        for atom in self.atoms:
            z = int(atom['Z'])
            a = int(atom['A'])

            # Získat vypočtené hodnoty
            raw_mass = float(atom['mass_theory_me'])
            binding_unit = float(atom['binding_unit_me'])

            # Simulace neměla "reálnou hmotnost", takže Alpha Wall se těžko hledá přímo.
            # Ale máme 'charge_stress' (Weak Force). Podíváme se, co říká on.

            is_stable = (atom['prediction_weak'] == 'STABLE')

            if z not in elements:
                elements[z] = {'stable_isotopes': 0, 'max_A': 0}

            if is_stable:
                elements[z]['stable_isotopes'] += 1
                if a > elements[z]['max_A']:
                    elements[z]['max_A'] = a

        # 2. Vypsat kritické body (Kde se to láme?)
        print(f" {'PRVEK (Z)':<10} | {'STABILNÍ IZOTOPY':<20} | {'NEJTĚŽŠÍ A'}")
        print("-" * 60)

        check_points = [1, 2, 6, 8, 20, 26, 82, 83, 84, 92, 110, 120]

        for z in sorted(elements.keys()):
            if z in check_points:
                data = elements[z]
                status = ""
                if data['stable_isotopes'] == 0: status = " (NEDOSTUPNÉ)"

                print(f" Z = {z:<6} | {data['stable_isotopes']:<20} | A = {data['max_A']} {status}")

        print("-" * 60)
        # Analýza konce tabulky
        last_stable = 0
        for z in sorted(elements.keys()):
            if elements[z]['stable_isotopes'] > 0:
                last_stable = z

        print(f" POSLEDNÍ PRVEK, KTERÝ MÁ ALESPOŇ 1 'STABILNÍ' IZOTOP: Z = {last_stable}")
        if last_stable > 83:
            print(" [VAROVÁNÍ] Model ignoruje rozpad alfa/štěpení (chybí Strong Force limit).")
            print("            Model momentálně řeší pouze Beta stabilitu (Charge Stress).")
        else:
            print(" [ÚSPĚCH] Model správně předpověděl konec stability.")

if __name__ == "__main__":
    auditor = DataAuditor()
    auditor.load_data()
    auditor.audit_particle_spectrum()
    auditor.audit_nuclear_stability()