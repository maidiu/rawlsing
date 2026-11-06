# SOROK P3-E1 — developmental-capital recovery, DevelopmentOwner ABI and first-consumer reconnaissance

**Worker:** independent source-native historical-code, executable-ABI and minimal-adapter investigator.
**Repository:** `maidiu/rawlsing` (private).
**Worker branch:** `research/sorok-p3-e1-developmental-capital-abi-recovery-20261106-r1`.
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516` on `integration/pre-main-reconciliation-r1`, verified by `git ls-remote` before work.
**Received engine runtime cut:** `81b01f654f8ba09550d03df17e8014f43ffcfc9f`; PR #704 receiving merge `0b7d8ba33b5cd905963292357507ae7bbc2219de`.
**Host:** Darwin 22.6.0, macOS 13.7.8 x86_64; CPython 3.11.3; pytest 9.1.1.
**Editor / model:** OpenCode; runtime identifies `opencode/deepseek-v4.1-flash`. The user requested DeepSeek V4.1-Flash MAX; the harness did not expose an independently verifiable reasoning-effort value, so reasoning configuration is recorded as **NOT_MACHINE_OBSERVED**.
**Execution date:** 2026-11-06, UTC.

## Verdict

**The next meaningful developmental chain is already implemented in B1, and the received `DevelopmentOwner` ABI can host it through a narrow test-only adapter. The adapter was built and executed: 9/9 tests pass, a stored CAN-011 mediator changes the later response from `inspect_alone:caretaker` to `joint_check:caretaker` for byte-identical later events. The production boundary is not B1's ABI. It is the P2 actor root's missing psychological state writer/reader: `P2Owner` has no psychological state in `snapshot().state_hash`, no psychological writer in `realize()`, and no later psychological consumer. No native science is issued or claimed.**

The exact reusable chain is:

```text
B1 Event
  -> B1 propose()                         (authored sourcefree CAN008 response)
  -> TestOnlyCAN011Owner.validate()       (separate destination court)
  -> Store.commit()                       (one SQLite transaction: mediator record,
                                           response, transition, joint receipt)
  -> persisted checkpoint['middle']       (V3MS_MEDIATOR / REGULATORY_PROTECTIVE)
  -> later B1 propose()                   (mode_for()/matches read ACTIVE mediator)
  -> later practical_activity             (joint_check vs inspect_alone)
```

That chain is exactly what the engine needs from a `DevelopmentOwner`. What it lacked was not psychology: it lacked `StateIdentity` root/branch/clock/state_hash, operation-id idempotency, and `EventProposal`/`RealizedEvent` mapping. The probe adapter supplies only those.

## What was actually executed

| Command | Result | Evidence |
|---|---|---|
| `python3 -B -m pytest -q -p no:cacheprovider test_bfirst.py` in the pinned B1 return | **39 passed** | B1's own author court; new execution, not inherited upload |
| `python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_engine.py` | **45 passed** | new execution at protected start |
| `python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_model_cycle.py` | **19 passed** | new execution at protected start |
| `python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py` | **9 passed** | new probe court |
| `python3 -B run_probe.py` | **0**; positive/control and guard receipts written | `probe/receipts/PROBE_RECEIPT.json`; `probe/receipts/junit.xml` |

The B1 test command was run against the byte-identical pinned `bfirst.py` (Git blob `94ffc52847e4c8ae760212d1bc8543594ba793fa`, SHA-256 `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`). The engine files were verified against `SOURCE_PINS.json` in `probe/receipts/PROBE_RECEIPT.json`.

**Not run:** the full #704 `P2Owner` suite (it needs the complete protected P2 vendored closure; this probe deliberately used the extracted engine units), B3A through `DevelopmentOwner`, HQ300/M01 through `DevelopmentOwner`, BP2P4J through `DevelopmentOwner`, and original V3 tests against exact archive bytes. Those are marked NOT_RUN, not PASS. The inherited author and independent-review results remain historical evidence at their own cuts.

## Exact answers to the engineering questions

### Q1 — What already implements compatible portions?

| ABI concern | Existing implementation | Compatibility verdict |
|---|---|---|
| Actor-root state | `P2Owner.snapshot()` at `p2_owner.py:63`; `StateIdentity(root, actor, branch, clock, state_hash)` at `contracts.py:32` | P2 has a real root/branch/clock/hash, but the hash covers only world/events/intervals/encounters; no psychological field |
| Event source and actor access | `P2Owner.validate_proposal()` at `p2_owner.py:79`; `P2Owner.actor_experience()` at `p2_owner.py:147` | Sourcefree P2 event admission and actor perception receipts; not native ADP-019/ADP-017 |
| Response/effect transaction | B1 `Store.commit()` at `bfirst.py:304`; B2 `Bridge.advance()` at `bridge.py:156`; B3A `Integration.run()` at `integration.py:194` | B1 is the smallest complete transaction; B3A is stronger but frame-based; B2 adds an independent witness |
| Mediator/tension/practice state | B1 `state['middle']` records; B3A `b3_transition` records; `target_owner.validate()` at `target_owner.py:9` | Both are authored TEST_ONLY CAN-011-shaped records; neither is issued CAN-011 law |
| Causal trace or memory | HQ300 `run_positive_chain()` at `positive_chain.py:89`; M01 `Cell.prepare()/read_owner()` at `cell.py:66/90` | In-memory test-only ADP-016/ADP-017 candidates; no durable owner |
| Contextual activation/inhibition | B1 later `propose()` reads ACTIVE `middle`; B3A `response()` at `integration.py:119` reads ACTIVE practice | Recruitment exists; inhibition/deactivation/weakening does not |
| Persistent state and replay | B1 `Store` SQLite; B3A logical readset/atomic publication; #704 `BatchEngine` journal | B1 has durable cold replay; B3A has schema/readset acceptance; neither is on the P2 root |
| Later same-actor first consumer | B1 `propose()` `mode_for()` at `bfirst.py:152` and `matches` in `propose()`; B3A `response()`; HQ300 `ledger.read_effects()`; M01 `Cell.read_owner()` | B1's later reader is the actual response engine, not a separate consumer module; the probe proved it reads the stored mediator |

The exact ABI comparison, including every incompatible field, is in [`02_DEVELOPMENT_OWNER_ABI_MATRIX.md`](02_DEVELOPMENT_OWNER_ABI_MATRIX.md).

### Q2 — Which old tests demonstrate a real stored-state effect, and which only change material/menus/labels?

**Stored psychological-like field + later read (real within the test-only fixture):**
- B1: first event creates `checkpoint['middle']` mediator; later event recruits it and changes `practical_activity` (`joint_check` vs `inspect_alone`). New execution: 39/39 B1 tests; probe 9/9. The field is a CAN-011-shaped mediator, but the rule is authored `PROVISIONAL_MODEL_HYPOTHESIS`.
- B3A: `b3_transition` V3MS_PRACTICE record after two performed practices; `middle()` is read by `response()` and changes the later `CHECK_LOCK` action. Author 71/71, atomicity 63/63, F2 42/42; independent I2 accepted the schema/readset repair only. Not run here.
- HQ300: in-memory `ADP016_TRACE_COMMIT` + `ADP017_EPISTEMIC_UPDATE`; later event reads the prior effect and returns `DEFLECT` vs `AMPLIFY`. Author 317/317; production registry empty. Not run here.
- M01: in-memory applied ADP016/ADP017 fixture state produces later `BUFFER`/`DEFLECT`/`AMPLIFY` and `REROUTE`/`BLOCK` streams. Author 413/413; `MECHANISM_IDENTIFICATION_HOLD`. Not run here.

**Material/menu/label-only changes (do not count as psychogenesis):**
- #704/P2: ACTUAL vs SCHEDULED_ONLY changes `material_remaining` and C9 eligibility `[false,false,false]` vs `[true,true,true]`. That is a material-state dependence, not a psychological writer; the owner explicitly reports `durable_psychological_transition: MISSING_RULE`.
- BP2P4J: the committed practice is materialized into `projects`/`tools_remaining`; the offscreen repair completes because the tool is available. The C12 record is stored, but the demonstrated later difference is material/action, not a native psychological field.
- B1/B3A `uptake` labels and `admissible_routes` are output labels; they are not state unless the target record is committed and later read.
- S35 reports a candidate `NO_CHANGE` with no issued positive rule; that is not evaluated O07.

### Q3 — What is the first missing executable adapter?

**For the received engine as used in production: the missing adapter is inside `P2Owner`, not between B1 and the engine.**

Exact seam:
- Source: `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py`
  - `P2Owner.snapshot()` line 63: state hash is `digest({"world", "events", "intervals", "encounters"})`; no psychological rows.
  - `P2Owner.realize()` line 140 and `_realize()` line 194: admits the P2 event, produces an interval, reads S43/C9, and returns `durable_psychological_transition: MISSING_RULE`.
  - `P2Owner.validate_proposal()` line 79: accepts only `ADMIT_EVENT`, P2 source digest, root participants, `history_refs`/`language_context`, and ACTUAL/SCHEDULED_ONLY interval.
- Target: a new `DevelopmentOwner` implementation (or extension) that owns:
  1. a psychological state table keyed by `(root, branch, actor, state_id)`;
  2. an atomic commit joining the P2 event/interval transaction and the psychological effect;
  3. `snapshot()` state hash including the psychological rows;
  4. `realize()` returning the psychological effect receipt;
  5. a later consumer in the P2 event/action path that reads the committed psychological row.
- Incompatible fields: P2 has no `mediator`, `tension`, `practice`, `memory`, or `claim` table; its `world.actor_state` is material (`cash`, `free_hours`, `completed_units`, `material_remaining`, `tools_remaining`, `projects`, `skill`); its `EventProposal` cases are `history_refs`/`language_context`, not B1's `project`/`offers`/`interrupted`; its clock is the session clock, not B1's event time; its SQLite root is `session.state_root`, not B1's checkpoint DB.

**For B1 specifically: the smallest missing adapter was built and executed.** It is `probe/b1_owner_adapter.py`:
- `snapshot()` maps B1's checkpoint to `StateIdentity(root, 'child', branch, clock, digest(state))`.
- `validate_proposal()` maps `EventProposal` to B1 `Event` and calls the pure `propose()` preflight.
- `realize()` adds root/branch/state/clock checks, a durable `b1_operations` reservation, B1 `admit_fixture`/`propose`/`TestOnlyCAN011Owner`/`Store.commit`, and a `RealizedEvent` result.
- It does **not** claim B1's authored psychology is native; it preserves B1's `TEST_ONLY_CAN008_B1`/`TEST_ONLY_CAN011_B1` rule IDs.

The adapter is a compatibility witness, not the production bridge. The production bridge still needs the P2 seam above.

### Q4 — What can work now at sourcefree TEST_ONLY grade?

- **YES, executed:** B1's CAN008→CAN011→persisted mediator→later reader mechanics through `DevelopmentOwner`/`BatchEngine`, with a test-only rule. 9/9 probe tests pass; production registry remains empty.
- **NO, not demonstrated:** B3A through `DevelopmentOwner`. `Integration.run(data)` takes a full material/social frame, needs the pinned B2/M2 closure, and has no operation-id `DevelopmentOwner` protocol. A port is possible but is a larger adapter, not the smallest.
- **NO, not demonstrated:** HQ300/M01 through `DevelopmentOwner`. Their ledgers and `FixtureOwnerState` are in-memory; a durable wrapper must add SQLite, root/branch/clock, and operation receipts. The rule chains are reusable as test-only candidates, not as owners.
- **NO, not demonstrated:** BP2P4J through `DevelopmentOwner`. It is a separate BP4 product with its own C8/C9/C10/C12 and world; it is high-value first-consumer capital but not a drop-in owner.

### Q5 — What cannot work without scientific issuance?

See [`04_SOURCE_SCIENCE_AND_NATIVE_HOLDS.md`](04_SOURCE_SCIENCE_AND_NATIVE_HOLDS.md). The exact holds are: CAN-008 Rule A, CAN-011 Rule T, CAN-010 need/expectation/striving, ADP-016 formation/retention/forgetting/recall, ADP-017 knowledge/first-person claim, ADP-019 native admission, ADP-020 causal RNG, ADP-021 native scheduler, CAN-012 rupture, O05/O07 acceptance, C9 native integration, O15 native later-E2 reader, C4 actor source, C8 action/omission, independent B source/owner, and any human/native-person claim. The production positive registry is empty and immutable; adding an entry requires a separate accepted authority change.

### Q6 — What compressed-development functionality is missing?

| Functionality | Existing capital | Exact gap |
|---|---|---|
| Actor-history state under sparse events | B1 synthetic prehistory + `responses`/`middle`/`transitions`; B3A `b3_source`; P2 event/interval history; V3 `events_this_year`/`micro_trace_this_year` (unverified archive) | No sparse-event salience/selection layer; B1's history is an authored fixture, not a generated life |
| Multi-event accumulation | #704 3–5 batch; B1 sequential responses; B3A 9-episode loop; HQ300/M01 two-event chains; BP2P4J | B1 only CREATEs one mediator per project/counterpart then recruits; no reinforcement/weakening/transformation across many selected events |
| Selective durable transformation | B1 `V3MS_MEDIATOR`; B3A `V3MS_PRACTICE`; HQ300 ADP016/ADP017; M01 memory/epistemic | No issued selective rule; B1/B3A are TEST_ONLY |
| Activation/inhibition without creation | B1 ACTIVE mediator recruitment; B3A ACTIVE practice → `CHECK_LOCK` | No inhibition, set-dormant, reactivation, weakening, or context-sensitive latency operation |
| Contradictory coexisting mediators | B1 supports multiple mediators for the same project/counterpart (`test_same_history_multiple_opposed_mediators_coexist`); B3A permits valid-empty/contradictions | No later composition/priority rule; B1's coexistence is not a contradiction-resolution mechanism |
| Material and relational context | B3A material acts/exposures/capability/readset; BP2P4J tool/material; P2 material interval/C9; B1 relation/project/power labels | B1's `world_ref`/`power_ref` are labels, not read material resources; no single schema joins material resource + relational mediator + sparse history |
| Actor-limited retrospective access | B1 `actor_surface` with `origin_explanation=NOT_ACCESSIBLE`; B3A `actor_safe` + `ADP017_access=HEARING_ONLY`; HQ300 K3; M01 audit-only; P2 actor perception | No issued ADP-017/M6 claim/expression right; B1's inaccessible history is fixture data, not a reader |
| Nondeclarative influence | B1 mediator changes later action without exposing the mediator; B3A active practice changes action; HQ300 causal trace is non-first-person; M01 hidden trace | No native ADP-016 trace or ADP-017 permission; B1's influence is authored rule |
| Durable change externally invisible | B1 mediator is stored and absent from `actor_surface`; B3A transition is stored and only the action is surfaced; HQ300 trace `content_first_person_readable=false`; M01 audit-only | B1 is durable SQLite; HQ300/M01 are in-memory; no native retention/access rule |

The strongest existing test-only evidence for *contradictory coexisting mediators* is B1. The strongest existing evidence for *material/relational context* is B3A/BP2P4J. The strongest existing evidence for *memory/knowledge mediation* is HQ300/M01. None is a drop-in native writer.

## Highest-leverage next implementation for Codex HQ

Do not rebuild #704, B1, B3A, HQ300, M01, or BP2P4J. The next bounded construction is:

1. **Define a psychological-state seam on the P2 actor root.** Add a `PsychologicalStateStore` (or `DevelopmentWriter`) with typed records for the selected CAN-011/CAN-010/ADP-016 family, keyed by root/branch/actor/clock, with a durable commit receipt.
2. **Extend `P2Owner.snapshot()`** so `state_hash` covers both the existing world/event/interval/encounter material and the psychological rows. Without this, the engine cannot detect a psychological change.
3. **Extend `P2Owner._realize()`** to commit the psychological effect in the same logical transaction as the P2 event/interval, or add a durable two-store protocol with an operation receipt and an ambiguity HOLD. Keep `MISSING_RULE` when no rule is issued.
4. **Add the later P2 consumer.** The earliest lawful consumer is the next event's C9/action eligibility or the actor's response path; it must read the committed psychological row, not a narrative impression.
5. **Keep the production registry empty.** Use a `TEST_ONLY` rule registry adapter for the first B1/B3A/HQ300/M01-style rule; do not mutate `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES`.
6. **Only then** request the competent original-science issuance for the chosen Rule A/T/memory transition.

The detailed task order, files, test gates and ownership boundaries are in [`05_MINIMUM_P3_IMPLEMENTATION_PLAN.md`](05_MINIMUM_P3_IMPLEMENTATION_PLAN.md).

## Mandatory test matrix

| # | Required test | Status | Evidence |
|---:|---|---|---|
| 1 | Valid actor/source/root | **PASS** | `test_positive_three_event_batch...`; positive receipt |
| 2 | Invalid actor or foreign root | **PASS** | `test_invalid_actor...`; `test_foreign_root...` |
| 3 | Wrong clock | **PASS** | `test_invalid_actor...` (`event_time=clock`) |
| 4 | Bad source/version hash | **PASS** | `test_invalid_actor...`; `test_foreign_root...`; `test_middle_rule_version...` |
| 5 | Missing scientific rule | **PASS (test-only rule explicit; production unissued)** | `test_production_zero_positive_guard...`; B1 rule IDs are `TEST_ONLY_*` |
| 6 | TEST_ONLY positive state effect | **PASS** | mediator id `994680…`, record hash `c06f526a…`; state hash changes; later action |
| 7 | Production registry still denies | **PASS** | guard `DENY_ZERO_EFFECT` / `ZERO_POSITIVE_REGISTRY` |
| 8 | State cold reopening | **PASS** | `test_positive...` reopened section; cold history 0.006s |
| 9 | Later first consumer reads state | **PASS** | `records[2].recruited == c06f526a…`; `joint_check:caretaker` |
| 10 | Same later event under changed prior state | **PASS** | identical event hash `5686ac24…`; positive `joint_check` vs control `inspect_alone` |
| 11 | Atomic refusal before durable mutation | **PASS** | `test_invalid_actor...`: 0 occurrences, 0 operations, 0 batches |
| 12 | Dormant/unexpressed effect stored | **PASS** | event 2 `NO_CHANGE`, no action, mediator remains; event 3 activates |
| + | Source severance / exact restoration | **PASS** | `test_mediator_severance...`; `test_foreign_root...` |
| + | Operation ambiguity, no duplicate | **PASS** | `test_operation_idempotency...` |

P2 native event admission, P2 full owner suite, B3A through `DevelopmentOwner`, HQ300/M01 through `DevelopmentOwner`, BP2P4J through `DevelopmentOwner`, and exact V3 archive tests are **NOT_RUN**, not PASS.

## Resource findings, measured

B1 3-event positive: owner DB 94,208 bytes; journal 98,304; state JSON 15,220; records 23,239; 1 mediator; 3 responses; 1 transition; 3 occurrences; 3 joint receipts; 3 operation rows. Control: DB 86,016; state 8,501; 0 mediators; 3 responses. Cold history replay 0.006s. Scaling (direct B1 owner): 3 events 94 KB / 9.7 ms per event; 10 events 217 KB / 12.2 ms; 30 events 549 KB / 16.9 ms; 60 events 1,065 KB / 23.7 ms; state 15,334 → 124,313 bytes. B1 rewrites one full checkpoint JSON per event and scans growing `responses`; this is acceptable for a 3–5-event batch but not a hidden thousand-event microsimulation. Full measurements and unmeasured fields are in [`06_RESOURCE_COST_FINDINGS.md`](06_RESOURCE_COST_FINDINGS.md).

## Non-claims

- No native CAN-008/009/010/011/012 or ADP-015/016/017/019/020/021 issuance.
- No O05/O07/C9/O15 acceptance; no actor C4/C8 source grant.
- No native generated person, independent B owner, human validation, privacy/deletion right, or product acceptance.
- No modification of product code, original science, historical worker returns, protected PROGRAMMA documents, or PRE-MAIN.
- No Codex usage and no delegation.
- The adapter's positive result is **sourcefree test-only engineering**: it proves the engine can host B1's authored rule and durable mediator, not that a human would develop this way.

## Publication

**Worker branch:** `research/sorok-p3-e1-developmental-capital-abi-recovery-20261106-r1`.
**Base:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`.
**Evidence commit:** `a2c3c36ef7c29432df92806271b31a64f344cd78` (16 files, pushed and verified). This public note is a subsequent metadata commit; the branch HEAD is reported in the worker's final message. A tracked file cannot contain its own containing commit SHA without a circular preimage.
**PR:** not opened by this worker; `gh` is unavailable on the host and the task leaves PR creation to repository permissions. The branch is ready to push.

I did not review my own work. Independent review, scientific issuance and protected receiving remain with their competent owners.
