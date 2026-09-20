# CLOSED35-R2-WVS1 — Governed Source-Specific Realization Contract

Schema: `CLOSED35_R2_WVS1_SOURCE_REALIZATION@1.0.0`

## 1. Purpose

This contract defines the single candidate-neutral governed realization for the exact canonical `WVS Wave 1.sav` source.

Candidates A, B and C may differ in physical execution strategy. They may not differ in:

- canonical source root;
- replay identity law;
- raw-versus-display treatment;
- physical missing-state treatment;
- all-system-column retention;
- the preserved weight-carrier surface;
- bounded-unknown behavior;
- semantic owner identity.

The realization consumes accepted physical/documentary authority. It does not reopen Authority71/72 adjudication and does not infer semantics from raw values.

## 2. Immutable source binding

```text
family                 = WVS
release                = Wave 1
canonical_filename     = WVS Wave 1.sav
canonical_sha256       = 051bf450568f44181559a5b2bfbe58b4f05b58bc806643d0c63353c937ff0824
source_format          = SAV
decoder_mode           = SAV_NATIVE_GOVERNED
compatibility_status   = NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE
replay_identity        = SOURCE_SHA256+ROW_ORDINAL
authority_class        = L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED
```

Authority71/72 packet preparation is not source certification. This realization does not upgrade it.

## 3. Governing authority surface

This realization freezes the accepted WVS1 holdings from:

- the CLOSED_35 canonical source-root registry;
- S35 physical edge-class court;
- Authority71 R09 WVS-other packet at accepted head `7d5e0cab3a35fb22d1396371f87d69231b2b40ad`;
- Authority72 synthesis at accepted head `3356b26f2dc518043ffde171c2dca0470b5ac79f`;
- the accepted generic R35-I01/I02/I03 contracts.

The source-native W1 codebook/questionnaire may support only the exact documentary claims already admitted by the accepted R09 packet. Absence of a dedicated W1 methodology document remains a bounded documentary limitation, not permission to infer design law.

## 4. Replay identity and native identifier evidence

The hard replay key is only:

`canonical source SHA-256 + zero-based physical row ordinal`.

Accepted source-local evidence includes:

- `V3`, documentarily named “Original respondent number”;
- `S007`, documentarily named “Unified respondent number”;
- accepted packet evidence that `V3` repeats globally;
- accepted packet evidence that `S007` is injective in the exact frozen snapshot.

None of these facts promotes either field to canonical replay identity.

The source-native semantic role of `V3` and `S007` beyond their admitted documentary names remains:

`BOUNDED_UNKNOWN`.

Injectivity is a physical/source-local property, not an authority grant.

## 5. S007 raw-storage / display nonidentity

Accepted physical sentinel:

```text
variable                = S007
display metadata        = F2.0
accepted raw minimum    = 320120001
accepted raw maximum    = 8400122325
source-native codebook  = domain through 9999999999
```

Governing law:

`RAW_STORAGE_VALUE_AND_DISPLAY_METADATA_PRESERVED_SEPARATELY`.

Therefore:

- raw stored magnitude is not truncated to display width;
- formatted/rendered text is not a physical value substitute;
- `F2.0` is preserved as display metadata;
- no width-derived parse, rounding, scaling or respondent-key semantics is authorized.

This is the WVS1 realization of S35 EC04. It adds no WVS-specific physical adapter.

## 6. Typed physical missingness

WVS1 physical missingness must remain typed.

At minimum the owner distinguishes:

- `OBSERVED_STORAGE_VALUE`;
- `SYSTEM_MISSING`;
- `FORMAT_USER_MISSING_VALUE`;
- `FORMAT_USER_MISSING_RANGE`;
- any other generic decoder physical state explicitly supplied by the accepted physical layer.

Accepted W1 fixtures include ordinary source values in declared user-missing ranges such as `-4` and `-3`, alongside system-missing states.

The realization preserves separately:

- physical state;
- raw stored code when one exists;
- source missing declaration;
- admitted documentary label when available.

It does not convert those fields into a universal semantic response ontology.

Unless exact documentary routing/applicability authority exists at the requested grain:

```text
semantic_response_state     = BOUNDED_UNKNOWN
routing_applicability_state = BOUNDED_UNKNOWN
```

A label such as “Not asked” or “Not applicable” does not make physical missingness itself a routing engine.

## 7. All-system columns

The accepted packet records eight WVS1 all-system columns.

The source-specific hostile sentinel is `I_WOMPOL`, whose accepted packet fixture preserves:

- variable identity;
- all-row system-missing incidence;
- separately declared user-missing metadata;
- no inferred applicability or semantic role.

Governing law:

`ALL_SYSTEM_DOES_NOT_MEAN_NONEXISTENT`.

Every all-system column remains part of source information and variable inventory. A candidate may represent it sparsely but may not delete it or replace its typed state with a generic null column.

Exact semantic/routing meaning remains `BOUNDED_UNKNOWN` unless separately authorized.

## 8. Exact 13-carrier weight surface

The preserved source-local weight/design carrier set is exactly:

1. `V236`
2. `SECVALWGT`
3. `RESEMAWEIGHT`
4. `WEIGHT1A`
5. `WEIGHT2A`
6. `WEIGHT3A`
7. `WEIGHT4A`
8. `WEIGHT1B`
9. `WEIGHT2B`
10. `WEIGHT3B`
11. `WEIGHT4B`
12. `S018`
13. `S019`

Accepted source-native documentary labels include:

- `V236` → “Weight”;
- `S018` → “Equilibrated weight-1000”;
- `S019` → “Equilibrated weight-1500”.

Those labels do not close sampling design, variance units, estimands, normalization law, or a lawful default among the carriers.

For all 13 carriers at current authority:

```text
role_state    = BOUNDED_UNKNOWN
design_state  = BOUNDED_UNKNOWN
estimand_state = BOUNDED_UNKNOWN
default_weight = NONE_AUTHORIZED
```

Physical presence never authorizes automatic selection, combination, normalization, or weight=1 fallback.

A later governed selector may consume an explicitly admitted source-native weight-role authority. It may not synthesize one from variable names or carrier existence.

## 9. Routing/applicability

Accepted WVS1 evidence includes large blocks of typed source missingness and all-system derived columns. It does not globally close the causal mechanism for each such state.

Accordingly:

- missingness incidence is not routing authority;
- labels are not a universal route ontology;
- country/module/ineligibility/derivation causes remain `BOUNDED_UNKNOWN` where the accepted documentary packet does not close them;
- unknown routing does not block source-specific realization because this source is L1.

No WVS4 or WVS7 routing/missing-code law may be imported into WVS1.

## 10. S35 physical edge binding

Exact applicable edge set:

```text
EC01  FORMAT_FAMILY_SAV_DTA
EC04  METADATA_VS_STORAGE_NONIDENTITY
EC05  PHYSICAL_MISSINGNESS_MULTICLASS
EC06  ALL_MISSING_COLUMN_RETENTION
EC12  WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN
EC14  COMPOUND_EDGE_INTERACTION_COURT
```

EC14 is composition law only. It requires simultaneous survival of EC01/04/05/06/12 and adds no source-special adapter.

## 11. R35 hooks

### R35-I01 — physical metadata

Required schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

WVS1-specific requirement: raw storage and display metadata remain independent witnesses. The `F2.0` declaration must coexist with the untruncated S007 raw magnitude in the candidate-neutral metadata court.

Semantic authority: `false`.

### R35-I02 — derivative parentage

Any non-direct-raw realization requires the accepted derivative-parentage chain ending at the exact WVS1 canonical SHA.

Required bundle schema:

`FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`

A derivative’s self-asserted source SHA is not ancestry proof.

Semantic authority: `false`.

### R35-I03 — whole-source physical equivalence

Required schemas:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

Exact WVS1 required physical dimensions:

- `physical_metadata`;
- `variable_inventory_order`;
- `raw_storage_values`;
- `row_replay_identity`;
- `raw_display_separation`;
- `typed_missingness`;
- `all_missing_column_retention`;
- `weight_design_variables`.

The I03 PASS token, when later earned, is only:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`.

This worker does not claim that receipt.

## 12. Candidate-neutral owner

All A/B/C candidates must bind the same deterministic:

`SOURCE_SPECIFIC_REALIZATION_IDENTITY`

derived from:

- exact source identity;
- replay law;
- raw/display nonconversion law;
- typed missing law;
- all-system retention law;
- exact 13-weight surface and nonselection law;
- bounded-unknown routing/identity/design state;
- S35 edge set;
- R35 integration schemas;
- common downstream semantic owner surface.

Candidate-specific physical optimization may change representation or cost. It may not change the governed source law.

## 13. Fail-closed law

Wrong source SHA:

`BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED`

S007 display metadata/rendering promoted to raw value:

`BLOCKED__DISPLAY_METADATA_PROMOTED_TO_STORAGE_AUTHORITY`

S007 or V3 promoted to hard replay key:

`BLOCKED__NATIVE_ID_PROMOTED_TO_REPLAY_AUTHORITY`

Physical user/system missing states collapsed:

`BLOCKED__PHYSICAL_MISSING_STATE_COLLAPSE`

All-system column deleted:

`BLOCKED__ALL_SYSTEM_COLUMN_ELIDED`

Default/estimand weight synthesized from carrier presence:

`BLOCKED__WEIGHT_ROLE_OR_DEFAULT_INVENTED`

Routing inferred from missingness:

`BLOCKED__ROUTING_INFERRED_FROM_PHYSICAL_MISSINGNESS`

Candidate semantic-owner divergence:

`BLOCKED__SEMANTIC_OWNER_DIVERGENCE`

## 14. Qualification boundary

This realization being implemented proves only:

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`.

It does not prove:

- raw WVS1 bytes were opened or executed by this worker;
- whole-source physical equivalence;
- Candidate A/B/C execution;
- I05;
- source certification;
- weighted population authority;
- measured P2X.

Those remain later qualification burdens.
