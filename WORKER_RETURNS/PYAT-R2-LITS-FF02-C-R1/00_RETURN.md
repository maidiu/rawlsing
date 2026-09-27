# PYAT R2 / FF02-C — FINAL LiTS CANONICAL EMPIRICAL PREIMAGE → 50-CANDIDATE STRUCTURAL-USE CROSSWALK — R1

## Terminal

`PYAT_R2_LITS_FF02_C_BLOCKED__FINAL_CANONICAL_PREIMAGE_CLOSURE_GAP_PROVED__NO_SOURCE_REOPEN`

## Exact identity

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-pyat-r2-lits-final-preimage-crosswalk-r1`
- exact live `integration/pre-main-reconciliation-r1` base: `bc207de1db6c1e48b81c7b27b2633ad1177077ff`
- binding final canonical empirical closure: `f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415`
- checkpoint identity: `3fab15f37db629f0ee24189620c65eff944d8a36c4b4509abb6b8bb2ea69c33f`
- checkpoint document SHA-256: `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`
- checkpoint bytes: `3404445161`
- current frozen oracle: `e5d66db4b6f8339672b0f4828b72a8df68b5525bf71ecfda899d0531d618a98a`
- D04-R2 historical comparison commit: `e631de162c582423639b7067a4f36b29f8aa4d89`
- FF01 historical comparison commit: `d60c2a0218c39b35d28f163b969e1784ff0af31e`

No raw LiTS bytes were accessed, no source was decoded, no I03/I05 source execution occurred, no FIABC/Candidate A/B/C state was consulted, and no production/semantic authority was mutated.

## Holding

The **final retained empirical closure itself is complete and green**. This return is blocked only because the commission requires a per-candidate/per-object exact-preimage crosswalk while this Browser/GitHub-only lane is forbidden from reading the durable local checkpoint that contains those full preimages.

The Git-banked control plane proves:

- canonical inventory = 1 EmpiricalUniverse, 24 AuthoritySnapshot, 35 EmpiricalPredicate, 63 EmpiricalQuerySpec, 60 EmpiricalFact, 1 DiscoveryAuthority, 50 DiscoveryResultReceipt;
- 50 candidates / 77 executed roles;
- 49 `DISCOVERED_RESULT_SUPPORTED`;
- 1 `VALID_EMPTY`;
- all 60 fact/query/predicate bindings close in the final checkpoint validator;
- all object authority refs resolve to retained exact snapshots;
- structural-admission object count = 0;
- replay/release provenance and zero-source resume PASS;
- candidate A/B/C process/output/state use = zero.

The Git-banked `current_standard_lits_oracle.json` is sufficient to enumerate exact current candidate hashes, candidate IDs, rules/families, all 77 query/predicate refs, all supporting fact refs, exact risk/universe/measure refs, denominators, typed terminals, and each candidate replay ref. Those are banked in the 50-row and 77-role ledgers here.

It is **not** sufficient to lawfully enumerate:

1. each candidate's exact `DiscoveryResultReceipt.ref`;
2. each object's exact `authority_snapshot_refs` and the complete 24-snapshot authority preimage set;
3. the individual P2 historical logical-member → current candidate mapping without the current CONDITION predicate preimage or the precomputed logical binding row.

Those fields are present in the retained checkpoint canonical preimage packet and were validated there. They were not exported into the Git-banked evidence/control plane. The standard oracle exposes an unordered pool of 50 `DiscoveryResultReceipt@1.0.0` exact refs, but no lawful candidate→receipt pairing. It exposes 12 AuthoritySnapshot refs in the standardized oracle closure while the final canonical retained closure contains 24 snapshots.

## Critical checks

| check | disposition |
|---|---|
| 1. 50 candidates each have a retained discovery receipt | **PASS existence / BLOCKED per-candidate exact-ref enumeration** |
| 2. 77 roles close over retained query/predicate preimages | **PASS final checkpoint validation; exact refs banked** |
| 3. 60 facts close over retained exact refs | **PASS 60/60; exact fact/query/predicate refs banked** |
| 4. every authority ref resolves to retained snapshot | **PASS global validation / BLOCKED per-object authority enumeration** |
| 5. single valid-empty remains identifiable/nonpositive | **PASS** — current candidate `a3dfb9c641e8efc16bdcdbcd5e6d1635a7446f3ff3c2f6ed53defba4b70e7eb4`, lane P3, `VALID_EMPTY` |
| 6. no structural-admission object hidden in closure | **PASS**, count 0 |
| 7. replay/release provenance closes source-free | **PASS** |
| 8. no candidate requires A/B/C-owned state | **PASS** |
| 9. no historical D04 field is canonical source of truth | **PASS**; ASTRA projection role is `OPTIONAL_HISTORICAL_REGRESSION__NOT_CANONICAL_CURRENT_STORAGE` |

Because checks 1 and 4 cannot be emitted at the exact per-object grain required by the commission from the allowed Git-only evidence surface, this lane stops at that exact grain.

## D04 / FF01 historical comparison

Accepted parity explicitly separates native identity domains:

- historical: `G02_EXECUTION_CANDIDATE_HASH`
- current: `PRE553_I05_CANDIDATE_HASH`
- native hash equality required: `false`

All P0–P4 parity sections PASS. Therefore D04 P0–P4 are classified here as:

`LOSSLESS_HISTORICAL_PROJECTION_OF_CURRENT_OBJECTS`

at the accepted cross-schema logical empirical grain, **not** `EXACT_CURRENT_PREIMAGE_EQUIVALENT`.

ASTRA-FF01's old structural-ingress disposition is classified:

`HISTORICAL_SUMMARY_ONLY__DO_NOT_USE_AS_CURRENT_AUTHORITY`

It does not override the final current closure or current Field Forge authority.

For P2 specifically, the accepted parity court proves 18 historical/current logical keys coincide, but the Git-banked final compact row does not expose the q301_2/q310/q311 logical binding. This worker refuses to recover it from empirical counts. The exact current predicate preimage or precomputed logical binding must be exported from the retained checkpoint/runtime materializer.

## Smallest lawful repair

**Do not reopen LiTS source. Do not rerun I03/I05.**

Run one checkpoint-only metadata extraction against the already retained checkpoint and bank a compact Git artifact containing:

- 50 rows: `candidate_hash -> DiscoveryResultReceipt.ref`;
- each receipt's `authority_snapshot_refs`, `dependency_refs`, `winning_predicate_ref`, `source_release_refs`, replay ref;
- all 24 retained AuthoritySnapshot exact refs plus their AuthorityRef triples;
- per-object authority snapshot refs for the 60 facts / 63 queries / 35 predicates / 50 receipts;
- the already-qualified 50 `cross_schema_logical_candidate_bindings` rows, or enough retained predicate preimages to reproduce them source-free.

The extraction needs only the already-retained checkpoint slice:

`current_i05_materialization_checkpoint_v3.json#/material/canonical_empirical_object_closure`

with its `public_object_preimages` + `preimage_fragments`. The checkpoint is content-addressed by `2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726`. It does not require raw source, a decoder, I03, I05, or A/B/C.

## Banked return files

- `00_RETURN.md`
- `01_50_CANDIDATE_FINAL_PREIMAGE_CROSSWALK.tsv`
- `02_77_ROLE_CLOSURE_LEDGER.tsv`
- `03_EMPIRICAL_FACT_EXACT_REF_CLOSURE_LEDGER.tsv`
- `04_AUTHORITY_RESOLUTION_CLOSURE_LEDGER.tsv`
- `05_D04_P0_P4_HISTORICAL_CURRENT_CROSSWALK.tsv`
- `06_VALID_EMPTY_PRESERVATION_RECEIPT.json`
- `07_STRUCTURAL_ADMISSION_ABSENCE_RECEIPT.json`
- `08_REPLAY_PROVENANCE_CLOSURE_RECEIPT.json`
- `09_EXACT_BLOCKER_INVENTORY.tsv`

## Terminal

`PYAT_R2_LITS_FF02_C_BLOCKED__FINAL_CANONICAL_PREIMAGE_CLOSURE_GAP_PROVED__NO_SOURCE_REOPEN`
