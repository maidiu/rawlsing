# LAUNCH IN: DeepSeek Harness — DeepSeek V4.1 Flash — Standard mode
# ROLE: PYAT C1-03R — OWNER-CLOSURE CORRECTION — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/deepseek-pyat-hq149-c1-03r-owner-closure-correction-r1`

Exact defective return base:
`1c2c0e4ba7f0f9a273b0387a887ed74871e981e9`

Original commission tip:
`8ce2a1aaa457fb1b08da9fca917dbb342bb98d41`

Original implementation commit:
`7e558194b8aa1ff2a8c2a335c68daa7305b63dc3`

This is a correction, not a reimplementation from scratch. Preserve useful AT18/AT19 work but repair the exact HQ blockers below. Do not overwrite the original return packet; it remains forensic evidence.

Read first:
- original C1-03R commission and return packet;
- `rawlsing_next/pre553_authority_maintenance.py`;
- `rawlsing_next/pre553_replay_audit.py`;
- `rawlsing_next/pre553_analytical_composition.py`;
- AT18 and AT19 acceptance docs.

## HQ blockers

### C1-03R-HQ-BLOCK-LIFECYCLE-OWNER-001
The adapter currently performs its own invalidation lifecycle:
- computes affected/unaffected;
- invokes recompilers;
- constructs `AuthorityInvalidationReceipt`;
- declares closure verified.

A static test that forbidden method names are absent does not prove the adapter is not a second lifecycle owner.

Repair law:
- delegate the actual invalidation/recompilation transition to the current lifecycle owner where the current contract can lawfully represent it;
- do not reproduce `AuthorityMaintenanceExecutor._recompile` semantics in the adapter;
- if the current owner cannot represent the required analytical dependency transition without inventing authority or changing accepted owner semantics, STOP and return
  `EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`
  with the smallest executable counterexample. Do not patch around the gap.

### C1-03R-HQ-BLOCK-FUTURE-DETERMINANT-EDGE-002
The old forward product is currently registered with:
`consumer_lane_authority_refs=(forward_model, _revised_forward_model())`.

That falsely pre-registers the future revised authority as a determinant of a product that was not produced under it, manufacturing reachability.

Repair law:
- the existing product may bind only determinants it actually consumed;
- the revised/new authority may enter only through the governed transition/change event;
- use the existing owner's changed-authority semantics honestly;
- do not depend on tuple position such as `changed[0]` to guess which authority is the lawful replacement.

### C1-03R-HQ-BLOCK-NONCURRENT-INVENTION-003
The adapter invents:
`C1_03R_NONCURRENT_PRODUCT`
and a `NO_CURRENT` sentinel to satisfy the owner receipt's exact affected-set coverage.

The current accepted maintenance owner contains no such product-state vocabulary.

Repair law:
- do not invent noncurrent semantics;
- if an affected product lacks a lawful replacement and the existing owner has no lawful representation for that case, return the exact owner gap rather than fabricating a sentinel.

### C1-03R-HQ-BLOCK-RETAINED-ANSWER-004
The retained-determinant artifact claims to contain no stored analytical output, but currently includes `expected_output_identity`, producer/evidence/result refs, and denominator support.

Repair law:
- fresh-runner input must contain only the retained determinants needed to reconstruct/re-execute the accepted path;
- expected output identity/support belongs in a separate oracle/parent assertion, not in the runner input;
- the fresh process must not read the expected answer or a stored equivalent;
- preserve genuine fresh-process recomputation through `compose_positioned_subject_possibility`.

### C1-03R-HQ-DOC-COUNT-005
`05_EXECUTION_RECEIPT.json` still says the summary line is `109 passed in 20.45s` while the authoritative final run is 16.58s.

Correct documentary inconsistency in the new correction packet.

## What may remain

AT18 replay-grade vocabulary is not rejected merely for being new: the commission itself requires explicit grades and no equivalent governed grade vocabulary was found in the current replay owner. Preserve it if semantically honest.

The separate-process recomputation path is salvageable if the runner input/oracle separation is repaired.

The missing-edge hostile is salvageable only if the lawful graph first contains only real determinant edges.

## Write terrain

You may modify only:
- `rawlsing_next/pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/test_pre553_analytical_replay_dependency.py`
- `rawlsing_next/tests/c1_at18_at19_fixture.py`
- `rawlsing_next/tests/c1_at18_at19_fresh_process_runner.py`
- `WORKER_RETURNS/PYAT-C1-03R-OWNER-CLOSURE-CORRECTION-R1/**`

Do not modify:
- `pre553_authority_maintenance.py`
- `pre553_replay_audit.py`
- `pre553_analytical_composition.py`
- C1-03A terrain
- N10E terrain

If an accepted-owner change is actually required, return the counterexample and stop.

## Required courts

Rerun because executable/test state must change.

At minimum:
- corrected AT18/AT19 court;
- authority-maintenance tests materially relied upon;
- replay-audit tests materially relied upon;
- accepted analytical-composition court materially relied upon.

Add explicit hostiles proving:
- future/new authority cannot be pre-bound as a determinant of the old product;
- a product with no lawful replacement does not get an invented sentinel;
- runner input contains no expected output/result/denominator answer fields;
- missing-edge closure fails despite object/cache presence.

## Return

Write only:
`WORKER_RETURNS/PYAT-C1-03R-OWNER-CLOSURE-CORRECTION-R1/**`

Required:
- `00_RETURN.md`
- `01_HQ_BLOCKER_DISPOSITION.json`
- `02_REPLAY_GRADE_AND_FRESH_PROCESS_RECEIPT.json`
- `03_OWNER_DEPENDENCY_INVALIDATION_RECEIPT.json`
- `04_MISSING_EDGE_HOSTILE.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`

Allowed dispositions:
- `PASS_C1_03R_OWNER_CLOSURE_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`
- `TYPED_AUTHORITY_RESIDUAL`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No raw source, C4, AT14-17, structural world, or V3 actor/person work.

Terminal:
`C1_03R_OWNER_CLOSURE_CORRECTION_RETURNED__HQ_ADJUDICATION_REQUIRED`
