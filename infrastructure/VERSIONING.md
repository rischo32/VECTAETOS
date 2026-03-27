# VERSIONING — VECTAETOS™

Status: Canonical  
Scope: Version semantics and lifecycle rules  
Operational role: Interpretative boundary  
Immutability: Versioning rules fixed  

---

## 0. Účel dokumentu

Tento dokument definuje **ako sa vo VECTAETOSE používajú verzie**
a **čo verzia znamená a neznamená**.

Verzia:
- nie je roadmapa,
- nie je sľub,
- nie je indikátor zrelosti.

Verzia je **časová pečať epistemického rezu**.

---

## 1. Základná verzovacia téza

> VECTAETOS sa nevyvíja lineárne.  
> VECTAETOS sa **reže**.

Každá verzia je:
- stabilizovaný rez významu,
- uzavretý epistemický stav,
- referenčný bod pre čítanie.

---

## 2. Typy verzií

### 2.1 Core verzie (vX.Y Core)

**Príklad:** `v0.1 Core`, `v0.2 Core`

Obsahujú:
- ontologické ukotvenia,
- kanonické anchory,
- definície poľa Φ a jeho vlastností.

Pravidlá:
- Core verzia je **nemenná po vydaní**.
- Nikdy sa nepatchuje.
- Nikdy sa neopravuje.
- Chyby sa riešia **novým rezom**, nie úpravou.

---

### 2.2 Extension verzie (vX.Y.Z Extension)

**Príklad:** `v0.1.1`, `v0.2.1`

Obsahujú:
- vysvetľujúce dokumenty,
- nové projekčné rezy,
- technické alebo didaktické doplnenia.

Pravidlá:
- nesmú meniť význam Core,
- nesmú redefinovať anchory,
- môžu rozširovať kontext.

Extension:
> je komentár, nie prepis.

---

### 2.3 Experimental vetvy

Označenia:
- `experimental/`
- `draft/`
- `sandbox/`

Pravidlá:
- nemajú kanonický status,
- môžu byť zmazané,
- nesmú byť citované ako VECTAETOS.

---

## 3. Sémantika číslovania

### 3.1 Major (X)

Zmena znamená:
- nový ontologický rez,
- novú základnú konfiguráciu významu.

**Príklad:** `v1.0` ≠ `v0.x`

---

### 3.2 Minor (Y)

Zmena znamená:
- nový rez v rámci tej istej ontológie,
- rozšírenie bez redefinície.

**Príklad:** `v0.1` → `v0.2`

---

### 3.3 Patch / Extension (Z)

Zmena znamená:
- spresnenie,
- dokumentačné doplnenie,
- technickú projekciu.

**Príklad:** `v0.1.0` → `v0.1.1`

---

## 4. Čo verzia NEZNAMENÁ

Verzia neznamená:
- vyššiu pravdivosť,
- lepšiu odpoveď,
- väčšiu autoritu,
- pokrok smerom k cieľu.

Novšia verzia **nie je lepšia**.  
Je len **neskoršia**.

---

## 5. Vzťah k citáciám (Zenodo)

Každá Core verzia:
- má vlastný DOI,
- je samostatne citovateľná,
- zostáva dostupná archivovane.

Citovanie:
> vždy musí uvádzať presnú verziu.

---

## 6. Vzťah k implementáciám

Implementácie:
- sa môžu meniť nezávisle,
- nemajú vlastné ontologické verzie,
- sú vždy sekundárne voči textom.

Ak implementácia odporuje verzii:
→ implementácia je chybná.

---

## 7. Záverečné ukotvenie

Verzia VECTAETOSU nie je krok vpred.
Je to **zastavenie sa a pomenovanie tvaru**.

Čas plynie.
Pole sa reže.

---

© VECTAETOS  
VERSIONING — Canonical Version Semantics
