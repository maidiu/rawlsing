# SOROK B05 AGENT B — typed parent join and restart-safe interleave

**Packet:** B05 `Prove multicycle material duration and later first-consumer parity`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Frozen composition:** `46a815643440857ff1185481a5e27ef7023e541f`.
**Branch:** `codex/sorok-duel-b04-b05-b-typed-parent-join-20261112-r1`.
**Implementation SHA:** `ef2129283fff3deffab8cefef6ff94da3045bc58`.
**Main handoff:** `SOROK-DUEL-B04-R1/AGENT_B_HANDOFF.md`.
**ABI:** `B05_B_INTERLEAVE_ADDENDUM.md`; prior `B05_B_ABI_REVISION_PRE_TYPED.md` is historical.

## 1. What changed

A's `PeriodInterleaveOwner` concept is preserved, but its in-memory positional `_index` and post-B02 `after` snapshot caused a same-journal restart to assign the wrong next date and to hit `P3_REPLAY_STATE_MISMATCH` when P3's durable after state was pre-B02. Repairs:

- `after_event_dates` is keyed by exact P3 event id, validated against the B02 plan before the event is delegated.
- An already-elapsed target is `ALREADY_ELAPSED`, never rewound.
- On a P3 replay refusal after a committed event, the adapter reads the P3 store's `COMPLETE` operation and returns its exact receipt/readset/objective/accessible/consequences only when operation id, proposal hash and expected before state match. It does not call the owner again or write P3.
- The real `BatchEngine` still owns batching, reservation, replay and record validation.

## 2. Actual join and cross-boundary cycle

- Actual typed B04 purchase -> C02 `read_parent_material`/`parent_feasible_actions`/`read_parent_history` READ with typed purchase row; next parent PAID_WORK; second purchase; later `read_purchase` historical; no bridge, no fake activity.
- Actual three-event `BatchEngine` crosses B02 employment split via B02 `materialize_to` after events 4, 5, 6; B02 reads old term at 2026-01-19 and `civic-works` at 2026-01-21; three P3 records preserve `MISSING_RULE`; B05 rent changes household cash 55→43; B03 feasibility refuses; P3 head unchanged by B04/B05.
- `test_b05_interleave_retry.py` injects failure after 2026-01-22 B02 advance but before the BatchEngine event record, then resumes on the same journal with a fresh adapter: event 4 target is not reused; one 2026-01-22 receipt/span; three event records; exact P3 receipt_ref/readset; no second action.

## 3. Proof

- B05 rolling/cross/batch/rollback/zero-held/interleave-retry: **7 passed in 283.62s** (`evidence/b05_b_typed.log`).
- Combined B01+B02+B03+B04+B05: **43 passed in 613.49s** (`evidence/b01_b02_b03_b04_b05_b_typed_combined.log`).
- B02 inherited: 9 passed (`SOROK-DUEL-B02-R1/evidence/b02_b_verified.log`).
- P6 inherited source unchanged by this round: 15 passed / MII 18 passed (`a_cross_adjacent.log`, `a_cross_mii.log`).

## 4. Limits

No 5-event cross-boundary batch, no crash between B02 materialize and next event beyond the one bounded retry proof, no arrears/landlord/variable rent/currency conversion, no public event/Nadia perception, no mother decision/utterance/uptake, no cold fork/full P6 live turn, no native/science/rights/human/merge. `period_uncovered` reports P3 event-tick gaps; no full scheduled coverage claim. Prior P3 roots incompatible; one independent nonauthor receiving remains required.

## 5. Challenge

Attack event-keyed interleave with failure before/after B02 advance, fresh adapter restart, duplicate target/receipt, and stale P3 replay recovery; prove no wrong next date, duplicate span/event, lost index, or fabricated P3 receipt/readset. Attack B05 rent after typed purchase/parent activity and source severance/cold.
