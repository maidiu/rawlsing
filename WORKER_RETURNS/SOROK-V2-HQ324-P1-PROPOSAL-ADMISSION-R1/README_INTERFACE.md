# HQ324 P1 — LLM developmental alternative admission (SOURCEFREE / NOT ADOPTED)

**Status:** `IMPLEMENTED_SOURCEFREE_CANDIDATE__AUTHOR_TESTS_ONLY__NO_CAN_ADP_SEMANTIC_ISSUANCE`  
**Seal:** `44f17132110274b07701bd4fea5bb1cbd10a5287`  
**Assigned branch:** `agent/rabochii-sorok-v2-hq324-p1-llm-alternative-admission-r1`  
**One accountable source-free worker.** No live LLM, production actor, source data, or native module imported.

## Reproduce

```bash
cd WORKER_RETURNS/SOROK-V2-HQ324-P1-PROPOSAL-ADMISSION-R1
python -m pytest -q tests/test_p1_contract.py --junitxml=evidence/p1_junit.xml
python run_demo.py --packet fixtures/packet_base.json --context fixtures/context_base.json \
  --policy fixtures/policy_design_weights.json --seed $(python -c 'print("0f"*32)') --coordinate 0
```

This package uses stdlib runtime functions; **pytest is only a test dependency**. `make_fixtures.py` regenerates the authored frozen, entirely synthetic packets. The frozen JSON (and hashes) must be inspected as implementation evidence, not as data about real people.

## Typed ingress: `P1_LLM_ALTERNATIVES_PROPOSAL_V1`

The model output is a JSON object with **exact** fields:

```
schema, epistemic_class = LLM_PROPOSAL, proposal_id, proposal_hash,
world_ref, context_hash, as_of, model {
  provider_label, model_version, prompt_version,
  prompt_sha256, sampling_record
}, candidates: [
  { candidate_id, family (OBSERVABLE_UTTERANCE |
     MATERIAL_ACTION_PROPOSAL | NONOCCURRENCE),
    parent_event_ref, time, place_ref,
    participants: [actor_ref...],
    prospective_participants: [{proposed_ref,role_ref,
      independent_history_ref,owner_proposal_ref,
      epistemic_class=NEW_ENTITY_CANDIDATE_ONLY}...],
    action_refs: [{actor_ref,opportunity_ref,act_kind}...],
    readset: [objective_event_ref...],
    prerequisites: [{kind,ref}...],
    interpretations: [{speaker_actor_ref,utterance,claim,
      claim_kind=ATTRIBUTED_UNVERIFIED_ASSERTION,
      claim_world_fact_ref=null,accessible_source_refs:[...]}...],
    courses: [{course_id,actor_ref,action_ref,description}...],
    possible_effects: [{target_actor_ref,description,
      owner_required=CAN011_EXTERNAL_OWNER,
      effect_kind=MAY_REVISE_PRACTICE | MAY_RETAIN_CONTRADICTION | NO_CHANGE,
      epistemic_class=HYPOTHESIS_ONLY}...],
    visibility:[actor_ref...], uncertainty
  }...
]
```

`proposal_hash=sha256(canonical(packet_without_proposal_hash))`; `context_hash=sha256(canonical(context_without_context_hash))`. The P1 canonicalization is sorted-key UTF-8 Python JSON, **not RFC 8785/JCS**. It is isolated research notation, **not** ADP019's native envelope hash. The model-supplied packet has no legal probability/weight, state mutation, admission/cursor, forged culprit, or other-owner authority fields anywhere; unknown fields reject. Source refs and role permissions bind only against the independently authored synthetic `P1_SYNTHETIC_CONTEXT_V1` fixture. `as_of` is a pinned snapshot time; prospective/future/retrospective events are not minted. A prospective new actor remains `DEFER` to a separate identity/history owner even when role refs are well-formed.

## Typed egress and decision precedence

`evaluate(packet,context,prior_proposals=None)` performs pure, fail-closed validation. Its result contains:

- top-level `decision: REJECT | DEFER | ADMIT | VALID_EMPTY`, `code`, `context_hash`, `proposal_hash`, `rule_ref/hash`;
- per-candidate `candidate_id`, `candidate_replay_hash`, `decision`, typed reason;
- an eligibility-only, sorted `eligible_entries[]` and `candidate_set_hash` (P1 domain-separated hash, **not** `ADP020_CANDIDATE_SET_V1`);
- `event_admission: NOT_PERFORMED`, `consumption: null`.

`ADMIT` here means **eligible as a P1 proposal alternative**, emphatically **not ADP019 `ADMIT` of a V3 event**. Distinct external-admission naming is a candidate seam discrepancy for HQ/B1 to reconcile. Invalid integrity rejects the whole packet. Explicit causal denials reject a candidate; unresolved required inputs defer. If *any* alternative defers, selection is blocked even when other alternatives are eligible—this conservative rule avoids quietly deleting a rival. An entirely empty or entirely rejected set returns `VALID_EMPTY`; no improvised event, first-candidate pick, invisible outcome or default lesson. A proposal with recognized prospective people defers instead of becoming a synthetic person.

Every qualified competing interpretation remains a **speaker-attributed utterance**. For the bike theft, material fact `THEFT-1` is separately admitted in the synthetic context, while the purported thief's identity is unknown; a peer's group-blame utterance is never encoded as perpetrator evidence. Independently generated actor and caregiver historical identities are typed and checked at the actual `people[actor].history_ref` binding; changing a history can alter **eligibility** but cannot force an interpreted psychological consequence. A caller can propose no lasting effect, internal contradiction, contested care/control meaning or nonoccurrence, never mutate another person's history.

`prior_proposals` is an optional immutable `proposal_id → proposal_hash` registry **supplied by a future owner**. The function rejects ID/content collisions but does not issue/persist native ADP019 receipts itself.

## Explicitly mock selection and probability provenance

`select_test_only(evaluation, policy, *, seed_hex, coordinate)` requires an **outside-the-LLM** authored policy fixture with exact nonnegative integer weight units for exactly the admitted set and signed-by-content `policy_hash`, `parameter_source=AUTHORED_DESIGN_HYPOTHESIS_TEST_ONLY` and `calibration_grade=PROVISIONAL_NOT_CALIBRATED`. Unknown weights, missing seed, policy mismatches and changed candidate set block; all zero weights produce `VALID_EMPTY`. Uniform selection is **not presumed**. A single positive alternative consumes zero entropy. Deterministic SHA-256 counter draws use rejection sampling to avoid modulo bias, but have the explicit label `ADP020_COMPATIBILITY_MOCK_TEST_ONLY`; not native ADP020 HMAC counter lineage/stream authorization.

The receipt records selected ID, exact sorted candidate-set hash, policy/source/grade, root-seed digest, static test stream, draw coordinate, counter and uniform ticket, choice replay identity, and `no_world_or_actor_mutation=true`. The **selected alternative remains noncausal**, including when its family is `NONOCCURRENCE`. A digest or metadata string is not a producer grant: this is a reproducibility demonstration, **not behavioral calibration**, signed authority, science-derived conditional probability, or production security against malicious operators able to rewrite policy fixtures. Raw root seed must be independently retained for replay; only its SHA-256 is emitted in selection receipts. The caller of this test API provides the seed and can replay exactly.

`replay_test_only(previous,evaluation,policy,...)` recomputes the mock receipt and refuses divergent outcome or identity. No sequence order of model-output candidate listing influences set hashing or the selected alternative.

## B1 provisional handshake; exact-owner boundary

| B-first shared concept | P1 sourcefree egress | Actual owner still needed |
|---|---|---|
| `BFirstScenarioRequest.world_ref, clock, actor_refs, activity_refs, actor_access_refs, actor_prestate_hashes` | Synthetic context `world_ref/as_of/people/histories/actor_access`; **no** authoritative actor-prestate hash | V3/world/ADP017 and B1 to reconcile exact schema |
| `BFirstCandidateDecision.candidate_id, event_admission` | `candidate_id`; **event_admission = NOT_PERFORMED** | ADP019/ADP010 determine actual occurrence after admitted external facts |
| `actor_response_rule_ref, recruited_source_refs, competing_influence_refs` | `null`, empty lists; candidate interpreted speech has its own attributed source | Concrete accepted CAN008 owner-bound positive rule absent |
| `response_effect_proposals, target_CAN011_update_proposals` | empty in consumption; **separate unconsumed `possible_effects` are hypotheses** | CAN011/MEDIATOR/TENSION and other exact durable owners must adjudicate |
| `probability_grade, model_proposal_provenance, negatives, rng_receipt` | `PROVISIONAL_NOT_CALIBRATED`, model packet SHA, typed per-candidate negatives, mock RNG receipt | ADP020 accepted RNG only with owner-issued rule/weights and real seed lineage |
| `BFirstAtomicReceipt` | **NOT_EMITTED** | B1/accepted owners validate exact joint event and state transaction/rollback/history |

The B1 source-free handshake is an **unadopted interface proposal** from the `03` source-graded program. It is not a license to implement CAN008/CAN011 in this worker branch. Genuine B1 integration requires adapting these research fields to actual accepted owner schemas, exact event/historical-person IDs, admissible producer signatures, material witness provenance, admission receipts, replay index, and independent effect approvals. The research-grade selection's `ADMIT` name must not be conflated with native ADP019 event admission.

## Source support and mismatches

- `03_SOURCE_GRADED_DELTA_AND_BFIRST_EXECUTABLE_PROGRAM_R1.md` @ `a563c4a14b4442b2beef7d652d1a1496249521a1`: B-first `BFirstScenarioRequest`, `BFirstCandidateDecision`, `BFirstAtomicReceipt`, D01–D10; candidate provenance ≠ native actors.
- `02_BIKE_THEFT_INTERPRETIVE_CONTEST_AND_LATER_DESIRE_RECURSION_R1.md` at sealed startup: same theft may support plural responses; independence and visibility, no compulsory one lesson, no automatic moral arc.
- `TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md` §22: LLM Pass 1 is candidate-only; event rules decide admissibility, no fallback; Pass 2 presentation cannot mutate.
- `ADP_019_V3_EXTERNAL_ADMISSION/AUTHORITY.md` §§7–9: externally asserted speech is not speech-content truth; same ID/different hash collision; only native external-admission court issues a real event.
- `ADP_020_V3_CAUSAL_RNG/AUTHORITY.md` §§5–12,15–16: qualified set first, explicit seed and registered streams; no random rescue; missing weights defer; ungoverned `Random()` prohibited.
- `ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.md` §§5–13: actual available/opportunity/encounter/exposure stages differ; exposure never implies belief/memory/response.
- Sorok 00C/00D process law: user-selected Browser agent, one author plus independent later I2; verified warm runtime, no silent host switching.

**Open owner questions:** ADP019 vs local P1 canonicalization profiles; ADP020-native candidate owner/eligibility receipt and seed lineage; whether multiple independent other-actor alternatives require mutually consistent joint opportunity evaluation at a new causal grain; how B1 reconciles deferred possible actors without manufactured life histories; accepted CAN008 positive actor rule still absent. These are HQ questions, not locally invented permissions.

**Authority and scope:** source-free research implementation only, no production V3 installation, original 35-source access, real model evaluation, native CAN008-positive effect, CAN011 mutation, actual ADP019 issuer, validated parameter calibration, real human psychology, or independent reviewer acceptance.
