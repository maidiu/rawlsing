# PYAT HQ232 — F7 SEALED OWNER-STATE CUSTODY FINAL HOSTILE REREVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** DeepSeek-Harness / OpenCode independent hostile reviewer  
**MODEL / INTELLIGENCE:** **DeepSeek V4.1 Flash**  
**MACHINE:** user's Mac / local disk / isolated sparse worktree  
**CHECKOUT:** **SPARSE_REQUIRED**  
**WORKTREE:** use the HQ-authorized isolated sparse worktree for this branch; if absent, report bootstrap required rather than cloning  
**BRANCH:** `agent/reviewer-pyat-hq232-f7-sealed-owner-state-final-rereview-r1`  
**EXACT STARTUP TIP:** `d6734e0150e91a60965e7db244ed2ef519ec831c`  
**CANDIDATE CODE-BEARING HEAD:** `62394d7ff817252d6d406c1e0ada96529697f5f2`  
**CANDIDATE RETURN HEAD:** `d6734e0150e91a60965e7db244ed2ef519ec831c`  
**CANDIDATE DISPOSITION:** `F7_SEALED_OWNER_STATE_CUSTODY_COMPLETE__READY_FOR_FINAL_REREVIEW`  
**BLOCKER UNDER REVIEW:** `F7-RR-04F__LIVE_AUTHENTICATED_OWNER_STATE_IS_EXPOSED_AND_POSTCONSTRUCTION_REPLACEABLE`  
**REVIEW MODE:** READ-ONLY / NO REPAIR / NO SELF-ADOPTION

Read:
- `PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`;
- the complete F7 repair/review chain through HQ228;
- `WORKER_RETURNS/PYAT-HQ231-F7-SEALED-OWNER-STATE-CUSTODY-R1/`;
- current `rawlsing_next/pre553_source_relations.py`;
- current F7/source-relation/M1 courts relevant to this candidate.

## Mission

Independently determine whether HQ231 actually closes the final F7 authenticated-owner custody defect without changing relation semantics, weakening provenance, hiding the live state behind cosmetic indirection, or breaking positive productive service.

This is a hostile rereview. Do not trust the candidate narrative or its static accounting. Reconstruct the load-bearing path from current code and attack it.

This lane is intentionally assigned to **DeepSeek-Harness in OpenCode** because final F7 closure is provenance/capability-sensitive and benefits from direct local code/worktree inspection. It remains independent of the separate F7 runtime-qualification lane. Do not mutate production or repair defects here; return a named defect to HQ if one is found.

## Required adjudication

### A. Exact lineage and write-terrain

Verify:
- startup lineage is exact and ancestry-preserving;
- production mutation is limited to `rawlsing_next/pre553_source_relations.py`;
- court mutation is limited to `rawlsing_next/tests/test_pre553_temporal_comparability.py`;
- `pre553_temporal_comparability.py` is unchanged;
- no unrelated accepted owner or authority material changed.

### B. Live-state exposure attack

Attack the claim that no caller-visible path exposes the exact authenticated custody state.

At minimum inspect:
- module globals and callable helpers;
- closures / cells reachable from public or module-visible authenticated entrypoints;
- diagnostic/inspection surfaces;
- returned tuple/NamedTuple material;
- weak-owner references and the lexical ledger;
- constructor sealer and loader reachability through reflection;
- ordinary resolver-visible fields and registry objects.

Do not accept underscore naming, frozen dataclasses, NamedTuple shape, or lexical closure by themselves as a provenance guarantee.

### C. Source→victim transplant hostile

Reconstruct HQ228's exact hostile shape:
- source resolver A is legitimately constructed with positive authorized relation custody;
- victim resolver B is constructed without that relation;
- obtain every caller-reachable custody/inspection/reflection surface;
- attempt post-construction source→victim transplant using `object.__setattr__`, container mutation, closure-cell reachable objects, resolver-visible field replacement, registry substitution, and any equivalent same-model primitive;
- victim must remain nonpositive.

Attack whether weak-reference identity or garbage-collection behavior creates aliasing/reuse hazards. Do not invent an impossible threat model, but do not ignore actual Python reflection surfaces already admitted by the F7 hostile court tradition.

### D. Registry and snapshot provenance conservation

Re-verify that the repaired path still pins:
- exact concrete `AuthorityRegistry`;
- constructor-admitted snapshots;
- exact snapshot semantic/hash validation;
- registry replacement immunity;
- subclass/override redirection refusal;
- relation-decision replay identity;
- outer/nested authority cross-binding.

### E. Semantic non-duplication

Compare the accepted P07/source-relation owner logic before and after the repair. Verify the candidate did not reimplement or fork relation semantics in F7.

The following must remain semantically conserved:
- 12 relation states;
- 19 authority kinds;
- exact-zero/no tolerance;
- total precedence;
- 3+ anchor refusal;
- exact measure/use binding;
- TEMPORAL_EVIDENCE source-scope identity;
- explicit unrestricted-token law;
- no ranking/selection/interpolation/trajectory/causation/currentness/pooling/equivalence-creation/actor authority.

### F. HQD-216 productive adequacy

A security/provenance fix that refuses everything is not acceptable.

Verify lawful constructor-admitted positive service remains possible for:
- same-universe;
- exact-zero;
- increase;
- decrease;
- lawful cross-universe relation.

### G. Fail-capability

Inspect the candidate's claimed fail-capability. It must break the actual repaired custody seam and cause the same discriminating hostile to fail for the intended reason. Reject stale or non-load-bearing monkeypatches.

## Runtime relationship

A separate HQ232 governed-runtime qualification lane is commissioned in parallel:

`agent/rabochii-pyat-hq232-f7-runtime-qualification-r1`

Do not wait for it. This review must independently finish its source/semantic hostile adjudication.

If a completed runtime qualification is already present when you reach final disposition, you may cite it as supplemental evidence, but do not mutate or depend on its branch history.

## Allowed dispositions

- `F7_SEALED_CUSTODY_SOURCE_REVIEW_ACCEPT__RUNTIME_QUALIFICATION_PENDING`
- `F7_SEALED_CUSTODY_FINAL_ACCEPT__RUNTIME_QUALIFIED`
- `F7_SEALED_CUSTODY_PARTIAL__NAMED_DEFECT`
- `F7_SEALED_CUSTODY_REQUIRES_OWNER_CONTRACT_CHANGE`
- `F7_SEALED_CUSTODY_REVEALS_ARCHITECTURE_CONFLICT`

Full F7 adoption is forbidden unless runtime qualification is independently green.

## Required return

Write only:

`WORKER_RETURNS/PYAT-HQ232-F7-SEALED-OWNER-STATE-FINAL-REREVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_LINEAGE_AND_WRITE_TERRAIN.json`
- `02_LIVE_STATE_AND_TRANSPLANT_ATTACK.json`
- `03_REGISTRY_SEMANTIC_CONSERVATION.json`
- `04_PRODUCTIVE_ADEQUACY_AND_FAIL_CAPABILITY.json`
- `05_FINAL_DISPOSITION.json`

No production mutation. No repair. No authority adoption.

Commit/push only this branch and report exact remote SHA.


SHARED_STORE_WORKTREE_REQUIRED:
- use the HQ-authorized sparse worktree for this branch;
- do not clone;
- do not recreate an existing worktree;
- do not broaden sparse scope;
- do not share a writable working directory with another branch;
- push only this commissioned branch.
