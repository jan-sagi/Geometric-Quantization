import numpy as np
import sys
import time
import math

# =============================================================================
# 1. AXIOMY (HARDCODED - NEMĚNNÉ ZÁKONY)
# =============================================================================
# Zdrojový kód reality podle tvých papírů
PI = np.pi
ALPHA_INV = 137.035999
ALPHA = 1.0 / ALPHA_INV
N = np.log(4 * PI)

# Baryon Scale (Maximální potenciál mřížky)
# Toto je jediná "síla", která vstupuje do systému.
BARYON_SCALE = 6 * (PI**5)

# Cílové hmotnosti pro detekci (pouze pro logování, neovlivňují fyziku)
TARGETS = {
    "PROTON": 1836.15,
    "MUON": 206.77,
    "TAU": 3477.14,
    "ELECTRON": 1.0
}

# =============================================================================
# 2. KONFIGURACE SIMULACE
# =============================================================================
GRID_SIZE = 1000      # 1 milion bodů (dostatečný statistický vzorek)
TIME_STEP = ALPHA * 0.1 # Opatrný časový krok pro stabilitu (jemná struktura)

class LogColor:
    RESET = "\033[0m"
    GREEN = "\033[92m"  # Shoda
    YELLOW = "\033[93m" # Blízko
    CYAN = "\033[96m"   # Info
    BOLD = "\033[1m"

print(f"{LogColor.BOLD}=== GEOMETRIC UNIVERSE: ROBUST MINER V2 ==={LogColor.RESET}")
print(f" > Axiomy: Pi={PI:.5f}, Alpha={ALPHA:.5f}, N={N:.5f}")
print(f" > Force (Baryon Scale): {BARYON_SCALE:.4f}")
print(f" > Metoda: Komplexní Relaxace v Potenciálovém Poli")
print("-" * 70)

# =============================================================================
# 3. FYZIKÁLNÍ MOTOR (ROBUSTNÍ)
# =============================================================================
class StableUniverse:
    def __init__(self, size):
        self.size = size
        self.t = 0.0

        # GENESIS: Start z Planckova šumu (téměř nula)
        # Komplexní čísla (Real = Hmotnost, Imag = Fáze/Náboj)
        self.Psi = (np.random.rand(size, size) + 1j * np.random.rand(size, size)) * 1e-12

    def evolve(self):
        """
        ROVNICE ROVNOVÁHY:
        dPsi = Alpha * ( Force * exp(i * |Psi| * N) - Psi )

        Vysvětlení:
        1. Vesmír se snaží dosáhnout energie BARYON_SCALE (6*Pi^5).
        2. Směr (fáze) této snahy je určen geometrií |Psi| * N.
        3. Člen '- Psi' představuje gravitaci/entropii (brzdění).
        4. Alpha určuje rychlost této evoluce.
        """

        # 1. Změříme aktuální geometrii (Magnituda)
        magnitude = np.abs(self.Psi)

        # 2. Vypočítáme vektor síly (Komplexní rotace podle N)
        # Použití Eulerovy formule exp(i*x) je numericky 100% stabilní.
        # Nemůže dojít k přetečení (Overflow), protože velikost je vždy 1.0 * Scale.
        target_vector = BARYON_SCALE * np.exp(1j * magnitude * N)

        # 3. Výpočet změny (Diference mezi cílem a aktuálním stavem)
        delta = (target_vector - self.Psi) * TIME_STEP

        # 4. Aplikace změny
        self.Psi += delta
        self.t += TIME_STEP

    def analyze(self):
        """Hledá stabilní částice (Atraktory)"""
        # Zajímá nás reálná magnituda (Energie/Hmotnost)
        mass_spectrum = np.abs(self.Psi)

        # Uděláme histogram energií
        # Rozsah 0 až 4000 pokrývá všechny zajímavé částice
        hist, bin_edges = np.histogram(mass_spectrum, bins=2000, range=(0, 4000))

        # Najdeme špičky (Kde se hmota hromadí?)
        peaks = []
        min_cluster_size = self.size**2 * 0.0005 # Alespoň 0.05% vesmíru musí souhlasit

        for i in range(len(hist)):
            if hist[i] > min_cluster_size:
                # Centrum binu
                mass_val = (bin_edges[i] + bin_edges[i+1]) / 2
                peaks.append((mass_val, hist[i]))

        # Seřadíme podle velikosti populace (nejčastější částice první)
        peaks.sort(key=lambda x: x[1], reverse=True)
        return peaks

# =============================================================================
# 4. SPUŠTĚNÍ
# =============================================================================
universe = StableUniverse(GRID_SIZE)
step = 0

print("Spouštím evoluci... (Ctrl+C pro ukončení)")

try:
    while True:
        universe.evolve()
        step += 1

        # Logování každých 50 kroků (ať vidíme vývoj v čase)
        if step % 50 == 0:
            peaks = universe.analyze()

            # Stavový řádek
            sys.stdout.write("\033[K") # Smazat řádek
            log_msg = f"T={universe.t:.4f} | "

            found_something = False

            if not peaks:
                log_msg += "Thermalizing..."
            else:
                # Projdeme nalezené špičky
                for mass, count in peaks[:5]: # Top 5
                    label = ""
                    val_color = LogColor.RESET

                    # Je to známá částice?
                    for name, target in TARGETS.items():
                        # Tolerance 2% (Rezonanční šířka)
                        if abs(mass - target) / target < 0.02:
                            label = f"[{name}]"
                            val_color = LogColor.GREEN
                            found_something = True
                        elif abs(mass - target) / target < 0.05:
                            label = f"[{name}?]"
                            val_color = LogColor.YELLOW

                    log_msg += f"{val_color}{mass:.1f}{label}({count}){LogColor.RESET} "

            print(f"\r{log_msg}", end="")

            # Pokud najdeme silnou shodu, vypíšeme ji na nový řádek trvale
            if found_something and step % 200 == 0:
                print(f"\n   >>> STABLE RESONANCE: {log_msg}")

except KeyboardInterrupt:
    print("\nSimulace zastavena.")
    print("Data analýza ukončena.")