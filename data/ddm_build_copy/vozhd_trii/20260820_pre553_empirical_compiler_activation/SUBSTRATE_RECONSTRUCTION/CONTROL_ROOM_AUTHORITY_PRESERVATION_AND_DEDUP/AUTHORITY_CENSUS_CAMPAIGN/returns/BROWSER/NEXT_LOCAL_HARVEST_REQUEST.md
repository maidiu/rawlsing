# HARVEST-005 — CURRENT-35 QUESTION-OCCURRENCE IDENTITY AND EXISTING-AUTHORITY COVERAGE BASELINE

Status: `ISSUED__AWAITING_LOCAL_PACKET`

## Exact authority question

Across the governed current-35 survey scope, what exact question/variable occurrence identities are physically represented by the present source/codebook/master/register authority surfaces, and which existing semantic/driver/structural authority carriers cover each occurrence?

This is an **identity and coverage census**, not a semantic-adjudication or repair task.

The objective is to build the mechanical identity spine needed for the future unified empirical-authority substrate and the later full-universe quality court, while preserving disagreements among existing carriers rather than collapsing them.

## Governing findings from H001–H004

Browser has established:

- current scope is 35 active family-wave identities, EVS1999 included and Asian Barometer W6 excluded;
- the 18,792-row question-structure register has an invariant manual/source-topology core across its recovered lineage;
- V525b 6,211-row semantic/driver masters are accepted historical structural authority for their historical scope;
- later `questions_master_semantic.csv` SHA `171d399d...` is a generated/heuristic carrier, not a proved lossless successor;
- later `questions_master_drivers.csv` SHA `d62accad...` is not safe as a flat question authority: H004 proves the GSS/LiTS updater appended a second representation of 10,455 already-present natural question keys because old rows lacked `item_id`, after which a downstream `(source,wave,var_name)` dict made row order effective precedence;
- row-order precedence is not semantic authority;
- the future canonical system therefore needs one governed question-occurrence identity spine and separately-grained authority assertions.

## Search roots

- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

Use checkout/repository authority first for governed scope identities where available. Local filesystem bytes remain evidence candidates until Browser adjudication.

## Primary identity surfaces

Locate and hash every distinct relevant occurrence of:

- `questions_master.csv`
- `questions_master_semantic.csv`
- `questions_master_drivers.csv`
- `question_structure_register.csv`
- current source/wave identity registries/manifests
- `SOURCE_BYTE_INVENTORY.csv`
- current final codebook/question-index surfaces used to create or normalize question identities
- FQRA question-relation authority carrier(s) where they expose source/wave/question identity
- QSM/QSMv2 carriers where they expose source/wave/question identity
- response-scale/directionality/manual-authority carriers only to the extent needed to mechanically report coverage by question identity; do not recursively harvest their full provenance in this packet.

Known exact identities that must be recognized, not silently substituted:

- later semantic master: `171d399da7e0f2bbd66dcce08a6c353978e48b69fee8d32ac6b1720d10d70ca5`
- later driver master: `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`
- V525b semantic master: `6e76965c1e00c90e1ae4a4647f99b851dc558a345c2a2792151143cb35fe2fc0`
- V525b driver master: `53feb28296705d2005f8c3d2548c136e2c15fabd62c103694f05caa555063711`
- question-structure Register A: `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84`
- Register B: `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b`
- current recovered Register C: `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219`

## Mechanical identity work

### A. Enumerate candidate question occurrences

For each mechanically identifiable question/variable occurrence, preserve all available source identity coordinates rather than choosing one prematurely:

- source family
- wave label as stored
- governed/current wave identity if an existing accepted registry supplies one
- item/question ID
- variable name
- question text hash where text exists
- source/codebook variable identity
- source file / codebook identity where available
- parent/child or constructed-column identity where explicitly represented

Do not invent a new canonical `question_uid`. Instead emit a deterministic **candidate identity tuple** and enough raw coordinates for Browser to define the future UID law.

### B. Build cross-carrier membership flags

For every candidate occurrence, mechanically report whether and how it appears in each located carrier, at minimum:

- questions master
- semantic master(s)
- driver master(s), preserving multiple physical rows rather than collapsing duplicates
- question-structure register
- FQRA
- QSM/QSMv2 if exact question identity is available
- response/directionality/manual authority presence when mechanically joinable by an existing explicit key

For each membership, record the exact join fields and whether the relationship is:

- exact unique
- exact one-to-many
- exact many-to-one
- ambiguous duplicate
- unmatched
- key unavailable

Do not resolve ambiguous joins.

### C. Duplicate/collision census

Mechanically enumerate collisions under all identity coordinates actually used by historical/current code, including when present:

- `item_id`
- `(source,wave,var_name)`
- question ID
- source/codebook variable
- question text hash

Explicitly isolate:

- the known GSS/LiTS d62 duplicate layer;
- the 7 duplicated V525b natural keys / 9 excess rows;
- variable-code reuse across waves;
- blank-ID cases;
- same question text attached to different source identities;
- same source/wave/var attached to conflicting IDs or texts.

Do not deduplicate.

### D. Coverage counts

Produce exact counts by current family/wave and carrier for:

- candidate question occurrences;
- unique candidate identity tuples;
- semantic-master covered/uncovered;
- driver-master covered/uncovered;
- structure-register covered/uncovered;
- FQRA covered/uncovered;
- ambiguous or duplicate mappings;
- blank critical identity fields.

These are descriptive counts only. `uncovered` does **not** mean missing authority.

## Required returned ZIP

One bounded ZIP containing:

- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `CURRENT35_QUESTION_OCCURRENCE_CANDIDATE_UNIVERSE.csv`
- `QUESTION_IDENTITY_CROSSWALK.csv`
- `AUTHORITY_CARRIER_COVERAGE_MATRIX.csv`
- `QUESTION_IDENTITY_COLLISION_LEDGER.csv`
- `COVERAGE_COUNTS_BY_FAMILY_WAVE.csv`
- `CARRIER_IDENTITY_AND_SCHEMA_RECEIPT.csv`
- `COVERAGE_MECHANICAL_RECEIPT.json`
- `payload/` containing only exact bytes of identity-defining carriers/scripts/manifests necessary to reproduce the census; reference already-returned H001–H004 large objects by exact SHA when their bytes need not be duplicated.

No raw respondent microdata.

## Forbidden

- no edit/delete/move/rename/normalization of source files;
- no producer/updater/compiler execution that writes repository/local authority files;
- no semantic adjudication;
- no choosing canonical authority from recency, path, filename, row count, `mapping_status`, or row order;
- no collapse of one-to-many rows;
- no invention of question equivalence from similar text;
- no new question UID law;
- no declaration that uncovered means missing;
- no repair of d62;
- no creation of new semantic/driver/structural authority.

This packet is the mechanical substrate for Browser's next identity/coverage adjudication.

Return token:

`AUTHORITY_CENSUS_LOCAL_HARVEST_REQUEST__HARVEST_005`
