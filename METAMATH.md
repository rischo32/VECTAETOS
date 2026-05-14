1. Invariantné singularity

```math
\Sigma = \{\Sigma_1,\Sigma_2,\ldots,\Sigma_8\}
```

```math
\Sigma =
\{\mathrm{INT},\mathrm{LEX},\mathrm{VER},\mathrm{LIB},
\mathrm{UNI},\mathrm{REL},\mathrm{WIS},\mathrm{CRE}\}
```

2. Relačná štruktúra

```math
R \in \mathfrak{so}(8)
```

```math
R_{ij} = -R_{ji}
```

```math
R_{ii} = 0
```

```math
\dim \mathfrak{so}(8) = \binom{8}{2} = 28
```

3. Pole Φ

```math
\Phi = (\Sigma, R)
```

4. Neformálna skratka — nepoužiť ako definíciu

```math
\Phi' = \Phi + \tau
```

This expression is informal shorthand only and must not be used as a formal definition.

5. Kandidátna trajektória ako deformácia

```math
\tau \leadsto \delta R_{\tau}
```

```math
\delta R_{\tau} \in \mathfrak{so}(8)
```

```math
\delta R_{\tau,ij} = -\delta R_{\tau,ji}
```

```math
\delta R_{\tau,ii} = 0
```

6. Kandidátna relačná konfigurácia

```math
R' = R + \delta R_{\tau}
```

```math
R' \in \mathfrak{so}(8)
```

```math
R'_{ij} = -R'_{ji}
```

```math
R'_{ii} = 0
```

```math
\Phi' = (\Sigma, R')
```

7. Operátor krivosti

```math
d_1 : C^1 \to C^2
```

```math
\Delta = d_1 R
```

```math
\Delta' = d_1 R'
```

```math
\Delta(i,j,k) = R_{ij} + R_{jk} + R_{ki}
```

```math
\Delta'(i,j,k) = R'_{ij} + R'_{jk} + R'_{ki}
```

```math
\Delta \in C^2
```

```math
\Delta' \in C^2
```

```math
\dim C^2 = \binom{8}{3} = 56
```

8. Doména reprezentovateľnej krivosti

```math
\mathcal{D} \subset C^2
```

```math
\mathcal{D}
=
\left\{
\Delta \in C^2
\;\middle|\;
\Delta
\text{ is ontologically representable}
\right\}
```

9. Koherenčný predikát cez 𝒟

```math
K_{\mathcal{D}}(\Phi)=1
\iff
\Delta \in \mathcal{D}
```

```math
K_{\mathcal{D}}(\Phi)=0
\iff
\Delta \notin \mathcal{D}
```

```math
K_{\mathcal{D}}(\Phi')=1
\iff
\Delta' \in \mathcal{D}
```

```math
K_{\mathcal{D}}(\Phi')=0
\iff
\Delta' \notin \mathcal{D}
```

10. Epistemický priestor E

```math
E =
\left\{
\Phi
\;\middle|\;
K_{\mathcal{D}}(\Phi)=1
\right\}
```

```math
\Phi \in E
\iff
K_{\mathcal{D}}(\Phi)=1
```

```math
\Phi \notin E
\iff
K_{\mathcal{D}}(\Phi)=0
```

11. ZMYSEL / Ξ

```math
\Xi = E
```

```math
\Phi \in \Xi
\iff
\Phi \in E
```

```math
\Phi \notin \Xi
\iff
\Phi \notin E
```

12. Reprezentovateľná vetva

```math
\Delta' \in \mathcal{D}
\Rightarrow
K_{\mathcal{D}}(\Phi')=1
```

```math
K_{\mathcal{D}}(\Phi')=1
\Rightarrow
\Phi' \in E
```

```math
\Phi' \in E
\land
\Xi = E
\Rightarrow
\Phi' \in \Xi
```

13. Nereprezentovateľná vetva

```math
\Delta' \notin \mathcal{D}
\Rightarrow
K_{\mathcal{D}}(\Phi')=0
```

```math
K_{\mathcal{D}}(\Phi')=0
\Rightarrow
\Phi' \notin E
```

```math
\Phi' \notin E
\land
\Xi = E
\Rightarrow
\Phi' \notin \Xi
```

14. QE aporia

```math
QE \iff \Phi' \notin \Xi
```

```math
QE_{\mathcal{D}} \iff \Delta' \notin \mathcal{D}
```

```math
QE_{\mathcal{D}}
\iff
K_{\mathcal{D}}(\Phi')=0
```

15. Projekcia

```math
\Pi : E \to \Gamma
```

```math
\Phi' \in E
\Rightarrow
\Pi(\Phi') \text{ is applicable}
```

```math
\Phi' \notin E
\Rightarrow
\Pi(\Phi') \text{ is not applicable}
```

```math
\Phi' \notin E
\Rightarrow
\nexists\, \Pi(\Phi')
```

16. Neexistencia projektovateľného stavu

```math
\Phi' \notin E
\Rightarrow
\text{no projectable state exists}
```

```math
\Phi' \notin E
\Rightarrow
\text{non-existence of a projectable state}
```

17. Impulz a realizovateľný prechod

```math
I \leadsto \tau_I
```

```math
\tau_I \leadsto \delta R_{\tau_I}
```

```math
R'_I = R + \delta R_{\tau_I}
```

```math
\Phi'_I = (\Sigma, R'_I)
```

```math
\Delta'_I = d_1R'_I
```

```math
\Delta'_I \notin \mathcal{D}
\Rightarrow
I \notin \mathrm{Transitions}_{\mathrm{realizable}}(\Phi)
```

18. Entropická pokora — mechanická forma

```math
\forall I:
\Delta'_I \notin \mathcal{D}
\Rightarrow
I \notin \mathrm{Transitions}_{\mathrm{realizable}}(\Phi)
```

```math
\forall I:
K_{\mathcal{D}}(\Phi'_I)=0
\Rightarrow
I \notin \mathrm{Transitions}_{\mathrm{realizable}}(\Phi)
```

```math
\forall I:
\Phi'_I \notin \Xi
\Rightarrow
I \notin \mathrm{Transitions}_{\mathrm{realizable}}(\Phi)
```

19. Nie zákaz, ale ontologická nemožnosť

```math
\Phi' \notin E
\Rightarrow
\text{ontological impossibility}
```

```math
\Phi' \notin E
\not\Rightarrow
\text{prohibition}
```

```math
\Phi' \notin E
\not\Rightarrow
\text{refusal}
```

```math
\Phi' \notin E
\not\Rightarrow
\text{punishment}
```

20. Kompletná reťaz v jednom bloku

```math
\Phi = (\Sigma, R)
```

```math
\tau \leadsto \delta R_{\tau}
```

```math
\delta R_{\tau} \in \mathfrak{so}(8)
```

```math
R' = R + \delta R_{\tau}
```

```math
\Phi' = (\Sigma, R')
```

```math
\Delta' = d_1R'
```

```math
\Delta' \in \mathcal{D}
\Rightarrow
K_{\mathcal{D}}(\Phi')=1
\Rightarrow
\Phi' \in E
\Rightarrow
\Phi' \in \Xi
```

```math
\Delta' \notin \mathcal{D}
\Rightarrow
K_{\mathcal{D}}(\Phi')=0
\Rightarrow
\Phi' \notin E
\Rightarrow
\Phi' \notin \Xi
\Rightarrow
QE
```

```math
\Phi' \notin E
\Rightarrow
\nexists\, \Pi(\Phi')
```

```math
\Phi' \notin E
\Rightarrow
\text{non-existence of a projectable state}
```

21. Najčistejší blok

```math
\tau \leadsto \delta R_{\tau}
\in \mathfrak{so}(8)
```

```math
R' = R + \delta R_{\tau}
```

```math
\Phi' = (\Sigma, R')
```

```math
\Delta' = d_1R'
```

```math
\Delta' \notin \mathcal{D}
\Rightarrow
K_{\mathcal{D}}(\Phi')=0
\Rightarrow
\Phi' \notin E = \Xi
\Rightarrow
QE
```

```math
\Pi : E \to \Gamma
```

```math
\Phi' \notin E
\Rightarrow
\Pi(\Phi') \text{ is non-applicable}
```

```math
\Phi' \notin E
\Rightarrow
\text{non-existence of a projectable state}
```
