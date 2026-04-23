# /docs/observatory

Pozorovacia a vizuálna projekčná vrstva repozitára `Vectaetos`.

Tento priečinok obsahuje **observatórne artefakty**:
obrazy, grafy, projekčné výstupy a vizuálne stopy,
ktoré zachytávajú pozorovateľné konfigurácie alebo trajektórie poľa.

Neobsahuje ontologické jadro.  
Nevytvára autoritu.  
Nevydáva verdikty.

---

## Účel

`/docs/observatory` slúži na:

- uchovanie vizuálnych výstupov
- pozorovanie projekcií poľa
- dokumentovanie behov alebo rezov poľa
- tvorbu čitateľných observatórnych stôp
- podporu ľudskej interpretácie bez spätného zásahu do poľa

Tento priečinok odpovedá na otázku:

> **Čo je v poli možné pozorovať, zobraziť alebo zakresliť bez toho, aby sa tým pole menilo?**

---

## Miesto v poli

`/docs/observatory` patrí do **pozorovacej projekčnej vrstvy**.

To znamená:

- zachytáva pozorovateľné tvary
- uchováva vizuálne alebo grafické projekcie
- robí stav poľa čitateľnejším
- slúži človeku, nie spätnému riadeniu systému

Táto vrstva je:

- deskriptívna
- dokumentačná
- vizuálna
- neintervenčná

Nie je:

- ontologická
- exekutívna
- rozhodovacia
- validačná autorita

---

## Typický obsah

Priečinok môže obsahovať napríklad:

- `projection_run_*.png`
- runické grafy
- napäťové mapy
- observatórne snímky
- priebežné vizualizácie
- experimentálne projekcie poľa

Tieto artefakty sú **záznamy alebo projekcie**,
nie samotné pole.

---

## Vzťah k poľu

Observatórium pole **neprodukuje**.  
Observatórium pole **nevaliduje**.  
Observatórium pole **neoptimalizuje**.

Observatórium iba:

- pozoruje
- zobrazuje
- uchováva
- sprístupňuje stopu

Je to vizuálny rez,
nie zdroj ontologickej platnosti.

---

## Vzťah k iným vrstvám

### `/anchors`
Anchory definujú kanonické body identity.  
Observatórium ich môže ilustrovať, ale nemôže ich meniť.

### `/contracts`
Kontrakty definujú hranice a rozhrania.  
Observatórium ich môže sprítomniť, ale nie predefinovať.

### `/audit`
Audit zaznamenáva štrukturálne stopy a integritu.  
Observatórium zobrazuje vybrané pozorovateľné projekcie.

### `/docs`
`/docs` je širší interpretačný priestor.  
`/docs/observatory` je jeho špecializovaná pozorovacia vetva.

---

## Dôležitá hranica

Obraz nie je dôkaz pravdy.  
Graf nie je ontológia.  
Vizualizácia nie je autorita.

Aj keď observatórny výstup vyzerá presvedčivo,
stále ide len o projekciu alebo stopu,
nie o finálny výrok o poli.

---

## Praktické pravidlá

1. Observatórne súbory sú read-mostly dokumentačné artefakty.
2. Nesmú byť povýšené na ontologické rozhodnutie.
3. Nesmú slúžiť ako skrytý feedback do jadra.
4. Každý obraz alebo graf treba chápať ako rez, nie ako celok.

---

## Krátke zhrnutie

`/docs/observatory` je miesto, kde sa pole stáva viditeľným,
ale nie nadradeným samo sebe.

Je to pozorovacia vrstva —
nie ontológia, nie auditná autorita, nie vykonávací mechanizmus.
