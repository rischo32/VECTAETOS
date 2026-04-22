# /config

Konfiguračný priečinok repozitára.

Tento priečinok obsahuje **runtime konfiguráciu** pre procedurálne správanie systému.  
Neobsahuje ontológiu, neobsahuje axiomatické jadro a nevytvára autoritu nad `VECTAETOS`.

---

## Účel

`/config` slúži na ukladanie **nastaviteľných parametrov vykonania**, najmä pre:

- simuláciu
- výstupné súbory
- registry logovanie
- synchronizačné uzly
- bezpečnostné prepínače

Tieto konfigurácie určujú **ako** sa systém spúšťa,  
nie **čo je ontologicky pravdivé**.

---

## Aktuálny obsah

```
/config
└── default.yaml
