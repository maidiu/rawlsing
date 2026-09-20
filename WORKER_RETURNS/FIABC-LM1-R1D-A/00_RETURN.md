# FIABC-LM1-R1D-A — C11 Physical-Value / Semantic-Identity Boundary Adjudication

Repository: `maidiu/rawlsing`

Base:

`agent/rabochii-premain-fiabc-lm1-r1c-governed-r5-rebuild-r1@ca3630f5f7146f611c8cdc30b010eab509a5145b`

Branch:

`agent/rabochii-premain-fiabc-lm1-r1d-a-c11-boundary-adjudication-r1`

Return:

`WORKER_RETURNS/FIABC-LM1-R1D-A/`

## Result

**PASS at adjudication/contract grain.**

Terminal:

`FIABC_LM1_R1D_A_C11_PHYSICAL_SEMANTIC_BOUNDARY_ADJUDICATED__MINIMAL_REPAIR_CONTRACT_READY`

A lawful bounded representation exists. The current R1C consumer failure does not require binary floats to enter generic C11 semantic numeric identity and does not require another R5 rebuild.

The defect is an ontology crossing:

`exact physical observation -> semantic canonicalize()`

where the correct law is:

`exact physical observation -> exact typed physical material`

followed, only when separately authorized, by:

`physical/source witness -> semantic canonical value`.

## Core holding

Three roles are distinct.

### A — Physical identity material

Purpose: deterministic exact identity of what the governed physical boundary observed.

A uses the already accepted typed representation vocabulary:

`PRE553_R5_TYPED_VALUE_CODEC@1.0.0`

but uses it only as physical material.

A physical binding identity must include:

- typed raw physical value;
- `PhysicalMissingState`;
- typed source missing declaration.

It must not call semantic `canonicalize(raw_value)`.

### B — Raw-source witness material

Purpose: preserve the physical source value inside a C11 object without claiming numeric or semantic meaning.

B may use a domain-tagged JSON-safe envelope around the same typed physical token.

This is lawful because C11 may hash an opaque witness structurally without interpreting the inner float bits as a semantic number.

### C — Semantic/canonical value

Purpose: represent only a value admitted by semantic authority.

C continues to use:

`pre553_empirical_objects.canonicalize()`.

No change is authorized to its binary-float prohibition.

A or B becomes C only through explicit source/transform/crosswalk/weight authority. Numeric equality or host-language coercion is not authority.

## Exact requested cases

The admitted physical representation preserves:

- finite float64 exact IEEE-754 bits;
- `+0.0` as bits `0000000000000000`;
- `-0.0` as bits `8000000000000000`;
- decoder-observed NaN as `float64_nan_decoder_state`;
- `+inf` as `float64_pos_inf`;
- `-inf` as `float64_neg_inf`;
- int separately from float;
- bool separately from int;
- string `"inf"` separately from infinity.

No NaN payload bits are invented.

No nonfinite state is reinterpreted as missingness.

If an upstream physical decoder has already normalized away information before this boundary, this contract does not reconstruct it retroactively.

## Why the existing R5 representation is sufficient for A/B

Evidence:

- `rawlsing_next/pre553_r5_codec.py`
  - blob `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540`
  - explicitly owns physical representation only;
  - finite float64 uses exact bits;
  - NaN/infinities have separate typed lanes;
  - bool/int/float/string equality is noncollapsed.

- accepted Candidate-A source-backed adapter:
  - owner `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`
  - blob `d4915e7e6755ba1850756aebff72f982f73a332b`
  - validates the typed R5 representation and restores `PhysicalCell.raw_value`;
  - does not assign semantic meaning.

Therefore the failure occurs **after** successful physical preservation, at the generic C11 boundary.

## Why generic canonicalize must remain unchanged

`rawlsing_next/pre553_empirical_objects.py`

blob:

`a61365b994e5c3c50de0f598fcf40e90abf757b6`

states that `canonicalize()` returns deterministic JSON-safe **semantic** material and rejects Python floats, NaN, and infinity.

That prohibition remains correct for C.

The repair is not:

- globally accepting floats;
- float→Decimal;
- float→Fraction;
- float→repr string;
- NaN/Infinity→None;
- NaN/Infinity→missing;
- dropping nonfinite cells.

## Current facade seams requiring repair/revalidation

`rawlsing_next/pre553_source_backed_c11_facade.py`

current R1C blob:

`c3647800f52fa81fdef34be6692207e092c48ee2`

Affected:

1. `physical_value_binding_key` — A;
2. source missing declaration inside physical binding — A;
3. response rule physical keys — A;
4. coordinate rule physical keys — A;
5. weight rule physical keys — A;
6. `RespondentEvent.raw_response_value` — B;
7. `EmpiricalCoordinateFact.raw_coordinate_value` — B;
8. weight raw-copy / exact-number conversion boundary — C, not B;
9. downstream raw-value query fallback — must treat B as opaque unless semantic authority binds it.

The exact seam matrix is in `03_AFFECTED_C11_SEAMS.csv`.

## Historical Decimal conversion is not adopted

The historical banked LiTS mechanical court:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

contains a local:

`float -> Decimal(str(value))`

shim specifically to make pyreadstat floats admissible to the semantic carrier.

That is evidence of the old boundary mismatch, not governing authority for this repair.

It does not preserve exact binary-float physical identity and cannot lawfully solve NaN/infinity.

Historical response physical keys constructed against Decimal surrogates must therefore be revalidated under the repaired physical-key law; they may not be silently assumed equivalent to float/int states.

## Weight holding

A weight cell has an A physical identity like every other cell.

However:

`WeightMeasureFact.exact_weight_value_representation`

is C, because query execution parses and uses it arithmetically.

It is not a place to store a B raw physical token.

`copy_observed_numeric` therefore cannot be generalized into a physical-preservation rule. Any physical-float→semantic-exact-number conversion remains authority-governed.

The current LiTS proving projection has no active weight slot, so no LiTS weight semantics are minted by this worker.

## Minimal repair

The minimal contract is:

1. reuse the existing typed physical codec representation at the source-backed C11 seam;
2. create a narrow exact physical material/witness function;
3. make `physical_value_binding_key` hash domain-separated physical material, not semantic material;
4. carry typed raw witnesses in raw response/coordinate fields;
5. leave semantic canonical values and `canonicalize()` unchanged;
6. regenerate/revalidate physical-key producers under the same exact physical law;
7. revalidate predicates/query domains that previously treated raw values as semantic values.

No R5 carrier rebuild is ordered by this worker.

Whether existing carrier/manifests/receipts require reseal, revalidation, or identity-only recomputation is outside Worker A and belongs to the dependency/rerun court.

## R1C frozen evidence preserved

This worker does not alter or consume the accepted R1C carrier evidence:

- root `7d85c5e4c3a91c3f6dc8f7896fe487cda116fc8cf67f0ab263a2654ff938afcd`;
- logical stream `076c6527f292c1d4ae2cce53c1f0363093eb9a5b5fb652edd96b448823589aba`;
- rows `34,745,595`;
- members `2,121`;
- member inventory `04dce8c3e942fc81a0558354c21a4b4a56faab417ce362657286f978b6686703`;
- parentage bundle `8b63de4ea902350ce197bc3ed49b59259bef2ad400c9f3c7db65ac96b015ace7`.

Replacement-success authority remains unconsumed.

## Execution boundary

Observed:

- GitHub/browser repository inspection only.

Not done:

- no local LiTS bytes;
- no local R5 carrier;
- no R5 rebuild;
- no Candidate A/B/C execution;
- no I03/I05;
- no measured P2X;
- no repair implementation beyond illustrative contract pseudocode.

## Outputs

- `00_RETURN.md`
- `01_ONTOLOGY_ADJUDICATION.md`
- `02_EXACT_PHYSICAL_VALUE_REPRESENTATION.json`
- `03_AFFECTED_C11_SEAMS.csv`
- `04_MINIMAL_REPAIR_CONTRACT.md`
- `RETURN.json`

