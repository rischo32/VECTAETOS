# Historické pozadie a slovenské korene Vectaetos

## Kontext úlohy
Vypracované pre interný výskum tímu Lab Φ: zmapovať historické pozadie autora (Richard Fonfára) a pôvod Vectaetos v slovenskom technicko‑filozofickom prostredí.

---

## 1) Executive summary (stručne)

- **Autorstvo:** Verejné metadáta repozitára Vectaetos uvádzajú autora **Richard Fonfára** (ORCID: `0009-0008-5980-8940`).
- **Slovenská stopa:** Projekt nesie **silnú slovenskú jazykovú a identitnú stopu** (slovenské názvy dokumentov, slovenské formulácie jadrových téz, committers.top badge viazaný na Slovensko; GitHub profil uvádza lokaciu Slovakia).
- **Historická os:**
  - interné metadáta deklarujú začiatok konceptu už v **2024** (codemeta `dateCreated`),
  - publikačná vrstva sa deklaruje od **2025-12-28**,
  - verejný vývoj v Git histórii je od **2026-01-02** (initial commit),
  - do **2026-05-20** je v lokálnej kópii 2193 commitov (web profil repozitára už hlási vyšší počet).
- **Filozofické korene:** Vectaetos je formovaný ako **onto-epistemický rámec** s centrálnymi konceptmi „entropickej pokory“, neagentnosti, ontologických hraníc reprezentovateľnosti a explicitnej anti-teleologickej/anti-optimalizačnej pozície.
- **Dôležité obmedzenie:** V dostupných verejných zdrojoch **nie je explicitne doložená** konkrétna slovenská inštitucionálna afiliácia (univerzita/firma/lab) autora; ide najmä o self-declared projektové metadáta + verejný Git footprint.

---

## 2) Historická chronológia Vectaetos (dátumovo)

## 2.1 Pred-public fáza (deklarovaná v metadátach)
- `codemeta.json` uvádza:
  - `dateCreated: 2024-06-01`
  - `datePublished: 2025-12-28`
  - `dateModified: 2026-01-29`

**Interpretácia:** koncepčný vznik je deklarovaný skôr než verejný Git bootstrap. Toto je interné/autorské metadátum, nie nezávisle verifikovaný externý audit.

## 2.2 Verejný Git bootstrap
- Najstarší commit v lokálnej kópii: **2026-01-02**
  - `ee82969 2026-01-02 Richard Fonfara Initial commit`
- V januári sa rýchlo pridáva identita projektu (CNAME, README expanzia, DOI/ORCID referencie).

## 2.3 Release disciplína
Tagy (podľa `git for-each-ref --sort=creatordate`):
- Vectaetos — 2026-01-14
- v0.1 — 2026-01-27
- v0.1.1 — 2026-01-29
- v0.2.0 — 2026-02-08
- v0.2.1 — 2026-02-15
- v1.0 — 2026-02-22
- v1.1 — 2026-04-01

## 2.4 Tempo vývoja (lokálna kópia)
Počet commitov podľa mesiacov:
- 2026-01: 178
- 2026-02: 277
- 2026-03: 931
- 2026-04: 527
- 2026-05: 280

Aktuálny head lokálnej kópie:
- commit: `34256c89e8c87265072a3446e67db7f6f7771fba`
- dátum: **2026-05-20 18:53:09 +0200**
- autor: Richard Fonfára

Poznámka: webová GitHub stránka repozitára už zobrazuje vyšší commit count než lokálny snapshot (očakávateľné pri neskoršej synchronizácii).

---

## 3) Pozadie Richarda Fonfáru (z verejných technických metadát)

## 3.1 Priamo uvedené autorstvo
- `CITATION.cff`: autor Richard Fonfára + ORCID `0009-0008-5980-8940` + DOI `10.5281/zenodo.18735195`.
- `codemeta.json`: autor Richard Fonfára (ORCID), prepojenie na GitHub repozitár a vectaetos.eu.

## 3.2 Reálna autorská stopa v Gite
`git shortlog -sne HEAD` ukazuje dominantné autorstvo variantov mena Richard Fonfára/Fonfara (spolu drvivá väčšina commitov).

**Interpretácia:** technická história repozitára silno podporuje tézu, že Richard Fonfára je hlavný tvorca/maintainer.

## 3.3 Verejný profilový kontext
- GitHub profil `https://github.com/rischo32` (verejne) uvádza lokalitu **Slovakia**.
- Repo README obsahuje committers.top badge smerujúci na slovak ranking URL.

---

## 4) Slovenské technické a filozofické korene projektu

## 4.1 Jazyková vrstva (silný indikátor pôvodu)
V repozitári sú explicitne slovenské texty a názvy, napr.:
- `EMPIRICKÁ_PRIORITA_BEZPEČNOSTI.md`
- `Verejná_bezpečnostná_pozícia.md`
- rozsiahle slovensko‑anglické formulácie v `README.md`, `METAMATH.md`, `REGULATORY_POSITION.md`, `ENTROPIC_HUMILITY.md`

Aj skoré commit správy obsahujú slovenčinu (napr. `Vectaetos: reprezentatívny stav poľa`, 2026-01-11).

## 4.2 Filozofický základ (slovenská formulácia jadra)
Kľúčové pojmy sú artikulované slovensky aj anglicky:
- ontologická architektúra,
- reprezentovateľnosť významu,
- entropická pokora,
- neagentnosť,
- kvalitatívna epistemická apória,
- explicitná suspendácia predčasnej operačnej legitimácie vyšších vrstiev.

To ukazuje, že filozofické jadro nebolo len preložené z externého anglického rámca, ale je tvorené organicky v slovenskom diskurze projektu.

## 4.3 Európsko-regulačné ukotvenie (kompatibilné so SK/EU prostredím)
Právno-regulačné dokumenty sú orientované na EU AI Act a európske inštitúcie; dokument `EU_AI_ACT_POSITION.md` má freshness review k **19 May 2026** a explicitne odkazuje na aktuálny európsky regulačný horizont.

---

## 5) Čo je potvrdené vs. čo je zatiaľ inferencia

## Potvrdené (vyššia istota)
1. Richard Fonfára je uvedený ako autor v CFF/codemeta + ORCID prepojenie.
2. Repo má silnú slovenskú jazykovú stopu a slovenské dokumenty už od skorého vývoja.
3. Git história ukazuje masívne dominantné autorstvo jedného jadra (Richard Fonfára/Fonfara varianty).
4. Projekt sa explicitne pozicionuje ako onto-epistemický, neagentný bezpečnostný rámec.

## Inferencia (stredná istota)
1. „Korene v slovenskom technicko-filozofickom prostredí“ sú veľmi pravdepodobné na základe jazyka, identity a profilovej lokácie, ale bez externého inštitucionálneho potvrdenia.
2. Pred‑2026 história (2024/2025) je v tejto fáze opretá najmä o self-declared metadata (codemeta/DOI prepojenia), nie o nezávislé archívne rekonštrukcie každej etapy.

---

## 6) Riziká interpretácie a metodické limity

- Verejné profily/badge môžu obsahovať self-reported položky.
- Nie všetky externé registry boli počas tejto iterácie rovnako strojovo extrahovateľné.
- Viaceré menné varianty v Git histórii (diakritika/bez diakritiky) treba normalizovať pri forenznom audite autorstva.

---

## 7) Odporúčaný follow-up (ak lead chce „forensic-grade“ verziu)

1. Spraviť DOI-level verifikáciu cez Zenodo API pre všetky citované DOI vetvy.
2. ORCID record export (JSON/XML) a kontrola časovej konzistencie profilových položiek.
3. Formálny snapshot GitHub metadata (repo creation/push timeline, release assets, signed tags).
4. Doplniť slovenské inštitucionálne väzby len po explicitne overiteľnom zdroji (obchodný register, právny subjekt, akademická afiliácia).

---

## 8) Použité zdroje

## Primárne lokálne (repo snapshot)
- `/home/team/shared/vectaetos_repo/README.md`
- `/home/team/shared/vectaetos_repo/codemeta.json`
- `/home/team/shared/vectaetos_repo/CITATION.cff`
- `/home/team/shared/vectaetos_repo/METAMATH.md`
- `/home/team/shared/vectaetos_repo/ENTROPIC_HUMILITY.md`
- `/home/team/shared/vectaetos_repo/EMPIRICKÁ_PRIORITA_BEZPEČNOSTI.md`
- `/home/team/shared/vectaetos_repo/Verejná_bezpečnostná_pozícia.md`
- `/home/team/shared/vectaetos_repo/infrastructure/legal/REGULATORY_POSITION.md`
- `/home/team/shared/vectaetos_repo/infrastructure/legal/EU_AI_ACT_POSITION.md`
- Git metadata priamo z lokálnej kópie (`git log`, `git tag`, `git shortlog`, `git rev-list`)

## Verejné web zdroje
- GitHub profil: https://github.com/rischo32
- GitHub repo: https://github.com/rischo32/Vectaetos
- ORCID profil: https://orcid.org/0009-0008-5980-8940
- DOI odkazy z README:
  - https://doi.org/10.5281/zenodo.19370185
  - https://doi.org/10.5281/zenodo.19478683
- Committers.top (SK ranking stránka): https://committers.top/slovakia.html
