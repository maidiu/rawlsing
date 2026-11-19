# SRC16 raw / mapped / I05 independent review

## Verdict

**DEFECT — the claimed actual row-deletion RED with restoration is only a set mutation.**

`common/shared_raw_lane_test.py:137-139` creates `mutation = set(control_selected)`
and removes one signature. It never deletes a mapped row from a saved estate,
reopens it RED, restores it, and reopens equal. The reported
`mutation_deleting_mapped_row_fails=true` does not prove the required actual
saved row-deletion behavior.

Smallest fix: mutate an exact saved mapped estate row, recompute its exact
manifest/root, prove the cold reopen fails/changes, then restore the exact
original estate and prove equality.

## Passing controls

- SAV mapped expected/raw/control counts 1/1/1, exact.
- DTA mapped expected/raw/control counts 2/2/2, exact.
- Raw witness, declared missing, observed unresolved and invalid physical
  refusal pass; no source read.
- Joint mixed saved I03: denominator 1/risk 2 → 0/0 held.
- Simple unresolved NOT/positive held.
- Known missing unchanged; standalone diagnostic unchanged.
- Mapped NOT remains legitimate `ZERO_SUPPORT` with risk 2.
- Native I05: RED `EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY`; patched GREEN
  `EVALUATED_UNRESOLVED`; valid empty remains `EVALUATED_VALID_EMPTY`; positive
  remains `SUPPORTED`; revoked authority remains `DirectEstateError`.
- Exact I05 patch applied in isolated copy; Batch patch not used.

No original source, frozen runtime, protected refs, real GSS run, or DHIKR.
