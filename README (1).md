# Equation Explorer v1.8

## Popis projektu

**Equation Explorer** je vysoce výkonný výpočetní nástroj navržený k systematickému prohledávání matematických vztahů mezi fundamentálními fyzikálními a matematickými konstantami. Cílem projektu není "fitting" dat, ale snaha o "znovuobjevení" známých fyzikálních zákonů nebo potenciální nalezení nových, dosud neznámých numerických souvislostí.

Program využívá masivně paralelní výpočty na grafických kartách NVIDIA (pomocí CUDA) k ověření bilionů kombinací v krátkém čase.

### Jak to funguje

Aplikace funguje na principu **Producer-Consumer Pipeline**:

1.  **Producer (CPU Proces):**
    *   **`equation_generator.py`** systematicky generuje rovnice od nejjednodušších po nejsložitější.
    *   V každém kroku aplikuje sadu "inteligentních" filtrů, aby se vyhnul generování matematicky triviálních rovnic (např. `A/A=1` nebo `A*1=A`).
    *   Vygenerované rovnice jsou tříděny na "Standardní" (vysoce přesné) a "Gravitační" (obsahující nepřesnou konstantu G).
    *   Dávky rovnic jsou posílány do dvou oddělených front.

2.  **Consumer (GPU Proces):**
    *   **`calculation_engine.py`** běží v hlavním procesu a monitoruje fronty.
    *   Jakmile se objeví dávka, načte ji a pomocí vlastního, vysoce optimalizovaného CUDA C++ kernelu ji paralelně zpracuje na GPU.
    *   GPU numericky vyhodnotí každou rovnici a provede dimenzionální analýzu.
    *   Nalezené numerické shody jsou poslány zpět na CPU, kde projdou finálním "Filtrem inteligence" (**Princip Emergence**), který zahodí všechny tautologické výsledky (např. `(G*m_p)/m_p = G`).
    *   Skutečně zajímavé výsledky jsou okamžitě zapsány do logovacích souborů.

## Systémové požadavky a závislosti

### Hardware
*   **Grafická karta NVIDIA** s podporou CUDA (architektura Maxwell nebo novější).
*   Vícejádrový procesor (doporučeno 4+ jader) pro efektivní generování rovnic.

### Software
*   **Linux** (testováno na Ubuntu 24.04).
*   **NVIDIA Ovladač** a kompletní **CUDA Toolkit**.
*   **Python** (testováno s verzí 3.11+).

### Python knihovny
Všechny potřebné knihovny lze nainstalovat pomocí `pip`.

```bash
# Hlavní knihovna pro GPU výpočty (vyberte verzi podle vašeho CUDA Toolkitu)
# Pro CUDA 12.x:
pip install cupy-cuda12x

# Pro CUDA 11.x:
# pip install cupy-cuda11x

# Knihovna pro práci s konfiguračními soubory
pip install PyYAML