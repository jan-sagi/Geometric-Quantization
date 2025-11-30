import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import os

# =============================================================================
# GEOMETRIC VACUUM DYNAMICS: POTENTIAL LANDSCAPE
# =============================================================================
# OBJECTIVE: Visualize the vacuum not as empty space, but as an energetic
#            topological landscape.
# CONCEPT:   Particles are "marbles" rolling into geometric wells.
#            Unstable particles are on peaks; Stable particles are in deep valleys.
# =============================================================================

# --- LOGGER CLASS ---
class DualLogger:
    """Redirects stdout to both console and a log file."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

class Constants:
    PI = np.pi
    ALPHA = 1.0 / 137.035999
    N = np.log(4 * PI)

    # Scale for energy normalization (Muon base)
    BASE_ENERGY = 105.66

def get_geometric_potential(k, scale_type):
    """
    Calculates the 'Topological Potential' of a node.
    Logic: Potential ~ -1 / (Geometric Stress)
    """
    # 1. Symmetry Factor (Divisors)
    # More divisors = Better symmetry = Lower Stress
    divisors = 0
    for i in range(1, int(math.sqrt(k)) + 1):
        if k % i == 0:
            divisors += 2 if i*i != k else 1

    symmetry_factor = divisors
    if symmetry_factor == 0: symmetry_factor = 1 # Safety

    # 2. Prime Penalty (Asymmetry)
    is_prime = True
    if k > 1:
        for i in range(2, int(math.sqrt(k)) + 1):
            if k % i == 0: is_prime = False

    # Primes > 3 cause topological stress
    if is_prime and k > 3:
        symmetry_factor = 0.5

    # 3. Intrinsic Velocity / Beta (Correction Factor)
    correction = 1 + (k * Constants.ALPHA) if scale_type == "LEPTON" else 1.0

    # PROTON SINGULARITY (k=6 Baryon)
    # Perfect Hexagonal Symmetry implies zero stress.
    if scale_type == "BARYON" and k % 6 == 0:
        correction = 0.0

    # Stress Calculation
    stress = (correction ** 4) / symmetry_factor

    # 4. Potential Inversion
    # High Stress = High Potential (Peak/Flat) -> Unstable
    # Low Stress = Low Potential (Deep Well) -> Stable

    if stress <= 1e-9:
        potential = -20.0 # Artificial depth for "Infinite Stability" (The Proton)
    else:
        potential = -1.0 / stress

    return potential

def simulate_vacuum_landscape():
    # Setup Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Vacuum_Dynamics_Log.txt"))

    print(f"{'='*80}")
    print(f" VACUUM DYNAMICS SIMULATOR")
    print(f" Generating topological potential map...")
    print(f"{'-'*80}")

    k_values = np.arange(1, 50)

    # Generate landscapes
    potentials_baryon = [get_geometric_potential(k, "BARYON") for k in k_values]
    potentials_lepton = [get_geometric_potential(k, "LEPTON") for k in k_values]

    # --- VISUALIZATION ---
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the "Gravity Wells" of the Lattice
    ax.plot(k_values, potentials_baryon, color='orange', linewidth=2, label='Baryon Field (Pi^5)')
    ax.plot(k_values, potentials_lepton, color='cyan', linewidth=2, linestyle='--', label='Lepton Field (N^3)')

    # Highlight Key Particles (Attractors)
    particles = [
        (6, "PROTON", "BARYON", -20.0, 'gold'), # The Deepest Well
        (1, "MUON", "LEPTON", -1.0, 'cyan'),
        (17, "TAU", "LEPTON", -0.3, 'red'),     # High on the hill
        (2, "PION", "MESON", -1.9, 'lime')
    ]

    print(f" {'PARTICLE':<10} | {'k':<3} | {'POTENTIAL':<10} | {'STATUS'}")
    print(f"{'-'*80}")

    for k, name, scale, y_fake, col in particles:
        # Get real calculated Y
        idx = k - 1
        y_val = potentials_baryon[idx] if scale == "BARYON" else potentials_lepton[idx]

        status = "UNSTABLE"
        if y_val < -10: status = "STABLE (Singularity)"
        elif y_val < -1.5: status = "META-STABLE"

        print(f" {name:<10} | {k:<3} | {y_val:<10.4f} | {status}")

        # Plot Marker
        ax.scatter(k, y_val, s=200, color=col, edgecolors='white', zorder=10)
        ax.text(k, y_val + 0.8, name, color=col, ha='center', fontweight='bold')

        # Visualizing Decay (Arrow down the gradient)
        if name == "TAU":
            # Tau (k=17) falls toward Muon (k=1)
            ax.annotate("", xy=(2, potentials_lepton[1]), xytext=(17, y_val),
                        arrowprops=dict(arrowstyle="->", color='red', linestyle='dotted', lw=2))
            ax.text(9, (y_val + potentials_lepton[1])/2 + 0.5, "DECAY PATH", color='red', fontsize=9)

    ax.set_title("VACUUM DYNAMICS: The Potential Landscape of Geometry", fontsize=16, color='white')
    ax.set_xlabel("Geometric Node (k)", fontsize=12)
    ax.set_ylabel("Topological Stability (Deeper = More Stable)", fontsize=12)

    ax.grid(True, linestyle='--', alpha=0.2)
    ax.legend(loc='center right')

    # Save and Show
    save_path = os.path.join(script_dir, "Vacuum_Landscape.png")
    plt.savefig(save_path, dpi=150)
    print(f"{'='*80}")
    print(f" Graph saved to: {save_path}")
    print(f" Interpretation: Particles 'roll' into the nearest geometric well.")
    print(f" Tau (k=17) is on an unstable slope. Proton (k=6) is at the bottom of the abyss.")

    plt.show()

if __name__ == "__main__":
    simulate_vacuum_landscape()