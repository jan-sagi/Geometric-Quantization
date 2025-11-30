import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os
import re

# =============================================================================
# GEOMETRIC UNIVERSE: STABILITY & TOPOLOGY AUDIT
# =============================================================================
# HYPOTHESIS:
#   1. Prime Numbers (k) offer a "Stability Shield" against decay.
#   2. Perfect Numbers (k=6) offer "Absolute Stability" (Proton).
#   3. High-energy Primes (like k=11 on Meson scale) may fail if they
#      exceed the natural capacity of the lattice ("blown up").
# =============================================================================

# --- LOGGER CLASS ---
class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        # Remove ANSI codes for cleaner log file
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.log.write(ansi_escape.sub('', message))

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# --- CONFIGURATION ---
PI = np.pi
N = np.log(4 * PI)
ME_MEV = 0.510998950

# --- SCALES ---
# Base Energy Units (MeV)
SCALE_LEPTON = 4 * PI * (N**3) * ME_MEV  # ~ 104.12 MeV
SCALE_MESON  = 137.036 * ME_MEV          # ~ 70.02 MeV
SCALE_BARYON = (PI**5) * ME_MEV          # ~ 156.37 MeV

# --- DATASET ---
# Stable particles are given a cap for visualization (10^20 seconds)
STABLE_LIFE = 1.0e20

# Format: Name, Node k, Scale Base, Real Lifetime (s)
PARTICLES = [
    # LEPTON SCALE
    {"name": "Muon",   "k": 1,  "scale": SCALE_LEPTON, "life": 2.2e-6},
    {"name": "Tau",    "k": 17, "scale": SCALE_LEPTON, "life": 2.9e-13},

    # MESON SCALE
    {"name": "Pion+",  "k": 2,  "scale": SCALE_MESON,  "life": 2.6e-8},
    {"name": "Kaon+",  "k": 7,  "scale": SCALE_MESON,  "life": 1.2e-8},
    {"name": "Rho",    "k": 11, "scale": SCALE_MESON,  "life": 4.5e-24}, # Prime, but unstable (Lattice Saturation)
    {"name": "Eta",    "k": 8,  "scale": SCALE_MESON,  "life": 5.0e-19},
    {"name": "Omega",  "k": 11, "scale": SCALE_MESON,  "life": 7.7e-23}, # Conflict at k=11
    {"name": "Phi",    "k": 15, "scale": SCALE_MESON,  "life": 1.5e-22},
    {"name": "J/Psi",  "k": 44, "scale": SCALE_MESON,  "life": 7.2e-21},

    # BARYON SCALE
    {"name": "Proton", "k": 6,  "scale": SCALE_BARYON, "life": STABLE_LIFE}, # The Perfect Node
    {"name": "Lambda", "k": 7,  "scale": SCALE_BARYON, "life": 2.6e-10},
    {"name": "Sigma",  "k": 8,  "scale": SCALE_BARYON, "life": 8.0e-11},
    {"name": "Delta",  "k": 8,  "scale": SCALE_BARYON, "life": 5.6e-24},
]

class Formatting:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# --- FUNCTIONS ---

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

def run_stability_analysis():
    # Setup Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.stdout = DualLogger(os.path.join(script_dir, "Stability_Analysis_Log.txt"))

    print("======================================================================")
    print(" STABILITY ANALYSIS: PRIME NODES VS LIFETIME")
    print("======================================================================")
    print(f" {'PARTICLE':<10} | {'k':<3} | {'TYPE':<12} | {'LIFETIME (s)':<15}")
    print("-" * 55)

    # Lists for plotting
    # Primes
    xp, yp, lp = [], [], []
    # Composites
    xc, yc, lc = [], [], []
    # Perfect (Proton)
    xh, yh, lh = [], [], []

    for p in PARTICLES:
        k = p['k']
        prime = is_prime(k)

        # Log10 Lifetime for Graphing
        # If stable, clamp to 5.0 for visual purposes (above graph limit)
        if p['life'] >= STABLE_LIFE:
            log_life = 5.0
        else:
            log_life = math.log10(p['life'])

        # Determine Type String & Color
        type_str = "COMPOSITE"
        color_code = Formatting.RED

        if k == 6 and "Proton" in p['name']:
            type_str = "PERFECT(6)"
            color_code = Formatting.YELLOW
            xh.append(k); yh.append(log_life); lh.append(p['name'])
        elif k == 1:
            type_str = "UNIT(1)"
            color_code = Formatting.GREEN
            xc.append(k); yc.append(log_life); lc.append(p['name'])
        elif prime:
            type_str = "PRIME"
            color_code = Formatting.GREEN
            xp.append(k); yp.append(log_life); lp.append(p['name'])
        else:
            xc.append(k); yc.append(log_life); lc.append(p['name'])

        print(f" {p['name']:<10} | {k:<3} | {color_code}{type_str:<12}{Formatting.RESET} | {p['life']:.1e}")

    print("-" * 55)
    print(" OBSERVATIONS:")
    print(" 1. Low-k Primes (Pion k=2, Kaon k=7) show extended lifetimes.")
    print(" 2. High-k Primes (Rho k=11, Omega k=11) are unstable.")
    print("    -> Theory: Lattice saturation limits the 'Prime Shield' effect.")
    print(" 3. Proton (k=6) is Perfect Geometry, outliving even Primes.")
    print("======================================================================")

    # --- PLOTTING ---
    print(f"\n[INFO] Generating graph in: {script_dir}")

    plt.figure(figsize=(11, 7))

    # Threshold Lines
    plt.axhline(y=-23, color='gray', linestyle='--', alpha=0.4, label='Strong Force Limit (1e-23s)')
    plt.axhline(y=-8,  color='orange', linestyle='--', alpha=0.4, label='Weak Force Limit (1e-8s)')

    # Scatter Points
    plt.scatter(xp, yp, s=180, c='blue', marker='o', label='Prime Numbers (k)')
    plt.scatter(xc, yc, s=150, c='red', marker='s', label='Composite Numbers (k)')
    plt.scatter(xh, yh, s=300, c='gold', marker='*', edgecolors='black', label='Perfect Number (k=6)')

    # Annotations
    # Primes
    for i, txt in enumerate(lp):
        plt.annotate(txt, (xp[i], yp[i]), xytext=(0, 10), textcoords='offset points', ha='center', color='blue', fontweight='bold')
    # Composites
    for i, txt in enumerate(lc):
        offset = -20 if "Sigma" in txt else -15
        plt.annotate(txt, (xc[i], yc[i]), xytext=(0, offset), textcoords='offset points', ha='center', color='darkred')
    # Proton
    for i, txt in enumerate(lh):
        plt.annotate(txt, (xh[i], yh[i]), xytext=(0, 15), textcoords='offset points', ha='center', color='black', fontweight='bold')

    # Styling
    plt.title("Stability Analysis: Geometric Topology vs. Lifetime", fontsize=14)
    plt.xlabel("Geometric Node Integer (k)", fontsize=12)
    plt.ylabel("Log10 Lifetime (seconds)", fontsize=12)

    # Set Y-Limit to show stable/unstable contrast clearly
    plt.ylim(-25, 6)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='lower right')

    # Save
    save_path = os.path.join(script_dir, "Stability_Analysis_Plot.png")
    plt.savefig(save_path, dpi=300)
    print(f"[SUCCESS] Graph saved to: {save_path}")
    print(f"[SUCCESS] Log saved to:   {os.path.join(script_dir, 'Stability_Analysis_Log.txt')}")

    # plt.show()

if __name__ == "__main__":
    run_stability_analysis()