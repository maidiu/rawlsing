# Sorok read-only opportunity contract — two TEST_ONLY epochs and a future N8E→N9 context adapter; no actor

**Status:** `TEST_ONLY_READONLY_CONTRACT_CANDIDATE__NO_SOROK_ACTOR__N8E_NOT_INSTALLED`
**Role limit:** this document is a contract candidate written by a bounded Pyat worker. It issues no Sorok actor, memory, genealogy, thought, action, personality, V3 or CAN008 authority, and no N9/OC05 installation.

## 1. What the read-only client may read from this return

Source product: `03_WORLD_TWO_EPOCH_CONSUMER_DELTA.json` (cold SHA-256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`).

A read-only client may dereference, by exact receipt hash only:

- `epochs.E1_EARLY_2026` and `epochs.E2_LATE_2027` — the actor-free consumer views;
- `epoch_receipts.E1_EARLY_2026` and `epoch_receipts.E2_LATE_2027` — the actual N9-shaped selected-world receipts;
- `consumer_delta` — the formal-eligibility / material-constraint / practical-opportunity comparison;
- `timeline_interventions`, `formal_eligibility_isolation`, `source_versus_rule_matrix`, `revocation`, `mismatch`;
- `n8e_input` — only to read that N8E is `ABSENT_HOLD`; it is not an input to either world.

**Permitted operations:** read exact values; compare the two epochs; retain the receipt hash; request a `historical_receipt` for an already-issued receipt (archival only, no fresh authorization); replay the cold product in a fresh process.

**Forbidden operations:** mutate the M4 catalog, publish a new rule, accept a caller-supplied snapshot, reuse a revoked receipt for fresh use, convert a modeled token into money/welfare, turn a route state into a probability, person, decision, action or durable trait, install N9/OC05, or treat the GSS/NCA fixture numerics as observed source facts.

## 2. The actual two-epoch read-only surface

| field | E1 | E2 | permitted interpretation |
|---|---|---|---|
| `training_access` | true | true | formal eligibility is preserved |
| `training_fee` | 2 modeled tokens | 6 modeled tokens | material affordability changes |
| `exit_cost` | 2 modeled tokens | 8 modeled tokens | material exit constraint changes |
| `civil_open` / `civil_sanction` | true / false | true / false | civil route unchanged |
| `NONPARENT_OPTIONS.training` | `ELIGIBLE` | `BLOCKED_BY_MODELED_RULE` | practical opportunity changed |
| `NONPARENT_OPTIONS.exit_constraint` | `WITHIN_MODELED_BUDGET` | `RESOURCE_CONSTRAINED` | material constraint changed |
| `NONPARENT_OPTIONS.civil` | `ELIGIBLE` | `ELIGIBLE` | legitimate null |
| scenario feasibility | FEASIBLE / FEASIBLE | FEASIBLE / FEASIBLE | client-grain null (reads access only) |
| empirical steps | 18/32→10/16→6/8 | identical | source held fixed |
| `route_probability` | `null` / `NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL` | same | no actor or route model |
| `selection_weight` | `null` / `NO_SCENARIO_SELECTION_MODEL_OR_ISSUER` | same | no person selection |
| `actor_executions` / `model_calls` | 0 / 0 | 0 / 0 | actor-free |

No row licenses a claim about a real person's options, a real institution, a real budget, a real country or a real historical period.

## 3. Future exact N8E→N9 context-only adapter contract

This is the contract shape that would be permitted **only after** the N03 docket returns all five positive owner decisions. It is not implemented, not installed and not requested by this return.

### 3.1 Required upstream receipts (all exact, all separately signed)

1. `GHA_R5_R9_ORIGINAL_MERGED_RELEASE_METHOD_ATTESTATION` from Afrobarometer/CDD-Ghana.
2. `SRC02_SRC03_GHA_EXACT_RETAINED_RELEASE_CUSTODY_RECEIPT` from the separately source-read-authorized Rawlsing custodian.
3. `GHANA_Q43_Q31_TWO_WAVE_MEASUREMENT_DESIGN_ESTIMAND_DECISION` from an independent survey statistician, including a variance method or a typed `UNQUANTIFIED_DESIGN_UNCERTAINTY`/`HOLD_METHOD`.
4. A positive exact EE12/C7 `SourceUniverseRelation` + immutable `AuthoritySnapshot` with target use `EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY`, revocation/falsification conditions and exact source/product refs.
5. Two per-wave native five-category fact products (0,1,2,3,4 preserved; R5 refusal 998 and R9 refusal 8 typed; no `0` laundering) and an independently qualified N8E comparator blob.
6. An explicit N9 product-family/target-use permission from the N9 owner, plus the exact as-of/dependency/replay/invalidation receipt.

### 3.2 Adapter input (no caller-supplied values)

```json
{
  "schema": "N8E_TO_N9_CONTEXT_REQUEST@1",
  "claim_id": "N8E_GHA_R5Q43_R9Q31_DSAT_R1",
  "wave_fact_refs": ["<exact R5 fact ref>", "<exact R9 fact ref>"],
  "ee12_relation_ref": "<exact positive relation ref>",
  "ee12_snapshot_ref": "<exact positive snapshot ref>",
  "science_decision_ref": "<exact independent decision ref>",
  "variance_method_ref": "<exact method ref or typed HOLD ref>",
  "target_use": "EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY",
  "as_of": "<exact ISO date>",
  "requested_pooling": false,
  "requested_person_exposure": false,
  "requested_model_use": false
}
```

The adapter must dereference the values from the owner registry; the request may carry refs but never category counts, weights, variance or a delta.

### 3.3 Adapter output (context only)

```json
{
  "schema": "N8E_TO_N9_CONTEXT_RECEIPT@1",
  "grade": "HISTORICAL_ATTITUDE_CONTEXT_ONLY",
  "claim_id": "N8E_GHA_R5Q43_R9Q31_DSAT_R1",
  "wave_five_category_distributions": ["<exact R5 distribution>", "<exact R9 distribution>"],
  "typed_special_counts": ["<R5 dk/refused/missing>", "<R9 dk/refused/missing>"],
  "weight_design_variance_refs": ["<exact R5>", "<exact R9>"],
  "delta": "<exact issued delta or null>",
  "uncertainty": "<issued interval or UNQUANTIFIED_DESIGN_UNCERTAINTY or HOLD>",
  "classification": "<issued classification or HOLD>",
  "as_of": "<exact ISO date>",
  "dependency_refs": ["<wave facts>", "<EE12>", "<science>", "<release custody>"],
  "revocation": {"mode": "SELECTIVE_DEPENDENCY", "source_change_invalidates": true},
  "replay": {"cold_replay_required": true},
  "operative_N9": false,
  "installed_OC05": false,
  "n8e_product": false,
  "person_exposure": false,
  "pooling": false,
  "model_use": false,
  "actor_executions": 0
}
```

**Hard refusals:** unissued EE12; missing custody; missing design variance; collapsed five-category topology; special code laundered into `0`; `NO_CHANGE` inferred from a null/interval crossing zero; any attempt to write the result into a V553 active-causal root, an N10W structural-route model, a person-selection weight, a durable trait or an actor action; any pooling of the two waves into a panel or common-respondent joint.

## 4. No-actor clause

1. No Sorok thought, intention, memory, emotion, action, genealogy, CAN008 rule, V3 person or V2 expression is created, inferred, simulated or authorized here.
2. The two consumers are **institutional-option and finite-proposal readers**, not actors. They produce no parent, relationship, conception, person, decision, probability or weight.
3. `actor_executions=0`, `model_calls=0`, `person_exposure=false`, `model_use=false`, `pooling=false`, `operative_N9=false`, `operative_OC05=false`.
4. A future Sorok-side consumer would need its own exact owner rule (CAN-008 R2 or successor), its own permitted readset, its own as-of clock and its own independent review. This contract cannot supply that rule.
5. The N8E Ghana input is **absent/HOLD** and remains outside the world root; a Sorok-facing client must not receive a Ghana attitude delta as if it were an installed structural fact.

## 5. Verification

- Cold product: two independent child processes, byte-identical, SHA-256 `c4697da7e08a6920d2208e46274a0bab122ecdd334249f6268875625ea2f857b`.
- 183 JUnit events: 41 new (20 N8E/comparator, 21 world), 30 original M4/M5, 75 original empirical chain, 37 original E04 court; 0 failures/errors/skips.
- Import preimages: 26 pins, all match; 53 module records.
- Revocation, mismatch, historical immutability and clock boundaries are executed in `03_WORLD_TWO_EPOCH_CONSUMER_DELTA.json`.
- Sanitized environment: `environment_passport.json`.

**No Sorok permission, N9 installation, N8E product, N10W model, N8S structural authority, EE12 issuance, N11/N12 or V3 permission is issued by this contract.**
