import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

def is_prime(n):
    """Pomocná funkce pro detekci prvočísel"""
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_stability_test():
    # Testujeme čísla od 2 do 50 (Atomová hmotnost / Energetické hladiny)
    k_values = range(2, 51)

    primes_k = []
    primes_amp = []

    composites_k = []
    composites_amp = []

    print("--- PRVOČÍSELNÝ SKENER ---")
    print("Analyzuji, zda prvočísla lépe odolávají kolapsu...")

    for k in k_values:
        # Hledáme maximální pnutí pro dané k
        # f(t) = |sin(t) + sin(k*t)|
        func = lambda t: -np.abs(np.sin(t) + np.sin(k * t))
        res = minimize_scalar(func, bounds=(0, 2*np.pi), method='bounded')
        max_amp = -res.fun

        if is_prime(k):
            primes_k.append(k)
            primes_amp.append(max_amp)
            type_str = "PRVOČÍSLO"
        else:
            composites_k.append(k)
            composites_amp.append(max_amp)
            type_str = "Složené  "

        # Výpis pro zajímavá čísla (pod zdí)
        if max_amp < 1.9:
            print(f"{type_str} k={k:2d} -> Max Amp: {max_amp:.4f} [STABILNÍ]")

    # --- VIZUALIZACE ---
    plt.figure(figsize=(14, 8))

    # 1. Složená čísla (Šedá - běžný šum)
    plt.scatter(composites_k, composites_amp, color='gray', alpha=0.5, s=50, label='Složená čísla (Composite)')

    # 2. Prvočísla (Červená - Kandidáti)
    plt.scatter(primes_k, primes_amp, color='red', s=100, marker='D', label='Prvočísla (Primes)')

    # Spojnice pro trend
    plt.plot(k_values, [max_amp for k in k_values if k in primes_k or k in composites_k], 'k-', alpha=0.1)

    # 3. Alpha Wall (Hranice existence)
    plt.axhline(y=1.9, color='blue', linestyle='--', linewidth=2, label='Alpha Wall (1.9)')

    # Anotace pro klíčová prvočísla z tvého úvodu
    # Tau = 17, Proton (Hexagon) = 6? (Složené), Mion = 1
    target_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for k, amp in zip(primes_k, primes_amp):
        if k in target_primes:
            plt.annotate(f"{k}", (k, amp), xytext=(0, 10), textcoords='offset points', ha='center', color='red', fontweight='bold')

    plt.title("Prvočísla vs. Složená čísla: Kdo přežije interferenci?")
    plt.xlabel("Harmonické číslo (k)")
    plt.ylabel("Maximální pnutí vakua")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(np.arange(0, 51, 2))

    # Invertujeme osu Y, aby "bezpečné dno" bylo dole?
    # Ne, nechme to takto: Nízká amplituda = Bezpečí (Dole), Vysoká = Smrt (Nahoře)
    # Ale pozor, v předchozích grafech jsme hledali minima. Tady čím nižší hodnota, tím lépe.

    plt.show()

if __name__ == "__main__":
    prime_stability_test()