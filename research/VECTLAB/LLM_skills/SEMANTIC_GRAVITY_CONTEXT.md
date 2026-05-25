# Semantic Gravity Context .md
# Semantic Gravity Context Budgeting
## Gravitačne vážené skladanie kontextu pre prompt-safe reasoning systémy

**Status:** technická teória / implementačný návrh  
**Scope:** prompt assembly, memory selection, context budgeting, fail-soft degradation  
**Layer:** LLM Adapter / Context Assembly Layer  
**VECTAETOS compatibility:** downstream only; descriptive, non-authoritative, non-mutating voči Φ  
**Canonical sentence:** Kontext nie je skladisko. Kontext je výber pod rozpočtom.

---

## 0. Executive Summary

Problém nevzniká tým, že používateľský vstup je príliš dlhý.

Problém vzniká tým, že výsledný prompt je skladaný z používateľského vstupu, šablóny, stavových inštrukcií, pamäte, cieľov, epizód, hypotéz, sémantických dát a vyhľadávacích výsledkov, pričom interný kontext môže byť neohraničený.

Ak systém obmedzí používateľský vstup napríklad na `MAX_INPUT_LENGTH = 4000`, ale výsledný prompt obmedzuje na `MAX_PROMPT_LENGTH = 8000`, stále môže dôjsť k tichej degradácii:

```text
short user input + huge memory/context/search results > MAX_PROMPT_LENGTH
```

Výsledkom je stav, kde všetky reasoning režimy vracajú:

```text
[PROMPT TOO LONG]
```

Používateľ však nemá ako problém opraviť, pretože problém nespôsobil jeho vstup, ale interný kontext systému.

Riešenie nie je zvýšiť limit.

Riešenie je zaviesť:

```text
budget-aware prompt assembly
semantic context selection
cluster-based context allocation
gravity-weighted memory retrieval
fail-soft degradation
transparent context report
```

---

## 1. Základná diagnóza

Pôvodný implicitný model:

```text
user_input + template + all_memory + all_context + all_search_results
    ↓
prompt
    ↓
if too long: fail
```

Tento model je krehký, pretože pracuje s kontextom ako so skladiskom.

Správny model:

```text
user_input
    ↓
meaning profile
    ↓
candidate context fragments
    ↓
semantic scoring
    ↓
clustering
    ↓
budget allocation
    ↓
selection / compression
    ↓
prompt preflight
    ↓
LLM call
```

Tým sa prompt neskracuje až po zlyhaní. Prompt sa skladá tak, aby zlyhanie nebolo potrebné.

---

## 2. Kritické rozlíšenie limitov

Treba oddeliť tri limity:

```text
MAX_INPUT_LENGTH
    chráni používateľský vstup

MAX_PROMPT_LENGTH alebo MAX_PROMPT_TOKENS
    chráni výsledný LLM call

CONTEXT_BUDGET
    chráni interný kontext, pamäť a search výsledky
```

Zásadné pravidlo:

```text
Do build_prompt() nesmie vstupovať neohraničený context.
```

Prompt builder nesmie prijímať „všetko, čo máme“. Musí prijímať len vybraný, orezaný, rozpočtovaný a auditovateľný kontext.

---

## 3. Context Economy

Kontext nie je neutrálna hmota. Kontext zaberá promptový rozpočet.

Každý fragment pamäte alebo vyhľadávania má cenu:

```text
cost(fragment) = počet znakov alebo tokenov
```

Každý fragment má zároveň relevanciu:

```text
value(fragment) = jeho sémantická užitočnosť pre aktuálnu otázku
```

Cieľom nie je maximalizovať množstvo kontextu, ale dosiahnuť najlepšie pokrytie významu pod rozpočtom:

```text
vybrať fragmenty tak, aby:
    total_cost <= CONTEXT_BUDGET
    semantic_coverage bolo čo najvyššie
    redundancia bola čo najnižšia
    kritické pamäťové invarianty neboli potlačené
```

Toto nie je ontologická optimalizácia. Je to downstream prompt-engineering mechanizmus.

---

## 4. Semantic Gravity

Semantic gravity je heuristické skóre, ktorým sa určuje, ako silno je kontextový fragment viazaný na aktuálnu otázku.

Nie je to pravda.  
Nie je to autorita.  
Nie je to hodnota reality.  
Nie je to rozhodnutie.  
Je to výberový signál pre prompt assembly layer.

Príklad:

```text
gravity =
    0.45 * semantic_similarity
  + 0.20 * intrinsic_importance
  + 0.15 * recency
  + 0.10 * source_reliability
  + 0.10 * continuity_with_current_session
  - 0.25 * redundancy
  - 0.20 * staleness_penalty
```

Interpretácia zložiek:

| Zložka | Význam |
|---|---|
| `semantic_similarity` | Ako blízko fragment súvisí s aktuálnou otázkou |
| `intrinsic_importance` | Ručne alebo systémovo označená dôležitosť |
| `recency` | Časová blízkosť fragmentu |
| `source_reliability` | Dôveryhodnosť zdroja |
| `continuity_with_current_session` | Väzba na aktuálne riešený problém |
| `redundancy` | Trest za opakovanie toho istého |
| `staleness_penalty` | Trest za zastaraný alebo prekonaný kontext |

Canonical warning:

```text
Gravity score nie je truth score.
```

---

## 5. ContextItem model

Každý fragment kontextu by mal byť normalizovaný do jednej štruktúry:

```python
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ContextItem:
    id: str
    text: str
    source: str
    kind: str
    importance: float = 0.5
    reliability: float = 0.5
    created_at: datetime | None = None
    similarity: float = 0.0
    cluster_id: str | None = None
```

Odporúčané `kind` hodnoty:

```text
goal
episode
active_hypothesis
semantic_memory
search_result
system_note
project_anchor
code_context
user_profile
recent_event
```

---

## 6. Klastrovanie

Klastrovanie bráni tomu, aby jeden typ kontextu zožral celý prompt.

Bez klastrov môže napríklad search výsledok alebo stará epizóda vytlačiť všetky active hypotheses.

Prvý jednoduchý cluster key:

```python
def cluster_key(item: ContextItem) -> str:
    if item.kind in {"goal", "active_hypothesis", "episode", "search_result"}:
        return item.kind
    return item.source
```

Pokročilejší variant:

```text
cluster = semantic topic
cluster = source type
cluster = time window
cluster = project layer
cluster = reasoning state
```

---

## 7. Percentuálny podiel váhy

Každý klaster dostane časť context budgetu podľa súčtu gravity scores svojich fragmentov.

```text
cluster_gravity = sum(gravity(item) for item in cluster)

cluster_budget_share =
    cluster_gravity / sum(all_cluster_gravities)

cluster_budget =
    CONTEXT_BUDGET * cluster_budget_share
```

Tým vznikne presne mechanizmus:

```text
kontext sa vyberá podľa obsahu, váhy a sémantickej gravitácie
```

Nie podľa toho, čo sa do promptu dostalo prvé.

---

## 8. PromptBudget

Prompt budget sa musí počítať pred skladaním promptu.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class PromptBudget:
    max_chars: int
    safety_margin: int
    template_chars: int
    user_input_chars: int
    state_chars: int

    @property
    def context_chars(self) -> int:
        return max(
            0,
            self.max_chars
            - self.safety_margin
            - self.template_chars
            - self.user_input_chars
            - self.state_chars,
        )
```

Použitie:

```python
budget = PromptBudget(
    max_chars=MAX_PROMPT_LENGTH,
    safety_margin=800,
    template_chars=len(template),
    user_input_chars=len(user_input),
    state_chars=len(state_instructions),
)

context = build_context(
    query=user_input,
    max_chars=budget.context_chars,
)
```

---

## 9. Tokeny namiesto znakov

Ak systém používa LLM s tokenovým limitom, `MAX_PROMPT_LENGTH` v znakoch je iba približný signál.

Lepšie:

```text
MAX_PROMPT_TOKENS
```

Ak nie je dostupný tokenizer:

```python
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
```

Ak je dostupný tokenizer:

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))
```

Odporúčanie:

```text
Ak sa používa znakový limit, safety margin má byť aspoň 20–30 %.
```

---

## 10. Reference implementation: scoring

```python
from datetime import datetime
from math import exp


def recency_score(item: ContextItem, now: datetime) -> float:
    if item.created_at is None:
        return 0.3

    age_days = max((now - item.created_at).days, 0)
    return exp(-age_days / 30)


def continuity_score(item: ContextItem) -> float:
    if item.kind in {"goal", "active_hypothesis", "current_project"}:
        return 1.0
    if item.kind in {"episode", "search_result"}:
        return 0.6
    return 0.4


def gravity_score(item: ContextItem, now: datetime) -> float:
    return (
        0.45 * item.similarity
        + 0.20 * item.importance
        + 0.15 * recency_score(item, now)
        + 0.10 * item.reliability
        + 0.10 * continuity_score(item)
    )
```

---

## 11. Reference implementation: selection

```python
from typing import Iterable


def select_context_items(
    items: Iterable[ContextItem],
    max_chars: int,
    now: datetime,
) -> tuple[list[ContextItem], dict]:
    scored = [
        (gravity_score(item, now), item)
        for item in items
        if item.text.strip()
    ]

    scored.sort(key=lambda pair: pair[0], reverse=True)

    selected: list[ContextItem] = []
    used_chars = 0
    skipped = []

    for score, item in scored:
        item_len = len(item.text)

        if item_len > max_chars * 0.35:
            skipped.append({
                "id": item.id,
                "reason": "single_item_too_large",
                "chars": item_len,
            })
            continue

        if used_chars + item_len > max_chars:
            skipped.append({
                "id": item.id,
                "reason": "context_budget_exceeded",
                "chars": item_len,
            })
            continue

        selected.append(item)
        used_chars += item_len

    report = {
        "candidate_count": len(scored),
        "selected_count": len(selected),
        "skipped_count": len(skipped),
        "used_chars": used_chars,
        "max_chars": max_chars,
        "skipped": skipped[:20],
    }

    return selected, report
```

---

## 12. Reference implementation: rendering

```python
def render_context(items: list[ContextItem]) -> str:
    if not items:
        return "No relevant bounded context selected."

    blocks = []

    for item in items:
        blocks.append(
            f"[{item.kind.upper()} | {item.source} | {item.id}]\\n"
            f"{item.text.strip()}"
        )

    return "\\n\\n---\\n\\n".join(blocks)
```

---

## 13. Reference implementation: cluster budget allocation

```python
def allocate_cluster_budgets(
    items: list[ContextItem],
    total_budget: int,
    now: datetime,
) -> dict[str, int]:
    cluster_scores: dict[str, float] = {}

    for item in items:
        key = cluster_key(item)
        cluster_scores[key] = cluster_scores.get(key, 0.0) + gravity_score(item, now)

    total_score = sum(cluster_scores.values()) or 1.0

    budgets = {
        key: max(300, int(total_budget * score / total_score))
        for key, score in cluster_scores.items()
    }

    scale = total_budget / max(sum(budgets.values()), 1)

    return {
        key: int(value * scale)
        for key, value in budgets.items()
    }
```

---

## 14. Reference implementation: clustered selection

```python
def select_clustered_context(
    items: list[ContextItem],
    max_chars: int,
    now: datetime,
) -> tuple[str, dict]:
    budgets = allocate_cluster_budgets(items, max_chars, now)

    selected_all: list[ContextItem] = []
    reports = {}

    for key, budget in budgets.items():
        cluster_items = [
            item for item in items
            if cluster_key(item) == key
        ]

        selected, report = select_context_items(
            items=cluster_items,
            max_chars=budget,
            now=now,
        )

        selected_all.extend(selected)
        reports[key] = report

    selected_all.sort(
        key=lambda item: gravity_score(item, now),
        reverse=True,
    )

    context_text = render_context(selected_all)

    if len(context_text) > max_chars:
        context_text = (
            context_text[:max_chars].rstrip()
            + "\\n\\n[CONTEXT TRUNCATED AFTER BUDGETED SELECTION]"
        )

    return context_text, {
        "cluster_budgets": budgets,
        "cluster_reports": reports,
        "final_context_chars": len(context_text),
        "max_context_chars": max_chars,
    }
```

---

## 15. Reference implementation: budget-aware prompt builder

```python
MAX_PROMPT_LENGTH = 8000
MAX_INPUT_LENGTH = 4000
PROMPT_SAFETY_MARGIN = 800


def build_prompt(
    user_input: str,
    state_name: str,
    context_provider,
) -> tuple[str, dict]:
    base_template_without_context = f"""
You are reasoning in state: {state_name}

User input:
{user_input}

Relevant context:
""".strip()

    closing_template = """

Return a clear answer.
""".strip()

    available_context_chars = (
        MAX_PROMPT_LENGTH
        - len(base_template_without_context)
        - len(closing_template)
        - PROMPT_SAFETY_MARGIN
    )

    if available_context_chars < 0:
        return (
            "[INPUT TOO LONG]",
            {
                "status": "failed",
                "reason": "user_input_or_template_exceeds_prompt_budget",
                "available_context_chars": available_context_chars,
            },
        )

    context, context_report = context_provider.build_context(
        query=user_input,
        max_chars=available_context_chars,
    )

    prompt = f"""
{base_template_without_context}
{context}

{closing_template}
""".strip()

    if len(prompt) > MAX_PROMPT_LENGTH:
        compressed_context, compression_report = context_provider.compress_context(
            context=context,
            max_chars=max(0, available_context_chars // 2),
        )

        prompt = f"""
{base_template_without_context}
{compressed_context}

{closing_template}
""".strip()

        context_report["compression"] = compression_report

    if len(prompt) > MAX_PROMPT_LENGTH:
        return (
            "[PROMPT ASSEMBLY FAILED]",
            {
                "status": "failed",
                "reason": "context_could_not_be_compressed_within_budget",
                "prompt_chars": len(prompt),
                "max_prompt_chars": MAX_PROMPT_LENGTH,
            },
        )

    return (
        prompt,
        {
            "status": "ok",
            "prompt_chars": len(prompt),
            "max_prompt_chars": MAX_PROMPT_LENGTH,
            "context_report": context_report,
        },
    )
```

---

## 16. Fail-soft degradation

Zakázaný režim:

```text
[PROMPT TOO LONG]
[PROMPT TOO LONG]
[PROMPT TOO LONG]
[PROMPT TOO LONG]
[PROMPT TOO LONG]
```

Správna degradačná kaskáda:

```text
full context
    ↓
budgeted context
    ↓
cluster summaries
    ↓
top-k memory fragments
    ↓
no context, direct answer
```

Ak systém nedokáže použiť celý kontext, má postupovať takto:

```text
1. vybrať relevantné klastre
2. vynechať nízko relevantné fragmenty
3. komprimovať priveľké fragmenty
4. použiť top-k fragmenty
5. odpovedať bez interného kontextu, ak inak nemožno
6. používateľovi ukazať interný debug marker
```

Používateľsky vhodná poznámka:

```text
Poznámka: Interný kontext bol automaticky zúžený podľa relevancie, aby sa zmestil do promptového rozpočtu.
```

Nevhodná odpoveď:

```text
[PROMPT TOO LONG]
```

---

## 17. Degradation Report

Systém má mať interný report:

```json
{
  "prompt_chars": 7214,
  "max_prompt_chars": 8000,
  "context_chars": 2480,
  "selected_clusters": {
    "active_hypotheses": 820,
    "semantic_memory": 740,
    "episodes": 520,
    "search_results": 400
  },
  "skipped_items": 17,
  "compression_applied": true
}
```

Report slúži na debugging, audit a transparentnosť.

Report nesmie byť interpretovaný ako truth verdict.

---

## 18. Používateľská komunikácia

Používateľ nesmie byť obviňovaný za interný context overflow.

Zlá formulácia:

```text
Tvoj prompt je príliš dlhý.
```

Lepšia formulácia:

```text
Interný kontext bol príliš veľký, preto som použil iba najrelevantnejšie časti.
```

Najlepšie správanie:

```text
Systém context overflow vyrieši automaticky a používateľ dostane normálnu odpoveď.
```

---

## 19. Testy

### Test 1: krátky input, obrovský context

```python
def test_short_input_large_context_does_not_return_prompt_too_long():
    user_input = "Ahoj, vysvetli mi stav."
    huge_context = ["x" * 5000 for _ in range(20)]

    prompt, report = build_prompt_with_budget(
        user_input=user_input,
        context_items=huge_context,
        state_name="AA",
    )

    assert "[PROMPT TOO LONG]" not in prompt
    assert len(prompt) <= MAX_PROMPT_LENGTH
    assert report["status"] == "ok"
```

### Test 2: context report obsahuje vynechané položky

```python
def test_context_selection_reports_skipped_items():
    result = build_context(
        query="test",
        max_chars=1000,
    )

    assert "skipped_count" in result.report
```

### Test 3: všetkých 5 stavov nesmie zlyhať naraz kvôli tomu istému contextu

```python
def test_all_reasoning_states_have_independent_context_budget():
    states = ["AA", "AN", "NA", "NN", "QE"]

    outputs = [
        reason_in_state(state, user_input="krátka otázka")
        for state in states
    ]

    assert not all("[PROMPT TOO LONG]" in output for output in outputs)
```

### Test 4: final prompt nikdy neprekročí limit

```python
def test_final_prompt_never_exceeds_max_prompt_length():
    prompt, report = build_prompt(...)
    assert len(prompt) <= MAX_PROMPT_LENGTH
```

---

## 20. Odporúčaná štruktúra modulov

Minimálne:

```text
core/
  reasoning.py
  context.py
```

Lepšie:

```text
core/
  reasoning.py
  context.py
  prompt_budget.py
  context_budget.py
  context_scoring.py
  context_clustering.py
```

Rozdelenie zodpovedností:

| Modul | Zodpovednosť |
|---|---|
| `reasoning.py` | zostavenie promptu, volanie LLM, stavové reasoning režimy |
| `prompt_budget.py` | výpočet dostupného budgetu |
| `context.py` | zber kandidátnych fragmentov |
| `context_scoring.py` | semantic gravity scoring |
| `context_clustering.py` | klastre a cluster budget allocation |
| `context_budget.py` | výber, orezanie, kompresia, report |

---

## 21. Implementačný plán

Najmenší bezpečný postup:

```text
1. Pridať PromptBudget.
2. Zmeniť build_prompt tak, aby počítal context_budget.
3. Upraviť build_context(query, max_chars).
4. Zaviesť ContextItem.
5. Pridať gravity_score.
6. Pridať cluster budget allocation.
7. Odstrániť používateľsky viditeľné [PROMPT TOO LONG].
8. Pridať context selection report.
9. Pridať testy na oversized context.
```

---

## 22. VECTAETOS compatibility

Táto teória patrí do downstream vrstvy:

```text
LLM Adapter / Context Assembly Layer
```

Nepatrí do:

```text
Φ
K(Φ)
κ
QE
Vortex core
RMK
ZMYSEL / Ξ
```

Semantic gravity nesmie byť interpretovaná ako ontologická sila v core.

Cluster priority nesmie byť interpretovaná ako dominancia singularity.

Context selection nesmie spätne meniť Φ.

Prompt budget nesmie byť chápaný ako κ.

Compression nesmie meniť vyššiu vrstvu.

Correct reading:

```text
Semantic Gravity Context Budgeting je pracovná disciplína pre bezpečné skladanie promptu.
Nie je to mechanizmus VECTAETOS core.
```

---

## 23. Anti-drift pravidlá

```text
1. Context selector nesmie tvrdiť pravdu.
2. Context selector iba vyberá reprezentovateľné fragmenty.
3. Gravity score nie je hodnota pravdivosti.
4. Cluster priority nie je ontologická priorita.
5. Vynechaný kontext nie je zamietnutý kontext.
6. Kompresia nesmie vytvárať nové fakty.
7. Prompt builder nesmie ticho zlyhať.
8. Používateľský vstup nesmie byť obviňovaný za interný context overflow.
9. Klastrovanie nesmie zavádzať skrytú autoritu.
10. Budget nesmie byť maskovaný ako epistemický verdikt.
11. Fail-soft režim nesmie predstierať, že použil celý kontext.
12. Audit report nesmie byť rozhodnutím.
```

---

## 24. Canonical formulations

```text
Kontext nie je skladisko. Kontext je výber pod rozpočtom.
```

```text
Nezvyšuj limit. Zaveď významovo vážený rozpočet.
```

```text
Prompt sa nemá skracovať až po zlyhaní.
Prompt sa má skladať tak, aby zlyhanie nebolo potrebné.
```

```text
MAX_INPUT_LENGTH chráni vstup.
MAX_PROMPT_LENGTH chráni LLM call.
CONTEXT_BUDGET chráni prompt builder.
SEMANTIC_GRAVITY vyberá, čo je hodné reprezentácie.
CLUSTERING bráni tomu, aby jeden typ pamäte zožral celý prompt.
DEGRADATION_REPORT bráni tichému zlyhaniu.
```

```text
Gravity score nie je truth score.
```

```text
Vynechaný kontext nie je zamietnutý kontext.
```

---

## 25. Final theorem

### Theorem: Prompt-Safe Context Assembly

A reasoning system is prompt-safe if no user input that satisfies `MAX_INPUT_LENGTH` can cause silent global reasoning degradation solely because internal memory, context, or retrieval results exceed the prompt limit.

This requires:

```text
1. bounded context retrieval
2. explicit context budget
3. semantic selection
4. cluster diversity
5. compression fallback
6. final prompt preflight
7. transparent degradation report
8. no user-visible raw debug marker
```

### Corollary

A system with bounded user input but unbounded internal context is not defensively designed.

### Strong form

```text
Prompt overflow is not a user error.
Prompt overflow is a context assembly failure.
```

---

## 26. Final verdict

Tento návrh mení problém z limit-checkingu na architektúru významového rozpočtu.

Pôvodný problém:

```text
prompt too long
```

Skutočný problém:

```text
context unmanaged
```

Správne riešenie:

```text
semantic gravity context budgeting
```

Najkratšia finálna veta:

```text
Prompt sa nemá skladať z toho, čo systém má.
Prompt sa má skladať z toho, čo je pod rozpočtom najviac relevantné.
```
