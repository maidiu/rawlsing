# AS3R3 Node 5A — Predicate Mint + Fresh Replay

Status: `BLOCKED__CANONICAL_SUCCESSOR_IDENTITY_COLLISION__HQ_ADJUDICATION_REQUIRED`

Repository: `maidiu/rawlsing`  
Worker branch: `as3r3-node5a-predicate-mint-replay-20260828`  
Exact starting HEAD: `88896314104b8387a613aefd04f61f0606578f8c`

## Holding

Node 5A fails closed before the authorized success disposition.

Exactly 19 frozen Node 4A predicate input records were consumed without alteration. All 19 pass the accepted frozen producer predicate validator and all 19 mechanical `construct_successor_predicate(...)` invocations are deterministic. However, the accepted Node 4A semantic mapping causes two distinct AS3 semantic source IDs to collapse to one canonical successor `EmpiricalPredicate@1.0.0` identity:

- `A000` — baseline risk cohort, mapped by accepted Node 4A law to the q301_2 `ELIGIBLE_APPLICABLE` routing leaf;
- `A1RAPP` — q301_2 `ELIGIBLE_APPLICABLE` routing-applicability atom.

Their complete producer inputs differ only in AS3 source/derivation wrapper material that the accepted producer validates but does not place into the canonical `EmpiricalPredicate` semantic projection. Their canonical predicate construction material is therefore identical, producing the same ExactRef.

This yields:

- frozen AS3 predicate source records consumed: **19**;
- mechanical constructor invocations: **19**;
- source-ID → successor-ExactRef mapping rows: **19**;
- distinct canonical successor predicate ExactRefs: **18**;
- collision classes: **1** (`A000`, `A1RAPP`).

## Why this is blocking

Authority 28 explicitly expects a successor executable layer containing **19 predicate runtime refs**, and the Node 5A command requires construction of exactly 19 successor predicates and fail-closed behavior on any identity/count mismatch. Node 5A has no authority to mutate the producer/schema, alter the frozen Node 4A mapping, inject AS3 source IDs into runtime identity merely to force uniqueness, or reinterpret the frozen semantic terrain.

The worker therefore does **not** emit the success token and does **not** authorize Node 4B.

## Replay finding

Fresh reconstruction is deterministic at the exact observed ceiling: the same 19 frozen inputs reproduce the same 19 source→ExactRef mappings, including the same `A000 == A1RAPP` collision. Determinism does not cure the cardinality/identity contradiction.

## Prohibitions preserved

No query input was frozen. No successor query was minted. No DiscoveryAuthority/frontier object was created. No LiTS-I or I05 execution occurred. No producer/schema/AS3R2/AS4I0/candidate/A-B-C semantic mutation occurred.

## Required HQ adjudication

HQ must reconcile the contradiction between:

1. the accepted 19-row AS3 semantic predicate terrain / Node 4A mapping in which `A000` is deliberately realized as the q301_2 routing-applicability leaf; and
2. Authority 28 / Node 5A's expectation of 19 successor runtime predicate identities.

Lawful options are outside this worker's authority. This return only establishes the collision and stops.

Terminal marker:

`AS3R3_NODE5A_BLOCKED__A000_A1RAPP_CANONICAL_IDENTITY_COLLISION__18_DISTINCT_SUCCESSOR_REFS_FROM_19_FROZEN_INPUTS__HQ_ADJUDICATION_REQUIRED`
