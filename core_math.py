import math
import json
import yaml
from decimal import Decimal, getcontext, InvalidOperation

class MathCore:
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_precision()

        # Načtení PI s vysokou přesností
        self.PI = self._generate_pi()
        # Načtení Eulerova čísla (pro logaritmy)
        self.E = Decimal(1).exp()

    def _load_config(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_precision(self):
        prec = self.config['math'].get('precision_digits', 100)
        getcontext().prec = prec
        print(f"[MathCore] Precision set to {prec} digits.")

    def _generate_pi(self):
        # Chudnovsky algoritmus pro PI (zjednodušený pro Decimal)
        # Pro naše účely zatím stačí načíst hardcoded string s vysokou přesností,
        # aby byl start rychlý. Pro 100 míst stačí toto:
        pi_str = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
        return Decimal(pi_str)

    def evaluate_expr(self, expr_str, context_vars={}):
        """
        Bezpečně vyhodnotí matematický výraz ze stringu (z JSONu).
        Nahradí 'pi', 'alpha' atd. za Decimal objekty.
        """
        # Základní konstanty
        local_context = {
            "pi": self.PI,
            "e": self.E,
            "ln": lambda x: x.ln() if isinstance(x, Decimal) else Decimal(math.log(x)),
            "sqrt": lambda x: x.sqrt() if isinstance(x, Decimal) else Decimal(math.sqrt(x))
        }
        # Přidání proměnných z kontextu (např. Alpha)
        local_context.update(context_vars)

        # Nahrazení syntaxe pro mocniny (pokud je v JSONu '^' místo '**')
        clean_expr = expr_str.replace("^", "**")

        try:
            # POZOR: eval() je nebezpečný v produkci, ale zde parsujeme vlastní JSONy.
            # Pro vědecké použití je to akceptovatelné.
            result = eval(clean_expr, {"__builtins__": None}, local_context)
            return Decimal(result)
        except Exception as e:
            print(f"[Error] Failed to evaluate: {expr_str} -> {e}")
            return None

    def load_data(self, json_path):
        with open(json_path, 'r') as f:
            return json.load(f)