# C05 independent nonauthor G5 handoff

**Candidate:** `C05_SOURCEFREE_CANDIDATE_FOR_NONAUTHOR_G5`
**Exact frozen implementation SHA:**
`9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`
**Start:** `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`
**Branch:** `codex/sorok-c05-continuing-relations-20261115-r1`
**Grade to receive:** `SOURCEFREE_S2_C05` (`SOURCEFREE_S2_ONLY`)

## What to receive

C05 sourcefree dated continuing relations:

- caller-supplied `ENTER`/`LEAVE`/`CHANGE` over actual world clocks;
- explicit actor-limited exposure;
- immutable dated entries plus depth-1 → depth-2 promotion;
- a terminal consumer that combines a genuinely later existing-owner shared
  event’s C01 actor-relative access with only the relation entries the viewer
  was exposed to;
- cold-process exactness, sequential retry idempotence, and qualified custody
  HOLDs on severance, forgery, wrong root/branch/actor, future/backdated clock
  or changed-operation reuse.

Do not receive it as native ADP-015/C4 relation authority, maternal psychology,
generated language, autonomous volition/autonomy, G2 selection, complete J1,
D04/D05, human/science/source-rights receiving or protected merge.

## Frozen product and test files

| Path | Git blob | SHA-256 |
|---|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/supporting_actor.py` | `98cb4ceb3e5e201815c0ac46ba93f773601d818c` | `ba831554d7da2879cf8b32dd8a7a0337ef61e072408c24e3da69db43a9848b92` |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/continuing_relations.py` | `343cf08a23da7a34305fdbb897102086f2124ee3` | `f4442b35e9d5fbf12b0fcc43fa99814a6a17f70aa16d877ba4a1fb4a621a7c3b` |
| `WORKER_RETURNS/SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py` | `4741264d5b23195731d7fe7f0f77e72ec847442e` | `115b0fd74837386340bb0bad4ef8eea3d7aba0c23671c72ed831f111ae69a79a` |

The only product change outside the new module is the deliberate role allowlist
extension from `parent` to `parent` + `neighbor`. No root/focal/source/
registration/participation/access semantics changed.

## Suggested independent checks

1. **Positive:** build the same P2 world with Nadia, a `parent` and a
   `neighbor`; `ENTER` exposed only to parent/neighbor; create a later real
   `P2Owner` `ADMIT_EVENT` with all three; read
   `read_actor_relative_context` for parent, neighbor and Nadia. Expect parent
   and neighbor `QUALIFIED` with the dated entry, Nadia a qualified
   `HOLD_NOT_EXPOSED`, and all three with `PERCEIVED` event access.
2. **Later event / separate access:** create a second real event with Nadia and
   parent only. Expect neighbor `NOT_PERCEIVED` but still relation-qualified.
3. **Exposure/no retro fill:** add a later `CHANGE` exposed to Nadia too. Expect
   Nadia to see only `CHANGE`, `history_complete: false`, no synthesized
   `ENTER`; parent/neighbor see both.
4. **Promotion:** promote depth 2 after the change. Expect depth 2 for exposed
   viewers, depth 1 for earlier-event reads, and byte-identical earlier
   entries/hashes.
5. **Negatives:** future/backdated clock, stranger actor, missing party
   exposure, changed-operation reuse, private-value leak, forged root/branch/
   alias/value, and a live actor querying a different relation token. Expect the
   documented refusals/HOLDs and no row/world change.
6. **Consumer sever/restore:** hide the `CHANGE` episode from the store reader.
   Expect `HOLD_CUSTODY_SEVERED` relation context with event access still
   `PERCEIVED`/`NOT_PERCEIVED`, and unchanged world/event/perception/checkpoint
   facts. Restore and expect exact pre-sever contexts.
7. **Cold:** close and reopen in a fresh interpreter. Expect exact root, world
   hash, clock, registrations, dated history, contexts, row counts, and no
   duplicated registration/change/head/speech rows.

## Exact commands used by the author

Interpreter:
`/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`

Every command:

```text
TMPDIR=$PWD/.local-logs/sorok-c05-continuing-relations/tmp
PYTHONDONTWRITEBYTECODE=1
python -B -m pytest -q -p no:cacheprovider <suite>
```

Run:

```text
WORKER_RETURNS/SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py
WORKER_RETURNS/SOROK-DUEL-C01-R1/test_c01_supporting_actor.py
WORKER_RETURNS/SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py
WORKER_RETURNS/SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py
WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py
```

Observed results: 5 + 6 + 6 + 12 + 5 passed, all exit 0. Logs are in
`evidence/logs/`.

## Residuals the reviewer must not over-accept

- Caller-supplied illustrative relation semantics; not native ADP-015/C4.
- Depth is finite (1 or 2); one relation scope is exercised.
- Raw C12 private values are developer-visible to a raw-store holder; actor
  readers return `NOT_READ`.
- Branch-fork replay is unobserved.
- Concurrent same-operation uniqueness is not proved; sequential retry is.
- Later event language content is inherited S45/S39, not C04/G2 authorship.
- C04 parent self-read metadata and D03 caller-receipt binding residuals remain
  excluded.
- Provider/token/cost is `UNOBSERVED`.

## Stop conditions

- No self-G5. This candidate requires one independent nonauthor receiving, and
  only after the candidate is banked.
- No protected merge, #939 fleet restart, PYAT, Browser contact, D04/D05, G2,
  E01, J2 or new duel is authorized by this handoff.
- STOP after the C05 job.
