import csv
import time
import sys
import os

# Import našeho vlastního enginu
# Tento skript musí být spouštěn ze složky Geometric_Simulation_Core
from Universe_Code.accelerator import GeometricAccelerator
from Universe_Code.detector import GeometricDetector

# =============================================================================
# HLAVNÍ SPOUŠTĚČ SIMULACE & ANALYZÁTOR (CLEAN VERSION)
# =============================================================================

class SimulationManager:
    def __init__(self):
        print(">>> INICIALIZACE GEOMETRICKÉHO VESMÍRU...")
        self.detector = GeometricDetector()
        self.accelerator = GeometricAccelerator(self.detector)
        self.particle_data = []
        self.atom_data = []

    def run_physics(self):
        """Spustí generování dat."""
        start_time = time.time()

        # 1. ČÁSTICOVÁ FYZIKA (High Energy Physics)
        # Skenujeme uzly k=1 až 250 (to pokryje energie hluboko za Higgse)
        print(f"\n[FÁZE 1] URYCHLOVAČ ČÁSTIC (Skenování mřížky)...")
        self.particle_data = self.accelerator.run_collision_experiment(max_k=250)
        print(f"   -> Vygenerováno {len(self.particle_data)} unikátních energetických uzlů.")

        # 2. JADERNÁ FYZIKA (Nucleosynthesis)
        # Skenujeme prvky Z=1 až Z=120 (včetně supertěžkých)
        print(f"\n[FÁZE 2] NUKLEOSYNTÉZA (Skládání atomů)...")
        self.atom_data = self.accelerator.run_nucleosynthesis(max_z=120)
        print(f"   -> Vygenerováno {len(self.atom_data)} konfigurací jader.")

        end_time = time.time()
        print(f"\n>>> SIMULACE DOKONČENA ({end_time - start_time:.2f} sekund).")

    def save_results(self):
        """Uloží surová data do CSV pro externí audit."""
        self._write_csv("universal_particles.csv", self.particle_data)
        self._write_csv("universal_atoms.csv", self.atom_data)

    def _write_csv(self, filename, data):
        if not data: return

        # Ukládáme do stejné složky, kde běží skript
        filepath = os.path.join(os.path.dirname(__file__), filename)

        # Získáme hlavičky z prvního záznamu
        keys = data[0].keys()

        try:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"   [ULOŽENO] {filename}")
        except Exception as e:
            print(f"   [CHYBA] Nelze zapsat {filename}: {e}")

    def analyze_data_console(self):
        """
        Rychlá statistická analýza pro operátora (do konzole).
        """
        print("\n" + "="*60)
        print(" ANALÝZA DAT (OKAMŽITÝ REPORT)")
        print("="*60)

        # --- 1. ANALÝZA ČÁSTIC ---
        stable_particles = [p for p in self.particle_data if p['prediction'] == 'STABLE']
        unstable_particles = [p for p in self.particle_data if p['prediction'] == 'UNSTABLE']
        resonances = [p for p in self.particle_data if p['prediction'] == 'RESONANCE']

        print(f"\n1. SPEKTRUM ČÁSTIC:")
        print(f"   Celkem uzlů:      {len(self.particle_data)}")
        print(f"   Stabilní (Inf):   {len(stable_particles)}  <-- (Kandidáti na hmotu)")
        print(f"   Nestabilní:       {len(unstable_particles)}")
        print(f"   Rezonance (Noise):{len(resonances)}")

        # Vypsat náhled stabilních částic (limit 15 řádků)
        if stable_particles:
            print(f"\n   [NÁHLED OSTROVŮ STABILITY]:")
            print(f"   {'SCALE':<15} | {'k':<3} | {'MASS (me)':<15} | {'TOPOLOGY'}")
            print("   " + "-"*50)
            for p in stable_particles[:15]:
                print(f"   {p['scale']:<15} | {p['k']:<3} | {p['mass_me']:<15.4f} | {p['topology']}")
            if len(stable_particles) > 15:
                print(f"   ... a dalších {len(stable_particles) - 15} záznamů.")

        # --- 2. ANALÝZA ATOMŮ ---
        # Hledáme stabilní jádra podle FINAL prediction (Beta i Alpha stabilita)
        stable_nuclei = [a for a in self.atom_data if a['final_prediction'] == 'STABLE']

        # Najít nejtěžší stabilní prvek (Z)
        max_z_stable = 0
        if stable_nuclei:
            max_z_stable = max(n['Z'] for n in stable_nuclei)

        print(f"\n2. ATOMOVÁ STRUKTURA:")
        print(f"   Celkem izotopů:   {len(self.atom_data)}")
        print(f"   Plně Stabilní:    {len(stable_nuclei)}")
        print(f"   Hranice stability:{max_z_stable} (Z)")

        # Interpretace výsledku
        if max_z_stable == 82 or max_z_stable == 83:
            print(f"   [FALSIFIKACE]: ÚSPĚCH. Model zastavil stabilitu na Olovu/Bismutu.")
        elif max_z_stable > 92:
            print(f"   [FALSIFIKACE]: VAROVÁNÍ. Model je příliš stabilní (vytváří supertěžké prvky).")
            print(f"                  Nutno posílit odpudivý člen v rovnici hmotnosti.")
        elif max_z_stable < 80:
            print(f"   [FALSIFIKACE]: NEÚSPĚCH. Model se zhroutil příliš brzy.")

        print("="*60)

if __name__ == "__main__":
    sim = SimulationManager()
    sim.run_physics()
    sim.save_results()
    sim.analyze_data_console()