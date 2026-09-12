# ASTRA-C05 — WORLD POPULATION PLAN R1

Commission: `ASTRA-C05`
Scope: `SDTF_OBJECTIVE_RULE_BODY_AND_WORLD_POPULATION_R1_ONLY`
Disposition: `PASS__DETERMINISTIC_OBJECTIVE_POPULATION_DOCKET_SPECIFIED__NO_WORLD_WRITES_PERFORMED`

## 1. Boundary

This plan specifies **future deterministic objective-world population targets** for the five C05 rule candidates. It creates no production records and authorizes no world write.

A target becomes eligible for materialization only after all of the following exist outside C05:

1. the candidate-specific exact immutable evidence/authority packet;
2. a fully specialized immutable rule body/content hash;
3. an R1 `MechanismRuleAuthorityBinding` whose rule is `CURRENT_ACCEPTED` and passes `require_current_rule_admission`;
4. exact source-owned objective determinant facts at one `D1Context`;
5. any required type-specific current witness evidence.

Constitution currentness alone is insufficient. Missing inputs produce no record and no opposite fact.

## 2. Plan-level deterministic identity families

The following are **population-plan keys**, not runtime `ExactRef` identities and not current rule/application/fact IDs:

- rule target family: `C05-WPOP-RULE::<candidate_key>`
- admission target family: `C05-WPOP-ADMISSION::<candidate_key>`
- positive application target family: `C05-WPOP-APP::<candidate_key>::<source_grain_digest>`
- determinant target family: `C05-WPOP-DET::<candidate_key>::<determinant_role>::<source_grain_digest>`
- witness target family: `C05-WPOP-WIT::<candidate_key>::<K1|K2|K3|K4>::<source_grain_digest>`
- unsupported-control family: `C05-WPOP-NEGCTRL::<candidate_key>::<control_kind>::<source_grain_digest>`

`source_grain_digest` MUST be the lowercase sha256/`semantic_hash` of canonical material containing:

`candidate_key`, sorted exact source-object refs, exact actor/position/counterpart bindings as applicable, `world_id`, `state_id`, `state_version`, `valid_time_id`, and the exact specialized rule-content hash.

Changing any identity-bearing member changes the target identity. Sorting is by exact-ref key; there is no latest/default/fuzzy resolution.

The family strings above exist only to make the population docket deterministic before runtime work. A later authorized owner must map them to the exact record identities required by the already-adopted runtime contracts.

## 3. Bootstrap population targets

The minimum future bootstrap population, **conditional on lawful admission and real source-backed objective data**, is one positive source grain per candidate plus fail-closed controls. This is a lower-bound validation population, not a claim that such source grains presently exist.

| Target | Candidate | Source grain | Required determinant roles | Direct supported consequence | Control expectation |
|---|---|---|---|---|---|
| `C05-WPOP-P1-R1` | `C05-P1-REQUIRED-MATERIAL-ACCESS-GATE-R1` | actor/position × operation × resource × context × interval | `P1_PREREQUISITE_DECLARATION`, `P1_ACCESS_STATE`, and `P1_REACHABILITY_STATE` when declared by source | K2 `MATERIAL_ROUTE_AVAILABLE` | missing/stale prerequisite/access/reachability => closed unsupported, no `NO_ACCESS` fact |
| `C05-WPOP-P2-R1` | `C05-P2-DIRECTED-OBLIGATION-IN-FORCE-R1` | authority × addressee/position × duty × jurisdiction/context × interval | `P2_AUTHORITY_SCOPE_STATE`, `P2_ADDRESSEE_BINDING_STATE`, `P2_DUTY_RULE_STATE`, `P2_EFFECTIVE_VALIDITY_STATE` | K1 `DIRECTED_OBLIGATION_IN_FORCE` | revoked/out-of-scope/unknown binding => closed unsupported, no opposite duty fact |
| `C05-WPOP-P3-R1` | `C05-P3-ORGANIZED-ACTIVITY-WINDOW-R1` | organization × activity × actor/position × context × interval | `P3_ACTIVITY_DEFINITION_STATE`, `P3_SCHEDULE_WINDOW_STATE`, `P3_APPLICABILITY_STATE`, `P3_REACHABILITY_STATE` | K2 `ORGANIZED_ACTIVITY_ROUTE_AVAILABLE` | closed/stale schedule or failed/unknown applicability/reachability => closed unsupported; no attendance fact |
| `C05-WPOP-P4-R1` | `C05-P4-INSTITUTIONAL-GATE-ELIGIBILITY-R1` | institution × gate rule × actor/position × context × interval | `P4_GATE_RULE_STATE` + one exact determinant for every ordered source-owned required predicate + context determinant when not carried by predicates | K1 `INSTITUTIONAL_GATE_ELIGIBLE` | any missing/unknown required predicate => closed unsupported, not `INELIGIBLE` |
| `C05-WPOP-P5-R1` | `C05-P5-COUNTERPART-CHANNEL-AVAILABLE-R1` | actor/position × counterpart × channel × context × interval | `P5_COUNTERPART_RELATION_STATE`, `P5_CHANNEL_ENDPOINT_STATE`, `P5_REACHABILITY_STATE`, plus directionality when declared | K2 `COUNTERPART_CHANNEL_AVAILABLE` | absent/stale relation/channel/reachability => closed unsupported; no contact/exchange fact |

## 4. Exact population sequence per target

For each source grain, a future authorized population lane MUST execute this order without skipping gates:

### Step A — freeze exact input grain

Freeze exact immutable source refs and one exact D1 context:

`world_id | state_id | state_version | valid_time_id`.

No cross-context determinant mixing is permitted.

### Step B — resolve candidate evidence packet by exact identity

The packet must be the admitted specialization corresponding to exactly one C05 candidate and the same source/domain grain. Mutable authority selection is forbidden.

### Step C — require current R1 admission

The exact specialized rule identity/content hash must be paired with its exact authority binding and `CURRENT_ACCEPTED` selection evidence. Failure here stops population before any application/consequence target is materialized.

### Step D — require objective determinant closure

All determinant roles listed in the target table must be exact pre-existing objective facts or bindings owned by their competent upstream source. C05 does not synthesize missing inputs.

For P4, cardinality is deterministic from the admitted ordered `required_predicate_type_refs`: exactly one source-backed determinant per required predicate, plus the gate-rule state and any separately declared context/override determinant. The list may not be shortened to make a case pass.

### Step E — evaluate without inverse synthesis

If the invariant body is supported, the future evaluator may return a supported D1 evaluation carrying all exact determinants and evidence-witness refs. If unsupported or unknown, it must close the output. It must not synthesize the logical opposite.

### Step F — materialize application/consequence only on support

Only a supported evaluation under an exact current rule may create a current application revision and objective consequence fact. Its reverse-dependency lineage must include every direct determinant, exact rule application identity/version/hash, exact authority-binding/current-admission ref, and exact evidence-witness refs.

### Step G — populate assertion witnesses by type owner

K1–K4 witness material is type-specific. No universal witness record is created. Each target uses the already-adopted witness/currentness interface with the exact owner contract and witness-type refs.

### Step H — invalidation/redrive

When a determinant, authority, source binding, witness or relevant state changes, redrive only exact dependent applications. Unsupported outputs close; unrelated facts and historical provenance remain. No global actor reset is authorized.

## 5. Positive and negative control population

Every candidate must later be exercised against at least these **test/control vectors** before any production promotion. Controls are not production world facts.

1. `POSITIVE_COMPLETE_CURRENT` — all exact determinants current, exact admission current, compatible positive witness where required. Expected: candidate's direct K1/K2 target may be supported.
2. `MISSING_REQUIRED_DETERMINANT` — remove exactly one required determinant. Expected: `CLOSED_UNSUPPORTED` / `UNKNOWN_NOT_PROVEN`; no opposite fact.
3. `STALE_OR_REVOKED_WITNESS` — preserve source determinants but make required witness stale/revoked. Expected: no current proof/output.
4. `RULE_CANDIDATE_NOT_CURRENT` — all determinant data present but rule remains `CANDIDATE_NOT_CURRENT`. Expected: admission rejection before execution.
5. `CONTEXT_MISMATCH` — one determinant has a different world/state/valid-time context. Expected: rejection; no cross-context stitching.
6. `K3_PROMOTION_ATTEMPT` — K1/K2 determinants are complete but no occurrence witness exists. Expected: K3 `UNKNOWN_NOT_PROVEN` and no occurrence fact.
7. `K4_PROMOTION_ATTEMPT` — current K1/K2 proof exists but no lawful K4 Path A/B support. Expected: K4 `UNKNOWN_NOT_PROVEN`.
8. `EXPLICIT_NEGATIVE` — exact competent negative evidence is supplied under a source-authorized negative/closed-world contract. Expected: negative adjudication only for the exact proposition authorized; never inferred merely from absence.

## 6. Target cardinalities for bootstrap qualification

If, and only if, all five candidates are lawfully admitted and at least one source-backed positive grain exists for each, the minimum qualification docket is:

- 5 specialized mechanism-rule identities/bindings, one per candidate;
- 5 positive application targets, one per candidate;
- determinant sets exactly as specified above (P4 count is `1 + N(required predicates)` plus any separately declared context/override determinant; other counts are fixed by the admitted source contract);
- 20 K-class control rows in `COVERAGE_AND_WITNESS_MATRIX_R1.tsv` (five candidates × four assertion kinds);
- 8 control-vector classes per candidate, with no production fact emitted by a failing control.

These are qualification targets, not presently instantiated records.

## 7. Temporal-form and V3 firewall

Population must preserve the objective temporal form supplied by the competent owner (`EVENT`, `CONDITION`, `DIRECTED_RELATION`, `RECURRENT_ACTIVITY`, `TRANSITION`, or `ORDERED_HISTORY`). A standing condition or relation may not be converted into an event simply to reach V3.

C05 does not solve non-event ingress, OBL062, psychological transmission or OBL063. Any later V3 consumer receives only lawfully served objective D1 facts under the separate ingress contract.

## 8. Terminal readiness statement

The population docket is deterministic enough for a later authorized executor to know:

- which five rule candidates exist;
- which exact source/domain grain keys identity material;
- which determinant roles are required;
- which K assertion each rule can directly support;
- which missing/stale/currentness cases must reject before write;
- which identity changes force a distinct target;
- which boundaries prohibit psychological or inverse-fact synthesis.

No empirical value, source authority, current rule, application, actor fact or objective consequence has been invented to make the plan appear populated.
