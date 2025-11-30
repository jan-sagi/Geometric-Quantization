import numpy as np
import matplotlib.pyplot as plt
import sys

class GeometricUniverseCore:
    def __init__(self):
        # Axiomy
        self.PI = 3.141592653589793
        self.alpha_inv = 4*(self.PI**3) + (self.PI**2) + self.PI
        self.alpha = 1.0 / self.alpha_inv

        # Frekvence mřížky (Vakuová báze)
        self.vacuum_freq = 137.036

        print("="*60)
        print(f" GEOMETRIC QUANTIZATION: SCHRODINGER DECODER v2.0")
        print("="*60)
        print(f" [SYSTEM]  Lattice Stiffness (Alpha^-1): {self.alpha_inv:.6f}")
        print(f" [SYSTEM]  Vacuum Frequency:             {self.vacuum_freq:.3f} Hz (Simulated)")
        print(f" [MODE]    DETERMINISTIC (Hidden Variables Visible)")
        print("-" * 60)

class GeometricNode:
    def __init__(self, name, k_node, topology_type="Prime"):
        self.name = name
        self.k = k_node
        self.topology = topology_type

        # Nastavení stresu podle topologie (Tvá teorie)
        if topology_type == "Perfect":
            self.stress = 0.00
            self.desc = "Stable (Proton-like)"
        elif topology_type == "Prime":
            self.stress = 0.26
            self.desc = "Unstable (High Stress/Tau-like)"
        else:
            self.stress = 0.15
            self.desc = "Meta-stable (Composite)"

        # Intrinsická rychlost fáze
        self.phase_velocity = self.stress * 100.0 + 50.0 # Offset aby to kmitalo jinak než vakuum

        print(f" [TARGET]  Node Name:    {self.name}")
        print(f" [TARGET]  Topology:     k={self.k} ({self.topology})")
        print(f" [TARGET]  Stress Level: {self.stress:.4f} -> {self.desc}")
        print(f" [TARGET]  Phase Velocity: {self.phase_velocity:.2f}")
        print("-" * 60)

    def get_amplitude(self, t):
        # 1. Vlnění uzlu (Intrinsická geometrie)
        node_wave = np.sin(t * self.phase_velocity)

        # 2. Vlnění vakua (Rezonanční pozadí)
        vacuum_wave = np.sin(t * 137.036)

        # 3. Interference (Superpozice)
        # Pokud se vrcholy potkají, amplituda roste
        total_amplitude = (node_wave + vacuum_wave) / 2.0
        return total_amplitude

def run_simulation():
    # Nastavení simulace
    universe = GeometricUniverseCore()

    # ZDE VYTVÁŘÍME SCHRÖDINGEROVU KOČKU
    # Změň topology_type na "Perfect" a uvidíš, že se nikdy nerozpadne (Proton)
    cat = GeometricNode("Schrodinger's Cat (Tau Particle)", 17, topology_type="Prime")

    # Parametry času
    duration = 0.6
    steps = 2000
    time_points = np.linspace(0, duration, steps)

    # Logování
    trajectory_geo = []
    trajectory_qm = []

    death_time = None
    death_amplitude = 0
    death_prob = 0

    print("\n>>> STARTING HIGH-RESOLUTION SCAN...")

    for i, t in enumerate(time_points):
        # 1. Získání deterministické amplitudy (Skrytá proměnná)
        amp = cat.get_amplitude(t)
        trajectory_geo.append(amp)

        # 2. Kvantová pravděpodobnost (To co vidí fyzik - kvadrát)
        prob = amp**2
        trajectory_qm.append(prob)

        # 3. Detekce "Blízké smrti" (Near Miss) - jen pro info do konzole
        # Pokud se amplituda blíží 0.9, ale nepřekročí ji
        if 0.90 < abs(amp) < 0.98:
            # Vypisujeme jen každých 50 kroků aby se nezahltila konzole
            if i % 50 == 0 and death_time is None:
                print(f" [WARNING] t={t:.4f} | Lattice Strain: {abs(amp)*100:.1f}% | Stability Critical...")

        # 4. DETEKCE ROZPADU (ALPHA WALL BREACH)
        # Práh je nastaven na 0.98 (98% saturace mřížky)
        if abs(amp) >= 0.98 and death_time is None:
            death_time = t
            death_amplitude = amp
            death_prob = prob

            print("\n" + "!"*60)
            print(f" >>> CRITICAL RESONANCE FAILURE (DECAY EVENT) <<<")
            print("!"*60)
            print(f" Time of Death (t):       {t:.5f} s")
            print("-" * 40)
            print(f" GEOMETRIC REALITY (YOU):")
            print(f"   > Amplitude:           {amp:.5f} (Constructive Interference)")
            print(f"   > Lattice Saturation:  {abs(amp)/1.0 * 100:.2f} %")
            print(f"   > Status:              WALL BREACHED")
            print("-" * 40)
            print(f" QUANTUM OBSERVER (THEM):")
            print(f"   > Probability (|ψ|²):  {prob:.2%} chance of decay")
            print(f"   > Interpretation:      'Bad luck, the wavefunction collapsed.'")
            print("!"*60 + "\n")

            # Můžeme ukončit smyčku, pokud chceme simulovat "konec",
            # ale necháme ji běžet pro graf
            # break

    # --- SOUHRNNÁ ZPRÁVA NA KONCI ---
    print("\n" + "="*30)
    print(" FINAL SIMULATION REPORT")
    print("="*30)
    if death_time:
        print(f" RESULT:  The Cat is DEAD.")
        print(f" CAUSE:   Geometric Topology Stress (Prime Node).")
        print(f" TIMING:  t = {death_time:.5f}")
    else:
        print(f" RESULT:  The Cat is ALIVE.")
        print(f" CAUSE:   Perfect Symmetry (Proton-like stability).")
        print(f" NOTE:    Lattice strain never exceeded Alpha Wall.")
    print("="*30)

    # --- GRAFICKÝ VÝSTUP (MATPLOTLIB) ---
    # Ten zůstává stejný, protože je vizuálně perfektní
    plt.figure(figsize=(12, 8))

    # Graf 1: Deterministická geometrie
    plt.subplot(2, 1, 1)
    plt.plot(time_points, trajectory_geo, color='#00cc00', linewidth=1.5, label='Geometric Amplitude (Hidden)')
    plt.axhline(y=0.98, color='red', linestyle='--', linewidth=2, label='Alpha Wall (+)')
    plt.axhline(y=-0.98, color='red', linestyle='--', linewidth=2, label='Alpha Wall (-)')
    if death_time:
        plt.axvline(x=death_time, color='black', linestyle='-', linewidth=2, label='DECAY MOMENT')
        plt.scatter([death_time], [death_amplitude], color='red', s=100, zorder=5)
        plt.text(death_time, death_amplitude + (0.1 if death_amplitude > 0 else -0.2), " WALL BREACH", color='red', fontweight='bold')

    plt.title(f"REALITY: Deterministic Geometric Waves (Prime Node k={cat.k})", fontsize=12)
    plt.ylabel("Lattice Amplitude", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')

    # Graf 2: Kvantová pravděpodobnost
    plt.subplot(2, 1, 2)
    plt.plot(time_points, trajectory_qm, color='#0066ff', linewidth=2, label='Wavefunction |ψ|²')
    plt.fill_between(time_points, trajectory_qm, color='#0066ff', alpha=0.3)
    if death_time:
         plt.axvline(x=death_time, color='red', linestyle=':', linewidth=2, label='Observed Collapse')

    plt.title("APPROXIMATION: What Quantum Mechanics Sees (Probability)", fontsize=12)
    plt.ylabel("Probability P(t)", fontsize=10)
    plt.xlabel("Time (simulation units)", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()