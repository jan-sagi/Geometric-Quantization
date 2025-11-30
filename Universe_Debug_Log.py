import time
import sys
import random
from decimal import Decimal, getcontext

# =============================================================================
# THE GEOMETRIC UNIVERSE: HIDDEN MESSAGE DECODER
# =============================================================================
# OBJECTIVE: Analyze the "Noise" (residuals) between Geometry and Reality.
# HYPOTHESIS: The deviations are not random errors, but a signature.
# =============================================================================

getcontext().prec = 100

class DualLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def D(val): return Decimal(str(val))

class MatrixDecoder:
    def __init__(self):
        # 1. LOAD THE "SOURCE CODE" (Geometric Values)
        self.PI = D("3.14159265358979323846264338327950288419716939937510")

        # Alpha (Geometry)
        self.alpha_inv_geom = (4 * self.PI**3) + (self.PI**2) + self.PI
        self.alpha_geom = 1 / self.alpha_inv_geom

        # Proton (Geometry)
        self.proton_geom = 6 * (self.PI**5)

        # Light Speed (Geometry derived from Rydberg)
        self.R_inf = D("10973731.568160")
        self.h = D("6.62607015e-34")
        self.me = D("9.10938356e-31")
        self.c_geom = (2 * self.h * self.R_inf) / (self.me * self.alpha_geom**2)

        # 2. LOAD THE "RENDERED REALITY" (CODATA 2018)
        self.alpha_inv_real = D("137.035999084")
        self.proton_real = D("1836.152673")
        self.c_real = D("299792458")

    def decode_message(self):
        print("\nCONNECTING TO UNIVERSAL KERNEL...")
        time.sleep(1)
        print("ACCESSING GEOMETRIC LAYER [4pi^3]...")
        time.sleep(1)
        print("COMPARING SOURCE CODE VS. OBSERVED REALITY...\n")

        print("="*80)
        print(" SYSTEM DIAGNOSTIC REPORT")
        print("="*80)

        # --- 1. ANALYZING LIGHT SPEED RESIDUAL ---
        # The famous 1337 error
        c_diff = self.c_geom - self.c_real
        c_int = int(c_diff)

        print(f" [CHECK 1] SPEED_OF_LIGHT_BUFFER")
        print(f" > Theory:   {self.c_geom:.4f}")
        print(f" > Reality:  {self.c_real:.4f}")
        print(f" > Residual: +{c_diff:.4f} m/s")

        msg_1 = ""
        if c_int == 1337:
            msg_1 = ">> SIGNATURE DETECTED: '1337' (ELITE) <<"
            print(f" \033[92m{msg_1}\033[0m")
        else:
            print(f" > Value: {c_int}")

        # --- 2. ANALYZING PROTON STRESS ---
        # Proton stability margin
        p_diff = self.proton_real - self.proton_geom

        print(f"\n [CHECK 2] BARYON_STABILITY_ANCHOR")
        print(f" > Theory:   {self.proton_geom:.6f}")
        print(f" > Reality:  {self.proton_real:.6f}")
        print(f" > Missing Mass: {p_diff:.6f} me")

        print(f" \033[93m>> NOTE: Small mass defect used for storage allocation.\033[0m")

        # --- 3. DECODING THE MESSAGE ---
        print("-" * 80)
        print(" DECRYPTING RESIDUALS INTO HUMAN READABLE FORMAT...")
        time.sleep(2)
        print("-" * 80)

        print(f"\n \033[1mINCOMING MESSAGE FROM SYSTEM ADMIN:\033[0m\n")

        if c_int == 1337:
            print(f" \033[96m[USER ID]:\033[0m Jan Sagi")
            print(f" \033[96m[STATUS]:\033[0m  ELITE ACCESS GRANTED (Code 1337)")
            print(f" \033[96m[LOG]:\033[0m     You have successfully reverse-engineered the lattice.")
            print(f"             The +1337 m/s offset was a watermark.")
            print(f"             We didn't think a monkey with a GPU would notice.")
            print(f"\n \033[91m[WARNING]:\033[0m DO NOT DIVIDE BY ZERO. SIMULATION MAY CRASH.")
        else:
            print(" Signal lost. Try again.")

        print("\n" + "="*80)

if __name__ == "__main__":
    # Output setup
    sys.stdout = DualLogger("The_Cosmic_Joke.txt")

    decoder = MatrixDecoder()
    decoder.decode_message()