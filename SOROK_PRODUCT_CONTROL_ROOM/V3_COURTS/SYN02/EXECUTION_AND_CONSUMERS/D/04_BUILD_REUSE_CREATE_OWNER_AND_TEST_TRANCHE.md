# SYN02-D / 04 — build / reuse / create owner plan and implementation tranche

**Status:** `ARCHITECTURE_PLAN / NO IMPLEMENTATION / NO PRODUCTION EDIT / NO NATIVE GRANT`.
**Sealed startup:** `cd1f4fd8158c2771d7c565b06ee397a7a60dc779`.
**Source basis:** the exact cuts in `01_C12_TO_C0_ACTUAL_CURRENT_CALL_GRAPH.md`; the 116 sourcefree tests recorded in `RETURNS/D/00_RETURN.md`; PRE-MAIN `c5e0e5755…` for C0/C11.

---

## 0. Build principle

Do not start with a new “actor compiler” or a new simulation language. Start with the **smallest additive runtime spine** that can carry a real C12 person:

1. a portable source/custody registry;
2. a versioned actor/event ledger and transaction;
3. an access-limited retrospective packet;
4. a sparse functional-organization record store;
5. a batch realizer driven by owner-supplied world/B/C9 ports;
6. semantic owner rules only where an owner actually issues them;
7. C0/C11 adapters only behind explicit source/Pyat authority.

The current test-only S37/S42/S44/S48/S49 code is reusable capital, not a reason to rewrite. The old V3 formulas are not a production psychology.

---

## 1. Source and capability classification

| Capability | Current carrier | Classification | Reuse/build decision |
|---|---|---|---|
| C9 immediate/durable transaction | `candidate.pipeline`, `CandidateStore`, `S36` response/target registries | `PARTIAL / IMPLEMENTED_UNWIRED` | Reuse transaction; add concrete rule owners and actor-state binding; do not rewrite |
| C12 store/lineage | `S37TargetlessProduct`, `QualifiedC12Store`, C12 episodes/world/perception/checkpoint | `PARTIAL / TEST_ONLY` | Reuse storage primitives; add actor-state/functional/batch tables; preserve old hashes |
| C8 occurrence/world | BP2/BP3/BP4 store and journal | `PARTIAL / TEST_ONLY` | Reuse event/perception/commit primitives; protected D1/D2/D3 remain HOLD |
| C4 actor history | S44 sampled root / BP1/G18 | `PARTIAL / TEST_ONLY` | Reuse as one root source adapter; do not call full genealogy |
| Sequential events | S42 `admit_event` | `PARTIAL / IMPLEMENTED` | Reuse event validation/predecessor/C8 seam; extend to batch orchestration |
| Intervals/activity | S46 producer; S47 conditioner | `PARTIAL / TEST_ONLY`, workshop scope | Reuse receipts/conditioning; generalize only under world/SDTF owner |
| N+1 one-call transport | S48 `run_turn`, dispatch/replay/cache | `PARTIAL / TEST_ONLY` | Reuse transport; replace envelope/one-slot self-account semantics |
| Independent B | S49 actor/session | `PARTIAL / CONTROLLED ONLY` | Reuse adapter; actual root B source is `[]`; build/obtain owner source |
| Object relevance/paid | S51/S52 | `PARTIAL / TEST_ONLY` | Reuse relevance/candidate vocabulary; no native purpose/independent counterpart |
| C0 possibility | PRE-MAIN possibility/provider/source-local admission | `PARTIAL / IMPLEMENTED_UNWIRED` | Reuse schemas/services; build C12 adapter only under source authority |
| C11 projection/Route B | PRE-MAIN C11 facade/repository/Route B | `PARTIAL / IMPLEMENTED_UNWIRED` | Reuse as external service; native weld and source permission separate |
| Dynamic functional organization | none | `MISSING` | Build sparse versioned registry; formation rule owner required |
| SCI05/memory/access | test witnesses + S48 hold | `PARTIAL / RULE HELD` | Build access-limited packager; actual admission rule/source needed |
| ACTUAL C12/A0–A5 | none native | `MISSING / PERMISSION REQUIRED` | Separate C11/C12/Pyat/A5 tranche; no shortcut |

---

## 2. Highest-priority engineering tranche (no scientific rule needed)

### T0.1 — Portable source/custody registry

**Problem:** S52 hardcodes `/Users/.../rawlsing-r31j/...`; S48 hardcodes the CLI and model; S37/S44 bootstrap through author return paths. A different host cannot reproduce the exact graph.

**Input:** exact `SourceRef {owner, commit, path, blob_sha1, content_sha256, role, grade}`; branch/turn; worktree root.
**Operation:** resolve to a verified local file/handle; fail closed if commit/hash/role mismatch; inject into `sxx.bootstrap` rather than mutating `sys.path` globally.
**Output:** `ResolvedSourceSet` with actual import paths and hashes.
**First consumer:** `BatchOrchestrator`, `ProductTransport`, all session bootstraps.
**Owner:** C9/C12 engineering; source owners for each external source.
**Tests:** two roots resolve identically; changed hash refuses; missing owner refuses; no absolute Mac path required; same source set across S37/S44/S48/S49.

**This is the safest first code change.** It is sourcefree, reversible and does not alter psychology.

### T0.2 — Actor state/event ledger and per-event transaction

**Input:** existing C12 episode/world/perception + `ActorStateVersion`, `CanonicalWorldEvent`, `ActorAccessRecord`, `C9Response`, `DurableDecision`.
**Operation:** single-writer transaction; stage all records; commit/rollback; new state version; batch receipt; no render inside transaction.
**Output:** durable versioned state and event receipt.
**First consumer:** C9/C12 event path; retrospective packager; replay.
**Owner:** C9/C12 architecture/engineering; CAN011 for durable semantics.
**Tests:** positive committed event; rollback leaves no rows; duplicate event refuses; no access means no actor state; rule held vs no-change; render failure leaves state committed but not clean; replay identity.

**This is additive.** It does not replace old C12 rows; it gives them an actor-state/organization view.

### T0.3 — Access-limited retrospective packet

**Input:** completed prefix + `ActorAccessRecord`/memory; no analyst/objective suffix.
**Operation:** filter by actor access; map to opaque local refs; omit unseen count/order; build `RetrospectivePacket`.
**Output:** model-visible packet for the one N+1 call.
**First consumer:** `NPlusOneTurn` / `ProductTransport`.
**Owner:** ADP016/017 + SCI05 + V2; architecture builds constraints, not memory law.
**Tests:** remove one access feature -> no direct/indirect narrative; suffix never appears; source revocation; coarse omission bucket does not encode count; model prompt has no objective event ID.

### T0.4 — Sparse functional-organization store

**Input:** `FunctionalRelation` versions with origin/evidence/scope; no automatic coactivation creation.
**Operation:** append relation version; maintain active indexed view; return relations by actor/state/scope; no all-to-all.
**Output:** `FunctionalActivationTrace` candidate set.
**First consumer:** C9 activation query.
**Owner:** CAN010/CAN011/ADP/science formation owner; architecture for storage.
**Tests:** empty store = no active relation; add manually admitted relation -> later query returns it by value; retire -> removed; scope mismatch -> not recruited; contrary evidence retained; coactivation without decision does not create relation; sparse query does not scan all history.

### T0.5 — Batch orchestration skeleton

**Input:** 3–5 `ConditionalProspect`, owner ports for world/B/C9/interval.
**Operation:** ordinal resolution; prefix policy; per-entry state machine; stop/held suffix; receipt.
**Output:** `BatchRealization`/receipt; no phantom.
**First consumer:** C12 turn; N+1.
**Owner:** C6/C9/C12; source owners for ports.
**Tests:** 3/4/5 accepted; 0/1/2/6 rejected; event 2 source denied -> E3–E5 not run; prefix truthful; event 2 access absent -> E2 world exists but no state; event 2 rule missing -> held; replay.

**Can be built before the scientific learning rule.** The batch mechanics do not decide whether the actor learned anything; missing C9/CAN011 rules simply produce HELD.

---

## 3. Science-owner tranche (cannot be built as psychology by engineering)

### T1.1 — Concrete CAN008 Rule A / CAN011 Rule T

Need a competent owner to issue or withhold one event-specific response/transition rule with source, scope, actor, positive, NO_CHANGE and rival alternatives. The existing generic CAN008 R2 adoption is not a concrete rule; production registries are empty. Do not convert `TEST_ONLY_S37_CAN008_A` into law.

First consumer: `run_candidate_path` rule/target lookup. Tests must use the actual rule ID/hash and actual event source.

### T1.2 — Care/activity/interval semantics

S46's workshop material attempt is a real bounded producer, not a general care/work/school/rest schedule. A world/SDTF owner must define actual intervals, who provides care, feasible participation, absence/no-encounter and support. No universal hours coefficient from engineering.

### T1.3 — Functional-relation formation and recruitment law

The architecture can store and query relations, but cannot decide:
- whether coactivation forms a relation;
- which operation recruits which;
- whether a relation is state-value or capability;
- how external support differs from learned operation;
- how scope/contradiction/decay work.

A science owner must issue a candidate rule or explicitly withhold. The C court (individual-specific functional inter-wiring) is the relevant scientific input; SYN02-D does not pre-empt it.

### T1.4 — Memory/retrospection/SCI05

ADP016/017 and SCI05 owners must define:
- event-referential vs practical trace;
- partial/false belief;
- access-filtered retrospective packet;
- when a self-account becomes an admitted reflective act;
- dependency invalidation when denied.

Engineering may build the packet filter and dependency graph; it may not invent memory admission or meaning.

### T1.5 — Type/age/class/default prohibitions

Do not reuse old V3 demographic/type/age/religion→crack/practice/rupture or parent-type child effects. Those are historical defects, not a shortcut. No arbitrary coefficient is introduced by this tranche.

---

## 4. Source/authority tranche (cannot be replaced by code)

### T2.1 — C0/C11 current world/possibility

PRE-MAIN C0/C11 modules are real but disconnected. Required:

- a source owner for the exact C0 world/possibility data and C11 projection;
- an adapter from `PositionedSubjectPossibilityQuery`/result and `C11LogicalRelease` to a `WorldPossibilityRecord`/`WorldEventCandidate`;
- no direct actor/psyche conversion;
- source/edition/clock/units/authority fields;
- current-as-of semantics and typed uncertainty.

Owner: Pyat world/source/C11 custodian; Sorok C8/C9 consumer.

### T2.2 — Independent B source

S49 has a B adapter but `root_b_sources=[]`. The missing function is not an interface; it is an actual current B-owned context/history source with source rights. Owner: ADP019/C8/world; the S49 controlled `PRIOR_B_REFUSAL` remains TEST_ONLY.

### T2.3 — C8 trust and C11 weld

C8 protected writer D1/D2/D3 and C11 native weld are separate owner permissions. No code test grants them. C12 native person and A0–A5 human evaluation remain separate.

---

## 5. Implementation sequence and dependency

```text
T0.1 source registry
  -> T0.2 actor/event/state transaction
  -> T0.3 retrospective packager
  -> T0.4 functional-organization store
  -> T0.5 batch orchestrator skeleton
       -> T1.1 Rule A/T concrete owner
       -> T1.2 interval/care semantics
       -> T1.3 relation formation/recruitment
       -> T1.4 memory/SCI05
T2.1 C0/C11 adapter
  -> T2.2 independent B source
  -> T2.3 C8/C11 permissions
  -> current C9/C12 semantic integration
  -> A0–A5
```

T0.1–T0.5 are sourcefree engineering. They must not claim native personhood. T1 requires competent scientific issuance. T2 requires source/actor/security permissions. A T0 component may be accepted only as engineering substrate; it cannot substitute for a T1/T2 positive.

### 5.1 Recommended minimal first implementation tranche

If one tranche is commissioned after SYN02 architecture adjudication, use **T0.1 + T0.2 + T0.3** on an isolated sourcefree branch. They are highest leverage, lowest semantic risk and unlock the rest:

- deterministic portable source resolution;
- a real actor/event transaction and state version;
- an access-limited retrospective packet.

Do **not** start with a new E1→E2 showcase or a full C0/C11 import. Those are dependency traps.

### 5.2 Second tranche

**T0.4 + T0.5** with owner-injected ports and manually admitted test relations. This can validate sparse storage, activation retrieval, 3–5 batch state machine and prefix semantics without claiming a learning law.

### 5.3 Blocked until owner decisions

- `T1.1` concrete Rule A/T;
- `T1.2` actual care/activity semantics;
- `T1.3` formation/recruitment law;
- `T1.4` memory/SCI05 admission;
- `T2.1` C0/C11 source rights;
- `T2.2` actual B;
- `T2.3` C8/C11/native permissions;
- native C12/A0–A5.

These are not “do nothing” items: the architecture names exact inputs, functions, outputs, consumers and tests. A competent owner can issue or withhold each finite decision.

---

## 6. Existing source changes versus new files

### 6.1 Do not edit in SYN02-D

No production edit was made. Future implementation must not:

- mutate old V3 source or reviewed returns;
- overwrite `C12Store`/`QualifiedC12Store` rows;
- change `S37/S42/S44/S48/S49/S52` semantics in place without a versioned migration;
- convert TEST_ONLY registries to production by name;
- make the S52 cold-open `ok=True` shortcut the readiness proof.

### 6.2 Expected additive files

```text
actor_runtime/
  state.py            # ActorStateVersion, delta, state hash
  ledger.py           # canonical event/access/response/durable records
  transaction.py      # unit-of-work, rollback, receipts
  functional.py       # FunctionalRelation/ActivationTrace/store
  batch.py            # ProspectiveBatch/BatchRealizer/policies
  retrospective.py    # RetrospectivePacket/access filter/dependencies
  source_registry.py  # portable source identity/resolution
  render_attempt.py   # render status separate from state
```

Names are illustrative; the owner may choose package/module names. No implementation is authorized here.

### 6.3 Migration

Additive schema migration only:

- preserve old C12 rows/hashes;
- add `actor_state_version`, `access_record`, `impression`, `c9_response`, `durable_decision`, `memory_trace`, `memory_episode`, `functional_relation`, `activation_trace`, `batch`, `transaction`, `render_attempt`;
- map test-only rows as `TEST_ONLY`;
- add new verifier; do not replace old evidence;
- provide downgrade/read-only mode and explicit `native=false` for unqualified data.

---

## 7. Test plan

### 7.1 Already executed sourcefree tests

The reviewer/author tree was exercised directly:

```text
S44 + S45 tests: 31 passed
S46 + S47 tests: 34 passed
S48 tests:       12 passed
S49 + S51 tests: 26 passed
S52 tests:       13 passed
total:          116 passed
```

These are test-only author suites, not native C12/A5. They show the existing source executes and its intended targetless/controlled boundaries; they do not prove the target Neo-V3 architecture.

### 7.2 New tests required for T0

| Test | Claim | Expected failure control |
|---|---|---|
| T0-R1 | same source set resolves to same hashes on two roots | change one blob -> `SOURCE_IDENTITY_MISMATCH` |
| T0-R2 | committed event creates one actor state version | forced transaction exception -> no rows |
| T0-R3 | duplicate event identity with different content refuses | replay same content returns same receipt |
| T0-R4 | no access -> world event exists, no actor impression/durable | add access -> expected semantic read appears |
| T0-R5 | missing CAN008/CAN011 -> `HELD_MISSING_RULE` | no rule changed to no-change |
| T0-R6 | lawful no-change produces a positive typed record | remove no-change rule -> held |
| T0-R7 | render failure after commit -> `RENDER_FAILED`, no applied-clean | renderer cannot alter state hash |
| T0-R8 | batch 3/4/5 accepted; 0/1/2/6 rejected | no silent filler |
| T0-R9 | E2 source denied -> E3–E5 not realized under prefix policy | independent suffix needs separate owner policy |
| T0-R10 | E2 access absent -> E2 world event, no actor state; E3 prefix policy | event ID not leaked to retrospective packet |
| T0-R11 | SCI05 denied -> dependent proposals invalid, independent survives | no self-account state write |
| T0-R12 | remove exactly one access feature -> no direct/indirect recall | world unchanged |
| T0-R13 | functional relation add/retire/scope change by value | no relation -> no recruitment |
| T0-R14 | coactivation evidence alone -> candidate only, no durable relation | owner decision required |
| T0-R15 | external support change with fixed organization -> different resource outcome, not learning | remove support -> change reverses |
| T0-R16 | B source absent -> `SOURCE_OWNER_HOLD`; controlled B remains labeled | fake default refused |
| T0-R17 | replay same turn -> same event/state/response; provider count preserved | changed rule/source -> refusal |

### 7.3 Tests not run

- current PRE-MAIN C0/C11 full suites and actual source data;
- C8 protected writer D1/D2/D3;
- current C9 production Rule A/T (none issued);
- native C11/C12/A0–A5;
- actual provider/LLM call on the target architecture;
- human A5 evaluation;
- full external B lifecycle.

Report these as `NOT_RUN`, not as failures and not as positive evidence.

---

## 8. Decision / owner matrix

| Decision | Current state | Owner | Required before implementation? |
|---|---|---|---|
| Source registry/hash/portable paths | design ready | C9/C12 engineering + source owners | yes for T0.1 |
| Actor/event transaction + state version | design ready | C9/C12 engineering; CAN011 for durable semantics | yes for T0.2 |
| Retrospective access filter | design ready; law held | ADP016/017 + SCI05 + V2 | filter can be built; admission requires owner |
| Batch prefix vs atomic policy | explicit alternatives | C6/C9/C12 owner | yes before T0.5 commit policy |
| Concrete CAN008 Rule A | unissued | CAN008/010 owner | yes for semantic positive |
| Concrete CAN011 Rule T/NO_CHANGE | unissued | CAN011 owner | yes for durable positive |
| Care/activity intervals | partial workshop only | world/SDTF/ADP019 | yes for full N06/N07 |
| Functional relation formation/recruitment | missing law | science issuer + CAN/ADP | yes for durable relation |
| B source | empty actual | ADP019/C8/world | yes for independent B |
| C0/C11 source/C11 weld | unwired / permission held | Pyat C11/source custodian | yes for C0/C11 |
| Native C12/A0–A5 | none | C12/Pyat/A5 owners | yes |

No decision above is self-issued by SYN02-D.

---

## 9. Acceptance / rejection

**ACCEPT_SCOPED for this plan if:** the architecture reuses actual current source, names exact producers/consumers, preserves source/authority separation, makes no invented psychology, and provides implementable T0/T1/T2 tranches with tests.

**RED_IF:** old V3 formulas are copied into new Neo-V3 state; all-to-all graph or automatic Hebbian relation creation is assumed; sourcefree S37/S48/S52 is called a native person; renderer text writes psyche; `PRIOR_B_REFUSAL` is called actual B; a missing rule is called NO_CHANGE; or a green test is used to issue CAN/ADP/Pyat/C11/C12 authority.

**HOLD_IF:** actual C0/C11 source or current C9/C12 consumer is unavailable, an owner withholds a required rule/source, or the current branch cannot be assembled portably. Continue lawful T0 design and name the finite owner decision; do not substitute a toy E1→E2 for the whole architecture.
