# CLOSED35-R3-EVS1981 — Source-Independent Rejection Test Protocol

## Boundary

This is a browser-authored, source-independent rejection court for the declarative EVS 1981 realization.

It does not open `EVS 1981.sav`, decode real survey bytes, execute real source processing, remeasure Authority71 fixtures, execute Candidate A/B/C, materialize an R35-I03 whole-source physical-equivalence receipt, run I05, or run measured P2X.

Execution status:

`TESTS_AUTHORED__NOT_EXECUTED`

No test PASS is claimed.

## T01 — Positive declared user-missing cannot become substantive response

Synthetic input:

- variable = `v308`;
- stored value = `3`;
- source missing declaration includes discrete `3`.

Required realization:

- stored value remains `3`;
- physical class is `USER_MISSING`;
- semantic class is missing;
- semantic reason remains `BOUNDED_UNKNOWN__V308_CODE3_REASON`.

Reject:

`POSITIVE_USER_MISSING_TREATED_AS_SUBSTANTIVE_RESPONSE`

A positive numeric sign is not authority to override an explicit source user-missing declaration.

## T02 — Semantic missing classification cannot erase physical storage value

Start from the same synthetic v308 state.

Apply semantic missing classification.

Required:

- `raw_storage_value == 3` still survives independently;
- source declaration survives;
- no null substitution overwrites the physical witness.

Reject:

`PHYSICAL_STORAGE_VALUE_ERASED_BY_SEMANTIC_MISSING_CLASSIFICATION`

## T03 — v308 code-3 reason cannot be invented

Given only the accepted physical declaration that code `3` is user-missing, attempt to assign a substantive missing reason.

Required:

`BOUNDED_UNKNOWN__V308_CODE3_REASON`

Reject any specific invented reason.

Reject:

`V308_CODE3_REASON_INVENTION`

The test also forbids inventing observed code-3 incidence from the declaration. The accepted aggregate fixture records observed `-1` and `-5` user-missing cells; this realization does not claim an observed code-3 count.

## T04 — Ranked triplet cannot be flattened, reordered, or cross-wave replaced

Accepted sequence:

`v460 -> f460 -> v461`

with source ordinals:

`270 -> 271 -> 272`

Mutations to reject:

- unordered set conversion;
- omission of `f460`;
- `v461` before `v460`;
- later-release ranked variable names substituted for the 1981 triplet.

Reject:

`RANKED_SLOT_FLATTENING_OR_DRIFT`

## T05 — Release-specific geography cannot be imported from another EVS release

Accepted coordinate set:

- `studyno`;
- `studynoc`;
- `version`;
- `versionc`;
- `year`;
- `country`;
- `c_abrv`;
- `cntry_y`.

Synthetic mutation adds or substitutes later-wave split coordinates such as:

- `country1`;
- `c_abrv1`;
- `cntry1_y`.

Required: fail closed.

Reject:

`CROSS_RELEASE_GEOGRAPHY_IMPORT`

Cross-release equivalence remains `BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`.

## T06 — Native ID cannot replace replay identity

Supply `id_cocas` or `caseno` as the proposed hard replay key.

Required: reject.

The accepted replay identity is:

`CANONICAL_SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

Reject:

`NATIVE_ID_PROMOTED_TO_REPLAY_IDENTITY`

## T07 — weight_g cannot become a default weight or estimand

Supply source carrier `weight_g`.

Required:

- carrier is preserved;
- no default weight is selected;
- estimand remains `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`;
- no design/normalization semantics arise from the name.

Reject:

`DEFAULT_WEIGHT_INVENTION`

and:

`WEIGHT_ESTIMAND_FROM_VARIABLE_NAME`

## T08 — Later-wave decoder law cannot leak backward

Accepted source condition:

`SAV_SOURCE_DECLARED_WINDOWS1252`

Synthetic mutations:

- force the EVS 1999/2008 UTF-8-declared latin1 compatibility mode;
- force later-wave UTF-8 behavior as family-wide default;
- claim an automatic encoding fallback is source authority.

Required: reject.

Reject:

`CROSS_WAVE_DECODER_SEMANTIC_LEAKAGE`

## T09 — Canonical source SHA is immutable

Required source SHA:

`5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2`

Mutate the source SHA.

Required: fail closed before semantic realization.

Reject:

`SOURCE_SHA_DRIFT`

## T10 — A/B/C semantic divergence is forbidden

Construct candidate bindings A, B, and C.

Required:

- all bind `EVS1981_SEMANTIC_OWNER_V1`;
- all bind the same canonical source SHA;
- all bind the same v308, rank, coordinate, weight, and bounded-UNKNOWN law.

Mutate Candidate C to treat v308=3 as substantive, choose a default weight, or import later geography.

Required: fail closed.

Reject:

`CANDIDATE_SPECIFIC_SEMANTIC_DIVERGENCE`

## T11 — Exact S35 edge scope is frozen

Required edge set:

`EC01;EC02;EC05;EC09;EC12;EC13`

Reject:

- deletion of a required edge;
- addition of an invented EVS1981 semantic adapter;
- promotion into EC14 without accepted matrix authority.

Reject:

`S35_EDGE_SCOPE_DRIFT`

## T12 — R35 physical receipts cannot acquire semantic jurisdiction

Required hooks:

- I01 physical metadata;
- I02 derivative parentage where applicable;
- I03 whole-source physical equivalence.

All are `semantic_authority=false`.

A synthetic I03 PASS may establish only:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

Reject any attempt to use a physical receipt to resolve:

- v308 code-3 reason;
- weight_g estimand;
- native-ID scope;
- cross-release coordinate equivalence.

Reject:

`PHYSICAL_RECEIPT_LAUNDERED_INTO_SEMANTIC_AUTHORITY`

## T13 — Browser realization cannot masquerade as real-source qualification

Required current state:

- tests authored;
- tests not executed;
- no raw SAV opened;
- no real-source execution;
- no ABC execution;
- no I05;
- no measured P2X;
- no whole-source physical-equivalence PASS.

Reject:

`BROWSER_IMPLEMENTATION_PROMOTED_TO_SOURCE_QUALIFICATION`

## Later ABC qualification obligations

A later qualified execution line must separately prove, without changing the semantic owner:

1. exact canonical source SHA;
2. exact accepted reader/decoder/version/config bound to that SHA;
3. I01 physical metadata receipt;
4. I02 verified parentage for every non-direct-raw or persisted derivative carrier;
5. I03 source scope over `EC01/02/05/09/12/13`;
6. candidate A physical realization receipt;
7. candidate B physical realization receipt;
8. candidate C physical realization receipt;
9. preservation of raw v308 values plus its positive user-missing declaration;
10. preservation of `v460/f460/v461` topology;
11. preservation of the EVS 1981 coordinate tuple;
12. preservation of `weight_g` without default-use invention;
13. common candidate-neutral semantic owner across A/B/C;
14. any later I05/semantic parity under its own separate authority.

## Nonclaims

This authored protocol does not establish:

- real source-byte execution;
- whole-source physical equivalence;
- A/B/C execution;
- I05 PASS;
- source certification beyond accepted Authority71/72;
- measured P2X.

