# GT12 FINAL E2A — real GT2 integrated-candidate rerun R1 — return

## Disposition

`FAIL_CLOSED__INTEGRATED_QUERY_AUTHORITY_CLOSURE_CHANGES_GT2_IDENTITY__CENTRAL_DISPOSITION_REQUIRED`

Requested PASS terminal **not issued**.

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-gt12-final-e2a-real-gt2-rerun-r1`

Exact starting HEAD: `820311811b3e4094aea7e0e665fd0a228520cd1a`

This worker executed only:

`integrated candidate + exact governed A1 C11 substrate -> real GT2 current-I03 -> authoritative deterministic replay -> downstream-input receipt`

It did not produce a FIELD FORGE relation, execute PRE-V3/M1/V558, perform the final hostile audit, acquire source data, or move PRE-MAIN/main.

## Exact A1 boundary reproduced

Using the persistent governed FFP014/FFP017 Library carriers, the integrated candidate reproduced and revalidated:

- C11 release: `R5_GT12_Q86A_Q86B_FROZEN`
- release hash: `8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295`
- replay manifest: `c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa`
- empirical universe: `4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1`
- source rows retained as provenance: `51,587`
- exact claim members: `19,210`
- public objects: `96,057`
- internal records: `19,212`

No governed respondent/source rows were committed.

## Real integrated GT2 execution

Claim:

`GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`

Exact semantic order:

`Q86B -> Q86A`

- CONDITIONER: `Q86B`
- TARGET: `Q86A`
- state: `SUPPORTED`
- denominator: `19,210`
- complete joint domain: `36` cells
- nonzero cells: `13`
- administrative typed states conserved: `DK`, `NOT_ASKED`, `REFUSAL`, `MISSING`
- complete 36-cell payload exactly equals A3's genuine payload

Integrated identities:

- predicate: `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query: `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- EmpiricalFact: `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- authoritative replay: `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`

Authoritative replay reproduced the integrated `QueryExecutionResult` exactly.

## Exact A3 comparison

A3 expected:

- predicate: `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query: `e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670`
- EmpiricalFact: `7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f`
- replay: `10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0`

Exact comparison:

- release: **IDENTICAL**
- empirical universe: **IDENTICAL**
- predicate: **IDENTICAL**
- denominator: **IDENTICAL**
- complete 36-cell payload: **IDENTICAL**
- administrative typed states: **IDENTICAL**
- selected predicate authority identity: **IDENTICAL**
- selected target-use authority identity: **IDENTICAL**
- query: **DIFFERENT**
- EmpiricalFact: **DIFFERENT**
- replay: **DIFFERENT**

### Why the hashes changed

The integrated candidate intentionally carries the **same exact A3 `TARGET_USE_PERMISSION` authority ref** in `EmpiricalQuerySpec.authority_snapshot_refs` alongside `PREDICATE_GRAMMAR`.

A3's legacy query carried only `PREDICATE_GRAMMAR` in that query-level authority closure.

Thus this is not a different selected permission object and it is not an empirical-result disagreement. It is a stronger integrated authority closure that changes the semantic identity of the query and, transitively, the producer-owned EmpiricalFact and replay identities.

Per the E2A instruction, these identities are **not** reported as equivalent. Central must explicitly dispose the identity change before downstream canonical adoption.

## Permission ceiling

Exact permission remains:

`EMPIRICAL_INPUT_TO_FROZEN_EXACT_CONDITIONAL_SUPPORT_ONLY__NO_CAUSAL_OR_ACTOR_PROMOTION`

Nothing in this rerun authorizes causal interpretation, actor state, positive V3 transition, V2 expression, or generalized FIELD / HEGEMONY / PRESSURE / MECHANISM claims.

## Timings

- exact claim-scoped C11 projection: `19.745604393 s`
- C11 candidate sealing: `33.759659992 s`
- C11 validation: `36.850393941 s`
- GT2 plan: `3.433379488 s`
- current-I03 GT2 execution: `21.368472868 s`
- authoritative deterministic replay: `21.558146247 s`

## Focused regression actually run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. pytest -q \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py \
  rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py \
  rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
```

Result:

`54 passed in 2.38s`

## Downstream transport

Machine-readable receipt:

`01_DOWNSTREAM_INPUT_RECEIPT.json`

It banks the exact integrated query semantic projection; exact fact/query/predicate/replay refs and hashes; empirical-universe/source/risk/release identities; exact GT2 authority snapshots and permission ceiling; complete 36-cell support; exact roles; and content-addressed digests/counts for the large respondent/provenance dependency closures needed to bind the producer-owned fact without committing governed source/respondent rows.

The receipt is evidence/transport only. It does not become semantic owner.

## Terminal

`FAIL_CLOSED__INTEGRATED_QUERY_AUTHORITY_CLOSURE_CHANGES_GT2_IDENTITY__CENTRAL_DISPOSITION_REQUIRED`
