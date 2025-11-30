# src/constants_manager.py

import json
from typing import List, Dict, Any

class ConstantsManager:
    """
    Třída pro načítání a správu fyzikálních a matematických konstant ze souboru JSON.

    Načte data a pro každou konstantu přidá klíč 'value_float', který obsahuje
    hodnotu převedenou na standardní 64-bitový float pro rychlé výpočty.
    """
    def __init__(self, json_path: str):
        """
        Inicializuje manažer a načte konstanty ze zadané cesty.

        Args:
            json_path (str): Cesta k souboru constants.json.
        """
        self._constants: List[Dict[str, Any]] = []
        self._load_constants(json_path)

    def _load_constants(self, json_path: str) -> None:
        """
        Interní metoda pro načtení a zpracování souboru JSON.
        """
        print(f"Loading constants from '{json_path}'...")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                raw_constants = json.load(f)

            for const_data in raw_constants:
                # Zpracujeme každou konstantu a přidáme pole pro rychlý výpočet
                processed_const = {
                    "name": const_data["name"],
                    "symbol": const_data["symbol"],
                    "value_str": const_data["value"],  # Původní hodnota jako string pro vysokou přesnost
                    "value_float": float(const_data["value"]), # Hodnota pro Fázi 1 na GPU
                    "uncertainty": const_data["uncertainty"],
                    # Rozměry: [kg, m, s, A, K, mol, cd]
                    "dimensions": const_data["dimensions"]
                }
                self._constants.append(processed_const)

            print(f"Successfully loaded and processed {len(self._constants)} constants.")

        except FileNotFoundError:
            print(f"ERROR: Constants file not found at '{json_path}'.")
            raise
        except json.JSONDecodeError:
            print(f"ERROR: Could not decode JSON from '{json_path}'. Check for syntax errors.")
            raise
        except KeyError as e:
            print(f"ERROR: Missing key {e} for a constant in '{json_path}'.")
            raise

    @property
    def constants(self) -> List[Dict[str, Any]]:
        """
        Vlastnost (property) pro bezpečný přístup k načteným a zpracovaným konstantám.
        """
        return self._constants

# --- Příklad použití (pro samostatné spuštění a testování) ---
if __name__ == '__main__':
    print("--- DEMO: Constants Manager ---")

    # Předpokládáme, že skript spouštíme z kořenového adresáře projektu
    CONSTANTS_FILE_PATH = "data/constants.json"

    try:
        # 1. Vytvoření instance manažera
        manager = ConstantsManager(CONSTANTS_FILE_PATH)

        # 2. Získání seznamu konstant
        all_constants = manager.constants

        # 3. Ověření, že data byla načtena a zpracována správně
        if all_constants:
            print("\nVerification:")
            print(f"Total constants loaded: {len(all_constants)}")

            print("\n--- Example: First constant ---")
            first_const = all_constants[0]
            for key, value in first_const.items():
                print(f"  {key}: {value} (type: {type(value).__name__})")

            print("\n--- Example: Gravitational constant (G) ---")
            g_const = next((c for c in all_constants if c['symbol'] == 'G'), None)
            if g_const:
                for key, value in g_const.items():
                    print(f"  {key}: {value} (type: {type(value).__name__})")
            else:
                print("Gravitational constant 'G' not found in the list.")

    except Exception as e:
        print(f"\nAn error occurred during the demo: {e}")