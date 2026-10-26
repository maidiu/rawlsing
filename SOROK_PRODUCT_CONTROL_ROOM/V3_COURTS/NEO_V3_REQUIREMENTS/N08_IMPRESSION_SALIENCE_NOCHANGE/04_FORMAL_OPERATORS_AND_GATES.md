# T02 / N08 — Candidate operators, commitments and no-change law

**Proposed, not adopted.** Do not encode a global salience scalar or universal age coefficient.

~~~typescript
type Ref = { id: string; hash: string };
type Evidence<T> = { status: "KNOWN" | "UNKNOWN" | "CONTESTED";
  value?: T; support: Ref[]; limitations: string[] };
type EncounterDescription = { worldEventRef: Ref; actualOtherResponses: Ref[];
  continuityNovelty: Evidence<string>; objectiveDanger: Evidence<Ref[]>;
  durationAndMaterialEffects: Evidence<Ref[]> };
type ReceivedExperience = { actorId: string; access: Ref[];
  scopedExpectationsConsulted: Ref[]; challengeComplicationThreatRefs: Ref[];
  perceivedDanger: Evidence<boolean>; sensoryAffectiveReaction: Evidence<Ref[]>;
  practicalActivityAndHelpSeeking: Evidence<Ref[]> };
type TransientConsequence = { actorId: string; cause: Ref[];
  affectOrBodilyEffect: Ref[]; activityEffect: Ref[]; resolution?: Ref[] };
type CandidateTransition = { targetStateRefs: Ref[]; causalParents: Ref[];
  category: "CONFIRM" | "QUALIFY" | "ADD_RIVAL" | "DIFFERENTIATE" |
    "NEW_MEDIATOR" | "NEW_TENSION" | "NEW_PRACTICE" |
    "MAJOR_REORGANIZATION" | "NONE"; reason: Ref[];
  acceptedUpdateRule?: Ref };
type CommitDisposition =
  | { status: "LAWFUL_NO_CHANGE"; evaluatedRule: Ref; priorStateHash: string;
      eventAndTransientRefs: Ref[] }
  | { status: "AUTHORIZED_TRANSITION"; rule: Ref; newStateHash: string;
      causalParents: Ref[] }
  | { status: "HELD_MISSING_AUTHORITY" | "HELD_INPUT_UNBOUND" |
      "HELD_AMBIGUOUS" | "DENIED"; priorStateHash: string; evidence: Ref[] };
function describeReceptionAndTransient(input: { encounter: EncounterDescription;
  actorHistory: Ref[]; actorAccess: Ref[]; relevantOthers: Ref[];
  acceptedAppraisalRules: Ref[] }): { reception: ReceivedExperience;
  transient: TransientConsequence[]; missing: string[] };
function adjudicatePersistentConsequence(input: { reception: ReceivedExperience;
  transient: TransientConsequence[]; priorStateHash: string;
  candidateChanges: CandidateTransition[]; acceptedRules: Ref[];
  orderingAndClockAuthority: Ref[] }): CommitDisposition;
// The first function does not mutate; the second cannot self-adopt rules.
~~~

## Critical decision distinctions
- A real admission can create transient fear/relief/effort and **zero** persistent changes.
- LAWFUL_NO_CHANGE means an actually accepted rule qualified the zero-transition result. HELD_MISSING_AUTHORITY means none exists and state is untouched by prohibition; the two must not be conflated.
- Old mean-confidence and scalar salience dynamics cannot be imported as psychological truth; no numerical update is specified.
- If multiple noncommuting proposals arise, require exact accepted scheduler/dependency law or HOLD; preserve possible contradictory records when not legally superseded.
- Preserve raw world episode, access, actor reaction, any authorized update, later fallible memory and expression as distinct identities.
- Immediate event in second-half batch n changes the history available to n+1, including actual later actions of others and activity intervals. No standard LLM call between; retrospective memory can narrate but cannot cause prior fact.

## Hostile test minimum
A. Expected care, no memorable event → conditional baseline allowed, N09 episodic absent.
B. Dog terror and prompt repair with no durable target change → LAWFUL_NO_CHANGE only if rule exists.
C. Dangerous dog without child noticing → objective danger independent; no imagined fear.
D. A single severe loss followed by changed objective dependence → major transition possible.
E. Two opposed expectation/response records survive together; no majority scalar.
F. Missing accepted update rule → HELD_MISSING_AUTHORITY not NO_CHANGE.
G. Same scenes different event order or different coactor reaction must be permitted different outcomes.
H. Memory retelling alone cannot modify causal facts.
I. Same-time incompatible transition proposals without dependency authority → HELD_AMBIGUOUS.

## Owner/consumer
N03, N04, N07 plus actual C9/C12 event history; CAN008 actor event semantics, CAN011 state updates only registered and rule-issued, ADP016 causal memory, N09 retrospective memory. Qualified C12-backward test with positive, no-change, missing-source and severed-source fault required before native release. NOT_RUN by T02.
