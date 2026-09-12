# W2-D03 — Governed Return R1

## Terminal

`W2_D03_PREV3_OBJECTIVE_POSITION_PRODUCER_OWNERSHIP_AND_MATERIALIZER_CONTRACT_R1__PASS__GATE_POSITION_PRODUCTION`

Result: **PASS**

Exact grain executed:

`PREV3_OBJECTIVE_POSITION_PRODUCER_OWNERSHIP_AND_MATERIALIZER_CONTRACT_R1_ONLY`

Worker branch:

`agent/rabochii-prev3-w2-d03-objective-position-owner-r1`

Commission tip verified at execution start:

`2074f0ca2292a4b77195130a2a7c993446c14489`

Frozen branch parent:

`107fb80308dafb6dc2e9ba1dd15b8b2d9e7ac2d2`

Pre-return-write branch head after the three subordinate artifacts were finalized:

`797be02f54686d456f8f03bb7dd190009aaed0a5`

Library requirement: `NO`. No supplied academic/library source was consumed.

Production-code scope: `NONE_GRANTED__NONE_MODIFIED`.

## PASS holding

D03 allocates the objective-position production jurisdiction without creating a universal position ontology.

The lawful production model is:

```text
EXACT COMPETENT OBJECTIVE-DOMAIN SEMANTIC OWNER
        +
EXACT HQ/DOMAIN PRODUCER DELEGATION
        +
EXACT DESIGNATED PRE-V3 OBJECTIVE-POSITION MATERIALIZER
        +
EXACT SOURCE/CLAIM/EVIDENCE
        +
EXACT APPLICABILITY/PERMISSION
        +
EXACT VALID-TIME/CURRENTNESS
        +
EXACT PROVENANCE/DEPENDENCY/REPLAY
        =
CONTENT-ADDRESSED OBJECTIVE POSITION FACT
```

The materializer is mechanical and fail-closed. It may emit `PREV3_OBJECTIVE_POSITION_FACT@1.0.0` only from the complete authorized tuple. It cannot infer position truth from demographics, coordinates, clusters, labels, favorable outcomes, downstream need, a V3 subject/person receipt, or a V3 runtime cursor.

This closes the **GAP-PREV3-014 owner-allocation/materializer-contract predecessor** at candidate-return grain. It does not self-adopt authority and does not close GAP-PREV3-015 implementation/population.

## Current authority consumed

1. HQ second-wave fan-in/dispatch at the D03 commissioned tip:
   `HQ_ADOPTED__FIRST_WAVE_FANIN_COMPLETE__SECOND_WAVE_CONSTRUCTION_AUTHORIZED`.
2. Adopted C04 return at `ae5666fa461f8baaa017fd0b4eff1d9ecfc1c0e5`, especially:
   - C04-SO-002 `OBJECTIVE_POSITION_FACT_MATERIALIZATION`;
   - C04-SO-003 `ATOMIC_STRUCTURAL_CHANNEL_ROUTE`;
   - C04-SO-007 `OBJECTIVE_CONSTRAINT_OR_OPPORTUNITY_PREREQUISITE`.
3. Adopted C02 world-root contract at `7a3def9262da5891f86f5e4f00384c07902e77b9`, preserving:
   `WORLD_ROOT_OWNER != OBJECTIVE_POSITION_PRODUCER`.
4. Field Forge OBL005 HQ adoption at `b3012b346b8dbb1569a77d998310e16f28cebf6c`:
   `FIELD_FORGE_OBL005_CLAIM_BOUNDED_POSITION_ROLE_AUTHORITY_AND_EVIDENCE_CONTRACT@1.0.0`.
5. Existing exact M2/V555 route runtime at semantic floor `3468673673db2f3de804d6e825585f86ff98e870`, whose F1 closure consumes exact source/receiving structural-position refs.
6. Existing source-backed positioned-subject possibility machinery only as a bounded downstream/query precedent; it remains:
   `PROXY != EXACT FACT != ACTOR BELIEF` and is not promoted into a generic position-world owner.

## Ownership disposition

The returned owner map separates nine roles:

- objective-position semantic owner;
- producer-authority owner;
- designated objective-position materializer;
- source/claim evidence owner;
- OBL005/domain-equivalent role-adjudication owner where applicable;
- objective valid-time/currentness owner;
- world-root owner;
- M2/Field Forge downstream consumer;
- V3 person owner.

The decisive allocation is that a positive fact may be minted only by an **exact designated PRE-V3 objective-position producer** under an exact producer authority whose scope covers that fact class/domain/claim/use/time grain. Sub-Vozhd II coordinates the implementation lane but does not become a universal semantic authority.

## Contract freeze

Candidate contract:

`PREV3_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT@1.0.0`

Positive fact schema:

`PREV3_OBJECTIVE_POSITION_FACT@1.0.0`

Positive state:

`POSITION_FACT_AUTHORIZED`

Identity:

`PREV3POS:<semantic_hash(canonical_fact_material)>`

The canonical material binds implementation/hash identity; producer and semantic authority; entity/actor and position/role identity; source universe/release/claim/evidence; role-adjudication/result-independence evidence where applicable; applicability; permission and negative ceiling; valid-time/currentness; provenance/dependencies/replay; and optional predecessor identity.

Typed nonpositive/negative states include explicit-negative-only-with-authority, `UNAVAILABLE`, `VALID_EMPTY`, missing producer/semantic/role/source/time authority, unresolved identity/applicability/currentness, `USE_DENIED`, stale/historical-noncurrent, `NONCOMPARABLE`, `OUT_OF_SCOPE`, and `INTEGRITY_FAILURE`.

Failed positive proof never becomes a negative objective fact.

## Downstream binding

For C04-SO-003, the resulting exact fact ref may be used as M2:

- `source_structural_position_ref`, or
- `receiving_structural_position_ref`

only when M2's own exact route/shape/F1-closure/use authority accepts it. D03 does not bypass M2.

For C04-SO-007, the ref may support separately authorized objective constraint/opportunity derivation, but never actor uptake, interpretation, belief, preference, knowledge, response or development.

The world root may publish/index/resolve an already-authorized position fact. It may not repair a missing producer, semantic owner, source, time or currentness authority.

## Deterministic static qualification

Static return checks: **PASS**.

- owner-map JSON parsed successfully;
- exactly 26 source/materializer input requirement rows are present;
- the contract carries implementation/hash replay identity;
- explicit negative, unavailable and noncomparable states are distinct;
- world-root and V3 bootstrap prohibitions are explicit;
- M2 source/receiver exact-ref handoff fields are explicit;
- no production module or test file was modified.

## Governed artifact identities

| Artifact | SHA-256 | Git blob SHA |
|---|---|---|
| `01_POSITION_PRODUCER_OWNER_MAP.json` | `00e98f6e40c53df647c0cf943e0c6eb900eed248c9256bab62af572696ae0ec3` | `acc940e64d1842771b939338ba3035f9a8ab5df0` |
| `02_OBJECTIVE_POSITION_MATERIALIZER_CONTRACT.md` | `eafc93c273ab60dc44d7ca916baf3f144098eee67ebb3c013787d63ec18a163a` | `eb5acb8f8c8e709c00a8bd86c6c605a00ba457ba` |
| `03_REAL_SOURCE_POSITION_INPUT_REQUIREMENTS.tsv` | `25efeacf53049d85343bbf5d212781e7debd321a69d7231bad3c69f1b7bc00a3` | `30d13a02068466a115cadca344666878d7b36a04` |

`00_RETURN.md` is intentionally not self-hashed in its own body; its exact SHA-256 and Git blob identity are reported with the final branch tip to HQ.

## Bounded implementation successor candidate

`PREV3_OBJECTIVE_POSITION_MATERIALIZER_IMPLEMENTATION_AND_REAL_SOURCE_POPULATION_R1_ONLY`

Minimum successor proof:

- competent adoption/narrowing of this D03 contract;
- exact implementation/hash binding;
- at least one real source-backed positive objective position row;
- explicit negative/unavailable/noncomparable controls;
- deterministic replay;
- currentness/invalidation/successor behavior;
- exact M2/Field Forge consumer handoff;
- independent qualification;
- zero person-state or V3 bootstrap leakage.

This successor remains bounded by row-specific objective-domain/source authority. It does not authorize a universal classifier.

## Successor gate

`GATE-POSITION-PRODUCTION`

## Terminal

`W2_D03_PREV3_OBJECTIVE_POSITION_PRODUCER_OWNERSHIP_AND_MATERIALIZER_CONTRACT_R1__PASS__GATE_POSITION_PRODUCTION`
