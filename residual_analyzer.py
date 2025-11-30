from decimal import Decimal

class ResidualAnalyzer:
    def __init__(self, math_core):
        self.math = math_core
        self.axioms = self.math.load_data("data/geometric_axioms.json")
        self.standard_model = self.math.load_data("data/standard_model.json")

    def compute_residuals(self):
        """
        Vypočítá rozdíly mezi Geometrickou Teorií a Standardním Modelem.
        Vrací seznam objektů 'Residual'.
        """
        residuals = []

        # 1. Nejdřív musíme vypočítat hodnotu Alpha (klíčová pro vše ostatní)
        # Najdeme axiom pro Alpha Inverse
        alpha_axiom = next(a for a in self.axioms if a['id'] == 'geo_alpha_inv')
        alpha_inv_val = self.math.evaluate_expr(alpha_axiom['expression_str'])
        alpha_val = Decimal(1) / alpha_inv_val

        # Kontext pro výpočet dalších rovnic (kde se vyskytuje 'alpha')
        context = {"alpha": alpha_val}

        # 2. Procházíme Standardní Model a hledáme páry v Axiomech
        for reality in self.standard_model:
            # Hledáme axiom se stejným jménem (nebo mapováním)
            # Zde zjednodušeně: předpokládáme, že id v axiomech je 'geo_' + zbytek
            target_id = reality['id'].replace("codata_", "geo_")
            theory = next((a for a in self.axioms if a['id'] == target_id), None)

            if theory:
                val_real = Decimal(reality['value_str'])
                val_theory = self.math.evaluate_expr(theory['expression_str'], context)

                if val_theory:
                    # A. Absolutní rozdíl (Additive)
                    diff_abs = val_theory - val_real

                    # B. Relativní poměr (Multiplicative)
                    # (Teorie / Realita) - 1.0
                    # Pokud je to 0, jsou identické. Pokud 0.001, liší se o promile.
                    ratio_res = (val_theory / val_real) - Decimal(1)

                    residuals.append({
                        "target": reality['name'],
                        "val_theory": val_theory,
                        "val_real": val_real,
                        "diff_abs": diff_abs,
                        "ratio_res": ratio_res,
                        "context": context # Předáme alfu dál pro Matcher
                    })

                    print(f"[Analyzer] {reality['name']}: Theory={val_theory:.6f}, Real={val_real:.6f}, Diff={diff_abs:.2e}")

        return residuals