# Codex in-place continuation brief — v39 candidate evidence staging, atomic promotion, and immutable convergence

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not download, upload, or extract another cumulative handoff.

Preserve the v39 blocker worktree and section-61 blocker delta as immutable evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v40_WORKING
```

If it does not exist, copy the v39 working tree locally with `rsync -a`. Do not reconstruct it from a ZIP.

Create section:

```text
62_P3A_V7_CANDIDATE_EVIDENCE_STAGING_AND_ATOMIC_PROMOTION
```

Preserve sections 00–61 unchanged.

## Blocker classification

The v39 stop is valid.

Status:

```text
BLOCKED_CANDIDATE_EVIDENCE_PROMOTION_CONTRACT
```

This is a bounded implementation-contract blocker, not a J-family semantic-doctrine blocker.

Verified state before the blocker:

- q33 current-stage closure is repaired:
  - 141 candidate revisions;
  - 141 status events;
  - 141 current-stage rows;
- projection and component semantic identities use identity-plus-binding surfaces;
- stable topology contract label exists;
- typed fake-evidence mutation is rejected;
- PostgreSQL is torn down cleanly;
- the only raw query failures are the two legitimate future-phase gates:
  - `q01b_postpromotion_pointer`;
  - `q15b_no_unadjudicated_at_p3_close`.

The remaining populated failure is exact:

```text
database candidate hash != complete packet evidence hash
```

for all four packeted candidates.

Do not hot-patch `p3_candidate_revision.evidence_bundle_hash`.

## Why the current insertion model cannot close

The current loader does this:

1. generates a candidate revision ID;
2. calculates a partial revision summary hash;
3. inserts immutable `p3_candidate_revision`;
4. inserts membership, components, pairs, typed constraints, obligations, flags, response references, exclusions, ranking, and status events;
5. later reconstructs a larger packet evidence surface.

The packet surface is strictly larger than the loader summary.

The revision row must exist before normalized child rows can satisfy their foreign keys, but its final immutable evidence hash must already be known.

The missing boundary is a non-authoritative evidence stage followed by one atomic canonical promotion.

## Governing correction

Implement one shared typed `CandidateEvidenceBundle` and two persistence layers:

1. **non-authoritative staging**;
2. **immutable canonical revision plus immutable evidence snapshot**.

Do not create a second kind of candidate authority.

The stage exists only to compute and validate the full evidence bundle before canonical insertion.

## CandidateEvidenceBundle

Create one typed Python model, dataclass, or equivalent structure that is the sole source for:

- staged canonical evidence;
- canonical SQL child rows;
- candidate evidence hash;
- packet export;
- database reconstruction;
- verifier reconstruction.

It must contain the complete governed candidate evidence surface.

At minimum:

```text
evidence_contract_version
identity_contract_version
topology_contract_version
candidate_family_id
candidate_revision_id
revision_number
authority_release_id
candidate_classification
candidate_origin_type
release-neutral family semantic origin
concrete release-scoped component IDs
component semantic fingerprints
candidate membership and membership bases
attachment projections and semantic fingerprints
complete proposition-signature matrix
complete signature field states and evidence IDs
response-contract references
complete pair projections
complete internal-pair matrix
collision objects and authority sources
unresolved boundaries
redirect boundaries
coordinate/hierarchy constraints
closure obligations and closure links
diagnostic flags and exact evidence IDs
family exclusions and excluded objects
candidate ranking and exact derivation inputs
exact evidence links
schema and serialization versions
```

Do not maintain one summary hash in the loader and a different packet hash in the exporter.

## Canonical evidence surface

Define one function, for example:

```python
build_candidate_evidence_bundle(...)
```

and one canonicalization function:

```python
candidate_evidence_surface(bundle)
```

The canonical candidate evidence hash is:

```python
sha256(canonical_json(candidate_evidence_surface(bundle)))
```

The following values must all be identical:

```text
staged evidence hash
p3_candidate_revision.evidence_bundle_hash
p3_candidate_evidence_snapshot.evidence_bundle_hash
offline packet evidence hash
draft decision evidence hash
database-reconstructed evidence hash
```

Packet ID remains derived from:

```text
candidate revision ID
+ evidence-bundle hash
+ packet schema version
```

Presentation-only packet fields must not create a second evidence definition.

## Non-authoritative staging surface

Create a separate staging schema or clearly non-authoritative table family, such as:

```text
p3a_build_stage.candidate_evidence_bundle
```

Recommended minimum columns:

```text
build_run_id
candidate_family_id
candidate_revision_id
authority_release_id
evidence_contract_version
canonical_payload JSONB
evidence_bundle_hash CHAR(64)
source_manifest_hash CHAR(64)
stage_status
created_at
validated_at
promoted_at
```

Allowed stage statuses:

```text
GENERATED
VALIDATED
PROMOTED
REJECTED
```

The stage must not:

- have an entry in `p3_object_registry`;
- be a candidate family or revision;
- receive candidate lifecycle events;
- appear in pilot selection;
- appear in release-change authority counts;
- be packet-addressable;
- become runtime-promotable;
- satisfy any canonical-candidate query.

Do not use an authority release status to represent stage state.

A staging row is build machinery, not P3 authority.

## Immutable canonical evidence snapshot

Add an immutable canonical table, for example:

```text
p3_candidate_evidence_snapshot
```

Minimum contract:

```text
candidate_revision_id PRIMARY KEY
evidence_contract_version
canonical_payload JSONB
evidence_bundle_hash CHAR(64)
authority_release_id
created_at
```

Required constraints:

- one and only one snapshot per canonical candidate revision;
- snapshot hash equals canonical hash of its payload;
- candidate revision hash equals snapshot hash;
- revision and snapshot release IDs agree;
- snapshot is immutable;
- no canonical candidate revision may commit without a snapshot.

The snapshot is authority evidence. The build stage is not.

## Atomic promotion algorithm

Implement a single promotion transaction per candidate revision or a deterministic batch transaction with equivalent rollback semantics.

Required sequence:

1. Read a `VALIDATED` staged `CandidateEvidenceBundle`.
2. Recompute its canonical payload and hash.
3. Confirm deterministic family/revision identity and release genealogy.
4. Acquire the required identity/allocation locks.
5. Insert required object-registry entries.
6. Insert candidate family when new.
7. Insert immutable candidate revision using the final staged hash.
8. Insert immutable evidence snapshot with the same payload and hash.
9. Insert every normalized canonical child row generated from the exact same bundle.
10. Insert genealogy, family semantic origin, status event, ranking, exclusions, and release-change records.
11. Force all deferred constraints.
12. Reconstruct the complete candidate evidence bundle from canonical PostgreSQL rows.
13. Canonicalize and compare:
    - exact canonical payload;
    - exact evidence hash;
    - exact release and identity versions.
14. If any value differs, raise and roll back the entire transaction.
15. Commit only after exact convergence.
16. Mark the non-authoritative stage `PROMOTED` only after canonical commit succeeds.

No partial canonical revision may survive a failed promotion.

## No direct hash mutation

Keep the immutable trigger on `p3_candidate_revision`.

Remove or prohibit every production path that executes:

```sql
UPDATE p3_candidate_revision
SET evidence_bundle_hash = ...
```

Do not temporarily disable the trigger.

Do not insert a placeholder or partial hash.

Do not call a later “finalize hashes” pass.

## One bundle, two renderings

The normalized SQL rows and packet JSON must be two renderings of the same `CandidateEvidenceBundle`.

Recommended structure:

```python
bundle.to_sql_rows()
bundle.to_evidence_surface()
bundle.to_packet_projection()
```

These methods must not independently rediscover or reinterpret evidence.

The packet builder should:

1. load the immutable evidence snapshot;
2. verify the normalized DB reconstruction equals the snapshot;
3. render the packet from that snapshot/bundle;
4. recompute the offline packet hash;
5. require equality with the candidate revision hash.

## Idempotency and resume behavior

Do not hide promotion defects behind `ON CONFLICT DO NOTHING`.

Required behavior:

### Stage rerun

Same build-run ID, revision ID, and exact bundle hash:

```text
IDEMPOTENT_STAGE_MATCH
```

Same IDs with different payload or hash:

```text
FAIL_STAGE_IDENTITY_DIVERGENCE
```

### Promotion rerun

Canonical revision already exists and exact:

- candidate hash;
- snapshot;
- normalized DB reconstruction;
- identity and release;

all match:

```text
IDEMPOTENT_ALREADY_PROMOTED
```

Any mismatch:

```text
FAIL_CANONICAL_IDENTITY_OR_EVIDENCE_DIVERGENCE
```

A duplicate-key exception by itself is never proof of successful idempotency.

## Required regression set

Use `V39_STAGING_PROMOTION_TEST_MATRIX.csv`.

At minimum prove:

1. missing staged child evidence rejects before canonical insertion;
2. stale staged hash rejects;
3. normalized DB/snapshot mismatch rolls back;
4. candidate revision hash update is forbidden;
5. canonical revision without one snapshot fails;
6. all four v39 blocker candidates converge:
   - DB hash;
   - snapshot hash;
   - packet hash;
   - draft hash;
7. every current candidate independently reconstructs to its immutable snapshot hash;
8. interrupted validated stage resumes and promotes exactly once;
9. same revision ID with divergent staged content fails;
10. staging rows remain absent from all authority and pilot surfaces;
11. deferred closure/origin failure leaves no partial canonical candidate;
12. the populated q01–q54 surface has no applicable failures.

Add mutation fixtures for:

- typed semantic evidence change;
- signature field evidence change;
- response-reference change;
- ranking derivation change;
- closure obligation change;
- attachment projection change;
- exact evidence-link change;
- schema/contract version change.

Each mutation must change the candidate evidence hash.

## Candidate status events

Preserve the v39 q33 repair.

The canonical `DISCOVERED` event is inserted during atomic promotion, not while the bundle is merely staged.

A staged candidate has no lifecycle stage.

## Release change ledger

The ledger entry for a candidate revision is inserted only during successful canonical promotion.

Its current content hash must be based on the governed canonical revision/snapshot contract.

A rejected or abandoned stage must not appear as an added/revised authority object.

## Resume all unfinished section-61 work

After the staging/promote blocker is repaired, continue—not package—through every remaining section-61 requirement:

- reconstruct and verify release-neutral R35/R40 family continuity;
- verify one-to-many semantic identity bindings;
- run every current candidate through the shared complete evidence builder;
- restore and execute the complete isolated authority fixture lifecycle;
- verify exact release-ledger prior/current snapshot hashes;
- recompute the evidence-backed pilot;
- execute q01–q54 against the final populated successor release;
- run the independent verifier;
- prove PostgreSQL and fixture teardown.

Do not infer that a section-61 surface passed merely because execution had not yet reached it before this blocker.

## Checkpoint rule

Do not package after ordinary staging implementation errors.

Create the next cumulative checkpoint only when:

1. all current candidate revisions are promoted atomically from validated stages;
2. no candidate hash is inserted partially or updated later;
3. all candidate snapshots independently reconstruct;
4. all pilot packets converge with PostgreSQL;
5. q01–q54 has no applicable failures;
6. the complete fixture lifecycle passes at named invariants;
7. release-neutral family continuity and the release ledger reconcile;
8. the independent verifier derives PASS;
9. PostgreSQL and fixture teardown are proven.

Build only then:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v40_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-62 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V40_CANDIDATE_EVIDENCE_STAGING_CONTRACT.json
P3A_V40_CANDIDATE_EVIDENCE_SNAPSHOT_CONTRACT.json
P3A_V40_STAGE_BUILD_RETURN.json
P3A_V40_PROMOTION_RETURN.json
P3A_V40_PROMOTION_IDEMPOTENCY_RETURN.json
P3A_V40_PROMOTION_ROLLBACK_RETURN.json
P3A_V40_ALL_CANDIDATE_SNAPSHOT_RECONCILIATION.csv
P3A_V40_DATABASE_PACKET_HASH_CONVERGENCE.csv
P3A_V40_RELEASE_CHANGE_LEDGER.csv
P3A_V40_FIXTURE_RETURN.json
P3A_V40_PILOT_STRATA_ELIGIBILITY.csv
P3A_V40_PILOT_PACKET_COVERAGE.csv
P3A_V40_QUERY_MATRIX.csv
P3A_V40_OBJECT_COUNTS.json
P3A_V40_EXECUTION_FINDINGS.csv
P3A_V40_DOCTRINE_DELTAS.csv
code/
sql/
schemas/
outputs/
postgres/
candidate_packets/
draft_decisions/
test_only_fixtures/
validation/
```
