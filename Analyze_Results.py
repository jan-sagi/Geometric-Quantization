import statistics

def analyze_audit_file(filename="MASSIVE_GALAXY_AUDIT.txt"):
    improvements = []
    wins = 0
    losses = 0
    total = 0

    print(f"ANALYZING REPORT: {filename}")
    print("-" * 40)

    with open(filename, "r") as f:
        lines = f.readlines()

        for line in lines:
            # Hledáme řádky s daty (obsahují '|')
            if "|" in line and "GALAXY" not in line:
                parts = line.split("|")
                if len(parts) < 5: continue

                try:
                    # Získáme procento z posledního sloupce
                    imp_str = parts[4].strip().replace("%", "")
                    imp = float(imp_str)

                    improvements.append(imp)
                    total += 1

                    if imp > 0: wins += 1
                    else: losses += 1

                except ValueError: continue

    if not improvements:
        print("No data found.")
        return

    median_imp = statistics.median(improvements)

    print(f"Total Galaxies:   {total}")
    print(f"Geometric WINS:   {wins} ({wins/total*100:.1f}%)")
    print(f"Newton WINS:      {losses} ({losses/total*100:.1f}%)")
    print("-" * 40)
    print(f"MEDIAN IMPROVEMENT: {median_imp:.1f} %")
    print("-" * 40)

    if median_imp > 0:
        print("CONCLUSION: The Geometric Model is statistically superior to Newton.")
        print("            (It improves the prediction for the majority of galaxies.)")
    else:
        print("CONCLUSION: Newton performs better on median.")

if __name__ == "__main__":
    analyze_audit_file()