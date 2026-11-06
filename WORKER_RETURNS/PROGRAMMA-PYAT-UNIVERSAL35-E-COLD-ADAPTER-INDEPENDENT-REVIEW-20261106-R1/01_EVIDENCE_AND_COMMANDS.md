# E r2 evidence and commands

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py
# 20 passed in 0.99s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
# 25 passed in 0.29s
```

Cold subprocess and alias were exercised against the sourcefree envelope:
direct API == `python -m ... --envelope` == `run_ingress.py envelope`.

## Discriminating sourcefree probes

- Positive: `CONDITIONAL_SUPPORT_PROFILE`, profile present, relation
  `2d384db4…`, `structural_grant=false`.
- Changed counts/denominator: denominator `3 -> 4`, profile changed, relation
  ref changed.
- Narrow permission: producer ceiling
  `["FIELD_FORGE_RELATION_PRODUCTION","OTHER"]`, relation ceiling
  `["FIELD_FORGE_RELATION_PRODUCTION"]`; both are preserved in the profile.
- Missing replay: `FieldForgeEmpiricalIngressError: envelope replay must be a mapping`.
- Missing provenance: `envelope provenance_refs must be a sequence`.
- Missing permissions: `envelope permissions must be a mapping`.
- Empty producer ceiling: `producer_permission_ceiling must be nonempty strings`.
- Widened relation ceiling: `TYPED_REFUSAL`, no profile, structural false.
- Tampered fact content hash: constructor content-hash mismatch.
- Tampered fact object ID: constructor deterministic-identity mismatch.
- Tampered replay fact ref: `envelope fact replay ref does not bind fact`.
- Wrong envelope schema: `envelope schema mismatch`.

## Boundary notes

- The test envelope is `TEST_ONLY_SOURCEFREE`; no authentic D fact was received.
- Optional `object_id`/`content_hash` omission causes the existing canonical
  constructor to recompute identity; contradictory/tampered supplied values still
  fail. This is normalization, not a new semantic or structural grant.
- `grade` is copied caller metadata; it does not change owner permissions,
  profile, replay, or structural grant.
- No eval/pickle or source-root/name lookup appears in the two changed paths.
- Existing 25-test owner regression preserves GT2 two-target RAW behavior,
  narrowing permission, and structural refusal.

## Limits / preserved evidence

- Prior E r1 review `6334063ab…` remains the accepted semantic-linkage/refusal
  base; this review covers only the new serialization layer.
- D authentic bind/producer, original data, native/all35, FieldForge/science and
  protected adoption remain `NOT_RUN`.
- No product/test/guide/progress/controller/protected edit or code repair.
