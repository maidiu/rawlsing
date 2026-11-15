# SOROK C05 — continuing relations and variable-depth supporting actors

**Terminal disposition:** `C05_SOURCEFREE_CANDIDATE_FOR_NONAUTHOR_G5`

**Capability grade:** `SOURCEFREE_S2_C05` (`SOURCEFREE_S2_ONLY`)

**Implementation / frozen candidate SHA:**
`9cf13763b0061400e2c936eaf1d0a2f4b76a03f7`

**Start SHA:** `ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9`
**Branch:** `codex/sorok-c05-continuing-relations-20261115-r1`
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1037-b-receipt-repair/Rawlsing`

This is the smallest C05 causal connection over the accepted C01 supporting
actor and C04-qualified child event paths. It is sourcefree engineering, not
native ADP-015/C4 relation authority, maternal psychology, generated speech,
independent volition, autonomy, household/genealogy issuance, or protected
integration.

## What was actually built

The exclusive lease allowed two product files. Only these product changes exist:

1. `supporting_actor.py`: the C01 role allowlist is deliberately extended from
   `parent` to `parent` + `neighbor`. No root, focal, source, private-state,
   registration, participation, or access semantics changed. This is the
   revision the C01 handoff explicitly reserved for C05.
2. `continuing_relations.py` (new): a dated relation carrier and its first
   consumer over the existing C12/P2 store.

No other product file changed. No new world, psyche, biography, event,
perception, scheduler, actor, or relation database was added.

### Carrier

Each caller-authorized relation change is one append-only C12 episode
(`P2_CONTINUING_RELATION_CHANGE`) plus one custody head
(`P2_CONTINUING_RELATION_HEAD`) in the same branch. The change body binds:

- schema/grade/root/branch/clock/operation,
- two live stable root/supporting actor IDs and their aliases,
- an illustrative caller-supplied relation token and change
  (`ENTER`/`LEAVE`/`CHANGE`),
- explicit `exposed_actor_ids` (both parties required; additional exposures
  allowed),
- a private-state commitment and raw private mapping in the C12 episode only,
- the previous relation episode, sequence, content address and source.

The head binds the primary episode ID/hash, previous head, sequence, exposure
and a content address. The reader walks both chains and fails to a qualified
custody HOLD if any change/head is missing, reordered, forged, wrong
root/branch/actor, or content-addressed to different bytes.

### State, promotion and depth

The relation state machine is finite: `ENTER` requires absent/left, `CHANGE`
requires active/changed, `LEAVE` requires active/changed. `PROMOTE` deepens only
the future representation from depth 1 to depth 2; it adds no relation fact,
does not rewrite any dated entry, and carries a hash of the history it deepens.
Variable depth is observable as depth 1 before promotion and depth 2 after it;
the original entry bytes and earlier consumer reads remain exact.

### First consumer

`read_actor_relative_context(session, actor_id, event_id)` is the terminal C05
consumer. It combines:

- the actual later BP4 event and the accepted C01 `read_actor_access` receipt
  path (with BP4 event hash/ID seal verification), and
- only the dated relation entries whose exposure names that actor, as of the
  event clock.

It returns `QUALIFIED`, `HOLD_NOT_EXPOSED`, `HOLD_UNKNOWN_SCOPE`, or
`HOLD_CUSTODY_SEVERED`. A denied scope is never reported as “no relation”.
Physical co-presence is not consulted for relation knowledge; a non-present
relation party can know the relation, and a present child can be held out.

## Minimum executable proof (actual, not precomputed)

The tests use the same P2 world with root focal Nadia, registered parent `P`
(role `parent`) and registered neighbor `O` (role `neighbor`), each with a
distinct stable ID, alias and private state.

- A dated `ENTER` at the actual world clock exposes only `P` and `O`; retry is
  `UNCHANGED` with no new episode/head.
- A genuinely later existing-owner P2 `ADMIT_EVENT` event at `clock + 6` has
  Nadia, `P` and `O` as actual co-present participants; all three have separate
  C12 `PERCEIVED` receipts.
- `P` and `O` contexts show the dated `ENTER` (clock 222 in the observed run),
  their own counterpart, `PERCEIVED` event access, and both-party event access.
- Nadia’s context for the same event is `PERCEIVED` but
  `HOLD_NOT_EXPOSED` with no relation token, party IDs or private value.
- A later event at `clock + 12` includes only Nadia and `P`; `O` is
  `NOT_PERCEIVED` yet still has its full qualified relation context, proving
  participation ≠ relationship knowledge.
- A later dated `CHANGE` (clock 234) exposes `P`, `O` and Nadia. Nadia sees only
  the `CHANGE`, never a retro-filled `ENTER`; `history_complete` is false and
  `prior_exposure` is `HOLD_NOT_EXPOSED`. `P`/`O` see both dated entries.
- A depth-2 promotion after the change deepens the representation; the earlier
  event’s `P` and Nadia contexts remain byte-exact (depth 1 there), and the
  stored `ENTER` episode bytes/hash never change.
- Actual `LEAVE` then re-`ENTER` at the consumer changes `P`/`O` context status
  (`ACTIVE` → `LEFT` → `ACTIVE`) while Nadia’s unexposed later history stays
  exactly what she was exposed to.
- Severing the `CHANGE` episode from the reader makes `P`, `O` and Nadia
  contexts `HOLD_CUSTODY_SEVERED` while event access remains `PERCEIVED` or
  `NOT_PERCEIVED`; world snapshot, world events, perceptions and checkpoints are
  unchanged. Restoring returns the exact pre-sever contexts.
- A fresh Python process reopens the same state root and returns the same
  registrations, dated history, event access, contexts, world hash and row
  counts; no registration/change/head/speech is duplicated.

## Proved

- Dated, exposure-limited relation entry/change/leave over actual world clocks.
- Later real existing-owner shared event plus separate parent/neighbor/child
  contexts that actually consume the dated history.
- Promotion deepens future representation without changing past entries or
  earlier consumer reads.
- Variable depth (1 vs 2) and qualified holds for unexposed/partial/unknown
  scopes.
- Physical co-presence separated from private relation knowledge.
- Same event, different actor-relative event access and relation access.
- Private relation values and C01 actor private values do not appear in any
  actor-facing relation context, world snapshot or later event.
- Stranger identity, future/backdated clock, forged root/branch/alias/value,
  changed-operation reuse, missing party exposure and private-value leak are
  refused without writes.
- Relation sever/restore changes the consumer to a qualified custody HOLD and
  back, with unrelated world/event/perception/checkpoint facts unchanged.
- Sequential request retry is idempotent; cold process read preserves exact
  state and does not duplicate rows or world material.
- C01 root actor list, focal owner binding, prior event/receipt access and
  normal C04/P2 lineages are preserved.

## Inherited (not re-proved as C05-native)

- S44/S47 generated root, Nadia focal identity, P2 world/clock and C12 store.
- C01 registration, private-state custody and actor-relative event access.
- P2 existing-owner `ADMIT_EVENT` sourcefree performed-event path.
- BP4 event hash/ID seal and S45 public event projection.
- C04 child-facing custody (used only as an adjacent qualified path; not
  extended, repaired or promoted here).
- Role `parent` semantics; this return deliberately adds only `neighbor`.

## Unproved / not claimed

- Native ADP-015/C4 relation authority, household membership, genealogy,
  family law, maternal psychology or independent volition.
- Mother-owned event selection, generated language, complete J1/Nadia response,
  G2 selected activity rule, durable acquisition, D04/D05.
- A multi-year relation simulator, trait drift, sparse-period biography, or a
  new relation campaign.
- Branch-fork replay of relation state. No public fork entry point was exercised.
- Concurrent same-operation writer uniqueness. Sequential retry is proved;
  C12 `BEGIN IMMEDIATE` serializes writes, but no concurrent same-operation
  proof is claimed.
- Provider/token/cost observations: `UNOBSERVED`.
- Human, scientific, source-rights or protected-merge receiving.

## Residuals

1. **Caller-supplied relation semantics.** `relation`, `ENTER/CHANGE/LEAVE`,
   value and exposure are illustrative caller facts. They are not an autonomous
   actor decision and not native C4/ADP-015 issuance.
2. **Depth is finite.** Only depth 1 → 2 promotion is implemented. Deeper
   representation is not implemented.
3. **One relation scope is exercised.** The module supports multiple scopes and
   per-viewer withheld counts, but the executed proof uses one scope.
4. **Private state in raw C12.** As with C01, raw relation private values live in
   the change episode and are developer-visible to a raw-store holder. Every
   actor-facing reader returns `NOT_READ`; only actor-facing non-leak is proved.
5. **Fork replay unobserved.** Cold process reopen is proved; a C12 branch fork
   carrying relation state was not exercised.
6. **Event content is inherited.** The later event is a real sourcefree P2
   owner admission. Any speech/language content in it is inherited S45/S39
   engineering, not C04 parent speech or G2 selection.
7. **C04 residuals excluded.** Parent self-read metadata exactness and D03
   caller-receipt root/branch/clock/operation binding remain excluded and are
   not promoted to authority by this return.
8. **No concurrency uniqueness proof.** Sequential idempotence is proved;
   concurrent same-operation deduplication is not.

## Test runs (actual commands, exits, time, RSS)

Interpreter: `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`
Every command used
`TMPDIR=$PWD/.local-logs/sorok-c05-continuing-relations/tmp`,
`PYTHONDONTWRITEBYTECODE=1`, `-B`, `-p no:cacheprovider`. Logs are under
`evidence/logs/`.

| Suite | Result | Exit | pytest s | Max RSS bytes |
|---|---:|---:|---:|---:|
| `SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py` | 5 passed | 0 | 55.31 | 60,870,656 |
| `SOROK-DUEL-C01-R1/test_c01_supporting_actor.py` | 6 passed | 0 | 16.51 | 56,037,376 |
| `SOROK-C03-C04-A-FINAL-R1/test_c04_first_consumer_identity.py` | 6 passed | 0 | 31.55 | 69,439,488 |
| `SOROK-C03-C04-GOFIRST-A-R1/test_c04_custody.py` | 12 passed | 0 | 70.62 | 72,499,200 |
| `SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py` | 5 passed | 0 | 19.94 | 60,014,592 |

The host was under concurrent unrelated load; these times are not an isolated
performance benchmark. Provider token/cost is `UNOBSERVED`.

## Source blobs at the frozen candidate

| Path | Git blob | SHA-256 |
|---|---|---|
| `.../developmental_recursion/supporting_actor.py` | `98cb4ceb3e5e201815c0ac46ba93f773601d818c` | `ba831554d7da2879cf8b32dd8a7a0337ef61e072408c24e3da69db43a9848b92` |
| `.../developmental_recursion/continuing_relations.py` | `343cf08a23da7a34305fdbb897102086f2124ee3` | `f4442b35e9d5fbf12b0fcc43fa99814a6a17f70aa16d877ba4a1fb4a621a7c3b` |
| `WORKER_RETURNS/SOROK_C05_CONTINUING_RELATIONS_R1/tests/test_c05_continuing_relations.py` | `4741264d5b23195731d7fe7f0f77e72ec847442e` | `115b0fd74837386340bb0bad4ef8eea3d7aba0c23671c72ed831f111ae69a79a` |

## Scope compliance

- No provider/model/account/auth/global-permission change, paid fallback, new
  server/VM/controller or nested agent.
- No timer or second campaign; the existing controller’s finite completion
  notification is unchanged.
- No #939 fleet restart, PYAT, protected merge, Browser management/contact, or
  D04/D05 implementation.
- No parent_speech.py, P3 owner/state_store, B04/B05, G2 performer or P2 owner
  edit.
- No `/tmp` write and no global-permission alteration.
- Only leased product files and this return’s own tests/evidence were written
  and committed.
- No self-G5. One independent nonauthor receiving may start only after this
  candidate is banked. STOP after this job.
