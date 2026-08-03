# Codex in-place continuation brief — v36 truthful historical identity migration, complete evidence closure, and actual pilot execution

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not download, upload, or extract another cumulative handoff.

Preserve the v36 worktree and section-58 delta as immutable blocked evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v37_WORKING
```

If the v37 tree does not exist, copy the v36 working tree locally with `rsync -a`. Do not reconstruct it from a ZIP.

Create section:

```text
59_P3A_V7_TRUTHFUL_HISTORY_COMPLETE_EVIDENCE_AND_ACTUAL_PILOT
```

Preserve sections 00–58 unchanged.

## Status correction

V36 does not earn PASS.

The historical/current candidate-origin boundary is now conceptually correct:

- incomplete historical graphs are no longer fabricated as current candidate revisions;
- frozen historical identity rows are immutable;
- new current candidates still satisfy the complete current origin trigger.

But the historical identities stored in that boundary are not truthful, and the packet, pilot, typed-schema, fixture, and verifier surfaces remain incomplete.

The operative status is:

```text
BLOCKED_HISTORICAL_IDENTITY_AND_EXECUTION_EVIDENCE_DEFECT
```

The two future-phase query overrides remain legitimate:

- `q01b_postpromotion_pointer`;
- `q15b_no_unadjudicated_at_p3_close`.

## Mandatory review evidence

Use these supplied files as regressions only:

- `V36_HISTORICAL_IDENTITY_AND_SUCCESSOR_CONTRADICTION.csv`
- `V36_PILOT_PACKET_COVERAGE_AUDIT.csv`
- `V36_ALL_CANDIDATE_HASH_CLOSURE_GAPS.csv`
- `V36_TYPED_CONSTRAINT_MUTATION_PROBE.json`
- `V36_FIXTURE_INVARIANT_AUDIT.csv`
- `V36_EXTERNAL_REVIEW_FINDINGS.json`

Production code may not read them to decide what objects to create.

## Defect 1 — historical identity values are fabricated

The historical importer currently computes:

```python
origin_key = sha256("historical-candidate-origin|<id>|<release>")
evidence_bundle_hash = sha256("historical-candidate-evidence|<id>|<release>")
```

These values did not exist in the prior releases.

For all 141 R35 candidate families/revisions, the actual origin keys and evidence hashes are present in the immutable v35 checkpoint. The supplied audit proves:

- synthetic origin matches actual: 0/141;
- synthetic evidence hash matches actual: 0/141.

The importer also uses one generic source-package label rather than the exact prior artifact path/hash.

### Required correction

Historical preservation must preserve the actual historical value or explicitly preserve `UNKNOWN`, never manufacture a plausible hash.

For each historical family/revision:

1. locate the authoritative prior checkpoint artifact;
2. import the exact historical object ID;
3. import the exact allocation release;
4. import the exact immutable origin key when available;
5. import the exact evidence-bundle hash when available;
6. record the exact source artifact path and SHA-256;
7. record which fields are unavailable;
8. use nullable/explicitly unknown fields for unavailable values rather than hashing a sentence;
9. preserve an evidence-status field distinguishing:
   - `EXACT_PRIOR_ARTIFACT`;
   - `PARTIAL_PRIOR_ARTIFACT`;
   - `IDENTITY_ONLY_NO_HASH_AUTHORITY`.

A frozen historical row with an invented origin or evidence hash must fail.

The actual v35 values in the supplied audit are mandatory regressions.

## Defect 2 — family genealogy is internally contradictory

V36’s migration table says:

```text
prior family 000001 → v36 family 000142
...
prior family 000141 → v36 family 000282
```

But current revisions are:

```text
P3CANDREV-000142-R0002
...
P3CANDREV-000282-R0002
```

This treats family 142 simultaneously as:

- a new successor family to family 1; and
- the existing R35 family receiving revision 2.

Those are different genealogies.

The actual R35 family IDs are already 142–282 with R0001 revisions.

### Required correction

For every rule-derived v36 candidate, compare the canonical immutable family-origin key against the actual R35 family-origin key.

Then apply exactly one branch:

### Branch A — unchanged family origin

When the canonical origin key is identical:

- preserve the same candidate family ID;
- preserve its actual historical family-origin key;
- append `R0002`;
- record predecessor revision `R0001`;
- create an explicit revision genealogy/change-ledger row.

### Branch B — changed family origin

When any identity-bearing origin element changes:

- preserve the old family and R0001 frozen;
- allocate a new candidate family ID after the existing maximum;
- create its first revision as `R0001`;
- record explicit family supersession/genealogy;
- do not call it R0002;
- do not reuse the old family ID.

The governing family-origin key includes exact:

- components;
- attachment projections;
- diagnostic lane/origin type;
- subject set.

Do not change that key under the same durable family ID.

Add database triggers/regressions proving:

1. a family ID cannot be rebound to a different origin key;
2. an R0002 revision requires a preserved R0001 predecessor in either the live revision table or the exact frozen-history ledger;
3. a new successor family begins at R0001;
4. the migration table cannot name a different prior family than the predecessor implied by revision numbering.

## Defect 3 — populate the release change ledger

R36 parentage and release-status events are now inserted. Preserve that progress.

However, delivered production code inserts no rows into:

```text
p3_release_change_ledger
```

Populate the ledger for:

- imported historical identity references;
- unchanged family references;
- appended revisions;
- newly allocated successor families;
- revised packet/schema objects;
- superseded or blocked prior objects.

Every R37 current object must be classified as:

- `ADDED`;
- `REVISED`;
- `SUPERSEDED`;
- `DEPRECATED`;
- `UNCHANGED_REFERENCE`.

The verifier must reconcile the ledger against actual object and content hashes.

## Defect 4 — one shared full-evidence builder must govern all candidates

The candidate loader computes one partial hash surface. The packet builder computes a larger surface and updates only the candidates for which packets are emitted.

V36 produces only eleven packets, so 130 candidate hashes never pass through the full packet evidence builder.

`P3A_V36_ALL_CANDIDATE_HASH_RECONCILIATION.csv` calls a hash PASS solely because its length is 64.

### Required correction

Implement one canonical evidence builder used by:

- current candidate revision creation;
- all-candidate hash reconciliation;
- packet export;
- database/packet convergence;
- the independent verifier.

Run it for every current candidate before inserting the immutable revision.

No later packet-export update to `p3_candidate_revision.evidence_bundle_hash` is permitted.

For all current candidates, include:

- family and revision identity;
- canonical origin;
- complete membership;
- component and attachment provenance;
- every pair fact and projection;
- full internal pair matrix;
- typed constraints;
- closure obligations;
- complete signature/blocker evidence;
- response references;
- exclusions;
- ranking and its evidence basis;
- exact evidence links;
- schema/serialization versions.

All candidate hashes must independently recompute without exporting a human packet.

## Defect 5 — the pilot index has forty candidates but only eleven packets

The pilot index contains forty selected rows.

The executable packet builder instead runs:

```python
selected = select_candidates(cur)[:args.limit]
```

and section 58 produced:

- pilot-index rows: 40;
- packets: 11;
- draft decisions: 11;
- convergence validations: 11.

That is not a forty-candidate pilot.

### Required correction

The set used for packet export must be the exact unique candidate set produced by the governed pilot coverage algorithm.

For every selected candidate create:

- packet;
- draft decision;
- schema-validator return;
- semantic-validator return;
- database/packet convergence return;
- canonical evidence hash.

Do not use a separate `--limit` to truncate the final pilot.

A separate three-candidate vertical slice may exist, but it must not be reported as the complete pilot.

## Defect 6 — pilot strata still use proxy predicates

The current predicates still equate:

- attachment-review origin with response variation;
- any UNRULED pair with split requirement;
- coordinate relation with hierarchy;
- proposition-only seed with derived index;
- unresolved authority with exact-only authority;
- semantic redirect with precedence-overlap conflict.

These are not the named evidence categories.

Use only actual persisted evidence for each stratum.

When evidence does not exist, report zero eligible candidates and an honest shortfall.

Do not infer response variation from attachment origin while all response contracts remain `UNKNOWN`.

Do not infer split requirement from absence of direct pair authority.

Do not infer derived-index status from graph origin.

## Defect 7 — overlap is allowed but globally suppressed

The selector still keeps one global `used` set.

This prevents an eligible candidate from satisfying multiple target strata, even though the governing rules allow overlap.

The hard-collision candidate is consumed as a clean-stratum substitute and then omitted from collision coverage.

### Required correction

Separate:

1. per-stratum eligibility and coverage;
2. the unique packet set.

A candidate may cover multiple strata.

For every stratum:

- calculate eligibility independently;
- select up to target independently;
- record all primary and secondary memberships;
- add a new packet only when the existing packet set does not cover the target;
- keep the unique packet count at or below forty.

Never report a shortfall when an eligible candidate is already in the packet set under another stratum.

## Defect 8 — typed-constraint semantics remain schema-optional

The supplied mutation probe removes from a redirect object:

- candidate revision;
- projection ID;
- redirect scope;
- evidence IDs;
- authority release;

leaving only endpoints.

After canonical hash and packet-ID recomputation, the shipped validator returns PASS.

### Required correction

Create dedicated JSON schemas and connected dictionary entries for:

- collision;
- unresolved boundary;
- redirect boundary;
- coordinate/hierarchy constraint.

Candidate packet arrays must `$ref` those schemas.

The semantic validator must verify:

- exact candidate revision;
- exact endpoint pair;
- exact projection;
- exact pair fact and governing authority;
- relation/scope;
- evidence IDs;
- release;
- hard-blocker semantics;
- downstream effects where applicable.

The stripped-redirect mutation must fail.

## Defect 9 — fixtures accept any exception as the named expected failure

`run_case` marks every exception in a negative case as `EXPECTED_FAIL`.

Therefore the suite passes even when the wrong prerequisite fails first.

The current incomplete-promotion case still fails at:

```text
Variant acceptance requires variant assignment
```

rather than incomplete promotion mapping.

The stale-hash case still modifies only top-level declared hashes rather than nested semantic evidence.

The code also retains `PASS_ALREADY_COMMITTED` for positive duplicate-key failures and runs fixture authority in the main schema.

### Required correction

For every negative fixture:

- specify expected SQLSTATE;
- specify expected invariant/function;
- specify an error-text pattern;
- fail the test when another prerequisite fires first.

Create a dedicated disposable fixture database or schema and tear it down.

Positive cases must commit once from clean state. Duplicate-key failure is not a positive pass.

The stale-hash case must mutate nested semantic evidence while preserving stale declared hashes.

Include all section-58 requested identity, typed-schema, release-lineage, and pilot mutations.

## Defect 10 — make the verifier independent

The v36 verifier trusts:

- CSV `status=PASS`;
- 64-character hashes;
- pilot row counts;
- fixture labels.

It does not derive the historical hashes, family genealogy, release change ledger, all candidate evidence, complete pilot packet coverage, typed schemas, or named fixture invariant.

The v37 verifier must independently reconstruct every one of those surfaces and must fail the inherited v36 worktree.

## Checkpoint rule

Do not package after ordinary corrections.

Create v37 only when:

1. historical values are exact or explicitly unknown—never synthetic;
2. family/revision genealogy is internally coherent;
3. release change ledger is populated;
4. every candidate hash comes from the shared full-evidence builder;
5. every pilot selection has a packet and draft;
6. pilot strata use their named evidence and overlap correctly;
7. typed constraints are schema-enforced;
8. fixtures fail at the named invariant in an isolated surface;
9. the independent verifier derives PASS;
10. PostgreSQL and fixture teardown are proven.

Build only then:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v37_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-59 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V37_HISTORICAL_IDENTITY_IMPORT.csv
P3A_V37_HISTORICAL_EVIDENCE_STATUS.csv
P3A_V37_FAMILY_ORIGIN_COMPARISON.csv
P3A_V37_FAMILY_AND_REVISION_GENEALOGY.csv
P3A_V37_RELEASE_CHANGE_LEDGER.csv
P3A_V37_ALL_CANDIDATE_HASH_RECONCILIATION.csv
P3A_V37_TYPED_CONSTRAINT_SCHEMA_RETURN.json
P3A_V37_PILOT_STRATA_ELIGIBILITY.csv
P3A_V37_PILOT_CANDIDATE_STRATA.csv
P3A_V37_PILOT_PACKET_COVERAGE.csv
P3A_V37_FIXTURE_RETURN.json
P3A_V37_QUERY_MATRIX.csv
P3A_V37_OBJECT_COUNTS.json
P3A_V37_EXECUTION_FINDINGS.csv
P3A_V37_DOCTRINE_DELTAS.csv
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
