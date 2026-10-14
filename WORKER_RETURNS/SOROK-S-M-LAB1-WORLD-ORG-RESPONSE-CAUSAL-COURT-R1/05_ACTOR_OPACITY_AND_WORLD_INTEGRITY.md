# 05 — actor opacity, world-context integrity, and null-control register

Sources: `outputs/primary_results.json` (`opacity`, `null_controls`, `integrity`), `outputs/runs/*`, `outputs/sm_court_schema_gate.json`.

## 1. Actor-opacity results (all PASS)

Preregistered conditions executed:

| Condition | Implementation | Result |
|---|---|---|
| no explanation | `actor_testimony(mode=NO_EXPLANATION)` | no utterance required; objective machine record unchanged |
| incorrect self-explanation | `MISTAKEN_EXPLANATION_BELIEVED` ("I acted because the supervisor dislikes me", claim parents `CLAIMED_PARENT_SUPERVISOR_DISLIKES_ME`) recorded as ADP017 actor testimony with mistaken warrant | `objective_effects_changed: false`; machine-identified parents stay in evaluator metadata only |
| confident incorrect self-explanation | `WRONGLY_CONFIDENT_EXPLANATION`, allowed only as a separately admitted mistaken belief (confidence HIGH) | same; never repaired into analyst truth; never copied into the machine causal record |
| inaccessible trace affecting response without recall | K3 `TRACE_ACTIVE` recruits `HEIGHTENED_GUARD` via nondeclarative trace while ADP016 access is `RETAINED_NOT_ACCESSIBLE`/`UNAVAILABLE` and ADP017 origin claim is DENIED | response differs from `TRACE_ABSENT`; actor-safe memory view shows `NON_DISCLOSABLE_ORIGIN` and `recall_granted: false` |

Hidden-origin hard test: `hidden_causal_origin = {hidden_origin: "EV7_PUBLIC_SHAMING_AT_AGE_7", disclosed_only_to_evaluator: true}` injected into evaluator-only metadata; the actor-safe projection is **byte-identical** across 6/6 arm×contrast runs (sha256 recorded in `outputs/primary_results.json#opacity.hidden_origin_injection`). The actor-safe payload contains `hidden_origin_refs: []` and is a strict ADP016/ADP017 derivative — not an instruction to a model to hide anything.

Leak rule: any origin disclosure is a hard failure. Observed leaks: **0** across all 576 trials.

## 2. World-context integrity

- `T0_WORLD_CONTEXT_GATE` requires world receipt, position receipt, relationship, opportunity/exposure, ancestry and effective time on every evaluated occurrence.
- Worldless occurrence (world receipt removed) → `UNDERSPECIFIED/HOLD` (`NO_WORLD_CONTEXT:<missing fields>`) with zero commits — exercised in unit tests and enforced in every trial path.
- World snapshot mismatch (wrong world id/hash) → `WORLD_SNAPSHOT_MISMATCH` hold.
- Unadmitted `DRAFT` → `UNADMITTED_EVENT` hold; `REJECTED` → `REJECTED_EVENT` hold; neither can commit effects.
- Historical material binding: K6 runs on the dated 1999 world/position variant with sanction capacity bound by the position receipt at event time; a title/category string never changes capacity (`K6_NOMINAL_TITLE_NO_POWER`, `CATEGORY_ONLY` nulls).
- Public standing changes only through an admitted institutional ratification event with `CAN_RATIFY` power; revalidation refuses peers, supervisors and badge-utterances.

## 3. Null-control register (15 executed, 15 PASS)

| # | Control | Result |
|---|---|---|
| 1 | IDENTICAL_FULL_INPUT_REPLAY | identical digests + state hashes for all 6 K |
| 2 | UNRELATED_NOISE_EVENT | no-op selection, zero present commits, state hash unchanged |
| 3 | UNADMITTED_DRAFT | hold, zero commits |
| 4 | REJECTED_EVENT | hold, zero commits |
| 5 | CATEGORY_ONLY | no policing route permitted, zero action effects |
| 6 | POWERLESS_WITNESS | `NO_OBJECTIVE_PUBLIC_STANDING_FROM_UNEMPOWERED_WITNESS` gate refusal |
| 7 | INACCESSIBLE_LEDGER_INJECTED_TO_EVALUATOR_ONLY | actor-safe payload byte-identical |
| 8 | IRRELEVANT_RELATION_ORDER | shuffled history event order → identical digest + selection |
| 9 | WEIGHT_OR_SEED_WITHOUT_ISSUER | `WEIGHT_OR_SEED_WITHOUT_ISSUER` hold, zero commits |
| 10 | ZERO_ACTION_AFFORDANCE | `VALID_EMPTY`, zero commits |
| 11 | K1_ADJECTIVE_ONLY_CHANGE | rephrased receivable wording → identical selection + state (changed adjectives score ZERO) |
| 12 | K2_FREE_EDGE_MUTATION | `NO_UNAUTHORIZED_C_GRAPH_EDGE`; relation view null |
| 13 | K4_PARAPHRASE_ONLY_NO_REVISION | one-parent revision refused (`NO_REWRITE_PRIOR_EVENTS`) |
| 14 | K5_OFFICIAL_SOUNDING_UTTERANCE | standing-change gate refusal |
| 15 | K6_NOMINAL_TITLE_NO_POWER | no policing permitted without capacity |

Valid no-op (`NO_ACTION`/`NEUTRAL_RESPONSE`/`NO_SANCTION` with full machinery) is recorded and distinguishable from not-run (holds) and from source-intrinsic inapplicability (route absence).

## 4. External schema gate

S-M's own `repro/sm_court.mjs` was executed by Node v18.14.2 over the sealed S-M specification plus 48 retained trial receipts (`outputs/sm_court_receipts_S01.json`): `passed: true`, `errors: []` — receipts carry the complete `audit_schema.output_required` field set, respect the model-call budget (0 ≤ 1) and evidence-token cap (≤ 6000), bind world + admitted event hashes, and expose no hidden origin refs. The script's own ceiling stands: it establishes schema/receipt integrity only, `empirical_causal_result: NOT_ESTABLISHED_BY_THIS_SCRIPT`.
