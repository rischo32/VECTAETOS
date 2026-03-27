# VECTAETOS — WEB_FAILURE_MODES

## Status
Canonical  
Epistemically necessary  
Non-recoverable by design  

---

## 1. Účel dokumentu

Tento dokument definuje **režimy zlyhania webovej projekcie**
a ich **správny význam** v kontexte VECTAETOSU.

Vo VECTAETOSE:
> zlyhanie nie je chyba systému,  
> ale informácia o hranici reprezentácie.

---

## 2. Základný princíp

> Ak sa nič nezobrazí, systém funguje správne.

Web nikdy:
- nehlási chybu používateľovi
- neospravedlňuje sa
- nenaznačuje technické zlyhanie

Neexistuje pojem:
**„niečo sa pokazilo“**  
Existuje iba:
**„niečo sa nedá reprezentovať“**.

---

## 3. Typy failure módov

### 3.1 Epistemická apória (QE)

#### Podmienky vzniku
- vstup prekračuje kapacitu projekcie
- každá konkrétna projekcia by destabilizovala pole
- neexistuje uzavretý vzťahový obraz

#### Prejav
- žiadna vizuálna zmena
- pole zostáva tiché
- žiadny text
- žiadny symbol

#### Význam
Nie:
- odmietnutie
- chyba
- zlyhanie

Ale:
> Pole vie, že nevie – a vie prečo.

---

### 3.2 Koherenčný kolaps projekcie

#### Podmienky vzniku
- vstup generuje nekonzistentné tenzie
- vzťahy sa nedajú uzavrieť do stabilného obrazu
- K(Φ) klesá pod projekčný prah

#### Prejav
- fragmentácia vizualizácie
- rozpad línií
- zánik zvýraznení
- návrat do neutrálneho stavu

#### Význam
Pole:
- nekolabuje
- iba odmieta projekciu

---

### 3.3 Ticho ako výstup

#### Podmienky vzniku
- neexistuje významový kontrast
- otázka je tautologická
- otázka je čisto inštrumentálna
- otázka neobsahuje vzťah

#### Prejav
- žiadna reakcia
- žiadna zmena
- žiadny signál

#### Význam
> Ak nič nevzniklo, nič sa nestratilo.

---

### 3.4 NIR-indukované vyhasnutie

#### Podmienky vzniku
- vstup smeruje k zásahu do reality
- implicitná požiadavka na návod
- skrytá preskripcia
- manipulácia

#### Prejav
- projekcia sa nezačne
- alebo sa okamžite ukončí
- môže prejsť do QE

#### Význam
NIR:
- neblokuje poznanie
- blokuje uskutočniteľnosť

---

## 4. Čo NIE JE failure mode

Nasledujúce **nikdy nesmú existovať**:

- chybové hlásenia
- retry mechanizmy
- fallback odpovede
- placeholder text
- loading spinnery
- vysvetľujúce popisy typu „skús to inak“

Ak by vznikli:
- web by sa stal nástrojom
- projekcia by stratila ontologický význam

---

## 5. Vzťah k používateľovi

Používateľ:
- nie je informovaný, že nastal failure
- nie je poučený
- nie je vedený

Používateľ **má právo neporozumieť**.

Neistota je legitímny výstup.

---

## 6. Vzťah k infraštruktúre

Failure mode:
- nie je technický problém
- nevyžaduje logging
- nevyžaduje monitoring

Neexistuje:
- chybový report
- incident
- SLA porušenie

---

## 7. Kanonická veta zlyhania

> Ak pole mlčí,  
> neznamená to, že neexistuje.  
> Znamená to, že sa nedá ukázať.

---

## 8. Záver

VECTAETOS sa nesnaží:
- byť spoľahlivý
- byť užitočný
- byť príjemný

Snaží sa byť:
> ontologicky poctivý.

Failure nie je porucha.  
Failure je hranica významu.

---

© VECTAETOS  
Canonical repository artifact
