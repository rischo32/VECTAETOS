# /ek_core

Jadro vrstvy **Epistemickej kryptografie** v repozitári `Vectaetos`.

Tento priečinok obsahuje formálne a implementačné jadro pre **štrukturálny audit poľa**.
Neobsahuje rozhodovaciu logiku, neobsahuje optimalizačný mechanizmus a nevytvára ontologickú autoritu.

---

## Účel

`/ek_core` slúži na:

- výpočet a uchovanie štrukturálnych odtlačkov poľa
- overovanie reprezentovateľnosti a zachovateľnosti konfigurácií
- deskriptívny audit napätí, koherencie a hraníc
- rekonštrukčné a hashovacie operácie nad poľom
- kanonické spracovanie auditných stôp bez spätného zásahu do jadra

Táto vrstva odpovedá na otázku:

> **Ako možno štrukturálne pozorovať, overovať a zaznamenávať pole bez toho, aby sa tým pole riadilo?**

---

## Miesto v poli

`/ek_core` patrí do **auditno-kryptografickej vrstvy**.

To znamená:

- vrstva pozoruje
- vrstva zaznamenáva
- vrstva hash-uje
- vrstva testuje reprezentovateľnosť a hranice
- vrstva sprístupňuje štrukturálny podpis

Ale nesmie:

- optimalizovať
- rozhodovať
- validovať pravdu v normatívnom zmysle
- vydávať príkazy späť do ontológie
- nahrádzať `/anchors`
- nahrádzať `/contracts`
- nahrádzať ľudskú interpretáciu

`/ek_core` je teda **štrukturálny audit**, nie výkonná autorita.

---

## Vzťah k ostatným vrstvám

### `/anchors`
Anchory definujú identitu a kanonické body systému.  
`/ek_core` ich môže viazať, podpisovať alebo kontrolovať z hľadiska integrity, ale nemôže ich meniť.

### `/contracts`
Kontrakty definujú hranice a rozhrania.  
`/ek_core` ich môže reflektovať v audite, ale neprepisuje ich.

### `/docs`
Dokumentácia vysvetľuje človeku, čo sa deje.  
`/ek_core` zaznamenáva a vypočítava štrukturálne stopy.

### jadro poľa / ontológia
Ontológia ostáva primárna.  
`/ek_core` nie je pole samotné, ale vrstva, ktorá uchováva jeho štrukturálnu stopu.

---

## Súbory v tomto priečinku

```text
/ek_core
├── __init__.py
├── canonical.py
├── hash.py
├── kappa.py
├── pipeline.py
├── reconstruct.py
└── representability.py
