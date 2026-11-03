# D2P3 — one owner-produced field registry and exact reader lineage

**VERDICT:** `CANDIDATE__TEST_ONLY__INDEPENDENT_REVIEW_REQUIRED`
**Role:** bounded implementation author; not D2R reviewer, objective source issuer, Pyat HQ or adopter.
**Write root:** `WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-D2P3-PRODUCER-READER-LINEAGE-R1/`
**Base canonical:** `0d551d36ff19dc9806e0ad490ff33a1e4c25e381`

## Implemented

`new/d2p/single_registry.py` now contains one producer-owned `ProducerRegistry`:

- Producer emits immutable exact `D2P_TESTONLY_FIELD:<sha256>` refs over all scientific fields.
- Reader accepts only those exact refs and returns the same refs in `selected_refs` and `dependency_readset`.
- No independent row-derived `TestOnlyRegistry` and no parallel producer/reader identity remain in the new path.
- Exact official publisher/family, native units/geography/measures, observation/publication clocks, GSS five-subtype sum and NCA prepaid/postpaid sum are checked before emission and on dereference.
- `TEST_ONLY_NO_EXTERNAL_USE_GRANT`; issued false; issuer signature null; PDF binary SHA null.
- New tests target the new code and are under `new/tests`.

## Seven D2R cases

The original D2R seven-case suite is preserved and was rerun against the preserved original D2P/N9C code: **7 failed** as historical RED (`repro/logs/d2r_7red_final.log`, `repro/logs/d2r_7red_junit.xml`).

The frozen adapted seven-case suite against the new code: **7 passed, 6 deselected** (`new/tests/d2p3_seven.log`, `new/tests/d2p3_seven_junit.xml`). The full new suite is **13 passed** (`new/tests/d2p3_all.log`, `new/tests/d2p3_junit.xml`).

## Other actual runs

- Original D2R 35 hostiles: **35 passed** (`repro/logs/d2r_35hostiles_final.log`)
- Original D2P tests: **29 passed** (`repro/logs/d2p_original_final.log`)
- N9C 47: **NOT_EXECUTED** (not staged as a runnable set in this bounded write root)
- D2I 40: **NOT_EXECUTED** (not staged as a runnable set in this bounded write root)
- Accepted direct transport: **EXECUTED** through the actual `compose_direct_producer`, with exact field-content determinant refs, terminal `SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND`, reason `DIRECT_PRODUCER_ROUTE_EXACTLY_AUTHORIZED`, TEST_ONLY ceiling (`new/d2p/direct_trace_stdout.json`).

## Numeric and authority proofs

- GSS minus one changes GSS field ref, reader readset, GSS numeric, and snapshot; NCA ref/value remains bitwise unchanged.
- NCA plus one is the inverse.
- Revocation invalidates dependent read, preserves attempted two-ref readset, and leaves no orphan read.
- 2022-03-01 is partial/nonpositive; before publication is refused; 2022-07-08 positive cold replay is consistent.
- Forged issuer signature, changed unit, wind→hydro rename, fake publisher, changed version and wrong permission refuse.
- Reader never emits person-level, rural-phone, pooled, correlational or causal inference.

## Hold

Original GSS/NCA publisher PDF byte identities, size, first/current version, reuse/licence and field-issuer rights remain **NULL/HOLD**. No N5/N6, N7/EE13, operative N9/OC05, N12/V3, original science, actor deployment or production adoption is claimed. See `04_DOCUMENT_SOURCE_AND_REAL_ISSUER_HOLD.md`.

**Next:** distinct independent reviewer must replay actual producer refs, numeric controls, cold replay and the seven hostiles; author result is not acceptance.
