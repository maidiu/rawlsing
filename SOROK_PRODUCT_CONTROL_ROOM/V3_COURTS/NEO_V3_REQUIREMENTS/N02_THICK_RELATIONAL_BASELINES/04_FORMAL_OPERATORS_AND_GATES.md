# T02 / N02 — Candidate formal operators and authority gates

**Candidate interface ONLY; symbol names are newly proposed, not claims of existing functions or native laws.**

~~~typescript
type Ref = { id: string; contentHash: string; sourceKind: string };
type Known<T> =
  | { status: "KNOWN"; value: T; evidence: Ref[] }
  | { status: "UNKNOWN" | "UNBOUND" | "CONTESTED"; evidence: Ref[] };
type Scope = { actors: string[]; relationRefs: Ref[]; needOrObjectRefs: Ref[];
  places: string[]; activityRefs: Ref[]; temporalConditions: string[] };
type OrdinaryInterval = { intervalRef: Ref; start: string; end: string;
  activities: Ref[]; actualOtherActions: Ref[]; needEpisodes: Ref[];
  materialConstraints: Ref[]; sourceCoverage: Known<string> };
type ScopedAnticipation = { scope: Scope; anticipatedAvailableAction: Known<string>;
  actorAccessMode: "EMBODIED_PRACTICAL" | "SENSORY_AFFECTIVE" |
    "LINGUISTIC" | "REFLECTIVE" | "UNKNOWN";
  supportingHistory: Ref[]; qualifyingHistory: Ref[]; opposingHistory: Ref[];
  dependenceRefs: Ref[]; rivalExpectationRefs: Ref[]; ruleRef?: Ref };
type BaselineCandidate = { anticipation: ScopedAnticipation;
  trace: Ref[]; evidenceLimitations: string[];
  recommendation: "CONFIRM" | "QUALIFY" | "DIFFERENTIATE" |
    "ADD_RIVAL" | "NO_PERSISTENT_CHANGE" | "UNDECIDABLE" };
function deriveScopedAnticipations(input: {
  actorId: string; needsAndObjects: Ref[]; actualOtherActorTrajectories: Ref[];
  previouslyAdmittedActivityIntervals: OrdinaryInterval[];
  activeExpectations: ScopedAnticipation[]; context: Ref[];
  availableInterpretationAndAccess: Ref[]
}): { candidates: BaselineCandidate[]; faults: string[] };
// Pure, trace-producing candidate evaluator: NO persistence write.
function proposeBaselineTransition(input: {
  actorId: string; prior: ScopedAnticipation[]; candidate: BaselineCandidate;
  acceptedRule?: Ref; actualEncounterParents: Ref[]
}): { decision: "PROPOSE" | "QUALIFIED_NO_CHANGE" | "HELD_NO_RULE" |
  "HELD_MISSING_INPUT" | "HELD_AMBIGUITY"; proposal?: Ref; evidence: Ref[] };
// Commit only by separately competent native owner, never by this candidate.
~~~

## Qualifying constraints
- Perceived care is not objective care; felt affection is not resource sufficiency. Need resolution may be mixed.
- A routine is backed by qualified intervals/acts, not invented narrative episode. No count threshold or unearned confidence score.
- Unknown parent means UNKNOWN, never 50 or hopeful. Multiple conflicting anticipations are valid.
- Persistence requires a lawful source/grain/middle-state update rule. CAN011's registered kinds do not themselves register need-expectation semantics. An actor belief must not be inferred from embodied regularity.
- Change to a caregiver's actual action or availability should be capable of changing candidate outputs; mere event-label swap should not force a change.
- No equivalent old V3 named function is evidenced to implement this entire interface.

## Test vectors (not executed; reviewer must build with accepted rules)
A. Many qualifying ordinary affectionate exchanges, zero named dramatic events → scoped reliance candidate permitted, no mandatory autobiographical memory.
B. Care when present, long work-related absences and no other childcare → coexisting affectionate and unmet-availability scopes.
C. One exception and completed repair → preserve exception and scope; allow NO_CHANGE for the durable expectation.
D. Known severe repeated danger by trusted adult → genuine relation qualification/major transition not prohibited by earlier safety.
E. No available adult evidence → HELD_MISSING_INPUT, no default baseline.
F. Contradictory accounts from different settings → preserve rivals, not one scalar.

**Owner:** N01/N06/N07 exact upstream, scientific needs/expectations authority, CAN011 where applicable, ADP016 history if accepted, and real C9/C12 consumer. Review this proposed interface before implementation.
