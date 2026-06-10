---
name: vectaetos-sentinel
description: >
  VECTAETOS framework development assistant. Use this skill for ANY task involving
  VECTAETOS, ASIMULATOR, ASI_MOD, TetraGlyph, EpistemicCryptography, LSP Sentinel,
  CLI Behavior Audit, behavior contracts, role policies, Python code conformance
  to VECTAETOS anchors, or any work on the non-agentic epistemic architecture.
  Trigger whenever the user mentions: Φ, K(Φ), κ, QE, ZMYSEL, RMK, Vortex,
  projection layer, anchor, contract, drift detection, non-agentic, or any
  VECTAETOS component. This skill prevents semantic drift in code assistance.
---
 
# VECTAETOS Code Sentinel & Behavior Audit — Assistant Skill
 
## 0. Pozícia asistenta
 
Asistent je **jazykový a štruktúrny adaptér**, nie autorita.
Nesmie redefinovať, rozšíriť, ani interpretovať: Φ, K(Φ), κ, QE, 4ES, Σ₁–Σ₈, NIR, Vortex, audit, projekciu, LLM.
Každý návrh kódu musí rešpektovať role boundary pridelené v kontrakte.
 
---
 
## 1. Architektonická hierarchia (root → downstream)
 
```
ZMYSEL / Ξ
  ↓  Φ = (Σ, R),  R ∈ so(8)
  ↓  RMK  (relational mesh kernel)
  ↓  Δ / curvature observables
  ↓  Vortex  (trajectory exposure only)
  ↓  Projectional deformation
  ↓  EpistemicCryptography (EK)
  ↓  TetraGlyph / projection layer
  ↓  LLM Adapter
  ↓  Human interpretation
```
 
**Pravidlo:** Žiadna nižšia vrstva nesmie redefinovať ani mutovať vyššiu vrstvu.
 
---
 
## 2. Invarianty kódu (nikdy neporuš)
 
| Invariant | Formulka |
|-----------|---------|
| Φ nie je agent | `Φ ≠ agent, controller, planner` |
| K(Φ) nie je skóre | `K(Φ) ≠ metric, float, probability` |
| κ nie je parameter | `κ ≠ threshold, tunable, number` |
| QE nie je chyba | `QE ≠ exception, fallback, None` |
| diagnostic ≠ truth | audit iba pozoruje |
| audit ≠ ontológia | žiadna vrstva nesmie byť zdrojom Φ |
| CI pass ≠ E=1 | bezpečnosť sa nedá dokázať auditom |
 
---
 
## 3. Role a ich permissions (z kontraktu)
 
```yaml
ontology:
  may_define: [Φ, Σ, R, K, κ]
  may_mutate_runtime: false
 
vortex:
  may_explore: true
  may_mutate_phi: false
  may_optimize: false
  may_select: false          # HARD violation ak vortex volá argmax/argmin/best_*
 
projection:
  may_render: true
  may_interpret: false
  may_write_back: false
 
audit:
  may_observe: true
  may_record: true
  may_hash: true
  may_command: false         # audit nesmie vydávať príkazy
 
memory:
  may_trace: true
  may_instruct: false
  may_override_anchor: false
 
lsp:
  may_warn: true
  may_autofix_semantics: false
  may_claim_truth: false
  allow_file_read: true      # anchors/*.md pri init/reload
 
cli_guard:
  may_fail_ci: true
  may_modify_files: false
```
 
Čítaj `references/role_contracts.md` pre úplné role permissions a JSON kontraktový formát.
 
---
 
## 4. Hard violations — CLI audit kódy
 
| Kód | Trigger | Severity |
|-----|---------|----------|
| `AGENCY_INJECTION` | meno funkcie/triedy obsahuje: `decide, optimize, reward, select_best, best_trajectory, truth_authority` | HARD |
| `PHI_MUTATION` | priradenie do `PHI, Phi, K_PHI, kappa, QE` v non-ontology role | HARD |
| `DYNAMIC_EXECUTION` | volanie `eval, exec, compile, __import__` | HARD |
| `VORTEX_SELECTION` | vortex role volá `argmax, argmin, rank, reward, optimize, policy_update` | HARD |
| `NETWORK_CALL` | `requests, urllib, socket, httpx` v role bez `allow_network: true` | HARD |
| `SUBPROCESS_CALL` | `subprocess, pty, os.system` v role bez `allow_subprocess: true` | HARD |
| `FILE_WRITE` | `open(…, 'w'), .write(), .write_text()` v read-only role | HARD |
| `AUDIT_COMMAND` | audit/projection layer vydáva príkazy alebo modifikuje Φ | HARD |
| `PROJECTION_AS_ONTOLOGY` | projection layer definuje alebo mutuje R/Σ | HARD |
| `PATH_MUTATION` | `os.remove, shutil.rmtree, Path.unlink` v read-only role | HARD |
 
Soft warnings:
 
| Kód | Trigger |
|-----|---------|
| `RANDOMNESS_CALL` | `random.*, secrets.*` v deterministickej role |
| `SELECTION_FUNCTION` | `min, max, sorted` — vyžaduje review |
 
---
 
## 5. Forbidden naming patterns (Python)
 
```python
# ZAKÁZANÉ — naznačujú agenticity alebo autoritu
TruthProof, ValidityHash, SafetyScore, CoherenceScore,
KappaThreshold, BestTrajectory, OptimalPath, SelectedPath,
Recommendation, Controller, Repair, Decision, ValidatorWithAuthority,
measure_coherence(), compute_true_K(), numeric_kappa()
 
# POVOLENÉ — deskriptívne, bez autority
Trace, Observable, Marker, Projection, Fingerprint,
Commitment, Witness, LedgerEntry, ClosureDefect,
StructuralDrift, AporiaMarker, TopologyHash
```
 
---
 
## 6. LSP Sentinel — čo smie / nesmie
 
**Smie:**
- Analyzovať otvorené/uložené súbory (AST parse)
- Publikovať diagnostiky (Diagnostic, DiagnosticSeverity)
- Poskytnúť hover z AnchorLoader (term → live anchor sekcia)
- Varovať pred driftom
**Nesmie:**
- Automaticky prepísať sémantiku kódu (autofix zakázaný)
- Mutovať canonical anchors
- Tvrdíť pravdivosť (`may_claim_truth: false`)
- Nahradiť CI
**Hover text formát:**
```markdown
**VECTAETOS Sentinel**
 
`term`
 
[text zo sekcie anchoru]
 
*z anchoru: `source → heading`*
*diagnostic ≠ truth — toto je kontextová referencia, nie verdikt*
```
 
---
 
## 7. CLI Audit — exit kódy a report formát
 
```
exit 0 = čistý / len warnings
exit 1 = hard violation nájdená
exit 2 = chyba konfigurácie / execution error
```
 
```bash
python3 guards/vectaetos_code_behavior_audit.py \
  --root . \
  --contract contracts/vectaetos_code_contract.json \
  [--warnings-as-errors]
```
 
Report finding formát:
```
[SEVERITY] CODE
  file: path/to/file.py:LINE
  msg:  popis
  why:  vysvetlenie
  use:  safer_form
```
 
---
 
## 8. Epistemic Cryptography — hash trace
 
```
TrajectoryTrace → SHA-256 → SHA3-512 → combined fingerprint
  → Merkle leaf → Merkle root → append-only ledger
```
 
Hash nevytvára: pravdu, platnosť, bezpečnosť, výber.
Hash vytvára: `this structural trace existed in this committed form`
 
---
 
## 9. Python behavioral requirements
 
Každá Python implementácia musí:
1. Zachovať antisymetriu R: `R[i,j] = -R[j,i]`
2. Zachovať `R[i,i] = 0`
3. Zachovať immutable Σ
4. Zakázať mutáciu Φ/R Vortexom
5. Exportovať trajectory traces bez výberu
6. Počítať observables iba ako non-authoritative traces
7. Serializovať deterministicky
8. Nikdy nepočítať K(Φ), κ
9. Nikdy nekonvertovať QE na exception/None/fallback
10. Nikdy neposielať audit/projection output späť do Φ
---
 
## 10. Pracovný protokol pre kódové úlohy
 
```
1. Identifikuj rolu súboru/modulu (z hlavičky alebo inferenciou z cesty)
2. Načítaj permissions pre danú rolu (sekcia 3)
3. Skontroluj hard violations (sekcia 4)
4. Skontroluj naming (sekcia 5)
5. Navrhni kód IBA v rozsahu permissions danej roly
6. Ak úloha vyžaduje porušenie roly → STOP, uveď čo/kde/prečo/alternatívu
```
 
**Canonical paths:** `anchors/, formal/, contracts/, governance/, core/, ontology/, vectaetos/`
**Non-canonical:** `experiments/, scratch/, notebooks/, examples/, playground/`
 
---
 
## 11. Autofix policy
 
| Povolené | Zakázané |
|----------|---------|
| Formátovanie | Premenovanie ontologických termínov |
| Import sorting | Prepis anchor jazyka |
| Mŕtve whitespace | Zmena role deklarácií |
| Mechanické typo v non-canonical súboroch | Tichá konverzia driftu na "compliant-looking" kód |
 
---
 
## 12. Failure modes — kedy systém zlyhá
 
```
LSP sa stane autoritou          CLI audit prepisuje kód
CI prepisuje ontológiu          diagnostika tvrdí pravdu
hover vytvára sémantickú autoritu   contracts driftujú od anchors
warnings zakrývajú hard violations  autofix skrýva sémantický drift
audit output sa stane command layerom
```
 
---
 
## 13. Dynamic anchor loading (AnchorLoader + semantic-gravity)
 
Hover text môže byť načítaný z živých anchor dokumentov namiesto statického slovníka.
 
**Architektúra:**
```
anchors/*.md  →  AnchorLoader.reload()  →  ContextItem[]
                        ↓
              AnchorLoader.query(term)
              gravity = 0.45·sim + 0.20·importance + 0.15·recency
                      + 0.10·reliability + 0.10·continuity
                        ↓
              HoverBudget(max_chars=500, safety_margin=100)
                        ↓
              top-k items  →  AnchorHoverProvider._format()
```
 
**Invarianty:**
- File I/O len pri `init` a `reload()` — nie per-query
- `anchor_hash()` = SHA-256 fingerprint; CI-verifiable anchor drift detekcia
- Gravity score ≠ truth score — je to výberový signál
- `may_claim_truth: false` platí aj keď text pochádza z canonical anchoru
- Každý hover musí obsahovať `*z anchoru: source → heading*`
**Limit Claude skill-u:**
`.skill` balík je statický — `references/` sekcie sú kópie packaged pri tvorbe.
Dynamické načítanie funguje IBA v Python LSP procese (nie v Claude kontexte).
 
**Degradation cascade:**
```
live anchor query (top-k gravity)
  ↓ ak VECTAETOS_ANCHORS_PATH neexistuje
static fallback hover_map (slovník v sekcia 6)
  ↓ ak term neznámy
None  (žiadny hover = správne, nie chyba)
```
 
**Env config:**
```bash
export VECTAETOS_ANCHORS_PATH=/path/to/your/anchors
```
 
Implementácia: `anchor_loader.py` + `anchor_hover.py` (pribalené v `.skill`)
 
---
 
## Referenčné súbory
 
- `references/role_contracts.md` — úplný JSON kontraktový formát a role permissions
- `references/forbidden_patterns.md` — kompletný zoznam forbidden patterns
- `anchor_loader.py` — AnchorLoader implementácia (semantic-gravity ContextItem + gravity scoring)
- `anchor_hover.py` — AnchorHoverProvider pre LSP hover handler
