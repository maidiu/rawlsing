# HARVEST-005L — LOCAL QUESTION-IDENTITY CARRIER DELTA DISCOVERY

Status: `ISSUED__LOCAL_DELTA_ONLY__NO_CROSS_CARRIER_COMPUTATION`

## Mission

Search the live local filesystem for H005-responsive question-identity evidence that Browser HQ does **not already possess as exact bytes/content**.

This is a bounded retrieval/delta harvest.

It is **not** the current-35 identity/coverage census itself. Browser HQ owns that computation under `HARVEST-005B_BROWSER_IDENTITY_COVERAGE_COURT.md`.

## Governing Browser exclusion inventory

Before collecting payload bytes, read:

`H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`

and:

`H005_BROWSER_LOCAL_SPLIT_CONTRACT.md`

The governing rule is:

`H005_REQUIRED_EVIDENCE - BROWSER_AVAILABLE_EXACT_EVIDENCE = H005L_LOCAL_DELTA_SCOPE`

If a responsive local file's SHA/content identity is already represented in the Browser inventory, do **not** package duplicate bytes. Record the local physical occurrence in the manifest/census if provenance matters.

If a responsive local file has a distinct SHA/content identity not represented in the Browser inventory, return the bounded exact bytes.

Do not infer canonicality from recency, path, filename, mtime, size or row count.

## Search roots

- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

## Browser already has

Do not rebuild or repackage identical copies of the H001-H004 evidence universe.

Browser has exact bytes of all four returned ZIPs and every member, including the known structure registers, semantic masters, driver masters, scope/identity registries/manifests, historical/current identity code, H004 producer lineage and review/provenance evidence listed in `H005_BROWSER_AVAILABLE_EVIDENCE_INVENTORY.csv`.

Browser also has connected GitHub access to the current/preserved governed SWID, source-census, FQRA/QSM/QRA/response/manual/negative authority surfaces listed there.

## High-priority local delta targets

Search especially for the classes currently marked `BAV-GAP-*`:

1. every distinct `questions_master.csv` identity;
2. current final-codebook/question-index identity surfaces that enumerate source/wave/question/variable occurrences;
3. local-only **distinct** FQRA/QSM/QSMv2 identity-bearing variants not represented by Browser's Git content;
4. source-native codebook variable/question identity indexes or manifests needed to bind normalized question rows to source occurrences;
5. any other exact identity-defining carrier clearly required to answer what source/wave/question occurrence a normalized row represents.

Do not return raw respondent microdata.

Do not broadly dump codebooks/PDFs merely because they exist. Return documentary/source files only if an exact identity surface depends on them and Browser does not already possess the relevant bounded evidence.

## Required local work

### A. Responsive content census

For every H005-responsive local occurrence, record:

- absolute path;
- SHA-256;
- size;
- mtime;
- basename/artifact class;
- relevant identity columns/fields if cheaply inspectable without executing producers;
- Browser inventory match state:
  - `EXACT_BROWSER_HELD_SHA`
  - `DISTINCT_SHA_RETURN_BYTES`
  - `GIT_CURRENT_EQUIVALENT_OR_CANDIDATE`
  - `LOCAL_ONLY_IDENTITY_SURFACE`
  - `AMBIGUOUS_REQUIRES_BROWSER`.

### B. Exact-byte delta

Package only:

- distinct responsive SHAs Browser does not already possess;
- local-only identity surfaces;
- minimal supporting schema/config/provenance bytes necessary to understand those new surfaces.

For an exact Browser-held SHA, manifest the occurrence but do not duplicate the bytes.

### C. Schema receipt only

For each distinct returned identity carrier, mechanically report:

- header/field names;
- row count where tabular;
- presence/absence of `source`, `wave`, `var_name`, `item_id`, question ID, question text, source/codebook ID or equivalent fields;
- duplicate counts only for single-carrier identity fields if trivial to calculate.

Do not join carriers to one another.

## Explicitly forbidden computation

The local worker must **not** produce:

- a global current-35 candidate question universe;
- a cross-carrier question identity crosswalk;
- carrier coverage matrices;
- per-wave cross-carrier coverage counts;
- global collision adjudication;
- candidate-by-carrier nested scans;
- a canonical question UID or proposed UID law.

Those are Browser H005B responsibilities.

## Required returned ZIP

One small bounded ZIP containing:

- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `LOCAL_DELTA_CARRIER_CENSUS.csv`
- `BROWSER_INVENTORY_MATCH_RECEIPT.csv`
- `UNSEEN_DISTINCT_CONTENT.csv`
- `LOCAL_ONLY_IDENTITY_SURFACES.csv`
- `CARRIER_SCHEMA_RECEIPT.csv`
- `payload/` containing only unseen/distinct H005-responsive exact bytes.

If the exhaustive search finds no unseen responsive bytes, return an evidence ZIP with empty payload plus the search/match receipts. An empty content delta is a valid positive result.

## Forbidden modifications

- no edit/delete/move/rename/normalization of any source or authority file;
- no governed producer/updater/compiler execution;
- no semantic adjudication;
- no deduplication;
- no question-equivalence inference from similar text;
- no authority choice by row order/path/recency;
- no `uncovered => missing authority` inference;
- no repair of d62;
- no new semantic/driver/structural authority.

## Return token

`AUTHORITY_CENSUS_LOCAL_HARVEST_REQUEST__HARVEST_005L`

## Stop condition

Once the local complement and receipts are packaged and verified, stop. Do not continue into H005B computation.
