# R61-R01V R8 defects and limits — ACCEPT_SCOPED_LOCAL

Verdict: **ACCEPT_SCOPED_LOCAL** for the exact R8 candidate under the declared
local trusted coordinator / TEST_ONLY profile. The four remaining R7 validation
defects are fixed through the shared create/live/restore validator, and the
retained R7 native/cold/hostile positives still pass. No new blocking defect was
found in the limited R8 diff.

## Targeted R7 defects now fixed

### D1 — Target/query compatibility
`target_label` is now checked against the query target refs and admitted source
question inventory. Reproductions:

- `target_label="wrong-label"` with the original `t` query ->
  `RecurrenceRefusal: CAMPAIGN_TARGET_LABEL_QUERY_MISMATCH`.
- `target_label="t"` with a query targeting `s3` -> same typed refusal.
- The correct `target_label="t"` with the `t` query still creates, issues and
  executes.
- Genuine restore passes; a changed target context is refused.

Evidence: `evidence/targeted_results.json`, `targeted_proof.log`.

### D2 — Condition key/value/predicate semantics
Each catalog `(OccurrenceKey, typed value, predicate)` is now checked against
the actual `SURVEY_RESPONSE_EVENT` leaf, admitted question inventory, occurrence
key/question identity and exact typed value.

- `(s1,0)` bound to the `s1=1` predicate ->
  `RecurrenceRefusal: CAMPAIGN_CONDITION_VALUE_PREDICATE_MISMATCH`.
- The correct `(s1,0)->s1=0` catalog still creates, issues and executes.
- Question/predicate mismatch and malformed catalog entries refuse.
- Restore reuses the same validator; changed catalog/value mapping refuses.

Evidence: `evidence/targeted_results.json`; the R8 author suite covers the
question/predicate mismatch and form-qualified variant.

### D3 — Malformed public condition key
`campaign.issue(condition_refs=(("s1",0),))` now raises
`RecurrenceRefusal: CAMPAIGN_TYPED_OCCURRENCE_KEY_REQUIRED`, not AttributeError.
No issuance record is created.

### D4 — Duplicate condition refs
Duplicate public condition refs now raise
`RecurrenceRefusal: DUPLICATE_CONDITION_REF`. The planner's duplicate predicate
ref check also raises `RecurrenceRefusal`, not bare ValueError.

## Retained R7 positive/control/cold evidence

All of the following passed on the exact R8 candidate:

- Author suite replayed independently: 32 passed, 0 failed/error/skip.
- Previous R7 independent probes copied unchanged into the R8 own root:
  - changed-data D=3 owner positive: 2 passed;
  - owner controls: 15 passed;
  - R7 hostile/closure suite: 9 passed (the five former R7 defects now refuse;
    the four closure cases remain refused);
  - R3 A1–A3 controls: 10 passed.
- The R7 positive independently reconstructs expected operation sets and
  root/parent typed states, preserves neutral hidden 75/25 minority and
  nonwinning exploration, and runs changed-data D3.
- The R7 controls preserve generation-1 multiple batches (cumulative 4 then 8),
  stopped/no-work predecessor advancement, pre-activation restore/activation
  without rerunning discovery, post-activation existing activation, native-call
  conservation, run-local concurrency, fixed-pin refusal, wrong query/catalog
  refusal, duplicate catalog/missing release refusal, typed receipt states and
  inflight typed HOLD.
- The targeted R8 proof independently rechecks the four defects and a retained
  multi-batch/pre-activation restore positive (`evidence/targeted_results.json`).

## Residual limits / not reached

- The fixed original pin correctly refuses altered/rehashed snapshots and
  missing pins; forged snapshot plus forged trusted pin remains the declared
  host-trust boundary per R61AF, not an in-scope product-refusal gate. No new
  pin registry/signing service is required or claimed.
- The R8 validator is exercised against the declared native-question TEST_ONLY
  inventory. Canonical-authorized question-ref variants that are not present in
  the native fixture were not independently constructed; no claim is made that
  every future canonical inventory shape is qualified.
- Inclusive target/condition label matching accepts an exact object id, a
  canonical tail label, or the final hyphen segment (the form used by the
  approved fixture). It is scoped to the declared source inventory; it is not a
  general naming authority.
- The inherited R7 text's "8 report hashes" is historical; the R8 return
  declares seven report artifacts. All seven manifest hashes and four code blobs
  were independently reproduced, and the manifest self-excludes. This is a
  documentary count difference, not a product defect.
- Local trusted-runtime campaign only; no protected issuer/signing service,
  global durable uniqueness, anti-rollback/fork, R04 joined custody or R09
  capture. R04/R09 obligations remain NOT_REACHED.
- Original 35/1890, global F6/F7/F8, N11/N12, Sorok, production/CI and J52/W52
  remain unqualified. R03 remains NOT_STARTED; no R03 wake is authorized.
- R08/R61Q is a separate lane and was not inspected, repaired or certified here.

## Minimal missing function

None for the targeted R8 scope. The four R7 obligations are implemented through
the shared validation path and independently demonstrated. Future work may
broaden canonical inventory coverage, but that is outside this bounded R8
qualification and does not block the declared native TEST_ONLY profile.
