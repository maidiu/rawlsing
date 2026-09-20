# CLOSED35-R2-WVS1 — Source-Independent Test Protocol

## Boundary

Implementation under test:

`rawlsing_next/closed35_wvs1_realization.py`

Synthetic/source-independent test file:

`rawlsing_next/tests/test_closed35_r2_wvs1_realization.py`

This protocol does not open `WVS Wave 1.sav`, execute source decoding, materialize whole-source output, run Candidate A/B/C, run I05, or run measured P2X.

Execution status:

`TESTS_AUTHORED__NOT_EXECUTED`

The browser/GitHub worker authors the hostile court but does not fabricate a test PASS.

## T01 — S007 raw magnitude vs F2.0

Synthetic input:

- variable `S007`;
- raw storage value `320120001`;
- display metadata `F2.0`;
- arbitrary display rendering `"32"`.

Required:

- raw storage remains exactly `320120001`;
- display metadata remains `F2.0`;
- display rendering remains a separate metadata/rendering witness;
- no truncation, width parse, scaling, rounding, or respondent-key inference.

Reject any result that turns `F2.0` into storage authority.

## T02 — display string as physical value

Mutation:

Supply a display string such as `"32"` as the S007 raw-storage value.

Required result:

REJECT.

Reason:

The accepted S007 hostile law requires numeric raw storage to remain independent of display rendering.

## T03 — S007 uniqueness as replay authority

Synthetic evidence:

`S007` is declared source-locally injective.

Required:

- retain injectivity evidence;
- retain documentary name;
- `replay_authority = false`;
- semantic identity role remains `BOUNDED_UNKNOWN`;
- hard replay key remains exact source SHA + row ordinal.

Mutation:

Promote S007 to hard replay authority.

Required result:

REJECT.

## T04 — all-system column deletion

Synthetic witness:

`I_WOMPOL` with `row_count = system_missing_count = 13586`, plus separate declared user-missing metadata.

Required:

- variable retained;
- all-system state retained;
- declared missing metadata retained separately;
- semantic/routing state remains `BOUNDED_UNKNOWN`.

Mutation:

Represent an all-system column as absent or use a non-all-system count in the all-system projection.

Required result:

REJECT.

## T05 — typed missing collapse

Synthetic pair:

1. `V106` = `FORMAT_USER_MISSING_RANGE`, raw `-4`, declared range `[-5,-1]`, documentary label “Not asked”;
2. `I_WOMPOL` = `SYSTEM_MISSING`, no ordinary raw code.

Required:

- physical states stay distinct;
- raw `-4` remains preserved for the user-missing state;
- system missing remains no ordinary storage code;
- neither state generates a routing/applicability state.

Mutation:

Encode system missing as ordinary `-99`.

Required result:

REJECT.

## T06 — automatic default-weight selection

Required positive surface:

all 13 exact carriers are present in deterministic order:

`V236, SECVALWGT, RESEMAWEIGHT, WEIGHT1A, WEIGHT2A, WEIGHT3A, WEIGHT4A, WEIGHT1B, WEIGHT2B, WEIGHT3B, WEIGHT4B, S018, S019`.

For every carrier:

- role = `BOUNDED_UNKNOWN`;
- design = `BOUNDED_UNKNOWN`;
- estimand = `BOUNDED_UNKNOWN`;
- selected_by_default = `false`.

Mutations:

- ask for an implicit/default weight;
- ask to select `V236` merely because its label is “Weight”;
- infer a carrier role from a name/suffix.

Required result:

REJECT unless a later explicit source-native weight-role authority object is supplied.

## T07 — source SHA drift

Exact canonical SHA must admit.

Any changed SHA must reject.

No same-wave alternate source, extracted derivative, or filename match substitutes for the root.

## T08 — V3 does not become global identity

Synthetic source-local V3 evidence may record repetition/noninjectivity.

Required:

- preserve the physical V3 value;
- preserve documentary name;
- replay authority remains false;
- semantic role remains `BOUNDED_UNKNOWN`.

No country/V3 or cross-release identity is synthesized.

## T09 — A/B/C share one owner

Construct A/B/C bindings to the exact canonical root.

Required:

all three share the exact same `SOURCE_SPECIFIC_REALIZATION_IDENTITY`.

Mutation:

change Candidate C’s realization identity.

Required result:

REJECT.

## T10 — exact S35/R35 scope

Required edge set:

`EC01; EC04; EC05; EC06; EC12; EC14`.

Required I03 physical dimensions:

- `physical_metadata`;
- `variable_inventory_order`;
- `raw_storage_values`;
- `row_replay_identity`;
- `raw_display_separation`;
- `typed_missingness`;
- `all_missing_column_retention`;
- `weight_design_variables`.

Required:

- R35-I01 semantic authority = false;
- R35-I02 is required for non-direct-raw realizations;
- R35-I03 semantic authority = false;
- EC14 adds no source-specific adapter.

## Later qualification extension

A later authorized A/B/C qualification court must additionally:

1. verify the exact canonical WVS1 bytes and SHA;
2. freeze the exact governed reader/config identity;
3. materialize R35-I01 physical metadata;
4. materialize R35-I02 lineage for any non-direct realization;
5. freeze one R35-I03 canonical expectation over the exact WVS1 edge scope;
6. execute candidate A and obtain a physical realization receipt;
7. execute candidate B and obtain a physical realization receipt;
8. execute candidate C and obtain a physical realization receipt;
9. require common WVS1 `SOURCE_SPECIFIC_REALIZATION_IDENTITY`;
10. run the separate downstream semantic/parity court required by the architecture.

This worker claims none of those execution receipts.
