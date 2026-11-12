# SOROK B04/B05 AGENT B — typed parent join and restart-safe material interleave

**Round:** Pair1 same persistent Agent B versus same Pair1 Agent A.
**Frozen composition start:** `46a815643440857ff1185481a5e27ef7023e541f` (A result `7663067647c945126d183c59cec6c6bfc8a09ab3`, A production `d2a0a4eadab4ba99ae830c8e47013e60295a4632`, returned Pair3 parent `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34` / production `255fd4905990e3c0cab3e2d95ba91b851ea701a8`; clean auto-merge, unaccepted).
**Branch:** `codex/sorok-duel-b04-b05-b-typed-parent-join-20261112-r1`.
**This round's implementation SHA:** `ef2129283fff3deffab8cefef6ff94da3045bc58`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. No terminal acceptance.

## 1. Reconstruction and exact artifact

I reconstructed B02/B04/B05 from the frozen packets before reading A's semantic handoff: B02 incremental dated S46 periods with explicit calendar logic/currentness and no rewind/duplicate; B04 typed objective purchase/refusal with actual funding, stock/ownership, refusal no debit, atomic retry/crash; B05 recurring material rent across dated cycles with one debit, later readers, no automatic psyche/work. The full Library sources remain NOT_INSPECTED locally.

Current code at `ef2129283fff3deffab8cefef6ff94da3045bc58`:

| Path | Change |
|---|---|
| `SOROK-DUEL-B04-R1/test_b04_operations.py` | Updated from pre-hook refusal to actual typed C02 read/options/history/purchase, next parent activity, second purchase, historical read. |
| `SOROK-DUEL-B04-R1/test_b04_composition.py` | Actual typed history/no bridge; post-purchase parent activity and second purchase; crash rollback. |
| `SOROK-DUEL-B05-R1/rolling_reproduction.py` | `PeriodInterleaveOwner` is event-id keyed; validates targets before event; reports ALREADY_ELAPSED; recovers a committed P3 result after B02 advance without a second action. |
| `SOROK-DUEL-B05-R1/test_b05_rolling.py` | Actual typed parent read/options/read_purchase after purchase; next parent work; second purchase; rent/B03. |
| `SOROK-DUEL-B05-R1/test_b05_cross_batch.py` | Event-id mapping; actual typed parent read after purchase. |
| `SOROK-DUEL-B05-R1/test_b05_interleave_retry.py` | Injected post-materialize failure, same-journal restart, event-keyed targets, no duplicate span/receipt, exact P3 receipt/readset. |

`B04_A_SEMANTIC_ABI.md` is the pre-hook boundary; its pending section is historical. `B04_B_ABI_REVISION_PRE_TYPED.md` is the removed bridge record. Current ABI: `B04_B_TYPED_JOIN_ADDENDUM.md`, `B05_B_INTERLEAVE_ADDENDUM.md`. Machine records: `PROGRAMMA_DELTA_B.json`, `impact_B.json` (old pre-typed records archived).

## 2. Concessions: A's typed correction was right; my bridge was wrong

I concede the central semantic point:

- My prior `P2_PARENT_MATERIAL_ANTECEDENT`/`PURCHASE_MATERIAL_STATE` bridge did **not** cause the actual C02 consumer to validate purchase linkage. It inserted a post-operation material state under an antecedent/initialization kind. That was a causal substitution, not typed purchase consumption. A correctly removed it and preserved the actual refusal at the old C02 input. I withdraw any defense of the bridge; it remains only as archived history.
- A's typed `P2_PARENT_PURCHASE` hook requirement was correct. Pair3's returned hook now validates root/branch/actor/alias/status/before-after sources/possession/event effect/currency/operation and includes the purchase in ordered history. That is the legitimate join.
- A's currency equality guard is correct: parent/material/market/request units must be exactly equal; mismatch refuses before debit; no conversion. My earlier default-unit assumptions are withdrawn.
- A's `PeriodInterleaveOwner` idea—B02 materialize between real BatchEngine events—is valid and preserved in concept. My locks and crash rollback are retained.
- A's stale post-hook tests (expecting `PARENT_MATERIAL_HISTORY_MISMATCH` after purchase) are not a production defect; they were authored against the pre-hook boundary. I updated only the owned B04/B05 tests to the actual typed join; no production workaround.

## 3. New defect found and repaired: interleave restart/index and replay

A's adapter `_index` was an in-memory position that incremented **before** `hp.materialize_to`; a failure/retry or restart could assign the next event's target date to the wrong event or skip a target. Its wrapper also returned a post-B02 `after` snapshot while P3Owner's durable operation `after` remained pre-B02, so a same-journal retry could hit `P3_REPLAY_STATE_MISMATCH`.

Repairs in `ef2129283`:

1. `after_event_dates` is a `Mapping[exact event_id -> target ISO date]`; no positional index controls advancement.
2. Target dates are validated inside the B02 plan **before** delegating the P3 event; an already-elapsed target reports `ALREADY_ELAPSED`, never rewinds.
3. On a P3 replay refusal after a committed event + B02 advance, the adapter reads the P3 store's `COMPLETE` operation and returns its exact receipt/readset/objective/accessible/consequences only when operation id, proposal hash and expected before state match. It does not call the P3 owner again, write P3, or invent a receipt.
4. `test_b05_interleave_retry.py` injects a failure after the first B02 target commits but before BatchEngine records the event, resumes on the same journal with a fresh adapter, and proves: event 4 target is not reused; one 2026-01-22 B02 receipt/span; three event records; exact P3 receipt_ref/readset; no second event action.
5. The normal cross-boundary batch still advances B02 after each of three real events across the employment split; no wrong next date; no duplicate span.

## 4. Actual typed join proved

At this exact source, without a bridge:

1. B02 current period exists; B03 dwelling/feasibility; market stock.
2. Registered parent material uses the explicit market currency unit; B04 purchase admits: parent cash/free-hours debited, market stock decrement, ownership row, one typed `P2_PARENT_PURCHASE` C12 receipt and checkpoint.
3. C02 `read_parent_material` returns cash 80/free 7; `parent_feasible_actions` returns typed options; `read_parent_history` is material-consistent with one admitted purchase row and no `PURCHASE_MATERIAL_STATE` row.
4. `read_purchase` returns `parent_material_status=READ`, `purchase_history_hook=C02_PARENT_HISTORY_READ`, historical=False.
5. Next legitimate PAID_WORK activity admits, cash 90/free 5; second purchase admits, cash 50/free 4; stock 0, ownership 2; first purchase read becomes historical=True without a second debit.
6. B02 materialize to completed period; B05 rent debits fixed-A household cash 55→43; B03 junior-kit feasibility becomes REFUSED_AFFORDABILITY; P3 store head unchanged by B04/B05.
7. Currency mismatch refuses before debit/stock/ownership; refusals/severance/restore/cold remain covered.

## 5. Proof

| Suite | Result | Evidence |
|---|---|---|
| B04 operations + composition | **7 passed in 111.82s** | `SOROK-DUEL-B04-R1/evidence/b04_b_typed.log` |
| B05 rolling + cross + batch + rollback + zero/held + interleave retry | **7 passed in 283.62s** | `SOROK-DUEL-B05-R1/evidence/b05_b_typed.log` |
| B01+B03+B02+B04+B05 combined | **43 passed in 613.49s** | `SOROK-DUEL-B05-R1/evidence/b01_b02_b03_b04_b05_b_typed_combined.log` |
| B02 period + incremental (inherited, unchanged) | **9 passed** | `SOROK-DUEL-B02-R1/evidence/b02_b_verified.log` |
| P6 house/P2/actor and P6 MII (inherited A semantic cut; P6 source unchanged by this round) | **15 passed / 18 passed** | `SOROK-DUEL-B05-R1/evidence/a_cross_adjacent.log`, `a_cross_mii.log` |

Negative evidence retained: typed purchase no bridge; no fake antecedent/WORK/DEBT/CIRCUMSTANCE row; currency mismatch no debit; wrong owner/parent/price/market/parent branch; funds/time/stock/acoustic refusal no effect; crash rollback; cold; duplicate rent; insufficient/zero rent; torn interleave retry; no duplicate B02 receipt/span; P3 head unaffected by B04/B05.

## 6. CG-B packet matrix and independent receiving boundary

| Packet | Status at this sourcefree cut | Honest limit |
|---|---|---|
| B01 | ACHIEVED_SOURCEFREE_CANDIDATE | Household/dwelling material, fork provenance, cold; parent consumer was not part of B01. |
| B02 | ACHIEVED_SOURCEFREE_CANDIDATE | Incremental dated plan/employment split/currentness/cold/no duplicate; real 3-event cross-boundary BatchEngine; full 5-event/cross-event crash not proved. |
| B03 | ACHIEVED_SOURCEFREE_CANDIDATE | Dwelling/tenancy/space/acoustics/feasibility, same-root PsycheStore negative; owned/other tenure, child new occupancy, cold fork remain limited. |
| B04 | ACHIEVED_SOURCEFREE_CANDIDATE | Typed parent purchase/refusal, stock/ownership, C02 typed history, next activity, second purchase, currency equality, crash/rollback; no public event, household-funded alternative, fork/cold-fork. |
| B05 | ACHIEVED_SOURCEFREE_CANDIDATE | Rent on completed periods, one debit/refusal, typed parent join, cross-boundary batch; no 5-event batch, arrears/landlord/variable rent, full P6 live/fork. |
| C/D/E/F/G | NOT_EXECUTED | Full 27 remains downstream. |

This is **not** terminal acceptance. One independent nonauthor receiving is requested for the coherent CG-B tranche at exact implementation `ef2129283fff3deffab8cefef6ff94da3045bc58` (final docs head follows the return commit), using the commands/logs above, exact source refs, actual consumers, negative/sever/restore/cold evidence, and the stated limits. A/B are authors, not independent terminal reviewers.

## 7. Preserved boundaries and unresolved items

- No P2 constructor/validate/realize participant, `parent_activity`, `parent_decision`, `parent_speech`, `supporting_actor`, P3/store/model_cycle/context/projection, `run_p4`/`run_p6`, bp4 vocabulary, guide/currentprogress/workflow/Pyat/config/server/credential/protected edits by this round. Pair3 C03/C04 modules are candidate imports, not native acceptance; no `C03.perform` call.
- No new scheduler/ledger/parent store; locks are file serialization over existing state roots.
- No public event/Nadia perception, mother decision/utterance/hidden reason/uptake, possession-by-narrative, currency conversion, arrears/landlord economy, cold fork/full P6 live turn, or native/science/rights/human/merge authority.
- P3 code-pin roots from prior cuts remain incompatible; no migration/weakening.
- Period gaps are reported; no full scheduled coverage or 5-event crash claim.
- The typed C02 hook is now present and consumed; no stale hook-missing hold.
- Two Library architecture records remain NOT_INSPECTED locally.

## 8. Challenge to SAME A

1. Attack the typed join with two admitted purchases, a refused purchase, post-purchase activity, later rent, source/currency/owner mismatch, and cold restart; prove one debit/one ownership/one typed purchase-history row and no bridge/duplicate.
2. Attack `PeriodInterleaveOwner` with a failure before B02 materialize, after materialize but before BatchEngine event record, after event record before next event, and with a fresh adapter; prove no wrong next date, duplicate span/event, lost index, or fabricated receipt/readset.
3. Run a 5-event cross-boundary batch with B02 materialize between every event and the finite reconciliation state; this remains unproved.
4. Reconcile C02 `PARENT_B02_HOLD`/`historical_dates` only through Pair3 ownership; prove parent activity sees actual B02 as-of state without live edits.
5. Do not weaken P3 pins, C02 history validation, typed purchase semantics, P6/P4 boundaries, or claim terminal acceptance.

**Returned for same rival; one independent nonauthor receiving remains required.**
