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

## 🚀 Key Findings & Verification

The Python scripts in this repository verify the following derivations using 110-digit decimal precision.

### 1. Fundamental Masses (Low Energy)
The model derives the masses of the Proton and Muon with extreme precision without arbitrary parameters.

| Particle | Theory Formula | Theoretical Mass ($m_e$) | Experimental ($m_e$) | Rel. Error |
| :--- | :--- | :--- | :--- | :--- |
| **Muon** ($\mu$) | $4\pi N^3 \cdot (1-2\alpha)^{-1}$ | 206.76826... | 206.76828... | **0.000007 %** |
| **Proton** ($p$) | $6\pi^5$ | 1836.118... | 1836.152... | **0.0019 %** |

### 2. Unification with Gravity ($G$)
The model analytically derives the Gravitational Constant ($G$) from the proton mass and $\alpha$.

$$ G_{theor} = \frac{\hbar c}{m_p^2} \cdot (\Gamma_p^2 \cdot \alpha^{2X}) $$

*Where $X \approx 10.47$ is a geometric dimensional exponent derived from $\pi$ and $\alpha$.*

*   **Theoretical G:** $6.6735 \times 10^{-11}$
*   **CODATA Value:** $6.6743 \times 10^{-11}$
*   **Error:** **0.011 %**

### 3. High-Energy Sector (The "Primes" Discovery)
An extended geometric scan (0–300 GeV) revealed that the heaviest unstable particles align with the **Meson Scale** ($\alpha^{-1}$) specifically at **Prime Number Nodes**.

| Particle | Node ($k$) | Type | Theoretical (MeV) | Experimental (MeV) | Error |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Z Boson** | **1301** | Prime | 91,102 | 91,187 | **0.09 %** |
| **Higgs** | **1787** | Prime | 125,135 | 125,100 | **0.02 %** |
| **Top Quark**| **2467** | Prime | 172,752 | 172,760 | **0.004 %** |

---

## 💻 Reproducibility

Scientific claims must be falsifiable. You can reproduce all calculations on your own machine using the provided Python scripts.

### Prerequisites
*   Python 3.x
*   Standard libraries (`decimal`, `math`, `sys`, `csv`)

### How to Run
*Note: Since filenames contain spaces, please use quotes as shown below.*

**1. Verify Fundamental Constants & G:**
Run the verification engine to check the proton mass and gravitational constant derivation.
```bash
python "The Geometric Universe: Grand Unified Engine.py"
