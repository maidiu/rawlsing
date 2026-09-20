# FIABC-R35-I03 — Physical Equivalence Receipt Contract

## 1. Separation of courts

This contract is upstream/orthogonal to I05 semantic parity.

`PHYSICAL_EQUIVALENCE PASS` means the declared source-native physical scope survived the candidate realization.

It does not imply:

`SEMANTIC PASS`

`SOURCE CERTIFIED`

`POPULATION/WEIGHT AUTHORIZED`

`DOCUMENTARY AUTHORITY CLOSED`.

A later semantic court may fail after physical equivalence passes. A semantic court may also pass while this physical court fails.

## 2. Candidate-neutral expectation

The canonical expectation contains:

1. canonical source family/release/filename/format/SHA;
2. exact frozen reader/config payload;
3. reader/config digest bound to canonical source SHA;
4. source-declared S35 edge classes;
5. derived minimum evidence dimensions;
6. candidate-neutral canonical physical evidence digests;
7. an external VERIFIED R35-I01 physical-metadata binding and its digest;
8. an expectation identity over the complete frozen object.

No candidate ID or candidate-owned cache/result is part of canonical truth.

## 3. Reader/config identity

The exact identity preimage is:

`source SHA + decoder implementation + decoder version + decoder mode + config + compatibility mode + compatibility semantic scope`.

Changing any member changes reader/config identity.

Compatibility execution may remain physically lawful but has zero source-text or semantic authority.

## 4. Evidence dimensions

Whole-source baseline:

- `physical_metadata`
- `variable_inventory_order`
- `raw_storage_values`
- `row_replay_identity`

Edge-specific dimensions are derived from the source's exact S35 declaration. An expectation may declare additional physical dimensions when the source contains further source-native information. Candidate realizations must preserve every expectation dimension; candidate-local extra audit dimensions are allowed but are not used as truth.

This avoids demanding MR/form/weight/etc. fields from sources where those classes are inapplicable while still preventing a narrow workload cache from masquerading as whole-source equivalence.

## 5. I01 metadata seam

The external metadata binding must be VERIFIED and bind:

- receipt identity;
- canonical source SHA;
- canonical physical metadata digest;
- producer/contract identity.

Its digest is the physical source's required raw-layout/file/display metadata witness. Thus a candidate that normalizes Latinobarometro 2024's 174 header witness into the 332 stream width changes the metadata digest and fails. Likewise raw-vs-display collapse changes the expected physical state.

I03 does not infer which conflicting witness is semantically correct. It preserves both physical witnesses as governed metadata.

## 6. I02 derivative-parentage seam

Every realization other than `DIRECT_RAW` requires an external VERIFIED parentage binding.

Required minimum fields:

- receipt identity;
- parent receipt identity;
- canonical source SHA;
- derivative identity;
- producer identity;
- derivation operation;
- exact reader/config digest;
- `CURRENT_AND_SCOPE_COMPLETE` state.

The parentage binding may not claim semantic authority.

Therefore:

`derivative.source_sha256 == canonical SHA`

without an external parentage receipt is mechanically insufficient.

## 7. Candidate realization

A/B/C may realize the physical state differently internally. A candidate descriptor binds:

- candidate ID;
- expectation identity;
- canonical source identity;
- exact reader/config and digest;
- exact source edge-class declaration;
- I01 metadata binding;
- physical evidence digests;
- direct-raw or derivative realization class;
- I02 parentage receipt if derivative;
- optional semantic-observation digest for audit only.

The semantic observation is explicitly never used as physical truth.

## 8. PASS rule

PASS requires all of:

- expectation integrity;
- exact canonical source identity;
- exact reader/config payload and digest;
- exact S35 edge declaration;
- exact canonical physical-metadata digest;
- every canonical physical evidence dimension present and digest-equal;
- valid derivative parentage for non-raw realization.

The PASS receipt names matched physical dimensions and carries four explicit negative claims:

- semantic parity not claimed;
- source certification not claimed;
- documentary semantic authority not claimed;
- weight/population authority not claimed.

## 9. EC14

EC14 is not another adapter. It is a composition meta-class.

A scope declaring EC14 must declare multiple atomic S35 classes. The receipt then requires simultaneous survival of all dimensions implied by those atomic classes. Passing one cannot compensate for failing another.
