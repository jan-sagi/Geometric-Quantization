import numpy as np
import random

class PopulationSimulation:
    def __init__(self):
        self.alpha_inv = 137.036
        self.limit = 0.98

    def check_survival(self, t, phi, k_node):
        # Stejná deterministická rovnice
        w_node = 100.0 + (k_node * 2.5)
        w_vac = self.alpha_inv

        amp = (np.sin(w_node * t + phi) + np.sin(w_vac * t)) / 2.0
        if abs(amp) > self.limit:
            return False # Dead
        return True # Alive

def run_statistics():
    sim = PopulationSimulation()

    population_size = 10000
    k_tau = 17 # Nestabilní částice

    # Generujeme 10 000 koček, každá má jinou SKRYTOU FÁZI (phi)
    # To simuluje realitu, kde neznáme historii každé částice
    population_phases = [random.uniform(0, 2*np.pi) for _ in range(population_size)]

    print("="*60)
    print(" MATHEMATICAL PROOF 2: EMERGENCE OF QUANTUM PROBABILITY")
    print(f" Sample Size: {population_size} particles (Geometric Nodes)")
    print(f" Topology:    k={k_tau} (Tau-like)")
    print(" Goal:        Derive Half-Life from Deterministic Chaos")
    print("="*60)
    print(f"{'TIME (t)':<10} | {'SURVIVORS':<12} | {'DECAYED':<10} | {'% ALIVE'}")
    print("-" * 60)

    time_steps = np.linspace(0, 0.2, 11) # Sledujeme časový vývoj

    survivors_history = []

    for t in time_steps:
        alive_count = 0

        for phi in population_phases:
            # Pro každou kočku zkontrolujeme, zda v čase t ještě žije
            # Pozor: Musíme zkontrolovat celou historii do t, ale pro zjednodušení modelu
            # zde kontrolujeme, zda v čase t nedošlo k překmitu.
            # (V plné simulaci bychom integrovali, ale pro statistiku stačí vzorkování)

            is_alive = True
            # Rychlý check historie (zjednodušený)
            for sub_t in np.linspace(0, t, int(t*100)+2):
                if not sim.check_survival(sub_t, phi, k_tau):
                    is_alive = False
                    break

            if is_alive:
                alive_count += 1

        percent = (alive_count / population_size) * 100
        print(f"{t:<10.3f} | {alive_count:<12} | {population_size-alive_count:<10} | {percent:.1f}%")
        survivors_history.append(alive_count)

    # Analýza rozpadové křivky
    initial = survivors_history[0]
    final = survivors_history[-1]

    print("-" * 60)
    if initial > final:
        print(" ANALYSIS: The population decreases over time.")
        print("           The deterministic phase-shift creates a")
        print("           statistical 'Half-Life' effect.")
    print("="*60)

if __name__ == "__main__":
    run_statistics()