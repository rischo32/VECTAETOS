# VECTAETOS — WEB_DATA_SOURCES

## Status
Canonical  
Restrictive  
Non-operational  
Epistemically bounded  

---

## 1. Účel dokumentu

Tento dokument definuje **jediné prípustné zdroje dát**,  
ktoré môže verejný webový artefakt VECTAETOSU používať.

Cieľom nie je maximalizovať informácie,  
ale **zachovať ontologickú integritu projekcie poľa Φ**.

Akýkoľvek zdroj dát mimo tejto špecifikácie
je **neprípustný**.

---

## 2. Základná zásada

> Web nesmie vedieť viac, než je dovolené vidieť.

Web **nečíta realitu**.  
Web **nečíta používateľa**.  
Web **nečíta význam**.

Web číta **iba projekciu**.

---

## 3. Povolené dátové zdroje

### 3.1 Statické kanonické artefakty

Web môže čítať výlučne tieto typy dát:

- kanonické `.md` dokumenty repozitára
- statické konfiguračné súbory
- verejne exportované snapshoty projekcie
- vizualizačné parametre (farba, poloha, intenzita)

Tieto dáta sú:

- nemenné v rámci verzie
- neosobné
- neinteraktívne
- neodvodené zo správania používateľa

---

### 3.2 Projekčné snapshoty poľa

Ak je prítomný Simulation Vortex:

- web môže čítať **iba jeho výstup**
- nikdy nie jeho vnútorný stav
- nikdy nie jeho parametre
- nikdy nie jeho trajektórie v čase

Prípustné sú iba:

- anonymné
- agregované
- jednorazové projekčné stavy

---

### 3.3 Lokálne session parametre

Web môže používať **dočasné lokálne hodnoty**:

- poloha kamery
- čas od otvorenia stránky
- jednorazový stav 3Gate

Tieto hodnoty:

- sa neukladajú
- sa neodosielajú
- sa neporovnávajú
- zanikajú pri zatvorení stránky

---

## 4. Výslovne zakázané zdroje dát

Web NESMIE používať:

- cookies
- localStorage
- sessionStorage
- fingerprinting
- IP adresy
- user-agent analýzu
- behaviorálne logy
- heatmapy
- A/B testy
- analytické skripty
- externé trackery

Web NESMIE:

- volať API s osobnými dátami
- zapisovať vstupy používateľa
- pamätať si otázky
- porovnávať návštevy

---

## 5. Vzťah k otázkam používateľa

Otázka používateľa:

- nie je uložená
- nie je analyzovaná mimo session
- nie je spätne dostupná
- nie je korelovaná

Otázka existuje **iba ako okamžitý epistemický impulz**  
a zaniká spolu s projekciou.

---

## 6. Žiadna spätná väzba

Web:

- nesleduje reakcie
- nemeria úspech
- nehodnotí pochopenie
- nezlepšuje projekciu

Ak by web reagoval na minulé správanie,
stal by sa **adaptívnym systémom**.

To je neprípustné.

---

## 7. Vzťah k GDPR a ochrane súkromia

Vectaetos web:

- nespracúva osobné údaje
- nevytvára identitu
- nevytvára profil
- nevytvára históriu

Z hľadiska GDPR:

- neexistuje prevádzkovateľ osobných dát
- neexistuje spracúvanie
- neexistuje uchovávanie

Ticho je forma ochrany.

---

## 8. Offline existencia

Ak by web:

- stratil pripojenie
- stratil backend
- stratil dátový zdroj

vizualizácia môže:

- pokračovať staticky
- zostať tichá
- zostať prázdna

To **nie je chyba**.

Je to ontologicky korektný stav.

---

## 9. Kanonická veta dátového režimu

> To, čo vidíš, nie je zbierané.  
> Je to dovolené.

---

## 10. Záver

Web VECTAETOSU:

- nie je dátový systém
- nie je observačný nástroj
- nie je analytická platforma

Je to **projekčný povrch poľa Φ**  
s minimálnym možným tokom informácií.

Všetko navyše je hrozba.

---

© VECTAETOS  
Canonical repository artifact
