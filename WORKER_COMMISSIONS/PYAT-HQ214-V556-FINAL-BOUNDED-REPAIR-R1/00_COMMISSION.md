# PYAT HQ214 — V556 FINAL BOUNDED REPAIR — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Space Bunny semantic-sensitive repair worker  
**MODEL / INTELLIGENCE:** **Space Bunny Max**  
**BRANCH:** `agent/rabochii-pyat-hq214-v556-final-bounded-repair-r1`  
**EXACT REPAIR BASE:** `e4d7e6f7352e60da9de956c7875293fca141d371`  
**HOSTILE REREVIEW:** `agent/reviewer-pyat-hq213-v556-final-rereview-r1 @ 4bfbeb499883d52940131a087374b8087bf503ea`  
**REREVIEW DISPOSITION:** `V556_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`  
**CHECKOUT:** SPARSE_REQUIRED  
**ARCHITECTURE REOPEN:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

Read and obey `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`.

Use the machine's canonical Rawlsing object store. **DO NOT CLONE.** Reuse an existing exact-branch worktree if present; otherwise create exactly one isolated sparse worktree for this branch. Suggested path:

`~/Desktop/Rawlsing_Worktrees/hq214-v556-final-bounded-repair-r1`

## Mission

Close only the four named defects from HQ213. Do not reopen V556 architecture, add ontology, add relation kinds, populate attractor semantics, or touch the adopted M3/M2 seams.

The HQ213 rereview sustained all load-bearing prior repairs. This commission is the final bounded cleanup before another hostile rereview.

## Repair D-1 — registry-level class/family coherence

The author path enforces class/family coherence, but `V556RuleMaterialRegistry.build` still accepts a consistently rehashed hand-built rule whose schema class does not belong to the rule family.

Make registry build independently enforce the same class/family ceiling after validating the contract/binding.

Requirements:
- derive the schema class from the validated result contract, not a caller-side convenience;
- derive the authorizing family from the rule itself;
- refuse a mismatched pair even when every hash is internally consistent;
- keep the check tranche-local and authority-derived;
- do not invent new classes or families.

## Repair D-2 — replace the vacuous class/family court

Replace `test_schema_class_must_be_the_class_authorized_by_its_family` with a behavioural test that constructs a genuinely mismatched class/family rule and proves:
- authoring refuses, AND
- direct registry build of a hand-built, consistently rehashed rule also refuses.

Do not prove the map by asserting an entry equals itself.

## Repair D-3 — remove self-referential court theatre

The HQ213 rereview proved `test_w10_court_does_not_prove_itself_from_production_vocabulary` cannot fail because it constructs the banned names by concatenation and then scans for literals.

Either:
- replace it with a genuinely fail-capable structural test independent of production's own vocabulary, OR
- remove it and state explicitly that self-reference protection is a review discipline, not a machine-enforced court invariant.

Do not keep a decorative test.

## Repair D-4 — machine-readable helper classification

The payload-participant helper is truthfully a court/helper utility, not seam enforcement.

Replace docstring-substring proof with an explicit machine-readable classification constant or enum, and court:
- classification value;
- absence of helper invocation from the seam/evaluation path;
- no claim that it is production enforcement.

No new seam may be added merely to make the helper "real".

## Preservation law

MUST remain unchanged in semantics and preferably byte-identical:
- `rawlsing_next/m3_v556_higher_order_structural.py`
- `rawlsing_next/m2_v555_atomic_route.py`

Preserve:
- semantic UNBOUNDED closed;
- lawful structural-cardinality UNBOUNDED only where already authorized;
- topology family positive;
- interaction + attractor families valid-empty;
- positive role allowlist;
- no numeric pressure magnitude;
- no actor/person semantics;
- no fabricated interaction kind;
- no attractor population;
- deep-freeze behavior;
- exact M3 hash mirroring.

## Qualification

Reproduce:
- repaired V556 focused court;
- M3 court;
- M2 court;
- HQ213's discriminating hostile probes;
- a real class/family mismatch on BOTH authoring and direct registry-build paths;
- before/after exact failure-ID set comparison on the same bounded slice.

Run focused courts twice if practical.

Environment classification must remain truthful.

## Required return

Write only under:
`WORKER_RETURNS/PYAT-HQ214-V556-FINAL-BOUNDED-REPAIR-R1/`

Required:
- `00_RETURN.md`
- `01_REGISTRY_COHERENCE_REPAIR.json`
- `02_COURT_AUTHENTICITY_REPAIR.json`
- `03_QUALIFICATION_AND_REGRESSION.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `V556_FINAL_BOUNDED_REPAIR_COMPLETE__READY_FOR_HOSTILE_REREVIEW`
- `V556_FINAL_BOUNDED_REPAIR_PARTIAL__NAMED_DEFECT`
- `V556_FINAL_BOUNDED_REPAIR_REVEALS_AUTHORITY_CONFLICT`

At completion: commit, push only this branch, re-fetch/verify origin HEAD, report exact SHA.

Terminal:
`HQ214_V556_FINAL_BOUNDED_REPAIR_RETURNED__HOSTILE_REREVIEW_REQUIRED`
