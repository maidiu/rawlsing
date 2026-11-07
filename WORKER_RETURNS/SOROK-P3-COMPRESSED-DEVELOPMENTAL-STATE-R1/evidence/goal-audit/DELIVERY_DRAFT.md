# P3 final delivery draft — for user/Browser-HQ review

**DRAFT ONLY — NOT INDEPENDENTLY ACCEPTED, NOT PR-READY, NOT MERGED.**

## Delivery identity

- Implementation cut: `486d42a4aa5dcd449564b95567ae93b59c4679a4`
- Current evidence cut: `16275d03fc4724a694c48ed9d447c4eeadbe25f2`
- Main integration branch from the current checkpoint:
  `agent/sorok-p3-compressed-developmental-state-20261106-r1`
- Protected start: `c852d7516e23fcb6cf2215e9be7c5fa268503516`
- Review/delivery evidence: this `evidence/goal-audit/` directory and
  `evidence/full-vertical-execution-combined/`

## What the current evidence supports

At explicitly **TEST_ONLY sourcefree** scope:

- The actual P2 actor/root is used through the unchanged `P2Owner`; no isolated
  B1 actor root substitutes for it.
- `P3Owner` composes the normalized sidecar store and actual P2 owner with exact
  root/actor/branch/clock/config/source/rule bindings.
- Formation writes source-bound `V3MS_MEDIATOR` records; a later event reads the
  exact persisted hashes and computes a changed response. The primary case
  reports `joint_check/private_check` streams and a material result read from
  actual P2/C9, never a rewritten native action.
- The combined author/HQ matrix records **13/13 PASS** at
  `486d42a4…`: PRIMARY, A–H, cold reopen, real process crash, and resource.
- Resource receipt at that matrix: two batches of three events, three provider
  calls, two retrospectives, six actual event latencies, cold open
  `10.754s`, DB `4096` B, WAL `1,536,792` B, DB+WAL `1,540,888` B,
  incremental DB+WAL `1,483,200` B, positive bytes/record/event, context
  `4,359` B, targeted queries and one full verification scan.
- Inherited #704/S39–S47 compatibility is separately demonstrated:
  **71 passed in 286.10s**, plus a cold CLI with `cold_verified=true`.
- Production guard is deny/zero-effect; native psychological, ADP016/017,
  human, B, source and protected authorities remain held.

## Exact limitations and remaining acceptance dependencies

1. **Focused nonauthor re-review is pending.** The earlier independent review
   at `d1a681…` returned **REVISE/CONDITIONAL** and found M1–M3 plus harness
   fixture defects. Current M1/M2 repairs and M3 measurement are actual and the
   combined matrix is green, but the focused recheck at the exact current
   evidence cut `16275d03…` is the acceptance gate. Author/HQ results are not
   independent acceptance.
2. **Same-history causal control is not exact in the current primary matrix.**
   The primary control uses `history_outcomes=()` — no history — rather than
   holding history fixed and removing only the prior mediator
   (`tests/test_p3_vertical_slice.py:62`). A prior nonauthor diagnostic at
   `d1a681…` showed FORMATION→2 records→`joint_check/private_check` versus
   STABILITY→0 records→`inspect_alone`, but it is not a current combined-case
   execution and is not a substitute for the exact current-cut control.
3. **True foreign root/fork is not proved.** The H cross-root test explicitly
   uses deterministic replicas with the same logical root hash and mutated
   foreign source fields; it does not instantiate an actually different P2 root
   or fork and prove non-migration (`tests/test_p3_vertical_slice.py:450-472`).
4. **Actual-chain source severance is unit-only.** Exact B1 source
   severance/restore is covered in `tests/test_rules.py:108`, not in the actual
   P2 producer→store→later-reader matrix.
5. No selective PRE-MAIN PR has been published; no protected receiving or merge
   is claimed.

## Recommended next action

Request the already-live focused nonauthor recheck to verify the exact current
cut, the M1–M3 repairs and the 13-case matrix. If it accepts the repaired scope,
disposition the three exact residuals above as either required final repairs or
explicitly bounded limitations before PR preparation. Only then prepare the
selective PRE-MAIN PR. Do not merge on author evidence.

## Suggested status line for the user/Browser-HQ

> P3 sourcefree engineering is implemented and the current author/HQ matrix is
> 13/13 at implementation `486d42a4…`; the earlier independent review found
> M1–M3 and harness defects, which are repaired and green in the author matrix.
> Independent focused acceptance is still pending. Known exact residuals are
> the same-history no-record control, a true foreign root/fork test, and
> actual-chain source severance/restore. No native science, memory/claim,
> human validation, production authority or merge is claimed.

## Full-deliverable item status

| Original §15 item | Current disposition |
|---|---|
| Implementation SHA/branch | `486d42a4…`; integration branch from checkpoint; evidence cut `16275d03…` |
| Actual reused capital | B1 `mode_for` source hash `478b9897…`; S39–S47/P2 exact; B3A/HQ300/M01/BP2P4J not adopted as owners; M01/V3 HOLD |
| P2 state integration | `p3/p3_owner.py` + `p3/state_store.py`; actual root and later reader demonstrated |
| Sourcefree positive / production deny | Combined primary/13 and `production_guard` deny/zero-effect |
| Compression evidence | Four forms actual in F; no fabricated acts/global multiplier |
| Context/contradiction | C, D, E actual matrix cases; pure read activation |
| Asymmetric opacity | G actual; actor/user/objective separation; claims/memory held |
| Causal contrasts | A/B/C/D actual author/HQ matrix; same-history control residual |
| Cold/negative proof | H identity/time/source/workflow, cold, replay, child crash; true foreign root/fork and actual source severance residual |
| Resource receipts | Actual combined metrics listed above |
| Scientific holds | Native/ADP016/017/human/B/production all HOLD |
| Independent review | Prior REVISE; focused recheck pending |
| Selective PRE-MAIN PR | **Not ready / not published** until focused acceptance and residual disposition |
| Next code edge | Qualified native developmental/memory writer only with issued authority; not invented here |

**Do not interpret this draft as goal acceptance, completion, merge permission or
native validation.**
