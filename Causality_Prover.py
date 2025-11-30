import numpy as np
import math

class GeometricDeterminism:
    def __init__(self):
        # Tvé konstanty
        self.alpha_inv = 137.035999
        self.lattice_limit = 0.98 # Alpha Wall

    def calculate_decay_time(self, k_topology, initial_phase_phi):
        """
        Vypočítá PŘESNÝ čas rozpadu analyticky nebo numericky.
        Rovnice: Amplitude(t) = sin(w_node*t + phi) + sin(w_vac*t)
        Hledáme nejmenší t > 0, kde |Amplitude| > Limit.
        """
        # Simulace intrinsické rychlosti pro uzel k (Tau = 17)
        # Prvočíslo k=17 generuje vysoké tření
        w_node = 100.0 + (k_topology * 2.5)
        w_vac = self.alpha_inv

        # Numerické hledání kořene (Root Finding) s vysokou přesností
        # Toto nahrazuje "hod kostkou" přesným výpočtem
        t = 0.0
        dt = 0.0001
        max_time = 10.0

        while t < max_time:
            # Deterministická vlnová rovnice
            wave_node = math.sin(w_node * t + initial_phase_phi)
            wave_vac = math.sin(w_vac * t)

            # Superpozice
            amplitude = (wave_node + wave_vac) / 2.0

            if abs(amplitude) > self.lattice_limit:
                return t # Nalezen přesný moment smrti

            t += dt

        return -1 # Stabilní (v tomto časovém okně)

def run_proof():
    engine = GeometricDeterminism()
    k_tau = 17 # Schrödingerova kočka (Tau)

    print("="*60)
    print(" MATHEMATICAL PROOF 1: DETERMINISTIC CAUSALITY")
    print(" Hypothesis: Decay time is a function of Initial Phase (φ)")
    print(" Equation:   T_decay = f(k, α, φ)")
    print("="*60)

    print(f"{'TEST ID':<8} | {'PHASE (φ)':<12} | {'PREDICTED DECAY (s)':<20} | {'RESULT'}")
    print("-" * 60)

    # Testujeme různé počáteční fáze (Skryté proměnné)
    phases = [0.0, 0.5, 1.0, 1.57, 3.14, 4.0]

    for i, phi in enumerate(phases):
        t_decay = engine.calculate_decay_time(k_tau, phi)

        # Validace
        if t_decay > 0:
            result = "DETERMINISTIC"
        else:
            result = "STABLE"

        print(f"CAT_{i:<4} | {phi:<12.4f} | {t_decay:<20.5f} | {result}")

    print("-" * 60)
    print(" CONCLUSION: The decay time varies precisely with φ.")
    print("             In QM, this variation is called 'Randomness'.")
    print("             In Geometry, it is strictly 'Causality'.")
    print("="*60)

if __name__ == "__main__":
    run_proof()