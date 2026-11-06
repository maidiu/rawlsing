# Minimum P3 implementation plan

**Purpose:** give Codex HQ a bounded, dependency-ordered construction plan that reuses the received engine and executed B1 mechanics without rebuilding them or counterfeiting native science. This is a plan, not a commission and not an authorization for native state.

## 0. Already executed — do not rebuild

| Component | Status | Action |
|---|---|---|
| #704 `BatchEngine`/`RecursionCycle`/`P2Owner` | accepted sourcefree TEST_ONLY, protected | Preserve; do not rewrite |
| B1 CAN008/CAN011/later-reader | 39/39 author tests; 9/9 adapter tests in this probe | Reuse the adapter pattern; do not rebuild B1 |
| B3A schema/readset transaction | independent ACCEPT_SCOPED for the repair | Reuse the transaction/readset pattern; do not reimplement the whole B3 engine |
| HQ300 / M01 | test-only candidates | Reuse rule/chain shapes at TEST_ONLY; do not promote to production |
| BP2P4J | joined product alpha | Reuse as first-consumer capital; do not build another joined-alpha shell |

The probe's `probe/b1_owner_adapter.py` is the reference for the owner-operation pattern: root/branch/clock/state hash, operation reservation, ambiguous HOLD, stored result, later reader. It is not a production module.

## 1. Task order

### Task P3-E1-1 — `P2PsychologicalStateStore` (highest leverage)

**Goal:** add a durable psychological-state store bound to the existing P2 session root/branch/actor/clock, without changing the engine.

**Files:**
- New: `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_psych_state.py` (or a new bounded package).
- Read/reuse: `p2_owner.py`, `contracts.py`, B1 `bfirst.py` transaction shape, B3A `target_owner.py` record shape.

**Types:**
```text
PsychRecord:
  record_id, root, branch, actor, kind,
  target_refs, lifecycle, payload,
  source_rule_id, source_rule_version, source_rule_hash,
  causal_parent_refs, effective_from, effective_to,
  prior_record_hash, receipt_hash, grade

PsychOperation:
  operation_id, proposal_hash, before_state, status,
  result, refusal
```

**Methods:**
```text
open(state_root, root, branch, actor, source_rule_ref) -> store
snapshot_rows() -> list[PsychRecord]
state_hash() -> digest(rows)
apply(operation_id, effect_proposal, expected_state) -> receipt
read_later(kind, target_refs, clock) -> active records
verify() -> bool
```

**Transaction requirement:** use the same SQLite file as the P2 session if the base session exposes a transaction hook; otherwise create `psych_state.sqlite` under `session.state_root` and use a durable two-phase protocol:
1. reservation committed before the P2 event;
2. P2 event/interval commit;
3. psychological commit with an operation receipt;
4. a crash between 2 and 3 leaves an explicit ambiguous HOLD, never a blind repeat.

Do not claim cross-database atomicity without a real protocol. The B1 probe's reservation/HOLD pattern is the minimum.

**Tests:**
- cold reopen returns the same rows and hash;
- same operation ID returns the same receipt;
- ambiguous reservation refuses;
- wrong root/branch/actor/clock/source/rule/version refuses before mutation;
- tampered row or readset refuses;
- dormant row remains stored;
- exact severance breaks `read_later`; exact restore restores.

**Done when:** a 3-event sourcefree batch commits one `PsychRecord`, changes `snapshot().state_hash`, and cold replay returns the same record without duplication.

### Task P3-E1-2 — extend `P2Owner` (or add `P2PsychologicalOwner`)

**Goal:** make the engine see the psychological state and call the store.

**Files:**
- `p2_owner.py` or a subclass `p2_psych_owner.py`.
- `contracts.py` unchanged unless a new consequence field is required.

**Exact changes:**
1. `snapshot()`: `state_hash = digest({material..., "psych": psych_store.state_hash()})`; include the store's rows in the material.
2. `validate_proposal()`: accept only the existing P2 `ADMIT_EVENT` fields plus an optional explicit `psych_effect` request; validate rule/source/version against the test-only registry; do not accept a prose impression as an effect.
3. `_realize()`: after `s.admit_event`/`read_event`/`read_c9_conditioning`, call `psych_store.apply(...)` when a test-only rule is present; if no rule, return `durable_psychological_transition: MISSING_RULE` as today.
4. `consequences`: add `psych_record_id`, `psych_receipt`, `psych_state_changed`, `native_science: NOT_ISSUED`.
5. Keep `operations` custody; the psychological store must resolve a repeated operation ID or HOLD.

**Tests:**
- existing P2 tests still pass unchanged;
- a sourcefree event with a test-only effect changes `state_hash`;
- no-effect event returns `MISSING_RULE`, not `NO_CHANGE`;
- stale/wrong operation/state refuses before P2 event admission;
- production guard remains empty.

**Done when:** `BatchEngine` with the extended owner realizes a 3–5-event batch whose `state_hash` includes a psychological record, and `history` survives cold reopen.

### Task P3-E1-3 — later P2 consumer

**Goal:** prove the next P2 event reads the committed psychological state and produces a computed difference.

**Candidate seams (choose one, smallest first):**
- C9 eligibility path: a `PsychRecord` of kind `MEDIATOR`/`PRACTICE` is consulted by the existing C9 conditioning read; the event's `objective_material_eligible` or action eligibility changes.
- Actor response path: a `PsychRecord` changes an admissible route/action in the S43/S36 response surface.
- Do **not** change a narrative field and call it a consumer.

**Files:**
- P2/C9 read path or the S43/S36 response path.
- A read-only `read_psych_for_event(event_ref, clock)` function.

**Tests:**
- byte-identical later event under prior record vs no record produces different computed output;
- removing the record breaks the consumer; restoring exact bytes restores it;
- wrong actor/root/branch/clock/source/rule/version refuses;
- a dormant record does not force outward behavior;
- no model/provider call between events.

**Done when:** the computed later difference is in an actual permitted/action result, not a prewritten description.

### Task P3-E1-4 — test-only rule registry adapter

**Goal:** let B1/B3A/HQ300/M01-style rules run under the owner without touching the production registry.

**Files:**
- New `test_only_rule_registry.py` with a frozen, explicit registry of candidate rule IDs and their content hashes.
- No change to `rawlsing_next/v3_psepf_zero_positive_guard.py`.

**Rules:**
- `TEST_ONLY` registry is per-run/fixture, not global mutable state.
- Rule identity, version, content hash and owner must be exact.
- A missing rule returns `MISSING_RULE`, not `NO_CHANGE`.
- Production `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` remains empty.
- A test must assert `DENY_ZERO_EFFECT` for the same request that the test-only registry accepts.

**Done when:** the positive test-only path and the production deny path coexist in the same test run.

### Task P3-E1-5 — sparse-event selection metadata (product-level, not native psychology)

**Goal:** support the user-settled sparse-event hypercompression without pretending every selected event is a random natural sample.

**Files:**
- Event/proposal metadata: `selection_basis`, `historical_scope`, `representativeness`, `compression_note`.
- No psychological delta; no universal multiplier.

**Tests:**
- each selected event carries a nonempty, typed selection basis;
- a no-psychology event may still change world/relationship/project state;
- the event's selection basis is not silently converted into a psychological rule;
- a sparse batch can contain a dormant event, a continuity event, and a transformation event.

**Done when:** the 3–5-event batch can express why each event is selected without making every event mutate a target field.

### Task P3-E1-6 — lifecycle, contradiction and inhibition

**Goal:** add only the operations the existing capital lacks, at test-only first.

**Minimal operations:**
- `CREATE` (B1/B3A already have)
- `REINFORCE`, `WEAKEN`, `SET_DORMANT`, `REACTIVATE`, `TRANSFORM` (canonical names only; concrete predicates must be issued)
- multiple records with incompatible payloads; no scalar winner
- explicit `UNEVALUABLE`/`MISSING_RULE` when a record cannot be composed

**Tests:**
- two contradictory records coexist;
- a dormant record does not act; reactivation restores action;
- a lifecycle operation without an issued rule is refused;
- a later reader can distinguish activation from formation;
- no automatic elapsed-time decay or reinforcement.

**Done when:** the store and later reader can represent coexistence, dormancy and activation without inventing a composition rule.

### Task P3-E1-7 — scientific issuance, then native

**Only after 1–6 are test-only green:**
- choose the first narrow family: CAN-008 Rule A, CAN-011 Rule T (O05), or ADP-016 memory;
- obtain exact issuer/owner rule, source, scope and later consumer;
- add the production registry entry through the separately accepted authority change;
- then, and only then, claim native transition.

Do not start here.

## 2. Dependency graph

```text
P3-E1-0 (preserve engine/probe)
  -> P3-E1-1 (psych state store)
  -> P3-E1-2 (owner extension)
  -> P3-E1-3 (later consumer)
  -> P3-E1-4 (test-only registry)
  -> P3-E1-5 (sparse selection metadata) [parallel with 1-4]
  -> P3-E1-6 (lifecycle/contradiction) [after 1-3]
  -> P3-E1-7 (science issuance) [only after 1-6]
```

P3-E1-5 is product-level and can proceed in parallel; it does not depend on the psychological store. P3-E1-6 depends on the store and the later reader. P3-E1-7 depends on all engineering and the competent science owner.

## 3. Exact test gates for Codex

| Gate | Required evidence |
|---|---|
| G-ENG-1 | Existing #704 engine tests still pass unchanged |
| G-ENG-2 | Existing P2 tests still pass unchanged |
| G-PSY-1 | 3–5-event batch commits a typed psychological record with a receipt |
| G-PSY-2 | `snapshot().state_hash` changes only when the record is committed |
| G-PSY-3 | Cold reopen returns the same record, hash and later result |
| G-PSY-4 | Same operation ID returns the same receipt; ambiguous reservation HOLDs |
| G-PSY-5 | Wrong root/actor/branch/clock/source/rule/version refuses before mutation |
| G-CON-1 | Byte-identical later event differs only when the prior record exists |
| G-CON-2 | Severance breaks the later consumer; exact restore restores it |
| G-CON-3 | Dormant record remains stored without forced outward behavior |
| G-CON-4 | Contradictory records coexist; no scalar winner without an issued rule |
| G-SCI-1 | Production guard still `DENY_ZERO_EFFECT` / `ZERO_POSITIVE_REGISTRY` |
| G-SCI-2 | Missing rule returns `MISSING_RULE`, not `NO_CHANGE` |
| G-SCI-3 | No prose impression becomes a record without a typed effect/owner rule |
| G-RES-1 | Per-actor/per-batch bytes and time measured; no hidden thousand-event simulation |
| G-RES-2 | No model/provider call between events; no provider mutation of owner state |

## 4. What not to build

- A second developmental engine, batch cycle or CLI.
- A second B1/B2/B3A canary or joined-alpha shell.
- A new arbitrary psychological delta formula or a universal event weight.
- A V3 numeric revival (0–100 modules, yearly drift, fixed trait defaults).
- A production registry entry without the competent accepted authority change.
- A memory/practice/belief inferred from an LLM's retrospective prose.
- A material tool bit relabeled as an acquired psychological capacity.
- A generic "personality" test that only compares narrative output.

## 5. Ownership and overlap

| Surface | Owner | This return's role |
|---|---|---|
| #704 engine, `contracts.py`, `p2_owner.py` | received engine owners | preserve; no rewrite |
| P2 S45–S47 material/C9 actor root | P2 owners | extend, do not replace |
| B1/B2/B3A/HQ300/M01/BP2P4J | their historical authors | reuse at TEST_ONLY; no silent adoption |
| CAN-008/CAN-010/CAN-011/CAN-012 | original science owners | hold; no issuance |
| ADP-015/016/017/019/020/021 | original science owners | hold; no issuance |
| O05/O07/C9/O15/C4/C8 | original gate owners | hold; no acceptance |
| Production positive registry | separately accepted authority owner | keep empty |
| Sparse-event product design | user/product owners | metadata and compression, not native psychology |

No overlap with the simultaneous Browser P3-S1 scientific-compression worker: this return writes only this directory and does not claim an interworker dependency.

## 6. If Codex can implement only one thing

Implement **P3-E1-1 + P3-E1-2 + P3-E1-3** as one bounded slice:

```text
psych_state.sqlite rows keyed by root/branch/actor/clock
  -> P2Owner.snapshot includes them
  -> P2Owner._realize commits one test-only record with a receipt
  -> next P2 event reads it and changes one computed action/eligibility
  -> cold replay, wrong-key refusal, severance/restore, production deny all pass
```

That slice makes the next scientific commission concrete without rebuilding any historical engine. Everything beyond it is either a second rule family, a lifecycle extension, or native issuance.
