# ASTRA-C05 — EVIDENCE AND CALIBRATION BINDING R1

Commission: `ASTRA-C05`
Scope: `SDTF_OBJECTIVE_RULE_BODY_AND_WORLD_POPULATION_R1_ONLY`
Disposition: `PASS__ADMISSION_INPUT_CONTRACTS_EXPLICIT__NO_AUTHORITY_MINTED`

This file binds the five C05 candidate bodies to exact **future input obligations**. It is not an authority registry and does not declare any source, rule, witness or calibration current.

## 1. Common admission packet contract

A future admission packet for any C05 candidate MUST provide immutable exact refs sufficient to populate the existing R1 contracts without fallback selection:

### Rule trace

- one or more exact `source_refs`;
- one or more exact `claim_refs`;
- exact `evidence_status_ref`;
- exact `normalized_mechanism_ref`;
- exact `permitted_rule_shape_ref`;
- exact `required_objective_inputs_bindings_ref`;
- exact `qualification_realization_proof_contract_ref`;
- exact `temporal_currentness_contract_ref`;
- exact `portability_ceiling_ref`;
- exact `currentness_ceiling_ref`;
- exact `historical_institutional_validity_ref`;
- exact `negative_ceiling_ref`;
- exact `v3_stop_boundary_ref`.

Mutable selectors such as latest/default/fuzzy/version ranges are forbidden.

### Authority ceiling roles

Every specialization must explicitly disposition all six R1 authority roles:

- `RULE_OWNER` — MUST be `BOUND`;
- `MEASUREMENT` — `BOUND` when the rule consumes measurements; otherwise exact `NOT_APPLICABLE` basis;
- `ESTIMAND` — `BOUND` when an estimand is asserted; otherwise exact `NOT_APPLICABLE` basis;
- `IDENTIFICATION` — `BOUND` when identification authority is required; otherwise exact `NOT_APPLICABLE` basis;
- `CAUSAL_USE` — MUST be `BOUND`;
- `CALIBRATION` — MUST be `BOUND` for `NUMERIC`; MUST be exact `NOT_APPLICABLE` for `NONNUMERIC`.

Every `BOUND` role must carry an exact authority ref and explicit current-selection evidence. C05 supplies neither and therefore leaves every candidate `CANDIDATE_NOT_CURRENT`.

## 2. Candidate-specific evidence packets

### `C05-EVID-P1-R1` — REQUIRED MATERIAL ACCESS GATE

**Required source claims**

1. the exact objective operation or route under consideration;
2. the exact resource/access prerequisite claimed necessary for that operation;
3. the source-declared actor/position/context applicability grain;
4. temporal validity / recurrence semantics for the access relation;
5. portability limits and negative-proof ceiling.

**Required objective determinant families**

- `P1_PREREQUISITE_DECLARATION` — exact source-owned statement that the resource/access relation is required;
- `P1_ACCESS_STATE` — type-compatible objective access state for the bound actor/position/context/time;
- `P1_REACHABILITY_STATE` when the source distinguishes nominal access from objective reachability.

**Nonnumeric baseline slots**

`operation_kind`, `required_resource_kind`, `access_relation_kind`, `coverage_interval_semantics`, `binding_type`, optional exact `quantity_band_ref`.

**Admission blocker**

`BLOCKED_PENDING_EXACT_SOURCE_CLAIM__RULE_OWNER__CAUSAL_USE__CURRENT_SELECTION__AND_OBJECTIVE_ACCESS_WITNESS_REFS`

No quantity threshold is authorized. If a later rule inserts a numeric threshold, it becomes a separate `NUMERIC` specialization and requires bound calibration authority.

---

### `C05-EVID-P2-R1` — DIRECTED OBLIGATION IN FORCE

**Required source claims**

1. competent authority ownership and scope;
2. exact addressee/position binding law;
3. exact duty content or immutable duty-code definition;
4. jurisdiction/context applicability;
5. effective/termination/supersession semantics;
6. any sanction route as a separately sourced proposition, never inferred from the obligation label.

**Required objective determinant families**

- `P2_AUTHORITY_SCOPE_STATE`;
- `P2_ADDRESSEE_BINDING_STATE`;
- `P2_DUTY_RULE_STATE`;
- `P2_EFFECTIVE_VALIDITY_STATE`;
- optional separately sourced `P2_SANCTION_ROUTE_STATE`.

**Nonnumeric slots**

`authority_relation_kind`, `addressee_binding_kind`, `duty_ref`, `jurisdiction_context_key`, `effective_interval_semantics`, optional `sanction_route_ref`.

**Admission blocker**

`BLOCKED_PENDING_COMPETENT_AUTHORITY_SOURCE__RULE_OWNER__CAUSAL_USE__CURRENT_SELECTION__AND_EXACT_DUTY_BINDING_REFS`

---

### `C05-EVID-P3-R1` — ORGANIZED ACTIVITY WINDOW

**Required source claims**

1. organization ownership of the activity/schedule state;
2. exact activity kind;
3. operative schedule/window semantics;
4. actor/position applicability requirements;
5. objective reachability requirements;
6. recurrence/freshness semantics if a durative/recurrent proposition is later asserted.

**Required objective determinant families**

- `P3_ACTIVITY_DEFINITION_STATE`;
- `P3_SCHEDULE_WINDOW_STATE`;
- `P3_APPLICABILITY_STATE`;
- `P3_REACHABILITY_STATE`.

**Nonnumeric baseline slots**

`organization_ref_kind`, `activity_kind`, `schedule_window_type`, `applicability_binding_kind`, `reachability_condition_set_ref`, optional `recurrence_contract_ref`.

**Admission blocker**

`BLOCKED_PENDING_ORGANIZATION_SOURCE__RULE_OWNER__CAUSAL_USE__CURRENT_SELECTION__AND_EXACT_SCHEDULE_APPLICABILITY_REFS`

No numeric capacity/timing coefficient is authorized. Any numeric specialization requires bound calibration authority.

---

### `C05-EVID-P4-R1` — INSTITUTIONAL GATE ELIGIBILITY

**Required source claims**

1. institution ownership of the gate/eligibility rule;
2. immutable gate rule identity/content;
3. complete ordered set of required objective predicate types;
4. actor/position/context binding grain;
5. effective interval and supersession semantics;
6. source-owned exception/override law, if any.

**Required objective determinant families**

- `P4_GATE_RULE_STATE`;
- one exact determinant for every member of the source-owned `required_predicate_type_refs` set;
- `P4_BINDING_CONTEXT_STATE` where context is not encoded in each predicate;
- optional source-authorized `P4_OVERRIDE_STATE`.

**Nonnumeric baseline slots**

`institution_ref_kind`, `gate_rule_ref`, ordered `required_predicate_type_refs`, `binding_grain`, `effective_interval_semantics`, optional `override_contract_ref`.

**Admission blocker**

`BLOCKED_PENDING_INSTITUTION_GATE_SOURCE__RULE_OWNER__CAUSAL_USE__CURRENT_SELECTION__AND_COMPLETE_PREDICATE_BINDING_REFS`

A missing predicate remains unknown and may not be silently treated as false. Numeric cutoff variants are separate `NUMERIC` specializations requiring calibration authority.

---

### `C05-EVID-P5-R1` — COUNTERPART CHANNEL AVAILABLE

**Required source claims**

1. exact actor/counterpart relation or role-binding semantics;
2. exact channel type and endpoint ownership;
3. operative/current channel-state semantics;
4. objective reachability/applicability requirements;
5. directionality if relevant;
6. termination/supersession/recurrence semantics.

**Required objective determinant families**

- `P5_COUNTERPART_RELATION_STATE`;
- `P5_CHANNEL_ENDPOINT_STATE`;
- `P5_REACHABILITY_STATE`;
- optional `P5_DIRECTIONALITY_STATE`.

**Nonnumeric baseline slots**

`counterpart_role_kind`, `channel_kind`, `endpoint_binding_kind`, `reachability_condition_set_ref`, `interval_or_recurrence_semantics`, optional `directionality_ref`.

**Admission blocker**

`BLOCKED_PENDING_COUNTERPART_CHANNEL_SOURCE__RULE_OWNER__CAUSAL_USE__CURRENT_SELECTION__AND_EXACT_CHANNEL_REACHABILITY_REFS`

## 3. K1–K4 evidence/witness binding

The existing proof grammar is used without reinterpretation:

- `K1_CONSTITUTIVE_POSITIONAL`: competent operative source-owned rule/state + exact actor/position/context binding + valid-time support.
- `K2_QUALIFIED_POSSIBILITY`: admitted objective route/channel/gate + exact actor applicability/reachability.
- `K3_REALIZED_OCCURRENCE`: exact type-compatible competent occurrence evidence at actor/context/time grain.
- `K4_ACTIVE_DURATIVE`: lawful Path A current/interval witness **or** Path B owner-declared continuing state + compatible support interval + complete termination/supersession/invalidation coverage through query time + no defeating closing fact.

For every candidate:

- positive proof must be supplied by the competent type-specific witness owner;
- a stale/revoked/unknown witness produces `UNKNOWN_NOT_PROVEN` and no fact;
- failed positive proof is not negative proof;
- explicit negative truth requires explicit competent negative evidence or a proved source-authorized closed-world contract at the exact grain;
- K1/K2 never auto-promote to K3;
- current K1/K2 never auto-promote to K4.

## 4. Deterministic evidence packet identity material

C05 defines plan-level packet keys only. A later authorized materializer MUST derive its exact immutable object identities from canonical material including at least:

`candidate_key | exact_source_refs | exact_claim_refs | exact_authority_refs_and_selection_evidence | exact_slot_bindings | exact_validity_domain | exact_proof_contract_ref | exact_negative_ceiling_ref | exact_v3_stop_boundary_ref`

Any change in any member creates a different packet identity. No alias, latest pointer, mutable default or silent renormalization is permitted.

Plan packet keys:

- `C05-EVID-P1-R1`
- `C05-EVID-P2-R1`
- `C05-EVID-P3-R1`
- `C05-EVID-P4-R1`
- `C05-EVID-P5-R1`

These keys are scheduling/docket identities only; they are not production `ExactRef` values.

## 5. Admission decision table

| Candidate | Evidence packet present? | All mandatory authority roles lawfully dispositioned? | Slot binding complete? | Exact current-selection evidence? | Permitted R1 state |
|---|---|---|---|---|---|
| any C05 candidate | no | any | any | any | `CANDIDATE_NOT_CURRENT`; execution forbidden |
| any C05 candidate | yes | no | any | any | `CANDIDATE_NOT_CURRENT`; execution forbidden |
| any C05 candidate | yes | yes | no | any | `CANDIDATE_NOT_CURRENT`; execution forbidden |
| any C05 candidate | yes | yes | yes | no | `CANDIDATE_NOT_CURRENT`; execution forbidden |
| any C05 candidate | yes | yes | yes | yes | eligible for later authorized R1 admission review; C05 itself still does not mint `CURRENT_ACCEPTED` |

## 6. C05 terminal evidence finding

The commissioned read set supplies constitutional categories, proof grammar, currentness/authority adapters and runtime seams; it does **not** supply candidate-specific immutable empirical source/claim/authority packets that would lawfully authorize these five concrete bodies as current production rules. The correct bounded result is therefore a complete admission docket with explicit blockers—not fabricated evidence or authority.
