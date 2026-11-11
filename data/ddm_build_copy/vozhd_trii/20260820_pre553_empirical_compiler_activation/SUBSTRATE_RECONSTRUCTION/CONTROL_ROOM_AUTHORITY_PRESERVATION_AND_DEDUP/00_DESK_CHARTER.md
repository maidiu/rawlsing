# CONTROL ROOM — AUTHORITY PRESERVATION & EXACT-DEDUP DESK

Status: `BINDING_CONTROL_ROOM_SUBSECTION__CROSS_DVA_TRII_CHETIRI`

Purpose:

Rawlsing contains substantial manually/adjudicatively created semantic and structural authority distributed across live manifests, reports, authority packets, historical handoffs, recovery bundles, RawlsingsExcess, and repeated exact byte copies.

This desk exists to make that material governable without either losing human-created semantic capital or retaining unlimited redundant storage.

## 1. Jurisdiction

The desk owns four cross-campaign concerns:

1. **Authority preservation** — identify every live manually/adjudicatively created semantic/structural authority required by current Rawlsing.
2. **Provenance and supersession** — prove which historical artifacts remain live, which have been losslessly absorbed, and which are merely archival witnesses.
3. **Canonical physical placement** — name one canonical retained physical copy for each exact content identity where path multiplicity is not semantically required.
4. **Exact-copy deduplication** — delete redundant physical copies only after exact SHA-256 identity and path nonrequirement are proved.

This desk does NOT infer semantic authority from filenames, labels, question text, correlations, later artifacts, or apparent similarity.

`MACHINE_READABLE_AUTHORITY != MACHINE_DERIVABLE_AUTHORITY`

`EXACT_BYTE_DUPLICATE != AUTOMATICALLY_SAFE_TO_DELETE`

## 2. Input classes

The desk treats at minimum the following as distinct:

- current Git-governed authority;
- local canonical runtime/configuration inputs;
- manually authored authority packets;
- source-semantic overlays and response-option authority;
- directionality / applicability / position-conditioning authority;
- question-structure and respondent-wave registries;
- driver/facet/structural mapping review artifacts;
- Full Question Relation / QSM / QRA outputs;
- historical handoff bundles and recovery packages;
- exact duplicate loose files;
- exact duplicate archives;
- RawlsingsExcess historical/recovery material;
- caches/build products/regenerable machine state.

## 3. Required canonical registers

The desk SHALL maintain or produce:

- `CANONICAL_AUTHORITY_OBJECT_REGISTRY.csv`
- `AUTHORITY_PROVENANCE_AND_SUPERSESSION_DAG.csv`
- `PHYSICAL_COPY_REGISTRY.csv`
- `EXACT_DUPLICATE_SHA_GROUPS.csv`
- `CANONICAL_SURVIVOR_SELECTION.csv`
- `PATH_REQUIREMENT_AUDIT.csv`
- `SAFE_DELETE_PLAN.csv`
- `DO_NOT_DELETE_OR_DEFER.csv`
- `DELETION_TOMBSTONES.csv`
- `POST_DEDUP_REPLAY_AND_INTEGRITY_RECEIPT.json`

A deletion tombstone must preserve at least:

- deleted absolute path;
- SHA-256;
- byte size;
- canonical survivor path;
- semantic/packaging role of deleted path;
- proof that path identity is not required;
- deletion timestamp;
- worker/authority ref.

## 4. Canonicality hierarchy

Canonicality is semantic/governance authority, not merely recency.

A newer file is not automatically canonical.
A larger file is not automatically canonical.
A file inside `data/ddm_build_copy` is not automatically canonical.
A file in RawlsingsExcess is not automatically obsolete.
An exact duplicate may still be required because a self-contained release/package contract requires that path.

## 5. Relationship to G1A

G1A manual-authority preservation work is an immediate consumer and feeder of this desk.

The desk SHALL absorb the G1A preservation inventory and supersession findings once accepted.

G1A blockers SHALL NOT be resolved by regenerating approximate semantic artifacts where exact historical payload survives.

## 6. Relationship to Trii source certification

Trii source certification may consume exact authority objects named by this desk.

Deduplication must never weaken source-certification replay, provenance, authority closure, or exact source identity.

## 7. Relationship to Chetiri physical architecture

Candidate A/B/C physical comparisons SHALL treat this desk's canonical authority objects as common required semantic inputs.

Storage reduction from deleting redundant historical copies must not be misreported as an architectural storage advantage of a candidate.

## 8. Safety invariant

For every deletion:

`EXACT SHA MATCH`
+
`NAMED CANONICAL SURVIVOR`
+
`SURVIVOR REHASHED`
+
`PATH NONREQUIREMENT PROVED`
+
`NOT GIT-TRACKED OR ACTIVE-WORKTREE REQUIRED`
+
`NOT REQUIRED FOR SELF-CONTAINED PACKAGE INTEGRITY`
+
`TOMBSTONE WRITTEN BEFORE DELETE`
+
`POST-DELETE SURVIVOR REHASH / REQUIRED-PATH CHECK`

Anything less is `DO_NOT_DELETE_YET`.

## 9. Command identity

This desk is preservation infrastructure, not a new redesign campaign.

Its purpose is to reduce accidental semantic loss and redundant storage while making the accumulated human wisdom of Rawlsing explicit, canonical, replayable, and inspectable.

`CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_EXACT_DEDUP_DESK_ESTABLISHED`
