# T01 / N01 — Needs, objects, motives, desires: source-grounded ontology and functional contract
**Status:** PROPOSED_THEORY / DOCUMENTARY_AS_BUILT_CROSSWALK / NOT_RULE_ISSUED / NOT_IMPLEMENTED.
**Evidence cut:** worker startup 2647a4cf25d8bb33a00471e1af9c5e58c2825efb. Other M cards are historical-report-derived, not direct original-code reads. This file does not confer CAN010/ADP authority.

## 1. The unit of explanation
Do not build a person from a trait inventory, an additive hardship number or a supposedly timeless list of psychological needs. A living person has embodied viability conditions *and* historically emerging needs realized, frustrated, redirected, and sometimes created through actual activity, objects, other people and social relations.

- **Embodied viability need:** a continuing condition of living/functioning (nutrition, shelter, sleep, bodily regulation, contact, protection), whose organismic consequences must not be equated with a narrated belief. Biological dependency is real, but its concrete satisfiers, distributors and social meanings are historically organized.
- **Socially developed need:** a dependence, concern or demand formed through relations and participation (recognition by particular others, doing something together, competence in a practice, play, affiliation, intimacy, meaningful contribution). Its form changes through experienced activity, not a trait seed.
- **Need-object:** a practically or imaginatively available *what/whom/relationship/activity* that could satisfy, mediate, deepen or transform a need. It is not merely an adjective or an automatically available consumer good. Objects have identity, access conditions, costs, other-agent consent and social meaning.
- **Motive:** the object-in-activity relation that organizes why this person pursues or continues an activity. Distinguish overt stated reason, practically demonstrated pursuit, and reconstructed motive; a single action can serve multiple motives, and the same object can serve different motives.
- **Desire:** an experienced or expressible attraction/want toward an object or condition. Desire need not be currently actionable, need not name the need, and may be altered by encounters, prohibition, fantasy and new concepts.
- **Support:** actually accessible resources, persons, practices or institutions permitting an activity or mitigating a need; not a passive positive modifier.
- **Available action:** an act currently feasible given actor capacities, rights/permission, tools, place, time, material resources, dependency and the consent/actions of others. A thinkable action and a possible action differ.
- **Effective care:** consequential provision of nourishment, protection, presence, repair, attention and enablement *as it reaches a recipient across actual situations*. Distinguish giver intention, performed work, reachable capacity, recipient's needs and recipient's registration.
- **Felt love:** a situated, imperfectly inferable experience of valued relational presence or commitment. It is not a direct readout of caregiving hours or parent intention; preverbal manifestations cannot be reverse translated into infant moral vocabulary.
- **Power:** uneven effective control over conditions/means of activity, others' time, access, rules, social standing or exit options; recognize coercive, protective, dependent and jointly enabling forms without collapsing them into one signed score.

## 2. Primary texts, narrowly and explicitly
**Leontiev, _Activity, Consciousness and Personality_ (project Portuguese translation, section on activity/personality):** he contrasts deriving activity from pre-given appetites with activity itself transforming needs and producing new ones; he makes the *system and connections of activities* central to personality, using the Gogol copyist to demonstrate that identical outward operations need not have identical motive-status. Reading basis: locally available PDF, SHA256 e65732b2cc91663d9d7aab437ab3c392f22c331aa4da06d7d78e11c71179df96. **Interpretation**, not a directly supplied computational law: instantiate motive-object relations from evidenced histories, never by dictionary mapping from one act to one hidden motive.

**Sève, _Man in Marxist Theory and the Psychology of Personality_, IV.I (acts, capacities, needs), pp. 304–330:** socially situated acts and acquired capacities compose a life; biological conditions of possibility should not be mistaken for the explanatory essence of developed personality (especially pp. 316–17). **Tension with a simplistic "needs-first" slogan:** *needs-first* is a demand to keep survival, dependency, care and situated concern primary in the generative account, not to subordinate activity to an immutable drive list. Competing possibility: emphasize the development of capacities and socially consequential acts rather than enumerated desires.

**Dreier, _Psychotherapy in Everyday Life_, chapter 2, esp. pp. 28–31:** persons are particular, partly efficacious participants in practices that precede them; feasible change depends on coparticipants and access to contexts. **Interpretation:** a need-object cannot be enacted unless a path of real participation exists.

**Elder, _Children of the Great Depression_, chapters 2–4:** economic contraction rearranges household maintenance, domestic labor, roles and relations. It does not prescribe one psychic conclusion for each child; household response mediates economic shock.

**Limits:** these texts warrant explanatory categories and research questions, not universal infant phenomenology or quantitative need weights.

## 3. Central parent–child case, decomposed
Objective facts may be simultaneously: (i) caregiver has enduring affectionate commitment; (ii) caregiver performs meaningful care when present; (iii) employment, travel, insecure hours or fatigue restrict available time; (iv) care available at moments of the child's need is insufficient; (v) another person sometimes supplies care; (vi) the child can experience both affectionate encounters and disquieting waits.

Neither "they didn't love me" nor "they sacrificed for me" follows at the early time index. The child may anticipate comforting reunions while bracing for evenings alone; seek a particular caregiver while acquiring competent reliance on another; show neither stable expectation change nor later memory. A felt contrast may precede concepts about work, wages, class or sacrifice. When explanatory language becomes available through family, school, union, religion or peers, *later* meaning can reconstitute the significance of that earlier experience without altering the earlier objective event.

**Competing causal accounts requiring differentiation:** (A) insufficient time/response is primary; (B) relationship repair/quality stabilizes reliable expectation despite time scarcity; (C) co-caregivers materially meet the need and alter object of pursuit; (D) material depletion affects routines indirectly through caregiver distress rather than hours; (E) practical scarcity is registered only locally and leaves no durable emotional disposition; (F) apparent retrospective grievance is later reinterpretation, not evidence that an infant believed it. The system must allow all six where supported, and withhold judgment otherwise.

## 4. Typed nonnumeric operator candidates (NOT scientific rules)
`derive_need_opportunity(actor_state, bodily_condition_observation, household_resources, resolved_context, history, time_window) -> NeedOpportunityAssessment`: include need kind, urgency as *observed/not-observed/indeterminate*, candidate attainable objects with permission/actor identity, evidence and noncoverage. Do not deduce desire from hunger or "low income".

`resolve_object_engagement(actor, motive_object_candidate, situated_action_options, coactor_actions, costs, outcome_evidence) -> EngagementRecord | NO_ENCOUNTER | BLOCKED`: expose whose action/decision rendered the object accessible; do not write motive from an LLM proposal.

`adjudicate_motive_formation(prior_object_history, performed_acts, achieved/failed objects, available_social_meanings, comparative_contexts, evidence) -> HypothesisSet | ABSTAIN`: hypotheses can remain alternatives; only competent psychological rule owner defines persistence and epistemic update. One isolated act is insufficient to fix a motive.

`record_dual_care_evidence(child, relation_id, episodes, child_accessible_cues, support, times) -> RelationEvidence`: preserve separable channels provision, absence, experienced safety, recognition and unknown; do not collapse into secure/insecure attachment labels.

Possible *first consumers*: N06's opportunity/routine resolver, N03/N04's event-response application, N08 impression/no-change, N07 multi-actor encounter; native actor C9/C12 only after source/authority. No psychological update simply from class category, parental work, gender, age or survey averages.

## 5. Historical candidate comparison (documentary, NOT direct V3 code)
| Candidate source (TD-R05/M-card) | Coverage grade | Proven capability / precise missing law |
|---|---|---|
| M02 `Capacity; update_capacity; update_health_drift` (`v3/core/state.py`, `v3/systems/capacity.py`, `health_drift.py`) | INFRASTRUCTURE_ONLY | Material capacity tracked annually; no proven situated object-access/care-recipient mediation. |
| M03 `PsychologicalCapacity; derive_vitality_profile` | PARTIAL_WRONG_MEANING | Internal regulatory dimensions, not a rights/objects/relations model; reject magical psyche-capacity-to-need mapping. |
| M04 `ReproductionConstraints; update_reproduction_constraints; _derive_hostage_index` | INFRASTRUCTURE_ONLY | Household/debt/work constraints; hostage/expression indices cannot issue felt meaning. |
| M15 `NEED_AXES; derive_child_expectation_baseline; infer_parent_baseline_and_regime` | PARTIAL_WRONG_MEANING / CONFLICTING DEFAULT | Typed needs and expectation scaffolding; missing behavior mapped to 50/50/50 and default "hopeful" — invalid unobserved-care inference. |
| M16 `StrivingObject; spawn_striving_objects_for_age; update_existing_objects; update_striving_step` | PARTIAL_WRONG_MEANING | Durable pursuit object useful; age-spawn must be replaced by history/availability/recognition-conditioned formation, not chronological psychological truth. |
| M22 `child_model; backbone_state_from_identity; PASS1_SYSTEM` | PARTIAL_WRONG_MEANING | Model of limits/taboos used in prompt; not a demonstrated endogenous preverbal meaning-development law. |
| M23 `autonomy_drive/safety_drive; autonomy_safety_micro_drift` | PARTIAL_WRONG_MEANING | Existing changes and trace but default drives and global drift not evidence of specific experienced needs. |

All function identities here are **reported by TD-R05 direct-archive audit**, commit 25830fe7462bb9e29bc4087e6ae14f3f84cec377, blob dfcc7e4fc7b6e907218d7a368ceb9d269a49206d; they are not independently recertified line-by-line. A direct fetch of `v3/core/state.py` on both worker startup and that historic commit returned 404. Coverage grades refer to *Neo-V3 requirement*, not proof of current code absence.

## 6. Falsifiers, scope, and owners
- **Adversarial positive:** loving parent works nights, third-party care is reliable, child shows comfort at reunion and also frustration at bedtime. Expected: dual evidence, no forced global judgment.
- **Adversarial no-change:** parent unavailable for a shift that falls entirely during a child's enjoyable, supported activity; no registered disruption. Objective schedule changes; psychological state legitimately unchanged.
- **Source-edge severance:** remove grounded access/permission or coactor availability; identical "motive" output from the same psychological initializer falsifies claimed object-conditioned causation.
- **Negative transfer:** interest/agency demonstrated in one practice must not automatically generalize across unrelated contexts.
- **Owner gates:** CAN010/ADP decides psychological meaning/transition if authorized; household/time/object sources are SDTF and competent world/actor owners; no native rule, numerical law or C9/C12 acceptance is issued here. Engineering owner must locate real source symbols and present person consumer; X01/X05 own direct old-code inquiry, not T01.
- **Discriminating evidence:** prospectively recorded care episodes, actual work rosters, co-caregiver actions, child task/activity participation, repeated across-context behavior and later speech, while respecting interpretation uncertainty. Post-hoc adult reports alone cannot specify the child's historical mental vocabulary.
