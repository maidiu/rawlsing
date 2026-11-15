# PYAT HQ186 — C1 WITHDRAWN, CORRECTED PACKET, POINTERS REPAIRED

Status:
`C1_WITHDRAWN_IN_FULL__C2_C5_UPHELD__STAGE_BLOCKERS_UNCHANGED__HQ185_CHECKPOINT_RETRO_SEALED__POINTERS_RECONCILED__HQ182_HOLD_UNLIFTED__RAW_SOURCE_EXECUTION_HELD`

Decision: `HQD-2026-10-02-186`
Base: `e24d78bd3ad1...` (control head at HQ185 seal)

## C1 withdrawn

User challenged HQ183's claim that the Sol shadow HQ's byte-identity
justification was false, naming the qualified candidate
`46f3bec824c1c9da7037bacf94ec08923bc33506` and the M01 court-run head
`74a067742a370d4f6296c56140c28cc8acc53e63`.

HQ reproduced the comparisons. All four files match between `46f3bec82` and
the freeze `8ff40d37d`, and the producer at `74a06774` is byte-identical to
the freeze. `74a06774` changed only `.rabochii/court_spec.json`,
repointing `semantic_candidate_sha` to `46f3bec82`, whose test array is the
four bounded-court files. The M01 61/61 therefore qualifies the exact freeze
bytes.

**C1 is withdrawn in full. Sol's justification is correct.** HQ attempted to
produce a counterexample and could not.

HQ's error was reading the first M01 court binding (`295d270c3`) instead of
the final one, having missed four rebinds. That is the same failure mode as
HQ182's C2, where a truncated grep was completed by guessing. Recorded as a
recurring HQ failure mode.

C2, C3, C4 and C5 stand. Stage-separated blockers are unchanged: 0 freeze,
1 issuance, 1 live execution, 9 advisory, 0 counterexamples.

## Pointers reconciled

`LATEST.json` claimed `pyat_review_adjudication_decision: HQD-2026-10-02-185`
while `checkpoint_id` still pointed at the HQ184 checkpoint and
`handoff_commit` named a commit with no sealed checkpoint. No HQ185
checkpoint directory existed.

HQ185 is now retro-sealed with a proper CURRENT.md, CURRENT.json and
MANIFEST.json. `LATEST.json` is repointed coherently: checkpoint_id,
paths, handoff_commit and decision now agree.

## Holds

Unchanged. C4 freeze unadopted. No locator, no warrant, no source access.
