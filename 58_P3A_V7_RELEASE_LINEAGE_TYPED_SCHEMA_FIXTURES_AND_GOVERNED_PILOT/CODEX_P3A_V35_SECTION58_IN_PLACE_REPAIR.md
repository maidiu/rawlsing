# Codex in-place continuation brief — v35 release-lineage repair, connected typed constraints, reproducible fixtures, and governed pilot

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not download, upload, or extract another cumulative handoff.

Preserve the existing v35 checkpoint ZIP and v35 worktree as immutable blocked evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v36_WORKING
```

If the v36 tree does not exist, copy the existing v35 working tree locally with `rsync -a`. Do not reconstruct it from a ZIP.

Create section:

```text
58_P3A_V7_RELEASE_LINEAGE_TYPED_SCHEMA_FIXTURES_AND_GOVERNED_PILOT
```

Preserve sections 00–57 unchanged as historical evidence.

## Status correction

V35 does not earn `PASS_WITH_PHASE_AWARE_OVERRIDES`.

The two raw query failures remain legitimate future-phase gates:

- `q01b_postpromotion_pointer` is post-promotion only;
- `q15b_no_unadjudicated_at_p3_close` is P3C-close only.

The operative v35 status is:

```text
BLOCKED_EXECUTION_EVIDENCE_AND_RELEASE_LINEAGE_DEFECT
```

V35 preserves important progress:

- topology is rule-derived;
- direct internal-pair closure reaches 335 UNRULED rows and 345 pair-level obligations;
- redirect no longer counts as a hard collision;
- forty packet artifacts and draft decisions exist;
- PostgreSQL teardown is evidenced.

The checkpoint still fails because its release migration, all-candidate hash closure, typed-constraint contract, fixture return, and pilot sampling are not reproducible from the delivered code.

## Mandatory review evidence

Use the supplied files as regression evidence only:

- `V35_RELEASE_LINEAGE_AND_IDENTITY_AUDIT.json`
- `V35_ALL_CANDIDATE_HASH_REPRODUCIBILITY_GAPS.csv`
- `V35_PILOT_STRATA_SEMANTIC_GAPS.csv`
- `V35_FIXTURE_CODE_OUTPUT_CONTRADICTION.json`
- `V35_TYPED_CONSTRAINT_SCHEMA_PROBE_RETURN.json`
- `V35_ZIP_UNICODE_PATH_AUDIT.json`
- `V35_EXTERNAL_REVIEW_FINDINGS.json`

No production builder may read these files to decide what authority objects to create.

## Defect 1 — R35 is not actually persisted as a successor release

The handoff claims:

```text
R35 parent = R31
```

The delivered loader executes:

```sql
VALUES (%s, NULL, ...)
```

for `p3_authority_release.parent_release_id`.

It also:

- writes stale builder version `p3a-phase3-loader-v30`;
- names section 52 as its migration artifact;
- inserts no `p3_release_status_event`;
- inserts no `p3_release_change_ledger`;
- records no executable migration from prior candidate identities.

### Required correction

Create a real successor release surface.

1. Preserve the blocked v35 release metadata and objects historically.
2. Create R36 with an explicit parent release and current builder/schema/migration metadata.
3. Load release lifecycle events through at least the non-promoted shadow/validated state actually reached.
4. Populate `p3_release_change_ledger` for added, revised, superseded, and unchanged-reference objects.
5. Keep the runtime promotion pointer untouched.
6. No release may be described as a successor when its persisted parent is null.
7. Add an exact release-chain query and mutation tests for:
   - missing parent;
   - self-parent;
   - absent parent row;
   - change ledger omission;
   - claimed shadow release without lifecycle events.

## Defect 2 — the append-only registry does not contain the prior identities

`P3A_V35_OBJECT_COUNTS.json` is generated from all rows in `p3_candidate_revision`, not an R35-filtered query. It reports only:

```text
141 candidate revisions
P3CANDREV-000142-R0001 through P3CANDREV-000282-R0001
```

Candidate revisions 000001–000141 are absent.

Starting numeric allocation at 142 is not an append-only migration if the prior objects are not present in the registry.

### Required correction

Rebuild the identity surface as an actual append-only history.

At minimum preserve/import:

- prior candidate-family identities;
- prior candidate-revision identities;
- prior component identities;
- prior packet identities;
- their allocation releases and immutable origin/content keys.

Then apply the successor logic:

- if a v35 candidate origin remains unchanged, preserve `P3CAND-000142`–`P3CAND-000282` and append an R36 revision such as `R0002`;
- if an origin truly changes, preserve the prior family/revision and allocate a new family under the append-only registry;
- never allocate a new family merely because the database was rebuilt from empty;
- never infer migration by zipping a review CSV to a sorted candidate query;
- persist exact old-to-new migration/supersession objects.

Add a live mutation proving that an existing family or revision identity cannot be rebound to a changed origin.

## Defect 3 — all 141 evidence hashes are not reconstructively closed

The only delivered code that computes the full packet evidence surface is `p3a_v35_packets.py`, and it updates only selected packet candidates.

The file:

```text
p3a_v35_all_candidate_hash_update_return.json
```

claims that 141 hashes were updated, but no delivered generator performs that update.

`p3a_v35_reports.py` calls a hash “PASS” when:

- it has length 64; and
- the literal word `placeholder` is absent from the hexadecimal string.

That does not recompute evidence.

### Required correction

Create one shared canonical evidence builder used by:

- candidate persistence;
- packet export;
- database/packet convergence;
- the independent verifier.

For every candidate revision, the evidence surface must contain the complete governed state, including:

- immutable origin and exact member set;
- component and attachment provenance;
- complete internal-pair matrix;
- direct pair facts and projections;
- all typed constraints and authority sources;
- all closure obligations and links;
- all signature blocker evidence;
- response references;
- exclusions;
- diagnostic flags;
- ranking values and their evidence basis when the governing contract includes ranking;
- exact evidence links;
- schema and serialization versions.

Create the full evidence hash before inserting the successor candidate revision. Do not insert a preliminary hash and later mutate the immutable revision row.

JSON packet export may remain limited to the pilot, but all candidate revisions must have a reproducible canonical evidence snapshot or a database-derived reconstruction return.

The verifier must independently recompute every candidate hash. A 64-character string is not evidence.

## Defect 4 — the typed-constraint contract remains semantically open

The v35 DDL has 78 tables, while the inherited connected dictionary governs 75. The three new tables are:

- `p3_internal_pair_unresolved_boundary`;
- `p3_internal_pair_redirect_boundary`;
- `p3_internal_pair_coordinate_constraint`.

They are absent from the connected schema dictionary and dedicated packet schemas.

In `candidate_packet.schema.json`, all typed-constraint arrays are declared merely as:

```json
{"type": "array", "items": {"type": "object"}}
```

The semantic validator checks endpoint-set reconciliation but not the required semantic fields.

An exact mutation probe removed from a redirect object:

- candidate revision;
- projection;
- redirect scope;
- evidence;
- authority release;

leaving only `left_id` and `right_id`. After canonical hash and packet-ID recomputation, the shipped validator returned PASS.

### Required correction

Connect every typed constraint across:

1. PostgreSQL persistence;
2. stable identity or canonical composite-key specification;
3. connected schema dictionary;
4. dedicated JSON Schema;
5. candidate-packet `$ref`;
6. categorical and object-reference bindings;
7. installer preflight and triggers;
8. packet export;
9. canonical evidence hash;
10. semantic validation;
11. database/packet convergence;
12. mutation tests.

For redirect, unresolved, coordinate, and collision objects, require exact:

- candidate revision;
- pair endpoints;
- pair projection;
- typed relation/scope;
- governing authority/evidence IDs;
- authority release;
- hard-blocker status where applicable;
- downstream effects where applicable.

The supplied stripped-redirect probe must fail.

A SQL typed object omitted from the packet must fail. A packet object with no SQL row must fail. Mutating any semantic field must change the evidence hash.

## Defect 5 — the delivered fixture code cannot produce the delivered fixture report

The clean v35 database contains candidate revisions 142–282.

The delivered fixture program still references old candidate revisions such as:

```text
P3CANDREV-000003-R0001
P3CANDREV-000121-R0001
P3CANDREV-000004-R0001
```

It also:

- runs in the main `p3a_v27_shadow` schema;
- creates no dedicated fixture schema;
- contains no cleanup implementation;
- still converts duplicate-key failures into `PASS_ALREADY_COMMITTED`;
- mutates only top-level hashes in its stale-hash case;
- implements far fewer negative cases than the report claims.

Strings such as `PASS_COMMITTED_ONCE` and many named invariants appear only in the output JSON, not in executable code.

### Required correction

Replace the fixture system rather than editing the summary.

1. Run fixtures in a dedicated disposable database or isolated schema.
2. Build valid fixture candidates inside that fixture surface; do not reference absent production IDs.
3. Execute each positive fixture once from clean state.
4. Test idempotency separately by comparing exact before/after state.
5. Never convert a duplicate-key exception into a positive pass.
6. Execute every named negative fixture in delivered code.
7. Capture SQLSTATE, exact error, named invariant, and transaction rollback.
8. Mutate nested semantic evidence while preserving stale declared hashes.
9. Tear down the fixture surface and prove the main release remains free of canonical families and adjudications.
10. Generate `P3A_V36_FIXTURE_RETURN.json` directly from the executable runner.

The verifier must run or independently replay the fixture suite. It may not accept a report because it contains fifteen labels.

## Defect 6 — six pilot strata are still proxies for unrelated concepts

The v35 eligibility code uses:

- attachment-review origin as `response_variant`;
- any UNRULED pair as `split_required`;
- any coordinate row as `hierarchical_target`;
- proposition-only seed origin as `derived_index`;
- unresolved authority as `exact_only_authority`;
- semantic redirect as `precedence_overlap_conflict`.

These are not evidence-backed definitions of the named strata.

All response references remain `UNKNOWN`, so attachment origin cannot establish response variation.

### Required correction

Define each of the eleven strata through the actual evidence named by the category.

- `response_variant` requires persisted response-contract variation evidence.
- `split_required` requires a governed split trigger, not generic missing pair authority.
- `hierarchical_target` requires a directional broader/narrower or explicitly governed hierarchy relation; coordinate-only is not enough.
- `derived_index` requires derived/index evidence.
- `exact_only_authority` requires exact authority without semantic governing authority, tracked from the precedence surface.
- `precedence_overlap_conflict` requires an actual overlap/conflict in authority precedence.
- `clean_multi_source` requires complete signatures and no noncompensable blockers.
- Other categories must likewise cite their exact persisted evidence.

If a category has zero eligible candidates, report zero. Do not rebrand origin type or uncertainty as the missing category.

## Defect 7 — overlap is allowed, but v35 globally suppresses it

The governing pilot rules state:

```text
overlap_allowed: true
```

The selector keeps one global `used` set. Once a candidate is selected or substituted for one category, it cannot satisfy a later category.

This creates false shortfalls:

- the only hard-collision candidate is consumed earlier as a clean-stratum substitute, so collision selected count becomes zero;
- the redirect candidate is consumed earlier, so precedence-overlap selected count becomes zero;
- other eligible candidates are similarly suppressed.

### Required correction

Separate:

1. stratum coverage; and
2. unique packet selection.

A candidate may satisfy multiple strata. Record all primary and secondary stratum memberships.

For every stratum:

- calculate eligibility independently;
- select up to target regardless of prior use;
- record coverage using eligible candidates already in the packet set;
- add new packets only when needed to increase coverage;
- keep the unique packet set at or below forty.

Do not record a shortfall when an eligible candidate is already selected under another stratum.

Substitutions must name the evidence-based distance or ordering that makes them the nearest unrepresented risk. A generic global fallback list is insufficient.

## Defect 8 — the verifier trusts summaries rather than evidence

The v35 verifier:

- checks candidate hashes only for length and a literal substring;
- trusts `status=PASS` in direct, typed, and ranking CSVs;
- checks fixture report status and case count without running the fixture code;
- checks pilot row counts but not category semantics or overlap;
- does not verify release parentage or historical identity preservation;
- does not verify the final ZIP path set or UTF-8 flags.

### Required correction

The v36 verifier must independently derive:

- release parentage, status history, and change ledger;
- preservation of prior identities;
- every candidate evidence hash;
- all typed SQL/schema/packet objects;
- pilot eligibility and overlap coverage;
- actual fixture execution and named failure reasons;
- package path/hash/count reconciliation;
- Unicode filename flags;
- absence of cache/bytecode debris.

It must fail the inherited v35 checkpoint.

## Defect 9 — final ZIP Unicode handling regressed

The final ZIP contains two governed payload paths containing `Latinobarómetro`, but the UTF-8 flag is not set.

Python `zipfile` therefore exposes:

```text
Latinobar├│metro
```

while `PACKAGE_INDEX.csv` names:

```text
Latinobarómetro
```

This reintroduces the packaging defect previously corrected in v29.

### Required correction

Build the final v36 ZIP with a Unicode-safe archiver that sets bit `0x800` for every non-ASCII filename.

Verify the actual final ZIP using Python `zipfile`:

- both governed paths round-trip exactly;
- both file entries have the UTF-8 flag;
- manifest path-set difference is empty;
- hashes and sizes match;
- the archive root is the release checkpoint name, not a mutable `*_WORKING` label.

## Defect 10 — release metadata is stale

Do not ship R36 with:

- a v30 builder version;
- a section-52 migration artifact;
- stale rollback metadata.

All release metadata must identify the actual section-58 builder, migration, validation, and rollback artifacts.

## Clean rebuild and stopping rule

Rebuild from an empty disposable PostgreSQL 15 instance, but import and preserve the historical release/identity surface before applying R36.

Continue through ordinary implementation defects.

Stop only if a real populated object exposes a remaining governing contradiction.

Do not package after ordinary repairs.

Create the v36 checkpoint only when:

1. release lineage and append-only identity history are executable;
2. all candidate hashes independently recompute;
3. typed constraints are fully connected;
4. fixtures are generated by the delivered runner;
5. pilot strata use their named evidence;
6. overlap coverage is correct;
7. the verifier derives PASS;
8. the final ZIP is Unicode-safe;
9. PostgreSQL and fixture teardown are proven.

Build:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v36_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-58 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V36_RELEASE_LINEAGE_RETURN.json
P3A_V36_RELEASE_CHANGE_LEDGER.csv
P3A_V36_HISTORICAL_IDENTITY_IMPORT_RETURN.json
P3A_V36_CANDIDATE_REVISION_MIGRATION.csv
P3A_V36_ALL_CANDIDATE_HASH_RECONCILIATION.csv
P3A_V36_TYPED_CONSTRAINT_CONVERGENCE.csv
P3A_V36_TYPED_SCHEMA_MUTATION_RETURN.json
P3A_V36_PILOT_STRATA_ELIGIBILITY.csv
P3A_V36_PILOT_CANDIDATE_STRATA.csv
P3A_V36_PILOT_SUBSTITUTION_LEDGER.csv
P3A_V36_FIXTURE_RETURN.json
P3A_V36_QUERY_MATRIX.csv
P3A_V36_OBJECT_COUNTS.json
P3A_V36_EXECUTION_FINDINGS.csv
P3A_V36_DOCTRINE_DELTAS.csv
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
