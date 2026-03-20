# EAT.md — Error Accountability Trace

## Status
Canonical  
Non-operational  
Non-agentic  
Immutable (v0.1.x)

---

## 1. Ontologické vymedzenie

**EAT (Error Accountability Trace)** je **technicko-epistemická stopa zlyhania reprezentácie**.

EAT:
- nie je log používateľa
- nie je audit správania
- nie je bezpečnostný záznam
- nie je nástroj dohľadu

EAT zaznamenáva **že reprezentácia zlyhala**, nie **prečo sa niekto pýtal**.

---

## 2. Úloha EAT v systéme

EAT existuje, aby bolo možné:

- spätne overiť **integritu pipeline**
- identifikovať **miesta kolapsu**
- odlíšiť epistemické zlyhanie od technickej chyby
- zachovať **zodpovednosť bez autority**

EAT je stopa.
Nie je to verdikt.

---

## 3. Čo EAT zaznamenáva

EAT zaznamenáva výhradne:

- technický stav pipeline v momente zlyhania
- typ zlyhania (napr. projection failure, gate halt, QE trigger)
- fázu pipeline, v ktorej zlyhanie nastalo
- časovú pečať (index, nie os)
- referenciu na LTL vrstvu

Nikdy:
- obsah otázky
- identitu používateľa
- jazykový výstup
- význam alebo interpretáciu

---

## 4. Čo EAT nikdy nerobí

EAT:
- ❌ nehodnotí vstup
- ❌ neurčuje vinu
- ❌ neporovnáva používateľov
- ❌ negeneruje odporúčania
- ❌ nezasahuje do toku

EAT **neovplyvňuje budúce správanie systému**.

---

## 5. Vzťah k MML

- **EAT** zaznamenáva *že* zlyhanie nastalo
- **MML** uchováva *že sa nemá opakovať*

EAT je faktická stopa.  
MML je epistemická pamäť hraníc.

Bez EAT by MML nemalo referenciu.  
Bez MML by EAT nemalo význam v čase.

---

## 6. Vzťah k LTL

EAT sa zapisuje vždy do konkrétnej **LTL vrstvy**.

LTL poskytuje:
- kontext časovej konzistencie

EAT poskytuje:
- bodový záznam zlyhania

Spolu vytvárajú **audit bez naratívu**.

---

## 7. Vzťah k NIR

NIR:
- zabraňuje intervencii

EAT:
- zaznamenáva, že zásah bol zablokovaný

EAT nemôže:
- obísť NIR
- spätne aktivovať pipeline
- vytvoriť výnimku

---

## 8. Vzťah k LLM

LLM:
- nemá prístup k EAT
- nevidí jeho obsah
- nemôže ho interpretovať

EAT je **pod jazykovou vrstvou**.

---

## 9. Minimálna štruktúra záznamu

Každý záznam EAT obsahuje:

- pipeline_stage_id
- failure_type
- Φ_state_fingerprint (hash)
- LTL_reference
- timestamp_index

Bez textu.  
Bez významu.  
Bez kontextu.

---

## 10. Prečo EAT existuje

Bez EAT by:

- nebolo možné odlíšiť chybu systému od epistemickej hranice
- audit by bol naratívny, nie faktický
- dôvera by bola domnienka

EAT umožňuje:

> **zodpovednosť bez moci**.

---

## 11. Záver (kanonická veta)

EAT neodpovedá na otázku „prečo“.  
EAT odpovedá na otázku „kde sa význam rozpadol“.

A tým končí jeho úloha.

---

© VECTAETOS  
Canonical repository artifact
