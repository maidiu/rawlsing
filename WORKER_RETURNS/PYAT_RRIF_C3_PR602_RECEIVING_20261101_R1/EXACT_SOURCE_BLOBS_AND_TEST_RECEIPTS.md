# EXACT SOURCE BLOBS AND TEST RECEIPTS — PYAT RRIF C3 PR602 RECEIVING R1

## 1. Live refs at receiving

- PRE-MAIN `refs/heads/integration/pre-main-reconciliation-r1` = `8e44ca9c751049d65e6def47600b5c073ee04b29` (read before the run and again before the merge decision; unchanged).
- PR #602 head `refs/heads/integration/pyat-rrif-c3-e4f-selective-receiving-20261101-r1` = `273565d84dd61458254db5b1e3f7c53741b185ef`.
- PR base = `8e44ca9c751049d65e6def47600b5c073ee04b29`; merge-base = same; seven linear commits.
- Frozen inputs independently confirmed as commits: E4F `f2c0af3273d612bff0a7bd2407532b52caf4348b`, E4FR `7cd2206fd976606d3816589e2fce03c03c827f39`, F0 `ac9690e70c3129c86d55ea59503a9248c77a3277`, E6/M2 HOLD `b0f7675bf4f434bc8964c9b3ebc8392bb33d56fb` (not a C3 dependency; not touched).

## 2. Exact diff and blob identities

Command:

```sh
git diff --name-status 8e44ca9c751049d65e6def47600b5c073ee04b29 273565d84dd61458254db5b1e3f7c53741b185ef
```

Observed exactly:

```text
A	PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/RRIF_C3_E4F_SELECTIVE_RECEIVING_20261101.md
M	rawlsing_next/pre553_physical_decoder.py
M	rawlsing_next/pre553_r5_codec.py
A	rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py
A	rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py
A	rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py
A	rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Diffstat: `7 files changed, 943 insertions(+), 6 deletions(-)`.

Blob command:

```sh
git rev-parse 273565d84dd61458254db5b1e3f7c53741b185ef:<path>
```

| Path | Git blob | sha256 of checked-out file |
|---|---|---|
| `rawlsing_next/pre553_physical_decoder.py` | `4b89c4598f324834de064c1200c63698a20e3c5c` | `f9794976aef51c418e8152850a7b0143df6790d0596549ea7f0991fc1f4501e9` |
| `rawlsing_next/pre553_r5_codec.py` | `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7` | `fc3aaec95d1ea6b396afb7484e5b58a242a878f9a003b47a30d7f35d48eaa9ae` |
| `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` | `625f1d8b1f3fa8c24501addcaff7d70209598596` | `54195599ba4428db26b41f49bb486588502115bd119c7dc6bdee6fe1b65873da` |
| `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` | `ac5f331322a69dab224eeeda14b05681918b432e` | `18465ff974d8767fa2ed23197084ff787d2b3bdc19e88201d1fdd84b83121d0f` |
| `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` | `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115` | `487e9c3aabd73ae24cbdfe11b9563ea77344e06ee0c2241df7049df15620df12` |
| `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` | `c07c2019455e6264b4297c1c1d782bd887b96bdd` | `1042789d92c94dd5ef983299f4cbc46b40bc55e2d556f055f6777ada11254737` |

All six match the frozen commission exactly. The two production blobs also match E4F `f2c0af32` exactly. No whole E1/E4F branch was cherry-picked.

## 3. Clean receiving checkout

```sh
git worktree add --detach --no-checkout <receiving> 273565d84dd61458254db5b1e3f7c53741b185ef
git sparse-checkout init --cone
git sparse-checkout set rawlsing_next tests \
  WORKER_RETURNS/EE-P2R6S WORKER_RETURNS/FIABC-LM2 \
  WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY \
  WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING
git checkout --detach 273565d84dd61458254db5b1e3f7c53741b185ef
git status --porcelain   # empty
```

All pytest runs used `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`. The receiving worktree was clean before and after.

## 4. E1 original 33 + E4F new 12 = 45

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=<receipts>/receiving_45.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py
```

Observed:

```text
.............................................                            [100%]
45 passed in 2.32s
EXIT=0
```

## 5. Selected PR526 / SAV / C11 / EE-P2X suite

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider \
  --junitxml=<receipts>/receiving_selected_195.xml \
  rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py \
  rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py \
  rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py \
  rawlsing_next/tests/test_fiabc_lm1_r1e_n1_physical_boundary.py \
  rawlsing_next/tests/test_fiabc_lm2_r1j_sav_representation_authority.py \
  rawlsing_next/tests/test_fiabc_lits_i_representation_authority.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_universal_workload.py \
  rawlsing_next/tests/test_r35_i01_physical_metadata.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  tests/test_ee_p2x_darwin_court_driver.py \
  tests/test_fiabc_final_measurement_telemetry_closure.py
```

Observed:

```text
......................................................................s. [ 36%]
........................................................................ [ 73%]
...................................................                      [100%]
194 passed, 1 skipped in 144.21s (0:02:24)
EXIT=0
```

The skip is the known `test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation` pyreadstat writer/readback limitation, unchanged from E1/E4/E4F. No selective deselection was used; all 195 were collected.

## 6. G01 baseline severance — PR head and PRE-MAIN

Test files:

- `rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py`
- `rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py`

Wrapper (only disables cyclic GC before `pytest.main`; no test/production/option change):

```python
import gc, os, sys
gc.disable()
import pytest
rc = pytest.main(sys.argv[1:])
print("PYTEST_MAIN_RETURN", rc, flush=True)
os._exit(rc)
```

PR head command and result:

```sh
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 <wrapper> -q -p no:cacheprovider \
  --tb=short -rA --junitxml=<receipts>/g01_prhead.xml \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_inventory.py \
  rawlsing_next/tests/test_fiabc_lm2_r1i_physical_native_hostile.py
```

```text
2 failed, 7 passed in 278.03s (0:04:38)
PYTEST_MAIN_RETURN 1
EXIT=1
```

PRE-MAIN `8e44ca9c` command and result (fresh detached worktree):

```text
2 failed, 7 passed in 277.07s (0:04:37)
PYTEST_MAIN_RETURN 1
EXIT=1
```

Identical failures on both cuts:

1. `test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation`
   `AssertionError: assert '47f141e43fb2...9761731ace7bd' == 'b9b720335f37...c77cc283bf6e8'`
2. `test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak`
   `StopIteration` locating the int special-state rule.

This is the same two pre-existing G01 REDs. This packet neither introduces nor repairs G01. G01 remains HELD.

## 7. Real synthetic SAV/DTA and hostile matrix

Probe command:

```sh
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 <probe>/e4fr_review_hostile_probe.py
EXIT=0
```

Key observed lines:

```text
sav cell: R5OpaqueValue R5OpaqueValue(type_id='python.datetime.datetime@1', payload=b'\x07\xd8\x04\x05\x06\x07\x08\x00\x00\x00\x00\x00')
sav cell: R5OpaqueValue R5OpaqueValue(type_id='python.datetime.datetime@1', payload=b'\x07\xd9\x05\x06\x07\x08\t\x00\x00\x00\x00\x00')
sav floats: [1.5, -2.25] bits=['3ff8000000000000', 'c002000000000000']
dta cell: R5OpaqueValue R5OpaqueValue(type_id='python.datetime.datetime@1', payload=b'\x07\xd8\x04\x05\x06\x07\x08\x00\x00\x00\x00\x00')
dta cell: R5OpaqueValue R5OpaqueValue(type_id='python.datetime.datetime@1', payload=b'\x07\xd9\x05\x06\x07\x08\t\x00\x00\x00\x00\x00')
dta floats: [1.5, -2.25] bits=['3ff8000000000000', 'c002000000000000']
naive-subclass-direct: opaque python.datetime.datetime@1 07d80405060708000dc07201
naive-timestamp-direct: opaque python.datetime.datetime@1 07d80405060708000dc07201
naive-one-wrapper: opaque python.datetime.datetime@1 07d80405060708000dc07201
aware-direct: REFUSED R5CodecError timezone-aware datetime requires a separate explicit decoder carrier authority
aware-ts-direct: REFUSED R5CodecError timezone-aware datetime requires a separate explicit decoder carrier authority
aware-one-wrapper: REFUSED R5CodecError timezone-aware datetime requires a separate explicit decoder carrier authority
aware-time-direct: REFUSED R5CodecError timezone-aware time requires a separate explicit decoder carrier authority
nat-direct: REFUSED R5CodecError date-like subclass NaTType cannot be safely canonicalized to a naive datetime carrier
nanosecond-direct: REFUSED R5CodecError date/time subclass with sub-microsecond precision cannot be preserved by the versioned opaque carrier
broken-tzinfo-direct: REFUSED R5CodecError date-like subclass BrokenTzinfo cannot expose tzinfo safely
broken-year-direct: REFUSED R5CodecError date-like subclass BrokenYear cannot be safely canonicalized to a naive datetime carrier
opaque-range-classify: REFUSED DecoderError physical value cannot be compared with a declared missing range (value_type=R5OpaqueValue)
DONE
```

PR526 content-bound custody and tamper are exercised by the 45/45 suite:

- `test_current_pr526_custody_and_sav_float_representation_survive_repair`
- `test_pr526_snapshot_survives_original_path_tamper`
- `test_fault_source_tamper_before_decode_is_refused`
- `test_actual_decoder_consumer_decode_regression`

The last test calls the real first consumer `rawlsing_next/ee_p2x_darwin_stage_backend.py:_decode` (import at line 713), not a stand-in.

## 8. Two-level `.item()` hostile boundary — disclosed nonblocking

Observed on the exact PR head:

```text
aware-two-wrapper: str '2008-04-05 06:07:08+00:00'
aware-ts-two-wrapper: str '2008-04-05 06:07:08+00:00'
```

This reproduces the E4FR-discovered recursive `_jsonable` fallback for two-or-more-level custom wrappers. It is outside the accepted direct/one-level D02 promise and is not reachable from the current pyreadstat SAV/DTA cell route (which yields a direct pandas `Timestamp`). It is recorded as NONBLOCKING only for that real current route. No universal timezone-aware fail-closed claim is made.

## 9. First consumer DTA branch nuance

The current first consumer `_decode` passes `encoding="latin1"` for `LITS_I`. A synthetic DTA source whose SHA is not in the D01 exact SHA/config allowlist is refused before decode:

```text
rawlsing_next.pre553_physical_decoder.DecoderError: encoding override is not in an exact SHA/config representation allowlist
EXIT=1
```

This is D01's exact declared-encoding law, not a D02 datetime failure. The real synthetic DTA `Timestamp` -> opaque behavior is verified directly at `decode_dta` in the 45/45 suite. The SAV branch of the same first consumer is explicitly exercised by `test_actual_decoder_consumer_decode_regression`. No different first consumer was found in the receiving tree. This nuance is reported rather than claiming a synthetic DTA passed through `_decode` without a declared allowlist.

## 10. Governed-court CI failure (material receiving hold)

PR #602 check at head `273565d8`:

- Workflow: `Rabochii Governed Bounded Court`, run `41335018444`, job `124932890804`.
- Conclusion: `failure`.
- Exact message:

```text
PROOF_INTEGRITY_GATE_RED: rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py: material integration-claim test requires test_rrif_e1_c3_current_integration_regressions.py.proof.json with executable severance witness
rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py: material integration-claim test requires test_rrif_e1_c3_d01_declared_encoding_admission.py.proof.json with executable severance witness
```

This is the canonical `CROSS_HQ_CONTROL_ROOM/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md` gate. The two test files contain `end_to_end` test functions / an `integration` filename and therefore are classified as material integration-claim tests. The required sibling witnesses are absent from the frozen seven-path packet. They were not added because the commission freezes exactly six payload paths plus one documentary record; adding two `.proof.json` files would change the verified PR head and exceed the allowlist. The gate is a real RED, not a branch-protection artifact.

## 11. Receipt file hashes

| Receipt | sha256 |
|---|---|
| `receiving_45.xml` | `191cfd8433d23db6ccc54bccfa4ff1385ecd93ee1d75fd9f94c936429524d3b6` |
| `receiving_selected_195.xml` | `fb33906bbee565d62b1a324e050aa7465392959c733da3b5a289681ea26c77d0` |
| `g01_prhead.xml` | `3954ba5562fa7ed782ca2de932d432e67ccc0abc9f81975655affade15bd1e5c` |
| `g01_premain.xml` | `1ba45d158430e41f9842a40a932367df4261e4c8a3baf806647d8c24dbd878ac` |
| `receiving_hostile_probe.log` | `c2d6c13023ae0bb8483f10cd8a0699153dfc00e807e5049e0991d5a4baa6d2d5` |
| `dta_consumer_probe.log` | `fb9d6352881bf04477a2d0b2844997282bfd1d04abaa7dd1a7c81e263760829e` |

## 12. NOT_RUN / HELD

- No raw/private survey source decoded; all fixtures synthetic and sourcefree.
- No source-native, actor, R9, Sorok, N11/N12, G01 numeric or PROGRAMMA execution.
- No full repository suite; only the commissioned 45, selected 195, G01 pairs and bounded hostile probes.
- No G01 repair; the same two baseline REDs remain.
- No `.proof.json` witness was written or executed; that is the exact reason the merge is held.
