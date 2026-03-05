# EPISTEMIC_CRYPTOGRAPHY_INTEGRATION.md
Status: INTERNAL PoC
Scope: Φ-Core Only
Influence on Φ: Descriptive
Influence from Monetization Layer: None

---

## 1. Ontological Position

Epistemická kryptografia je štrukturálna auditná vrstva,
ktorá zachováva geometriu neistoty bez zásahu do systému.

Referenčný formalizmus:
0

Táto vrstva:

- neoptimalizuje
- nerozhoduje
- neblokuje
- neintervenuje
- nevytvára spätné slučky

Je čisto deskriptívna.

---

## 2. Implementačný Status v rámci Vortex architektúry

Epistemická kryptografia je implementovaná:

- v module `core/epistemic_crypto.py`
- ako výpočtová vrstva nad stavom Φ
- pred projekciou do monetizačnej vrstvy

Nie je implementovaná:

- vo vortexmoneti/
- v UI
- v reporte
- v agregátore

---

## 3. Výpočtové veličiny

Nech:

µ_i(t) = lokálna epistemická neistota  
A_ij(t) = párová štrukturálna asymetria  

Potom:

µ_total(t) = Σ µ_i(t)  
A_total(t) = Σ A_ij(t)

Topologická pokora:

h(t) = µ_total / (µ_total + A_total)

Platí:

0 ≤ h ≤ 1

Ak menovateľ = 0 → h = 1

---

## 4. Kritická podmienka oddelenia

Epistemická kryptografia:

- je vypočítaná v Core
- je zahrnutá v Projection JSON
- je read-only pre monetizačnú vrstvu

Platí:

∂Φ / ∂Monetization = 0

---

## 5. Proof of Concept Test

Ak odstránime:

/vortexmoneti/

Φ + Epistemická kryptografia musia zostať:

- funkčné
- identické
- invariantné

Ak nie, architektúra je porušená.

---

## 6. Záver

Epistemická kryptografia je:

- ontologicky nadradená monetizačnej vrstve
- nezávislá od biznis logiky
- invariantná voči UI a reportom

Je to audit geometrie neistoty,
nie nástroj rozhodovania.
