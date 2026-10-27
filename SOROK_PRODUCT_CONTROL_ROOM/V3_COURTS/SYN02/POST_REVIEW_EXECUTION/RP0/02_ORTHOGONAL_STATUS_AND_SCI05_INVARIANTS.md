# RP0/02 — Orthogonal truth, nochange and implicit SCI05 dependency

**Authority:** Proposed source-preserving adapter contract, NOT original CAN/ADP/SCI05 issuance. SCI05 postcall authorization and batch policy require competent original source/actor owners; the user fixed the N/N+1 recursion, not the failure-commit policy. Source cuts and exact code blobs in RP0/01. SYN02-S-R REDs G04 and G09 require this repair.

## Independent status axes — never collapse to a global event flag

| Axis and authority | Proposed exhaustive values | Meaning and source requirement |
|---|---|---|
| SourceQualification / original source | QUALIFIED, SOURCE_HELD, SOURCE_DENIED, INTEGRITY_FAILED, UNKNOWN | Authority to state particular sourced claim; not identical to event occurrence or response. Claim with changed hash is not identical. |
| WorldOccurrence / C8 | PROPOSED_ONLY, OCCURRED, NOT_REALIZED, NO_EVENT, NOT_YET_OBSERVED, OCCURRENCE_UNKNOWN | Objective actual source-owned action, including independent B, or positively qualified non-occurrence. NOT_YET_OBSERVED is epistemic, not non-occurrence. |
| ActorReception / ADP | RECEIVED, PARTIAL, NOT_WITNESSED, LATER_TESTIMONY, UNKNOWN, NOT_APPLICABLE | The actor's access, not objective fact, response, memory or psychological change. Later testimony is a new later-time reception. |
| RuleA / CAN008 | APPLIED_WITH_RESPONSE, APPLIED_VALID_EMPTY, HELD_MISSING_RULE, HELD_SOURCE, NOT_APPLICABLE_BY_ISSUED_RULE, INTEGRITY_FAILED | Immediate qualified evaluation, possible effectless outcome; cannot mint Rule T, belief, new skill or coactor action. |
| RuleT / CAN011 | COMMITTED_CHANGE, TRUE_NO_CHANGE_EVALUATED, HELD_MISSING_RULE, HELD_MISSING_SOURCE, DEFERRED, NOT_APPLICABLE_BY_ISSUED_RULE, INTEGRITY_FAILED | Genuine negative means an exact **issued/evaluated** Rule T with readset, source and clock. |
| ActorState / C9 | VALID_EMPTY, VERSIONED_PRESENT, UNAVAILABLE_PENDING_RECONCILIATION, MIGRATION_HELD | VALID_EMPTY is valid person history, not a default no-effect decision. |
| MemoryEvidence / ADP016/017 | ACTOR_ACCESSIBLE, PARTIAL_TRACE, BELIEF_WITH_SOURCE, ACTOR_UNKNOWN, ANALYST_ONLY | Trace is not automatically episodic recall; objective inaccessible data stays analyst-only. |
| ProductReadiness / C12 | CLEAN, WORLD_COMMITTED_ACTOR_HELD, SYNC_HELD, POLICY_UNDECIDED, FORK_HELD_INTEGRITY, SOURCE_HELD, NATIVE_RELEASE_HELD | Product operations only, never an actor's subjective condition. |

All names in this table are **proposed adapter statuses**, not silent amendments of existing enums. Direct S36 response_rules.py blob 8344ce9c10c536fb4a497e4620fe2f695211ef2e has RuleLookupStatus.FOUND/RULE_ABSENT/RULE_ISSUER_UNVERIFIED/RULE_BINDING_MISMATCH/REQUEST_INVALID and ResponseStatus.RESPONSE_COMMITTED/RESPONSE_EFFECTS_VALID_EMPTY/REFUSED/HELD. Its production registry is empty and absent Rule A returns REFUSED. Direct target_rules.py blob c33fc2a6a58efd422cb5289c080205b9e0183102 returns branch CREATE/NO_CHANGE/DENY and reasons including NO_PROPOSAL, INSUFFICIENT_ENACTED_HISTORY, TARGET_RULE_ABSENT, permission failures, NATIVE_ADMISSIBILITY_HELD. **Mapping is a pair (branch, reason, grade, issuer, actual evaluated readset), not branch alone.** NO_CHANGE/NO_PROPOSAL is NOT TRUE_NO_CHANGE_EVALUATED. INSUFFICIENT_ENACTED_HISTORY in test-only evaluation is not an original developmental rule. Response effects VALID_EMPTY is not a tested Rule T nochange. CAN011 v1 registers only V3MS_MEDIATOR, V3MS_TENSION and V3MS_PRACTICE and expressly permits VALID_EMPTY_MIDDLE_STATE.

## Decisive cross-axis invariants

- I01 Objective world event may occur with actor reception NOT_WITNESSED; this can change material opportunities even if actor does not remember it. For example an aunt works overnight caring for a child: C8 records witnessed independent source, household hours/resources change, the child has no direct episodic memory or unwarranted Rule A. When another person later tells the child, create LATER_TESTIMONY receipt at the later access clock; no retroactive eyewitness memory.
- I02 Source-qualified absence of event (NO_EVENT) differs from source denied, unknown, not yet observed, event held, no encounter, or actually evaluated nochange. No silent inference from missing row; unknown remains unknown. No actor-caused fictional B act simply because one of N's prose proposals named B.
- I03 Tool unavailable, task not encountered, temporary ineligibility, or inaccessible teaching do NOT imply durable CAN011 DORMANT/ENDED, lost ability, permanent attitude or actor failure. A formed practice may persist with today's operation gated by externally supplied tool/time. Unchanged adult with many material events is affirmative allowed history.
- I04 Distinguish actual externally enabled task performance from newly acquired personal operation: compare existing qualified operation, event-local activation, newly learned composed procedure, any owner-qualified functional relation, teacher/resource/help and authentic nochange **concurrently**. Observationally unidentifiable causal histories receive UNDETERMINED, never motivational or relational invention.
- I05 Valid-empty actor is permitted at seed, during life and at later cold/fork cuts. Historical V3 module names/numerics, default 50 baseline, age, type, demographic origin, hopeful parent, mandatory rupture, render prose and M26 writes may not populate it.
- I06 No Rule T = HELD_MISSING_RULE and no new psyche, even if C8 event is objective. A real issuer-qualified evaluation of Rule T with negative result = TRUE_NO_CHANGE_EVALUATED plus receipt with exact semantic readset and unmodified semantic hash. Administrative version may advance once for evaluated event, not a semantic-delta assertion.
- I07 B acted before C9 fault => real world remains; no duplicate B call; C9 partially pending => actor held; C12 missing mirror => SYNC_HELD, not CLEAN. V2 cannot write actor. No double C9 receipt or branch-epoch overwrite.
- I08 E2 must consume prior semantic value from actor store, not merely a receipt hash. Sever E1 operation value under unchanged E2 world/B/tool and show controlled difference/refusal. The software consequence does not alone demonstrate the psychological theory's empirical truth.
- I09 An actor-safe memory packet is recomputed from permitted features, not summarized omnisciently and redacted afterward. Hidden event IDs/total slots/gaps/numbers and unobserved B facts never leak directly or via derived prose/ordering.
- I10 SCI05 model-generated interpretations are proposals only until original owner admits them after the same call; they cannot self-authorize Rule T. Changed source, rule or permission on retry is integrity/authority fault, not nochange.

## Original temporal architecture and policy limit

User-settled: at **second half of call N** propose 3–5 conditional prospective events; C0/C8/independently acting B source process realizes or refuses actual events sequentially with genuine inter-event labor, care, material time and actor state updates, **no extra ordinary LLM call between them**; **first half of call N+1** allows fallible actor-accessible retrospective; **second half of that same N+1 call** proposes the next 3–5 conditional events. The integer 3–5 counts *proposals*, not guaranteed occurrences, witnessed episodes, memories or causal learning updates. The world can produce off-proposal coactor events; those need objective world receipts. Before irreversible multi-event activity, POLICY_UNDECIDED is a hard STOP until C6/C8/C9/C12 competent owner chooses PREFIX_CONTIGUOUS, truly reversible WHOLE_BATCH_ATOMIC, or proved INDEPENDENT_SUFFIX (with causal/no-gap policy). Never auto-select a strategy; B's completed care/work cannot be rolled back because a C9 row did not commit.

## SCI05 implicit same-call dependence: default set-wide quarantine

The first-half self-account and second-half proposals were generated by a *single* ordinary autoregressive inference. Even absent a dependencyOnSelfAccountRef, prospect semantics may depend on words the model just generated. An optional model-authored pointer, keyword absence, classifier guess or self-assurance cannot establish nondependence. Example: half1 “I understand that I am safe now” denied by SCI05; half2 “because I finally feel safe I ask for help” must be held even with empty pointer.

Algorithm, fully server-side, **no second ordinary inference**:
1. At the end of N+1 parse half1 self-account and all 3–5 half2 conditional prospects as separate candidate records; store raw envelope hash and permitted actor-input feature-set hash in protected server data. No prospects are forwarded to actual C8 action yet; default QUARANTINED_POSTCALL_SCI05.
2. Competent original SCI05 authority evaluates half1 against actual actor source, access, and eligible mental-act operands. Result ADMITTED with signed original ref, DENIED, HELD or INTEGRITY_FAILED. Text alone and sibling prospective rationales are not evidence.
3. If ADMITTED, requalify each prospect's source, world possibility and actor causal prerequisites independently using the resulting admitted actor state and batch policy. Do not backdate state to the model's draft. Where mental act carries enduring change, separately issued Rule T/C9 commit required.
4. If DENIED, HELD or INTEGRITY_FAILED: **HOLD THE ENTIRE SECOND-HALF PROPOSAL SET by default** as potentially semantically dependent, including prospects without pointer. Do not repair the model's propositions with a covert new ordinary call. Do not allow ghost next events.
5. An individual prospect may escape quarantine only with a distinct, pre-existing-world causal-independence certificate issued by competent SCI05/C8/ADP authority. Certificate must enumerate immutable independent source refs, actor prerequisites that do not depend on the proposed unadmitted interpretation, source-effective clock, basis of feasibility and negative dependency argument; it cannot rely on the model's own claimed independence. Undecidable semantics remains HELD. Independently sourced autonomous B action may still occur, but is not counted as validation of quarantined text.
6. Bind any released prospect to exact certificate hash and recheck source/time immediately before possible realization; altered source or scope invalidates permission. All denied/held outcomes persist as server-only receipts, not actor-memory facts.

### Minimal proposed actor-safe serializer

Input: individually sourced ADP access features with actor-access effective clock, scope, original source grade, accessible phrasing, confidence, dependency feature IDs and actual actor-permitted chronological cues. Compute transitive dependency closure BEFORE summarization; filter inaccessible/analyst-only first, then generate accessible discourse only from remaining information; never send raw event_id, proposal_id, branch/actor join key, source receipt hashes, world total-event count, failed slot index, gap marker, B's unobserved act or later certainty. Known actor misbelief can be represented as believed-on-sourced-testimony rather than narrator truth. If ADP feature/capability not issued, return HELD_MEMORY_SOURCE with no fictional recollection. Noninterference: remove one accessible feature and all direct/indirect dependent detail vanishes, including accidental counts, order and gap metadata. The projection must be read-only; V2 phrasing changes cannot alter C9 actor state.

## Finite adversarial contrasts — proposed, NOT_RUN

| Falsifier | Assert |
|---|---|
| F01 absent Rule T | WORLD_OCCURRED / actor HELD_MISSING_RULE; never TRUE_NO_CHANGE_EVALUATED |
| F02 issued negative Rule T | Readset/issuer exact, unchanged semantic hash, durable evaluated-nochange receipt |
| F03 real B unseen care | World consequence real; child episodic memory absent; later testimony separate |
| F04 external teacher/tool | Performance improvement without invented internal practice |
| F05 tool withdrawn | Operation retained but ineligible; not DORMANT |
| F06 source denied versus NO_EVENT | Orthogonal statuses and no event invented |
| F07 valid-empty lifelong actor | No compulsory psyche formation despite labor/care chronology |
| F08 SCI05 implicit text | Denied half1 with null pointer holds dependent half2 |
| F09 independent candidate | Independent source certificate necessary, otherwise held |
| F10 memory leak | Removing feature deletes hidden indirect count/order/prose |
| F11 C9 C12 crash | Stale mirror cannot CLEAN open or stale fork |
| F12 POLICY_UNDECIDED | No irreversible first batch act |
| F13 same-person E2 | Actual typed semantic operand consumed/severed, not hash-only |
| F14 original V3 archive | No old M19/M26 or narrator writes become C9 formed psyche |

Each positive needs producer -> exact typed output -> **first effective consumer**, source/grade and severed counterfactual, tested by an independent implementer/reviewer after original owners issue necessary rules. RP0 performs no local sourcefree tests or Mac/native tests.
