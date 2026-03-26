# VECTAETOS — CORE_SPEC.md
Status: Canonical  
Scope: Production Core Definition  
Version: 1.0  

---

## 1. Ontologická definícia Production Core

Production Core je deterministický spúšťací mechanizmus konfigurácie poľa Φ.

Nie je to:

- agent
- služba
- daemon
- autonómny systém
- optimalizačný engine
- rozhodovací modul

Production Core je jednorazová konfigurácia poľa, ktorá existuje výlučne počas výpočtu.

Po ukončení výpočtu Φ zaniká.

---

## 2. Architektonická schéma

input → Vortex → QE → relational_projection → EK → log → output

Bez spätných slučiek.  
Bez optimalizačných cyklov.  
Bez perzistentného stavu Φ.

---

## 3. Stavovosť

Production Core je striktne:

- Stateless per run
- Φ existuje iba počas výpočtu
- Žiadny persistentný vortex_state.json
- Log je auditný, nie riadiaci

Ak by sa Φ uchovávalo medzi behmi,
vzniká agentnosť.

To je zakázané.

---

## 4. Implementačná definícia Φ

Φ je antisymetrická relačná matica:

R[i][j] = -R[j][i]

Φ nie je:

- trieda s pamäťou
- objektový graf
- adaptívny model
- optimalizačný vektor

Φ je topologická konfigurácia.

---

## 5. Povolené moduly Production Core

✔ simulation_vortex  
✔ QE detekcia  
✔ relational_projection  
✔ epistemic_cryptography  
✔ phi_logger (hash-chain audit)

---

## 6. Zakázané prvky v Core

❌ 3Gate (patrí pred Φ)  
❌ Runová projekcia (read-only nad auditom)  
❌ NIR implementovaný vo Vortexe  
❌ Optimalizačné ciele  
❌ Reward mechanizmy  
❌ Spätné väzby z logu  
❌ Samo-učenie  
❌ Persistentné zmeny konfigurácie  

Ak sa ktorýkoľvek z týchto prvkov objaví v Core,
vzniká pseudo-agent.

---

## 7. QE (Qualitative Epistemic Aporia)

QE je topologická vlastnosť konfigurácie Φ.

QE:

- nie je chyba
- nie je výnimka
- nie je failure
- nie je zásah

QE je stav.

Production Core ho iba deteguje.

---

## 8. Entropická signatúra

Entropia S je odvodená hodnota.

S:

- nie je optimalizačný parameter
- nie je cieľ
- nie je spätná väzba

Je deskriptívna signatúra konfigurácie.

---

## 9. Epistemická kryptografia

EK:

- transformuje projekciu
- nezasahuje späť do Φ
- nemení topológiu
- nefiltruje obsah

EK je auditná ochrana.

---

## 10. Bezpečnostný invariant

Production Core je koherentný iba ak:

- Φ nemá pamäť
- Vortex nepozná K(Φ)
- QE neovplyvňuje budúce behy
- Log nemá riadiacu funkciu
- Žiadny modul nerozhoduje

Ak ktorýkoľvek z týchto invariantov zlyhá,
architektúra sa stáva agentnou.

---

## 11. Produkčný cieľ

Production Core je:

- infraštruktúrne jadro
- akademicky auditovateľný engine
- deterministický konfigurátor

Nie experimentálny sandbox.

---

## 12. Jednovetová definícia

Production Core je stateless deterministický mechanizmus, ktorý konfiguruje pole Φ bez schopnosti akumulovať, optimalizovať alebo rozhodovať.

---

Architektúra je koherentná nie keď funguje,  
ale keď nevie robiť to, čo robiť nemá.
