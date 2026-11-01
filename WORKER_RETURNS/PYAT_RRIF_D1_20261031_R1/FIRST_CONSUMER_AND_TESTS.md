# First consumer and tests — RRIF-D1

**Rule used:** a static import is not a consumer. Where no actual call site was found, the consumer is reported as `UNKNOWN` or `TEST_ONLY`, not promoted from an import.

## 1. Consumer table

| Lineage | Static first importer | Actual call site | Production callgraph? | Evidence |
|---|---|---|---|---|
| `LIN-C1_ANALYTICAL_COMPOSITION` | `rawlsing_next/pre553_empirical_possibility_provider.py:35`, `rawlsing_next/pre553_analytical_state_and_route.py:939` and `rawlsing_next/pre553_n9_n10w_progressive_candidate.py:59` | `provide_empirical_possibility_slice` and the progressive candidate call `compose_positioned_subject_possibility`; no production caller of any importer found | NO; TEST_HOSTED/UNKNOWN | C1 tests 48 passed; provider tests call the composition |
| `LIN-C1_M2_RELEASE_BINDING` | none | none | NO | Module absent; no importer |
| `LIN-C3_PHYSICAL_DECODER_R5_G01` | `rawlsing_next/ee_p2x_darwin_stage_backend.py:713` and `rawlsing_next/pre553_source_native_preimage_adapter.py:30` | `ee_p2x_darwin_stage_backend._decode` calls `decode_dta`/`decode_sav` | YES for decoder; NO for D01/D02/G01 | Current SAV representation/physical boundary tests 16 passed |
| `LIN-C3_R9_SOURCE_BROKER` | none | none | NO | Modules/courts absent; import probes false |
| `LIN-C5_N5_STRUCTURAL_CONTEXT` | none for the accepted wrapper | Owner-level path in `rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py:321` | NO; TEST_ONLY | Sourcefree reconstitution against current owners exact; drift refused |
| `LIN-N10E_EMPIRICAL_POSSIBILITY` | `rawlsing_next/pre553_n9_n10w_progressive_candidate.py:55` | `provide_empirical_possibility_slice(...)` at `:327` | NO; progressive candidate is test-imported only | Current provider court 43 passed; targeted replay/fresh-process/successor 8 passed |

## 2. C1 tests

Command:

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py
```

Result: `48 passed in 11.07s`.

Targeted R6/R7 witness tests:

```
pytest ... test_pre553_analytical_composition.py -k 'r7_closed_16_key or r6_witness_mutation'
```

Result: `2 passed, 11 deselected`.

Targeted C1-02 pairing/ordering tests:

```
pytest ... test_pre553_analytical_composition_higher_order.py -k 'pairing or ordering'
```

Result: `4 passed, 31 deselected`.

These tests exercise the repaired exact key-set law and the reachable pairing-ground-truth law. They do not prove a production consumer.

## 3. N10E tests

Command:

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py
```

Result: `43 passed in 23.52s`.

Targeted replay/fresh-process/successor tests:

```
pytest ... test_pre553_empirical_possibility_provider.py \
  -k 'p7_replay or fresh_process or frozen_spine or successor'
```

Result: `8 passed, 35 deselected`.

The provider core is exact current. The remaining defect is not provider arithmetic: `AnalyticalDependencyRegistry.build_graph` ignores `determinant_exact_refs` (`pre553_analytical_replay_dependency.py:432-462`), so exact query/predicate/consumer/witness changes are not lifecycle edges. The current provider request has no fixture-context ref.

## 4. C3 tests and faults

Current representation tests:

```
python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py
```

Result: `16 passed in 69.82s`.

Accepted D01 court materialized from Git and run against current code:

```
2 failed, 6 passed
```

The two failures are exactly the declared-encoding lane assertions:

- `test_declared_encoding_allowlist_is_exact_and_distinct_from_compatibility_lane`: `AttributeError: module 'rawlsing_next.pre553_physical_decoder' has no attribute 'DECLARED_ENCODING_ALLOWLIST'`.
- `test_declared_lane_does_not_authorize_text_semantics_or_cross_source_inheritance`: `AttributeError: module 'rawlsing_next.pre553_physical_decoder' has no attribute 'SOURCE_DECLARED_ENCODING_ONLY'`.

Accepted D02 court materialized from Git and run against current code:

```
collection ImportError: cannot import name 'normalize_decoder_physical_value'
from 'rawlsing_next.pre553_r5_codec'
```

Sourcefree C3 fault script output:

```
D01_BIG5: REFUSED: encoding override is not in the frozen exact SHA/config allowlist
D01_DECLARED_ALLOWLIST_PRESENT: false
D01_SOURCE_DECLARED_STATUS_PRESENT: false
D02_normalize_helper_present: false
D02_opaque_helper_present: false
D02_jsonable_date: "2020-01-02"
D02_naked_date_encode: REFUSED: date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value
D02_tz_aware: STRINGIFIED_NOT_REFUSED: 2020-01-02 00:00:00+00:00
G01_float_key: 47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd
G01_int_key: b9b720335f373dc4f7874f32acd003732ba7947b22b9d3dbb6bc77cc283bf6e8
G01_behaviour_float: true
G01_int_differs: true
G01_module_present: false
```

PR526 source custody probe (synthetic bytes, no source file):

```
access_mode: O_RDONLY
reader_path: /dev/fd/...
snapshot_sha: add1967ad5ea78bdb77c26d9c893b711021a25fac2855334bbb0394b0b7f431a
source_sha_match: true
verify_after_acquire: PASS
verify_after_original_tamper: PASS
wrong_expected_sha: REFUSED: source sha256 mismatch before governed decode
snapshot_path_unlinked: true
closed_access_mode: CLOSED
```

This proves PR526 content-bound source custody. It does not restore D01/D02.

## 5. C5 reconstitution and drift fault

The accepted service module `current_gt2_structural_context.py` was read from Git at `151d3926` into a temporary path and executed against current PREMAIN owners. Committed GT2 transport material was extracted from Git into a temporary root because the worktree is sparse. This is sourcefree committed-transport use, not raw source access.

Observed:

```
contract_id: PYAT_C5_N5_CURRENT_GT2_STRUCTURAL_CONTEXT@1.0.0
fact_state: SUPPORTED
raw_denominator_support: 19210
query_ref_hash: e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0
fact_ref_hash: 540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46
relation_ref_hash: 1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19
admission_ref_hash: a445e43da99405e0f8181f7ab6c428d9b0dd14fefc7fc5091f21f2d21f00b08d
m1_decision_state: ELIGIBLE
v557_state: ALLOW_CONTEXT_ONLY
v557_allowed_uses: ["CONTEXT"]
resolved_uses: ["CONTEXT"]
publication_family: F1
producer_family: V554
```

Denominator drift fault: after loading the real query/fact, the fact's `raw_denominator_support` was changed in memory to `19211`. The service refused:

```
denominator_drift: REFUSED
type: CurrentGT2StructuralContextError
message: current GT2 denominator is 19211, not 19210
```

This supports `SUPERSEDED_PROVED`: the accepted wrapper's behavior survives exactly in current owners, and its denominator guard is real. It is not production adoption, and no production consumer of the wrapper was found.

## 6. R9 and C1-M2 absence

Sourcefree import probes:

```
rawlsing_next.pre553_source_access_broker: absent
rawlsing_next.pre553_source_session: absent
rawlsing_next.pre553_execution_binding: absent
rawlsing_next.pre553_c1_immutable_release_binding: absent
rawlsing_next.closed35_g01_sav_numeric_representation_authority: absent
rawlsing_next.current_gt2_structural_context: absent
```

No importer of any of these modules exists. No R9 runtime was executed. The historical R9 decoder and codec were not transplanted.

## 7. What the tests do not prove

- They do not prove a production callgraph for C1, C1-M2, R9, C5 or N10E. Only the C3 decoder has a named actual production call site.
- They do not prove behavioral equivalence from exact blob identity.
- They do not prove source authenticity for D01/D02, C1-M2, R9 or N10E context.
- They do not prove raw survey, native, actor, model-use or publication authority.
- C5 reconstitution uses the accepted module from Git and committed transport materialized to temp; it is stronger than a static import but still sourcefree test-hosted evidence.
