import math
import csv
import sys
import os
from decimal import Decimal, getcontext

# Nastavení přesnosti
getcontext().prec = 100

class Constants:
    # AXIOMS
    PI = Decimal("3.14159265358979323846264338327950288419716939937510")
    ALPHA_INV = Decimal("137.035999084")
    ALPHA = Decimal(1) / ALPHA_INV
    N = (Decimal(4) * PI).ln()

    # PHYSICS UNITS
    ME_TO_MEV = Decimal("0.510998950")

    # TIME ANCHORS (Muon k=1)
    MUON_LIFE = 2.197e-6
    MUON_BETA = 0.1702

class StandardModel:
    """
    Referenční data pro ověření (Ground Truth).
    """
    PARTICLES = {
        # LEPTONS
        "Muon": 105.66, "Tau": 1776.86, "Electron": 0.511,
        # MESONS
        "Pion0": 134.98, "Pion+": 139.57, "Kaon+": 493.68, "Eta": 547.86,
        "Rho": 775.26, "Omega": 782.65, "Phi": 1019.46, "J/Psi": 3096.90,
        "Upsilon": 9460.30, "B+": 5279.32, "D+": 1869.65,
        # BARYONS
        "Proton": 938.27, "Neutron": 939.57, "Lambda": 1115.68, "Sigma": 1189.37,
        # BOSONS
        "W Boson": 80379.0, "Z Boson": 91187.6, "Higgs": 125100.0
    }

class GeometricPhysics:
    @staticmethod
    def get_scales():
        return {
            "LEPTON": Decimal(4) * Constants.PI * (Constants.N**3),
            "MESON":  Constants.ALPHA_INV,
            "BARYON": Constants.PI**5
        }

    @staticmethod
    def calculate_lifetime(k, beta, scale_type):
        """
        Zákon rozpadu: T ~ 1 / (k^5 * beta^2)
        """
        if beta < 1e-6: return float('inf') # Stabilní

        # Penalizace pro mezony (silná interakce je rychlejší než slabá)
        scale_factor = 1.0
        if scale_type == "MESON": scale_factor = 1000.0 # Mezony žijí krátce

        # Výpočet relativně k Mionu
        life = Constants.MUON_LIFE / ((float(k)**5) * ((beta/Constants.MUON_BETA)**2) * scale_factor)
        return life

class ZooGenerator:
    def __init__(self):
        self.zoo = []
        self.scales = GeometricPhysics.get_scales()

        # Kvantované topologické stavy, které jsme objevili v diagnostice
        # (Název, Hodnota n v rovnici 1 + n*Alpha)
        self.topologies = [
            ("Perfect (0)",    Decimal(0)),
            ("Spinor (+0.5)",  Decimal(0.5)),
            ("Spinor (-0.5)",  Decimal(-0.5)),
            ("Vector (+1.0)",  Decimal(1.0)),
            ("Vector (-1.0)",  Decimal(-1.0)),
            ("Sphere (+2.0)",  Decimal(2.0)), # Inverzní logika pro sféru se řeší zvlášť
            ("Sphere (-2.0)",  Decimal(-2.0))
        ]

    def scan(self, max_mev=130000):
        print(f">>> GENERATING PARTICLE ZOO (0 - {max_mev} MeV)...")

        for scale_name, base_val in self.scales.items():
            k = 1
            while True:
                # Základní hmotnost uzlu
                base_mass_me = Decimal(k) * base_val
                base_mass_mev = base_mass_me * Constants.ME_TO_MEV

                if base_mass_mev > max_mev: break

                # Zkoušíme všechny povolené topologie pro tento uzel
                for topo_name, n_alpha in self.topologies:

                    # Aplikace korekce F
                    # Speciální případ pro Mion (Sféra k=1): F = 1/(1-2a)
                    if "Sphere" in topo_name and k == 1:
                        # Použijeme přesnou sférickou metriku
                        sign = -1 if n_alpha < 0 else 1
                        correction = Decimal(1) / (Decimal(1) - (Decimal(2)*sign*Constants.ALPHA))
                    else:
                        # Standardní lineární topologie: F = 1 + n*Alpha
                        correction = Decimal(1) + (n_alpha * Constants.ALPHA)

                    # Výsledná hmotnost
                    mass_final_mev = float(base_mass_mev * correction)

                    # Vnitřní rychlost (Beta) pro výpočet času
                    # F = gamma
                    F = float(correction)
                    if F < 1.0: F = 1.0/F
                    try: beta = math.sqrt(1 - 1/(F**2))
                    except: beta = 0.0

                    # Životnost
                    lifetime = GeometricPhysics.calculate_lifetime(k, beta, scale_name)

                    # Identifikace (Je to známá částice?)
                    match_name = None
                    match_err = 100.0

                    for name, real_mass in StandardModel.PARTICLES.items():
                        err = abs(mass_final_mev - real_mass) / real_mass * 100
                        if err < 1.5: # Tolerance 1.5%
                            if err < match_err:
                                match_err = err
                                match_name = name

                    # Uložení, pokud je to zajímavé
                    # (Buď shoda, nebo vysoká stabilita u predikce)
                    is_interesting = False
                    status = "Noise"

                    if match_name:
                        status = f"CONFIRMED [{match_name}]"
                        is_interesting = True
                    elif lifetime > 1e-12: # Dlouho žijící kandidát
                        status = "PREDICTION (Stable)"
                        is_interesting = True
                    elif lifetime > 1e-20 and self._is_prime(k): # Rezonance na prvočísle
                        status = "PREDICTION (Resonance)"
                        is_interesting = True

                    if is_interesting:
                        self.zoo.append({
                            "Mass": mass_final_mev,
                            "Scale": scale_name,
                            "k": k,
                            "Topology": topo_name,
                            "Lifetime": lifetime,
                            "Status": status,
                            "Error": match_err if match_name else 0.0
                        })

                k += 1

        # Seřadit podle hmotnosti
        self.zoo.sort(key=lambda x: x["Mass"])

    def _is_prime(self, n):
        if n <= 1: return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0: return False
        return True

    def report(self):
        # 1. Výpis do souboru
        filename = "Universal_Particle_Map.txt"
        with open(filename, "w", encoding="utf-8") as f:
            header = f"{'MASS (MeV)':<12} | {'SCALE':<10} | {'k':<4} | {'TOPOLOGY':<15} | {'LIFETIME (s)':<12} | {'STATUS'}"
            print("-" * 100)
            print(header)
            print("-" * 100)
            f.write(header + "\n" + "-"*100 + "\n")

            for p in self.zoo:
                life_str = "STABLE" if p['Lifetime'] == float('inf') else f"{p['Lifetime']:.1e}"
                line = f"{p['Mass']:<12.2f} | {p['Scale']:<10} | {p['k']:<4} | {p['Topology']:<15} | {life_str:<12} | {p['Status']}"

                # Color logic for console
                color = "\033[0m"
                if "CONFIRMED" in p['Status']: color = "\033[92m" # Green
                elif "Stable" in p['Status']: color = "\033[96m" # Cyan

                print(f"{color}{line}\033[0m")
                f.write(line + "\n")

        print("-" * 100)
        print(f"Mapped {len(self.zoo)} significant geometric nodes.")
        print(f"Data saved to: {filename}")

if __name__ == "__main__":
    gen = ZooGenerator()
    gen.scan(130000) # Až po Higgs
    gen.report()