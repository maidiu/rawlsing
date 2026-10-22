# R56-R02 — GOVERNED SOURCE-NATIVE OCCURRENCE PROJECTION — RETURN

**Disposition:** `SCOPED_AUTHOR_CANDIDATE_WORKING__ENGINEERING_RED_BEFORE__GREEN_AFTER__INDEPENDENT_R02V_NOT_RUN`
**Startup:** `6d95a78bf6b7bcf70022e303a151255e65edc38a`
**Branch:** `agent/rabochii-pyat-r56-r02-occurrence-projection-repair-r1`
**Return root:** `WORKER_RETURNS/PYAT-R56-R02-OCCURRENCE-PROJECTION-REPAIR-R1/`
**Author role:** R02 implementation owner, not R00P policy owner and not R02V reviewer.
**Runtime:** mainMac / OpenCode / Python 3.11.3 / pytest 9.0.2 / pyreadstat 1.3.2.

## Finding → interpretation → action → owner

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| The inherited adapter projected repeated SCORE through a value-key rule shared by every row, producing two events per physical cell and 48 SCORE events for a 24-cell 12×2 source. | The old carrier had no per-row occurrence binding; equal values at different occasions were indistinguishable. | Added a governed row/occurrence plan to the adapter and occurrence-specific physical binding envelopes. One physical cell now produces exactly one C11 event. | R02 author (this candidate) |
| The inherited adapter assigned rows to respondents by row-index cycling. | Respondent identity was positional, not source-native. | Row respondent identity is now derived from a governed source respondent variable and an explicit bijective source-ID map. | R02 author |
| A caller could supply a value map that collides or leaves an occasion unmapped. | Silent fallback would create misidentified facts. | Duplicate keys/values, missing mappings, duplicate row/occasion identities, scalar ambiguity and cross-unit pooling fail closed before C11 release construction. | R02 author |
| The corrected release was not yet connected to the unchanged I03 repeated-query consumer. | A disconnected valid C11 object is not a repair. | The tests build C11 from the corrected stream with the unchanged facade and execute the unchanged repeated-query consumer. | R02 author; R02V independent review pending |

## Actual native/sourcefree qualification performed

Command:

```
cd /Users/matthewsmith/Desktop/Rawlsing/R56-R02-occurrence-projection-wt
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -m pytest \
  rawlsing_next/tests/test_universal_source_projection.py \
  -q -rA --junitxml=WORKER_RETURNS/PYAT-R56-R02-OCCURRENCE-PROJECTION-REPAIR-R1/receipts/pytest.xml
```

Result: **15 passed, 0 failed, 0 errors, 0 skipped**. The proof-integrity witness also passed: baseline PASS, exact implementation mutation produced `TARGET_ASSERTION_FAILED`, source restored. The changed-test gate detected the integration-claim test, ran the sidecar witness, and returned `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION` with `witness_contracts_run=1` (`receipts/proof_gate_changed.json`).

The 12×2 synthetic repeated case (`24` physical SCORE cells):

- C11 `RespondentEvent` count for the repeated question: **24**, not 48.
- Exact tuple set: `(R56R02:P0, occasion 0, "0")`, `(R56R02:P0, occasion 1, "0")`, … for all 12 respondents.
- I03 repeated-query result: `SUPPORTED`, raw denominator **12**, raw numerator **12**, 12 exact sequence cells.
- Source SHA256 (one generated fixture run; receipt `evidence/occurrence_receipt.json`): `91df04cfb1bd6b3cccfe7360cef96a5823d7fc5ffec4c6c1417ff6c5d07b6f3c`.
- C11 release ref: `C11LogicalRelease|R56-SYNTHETIC-RELEASE|09580841a5896052ace6835f5b57d78f31644250508a779e30976456a4060296`.
- I03 fact ref content hash: `1a950b1bcf74446facd2b44fc462a5266b2240b2f83ba919de207d13a0a4010b`.
- The synthetic SAV writer adds metadata, so the fixture byte hash is per-generation; the receipt records the exact source/release/fact identity of the run. The semantic tuple assertion does not depend on that stable byte hash.

Actual public call path:

```
rawlsing_next.pre553_source_native_preimage_adapter.materialize_native_preimages
  -> rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream
  -> rawlsing_next.pre553_source_backed_c11_facade.build_source_backed_c11_repository
  -> rawlsing_next.pre553_empirical_query.execute_empirical_query
```

No facade, decoder, C11, I03, Batch or Route B module was edited.

## Cases covered

- 12 respondents × 2 occasions; 5 × 3; 4 × 2; equal values at both occasions.
- Row-order reversal with the same governed source-ID map: exact tuple set conserved.
- Missing SCORE state: event state `MISSING`, no invented support; repeated query does not return `SUPPORTED`.
- Different column labels with same source values: identical exact tuple set.
- S1 rectangular one-row-per-respondent scalar path: still `SUPPORTED`.
- S2 separate-unit package: refused `CROSS_UNIT_POOLING_UNAUTHORIZED`, not pooled.
- MR/MULTISELECT and RANK/ORDERED_SEQUENCE topology fields preserved in C11 events.
- Unadministered rule: held, not projected.
- Duplicate occurrence keys, duplicate source values, unmapped respondent, unmapped occasion, duplicate occurrence identity, duplicate respondent key, and scalar repeated-form ambiguity: fail closed before C11 facts.
- Value mutation in the same fixture changes the same repeated-query assertion; a fresh interpreter restores the baseline fingerprint exactly.

## Engineering / science / authority

**Engineering:** scoped working candidate; actual C11 and I03 consumed; exact tuples verified; proof-integrity mutation witness passed. This is an author candidate, not R02V acceptance.

**Science:** TEST_ONLY sourcefree only. No original SAV/DTA, original respondent data, original U/E_pre, F1–F8, FF/F6/F7, learned/world, actor or N11/N12 issuance. No scientific meaning is promoted from synthetic values.

**Authority:** R56 narrow grant; R57 delegated technical seal; R00P-R2 admitted TEST_ONLY contract. No production promotion, protected CI, source right, original35 measurement, adoption, or new architecture. J52/W52 remain USER_STOPPED.

## Limits and next step

- R02V independent native review is **NOT RUN**. This author must not self-review.
- Full R01 grammar/lowering, R03 native integration, R04.byte custody, R04.joined, R05/R06 consumers and original35 remain out of scope.
- The adapter now supports governed repeated rows and scalar rectangular rows. It deliberately refuses scalar variables repeated across multiple physical rows rather than guessing a form-constant rule.
- The occurrence binding uses the existing physical binding envelope and leaves the original source declaration nested inside; C11 event raw values are unchanged. R02V should challenge this binding choice and the proof witness independently.
