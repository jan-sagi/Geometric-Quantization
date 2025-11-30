import random
from typing import List, Dict, Any

class EquationGenerator:
    """
    Generátor rovnic pracující na principu Monte Carlo (Random Walk).

    Místo systematického prohledávání (které v hloubce 4+ exponenciálně exploduje)
    generuje náhodné, matematicky validní RPN sekvence.

    Tento přístup umožňuje "sondovat" hluboký prostor kombinací (5-7 konstant),
    kam by se systematický generátor nikdy nedostal.
    """

    def __init__(self, constants: List[Dict[str, Any]], operators: Dict[str, int], max_depth: int):
        """
        Args:
            constants: Seznam načtených konstant.
            operators: Slovník operátorů a jejich kódů (např. {'add': -1}).
            max_depth: (V tomto režimu slouží spíše jako horní limit pro náhodnou délku).
        """
        self.constants = constants
        self.operators = operators
        # Seznam ID konstant (1, 2, 3...)
        self.const_ids = [i + 1 for i in range(len(constants))]
        # Seznam ID operátorů (-1, -2...)
        self.op_ids = list(operators.values())

        # Optimalizace: Identifikace "jednoduchých" konstant pro případné váhování
        self.simple_const_ids = []
        for i, c in enumerate(constants):
            if c['symbol'] in ['one', 'two', 'half', 'three', 'pi', 'alpha']:
                self.simple_const_ids.append(i + 1)

    def _generate_random_rpn(self, num_constants: int) -> List[int]:
        """
        Vygeneruje jednu náhodnou validní RPN rovnici.

        Aby byla RPN rovnice platná, musí platit:
        1. Počet konstant = N
        2. Počet binárních operátorů = N - 1
        3. V každém kroku čtení zleva musí být v zásobníku dostatek operandů (stack_size >= 2 pro operátor).

        Args:
            num_constants: Požadovaný počet konstant v rovnici (složitost).
        """
        if num_constants == 1:
            return [random.choice(self.const_ids)]

        rpn = []
        stack_size = 0
        consts_left = num_constants
        ops_left = num_constants - 1

        # Stavíme rovnici zleva doprava
        while consts_left > 0 or ops_left > 0:
            choices = []

            # Můžeme přidat konstantu? (Pokud ještě nějaké zbývají)
            # Poznámka: Nemůžeme přidat konstantu jen tehdy, pokud by nám pak nezbyly sloty pro operátory
            # k redukci, ale u RPN to většinou není problém, dokud máme operátory.
            if consts_left > 0:
                choices.append('CONST')

            # Můžeme přidat operátor? (Jen pokud máme v zásobníku alespoň 2 čísla)
            if ops_left > 0 and stack_size >= 2:
                # Speciální pravidlo: Pokud už nemáme žádné konstanty, MUSÍME dát operátor
                if consts_left == 0:
                    choices = ['OP']
                else:
                    choices.append('OP')

            # Pokud je zásobník prázdný nebo má 1 prvek, MUSÍME dát konstantu (pokud to jde)
            if stack_size < 2 and 'OP' in choices:
                if 'CONST' in choices:
                    choices = ['CONST']

            # Náhodný výběr kroku
            pick = random.choice(choices)

            if pick == 'CONST':
                # Zde můžeme jemně zvýhodnit jednoduchá čísla, aby rovnice nebyly příliš "divoké",
                # ale pro čistý random search je lepší uniformní rozdělení.
                # Občas (30%) zkusíme vzít jednoduchou konstantu (one, two, pi...), pokud existují.
                if self.simple_const_ids and random.random() < 0.3:
                     cid = random.choice(self.simple_const_ids)
                else:
                     cid = random.choice(self.const_ids)

                rpn.append(cid)
                stack_size += 1
                consts_left -= 1
            else:
                # Výběr operátoru
                oid = random.choice(self.op_ids)
                rpn.append(oid)
                stack_size -= 1
                ops_left -= 1

        return rpn

    def generate_random_batch(self, batch_size: int, min_consts: int = 3, max_consts: int = 6) -> List[List[int]]:
        """
        Hlavní metoda pro generování dávky náhodných rovnic.

        Args:
            batch_size: Kolik rovnic vygenerovat.
            min_consts: Minimální složitost (počet konstant). 3 odpovídá (A*B/C).
            max_consts: Maximální složitost. 6 odpovídá velmi komplexním vztahům.
        """
        batch = []
        for _ in range(batch_size):
            # Náhodně zvolíme složitost pro tuto konkrétní rovnici
            n_c = random.randint(min_consts, max_consts)

            # Vygenerujeme RPN
            eq = self._generate_random_rpn(n_c)
            batch.append(eq)

        return batch

    def generate_in_batches(self, batch_size: int):
        """
        Legacy metoda pro zachování kompatibility s původním voláním v main.py,
        pokud by nebyl main.py upraven. Přesměruje na random batch.
        """
        while True:
            # Generujeme donekonečna
            yield self.generate_random_batch(batch_size, min_consts=3, max_consts=5)