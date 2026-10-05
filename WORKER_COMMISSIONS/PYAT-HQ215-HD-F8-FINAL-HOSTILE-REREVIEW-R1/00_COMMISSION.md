# PYAT HQ215 — H-D/F8 SOURCE-SCOPE BINDING FINAL HOSTILE REREVIEW — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** Browser/GitHub independent hostile reviewer  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**BRANCH:** `agent/reviewer-pyat-hq215-hd-f8-final-rereview-r1`  
**EXACT CANDIDATE BASE:** `09e4dc0d9e8dba21eadab0b5dd55821af7f4811c`  
**REPAIR CANDIDATE:** `agent/rabochii-pyat-hq213-hd-f8-binding-repair-r1 @ 09e4dc0d9e8dba21eadab0b5dd55821af7f4811c`  
**PRIOR HOSTILE REVIEW:** `33062ccfcca5c121bd699a98af11460440cd15ba`  
**REVIEW MODE:** READ-ONLY / HOSTILE / NO REPAIR  
**CHECKOUT:** SPARSE_REQUIRED

Read and obey `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`. Use the canonical clone/object store. **DO NOT CLONE.**

## Mission

Independently decide whether the repaired H-D/F8 source-scope binder is now safe for HQ adoption.

Do not modify implementation, merge, rebase, or self-adopt.

## Mandatory attacks

1. Reproduce the original A-bound/B-query defect and prove it now refuses in SINGLE_SOURCE_VALIDATION.
2. Verify requested source:
   - equals the bound requested source;
   - is positively admitted;
   - is present in the bound F8 rule's source_universe_refs.
3. Verify the requested-source refinement participates in replay/content identity and cannot be dropped without detection.
4. Audit public API/power accounting: source-touching powers, constructor, delegating evaluator, replay verifier, coverage guard. Confirm there is no false "exactly two returning functions" claim.
5. Verify delegating F8 evaluation grants no new authority and leaves adopted F8 algorithm/geometry/conditioners unchanged.
6. Attack COMPLETE/INCOMPLETE semantics, including laundering a partial set into exhaustive exposure.
7. Attack release/currentness handling:
   - forged off-release positive decision must fail closed;
   - adopted currentness vocabulary pin must be exact;
   - no new currentness authority may be inferred.
8. Verify all three adopted owners remain byte-identical:
   - `pre553_service_source_applicability.py`
   - `source_backed_positioned_subject_possibility.py`
   - `objective_consumer_bounded_evidence.py`
9. Verify no selection/ranking/preference/weight/first/best/latest/local, pooling/composition, permission grant, equivalence creation, backfill, F8 conditioning, geometry/distribution transformation, or actor/person inference is reachable.
10. Court authenticity:
   - reproduce the claimed 190/190 surface if lawful;
   - confirm zero skips;
   - verify repair witnesses fail against the pre-repair binder where claimed;
   - confirm write-terrain guards now fail loudly rather than silently skip.
11. Evaluate the new read-only import of `objective_non_event_currentness_contract`: confirm it is only a vocabulary dependency and creates no authority dependency cycle or semantic leak.
12. Environment classification must remain honest.

## Required return

Write only under:
`WORKER_RETURNS/PYAT-HQ215-HD-F8-FINAL-HOSTILE-REREVIEW-R1/`

Required:
- `00_REVIEW.md`
- `01_SINGLE_SOURCE_AND_POWER_ATTACK.json`
- `02_F8_NONTRANSFORMATION_AND_CURRENTNESS_ATTACK.json`
- `03_COURT_OWNER_AND_REPLAY_ATTACK.json`
- `04_FINAL_DISPOSITION.json`

Allowed dispositions:
- `ACCEPT_HD_F8_BINDING_REPAIR__READY_FOR_HQ_ADOPTION`
- `HD_F8_REPAIR_PARTIAL__NAMED_DEFECT`
- `HD_F8_REPAIR_AUTHORITY_OVERREACH`
- `HD_F8_REREVIEW_BLOCKED_BY_MISSING_EXACT_EVIDENCE`

At completion commit, push only this branch, verify remote HEAD, and report exact SHA.

Terminal:
`HQ215_HD_F8_FINAL_REREVIEW_RETURNED__HQ_DECISION_REQUIRED`
