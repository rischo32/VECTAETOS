# LLM_CONTEXT_SWAP_AND_TASK_LEDGER

**Status:** accepted working adapter / non-core  
**Layer:** LLM Adapter / Context Assembly / External Workspace  
**Scope:** ASI_MOD™ / VECTAETOS-compatible long task support  
**Core impact:** none  
**Feedback into Φ:** none  
**Authority:** none  
**Agency:** none  
**Optimization:** none  
**Decision power:** none  

---

## 0. Canonical Working Sentence

```text
LLM_CONTEXT_SWAP_AND_TASK_LEDGER preserves working continuity;
it does not create epistemic authority.
```

Slovensky:

```text
LLM_CONTEXT_SWAP_AND_TASK_LEDGER zachováva pracovnú kontinuitu;
nevytvára epistemickú autoritu.
```

---

## 1. Purpose

`LLM_CONTEXT_SWAP_AND_TASK_LEDGER` is a working-continuity adapter for long LLM-assisted tasks.

It supports:

- extra-long work sessions,
- task decomposition,
- explicit checkpoints,
- context parking,
- context rehydration,
- resumable task state,
- artifact indexing,
- drift notes,
- append-only working ledger.

It does **not** create memory inside Φ.  
It does **not** modify Φ, R, Vortex, K(Φ), κ, QE, anchors, or canonical layers.  
It does **not** decide truth.  
It does **not** rank epistemic states.  
It does **not** optimize trajectories.  
It does **not** run as an autonomous agent.

---

## 2. Architectural Boundary

Allowed direction:

```text
Φ → projection → audit/log → LLM adapter → ledger
```

Forbidden direction:

```text
ledger → Φ
ledger → Vortex
ledger → K(Φ)
ledger → κ
ledger → truth verdict
ledger → ontology update
```

The adapter belongs to the working surface:

```text
VECTAETOS core
  ↓ read-only projection
Audit / trace / external observables
  ↓
LLM Adapter
  ↓
LLM_CONTEXT_SWAP_AND_TASK_LEDGER
  ↓
Human working continuation
```

---

## 3. Non-Identity Clauses

```text
ledger ≠ truth
checkpoint ≠ canon
hash ≠ proof
swap ≠ memory of Φ
task status ≠ epistemic verdict
summary ≠ new fact
rehydration ≠ ontology reconstruction
index ≠ authority
worker ≠ agentic will
DAG ≠ decision system
```

---

## 4. Accepted Role

The adapter may act as:

```text
working notebook
context cache
task ledger
checkpoint manager
rehydration pack generator
artifact index
drift note register
DAG task surface
```

The adapter may not act as:

```text
truth memory
autonomous agent
runtime controller
Vortex selector
Φ modifier
κ score calculator
K(Φ) optimizer
audit-as-control mechanism
canonical authority
```

---

## 5. Relationship to Multi-Tasker

The multi-tasker is preserved, but constrained.

```text
LLM_CONTEXT_SWAP_AND_TASK_LEDGER
= working continuity, context swap, checkpoints, ledger

multi-tasker
= DAG structure, dependencies, task status, failure isolation
```

Safe translation:

```text
agent              → worker / callable
orchestrator       → task graph runner
persistent state   → working state
result             → working output, not verdict
completion         → task state, not epistemic proof
```

The multi-tasker is subordinate to the ledger/swap layer:

```text
ledger holds continuity
multi-tasker holds structure
human review holds interpretation
```

---

## 6. File Structure

Recommended workspace:

```text
long_task_support/
  LLM_CONTEXT_SWAP_AND_TASK_LEDGER.behavior.md
  llm_context_swap_and_task_ledger.py
  SESSION_STATE.md
  CONTEXT_SWAP.md
  TASK_LEDGER.jsonl
  TODO_DAG.json
  ARTIFACT_INDEX.json
  DRIFT_NOTES.md
  checkpoints/
    CHECKPOINT_0001.md
    CHECKPOINT_0002.md
```

### 6.1 File Roles

```text
SESSION_STATE.md
= short active state of the current work

CONTEXT_SWAP.md
= parked long context outside the active prompt

TASK_LEDGER.jsonl
= append-only working event ledger

TODO_DAG.json
= tasks, dependencies, task states

ARTIFACT_INDEX.json
= map of generated artifacts and references

DRIFT_NOTES.md
= warnings about possible conceptual drift

CHECKPOINT_N.md
= rehydration point for returning to work
```

---

## 7. Workflow

Canonical workflow:

```text
capture → canonicalize → hash → append → summarize → index → retrieve → rehydrate → audit
```

Expanded:

1. **capture**  
   Collect working state, current goal, relevant facts, assumptions, risks.

2. **canonicalize**  
   Serialize deterministic JSON or structured markdown.

3. **hash**  
   Produce integrity digest. Hash is provenance/integrity, not truth.

4. **append**  
   Add event to `TASK_LEDGER.jsonl`.

5. **summarize**  
   Compress only as a representation of existing content. No new facts.

6. **index**  
   Register artifacts, tasks, parked context, checkpoint paths.

7. **retrieve**  
   Load relevant state under context budget.

8. **rehydrate**  
   Build a compact rehydration pack.

9. **audit**  
   Detect obvious drift risks before continuing.

---

## 8. Rehydration Pack Contract

Every rehydration pack must separate:

```text
stable facts
working assumptions
open risks
parked context
active task
next safe step
```

Template:

```md
# REHYDRATION_PACK

## Boundary
- Restores working context only.
- Is not canon.
- Is not truth memory.
- Does not modify Φ.

## Stable facts
- ...

## Working assumptions
- ...

## Open risks
- ...

## Parked context
- CONTEXT_SWAP.md
- checkpoints/CHECKPOINT_0004.md

## Active task
- ...

## Next safe step
- ...
```

---

## 9. Behavior Contract

```md
# LLM_CONTEXT_SWAP_AND_TASK_LEDGER.behavior.md

Status: accepted working adapter / non-core  
Layer: LLM Adapter / Context Assembly / External Workspace  
Core impact: none  
Feedback into Φ: none  
Authority: none  
Agency: none  

## Purpose

LLM_CONTEXT_SWAP_AND_TASK_LEDGER supports long working tasks by preserving
working continuity through context snapshots, task ledgers, checkpoint files,
rehydration packs, and parked context.

It does not create memory inside Φ.
It does not modify Φ, R, Vortex, K(Φ), κ, QE, anchors, or canonical layers.
It does not decide truth.
It does not rank states.
It does not optimize epistemic trajectories.

## Canonical sentence

Working memory preserves continuity; it does not create epistemic authority.

## Allowed operations

capture
canonicalize
hash
append
summarize
index
retrieve
rehydrate
audit

## Forbidden interpretations

ledger ≠ truth
checkpoint ≠ canon
hash ≠ proof
swap ≠ memory of Φ
task status ≠ epistemic verdict
summary ≠ new fact
rehydration ≠ ontology reconstruction

## Rehydration pack

Every rehydration pack must separate:

- stable facts
- working assumptions
- open risks
- parked context
- active task
- next safe step

## Stop cases

Stop or fail-lower if the adapter is used as:

- truth memory
- autonomous agent
- runtime controller
- Vortex selector
- Φ modifier
- κ score
- K(Φ) numeric optimizer
- audit-as-control mechanism
```

---

## 10. Python Implementation

```python
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


TaskStatus = Literal["pending", "active", "blocked", "completed", "failed", "suspended"]

LedgerEventType = Literal[
    "session_start",
    "context_capture",
    "context_swap",
    "checkpoint",
    "task_add",
    "task_update",
    "artifact_add",
    "drift_note",
    "rehydration",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class LedgerEntry:
    event_type: LedgerEventType
    payload: dict[str, Any]
    created_at: str = field(default_factory=utc_now)
    previous_hash: str | None = None
    entry_hash: str | None = None

    def seal(self) -> "LedgerEntry":
        body = {
            "event_type": self.event_type,
            "payload": self.payload,
            "created_at": self.created_at,
            "previous_hash": self.previous_hash,
        }
        self.entry_hash = sha256_text(canonical_json(body))
        return self


@dataclass
class TaskNode:
    id: str
    title: str
    status: TaskStatus = "pending"
    dependencies: list[str] = field(default_factory=list)
    notes: str = ""
    result_ref: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass
class RehydrationPack:
    stable_facts: list[str]
    working_assumptions: list[str]
    open_risks: list[str]
    active_task: str | None
    parked_context_ref: str
    next_safe_step: str
    generated_at: str = field(default_factory=utc_now)


class LLMContextSwapAndTaskLedger:
    """
    Working-continuity adapter for long tasks.

    Boundary:
    - not memory inside Φ
    - not truth source
    - not autonomous controller
    - not ontology updater
    """

    def __init__(self, root: str | Path = "long_task_support") -> None:
        self.root = Path(root)
        self.checkpoints = self.root / "checkpoints"
        self.ledger_path = self.root / "TASK_LEDGER.jsonl"
        self.task_path = self.root / "TODO_DAG.json"
        self.session_path = self.root / "SESSION_STATE.md"
        self.swap_path = self.root / "CONTEXT_SWAP.md"
        self.artifact_index_path = self.root / "ARTIFACT_INDEX.json"
        self.drift_notes_path = self.root / "DRIFT_NOTES.md"
        self._ensure_workspace()

    def _ensure_workspace(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self.checkpoints.mkdir(parents=True, exist_ok=True)

        if not self.task_path.exists():
            self._write_json(self.task_path, {"tasks": {}})

        if not self.artifact_index_path.exists():
            self._write_json(self.artifact_index_path, {"artifacts": []})

        for path, title in [
            (self.session_path, "# SESSION_STATE\n\n"),
            (self.swap_path, "# CONTEXT_SWAP\n\n"),
            (self.drift_notes_path, "# DRIFT_NOTES\n\n"),
        ]:
            if not path.exists():
                path.write_text(title, encoding="utf-8")

    def _read_json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, data: dict[str, Any]) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _last_hash(self) -> str | None:
        if not self.ledger_path.exists():
            return None

        lines = [
            line
            for line in self.ledger_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        if not lines:
            return None

        try:
            return json.loads(lines[-1]).get("entry_hash")
        except json.JSONDecodeError:
            return None

    def append_event(self, event_type: LedgerEventType, payload: dict[str, Any]) -> LedgerEntry:
        entry = LedgerEntry(
            event_type=event_type,
            payload=payload,
            previous_hash=self._last_hash(),
        ).seal()

        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(canonical_json(asdict(entry)) + "\n")

        return entry

    def save_session_state(
        self,
        *,
        active_goal: str,
        stable_facts: list[str],
        open_risks: list[str],
        next_safe_step: str,
    ) -> None:
        body = [
            "# SESSION_STATE",
            "",
            f"Updated: {utc_now()}",
            "",
            "## Active goal",
            active_goal,
            "",
            "## Stable facts",
            *[f"- {item}" for item in stable_facts],
            "",
            "## Open risks",
            *[f"- {item}" for item in open_risks],
            "",
            "## Next safe step",
            next_safe_step,
            "",
        ]

        self.session_path.write_text("\n".join(body), encoding="utf-8")

        self.append_event(
            "context_capture",
            {
                "active_goal": active_goal,
                "stable_facts_count": len(stable_facts),
                "open_risks_count": len(open_risks),
                "next_safe_step": next_safe_step,
            },
        )

    def park_context(self, title: str, content: str) -> str:
        digest = sha256_text(content)

        block = [
            "",
            f"## {title}",
            f"Captured: {utc_now()}",
            f"Content-SHA256: {digest}",
            "",
            content,
            "",
        ]

        with self.swap_path.open("a", encoding="utf-8") as f:
            f.write("\n".join(block))

        self.append_event(
            "context_swap",
            {
                "title": title,
                "content_hash": digest,
                "target": str(self.swap_path),
            },
        )

        return digest

    def add_task(
        self,
        task_id: str,
        title: str,
        *,
        dependencies: list[str] | None = None,
        notes: str = "",
    ) -> TaskNode:
        data = self._read_json(self.task_path)
        tasks = data.setdefault("tasks", {})

        if task_id in tasks:
            raise ValueError(f"Task already exists: {task_id}")

        task = TaskNode(
            id=task_id,
            title=title,
            dependencies=dependencies or [],
            notes=notes,
        )

        tasks[task_id] = asdict(task)
        self._write_json(self.task_path, data)

        self.append_event(
            "task_add",
            {
                "task_id": task_id,
                "title": title,
                "dependencies": dependencies or [],
            },
        )

        return task

    def update_task(
        self,
        task_id: str,
        *,
        status: TaskStatus | None = None,
        notes: str | None = None,
        result_ref: str | None = None,
    ) -> TaskNode:
        data = self._read_json(self.task_path)
        tasks = data.setdefault("tasks", {})

        if task_id not in tasks:
            raise KeyError(f"Unknown task: {task_id}")

        raw = tasks[task_id]

        if status is not None:
            raw["status"] = status
        if notes is not None:
            raw["notes"] = notes
        if result_ref is not None:
            raw["result_ref"] = result_ref

        raw["updated_at"] = utc_now()
        tasks[task_id] = raw
        self._write_json(self.task_path, data)

        self.append_event(
            "task_update",
            {
                "task_id": task_id,
                "status": raw["status"],
                "result_ref": raw.get("result_ref"),
            },
        )

        return TaskNode(**raw)

    def add_artifact(self, name: str, path: str, kind: str, note: str = "") -> None:
        data = self._read_json(self.artifact_index_path)

        artifact = {
            "name": name,
            "path": path,
            "kind": kind,
            "note": note,
            "created_at": utc_now(),
        }

        data.setdefault("artifacts", []).append(artifact)
        self._write_json(self.artifact_index_path, data)

        self.append_event("artifact_add", artifact)

    def create_checkpoint(
        self,
        *,
        name: str,
        stable_facts: list[str],
        working_assumptions: list[str],
        open_risks: list[str],
        active_task: str | None,
        next_safe_step: str,
    ) -> Path:
        existing = sorted(self.checkpoints.glob("CHECKPOINT_*.md"))
        number = len(existing) + 1
        path = self.checkpoints / f"CHECKPOINT_{number:04d}.md"

        pack = RehydrationPack(
            stable_facts=stable_facts,
            working_assumptions=working_assumptions,
            open_risks=open_risks,
            active_task=active_task,
            parked_context_ref=str(self.swap_path),
            next_safe_step=next_safe_step,
        )

        body = [
            f"# CHECKPOINT_{number:04d}: {name}",
            "",
            f"Generated: {pack.generated_at}",
            "",
            "## Boundary",
            "- Restores working context only.",
            "- Is not canon.",
            "- Is not truth memory.",
            "- Does not modify Φ.",
            "",
            "## Stable facts",
            *[f"- {item}" for item in stable_facts],
            "",
            "## Working assumptions",
            *[f"- {item}" for item in working_assumptions],
            "",
            "## Open risks",
            *[f"- {item}" for item in open_risks],
            "",
            "## Active task",
            active_task or "None",
            "",
            "## Parked context",
            str(self.swap_path),
            "",
            "## Next safe step",
            next_safe_step,
            "",
        ]

        path.write_text("\n".join(body), encoding="utf-8")

        self.append_event(
            "checkpoint",
            {
                "name": name,
                "path": str(path),
                "active_task": active_task,
                "next_safe_step": next_safe_step,
            },
        )

        return path

    def make_rehydration_pack(self, max_chars: int = 6000) -> str:
        session = self.session_path.read_text(encoding="utf-8")
        tasks = self._read_json(self.task_path)
        artifacts = self._read_json(self.artifact_index_path)
        drift = self.drift_notes_path.read_text(encoding="utf-8")

        pack = [
            "# REHYDRATION_PACK",
            "",
            "## Boundary",
            "- This pack restores working context only.",
            "- It is not canon.",
            "- It is not truth memory.",
            "- It does not modify Φ.",
            "",
            "## Session",
            session,
            "",
            "## Task DAG",
            json.dumps(tasks, ensure_ascii=False, indent=2),
            "",
            "## Artifact index",
            json.dumps(artifacts, ensure_ascii=False, indent=2),
            "",
            "## Drift notes",
            drift,
            "",
        ]

        text = "\n".join(pack)

        self.append_event(
            "rehydration",
            {
                "max_chars": max_chars,
                "full_chars": len(text),
                "truncated": len(text) > max_chars,
            },
        )

        if len(text) <= max_chars:
            return text

        return text[:max_chars] + "\n\n[TRUNCATED: context budget reached. Use checkpoint or swap file.]"

    def add_drift_note(self, note: str) -> None:
        with self.drift_notes_path.open("a", encoding="utf-8") as f:
            f.write(f"\n- {utc_now()} — {note}")

        self.append_event("drift_note", {"note": note})

    def audit_guard(self) -> list[str]:
        """
        Guard check for obvious conceptual misuse.

        Returns warnings, not verdicts.
        """
        warnings: list[str] = []

        texts = [
            self.session_path.read_text(encoding="utf-8"),
            self.swap_path.read_text(encoding="utf-8"),
            self.drift_notes_path.read_text(encoding="utf-8"),
        ]

        combined = "\n".join(texts).lower()

        risky_phrases = [
            "ledger proves truth",
            "checkpoint is canon",
            "memory modifies phi",
            "memory modifies Φ",
            "κ score",
            "k(phi) score",
            "vortex control",
            "autonomous decision",
            "hash proves truth",
            "audit controls runtime",
        ]

        for phrase in risky_phrases:
            if phrase.lower() in combined:
                warnings.append(f"drift_risk_detected: {phrase}")

        return warnings
```

---

## 11. Minimal Usage

```python
ledger = LLMContextSwapAndTaskLedger()

ledger.save_session_state(
    active_goal="Navrhnúť LLM_CONTEXT_SWAP_AND_TASK_LEDGER",
    stable_facts=[
        "Adapter patrí do LLM Adapter / Context Assembly.",
        "Nezasahuje do Φ, R, Vortex, K(Φ), κ ani QE.",
        "Ledger zachováva kontinuitu, nie pravdu.",
    ],
    open_risks=[
        "Zamieňať checkpoint za kánon.",
        "Zamieňať task status za verdikt.",
        "Zamieňať swap za ontologickú pamäť.",
    ],
    next_safe_step="Vytvoriť behavior kontrakt a Python skeleton.",
)

ledger.park_context(
    title="Long design notes",
    content="Sem patria dlhé poznámky mimo aktívneho prompt okna.",
)

ledger.add_task(
    task_id="T001",
    title="Napísať behavior kontrakt",
)

ledger.add_task(
    task_id="T002",
    title="Implementovať Python skeleton",
    dependencies=["T001"],
)

checkpoint = ledger.create_checkpoint(
    name="Initial adapter design",
    stable_facts=[
        "Pamäť je pracovná kontinuita.",
        "Multi-tasker ostáva ako DAG disciplína.",
    ],
    working_assumptions=[
        "Workspace zápis je povolený mimo jadra.",
    ],
    open_risks=[
        "memory → will",
        "audit → control",
    ],
    active_task="T001",
    next_safe_step="Doplniť testy.",
)

print(checkpoint)
print(ledger.make_rehydration_pack())
```

---

## 12. Tests

```python
from pathlib import Path


def test_hash_is_stable():
    a = canonical_json({"b": 2, "a": 1})
    b = canonical_json({"a": 1, "b": 2})
    assert a == b
    assert sha256_text(a) == sha256_text(b)


def test_task_add_and_update(tmp_path: Path):
    ledger = LLMContextSwapAndTaskLedger(tmp_path)

    ledger.add_task("T001", "First task")
    task = ledger.update_task("T001", status="completed", result_ref="artifact.md")

    assert task.status == "completed"
    assert task.result_ref == "artifact.md"


def test_rehydration_pack_contains_boundary(tmp_path: Path):
    ledger = LLMContextSwapAndTaskLedger(tmp_path)
    pack = ledger.make_rehydration_pack()

    assert "This pack restores working context only" in pack
    assert "It does not modify Φ" in pack


def test_checkpoint_is_created(tmp_path: Path):
    ledger = LLMContextSwapAndTaskLedger(tmp_path)

    checkpoint = ledger.create_checkpoint(
        name="Test",
        stable_facts=["A"],
        working_assumptions=["B"],
        open_risks=["C"],
        active_task="T001",
        next_safe_step="Continue",
    )

    assert checkpoint.exists()
    text = checkpoint.read_text(encoding="utf-8")
    assert "Restores working context only" in text


def test_guard_detects_risk(tmp_path: Path):
    ledger = LLMContextSwapAndTaskLedger(tmp_path)

    ledger.park_context(
        title="Bad statement",
        content="checkpoint is canon",
    )

    warnings = ledger.audit_guard()

    assert warnings
```

---

## 13. Drift Audit Checklist

Before using the adapter, check:

```text
[ ] Are we treating ledger as continuity, not truth?
[ ] Are checkpoints marked as working state, not canon?
[ ] Are hashes described as integrity/provenance only?
[ ] Are summaries prevented from creating new facts?
[ ] Is the multi-tasker a DAG discipline, not an autonomous agent?
[ ] Is there no feedback into Φ?
[ ] Is there no Vortex selection?
[ ] Is κ not used as score?
[ ] Is K(Φ) not used as numeric optimizer?
[ ] Is human interpretation kept separate from artifact output?
```

---

## 14. Stop Conditions

Stop or fail-lower if any of these appear:

```text
guard = truth
contract = ontology
CI = proof
hash = truth
ledger = truth witness
EK event = decision
feedback into Φ
Vortex selection
κ = score / threshold
K(Φ) = numeric target
QE = exception
audit = runtime controller
gravity = truth
prompt budget = κ
compression = synthesis
checkpoint = canon
memory = will
```

---

## 15. Recommended Repository Path

```text
skills/long_task_support/LLM_CONTEXT_SWAP_AND_TASK_LEDGER.behavior.md
skills/long_task_support/llm_context_swap_and_task_ledger.py
```

Alternative if kept as research artifact:

```text
research/LLM_CONTEXT_SWAP_AND_TASK_LEDGER.md
```

Alternative if kept as working adapter:

```text
adapters/llm_context_swap_and_task_ledger/
```

---

## 16. Final Invariant

```text
Rehydration restores working orientation.
It does not restore ontology.
```

Slovensky:

```text
Rehydratácia obnovuje pracovnú orientáciu.
Neobnovuje ontológiu.
```
