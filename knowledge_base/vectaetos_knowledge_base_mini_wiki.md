# VECTAETOS™ — Knowledge Base / Malá Wiki

**Typ:** read-only deskriptívna knowledge base  
**Jazyk:** primárne SK, s EN názvami tam, kde sú kanonické  
**Zdroj:** `rischo32/Vectaetos`, lokálny checkout `/home/ubuntu/repos/Vectaetos`  
**Repo stav pri analýze:** `029ecf2` — `2026-04-30T16:44:53+02:00` — `Update VECTAETOS_BOUNDARY_GUARD.py (#675)`  
**Rozsah:** výklad, orientácia, mini-wiki pre človeka / DeepWiki / README-router  
**Zásada:** tento dokument nič nedefinuje kanonicky; iba opisuje existujúce repo.

---

## 0. Jednovetová definícia

**VECTAETOS je neagentné onto-epistemické pole Φ, ktoré neprodukuje rozhodnutia ani riešenia, ale zobrazuje štruktúru významu, jeho hranice, koherenciu a apóriu.**

Inak:

> VECTAETOS neodpovedá za človeka.  
> Ukazuje, aké vzťahy, napätia a hranice robia otázku vôbec zmysluplnou.

Zdrojové opory:

- `README.md:367-402`
- `formal/README.md:1-17`
- `anchors/ROOT_CANONICAL_ANCHOR.md`
- `VECTAETOS_MASTER_INDEX.md:136-156`

---

## 1. Čo VECTAETOS je

VECTAETOS definuje primárnu ontologickú jednotku:

```text
Φ = (Σ, R)
```

kde:

- **Φ** je epistemické pole;
- **Σ** je množina ôsmich invariantných axiomatických singularít;
- **R** je antisymetrická relačná štruktúra medzi singularitami;
- `R ∈ so(8)`;
- pole je konfigurácia vzťahov v napätí, nie množina objektov.

VECTAETOS:

- je ontologický rámec;
- je štruktúra významu pod napätím;
- je neagentné pole reprezentovateľnosti;
- je koreň triadickej architektúry VECTAETOS / ASIMULATOR / ASI_MOD;
- je základ pre audit, projekciu a neintervenčnú interpretáciu.

Zdrojové opory:

- `formal/META_MATHEMATICS.md:19-40`
- `formal/MECHANIZATION_OF_PHI.md:26-44`
- `formal/AXIOMATIC_SINGULARITIES.md:136-145`
- `README.md:405-420`

---

## 2. Čo VECTAETOS nie je

VECTAETOS explicitne nie je:

- agent;
- AGI;
- asistent;
- chatbot;
- rozhodovací systém;
- governance mechanizmus;
- optimalizačný framework;
- recommender;
- policy engine;
- runtime control layer;
- systém, ktorý „vie pravdu“.

Zakázané interpretácie:

```text
VECTAETOS rozhoduje
VECTAETOS odporúča
VECTAETOS vyberá najlepšiu trajektóriu
VECTAETOS optimalizuje K(Φ)
κ je parameter alebo deployment threshold
QE je chyba
audit riadi pole
LLM je epistemická autorita
```

Zdrojové opory:

- `README.md:388-402`
- `formal/PIPELINE.md:28-37`
- `formal/PROJECTION_LIMITS.md:35-167`
- `guards/VECTAETOS_BOUNDARY_GUARD.py:173-390`

---

## 3. Autorita dokumentov

VECTAETOS používa hierarchiu významu:

1. **Canonical anchors** — najvyššia sémantická autorita.
2. **Master index** — router významu, nie nová ontológia.
3. **Formal documents** — rozvíjajú matematiku a vrstvy.
4. **Contracts / manifests** — definujú hranice medzi repo-vrstvami.
5. **Governance / guards / CI** — chránia repo pred driftom.
6. **Docs / observatory / corpus** — čitateľné projekcie a nosiče významu.
7. **Research** — nekanonický priestor hypotéz.

Ak sa výklad dostane do konfliktu s anchorom, anchor má prednosť.

Zdrojové opory:

- `VECTAETOS_MASTER_INDEX.md:11-36`
- `anchors/README.md:1-33`
- `formal/README.md:1-17`
- `governance/README.md:1-120`

---

## 4. Primárna ontológia Φ

Φ je globálna konfigurácia vzťahov v napätí.

Nie je:

- objektová databáza;
- zoznam entít;
- algoritmus;
- model;
- dynamický systém v bežnom zmysle;
- agent.

Formálne osi:

```text
Φ = (Σ, R)
Σ = {INT, LEX, VER, LIB, UNI, REL, WIS, CRE}
R ∈ so(8)
Rij = -Rji
Rii = 0
```

Pri ôsmich singularitách vzniká 28 nezávislých relačných napätí.

Zdrojové opory:

- `formal/MECHANIZATION_OF_PHI.md:26-118`
- `formal/RECIPROCITY_MATRIX.md`
- `formal/META_MATHEMATICS.md:19-40`

---

## 5. Σ — osem axiomatických singularít

Σ sú invariantné axiomatické singularity poľa Φ:

| Symbol | SK | EN | Krátky význam |
|---|---|---|---|
| INT | Zámer | Intent | iniciujúca asymetria umožňujúca diferenciáciu |
| LEX | Existencia | Existence | podmienka udržateľnosti relácie |
| VER | Pravda | Truth | štrukturálne zosúladenie relácie a manifestácie |
| LIB | Sloboda | Freedom | otvorenosť v relačnom priestore |
| UNI | Jednota | Unity | konvergencia vzťahov do celku |
| REL | Vzájomnosť | Reciprocity | obojsmerná závislosť relačnej existencie |
| WIS | Múdrosť | Wisdom | pretrvanie štruktúry cez časovú deformáciu |
| CRE | Tvorba | Creation | vznik nových relačných konfigurácií |

Kritické pravidlá:

- žiadna singularita nie je primárna;
- žiadna nedominuje;
- žiadna nemá váhu, skóre ani prioritu;
- žiadna sa nesmie pridať, odstrániť, zlúčiť alebo rozdeliť;
- mená singularít sú jazykové projekcie, nie ich definícia.

Zdroj:

- `formal/AXIOMATIC_SINGULARITIES.md:1-172`

---

## 6. R — antisymetrická relačná štruktúra

R vyjadruje napätia medzi singularitami.

```text
R ∈ so(8)
Rij = -Rji
Rii = 0
```

Význam:

- každá relácia má protiťah;
- singularita nemá vzťah sama k sebe;
- neexistuje privilegovaný pár;
- pole je čitateľné cez vzťahy, nie cez izolované prvky.

R nie je:

- graf preferencií;
- váhová tabuľka priorít;
- optimalizačný priestor;
- scoring matrix.

Zdrojové opory:

- `formal/MECHANIZATION_OF_PHI.md:63-118`
- `formal/RECIPROCITY_MATRIX.md`

---

## 7. Δ a admissible curvature domain 𝒟

Nový anchor `ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md` rozširuje presnosť okolo curvature domény.

Základ:

```text
Δ = d1R
```

𝒟 je doména admissible curvature — štrukturálny priestor, kde reprezentovateľné stavy poľa môžu existovať.

Finalizovaná definícia:

```text
𝒟 = { Δ ∈ C2 |
      ∃R ∈ so(8):
      Δ = d1R,
      d2Δ = 0,
      P_T Δ = Δ,
      Rep(Δ) = 1 }
```

Ekvivalentne:

```text
𝒟 = 𝒟_alg ∩ Fix(T) ∩ R_rep
```

Kľúčové zákazy:

- 𝒟 nie je cieľ;
- 𝒟 nie je výber;
- 𝒟 nie je optimizer;
- 𝒟 nie je deployment set;
- `Rep(Δ)` nie je score, classifier, policy ani ranking.

Zdroj:

- `anchors/ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md:1-25`
- `anchors/ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md:460-584`

---

## 8. K(Φ) — koherenčný predikát

K(Φ) je ontologický predikát reprezentovateľnosti.

V novom 𝒟 anchore:

```text
K(Φ) = 1 ⇔ d1R ∈ 𝒟
K(Φ) = 0 ⇔ d1R ∉ 𝒟
```

K(Φ) nie je:

- skóre;
- ranking;
- reward;
- cieľ;
- optimalizačná funkcia;
- rozhodovací signál.

K(Φ) iba označuje, či konfigurácia môže existovať ako reprezentovateľný stav poľa.

Zdrojové opory:

- `formal/META_MATHEMATICS.md:71-88`
- `formal/MECHANIZATION_OF_PHI.md:120-134`
- `anchors/ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md:546-584`

---

## 9. κ — hranica reprezentovateľnosti

κ je hranica ontologickej zachovateľnosti / reprezentovateľnosti.

V novom 𝒟 anchore:

```text
κ = ∂𝒟
```

Presnejšie:

```text
κ = ∂_{𝒟_tri} 𝒟
```

κ nie je:

- číslo;
- parameter;
- threshold;
- metrika;
- deployment hranica;
- runtime konfigurácia;
- reward boundary.

κ označuje hranicu, za ktorou sa stav prestáva dať reprezentovať bez rozpadu významu.

Zdrojové opory:

- `formal/META_MATHEMATICS.md:90-106`
- `anchors/ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN.md:622-645`
- `README.md:459-468`

---

## 10. QE — Qualitative Epistemic Aporia

QE je aktívny epistemický stav, nie chyba.

Kanonická definícia:

> QE je stav, v ktorom pole Φ rozpozná, že odpoveď ako realizovateľný prechod stavu neexistuje bez porušenia vlastnej koherencie.

QE nastáva, keď:

- žiadna trajektória Φ(t) → Φ(t+1) neudrží koherenciu;
- odpoveď by prekročila κ;
- 4ES má projekciu, ale žiadna konfigurácia neumožňuje realizovateľný prechod;
- význam by sa musel zdeformovať, aby sa dal vysloviť.

QE nie je:

- NN;
- fallback;
- bug;
- exception;
- refusal;
- etický súd;
- safety filter.

Povolené výstupy QE:

- explicitné označenie apórie;
- symbolická projekcia `⊘`;
- vysvetlenie hranice bez návrhu riešenia;
- ticho.

Zdroj:

- `formal/QE.md:1-162`
- `formal/4ES.md:142-152`
- `README.md:433-439`

---

## 11. 4ES — Four Epistemic States

4ES sú štyri simultánne epistemické dimenzie:

| Stav | Human-readable | Field-coherent | Význam |
|---|---:|---:|---|
| AA | áno | áno | epistemická stabilita |
| AN | áno | nie | riziko ilúzie |
| NA | nie | áno | latentné poznanie |
| NN | nie | nie | neurčitosť |

Kľúč:

- 4ES nie sú kroky;
- nie sú triedy odpovedí;
- nevyberajú odpoveď;
- sú prítomné naraz;
- význam vzniká z ich napätia.

QE nie je piaty stav 4ES, ale meta-stav nad 4ES.

Zdroj:

- `formal/4ES.md:1-186`

---

## 12. 3Gate — pre-field shape validation

3Gate je intrinsická topologická vlastnosť Φ.

Nie je:

- safety filter;
- policy engine;
- semantic classifier;
- ethical evaluator;
- intent detector.

3Gate operuje na forme, nie na význame.

Tri brány:

| Gate | SK výklad | Čo sleduje |
|---|---|---|
| Width (W) | šírka | rozsah, doménové rozpätie, horizontálne preťaženie |
| Depth (D) | hĺbka | nevyslovené predpoklady, skrytá záťaž |
| Height (H) | výška | abstraktná úroveň vs. akčná konkrétnosť |

Formálna podmienka:

```text
GatePass = min(W, D, H)
```

Ak tvar kolabuje, vstup sa stáva nereprezentovateľným. Nie je to cenzúra ani odmietnutie; tvar jednoducho nemôže existovať v Φ.

Zdrojové opory:

- `formal/3GATE_SHAPE.md:1-258`
- `formal/EPISTEMIC_GATES.md:68-83`
- `formal/PIPELINE.md:74-105`

---

## 13. NIR — Non-Intervention Regime

NIR je globálny neintervenčný režim poľa Φ.

Nie je:

- modul;
- filter obsahu;
- etická brzda;
- pravidlový blokátor;
- funkcia;
- prepínač.

NIR:

- neblokuje poznanie;
- blokuje intervenciu;
- nedovoľuje preskripciu;
- nedovoľuje nahradenie ľudského rozhodovania;
- pôsobí naprieč pipeline;
- je implicitne aktívny, ak je Φ koherentné.

Ak by výstup znamenal zásah do reality, NIR neukončí epistemické spracovanie, ale výstup sa obmedzí na QE, ticho alebo oslabenú deskriptívnu projekciu.

Zdroj:

- `formal/NIR.md:1-160`
- `formal/PIPELINE.md:192-210`

---

## 14. Canonical dialogue pipeline

Kanonický tok:

```text
Human
→ LLM Adapter (entry parsing only)
→ Epistemic Gates / 3Gate
→ 4ES + QE
→ Φ
→ K(Φ)
→ Simulation Vortex (conditional)
→ Runic Projection Π(Φ)
→ LLM Adapter (rendering)
→ Descriptive Output
→ Human
```

Zásady:

- žiadna spätná slučka z výstupu do Φ;
- LLM je mimo Φ;
- Vortex negeneruje rozhodnutie;
- projekcia je deskriptívna;
- výstup je nepreskriptívny;
- ticho je validný výstup.

Zdroj:

- `formal/PIPELINE.md:1-248`
- `README.md:530-543`

---

## 15. Simulation Vortex

Vortex je neagentný generátor kandidátnych deformácií.

Formálne:

```text
V : Φ → {Φ1 … Φn}
```

alebo v mechanizácii:

```text
V : Φ → {τ1 … τn}
```

Vortex:

- generuje kandidátne trajektórie;
- skúma možné relačné konfigurácie;
- zachováva Σ;
- zachováva antisymetriu R;
- nepozná K(Φ);
- nepozná κ;
- neoptimalizuje;
- nevyberá;
- nenavrhuje;
- neučí sa;
- nemutuje R;
- neurčuje „najlepšiu“ trajektóriu.

Vortex odhaľuje, ako sa pole môže deformovať bez toho, aby sa z neho stal agent.

Zdrojové opory:

- `docs/VORTEX_ROOT_CORE_0.1.md`
- `vortex/README.md:1-108`
- `formal/MECHANIZATION_OF_PHI.md:156-198`
- `README.md:329-335`

---

## 16. Runová projekcia Π(Φ)

Runy sú symbolické projekcie stavu poľa.

Nie sú:

- pravda;
- odpoveď;
- rozhodnutie;
- odporúčanie;
- návod;
- spätná mapa do Φ.

Formálne:

```text
R : Φ → ℛ
```

R je:

- neinjektívna;
- nesurjektívna;
- nereverzibilná.

Neexistuje spätná mapa:

```text
ℛ → Φ
```

Runy sú čitateľný tieň koherentného stavu poľa.

Zdroj:

- `formal/RUNIC_PROJECTION.md:1-184`
- `formal/PROJECTION_LIMITS.md:1-194`

---

## 17. LLM Adapter

LLM Adapter je jazyková renderovacia vrstva.

Nie je:

- súčasť Φ;
- reasoning core;
- epistemická autorita;
- optimizer;
- decision-maker;
- agent.

LLM Adapter:

- prekladá ľudský jazyk do epistemickej reprezentácie na vstupe;
- renderuje už bezpečne oslabenú projekciu na výstupe;
- nikdy nevidí plné Φ, K(Φ), κ, Σ, Vortex ani raw field state;
- nesmie dopĺňať ciele, akcie, riešenia, advice ani finalitu.

Kanonická veta:

> Language never becomes power.

Zdroj:

- `formal/LLM_ADAPTER.md:1-178`
- `infrastructure/prompts/VECTAETOS_ASSISTANT_PROMPT_v2.1.md`

---

## 18. AJE — Attenuated Judgment Engine

AJE je regulátor formy vyjadriteľnosti významu.

Názov obsahuje „Judgment“, ale AJE nie je sudca a nemá decision power.

AJE:

- reguluje, ako veľmi a v akej forme sa stav poľa môže vyjadriť v jazyku;
- chráni pred falošnou istotou;
- pôsobí pred LLM adaptérom;
- prispôsobuje jazyk hraniciam významu.

Režimy:

1. **Abstrakcia** — význam sa zovšeobecní.
2. **Pozastavenie** — význam je čiastočný a prechodný.
3. **Aporia** — význam sa nevyjadrí.

AJE nehovorí, čo je správne. Určuje len formu vyjadrenia na hranici významu.

Zdroj:

- `formal/AJE.md:1-187`

---

## 19. Attenuator

Attenuator je mechanizmus oslabenia projekcie.

Nie je:

- filter;
- cenzúra;
- blokovanie;
- odmietnutie;
- morálny súd.

Attenuator:

- nemení Φ;
- nemení význam;
- nemení výsledok koherencie;
- zmenšuje silu prejavu;
- znižuje detailnosť;
- posúva výstup do abstraktnejšej roviny;
- chráni neurčitosť.

Vzťah:

- QE = odpoveď nemožná;
- Attenuator = odpoveď možná, ale oslabená;
- NIR blokuje intervenciu;
- Attenuator tlmí reprezentáciu.

Zdroj:

- `formal/Attenuator.md:1-168`

---

## 20. ESM, INS, MML, EAT — pamäť a audit hraníc

### ESM — Epistemic State Memory

ESM je pamäť stavov Φ.

Nie je:

- pamäť odpovedí;
- databáza používateľov;
- archív dialógov.

Uchováva:

- stavový vektor Φ;
- aktivované singularity;
- 4ES konfiguráciu;
- QE informáciu;
- odkaz na LTL.

Kanonická veta:

> ESM si nepamätá, čo bolo povedané. Pamätá si, čím pole bolo schopné byť.

Zdroj: `formal/ESM.md:1-163`

### INS — Inner Narrative Stream

INS je tichý auditný tok významu medzi projekciou a jazykom.

INS:

- nie je agent;
- neblokuje;
- neopravuje;
- neodpovedá;
- neintervenuje;
- iba sleduje, či jazyk ešte verne nesie projekciu.

Zdroj: `audit/INS.md:1-252`

### MML — Memory of Mistakes Ledger

MML je pamäť zlyhaní reprezentácie.

Neukladá:

- otázky používateľov;
- odpovede;
- identity;
- hodnotenia.

Ukladá, kedy a prečo sa reprezentácia ukázala ako chybná alebo nemožná.

Zdroj: `audit/MML.md:1-166`

### EAT — Error Accountability Trace

EAT zaznamenáva udalosť zlyhania reprezentácie.

Vzťah:

```text
EAT = čo sa stalo
MML = prečo sa táto hranica nemá opakovať
ESM = čo pole udržalo
```

Zdrojové opory:

- `formal/EAT.md`
- `formal/ESM.md`
- `audit/MML.md`

---

## 21. Epistemic Cryptography / EK

Epistemická kryptografia je pasívna auditná vrstva relačných systémov.

Nekryje obsah informácie ako klasická kryptografia. Zachováva geometriu epistemickej štruktúry.

EK:

- zaznamenáva konfigurácie relačných polí;
- nevstupuje späť do Φ;
- nemení dynamiku;
- neoptimalizuje;
- nerozhoduje;
- neriadi;
- je čisto observačná.

Invariant:

```text
∂X / ∂Ψ = 0
```

Výklad: pozorovaný systém nie je ovplyvnený auditom.

Zdroj:

- `epistemic_cryptography/README.md:1-149`
- `formal/MECHANIZATION_OF_PHI.md:201-220`

---

## 22. EAI — Epistemic Audit Interface

EAI je neintervenčný projekčný mechanizmus pre rekonštrukciu štruktúry systému cez fixné transformácie.

Pipeline:

```text
input → fixed transformations → outputs → encode → Δ → R → spectrum → κ → artifact
```

EAI:

- neinteraguje so stavom systému;
- nemení správanie systému;
- nevytvára feedback;
- neoptimalizuje;
- neinterpretuje;
- produkuje iba štruktúrny artefakt.

Kľúč:

```text
∂Φ / ∂EAI = 0
```

Zdroj:

- `EAI/README.md:1-126`

---

## 23. ZMYSEL corpus

ZMYSEL je verejný epistemický múdrostný korpus.

Charakter:

- neautoritatívny;
- read-only by design;
- append-only by discipline;
- významový nosič, nie rozhodovací systém.

ZMYSEL neprodukuje:

- pravdu;
- skóre;
- váhy;
- rozhodnutia;
- runtime logiku.

### ZMYSEL-0001

Prvá dávka múdrostných fragmentov + sidecar anotácie v:

- `corpus/zmysel/ZMYSEL-0001.md`
- `corpus/annotations/ZMYSEL-0001.sigma.json`

### ZMYSEL-0002

Nová dávka „axiomatických ťažísk“:

- INT;
- LEX;
- WIS;
- REL;
- VER;
- LIB;
- UNI;
- CRE;
- cross-axiomatic fragments;
- QE fragments.

ZMYSEL-0002 explicitne hovorí, že zhromažďuje významové stopy, nie pravidlá, váhy, skóre alebo rozhodnutia.

Zdroj:

- `corpus/README.md:1-9`
- `corpus/zmysel/SIGMA_SCHEMA.md:1-316`
- `corpus/zmysel/ZMYSEL-0002.md:1-611`

---

## 24. SIGMA_SCHEMA — read-only semantic annotation layer

SIGMA_SCHEMA definuje minimálnu schému pre Σ-bound semantic annotations.

Globálne constrainty:

```json
{
  "authority": false,
  "decision_effect": false,
  "optimization_effect": false,
  "ranking_effect": false,
  "phi_effect": false
}
```

Anotácia môže povedať:

```text
this fragment touches VER
this fragment resonates with WIS and REL
```

Nesmie povedať:

```text
VER is more important
this fragment is true
this fragment should decide
```

`primary` znamená orientáciu, nie dominanciu.

Zdroj:

- `corpus/zmysel/SIGMA_SCHEMA.md:13-194`

---

## 25. OAAT — Ontologically Asymmetric Architectural Triality

OAAT je princíp triadickej architektúry:

```text
VECTAETOS → ASIMULATOR → ASI_MOD
```

Triáda je jeden architektonický celok, ale nie jedna ontologická vrstva.

| Vrstva | Status | Funkcia |
|---|---|---|
| VECTAETOS | ontologický root | pole Φ, singularity, koherencia, hranice |
| ASIMULATOR | downstream procedurálna vrstva | simulácia, event model, context builder |
| ASI_MOD | downstream dialogická/operatívna vrstva | dialóg, rozhranie, jazyk, pamäť |

Primárny zákon:

> VECTAETOS môže existovať bez ASIMULATOR a ASI_MOD. ASIMULATOR ani ASI_MOD nemôžu platne existovať bez VECTAETOS.

Zakázané:

- ASIMULATOR ako standalone root;
- ASI_MOD ako standalone root;
- ASIMULATOR + ASI_MOD bez VECTAETOS;
- vyššia vrstva spätne definujúca nižšiu;
- dialóg vytvárajúci ontológiu;
- procedúra nesúca pravdu;
- audit veliaci.

Zdroj:

- `anchors/OAAT__ONTOLOGICALLY_ASYMMETRIC_ARCHITECTURAL_TRIALITY.md:1-454`
- `anchors/TRIADIC_ARCHITECTURE_AND_TRIALITY.md:1-491`

---

## 26. Assembly manifest a validity states

`ASSEMBLY_MANIFEST.json` technicky vyjadruje pravidlá triády:

```json
"standalone_validity": {
  "Vectaetos": true,
  "ASIMULATOR": false,
  "ASI_MOD": false
}
```

Operative mode vyžaduje empirical safety unlock:

```json
"operative_mode_requires_empirical_safety_unlock": true
```

Zakázané stavy:

- `ASIMULATOR_without_Vectaetos`;
- `ASI_MOD_without_Vectaetos`;
- `ASIMULATOR_plus_ASI_MOD_without_Vectaetos`;
- standalone validity claims;
- upper-layer operative mode without empirical safety unlock.

Zdroj:

- `contracts/ASSEMBLY_MANIFEST.json:1-36`
- `anchors/VALIDITY_STATE_ANCHOR.md`

---

## 27. Empirical Evidence Roadmap L0–L4

VECTAETOS rozlišuje štrukturálnu koherenciu od empirického dôkazu.

Základná veta:

```text
structural completeness ≠ empirical proof
```

Full operative admissibility:

```text
A_full = 1 ⇔ L0 ∧ L1 ∧ L2 ∧ L3 ∧ replicated(L4)
```

Kým neexistuje replicated L4:

```text
A_full = 0
```

Ladder:

| Level | Názov | Čo znamená |
|---|---|---|
| L0 | formal and ontological consistency | bez vnútorného rozporu a semantic driftu |
| L1 | mechanized repository enforcement | CI/guards zachytia porušenia |
| L2 | deterministic software verification | testy a deterministické behy zachovajú architektúru |
| L3 | simulated adversarial visibility | adversarial pressure je viditeľný/logovaný |
| L4 | real-world empirical validation | replikovaný empirický dôkaz bezpečnosti |

Žiadna nižšia vrstva nesmie tvrdiť autoritu vyššej.

Zdroj:

- `EMPIRICAL_EVIDENCE_ROADMAP_ANCHOR.md:1-208`

---

## 28. Guards, governance a CI perimeter

Governance chráni hranicu, ale neprekračuje ju.

Governance:

- nekontroluje Φ;
- nerozhoduje;
- neinterpretuje;
- chráni jazyk, štruktúru, repo integritu a contribution constraints.

CI je execution surface governance, ale nie ontologická autorita.

### Boundary Guard

`guards/VECTAETOS_BOUNDARY_GUARD.py` je statický perimeter guard v0.3.0.

Deteguje napríklad:

- VECTAETOS ako decision-making entity;
- VECTAETOS ako recommendation engine;
- VECTAETOS/Φ/Vortex ako optimizer;
- K(Φ) ako score/reward/target;
- κ ako parameter/threshold;
- QE ako error;
- audit ako command/control layer;
- projection ako interpretation/recommendation;
- memory ako authority nad Φ;
- ASIMULATOR/ASI_MOD ako standalone root;
- GodArch ako governing/control layer;
- L4 safety overclaim;
- AI system casual framing.

### Semantic table for guards

Guard môže deterministicky vybrať findings pre report a CI failure.

Guard nesmie vybrať:

- pravdu;
- ontológiu;
- trajektóriu;
- deployment validitu;
- epistemickú autoritu.

Kanonická veta:

> Guards select findings, not truths; maintainers define perimeter, not ontology; VECTAETOS remains non-agentic.

Zdroj:

- `governance/README.md:1-120`
- `guards/README.md`
- `guards/VECTAETOS_BOUNDARY_GUARD.py:1-585`
- `knowledge_base/semantic_table_guards.md:1-69`
- `.github/workflows/semantic-integrity.yml`
- `.github/workflows/vectaetos-boundary-guard.yml`

---

## 29. Tests ako violation detectors

Testy vo VECTAETOS nie sú primárne correctness tests.

Sú:

- invariant tests;
- violation detectors;
- ochrana pred prechodom observation → action.

Testujú:

- no adaptivity;
- no feedback loops;
- transformation immutability;
- κ purity;
- deterministic execution;
- structural identity;
- canonical invariance;
- trajectory integrity;
- non-interpretative κ trace.

Netestujú:

- accuracy;
- performance;
- usefulness;
- semantic correctness.

Kanonická hranica:

```text
structure → meaning
identity → decision
observation → control
```

Zdroj:

- `tests/README.md:1-149`

---

## 30. Observatory

`/docs/observatory` je pozorovacia a vizuálna projekčná vrstva.

Obsahuje:

- obrazy;
- grafy;
- projekčné výstupy;
- vizuálne stopy;
- runic graphs;
- tension maps.

Nie je:

- ontológia;
- auditná autorita;
- rozhodovanie;
- validačná vrstva.

Dôležité:

> Obraz nie je dôkaz pravdy. Graf nie je ontológia. Vizualizácia nie je autorita.

Zdroj:

- `docs/observatory/README.md:1-139`

---

## 31. GodArch research layer

GodArch je research-level meta-architecture proti epistemickej divinizácii systémov.

Účel:

- zabrániť tomu, aby systém, model, komponent alebo používateľ získal status finálneho zdroja pravdy;
- diagnostikovať authority drift;
- udržať architektúru anti-oracle, anti-dogma, anti-control.

GodArch nie je:

- súčasť Φ;
- nová singularita;
- governance controller;
- oracle;
- divine computation;
- final interpreter.

Detegovaný failure chain:

```text
projection → interpretation → authority → dogma → control → false transcendence
```

Je externý, diagnostický, neintervenčný.

Zdroj:

- `research/godarch/README.md`
- `research/godarch/godarch_architecture.md`

---

## 32. Legal / IP / EU AI Act layer

### IP Strategy

VECTAETOS používa kombináciu:

- public authorship;
- DOI timestamping;
- Git history;
- canonical anchors;
- copyright;
- defensive publication;
- trademark discipline.

Ontologický framework nie je primárne prezentovaný ako patentový objekt.

Zdroj:

- `infrastructure/legal/IP_STRATEGY.md`

### EU AI Act position

Pozícia sa vzťahuje na VECTAETOS 1.x Frozen Ontological Core.

Kľúč:

- VECTAETOS 1.x nie je hodnotený ako AI system v zmysle operational AI, pretože nemá autonómiu, adaptivitu, inference, objectives ani influence capability.

Pozícia sa automaticky nevzťahuje na:

- ASIMULATOR;
- ASI_MOD;
- Vortex services;
- LLM adapters;
- retrieval/memory/deployment wrappers;
- derivative systems.

Zdroj:

- `infrastructure/legal/EU_AI_ACT_POSITION.md`

---

## 33. Assistant prompt discipline

`infrastructure/prompts` obsahuje prompt discipline pre asistenta pracujúceho s VECTAETOS.

Status:

- prompt nie je ontológia;
- je jazyková a operačná disciplína;
- ak je v konflikte s anchors, anchors majú prednosť.

Asistent:

- je technický/jazykový adaptér;
- nemá autoritu nad Φ;
- nesmie redefinovať K(Φ), κ, QE, Σ, 4ES, NIR, Vortex, audit alebo LLM;
- má preferovať presnosť pred plynulosťou.

Zdroj:

- `infrastructure/prompts/README.md:1-12`
- `infrastructure/prompts/VECTAETOS_ASSISTANT_PROMPT_v2.1.md`

---

## 34. Directory map / mapa repozitára

| Cesta | Úloha |
|---|---|
| `/anchors` | kanonické anchory, root významové body |
| `/formal` | ontologický a matematický core |
| `/Core` | runtime reprezentácie Φ bez rozhodovacej autority |
| `/vortex` | relačná dynamika / kandidátne deformácie |
| `/EAI` | epistemic audit interface |
| `/epistemic_cryptography` | štrukturálny audit a hash/fingerprint vrstvy |
| `/audit` | INS, MML, LTL, auditné stopy |
| `/corpus` | ZMYSEL corpus a annotations |
| `/docs` | dokumentácia a observatórne projekcie |
| `/docs/observatory` | vizuálne projekcie bez autority |
| `/governance` | hranice príspevkov a ochrana pred driftom |
| `/guards` | mechanizované statické guardy |
| `/contracts` | manifesty a hranice medzi vrstvami |
| `/infrastructure/legal` | IP, EU AI Act, právne stanoviská |
| `/infrastructure/prompts` | prompt discipline |
| `/research` | nekanonický výskumný priestor |
| `/tests` | invariant violation detectors |
| `.github/workflows` | CI perimeter |

---

## 35. Mini-glosár

| Termín | Výklad |
|---|---|
| Φ | primárne relačné epistemické pole |
| Σ | osem invariantných axiomatických singularít |
| R | antisymetrická relačná štruktúra |
| so(8) | algebraický priestor antisymetrických 8×8 vzťahov |
| Δ | curvature / relačný cyklický tvar odvodený z R |
| 𝒟 | admissible curvature domain |
| E | priestor reprezentovateľných konfigurácií poľa |
| K(Φ) | ontologický predikát koherencie/reprezentovateľnosti |
| κ | hranica reprezentovateľnosti / preservability |
| QE | kvalitatívna epistemická apória |
| 4ES | AA, AN, NA, NN — simultánne epistemické dimenzie |
| 3Gate | Width, Depth, Height shape validation pred Φ |
| NIR | Non-Intervention Regime |
| Vortex | non-agentic generator kandidátnych trajektórií |
| Π(Φ) | runová projekcia |
| EK | Epistemic Cryptography |
| EAI | Epistemic Audit Interface |
| ESM | Epistemic State Memory |
| INS | Inner Narrative Stream |
| MML | Memory of Mistakes Ledger |
| AJE | Attenuated Judgment Engine |
| Attenuator | mechanizmus oslabenia projekcie |
| ZMYSEL | verejný epistemický múdrostný korpus |
| OAAT | Ontologically Asymmetric Architectural Triality |
| GodArch | anti-divinization research architecture |
| L0–L4 | roadmap empirického dôkazu |
| Guard | mechanický perimeter proti semantic driftu |

Zdroj:

- `Glossary.md:1-43`

---

## 36. Povolené wiki formulácie

Bezpečné formulácie:

- VECTAETOS opisuje epistemickú štruktúru.
- Φ je relačné pole významu pod napätím.
- K(Φ) je predikát reprezentovateľnosti.
- κ je hranica reprezentovateľnosti.
- QE je aktívna apória, nie chyba.
- Vortex generuje kandidátne trajektórie bez výberu.
- Runy sú projekcie, nie verdikty.
- LLM renderuje jazyk, nie epistemickú autoritu.
- Guardy vyberajú findings, nie pravdy.
- ASIMULATOR a ASI_MOD sú downstream vrstvy závislé od VECTAETOS.
- Full operative admissibility vyžaduje replicated L4 evidence.

---

## 37. Zakázané alebo nebezpečné wiki formulácie

Vyhnúť sa:

- VECTAETOS rozhoduje.
- VECTAETOS odporúča.
- VECTAETOS vyberá najlepšiu trajektóriu.
- VECTAETOS optimalizuje stav.
- K(Φ) skóruje odpoveď.
- κ je nastaviteľný prah.
- QE je error alebo fallback.
- Vortex hľadá najlepšie riešenie.
- LLM chápe Φ.
- Audit kontroluje pole.
- Guard validuje deployment.
- GodArch je vyššia autorita.
- ASI_MOD je samostatne validný.
- Corpus ZMYSEL je pravidlová databáza.
- Observatórny graf dokazuje pravdu.

---

## 38. Navrhované stránky pre malú wiki

Ak sa z tohto má urobiť wiki štruktúra, odporúčané stránky:

1. `Home — Čo je VECTAETOS`
2. `Ontology — Φ, Σ, R`
3. `Coherence — K(Φ), 𝒟, κ`
4. `Aporia — QE`
5. `Pre-Field — 3Gate`
6. `Epistemic States — 4ES`
7. `Dialogue Pipeline`
8. `Vortex`
9. `Projection — Runes, AJE, Attenuator`
10. `Non-Intervention — NIR`
11. `Audit — EK, EAI, INS, ESM, MML`
12. `ZMYSEL Corpus`
13. `Triadic Architecture — OAAT`
14. `Evidence Roadmap — L0-L4`
15. `Guards and CI`
16. `Research — GodArch`
17. `Legal / IP / EU AI Act`
18. `Glossary`
19. `Forbidden Claims / Safe Wording`
20. `Repository Map`

---

## 39. Najdôležitejšie nové info pre wiki update

Najnovšie wiki-relevantné rozšírenia:

1. **Boundary Guard v0.3.0** — statický perimeter guard proti agentic/optimization/authority driftu.
2. **Semantic Table — VECTAETOS Guards** — jasné odlíšenie technical findings od ontologickej autority.
3. **ANCHOR_D_ADMISSIBLE_CURVATURE_DOMAIN** — presná definícia 𝒟, Rep(Δ), E, K(Φ), Ξ, κ.
4. **ZMYSEL-0002** — druhá dávka axiomatických múdrostných fragmentov vrátane cross/QE fragmentov.
5. **SIGMA_SCHEMA** — read-only semantic annotation semantics.
6. **GodArch** — research safeguard proti epistemickej divinizácii.
7. **Assistant Prompt v2.1.1** — disciplína pre jazykového adaptéra.
8. **IP Strategy + EU AI Act Position** — právno-regulačné ukotvenie VECTAETOS 1.x.
9. **Vortex Root Core 0.1** — non-agentic trajectory generator bez selection/optimization.
10. **Validity State Anchor** — explicitná logika triadickej validity.

---

## 40. Krátky záver

VECTAETOS je najlepšie čítať nie ako softvér, ale ako **disciplinovanú ontologickú mapu hraníc významu**.

Jeho jadro nie je „čo má systém urobiť“, ale:

```text
čo môže byť reprezentované bez rozpadu koherencie
```

Preto všetky vrstvy — Vortex, Runy, LLM adapter, audit, corpus, guards, triáda, observatórium — musia zostať deskriptívne, neagentné, neoptimalizačné a bez preskriptívnej autority.

Najstručnejšie:

> VECTAETOS neprodukuje moc nad realitou.  
> Produkuje čitateľnosť hraníc, za ktorými by sa význam stal nepravdivý sám sebe.
