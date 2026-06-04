# VECTAETOS — ANCHOR: 𝒟 / Δ / E / κ / QE
## Admissible Curvature Domain of Φ

Status: CANONICAL ANCHOR  
Layer: Ontological / Meta-Mathematical  
Scope: Admissible Curvature Domain of Φ  
Lineage: VECTAETOS 1.x  
Authority: Descriptive Only  
Agency: None  
Optimization: None  
Feedback: None

---

## 0. Purpose

This anchor defines the admissible curvature domain **𝒟** of the VECTAETOS epistemic field.

𝒟 is not an algorithm.  
𝒟 is not a scoring space.  
𝒟 is not a safety filter.  
𝒟 is not a decision boundary.  
𝒟 is not a runtime validator.

𝒟 defines the domain of epistemic curvature configurations that can exist as representable field states.

---

## 1. Base Field

Let:

$$\Sigma = \{\Sigma_1,\ldots,\Sigma_8\}$$

be the fixed set of invariant axiomatic singularities.

Let:

$$R \in C^1\simeq\mathfrak{so}(8)$$

be the antisymmetric relational tension matrix, with:

$$R_{ij}=-R_{ji}$$

$$R_{ii}=0$$

The epistemic field is:

$$\Phi=(\Sigma,R)$$

Φ is not an agent.  
Φ is not a controller.  
Φ is not an optimizer.  
Φ is not a decision system.

Φ is a relational epistemic field.

---

## 2. Relational Cochain Spaces

Let:

$$C^0$$

be the space of scalar assignments to singularities.

Let:

$$C^1$$

be the space of antisymmetric relational cochains on pairs of singularities.

Let:

$$C^2$$

be the space of oriented triangular relational curvature cochains.

Let:

$$C^3$$

be the space of oriented tetrahedral boundary-consistency cochains.

Since $|\Sigma|=8$:

$$\dim C^0 = 8$$

$$\dim C^1 = \binom{8}{2}=28$$

$$\dim C^2 = \binom{8}{3}=56$$

$$\dim C^3 = \binom{8}{4}=70$$

These spaces are structural.

They are not action spaces.

They are not decision spaces.

They are not optimization spaces.

---

## 3. Gauge Operator $d_0$

Define:

$$d_0:C^0\rightarrow C^1$$

by:

$$(d_0\varphi)_{ij}=\varphi_j-\varphi_i$$

for scalar assignments:

$$\varphi \in C^0$$

This expresses relational gauge displacement.

It does not create authority.

It does not define preference.

It does not privilege any singularity.

---

## 4. Curvature Operator $d_1$

Define:

$$d_1:C^1\rightarrow C^2$$

by:

$$(d_1(R))_{ijk}=R_{ij}+R_{jk}+R_{ki}$$

The epistemic curvature is:

$$\Delta=d_1(R)$$

Thus:

$$\Delta \in C^2$$

Δ is not an algorithmic output.

Δ is the relational curvature induced by the field configuration $R$.

Because:

$$d_1d_0=0$$

curvature is invariant under relational gauge transformations:

$$R\sim R+d_0\varphi$$

Thus Δ does not encode absolute relational authority.

It encodes only cyclic relational tension.

---

## 5. Boundary-Consistency Operator $d_2$

Let:

$$d_2:C^2\rightarrow C^3$$

be the induced boundary-consistency operator satisfying:

$$d_2d_1=0$$

Therefore:

$$d_2\Delta=0$$

whenever:

$$\Delta=d_1(R)$$

Important clarification:

$$d_2\Delta=0$$

is a topological consistency condition.

It must not be interpreted as a Hodge codifferential condition.

It is not a minimization condition.

It is not a smoothness objective.

It is not an optimization constraint.

---

## 6. Algebraic Curvature Domain

Define the algebraic curvature domain as the image of the first coboundary map:

$$\mathcal{D}_{\mathrm{alg}} := \mathrm{Im}\left(d_1:C^1\to C^2\right) \subseteq C^2$$

Equivalently:

$$\mathcal{D}_{\mathrm{alg}} = \left\{\Delta\in C^2\;\middle|\;\exists R\in C^1\simeq\mathfrak{so}(8)\text{ such that }\Delta=d_1(R)\right\}$$

Because:

$$d_2d_1=0$$

every algebraic curvature configuration satisfies:

$$d_2\Delta=0$$

Thus:

$$\Delta\in\mathcal{D}_{\mathrm{alg}}\Rightarrow d_2\Delta=0$$

This is a structural condition.

It is not a validity score.

---

## 7. Triality Action

Let:

$$\mathcal{T}$$

be the declared finite triality action on $C^2$.

For:

$$\tau\in\mathcal{T}$$

define the induced signed cochain action:

$$(\tau\cdot \Delta)_{ijk}=\mathrm{sgn}\left(\tau|_{\{i,j,k\}}\right)\,\Delta_{\tau(i)\tau(j)\tau(k)}$$

with the canonical antisymmetric extension on oriented triples.

This action is declared structurally.

It does not introduce:

- a generator
- a selector
- an optimizer
- a preferred axis
- a privileged singularity
- a decision mechanism

Let:

$$P_{\mathcal{T}}$$

be the triality-invariant projection:

$$P_{\mathcal{T}}=\frac{1}{|\mathcal{T}|}\sum_{\tau\in\mathcal{T}}\tau$$

A curvature configuration is triality-balanced iff:

$$P_{\mathcal{T}}\Delta=\Delta$$

Triality does not generate configurations.

Triality prevents degeneracy into a privileged representational axis.

---

## 8. Triality-Compatible Curvature Domain

Define:

$$\mathcal{D}_{\mathrm{tri}}=\mathcal{D}_{\mathrm{alg}}\cap\mathrm{Fix}(\mathcal{T})$$

where:

$$\mathrm{Fix}(\mathcal{T})=\left\{\Delta\in C^2\;\middle|\;P_{\mathcal{T}}\Delta=\Delta\right\}$$

Thus:

$$\mathcal{D}_{\mathrm{tri}}=\left\{\Delta\in C^2\;\middle|\;\exists R\in\mathfrak{so}(8):\Delta=d_1(R),\;d_2\Delta=0,\;P_{\mathcal{T}}\Delta=\Delta\right\}$$

$\mathcal{D}_{\mathrm{tri}}$ is the triality-compatible structural domain.

It is not yet the full admissible domain.

Representability is still required.

---

## 9. Ontological Representability Predicate

Define:

$$\mathrm{Rep}(\Delta)\in\{0,1\}$$

where:

$$\mathrm{Rep}(\Delta)=1$$

iff Δ can exist as a representable epistemic curvature configuration.

Rep is not:

- a metric
- a score
- an optimization target
- a probability
- a ranking function
- a classifier
- a policy
- a deployment threshold

Rep is an ontological predicate of representability.

A curvature configuration fails representability if it:

- privileges a single triality axis
- forces dominance of one singularity
- collapses 4ES plurality
- induces prescriptive closure
- destroys global relational readability
- cannot sustain representable epistemic carrier status

Rep does not decide.

Rep does not filter.

Rep does not command.

Rep only marks whether a curvature configuration is ontologically representable.

---

## 10. Final Definition of 𝒟

The admissible curvature domain is:

$$\boxed{\mathcal{D}=\left\{\Delta\in C^2\;\middle|\;\exists R\in\mathfrak{so}(8):\Delta=d_1(R),\;d_2\Delta=0,\;P_{\mathcal{T}}\Delta=\Delta,\;\mathrm{Rep}(\Delta)=1\right\}}$$

Equivalently:

$$\boxed{\mathcal{D}=\mathcal{D}_{\mathrm{alg}}\cap\mathrm{Fix}(\mathcal{T})\cap\mathcal{R}_{\mathrm{rep}}}$$

where:

$$\mathcal{R}_{\mathrm{rep}}=\left\{\Delta\in C^2\;\middle|\;\mathrm{Rep}(\Delta)=1\right\}$$

𝒟 is the domain of admissible curvature.

𝒟 is not computed as authority.

𝒟 is not selected as a target.

𝒟 is not optimized.

𝒟 is the structural domain in which representable epistemic field states can exist.
