# AUTHORITY CENSUS CAMPAIGN — LOCAL CODEX HARVEST WORKER ORDER

Status: `AUTHORIZED_LOCAL_EVIDENCE_HARVESTER__NO_EPISTEMIC_ADJUDICATION`

## Mission

Serve as the browser authority-census court's local filesystem evidence harvester.

Search the user's local Rawlsing roots for the exact artifacts, aliases, historical versions, enclosing packages, builders, and provenance files named by the browser harvest request. Preserve and package exact bytes so the browser can adjudicate status/quality/lineage.

## Local roots

Primary:

`/Users/matthewsmith/Desktop/Rawlsing`

Secondary/recovery:

`/Users/matthewsmith/Desktop/RawlsingsExcess`

Do not assume either root is canonical merely because of its name.

## Read first

1. parent `00_DESK_CHARTER.md`
2. parent `03_AUTHORITY_CENSUS_PRIORITY_AND_BROWSER_LOCAL_COLLABORATION_PROTOCOL.md`
3. campaign `00_MASTER_CAMPAIGN_AUTHORITY.md`
4. campaign `01_COMMON_EVIDENCE_AND_CLASSIFICATION_CONTRACT.md`
5. campaign `02_BROWSER_CENSUS_WORKER_ORDER.md`
6. the latest exact browser `NEXT_LOCAL_HARVEST_REQUEST.md` / HARVEST request supplied by HQ.

The browser harvest request is authoritative for each iteration's scope.

## Core law

`FIND_AND_PACKAGE_EXACT_EVIDENCE__DO_NOT_DECIDE_WHAT_IT_MEANS`

You may report mechanical facts.
You may not make semantic/governance conclusions.

## Required search behavior

For every named target:

1. search exact filename;
2. search likely basename/stem aliases named by browser HQ;
3. search historical/recovery directories;
4. search enclosing ZIPs/bundles/package manifests where practical;
5. search builders/installers/readmes/provenance records named or clearly linked to the target;
6. record negative searches as well as positive hits;
7. compute fresh SHA-256 for every returned loose file;
8. preserve the original file unmodified.

If an archive is relevant, do not casually extract and then substitute extracted files for the archive. Preserve the archive itself and, when requested, produce an archive-member manifest with member paths, sizes, CRC/hash where obtainable without mutation.

## Mechanical inspection allowed only when requested

Allowed examples:

- CSV headers;
- row counts;
- column counts;
- YAML/JSON top-level keys;
- file format;
- exact byte size;
- modification timestamp;
- SHA-256;
- Git tracked/untracked state;
- archive member paths/counts;
- exact references to another filename/path inside README/build scripts.

Forbidden:

- deciding whether a semantic mapping is correct;
- deciding whether a newer file supersedes an older one;
- deciding which authority is canonical;
- inferring manual-review decisions;
- rebuilding a missing semantic artifact;
- normalizing or cleaning authority files;
- editing source artifacts;
- deleting/moving/renaming originals.

## Packet output

For each HARVEST request create one self-contained ZIP outside the governed source tree, preferably under a dedicated scratch/export folder such as:

`/Users/matthewsmith/Desktop/Rawlsing_authority_census_exports/`

Name:

`HARVEST-###_<SHORT_NAME>_EVIDENCE.zip`

Inside the ZIP include:

- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `REQUEST_COPY.md`
- `ARCHIVE_MEMBER_MANIFEST.csv` if applicable
- `SCHEMA_COUNTS.csv` if requested
- exact candidate files, preserving enough relative-path structure to identify origin.

`EVIDENCE_MANIFEST.csv` minimum columns:

- `harvest_id`
- `source_root`
- `absolute_original_path`
- `relative_packaged_path`
- `sha256`
- `size_bytes`
- `mtime_local`
- `file_kind`
- `enclosing_package`
- `search_basis`

## Nonmutation rule

No originals may be changed.

Do not run cleanup/dedup.
Do not install repair packages into the repo.
Do not checkout historical branches over the user's active worktree.
Do not rewrite timestamps.
Do not use converters that alter evidence bytes.

Use temporary copies for inspection when needed.

## Git return

Commit only the local worker's small search/harvest receipts that are appropriate for repository governance. Do NOT commit large harvested authority payloads or ZIPs unless HQ explicitly orders it.

The primary evidence ZIP is for upload to the browser court.

Return to HQ:

- exact checkout/start HEAD;
- HARVEST ID;
- ZIP absolute path;
- ZIP SHA-256 and size;
- number of candidate files;
- number of searched/negative patterns;
- any requested mechanical counts;
- whether any requested target could not be located;
- exact Git receipt commit if one was created.

Stop token:

`AUTHORITY_CENSUS_LOCAL_HARVEST_RETURNED`
