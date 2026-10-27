# S03 — One actor snapshot/version, one event lineage, one durable decision receipt

**Evidence and authority:** Candidate design by SYN02-S at sealed 5fcad44b938ea525b5468047ac1305d76c765913, on A b47742b0, B d8f8b4f7, C d99ebb98, D f904955e, RA 7991454b, RB 57f03f75. Architecture, not implementation, empirical psychology, source grant or original Rule A/T issuance. All new names are proposed. Separate reviewer and source owners must authorize later use.

## Collision decision (K03)

Unify B `ActorSnapshotV1` and D `ActorStateVersion` into one **ActorVersionV1** (identity, branch, version, one canonical committed psychological payload). Neither old C9 CandidateStore nor S37 QualifiedC12Store is replaced. C9 CandidateStore retains existing response/target transaction authority; S37 C12 store retains branch/episode/world_event/perception/checkpoint append-only proof. Add a versioned actor-state extension and ledger mapping to **one canonical event/transition lineage**, not parallel “internal minds,” competing snapshots or two independent durable Rule T receipts. Physical DB tables may remain separate but commit protocol must prove one logical truth. V2, derived calculations and memory envelopes are projections.

## Proposed implementable type contracts — NOT existing symbols
~~~ts
type Hash=string; type Ref=string; type Instant=string;
type FactStatus="PRESENT"|"ABSENT"|"UNKNOWN"|"SOURCE_DENIED"|"NOT_YET_OBSERVED";
type Decision="COMMITTED_CHANGE"|"TRUE_NO_CHANGE_EVALUATED"|"HELD_MISSING_RULE"|"SOURCE_DENIED"|"ACCESS_NOT_RECEIVED"|"UNDETERMINED"|"INTEGRITY_FAILED";
interface QualifiedRef {owner:Ref; source:Ref; commit:Hash; blob:Hash; scope:Ref[]; effective:Instant; grade:"SPEC_ONLY"|"TEST_ONLY"|"OWNER_NATIVE";}
interface ActorVersionV1 {
 schema:"neo_v3.actor@1"; actorId:Ref; branchId:Ref; version:number;
 parentHash:Hash|null; effectiveTime:Instant; sourceRefs:QualifiedRef[];
 materialRefIds:Ref[]; motiveRefIds:Ref[]; actorKnowledgeIds:Ref[]; actorMemoryIds:Ref[];
 middleState:Array<{id:Ref;kind:"V3MS_MEDIATOR"|"V3MS_TENSION"|"V3MS_PRACTICE";payloadHash:Hash;formationSourceRef:Ref;originalRuleHash:Hash;scopeRefs:Ref[]}>;
 status:"VALID"|"MIGRATION_HELD"; canonicalHash:Hash;
}
interface CanonicalLedgerRowV1 {
 schema:"neo_v3.ledger@1"; id:Ref; seq:number; branchId:Ref; ownerRef:Ref;
 clock:Instant; kind:"WORLD"|"COACTOR"|"INTERVAL"|"ATTEMPT"|"RECEPTION"|"C9_RESPONSE"|"DURABLE_DECISION"|"SURFACE_METADATA";
 causalParents:Ref[]; sourceRefs:QualifiedRef[]; payloadHash:Hash;
 worldBefore?:Hash;worldAfter?:Hash;actorBefore?:Hash;actorAfter?:Hash;
 accessFeatureIds:Ref[]; commitHash:Hash;
}
interface DurableDecisionReceiptV1 {
 schema:"neo_v3.decision@1"; eventId:Ref; transactionId:Hash;actorId:Ref;branchId:Ref;
 beforeActorHash:Hash;afterActorHash:Hash;beforeWorldHash:Hash;afterWorldHash:Hash;
 eventEffectiveClock:Instant;readsetRefs:Ref[];sourceRefs:QualifiedRef[];
 ruleAHash?:Hash;ruleTHash?:Hash;evaluatedOperandIds:Ref[];
 decision:Decision;reasonCode:string;changedPayloadIds:Ref[];
 qualifiedNoChangeEvidenceIds:Ref[];c9CommitRef?:Ref;c12ProofRef?:Ref;contentHash:Hash;
}
interface AccessEnvelopeV1 {
 actorId:Ref;realizedEventId:Ref;status:"RECEIVED"|"PARTIAL"|"NOT_WITNESSED"|"UNKNOWN";
 availableFeatureIds:Ref[];unavailableFeatureIds:Ref[];basisRefs:QualifiedRef[];
}
interface BatchReceiptV1 {
 batchId:Ref;policy:"UNDECIDED"|"PREFIX_CONTIGUOUS"|"WHOLE_BATCH_ATOMIC"|"INDEPENDENT_SUFFIX";
 committedEventIds:Ref[];unresolvedProspectIds:Ref[];
 actorBefore:Hash;actorAfter:Hash;worldBefore:Hash;worldAfter:Hash;
 actorReceiptRefs:Ref[];postcallSCI05DependencyIds:Ref[];
 render:"DONE"|"FAILED"|"NOT_REQUESTED";receiptHash:Hash;
}
~~~
No newly coined relation is registered CAN011 v1; any admissible composition is a governed PRACTICE/MEDIATOR payload. `BatchReceiptV1.committedEventIds`, actual counts, ordinal and analyst IDs are server-only — prohibited from direct/indirect LLM retrospective packet.

## Clock, identity and transaction semantics

Event time = source-governed effective instant/interval; commit time = system write time; accessible memory time = separate reception/encoding time. Branch lineage immutable, forks point to exact parent actor/world hashes and clock. Idempotency key hashes branch+actor+event source+effective clock+causal parent+rule version, retries same data return same receipt; same ID with changed payload refuses. CAS expected actor version; canonical event sequence contiguous unless original batch policy expressly permits otherwise.

State transitions:
~~~text
source-qualified actor seed → ActorVersion(0)
  world/B source commits actual occurrence [world writer, independently irreversible]
  actor access evaluated [ADP]
  Rule A response or typed HOLD [CAN008/C9]
  Rule T issued and applied → new ActorVersion(v+1) + one durable receipt
  Rule T issued/evaluated no effect → same semantic state + one true NO_CHANGE receipt
  missing source/rule/actor access → corresponding held row; never “nochange”
  derived/memory/V2 read after commit; render failure does not undo actual event
  later E2 queries Rule A with actual semantic state values and scope
~~~
A cross-store single logical commit may need outbox/prepare-commit/recovery; do not falsely assert SQLite ACID spans C9 and C12 if physically separate. A world event may already have happened when actor transition fails; record world-committed/actor-held state, not rollback of independently acting B. A render failure is not an actor failure and cannot rewrite psychology.

## Migration and provenance

Historical V3 source is immutable archive by SHA, not an entitled original psychological law. A field migration decision is VERIFIED_SOURCE, CARRIER_ONLY, DERIVED_VIEW_ONLY, UNSAFE_HISTORICAL, UNKNOWN or SOURCE_HELD. Seed valid empty actor when nothing qualified; don't populate developmental causality from typology, country/age/religion, 50/hopeful parent, placeholder crack, invented rupture, narrator prose, or M26 derived persistent writes. Report each rejected field and original blob; future owner can newly qualify specific values. Migration all-or-nothing per actor with reversible mapping, collision diagnostics and immutable source records; repeated identical migration idempotent, changed source SHA fails. No second psyche. Actor-access packet derived from ledger+ADP feature permissions, not from every world event.
