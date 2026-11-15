# SOROK C05 R2 — one exact promotion defect correction

**Terminal disposition:** `AUTHOR_C05_R2_CANDIDATE_FOR_SAME_NONAUTHOR`

**Candidate SHA:** `5d771dd86767655534b23576075e5da2db4fba78`
**Frozen start:** `bc45f699a22708aae3df7e34b1ba3b272a362565`
**Original implementation:** `9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Independent review:** `b5b810cdd7b51b20efcc42d4ce76960f9e410706`
**Branch:** `codex/sorok-c05-promotion-repair-20261115-r2`
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1037-b-receipt-repair/Rawlsing`
**Grade:** `SOURCEFREE_S2_C05` / `SOURCEFREE_S2_ONLY`

This is the same original author’s one narrow correction of the exact G5
defect. It is not a new investigation, campaign, theory dispute, or review
cycle. `supporting_actor.py`, C04, P3, P2, B, G2 and all other product remain
read-only and unchanged. #1037 B05 remains a separate unaccepted line and was
not reopened.

## Exact defect (reproduced at the frozen base)

`promote_relation` computed its pre-write current depth from only
`RELATION_STATE_CHANGES` (`ENTER`/`LEAVE`/`CHANGE`). Prior `PROMOTE` episodes were
invisible, so `machine["depth"]` stayed 1. A second depth-2 promotion with a new
operation ID passed the guard, appended a change+head, and only then failed
`_verify_scope`. The public call raised `RELATION_CUSTODY_SEVERED` after
permanently severing the relation context.

The independent reviewer probe was copied byte-identically to
`newprobes/c05_defect_probe.py` (blob `31a888cb9189686d321f29ab27e95aa8fe5f9d9e`,
SHA-256 `1172fec4621c353bee5736423c42e5278dc3a1148112c676cd53f7b687105a70`).
At the base it reproduced exactly:

- `second_call_refusal: RELATION_CUSTODY_SEVERED`
- `wrote_episode_on_refusal: true`
- `scope_severed_after_write: true`
- episodes/changes/heads: 49/2/2 → 51/3/3
- world events/perceptions/checkpoints unchanged: 14/42/33
- relation status: `QUALIFIED` → `HOLD_CUSTODY_SEVERED`
- first-operation retry after the write: `RELATION_CUSTODY_SEVERED`
- literal probe exit: `0` (reviewer bug oracle reproduced)

Immutable RED report:
`evidence/c05_defect_report_RED_at_bc45f699a.json`
SHA-256 `8f5f0a79190068b0ce714ee2d76a6f2e93934f262bfd401e16f4f3f0a853f38d`.

## Correction

One line in `promote_relation`:

```diff
-    machine = _state_machine(state_changes)
+    machine = _state_machine(scope["changes"])
```

`state_changes` remains the input to the promotion `history_hash` (state entries
only). The pre-write depth guard now sees the full verified scope history,
including prior `PROMOTE`. A new depth-2 operation at current depth 2 refuses
`RELATION_PROMOTION_NOT_DEEPER` before `_append_change`. The existing
`_StoreWrite` owner and reader verification are unchanged. No generic rollback,
new ledger, new representation, or post-append framework was added; the
full-history pre-write guard removes the observed write-on-refusal path, and the
focused test/probe show zero write. No same-path post-append failure remained
that would make a transaction change indispensable.

Corrected product blob:
`d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
SHA-256 `72e213220ed2855a5bd303985a7a584cb14b1a3b2e704b26aa4b8161fef068d2`.

## Corrected semantic proof

The same byte-identical probe after correction (literal exit `2`, expected
because its own oracle still asserts the old bug):

- `second_call_refusal: RELATION_PROMOTION_NOT_DEEPER`
- `wrote_episode_on_refusal: false`
- `scope_severed_after_write: false`
- episodes/changes/heads: 49/2/2 → 49/2/2
- world events/perceptions/checkpoints unchanged: 14/42/33
- relation status: `QUALIFIED` → `QUALIFIED`
- first-operation retry: `UNCHANGED`, same primary episode ID
- C12 verify: `ok`

Post-fix report:
`evidence/c05_defect_report_POST_FIX.json`
SHA-256 `ebdf5da8e665598ae5859ce4e1dd9a186891786a56f6dfe398d9b0bbff37c720`.

Focused test `tests/test_c05_promotion_repair_r2.py`:

- base RED: 1 failed, exit 1, failing on expected
  `RELATION_PROMOTION_NOT_DEEPER` versus actual `RELATION_CUSTODY_SEVERED`;
- corrected GREEN: 1 passed, exit 0, 6.80 s, max RSS 58,249,216 B.

It proves: first depth-2 promotion succeeds; the same original operation retry
is `UNCHANGED` with the same primary ID; a different new depth-2 operation
refuses `RELATION_PROMOTION_NOT_DEEPER` with zero episode/change/head/world/
perception/checkpoint delta; dated history and real-event context stay
`QUALIFIED` and byte-exact; the original retry still works; C12 verifies; a fresh
process reopens with exact history/context/counts and `UNCHANGED` retry.

## Normal/negative/cold preservation

The reviewer’s 89-check normal/negative/cold probe and both helper imports were
copied byte-identically:

| File | Git blob | SHA-256 |
|---|---|---|
| `newprobes/c05_probe.py` | `c89e22a7c4ba683fe99994f2833b8b710e888401` | `1f44fef5f7648215db72eed2cc805f778cfbbadda0c9a830ea592397c5132fb7` |
| `newprobes/c05_observe.py` | `e588b00afed41d4556a63497a3f9aa8b57ace66f` | `94cfa307161df9597103e01617a1625359213a7f71c4e48befb1ab4106f40850` |
| `newprobes/c05_cold_child.py` | `7feae9d8091d65fec612dddd4051f3b00e3a3bbc` | `230d85a841f96161b4033244ad6206992e66c8bda681026fa85bbbc58dfbb8ff` |

After correction: **89/89 checks passed**, exit 0, 160.38 s real, max RSS
55,271,424 B, cold child exit 0, cold snapshot exact, cold retry `UNCHANGED`.
Report `evidence/c05_probe_report.json` SHA-256
`b072782c595876485e1a92c2699c7768d8ac017cb03fb99276fdbf8b633f6a7d`.

The probe’s `coherent_append_only_relation_accepted` observation is the
reviewer’s pre-existing scope boundary, not a defect or a new claim: a caller
able to append a coherent change+head through the public C12 store is accepted
as caller-authorized sourcefree input. The self-hash chain is not an owner
signature, relation perception, native ADP-015/C4 authority or actor truth.

## Suites on final source

Every command used
`TMPDIR=$PWD/.local-logs/sorok-c05-promotion-r2/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`,
`-B`, `-q`, `-p no:cacheprovider`. Logs are under `evidence/logs/`.

| Suite | Result | Exit | s | Max RSS B |
|---|---:|---:|---:|---:|
| `SOROK_C05_PROMOTION_EXACT_REPAIR_R2/tests/test_c05_promotion_repair_r2.py` | 1 passed | 0 | 6.80 | 58,249,216 |
| `SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py` | 5 passed | 0 | 43.39 | 62,324,736 |
| `SOROK-DUEL-C01-R1/test_c01_supporting_actor.py` | 6 passed | 0 | 12.72 | 56,705,024 |
| `SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py` | 6 passed | 0 | 25.84 | 63,750,144 |
| `SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py` | 12 passed | 0 | 55.40 | 68,902,912 |
| `SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py` | 5 passed | 0 | 14.40 | 55,726,080 |

Defect probe: base RED literal exit 0, 2.94 s real, max RSS 42,360,832 B;
post-fix literal exit 2, 2.63 s real, max RSS 43,233,280 B. Timings are
observations under host load, not isolated benchmarks. Provider/token cost is
`UNOBSERVED`; checkpoint/org/quota is `UNOBSERVED`.

## Proved

- The exact repeat-depth-2-promotion defect is reproduced at the frozen base and
  corrected at the same public path.
- The bad public request now refuses before any append: zero episode, change,
  head, world-event, perception or checkpoint delta.
- Relation history/context remain `QUALIFIED` and byte-exact after the refusal.
- First depth-2 promotion and same-operation retry still work.
- Original retry and fresh-process cold remain exact; no invalid artifact.
- Normal 89-check probe, original C05 and C01/C04/P2 suites remain green.
- Earlier event contexts, partial-exposure, private boundaries and later real
  P2 event semantics are preserved.

## Inherited / unchanged

- C01 supporting registration and actor-relative event access.
- C04 child-facing custody and D03/J1 adjacent paths (not extended, not
  repaired, residuals held).
- P2 owner performed-event path, BP4 event seal, S47 world/clock and C12 store.
- Role allowlist `parent` + `neighbor`; `supporting_actor.py` byte-unchanged.

## Unproved / held

- Native ADP-015/C4 relation authority, household/genealogy issuance.
- Maternal psychology, independent volition/autonomy, generated language.
- G2 mother-owned selection, complete J1/Nadia response, D04/D05, durable
  acquisition.
- Human/scientific/source-rights receiving and protected merge.
- #939 fleet, PYAT, Browser management/contact, new campaign/duel.
- Concurrent same-operation uniqueness, branch-fork replay, depth > 2.
- C04 parent self-read metadata and D03 caller-receipt residuals.

## Scope boundary preserved

- `exposed_actor_ids` remains caller-supplied; both parties remain mandatory.
- No owner/source receipt qualifies relation knowledge; the reader remains
  `DATED_EXPOSURE_ONLY` and does not claim relation `PERCEIVED`.
- A coherent public append of a change+head remains accepted as the disclosed
  caller-authorized sourcefree boundary; it is not owner authentication.
- Normal physical event `PERCEIVED` and relation dated exposure stay distinct.
- The repair does not invent psychology, selection, perception or a scientific
  grant, and does not advertise all C05/actual relationship knowledge as
  complete.

## Compliance / STOP

Only the leased `continuing_relations.py` and this own R2 return were written
and committed. No supporting_actor/C04/P3/P2/B/G2 edit. No provider/model/
account/auth/global-permission change, paid fallback, dependency install, new
server/VM/controller, nested agent, CI/GitHub Actions, protected merge, PYAT,
Browser management/contact or #939 fleet. No `/tmp` write. No B05 reopen.
No self-G5.

STOP after the same nonauthor reviewer’s focused readback of this frozen
candidate. No new opponent, cycle or automatic author round.
