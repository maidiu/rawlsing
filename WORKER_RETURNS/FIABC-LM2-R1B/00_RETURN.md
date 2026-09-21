# FIABC-LM2-R1B — R6S / C11 Mapping-Authority Contract Archaeology

Status: `COMPLETE__HISTORICAL_COMPOSITION_CONTRADICTION_LOCATED__MINIMUM_RERUN_BOUNDARY_PROVED`

Terminal:

`FIABC_LM2_R1B_R6S_C11_CONTRACT_ARCHAEOLOGY_COMPLETE__MINIMUM_RERUN_BOUNDARY_PROVED`

## Exact worker coordinates

- Repository: `maidiu/rawlsing`
- Branch: `agent/rabochii-premain-fiabc-lm2-r1b-r6s-c11-authority-archaeology-r1`
- Exact base: `bf0f4ebb00e7304e1cda29f7ca9b6595fff248dc`
- Return: `WORKER_RETURNS/FIABC-LM2-R1B/`

## Holding

The LM2 blocker is a **later composition contradiction between independently accepted contracts**, not evidence that the original PRE553 authority ontology intended `SOURCE_SEMANTICS_TOPOLOGY` to satisfy native-to-canonical mapping claims.

The authority ontology deliberately separated the two claims from its first implementation:

- `SOURCE_SEMANTICS_TOPOLOGY`: source-native question/component meaning, response values/special states, and topology.
- `NATIVE_CANONICAL_MAPPING_HARMONIZATION`: native-to-canonical identifier/value transformation.

The C11 integrity layer then deliberately required positive `NATIVE_CANONICAL_MAPPING_HARMONIZATION` whenever a `RespondentEvent` contains canonical question or canonical response material.

That guard predates R6S by about a month.

The later R6S WVS7 materializer preserved the question boundary correctly — its `QuestionVariableBinding` leaves `canonical_question_ref_or_typed_absence=NOT_AUTHORIZED` — but crosses the boundary in the substantive response-value lane:

`canonical_value=str(code)`

paired with:

`transform_authority_ref=SOURCE_AUTH_REF`

where `SOURCE_AUTH_REF` is exact kind:

`SOURCE_SEMANTICS_TOPOLOGY`.

That construction is the exact historical divergence now rejected by C11.

## What history proves

### 1. The ontology split is original, not a later tightening

Commit:

`2faacc3f084cf65e61843f1692b947177a617013`

introduced both authority kinds simultaneously in `pre553_empirical_authority.py`.

Its original operation ceilings already distinguished:

- source interpretation operations under `SOURCE_SEMANTICS_TOPOLOGY`;
- `MAP_NATIVE_CANONICAL_IDENTIFIER` / `MAP_NATIVE_CANONICAL_VALUE` under `NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

No inspected later change merged those meanings.

### 2. C11's positive mapping check is also old and intentional

Commit:

`e6cb975e1b2e401279c5580955464f6976929804`

introduced the C11 carrier integrity layer. The current accepted file remains exact blob:

`7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd`.

For `RespondentEvent`, any non-null canonical question or canonical response field requires a positive exact authority of kind:

`NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

The ingest hostile court also explicitly rejects unauthorized canonical promotion.

### 3. The generic source-backed facade did not authorize source semantics as canonical mapping

The C05-R2A source-backed facade was introduced at:

`91315bd3df9bd7f5e710d9791cc8be0bb96173fb`

and hostile/parity tests followed at:

`018960039aa8cad19576e915e0358b5c05461ff7`.

The facade exposes separate fields:

- `canonical_value`;
- `transform_authority_ref`.

It passes those directly into C11 and does not itself reinterpret authority.

Its accepted proving fixtures use `SOURCE_SEMANTICS_TOPOLOGY` for source semantics but leave response `canonical_value` and transform authority absent. Thus C05-R2A did **not** establish a precedent that source-semantics authority may populate canonical response material.

### 4. Accepted WVS7 history contains the opposite precedent

The accepted G-SR07-R2A WVS7 ownership bridge, commit:

`a06f2bced8677453cf77fec5e622cb334a9810a5`

authorized source-semantic `RespondentEvent` ownership without granting canonical respondent/question/value mapping.

Later, the accepted HB01 Full GSR07 R2 real-source certification:

`a07e2a9a9c5299b80296aed323b7912192b31ddd`

successfully constructed a WVS7 C11 release while leaving:

- canonical question = `NOT_AUTHORIZED`;
- response canonical value = absent;
- response transform authority = absent.

That real-source court passed source-backed/direct I03 parity and was HQ-closed by:

`3468673673db2f3de804d6e825585f86ff98e870`.

This is a concrete accepted WVS7 precedent for **native/source-semantic C11 material without canonical mapping promotion**.

### 5. R6A and P2F2 closed source-native semantics, not native→canonical mapping

R6A commit:

`4b141b8b5748175e34c9286eba36f53d8df1e9d5`

explicitly describes its result as source-native response semantics and preserves source-native distinctions rather than harmonizing them.

P2F2 then issued exact source authority:

`EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY`

with authority hash:

`c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`

of kind:

`SOURCE_SEMANTICS_TOPOLOGY`.

No `NATIVE_CANONICAL_MAPPING_HARMONIZATION` snapshot appears in the inspected P2F2 WVS7 authority bundle.

### 6. R6S is where the two lanes were composed incorrectly

Current accepted R6S materializer blob:

`11b28416aac5a4899706150721f2f8ac8bb6ee43`.

It correctly leaves question canonical mapping unauthorized, but for substantive response codes 1..5 it constructs:

- `canonical_value=str(code)`;
- `transform_authority_ref=SOURCE_AUTH_REF`.

The referenced authority remains `SOURCE_SEMANTICS_TOPOLOGY`.

R6S browser qualification did not establish a real common-C11 response-value build: its return explicitly reports deterministic/browser fixtures, no real WVS carrier, and no empirical outcome execution. The mismatch therefore remained latent until LM2 attempted the candidate-neutral common C11 build against the accepted C11 validator.

There is no evidence in the inspected lineage that this mismatch was knowingly accepted as an authority exception.

## Existing mapping authority / derived-authority findings

No already-accepted **WVS7** positive authority of kind `NATIVE_CANONICAL_MAPPING_HARMONIZATION` was found in the inspected R6A, P2F2, R6S, GSR07, HB01, C05-R2A, I01, or I02 lineage.

The archaeology does find accepted precedent for:

1. source-native C11 response material with canonical fields absent; and
2. exact authority objects derived mechanically from already-accepted premises for other authority families.

But history alone does **not** prove that a new WVS7 native→canonical mapping authority may be minted from R6A/P2F2 semantics. That semantic adjudication belongs to LM2-R1A/R1C or HQ. Worker B does not create it.

## Minimum lawful rerun boundary

The frozen physical/source chain remains untouched:

- canonical WVS7 source receipt: unchanged;
- structural preimage identity `151907b3…`: unchanged;
- derivative parentage receipt: unchanged;
- parentage bundle `5037c55b…`: unchanged;
- Lock2 `8e5842eb…`: unchanged;
- canonical physical expectation `9845c24d…`: unchanged.

No source reread is historically justified by this semantic-authority reference defect.

For any lawful repair that changes only the source-specific semantic projection / mapping authority layer, recovery can restart no earlier than:

`CANDIDATE_NEUTRAL_COMMON_C11_BUILD`

using the already frozen structural preimage and source/authority/workload freezes.

The common C11 release must be rebuilt/revalidated because its public objects and closure refs are downstream of the repaired semantic projection.

The independent oracle was never frozen and therefore must be constructed fresh only after the repaired common C11 build succeeds.

Candidate A/B/C remain prohibited until that oracle freeze exists.

## Common-return boundaries

- WVS7 source opened by this worker: **NO**
- structural preimage regenerated: **NO**
- Candidate A/B/C process started: **NO**
- I03 executed: **NO**
- I05 executed: **NO**
- measured P2X executed: **NO**
- new semantic authority silently minted: **NO**
- frozen LM2 physical/source evidence altered: **NO**
