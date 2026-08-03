# Codex in-place continuation brief — v37 release-neutral family identity, truthful historical sourcing, immutable candidate evidence, and live R38 verification

## Fixed workspace

Continue inside:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution
```

Do not download, upload, or extract another cumulative handoff.

Preserve section 59 and the v37 delta as immutable blocked evidence.

Create or resume:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/work/Rawlsing_J_Family_Authority_Strategy_Handoff_v38_WORKING
```

If the v38 tree does not exist, copy the v37 working tree locally with `rsync -a`. Do not reconstruct from a ZIP.

Create section:

```text
60_P3A_V7_RELEASE_NEUTRAL_FAMILY_IDENTITY_AND_LIVE_VERIFICATION
```

Preserve sections 00–59 unchanged.

## Status correction

V37 does not earn PASS.

The typed-constraint stripping probe is now correctly rejected, all 141 candidates pass through the fuller packet evidence builder, and the historical/current trigger boundary commits.

The remaining blocker is deeper:

```text
BLOCKED_IDENTITY_KEY_AND_REPRODUCIBILITY_CONTRACT_DEFECT
```

## Governing identity contradiction

The delivered v7 identity specifications currently compose as follows:

1. `PAIR_PROJECTION` identity includes `authority_release_id`.
2. `CANDIDATE_COMPONENT` identity includes exact pair projection IDs.
3. `CANDIDATE_FAMILY` origin includes exact component and attachment-projection identities.

Therefore changing only the authority release changes:

- every pair projection ID;
- every component ID;
- every candidate family origin key.

This makes the `UNCHANGED_ORIGIN_APPEND_REVISION` branch impossible across releases.

V37 demonstrates the consequence: all 141 R35 origins compare unequal and 141 new families are allocated, even though the v35 and v37 topology algorithms derive the same semantic candidate graph.

This is a governing identity-key contradiction, not an ordinary missing-row bug.

## Required bounded contract correction

Separate release-neutral family identity from release-scoped revision evidence.

### A. Release-neutral projection semantic fingerprint

Define a canonical semantic fingerprint from:

- pair fact identity;
- resolved left subject;
- resolved right subject;
- projection basis.

Exclude `authority_release_id`.

The concrete `p3_pair_projection.projection_id` may remain release-scoped under the existing contract. The new semantic fingerprint is used only for cross-release component and family identity comparison.

### B. Release-neutral component semantic fingerprint

Define from:

- component type;
- exact sorted subject IDs;
- exact sorted release-neutral projection semantic fingerprints;
- immutable topology/build-rule contract version.

Do not use concrete release-scoped projection IDs.

### C. Release-neutral candidate-family semantic origin key

Define from:

- candidate origin lane/type;
- exact sorted subject set;
- exact sorted component semantic fingerprints;
- exact sorted attachment projection semantic fingerprints;
- explicit origin-key serialization version.

Do not use concrete release-scoped component or projection IDs.

### D. Release-scoped candidate revision evidence

Candidate revisions continue to contain and hash:

- concrete release-scoped component IDs;
- concrete release-scoped projection IDs;
- current typed constraints;
- current obligations;
- current authority and evidence.

Thus:

- family identity answers, “Is this the same semantic candidate origin?”
- revision evidence answers, “What exact release-specific evidence surface currently represents it?”

Update `P3_IDENTITY_KEY_SPEC_v7.csv` or issue a narrowly scoped successor identity-contract revision. Record doctrine change as identity-contract clarification/migration, not J-family semantic doctrine.

## Identity migration rule

Preserve all blocked historical identities.

Freeze v37 families `P3CAND-000283` through `P3CAND-000423` as blocked identities produced under the contradictory origin-key contract. They must not become current or promoted.

For each R35 family `P3CAND-000142` through `P3CAND-000282`:

1. compute the corrected release-neutral semantic origin key from the exact prior semantic topology;
2. compute the corrected key for the current R38 topology;
3. if the keys match one-to-one:
   - preserve the R35 family ID;
   - append an R38 successor revision;
   - record `IDENTITY_KEY_CORRECTION_NO_FAMILY_RENUMBER`;
4. if they differ materially:
   - allocate a new family;
   - begin at `R0001`;
   - record exact changed semantic element;
5. if corrected keys collide:
   - stop with the exact collision set and bounded migration blocker.

Do not allocate 141 new families solely because authority release IDs changed.

Add regressions proving:

- changing only release ID leaves the family semantic origin unchanged;
- changing a member, pair fact, endpoint, origin lane, or build-rule contract version changes it;
- concrete revision evidence hashes may change while family semantic origin remains stable;
- v37 blocked identities never become current.

## Historical import must use immutable prior artifacts

Production code currently reads:

```text
V36_HISTORICAL_IDENTITY_AND_SUCCESSOR_CONTRADICTION.csv
```

as its historical authority.

That file is a review regression, not a governing source.

Remove every review/audit CSV from production inputs.

For R35, read the exact values from immutable section-57 artifacts, including at minimum:

- `P3A_V35_CANDIDATE_IDENTITY_MIGRATION.csv`;
- `P3A_V35_ALL_CANDIDATE_HASH_RECONCILIATION.csv`;
- exact source artifact path and SHA-256.

For the R31 candidate namespace, perform a real recoverability inventory across immutable sections 53–56.

Do not blanket all 141 families/revisions as `IDENTITY_ONLY_NO_HASH_AUTHORITY`.

For each field record one of:

- exact value and exact source artifact;
- deterministically reconstructible value and reconstruction contract;
- explicit unknown with the searches performed and why authority is unavailable.

Never cite the section-59 review audit as the “exact prior artifact.”

The review CSVs supplied with this brief remain tests only. Deleting them must not change production output.

## Candidate evidence hash must be immutable at insertion

V37 currently:

1. inserts each candidate revision with a partial hash from `p3a_v37_load.py`;
2. runs `--finalize-hashes`;
3. updates `p3_candidate_revision.evidence_bundle_hash`.

That violates immutable revision semantics.

Create one shared canonical evidence builder that can operate on generated in-memory/staged rows before canonical revision insertion.

Allowed designs include:

- construct the complete candidate evidence surface in memory, compute the final hash, then insert the revision and all children in one transaction; or
- use explicit non-authoritative staging tables and promote once to the immutable revision surface.

Do not insert a canonical revision until its final evidence hash is known.

Add a database trigger preventing updates to:

- candidate family ID;
- revision number;
- origin key;
- evidence-bundle hash;
- allocation/authority release.

Remove the production `UPDATE p3_candidate_revision SET evidence_bundle_hash` path.

## Execute q01–q54 against R38

`p3a_v37_reports.py` currently parses:

```text
57/.../postgres/v35_populated_q01_q54_raw.tsv
```

and relabels that as `P3A_V37_QUERY_MATRIX.csv`.

This is not R37 validation.

For R38:

- execute the complete governing q01–q54 SQL against the final populated R38 database;
- capture raw stdout/stderr and SQLSTATE;
- classify the two future gates phase-aware;
- execute the five named diagnostics;
- generate the query matrix only from that run.

The verifier must confirm the raw execution identifies R38 objects and release.

## Make the release change ledger reproducible

V37 delivers 53,611 ledger rows, but no delivered production code inserts or derives them.

Create a deterministic ledger builder.

For every row, derive:

- current object ID;
- exact prior object/content hash when one exists;
- current content hash;
- change type;
- evidence-backed reason.

`UNCHANGED_REFERENCE` requires a matching prior identity/content basis. It may not have a blank prior hash merely because the object is historical.

The verifier must rebuild the ledger and compare exact rows.

## Correct the remaining pilot proxies

The following are still invalid:

- unresolved exact authority → `exact_only_authority`;
- other-domain redirect → `precedence_overlap_conflict`.

Set those strata to zero unless their named evidence exists.

For hierarchy, require an explicitly hierarchical directional relation such as governed `NESTED_TARGET_RELATION`; a generic coordinate relation is insufficient.

Preserve honest shortfalls. Do not substitute unrelated risk.

Seven packets may be a valid pilot result if only seven unique candidates satisfy actual named strata. The count is not the problem; semantic eligibility is.

## Fixture runner must fail at the named invariant

The fixture database isolation and nested stale-hash mutation are now useful.

But `run_case` still treats any exception as an expected negative result.

For every negative fixture specify:

- expected SQLSTATE;
- expected trigger/function or validator;
- expected error regex.

The incomplete-promotion fixture must first create every valid variant assignment and prerequisite, then fail specifically because promotion mapping is incomplete.

Add fixtures for:

- release-neutral family origin unchanged across release-only change;
- changed semantic origin requiring a new family;
- attempted candidate hash update;
- production dependency on a review CSV;
- relabelled old query output as current query evidence;
- release ledger row with no prior-content basis.

## Report builder and verifier must be portable and current

`p3a_v37_reports.py` hardcodes:

- the local workspace path;
- the DSN;
- stale F57/D57 findings.

Replace hardcoded values with command-line arguments.

Generate all reports from current R38 evidence.

The verifier must fail when:

- review CSVs are production inputs;
- origin keys churn on release-only changes;
- candidate hashes were updated after insertion;
- query evidence comes from another release;
- release ledger generation is absent;
- pilot proxy strata are used;
- a fixture fails at the wrong prerequisite.

## Checkpoint rule

Do not package after ordinary repairs.

Create v38 only when:

1. release-neutral family semantic identity is governed and migrated;
2. R35/R38 continuity is determined without release-induced churn;
3. historical sourcing is direct and truthful;
4. candidate hashes are final before insertion;
5. q01–q54 execute against R38;
6. the release change ledger is reproducible;
7. pilot eligibility uses named evidence only;
8. fixtures fail at named invariants;
9. the independent verifier derives PASS;
10. PostgreSQL and fixture teardown are proven.

Build only then:

```text
/Users/matthewsmith/Desktop/Rawlsing/rawlsing_p3a_v31_execution/build/Rawlsing_J_Family_Authority_Strategy_Handoff_v38_20260801.zip
```

No real canonical J-family authority may be authored, accepted, or promoted.

## Required section-60 return

At minimum include:

```text
WORKTREE_BASELINE.json
WORKTREE_STATE.json
EXACT_CONTINUATION.md
P3A_V38_IDENTITY_CONTRACT_REVISION.json
P3A_V38_PROJECTION_SEMANTIC_FINGERPRINTS.csv
P3A_V38_COMPONENT_SEMANTIC_FINGERPRINTS.csv
P3A_V38_FAMILY_SEMANTIC_ORIGIN_COMPARISON.csv
P3A_V38_BLOCKED_V37_IDENTITY_LEDGER.csv
P3A_V38_HISTORICAL_SOURCE_RECOVERABILITY.csv
P3A_V38_CANDIDATE_HASH_INSERTION_RETURN.json
P3A_V38_RELEASE_CHANGE_LEDGER.csv
P3A_V38_PILOT_STRATA_ELIGIBILITY.csv
P3A_V38_PILOT_PACKET_COVERAGE.csv
P3A_V38_FIXTURE_RETURN.json
P3A_V38_QUERY_MATRIX.csv
P3A_V38_OBJECT_COUNTS.json
P3A_V38_EXECUTION_FINDINGS.csv
P3A_V38_DOCTRINE_DELTAS.csv
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
