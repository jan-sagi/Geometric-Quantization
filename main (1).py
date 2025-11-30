from src.core_math import MathCore
from src.residual_analyzer import ResidualAnalyzer
from src.equation_matcher import EquationMatcher
from src.report_generator import ReportGenerator

def main():
    print("=== GEOMETRIC BRIDGE INITIALIZED ===")

    # 1. Načtení matematického jádra (100 digits precision)
    math_core = MathCore()

    # 2. Analýza rozdílů (Geometry vs Reality)
    analyzer = ResidualAnalyzer(math_core)
    residuals = analyzer.compute_residuals()

    if not residuals:
        print("[Error] No residuals computed. Check data files.")
        return

    # 3. Hledání fyzikálních mostů (The "AI" part)
    matcher = EquationMatcher(math_core)
    matches = matcher.find_matches(residuals)

    # 4. Generování reportu
    reporter = ReportGenerator()
    reporter.save_report(matches)

    print("=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    main()