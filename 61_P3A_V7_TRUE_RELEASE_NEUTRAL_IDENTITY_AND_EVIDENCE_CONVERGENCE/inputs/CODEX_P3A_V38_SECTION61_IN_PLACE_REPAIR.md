# Codex in-place continuation brief — v38 true release-neutral identity, immutable evidence convergence, and restored lifecycle verification

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not download, upload, or extract another cumulative handoff.

Preserve section 60 and the v38 review delta as immutable blocked evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v39_WORKING
```

If the v39 tree does not exist, copy the v38 working tree locally with `rsync -a`. Do not reconstruct it from a ZIP.

Create section:

```text
61_P3A_V7_TRUE_RELEASE_NEUTRAL_IDENTITY_AND_EVIDENCE_CONVERGENCE
```

Preserve sections 00–60 unchanged.

## Status correction

V38 does not earn PASS.

The operative status is:

```text
BLOCKED_RELEASE_NEUTRAL_IDENTITY_AND_EVIDENCE_CONVERGENCE_DEFECT
```

The two future-phase query failures remain legitimate:

- `q01b_postpromotion_pointer`;
- `q15b_no_unadjudicated_at_p3_close`.

However, V38 also has an applicable failure:

```text
q33_candidate_revision_has_current_stage = FAIL
```

That failure alone prohibits PASS.

## Mandatory review evidence

Use the supplied files as regressions only:

- `V38_APPLICABLE_QUERY_FAILURES.csv`
- `V38_DATABASE_PACKET_HASH_DIVERGENCE.csv`
- `V38_RELEASE_NEUTRAL_ORIGIN_IMPLEMENTATION_PROBE.csv`
- `V38_FAMILY_CONTINUITY_COMPARISON_AUDIT.csv`
- `V38_TYPED_EVIDENCE_HASH_MUTATION_PROBE.json`
- `V38_FIXTURE_COVERAGE_AUDIT.json`
- `V38_RELEASE_LEDGER_PRIOR_HASH_AUDIT.csv`
- `V38_EXTERNAL_REVIEW_FINDINGS.json`

Production builders may not read these files to decide what objects to create.

## Defect 1 — the release-neutral family origin is still release-scoped

V38 claims that family origin is:

```text
origin lane
+ sorted subjects
+ component semantic fingerprints
+ attachment projection semantic fingerprints
```

The actual candidate loader computes `origin_key` before those semantic fingerprints exist.

For each component it hashes:

```text
component type
+ members
+ concrete connectivity projection IDs
```

Those projection IDs are release-scoped.

The later `p3_candidate_family_semantic_origin` insert stores the already computed, release-scoped `origin_key`. It does not recompute the key from `p3_candidate_component_semantic_fingerprint` and `p3_pair_projection_semantic_fingerprint`.

The supplied four-packet probe proves:

- stored key matches the shipped release-scoped loader formula: 4/4;
- stored key matches the declared semantic-fingerprint formula: 0/4.

### Required correction

Construct semantic identity before canonical family/revision insertion.

Required order:

1. generate concrete release-scoped projections;
2. generate release-neutral projection semantic identities;
3. generate concrete components;
4. generate release-neutral component semantic identities;
5. construct release-neutral family semantic origin;
6. compare against reconstructed prior semantic origin;
7. allocate/preserve family identity;
8. build complete revision evidence;
9. insert the immutable revision.

The `candidate_revision.origin_key`, family-origin ledger, family semantic-origin row, genealogy, packet, and verifier must use the same canonical semantic origin key.

Add a database assertion that recomputes the semantic origin key from its stored payload and rejects a mismatch.

## Defect 2 — semantic identity requires one-to-many bindings

Current DDL makes these globally unique:

```text
p3_pair_projection_semantic_fingerprint.semantic_fingerprint
p3_candidate_component_semantic_fingerprint.semantic_fingerprint
```

But release-neutral identity exists specifically so multiple release-scoped concrete projections/components can share one semantic identity across releases.

The present uniqueness design makes genuine append-only coexistence impossible once historical concrete objects are imported.

### Required bounded redesign

Use an identity-plus-binding shape.

For projections:

```text
p3_pair_projection_semantic_identity
  semantic_fingerprint PRIMARY KEY
  release-neutral canonical payload

p3_pair_projection_semantic_binding
  projection_id PRIMARY KEY
  semantic_fingerprint FOREIGN KEY
  authority_release_id
```

For components:

```text
p3_candidate_component_semantic_identity
  semantic_fingerprint PRIMARY KEY
  release-neutral canonical payload

p3_candidate_component_semantic_binding
  component_id PRIMARY KEY
  semantic_fingerprint FOREIGN KEY
  authority_release_id
```

Multiple concrete release-scoped objects may bind to one semantic fingerprint.

The semantic identity payload must be immutable and independently hash-verified.

## Defect 3 — build-rule identity remains release-specific

Strict component semantic fingerprints currently include:

```text
P3A_COMPONENT_BUILD_V38
```

Seed components use:

```text
P3A_V38_RULE_DERIVED_TOPOLOGY
```

A release-specific label inside the semantic fingerprint recreates release churn in the next release.

Use a stable governed topology contract identifier, for example:

```text
P3_COMPONENT_TOPOLOGY_CONTRACT_V1
```

Change the semantic identity only when the topology contract actually changes, not when the package version changes.

Add a regression proving:

- R38 → R39 release-only change leaves semantic component identity unchanged;
- changing the governed topology contract version changes it.

## Defect 4 — R35 family continuity is not actually compared

`P3A_V38_FAMILY_SEMANTIC_ORIGIN_COMPARISON.csv` contains:

- 141 R38 semantic-origin keys;
- 141 old R35 release-scoped origin keys;
- 141 key mismatches;
- 141 PASS statuses.

The report marks PASS solely because the candidate ID falls between 142 and 282.

Old release-scoped origin keys and corrected release-neutral semantic keys are not directly comparable.

### Required correction

Reconstruct the corrected release-neutral R35 semantic origin from immutable prior evidence:

- exact R35 member set;
- exact semantic pair facts/endpoints;
- exact origin lane;
- exact topology contract;
- release-neutral projection fingerprints;
- release-neutral component fingerprints.

For every family deliver:

```text
R35 old release-scoped origin key
R35 reconstructed release-neutral semantic key
R38 release-neutral semantic key
exact equality result
source artifacts and hashes
migration branch
```

Only exact equality permits appending `R0002` to the same family.

A changed semantic origin requires a new family and `R0001`.

Do not infer continuity from numeric ID range.

## Defect 5 — PostgreSQL and packet evidence hashes disagree

All four exported V38 packets disagree with the immutable database revision hash.

The direct cause already visible in delivered code is:

- loader: `diagnostic_signature_count = len(incomplete_signature_ids)`;
- packet builder: `diagnostic_signature_count = 1 if blocker flag exists`.

The supplied regression contains all four mismatches.

### Required correction

Create one shared canonical evidence module imported by:

- candidate staging/insertion;
- packet export;
- report generation;
- verifier.

No duplicate implementations of the candidate evidence surface are permitted.

The candidate revision may be inserted only after the final shared hash is known.

Every exported packet must equal the database revision hash exactly.

Add a global query:

```text
all packet evidence hashes = corresponding immutable candidate revision hashes
```

## Defect 6 — the candidate evidence hash is still only a summary hash

Even if the loader and packet builder used the same summary, the summary omits governing semantic content, including typed constraint evidence.

The supplied mutation:

- replaces a typed coordinate constraint's governing evidence ID with a fake value;
- leaves packet ID and every evidence hash unchanged;
- passes the shipped V38 schema and semantic validator.

### Required complete evidence surface

The canonical candidate evidence hash must include exact canonical content for:

- family and revision identity;
- release-neutral semantic origin;
- concrete release-scoped components and projections;
- membership;
- complete internal-pair matrix;
- pair facts and source authority;
- collision objects and sources;
- unresolved, redirect, coordinate, and hierarchy objects;
- closure obligations and links;
- exact signature IDs, statuses, field states, and evidence IDs;
- response references;
- exclusions;
- diagnostic flags and their evidence IDs;
- ranking values and derivation evidence;
- exact evidence links;
- schema, serialization, identity-contract, and topology-contract versions.

Changing any semantic field must change the evidence hash.

A typed evidence ID that does not resolve to the governing authority surface must fail validation.

## Defect 7 — candidate status events are erased

The loader appends one `DISCOVERED` event per candidate and then executes:

```python
event_rows = []
```

No candidate status events are inserted.

Consequences:

- `q33_candidate_revision_has_current_stage` fails;
- `q17_candidate_event_contiguous` passes vacuously.

### Required correction

Insert the generated candidate events.

For every current revision:

- exactly one current stage exists;
- event ordinals start at one and are contiguous;
- event revision/family/release agree;
- current stage reconstructs from the latest event.

Add mutations for:

- no event;
- ordinal gap;
- wrong family;
- wrong release;
- two current terminal stages.

The complete populated query matrix must contain no applicable failures.

Capture the five formerly unaliased diagnostics under stable names.

## Defect 8 — the fixture lifecycle was replaced with metadata assertions

`P3A_V38_FIXTURE_RETURN.json` contains seven checks such as:

- family count equals 141;
- a toy hash changes when one member changes;
- an UPDATE is blocked;
- a filename string is absent from code.

It does not execute the required authority lifecycle.

Restore the complete isolated fixture suite:

### Positive

- accepted adjudication;
- split adjudication with complete disjoint union;
- hierarchy adjudication covering both governed endpoints.

### Negative

- duplicate disposition;
- incomplete split union;
- omitted hierarchy endpoint;
- nested semantic mutation with stale hashes;
- release mismatch;
- incomplete promotion mapping after all prerequisites are valid;
- release-neutral origin mismatch;
- reused family/revision identity after semantic change;
- missing semantic binding;
- DB/packet hash divergence;
- missing candidate status event;
- release-ledger prior-hash mismatch.

Run fixtures in a dedicated disposable database or schema and tear it down.

Every negative case must assert:

- SQLSTATE or validator return;
- named trigger/function;
- error regex;
- rollback.

Any other prerequisite failure is a failed test.

## Defect 9 — release change ledger prior hashes are synthetic

For retained R35 families, V38 computes `prior_content_hash` as a new wrapper hash over:

```text
object ID
+ allocation release
+ origin authority ID
```

It is neither the exact prior origin key nor the exact prior candidate evidence hash.

All 141 supplied rows confirm that mismatch.

### Required correction

Define one canonical object snapshot per ledgered object type.

The ledger must compare:

```text
exact prior canonical snapshot hash
exact current canonical snapshot hash
```

The prior snapshot must be read or reconstructed from immutable prior authority artifacts.

Document the snapshot contract and version.

`REVISED` must identify the exact changed fields. `UNCHANGED_REFERENCE` requires exact snapshot equality.

## Defect 10 — reports and verifier accept claims instead of deriving them

The V38 verifier:

- ignores the applicable q33 failure;
- does not compare database and packet hashes;
- does not recompute family semantic origins;
- accepts 141 family continuities by numeric range;
- accepts the seven-case metadata fixture report;
- does not test the evidence-hash mutation probe.

The V39 verifier must independently derive every repaired surface and must fail the inherited V38 worktree.

## Pilot checkpoint

V38 now reports honest zero shortfalls for unsupported proxy strata. Preserve that improvement.

Four unique pilot packets can be valid if those are the only candidates satisfying named persisted evidence after the rebuild.

Recompute the pilot after identity, hash, status-event, and fixture repairs.

Every selected packet must converge with its immutable database revision hash.

## Checkpoint rule

Do not package after ordinary repairs.

Create V39 only when:

1. release-neutral identities truly exclude release-scoped IDs;
2. semantic identities support one-to-many concrete bindings;
3. R35/R39 family continuity is proven by reconstructed semantic origins;
4. all database and packet evidence hashes converge;
5. all semantic evidence is hash-covered;
6. q33 and every applicable populated query pass;
7. the full isolated fixture lifecycle passes at named invariants;
8. the release ledger uses exact canonical prior/current snapshots;
9. the independent verifier derives PASS;
10. PostgreSQL and fixture teardown are proven.

Build only then:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v39_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-61 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V39_IDENTITY_CONTRACT_REVISION.json
P3A_V39_PROJECTION_SEMANTIC_IDENTITIES.csv
P3A_V39_PROJECTION_SEMANTIC_BINDINGS.csv
P3A_V39_COMPONENT_SEMANTIC_IDENTITIES.csv
P3A_V39_COMPONENT_SEMANTIC_BINDINGS.csv
P3A_V39_R35_SEMANTIC_ORIGIN_RECONSTRUCTION.csv
P3A_V39_FAMILY_CONTINUITY_DECISIONS.csv
P3A_V39_DATABASE_PACKET_HASH_CONVERGENCE.csv
P3A_V39_ALL_CANDIDATE_HASH_RECONCILIATION.csv
P3A_V39_CANDIDATE_STATUS_EVENT_RETURN.json
P3A_V39_RELEASE_CHANGE_LEDGER.csv
P3A_V39_RELEASE_LEDGER_SNAPSHOT_CONTRACT.json
P3A_V39_FIXTURE_RETURN.json
P3A_V39_PILOT_STRATA_ELIGIBILITY.csv
P3A_V39_PILOT_PACKET_COVERAGE.csv
P3A_V39_QUERY_MATRIX.csv
P3A_V39_OBJECT_COUNTS.json
P3A_V39_EXECUTION_FINDINGS.csv
P3A_V39_DOCTRINE_DELTAS.csv
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
