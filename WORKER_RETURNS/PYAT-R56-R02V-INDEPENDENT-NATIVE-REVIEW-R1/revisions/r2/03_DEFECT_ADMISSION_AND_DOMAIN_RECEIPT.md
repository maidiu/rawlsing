# R02V r2 — defect, admission and source-domain receipt

## 1. Original defect mappings through the public adapter

Both cases call
`pre553_source_native_preimage_adapter.materialize_native_preimages` with a real
decoded two-row synthetic SAV and the exact original governed mappings. The
refusals occur before any C11 release or I03 fact can exist. A test-only
sentinel on the unchanged facade builder confirms the C11 release construction
is not reached for the refusal.

| ID | Governed mapping | Repaired result | Detail | Original `a287` behavior |
|---|---|---|---|---|
| D1 | `{0: "1", 1: 1}` | `NativePreimageRefusal("DUPLICATE_RESPONDENT_KEY_MAPPING")` | `1` | Both source respondents collapsed to `R56R02:1`; I03 `SUPPORTED`, denominator 1 |
| D2 | `{0: "P0", "0": "P1", 1: "P2"}` | `NativePreimageRefusal("DUPLICATE_NORMALIZED_SOURCE_KEY")` | `0` | Silent last-wins; source PID 0 projected as `P1` |

Exact original-script replay against the repaired candidate:

```
D1_defect_normalized_respondent_key: REFUSED code='DUPLICATE_RESPONDENT_KEY_MAPPING' detail='1'
D2_defect_ambiguous_source_key: REFUSED code='DUPLICATE_NORMALIZED_SOURCE_KEY' detail='0'
```

No bundle, release, respondent event or fact is emitted. The original scripts
are read from `a287` at execution time; they were not merged into this tree.

## 2. Normalized admission and uniqueness matrix

`test_r2v_r2_normalized_admission_uniqueness_matrix` calls the public adapter
for each case. All cases raise `NativePreimageRefusal` with the exact code:

| Input mapping | Code |
|---|---|
| `{10: 20, 11: "20"}` | `DUPLICATE_RESPONDENT_KEY_MAPPING` |
| `{0: True, 1: "True"}` | `DUPLICATE_RESPONDENT_KEY_MAPPING` |
| `{0: nan, 1: "P1"}` | `NON_FINITE_RESPONDENT_KEY` |
| `{0: inf, 1: "P1"}` | `NON_FINITE_RESPONDENT_KEY` |
| `{0: "", 1: "P1"}` | `EMPTY_RESPONDENT_KEY` |
| `{0: "   ", 1: "P1"}` | `EMPTY_RESPONDENT_KEY` |
| `{0: None, 1: "P1"}` | `NON_ADMITTED_RESPONDENT_KEY_TYPE` |
| `{0: b"P0", 1: "P1"}` | `NON_ADMITTED_RESPONDENT_KEY_TYPE` |
| `{0: ("P0",), 1: "P1"}` | `NON_ADMITTED_RESPONDENT_KEY_TYPE` |
| `{0: ["P0"], 1: "P1"}` | `NON_ADMITTED_RESPONDENT_KEY_TYPE` |
| `{0: {"key": "P0"}, 1: "P1"}` | `NON_ADMITTED_RESPONDENT_KEY_TYPE` |
| `{20: "A", "20": "B", 21: "C"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY` |
| `{0.0: "P0", "0": "P1", 1: "P2"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY` |
| `{True: "P0", "true": "P1", 1: "P2"}` | `DUPLICATE_NORMALIZED_SOURCE_KEY` |
| `{None: "P0", 1: "P1"}` | `NON_ADMITTED_SOURCE_IDENTITY_TYPE` |
| `{b"0": "P0", 1: "P1"}` | `NON_ADMITTED_SOURCE_IDENTITY_TYPE` |
| `{(1, 2): "P0", 1: "P1"}` | `NON_ADMITTED_SOURCE_IDENTITY_TYPE` |
| `{nan: "P0", 1: "P1"}` | `NON_FINITE_SOURCE_IDENTITY` |
| `{inf: "P0", 1: "P1"}` | `NON_FINITE_SOURCE_IDENTITY` |

The checks operate on admitted token representations, not on literal `0`/`1`
values. Cases with source keys `10`, `11`, `20`, `21` exercise the same rules
without those literals.

## 3. Legitimate identities and injective destinations

`test_r2v_r2_mixed_numeric_string_identities_conserve_tuples_and_domain` uses
4 respondents x 3 occasions, an interleaved/reversed row order, and mapping:

```
{0: "P0", "1": "one", 2: 2, 3.0: "three"}
```

It freezes the expected exact tuples and prospective I03 domain from the
decoded source cells and governed mapping before inspecting candidate events.
Both row orders preserve 12 exact tuples, four distinct respondent keys
(`P0`, `one`, `2`, `three`), `SUPPORTED` denominator 4, numerator 4, and the
exact expected cell set.

Additional controls:

- numeric destinations `{0: 7, 1: 8, 2: 9}` on 3 respondents x 2 occasions
  preserve keys `7`, `8`, `9`, exact tuples and `SUPPORTED` denominator 3;
- non-literal source keys `{10: "P10", 11: "P11"}` on PIDs 10 and 11 preserve
  exact tuples and `SUPPORTED` denominator 2.

No candidate-emitted event identity is used to build the expected domain. The
oracle reconstructs the event identity from the exact source SHA, decoded cells,
governed mapping, occurrence fields, physical binding key and the unchanged
facade `_event` formula.

## 4. Same frozen assertion, faults, and fresh restore

`test_r2v_r2_source_domain_faults_same_assertion_and_fresh_restore` uses a
3 respondent x 2 occasion source. Against the same frozen expected tuples and
prospective I03 domain:

| Fault on the same query assertion | Observed result |
|---|---|
| omit selected SCORE cell | adapter refuses `SELECTED_VARIABLE_CELL_ABSENT` |
| swap occurrence multiplicity order | event tuples differ; same query not `SUPPORTED`; fact ref differs from baseline |
| replace one selected raw value | event tuples differ; same query not `SUPPORTED`; fact ref differs from baseline |
| fresh-process restored baseline | exact fingerprint restored: state, fact ref, denominator 3, numerator 3, cells |

The fresh process re-decodes the saved synthetic source, re-derives the domain,
re-runs the adapter/facade/C11/I03 path and compares the full fingerprint.
Setup/import failures would not satisfy this check; the restored run exits 0 and
reproduces `SUPPORTED`.

## 5. Retained S1/S2/MR/rank/admin/missingness

The nine ported tests were rerun unchanged and passed. They cover:

- S1 seven-row scalar `SUPPORTED` denominator 7, exact row tuples, cell counts
  3/4;
- S2 person-unit and household-unit separate positives with distinct release
  refs; mixed-unit package refused `CROSS_UNIT_POOLING_UNAUTHORIZED`;
- MR1 `MULTISELECT`, RANK1 `ORDERED_SEQUENCE`, held/unadministered rule absent
  from projected questions, exact I03 consumption at denominator 2;
- typed missingness: `MISSING` event preserved, I03 with `MISSING` included is
  `SUPPORTED` denominator 3, substantive-only query does not invent support;
- incomplete order fields do not fabricate support (`INTEGRITY_FAILURE` /
  `UNRESOLVED`).

The independent `test_r2v_r2_scalar_and_separate_unit_positives_retained`
rechecks the S1 positive and the S2 person/household positives plus the unlinked
cross-unit refusal with exact constants.

## 6. Envelope boundary

The transformed `physical_stream` is bounded to the tested
adapter -> unchanged facade/C11 -> unchanged I03 route. It is not a raw
`PhysicalCell` stream and no general raw-compatibility repair is claimed. The
strict receiver
`fiabc_lits_i_representation_authority.authorized_banked_raw_value` still
refuses the occurrence envelope with
`ValueError: LiTS observed representation has unexpected missing declaration`.
The unchanged facade, C11, decoder and strict-receiver code hashes match the
candidate. The original source declaration remains nested in the transformed
envelope; raw value and missing state are unchanged.

## 7. Residual boundaries

- `row_occurrence_plan=None` remains the S1 scalar path; omitting it on a
  repeated source is still a caller-contract boundary.
- The raw exact-duplicate destination guard can refuse raw-equal but
  normalized-distinct scalar destinations such as `1`/`True` before the
  normalized check. This is conservative over-refusal, not false population;
  it is outside the requested numeric/string destination-control set.
- Incomplete order fields remain fail-closed at I03 rather than refused before
  C11; no false support was observed.
