# PYAT H03 — execution, negatives and replay

## Environment

| Item | Value |
|---|---|
| Host | macOS Darwin 22.3.0, x86_64 (`MacBook-Pro.lan`) |
| Python | 3.11.3 |
| pytest | 9.0.2 |
| SQLite | 3.40.1 |
| Branch | `agent/pyat-h03-retained-gt2-n10e-analytical-consumer-r1` |
| Start HEAD | `2e3e3dece53fbfdd2a419e4cd538559b8b9ed1d7` |
| Determinism | `PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1` |
| Source access | none; no SAV, no source rows, no respondent reopening, no native source execution |

## 1. New H03 preparation court — PASS

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest \
  rawlsing_next/tests/test_pre553_retained_gt2_n10e_analytical_preparation.py \
  -q --junitxml=WORKER_RETURNS/PYAT-H03-RETAINED-GT2-N10E-ANALYTICAL-CONSUMER-R1/evidence/01_H03_PREPARATION_18.xml
```

Actual result: **18 passed**, 0 failed, 0 errors, 0 skipped, 67.24s. JUnit SHA-256 `5dc151a8eb40551cee0e67d8153d8a0a03a61bfbe8e29b30cf3ce9d5f239557c`.

The court proves:

| Witness | Result |
|---|---|
| retained query/fact/replay/risk/release/universe identities exact | PASS |
| retained predicate body reconstructs to `bd91b405…` | PASS |
| predicate is `DERIVED_BRANCH_COHORT` with zero value-bearing leaves | PASS |
| complete 36-cell native geometry, 23 zero cells, real anchors | PASS |
| six conditioned rows, denominators `6784/11787/624/0/0/15`, total 19,210 | PASS |
| Q86B→Q86A direction and all six target states per row | PASS |
| exact determinant vs typed-null determinant states | PASS |
| provider request shape has no geometry/probability/evidence channel | PASS |
| `N10E_RETAINED_CONTRACT_GAP` names all six absent determinants | PASS |
| preparation cannot claim provider receipt, consumer result or replay | PASS |
| deterministic content-addressed preparation | PASS |
| accepted provider/composer have no `fact`/`retained_fact`/`producer_result` input | PASS |
| direct grain rejects a Q86A consumer against Q86B-first joint target | PASS |
| reverse Field Forge conditioning rejected | PASS |
| tampered joint count fails closed | PASS |
| incomplete native cell set fails closed | PASS |
| wrong query/risk/target-order identity rejected | PASS |
| transport has no release object bodies or respondent preimages | PASS |
| structural Field Forge permission is not an N10E model authority | PASS |
| HQ230 model authority is candidate-only and AT07-scoped | PASS |

## 2. Reused H02 structural court — PASS (no redo of the positive claim)

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py -q
```

Actual result: **40 passed**, 0 failed/errors/skipped, 132.56s. Log SHA-256 `058bc5582965c20c37d79403f0853d65023f263421643535644c9c90c25aef70`.

This rerun confirms H03’s helper addition did not disturb the accepted structural positive. It is not presented as a new H03 analytical positive.

## 3. Synthetic N10E provider court — PASS (capability only)

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest rawlsing_next/tests/test_pre553_empirical_possibility_provider.py -q
```

Actual result: **43 passed**, 0 failed/errors/skipped, 18.14s. Log SHA-256 `0767873655951512e6e5a771c885b2d11503f6c5b4fe1bc1d028f28fbbc32ee9`.

This is the synthetic AT07 54/60 forward and 54/62 reverse law. It is a capability proof, not retained GT2 realization.

## 4. Supporting analytical route — 25 PASS, 1 pre-existing RED

```sh
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest \
  rawlsing_next/tests/test_pre553_repo_native_current_rehydration.py \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py \
  rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py -q
```

Actual result: **25 passed, 1 failed**, 15.64s. Log SHA-256 `aba1726f7e32af8408124f041e544c7724f85e8e87c8973d3ea4885d4bac4f9f`.

Failure:

`rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py::test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay`

```
GT12BI03BindingError: validated projection domain omits an observed exact source-native response state
```

### A2 RED diagnosis (does not obstruct H03)

Observed cause:

1. `_tiny_a2` builds a source-backed C11 release from the tiny synthetic `_rows()` fixture via `build_validated_source_backed_c11_release_from_stream`.
2. The resulting `RespondentEvent.raw_response_value` is the exact physical wrapper `{"$raw_physical_value": …}` and `canonical_response_value_if_authorized` is `None`.
3. `wave1_gt12_i03_positive_facts._event_value` returns `canonicalize(event.raw_response_value)` when no canonical value exists, so it returns the wrapper mapping rather than the native state token.
4. `_validate_release_member_scope_linear` compares that canonical JSON against the six-state `_source_native_domain()` and fails at the unchanged domain check (currently line 457, same check as at the parent).

The failure reproduces at the untouched receiving base and was already reported by H02. H03’s change to `wave1_gt12_i03_positive_facts.py` is addition-only (`reconstruct_gt2_risk_cohort_predicate`); the failing check and `_event_value` are unchanged.

Why it does not obstruct H03:

- H03 consumes the already-executed retained GT2 fact and the accepted Field Forge count profile. It never uses the tiny A2 source-backed release or a fresh I03 execution over synthetic rows.
- The A2 failure is a fixture/decoder discrepancy in a synthetic GT1 route, not a source-intrinsic negative and not a retained GT2 analytical result.
- No repair was performed; the one bounded repair cycle was not spent on an unrelated lane. A future fresh conditioned I03 route from a source-backed release will need its owner to align physical-wrapper decoding/canonical value production, but that route also requires source access/authority beyond H03.

## 5. Negative controls and anti-counterfeit checks

Executed in the 18-test court:

- wrong query/fact/risk identity rejected before predicate reconstruction;
- reverse Q86A→Q86B Field Forge conditioning rejected;
- direct grain rejects Q86A consumer target against the Q86B-first joint target;
- tampered joint count fails closed on count conservation;
- incomplete 35-cell topology fails closed;
- preparation cannot carry a provider receipt, consumer result or replay;
- provider request shape contains no geometry/probability/evidence field;
- structural Field Forge permission is not treated as N10E model authority;
- HQ230 model authority is verified `CANDIDATE_NOT_ADOPTED` and AT07-scoped;
- retained transport is verified to contain no release public-object/internal-record bodies and no raw respondent values.

No test was made green by deleting an observed state, weakening domain validation or altering expected retained counts.

## 6. Reproduction and replay identities

| Identity | Value |
|---|---|
| Retained query | `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0` |
| Retained fact | `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46` |
| Retained replay | `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f` |
| Retained predicate | `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3` |
| Field Forge relation | `1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19` |
| H03 preparation | `0ef9fc9c1ce71f53c802a195584782ecb813d015b505c80bb4450bf4d119e101` |
| N10E provider receipt | null (no counterfeit) |
| N10E consumer result | null (no authority) |
| N10E replay | null (no provider product) |

The preparation court loads the retained transport twice and requires identical `material()` and `preparation_ref`, so the preparation is deterministic and content-addressed. No N10E replay is claimed because no N10E product was generated.

DONE: exact commands, environment, pass/fail counts, A2 diagnosis, negative controls and replay identities. REMAINING: sealed C11 release/preimages or owner-authorized retained-fact bridge; GT2 N10E model/query/witness authority. CRITICAL BLOCKERS: absent repository/preimages and N10E authority. LARGEST PRODUCTIVE MOVE: authorize the bridge or commission the sealed-release conditioned execution.
