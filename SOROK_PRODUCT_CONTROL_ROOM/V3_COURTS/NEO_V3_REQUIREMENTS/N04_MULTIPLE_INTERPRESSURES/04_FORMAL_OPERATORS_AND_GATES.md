# T03 / N04 — Provisional typed operator calculus, no arbitrary coefficients

**NOT NATIVE LAW.** The following are precise design candidates constrained by adopted CAN008 R2; concrete source classes, predicates, admissible rules, and state transitions require competent issuance. An operator denotes a causal *relation* with exact preconditions, effects and typed failure, not a psychological force or scalar multiplier.

## Data contracts (identity / ownership first)

`PersonAt(t)` = versioned actor snapshot references with CAN010 strivings/expectations, CAN011 mediators/practices/tensions, ADP015 counterpart-specific relationship state, ADP016 causal trace/memory (subject to privacy/access), ADP017 actor epistemic permissions, CAN009 embodied ability; each has owner, rule/version/hash, causal parents, effective interval, context/support constraints. `WorldAt(t)` = independently produced positions, material opportunities, counterpart actions, institutional power, supports, refusals, changed conditions; never read as desire. `Encounter` = actual ADP019/ADP010 or other owner-admitted precipitating event with visibility/feature scopes. `OperationAvailability` = PRESENT / RETAINED_BUT_CONTEXT_INELIGIBLE / SUPPORT_DEPENDENT / ACTOR_INACCESSIBLE / RETIRED / UNKNOWN; distinguish causal recruitability from declarative recollection. `CouplingTrace` = read-only candidate set and effect/interaction witness, *not* a new psyche store.

Each output links `event_ref, actor_ref, source_owner_ref[], relation_id, scope, context_match, supports, rule_id/version/hash, causal_use_role, effective_time, actor_access_class, uncertainty, decision`. Causal hypotheses remain distinguishable from actual admitted facts.

## Evaluation-local operators

| Operator | Preconditions | Concrete read/operation | Write/effect (evaluation-local unless owner separately grants) | Typed alternative |
|---|---|---|---|---|
| `RECEIVE_PARTIAL` | occurred event; named receivability rule and accessible features | select eligible *event features* for actor, not machine comprehensibility | `ReceivedFeature[]`; preserves not-seen/unknown features | VALID_EMPTY / DEFER_AMBIGUOUS / REFUSE |
| `RECRUIT_MULTIPLE` | eligible event significance, valid person-owner readsets | choose context-matching expectation/striving/mediator/practice/tension refs; each causal role independent | `Recruitment[]`; no dominance/weight unless independently justified | AVAILABLE_NOT_RECRUITED / UNKNOWN |
| `GATE_EXECUTION` | recruited operation, actual ability and material/social opportunity, support/access permissions | check needed tool, instruction, time, coactor and safety conditions; check distinguish `received` from `capacity` | `ExecutableAlternative[]` with `could_execute`; never modifies durable competence | SUPPORT_MISSING / WORLD_BLOCKED / ACCESS_MISSING / NO_CHANGE |
| `CO_DETERMINE` | two or more causally role-bearing recruited operations, explicit interaction rule | interpret one operation's significance *through* another (e.g. gratitude conditioned by debt expectation) and cross-rule context; do not sum values | ordered relation witnesses `ENABLES, INHIBITS, REINTERPRETS, COMPETES_WITH, REDIRECTS, REGULATES` with parent refs; preserve plurality | CONFLICT_UNRESOLVED / RULE_MISSING |
| `INHIBIT_EXPRESSION` | op recruited, specific inhibiting relation and scope | prevent public enactment while leaving internal operation and its parent history intact | expressive/attempt blockage and rationale, not `DELETE op` | DOES_NOT_INHIBIT / UNCERTAIN |
| `BUFFER_WITH_COST` | actual regulatory practice/support, eligible risk, valid material/time/social cost | reroute immediate consequence while charging only a governed owner-backed resource | CAN008 `BUFFER/DEFLECT` with cost proposal to owner; source episode unchanged | BUFFER_FAILED / COST_UNAVAILABLE / NO_CHANGE |
| `AMPLIFY_SITUATED` | compatible support relation/counterpart and scoped response rule | increase *effective opportunities, salience of a relation, or reachable candidate class*, not hidden amplitude | CAN008 AMPLIFY, provenance-typed downstream consequence | NO_SUPPORT / NO_CHANGE |
| `REROUTE_ACTION` | feasible alternate activity-route, actual needs, commitments and tools | select or preserve alternatives after competing conditions; no forced single choice | CAN008 `REROUTE/TRANSFORM` response and possible action intent | OPEN_CHOICE_SET / BLOCKED |
| `SUSPEND_REGULATED` | an ongoing conflict and actual reasons/conditions for postponement | hold incompatible orientations while deferring a decision, e.g. temporal/resource constraint | `DEFERRED_WITH_ACTIVE_CONTRADICTION`; no winner, no durable removal | FORCED_NOW / UNKNOWN |
| `VALID_EMPTY` | no lawfully significant recruitment/effect or unreceived/irrelevant event | preserve prior state exactly under replay | typed NO_CHANGE, zero causal effect | MISSING_RULE must not be mislabeled empty |

## Co-determination without fake convergence

A rule may run an **order-independent finite constraint evaluation**: start with raw admitted candidate refs, expose possible interpretations/recruitments, repeatedly add only licensed contextual relations, then close when no new warranted relation arises. If new relations can *retract* old ones or generate cycles, a bounded rule must explicitly resolve order/priority or report `COUPLING_AMBIGUOUS`; **do not** assume monotone fixed point, choose first candidate or hide a recursion count. No automatic collapse to a single 'dominant' disposition.

**Multiplicity witness:** Actor simultaneously wants to accept a work offer (sustenance), refuses humiliating conditionality (dignity), and desires to honor a helping relationship (care). A single acceptance/refusal act may belong to multiple activities, so the engine may return competing options, a conditional acceptance plan or suspension. No personality score and no inevitable virtuous act.

**Severance**: remove only a historically admitted relation linking prior exclusion to present interpretation while keeping present material facts constant. Subsequent typed recruitment/composition must differ if that relation was causal; unchanged is allowed if alternative independently authorized cause explains it. A changed adjective or narration fails.

**Fail-closed:** missing event, missing/read-only authority, actor/clock mismatch, hidden-memory leak, nonconvergent composition, absent target-owner signature, unlicensed stochastic draw or unsupported scientific relation → distinct `HOLD/REFUSAL`, never fabricated meaningful choice.
