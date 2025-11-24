import math
import sys

# =============================================================================
# GEOMETRIC UNIVERSE: PERIODIC TABLE GENERATOR (v1.0)
# =============================================================================
# GOAL: Generate a periodic table and search for ISLANDS OF STABILITY.
# LOGIC: Nuclear stability is determined by the resonance of the proton number (Z)
#        with geometric constants (6, Pi, Alpha).
# =============================================================================

class Formatting:
    GREEN = "\033[92m"  # Stable / Known
    RED = "\033[91m"    # Island of Stability (Prediction)
    CYAN = "\033[96m"   # Interesting Note
    BOLD = "\033[1m"
    RESET = "\033[0m"

class Theory:
    # Fundamental theory constants
    PROTON_NODE = 6      # Proton is k=6 (Symmetry)
    ALPHA_INV = 137.036  # Inverse Alpha (Electromagnetic Limit)
    PI = math.pi

    @staticmethod
    def get_stability_score(Z):
        """
        Calculates the 'Geometric Stability Score' for a given proton number Z.
        """
        score = 0
        notes = []

        # 1. PROTON SYMMETRY RULE (Multiples of 6)
        # If there are enough protons to form closed geometric shells (multiples of 6)
        if Z % Theory.PROTON_NODE == 0:
            score += 20
            # If it is also a "power" or "magic multiple"
            ratio = Z / Theory.PROTON_NODE
            if ratio.is_integer():
                # Z = 6, 12 (C), 18 (Ar), ...
                # Special bonus for prime multiples (Topology)
                notes.append("Hex")

        # 2. MAGIC NUMBERS (Standard Physics comparison)
        # Standard nuclear magic numbers: 2, 8, 20, 28, 50, 82, 114, 126
        magic_numbers = [2, 8, 20, 28, 50, 82, 114, 126]
        if Z in magic_numbers:
            score += 30
            notes.append("Magic")

        # 3. ALPHA RESONANCE (The Feynmanium Limit)
        # Proximity to Alpha^-1 (137)
        diff_alpha = abs(Z - Theory.ALPHA_INV)
        if diff_alpha < 1.0:
            score += 100 # MASSIVE BOOST
            notes.append("ALPHA-LIMIT")

        # 4. GEOMETRIC HARMONICS (Pi resonance)
        # Z = Pi^3 (~31), Z = Pi^4 (~97)
        pi_harmonics = [round(Theory.PI**n) for n in range(2, 6)] # 10, 31, 97, 306
        if Z in pi_harmonics:
            score += 15
            notes.append("Pi-Harm")

        # 5. PRIME STABILITY (Similar to Mesons)
        # Note: Mesons prefer primes. Nuclei prefer even numbers (spin pairing).
        # We apply a bonus for even numbers here (Proton Rule 6 is even).
        if Z % 2 == 0:
            score += 10

        return score, ", ".join(notes)

    @staticmethod
    def get_element_name(Z):
        # Basic elements
        elements = {
            1: "H", 2: "He", 6: "C", 7: "N", 8: "O", 26: "Fe",
            79: "Au", 82: "Pb", 92: "U", 94: "Pu"
        }
        if Z in elements: return elements[Z]

        # Superheavy (known)
        if Z == 114: return "Fl (Flerovium)"
        if Z == 118: return "Og (Oganesson)"

        # Hypothetical names
        if Z == 119: return "Uue"
        if Z == 120: return "Ubn"
        if Z == 126: return "Ubh"
        if Z == 137: return "Feynmanium"

        return f"E-{Z}"

def scan_periodic_table():
    print(f"{Formatting.BOLD}{'='*90}")
    print(f" GEOMETRIC PERIODIC TABLE & ISLANDS OF STABILITY SCAN")
    print(f" Looking for resonance at Z = n*6, Z = 137 (Alpha), and Magic Numbers.")
    print(f"{'='*90}{Formatting.RESET}")

    print(f" {'Z':<4} | {'ELEMENT':<14} | {'SCORE':<5} | {'GEOMETRY NOTES':<30} | {'STATUS'}")
    print("-" * 90)

    # Scan from Z = 1 to 172
    for Z in range(1, 173):
        score, notes = Theory.get_stability_score(Z)
        name = Theory.get_element_name(Z)

        # Visualization
        status = ""
        color = Formatting.RESET

        # Output Filters
        # Print only interesting elements to avoid cluttering the console
        is_interesting = False

        if score >= 40: # Very Stable
            status = "STABLE ISLAND"
            color = Formatting.GREEN
            is_interesting = True

        if Z > 100 and score >= 30: # Superheavy candidates
            status = "SUPER-HEAVY ISLAND"
            color = Formatting.RED
            is_interesting = True

        if Z == 137: # Feynmanium Special
            status = "!!! GEOMETRIC LIMIT !!!"
            color = Formatting.RED + Formatting.BOLD
            is_interesting = True

        # Always print known important elements
        if Z in [1, 6, 26, 82, 92]:
            is_interesting = True
            if status == "": status = "Known Stable"

        if is_interesting:
            print(f"{color} {Z:<4} | {name:<14} | {score:<5} | {notes:<30} | {status}{Formatting.RESET}")

    print("-" * 90)
    print(f"{Formatting.BOLD}PREDICTION SUMMARY:{Formatting.RESET}")
    print("1. Standard physics predicts stability at Z=114 and Z=126.")
    print("2. GEOMETRIC THEORY predicts a massive singularity at Z=137 (Feynmanium).")
    print("   Reason: Z = 137 matches exactly with Alpha^-1.")
    print("   Prediction: Element 137 might be the final limit of normal matter.")

if __name__ == "__main__":
    scan_periodic_table()