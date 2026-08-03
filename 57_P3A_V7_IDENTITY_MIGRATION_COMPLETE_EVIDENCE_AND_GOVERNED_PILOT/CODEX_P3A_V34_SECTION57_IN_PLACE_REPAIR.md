# Codex in-place continuation brief — v34 identity migration, complete evidence closure, and governed P3A pilot

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not upload, download, or extract another cumulative handoff.

Preserve the existing v34 checkpoint and v34 working tree as immutable review evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v35_WORKING
```

If it does not exist, copy the v34 working tree locally with `rsync -a`. Do not reconstruct from a ZIP.

Create section:

```text
57_P3A_V7_IDENTITY_MIGRATION_COMPLETE_EVIDENCE_AND_GOVERNED_PILOT
```

Preserve sections 00–56 unchanged as historical evidence.

## Status correction

V34 does not earn `PASS_WITH_PHASE_AWARE_OVERRIDES`.

The two phase-aware raw query overrides remain legitimate:

- `q01b_postpromotion_pointer` is post-promotion only;
- `q15b_no_unadjudicated_at_p3_close` is P3C-close only.

The operative status is:

```text
BLOCKED_EXECUTION_EXPOSED_IDENTITY_AND_PILOT_EVIDENCE_DEFECT
```

V34 made one real architectural advance: it derives topology from populated projections rather than reading the diagnostic preflight candidate inventory. Preserve that work.

The blocker is that the new derived topology was installed by reusing immutable identities and by producing only a partially closed candidate evidence surface.

## Mandatory review fixtures

Use the supplied files as regression evidence only:

- `V34_CANDIDATE_IDENTITY_REUSE_AUDIT.csv`
- `V34_PACKET_IDENTITY_REUSE_AUDIT.csv`
- `V34_INTERNAL_DIRECT_PROPOSITION_GAP.csv`
- `V34_TYPED_CONSTRAINT_EXPORT_GAPS.csv`
- `V34_RANKING_AND_PILOT_GAPS.csv`
- `V34_EXTERNAL_REVIEW_FINDINGS.json`

No production builder may read these files to decide what objects to create.

## Defect 1 — durable candidate identities were overwritten

The governing identity contract says:

- `CANDIDATE_FAMILY` is a registry-allocated durable ID;
- its idempotency key is the immutable candidate origin key;
- allocation is deterministic from sorted origin keys and append-only thereafter;
- `CANDIDATE_REVISION` identities append and never overwrite.

V34 enumerates rule-derived candidates from `1` again and writes:

```text
P3CAND-000001 ... P3CAND-000141
P3CANDREV-000001-R0001 ... P3CANDREV-000141-R0001
```

under the same R31 release.

Independent comparison establishes:

- all 141 origin keys changed under reused family/revision IDs;
- for the first 119 strict/seed candidates, the member set is the same but the immutable origin key changes;
- all 22 attachment-review numeric IDs now denote different member sets;
- the same 22 attachment groups still exist, but every one moved to a different numeric candidate ID.

A clean rebuild concealed an identity overwrite that an in-place append-only registry would reject.

### Required correction

Do not mutate or reinterpret any v31–v34 candidate family, revision, packet, or origin key.

1. Load the prior candidate identity surface from the immutable local v33/v34 checkpoint.
2. Recompute the canonical origin descriptor under the actual identity specification:
   - exact component IDs;
   - exact attachment projection IDs;
   - diagnostic lane/origin type;
   - exact subject set;
   - canonical JSON serialization version.
3. Produce a 141-row migration ledger comparing prior and corrected origin identities.
4. Determine whether the previous origin key was valid under the governing identity contract:
   - if valid, preserve it and map rule-derived topology to the existing family;
   - if invalid, preserve the old family/revision as historical and allocate a new family under a successor release.
5. Never reuse an existing `candidate_family_id` or `candidate_revision_id` for a different origin key or member surface.
6. Never reset allocation to candidate 1. Allocate from the append-only registry.
7. If the same semantic family receives corrected evidence or origin machinery, create an append-only successor revision or explicit supersession/migration; do not rewrite `R0001`.
8. Preserve old-to-new genealogy/supersession and exact migration reason.
9. Add a live mutation test proving an attempt to bind an existing family or revision ID to a changed origin fails.

Create a successor non-promoted P3A authority release with R31 as parent. Do not continue mutating R31 in place.

No runtime promotion is authorized.

## Defect 2 — packet IDs are not content addressed

`P3_IDENTITY_KEY_SPEC_v7.csv` requires the candidate packet idempotency key to include:

- candidate revision ID;
- evidence-bundle hash;
- packet schema version.

V34 calculates:

```python
packet_id = stable("P3PKT", candidate_revision_id)
```

All 40 packet IDs are therefore identical to their v33 packet IDs even though all 40 evidence-bundle hashes changed.

### Required correction

- Compute packet ID from canonical serialization of:
  - corrected candidate revision ID;
  - full evidence-bundle hash;
  - exact packet schema version/ID.
- Preserve prior packet artifacts unchanged.
- Allocate new packet IDs whenever evidence or packet schema changes.
- Add a collision regression using all 40 supplied rows.
- The verifier must independently recompute every packet ID.

Draft-decision artifact IDs must likewise remain stable only for the same candidate revision and decision draft identity; selection-order changes may not silently reassign them.

## Defect 3 — component IDs omit the build-rule version

The component identity contract requires:

```text
sorted member IDs + sorted pair projection IDs + build-rule version
```

V34 component IDs omit the build-rule version from the content-addressed payload.

Correct strict and proposition-only component identity generation. Preserve existing components historically and migrate/supersede rather than overwriting IDs when the corrected content key differs.

Add a mutation proving a changed build-rule version changes the component ID.

## Defect 4 — 101 candidate revisions retain placeholder evidence hashes

All 141 revisions are inserted with:

```text
sha256("v34-candidate-evidence-placeholder|...")
```

Only the forty packet-selected revisions are updated with full semantic evidence hashes. The remaining 101 revisions retain syntactically valid but nonreconstructive placeholders.

### Required correction

Build the complete semantic evidence surface and canonical evidence hash for every candidate revision before declaring the candidate inventory complete.

Exporting a JSON packet may remain limited to the human pilot, but every persisted candidate revision must have:

- reconstructive origin;
- complete membership;
- component and attachment provenance;
- complete internal pair matrix;
- all typed constraints;
- all pair-level obligations;
- all diagnostic blocker evidence;
- ranking;
- exclusions;
- response references;
- canonical evidence hash.

No production code or database row may contain `placeholder` evidence-hash logic.

Add a global query and verifier gate that recomputes all 141-or-migrated candidate hashes.

## Defect 5 — one direct proposition authority is still dropped

The strict candidate containing component:

```text
P3COMP-6f3d25ad2139837f
```

has a direct proposition-only internal relation:

```text
P3PF-dd51a3300d36108e
P3PROJ-78c82f5606716abb
p2lineage_2ac8db9fd682548265564412
p2lineage_d91ccee2119ae964f50a4297
```

V34 explicitly excludes proposition-only relations inside strict candidates from `DIRECT_POSITIVE`, then falls through to `UNRULED` without creating an obligation.

This is why the summary contains:

- 336 UNRULED pair rows;
- only 345 pair-level obligations.

### Required correction

An internal direct proposition-only authority is direct pair evidence even when the strict component is already connected by response-compatible edges.

For the affected strict candidate:

- persist `DIRECT_POSITIVE`;
- cite the existing projection;
- do not create an unruled obligation.

Expected count effect on the current topology:

- UNRULED: 336 → 335;
- total pair-level obligations: remains 345.

Apply the rule globally.

Add database gates:

- every candidate-internal direct pair fact is represented;
- no direct pair fact is labeled UNRULED;
- every remaining UNRULED pair has exactly one UNRULED obligation;
- every pair-level obligation is linked exactly once.

## Defect 6 — typed constraints are not a connected contract surface

V34 adds three SQL tables:

- `p3_internal_pair_unresolved_boundary`;
- `p3_internal_pair_redirect_boundary`;
- `p3_internal_pair_coordinate_constraint`.

They are absent from the governing 75-table schema dictionary, connected JSON schemas, categorical/type bindings, and packet contract.

Their semantic fields are not exported into candidate packets or included in evidence hashes.

### Required correction

Connect each typed constraint across:

1. PostgreSQL persistence;
2. stable identity or explicit canonical child-key contract;
3. schema dictionary;
4. JSON Schema;
5. vocabulary and object-reference bindings;
6. packet export;
7. canonical evidence hash;
8. semantic validator;
9. database/packet convergence checks;
10. mutation tests.

The complete collision object must also export and hash:

- `hard_blocker`;
- source scope;
- historical scope;
- downstream effects;
- governing authority links.

A mutation to any typed constraint field must change the packet evidence hash.

A typed constraint present in SQL but absent from the packet must fail.

## Defect 7 — redirect authority is still misclassified as a hard collision

`REDIRECT_OTHER_DOMAIN` is currently:

- stored as `DIRECT_COLLISION`;
- counted in `hard_collision_count`;
- exported in `hard_collisions`;
- classified as `COLLISION_BEARING_CANDIDATE`;

while its SQL collision row says `hard_blocker=false`.

Use the available `SEMANTIC_ARTIFACT_RISK` candidate classification or an equally explicit governed representation.

A semantic redirect must not:

- increment hard-collision count;
- satisfy collision pilot eligibility merely by existing;
- appear as a hard collision;
- erase its redirect scope.

The explicit negative pair remains a real collision and must remain distinct.

## Defect 8 — candidate ranking fields contain unrelated quantities

V34 populates:

- `primary_class_rank` with candidate enumeration ordinal;
- `hard_collision_count` with negative plus redirect count;
- `structure_support_count` with direct-positive pair count;
- `response_variant_complexity` with unresolved plus hierarchy count.

These are not approximations. They are different concepts.

### Required correction

Define and persist exact evidence-backed calculations:

- `primary_class_rank`: finite ranking of candidate classification;
- `hard_collision_count`: hard-blocker collision objects only;
- `structure_support_count`: actual persisted structural-context/support evidence;
- `response_variant_complexity`: explicit response-form variant evidence;
- signature completeness: governed field-level completeness;
- unresolved obligation count: exact open unresolved/closure burden.

Unknown evidence yields zero or fail-closed status, not a substituted metric.

Add field-level provenance or reproducible query definitions for every ranking value.

## Defect 9 — the eleven-stratum pilot is still not executed

The production selector runs five broad queries and truncates the resulting list to forty.

The supplied eligibility artifact is internally impossible:

- one hierarchy candidate is eligible but zero are selected;
- selected counts of 22, 16, 15, 40, 103, and 3 exceed their category targets;
- `SHORTFALL_RECORDED` is used when selected count exceeds target;
- no pilot candidate index links selected candidates to primary/secondary strata;
- the substitution ledger contains no substitute candidate IDs.

All signatures remain fail-closed and response topology remains `UNKNOWN`, so categories such as clean multi-source and response variant cannot be populated merely from graph origin.

### Required correction

Implement eleven independent evidence-backed eligibility queries:

- `clean_multi_source`: 7;
- `response_variant`: 5;
- `split_required`: 5;
- `collision_or_nontransitive`: 5;
- `hierarchical_target`: 4;
- `derived_index`: 3;
- `heterogeneous_lineage`: 3;
- `structure_supported`: 3;
- `source_dominated_or_sparse`: 2;
- `exact_only_authority`: 2;
- `precedence_overlap_conflict`: 1.

For each category record:

- target;
- exact eligibility definition;
- eligible candidate IDs;
- ranked eligible population;
- selected candidate IDs, never exceeding target;
- shortfall;
- named substitute candidate IDs;
- reason each substitute is the nearest unrepresented risk.

Overlap is allowed, but each selected candidate must carry evidence-backed category membership.

Select the available hierarchical candidate before recording a hierarchy shortfall.

Generate:

- an actual pilot candidate index;
- eligibility CSV;
- selection return;
- substitution ledger;
- all packets and drafts;

from delivered code against the populated database.

The verifier must reconstruct the selection independently.

## Defect 10 — fixture claims remain false

The fixture runner still:

- treats duplicate-key exceptions in positive cases as `PASS_ALREADY_COMMITTED`;
- allows incomplete-promotion mapping to fail at the earlier missing-variant-assignment prerequisite;
- mutates only top-level hash fields in the stale-hash case;
- omits the new identity, typed-constraint, topology, and pilot mutations requested in section 56.

### Required correction

Run fixtures on a genuinely clean isolated fixture database/schema.

Positive cases must commit once from clean state. A duplicate is not a positive pass.

A separate idempotency rerun may verify exact no-op behavior, but must compare complete object state.

Required negative fixtures include:

- incomplete split union;
- omitted hierarchy endpoint;
- duplicate dispositions;
- release mismatch;
- incomplete promotion mapping after every prerequisite is valid;
- nested semantic evidence mutation with stale declared hashes;
- missing typed collision;
- missing unresolved/redirect/coordinate object;
- direct pair fact mislabeled UNRULED;
- reused candidate family/revision ID with changed origin;
- reused packet ID after evidence change;
- changed build-rule version retaining component ID;
- missing seed component link;
- review/preflight regression input dependency;
- pilot candidate selected without stratum evidence.

Every mutation must fail at the named invariant.

Report separately:

- fixture positive adjudications executed;
- fixture negative cases;
- main P3A adjudications/canonical families;
- fixture cleanup or teardown.

Do not report fixture adjudications as both already committed and zero.

## Defect 11 — reports and verifier are not independently reproducible

No delivered production code generates most of the summary artifacts consumed by `verify_handoff_v34.py`.

The verifier checks fixed counts and summary statuses rather than deriving:

- candidate identity migration;
- all candidate evidence hashes;
- global direct-pair closure;
- typed constraint packet convergence;
- ranking values;
- pilot eligibility and substitutions;
- fixture failure reasons.

### Required correction

Deliver one reproducible report builder or explicit per-artifact generators.

The verifier must independently derive the result from:

- immutable inputs;
- delivered code;
- populated PostgreSQL returns;
- packet artifacts.

It must not trust a summary file merely because it says `PASS`.

## State, release, teardown, and checkpoint rules

`WORKTREE_STATE.json` and `EXACT_CONTINUATION.md` remain at pre-execution state, while the package claims completion. No section-56 PostgreSQL teardown proof is delivered.

At the next checkpoint:

- update state only after the final clean rebuild;
- record the actual successor release;
- preserve R31 unchanged;
- prove PostgreSQL teardown on `127.0.0.1:55432`;
- report no running disposable server;
- produce a deterministic database rebuild;
- produce a complete full-package extraction verification.

Do not package after ordinary implementation repairs.

Create v35 only when:

1. candidate and packet identities are append-only and migration-safe;
2. all candidate hashes are reconstructive;
3. every direct internal authority is represented;
4. typed constraints are connected across SQL/schema/packet/hash;
5. ranking fields are semantically correct;
6. the eleven pilot strata are truly executed;
7. fixtures fail at named invariants;
8. the independent verifier derives PASS;
9. state and teardown evidence are current.

Build:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v35_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-57 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V35_CANDIDATE_IDENTITY_MIGRATION.csv
P3A_V35_PACKET_IDENTITY_RECONCILIATION.csv
P3A_V35_COMPONENT_IDENTITY_RECONCILIATION.csv
P3A_V35_ALL_CANDIDATE_HASH_RECONCILIATION.csv
P3A_V35_DIRECT_PAIR_CLOSURE_RECONCILIATION.csv
P3A_V35_TYPED_CONSTRAINT_CONVERGENCE.csv
P3A_V35_RANKING_DERIVATION.csv
P3A_V35_PILOT_STRATA_ELIGIBILITY.csv
P3A_V35_PILOT_CANDIDATE_INDEX.csv
P3A_V35_PILOT_SUBSTITUTION_LEDGER.csv
P3A_V35_FIXTURE_RETURN.json
P3A_V35_QUERY_MATRIX.csv
P3A_V35_OBJECT_COUNTS.json
P3A_V35_EXECUTION_FINDINGS.csv
P3A_V35_DOCTRINE_DELTAS.csv
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
