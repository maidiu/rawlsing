# 03 — Regression, hostiles and run logs

All commands run from the worktree root on local Python/pytest. Model calls 0,
actor runs 0, original SAV/DTA 0, paid overflow off.

## Run 1 — D2P new suite (this return)

Command:
`python3 -m pytest WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-D2P-OBJECTIVE-SOURCEFREE-PRODUCER-R1/repro/tests/test_d2p_producer_reader.py -q --junitxml=WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-D2P-OBJECTIVE-SOURCEFREE-PRODUCER-R1/repro/logs/d2p_junit.xml`

**Exit 0. 29 passed, 0 failed, 0 skipped.** JUnit:
`repro/logs/d2p_junit.xml`. Full stdout: `repro/logs/d2p_pytest_stdout.txt`.

Cases: field binding (units/values/denominators/clocks/authority), five GSS
subtypes + 72.6%, NCA split integrity, two values dereferenced, ref-only
consumer recovers nothing, GSS −1 / NCA +1 directed isolation, stale-ref
refusal, four publication cutoffs, forged issuer ×2, fake binary SHA ×1,
fake permission, wrong-scope/wrong-unit ('rural phone people', person
electricity), revocation fail-closed, missing field hold, forged
correlation/causal relation ×2, inference/model flags ×4, CURRENT clock,
bad as-of, real owner handoff ×2, no-actor counterfactual ×2.

## Run 2 — N9C 47-test reader (read-only reproduction, unmodified)

Command (isolated staging of the exact N9C commit files):
`python3 -m pytest tests/test_hq297_n9c_two_field_reader.py -q`

**Exit 0. 47 passed, 0 failed.** Exact committed reader blob
`03eb46efccadd6880cb34b2e2ac609ffc9b16c59` and fixture blob
`1a1bec6e2fc5a89e2ea1b589832801a43933a632` verified. Nothing modified.

## Run 3 — D2I 40-test suite (read-only reproduction, unmodified)

Command (isolated staging of the exact D2I commit files):
`python3 -m pytest test_d2i_sourcefree.py -q`

**Exit 0. 40 passed, 0 failed.** Nothing modified.

## Totals

**116 executed cases: 29 + 47 + 40, 0 failures, 0 NOT_EXECUTED among the
sourcefree suites.** Real-source binary custody, N5/N6 issuance, EE13/N7,
N9/OC05, model/actor trials were never attempted and are NOT_EXECUTED by
commission boundary (see 04), not by runner failure.

## Hostile ledger (all executed, all fail-closed as required)

| Hostile | Expected | Observed |
|---|---|---|
| forged `issuer_signature` (GSS + NCA) | `ISSUER_FORGERY` | `ISSUER_FORGERY` |
| `issued: true` | `ISSUER_FORGERY` | `ISSUER_FORGERY` |
| fake `source_pdf_sha256` | `UNVERIFIED_BINARY_CUSTODY` | `UNVERIFIED_BINARY_CUSTODY` |
| fake `permission: GRANTED` | `REAL_USE_PERMISSION_NOT_ISSUED` | same |
| stale/unknown ref | `UNKNOWN_EXACT_FIELD_REF` | same |
| `RURAL_PHONE_PEOPLE` unit | `NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT` | same |
| `PERSON_HAS_ELECTRICITY` unit | `GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT` | same |
| revocation | `SOURCE_REVOKED`, whole-read HOLD | same |
| missing second field | hold | `TWO_INDEPENDENT_FIELDS_REQUIRED` / `REQUIRED_SOURCE_UNAVAILABLE_HOLD` |
| forged correlation (`population_join`) / causal (`requested_model_use`) | `INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED` / `PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN` | same |
| ref-only hash presented without registry | `UNKNOWN_EXACT_FIELD_REF` | same |
| cold replay | identical snapshots | identical |
| targeted invalidation | GSS-only change, NCA untouched | same |
| CURRENT clock / bad as-of | `CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED` / `INVALID_CLOCK` | same |
| 2021 retrospective knowledge | both refused | both refused |
