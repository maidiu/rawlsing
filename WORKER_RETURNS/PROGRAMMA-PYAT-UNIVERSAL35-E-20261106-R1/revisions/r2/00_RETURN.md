# PROGRAMMA PYAT universal35 — E ingress r2 cold-use adapter

**RESULT:** `E_INGRESS_R2_COLD_USE_ENVELOPE_ADAPTER__AUTHOR_FOCUSED_PASS__20_INGRESS_25_REGRESSION__D_AUTHENTIC_BIND_NOT_RUN__INDEPENDENT_REREVIEW_PENDING`.

**Lineage:** base `d119045f4169439b4ba02d0870bc328f8beb3aaa`; repaired head
`7d1aadfd4f655930ca2e65ea64cfa3df180a5f7b`; implementation
`7920b7fca4471c035f5b728dace9e1777c68c074`; reviewer
`6334063ab290d6497e7b8047eb1292b69661f51e`. r1 exact linkage repair retained.

## Exact adapter

Added only a cold invocation/serialization layer around the accepted
`ingest_empirical_fact` owner:

- `PRE553_FIELD_FORGE_EMPIRICAL_ENVELOPE@1` JSON envelope with exact
  `fact.as_dict()`, `query.as_dict()`, replay refs/provenance and explicit
  caller permission ceiling.
- Decoder reconstructs `EmpiricalFact@1.0.0` / `EmpiricalQuerySpec@1.0.0` via
  existing object constructors, validating schema/semantic hashes/ref linkage.
- Replay section must bind `fact.replay_ref`, query replay root and exact
  provenance set; missing or mismatched replay is an envelope error.
- Permissions must include a nonempty caller `producer_permission_ceiling`;
  relation ceiling is optional and narrowing only. No auto-fill.
- Calls existing `ingest_empirical_fact`; output is the exact existing result
  material plus the exact profile (`relation.as_dict()`) or typed refusal.
- No pickle/eval, source-root lookup, original-data read, structural admission
  grant, second empirical compiler or D fact fabrication.

## Cold command

```text
python3 -m rawlsing_next.pre553_field_forge_empirical_ingress \
  --envelope <exact-envelope.json> [--out <result.json>]
```

Alias:

```text
python3 WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/run_ingress.py \
  envelope --envelope <exact-envelope.json>
```

The envelope need not be a test fixture; the command reads only the supplied
caller path and existing owner code. No worker globals or private test fixture
names are used by the adapter.

## Results

Runner unchanged: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`
(Python 3.11.3, PyArrow 22.0.0, DuckDB 1.5.2, macOS 13.7.8 x86_64).

```text
python3 -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/evidence/junit_ingress.xml \
  rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py
# 20 passed in 0.87s, exit 0

python3 -m pytest -q -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-E-20261106-R1/evidence/junit_regression.xml \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
# 25 passed in 0.26s, exit 0
```

Adapter evidence (`evidence/adapter_comparison.json`):

- Sourcefree envelope: direct API output == cold subprocess output exactly.
- Positive: existing `CONDITIONAL_SUPPORT_PROFILE`, `structural_grant=false`.
- Changed counts/denominator: profile denominator `3 -> 4`, relation ref changes.
- Missing replay: `ENVELOPE_ERROR`, exit 2, no profile.
- RAW weighted numerator: `TYPED_REFUSAL`
  `FIELD_FORGE_RELATION_TYPED_REFUSAL`, structural grant false.
- Sourcefree label: `envelope_grade=TEST_ONLY_SOURCEFREE`.
- Existing 1-target/3+-target/role/domain/missing-cell/semantic-linkage refusals
  remain covered by the 20 ingress tests.

Evidence: `evidence/sourcefree_envelope.json`,
`evidence/subprocess_output.json`, `evidence/direct_output.json`,
`evidence/changed_envelope.json`, `evidence/changed_output.json`,
`evidence/weighted_envelope.json`, `evidence/weighted_output.json`,
`evidence/missing_replay_envelope.json`, `evidence/missing_replay_output.json`,
`evidence/alias_output.json`, `evidence/adapter_comparison.json`,
`evidence/junit_ingress.xml`, `evidence/junit_regression.xml`,
`evidence/test_run.json`, `evidence/result.json`, `evidence/source_manifest.json`,
`evidence/environment.json`, `logs/`.

## D handoff

D must emit the exact envelope in `D_INPUT_CONTRACT.json`, using real current
`EmpiricalFact@1.0.0` + `EmpiricalQuerySpec@1.0.0` products. Authentic D products
remain `NOT_RECEIVED_BY_E`; this sourcefree adapter evidence is explicitly
labelled and is not an authentic D/native result.

## Limits

- Sourcefree/test-only; no original respondent bytes read by E.
- No native/all35 claim, structural/science/actor issuance, protected merge or
  self-acceptance.
- GT2 two-target RAW single-universe remains the existing owner limit.
- Independent rereview of the exact adapter head remains required.

## Owner / next action

Distinct nonauthor reviewer rechecks the exact head and adapter receipts. D uses
the frozen envelope ABI/command for the later authentic handshake. No protected
write follows from this return.
