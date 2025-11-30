from decimal import Decimal

class EquationMatcher:
    def __init__(self, math_core):
        self.math = math_core
        self.mechanisms = self.math.load_data("data/physics_mechanisms.json")
        
        self.fractions = {
            Decimal("1"): "1", Decimal("-1"): "-1",
            Decimal("2"): "2", Decimal("-2"): "-2",
            Decimal("3"): "3", Decimal("-3"): "-3",
            Decimal("4"): "4", Decimal("-4"): "-4",
            Decimal("5"): "5", Decimal("-5"): "-5",
            Decimal("0.5"): "1/2", Decimal("-0.5"): "-1/2",
            Decimal("0.3333333333333333333333333333333333333333"): "1/3",
            Decimal("-0.3333333333333333333333333333333333333333"): "-1/3",
            Decimal("0.6666666666666666666666666666666666666667"): "2/3",
            Decimal("-0.6666666666666666666666666666666666666667"): "-2/3",
            Decimal("0.25"): "1/4", Decimal("-0.25"): "-1/4",
            Decimal("0.125"): "1/8", Decimal("-0.125"): "-1/8",
            Decimal("0.4"): "2/5", Decimal("-0.4"): "-2/5",
            Decimal("0.0"): "0"
        }

    def find_matches(self, residuals):
        matches = []
        for res in residuals:
            print(f"   -> Analyzuji reziduum pro: {res['target']} (Diff: {res['diff_abs']:.2e})")
            context = res['context']
            for mech in self.mechanisms:
                mech_val = self.math.evaluate_expr(mech['expression_template'], context)
                if mech_val and mech_val != 0:
                    factor = res['diff_abs'] / mech_val
                    best_frac_val = None
                    best_frac_name = ""
                    min_dist = Decimal("Infinity")
                    for frac_val, frac_name in self.fractions.items():
                        dist = abs(factor - frac_val)
                        if dist < min_dist:
                            min_dist = dist
                            best_frac_val = frac_val
                            best_frac_name = frac_name
                    
                    # Tolerance 15%
                    threshold = abs(best_frac_val) * Decimal("0.15") if best_frac_val != 0 else Decimal("0.000001")
                    
                    if min_dist < threshold and best_frac_val != 0:
                        print(f"      [HIT!] {mech['name']} -> Koeficient: {best_frac_name} (Quality: {min_dist:.4f})")
                        match_data = {
                            "particle": res['target'],
                            "mechanism": mech['name'],
                            "coefficient": best_frac_name,
                            "residual_explained": float(min_dist),
                            "final_equation_latex": self._format_latex(res, mech, best_frac_name)
                        }
                        matches.append(match_data)
        return matches

    def _format_latex(self, res, mech, coef_str):
        sign = "+" if not coef_str.startswith("-") else "-"
        val_str = coef_str.replace("-", "")
        if val_str == "1": val_str = ""
        return f"V_{{exp}} \approx V_{{geo}} {sign} {val_str} \left( {mech['expression_template']} \right)"
