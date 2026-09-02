# WSC001F — V3 DEVELOPMENTAL RUNTIME MINIMUM SEAM CONTRACT R1

**Proposed contract identity:** `WSC001F_V3_DEVELOPMENTAL_RUNTIME_MINIMUM@1.0.0`

**Status:** `WORKER_CONSTITUTION_PROPOSAL__NOT_PROJECT_ADOPTED`

## 1. Semantic producer / owner

The semantic owner of **actor-indexed generated occurrence and developmental causal history** is the V3 generated-person runtime owner.

That owner may create only new V3 meanings:

- generated-person identity;
- actor-indexed generated position when separately authorized;
- generated relationship / household / genealogy facts when separately authorized;
- admitted causal-event occurrence;
- event parentage / effective-time / causal-order identity;
- actor-state checkpoint identity;
- causal-memory state when separately governed;
- present accessibility state when separately governed;
- persistent-change state only when an exact rule owns that change.

It does **not** re-own:

- empirical facts;
- FIELD FORGE structural commitments;
- PRE-V3 structural objects;
- M5 ResolvedStructuralContext or peer-use receipts;
- comparator/PSEPF evidence;
- upstream relation/query semantics;
- downstream first-person claim permission;
- phenomenology;
- rendered expression.

Producer ownership follows current Authority31: exact upstream objects are referenced, not republished into V3 ownership.

## 2. Consumer

Immediate consumers are:

1. the V3 state/read subsystem itself, for replay and later lawful transitions;
2. the later V3→V2 mediation seam, which receives a read-only actor runtime snapshot;
3. the exact typed V2→V3 return admission seam, which may submit a proposal but may not self-append a causal event.

No consumer may widen permissions or convert a control/audit receipt into actor fact.

## 3. Minimum object families

These are **minimum proposed interface identities**, not claims of already-existing current authority.

### 3.1 `V3GeneratedPersonRef@1.0.0`

Minimum identity:

- `actor_id`;
- `actor_identity_hash`;
- exact initialization receipt ref;
- exact initialization authority ref;
- initialization effective-time ref;
- immutable provenance root.

If no competent production initialization authority is available, positive actor creation is `OPEN_GATE`; fixtures may not leak into production semantics.

### 3.2 `V3CausalCursor@1.0.0`

Minimum identity:

- actor ref;
- monotone causal sequence/cursor;
- as-of effective-time ref;
- current causal-ledger root hash;
- current actor-state checkpoint ref/hash.

Wall clock, filesystem order, "latest", and annual cadence are not causal authority.

### 3.3 `V3TransitionProposal@1.0.0`

Minimum input identity:

- exact actor ref;
- exact proposal ref/hash;
- source class;
- exact source object refs/hashes;
- requested operation class;
- intended V3 semantic target family;
- exact effective-time ref;
- exact causal-parent refs, if any;
- exact transition-owner authority presentation, if positive mutation is requested;
- exact comparator/PSEPF/admission receipt refs where required by the transition;
- optional structural-peer-use receipt as eligibility evidence only;
- optional target-state authority refs;
- optional named RNG authority/receipt only when the exact transition rule lawfully requires stochastic selection.

A raw structural object, M5 RSC, structural peer-use receipt, comparator receipt, replay receipt, or empirical prevalence is never positive actor mutation authority by itself.

### 3.4 `V3TransitionDispositionReceipt@1.0.0`

Every proposal produces exactly one noncausal disposition receipt containing:

- actor ref;
- proposal ref/hash;
- pre-state fingerprint;
- exact rule/authority presentations examined;
- exact typed disposition;
- zero/nonzero mutation declaration;
- causal-ledger append count;
- causal-cursor delta;
- RNG-state delta;
- scheduler-state delta;
- replay/provenance refs;
- integrity hash.

This receipt belongs to audit/control history, not automatically to actor causal history.

### 3.5 `V3DevelopmentalEvent@1.0.0`

Created **only** after exact positive transition authorization.

Minimum identity:

- actor ref;
- event semantic-kind ref owned by the competent transition rule;
- event ID/content hash;
- effective-time ref;
- exact causal-parent sequence refs;
- transition-owner authority ref;
- source proposal/admission receipt refs;
- exact generated target-state/effect refs;
- pre-state checkpoint ref/hash;
- post-state checkpoint ref/hash;
- optional named RNG receipt ref;
- exact replay receipt/root.

The V3 runtime owns occurrence/parentage/ledger identity. It does not steal the semantic meaning of upstream source objects or of separately governed target-state rules.

### 3.6 `V3ActorStateCheckpoint@1.0.0`

Minimum checkpoint is intentionally sparse and extensible:

- actor ref;
- causal cursor;
- causal-ledger root hash;
- exact current generated-position refs;
- exact generated-relationship refs;
- exact household refs;
- exact genealogy refs;
- exact causal-memory-state refs;
- exact accessibility-state refs;
- exact persistent-developmental-state refs produced by governed rules;
- exact open-process refs;
- checkpoint hash;
- checkpoint schema/version;
- provenance/replay root.

A checkpoint is a materialized/replay convenience. It does not become semantic owner merely because it is stored.

### 3.7 `V3ActorRuntimeSnapshot@1.0.0`

Read-only handoff to mediation:

- actor ref;
- as-of causal cursor/effective time;
- actor-state checkpoint ref/hash;
- causal-ledger root;
- objective generated-history refs;
- causal-memory refs;
- present accessibility refs;
- generated relationship/household/genealogy refs;
- current generated-position refs;
- exact replay closure;
- typed unresolved/blocked/valid-empty states.

It contains **no automatic first-person claim permission, phenomenology, voice, tone, narrative, or render authority**.

## 4. Developmental noncollapse law

The runtime must preserve:

`STRUCTURAL/APPLICABLE POSSIBILITY != ACTOR OPPORTUNITY != ENCOUNTER != EXPOSURE != ROUTE REALIZATION != ACTOR RESPONSE != PERSISTENT CHANGE != ATTRACTOR CHANGE`.

No transition in that chain is automatic.

The minimum runtime does **not** require every stage to be populated in GT0. It requires that, when a later authority introduces one, its identity and owner remain distinct and its event/effect be parented exactly.

## 5. Generated position / relationship / household / genealogy ownership

### 5.1 Generated position

A V3 generated-position fact is actor-indexed and V3-owned only after a competent generated-position rule creates it.

Forbidden shortcuts include:

- geography -> class membership;
- structural prevalence -> party/sect identity;
- field position -> actor identity;
- questionnaire category -> generated position;
- source-backed possibility -> actor fact.

Upstream structural position remains upstream-owned evidence/prior/query input.

### 5.2 Relationships and households

A relationship or household exists in V3 only through an exact generated-person/relationship/household rule and causal record.

Structural co-location, demographic similarity, source linkage or shared context does not establish a generated relationship.

### 5.3 Genealogy

Parent/partner/child relations require exact generated-person refs and causal lineage. Household/genealogy fields may remain valid-empty in GT0.

No parent belief/personality/behavior may be inferred from demographic or structural priors.

## 6. Event admission and mutation law

### 6.1 Positive path

A positive proposal may mutate actor state only when:

1. actor and pre-state identities verify;
2. source proposal identity verifies;
3. every required upstream comparator/PSEPF/admission dependency is exact and current at its own grain;
4. an exact separately accepted transition owner authorizes the requested operation;
5. every causal parent is already generated/admitted;
6. effective-time/order constraints are lawful;
7. every target-state mutation has a competent target owner;
8. required RNG is named, authority-bound and receipt-bearing;
9. full disposition/event/checkpoint/replay identities are buildable before commit.

Then commit is atomic:

`VALIDATE -> BUILD RECEIPTS -> APPEND ONE OR MORE EXACT AUTHORIZED EVENTS -> UPDATE CHECKPOINT -> ADVANCE CURSOR`.

No partial mutation is permitted.

### 6.2 Zero / abstention path

For missing/unaccepted/mismatched authority, blocked comparator/PSEPF, noncomparability, unresolved target owner, invalid identity, rule abstention, or valid-empty evaluation:

- actor state hash is unchanged;
- causal-ledger hash is unchanged;
- causal append count = 0;
- causal cursor delta = 0;
- RNG state is unchanged;
- scheduler state is unchanged;
- a typed `V3TransitionDispositionReceipt` records the control outcome outside actor causal history.

This directly reuses the zero-effect semantics already enforced by `rawlsing_next/v3_psepf_zero_positive_guard.py`.

A control refusal is **not** proof that an in-world event did not occur; it proves only that this runtime invocation did not lawfully create actor state.

## 7. Typed negatives / abstentions

Minimum typed states:

- `ADMITTED_CAUSAL_TRANSITION`
- `VALID_EMPTY_NO_CAUSAL_EVENT`
- `RULE_ABSTENTION_VALID_EMPTY`
- `DENIED_ZERO_EFFECT`
- `BLOCKED_MISSING_POSITIVE_TRANSITION_AUTHORITY`
- `BLOCKED_COMPARATOR_OR_PSEPF_AUTHORITY`
- `BLOCKED_TARGET_STATE_AUTHORITY`
- `BLOCKED_ROUTE_REALIZATION_AUTHORITY`
- `BLOCKED_PREREQUISITE_SATISFACTION_AUTHORITY`
- `BLOCKED_ATTRACTOR_UPDATE_AUTHORITY`
- `NONCOMPARABLE_ZERO_EFFECT`
- `DEFERRED_UNRESOLVED_ZERO_EFFECT`
- `STALE_PRESTATE_ZERO_EFFECT`
- `DUPLICATE_IDEMPOTENT_NO_APPEND`
- `INTEGRITY_FAILURE_ZERO_EFFECT`

Missing != false; blocked != nonoccurrence; valid-empty != zero-valued developmental effect.

## 8. Causal memory, accessibility and replay

### 8.1 Objective history

The immutable event ledger is objective generated history.

### 8.2 Causal memory

Causal memory is a separately governed V3 state: prior history may influence current development only through exact memory objects/transitions or explicit history predicates.

Ledger presence alone does not make an event causally remembered.

### 8.3 Present accessibility

Current accessibility/recall is separate from both objective history and causal memory.

If no exact accessibility rule is available, accessibility is typed unknown/empty, not omniscient.

### 8.4 First-person permission

First-person claim permission is downstream mediation authority and is not created here.

### 8.5 Replay burden

Exact replay requires, at minimum:

- generated-person initialization identity and authority;
- ordered causal event refs/hashes;
- exact causal-parent sequence;
- exact effective-time refs;
- transition rule IDs/versions/hashes;
- target-state rule IDs/versions/hashes;
- comparator/PSEPF/admission receipts where causal;
- prior checkpoint hash;
- named RNG receipts where used;
- checkpoint schema/version;
- all control dispositions needed to explain why candidate transitions did not enter causal history.

Replay with identical immutable inputs must reproduce the same event sequence, cursor, ledger root and checkpoint hash.

## 9. Scheduler / time minimum

GT0 does not require a universal scheduler.

The minimum runtime accepts an explicit governed effective-time ref per proposal and a monotone causal cursor.

No universal annual tick, developmental phase ladder, slow-process cadence, catch-up rule, route probability or wall-clock progression is constituted.

Quiescence is valid.

A future scheduler may be added only through separately governed semantic and cadence authorities.

## 10. Randomness minimum

GT0 requires no stochastic rule.

Default is `NO_RNG_CONSUMED`.

A future stochastic transition must bind a named causal RNG authority and produce an exact receipt. RNG may choose only among already lawful candidates and cannot create semantic authority.

## 11. Existing reusable implementation / tests

### Directly reusable/adaptable

- `rawlsing_next/v3_psepf_zero_positive_guard.py`: exact zero-effect firewall; current default positive registry is empty.
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`: proves no state/ledger/cursor/RNG mutation for absent/unaccepted/mismatched positive authority.
- `rawlsing_next/m5_runtime_rsc_peer_prior.py`: structural-currentness and peer-use proof while explicitly denying direct actor mutation authority.
- `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`: exact currentness / structural-peer boundary tests.
- `rawlsing_next/m6_actor_safe_expression.py`: downstream replay-closure shape proving objective actor state, causal memory, epistemic/accessibility and expression permission are separable.
- `rawlsing_next/tests/test_m6_actor_safe_expression.py`: stale/integrity/valid-empty/actor-binding tests useful for the V3 read-handoff.
- `rawlsing_next/source_backed_positioned_subject_possibility.py`: current accepted upstream function preserving `PROXY != EXACT FACT != ACTOR BELIEF`.

### Historical design capital only

Dva TD-R05 and W42 inheritance establish useful event-sourced, genealogy, scheduler, memory and noncollapse concepts, but W3 event-ledger/state implementation never returned. They are reference design capital, not permission to revive the historical full roadmap or constants.

## 12. Exact forbidden inferences

The runtime must reject or fail closed on:

- empirical prevalence -> actor fact;
- structural possibility -> opportunity;
- applicability -> encounter;
- encounter -> exposure;
- exposure -> route traversal;
- route existence -> route realization;
- topology/co-occurrence -> actor-history realization;
- prerequisite topology -> satisfaction;
- response -> persistent change without a rule;
- repeated exposure/response -> attractor update without a rule;
- source-backed proxy -> actor belief;
- generated position -> knowledge/accessibility;
- objective history -> causal memory;
- causal memory -> present accessibility;
- accessibility -> first-person claim permission;
- relationship/household prior -> generated relation;
- rendered/session/transcript persistence -> causal event;
- missing authority -> neutral effect / zero-valued truth;
- blocked transition -> false proposition;
- storage/checkpoint presence -> semantic ownership;
- current structural peer-use permission -> V3 mutation permission;
- historical Dva authority/code -> current production authority merely by existence.

## 13. Exact open gates

See `03_OPEN_GATES.tsv`.

GT0 must not silently close them.

## 14. Minimal GT0-compatible path through V3

### Current fail-closed path at `d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`

1. Start with an exact actor/pre-state fingerprint if a lawful actor already exists.
2. Present one exact upstream structural/empirical/PSEPF transition proposal.
3. Evaluate the current zero-positive PSEPF guard.
4. Because the current production positive-transition registry is empty, receive `BLOCKED_MISSING_POSITIVE_TRANSITION_AUTHORITY` / zero-effect disposition.
5. Assert identical pre/post actor-state hash, causal-ledger hash, causal cursor, RNG state and scheduler state.
6. Produce a read-only `V3ActorRuntimeSnapshot` preserving the typed blocker/valid-empty status for downstream mediation.

This is a lawful GT0 path because GT0 may prove conservation and jurisdiction through a typed blocker.

### Future positive path after competent authority exists

1. Exact actor and pre-state verify.
2. Exact proposal + comparator/PSEPF/admission receipts verify.
3. Exact separately accepted transition owner authorizes one operation.
4. V3 atomically appends the exact event and advances one causal cursor.
5. Rebuild/validate checkpoint.
6. Export read-only runtime snapshot.

The positive path is conditional; WSC001F does not claim the required authority currently exists.

## 15. Later extensions explicitly deferred

Not required for minimum GT0:

- generalized trajectory/history query language;
- universal position/pendulum ontology;
- automatic route realization;
- generalized V556 actor-history realization;
- prerequisite-satisfaction engine;
- universal response/metabolism rule library;
- persistent-change updater;
- relationship/household/genealogy generation beyond explicit governed events;
- multi-timescale scheduler;
- universal developmental phases;
- slow-process cadence;
- route probabilities;
- universal satisfaction rule;
- attractor update/interpretation;
- universal psychological/vector state;
- V2 phenomenology/expression logic.

Each may be added only by an exact competent owner without altering the minimal causal shell's jurisdiction.
