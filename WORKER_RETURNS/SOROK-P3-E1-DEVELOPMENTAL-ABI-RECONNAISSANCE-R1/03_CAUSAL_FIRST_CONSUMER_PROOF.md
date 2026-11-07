# Causal first-consumer proof — executed B1 compatibility chain

**Grade:** `TEST_ONLY_B1_DEVELOPMENT_OWNER_ADAPTER_NOT_NATIVE`. This is sourcefree engineering evidence. It does not issue CAN-008/CAN-011/ADP-016/ADP-017 science and does not claim a generated native person.

**Execution root:** isolated worker worktree at protected start `c852d7516e23fcb6cf2215e9be7c5fa268503516`. **Host:** macOS 13.7.8 x86_64, CPython 3.11.3, pytest 9.1.1. **Model reported:** `opencode/deepseek-v4.1-flash`; reasoning effort not machine-observable.

## 1. What was actually run

| Run | Command | Result |
|---|---|---|
| B1 author court | `python3 -B -m pytest -q -p no:cacheprovider probe/vendor/B1/test_bfirst.py` (pinned B1 bytes) | **39 passed in 0.50s** |
| Engine core | `python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_engine.py` | **45 passed in 0.99s** |
| Engine coordinator | `.../tests/test_model_cycle.py` | **19 passed in 0.36s** |
| Adapter court | `python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py` | **13 passed in 0.86s** |
| Full probe | `python3 -B run_probe.py` | **0**; positive/control, scaling, guard, JUnit receipt written |

Receipts:

- `probe/receipts/PROBE_RECEIPT.json` — host, git, source pins, positive/control traces, scaling, guard, pytest counts.
- `probe/receipts/junit.xml` — pytest JUnit.
- `probe/source_pin.json` — B1 and engine pins.

## 2. The positive three-event batch

The batch is three `EventProposal`s at times 2, 3, 4:

| Event | Event hash | Input | Observed status | Observed action |
|---|---|---|---|---|
| `event1` | `abe04b9e0812fd9fb23ad19c0060dae36a2ee917a5e7529e7c6b36450716df7d` | interrupted bike-loss offer, `joint_inventory` | `REALIZED` | `compare_current_plan:caretaker` |
| `event2` | `b54f9838f8f33f5fc1161ecbab6a2645cdc189c4e05a398fbfff6586492b08d5` | non-interrupted offer, `no_plan` | `NO_CHANGE` | none; mediator remains |
| `event3` | `5686ac24711ffb79411c5658ab29f96328df5cd7da375683c683e6bd8455392d` | non-interrupted offer, `joint_inventory` | `REALIZED` | `joint_check:caretaker` |

Persisted state after the batch:

```text
mediator middle_state_id         994680cacb8f98757302ad2d6435e2c1052bd8f7cb8052aebb199efebc6df765
mediator record hash             c06f526ae0fbfebb5af37bda74846c93716b03016a0a6fb2ce3e13d0e197c495
StateIdentity                    root=root-positive actor=child branch=main clock=4
state_hash                       0bd9a3249f2f42a4a71326610c70a9d085283a01b626f8ef8921dad88e5bf872
history_hash                     d34f5032df58d1a3bcdcb2c02059d45a78bd4bbfa692198c5b9f85fddb6f7c9f
```

The later reader is `propose()` at `bfirst.py:161`, using `mode_for()` at line 152 and the ACTIVE-middle match block. `event3`'s `recruited` is exactly the persisted record hash; the actor-visible surface contains only the action and `origin_explanation=NOT_ACCESSIBLE`. The mediator's `governed_payload.mode='joint_check'` is not in `event1`'s accessible surface; it is engine-internal objective history.

The event-2 result is the dormant-effect control: the response is valid-empty, no outward action occurs, the mediator is still in `state['middle']`, and event 3 later activates it.

## 3. The causal contrast

The control run uses byte-identical proposals (the same `EventProposal` objects; same source reference, event IDs, times, offers, participants) and the same B1 rule, but `journal_only=True`, which suppresses the CAN-011 target commit while retaining the admitted occurrence and response record. This is a test-only suppression control, not a natural "no-mediator" life.

| Measure | Positive | Journal-only control |
|---|---|---|
| Event hashes | `abe04b9e…`, `b54f9838…`, `5686ac24…` | identical |
| Event 3 hash | `5686ac24711ffb79411c5658ab29f96328df5cd7da375683c683e6bd8455392d` | **identical** |
| Mediator count | 1 | 0 |
| Event 3 recruited | `[c06f526a…]` | `[]` |
| Event 3 action | `joint_check:caretaker` | `inspect_alone:caretaker` |
| Event statuses | `REALIZED, NO_CHANGE, REALIZED` | `IMMEDIATE_ONLY, IMMEDIATE_ONLY, IMMEDIATE_ONLY` |
| Owner DB | 94,208 bytes | 86,016 bytes |
| State JSON | 15,220 bytes | 8,501 bytes |
| Responses | 3 | 3 |
| Transitions | 1 | 0 |

The difference is a computed response difference from stored prior state, not a comparison of prewritten narrative. It is still **authored test-only** psychology: the B1 rule's mapping from recognized/imposed plan to `joint_check`/`private_check` is a `PROVISIONAL_MODEL_HYPOTHESIS`.

## 4. Cold reopening

After the positive batch, the owner and engine were closed and reopened on the same SQLite files:

- `engine.history("batch-positive")` returns the exact stored records.
- `owner.snapshot()` equals the final `StateIdentity` above.
- The mediator is still present; `responses` = 3; `middle` = 1.
- `run_batch("batch-positive", proposals)` returns the same result without duplicating the mediator or effect.
- Cold history read took **0.005953 s** (positive) and **0.004826 s** (control) on this host.

## 5. Source severance and exact restoration

The actual later reader is state-dependent, not a static fixture:

1. A fresh DB is advanced through `event1` and the dormant `event2`; its mediator is stored.
2. The DB is byte-copied.
3. In the copy, the mediator is removed from `checkpoint['middle']` (an exact state severance; the orphan transition is not consulted by the later reader).
4. The same `event3` proposal then yields `inspect_alone:caretaker` and `recruited=[]`.
5. The original DB (never mutated after the pre-event copy) yields `joint_check:caretaker` and `recruited=[c06f526a…]`.
6. The exact pre-event DB bytes are copied over the tampered path, and the same `event3` is run again with a fresh operation ID. It yields `joint_check:caretaker` and `recruited=[c06f526a…]`.

This proves the later response consumes the stored mediator edge. The restoration is exact at the SQLite-file byte level from the pre-event copy; the tampered copy is the severed control.

Additional source custody:

- **Foreign root:** reopening the same DB with root `root-b` raises `B1_OWNER_BINDING_MISMATCH`.
- **Source identity tamper:** rewriting `b1_source.response_rule_hash` raises `B1_SOURCE_IDENTITY_TAMPERED`; exact body restoration restores `snapshot()`.
- **Bad middle rule version:** changing `creation_or_update_rule_ref.rule_version` in a persisted mediator raises `B1_PROPOSAL_REFUSED:MIDDLE_STATE_INTEGRITY_FAILURE` at the next proposal; owner state is unchanged.
- **Wrong source reference:** a proposal with `source_refs=("B1_FIXTURE:wrong",)` is refused before any occurrence or operation row is written.
- **Wrong clock:** `event_time == current clock` is refused before any mutation.
- **Wrong operation/interval/participants:** `CAN008_NATIVE`, a non-null interval, or a stranger participant is refused before mutation.

## 6. Operation ambiguity and no duplicate effects

- `realize("op-1", proposal, before)` returns a stored result; a second call with the same operation returns the same result.
- The same operation ID with a different proposal raises `B1_OPERATION_REUSE_MISMATCH`.
- A manually inserted `RESERVED` row for an uncommitted operation raises `B1_AMBIGUOUS_PRIOR_OPERATION_HOLD` and leaves the owner state unchanged.
- Deleting the ambiguous reservation and retrying commits once; the response count is 2, not 3, after events 1 and 2.

This is the same fail-closed custody pattern as `P2Owner`, not a blind reissue.

## 7. Production guard still denies

The probe loaded the actual protected `rawlsing_next/v3_psepf_zero_positive_guard.py` and evaluated a well-typed positive transition request:

```text
outcome = DENY_ZERO_EFFECT
reason  = ZERO_POSITIVE_REGISTRY
registry_empty = true
actor_state_effect = ZERO
causal_ledger_appends = 0
rng_mutations = 0
scheduler_mutations = 0
zero_effect = true
```

The B1 adapter does **not** mutate this registry. B1's rules remain `TEST_ONLY_CAN008_B1` / `TEST_ONLY_CAN011_B1`; they are not production entries. The adapter is a separate test-only store.

## 8. Mandatory matrix status

| # | Test | Status | How |
|---:|---|---|---|
| 1 | Valid actor/source/root | **PASS** | positive batch |
| 2 | Invalid actor or foreign root | **PASS** | `participants=("child","stranger")`; `B1Owner(root-b)` |
| 3 | Wrong clock | **PASS** | `event_time == owner.snapshot().clock` |
| 4 | Bad source/version hash | **PASS** | wrong `source_refs`; source-body tamper; mediator rule-version tamper |
| 5 | Missing scientific rule | **PASS for production DENY; native missing-rule owner path NOT_RUN** | production guard denies; B1's authored rule is labeled test-only |
| 6 | TEST_ONLY positive state effect | **PASS** | mediator record and changed state hash |
| 7 | Production positive registry still denying | **PASS** | guard receipt |
| 8 | State cold reopening | **PASS** | reopen + history + same snapshot |
| 9 | Later first-consumer reading the state | **PASS** | event 3 `recruited` / action |
| 10 | Same later event under changed prior state | **PASS** | positive vs journal-only control, identical event 3 hash |
| 11 | Atomic refusal before durable mutation | **PASS** | 0 occurrences, 0 operations, 0 journal batches on invalid proposals |
| 12 | Dormant/unexpressed effect stored | **PASS** | event 2 `NO_CHANGE`, mediator remains, event 3 activates |
| + | Source severance / exact restoration | **PASS** | mediator removal vs original DB |
| + | Ambiguity / no duplicate | **PASS** | RESERVED row HOLD; retry once |

**NOT_RUN (not PASS):**
- Full #704 `P2Owner` suite and the P2 S45–S47 closure in this probe root.
- B3A `Integration.run` through `DevelopmentOwner`.
- HQ300 `run_positive_chain` through `DevelopmentOwner`.
- M01 `Cell` through `DevelopmentOwner`.
- BP2P4J `JoinedProduct` through `DevelopmentOwner`.
- Original V3 yearly/flow tests against exact protected archive bytes.
- Any native CAN/ADP production operation.

The inherited author/independent results for those components remain historical evidence at their own cuts and are not recounted as new execution here.

## 9. New evidence versus inherited evidence

**New in this probe:**
- B1 39/39 (new run of pinned bytes).
- Engine `test_engine` 45/45 and `test_model_cycle` 19/19 (new run at protected start).
- Adapter 13/13 at the R02 head, positive/control, cold reopen, severance/restore, ambiguity, mode binding, guard (new).
- Scaling measurements 3/10/30/60 events (new).

**Inherited, not rerun:**
- #704 71/71 author suite, independent scoped reviews, P2 material→C9 contrast.
- B1 pending I2; B2 45+36 author tests, independent scientific review found authored labels; native F1 17 RED.
- B3A 71/63/42/33 author suites; independent I2 ACCEPT_SCOPED for schema/readset.
- BP2P4J 98 author tests and 7+3 severances; no independent complete acceptance.
- HQ300 317/317; production registry empty.
- M01 413/413; `MECHANISM_IDENTIFICATION_HOLD`.

## 10. Conclusion of the proof

The received engine can host a real stored-state → later-reader chain when an owner supplies the mapping. B1 is the smallest such owner. The proof does **not** show that the P2 actor root can do this: P2's `state_hash` does not include psychology and its `realize()` returns `MISSING_RULE`. That is the first production adapter.
