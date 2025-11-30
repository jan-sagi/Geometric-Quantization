import matplotlib.pyplot as plt
import numpy as np
import math

# --- CONFIGURATION ---
PI = np.pi
N = np.log(4 * PI)
ME_MEV = 0.510998950
SCALE_LEPTON = 4 * PI * (N**3) * ME_MEV  # ~ 104.12 MeV

# --- DATA FROM TEST (Tau Neighborhood) ---
# Format: k, Theory_Mass, Real_Name, Real_Mass
ladder_data = [
    (15, 15 * SCALE_LEPTON, "N(1535)", 1535.0),
    (16, 16 * SCALE_LEPTON, "Omega-", 1672.45),
    (17, 17 * SCALE_LEPTON, "Tau (Lepton)", 1776.86),
    (18, 18 * SCALE_LEPTON, "D+ (Meson)", 1869.65),
    (19, 19 * SCALE_LEPTON, "D_s+ (Meson)", 1968.34),
    (20, 20 * SCALE_LEPTON, "???", None), # Noise / Gap checking
    (21, 21 * SCALE_LEPTON, "Lambda_c?", 2286.46) # k=21 is 2186 (gap), Lambda_c is higher
]

def plot_ladder():
    k_vals = [d[0] for d in ladder_data]
    theory_vals = [d[1] for d in ladder_data]

    real_k = []
    real_mass = []
    labels = []

    for k, t_mass, name, r_mass in ladder_data:
        if r_mass is not None:
            real_k.append(k)
            real_mass.append(r_mass)
            labels.append(name)

    plt.figure(figsize=(10, 6))

    # 1. Theoretical Line (Linear regression through theory)
    plt.plot(k_vals, theory_vals, '--', color='gray', alpha=0.5, label=f'Geometric Theory ($k \\times 4\\pi N^3$)')

    # 2. Theory Nodes
    plt.scatter(k_vals, theory_vals, s=100, facecolors='none', edgecolors='blue', label='Theory Nodes')

    # 3. Real Particles
    colors = ['red' if 'Tau' in l else 'green' for l in labels]
    plt.scatter(real_k, real_mass, s=100, color=colors, marker='x', label='Real Particles (NIST)')

    # Labels / Annotations
    for i, txt in enumerate(labels):
        offset = 15 if i % 2 == 0 else -25
        plt.annotate(txt, (real_k[i], real_mass[i]),
                     xytext=(0, offset), textcoords='offset points', ha='center',
                     fontsize=9, fontweight='bold' if 'Tau' in txt else 'normal')

    # Styling
    plt.title(f"The 'Tau Ladder': Unified Scaling of Leptons & Hadrons\n(Base Scale: $4\\pi N^3 \\approx 104.1$ MeV)", fontsize=12)
    plt.xlabel("Geometric Node Integer (k)")
    plt.ylabel("Mass (MeV)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    print("Generating 'Tau Ladder' graph...")
    plt.savefig("tau_ladder_proof.png")
    plt.show()

if __name__ == "__main__":
    plot_ladder()