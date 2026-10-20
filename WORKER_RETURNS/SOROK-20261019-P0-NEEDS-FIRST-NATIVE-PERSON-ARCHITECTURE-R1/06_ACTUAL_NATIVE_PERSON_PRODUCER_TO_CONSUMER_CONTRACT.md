# P0 / 06 — native person producer→consumer contract: source and effect custody
**Status:** a build specification with verified *existing exact API names* and explicit **PROPOSED COMPOSITION ENVELOPES**. It is not an adopted schema, human psychological model, issuer, license, actor or actual person.

## Found APIs, not imaginary engine
At C9R authored sourcefree return `6fa2939972ce5a2c0cc4f2b033946b276f1c2934`:
- `candidate.identity.ingress_actor(raw, *, as_of:int, resolver: ActorSourceResolver | None)`, blob `ac87f640b58c00e2a2cfa178f4ac0eaf40d3fc5a`; `ActorSourceResolver.resolve_actor_source(actor_id, source_ref, source_hash, as_of)` required for non-TEST_ONLY native identity. Reject psychology embedded directly in identity record.
- `candidate.events.ingress_event(raw, *, as_of:int, last_time:int, prior_event_hashes:frozenset[str], focal_actor_id:..., owner_resolver:OwnerReceiptResolver|None)`, blob `5d8ef2c440efbafef98502edb53216328a40c7f1`. Native grade resolves `OwnerReceiptResolver.resolve_owner_receipt(owner_ref, owner_receipt_ref, event_id, as_of)`. Identical label/hash with no resolver is not native evidence.
- `candidate.pipeline.run_candidate_path`, blob `cb0350909dedd9f7159dce145ba216b211a8185c`, exact keyed arguments include `store, actor_raw, event_raw, conditioning_sources, response_registry, target_registry, authority_id, rule_version, rule_content_hash, as_of, permitted_issuer_refs, other_person_offer_ref, material_opportunity_ref, enacted_history_refs, later_consumer, later_as_of, target_permission, action_owner_receipt, expected_act, actor_resolver, owner_resolver, occurrence_resolver, native_positive_claim`. It is **NOT by itself native-permitted**; current production registries are empty and guard denies native positive.
- `candidate.response_rules.lookup_rule/evaluate_response`, `target_rules.evaluate_target` with `TargetBranch.CREATE/NO_CHANGE/DENY`, `transaction.CandidateStore.commit` full sealed record, `later_action.read_target_for_later_action` (blob `ed09b659ad6e53f347527feedee66522eac26523`), `action_admission.admit_performed_action` (blob `01220ba2ceea8e4c17a6228868db8df5cc3211a2`).
- `rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound.admit_available/opportunity/encounter` (blob `fa169dbb525475c17b2495a5b35aa300aa809881`) must consume actual OBL056 role-accepted evidence; installed OBL056 source registry is zero positive, native not established.
- `rawlsing_next.m6_actor_safe_expression.evaluate_actor_safe_ingress` and `project_actor_safe_entry` (blob `74d9701cdc7dabccf61eb5089498db290c1efd9c`) guard actor-access-only V2 envelope, not full rendering.

## Proposed minimum connecting contracts (NOT production schemas)
```text
QualifiedWorldSlice {
  world_owner_ref, source_edition_and_permission_ref, N11_release_ref,
  N12_wake_ref, as_of_world, structural_positions[],
  feasible_opportunities[], unknowns[], provenance_refs[]
}

HistoricalActorRoot {
  actor_id, birth_clock, root_world_ref, subject_owner_ref,
  developmental_owner_and_rule_version, parent_actor_refs[],
  own_admitted_prior_event_refs[], independently_generated_practices[],
  contradictions_and_unresolved[], own_memory_access_view_ref,
  source_generation_proof_ref, version, owner_signature_ref
}

CurrentPersonAndEvent {
  actor_root_ref, actor_current_snapshot_ref,
  world_snapshot_ref, other_actor_offered_action_ref,
  exact_admitted_E1_ref, actor_perceived_event_ref_or_VALID_EMPTY,
  CAN008_current_rule_and_causal_use_ref, CAN011_target_owner_grant_ref,
  as_of_occurrence, as_of_actor
}

OwnerEffectEnvelope {
  target_id, target_owner, source_event_ref, response_ref,
  before_state_hash, target_rule_ref, grant_ref,
  decision_CREATE_NO_CHANGE_DENY, after_state_hash_or_none,
  commit_clock, canonical_receipt_hash, causal_parents[]
}

PerformedE2 {
  target_id, committed_state_hash, consuming_actor_id,
  independent_actuator_owner, independently_admitted_occurrence_ref,
  performed_time, world_response_ref_or_NO_EFFECT, receipt_ref
}

C12PersonContinuity {
  root_world_ref, root_actor_ref, genealogy_refs[], branch_id,
  canonical_c8_event_cursor, durable_owner_state_refs[],
  actor_memory_and_epistemic_view_ref, other_actor_refs[],
  independent_agenda_ref, later_E2_receipts[],
  actor_safe_V2_envelope_ref_or_NONRENDERABLE,
  version_vector, replay_provenance_refs
}
```
These are **logical interface content requirements** for implementers to map onto existing exact canonical owner types and custody. They are not permission-bearing receipted native structs. Do not mint these new record names as a shortcut around CAN008/CAN011/ADP019/N11/N12.

## One lawful causal history, with concrete acts and alternatives
**Pre-contact:** At world time T0, qualified Pyat selects source-backed situated household/work position `W0` under real host/source/permission. Competent V3 person former generates actor `A` from eligible childhood experiences, household, older parent `M`, counterpart `F`, work and relationship histories, with actual source/owner receipts. `M` and `F` have independent histories and differing interpretations of a prior material conflict. The actor `A` maintains an acquired practice P and a contradictory expectation Q; actor may not currently recall origin of Q. A structured precontact root remains shared; never one adult prewritten plot with a plausible label. Identical inputs replay identical root; alternative original material opportunity generates a different bounded developmental trajectory without replacing a person's essential humanity by class determinism.

**Ordinary E1:** At T1 actor A encounters an actual offer from distinct actor B at a workplace, with opportunity status under ADP010 and **separately established contact**, not same building. An independent owner issues authentic ADP019 E1 occurrence with source and observed `B` act. It may not be inferred solely from A's belief about B or user's requested scene. C8 authenticated append witnesses both world event and actor-specific availability (not necessarily understanding).

**CAN008/RULE_A:** At T2 (T2 >= T1), `ingress_actor` reads A's owner-bound actor state and `ingress_event` verifies E1 and C8 journal. The current concrete, independently competent CAN008 rule consumes A's existing real enacted practice history, opportunity, B's separately declared act, memory accessibility, current material constraints and rule scope. Its alternative responses could be (i) receive and provisionally undertake a bounded shared task, (ii) hear but decline, (iii) fail to receive (VALID_EMPTY). This is a *possible test family*, not a ruled prediction. The rule must preserve multiple streams, contradiction and partial uptake. Response cannot directly alter durable belief or report introspection as objective fact.

**CAN011/RULE_T:** If uptake yields a proposed continued practice, distinct current CAN011 target owner with exact grant checks authorized change to one practice/expectation/relationship. `CREATE` commits a full sealed durable record with objective E1 causal parents; `NO_CHANGE` preserves E1 and unchanged target; `DENY` returns typed refusal and no ghost target. Neither immediate CAN008 reply nor narrative response alone is durable. The exact stored target record survives process death and is read back by the `LaterActionConsumer`; different time and independent actor cause are retained.

**Later performed E2:** At T3>T2, A independently executes an actual bounded action, conditional on work hours, material resources, B's availability and competing agenda, and a competent actuator/event source establishes that the action **occurred**. The E2 receipt includes consumed committed target hash and commit lower bound, independent actuator/occurrence and time. A plan or model utterance alone yields `HELD`. Objective world change, if any, is separately admitted and `sdtf_r4_world_response_redrive.request_r4_invalidation_rederivation` may request recomputation, not manufacture it.

**Continuation and user surface:** At T4>T3, C10/12 reads exact event ledger, target owner's durable state, independently advancing B/M/F histories, current world, and epistemic-access index. It exposes only actor-safe V2-accessible consequences. The user's branch may perceive that A now schedules a meeting independently, or says nothing due to inaccessibility: both are real conditional results. Later A may reconsider P under new life events without rewriting E1/E2, while user fork B remains independent of user fork A; narration is a bounded renderer, never a state commit.

### Call-order sketch — composition pseudocode, not runnable with current native zero registries
```python
# BUILD-PLAN PSEUDOCODE, no fabricated accepted inputs or signatures.
world = pyat_owner.get_current_qualified_world(as_of_world)    # N11+N12 required for native
root = v3_qualified_person_former.from_historical_sources(world, valid_genealogy)
actor = authentic_actor_resolver.resolve(root.actor_id, root.version)
enc = obL055_oee.admit_encounter(competent_role_receipts, real_contact)  # illustrative adapter
E1 = adp019_owner.admit_external_occurrence(enc, actual_action_B)       # distinct current owner
c8_owner.append_verified_occurrence(E1)                                 # trusted exclusive journal
result = c9r.run_candidate_path(
    store=native_bound_store,
    actor_raw=actor.current_C9_actor_identity_record(),
    event_raw=E1.C9_event_witness_record(),
    conditioning_sources=actor.current_owner_readonly_sources(),
    response_registry=competent_can008_current_rule_registry,
    target_registry=competent_can011_current_target_registry,
    authority_id=issued_CAN008_id,
    rule_version=issued_CAN008_version,
    rule_content_hash=issued_CAN008_hash,
    as_of=T2,
    permitted_issuer_refs=competent_issuer_refs,
    other_person_offer_ref=B.owner_bound_actual_offer_ref,
    material_opportunity_ref=world.actual_eligible_opportunity_ref,
    enacted_history_refs=A.source_bound_real_history_refs,
    later_consumer=named_committed_target_consumer,
    later_as_of=T3,
    target_permission=competent_CAN011_grant,
    action_owner_receipt=independent_E2_performed_receipt,
    expected_act=issued_eligible_act,
    actor_resolver=authentic_actor_resolver,
    owner_resolver=authentic_adp019_resolver,
    occurrence_resolver=independent_performed_owner_resolver,
    native_positive_claim=True
)
# Native-positive execution remains HOLD until all competent current registries and
# sources actually exist; sourcefree machinery may never set native success by fiat.
if result.stage("performed_action") is a_real_admission:
    c10.consume_exact_readset_then_c12_continue_actor(result)
else:
    c10.consume_only_lawful_occurrence_and_no_effect_or_hold(result)
v2 = m6_actor_safe_ingress_from_issuer_and_access(c12_state)  # no direct world-to-V2 jump
```
The actual C9R function signature is verified as listed; names `pyat_owner`, `v3_qualified_person_former`, `adp019_owner`, `native_bound_store`, `c10`, and their methods are **placeholders for non-existent/unverified orchestration** and must NOT be presented as imported runtime.

## Negative and no-effect matrix
| Same intended consumer | Change exactly one upstream edge | Required result |
|---|---|---|
| C4 childhood → C9 actor | Remove source owner/authentic developmental parent, retaining same label/hash | Native actor ingress rejects `SOURCE_UNRESOLVED`; no person |
| ADP010 → E1 | Supply co-location instead of independent contact evidence | No ENCOUNTER; no E1 from contact; no actor uptake |
| C8→C9 E1 | Forge event owner or ADP019 receipt, replay old anchor | Typed missing witness/refusal; no target; journal unchanged |
| C9 RULE_A | Rule currentness revoked after lookup before apply | Response refuses; no durable CREATE |
| C9 RULE_T | Change permission or before-state at commit | Atomic rollback; canonical occurrence remains if already admitted |
| CAN011 NO_CHANGE | Valid event but no target-altering effect | E1 remains, target store/hash unchanged, later E2 cannot claim new practice |
| E2 | Return counterfeit body plus real digest, or self-actuator/old clock | `CONSUMER_READSET_MISMATCH` / performed HOLD, no occurrence |
| V2 | Inject hidden structural prior as visible actor confession | `ActorSafe...` refuses or nonrenderable; no retroactive truth |
| A0/C12 | Same historical root, different user wording alone | Same pre-contact canon; only lawfully admitted post-contact branches may diverge |
| Other actors | Nested future-child metadata or inferred F_EXISTING with no admitted parent history | No generated child/second parent; G18/M2 exact HOLD |

## Schema ownership and permission table
Pyat world = Pyat current source+N11/N12; historical actor = original V3/ADP person/parent science and executor; E1 occurrence = ADP019/C8 trusted event; immediate response = CAN008 R2 competence+runtime; durable mediators/practice = CAN011 (needs CAN010, relations ADP015, memory ADP016, access ADP017, rupture CAN012 each own effect); E2 = distinct actual performer+occurrence, no self-attestation; world change = objective world owner; V2 = actor-access owner with renderer constrained, not causally sovereign; C11 weld = separate joint permission. P0 cannot issue any of these identities.
