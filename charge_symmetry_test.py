import math

def get_divisors(n):
    """Vrátí počet dělitelů čísla n (míra symetrie)."""
    divs = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            if i * i == n: divs += 1
            else: divs += 2
    return divs

def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def calculate_topological_stress(Z):
    """
    Vypočítá 'Geometrické pnutí' jádra na základě čísla Z.
    Hypotéza: Prvočísla mají vysoké pnutí (nemají symetrii).
    Složená čísla (zvláště s mnoha děliteli) mají nízké pnutí.
    """
    if Z == 0: return 0

    # Faktor symetrie (počet možných uspořádání mřížky)
    symmetry_factor = get_divisors(Z)

    # Penalizace za prvočíslo (Prime Penalty)
    # Pokud je prvočíslo, symetrie je minimální (jen 1 a Z).
    # Ve fyzice to odpovídá "Topological Defect".

    # Stress skóre: Nepřímo úměrné symetrii
    # Normalizujeme Alpha konstantou, abychom zůstali v kontextu teorie
    alpha = 1/137.036

    # Zde je heuristický vzorec ze Sekce 3:
    # Stress ~ (Z * Alpha) / Symmetry
    stress = (Z * alpha) / symmetry_factor

    # Korekce pro "Magic Numbers" (Platónská tělesa)?
    # 2, 8, 20, 28, 50, 82... (Standardní fyzika)
    magic_numbers = [2, 8, 20, 28, 50, 82, 126]
    if Z in magic_numbers:
        stress = stress * 0.1 # Bonus za magickou stabilitu

    return stress

def analyze_isobar_pair(name1, Z1, name2, Z2):
    s1 = calculate_topological_stress(Z1)
    s2 = calculate_topological_stress(Z2)

    print(f"--- ISOBAR CHECK (A is constant) ---")
    print(f"{name1:<12} (Z={Z1}): {'PRIME' if is_prime(Z1) else 'Composite'} | Stress: {s1:.5f}")
    print(f"{name2:<12} (Z={Z2}): {'PRIME' if is_prime(Z2) else 'Composite'} | Stress: {s2:.5f}")

    if s1 > s2:
        print(f"PREDICTION: {name1} will decay into {name2} (Stress Relief).")
    elif s2 > s1:
        print(f"PREDICTION: {name2} will decay into {name1} (Stress Relief).")
    else:
        print("Equilibrium.")

if __name__ == "__main__":
    print("=== CHARGE TOPOLOGY & WEAK INTERACTION TEST ===\n")

    # 1. Rubidium-87 vs Strontium-87
    # Rubidium-87 je nestabilní (beta rozpad). Strontium je stabilní.
    analyze_isobar_pair("Rubidium", 37, "Strontium", 38)
    print("")

    # 2. Potassium-40 vs Argon-40 / Calcium-40
    # K-40 je nestabilní. Ar-40 a Ca-40 jsou stabilní.
    analyze_isobar_pair("Potassium", 19, "Argon", 18)
    print("")
    analyze_isobar_pair("Potassium", 19, "Calcium", 20)
    print("")

    # 3. Indium-115 (Z=49) vs Tin-115 (Z=50)
    # Zde je chyták! 49 není prvočíslo (7x7), ale 50 je "Magic Number".
    # Indium-115 se rozpadá.
    analyze_isobar_pair("Indium", 49, "Tin", 50)