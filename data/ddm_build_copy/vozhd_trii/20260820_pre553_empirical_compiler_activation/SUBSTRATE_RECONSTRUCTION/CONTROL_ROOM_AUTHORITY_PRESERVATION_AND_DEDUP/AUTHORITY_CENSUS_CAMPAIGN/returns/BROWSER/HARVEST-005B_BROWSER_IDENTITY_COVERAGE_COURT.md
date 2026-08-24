# HARVEST-005B — Browser Current-35 Question-Occurrence Identity & Existing-Authority Coverage Court

Status: `READY_ON_BROWSER_EVIDENCE__FINALIZE_AFTER_H005L_LOCAL_DELTA`

## Authority question

Across the governed current-35 scope, what mechanically defensible candidate question/variable occurrence identities exist across the available source/codebook/master/register/relation authority surfaces, and which existing authority carriers bind to each occurrence at what cardinality?

This is a Browser-owned relational evidence court. It does not create canonical question identity or new semantics.

## Inputs already available to Browser

Normative availability list:

`H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`

Browser already holds:

- exact H001-H004 ZIP bytes and every member;
- accepted current-35 GitHub identity/scope surfaces;
- accepted/recovered semantic, driver, structure, FQRA/QSM/QRA/response/negative authority surfaces available through GitHub or prior packets;
- Library filesystem/tree SHA indexes;
- H005L local delta when returned.

## Browser computation plan

### 1. Carrier schema census

Read each distinct identity-bearing carrier once.

For each carrier record:

- exact content identity;
- rows and columns;
- source/wave coordinates;
- item/question IDs;
- variable names;
- source-native/codebook IDs when present;
- text fields and deterministic text hash when text exists;
- parent/child/battery/constructed-column coordinates when explicit;
- duplicate counts for each identity coordinate actually present.

No authority is inferred from the fact that a carrier is newer or wider.

### 2. Candidate occurrence relation

Construct a unioned candidate-occurrence relation from mechanically identifiable source/wave/question coordinates.

Preserve the raw identity coordinates from each originating carrier.

Do **not** invent the final `question_uid`.

A temporary Browser computation key may be used only as an internal row handle and must not be represented as governed identity.

### 3. Indexed carrier joins

Use DuckDB/Polars/pandas hash-indexed relational operations or equivalent.

Naive nested row scans are forbidden.

For every carrier membership, report:

- exact join fields;
- `EXACT_UNIQUE`;
- `EXACT_ONE_TO_MANY`;
- `EXACT_MANY_TO_ONE`;
- `AMBIGUOUS_DUPLICATE`;
- `UNMATCHED`;
- `KEY_UNAVAILABLE`.

One-to-many relationships remain rows. Physical duplicates are not silently collapsed.

### 4. Collision census

Mechanically inspect collisions under historically/currently used coordinates including:

- `item_id`;
- `(source,wave,var_name)`;
- question ID;
- source/codebook variable ID;
- text hash;
- governed source/wave UID where available.

Explicitly isolate:

- H004 GSS/LiTS d62 identity mismatch layer;
- V525b natural-key duplicates/blank keys;
- variable-code reuse across waves;
- blank-ID cases;
- one source/wave/var with conflicting IDs/text;
- one item/question ID bound to conflicting source occurrence coordinates.

### 5. Coverage census

By governed family/wave and carrier, report descriptive counts for:

- candidate occurrences;
- unique candidate identity tuples under each tested coordinate law;
- semantic authority/carrier presence;
- driver/facet carrier presence;
- question-structure presence;
- FQRA presence;
- QSM/QSMv2 presence where joinable;
- response/direction/manual/negative authority presence where explicitly joinable;
- ambiguous joins;
- blank critical identity fields.

`uncovered` is descriptive only.

### 6. Browser adjudication after mechanics

After the mechanical relations exist, Browser may adjudicate:

- which identity coordinates are reliable enough to contribute to the future question-occurrence identity law;
- which collisions require explicit identity reconciliation;
- what relation cardinalities the unified substrate must encode;
- which existing authority can be bound cleanly and which remains ambiguous;
- what evidence remains genuinely absent;
- the Trii/Chetiri dependency implications.

No semantic/content adjudication is implied merely by identity binding.

## Planned Browser outputs

- `CURRENT35_QUESTION_OCCURRENCE_CANDIDATE_UNIVERSE.csv`
- `QUESTION_IDENTITY_CROSSWALK.csv`
- `AUTHORITY_CARRIER_COVERAGE_MATRIX.csv`
- `QUESTION_IDENTITY_COLLISION_LEDGER.csv`
- `COVERAGE_COUNTS_BY_FAMILY_WAVE.csv`
- `CARRIER_IDENTITY_AND_SCHEMA_RECEIPT.csv`
- `COVERAGE_MECHANICAL_RECEIPT.json`
- `HARVEST-005B_ADJUDICATION.md`

These outputs belong in the Browser Control Room, not in a local evidence ZIP.

## Forbidden

- no source/authority mutation;
- no canonical `question_uid` invention before the identity-law court;
- no deduplication by row order;
- no text-similarity equivalence promotion;
- no `uncovered => missing` inference;
- no semantic authority creation;
- no d62 repair;
- no flattening of legitimate one-to-many authority assertions.

## Completion condition

H005B closes when Browser has a reproducible current-35 candidate identity/coverage relation from all Browser-held evidence plus the H005L delta, with every ambiguous mapping preserved and every unresolved identity class explicit.
