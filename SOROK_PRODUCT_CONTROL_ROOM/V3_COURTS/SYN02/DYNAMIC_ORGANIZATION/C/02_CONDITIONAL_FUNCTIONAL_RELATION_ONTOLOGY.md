# SYN02-C / 02 — Typed conditional functional-organization ontology

**Status:** SPECIFICATION_ONLY / proposed abstract types and algorithms / **not existing executable names**, not a fourth CAN011 registered kind, not admitted developmental psychology. Proposed end-person jurisdiction: C0 qualified world → C4 historically situated actor + C8 independent event → C9 Rule A immediate response, separate CAN011 Rule T → C12 continuity/V2 actor-limited account.

## 1. Semantic invariant: the unit of analysis is a situated activity, not an all-to-all “psychic connectome”

An “operation” is an identifiable mode of transforming context-available information, material/practical action or actor state under a qualified owner. It may be a practical procedure, orienting discrimination, use of a concept, anticipation, recollection-sensitive response, inhibition, or an activity-linked action schema. Needs, motives, affect, memory objects and enacted practices are **not automatically interchangeable generic graph nodes**. Their owners govern whether and how they may participate as typed inputs/conditioners/outputs.

A **functional relationship** is a *conditional, source-and-history-warranted rule of organization* whereby one eligible operation/output/context **recruits, inhibits, orders, constrains, routes through or transforms the use of another** with a different resulting later practical possibility or evaluation. Relation identity is always actor-/scope-/time-/rule-specific; a relation can be stable, temporary activation, contextual, dormant or genuinely invalidated.

A relation is **NOT** any of: two high scalar scores, correlated co-occurrence, same noun in narrative, inherited structural demographic fact, social network link copied into psyche, an emotion linked by analyst intuition, or an external caregiver doing all the work. “A influences B” is only a meaningful candidate after the *direction, operand, condition and observed/practicable output* are specified. Prefer evidence of an *acquired coordination/procedure* over invented edge identity when the operation level suffices.

## 2. Identity domains and ownership (type level, no production code)

| Typed identity | Content / exclusive source meaning | Why it may not be silently rewritten |
|---|---|---|
| ActorRef / ActorBranchRef | The **same actual actor** and immutable history branch; identity/owner from C4/C8/C9/C12 | An independent B actor cannot be a synthetic limb of A. |
| ActualEventRef / EffectiveTime | Owner-admitted event with exact hash, chronological parents, what occurred vs was proposed | N call's suggested event is not occurrence; memories cannot rewrite event facts. |
| ObjectiveSupportRef | Tool, resource, real parent/aunt, teacher, employer, institution, material opportunity and ownership in world | C8/world/ADP019 owns; no duplicated implicit “helper motive” inside A. |
| ActorReceptionRef | What A actually encountered/could participate in, with source and access | Objective love/time/job truth does not entail child's reception. |
| OperationRef | Scoped practical, attentional, interpretive, regulatory or response operation, with existing identity and governing owner | Existing C9 or CAN008 operand semantics must be known; no all-operands-any-type permission. |
| CompositeProcedureRef | Scoped *newly acquired or configured* ordered/cooperative operation with exact component refs | A procedure can model genuine reorganization without literal new pairwise relation. Rule owner separately required. |
| RelationRef | Conditionally operative **actor-owned relation of operations**, oriented/typed/sparse | Not CAN011 v1 fourth state kind by declaration; pending owner-approved storage mapping. |
| ActorMiddleStateRef | CAN011 v1 V3MS_MEDIATOR / V3MS_TENSION / V3MS_PRACTICE only; actor historical state | Existing authority owns representation; cannot mint V3MS_RELATION. |
| Memory/ClaimRef | ADP016 causal trace / event memory and ADP017 actor-belief/knowledge/uncertainty claim, separately | Analyst source not available episode; false claim ≠ fabricated episodic memory; narration cannot create either. |
| ContextPredicateRef | Qualifying source-based conditions: current activity, tool, partner, object, practice site, competence/use and access | Context is not an untyped label like “stress,” “religion” or “adolescent.” |
| RuleIdentityRef / QualificationRef | Exact owner, rule/version/hash, rights, effect validity and qualified NO_CHANGE | A plausible human science paragraph cannot issue a transition law. |

## 3. Abstract typed proposals (not adopted interfaces)

~~~ts
// All types below are CANDIDATE CONCEPTUAL INTERFACES, no current module asserted.
type OrganizationKind =
  | "EXISTING_VALUE_CHANGED"         // D0
  | "PREEXISTING_CONTEXT_ACTIVATED" // D1
  | "NEW_OPERATION_FORMED"         // D2
  | "NEW_FUNCTIONAL_RELATION"      // D3
  | "RELATION_SCOPE_REORGANIZED"   // D4
  | "INHIBITED_OR_DORMANT"         // D5
  | "CAPACITY_TO_LEARN_MODIFIED"   // D6; hypothesis only
  | "EXTERNAL_JOINT_SUPPORT_ONLY"  // D7
  | "TRUE_NO_CHANGE"
  | "UNDETERMINED_OR_HELD";

type FunctionalRelationMode =
  | "RECRUITS"          // one operation makes another eligible in a scoped task
  | "INHIBITS"          // veto/attenuation under actual compatible response rule
  | "ORDERS_BEFORE"     // temporal/procedural coordination
  | "MODULATES_SCOPE"   // governs when another operation may apply
  | "COOPERATES_IN"     // jointly required components of a named task/procedure
  | "TRANSFORMS_OUTPUT" // eligible operation result becomes material input to another
  | "CONTEXTUAL_REDIRECT"; // task-specific rerouting, not arbitrary label

type RelationLifecycle =
  | "PROPOSED_UNADMITTED"
  | "ACTIVE"
  | "DORMANT_CONTEXT"
  | "INHIBITED_CURRENTLY"
  | "UNAVAILABLE_EXTERNAL_MEANS"
  | "SUSPENDED_BY_RULE"
  | "REORGANIZED_WITH_SUCCESSOR"
  | "TERMINATED_BY_ISSUED_RULE";

interface QualifiedOperationRef {
  actorId: string;
  operationId: string;
  operationKind: string;     // independently issued operand type
  ownerId: string;
  semanticVersion: string;
  sourceRuleHash: string;
  availableScopeRefs: string[];
}

interface HistoricalFunctionalRelationCandidate {
  candidateId: string;
  actorId: string;
  branchId: string;
  existingOrProposedOperationRefs: QualifiedOperationRef[];
  fromOperationId: string;
  toOperationId: string;        // or typed composite ID for n-ary procedure
  relationMode: FunctionalRelationMode;
  localActivityObjectRef: string;
  scopePredicateRefs: string[];
  eligibleActorReceptionRefs: string[];
  observedActivityRefs: string[];
  actualOtherActorRefs: string[];
  requiredWorldSupportRefs: string[];
  proposedNoveltyContrast:
    | "BEYOND_EXISTING_VALUE"
    | "BEYOND_EXISTING_CONTEXT_GATE"
    | "BEYOND_PRIOR_COMPOSITION"
    | "INSUFFICIENT_COMPARISON";
  firstProposedEffectiveTime: string;
  sourceOwnerRefs: string[];
  rivalExplanations: string[];
  uncertainOrMissingObservations: string[];
  ruleARef?: string;            // actual response, requires competent rule
  ruleTRef?: string;            // persistent formation, requires separate competence
}

interface CandidateOrganizationDecision {
  actorId: string;
  eventHash: string;
  actorPreStateHash: string;
  effectiveTime: string;
  kind: OrganizationKind;
  proposedOperationOrRelationRefs: string[];
  qualifyingActivityRefs: string[];
  staticAlternativeEvidenceRefs: string[];
  externalSupportAlternativeRefs: string[];
  decision:
    | "PROPOSAL_ONLY"
    | "COMMIT_BY_COMPETENT_RULE"
    | "NO_CHANGE_BY_COMPETENT_RULE"
    | "REFUSED_SOURCE_OR_PERMISSION"
    | "HELD_MISSING_SCIENTIFIC_RULE"
    | "HELD_UNDERDETERMINED";
  ownerRuleHash?: string;
  actorPostStateHash?: string;
  valueReadConsumerRef?: string; // required before causal-efficacy proof
}

interface ActiveRelationRead {
  actorId: string;
  relationOrProcedureRef: string;
  actorStateHash: string;
  actualWorldAndTaskRefs: string[];
  externalSupportAvailable: boolean | "UNKNOWN";
  relationLifecycle: RelationLifecycle;
  activationDecisionWithRuleRef: string;
  admittedOperandSemanticValues: unknown; // owner typed, never raw text
  admittedEffectOrNoEffectReceipt: string;
}

interface DistributedActivityConfiguration {
  actorId: string;
  worldVersionHash: string;
  currentActivityObjectRef: string;
  eligibleActorOperationRefs: string[];
  independentActorActionRefs: string[];
  actualMaterialToolAndSupportRefs: string[];
  actorOwnedAcquiredRelationRefs: string[]; // possibly valid empty
  jointResultOrFailedAttemptRef?: string;
  unresolvedOwnerOrObservationRefs: string[];
}
~~~

**NOT an accepted meaning:** Boolean externalSupportAvailable is illustrative for the source/unknown/available distinction, not authority to set a tool “available” absent actual world owner. Generic unknown typed value cannot be directly serialized into approved science; schema owner must specify sanctioned operand payload.

**N-ary caution:** The relation of planning, remembered instruction, attending to others and performing a practical act may be a *single composed procedure with several steps*, not all six pairwise edges. Preserve ordered component/goal/condition/provenance refs. Some interactions can be jointly realized rather than linearly oriented; use a named composite with participant roles, not fictitious causal symmetry.

## 4. Proposal, qualification, activation, reorganization: conceptual decision protocol

~~~text
C12 needs actor A and actual person-world next-event response.
  1. C8/world independently source and realize E under exact actor/world clocks.
  2. CAN008 concrete Rule A (if issued) evaluates A's actor-accessible current
     received activity and named operation participation; records transient and no-effect.
  3. Conceptual candidate discovery considers:
       a. existing operator changed scalar;
       b. same old operator under newly applicable context;
       c. new actual skill/procedure learned;
       d. acquired relation/recruitment/inhibition between already qualified operations;
       e. distributed outside support/other actor, not individual acquired change;
       f. no evidence / missing rule.
     All remain interpretations until a competent owner evaluates them.
  4. Original CAN011 Rule T (or other original domain owner, if separately issued)
     adjudicates formation/change/true NO_CHANGE/REFUSE/HELD, with exact
     causal parents, activity, source, pre/post state and rule identity.
  5. If allowed, store as ONE of existing CAN011 v1 kinds with an owner-approved
     typed payload / linked procedure; otherwise request explicit CAN011 amendment.
     No "V3MS_RELATION" invented by SYN02-C.
  6. On genuinely later E2, C9 reads the actual qualified semantic operation/
     relation VALUE under the current context, possibly yielding a new response.
     Log operand values/read-set/result and competing external-support route.
  7. V2 retrospective may describe actor-accessible memory/claims only.
     A new SCI05 reflective act needs separate owner admission before being
     allowed to condition future psychological organization.
~~~

**Formation is not usage:** an actor can possess a qualified relation that is unused in a given situation, or use a supplied teacher's scaffold without independently acquiring any relation. A stored relation does not guarantee recruitment. Conversely an actually enacted new procedure may not warrant a permanent record if evidence insufficient or world support was temporary. Need domain-specific persistence verdict.

**Rejection/status law:** \`TRUE_NO_CHANGE\` is available *only* when the competent issuer's admitted rule has actually evaluated the qualifying source and returned no persistent transition. \`HELD_MISSING_SCIENTIFIC_RULE\`, \`UNOBSERVED\`, \`SOURCE_NOT_OWNED\`, \`ACTOR_NOT_RECEIVABLE\`, \`OPERATOR_IDENTITY_UNKNOWN\`, \`CONTEXT_MISMATCH\`, \`NO_EVENT\` are distinct and must not be silently treated as zero effect or empty history. Context-ineligible is not psychological unlearning.

## 5. Identity, version, lineage and sparse relationality

- A relationship's **identity** should be derived deterministically from actor ID, admitted formation receipt, typed endpoints/roles, semantic scope and owner/version—not from the transient wording of an LLM proposal. For any re-scoping/new semantics, create a successor (supersedes parent) rather than rewrite source history. Hash recipe requires owner approval; the proposed identifiers are not issued SHA schemes.
- **Persistence** is explicit and evidenced, never a universal “remember 0.985 each year.” Historical absence of use is not evidence of lost competence. \`DORMANT_CONTEXT\` and \`UNAVAILABLE_EXTERNAL_MEANS\` preserve meaningful distinction. Reactivation demands actual context and owned response, not nostalgia prose.
- **Graph cardinality** should track observed/qualified relations, normally sparse relative to all possible pairs. Candidate fanout must be constrained by typed admissibility and source evidence; no universal numeric degree bound invented. A person with no warranted new edges is **complete valid empty** under CAN011, not underdeveloped.
- **Contradiction**: relation R1 can recruit help-seeking under the aunt's household, R2 inhibit help-seeking under a historically different adult/social exposure. Both may coexist without mandatory tie-break or hidden winner; a specific present context/rule determines recruitment. Alternatively a coherent organization with one reliable cross-context procedure needs no conflict record.
- **Potential cycles:** simultaneous mutual recruitment is not proof of a new memory loop. If admitted algorithm has cyclic dependency, require explicit source-owned ordering, bounded fixed-point/iteration semantics or a higher-order procedure with a termination proof and honest failed evaluation, rather than silently continuing forever. No numeric relaxation coefficient adopted.
- **Current relation read** is an actual event-local effective operation; an unobserved inferred historical relation has no actor-semantic permissions until qualifying original owner acts. Maintain separate scientist hypotheses vs committed actor state vs actor known claims vs artist render.

## 6. Examples with competing representations

**A. Single instruction:** student can already sort objects and follow a verbal rule. Teacher delivers one discriminating instruction; student now actually makes a valid categorical inference unaided. Model might represent \`NEW_OPERATION_FORMED\` (new rule-based categorization), \`PREEXISTING_CONTEXT_ACTIVATED\` (already knew and was prompted), or \`COOPERATES_IN\` (new linguistic instruction recruited practical sorting). To distinguish: hold teacher absent at E2; check scope and prior repertoire; don't require repetitions or assume learner acquired a relation from parroting.

**B. Caring mother absent at night, aunt supports:** objective work shift and affection, actual care gaps, aunt's independent availability, child's particular help access are separate. Later the actor may use remembered availability to recruit collaboration despite embarrassment under a specific task; or self-regulation may suppress asking after an observed humiliating encounter. Before storing an edge, ask whether mother/aunt **currently doing the task**, a fixed context-gated help schema, or actual new self-directed strategy fully explains observed conduct. A child may remain steadily trusting without any new edge; lawful NO_CHANGE requires Rule T.

**C. Later political/religious recontextualization:** participation in a real collective introduces a concept that the actor uses to interpret historical insufficiency. This is an adult-time **NEW_OPERATION** or scoped \`INTERPRETIVE_ORIENTING\` potentially recruiting practical solidarity, not infant doctrine or an overwritten memory. Source-qualified ADP017 mistaken belief can coexist with objectively contradicted analyst relation; ADP016 forbids fabricated infancy episode details. V2 prose has no write authority.

**D. Loss of support:** actor learned to manage a task jointly with a specific friend; friend departs. On solo attempt the activity fails. Distinguish \`UNAVAILABLE_EXTERNAL_MEANS\` from deletion of actor's acquired coordination/competence. If new means later arise, success may return without “rewiring again.”

## 7. Existing authority and reuse ceiling

- **CAN008 R2 adopted generic semantics** (candidate blob b80dd6925066510ecbbfec7b427bf9f688475663): coupled occurrence/receivability/uptake/recruitment; NOT an issued domain Rule A or existing universal new-edge type.
- **CAN011 v1** original authority blob 1ed04e62a363493bc7032a99139454a3126e6ea0: three state kinds only, valid empty, contradictory coexistence, exact generated-history/rule update; NO new fourth state kind or concrete formation algorithm licensed here. A newly acquired *functional relation* might be a typed role/payload of \`V3MS_MEDIATOR\` or \`V3MS_PRACTICE\`, but original CAN011 owner must decide whether that satisfies its registry. If not, explicit amendment/companion registry by competent authority is required; documentary design alone cannot revise it.
- **ADP016** blob 0b7bbe29f6509e31ac7d842962a2bf3d636daa2c owns event memory versus nondeclarative causal trace; **ADP017** blob 6b4162df27003bec413074178c46fea6360d71a0 owns actor-known claim permission; **SCI05** still held in current C12 self-account path.
- **Historical V3** M21 grooves/route change and M14 topology/boundary fixed hysteresis are existing *computational affordances*, not observed learned relation creation. RX02 confirmed route-value changes may alter channel selection; grooves alone affect conductance. RX03 verified historical fixed topology and no qualified new relation-edge creation. **N05** remains a scientific/engineering new capability, not necessarily new graph storage.
- **Current S39–S52** RC static source review and SYN01 R2 source closeout locate partial material/current-consumer paths but do not establish an actual C12 qualified learned relation E1→E2 semantic read. No unconditional new executable package name assigned by SYN02-C.

**First actual native falsifier (SPECIFICATION_ONLY):** record source-owned E1 under issued Rule A/T forming specific *relation or composed operation*, hold E2 world/coactor and endpoint values fixed, require C9 same-person read of *the acquired semantic content* to affect a genuinely later considered/attempted action. Sever only formation/read link. It must not be satisfied by different edge count, branch SHA, narrator flourish, default source flags or independent B doing the work. Separate true NO_CHANGE, missing-rule HOLD and support-only competitor.
