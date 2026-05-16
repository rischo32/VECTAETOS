| ID             | Typ                 | Stav | Popis                                                                                                                                                            |
| -------------- | ------------------- | ---: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TOOL_001`     | tool limitation     | open | GitHub konektor nedáva priamy recursive tree/full clone; postupujeme `search → fetch_file → reconciliation`.                                                     |
| `PATH_001`     | mismatch            | open | Master index používa staršie canonical pathy, napr. `FORMAL_META_MATHEMATICS.md`, reálne je `formal/META_MATHEMATICS.md`.                                        |
| `PATH_002`     | mismatch            | open | `ENTROPIC_HUMILITY.md` je v root-e repa, nie vo `/formal/`.                                                                                                      |
| `PATH_003`     | mismatch            | open | `FORMAL_EPISTEMIC_GATES.md` je reálne `formal/EPISTEMIC_GATES.md`.                                                                                               |
| `PATH_004`     | mismatch            | open | `3GATE.md` nie je na master-index path-e; nájdené kandidáty: `formal/3GATE_SHAPE.md`, `scripts/3gate/3GATE_MECHANISM.py`.                                        |
| `PATH_005`     | mismatch            | open | `MECHANIZATION_OF_Φ.md` zatiaľ nenájdený pod týmto názvom; súvisiaci kandidát `formal/EPISTEMIC_SPACE.md`, ale nepotvrdzujem ekvivalenciu.                       |
| `DOC_001`      | documentation drift | open | `guards/README.md` má aktívne detailne rozpísané len GUARD-01 až GUARD-03, hoci repo má viac guardov a workflowov.                                               |
| `NAME_001`     | naming drift        | open | Nový invariant: súbory s `_`; legacy workflowy stále používajú `-`, napr. `canonical-ontology-guard.yml`, `vectaetos-boundary-guard.yml`.                        |
| `FORMAL_001`   | semantic risk       | open | `formal/EPISTEMIC_SPACE.md` používa numerický jazyk `C(Φ)`, `C(Φ) ≥ κ`, `C(Φ) < κ`; to je riziko voči novšiemu invariantnému výkladu, že koherencia sa nemeria.  |
| `FORMAL_002`   | semantic risk       | open | `formal/SECURITY_MODEL.md` obsahuje silné bezpečnostné formulácie; empirické claimy musia ostať pod L0–L4 disciplínou.                                           |
| `GATE_001`     | false-positive risk | open | `formal/3GATE_SHAPE.md` používa numerické `W,D,H ∈ [0,1]`, `GatePass`, `τ_gate`; treba rozlišovať shape observable od K(Φ)/κ.                                    |
| `WORKFLOW_001` | mode mismatch risk  | open | Niektoré workflowy sú report-only, niektoré strict; registry musí rozlíšiť enforcement status.                                                                   |
| `WORKFLOW_002` | trigger variance    | open | Niektoré workflowy skenujú celý textový priestor, iné len diff/paths; registry musí rozlíšiť scan surface.                                                   |
| `VECTOR_001`   | meta-score risk     | open | `Vector_Drift` nesmie byť chápaný ako nadradené skóre bezpečnosti ani ako K(Φ). Workflow je správne report-only (`VECTOR_DRIFT_ENFORCE=false`).                  |
| `ZMYSEL_001` | canonical alignment | open | `ZMYSEL.md` správne definuje Ξ ako substrát reprezentovateľnosti; treba ho zosúladiť s 𝒟 anchorom cez Ξ = E bez aktívneho filtrovania. |
| `IMPULSE_001` | wording fix | open | `FORMAL_IMPULSE.md` má v §3 nedokončenú vetu: „ktorá by pri realizácii prechodu mimo...“; treba doplniť bez agentnosti. |
| `COHERENCE_001` | semantic risk | open | `FORMAL_COHERENCE.md` používa slovo „mieru“ pri K(Φ); treba zjemniť na vlastnosť/predikát, nie kvantitu. |
| `SPACE_001` | legacy formalism risk | open | `EPISTEMIC_SPACE.md` obsahuje C(Φ), C(Φ) ≥ κ, Frobenius metric; ponechať iba ako external observable / legacy note. |
| `SPACE_002` | semantic risk | open | `EPISTEMIC_SPACE_SPECIFICATION.md` obsahuje K(Φ) ≥ κ; treba opraviť na predikátový jazyk bez numerického porovnania. |
| `EK_001` | observable boundary | open | EK veličiny μ, A, h sú audit observables; nesmú byť K(Φ), κ proxy, safety score ani validity score. |
| `EAI_001` | external audit boundary | open | EAI black-box audit môže mapovať štruktúru, ale nesmie tvrdiť ontologickú autoritu nad Φ. |
