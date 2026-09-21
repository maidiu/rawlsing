# CLOSED35-R3-EVS1990 — Source-Independent Rejection Test Protocol

## Boundary

This is a browser-authored, source-independent rejection court for the declarative EVS 1990 realization.

It does not open `EVS 1990.sav`, decode real survey bytes, execute real source processing, remeasure Authority71 fixtures, execute Candidate A/B/C, materialize an R35-I03 whole-source physical-equivalence receipt, run I05, or run measured P2X.

Execution status:

`TESTS_AUTHORED__NOT_EXECUTED`

No test PASS is claimed.

## T01 — All-user-missing q745 cannot be deleted

Accepted synthetic fixture mirrors inherited authority:

- variable = `q745`;
- source ordinal = 389;
- row count = 38,213;
- every source cell physically present;
- raw code = `-5`;
- source declaration covers `-5..-1`;
- physical class = user-missing.

Required:

- variable remains addressable;
- every source row retains q745 incidence;
- raw value and declaration survive separately.

Reject:

`ALL_USER_MISSING_COLUMN_DELETION`

and:

`Q745_TREATED_AS_NONEXISTENT`

## T02 — q745 user-missing cannot be coerced into system missing or generic null

Mutate q745's physical class from source user-missing to system missing, source-cell absent, or untyped null.

Required: fail closed.

Reject:

`Q745_USER_MISSING_STATE_COLLAPSE`

Physical user-missing state is not interchangeable with system missing or column absence.

## T03 — Ranked triplets cannot be flattened

Accepted sequences:

- `q530a -> f530a -> q531b`
- `q532a -> f532a -> q533b`

with ordinals 271–276.

Reject:

- unordered set conversion;
- dropping `f530a` or `f532a`;
- swapping first/second slots;
- merging the two triplets;
- importing ranked variables from another EVS release.

Reject:

`RANKED_TRIPLET_FLATTENING_OR_DRIFT`

## T04 — Release-specific coordinates cannot be harmonized silently

Preserve EVS 1990 split-up companions:

- `country1`
- `c_abrv1`
- `cntry1_y`

as distinct from their base coordinate family.

Mutations to reject:

- aliasing split and unsplit variables;
- importing 2017 ISO semantics;
- recoding to another EVS release without authority.

Reject:

`CROSS_RELEASE_COORDINATE_HARMONIZATION`

Unresolved relation remains:

`BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`

## T05 — weight_g and weight_s cannot collapse

Accepted carriers:

- ordinal 11 `weight_g`
- ordinal 12 `weight_s`

Required: preserve both independently.

Reject:

`WEIGHT_G_WEIGHT_S_COLLAPSE`

## T06 — No default weight may be invented

Given both weight carriers and no stronger estimand authority:

Required:

- no primary weight selected;
- no weight=1 fallback;
- no normalization invented;
- no survey-design use inferred.

Reject:

`DEFAULT_WEIGHT_INVENTION`

and:

`WEIGHT_ESTIMAND_FROM_VARIABLE_NAME`

## T07 — Native IDs cannot replace replay identity

Supply `id_cocas` or `caseno` as proposed hard replay identity.

Required: reject.

Hard replay identity remains:

`CANONICAL_SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

Reject:

`NATIVE_ID_PROMOTED_TO_REPLAY_IDENTITY`

## T08 — Later-wave decoder law cannot leak backward

Accepted source condition:

`SAV_SOURCE_DECLARED_WINDOWS1252`

Reject:

- EVS 1999/2008 exact-SHA latin1 compatibility exception imported into 1990;
- later UTF-8 behavior imposed as family-wide default;
- automatic encoding fallback promoted to source authority.

Reject:

`CROSS_WAVE_DECODER_SEMANTIC_LEAKAGE`

## T09 — q745 missingness cannot mint routing/applicability semantics

Given q745 is all user-missing, attempt to infer that the question was not asked, inapplicable, or outside a routing module.

Required: reject and preserve only the accepted physical facts.

Reject:

`ROUTING_INFERRED_FROM_ALL_MISSINGNESS`

## T10 — Cross-wave semantic import is forbidden

Attempt to import into EVS1990:

- EVS1981 coordinate topology;
- EVS1999/2008 text/decoder exception;
- EVS2017 weight or ISO coordinate semantics;
- another release's q745 interpretation.

Required: fail closed.

Reject:

`CROSS_WAVE_SEMANTIC_LEAKAGE`

## T11 — Canonical source SHA is immutable

Required SHA:

`66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec`

Mutate it.

Required: fail closed before source realization.

Reject:

`SOURCE_SHA_DRIFT`

## T12 — Candidate A/B/C semantic divergence is forbidden

A/B/C must all bind:

`EVS1990_SEMANTIC_OWNER_V1`

Mutate Candidate C to:

- drop q745;
- flatten ranked triplets;
- alias weight_g/weight_s;
- choose a default weight;
- harmonize split coordinates;
- use a native ID as replay key.

Required: fail closed.

Reject:

`CANDIDATE_SPECIFIC_SEMANTIC_DIVERGENCE`

## T13 — Exact S35 edge scope is frozen

Required edge set:

`EC01;EC02;EC05;EC06;EC09;EC12;EC13`

Reject:

- deletion of a required edge;
- addition of an invented EVS1990 semantic adapter;
- promotion to EC14 without accepted matrix authority.

Reject:

`S35_EDGE_SCOPE_DRIFT`

## T14 — R35 physical receipts cannot create semantic authority

I01/I02/I03 all have `semantic_authority=false`.

Even a future I03 PASS can establish only:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

It cannot resolve:

- native-ID scope;
- weight_g estimand;
- weight_s estimand;
- relation/default use between the weights;
- cross-release coordinate equivalence.

Reject:

`PHYSICAL_RECEIPT_LAUNDERED_INTO_SEMANTIC_AUTHORITY`

## T15 — Browser implementation cannot masquerade as real-source qualification

Current required state:

- tests authored;
- tests not executed;
- no raw SAV opened;
- no real-source processing;
- no ABC execution;
- no I05;
- no measured P2X;
- no whole-source physical-equivalence PASS.

Reject:

`BROWSER_IMPLEMENTATION_PROMOTED_TO_SOURCE_QUALIFICATION`

## Later ABC qualification obligations

A later qualified execution line must separately prove:

1. canonical source SHA;
2. exact accepted reader/configuration bound to that SHA;
3. I01 physical metadata receipt;
4. I02 verified parentage for every non-direct-raw/persisted derivative;
5. I03 scope over `EC01/02/05/06/09/12/13`;
6. candidate A physical realization receipt;
7. candidate B physical realization receipt;
8. candidate C physical realization receipt;
9. q745 variable identity and every-row physical incidence survive;
10. q745 raw storage/user-missing declaration survive without system-missing collapse;
11. both ranked triplets survive;
12. split-up release coordinate family survives without harmonization;
13. `weight_g` and `weight_s` survive independently;
14. no default weight/estimand is invented;
15. common semantic owner across A/B/C;
16. any later I05 under separate authority.

## Nonclaims

This protocol does not establish:

- real source-byte execution;
- whole-source physical equivalence;
- A/B/C execution;
- I05 PASS;
- source certification beyond accepted Authority71/72;
- measured P2X.
