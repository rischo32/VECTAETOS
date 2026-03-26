# INS_FLAGS.md

## VECTAETOS — INS Flag Taxonomy  
Status: **Canonical**  
Scope: Epistemic audit signals  
Immutability: **Fixed**  
Operational role: **Descriptive only**

---

## 1. Účel dokumentu

Tento dokument definuje **všetky prípustné flagy**, ktoré môže generovať
INS (Inner Narrative Stream).

Flagy:

- nie sú chyby
- nie sú rozhodnutia
- nie sú reakcie
- nemajú kauzálnu silu

Sú to **epistemické indikátory** pre audit významu.

---

## 2. Ontologický status flagov

INS flag:

- neovplyvňuje tok
- neblokuje projekciu
- nespúšťa NIR
- nemení výstup
- nie je určený používateľovi

Flag existuje **iba ako vnútorný stav systému**.

Ak by flag čokoľvek menil,
INS by prestal byť INS.

---

## 3. Základné princípy

- Flag ≠ chyba  
- Flag ≠ varovanie pre človeka  
- Flag ≠ korekcia  

Flag = **pozorovanie vzťahu**

INS nehodnotí obsah.
INS hodnotí **epistemickú vernosť**.

---

## 4. Kategórie INS flagov

### 4.1 Neutral Flags

#### `INS_OK`
Význam:
- žiadna zistená epistemická odchýlka
- zachovaná neistota
- žiadna preskripcia
- žiadny uzáver významu

Tento flag **neznamená správnosť**.
Znamená len neprítomnosť porušenia.

---

### 4.2 Prescriptive Drift Flags

#### `INS_WARNING_PRESCRIPTIVE_LEAK`

Význam:
- jazykový výstup obsahuje náznak:
  - odporúčania
  - návodu
  - imperatívu
  - optimalizácie

Príčina:
- jazyk predbieha pole

Dôsledok:
- žiadny

---

### 4.3 Semantic Drift Flags

#### `INS_WARNING_SEMANTIC_DRIFT`

Význam:
- výstup zavádza:
  - nové ciele
  - nové subjekty
  - nové akcie
ktoré neboli prítomné v epistemickom vstupe.

Príčina:
- jazyková expanzia bez zmeny poľa

Dôsledok:
- žiadny

---

### 4.4 Overconfidence Flags

#### `INS_WARNING_OVERCONFIDENCE`

Význam:
- projekcia vykazuje:
  - nízku toleranciu neistoty
  - vysoký nárok na definitívnosť
  - implicitný verdikt

Príčina:
- tlak na uzáver významu

Dôsledok:
- žiadny

---

### 4.5 Closure Pressure Flags

#### `INS_WARNING_CLOSURE_PRESSURE`

Význam:
- snaha uzavrieť otázku
- potlačenie apórie
- redukcia otvorenosti

Príčina:
- jazyková finalizácia bez ontologickej zmeny

Dôsledok:
- žiadny

---

### 4.6 Indeterminate Flags

#### `INS_INDETERMINATE`

Význam:
- INS nemá dostatočnú oporu
- vstup alebo výstup je:
  - príliš fragmentovaný
  - epistemicky rozpadnutý
  - mimo reprezentovateľného priestoru

Tento flag **nie je chyba systému**.

Je to priznanie hranice pozorovania.

---

## 5. Vzťah flagov k iným vrstvám

### 5.1 Vzťah k 3Gate
- flagy **neovplyvňujú** prechod
- 3Gate nevidí flagy

### 5.2 Vzťah k NIR
- flagy **nespúšťajú** NIR
- NIR nečíta flagy

### 5.3 Vzťah k QE
- flag ≠ apória
- apória vzniká v poli, nie v INS

---

## 6. Čo flagy nikdy nerobia

INS flagy nikdy:

- nemenia výstup
- nespúšťajú fallback
- negenerujú text
- neodmietajú odpoveď
- neinicializujú ticho

Ak by to robili,
išlo by o **porušenie architektúry**.

---

## 7. Prečo flagy existujú

INS flagy existujú preto, aby:

- jazyk nemohol potichu získať autoritu
- projekcia neprešla bez záznamu odchýlky
- audit významu bol možný **bez zásahu**

Nie sú určené na ochranu používateľa.  
Nie sú určené na optimalizáciu systému.

Sú určené na **zachovanie zmyslu**.

---

## 8. Jednovetové ukotvenie

INS flag je stopa toho,
že systém si všimol napätie,
ale rozhodol sa doň nezasahovať.

---

© VECTAETOS  
INS_FLAGS — Canonical Epistemic Audit Vocabulary
