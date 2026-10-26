# T02 / N03 — Candidate typed interface and authority gates

**Candidate formal interface; no existing source symbol or accepted rule is asserted.**

~~~typescript
type Ref = { id: string; hash: string };
type Epistemic<T> = { status: "KNOWN" | "UNKNOWN" | "CONTESTED";
  value?: T; evidence: Ref[] };
type AppraisalKind = "CHALLENGE" | "COMPLICATION" | "THREAT";
type ActorScope = { actorId: string; relationRefs: Ref[];
  needOrValuedObjectRefs: Ref[]; placeOrActivityRefs: Ref[] };
type WorldEncounter = { eventRef: Ref; time: string; objectiveActionRefs: Ref[];
  physicalConditions: Ref[]; actualOthers: Ref[]; objectivelyEndangered:
  Epistemic<Ref[]>; opportunityAndCapacityDemands: Ref[] };
type ActorReception = { actor: ActorScope; access: Epistemic<Ref[]>;
  perceivedThreat: Epistemic<boolean>; demands: Epistemic<AppraisalKind[]>;
  affectAndPracticalResponses: Ref[]; basis: Ref[];
  noVerbalInterpretationAssumed: boolean };
type RepairRecord = { originalFailureRef: Ref; laterActionRef: Ref;
  actingOtherRef: Ref; objectiveRestoration: Epistemic<Ref[]>;
  remainingUnmetNeeds: Epistemic<Ref[]>; actorReception: ActorReception };
function classifyEncounterDemands(input: { world: WorldEncounter;
  actorPriorExpectations: Ref[]; needsAndPurposes: Ref[];
  actorSensoryAndPracticalAccess: Ref[]; materialSupports: Ref[]
}): { reception: ActorReception; alternatives: string[];
  uncertainty: string[]; durableChanges: "NOT_EVALUATED" };
function evaluateRepair(input: { failure: WorldEncounter; subsequent: WorldEncounter;
  distinctOtherActions: Ref[]; actorHistory: Ref[]; unmetNeeds: Ref[]
}): { repair: RepairRecord | null; evidence: Ref[]; faults: string[] };
// Neither writes middle state nor names trauma; downstream N08 adjudicates consequences.
~~~

## Classification invariants
- Objective endangerment belongs to world and is **independent** from perceived threat. Actor may be unaware.
- Challenge concerns demanded ability/effort for a valued possibility; complication concerns insufficiency/exception/ambiguity; threat concerns jeopardized valued conditions. They may overlap or none apply.
- Event title (lost, dog, rejection) never proves perception or durable trauma. Same event changes reception when actor history/access/coactor response changes.
- Failure and repair are separate dated causal facts. A restorative claim requires actual independent coactor action; perceived restoration may differ.
- Distinguish uncertainty from absence: if actor access unknown, no invented immediate distress.
- No retroactive adult linguistic labels assigned to preverbal reception.

## Adversarial tuples
1. danger known true, perceived threat known false; 2. danger false, felt threat true; 3. challenge true without threat; 4. complication true without either; 5. all three overlap; 6. wrong-leg kindly reacting stranger versus rejecting stranger; 7. loving apology while material deprivation unremedied; 8. event intensely upsetting but NO_CHANGE in later N08.
Any design that collapses 1/2 or forces 8 to trauma is RED.

## Owner gates
Exact W0 world/other-actor event and time, N01 needs, N02 historical anticipations, N07 coactor autonomous response, current CAN008 permitted use. A/T appraisal rules are not issued here. A test of type discrimination is a software test, not proof of human universality.
