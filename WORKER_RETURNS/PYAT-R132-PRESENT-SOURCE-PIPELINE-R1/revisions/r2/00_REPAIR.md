# R132 r2 — present-source composition repair

**Status:** `COMPOSITION_SMOKE_PASS__CURRENT_SOURCE_AUTHORITY_DECISION_BANKED__NO_SOURCE_RUN`

This supersedes the prior R132 return's no-runtime guard as the technical test.
The actual current native composition was exercised through the existing
U43/C11/Route-B/I03/I05/Batch owners with a synthetic TEST_ONLY source. It is
explicitly **not** source proof and is not counted as present source success.

## Actual smoke result

- Synthetic input: `.r61/r132-present-source-pipeline/r2-smoke/synthetic-small.sav`
- Compilation: 3 compiled, 3 issued.
- Actual native executions: 3/3 `TEST_ONLY_SOURCEFREE`; each emitted one
  native output and one empirical fact.
- Correct `NativeWorkloadResult` fields were read:
  `scope`, `decision_ref`, `envelope_sha256`, `manifest.manifest_hash`,
  `route_results`, `native_outputs`, `receipts`, `output_refs`.
- No `native_result` attribute was assumed.
- Counted as source proof: **false**.

## What changed from the rejected return

1. The R132 defect was not that code was absent; the prior no-runtime wrapper
   only exercised its own guard. This r2 executes actual current native owners
   and proves the composition is callable.
2. `S44 grant_present=false` is no longer treated as a current decision or as
   evidence of global unavailability. It is only historical evidence.
3. No historical SRC27 default is selected.
4. No new engine, runtime module, resolver trust, or authority was invented.
5. The remaining blocker is the exact current source-specific authority tuple:
   source selection/edition, current host/purpose/use, native U/Epre, and
   consumer purpose. This is an authority/scientific-owner decision, not merely
   missing Python wiring.

## Current source-specific evidence

- WVS7 current runtime package:
  `rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json`;
  source SHA `2bd2a20f…09af7d`, 6 authorities, 11 predicates, 3 queries,
  1 discovery authority, 46 candidate frontier; `source_access:false`.
- LiTS retained source-specific package exists with source SHA
  `7cac43e2…fcec09`; no current source/host/purpose/use grant is present in the
  inspected records.
- Neither source is selected by this return. Source possession and historical
  packages are not permission.
- Exact decision and owners: `SOURCE_AUTHORITY_DECISION.json`.

## What is ready

The current code composition is callable:
`NativeWorkload` + `CurrentDecisionResolver` + `execute_issued_workload` →
C11/Route-B/I03/I05/Batch → empirical facts; the accepted M1/M2/B5 and FF/V553
owners remain available for the learned/consumer stages. No replacement
empirical engine was built.

## What is not run

No source file was opened, hashed, decoded, or expanded. No present empirical,
learned, M1/M2/B5, FF, or V553 consumer was claimed. The source-specific native
workload/admission tuple is missing. This is the smallest consequential decision
for HQ/source custodian:

- choose one current source-specific package;
- provide exact current source edition, host, purpose/use, permission refs,
  currentness/revocation/retention/export scope;
- provide or authorize the exact native U/Epre/projection/catalog/requests and
  `NativeWorkload`/`IssuedWorkloadRecord`.

The user is asked only for access/use authorization where that is the user's
jurisdiction; the scientific U/Epre and code binding remain with the competent
HQs/owners. No human is asked to design them.

## Exact next call

```python
result = execute_issued_workload(
    workload,
    resolver,
    source_factory=source_factory,
    host=host,
    purpose=purpose,
    allow_test_only=False,
    prior_receipts=(),
    max_units=None,
)
```

It executes only after `admit()` closes the exact current record/envelope/U/Epre
and source factory. R131 remains stopped. All prior holds remain.
