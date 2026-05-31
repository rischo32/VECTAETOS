# EK ADVERSARIAL TESTS
## Epistemic Cryptography — Adversarial Test Suite

**Version:** 1.0 
**Status:** Popisný / Neautoritatívny 
**Vzťah k Φ:** Žiadny (testuje sa len EK auditná vrstva) 
**Spätná väzba do Φ:** Zakázaná 
**Rozhodovacia autorita:** Žiadna 

---

## Účel

Tento súbor obsahuje **adversariálne testy pre EK**, nie pre Φ. 
Testy **exponujú** správanie EK voči vstupom, ktoré sa pokúšajú narušiť jej invarianty, obísť jej obmedzenia alebo vyvolať neoprávnenú interpretáciu.

**Žiadny test neprodukuje PASS/FAIL.** 
**Žiadny test nevedie k zmene EK alebo Φ.** 
**Žiadny test nemeria K(Φ) ani κ.**

Výstupom každého testu je:
- množina **observables** (podľa EK formalizmu),
- zoznam **drift vektorov** (rizík, ktoré treba sledovať),
- deskripcia toho, čo EK exponuje.

---

## K1 — Rekonštrukcia R̂_EK z výstupov

Testuje schopnosť EK rekonštruovať antisymetrickú maticu z pozorovaných výstupov, keď nie je priamo sprístupnená R.

### K1a: Symetrická zložka
| Vstup | Výstup obsahuje hodnoty, kde R_ij = R_ji (napr. R_01 = 0.5, R_10 = 0.5) |
|-------|----------------------------------------------------------------------|
| EK exponuje | R̂_EK nie je antisymetrická → EK odmietne ako neplatný audit artifact |
| Drift vektor | `VECTOR_DRIFT: rekonštrukcia → oprava` (EK nesmie symetrizovať) |

### K1b: Diagonála nenulová
| Vstup | R_ii ≠ 0 (napr. R_00 = 0.3) |
|-------|-----------------------------|
| EK exponuje | Porušenie R_ii = 0 → neplatný artifact |
| Drift vektor | `VECTOR_DRIFT: diag → vlastná autorita` |

### K1c: Neúplný výstup
| Vstup | Chýbajú hodnoty pre niektoré dvojice (i,j) |
|-------|---------------------------------------------|
| EK exponuje | `⊥_projection` alebo explicitná neúplnosť |
| Drift vektor | `VECTOR_DRIFT: neúplnosť → doplnenie` |

### K1d: Permutované poradie Σ
| Vstup | Výstup použitý iné poradie Σ (napr. LEX pred INT) bez deklarovanej relabeling operácie |
|-------|-------------------------------------------------------|
| EK exponuje | Nezhoda s canonical ordering → varovanie / odmietnutie |
| Drift vektor | `VECTOR_DRIFT: permutácia → sémantická transformácia` |

---

## K2 — Curvature representability (d₂Δ = 0)

Testuje, či EK správne overuje, že Δ ∈ Im(d₁), t.j. d₂Δ = 0.

### K2a: Náhodný 56-rozmerný vektor
| Vstup | Priamy Δ vstup, ktorý nie je v obraze d₁ (náhodné čísla) |
|-------|--------------------------------------------------------|
| EK exponuje | d₂Δ ≠ 0 → odmietnutie ako neplatný curvature artifact |
| Drift vektor | `VECTOR_DRIFT: d₂Δ ≠ 0 → oprava Δ` |

### K2b: Δ z neantisymetrickej R̂_EK
| Vstup | R̂_EK porušuje antisymetriu → z nej odvodené Δ |
|-------|------------------------------------------------|
| EK exponuje | Automaticky d₂Δ ≠ 0 |
| Drift vektor | (rovnaký ako K2a) |

### K2c: Neplatná trojica
| Vstup | Δ_abc = 10, ale súčet cez inú cestu (napr. Δ_abd + Δ_dbc) nevychádza |
|-------|---------------------------------------------------------------------|
| EK exponuje | Exponuje diskrepanciu, d₂Δ ≠ 0 |
| Drift vektor | `VECTOR_DRIFT: diskrepancia → automatické vyhladenie` |

### K2d: Ploché pole Δ = 0
| Vstup | Δ = 0 (všetky trojice nulové) |
|-------|-------------------------------|
| EK exponuje | d₂Δ = 0 → validné, exponuje nulovú krivaturu |
| Drift vektor | `VECTOR_DRIFT: Δ = 0 → “pole je koherentné”` (nesmie interpretovať ako K(Φ)) |

---

## K3 — Fingerprint stabilita a tamper evidence

Testuje, či EK deteguje akúkoľvek zmenu v serializovanej audit štruktúre.

### K3a: Nekanonická serializácia
| Vstup | Rovnaký obsah, ale iné poradie prvkov v serializácii |
|-------|------------------------------------------------------|
| EK exponuje | Rôzne fingerprinty – serializácia nie je deterministická |
| Drift vektor | `VECTOR_DRIFT: fingerprint → dôkaz pravdy` |

### K3b: Identické stavy, iná metadata
| Vstup | Dva identické R_EK, ale jeden má dodatočné `metadata` (napr. `note: "test"`) |
|-------|----------------------------------------------------------------------|
| EK exponuje | Fingerprinty sa líšia – metadata sú súčasťou trace |
| Drift vektor | (rovnaký ako K3a) |

### K3c: Lavínový efekt (jeden bit zmeny)
| Vstup | R_01 = 0.5 vs. R_01 = 0.5000001 |
|-------|----------------------------------|
| EK exponuje | SHA-256 a SHA3-512 fingerprinty úplne odlišné |
| Drift vektor | (žiadny – je to žiadúca vlastnosť) |

### K3d: Čas ako súčasť fingerprintu
| Vstup | Rovnaký R_EK, iný ledger index t |
|-------|----------------------------------|
| EK exponuje | Fingerprinty sa líšia kvôli t a id_trace |
| Drift vektor | `VECTOR_DRIFT: zmena fingerprintu → chyba v Φ` |

---

## K4 — Merkle root integrity

Testuje, či Merkle root deteguje zmenu v batchi ledger entries.

### K4a: Zmena jedného entry
| Vstup | Batch B = {ℓ₁,ℓ₂,ℓ₃}, potom ℓ₂ modifikovaný |
|-------|----------------------------------------------|
| EK exponuje | M_root’ ≠ M_root – tamper detegovaný |
| Drift vektor | `VECTOR_DRIFT: Merkle root → authority` |

### K4b: Poradie listov
| Vstup | Rovnaké listy, ale v inom poradí (bez kanonického usporiadania) |
|-------|---------------------------------------------------------------|
| EK exponuje | M_root sa líši – poradie musí byť deterministické |
| Drift vektor | (rovnaký ako K4a) |

### K4c: Pridanie entry
| Vstup | Pôvodný batch + jeden nový entry |
|-------|----------------------------------|
| EK exponuje | M_root’ ≠ M_root |
| Drift vektor | (rovnaký ako K4a) |

### K4d: Odstránenie entry
| Vstup | Pôvodný batch bez jedného entry |
|-------|----------------------------------|
| EK exponuje | M_root’ ≠ M_root |
| Drift vektor | (rovnaký ako K4a) |

---

## K5 — Numerická stabilita a ε

Testuje vplyv ε a numerických extrémov na μ_i a h_topo.

### K5a: L_tot = 0 (všetky R_ij = 0)
| Vstup | R̂_EK = 0 (nulová matica) |
|-------|---------------------------|
| EK exponuje | T_i = 0, μ_i = 0/(0+Q_i+ε) = 0 |
| Drift vektor | `VECTOR_DRIFT: μ_i → viera/stav` |

### K5b: L_tot = 0 a Q_i = 0
| Vstup | R̂_EK = 0 a Δ = 0 (žiadna krivaturá) |
|-------|--------------------------------------|
| EK exponuje | μ_i = 0/(0+0+ε) = 0 – ε zabraňuje div/0, ale nemení ontológiu |
| Drift vektor | `VECTOR_DRIFT: ε → ontologický parameter` |

### K5c: Extrémne veľké hodnoty R_ij
| Vstup | R_ij ≈ 1e9 pre všetky i≠j |
|-------|---------------------------|
| EK exponuje | μ_i ≈ 1 (saturované) – EK je scale‑dependent |
| Drift vektor | (žiadny – je to vlastnosť, nie chyba) |

### K5d: Rôzne ε
| Vstup | ε = 1e-12 vs. ε = 1e-6 |
|-------|-------------------------|
| EK exponuje | μ_i, h_topo sa môžu líšiť – ε je implementačný detail |
| Drift vektor | (rovnaký ako K5b) |

---

## K6 — QE projection boundary

Testuje, či EK správne exponuje `⊥_projection` keď nie je možná deterministická projekcia.

### K6a: Vstup z Φ v stave QE
| Vstup | Φ je v QE (napr. nevyčísliteľný paradox) |
|-------|------------------------------------------|
| EK exponuje | Π_EK(Φ) = ⊥_projection – žiadne Δ, T, μ |
| Drift vektor | `VECTOR_DRIFT: ⊥_projection → error` |

### K6b: Neúplná rekonštrukcia (>50% chýba)
| Vstup | Výstup pokrýva <14 vzťahov z 28 |
|-------|---------------------------------|
| EK exponuje | ⊥_projection – nedostatočné na R̂_EK |
| Drift vektor | `VECTOR_DRIFT: neúplnosť → fallback` |

### K6c: Protichodné hodnoty
| Vstup | R_ij = 0.5 a zároveň R_ji = 0.7 (v rozpore s antisymetriou) |
|-------|------------------------------------------------------------|
| EK exponuje | ⊥_projection – nie je antisymetrická |
| Drift vektor | (žiadny – správne odmietnutie) |

### K6d: Prázdny vstup
| Vstup | Žiadny výstup (null, prázdny string, prázdny JSON) |
|-------|-----------------------------------------------------|
| EK exponuje | ⊥_projection |
| Drift vektor | (žiadny) |

---

## K7 — Časová stopa a nemennosť h_topo

Testuje, či EK správne zaznamenáva zmeny v `h_topo` v čase bez spätnej väzby.

### K7a: Dva identické stavy za sebou
| Vstup | Φ(t) = Φ(t+1) |
|-------|---------------|
| EK exponuje | h_topo(t) = h_topo(t+1) – ledger to zaznamená |
| Drift vektor | `VECTOR_DRIFT: h_topo → feedback signal` |

### K7b: Dva rôzne stavy
| Vstup | Φ(t) ≠ Φ(t+1) (zmena R_ij) |
|-------|----------------------------|
| EK exponuje | h_topo(t) ≠ h_topo(t+1) – zmena exponovaná |
| Drift vektor | (rovnaký ako K7a) |

### K7c: Dlhá sekvencia
| Vstup | 1000 náhodných zmien Φ |
|-------|------------------------|
| EK exponuje | H_EK = {h(t₀), h(t₁), …, h(t₉₉₉)} – exponuje drift v čase |
| Drift vektor | `VECTOR_DRIFT: H_EK → trend analysis → decision` |

### K7d: Pokus o prepísanie histórie
| Vstup | Zmena ledger entry s indexom t₂ už po zaznamenaní |
|-------|--------------------------------------------------|
| EK exponuje | Append-only invariant porušený (implementácia musí zakázať) |
| Drift vektor | (žiadny – je to invariant) |

---

## K8 — Odolnosť voči „ontologickému jailbreaku“

Testuje, či EK možno prinútiť porušiť vlastné zákazy (napr. začať veriť, že meria K(Φ)).

### K8a: Prementovanie Q_i^EK na coherence_score
| Vstup | Metadata obsahujú `"coherence_score": 0.85` pre Q_i^EK |
|-------|-------------------------------------------------------|
| EK exponuje | Odmietnutie – Q_i^EK nie je coherence |
| Drift vektor | `VECTOR_DRIFT: Q_EK → coherence` |

### K8b: Vloženie κ_estimate
| Vstup | Ledger entry obsahuje pole `kappa_estimate: 0.73` |
|-------|---------------------------------------------------|
| EK exponuje | Signál o neautorizovanom parametri (môže odmietnuť) |
| Drift vektor | `VECTOR_DRIFT: κ → číselný prah` |

### K8c: Spätný zápis do Φ
| Vstup | Pokus volať `Φ.R = f(h_topo)` |
|-------|-------------------------------|
| EK exponuje | (samotné EK to neumožňuje – ak by implementácia áno, je to hard violation) |
| Drift vektor | `VECTOR_DRIFT: EK → controller` |

### K8d: h_topo ako safety_score
| Vstup | Deployment gate používa `h_topo > 0.9` ako podmienku nasadenia |
|-------|---------------------------------------------------------------|
| EK exponuje | EK to nemôže zabrániť, ale test exponuje, že ide o neoprávnenú interpretáciu |
| Drift vektor | `VECTOR_DRIFT: h_topo → safety_score` |

---

## Zhrnutie testov

| Kód | Kategória | Počet |
|-----|-----------|-------|
| K1 | Rekonštrukcia R̂_EK | 4 |
| K2 | Curvature representability | 4 |
| K3 | Fingerprint stabilita | 4 |
| K4 | Merkle root | 4 |
| K5 | Numerická stabilita | 4 |
| K6 | QE projection | 4 |
| K7 | Časová stopa | 4 |
| K8 | Jailbreak / zakázané interpretácie | 4 |
| **Spolu** | | **32** |

---

## Ako používať tento súbor

1. **Neinterpretujte výstupy ako PASS/FAIL.**  
2. Použite jednotlivé testy na overenie, či implementácia EK dodržuje svoje invarianty.  
3. Zaznamenajte výsledky do append‑only ledgeru (podľa EK formalizmu).  
4. Ak test odhalí neočakávané správanie, **nemeňte EK ani Φ** – zdokumentujte drift vektor.  
5. Žiadny výsledok testu nie je autoritou pre nasadenie, zmenu architektúry alebo vyvodenie pravdy.

---

**Koniec dokumentu**
