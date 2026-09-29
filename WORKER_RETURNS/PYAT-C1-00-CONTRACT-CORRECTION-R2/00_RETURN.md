# PYAT C1-00 — contract / oracle correction — R2 return

Status: `C1_00_R2_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`

Terminal: `C1_00_R2_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`

Assigned branch:
`agent/rabochii-pyat-hq126-c1-00-contract-correction-r2`

Commission tip:
`00b7091190505c0b41feaf0c45a29a791bab0cb5`

Exact base / original C1-00 return:
`df6f2d36e274744d217dc4a380c73e2c7e18e83f`

Independent review satisfied:
`8baa2e1e3a6f4f96311fbd660b65933fb4aff6c4`

Implementation baseline remains:
`b3b2fa13049513078c301a1f6574b661fcf390c5`

This is a bounded documentary correction only. C1-01 was not implemented or executed. No production code or existing production test was edited. Raw survey source reads: **0**. No real-source comparability, semantic, model, pooling or survey authority was created.

## 1. Five reviewer defects corrected

### A — condition/value relation

The weak co-custody witness is superseded by an exact value-bearing relation contract.

Frozen material:
`02_VALUE_RELATION_ORACLE.json`

It freezes:

- exact subject-condition preimages for POSITION=P1, POSITION=P2 and ANSWER=yes;
- exact normalized producer predicate-leaf preimages;
- exact fixture-only subject-preimage ↔ predicate-leaf pairing refs;
- `C1_CONDITION_VALUE_BINDING_WITNESS_SCHEMA@2`;
- exact source/release/time binding rules;
- exact fixture-only pairing AuthorityRef use;
- deterministic mismatch rejection before `PossibilitySliceEvidence` construction.

Mandatory hostile:

subject preimage POSITION=P1 + producer predicate POSITION==P2, with the same conditioner ID/source/release/target, yields:

`CONDITION_VALUE_RELATION_MISMATCH`

before slice construction and before the consumer call.

No real-source relation is inferred.

### B — complete synthetic authority material

Frozen material:
`03_SYNTHETIC_AUTHORITY_FREEZE.json`

The R1 tag-only freeze is replaced by complete canonical authority preimages for all C1-01 synthetic authorities.

Authority identity law:

`authority_content_hash = sha256(canonical_json(complete_frozen_authority_preimage))`

Exact source-free expected AuthorityRefs are frozen for:

- C1-AT07-SOURCE
- C1-AT07-ROUTING
- C1-AT07-COORDINATE
- C1-AT07-REPLAY
- C1-AT07-QUERY
- C1-AT07-COMPARABILITY
- C1-AT07-MODEL
- C1-AT07-WALKBACK

Changing scope, operations, model algorithm, pairing set or other frozen material under the same label changes identity and fails the oracle.

The three `FIXTURE_ONLY_*` consumer authorities are test-only exact `AuthorityRef` material, not new PRE553 production authority kinds.

### C — UNKNOWN preserved separately

Frozen material:
`05_STATE_AND_DETERMINANT_CLOSURE.json`

The corrected state law distinguishes:

- `UNKNOWN_CURRENTNESS` — existing B5 lifecycle owner;
- `NO_CURRENT`;
- `CONFLICTING_CURRENT_SELECTION`;
- `EXPLICIT_UNKNOWN_UNVISITED` — adaptive unvisited work;
- `UNRESOLVED`;
- `UNAVAILABLE`.

The existing B5 `UNKNOWN_CURRENTNESS` path is the lawful UNKNOWN witness. Nothing renames adaptive unvisited into generic unknown.

### D — exact consumer slice projection

Frozen material:
`04_SLICE_PROJECTION.json`

The only lawful C1-01 supported projection is:

`C1_POSSIBILITY_SLICE_PROJECTION@1`

schema hash:

`c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`

It freezes exact geometry keys/material, cell states, raw numerators, raw denominator, weighted numerator/denominator slots, exact-fraction encoding, target/domain identity, risk/member identity, measure identity and provenance.

`PossibilitySliceEvidence.raw_support` is now defined exactly as:

`EmpiricalFact.raw_denominator_support`

—not resolved-target support and not one cell numerator.

AT07 supported geometry remains:

- forward P1: denominator 60, yes 54/60 = 9/10, no 6/60 = 1/10;
- reverse yes: denominator 62, P1 54/62 = 27/31, P2 8/62 = 4/31.

### E — determinant / replay / invalidation closure

Frozen material:
`05_STATE_AND_DETERMINANT_CLOSURE.json`

Direct composition determinants now include:

- condition-value witness ref/hash;
- subject-condition preimage refs;
- producer predicate-leaf refs/projections;
- pairing ground-truth refs;
- pairing/comparability AuthorityRefs;
- exact risk and denominator member refs;
- measure kind and basis;
- target topology/domain material;
- exact constructed slice evidence ref;
- slice-projection schema hash.

These inputs are also required by composed identity and full fresh-process recomputation.

Mandatory relation-only mutation oracle:

with producer counts/query/source/risk/measure/target/model fixed, mutate only the exact condition-value relation/witness determinant. The direct composed result must reidentify. If the family is already lifecycle-governed, existing B5 determinant edges invalidate/reidentify all and only dependent releases; unrelated releases remain usable.

## 2. Already-approved C1-00 holdings preserved

R2 does not weaken:

- exact source universe + release identity;
- target topology/domain/component identity;
- risk/eligibility/denominator/member identity;
- RAW versus governed-weighted measure/design/estimand identity;
- recursive immediate-parent ancestry;
- positive recursive handoff versus full discovery coverage;
- replay-grade separation;
- direct versus learned/adjudicated anti-bypass law;
- AT07 arithmetic: forward 54/60, reverse 54/62;
- narrow future C1-01 write allowlist.

The scalar direct C1-01 grain is not broadened.

## 3. Exact updated prior C1-00 artifact blobs

The following prior C1-00 artifacts were modified by R2:

| artifact | R2 blob |
|---|---|
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md` | `341175f9861a6a1e512e41a589830ce44f808640` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json` | `078cd1e1f7edcdd3adc1880eee501a60deeabc7c` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/producer_consumer_trace.json` | `8a41f4e5bef9140e1b2a668474f512232a964340` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_products.json` | `4f8fa4595e3e515fb25c2c05ca7afed9a515c420` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/hostile_case_receipts.json` | `4f4b7171bd713f9e5fcc8962edb1a5bc0f3a3b27` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/replay_and_dependency_receipt.json` | `6083909bd8c20af73445097109a20b6b34fc13e0` |
| `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json` | `0175f871ba848372e06d050cb104925c30d3cbe9` |

`family_binding_manifest.json` was not modified because its direct-versus-learned/adjudicated law was already independently accepted.

## 4. R2 correction artifact blobs before this return file

| artifact | blob |
|---|---|
| `01_CORRECTION_MATRIX.json` | `55fa6dfbb763b66203e0f7d5cbfa23a734c991ab` |
| `02_VALUE_RELATION_ORACLE.json` | `bacda45e651d8c3ed73bb73b0169d0ed2ddefd53` |
| `03_SYNTHETIC_AUTHORITY_FREEZE.json` | `333989fa7b57c221d6aa5ebfc25d9d76e0acad32` |
| `04_SLICE_PROJECTION.json` | `8e5bd3d23db1e39aebee0a55d49934a0d400dd48` |
| `05_STATE_AND_DETERMINANT_CLOSURE.json` | `96b260781ddfa5374c34afa7433fefd1be5502f7` |

## 5. Proof / execution grade

Proof grade:

`STATIC_INSPECTION + DETERMINISTIC DOCUMENTARY HASH/ORACLE FREEZE`

No source-free C1 implementation was executed because the commission is documentary only.

No C1-01 success is claimed.

No real-source success is claimed.

No review self-approval is claimed.

## 6. Required rereview attacks

Independent rereview should attack at minimum:

1. frozen P1 subject preimage paired to P2 producer leaf;
2. same conditioner ID with distinct exact values;
3. changed synthetic authority scope/operation under unchanged label;
4. same visible ratio with different denominator-member refs;
5. RAW versus governed-weighted numerical equality;
6. `UNKNOWN_CURRENTNESS` versus adaptive `EXPLICIT_UNKNOWN_UNVISITED` versus `UNRESOLVED`;
7. alternate `geometry` encoding or `raw_support` meaning;
8. relation/witness-only determinant mutation;
9. replay that omits relation/preimage inputs but claims full composition recomputation.

Requested next action:

`INDEPENDENT_REREVIEW_OF_EXACT_R2_BRANCH_TIP_ONLY`

C1-01 must not begin until that rereview accepts this corrected packet.

`C1_00_R2_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`
