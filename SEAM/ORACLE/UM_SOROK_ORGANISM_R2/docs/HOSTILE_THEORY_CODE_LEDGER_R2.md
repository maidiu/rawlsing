# UM-SOROK R2 — HOSTILE THEORY↔CODE CONSTRUCTION LEDGER

**Date:** 2026-11-19. **Status:** SOURCEFREE_RESEARCH_PROVISIONAL; author-reviewed working R2, NOT native SOROK owner integration, NOT independent psychological adequacy. **Governing user correction:** do not abandon hostile criticism, original-theory recovery and constructive conceptual advance while building; enact those in code together. Protected integration deferred per user's last sequencing.

## The thesis R1 did not earn

R1 was no longer only a psychology demo: it persisted several independently endowed actors, a shared world, bodily gates, acquired forms, recruitment, proposals, effects, parental entry and child development. But **having these components is not proof of their causal adequacy**. In particular, R1's engine could repeatedly misperceive historical cues as current, treat a stored associative connection as sufficient to override the target form's context, infer a shared relational competence from two encounters, and spontaneously install investment from one cooperative act. It could claim a socially meaningful person's history while ignoring objective ownership of the product of labor. R2 repairs selected instances rather than renaming the architecture.

### F01 — Historical event is not permanently present perception [REPAIRED]
- **Savage:** `world.cues` persisted everything and R1 `actor_access` iterated all cues. Past public events therefore became repeatable present sensations. The actor could indefinitely 'see' history even absent any memory record. History had been made equivalent to perception.
- **Recovered capital:** PRE-A0 §1: actual causal event != lived realization != psychic afterlife; ADP-010 separate exposure/encounter/access; ADP-016 nondeclarative trace; ADP-017 actor knowledge; original SOROK temporal continuity.
- **Code:** `world.add_cue` now records event clock and bounded `last_access_clock`; `constitution.actor_access` checks the clock before sensory/location/privacy eligibility. `runtime.cue` emits into the subsequent clock without forging prior experience. Historical `world.cues` and public-event receipts are preserved, NOT deleted.
- **Executable consequence:** R2 `test_historical_cue_expires_without_becoming_memory`: a heard event becomes unavailable after advancing three days; objective history remains; no memory is fabricated.
- **Open:** Long-term material signs (photographs, documents, continuing sounds), memory and mundane environment persistence require explicit positive owners/rules, not an arbitrary permanent cue.

### F02 — Association is not lawful cross-context transfer [REPAIRED]
- **Savage:** R1 association traversal recruited a linked target despite target-scope denial. The system therefore 'proved' transfer by simply writing an edge; context was overridden behind the issuer's back.
- **Recovered capital:** PFF R1 `SAME NODES != SAME PERSON`, context-conditional typed multigraph and scope; CAN-011 actor-specific sparse qualified mediators/practices; Lahire's conditional dispositions discussed in SOROK O05, not universal always-on traits.
- **Code:** `constitution._form_in_scope()` checks location and counterpart identity for direct AND edge-recruited targets; links retain their own contexts, separate from target scope. `development.CHANGE_RECRUITMENT_SCOPE` persists the explicit genealogical change. This is a bounded first step, not proven analogical transfer.
- **Executable consequence:** `test_recruitment_link_cannot_break_target_scope` denies SING despite RECRUITS edge, then changes target scope in a controlled synthetic actor and establishes changed eligibility. Historical runtime `test_cross_context_recruitment_becomes_real_after_new_life` separately exercises event-conditioned scope change.
- **Open:** No general learned feature analogy, distributional transfer, self-validating link typology, or native PFF attractor implementation.

### F03 — A dormant project must not summon its own stimulus [REPAIRED]
- **Savage:** R1 let *every* active project's `cue_terms` prime psychological-form recruitment before establishing whether that project was accessible. A contextual-only project could effectively cause its own opportunity.
- **Recovered capital:** Holzkamp's distinction between societal possibilities and the actor's actual premises; ADP-010 qualified exposure, SEAM/19 reproduction != possibility != access != appropriation; O05 object-directed activities rather than a universal motive selector.
- **Code:** seed only the independently eligible ongoing projects via `activity.eligible_activities(..., recruited_forms=())`; subsequent form and activity links may recruit further activities without circular bootstrap.
- **Executable consequence:** `test_unrecruited_project_does_not_summon_its_own_form`: no context => no SING, genuine present cue => the previously stored form and project become operative.
- **Open:** This provisional two-pass approximation lacks fixed-point semantics for more complex reciprocal activity networks and should not silently construct 'inner necessity' from any project's existence.

### F04 — A psychological person has *activities*, not a priority-weighted action menu [PARTIAL REPAIR]
- **Savage:** R1 `projects` were strings with `means` and priority; the same operation could be called a goal, and technical success would seem to fulfill its purpose. Leontiev's object–motive–action–operation differentiation was acknowledged in prose yet not encoded as operative distinction.
- **Recovered capital:** SOROK O05's scientific adjudication: *historically unfolding object-directed activity*, not an acquired skill, is the relevant unit; Leontiev's bitter candy case (action success, changed social significance), Sève's relations between acts, Dreier's conduct across actual contexts, legacy V3 unfinished strivings and metabolization.
- **Code:** new `activity.py::eligible_activities` and `record_activity_afterlife`; `Constitution.activity_links` and `development.LINK_ACTIVITY`, `ADD_PROJECT.motive` and `REORGANIZE_PROJECT` support historically changing relation between form, current activity, object, hypothesized motive and means. Runtime persists actor-owned performed-operation histories separately from world outcomes. Same operation may serve different projects simultaneously. It explicitly records `motive_realized='UNDETERMINED_BY_TECHNICAL_OUTCOME'`.
- **Executable consequence:** `test_one_operation_can_serve_competing_activities_without_motive_deduction`; actual runtime `test_lived_activity_rewires_recruitment_and_project_objects`.
- **Open:** Motive identification and the transformation of an activity's object are still coarse, sometimes seeded; no general purpose genesis or adequate developmental law. An activity node with a `motive` string is **not** itself the experienced motive.

### F05 — Material production is not personal possession of its fruits [PARTIAL REPAIR]
- **Savage:** R1's `WORK` simply increased workshop stock. It hid ownership, wage access and the fact that an ability to produce need not confer control over the result; nearly Marxist-looking nomenclature but no class mediation.
- **Recovered capital:** Governing Spirit material social reproduction, SOROK O05 Sève section on labor, class and access to the product, Erik Olin Wright's structured positions; SEAM/19, /26–29 on objective reproduction, differential access and recruitment of actual Others.
- **Code:** `world.py` now distinguishes institutional controller, material stock increment, wage transfer from steward's account, worker's separate account and `material_claims` with `worker_control_of_output=False`. Food has separately modeled world/site stocks, private holdings, purchases and material eligibility. Claim references are assigned only for actual owned-production transactions; blocked work does not conjure them. Actor psychological motive remains independent of the actual output relation.
- **Executable consequence:** `test_objective_labor_and_wage_are_not_technical_fulfillment` and activity-afterlife motive-underdetermination test.
- **Open:** Still a *tiny, illustrative* labor process, not a theory of capitalism, class mobility, institutional reproduction or empirically generated wage distribution. Whether the worker knows/approves of appropriation is a **different** actor-access/meaning question.

### F06 — Co-regulation can be objectively produced between two distinct beings [PARTIAL REPAIR]
- **Savage:** R1's dyadic cooperation recorded history but was not an actual joint power: two independent choice receipts plus a text field. It could not alter embodied conditions in a way irreducible to a narrator's impression.
- **Recovered capital:** PRE-A0 §8 caregiver bid/response, distress/comfort and scaffolding; the user's non-ideological mutually productive *unity of Them*; ADP-015 objective relationship vs each participant's experience.
- **Code:** independently selected infant `SIGNAL` and caregiver `CARE` can generate one *world-owned* `CONTINGENT_CARE_REGULATION` material effect, with infant body's comfort/arousal changed, real caregiver cost, and two distinct actor experience receipts. The field belongs to the world, no fused mind. No claim that this one conditional effect models human attachment science.
- **Executable consequence:** `test_mutual_care_has_world_field_bodily_effect_and_distinct_experience`, actual two-person performed event, durable objective relation and separate subjective paths.
- **Open:** Repeated attunement, misattunement, asymmetry, libido, care availability, relationship-specific histories, institutionally structured care labor and reciprocal long-run transformation remain mostly unwritten. This is **not** a complete model of love or attachment.

### F07 — Co-occurrence is NOT persistent capacity [REPAIRED R2-SECOND PASS]
- **Savage:** Early R2 itself automatically promoted two joint encounters to `RECURRENT_COORDINATION` in `joint_capabilities`. That falsely equated a count of world acts with a reliably acquired joint power.
- **Recovered capital:** Original PFF noncollapse `CO-OCCURRENCE != RELATIONAL ORGANIZATION` and `PERSISTENT RELATION != ATTRACTOR`; CAN-011 no automatic ruleless acquired state; PRE-A0's separable objective relational field vs individual afterlife.
- **Code:** the world now records `observed_patterns=['REPEATED_JOINT_ACT_OBSERVED']`; `joint_capabilities` remains empty pending a genuinely qualified positive rule. `constitution.compose` can refer to the objective recurrence **as observation**, not as presumed psychological or collective competence.
- **Executable consequence:** `test_repetition_is_not_stable_relational_power_or_investment`. The earlier R2/ R1 test asserting `RECURRENT_COORDINATION` was intentionally replaced, not falsely grandfathered as a success.
- **Open:** Need a real conditioned learning/coordination law to admit a continuing shared capability.

### F08 — Coactivity does NOT automatically install love, investment or recognition [REPAIRED R2-SECOND PASS]
- **Savage:** R1 and initial R2 heuristic created `RELATIONAL_INVESTMENT` after any single co-performed event. Exactly the caregiver-recognition ideology the user explicitly rejected had leaked into code.
- **Recovered capital:** PRE-A0 §§7–8: love preserves alterity, recognition is different from approval and co-presence; PFF noncollapse; personal self-understanding need not coincide with objective relation; user infant-caregiver is a **generative rumination**, not a fixed theory of universal attachment.
- **Code:** sourcefree heuristic no longer auto-installs investment or increases its strength from one event. It may instead form an explicitly tentative nondeclarative trace and actor-specific Other-model of **possible** future coactivity; actual relation remains world-owned. An explicit, appropriately qualified generative provider may propose investment later; current sourcefree runtime cannot claim such a law.
- **Executable consequence:** `test_shared_activity_yields_separately_owned_relational_afterlives` now verifies *absence* of automatically created investment, presence of separately owned traces and fallible models, and world-owned joint act. `test_repetition_is_not_stable_relational_power_or_investment` adds counterevidence against count-based promotion.
- **Open:** Actual historical constitution of libidinal investments and recognition, culturally and materially differentiated, not implemented by the trace heuristic. This is a **conservation of complexity**, not denial that love exists.

### F09 — An actor can bodily undergo an act without seeing its old-location public cue [REPAIRED]
- **Savage:** After a successful MOVE, an action cue was published at origin while the actor's location was already destination. R1 gave the mover no current cue and no structured bodily indication of their own action; the 'lived' layer was largely only ID references.
- **Recovered capital:** PRE-A0 objective event / lived realization / psychic afterlife; ADP-017 actor access, Holzkamp situated bodily agency, independent world; actor interpretation can remain false/incomplete.
- **Code:** `runtime.step` constructs `felt_enactment` as actor-specific proprioceptive candidate for the actor's own action **without asserting objective outcome knowledge**; stores `private_actor_experience_receipts` as distinct system-audit payloads while keeping them unavailable to the public expression input. Somatic effects on externally affected actors are separate and may be uninterpreted.
- **Executable consequence:** `test_actor_somatic_feedback_not_equated_with_public_event_cue` and `test_private_experience_receipts_not_sent_to_public_expression` plus infant-care receipt tests.
- **Open:** System-level causal audit is not subjective phenomenology, and private ledger retention requires later genuine actor-secret access controls on native integration; this is not a production confidentiality system.

### F10 — Maturation is not acquisition of language or adult ideology [PRESERVED + EXPOSED]
- **Savage:** A generic maturation equation could install culture by aging the body. A child might 'learn to speak' by waiting in isolation, falsely making linguistic psychology biology.
- **Recovered capital:** ADP-007 sparse viable organism, CAN-009 bodily capacity and limits; Luria socially mediated development; SEAM/21 variable acquired ontology; user's refusal of prepsychologizing newborn nature.
- **Code:** `organism.mature` increases **readiness ceiling** (`language_ceiling`), while actual `body.language` remains zero without acquired competence. `test_bodily_maturation_is_not_automatically_language_competence` rejects `SPEAK` after two years of clock passage with no language-acquisition rule.
- **Open:** Genuine embodied cultural language genesis is largely absent. This is a deliberate conspicuous gap rather than a fake happy-path pass.

### F11 — Independence of the Other also includes refusal, coercion and imposition [PRESERVED]
- **Savage:** A rule prohibiting imposed consequences absent consent would confuse authorship with power. Conversely, a caller-supplied consent Boolean for joint action is a forgery.
- **Recovered capital:** ADP-015 objective independent Other, CAN-008 pressure-flow, PRE-A0 power and recognition, Sève and Foucault on asymmetric relations, G2 prospective missing native performer.
- **Code:** R1 independently issued other policy in `IndependentWorldAuthority`; `IMPOSE` is a one-sided objective act, never marked as target's voluntary performance. R2 preserves that split while adding care as an independent, bodily consequential co-performance. Research process lacks OS-level malicious caller isolation.
- **Executable consequence:** inherited tests `test_no_bool_partner_consent_bypass_public_runtime`, `test_independent_partner_may_refuse_and_world_does_not_fake_joint_act`, `test_imposition_not_consent` still PASS.

### F12 — The ontology must not be redefined by the research code [PRESERVED]
- **Savage:** 'Build the organism' could create another personality truth store and inadvertently supersede native P3/CAN-011 and P2 material world rights. R1's SQLite store is an actual parallel research ledger: okay for experimentation, **not** a native replacement.
- **Recovered capital:** CAN-011 valid empty middle state and sparse qualified updates; P2/P3 actual sourcefree owner contracts; existing SOROK PROGRAMMA 144 functions / 38 seams / 83 gates; user instruction integration LATER.
- **Code:** R2 remains an isolated sourcefree owner with explicit grading; no protected code is written; all new psychic effects enter only the research actor's qualified event pipeline; existing `adapters.py` identifies future read/nonwriter seams. The paired PROGRAMMA source bank is candidate/documentary only.
- **Executable consequence:** inherited `test_zero_positive_native_rights` passes; no protected merge or native P2/P3 claim.

## The deeper theoretical finding produced by these repairs

**A person is not one state graph + a selector + an event updater.** The present productive unit is an ongoing historically constituted *organization of activities* in an independent material/social world, capable of context-sensitive composition of acquired practices, interpretive mediators, memory traces, object/motive relations and jointly generated possibilities. The state's topology matters, **but the relation between organization, activity, material ownership and future recruitment matters more**. R2 increases the number of those relations that have actual effects, rather than merely assigning evocative names. The embryo of the computational human is the process by which an already materially organized being changes what it can distinguish, attempt, care about, and organize with Others—and changes which parts of its own history can become operative next.

**Counterwarning against the other direction:** R2 still contains weighted action options, an offline heuristic and canned action alphabet; it is emphatically not a mature psychologically open-ended human. The next critique must attack *actual semantic production* of meaningful objects/purposes rather than using a universal template to install the same desire in every person. Nor should scientific humility prevent coding those provisional mechanisms when grounded by actor-specific history.

## Not fixed; explicit exposed science/engineering deficits

1. **R2 provisional psychogenesis remains narrow:** `semantics.py` automatically adds a project on one SING in some cases; it is not a general theory of object formation and may still overinfer a continuing motive. `NOT_FIXED` pending a better historically situated semantic construction mechanism.
2. **No actual provider run:** `model_provider.py` only an interface. No evaluated LLM for novel differentiated psychologies; offline heuristic is deterministic, not the promised semantic intelligence.
3. **Parent independent survey correspondence NOT FIXED:** keyed answer forms and synthetic seed fixtures remain. This is not a recovered empirical respondent psyche; no source-qualified sampling.
4. **Scientific validation NOT FIXED**: bodily rates, time resolutions, acquisition and transfer rules are research approximations, with unspecified comparative human fidelity.
5. **Incomplete same-world broad historical causality:** objective classes, property and institutions are caricatured; social reproduction is not yet a real population/production engine.
6. **No protected P2/P3/P4/P5/P6 integration:** user explicitly deferred it; standalone SQLite remains research, native P3 `MISSING_RULE`, actor G2 missing performer.
7. **No stable joint capacity formation law:** two cooccurrences no longer fabricate stable capability; a new qualified positive learning rule is still missing.
8. **No full affective/libidinal developmental mechanism:** genuine becoming-together beyond care co-regulation, unequal attention, memory, inhibition, recognition/authority and continuing relationships is not yet constituted. `NOT_FIXED`.
9. **No robust fixed-point mechanism for complex reflective project/recruitment networks:** two-pass seed/edge approach can miss or misclassify higher-order loops; provisional until richer compiler/interpreter.
10. **System-private lived audit not production confidentiality:** operator can inspect all actor receipts; no native access/secret isolation; do not equate with the character's knowledge or public exposure.

## Evidence and no-promotion

- **R1 source:** ORACLE draft [PR #1159](https://github.com/maidiu/rawlsing/pull/1159), exact R1 source commit `79dbbbc6a998739c6d8d782e8e73df7d297d6934`; R1 GitHub research code at `SEAM/ORACLE/UM_SOROK_ORGANISM_R1/`.
- **Protected source observation:** `integration/pre-main-reconciliation-r1` = `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e` at first R2 source review; canonical Oath read, paired CURRENT_PROGRESS reviewed; no HQ accreditation or protected receiving.
- **PFF original:** `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N033_ORIGINARY_PERSON_WORLD_PAX_MARXICA/CORPUS/ORIGINAL/91fd9f3214a8__26_PERSONAL_RELATIONAL_FIELD_AND_EMERGENT_ATTRACTOR_R1.md`, Git blob `91fd9f3214a8bfaac5e0323fa69f51722a7d9f52`.
- **PRE-A0 original:** `SOROK_PRODUCT_CONTROL_ROOM/PRE_A0_PSYCHIC_ARCHITECTURE_R1/00_PRE_A0_ARCHITECTURAL_BANK_R1.md`, archived branch blob `983d4133838ad9783eda1e9439ea97f2e1a68b4f`.
- **CAN-011:** `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_011_V3_MIDDLE_STATE/AUTHORITY.md`, blob `1ed04e62a363493bc7032a99139454a3126e6ea0`.
- **SOROK O05 science adjudication:** `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/P3_RULEBOUND_DEVELOPMENT_SOURCEPACK_R1/12_O05_FORMATION_VS_ACTIVATION_SCIENCE_ADJUDICATION_R1.md`, blob `dbca1502426974643f27a1058f56ac00a1398d88`.
- **SEAM/21 variable ontology:** dossier PR #1144, blob `e9f60f09933964fc7e3f7a224655cf46b1d9f477`.
- **Test execution:** use `python -m unittest discover -s tests -v` in R2 package; `tests/TEST_RESULTS_R2.txt` and `docs/R2_MACHINE_RECEIPT.json` store actual local author-side results and code manifest. These are NOT independent receiving or scientific accreditation.
