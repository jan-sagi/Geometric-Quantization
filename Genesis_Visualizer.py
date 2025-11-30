import numpy as np
import matplotlib.pyplot as plt
import math
import os
import sys

# =============================================================================
# GENESIS VISUALIZER: THE BIRTH OF MATTER (Fixed Layout)
# =============================================================================
# OBJECTIVE: Visualize the Casimir Pressure Curve and the breakdown point
#            where Vacuum Energy converts into Electron Mass.
# FIXES:     Improved label positioning and readability on log-scales.
# =============================================================================

# --- LOGGER ---
class DualLogger:
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
    H_BAR = 1.054571817e-34
    C = 299792458
    ME_KG = 9.10938356e-31

    # Energy of Pair Creation (2 * me * c^2)
    PAIR_ENERGY = 2 * ME_KG * (C**2)

    # Compton Wavelength (Size of Electron Interaction)
    LAMBDA_C = (2 * PI * H_BAR) / (ME_KG * C)

def visualize_genesis():
    # Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Genesis_Vis_Log.txt"))

    print(f"{'='*80}")
    print(f" VISUALIZING THE GENESIS POINT (High Readability Mode)")
    print(f"{'-'*80}")

    # 1. Define Range (from Atom size down to Breakdown)
    # Logspace from 100 pm down to 0.005 pm
    d_pm = np.logspace(2, -2.3, 500)
    d_meters = d_pm * 1e-12

    # 2. Calculate Vacuum Energy in the Cell (Volume d^3)
    # E = P * V = (pi^2 * hbar * c) / (240 * d)
    numerator = (Constants.PI**2) * Constants.H_BAR * Constants.C
    energy_vacuum = numerator / (240 * d_meters)

    # 3. Target Energy (Constant Line)
    energy_matter = np.full_like(d_meters, Constants.PAIR_ENERGY)

    # 4. Find Intersection (Genesis Point)
    idx = np.argwhere(np.diff(np.sign(energy_vacuum - energy_matter))).flatten()
    d_crit_pm = d_pm[idx][0]

    print(f" Critical Distance found at: {d_crit_pm:.6f} pm")

    # --- PLOTTING ---
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8)) # Wider aspect ratio

    # Curves
    ax.plot(d_pm, energy_vacuum, color='#00FFFF', linewidth=2.5, label='Vacuum Stress Energy (Casimir Pressure)')
    ax.plot(d_pm, energy_matter, color='#00FF00', linewidth=2.5, linestyle='--', label='Electron-Positron Mass Limit')

    # --- ANNOTATIONS (Improved) ---

    # 1. Intersection Marker (Genesis Point)
    ax.scatter(d_crit_pm, Constants.PAIR_ENERGY, s=300, color='white', edgecolors='red', zorder=10, linewidth=2)

    # Label with arrow pointing to the dot
    ax.annotate('GENESIS POINT\n(Lattice Breakdown)',
                xy=(d_crit_pm, Constants.PAIR_ENERGY),
                xytext=(-20, 40), textcoords='offset points',
                arrowprops=dict(facecolor='white', shrink=0.05),
                fontsize=12, fontweight='bold', color='white',
                bbox=dict(boxstyle="round,pad=0.3", fc="red", alpha=0.7))

    # 2. Reference Line: Compton Wavelength
    lambda_pm = Constants.LAMBDA_C * 1e12
    ax.axvline(x=lambda_pm, color='yellow', linestyle=':', linewidth=2, alpha=0.8)

    # Label for Electron Size (Placed at the top to avoid clutter)
    ax.text(lambda_pm * 1.1, energy_vacuum[0], "Electron Size\n(Compton Wavelength)",
            color='yellow', fontsize=11, fontweight='bold', va='top',
            bbox=dict(boxstyle="round", fc="black", alpha=0.6))

    # 3. THE RESULT BOX (Pi^5) - Floating in empty space
    ratio = lambda_pm / d_crit_pm

    info_text = (
        f"GEOMETRIC DISCOVERY:\n"
        f"--------------------\n"
        f"Electron Size / Genesis Point\n"
        f"= {ratio:.1f}\n"
        f"≈ Pi^5 (Proton Geometry)"
    )

    # Place box in top-center-left area (relative to axes)
    ax.text(0.35, 0.20, info_text, transform=ax.transAxes,
            fontsize=14, color='#00FF00', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", fc="#202020", ec="#00FF00", lw=2))

    # 4. Connection Arrow (Visualizing the compression range)
    # Draws a double-headed arrow between Genesis and Electron Size
    ax.annotate('', xy=(d_crit_pm, Constants.PAIR_ENERGY * 0.3),
                xytext=(lambda_pm, Constants.PAIR_ENERGY * 0.3),
                arrowprops=dict(arrowstyle='<->', color='white', lw=1.5))
    ax.text(math.sqrt(d_crit_pm * lambda_pm), Constants.PAIR_ENERGY * 0.2,
            f"Compression Factor: {ratio:.1f}x",
            color='white', ha='center', fontsize=10)

    # Scales & Labels
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel("Lattice Compression Distance (pm)", fontsize=14)
    ax.set_ylabel("Energy per Cell (Joules)", fontsize=14)
    ax.set_title("THE ORIGIN OF MASS: Vacuum Breakdown at Pi^5", fontsize=18, color='white', pad=20)

    ax.legend(loc='upper right', fontsize=12)
    ax.grid(True, which="major", ls="-", alpha=0.3)
    ax.grid(True, which="minor", ls=":", alpha=0.1)

    plt.tight_layout()

    save_path = os.path.join(script_dir, "Genesis_Graph.png")
    plt.savefig(save_path, dpi=300)
    print(f" Graph saved to: {save_path}")
    print(f"{'='*80}")

    # plt.show() # Uncomment if you have a display

if __name__ == "__main__":
    visualize_genesis()