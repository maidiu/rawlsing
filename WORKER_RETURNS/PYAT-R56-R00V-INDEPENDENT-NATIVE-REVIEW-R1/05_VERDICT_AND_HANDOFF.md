# Finite verdict and handoff

**ENGINEERING:** `REVISE__DO_NOT_ACCEPT`.
**SCIENTIFIC:** `NO_SCIENTIFIC_CLAIM`.
**AUTHORITY:** `HOLD`.

The gate reproduces all 36 frozen cases, but it fails eight adversarial claim-transition paths in the same public evaluator. It is not accepted as a generic independent-policy claim gate.

## Required R00E work

1. Reject/HOLD `claim_kind=EXECUTED_NATIVE` unless an independently trusted observation handle is present; `verified_evidence` must actually be consumed or typed HOLD.
2. Validate status/disposition edits against the original eligibility/execution/result axis; do not allow PROHIBITED→ELIGIBLE, ELIGIBLE→HELD, or UNKNOWN laundering.
3. Do not suppress exact semantic comparison for an operation merely because a status/disposition edit names it.
4. Verify claim grade is one of the frozen grades; refuse unknown grades.
5. Consume and validate `occurrence_objects` or explicitly reject unsupported occurrence transport.
6. Verify handle contract/version/commit identity, not just blob sets.
7. Produce a real candidate `manifest.json` and refresh `SHA256SUMS`; do not leave stale hashes.
8. Supply the exact shared-contract ref or record its missing obligations.

## What is not claimed

No R09 deployment, native execution, actual consumer, survey/decoder qualification, original35 measurement or N11/N12 release. R02/R04.byte may proceed independently under their own seals, but not on this gate as native proof.

Stop after this finite R00V verdict. No replacement gate architecture, no self-adoption.
