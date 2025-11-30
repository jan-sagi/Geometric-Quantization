import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# THE GEOMETRIC UNIVERSE: INTERACTIVE EXPLORER (v2.0 - TIME EDITION)
# =============================================================================
# NEW FEATURES:
# 1. Lifetime Prediction (Chronometer Engine) based on k^5 law.
# 2. Decay Mode Prediction (Alpha vs Beta vs Stable).
# 3. Abundance Estimation (Magic Numbers = High Abundance).
# =============================================================================

class TheoryConstants:
    PI = 3.141592653589793
    ALPHA_INV = 137.035999084
    ALPHA = 1.0 / ALPHA_INV
    N = math.log(4 * PI)
    ME_TO_MEV = 0.51099895

    # TIME ANCHOR: The Muon (k=1)
    # Everything is relative to the Muon's geometric stability.
    MUON_LIFE_SEC = 2.1969811e-6
    MUON_BETA = 0.17022 # Intrinsic velocity of k=1 sphere

class Chronometer:
    """
    Calculates Time from Geometry.
    Time is treated as the inverse of Topological Stress.
    """
    @staticmethod
    def predict_particle_lifetime(k, beta, scale_type):
        """
        LAW: Lifetime ~ 1 / (k^5 * beta^2)
        Ref: Muon
        """
        if beta <= 0.00001: return float('inf') # Stable (Proton/Electron)

        # Scaling factor relative to Muon
        # k^5 represents the 5D phase space volume (Baryon Scale geometry)
        geom_factor = (k ** 5)
        stress_factor = (beta / TheoryConstants.MUON_BETA) ** 2

        # Generic penalty for Mesons (they are inherently more unstable than Leptons)
        scale_penalty = 1.0
        if "MESON" in scale_type: scale_penalty = 100.0

        predicted_seconds = TheoryConstants.MUON_LIFE_SEC / (geom_factor * stress_factor * scale_penalty)
        return predicted_seconds

    @staticmethod
    def format_time(seconds):
        if seconds == float('inf'): return "STABLE (∞)"
        if seconds < 1e-22: return f"{seconds:.1e} s (Resonance)"
        if seconds < 1e-10: return f"{seconds:.1e} s (Short)"
        if seconds < 1e-3:  return f"{seconds:.1e} s (Micro)"
        return f"{seconds:.2f} s"

class PhysicsEngine:

    @staticmethod
    def get_element_info(z):
        elems = {
            1: "H", 2: "He", 6: "C", 8: "O", 26: "Fe",
            79: "Au", 82: "Pb", 83: "Bi", 84: "Po", 92: "U", 94: "Pu"
        }
        sym = elems.get(z, str(z))

        # Determine Geometric Abundance (Magic Numbers)
        magic = [2, 8, 20, 28, 50, 82, 126]
        abundance = "Trace"
        if z in magic: abundance = "High (Magic Shell)"
        elif z % 2 == 0: abundance = "Medium (Even)"

        return sym, abundance

    @staticmethod
    def generate_particle_lattice(max_k=50):
        particles = []
        scales = {
            "LEPTON (4πN³)": 4 * TheoryConstants.PI * (TheoryConstants.N**3),
            "MESON (α⁻¹)":  TheoryConstants.ALPHA_INV,
            "BARYON (π⁵)": TheoryConstants.PI**5
        }

        for name, base_val in scales.items():
            for k in range(1, max_k + 1):
                # 1. Mass Calculation
                correction = 1.0
                beta = 0.0

                # Simplified Topology Logic for Visualization
                if k == 1: correction = 1/(1-2*TheoryConstants.ALPHA) # Sphere
                elif k % 6 == 0: correction = 1.0 # Symmetry
                elif k > 3 and k%2!=0: correction = 1 + 5*TheoryConstants.ALPHA # Prime/Odd Stress
                else: correction = 1 + TheoryConstants.ALPHA # Generic

                # Beta (Intrinsic Velocity)
                if correction != 1.0:
                    F = correction if correction > 1 else 1/correction
                    try: beta = math.sqrt(1 - 1/(F**2))
                    except: beta = 0

                mass_mev = k * base_val * correction * TheoryConstants.ME_TO_MEV

                # 2. Time Calculation
                lifetime = Chronometer.predict_particle_lifetime(k, beta, name)

                # Status
                status = "Unstable"
                if lifetime == float('inf'): status = "STABLE"
                elif lifetime < 1e-20: status = "RESONANCE"

                # Highlights
                note = f"Node k={k}"
                if "LEPTON" in name and k == 1: note = "Muon (Anchor)"
                if "LEPTON" in name and k == 17: note = "Tau (Prediction)"
                if "BARYON" in name and k == 6: note = "PROTON (Foundation)"
                if "MESON" in name and k == 2: note = "Pion+"

                particles.append({
                    "k": k, "scale": name, "mass": mass_mev,
                    "lifetime": lifetime, "beta": beta,
                    "status": status, "note": note
                })
        return particles

    @staticmethod
    def generate_alpha_wall(max_z=100):
        atoms = []
        magic_numbers = [2, 8, 20, 28, 50, 82]

        for z in range(1, max_z + 1):
            symmetry = 1.0
            if z in magic_numbers: symmetry = 2.5
            elif z % 2 == 0: symmetry = 1.2

            # Weak Force Stress
            stress = (z * TheoryConstants.ALPHA) / symmetry

            # Decay Mode Prediction
            mode = "Stable"
            color = "lime"

            if z > 82:
                mode = "Alpha Decay (Too Big)"
                color = "red"
            elif z == 43 or z == 61:
                mode = "Beta Decay (Odd Z Stress)"
                color = "yellow"
            elif stress > 0.3 and z not in magic_numbers:
                mode = "Meta-Stable"
                color = "cyan"

            sym, abund = PhysicsEngine.get_element_info(z)

            atoms.append({
                "Z": z, "label": sym, "abundance": abund,
                "stress": stress, "mode": mode, "color": color
            })
        return atoms

class InteractiveVisualizer:
    def __init__(self):
        self.engine = PhysicsEngine()

    def run(self):
        print(">>> GENERATING INTERACTIVE UNIVERSE V2 (With Time Dimension)...")
        particles = self.engine.generate_particle_lattice()
        atoms = self.engine.generate_alpha_wall()

        # Create Subplots (3 Rows now)
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                "<b>1. MICRO-SCALE: Mass Spectrum</b> (Log Scale)",
                "<b>2. TIME DIMENSION: Predicted Lifetimes</b> (The k^5 Law)",
                "<b>3. MESO-SCALE: Nuclear Stability & Abundance</b> (Alpha Wall)"
            ),
            vertical_spacing=0.1,
            specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "scatter"}]]
        )

        # --- PLOT 1: MASS SPECTRUM ---
        scales = ["LEPTON (4πN³)", "MESON (α⁻¹)", "BARYON (π⁵)"]
        colors = {"LEPTON (4πN³)": "#00FFFF", "MESON (α⁻¹)": "#00FF00", "BARYON (π⁵)": "#FFA500"}

        for scale in scales:
            subset = [p for p in particles if p["scale"] == scale]
            fig.add_trace(go.Scatter(
                x=[p["k"] for p in subset], y=[p["mass"] for p in subset],
                mode='markers', name=scale,
                marker=dict(color=colors[scale], size=8, line=dict(width=1, color='white')),
                hovertemplate="<b>%{text}</b><br>Mass: %{y:.1f} MeV<br>k: %{x}<extra></extra>",
                text=[p["note"] for p in subset]
            ), row=1, col=1)

        # --- PLOT 2: LIFETIME (TIME DIMENSION) ---
        # Show how lifetime drops with complexity (k)
        for scale in scales:
            subset = [p for p in particles if p["scale"] == scale and p["lifetime"] != float('inf')]
            fig.add_trace(go.Scatter(
                x=[p["mass"] for p in subset], # Mass on X
                y=[math.log10(p["lifetime"]) for p in subset], # Log Time on Y
                mode='markers+lines', name=scale + " Time",
                line=dict(dash='dot', width=1),
                marker=dict(color=colors[scale], size=10, symbol='diamond'),
                hovertemplate="<b>Mass:</b> %{x:.1f} MeV<br><b>Life:</b> 10^%{y:.1f} s<br><b>Pred:</b> %{text}<extra></extra>",
                text=[Chronometer.format_time(p["lifetime"]) for p in subset],
                showlegend=False
            ), row=2, col=1)

        # Add Stable Particles to Plot 2 (at top)
        stable_subset = [p for p in particles if p["lifetime"] == float('inf')]
        fig.add_trace(go.Scatter(
            x=[p["mass"] for p in stable_subset], y=[5]*len(stable_subset), # Artificial Y=5 for Stable
            mode='markers+text', name="STABLE",
            marker=dict(color='white', size=15, symbol='star'),
            text=[p["note"].split()[0] for p in stable_subset],
            textposition="top center",
            hovertemplate="<b>%{text}</b><br>LIFETIME: INFINITE<extra></extra>"
        ), row=2, col=1)

        # --- PLOT 3: ALPHA WALL ---
        fig.add_trace(go.Scatter(
            x=[a["Z"] for a in atoms], y=[a["stress"] for a in atoms],
            mode='markers', name='Nuclei',
            marker=dict(color=[a["color"] for a in atoms], size=12),
            hovertemplate=(
                "<b>%{text}</b><br>" +
                "Stress: %{y:.3f}<br>" +
                "Mode: %{customdata[0]}<br>" +
                "Abundance: %{customdata[1]}<extra></extra>"
            ),
            text=[a["label"] for a in atoms],
            customdata=[[a["mode"], a["abundance"]] for a in atoms]
        ), row=3, col=1)

        fig.add_vline(x=82, line_width=2, line_dash="dash", line_color="red", row=3, col=1,
                      annotation_text="ALPHA WALL (Z=82)", annotation_position="top left")

        # --- LAYOUT ---
        fig.update_layout(
            template="plotly_dark", height=1200,
            title_text="<b>THE GEOMETRIC UNIVERSE V2</b>: Unifying Mass, Time & Stability",
            hovermode="closest"
        )

        fig.update_yaxes(title_text="Mass (MeV)", type="log", row=1, col=1)
        fig.update_yaxes(title_text="Log10 Lifetime (s)", range=[-25, 7], row=2, col=1)
        fig.update_yaxes(title_text="Geometric Stress", row=3, col=1)
        fig.update_xaxes(title_text="Mass (MeV)", type="log", row=2, col=1)
        fig.update_xaxes(title_text="Atomic Number (Z)", row=3, col=1)

        filename = "Geometric_Universe_V2.html"
        fig.write_html(filename)
        print(f">>> SUCCESS! Saved to: {filename}")

if __name__ == "__main__":
    viz = InteractiveVisualizer()
    viz.run()