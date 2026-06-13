# vectaetos_lsp.py
# Python 3.11+
"""
VECTAETOS Code Sentinel LSP prototype.

Research prototype for local editor diagnostics in VECTAETOS-related Python code.

It is NOT:
- a truth validator
- a deployment validator
- an optimizer
- a decision engine
- a canonical guard
- an authority over Φ, K(Φ), κ, QE, Vortex, Projection, EK, or human judgment

It only exposes possible semantic drift for human review.

Current capabilities:
- AST-based detection of agentic / optimization fragments in names
- assignment checks for protected ontology identifiers in restricted roles
- dynamic execution detection
- Jedi completions
- optional explicit dual-hash ledger helper

Ledger note:
The ledger never writes automatically from diagnostics.
A ledger write requires an explicit call to commit_trajectory_trace().
"""

from __future__ import annotations

import ast
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import jedi
from lsprotocol.types import (
    CompletionItem,
    CompletionList,
    CompletionParams,
    Diagnostic,
    DiagnosticSeverity,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    Position,
    Range,
)
from pygls.features import COMPLETION, TEXT_DOCUMENT_DID_OPEN, TEXT_DOCUMENT_DID_SAVE
from pygls.server import LanguageServer


# ---------- Config ----------
CONTRACT_PATH = Path("contracts/vectaetos_code_contract.json")
LEDGER_PATH = Path(".vectaetos/ledger.log")
MAX_WORKERS = 2


# ---------- LSP server ----------
server = LanguageServer("vectaetos-code-sentinel-lsp", "0.3.0")
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)


# ---------- Deterministic serialization and hashing ----------
def deterministic_serialize(obj: Any) -> bytes:
    """Serialize objects with sorted keys and stable float formatting."""
    def _clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: _clean(value[key]) for key in sorted(value)}
        if isinstance(value, (list, tuple)):
            return [_clean(item) for item in value]
        if isinstance(value, float):
            return format(value, ".12g")
        return value

    text = json.dumps(_clean(obj), separators=(",", ":"), ensure_ascii=False)
    return text.encode("utf-8")


def dual_hash(data: bytes) -> Tuple[str, str]:
    """Return SHA-256 and SHA3-512 hex fingerprints."""
    return hashlib.sha256(data).hexdigest(), hashlib.sha3_512(data).hexdigest()


# ---------- Ledger (append-only, explicit only) ----------
class Ledger:
    """
    Append-only audit ledger.

    This helper is deliberately passive.
    It does not run from diagnostics and must not become enforcement.
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def commit(self, meta: Dict[str, Any]) -> Dict[str, str]:
        """
        Commit an explicit audit trace.

        The timestamp makes the record time-bound and non-replay-deterministic.
        The serializer is deterministic for payload shape, but the event itself is
        intentionally tied to time.
        """
        payload = {"meta": meta, "ts": time.time()}
        data = deterministic_serialize(payload)
        sha256, sha3 = dual_hash(data)

        record = {
            "ts": payload["ts"],
            "sha256": sha256,
            "sha3": sha3,
            "meta": meta,
        }

        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n")

        return {"sha256": sha256, "sha3": sha3}


ledger = Ledger(LEDGER_PATH)


# ---------- Contract loader ----------
def load_contract(path: Path = CONTRACT_PATH) -> Dict[str, Any]:
    """
    Load an optional contract file.

    Current prototype keeps rules embedded.
    Future versions may externalize protected names, role rules, and severities.
    """
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


contract = load_contract()


# ---------- Rule engine / epistemic checks ----------
PROTECTED_ONTOLOGY_NAMES = {
    "PHI",
    "Phi",
    "K",
    "K_PHI",
    "KPhi",
    "KAPPA",
    "kappa",
    "QE",
}

FORBIDDEN_FRAGMENTS = (
    "decide",
    "decision",
    "recommend",
    "optimize",
    "reward",
    "policy_update",
    "best_trajectory",
    "select_best",
    "rank",
    "argmax",
    "argmin",
)

RESTRICTED_MUTATION_ROLES = {"vortex", "projection", "adapter"}


def infer_role_from_uri(uri: Optional[str]) -> str:
    """
    Heuristically infer role from URI/path.

    This is a research heuristic, not a canonical classifier.
    """
    if not uri:
        return "utility"

    text = uri
    if uri.startswith("file://"):
        parsed = urlparse(uri)
        text = parsed.path or uri

    lowered = text.lower()

    if "vortex" in lowered:
        return "vortex"
    if "projection" in lowered or "glyph" in lowered:
        return "projection"
    if "audit" in lowered or "guard" in lowered:
        return "audit"
    if "adapter" in lowered or "llm" in lowered:
        return "adapter"
    if "test_" in lowered or "/tests/" in lowered:
        return "test"

    return "utility"


def make_diag(
    node: ast.AST,
    message: str,
    severity: DiagnosticSeverity = DiagnosticSeverity.Error,
) -> Diagnostic:
    """Create a one-character LSP diagnostic at node location."""
    lineno = getattr(node, "lineno", 1) - 1
    col = getattr(node, "col_offset", 0)

    return Diagnostic(
        range=Range(
            start=Position(line=lineno, character=col),
            end=Position(line=lineno, character=col + 1),
        ),
        message=message,
        severity=severity,
        source="VectaetosCodeSentinel",
    )


def analyze_source(uri: str, source: str) -> List[Diagnostic]:
    """
    Analyze Python source for semantic drift.

    Diagnostics are advisory. They do not validate or invalidate code.
    """
    diagnostics: List[Diagnostic] = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        # LSP clients already show syntax errors.
        return diagnostics

    role = infer_role_from_uri(uri)

    for node in ast.walk(tree):
        # Forbidden fragments in function/class definitions.
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = getattr(node, "name", "")
            lower_name = name.lower()
            if any(fragment in lower_name for fragment in FORBIDDEN_FRAGMENTS):
                diagnostics.append(
                    make_diag(
                        node,
                        f"ONTOLOGICAL_DRIFT: forbidden agentic fragment in definition name '{name}'",
                        DiagnosticSeverity.Warning,
                    )
                )

        # Forbidden fragments in variable names.
        if isinstance(node, ast.Name):
            identifier = node.id
            lower_identifier = identifier.lower()
            if any(fragment in lower_identifier for fragment in FORBIDDEN_FRAGMENTS):
                diagnostics.append(
                    make_diag(
                        node,
                        f"ONTOLOGICAL_DRIFT: forbidden token '{identifier}'",
                        DiagnosticSeverity.Warning,
                    )
                )

        # Protected ontology name assignments in restricted roles.
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets: List[ast.expr]
            if isinstance(node, ast.Assign):
                targets = list(node.targets)
            else:
                targets = [node.target]

            for target in targets:
                if isinstance(target, ast.Name):
                    if target.id in PROTECTED_ONTOLOGY_NAMES and role in RESTRICTED_MUTATION_ROLES:
                        diagnostics.append(
                            make_diag(
                                target,
                                f"PHI_MUTATION: assignment to protected ontology name '{target.id}' in role '{role}'",
                                DiagnosticSeverity.Error,
                            )
                        )

        # Dynamic execution calls.
        if isinstance(node, ast.Call):
            func = node.func
            name = ""

            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr

            if name in {"eval", "exec", "compile", "__import__"}:
                diagnostics.append(
                    make_diag(
                        node,
                        f"DYNAMIC_EXECUTION: forbidden call '{name}'",
                        DiagnosticSeverity.Error,
                    )
                )

    return diagnostics


# ---------- LSP handlers ----------
@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """Analyze a document after open."""
    doc = ls.workspace.get_document(params.text_document.uri)
    ls.loop.run_in_executor(executor, _analyze_and_publish, ls, doc)


@server.feature(TEXT_DOCUMENT_DID_SAVE)
async def did_save(ls: LanguageServer, params: DidSaveTextDocumentParams):
    """Analyze a document after save."""
    doc = ls.workspace.get_document(params.text_document.uri)
    ls.loop.run_in_executor(executor, _analyze_and_publish, ls, doc)


def _analyze_and_publish(ls: LanguageServer, doc: Any) -> None:
    diagnostics = analyze_source(doc.uri, doc.source)
    ls.publish_diagnostics(doc.uri, diagnostics)


@server.feature(COMPLETION)
def completions(ls: LanguageServer, params: CompletionParams) -> CompletionList:
    """Provide completions via Jedi."""
    doc = ls.workspace.get_document(params.text_document.uri)
    line = params.position.line + 1
    column = params.position.character

    try:
        script = jedi.Script(code=doc.source, path=str(doc.path) if doc.path else None)
        completions_ = script.complete(line, column)
    except Exception:
        return CompletionList(is_incomplete=False, items=[])

    items: List[CompletionItem] = []
    for completion in completions_:
        items.append(
            CompletionItem(
                label=completion.name,
                detail=completion.type or "",
                documentation=completion.description,
            )
        )

    return CompletionList(is_incomplete=False, items=items)


# ---------- Explicit audit helper ----------
def commit_trajectory_trace(meta: Dict[str, Any]) -> Dict[str, str]:
    """
    Explicitly commit a trajectory/audit trace.

    This must be called by a deliberate editor/user action.
    The LSP server does not call it automatically.
    """
    return ledger.commit(meta)


# ---------- Server start ----------
if __name__ == "__main__":
    server.start_io()
