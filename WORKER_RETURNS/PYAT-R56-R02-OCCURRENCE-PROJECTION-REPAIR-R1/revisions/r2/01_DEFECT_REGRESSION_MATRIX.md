# R02 r2 — defect -> regression -> result matrix

**Repair parent:** `236fd4d1064f7c14113616db300c955294a474ac`
**Reviewer source:** `a287674b97a2bbde4bf9acf3b6badf19b5ce72f5`
**Scope:** normalized mapping admission only. No new architecture, source
semantics, policy, facade/C11/I03 change, or scientific judgment.

## Matrix

| Defect | Reviewer evidence at `a287` | Observed before repair | Repair boundary | Regression test | Result after repair | Near-positive control |
|---|---|---|---|---|---|---|
| **D1** normalized destination collision | `00_RETURN.md` D1; `evidence/defect_normalized_respondent_key.py` / `.out.json` | Mapping `{0:"1",1:1}` merged two source respondents into one C11 respondent; I03 `SUPPORTED`, denominator 1. | `_normalized_respondent_identity` admits scalar values on the historical string form, rejects empty/None/container values, and `normalized_respondent_mapping()` checks destination uniqueness **after** normalization and **before** constructing the lookup dict or any C11 release. | `test_r02v_normalized_duplicate_respondent_key_is_refused` (reviewer, ported) and `test_r02v_normalized_collisions_refuse_before_c11` (author r2) | `NativePreimageRefusal("DUPLICATE_RESPONDENT_KEY_MAPPING")`; no bundle/fact. Receipt: `evidence/r2_defect_resolution_receipt.json`. | Int/float/string source keys and injective string destinations; numeric destination scalars `{0:1,1:2,2:3}`; all exact tuples and I03 denominator 3. |
| **D2** normalized source-key collision | `00_RETURN.md` D2; `evidence/defect_ambiguous_source_key.py` / `.out.json` | Mapping `{0:"P0","0":"P1",1:"P2"}` silently last-wins; source PID 0 became `P1`. | `_normalized_source_identity` validates the actual token representation and `normalized_respondent_mapping()` checks source-token uniqueness before building the lookup dict. | `test_r02v_ambiguous_normalized_source_key_is_refused` (reviewer, ported) and `test_r02v_normalized_collisions_refuse_before_c11` (author r2) | `NativePreimageRefusal("DUPLICATE_NORMALIZED_SOURCE_KEY")`, detail `"0"`; no bundle/fact. Receipt: `evidence/r2_defect_resolution_receipt.json`. | Int/float/string source keys with injective destinations, including row permutation; exact conservation. |

## Admission policy actually implemented

Source identity keys are admitted on the same representation used for source
cell lookup: exact `bool`/`int`/`str` tokens and finite `float` tokens. The
repair does not special-case literal `0`, `1`, or any fixed string. Unsupported
key types and non-finite floats refuse. Scalar destination values keep the
adapter's historical string form (`str` for `bool`/`int`/finite `float`, exact
string otherwise); empty strings, `None`, bytes and containers refuse. Both
uniqueness checks run on the admitted normalized representation before the
lookup dictionary is built.

The earlier raw duplicate-value check in `GovernedRowOccurrencePlan.__post_init__`
is retained for exact duplicates. It is no longer the only check; the new
normalized bijection check is the one that governs lookup and release
construction. The lossy `{token(k): str(v)}` comprehension was removed.

## Requirement coverage

| Requirement | Result |
|---|---|
| Both reviewer defect assertions pass as typed refusals before C11/fact | PASS: D1 code `DUPLICATE_RESPONDENT_KEY_MAPPING`; D2 code `DUPLICATE_NORMALIZED_SOURCE_KEY` |
| Equivalent normalization collisions and near positives | PASS: `test_r02v_normalized_collisions_refuse_before_c11`, `test_r02v_normalized_near_positive_controls` |
| Row permutations | PASS: reviewer permutation test and near-positive permuted case |
| Exact source/respondent/occasion/value conservation | PASS: exact tuples and prospective source-derived I03 domains |
| Retain 15 author tests | PASS: 15/15 |
| Retain 7 independent positive consumer tests | PASS: 7/7 (within the 9 reviewer tests) |
| Retain 2 reviewer defect tests | PASS: 2/2 |
| Retain 42 retained facade/query tests | PASS: 42/42 |
| Prospective source-derived domains | PASS: reviewer `_r02v_expected_domain_and_tuples` ported; no candidate-generated expectation circle |
| Proof-integrity same-assertion fault/cold restore | PASS: 4 claims, baseline PASS, target assertion RED, adapter restored |
| S1/scalar, S2 separate-unit positive/refusal | PASS: reviewer positive test retained |
| MR/rank/admin and typed missingness | PASS: reviewer tests retained |
| Binding-envelope limitation explicit | PASS: see below; no facade/strict-receiver change |

## Binding-envelope limitation (unchanged)

The transformed `NativePreimageBundle.physical_stream` is compatible with the
tested adapter -> unchanged facade/C11 -> unchanged I03 route only. It is **not**
a raw `PhysicalCell` replacement for strict declaration receivers such as
`fiabc_lits_i_representation_authority.authorized_banked_raw_value` or
`fiabc_lm2_r1e_common_c11._cells`, which reject/compare the decoder declaration.
The repair did not change the facade or any strict receiver and makes no
general raw-compatibility claim. The original source declaration remains nested
inside the occurrence envelope, and raw value/missing state are unchanged.

## Prior residual observations

The reviewer's non-blocking observations remain as stated at `a287`:
incomplete order fields are accepted at C11 but I03 fails closed with
`INTEGRITY_FAILURE`/`UNRESOLVED`; an omitted plan on a repeated source follows
the S1 row path and is a caller-contract boundary. This repair does not expand
scope to change either behavior.
