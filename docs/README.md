# /docs

Dokumentačná vrstva repozitára `Vectaetos`.

Tento priečinok obsahuje **ľudsky čitateľné mapy, poznámky, diagramy, interpretácie a projekcie**
súvisiace s poľom VECTAETOS™.  
Neobsahuje ontologické jadro, nenahrádza anchor dokumenty a nevytvára autoritu nad poľom.

---

## Účel

`/docs` slúži na:

- vysvetlenie architektúry
- zobrazenie štrukturálnych vzťahov
- publikovanie diagramov a formálnych poznámok
- orientáciu človeka v poli
- dokumentačné premostenie medzi formalizmom a čitateľnosťou

Tento priečinok odpovedá na otázku:

> **Ako je možné pole čítať a mapovať bez toho, aby sa zamieňalo za samotné pole?**

---

## Miesto v poli

`/docs` patrí do **interpretačno-dokumentačnej vrstvy**.

To znamená:

- pomáha človeku čítať štruktúru
- sprístupňuje formu a vzťahy
- môže opisovať pole
- môže vizualizovať pole
- môže uchovávať vysvetlenia

Ale nesmie:

- definovať ontológiu
- meniť axiomatické jadro
- nahrádzať `/anchors`
- nahrádzať `/contracts`
- vystupovať ako zdroj pravdy poľa

---

## Vzťah k ostatným priečinkom

### `/anchors`
Obsahuje kanonické anchor dokumenty.  
Ak vznikne konflikt medzi `/docs` a `/anchors`, prednosť majú vždy `/anchors`.

### `/contracts`
Obsahuje exportované hranice a rozhrania pre downstream vrstvy.  
`/docs` ich môže vysvetľovať, ale nemôže ich meniť.

### `/audit`
Audit zaznamenáva a pozoruje.  
`/docs` interpretuje a sprístupňuje človeku.

### `/docs/observatory`
Podpriečinok určený pre pozorovacie výstupy, vizuálne projekcie a observatórne artefakty.

---

## Aktuálny charakter obsahu

Tento priečinok môže obsahovať napríklad:

- systémové mapy
- architektonické náčrty
- relačnú geometriu
- bezpečnostné interpretácie
- poznámky k so(8)
- diagramy poľa
- observatórne výstupy
  ___
      aktualny docs/VECTAETOS — METAMATEMATICKÝ ANCHOR.pdf je starší, a plaťí novší, a to v /anchors
  ___

### Jednotný architektonický diagram

[`UNIFIED_ARCHITECTURE.md`](./UNIFIED_ARCHITECTURE.md) konsoliduje všetky existujúce mapy
(`ARCHITECTURE.md`, `MAPARCH.md`, `VECTAETOS_SYSTEM_MAP.md`, `VECTAETOS_FIELD_DIAGRAM.md`,
`arch_pipe.md`) do jedného pohľadu, ktorý zobrazuje nielen povrchový pipeline, ale aj
**hĺbku vrstiev** (L0 → L10), **Δ / so(8) štrukturálny skelet**, **triadickú hranicu**
s ASIMULATOR / ASI_MOD, a **CI ontology guards**. Predrenderované obrázky sú
v [`unified_architecture/`](./unified_architecture/).

Tieto súbory majú **deskriptívny alebo interpretačný charakter**.  
Nie sú to exekutívne ani ontologicky nadradené dokumenty.

---

## Dôležitá hranica

Dokumentácia nie je pole.  
Mapa nie je ontológia.  
Diagram nie je realizovateľnosť.

Preto všetko v `/docs` treba čítať ako:

- pomoc pri orientácii
- vysvetľujúcu projekciu
- dokumentačný rez poľa

nie ako finálny zdroj rozhodnutia.

---

## Praktické pravidlá

1. `/docs` môže vysvetľovať, ale nesmie vládnuť.
2. `/docs` môže interpretovať, ale nesmie definovať jadro.
3. `/docs` môže byť bohaté, ale nesmie porušiť vrstvy.
4. Pri kolízii má prioritu:
   - `/anchors`
   - potom `/contracts`
   - až potom `/docs`

---

## Krátke zhrnutie

`/docs` je priestor, kde sa pole stáva čitateľným pre človeka.  
Je to dokumentačná a interpretačná vrstva — nie ontologická autorita.
