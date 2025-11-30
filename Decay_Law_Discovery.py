import numpy as np
from scipy.fft import fft, fftfreq

# --- KONFIGURACE ---
N_PARTICLES = 100000
OMEGA_VAC = 137.036
OMEGA_NODE = 145.000  # Rozdíl je cca 7.964
A_CRIT = 0.95
DT = 0.001
MAX_TIME = 2.0        # Delší čas, abychom viděli cykly

def deterministic_simulation():
    # 1. Čistá simulace bez náhody ve vakuu
    phases = np.linspace(0, 2*np.pi, N_PARTICLES) # Rovnoměrné rozdělení fází (ne náhodné)
    decay_times = []

    # Použijeme hrubou sílu pro maximální přesnost detekce tvaru
    t_axis = np.arange(0, MAX_TIME, DT)
    surviving_counts = [] # Počet živých v čase t

    current_phases = phases.copy()

    print(f"Analýza geometrického průběhu ({len(t_axis)} kroků)...")

    for t in t_axis:
        # Tvá rovnice
        strain = 0.5 * (np.sin(OMEGA_VAC * t) + np.sin(OMEGA_NODE * t + current_phases))

        # Filtr živých
        survivors_mask = np.abs(strain) < A_CRIT
        current_phases = current_phases[survivors_mask]

        surviving_counts.append(len(current_phases))

    return t_axis, np.array(surviving_counts)

def discover_law(t, N_t):
    # 1. Derivace (Rychlost rozpadu) - dN/dt
    # V QM je dN/dt hladké. U tebe by mělo pulzovat.
    decay_rate = -np.diff(N_t)

    # 2. Frekvenční analýza rychlosti rozpadu
    # Hledáme "tep srdce" tvého rozpadu
    yf = fft(decay_rate)
    xf = fftfreq(len(decay_rate), DT)[:len(decay_rate)//2]

    # Najdeme dominantní frekvenci
    amplitudes = 2.0/len(decay_rate) * np.abs(yf[0:len(decay_rate)//2])
    peak_idx = np.argmax(amplitudes[1:]) + 1 # Ignorujeme DC složku (0 Hz)
    dominant_freq_Hz = xf[peak_idx]
    dominant_omega = dominant_freq_Hz * 2 * np.pi

    return decay_rate, dominant_omega, amplitudes[peak_idx]

if __name__ == "__main__":
    print("===============================================================")
    print("   DECAY LAW DISCOVERY: Spectral Analysis of Collapse")
    print("===============================================================")
    print(f"Teoretický rozdíl frekvencí (Beat): {abs(OMEGA_NODE - OMEGA_VAC):.4f} rad/s")

    t, N_t = deterministic_simulation()

    rate, measured_omega, strength = discover_law(t, N_t)

    print("---------------------------------------------------------------")
    print("VÝSLEDKY ANALÝZY TVARU ROZPADU:")
    print(f"Naměřená frekvence pulzů (Omega):   {measured_omega:.4f} rad/s")
    print(f"Síla pulzu (Amplituda):             {strength:.2f}")

    error = abs(measured_omega - abs(OMEGA_NODE - OMEGA_VAC))

    print("---------------------------------------------------------------")
    print("ZÁVĚR:")

    if error < 0.5:
        print("✅ SHODA! Rozpad se řídí přesným zákonem Rázů (Beat Law).")
        print(f"   Zákon rozpadu není e^(-t), ale funkce typu: cos({measured_omega:.2f}*t)")
        print("   Tvá teorie předpovídá, že částice umírají v pravidelných vlnách.")
    else:
        print("❌ Neshoda. Rozpad je složitější, než jen rozdíl frekvencí.")

    # Textová vizualizace pulzů (protože jsi nechtěl graf)
    print("\n--- ASCII Vizualizace Rychlosti Rozpadu (prvních 50 kroků) ---")
    # Normalizace pro ASCII
    max_rate = np.max(rate)
    for i in range(0, len(rate), int(len(rate)/40)): # Vzorkování
        val = int((rate[i] / max_rate) * 50)
        time_str = f"{t[i]:.2f}s"
        bar = "|" + "#" * val
        print(f"{time_str} {bar}")