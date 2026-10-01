# LAUNCH IN: Astra — High
# ROLE: OMEGA-VOZHD EXCEPTION E03 — C1-03R LIFECYCLE NONCURRENT OWNER GAP — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/astra-pyat-hq150-c1-03r-e03-owner-gap-r1`

Exact corrected C1-03R return:
`1f270880f7e3353003ef6199d76d7ff28303301d`

Current sealed HQ checkpoint:
`20261001-PYAT-HQ149-POST-HQ148-RECONCILIATION-R1`
handoff commit:
`f08e33cd98653b2a0e02e1884955220ef1c13f42`

Escalation trigger:
`E03_REQUIRED_UNREPRESENTABLE_GRAIN`

This is one narrow decision. Do not redo the Pyat audit or produce a new general plan.

## Decision question

AT19, authored in the Astra development atlas, requires:

> One exact determinant mutation reaches all and only registered affected products, with replacement or NO_CURRENT.

The corrected C1-03R implementation now delegates lifecycle execution to the accepted owner and registers only determinants actually consumed. That fixed the prior fake future-authority edge and duplicate lifecycle.

It then establishes a minimal owner counterexample:

- `AuthorityMaintenanceExecutor.promote_current(..., recompiler=None)` with an affected dependent fails because affected dependents require an explicit deterministic recompiler.
- An identity recompiler fails because every affected dependent must produce a new exact ref.
- `AuthorityInvalidationReceipt` requires recompilation pairs to cover the affected set.
- Therefore an affected dependent for which no lawful replacement exists cannot currently be represented without fabricating a replacement identity.
- The worker removed its invented `C1_03R_NONCURRENT_PRODUCT` / `NO_CURRENT` sentinel and returned `EXISTING_LIFECYCLE_OWNER_CHANGE_REQUIRED`.

Relevant exact artifacts:
- Astra AT19: `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/AT19.md`
- C1 law: `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`
- lifecycle owner: `rawlsing_next/pre553_authority_maintenance.py`
- corrected adapter: `rawlsing_next/pre553_analytical_replay_dependency.py`
- correction receipt: `WORKER_RETURNS/PYAT-C1-03R-OWNER-CLOSURE-CORRECTION-R1/03_OWNER_DEPENDENCY_INVALIDATION_RECEIPT.json`
- final disposition: `.../06_FINAL_DISPOSITION.json`

The corrected lane also discloses a related fixture/identity limitation: `AuthorityCandidate` mints authority content identity from candidate material rather than analytical model law, so the source-free synthetic revision used here does not itself produce a distinct analytical-law identity. State whether that is merely a fixture limitation for the AT19 proof, or part of the owner-contract change required to satisfy AT19 honestly.

## Options

**A — minimal lifecycle-owner extension.**
Authorize a bounded extension of the accepted owner/receipt vocabulary so an affected dependent can be explicitly represented as noncurrent/deferred/unavailable when no lawful replacement exists, without fabricating a replacement exact ref. Require exact invariants, serialization/replay behavior, and independent review.

**B — existing-contract route.**
Identify an already-existing lawful owner path that satisfies AT19's `replacement or NO_CURRENT` requirement without an owner extension or adapter-invented sentinel. Name the exact API/vocabulary and the proof needed.

**C — revise AT19 obligation.**
Conclude that the `or NO_CURRENT` branch should not be mandatory at the current C1 source-free grain. If choosing this, explicitly revise the acceptance law and explain why this is not silent scope reduction.

## HQ recommendation

Prefer **A** unless you can identify a concrete existing governed representation satisfying **B**. The negative state appears semantically real and AT19 explicitly requires it; silently dropping it would violate the acceptance obligation. Any extension should remain generic lifecycle state, not C1-specific analytical vocabulary.

## Required decision

Return exactly:
1. selected option and rationale;
2. whether an accepted-owner change is authorized/recommended, and its maximum semantic scope;
3. required receipt/invariant shape if changed;
4. whether the AuthorityCandidate/model-law identity issue must be repaired for AT19 or only disclosed as a fixture limitation;
5. exact proof/review conditions for C1-03R acceptance;
6. what remains forbidden.

Astra cannot authorize raw-source access, new survey/model/comparability authority, or V3 actor/person implementation. Those remain forbidden.

Unrelated work continues independently: C1-03A repair and C5/N5 independent review.

Write the decision only under:
`WORKER_RETURNS/PYAT-C1-03R-ASTRA-E03-OWNER-GAP-R1/**`

Required:
- `00_DECISION.md`
- `01_DECISION.json`

Terminal:
`C1_03R_ASTRA_E03_DECISION_RETURNED__HQ_ADJUDICATION_REQUIRED`
