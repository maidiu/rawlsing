# CONTROL ROOM — EXACT DUPLICATE DELETION LAW

Status: `BINDING__DELETE_ONLY_AFTER_CONTENT_IDENTITY_AND_PATH_SAFETY_PROOF`

## 1. Governing distinction

`SAME SHA-256` proves exact byte identity.

It does NOT by itself prove that one path may be removed.

Rawlsing historically uses self-contained handoff bundles, installer/reproduction packets, extracted verification trees, active working trees, canonical runtime locations, and provenance-preserving historical packages. Some of those deliberately repeat identical bytes.

Therefore the deletion unit is not merely a duplicate SHA group. It is:

`duplicate SHA group + path-role classification + canonical-survivor decision`.

## 2. Allowed deletion classes

A redundant exact copy may be deleted when all of the following hold:

- another byte-identical survivor has been rehashed immediately before deletion;
- the survivor's absolute path is recorded;
- the candidate path is not Git-tracked in an active required working tree;
- no accepted code/configuration/manifest requires the candidate path specifically;
- the candidate is not required to preserve a self-contained package/release contract;
- deleting the copy does not invalidate a package checksum/manifest that remains represented as intact;
- the copy is not the sole witness of a historical directory/package topology still required for provenance;
- a deletion tombstone is committed/recorded before physical removal;
- the survivor remains readable and hash-identical after deletion.

## 3. Automatic no-delete classes

Without separate positive authority, DO NOT delete:

- files under `.git`;
- files in active Git worktrees solely because another worktree contains the same blob;
- currently canonical runtime/configuration paths;
- immutable raw survey source bytes where source path remains part of a governed execution order;
- files inside a still-authoritative self-contained handoff/package tree;
- files named by an accepted SHA256SUMS/package manifest unless that entire package is itself retired;
- the only retained copy of any manually/adjudicatively created authority;
- files whose supersession is unresolved by G1A / the preservation desk;
- files whose apparent duplicate relationship crosses different semantic products despite equal bytes unless that equivalence is explicitly recorded.

## 4. Preferred deletion order

Within a proven-safe SHA group, prefer deleting in this order:

1. extracted verification copies that can be recreated from a retained immutable archive;
2. obsolete scratch/build copies;
3. redundant handoff copies whose package has been formally retired and whose topology is preserved by tombstone/manifest;
4. RawlsingsExcess duplicate copies after a canonical Rawlsing survivor is proven;
5. duplicate loose authority inputs after one canonical governed authority location is established.

Do not use modification date alone to choose the survivor.

## 5. Canonical survivor preference

When semantic status is otherwise equal, prefer:

1. current accepted canonical authority path;
2. exact source-of-record manually authored packet;
3. immutable accepted release/archive;
4. complete historical package over an orphan loose copy;
5. Rawlsing over RawlsingsExcess only when governance and path-consumer checks confirm equivalence.

## 6. Self-contained package rule

If two complete packages contain the same internal artifact, the internal copy is NOT individually deletable while the package remains designated self-contained.

Instead choose one of:

- retain the package intact;
- retire/delete the entire redundant package if another exact package copy survives;
- explicitly reclassify the package as non-self-contained before internal deduplication.

Never silently hollow out a package and continue calling it intact.

## 7. Exact duplicate archive rule

If entire archive files are byte-identical, the archive object itself is eligible for canonical-survivor deduplication subject to path checks.

This is high-value because it preserves every internal path/manifest while removing redundant storage.

## 8. Raw source duplicate rule

Exact duplicate raw source binaries may be consolidated only if:

- exact source SHA remains the governing source identity;
- every consumer is migrated to the canonical path or is path-neutral;
- no accepted local execution order still requires the old path;
- source transport/provenance remains recorded.

No source binary is deleted merely because a CSV, SAV, DTA, ZIP, or extracted copy appears semantically equivalent. Only exact-byte duplicates qualify under this law.

## 9. Required before/after receipts

Before a deletion batch:

- root tree hashes / source manifest identity;
- candidate SHA group ledger;
- canonical survivor ledger;
- path-consumer audit;
- package-integrity audit;
- projected reclaimed bytes.

After a deletion batch:

- deleted path tombstones;
- survivor rehashes;
- remaining copy counts;
- Git cleanliness for governed trees;
- selected replay/integrity probes;
- new root tree hashes;
- actual reclaimed bytes.

## 10. Fail closed

If the worker cannot prove whether a path is required:

`DEFER__PATH_REQUIREMENT_UNRESOLVED`

If it cannot prove which copy is canonical:

`DEFER__CANONICAL_SURVIVOR_UNRESOLVED`

If an authority object exists only in repeated historical packages and supersession is unresolved:

`DEFER__AUTHORITY_PRESERVATION_UNRESOLVED`

The goal is aggressive deduplication after proof, not timid indefinite accumulation and not reckless filesystem thinning.

`EXACT_DUPLICATE_DELETION_LAW_SEALED`
