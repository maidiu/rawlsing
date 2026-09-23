# FIABC LiTS INTEGRATED PRE-ORACLE INDEPENDENT ACCEPTANCE AUDIT — R1

## Holding

**BLOCKED — source-free pre-oracle closure is not yet adoptable.**

Exact blocker:

`BLOCKED__ASTRA_G02_CANDIDATE_HASH_DOMAIN_IS_NOT_CURRENT_PRE553_CANDIDATE_HASH_DOMAIN__NO_EXPLICIT_CROSS_SCHEMA_LOGICAL_CANDIDATE_NORMALIZATION__P2_PARAMETER_AND_CONDITION_BASELINE_IDENTITIES_NOT_CONSERVED`

This audit does **not** accept the integrator's PASS terminal as proof. Courts 1–4 and 6–11 independently pass. Court 5 / Court 8 exposes one concrete pre-oracle source-free defect in the integrated parity law.

## Subject

Repository: `maidiu/rawlsing`

Integrated subject branch:

`agent/vozhd-premain-fiabc-lits-preoracle-integrated-closure-r1`

Audited final tip:

`56d33a910ccf0df3c50f7bb053dbab57cad5b271`

Qualified implementation tree:

`516643348181048381ebe732ac8ea748d9a82fd7`

Audit branch:

`agent/rabochii-premain-fiabc-lits-integrated-preoracle-acceptance-audit-r1`

Audit base:

`56d33a910ccf0df3c50f7bb053dbab57cad5b271`

## What independently passes

- Worker A jurisdiction law is retained in ancestry and in the live execution chain.
- Worker B's substantive normalizer/comparator is present, with all Worker-B functions retained; the integrated tree adds the F02 selector-population court rather than replacing Worker-B law.
- Worker C's stale WVS packaging defect is repaired.
- Qualified→final integrated commits are return/documentation only.
- Temporary CI court-spec/workflow mutations are absent from the qualified/final tree.
- governed P2X remains frozen at `78caf7eb4396dd576cf478c860372b7e26455cd9`.
- immutable ASTRA expected inputs are exact-commit/exact-blob pinned.
- current empirical normalization happens from the retained current I05 result before oracle freeze.
- current q310/q311 substrate is scanned from the same already-decoded current incidence through frozen R5B/F02 code.
- F02 historical/current roots are in the same actual canonical hash domain, not merely prose-asserted.
- P0/P1/P2/P3/P4 empirical quantities, risk topology, selector substrate, and 49/1 terminal envelope are otherwise strongly checked.
- parity and selector failures prevent `build_lits_i_oracle()`.
- WVS7 successor truth and packaging pins are current and uncontaminated by LiTS successor authority.
- focused CI run `35826661112` / job `107069779873`: 20 protocol tests + 80 governed tests pass.
- broad CI run `35826798791` / job `107070206829`: 20 protocol tests + 309 tests / 28 subtests pass.

## Blocking defect

Accepted ASTRA-D04-R2 records 25 candidate hashes across P0/P1/P2/P3. Independent comparison against the accepted G02 terminal ledger proves **all 25 are historical G02 `execution_candidate_hash` values**.

Historical G02 producer blob:

`7a9b8b53e36041b453eb62e7a22a52ff0d392c16`

Historical G02 hash material is:

```
{
  "contract": PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_REAL_EXECUTION_AND_REPLAY_R2@1.0.0,
  "d02_frontier_blob": ...,
  "f02_frontier_readoption_hash": ...,
  "candidate_semantics": {
      lane, rule_id, family, form, parameters, validation, query_roles, ...
  }
}
```

Current PRE553 `_candidate()`, exact code blob:

`ee0544115feb9d76c8c68b9dd773302c8fa8bb48`

hashes a different material:

```
{
  "contract": PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0,
  "family": ...,
  "rule_id": ...,
  "winning_predicate_ref": ...,
  "query_roles": [{"role", "predicate_ref", "query_ref"}, ...],
  "validation": ...,
  "ancestry_refs": ...
}
```

Those are different identity domains. The integrated comparator nevertheless puts ASTRA's historical hashes and current PRE553 hashes into the same `candidate_hash` field and exact-compares them, including `frontier.recorded_candidate_hashes`.

That equality is not authorized by common canonical construction.

The source-free tests mask this: their synthetic “current” receipts are directly injected with the historical ASTRA hashes rather than compiling the current PRE553 frontier and proving a logical cross-schema identity map.

## P2-specific consequence

ASTRA's immutable P2 rows explicitly contain all 18 parameter triples:

`{q301_2, q310, q311}`

plus the first exact difference witness.

The accepted-side normalizer drops `parameters`.

The current-side normalizer keeps only:

- current `candidate_hash`;
- terminal state;
- first difference witness.

Although the real current receipt carries exact CONDITION/BASELINE query-role predicate/query refs, the normalizer drops those refs too. Therefore it does not explicitly conserve:

- historical P2 parameter identity;
- current CONDITION semantic identity;
- current BASELINE semantic identity;
- the cross-schema mapping among those identities.

This violates the commissioned P2 acceptance law independently of terminal support and witness equality.

## Smallest lawful repair

Do **not** reintroduce whole-object hash equality and do **not** attempt to make G02 and PRE553 candidate hashes equal.

Add an explicit deterministic logical candidate-identity normalization derived from immutable workload authority on the historical side and the current compiled candidate semantics on the current side.

For P2 the normalized key must at minimum bind:

- lane/rule;
- exact `q301_2/q310/q311` parameter tuple;
- exact CONDITION semantic identity;
- exact BASELINE semantic identity;
- target/query semantics necessary to prove that both schemas describe the same logical role.

Then compare the empirical witness under that common logical key.

Hostile tests must mutate parameter/condition/baseline identity while holding the witness, terminal state, 50/77, 49/1, risk roots, and selector substrate fixed and require failure.

## Boundary audit

- raw survey files opened/materialized by this audit: **false**
- source-backed LiTS run: **false**
- real-source I05 run: **false**
- Candidate A/B/C run: **false**
- measured P2X run: **false**
- P3 run: **false**
- architecture selection: **false**
- governed execution branch mutation: **false**
- production code changed by this audit: **false**
- user Mac used: **false**

## Terminal

`PREMAIN_FIABC_LITS_INTEGRATED_PREORACLE_ACCEPTANCE_AUDIT_R1__BLOCKED__CROSS_SCHEMA_CANDIDATE_IDENTITY_NORMALIZATION_REQUIRED__P2_PARAMETER_CONDITION_BASELINE_IDENTITY_CONSERVATION_REQUIRED__SOURCE_FREE_BLOCKER__NO_CANDIDATES_RUN`
