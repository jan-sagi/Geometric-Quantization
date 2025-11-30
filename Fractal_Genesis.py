import math
import time
import sys
import os
from decimal import Decimal, getcontext

# Nastavení přesnosti pro výpočet evoluce
getcontext().prec = 100

class CosmicConstants:
    """
    Konstanty našeho geometrického vesmíru.
    """
    PI = Decimal("3.14159265358979323846264338327950288419716939937510")

    # Odvozené G (z našeho předchozího auditu)
    # Zde ho používáme pro simulaci gravitace mračen
    GRAVITY_G = Decimal("6.67405e-11")

    # Alpha (pro chemické reakce a svítivost hvězd)
    ALPHA = Decimal("1") / Decimal("137.035999084")

class FractalRNG:
    """
    DETERMINISTICKÝ GENERÁTOR (The Pi Stream)
    V geometrickém vesmíru není náhoda. "Náhoda" je jen další číslice Pí.
    Tento generátor čte Pí a rozhoduje o rozložení hmoty.
    """
    def __init__(self):
        # Pí jako string (seed)
        self.pi_stream = str(CosmicConstants.PI).replace(".", "")
        self.cursor = 0

    def get_fraction(self):
        """Vrátí číslo 0.0 až 1.0 na základě další číslice Pí."""
        if self.cursor >= len(self.pi_stream):
            self.cursor = 0 # Loop vesmíru (Poincare Recurrence)

        digits = self.pi_stream[self.cursor : self.cursor+5]
        self.cursor += 1
        return float(int(digits) / 100000.0)

class UniverseSimulator:
    def __init__(self):
        self.rng = FractalRNG()
        self.age_myr = 0 # Věk v milionech let
        self.matter_clouds = []
        self.stars = []
        self.planets = []
        self.log_file = open("Genesis_Log.txt", "w", encoding="utf-8")

    def log(self, message):
        timestamp = f"[T+{self.age_myr:>6} Myr]"
        print(f"{timestamp} {message}")
        self.log_file.write(f"{timestamp} {message}\n")

    def epoch_big_bang(self):
        self.log(">>> INICIALIZACE GEOMETRICKÉHO ČASOPROSTORU <<<")
        self.log(f"Axiomy: PI={str(CosmicConstants.PI)[:10]}..., ALPHA=1/{1/CosmicConstants.ALPHA:.3f}")
        self.log("Vzniká primordiální mřížka...")

        # Generování hmoty z Pí (Fluktuace vakua)
        # Ve fraktálu se hmota shlukuje tam, kde jsou v Pí specifické vzory
        total_mass = 0
        for i in range(100):
            density = self.rng.get_fraction()
            if density > 0.5:
                # Vznik mračna Vodíku a Helia
                mass = 1000 * density # Hmotnost v "Sluncích"
                self.matter_clouds.append({"id": i, "mass": mass, "composition": "H/He"})
                total_mass += mass

        self.log(f"Nukleogeneze dokončena. Vzniklo {len(self.matter_clouds)} mlhovin. Celková hmotnost: {total_mass:.1f} Sol.")

    def epoch_star_formation(self):
        # Gravitační kolaps mračen
        # Používáme naše G k určení, které mračno se zhroutí
        self.age_myr += 50
        self.log("Začíná gravitační kolaps (Epoch of Light)...")

        for cloud in self.matter_clouds:
            # Kritérium Jeansovy nestability (zjednodušené pro simulaci)
            # Větší mračna se hroutí rychleji
            collapse_chance = cloud["mass"] * float(CosmicConstants.GRAVITY_G) * 1e10

            if self.rng.get_fraction() < collapse_chance:
                # Vznik hvězdy
                star_type = "Yellow Dwarf"
                if cloud["mass"] > 500: star_type = "Blue Giant"
                if cloud["mass"] < 50: star_type = "Red Dwarf"

                self.stars.append({
                    "id": cloud["id"],
                    "mass": cloud["mass"],
                    "type": star_type,
                    "stable": True,
                    "planets": []
                })
                self.log(f"   * Zážeh hvězdy! ID:{cloud['id']} ({star_type}, Mass={cloud['mass']:.1f})")

    def epoch_metallicity(self):
        # Tvorba těžkých prvků (Supernovy)
        # Zde využíváme naši znalost, že Z=6 (Uhlík) a Z=8 (Kyslík) jsou stabilní
        self.age_myr += 1000
        self.log("Hvězdná alchymie. Modří obři explodují a tvoří Uhlík a Kyslík...")

        # Modří obři umírají rychle (geometrický zákon rozpadu)
        surviving_stars = []
        for star in self.stars:
            if star["type"] == "Blue Giant":
                self.log(f"   ! Supernova ID:{star['id']}. Obohacení okolí o těžké prvky (C, O, Fe).")
                # Vytvoří protoplanetární disk pro okolní hvězdy
            else:
                star["metallicity"] = "High" # Obohaceno
                surviving_stars.append(star)

        self.stars = surviving_stars

    def epoch_planetary_accretion(self):
        self.age_myr += 3000
        self.log("Formování planetárních systémů z fraktálního prachu...")

        for star in self.stars:
            if star["metallicity"] == "High":
                # Generujeme planety pomocí Pí
                num_planets = int(self.rng.get_fraction() * 10)
                for p in range(num_planets):
                    dist = 0.5 + (p * 0.4) + (self.rng.get_fraction() * 0.2) # AU

                    # Typ planety
                    p_type = "Gas Giant"
                    if 0.8 < dist < 1.5 and self.rng.get_fraction() > 0.3:
                        p_type = "Rocky World"

                    planet = {
                        "dist": dist,
                        "type": p_type,
                        "life_potential": 0.0
                    }
                    star["planets"].append(planet)
                    if p_type == "Rocky World":
                        self.log(f"   o Planeta u hvězdy {star['id']}: {p_type} ve vzdálenosti {dist:.2f} AU.")

    def epoch_emergence_of_life(self):
        self.age_myr += 1000
        self.log("Hledání geometrické rezonance (Života)...")

        life_found = False
        for star in self.stars:
            for planet in star["planets"]:
                if planet["type"] == "Rocky World":
                    # 1. Podmínka Goldilocks (Voda)
                    # Závisí na Alfě (interakce světla)
                    optimal_dist = 1.0 # AU
                    dist_score = 1.0 - abs(planet["dist"] - optimal_dist)

                    # 2. Podmínka Uhlíku (Z=6)
                    # Stabilita C-12 je klíčová (naše k=6 symetrie)
                    carbon_score = 1.0 # Předpokládáme přítomnost díky supernovám

                    # Celkové skóre
                    probability = dist_score * carbon_score * self.rng.get_fraction()

                    if probability > 0.85:
                        self.log(f"   >>> ŽIVOT DETEKOVÁN! <<<")
                        self.log(f"       Systém: {star['id']}, Vzdálenost: {planet['dist']:.2f} AU")
                        self.log(f"       Základ: Uhlík (Geometrie k=6)")
                        self.log(f"       Rozpouštědlo: Voda (Dipól řízený Alfou)")
                        life_found = True

        if not life_found:
            self.log("   ... Vesmír je zatím tichý. Geometrické podmínky nebyly splněny.")

    def run(self):
        self.epoch_big_bang()
        time.sleep(1)
        self.epoch_star_formation()
        time.sleep(1)
        self.epoch_metallicity()
        time.sleep(1)
        self.epoch_planetary_accretion()
        time.sleep(1)
        self.epoch_emergence_of_life()

        self.log_file.close()
        print("\n[SIMULACE DOKONČENA] Log uložen do 'Genesis_Log.txt'")

if __name__ == "__main__":
    sim = UniverseSimulator()
    sim.run()