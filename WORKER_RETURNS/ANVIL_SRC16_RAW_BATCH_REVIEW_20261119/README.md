# SRC16 saved Batch corrected independent recheck

Sourcefree recheck of the changed-predicate stale-cache defect only.

## Pinned inputs

- IMPLEMENTER `0dcd75749e5c186842a70dec777096b3f22086d8`
- MEASUREMENT_PREP trace `aa9e91d58b24ea4366a902fb16ba110b566edd5d`
- OWNER corrected `aaa8a548df8baf1cc90e22fb9e6d72adb908406e`
- corrected patch SHA-256:
  `71b128749e108dd5dff5a1729ad33a4c84c1a3a088bc1b3c5c94476f150c4c58`
- previous OWNER patch SHA-256:
  `9cda4d5bba659f6b0b69990d6b66f85451471355d773798fb9bb7b8e075a29e4`

The corrected patch was applied unchanged to an isolated copy of the pinned
IMPLEMENTER tree. No production tree, live runner, frozen runtime, original
data, GSS build, protected ref, or DHIKR was touched. The I05 patch was not
used.

## Old stale acceptance — confirmed

With the previous OWNER patch and exact prior outputs, changing
`predicate_ref_by_query` was accepted: three completed units were skipped,
the old result receipts were returned, and Batch said `COMPLETED`.

## Corrected refusal — confirmed

With the corrected OWNER patch and the same changed mapping, the call refused
with:

`SavedC11AdmissionError: SAVED_BATCH_PREDICATE_BINDING_MISMATCH`

The corrected check binds each query unit's supplied predicate to the exact
predicate in `unit.semantic_input_refs` before prior-cache reuse.

## Preserved behavior

- Forged completed prior receipts: discarded; units genuinely reexecuted.
- Genuine same-root reuse: exact prior outputs and matching predicate mapping
  returned the same three receipt hashes; summary `COMPLETED`.
- Changed prior output: refused with
  `WorkloadAdmissionError: PRIOR_OUTPUT_KIND_MISMATCH`.
- Legitimate partial resume: the DEFERRED receipt was retained; only its unit
  reexecuted on attempt 2; summary completed.
- Authority revocation: `DirectEstateError: current source/operation authority refused`.

## Verdict

`ACCEPT_SCOPED`: the changed-predicate stale-cache defect is corrected in the
tested scope. No residual defect was observed for exact same-root reuse,
changed-output refusal, or legitimate partial resume.
