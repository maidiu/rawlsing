# CONTROL ROOM — AUTHORITY CENSUS PRIORITY & BROWSER/LOCAL COLLABORATION PROTOCOL

Status: `BINDING_PRIORITY_RESET__AUTHORITY_CENSUS_FIRST__BROWSER_ADJUDICATES__LOCAL_HARVESTS`

This authority resets the immediate mission of the Control Room Authority Preservation & Dedup Desk.

The present priority is NOT deletion, cleanup, storage reduction, or package consolidation.

The present priority is:

> **Map every authority-bearing object that exists or is claimed to have existed, prove what epistemic work it contains, prove how it relates to later authority, and identify only after that mapping what authority is genuinely absent and still must be created.**

`KNOW_WHAT_EXISTS_BEFORE_DECIDING_WHAT_TO_BUILD`

`AUTHORITY_CENSUS_BEFORE_HYGIENE`

## 1. Two-agent operating model

The authority census SHALL use a browser/local collaboration model.

### A. Browser agent — epistemic adjudicator

The browser agent owns the reasoning-heavy work.

It SHALL:

- ground in GitHub Dva/Trii/Chetiri authority and accepted runtime contracts;
- read accepted handoffs, manifests, provenance, QRA/QSM/FQRA/V550/V551/V552 authority lineage;
- inspect Library/browser-available documentary authority;
- define expected authority classes and exact questions to be answered;
- determine which local artifacts must be recovered or compared;
- adjudicate whether an artifact is authoritative, review-only, candidate, superseded, partially absorbed, unresolved, or irrelevant;
- adjudicate whether two non-identical artifacts are semantic successors, divergent branches, or independent authority surfaces;
- determine whether apparent gaps are genuine missing authority or merely missing physical access to existing authority;
- determine what human/manual authority must still be created only after positive absence is established;
- maintain the canonical authority inventory and provenance/supersession DAG.

The browser agent MUST NOT declare a local artifact absent merely because GitHub does not contain it.

The browser agent MUST NOT infer manual authority from later products merely because the later product appears compatible.

### B. Local Codex agent — evidence harvester

The local agent owns filesystem search, byte identity, and evidence packaging.

It SHALL:

- search `/Users/matthewsmith/Desktop/Rawlsing` and `/Users/matthewsmith/Desktop/RawlsingsExcess` plus specifically authorized adjacent Rawlsing recovery paths;
- locate exact requested filenames, variants, archives, packet directories, manifests, review ledgers, overlays, registries, historical copies and recovery bundles;
- compute SHA-256, byte size, mtime, row count/schema where safe and requested;
- identify exact duplicate physical copies by SHA without deleting them;
- preserve original bytes and paths;
- package browser-requested evidence into narrowly scoped ZIPs;
- include a deterministic package manifest containing original absolute path, SHA-256, byte size, mtime, reason collected, and archive-relative path;
- include directory listings and SHA256SUMS for every returned ZIP;
- return named evidence gaps when requested material cannot be found.

The local agent SHALL NOT:

- decide which authority is semantically canonical;
- decide that a later artifact supersedes an earlier artifact;
- regenerate missing manual semantic authority;
- infer authority from filenames, labels, recency, apparent similarity, or downstream compatibility;
- delete, move, normalize, or rewrite source artifacts during the census;
- collapse multiple divergent versions into one;
- silently omit inconvenient or contradictory candidates.

`LOCAL_AGENT = EVIDENCE_HARVESTER__NOT_EPISTEMIC_COURT`

## 2. Iterative court loop

The census proceeds in repeated bounded loops:

1. **Browser frames a named authority question.**
2. Browser searches GitHub/Library and identifies known references and unknown physical evidence.
3. Browser issues a narrow local evidence request.
4. Local Codex searches the hard drive and produces an immutable evidence ZIP + manifest.
5. The ZIP is supplied to the browser court.
6. Browser adjudicates status, quality, scope, provenance, supersession, and remaining gaps.
7. Browser updates the canonical authority map.
8. Only unresolved evidence questions generate another local harvest request.

No large undifferentiated "zip the whole project" packet is preferred when a bounded packet can answer the question.

## 3. Mandatory local evidence packet contract

Every returned ZIP SHALL contain at minimum:

- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `payload/...`

`EVIDENCE_MANIFEST.csv` columns SHALL include:

- `archive_relative_path`
- `original_absolute_path`
- `sha256`
- `size_bytes`
- `mtime_local`
- `artifact_name`
- `browser_request_id`
- `collection_reason`
- `exact_duplicate_group_if_known`

`SEARCH_RECEIPT.md` SHALL record:

- exact roots searched;
- exact search terms/patterns;
- omitted roots, if any;
- files found;
- files not found;
- errors/permission barriers;
- whether archives were inspected or merely collected;
- whether any payload was transformed (default MUST be no).

## 4. Canonical authority map

The active census SHALL build these primary products before destructive hygiene begins:

### `AUTHORITY_OBJECT_CENSUS.csv`

One row per distinct authority-bearing content object, not per physical copy.

Required fields include:

- `authority_object_id`
- `sha256_or_content_identity`
- `artifact_name`
- `authority_family`
- `survey_family_or_global_scope`
- `wave_scope`
- `semantic_scope`
- `epistemic_class`
- `manual_adjudication_present`
- `current_status`
- `canonicality_status`
- `accepted_authority_ref`
- `downstream_consumers`
- `supersession_status`
- `quality_status`
- `open_questions`

### `AUTHORITY_PHYSICAL_LOCATION_MAP.csv`

One row per physical copy/path.

Required fields include:

- `authority_object_id`
- `absolute_or_repo_path`
- `sha256`
- `size_bytes`
- `mtime`
- `container_or_archive`
- `git_library_local_excess_class`
- `physical_access_status`

### `AUTHORITY_PROVENANCE_AND_SUPERSESSION_DAG.csv`

Edges SHALL distinguish at minimum:

- `DERIVED_FROM`
- `MANUALLY_ADJUDICATED_FROM`
- `LOSSLESSLY_ABSORBS`
- `PARTIALLY_ABSORBS`
- `SUPERSEDES_BY_AUTHORITY`
- `PARALLEL_DIVERGENT_VERSION`
- `EXACT_BYTE_DUPLICATE_OF`
- `PACKAGES`
- `REFERENCES`
- `REVIEW_INPUT_TO`

### `AUTHORITY_GAP_LEDGER.csv`

A gap may be entered as `GENUINELY_MISSING_AUTHORITY` only after the census records:

- the exact expected authority class;
- why downstream law requires it;
- all GitHub/Library searches performed;
- all local evidence requests performed;
- all plausible predecessor/successor artifacts examined;
- why no located object closes the requirement.

Other allowed gap states include:

- `EXISTS__NOT_YET_ADJUDICATED`
- `EXISTS__PHYSICAL_PAYLOAD_RECOVERY_REQUIRED`
- `EXISTS__SUPERSESSION_NOT_PROVED`
- `EXISTS__QUALITY_INSUFFICIENT`
- `EXISTS__REVIEW_ONLY_NOT_EXECUTION_AUTHORITY`
- `EXISTS__PARTIAL_SCOPE_ONLY`
- `DOCUMENTARY_AUTHORITY_REQUIRED`
- `GENUINELY_MISSING_AUTHORITY`

## 5. Priority authority families

The census begins with the authority families most likely to contain irreducible human judgment:

1. question structure registers and manual-review rows;
2. respondent-wave source/semantics registries;
3. source/family semantic authority overlays;
4. response-option authority;
5. directionality/signability authority;
6. position-conditioning and applicability authority;
7. routing/topology/manual source exceptions;
8. `questions_master_semantic.csv` / `questions_master_drivers.csv` and driver/facet deepening reviews;
9. QRA accepted manual calibration surfaces;
10. QSMv2 semantic-unit/block/structural-coordinate adjudication;
11. Full Question Relation Authority R1 and its manual/QSM provenance;
12. V550/V551/V552J governing inputs and manual overrides;
13. structural mapping/target/axis/domain registries;
14. negative/blocked/review-required authority;
15. family-specific manual authority packets and hygiene-correction packets;
16. historical recovery bundles that may contain predecessor authority not proved absorbed.

## 6. Relationship to G1A

G1A-R1/R2/R3 are first consumers of this collaboration protocol.

Their findings SHALL feed the same authority census rather than remain isolated one-off receipts.

In particular:

- G1A-R1 local question-structure recovery is a local evidence-harvest cell;
- G1A-R2 itinerary reclosure is browser adjudication;
- G1A-R3 manual-authority supersession closure is browser-led and may issue iterative local evidence requests.

## 7. Hygiene and dedup are preserved but deferred

The existing exact-dedup plan remains valid future maintenance work.

No destructive dedup campaign SHALL begin until HQ has at minimum:

- a materially complete authority-object census;
- a physical-location map;
- a provenance/supersession DAG sufficient to distinguish canonical authority from historical witness;
- a gap ledger distinguishing truly missing authority from merely undiscovered authority.

The previously created branch:

`agent/vozhd-controlroom-local-exact-dedup-r1`

is therefore PARKED and SHALL NOT delete files under the present priority.

## 8. Completion question

The authority census is not complete until HQ can answer, for every authority family relevant to PRE553 and the generated-person chain:

> **What authority exists? Where are its exact bytes? Who/what created its semantic content? What does it govern? What supersedes it, if anything? Is the successor lossless? Is it execution authority or only review evidence? And what required semantic decision, if any, genuinely has no existing authority object?**

Only after those questions are answered may Rawlsing safely decide what new manual authority must be made.

`AUTHORITY_CENSUS_FIRST__BROWSER_REASONING_PRIMARY__LOCAL_EVIDENCE_HARVEST_SUPPORT__HYGIENE_DEFERRED`
