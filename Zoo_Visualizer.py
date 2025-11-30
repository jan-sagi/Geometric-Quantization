import plotly.graph_objects as go
import csv
import os

class ZooVisualizer:
    def __init__(self):
        self.predictions = []
        self.real_particles = [
            # (Mass MeV, Name, Scale_Hint)
            (0.511, "Electron", "LEPTON"),
            (105.66, "Muon", "LEPTON"),
            (139.57, "Pion+", "MESON"),
            (493.67, "Kaon+", "MESON"),
            (547.86, "Eta", "MESON"),
            (775.26, "Rho", "MESON"),
            (938.27, "Proton", "BARYON"),
            (939.57, "Neutron", "BARYON"),
            (1019.46, "Phi", "MESON"),
            (1115.68, "Lambda", "BARYON"),
            (1776.86, "Tau", "LEPTON"),
            (1869.65, "D+", "MESON"),
            (3096.90, "J/Psi", "MESON"),
            (5279.32, "B+", "MESON"),
            (9460.30, "Upsilon", "MESON"),
            (125100.0, "Higgs", "BOSON")
        ]

    def load_predictions(self):
        filename = "Particle_Zoo_Predictions.csv"
        if not os.path.exists(filename):
            print("CHYBA: Nejdřív spusť Particle_Zoo_Generator.py!")
            return

        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filtrujeme jen zajímavé kandidáty pro vizualizaci (do 10 GeV)
                mass = float(row['Mass_MeV'])
                if mass < 15000:
                    self.predictions.append(row)

    def plot_zoo(self):
        fig = go.Figure()

        # 1. Vykreslení PREDIKCÍ (Tvá teorie)
        # Rozdělíme podle topologie pro barvy
        for topo in ["Prime (Spinor)", "Hexagon (Perfect)", "Sphere (Singularity)"]:
            subset = [p for p in self.predictions if topo in p['Topology']]

            color = "gray"
            symbol = "x"
            size = 8

            if "Prime" in topo: color = "orange"; symbol = "cross"; size=10
            if "Hexagon" in topo: color = "cyan"; symbol = "diamond"; size=12
            if "Sphere" in topo: color = "magenta"; symbol = "circle"; size=12

            fig.add_trace(go.Scatter(
                x=[float(p['Mass_MeV']) for p in subset],
                y=[p['Scale'] for p in subset],
                mode='markers',
                name=f"Theory: {topo}",
                marker=dict(color=color, symbol=symbol, size=size, line=dict(width=1, color='white')),
                text=[f"k={p['Node_k']}<br>Life: {p['Lifetime_s']}" for p in subset],
                hovertemplate="<b>Theory Candidate</b><br>Mass: %{x} MeV<br>%{text}<extra></extra>"
            ))

        # 2. Vykreslení REALITY (Standardní model)
        # Musíme je přiřadit ke správné škále (Y-osa) pro porovnání

        # Mapování škál pro Y-osu
        scale_map = {
            "LEPTON": "LEPTON (4pi*N^3)",
            "MESON": "MESON (Alpha^-1)",
            "BARYON": "BARYON (Pi^5)",
            "BOSON": "BARYON (Pi^5)" # Bosony dáme k Baryonům pro vizualizaci
        }

        real_x = []
        real_y = []
        real_text = []

        for mass, name, type_hint in self.real_particles:
            real_x.append(mass)
            # Najdeme nejbližší scale v grafech (zjednodušení)
            target_y = scale_map.get(type_hint, "MESON (Alpha^-1)")
            real_y.append(target_y)
            real_text.append(name)

        fig.add_trace(go.Scatter(
            x=real_x,
            y=real_y,
            mode='markers+text',
            name='STANDARD MODEL (Real)',
            text=real_text,
            textposition="top center",
            marker=dict(color='#00FF00', size=15, symbol='circle-open', line=dict(width=2)),
            hovertemplate="<b>Confirmed Particle</b><br>%{text}<br>Mass: %{x} MeV<extra></extra>"
        ))

        # Styling
        fig.update_layout(
            template="plotly_dark",
            title="<b>THE PARTICLE ZOO: Theory vs Reality</b><br><i>Search for missing resonances</i>",
            xaxis_title="Mass (MeV) - Log Scale",
            xaxis_type="log",
            yaxis_title="Geometric Scale",
            height=800
        )

        # Uložení
        fig.write_html("Particle_Zoo_Map.html")
        print(">>> MAPA POKLADŮ VYGENEROVÁNA: Particle_Zoo_Map.html")

if __name__ == "__main__":
    viz = ZooVisualizer()
    viz.load_predictions()
    viz.plot_zoo()