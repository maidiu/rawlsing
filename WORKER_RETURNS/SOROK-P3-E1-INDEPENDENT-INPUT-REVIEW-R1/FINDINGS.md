# E1 input review — detailed findings

**Exact subject:** `ee1ff298fe7e57277c34a5af16df33165743d84f` / PR #735.
**E1 tree:** `5af145f2b0192636aba7adc6944813ef4fb703a5`; startup copy at `5f30f4f89` has the same tree.
**Protected start:** `c852d7516e23fcb6cf2215e9be7c5fa268503516`.
**Review grade:** independent source-consistency/engineering input review; no native science or protected receiving.

## 1. Method and scope

I read the full E1 return (`00`–`06`), the actual `b1_owner_adapter.py`, nine-test probe court, `run_probe.py`, source pins, receipts, vendored B1 `bfirst.py`, and the native receiving `DevelopmentOwner`/`P2Owner` source. I executed the nine probe tests and `run_probe.py` at the exact E1 tree in a `git archive` scratch copy, then independently exercised the positive, identical-later-event control, cold reopen and wrong-source refusal through the actual `B1Owner`/`BatchEngine` path.

I did **not** rerun B1's 39-test author court, the #704 45/19 engine courts, B3A/HQ300/M01/BP2P4J, or historical V3 tests. E1 discloses those as inherited/not-run; the instruction says not to redo all B1/#704 without a demonstrated need. The B1 vendored bytes are exact, and the nine probe tests are the claimed new execution.

## 2. Exact source identity and pins

- E1 tree at subject `ee1ff298` and at the startup `5f30f4f89` is identical: `5af145f2b0192636aba7adc6944813ef4fb703a5`.
- Vendored `probe/vendor/B1/bfirst.py`: SHA-256 `478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3`, Git blob `94ffc52847e4c8ae760212d1bc8543594ba793fa`; matches B1 commit `c0f4588c158b40c8903b4aae2f292eae5238b8a0` exactly.
- All 14 E1 `engine_files` entries in `probe/source_pin.json` match the startup engine files. Key hashes: `p2_owner.py` `fd98a757…`, `engine.py` `ba6caa74…`, `contracts.py` `9aabbc9f…`, `model_cycle.py` `af83f8f1…`.
- Probe file SHA-256 values: `b1_owner_adapter.py` `c56732eb…`, `run_probe.py` `3364d531…`, `test_b1_owner_adapter.py` `daf5d25c…`; they match E1 `source_pin.json`.
- E1's stored `PROBE_RECEIPT.json` records `git.current_head=0d6baf55…`, the parent of final subject `ee1ff298`. The final commit adds the exact pre-event restore and test changes. This is a **pre-final-commit receipt provenance limit**; independent execution at the exact subject tree passes 9/9 and the receipt's positive/control hashes match.

## 3. Independent execution

```
cd <exact-E1-scratch>/WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
# 9 passed in 0.46s

PYTHONDONTWRITEBYTECODE=1 python3 -B run_probe.py
# exit 0; positive joint_check:caretaker; control inspect_alone:caretaker;
# guard DENY_ZERO_EFFECT; pytest 9/9
```

Independent direct witness (`logs/e1-positive-control-cold-refusal.log`):

```
positive statuses: REALIZED, NO_CHANGE, REALIZED
positive event hashes: abe04b9e…, b54f9838…, 5686ac24…
record state hashes: c28d6ccb…→48d11851…, 48d11851…→d082f85d…, d082f85d…→0bd9a324…
mediator: 994680ca… / record c06f526a…
event3: joint_check:caretaker; recruited [c06f526a…]
control statuses: IMMEDIATE_ONLY ×3
control event hashes: identical; event3 inspect_alone:caretaker; recruited []
control mediator count: 0
cold snapshot equal: True; cold history equal: True; cold mediator_count 1; response_count 3
refusal (wrong source): B1_SOURCE_REF_MISMATCH; state_same True; occurrences 0; operations 0; batches 0
```

The positive/control equality is confirmed at the `EventProposal` and B1 event-hash level; the later event is byte-identical. The difference is the stored mediator, and event 3 reads it.

## 4. Is the mediator actually read by the later response?

Yes, at the B1 test-only scope:

- B1 `propose()` creates a `V3MS_MEDIATOR` for the interrupted event (`bfirst.py:190-209`).
- `Store.commit()` appends the mediator record and transition to the checkpoint under `BEGIN IMMEDIATE` (`bfirst.py:304-349`).
- Event 2 is a valid-empty `NO_CHANGE`; the mediator stays in `state['middle']`.
- Later `propose()` matches `lifecycle_status='ACTIVE'` and `target_refs == [project, counterpart]` and recruits its `middle_state_record_hash` (`bfirst.py:211-215`).
- The adapter `consequences.recruited` equals that exact record hash; event 3 is `joint_check:caretaker`.
- In the journal-only control, no mediator/transition is committed, `state['middle']=[]`, and event 3 is `inspect_alone:caretaker`.
- Removing the mediator from the checkpoint breaks the reader; exact pre-event DB restoration restores `joint_check` and the recruited hash.

This is real computed state → later reader at the B1 test-only scope, not a narrative comparison.

## 5. Native P2Owner check

The E1 P2 claims are exact against the receiving source:

- `P2Owner.snapshot()` (`p2_owner.py:63-77`) hashes `world`, `events`, `intervals`, `encounters`; no psychological rows.
- `P2Owner._realize()` (`p2_owner.py:194-281`) admits the P2 event/interval and returns `durable_psychological_transition: "MISSING_RULE"` (`:269`).
- No P2 psychological writer or later psychological reader was found.
- E1's `02_DEVELOPMENT_OWNER_ABI_MATRIX.md` calls out the missing psych rows in `state_hash`, the missing target receipt, and the missing later consumer. This is the correct P2 seam diagnosis.

E1's adapter is **not** that seam:

- `B1Owner` imports `developmental_recursion.contracts`/engine, but owns a B1 `Store` SQLite file with `checkpoint/occurrence/joint_receipt` plus `b1_owner_meta/b1_source/b1_operations`.
- `B1Owner.snapshot()` returns adapter root/branch labels, actor `child`, adapter clock, and `digest(B1 state)`; B1 itself has no root/branch/clock.
- The source is `B1_FIXTURE:` over synthetic prehistory and authored rules.
- B1's actor is `child`; the caretaker is an authored participant, not independent B.
- Therefore E1 is an **isolated B1 store**, not integrated P2 psychology. E1 states this correctly; the review rejects any reading of E1 as P2 integration.

## 6. Source/root/operation/version limitations

| Limitation | Exact evidence | Consequence |
|---|---|---|
| Adapter-label root/branch | `B1Owner.__init__` root/branch; B1 `initialize` state has no root/branch | Root/branch are custody labels; no B1-native or P2 root |
| Actor `child` | B1 `initialize(actor_id='child')`; adapter fixes `actor_id='child'` | No original actor/C4 source; synthetic fixture |
| Synthetic source | `B1_FIXTURE:` digest over `initialize(prehistory())` + rule/registry hashes | No native source, no generated life |
| Adapter clock | `B1Owner._clock` = max of history/middle/responses times | Not a B1-native or P2 session clock |
| Adapter operation IDs | `b1_operations(id, proposal_hash, before_state, status, result, refusal)`; B1 `Store` has no operation_id | Adapter-added custody; B1 exact replay alone is not an operation receipt |
| Test-only rule/version | `TEST_ONLY_CAN008_B1` / `TEST_ONLY_CAN011_B1`, `PROVISIONAL_MODEL_HYPOTHESIS` | No CAN-008/011 issuance; version tamper refused, but rule is authored |
| B1 store shape | SQLite `checkpoint` JSON, `occurrence`, `joint_receipt`; whole checkpoint rewrite per event | Not P2 S47 SQLite/world; cost grows with history |
| No P2 full suite | E1 says full P2 owner suite NOT_RUN; probe uses engine core | No P2-root psychological integration acceptance |
| B1 39 / #704 45/19 | E1 author execution; not independently rerun here | Retain as author evidence; nine probe tests are the independent new execution |
| Receipt head | Stored receipt `git.current_head=0d6baf55`, parent of `ee1ff298` | Final exact-subject test independently passes; receipt provenance is pre-final |

## 7. Cost audit

Storage/state shape reproduced independently:

| Events | Owner DB | State JSON | Responses | Mediators | Transitions | Independent per-event |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 94,208 B | 15,334 B | 3 | 1 | 1 | 8.694 ms |
| 10 | 217,088 B | 28,713 B | 10 | 1 | 1 | 10.946 ms |
| 30 | 548,864 B | 66,953 B | 30 | 1 | 1 | 17.041 ms |
| 60 | 1,064,960 B | 124,313 B | 60 | 1 | 1 | 23.067 ms |

The E1 `06_RESOURCE_COST_FINDINGS.md` reports 9.738/12.150/16.908/23.694 ms and the stored receipt reports 9.42/13.74/20.45/22.72 ms for the same sizes; the E1 `00_RETURN` prose reports 9.7/12.2/16.9/23.7 ms. These are single-run observations and vary; `06` explicitly says they are not a benchmark gate. The **storage bytes, state growth, response counts, mediator count, transition count and shape** reproduce; the exact milliseconds are approximate. The architectural warning (full checkpoint rewrite, growing response history) is supported.

Three-event positive/control storage also reproduces: owner DB 94,208/86,016; journal 98,304/94,208; state JSON 15,220/8,501; records 23,239/21,746; history 23,361/21,867; mediator/transition 1/0; responses 3/3; occurrences 3/3; joint receipts 3/3; operations 3/3; model/provider calls 0/0.

## 8. Claim audit

| E1 claim | Independent disposition |
|---|---|
| B1 mediator persists and later response reads it; identical later event differs | **PASS** (positive/control witness, event3 hash identical) |
| 9/9 adapter tests pass | **PASS** independent `9 passed in 0.46s` |
| Cold reopen same snapshot/history/mediator; replay no duplicate | **PASS** independent direct check and test |
| Exact severance/restore | **PASS** independent test; exact pre-event DB restore |
| Wrong root/source/clock/operation/interval/participant/rule-version refuse before mutation | **PASS** within the nine tests; pre-effect counts 0 for wrong source |
| Operation ambiguity HOLDs, no duplicate | **PASS** test; RESERVED row HOLD; no blind reissue |
| Production registry empty and denies | **PASS** guard `DENY_ZERO_EFFECT` / `ZERO_POSITIVE_REGISTRY` |
| P2Owner has no psych in state hash/writer/later reader | **PASS** source exact (`p2_owner.py:63-77`, `:269`) |
| B1 39/39, #704 45/19 | **Author evidence, not independently rerun** here; B1 vendored bytes exact |
| B1 contradictory coexisting mediators | **Author test evidence, not independently rerun**; B1 stores a list but E1 itself notes no composition/priority rule |
| B1 scaling bytes/state | **PASS** storage shape; exact ms vary |
| E1 is P2 integration | **NOT CLAIMED / FALSE if read so**; isolated B1 store, no P2 root |
| E1 native science | **NOT CLAIMED / HOLD**; test-only rules and P2 `MISSING_RULE` |
| Receipt current head | **Pre-final parent**, not exact final subject; exact-subject tests independently pass |

## 9. Recommendations overrunning the current commission — declined

E1's engineering evidence is safe; the following plan recommendations are not accepted as written:

1. **Add optional `psych_effect` to P2Owner proposal grammar — DECLINED.**
   `05_MINIMUM_P3_IMPLEMENTATION_PLAN.md`, Task P3-E1-2, says “accept only the existing P2 `ADMIT_EVENT` fields plus an optional explicit `psych_effect` request.” The P3 commission (§7) says not to insert unsupported new fields into `P2Owner`'s existing proposal schema. Use a separate owner-validated sidecar/state-writer operation keyed to the existing event operation, or an explicit separate protocol. Do not extend the existing P2 proposal grammar.
2. **Use C9 `objective_material_eligible` as the psychological later consumer — DECLINED as written.**
   `05`, Task P3-E1-3, and the “Highest-leverage” section suggest C9 eligibility/action eligibility. `objective_material_eligible` is a material-feasibility signal. A psychological record must not make tools/money/institutional permissions exist and must not conflate material feasibility with actor competence/willingness/response selection (commission §6). Use an actor-capability/response authority or a separate consumer; material feasibility remains independently grounded.
3. **Add `selection_basis`/`historical_scope`/`representativeness`/`compression_note` as P2 proposal fields — DECLINED as written.**
   `05`, Task P3-E1-5, calls them “Event/proposal metadata.” The commission requires an owner-validated source-bound sidecar or evidence envelope; do not insert unsupported fields into the existing P2 proposal schema.
4. **Lifecycle operations — qualified, not accepted as issued.**
   `05`, Task P3-E1-6, lists `REINFORCE`, `WEAKEN`, `SET_DORMANT`, `REACTIVATE`, `TRANSFORM`. E1 does not implement them. No name-only or automatic lifecycle mutation is accepted; any future test-only surface must be refusal-first and governed by a specifically qualified predicate. No automatic elapsed-time decay/reinforcement.
5. **Production registry / native issuance — DECLINED.**
   Keep `DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES` empty. The E1 plan's Task P3-E1-7 correctly defers to a separately accepted authority change; this review does not issue it and does not accept a production entry.

## 10. What E1 does not prove

- P2-root psychological state, P2 state-hash psychological inclusion, P2 psychological writer, or P2 later psychological consumer.
- Sparse-event compression metadata or any P3 workstream C implementation.
- Conditional activation/contradiction composition; B1’s single mediator read is not a composition/priority rule.
- Actor/user opacity beyond B1’s `actor_surface`/`origin_explanation=NOT_ACCESSIBLE` fixture.
- Native CAN/ADP memory, practice, relation, B, human validity, C9 native integration, O05/O07/C9/O15 acceptance, or production registry issuance.
- A full P2 3–5-event batch with psychological state; E1 uses the actual #704 engine but the B1 owner, not P2.

## 11. Commands

```
cd <exact-E1-scratch>/WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
PYTHONDONTWRITEBYTECODE=1 python3 -B run_probe.py

# independent direct witness from this review
cd <exact-E1-scratch>
PYTHONDONTWRITEBYTECODE=1 python3 -B e1_positive_control_cold_refusal.py
```

The review reproduction script is `reproductions/e1_positive_control_cold_refusal.py`; logs and receipts are in `logs/`.

## 12. Limits

- E1’s B1 rules are authored test-only; no native issuance.
- The B1 actor `child`, synthetic prehistory and caretaker offers are not original actor or independent B.
- The full P2 owner suite, B1 39, #704 45/19, B3A/HQ300/M01/BP2P4J and V3 exact archive tests were not rerun; no acceptance of those components is inferred.
- Cost times are single-run observations, not benchmarks.
- Quota UNKNOWN; no UI/model/account/provider change.
