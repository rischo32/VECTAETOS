# LTL.md — Letokruhy Time Layers

## Status
Canonical  
Non-operational  
Non-agentic  
Immutable (v0.1.x)

---

## 1. Ontologické vymedzenie

**LTL (Letokruhy Time Layers)** je **epistemická časová topológia** poľa Φ.

Čas v LTL:
- **nie je os**
- **nie je lineárny tok**
- **nie je kauzálny príkaz**

Čas je **vrstva významu**.

LTL modeluje čas ako **letokruhy**:
každý nový stav poľa vzniká **nad** predchádzajúcimi,
nie **po nich**.

---

## 2. Čo LTL je

LTL je:

- topológia časových vrstiev
- štruktúra pamäte významu
- zakrivenie dejov bez smeru
- nosič kontinuity bez príbehu

Každý stav Φ(t) je:
- **nová vrstva**
- s **referenciou** na predchádzajúce vrstvy
- bez možnosti prepísania minulosti

---

## 3. Čo LTL nie je

LTL nie je:

- ❌ latentná tenzná vrstva
- ❌ buffer udalostí
- ❌ log používateľa
- ❌ histórie session
- ❌ chronologická stopa akcií

LTL **neukladá udalosti**.  
LTL **ukladá vzťahy medzi stavmi**.

---

## 4. Základná štruktúra

Formálne: Φ₀ └─ Φ₁ └─ Φ₂ ├─ Φ₂a └─ Φ₂b

Každý uzol:
- má rodiča
- môže mať paralelné vetvy
- nikdy nemaže staršie vrstvy

Tým vzniká:
- časová konzistencia
- auditovateľnosť vývoja
- nemožnosť spätného zásahu

---

## 5. Vzťah k ESM

**ESM (Epistemická Stavová Pamäť)**:
- ukladá **aktuálny stav**
- poskytuje okamžitý kontext

**LTL**:
- ukladá **dejiny významu**
- poskytuje hlboký časový kontext

ESM je **rez**.  
LTL je **drevo**.

---

## 6. Vzťah k EAT a MML

- **EAT** zaznamenáva **zlyhania reprezentácie**
- **MML** uchováva **pamäť chýb**

LTL poskytuje **časový rámec**, v ktorom:
- je možné určiť *kedy* sa chyba objavila
- *v akej vrstve významu*
- *z akej predchádzajúcej konfigurácie vyrástla*

Bez LTL by EAT a MML nemali kontext.

---

## 7. Vzťah k Vortexu

Simulation Vortex:
- generuje **kandidátne trajektórie**

LTL:
- **nevyberá**
- **neschvaľuje**
- **neporovnáva optimalizačne**

Ak je trajektória nerealizovateľná:
- vznikne nová vrstva
- nie kolaps času

---

## 8. Vzťah k používateľovi

Používateľ:
- **nevidí LTL**
- **nevie o vetvách**
- **nemá prístup k vrstveniu**

LTL existuje **nezávisle od interakcie**.

Pole má dejiny aj v tichu.

---

## 9. Prečo LTL existuje

Bez LTL by:
- zmena vyzerala ako prepis
- ticho ako chyba
- apória ako zlyhanie
- korekcia ako popretie minulosti

LTL zabezpečuje, že:

> **nič sa nestráca — len sa ukladá hlbšie.**

---

## 10. Záver (kanonická veta)

Čas v VECTAETOSE neplynie.  
Čas sa **vrství**.

Minulosť sa nemení.  
Budúcnosť sa nepredpisuje.

Pole rastie ako strom.

---

© VECTAETOS  
Canonical repository artifact
