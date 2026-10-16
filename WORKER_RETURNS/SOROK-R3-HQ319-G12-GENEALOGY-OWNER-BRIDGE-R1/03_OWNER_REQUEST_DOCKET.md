# G12 competent-owner request docket — proposed interface only

**Disposition: GENEALOGY_ADP_OWNER_AUTHORITY_HOLD.** No signature or API implementation is fabricated. `court_hold` below is this court's typed classification; quoted native refusals are separately observed in `evidence/g12_observations.json`. Accepted ADP015@1.0.0, ADP020@1.0.0 and ADP007 remain controlling. Implementers cannot self-issue the proposed semantics.

## Exact missing operations and issuer requirements

| Court hold / requested operation | Exact input and output contract needed | Competent issuer and current evidence |
|---|---|---|
| `MOTHER_NATIVE_CHECKPOINT_UNBOUND` — `prepare_plan` | Immutable generated mother actor/checkpoint/history anchor immediately before target; exact world/as-of, roles, phase, position, prior children/partners/household/shared events and access. Output `PLAN_PENDING_NONCAUSAL`, with zero causal cursor/draw/state effects. | V3 developmental/ADP007 + ADP015/021. Current mother checkpoints are SGI1 fixtures. ADP007 §§5–10 permits sparse beginning; §13 forbids invented prior life. |
| `RETROSPECTIVE_CONSTRUCTION_RULE_UNISSUED` — `plan_history` | Minimal endpoint constraints, immutable mother/known counterpart, independent partial-history facts and explicit unknown roots, construction dependency DAG, finite attempt budget and full rejected-attempt log. Output construction-only history proposal; never an admitted event. | ADP015 genealogy adjunct, ADP007 identity, ADP021 scheduling. Astra16 §4D is a proposal. ADP015 requires independent represented histories, without supplying this construction schedule. |
| `NATIVE_DEVELOPMENTAL_EFFECT_RULE_UNBOUND` — `replay_history` | For each proposed event: exact stable actor, admitted source/witness, world/context and effective time, native owning rule/version/hash, pre-state, read set, target effect, post-state and rollback/replay receipt. Parent links must resolve and be causally earlier; same-time conflicts need owner precedence. | ADP007/009/010, CAN008_R2 and each durable/project/material/memory/relationship owner. Observed generic project trace: `UNAUTHORIZED_TRANSITION`; fixed candidate only. No conversion of SGI1 tags into native memories, practices or beliefs. |
| `SCENARIO_SELECTION_AUTHORITY_UNBOUND` — `seal_selectable_set` | Prospectively sealed finite equivalence classes, exact candidate payload/replay/eligibility hashes, unknown/other coverage, rule-owned eligible set, integer weights or equiprobability, purpose/estimand and explicitly synthetic versus calibrated meaning. Changes invalidate selection identity. | ADP015 §§8/10/11 domain issuer + scientific selection owner. ADP020 cannot supply weights. The lab's policy names do not constitute a registered semantic rule. A singleton is no permission to admit an unlawful candidate. |
| `ADP020_NATIVE_BINDING_UNBOUND` — `select_endpoint` | Exact 32-byte root capability and provenance; owner-issued JOINT or GENEALOGY scope; decision classification and static stream registration; rule invocation, event anchor, occurrence/slot/draw indices; HMAC algorithms; unbiased mapping; complete Decision/Draw receipts. Zero draws for empty/singleton/deterministic/underauthorized paths. | ADP020 §§5–16, with ADP015 providing semantics. Proposed `conception_scenario_selection` is not licensed merely by its spelling. Current lab sampler is SHA256/modulo and lacks accepted receipt semantics. |
| `RETRY_SELECTION_MEASURE_UNBOUND` — `record_attempt` | Freeze q, frame, selected endpoint and finite history attempt slots before construction. Record each failure; retain no-history/HOLD. Any resampling or changing eligibility must version its measure, acceptance a and normalization. | ADP015 decision/science owner with ADP020 reviewer. Exact analytic survivor-bias example is not calibration or a new posterior. Default: hold selected unconstructible endpoint, no hidden redraw. |
| `RELATIONSHIP_FORMING_WITNESS_UNBOUND` — `admit_relation` | Two already-generated actor refs and immutable independent anchors; exact rule-owned forming witness beyond encounter; roles/direction, shared event identity once, per-actor perceived facts and access, separate household membership effects. No automatic reciprocity or household. | ADP015 §§6–9; ADP010 encounter, ADP017 access and relevant material owner. Current helper emits a placeholder relation even with empty history; it cannot supply this witness. A native relationship transition is NOT established. |
| `CONCEPTION_BIOLOGY_AUTHORITY_HOLD` — `admit_conception` | Separately defined occurrence/biological trigger, eligible participants, exact time/interval, physiological/consent/material constraints where required, world witness, scheduler admission and prospective consequences. Otherwise target remains pending. | Competent V3 reproduction/organismic/occurrence issuer + ADP021; ADP019 only for external events in its jurisdiction. ADP015 bare child-generation event is not conception or birth authority. No such event is created here. |
| `CHILD_GENERATION_NATIVE_PRODUCER_UNBOUND` — `generate_child_ref` | ADP015 §10 exact two parents and generation-time anchors, generation trigger, context, candidate/admission, effective time/occurrence index and accepted deterministic ID scheme. Result bare child ref with `GENERATION_COMPLETE_INITIALIZATION_PENDING`; no personality or household. | ADP015 registered explicit-trigger profile is semantically defined and zero-draw; no real trigger/runtime grant supplied by this court. Production guard denied this requested path. Prior older child in M2 is retained fixture history, not a new native child. |
| `BIRTH_AND_CHILD_INITIALIZATION_HOLD` — `admit_birth` / `initialize_child` | Birth/gestation semantics and timing remain distinct from generation; child initialization requires real generated subject, Phase-A provenance, ADP007 entity/activation receipts and separate child scope. Child exposures/uptake follow their actual events. | Biological/organismic/time owner plus ADP007/008/009/010. No inferred nine-month constant, birth alias, inherited psyche or parent averaging. |
| `SOURCE_DYAD_HOUSEHOLD_USE_UNBOUND` — `qualify_generic_possibility` | Generic target/conditioner native coordinates, direction, unit, universe/risk set/denominator, exact source/release/readset, design/weights/uncertainty and all clocks; explicit lawful support/unknown/noncomparability. Dyad/household queries require those actual sampling units and bridge authority. | Pyat N9/N10E/N10W/C1 and source/model-use issuers. Single-respondent marginals cannot estimate parent pairing, joint household truth, attraction or individual history. Generic PRE-V3 output remains possibility, never a parent. No real-source operation was run. |

## Proposed transaction shape

```text
prepare_plan(mother_checkpoint, pending_target, world_ref, embargo_manifest)
  -> construction_plan | typed_hold                  # zero causal effects
qualify_generic_possibility(plan, exact_query_grants)
  -> supported / unknown / noncomparable / denied     # no actor facts
seal_selectable_set(plan, candidate_replay_hashes, issued_selection_rule)
  -> sealed_candidates | selection_authority_hold
select_endpoint(sealed_candidates, issued_adp020_binding)
  -> SELECTED_PENDING_HISTORY | typed_no_draw_hold
plan_history(selected_endpoint, immutable_partial_past, finite_attempt_budget)
  -> noncausal_attempts                              # log all failures
replay_history(attempt, actual_native_owner_capabilities)
  -> independently_replayed_parent_anchor | typed_hold
reconcile_shared_witnesses(mother_anchor, second_parent_anchor, admitted_events)
  -> relation_candidate | contradiction_hold         # never rewrite mother
admit_relation / admit_conception / generate_child_ref / admit_birth / initialize_child
  -> distinct separately authorized transactions, or each remains HOLD
```

These names are **requested interface proposals**, not calls claimed to exist. No new production adapter or positive registry entry was installed. Frozen model records can be reused for a later source-free test; any new model acquisition still needs a separate grant. Separate independent I2 acceptance follows any new candidate, before competent adoption. No C11/C12, N11/N12, physical weld or operative wake is inferred.
