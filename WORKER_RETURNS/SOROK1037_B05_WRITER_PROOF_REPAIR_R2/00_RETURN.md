# SOROK #1037 B05 writer-proof repair R2 — author return

**Verdict:** `AUTHOR_R2_CANDIDATE_FOR_SAME_NONAUTHOR_FOCUSED_RERECEIVING`
**Issue:** #1037
**Session:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Base:** `c7018020f002bb7f509a83fba0bf2a6a5955cc00`
**Branch:** `codex/sorok1037-b05-writer-proof-repair-20261115-r2`
**Grade:** `SOURCEFREE_S2_ONLY`
**Terminal:** STOP. No second repair round launched.

## Exact received defect

Independent nonauthor G5 `5b65a35b1f54cd13da0a340eed1c9b92783a0ce1`
(`REVISE_EXACT_DEFECT`) reproduced one in-scope B05 false accept at
`c7018020`: a sole, caller-rehashed `ADMITTED` `P2_HOUSEHOLD_RENT` receipt for
a completed period, appended through the public `append_episode` API with no
actual `apply_household_rent` debit and no checkpoint transition, was returned
`READ historical=false` with unchanged household cash.

## Single correction

Only `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py` changed, on the
read side:

```text
before (reviewed)  b944b8f0b6e0d700e85141256df01cdaef8d59e2
after (R2)         a193fb5bfb6a1955209bedf0e66be974dcfa8e1b
sha256             5ac75cb66c61fb120f56900e976a8cdcd4e153fd4b0d37d9a93a0c95ab578331
```

For an `ADMITTED` receipt, `read_household_obligation` now requires the actual
owner transition already written by the existing `apply_household_rent`
`_StoreWrite` + `_checkpoint` path: two adjacent durable C12 checkpoints at the
receipt/episode clock whose A-household cash and independently reconstructed
household material hashes reproduce the receipt's exact before/after values and
current household source. The transition tuple may back exactly one rent
operation, so an appended sibling cannot copy a real debit as its own evidence.
Missing proof refuses `B05_RENT_OPERATION_UNPROVEN`.

No writer, schema, lock, ledger, registry, key, currency, C03/C04, P6 or D03
change. B04 is byte-identical to the reviewed candidate:
`3c1d326bfa2f8a78c92a84e5cc5e039e04376441`.

`UNCHANGED` (genuine zero rent) and `REFUSED` (held rent) do not manufacture a
cash checkpoint and remain readable; the new requirement applies to `ADMITTED`
only.

## Exact RED -> GREEN

The frozen reviewer probe was extracted byte-identically
(`blob 3e98929dbb526edf6fab60f74132cafe03d63239`, sha256 `fb42f9fd...`).

| Run | Source | Exit | Checks | Result |
|---|---|---|---|---|
| RED | unchanged `c7018020`/`b944b8f0` | `2` | 33/34 | sole rehashed receipt accepted `READ` |
| GREEN | R2 `a193fb5b` | `0` | 34/34 | sole rehashed receipt refused `B05_RENT_OPERATION_UNPROVEN` |

The exact #1027 witness is byte-identical (`blob 7cd5a230...`) and preserves its
literal-exit-1 oracle quirk: `63/63` checks pass, both historical defect rows
`accepted=false` with typed refusals. The exact #1027 cold probe
(`blob 6fc86dc5...`) exits `0` with `ok=true`, `warm_ok=true`, two purchases and
one rent, unchanged head.

## Tests run once on final source

| Suite | Result |
|---|---|
| New focused R2 tests (5): no-effect append, sever/restore, sibling transition copy, zero/held, historical/replay | `5 passed` |
| Author provenance tests | `6 passed` |
| Inherited original B01–B05 43 | `43 passed` |
| Selected read-only C03/C04 consumer | `3 passed` |

Observed elapsed/RSS: RED 51.11 s / 52,416,512 B; GREEN 58.72 s / 55,476,224 B;
witness 21.50 s / 60,768,256 B; cold 16.58 s / 61,751,296 B; focused 41.73 s /
69,537,792 B; author 51.67 s / 70,066,176 B; consumer 65.14 s / 72,785,920 B;
inherited 43 520.56 s / 77,344,768 B. Host load at close `3.91 4.97 6.13`;
timings are observations, not isolated benchmarks.

## Preserved strengths

- B04 foreign-root/branch/actor/operation and coherent C02 chain attacks still
  refuse; ownership changed/restored still reads exactly.
- B05 foreign root/branch/body-root/actor/exchange/period/rent controls still
  refuse; same-period second receipt remains `B05_RENT_OPERATION_NOT_UNIQUE`.
- Genuine zero (`UNCHANGED`) and held (`REFUSED`) rents still read.
- Genuine h1 remains `historical=true` after h2; h2 remains `historical=false`;
  replay/retry never double-debits.
- Normal two purchases + one rent survives warm first readers and fresh-process
  cold reopen.
- Pre-existing dwelling-source `B05_RENT_SOURCE_STALE` and exact restore are
  unchanged.

## Limits

The proof uses only existing durable state. A fully privileged world rewrite
that also fabricates a matching checkpoint pair is outside the observed public
`append_episode` threat model, as the independent reviewer scoped the B04
privileged-rewrite residual. A forged sibling that copies a real transition
causes fail-closed ambiguity refusal of the genuine receipt while present; that
is not a false accept. Provider checkpoint/org/quota and token/USD cost are
`UNOBSERVED`.

No native science, human/actor authority, J1/Nadia G2 acceptance, protected
PRE-MAIN merge, new ledger, or psychological fact is claimed.

## STOP

Author cannot self-G5. HQ should route the frozen R2 candidate back to the same
independent nonauthor for focused rereceiving. Evidence and pins:
`EVIDENCE.json`, `evidence/`, `G5_HANDOFF.md`, `PROGRAMMA_DELTA.json`.
