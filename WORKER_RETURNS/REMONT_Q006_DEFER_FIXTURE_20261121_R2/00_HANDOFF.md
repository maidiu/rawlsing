# Q006 persisted-DEFER fixture — actual entry result

## Status

**`FIXTURE_ACTUAL_ENTRY_EXERCISED__SCRATCH_EXACT_BASIS_GREEN__DF18_PRODUCT_RED`**

The test now builds the persisted-DEFER fixture and invokes the actual recorded
operation and native entry, not just an import check.

## Scratch exact-basis proof

Used only as permitted scratch basis, not a product edit:

- exact earlier `HeldRecordedOperation` class from `8a9ffe49`;
- exact earlier `_CODEC` and `_unwrap_raw_physical_value` definitions from
  `8a9ffe49`;
- current `bfa04aa9` canonical scope contract.

Result: **1/1 passed**. The fixture produced seven recorded outcomes,
denominator 7, separate system-missing and absent counts, historical DEFER and
positive ALLOW refs, and identical replay. Missing/revoked scope and ordinary
native DEFER paths were exercised as typed refusals.

## Corrected exact branch

Against the published exact corrected commit `df18dd6a0`
(`HeldRecordedOperation` restored at strict scope cut), the same actual entry
reaches:

```text
RecordedResponseError: stored R5 raw_typed value cannot be decoded exactly
```

The underlying decoders `_CODEC` and `_unwrap_raw_physical_value` are still
absent from the corrected module. This is the exact earliest real-entry product
red; no fixture rewrite or monkeypatch was used to hide it.

## Boundaries

No product edit in this branch, no monkeypatch of reader/index/authorities, no
original SRC04/SRC16 body, no real query or I03 on an estate, no issue posts.
