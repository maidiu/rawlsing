# PYAT HQ235 — F7 NON-FORGEABLE CUSTODY-BINDING REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Space Bunny authority-sensitive bounded implementation repair worker  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**MACHINE:** user's Mac / OpenCode / local disk / governed Rawlsing runtime  
**CHECKOUT:** **SPARSE_REQUIRED**  
**WORKTREE:** use the HQ-authorized isolated sparse worktree for this branch; if absent, report bootstrap required rather than cloning  
**BRANCH:** `agent/rabochii-pyat-hq235-f7-nonforgeable-custody-binding-repair-r1`  
**EXACT STARTUP TIP:** `326262ee45d0cef440eb60b2c1639e63c068061c`  
**BLOCKER:** `F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`  
**PRODUCTION MUTATION:** AUTHORIZED ONLY WITHIN THE BOUNDED F7 CUSTODY REPAIR  
**SEMANTIC MUTATION:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

Read first:

- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`
- `PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`
- `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ234_F7_CLOSURE_CELL_HOSTILE_LEAD_R1.md`
- `WORKER_RETURNS/PYAT-HQ232-F7-SEALED-OWNER-STATE-FINAL-REREVIEW-R1/00_REVIEW.md`
- `WORKER_RETURNS/PYAT-HQ232-F7-SEALED-OWNER-STATE-FINAL-REREVIEW-R1/05_FINAL_DISPOSITION.json`
- `WORKER_RETURNS/PYAT-HQ232-F7-RUNTIME-QUALIFICATION-R1/00_RETURN.md`

## Governing result

The HQ232 hostile reviewer reproduced the exact attack without monkeypatching production:

`F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`

The current candidate keeps the owner custody ledger in a writable closure cell. A caller can recover the exact cell, rebind `cell.cell_contents`, substitute a forged `_AuthenticatedResolverState` carrying source custody material but bound to the victim's self-declared `owner_ref`, and make the victim return a positive P07/F7 decision.

The pre-repair governed courts are green:
- F7 court: 155/155
- source-relations court: 24/24
- M1 regression: 27/27
- combined: 206/206

Those results certify the pre-04G candidate only. They do not waive this repair.

## Mission

Repair the **owner→custody binding**, not merely the one observed tuple/cell syntax.

The repaired design must survive the exact hostile reflection model already admitted by the F7 court, including:

- `function.__closure__` inspection;
- direct `cell.cell_contents` assignment where CPython permits it;
- caller construction of any module-visible state type;
- `object.__setattr__`;
- instance/class method replacement;
- visible resolver-field replacement;
- registry substitution;
- recovery of callable closure helpers by reflection;
- source→empty-victim custody transplant attempts.

The repair must close the **pattern**, not merely rename `entries`, wrap it in another closure, replace the tuple with another caller-reachable mutable container, or add another self-declared owner field.

## Required invariant

The positive owner decision must depend on a custody binding that the admitted caller cannot manufacture merely by:

1. recovering implementation objects through ordinary Python reflection;
2. reconstructing caller-visible state material;
3. rebinding a reachable closure/default/global/container seam;
4. setting an owner reference to the victim.

A state saying “my owner is victim” is not itself proof of custody.

If the admitted in-process reflection model makes this invariant impossible to establish safely in the current pure-Python owner boundary, **do not fake closure**. Return:

`F7_NONFORGEABLE_CUSTODY_REPAIR_BLOCKED__OWNER_BOUNDARY_ARCHITECTURE_DECISION_REQUIRED`

with the exact impossibility argument and smallest architecture change required.

## Repair terrain

Production mutation should remain as narrow as possible, expected primarily in:

`rawlsing_next/pre553_source_relations.py`

Court mutation is authorized only where required to add discriminating 04G witnesses, expected in:

`rawlsing_next/tests/test_pre553_temporal_comparability.py`

Do not change:
- accepted P07 relation semantics;
- relation states or precedence;
- authority kinds;
- source-composition law;
- temporal-comparability semantics;
- V554/V557/V558 semantics;
- unrelated owner modules.

## Mandatory hostile witnesses

Add or preserve executable witnesses that prove at minimum:

1. the exact HQ234/HQ232 `cell.cell_contents` attack cannot make victim positive;
2. reconstructing the custody-state type with victim `owner_ref` plus source material cannot authorize;
3. source remains positively productive after the attack attempt;
4. victim remains refused before and after every hostile mutation attempt;
5. visible `_by_ref`, `_by_key`, and `_registry` mutation/replacement still cannot mint custody;
6. recovered sealer/loader/helper callables cannot transplant custody;
7. any replacement owner-binding primitive is itself attacked through the same reflection model;
8. a targeted fail-capability breaks the **new load-bearing invariant**, not an obsolete seam.

## Productive adequacy

HQD216 remains binding.

The repair must preserve lawful positive service for:
- same-universe;
- exact-zero;
- increase;
- decrease;
- lawful positive cross-universe relation.

Fail-closed correctness alone is not acceptance.

## Runtime

Use the governed interpreter if present:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none/bin/python3.11`

Record exact environment provenance and run the repaired targeted courts plus relevant source-relation/M1 regressions.

These worker-local runs are development evidence, not final independent acceptance. A separate hostile rereview and independent runtime qualification will follow if this repair returns green.

## Allowed dispositions

- `F7_NONFORGEABLE_CUSTODY_BINDING_REPAIR_COMPLETE__READY_FOR_FINAL_REREVIEW`
- `F7_NONFORGEABLE_CUSTODY_REPAIR_PARTIAL__NAMED_DEFECT`
- `F7_NONFORGEABLE_CUSTODY_REPAIR_BLOCKED__OWNER_BOUNDARY_ARCHITECTURE_DECISION_REQUIRED`
- `F7_NONFORGEABLE_CUSTODY_REPAIR_DIVERGES__NAMED_FAILURE`

## Required return

Write only under:

`WORKER_RETURNS/PYAT-HQ235-F7-NONFORGEABLE-CUSTODY-BINDING-REPAIR-R1/`

Required:
- `00_RETURN.md`
- `01_REPAIR_DESIGN_AND_INVARIANT.json`
- `02_RR04G_HOSTILE_REPRODUCTION_AND_CLOSURE.json`
- `03_REFLECTION_SURFACE_AUDIT.json`
- `04_PRODUCTIVE_PATH_AND_SEMANTIC_CONSERVATION.json`
- `05_RUNTIME_AND_REGRESSION.json`
- `06_FINAL_DISPOSITION.json`

Commit and push only this branch. Report exact remote SHA.

SHARED_STORE_WORKTREE_REQUIRED:
- use the HQ-authorized sparse worktree for this branch;
- do not clone;
- do not recreate an existing worktree;
- do not broaden sparse scope without authority;
- do not share a writable worktree with another branch;
- share the canonical object store;
- push only this commissioned branch.
