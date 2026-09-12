# ASTRA-C05 — MECHANISM RULE CANDIDATE LEDGER R1

Commission: `ASTRA-C05`
Scope: `SDTF_OBJECTIVE_RULE_BODY_AND_WORLD_POPULATION_R1_ONLY`
Commission parent: `8688f8886601cb18ca34cc0150d055f036ed4836`
Semantic/runtime floor read exactly as commissioned: `3468673673db2f3de804d6e825585f86ff98e870`; R4 companion specification: `43e52f12bb7e175d108446c6c852e5532d22b9ad`.

## Governed disposition

`PASS__FINITE_OBJECTIVE_RULE_CANDIDATE_DOCKET_AND_DETERMINISTIC_POPULATION_PLAN_SUPPLIED`

This is a **candidate ledger only**. It mints no `CURRENT_ACCEPTED` mechanism rule, no rule-authority binding, no rule application, no actor fact, no objective consequence fact, and no production authority. Every candidate below remains `CANDIDATE_NOT_CURRENT` until a later authorized lane supplies exact immutable source/evidence/authority material and an R1 binding passes `require_current_rule_admission`.

`OBL063` therefore remains unmet. Nothing in this return claims that operational world population has occurred.

No D2, D3, D4, P6, subjective premise, appraisal, uptake, motive, belief, distress, mastery, perceived support, memory, learning, trait, capacity, or durable-development state is introduced.

## Binding law used by every candidate

Each candidate is a non-executable rule-body specification with four separately reviewable layers:

1. **Invariant body** — qualitative objective relation that must not vary with a calibration value.
2. **Calibration/configuration slots** — exact source-owned parameters needed to specialize the body to a domain; unresolved slots block admission.
3. **Evidence dependency** — exact immutable trace and authority inputs required by `RuleTraceBinding` / `MechanismRuleAuthorityBinding`.
4. **Validity domain** — actor/position/context/world/valid-time grain within which the rule may be considered.

All candidates preserve these hard gates:

- exact `RULE_OWNER` and exact `CAUSAL_USE` authority are mandatory;
- `SOURCE CITATION != CAUSAL-USE AUTHORITY`;
- any `NUMERIC` specialization additionally requires exact current `CALIBRATION` authority;
- a nonnumeric specialization must carry explicit calibration `NOT_APPLICABLE` basis;
- constitution currentness never implies rule currentness;
- a failed positive proof yields `UNKNOWN_NOT_PROVEN`, never an opposite fact;
- an application may be hosted only against the exact current R1 admission and exact determinant facts;
- K3 realized occurrence is never inferred from K1/K2 qualification alone;
- K4 active/durative status requires its own type-specific current witness path.

## Candidate index

| Candidate key | Exact mechanism class | Direct objective target | Value mode at docket | Current status |
|---|---|---|---|---|
| `C05-P1-REQUIRED-MATERIAL-ACCESS-GATE-R1` | `P1 MATERIAL_ACCESS_DEPENDENCY` | K2 material route/operation objectively available | `NONNUMERIC` baseline | `CANDIDATE_NOT_CURRENT__EVIDENCE_BLOCKED` |
| `C05-P2-DIRECTED-OBLIGATION-IN-FORCE-R1` | `P2 DIRECTED_AUTHORITY_OBLIGATION_SANCTION` | K1 source-constituted directed obligation | `NONNUMERIC` | `CANDIDATE_NOT_CURRENT__EVIDENCE_BLOCKED` |
| `C05-P3-ORGANIZED-ACTIVITY-WINDOW-R1` | `P3 ORGANIZED_ACTIVITY_TIME` | K2 organized activity route objectively available in a source-owned window | `NONNUMERIC` baseline | `CANDIDATE_NOT_CURRENT__EVIDENCE_BLOCKED` |
| `C05-P4-INSTITUTIONAL-GATE-ELIGIBILITY-R1` | `P4 INSTITUTIONAL_GATE_TREATMENT` | K1 source-constituted institutional eligibility/gate status | `NONNUMERIC` baseline | `CANDIDATE_NOT_CURRENT__EVIDENCE_BLOCKED` |
| `C05-P5-COUNTERPART-CHANNEL-AVAILABLE-R1` | `P5 COUNTERPART_CHANNEL_RELATION` | K2 counterpart/channel route objectively available | `NONNUMERIC` baseline | `CANDIDATE_NOT_CURRENT__EVIDENCE_BLOCKED` |

The candidate keys are docket identities, **not** `MechanismRuleIdentity.rule_id` values and not production object IDs.

---

## C05-P1-REQUIRED-MATERIAL-ACCESS-GATE-R1

**Invariant body.** For a source-defined objective operation `operation_kind` that requires material resource/access relation `required_resource_kind`, a bound actor/position/context/time may qualify as `MATERIAL_ROUTE_AVAILABLE` only when type-compatible competent objective evidence proves the required access relation covers the asserted valid-time slice. Lack of such proof closes the derivation as unsupported; it does not prove `NO_ACCESS`.

**Calibration/configuration slots.** `operation_kind`; `required_resource_kind`; `access_relation_kind`; `coverage_interval_semantics`; optional exact nonnumeric quantity-band identifier; exact actor/position/context binding type. A future numeric threshold variant is outside this baseline and would require `RuleValueMode.NUMERIC` plus bound `CALIBRATION` authority.

**Evidence dependency.** Source/claim refs establishing the material prerequisite; evidence-status ref; normalized-mechanism ref; permitted-rule-shape ref; required-objective-inputs binding; proof/currentness contract; portability/currentness/historical-validity/negative ceilings; V3 stop boundary; exact rule-owner and causal-use authorities; measurement/identification/estimand dispositions as required by the source contract.

**Validity domain.** Only the source-declared operation, resource kind, actor/position binding, world/state version and valid-time interval. No transport across resource type, organization, jurisdiction or period without explicit portability authority.

**Intended witness shape.** Positive K2 requires a current type-specific access witness plus exact reachability/applicability. K1 is not implied. K3 performance/use is not implied. K4 continuing access requires a lawful Path A interval witness or Path B continuing-state support with complete invalidation coverage.

**Application gate.** Exact current R1 rule admission + exact D1 context + nonempty determinant fact set including the prerequisite declaration and access-state fact + exact evidence-witness refs. Missing/stale access closes unsupported.

---

## C05-P2-DIRECTED-OBLIGATION-IN-FORCE-R1

**Invariant body.** A directed obligation may be constituted for an actor/position only when a competent source-owned authority relation proves: authority scope, addressee binding, duty content, jurisdiction/context, and valid-time applicability. The rule may derive the exact K1 proposition `DIRECTED_OBLIGATION_IN_FORCE`. It does not infer performance, enforcement, sanction occurrence, subjective acceptance, or motive.

**Calibration/configuration slots.** `authority_relation_kind`; `addressee_binding_kind`; `duty_code_or_exact_content_ref`; `jurisdiction_context_key`; `effective_interval_semantics`; optional separately sourced `sanction_route_ref`. A sanction route may not be fabricated when absent.

**Evidence dependency.** Competent source rule/state establishing the obligation and authority scope; exact trace refs for source, claim and evidence status; exact rule-owner and causal-use authorities; measurement/identification/estimand dispositions where applicable; negative ceiling requiring explicit denial/revocation/termination or proved closed-world semantics for a negative obligation proposition.

**Validity domain.** Exact authority owner, addressee/position, duty content, jurisdiction/context and valid-time interval. No authority inheritance or jurisdictional portability by naming similarity.

**Intended witness shape.** K1 may be `PROVEN` only from competent operative source-owned rule/state plus exact binding/current validity. K2 permission/route is not implied by an obligation. K3 compliance/enforcement/sanction occurrence needs separate occurrence evidence. K4 persistence needs a competent interval or continuing-state witness and no defeating closing fact.

**Application gate.** Exact current R1 admission + exact operative authority-source fact + exact actor/position binding + valid-time coverage. Revoked, superseded or out-of-scope authority closes unsupported.

---

## C05-P3-ORGANIZED-ACTIVITY-WINDOW-R1

**Invariant body.** An organized activity route may qualify as objectively available to a bound actor/position only when a competent organization-owned schedule/state proves the activity exists, the asserted interval overlaps an operative availability window, and all source-declared objective applicability/reachability conditions are proved. The rule may derive K2 `ORGANIZED_ACTIVITY_ROUTE_AVAILABLE`; it never derives attendance or participation.

**Calibration/configuration slots.** `organization_ref_kind`; `activity_kind`; `schedule_window_type`; `applicability_binding_kind`; `reachability_condition_set_ref`; recurrence semantics if any. Numeric capacity or timing thresholds are not part of this nonnumeric baseline unless separately calibrated and authorized.

**Evidence dependency.** Exact organization/schedule source refs and claims; evidence-status and normalized-mechanism refs; permitted rule shape; objective-input binding; temporal/currentness and portability ceilings; current organization rule-owner plus causal-use authority; explicit recurrence/freshness semantics where K4 is requested.

**Validity domain.** One organization/activity type, exact world/state, applicability grain, and declared schedule interval. No inference from a published schedule to realized attendance.

**Intended witness shape.** K2 positive proof requires current availability + exact actor applicability/reachability. K3 requires a separate competent occurrence witness such as attendance/participation/transaction evidence. K4 recurring/ongoing activity requires owner-declared recurrence/continuing-state semantics and lawful currentness proof.

**Application gate.** Exact current R1 admission + schedule-state determinant + exact applicability/reachability determinant(s) + valid-time overlap. Closed schedule, failed applicability, stale witness or missing reachability closes unsupported.

---

## C05-P4-INSTITUTIONAL-GATE-ELIGIBILITY-R1

**Invariant body.** An institutional eligibility/gate proposition may be constituted only when the competent institution-owned gate rule is operative and every rule-declared objective eligibility predicate for the bound actor/position/context is proved at the asserted valid time. The rule may derive exact K1 `INSTITUTIONAL_GATE_ELIGIBLE`. It does not infer treatment receipt, service use, decision outcome, subjective uptake, or future success.

**Calibration/configuration slots.** `institution_ref_kind`; `gate_rule_code_or_exact_ref`; ordered `required_predicate_type_refs`; `binding_grain`; `effective_interval_semantics`; optional source-defined exception/override contract. Numeric cutoffs, if any, require a later numeric specialization with exact calibration authority.

**Evidence dependency.** Exact gate-rule source and claim refs; evidence status; normalized mechanism; objective-input and qualification proof contract; temporal/currentness/portability/negative ceilings; exact institutional rule-owner and causal-use authority; exact measurement/identification dispositions for each predicate source.

**Validity domain.** Exact institution, gate rule, actor/position class, context/jurisdiction and valid-time interval. No transfer to a different institution or gate family without explicit portability authority.

**Intended witness shape.** K1 may be proved from the operative gate rule plus complete objective predicate bindings. K2 route/reachability is separate unless the source rule explicitly constitutes it. K3 treatment/receipt requires separate occurrence evidence. K4 continuing eligibility needs lawful interval or continuing-state proof with invalidation coverage.

**Application gate.** Exact current R1 admission + current gate-rule determinant + complete predicate determinant set. Any unknown required predicate yields `UNKNOWN_NOT_PROVEN`/closed unsupported, not ineligibility.

---

## C05-P5-COUNTERPART-CHANNEL-AVAILABLE-R1

**Invariant body.** A counterpart/channel relation may qualify as objectively available only when a competent source proves the channel relation exists for the exact actor/counterpart/context, the endpoint/channel is operative for the asserted interval, and source-declared reachability conditions are satisfied. The rule may derive K2 `COUNTERPART_CHANNEL_AVAILABLE`; it does not infer contact, exchange, receipt, response, support, or subjective experience.

**Calibration/configuration slots.** `counterpart_role_kind`; `channel_kind`; `endpoint_binding_kind`; `reachability_condition_set_ref`; `interval_or_recurrence_semantics`; optional source-defined directionality.

**Evidence dependency.** Exact source/claim/evidence refs for counterpart relation and channel state; normalized mechanism; permitted rule shape; objective input binding; temporal/currentness and portability/negative ceilings; exact rule-owner and causal-use authority; measurement/identification/estimand dispositions where required.

**Validity domain.** Exact actor/counterpart pair or role binding, channel type, context/world-state and valid-time interval. No inference across counterpart, channel type or time.

**Intended witness shape.** K2 may be proved by operative channel plus applicability/reachability. K3 contact/exchange requires separate competent occurrence evidence. K4 channel persistence requires interval/continuing-state proof with termination/supersession/invalidation coverage. No social/psychological interpretation follows.

**Application gate.** Exact current R1 admission + counterpart-relation determinant + channel-state determinant + reachability determinant(s). Missing or stale channel evidence closes unsupported and produces no opposite fact.

## Terminal hold

All five candidates are concrete enough to bind later evidence and deterministic population work, but none is lawfully current on this branch. The smallest current-admission blocker for each is the same class of missing input: **no exact candidate-specific immutable evidence/authority packet and populated calibration/configuration binding was commissioned into C05 from which R1 could lawfully produce a `CURRENT_ACCEPTED` rule binding.** C05 records that blocker rather than inventing the missing authority.
