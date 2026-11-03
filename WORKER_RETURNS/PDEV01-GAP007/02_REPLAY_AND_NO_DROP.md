# GAP-007 replay and no-drop evidence

## Exact consumer calls

```python
plan = construct_original35_epre(Original35Input(...35 synthetic waves...))
manifest = BatchManifest(plan.batch_units)
assert manifest.units == plan.batch_manifest.units
runner = BatchExecutionRunner(
    manifest=plan.batch_manifest,
    repository=C11Repository(),
)
```

The manifest call succeeds. The runner call raises:

```text
BatchIntegrityError: exact C11 release unavailable; no latest/default/fuzzy/nearest fallback
```

No unit executed. The refusal occurs before any scheduling or executor invocation.

## P1 plan

| Field | Value |
|---|---:|
| Waves | 35 |
| Items | 70 |
| Operations | 840 |
| Batch units | 840 |
| Holds | 0 |
| Abstentions | 0 |
| Distinct operation refs | 840 |
| Distinct batch unit refs | 840 |
| `no_drop_ok` | true |
| Source qualification | TEST_ONLY_SOURCEFREE |

The P1 `batch_manifest` and a freshly constructed current `BatchManifest` have the same manifest ref `d9164f33d81ea2ec30681af98364e06983967a3a1f784f40d30ab2639553dca5`.

## First typed mismatch

- Stage: `BatchExecutionRunner` construction / exact C11 release resolution
- Code: `BatchIntegrityError`
- Message: `exact C11 release unavailable; no latest/default/fuzzy/nearest fallback`
- Distict release refs: 35, all synthetic fixture `C11LogicalRelease` refs
- Executed units: 0
- Invented units: 0
- Dropped P1 operations: 0

Full JSON: `evidence/replay_gap.json` and `01_GAP007_REPLAY.json`.
