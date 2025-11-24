# Geometric Quantization of Matter
### Analysis of Correlations between Fundamental Constants and Particle Spectrum

**Author:** Jan Šági  
**Status:** Public Review / Phenomenological Study  
**Date:** November 2025

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

## 📄 Abstract
This repository contains the verification code and data for the hypothesis of **Geometric Quantization**. The model suggests that the masses of stable elementary particles and the gravitational constant ($G$) are derived from strict geometric relations of the constants $\pi$, $\alpha$ (fine-structure constant), and the logarithmic spacetime base $N = \ln(4\pi)$.

Unlike standard numerology, this model offers a **single geometric framework** that connects the microscopic scale (particle masses) with the macroscopic scale (Gravity) with high statistical significance.

---

## 🧪 The "Fair Test" (Discovery Mode)
To demonstrate that the correlations are not a result of overfitting or parameter tuning, we provide the **FairTest** engine (`FairTest.py`). 

This script performs a **"blind scan"** of the energy spectrum (0–15 GeV) using **only integers ($k$)** and base constants ($\pi, \alpha, N$). **No specific topological corrections ($n\alpha$) are applied in this scan.** This tests the existence of the fundamental lattice itself.

### Key Results from `FairTest.txt`
The raw scan reveals that known particles align with the geometric lattice spontaneously, often at **Prime Number Nodes**.

| Particle | Scale Type | Node ($k$) | Error (Raw) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Pion+** ($\pi^+$) | Meson ($\alpha^{-1}$) | **2** (Prime) | 0.3 % | ✅ Confirmed |
| **Kaon+** ($K^+$) | Meson ($\alpha^{-1}$) | **7** (Prime) | 0.7 % | ✅ Confirmed |
| **Proton** ($p$) | Baryon ($\pi^5$) | **6** (Hexagon) | **0.0 %** | ✅ **Exact Match** |
| **Rho** ($\rho$) | Meson ($\alpha^{-1}$) | **11** (Prime) | 0.6 % | ✅ Confirmed |
| **Tau** ($\tau$) | Lepton ($N^3$) | **17** (Prime) | 0.4 % | ✅ Confirmed |
| **Glueball?** | Baryon ($\pi^5$) | **11** (Prime) | 0.0 % | ⚠️ Matches $f_0(1710)$ |
| **Prediction** | Baryon ($\pi^5$) | **41** (Prime) | --- | ❓ **Candidate at 6411 MeV** |

> **Run the Fair Test yourself:**
> ```bash
> python FairTest.py
> ```
> *Full output logs are available in [`FairTest.txt`](FairTest.txt).*

---

## 📐 Rigorous Verification (High Precision)
While the Fair Test shows the lattice exists, the **Rigorous Engine** (`The Geometric Universe...py`) applies topological corrections (based on Euler characteristics) to derive masses with 110-digit precision.

### 1. Fundamental Masses
The model derives the masses of the Proton and Muon with extreme precision without arbitrary parameters.

| Particle | Theory Formula | Theoretical Mass ($m_e$) | Experimental ($m_e$) | Rel. Error |
| :--- | :--- | :--- | :--- | :--- |
| **Muon** ($\mu$) | $4\pi N^3 \cdot (1-2\alpha)^{-1}$ | 206.76826... | 206.76828... | **0.000007 %** |
| **Proton** ($p$) | $6\pi^5$ | 1836.118... | 1836.152... | **0.0019 %** |

### 2. Unification with Gravity ($G$)
The model analytically derives the Gravitational Constant ($G$) from the proton mass ($m_p$) and $\alpha$.

$$ G_{theor} = \frac{\hbar c}{m_p^2} \cdot (\Gamma_p^2 \cdot \alpha^{2X}) $$

*Where $X \approx 10.47$ is a geometric dimensional exponent derived from $\pi$ and $\alpha$.*

*   **Theoretical G:** $6.67405 \times 10^{-11}$
*   **CODATA Value:** $6.67430 \times 10^{-11}$
*   **Error:** **0.0037 %**

---

## 📂 Repository Contents

*   `FairTest.py` - **Start Here.** A brute-force scanner that maps integers to particle masses. Zero-tuning.
*   `FairTest.txt` - The raw console output from the Fair Test scan.
*   `The Geometric Universe: Grand Unified Engine.py` - The rigorous verification script with 110-digit precision.
*   `geometric_scan_results.csv` - Dataset of all geometric nodes up to 30 GeV.
*   `paper_final.pdf` - The formal scientific paper describing the theory.
*   `index.html` - A web-based presentation of the equations.

## 💻 Reproducibility

Scientific claims must be falsifiable. You can reproduce all calculations on your own machine using the provided Python scripts.

### Prerequisites
*   Python 3.x
*   Standard libraries (`decimal`, `math`, `sys`, `csv`, `numpy`)

### How to Run

**1. Run the Fair Test (Discovery Mode):**
```bash
python FairTest.py
