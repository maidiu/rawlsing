# OBL059 — GOVERNED BOUNDED COURT EVIDENCE R1

## Frozen target

- frozen candidate commit: `8f209b52f81a5c1bf5ed158782f25f56153ac68e`
- authority artifact SHA-256: `20a0bce78f290da4e47146e7a06c478d1f483133cc0a47eb8b1060bbf19a27b2`
- governed-court artifact SHA-256: `2851a5407dbdc9cab71f776cd5327b6262d576da776fba4d3f6032a2306b028b`
- execution scope: `NONCURRENT_SYNTHETIC`
- project-current state creation authorized: `NO`

The frozen executable blobs were re-read from GitHub at the frozen commit before evidence execution. The content identities matched the freeze manifest.

## Exact execution

Command:

`python governed_bounded_court.py`

Terminal summary emitted by the frozen court:

```json
{"court": "OBL059_R1_GOVERNED_BOUNDED_COURT", "errors": 0, "execution_scope": "NONCURRENT_SYNTHETIC", "failures": 0, "project_current_state_created": false, "successful": true, "tests_run": 30}
```

Python unittest terminal:

```text
Ran 30 tests in 0.004s

OK
```

## Covered minimums

The 30-test court proved, within its fixture domain:

- exact actor/subject/world/time/ADP-010 opportunity bindings are mandatory;
- missing or ordinary malformed required bindings fail closed;
- wrong actor/world/time/opportunity/consumer bindings fail closed;
- stale structural, actor, and phase receipts fail closed;
- `SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL` alone is insufficient;
- routing alone is insufficient;
- V554, CAN-001, CAN-003, routing, and ADP-010 cannot alias the OBL059 source authority;
- wrong ADP-007 or ADP-008 authority receipts fail closed;
- consumed OBL048/ADP-007/ADP-008 evidence ownership is preserved rather than absorbed;
- a positive synthetic receipt remains source-owned by OBL059 and binds the exact tuple;
- every positive/negative receipt attests `project_current_state_created=false` and all neighboring forbidden effects false.

## Court terminal

`PASS__OBL059_R1_GOVERNED_BOUNDED_COURT__30_OF_30`

This court PASS is not an adoption recommendation by itself. The required later hostile review found a narrower malformed-input totality defect and therefore controls the worker return recommendation.
