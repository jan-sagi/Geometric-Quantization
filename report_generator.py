import datetime

class ReportGenerator:
    def __init__(self, output_path="results/bridges_found.log"):
        self.path = output_path

    def save_report(self, matches):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.path, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f" GEOMETRIC BRIDGE ANALYSIS REPORT\n")
            f.write(f" Generated: {timestamp}\n")
            f.write("="*80 + "\n\n")

            if not matches:
                f.write("No significant physical bridges found within current tolerance.\n")
                f.write("Suggestion: Increase tolerance or add more mechanisms.\n")
            else:
                f.write(f"SUCCESS: Found {len(matches)} significant correlations linking Geometry to Physics.\n\n")

                for i, m in enumerate(matches, 1):
                    f.write(f"BRIDGE #{i}: {m['particle']}\n")
                    f.write(f"{'-'*40}\n")
                    f.write(f"   Identified Mechanism:  {m['mechanism']}\n")
                    f.write(f"   Coupling Coefficient:  {m['coefficient']}\n")
                    f.write(f"   Residual Quality:      {m['residual_explained']:.6e} (lower is better)\n")
                    f.write(f"   Proposed Equation:     {m['final_equation_latex']}\n")
                    f.write("\n")

            f.write("="*80 + "\n")
            f.write("END OF REPORT\n")

        print(f"\n[Report] Analysis saved to: {self.path}")