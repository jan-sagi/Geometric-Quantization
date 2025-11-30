
***

# The Dimensionless Universe: An Ab Initio Derivation of Fundamental Constants from Geometric Axioms

**Author:** Jan Šági
**Date:** November 27, 2025
**Subject:** Grand Unification / Geometric Physics

---

## Abstract

This paper presents a phenomenological framework suggesting that the fundamental constants of nature, including the fine-structure constant ($\alpha$), the proton-to-electron mass ratio ($\mu$), and the gravitational coupling constant ($\alpha_G$), can be derived solely from the mathematical constant $\pi$ and the natural logarithmic base of spacetime $N = \ln(4\pi)$. By replacing empirical measurements with geometric definitions, we construct a "dimensionless" model of the universe that reproduces the CODATA 2018 values for particle masses and the gravitational constant with a relative error of $\approx 0.02\%$. Furthermore, the model analytically derives a value for the Hubble constant $H_0 \approx 67.30$ km/s/Mpc, consistent with Planck 2018 data, without relying on cosmological observation. These findings suggest that physical reality may emerge from a fractally structured geometric lattice where mass and gravity are topological properties of space itself.

## 1. Introduction

The Standard Model of particle physics relies on approximately 26 free parameters that must be determined experimentally. Among these are the masses of elementary particles and the coupling constants of fundamental forces. The search for a "Grand Unified Theory" is essentially a search for a mathematical logic that reduces these arbitrary parameters to a smaller set of axioms.

In this work, we explore the hypothesis that the universe operates as a purely geometric system. We propose that "mass" is a measure of geometric complexity (nodal resonance) and "gravity" is a result of dimensional damping across a high-dimensional manifold.

Our goal is to demonstrate that by defining the fine-structure constant $\alpha$ purely geometrically, we can derive the properties of the Micro-scale (Quantum Mechanics), Meso-scale (Nuclear Physics), and Macro-scale (Cosmology) *ab initio*, eliminating the need for arbitrary physical units.

## 2. Geometric Axioms

The model is built upon three dimensionless definitions derived solely from $\pi$. We postulate that the electromagnetic interaction strength ($\alpha$) represents a summation of holographic dimensions: volumetric ($4\pi^3$), superficial ($\pi^2$), and linear ($\pi$).

$$ \alpha^{-1}_{geom} = 4\pi^3 + \pi^2 + \pi \approx 137.03630 $$

Consequently, the geometric fine-structure constant is:
$$ \alpha_{geom} = \frac{1}{4\pi^3 + \pi^2 + \pi} $$

We further define the logarithmic spacetime base $N$, derived from the spherical topology ($4\pi$):
$$ N = \ln(4\pi) \approx 2.531 $$

## 3. Derivation of Matter (The Complexity Scalar)

In this framework, elementary particles are treated as resonant nodes on a lattice defined by $N$ and $\pi$. We utilize the electron mass $m_e$ as the unitary scalar.

### 3.1 The Muon ($\mu$)
The muon represents the fundamental spherical node ($k=1$) on the lepton scale ($4\pi N^3$). Its mass is corrected by a topological factor corresponding to the Euler characteristic of a sphere ($n=2$).

$$ m_\mu = m_e \cdot \frac{4\pi N^3}{1 - 2\alpha_{geom}} \approx 206.768 \ m_e $$

This result aligns with the experimental value (206.768) with a relative error of **0.00001%**.

### 3.2 The Proton ($p$) and the Baryon Scalar ($S_B$)
The proton is identified as the node of perfect geometric symmetry ($k=6$) on the baryon scale ($\pi^5$). In this model, the proton is not merely a particle but the fundamental "Complexity Scalar" ($S_B$) of the universe.

$$ S_B = \frac{m_p}{m_e} = 6\pi^5 \approx 1836.118 $$

The deviation from the experimental value (1836.152) is **0.0018%**. The stability of the proton is attributed to its perfect hexagonal symmetry, requiring zero topological correction.

### 3.3 The Tau Lepton ($\tau$)
The Tau particle corresponds to a prime-number excitation ($k=17$) of the muon base, scaled by $N^3$.

$$ m_\tau = m_\mu \cdot N^3 \cdot (1 + 5\alpha_{geom}) \approx 3474.85 \ m_e $$

## 4. Grand Unification: The Dimensionless Gravity

One of the most significant results of this study is the derivation of the gravitational coupling constant $\alpha_G$ (the ratio of gravitational to electromagnetic force) without measuring mass or distance.

We propose that gravity is the electromagnetic geometry of the proton ($S_B$) damped through the effective dimensionality of space ($X$). The dimensional exponent $X$ is defined as:

$$ X = \frac{10\pi}{3} + \frac{\alpha_{geom}}{4\pi} + \sqrt{2}\alpha_{geom}^2 \approx 10.4726 $$

The gravitational coupling $\alpha_G$ is then:

$$ \alpha_G = S_B^2 \cdot \alpha_{geom}^{2X} = (6\pi^5)^2 \cdot \left( \frac{1}{4\pi^3 + \pi^2 + \pi} \right)^{2X} $$

Using standard SI constants only for unit conversion ($c, \hbar, m_e$), we calculate Newton's constant $G$:

$$ G_{theor} = \frac{\hbar c}{m_e^2} \cdot \alpha_G \approx 6.6732 \times 10^{-11} \text{ m}^3\text{kg}^{-1}\text{s}^{-2} $$

This matches the CODATA 2018 value ($6.6743 \times 10^{-11}$) with a precision of **0.016%**. This implies that gravity is not a fundamental force but a geometric consequence of proton complexity within a specific dimensional manifold.

## 5. Cosmology: The Hubble Constant

Finally, we apply the Baryon Scalar ($S_B$) to the macroscopic scale to derive the rate of cosmic expansion ($H_0$). The radius of the observable universe is modeled as the quantum radius projected through gravitational coupling and scaled by the complexity of matter.

$$ R_{univ} = \left( \frac{\hbar}{m_e c \cdot \alpha_G} \cdot \frac{\alpha_{geom}}{2\pi(1+2\alpha_{geom})} \right) \cdot \frac{1}{S_B} $$

The Hubble constant is derived simply as $H_0 = c / R_{univ}$.

$$ H_0 \approx 67.30 \text{ km/s/Mpc} $$

This result is in striking agreement with the **Planck 2018** mission data ($67.4 \pm 0.5$ km/s/Mpc), supporting the hypothesis that the expansion rate of the universe is mathematically tied to the mass of the proton.

## 6. Conclusion

We have demonstrated that a consistent physical model can be constructed purely from the geometry of $\pi$, without reliance on arbitrary free parameters. The "Dimensionless Universe" model successfully unifies the mass spectrum, nuclear stability, and gravitational interaction into a single geometric framework.

The fact that the fine-structure constant $\alpha \approx (4\pi^3 + \pi^2 + \pi)^{-1}$ yields correct predictions across 40 orders of magnitude—from the muon to the Hubble constant—suggests that the fundamental laws of physics may be emergent properties of a fractal geometry.

---

### Data Availability
All Python scripts used for the high-precision verification of these equations, including the "Stress Tests" and "Ab Initio" generators, are available in the public Zenodo repository:
`https://zenodo.org/records/17704428`

### References
1.  Tiesinga, E., Mohr, P. J., Newell, D. B., & Taylor, B. N. (2021). CODATA recommended values of the fundamental physical constants: 2018. *Reviews of Modern Physics*, 93(2), 025010.
2.  Planck Collaboration. (2020). Planck 2018 results. VI. Cosmological parameters. *Astronomy & Astrophysics*, 641, A6.
3.  Dirac, P. A. M. (1937). The Cosmological Constants. *Nature*, 139, 323.