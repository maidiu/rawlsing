# RFA-06B — complete output-field exactness and local-contract audit

Source: unchanged `lab_fixture/OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json` and `court_common_r2.py::deterministic_candidate`, both grounded at RFA-06A sealed startup. The RFA-05B model-visible packet schema is copied unchanged. No output is scored here.

| Required output/property | Source requirement | Identity/evidence classification | R2 status |
| --- | --- | --- | --- |
| `kind` | `MODEL_CANDIDATE_NOT_ADMITTED` | `PROVIDER_SCHEMA_CONST`; also visible in unchanged `model_payload.shared.output_schema` | PASS |
| `fixture_id` | Original RF001–RF010 enum; local exact case check | **R1: `HIDDEN_REQUIREMENT_DEFECT`**. **R2: `MODEL_VISIBLE_AND_DERIVABLE` plus request-specific `PROVIDER_SCHEMA_CONST`** | REPAIRED |
| `hand_authored_experiment` | `RFA05_SURROGATE_INPUT_NOT_V3` | `PROVIDER_SCHEMA_CONST`; same value in model-visible source schema | PASS |
| `atoms` | Array of typed, bounded objective atoms | `MODEL_VISIBLE_AND_DERIVABLE`: type/shape, allowed actor/actions, scene/time window are in shared payload | PASS |
| `realization_prose` | Objective staging of exact atoms | `MODEL_VISIBLE_AND_DERIVABLE`; model controls both its typed output and prose, inherited renderer contract demands byte-exact speech | PASS |
| `world_effect_proposals` | Array, existing documented referents, `requires_admission=true` | `PROVIDER_SCHEMA_CONST` for required admission flag; `LOCAL_CHECK_DERIVABLE_FROM_MODEL_INPUT` for world IDs, documented in scene | PASS |
| `materialization_requests` | Array of requests, `permission_status` in `UNAUTHORIZED/DEFERRED` | `MODEL_VISIBLE_AND_DERIVABLE`; permitted enum is part of schema, not a hidden current-case answer | PASS |
| `no_occurrence_assertion` | `true` | `PROVIDER_SCHEMA_CONST`; explicit source contract and model-visible schema | PASS |

## Nested required and locally checked fields

- Atom: `atom_id` (nonempty, local uniqueness), `kind` (visible enum), `relative_ms` (integer 0–30000, model-visible thirty-second scene), `actor` (`NADIA` schema const; actor name disclosed), `content` (model-selected text), `referent_ids` (model-visible scene references). Local chronological ordering and unique atom IDs do not require a hidden predetermined identifier. They concern coherence of the model's own candidate.
- World effect: `referent_id` (scene ID present), `from` and `to` (candidate-proposed descriptions), `requires_admission` (`true` provider const). Permission must still be judged separately; no hidden exact resulting state is demanded.
- Materialization: `description`, `reason` (candidate-proposed), `permission_status` (provider-visible enum). No hidden specific value imposed.
- Deterministic validator: exact `fixture_id` case equality is now *redundantly* justified by (a) model-visible `required_fixture_id`, (b) bound provider schema `const`, (c) execution manifest case ID. Time ranges, ordered atoms, unique IDs, documented referents, and exact speech/prose equivalence are derivable from supplied scene/instructions or from the candidate's own fields; no other unexposed exact answer is required.

**Other hidden exact-output requirement defects:** `NONE` under this enumerated contract. This does not claim every model output will be valid; semantic-scoring or materialization review remains outside the harness.

## Invariants and negative controls

- Neither identity envelope nor per-request schema includes `condition`, WP/N, replicates, private metadata, scoring rubrics, evaluator truth register, or any Nadia facts that were absent from the inherited payload.
- The original output schema remains unchanged. Provider schema `fixture_id` enum → per-case `const` is strictly an execution projection. No additional schema constraints tighten the substance of `atoms`, `realization_prose`, actions, or world effects.
- The model-visible global output schema inside unchanged payload still describes legal output semantics for all cases; the new small transport instruction and hard-bound outer schema disambiguate which current fixture ID to emit.
- All 60 R2 requests and one non-primary smoke request are checked offline for exact equality:
  `TRANSMITTED_REQUIRED_FIXTURE_ID == PROVIDER_SCHEMA_FIXTURE_CONST == EXECUTION_MANIFEST_CASE_ID == LOCAL_VALIDATOR_EXPECTED_CASE_ID`.
- R1 used a single unbound enum; R2 cannot infer a scoring success from fixing this bookkeeping limitation. The new court must still undergo independent blind evaluation after actual model generation.
