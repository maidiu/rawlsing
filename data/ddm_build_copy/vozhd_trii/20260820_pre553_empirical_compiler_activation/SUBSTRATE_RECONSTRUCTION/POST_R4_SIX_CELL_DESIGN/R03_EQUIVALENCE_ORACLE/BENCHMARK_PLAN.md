# R03 ACCEPTANCE / RESOURCE EXECUTION PLAN

Status: `PLAN_ONLY__CORRECTNESS_PRECEDES_RESOURCE`

This is not a performance contest between carrier designs. It defines the bounded execution shape HQ can use to estimate the cost of running the representation-neutral oracle after a candidate exists.

## Phase A — static authority and bundle validation

Inputs:
- exact source manifest;
- source-family hostile evidence;
- C11/I03/I05/I04 contract pins;
- candidate commit/build identity;
- tuning disclosure;
- candidate cache declaration.

Checks:
- immutable identities close;
- required source families present;
- required M01-M18 matrix complete;
- no forbidden mutable selector;
- blind-workload seed inputs recorded.

Expected cost: negligible relative to source scan.

## Phase B — source-native physical certification

Run exact source identity/shape/physical witnesses for every source in the candidate's claimed scope.

Minimum CLOSED_35 full-run accounting target from accepted census evidence:
- 35 source snapshots;
- 486,174,936 physical cells;
- 326,652,033 ordinary cells;
- 112,031,914 system-missing cells;
- 47,490,989 SPSS user-missing cells;
- 18 native SPSS MR sets in exactly 3 sources.

These counts are *census expectations*, not substitutes for cell/source equivalence.

Record:
- wall time;
- peak RSS;
- source-by-source throughput;
- physical witness digest;
- failure/block state.

No threshold is an acceptance criterion.

## Phase C — C11 semantic inventory

For each sealed candidate release:
- enumerate canonical public objects;
- enumerate internal C11 records;
- recompute every semantic hash/ExactRef;
- compare full expected/observed ref multisets;
- validate M01-M18 coverage;
- validate release/replay closure.

Record:
- objects/records scanned;
- hash verification time;
- peak RSS;
- semantic release digest.

Target resource property: the oracle implementation itself should be streaming/bounded where possible, but an oracle resource problem may never weaken equality.

## Phase D — I03 regression + property corpus

Run:
1. hand-anchored positive/negative cases;
2. generated typed-state/topology/routing/weight/source-relation cases;
3. independent set/incidence evaluation;
4. frozen I03 execution.

Require exact agreement.

Record by query:
- source scope;
- predicate arity;
- target arity;
- denominator size;
- fact state;
- candidate result digest;
- independent reference digest;
- frozen I03 digest;
- time/RSS.

## Phase E — I05 declared + blind frontier

### E1 declared regression frontier

Cover every applicable frozen I05 candidate family.

### E2 blind frontier

After candidate/tuning disclosure freeze:
- record nonce;
- compile frontier;
- verify no selected workload hash appears in disclosure;
- require pair, k-way, conditional, reversal, recursive, branch and co-signature/cloud-like coverage;
- evaluate every candidate;
- seal coverage receipt.

Record:
- candidate_count;
- covered_candidate_count;
- family counts;
- fact/receipt digests;
- wall/RSS;
- no-pruning proof.

Correctness requirement: candidate_count == covered_candidate_count for exact-bounded coverage.

## Phase F — I04 admission

Run positive and each nonpositive class plus multi-blocker precedence cases.

Record exact receipt digests and projection permission.

## Phase G — fresh-process replay

At least three clean runs:
- Run 1: baseline environment, caches present if normally built.
- Run 2: different PYTHONHASHSEED, caches deleted, permuted irrelevant enumeration.
- Run 3: different lawful worker count and fresh cache rebuild.

Require identical canonical outputs.

## Phase H — corruption / partial publication

Use copies of the candidate release or dedicated fault-injection hooks. Never damage source authority.

Inject:
- one authoritative byte flip;
- one member removal;
- one member truncation;
- one stale content hash/ref;
- one authority hash mismatch;
- one pre-seal partial release.

Each case must fail before semantic truth is returned.

## Phase I — stale-cache challenge

Copy a cache/index from a different exact release into the candidate cache location. Required behavior:
- reject and rebuild, or
- reject use and proceed without it.

Returning stale semantic truth is failure.

## Comparison outputs

The resource report may compare:
- source certification throughput;
- semantic inventory throughput;
- I03 latency;
- exact I05 frontier throughput;
- peak RSS;
- cache rebuild cost;
- fresh-process variance.

It may not compare “pass percentages.” Semantic acceptance is conjunctive, not scored.

## Stop rule

Stop on the first hard semantic/integrity mismatch only if the goal is candidate rejection. For a diagnostic synthesis run, continue and enumerate all failures, but the acceptance state remains failed after the first authoritative mismatch.
