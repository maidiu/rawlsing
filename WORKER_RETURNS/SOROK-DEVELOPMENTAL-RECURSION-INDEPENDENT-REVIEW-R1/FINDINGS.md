# Findings and reproductions

Exact subject: `41863919210021eced174ad5abdf49cb2df2042a`.
The detailed evidence JSON is `EVIDENCE.json`; the source closure is `SOURCE_CLOSURE.json`.
All reproductions ran in a `git archive` scratch copy; no subject file was edited.

## R1 — Portal user view substituted for developing-actor experience

### Actual chain in the exact subject

```
P2Owner._realize
  -> self.fanin.public_opportunity(observation)              p2_owner.py:192
  -> public_opportunity returns "view": self.view()           p2_product_fanin/integration.py:153
  -> LifecycleEncounter.view -> S45Projection.view
  -> project_view(session, mode=...)                          s45_projection/projection.py:304
  -> perceived = set(session.user_perceived_ids())            projection.py:316
  -> user_perceived_ids = perceptions(branch, USER_ACTOR)     r30a/first_session.py:212-214
```

The developing actor is `root["actor_ids"][0]` (`p2_owner.py:47`), for example
`TEST_ONLY_BP1_R26V_ACTOR_A`; the portal user is `USER_ACTOR` (`U`). The
accessible payload is therefore U's public view, not A's actual perception
receipts. The exact subject's accessible payload has no `actor_ref`, no
perception receipts and no actor-specific status.

### Reproduction

```
cd <exact-subject-scratch>
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_actor_access.py
```

Observed (`logs/actor-access.log`):

- root actors `('TEST_ONLY_BP1_R26V_ACTOR_A','TEST_ONLY_BP1_R26V_ACTOR_B')`;
- `user_actor: U`; action alias `A`;
- accessible keys contain no `actor_ref` and no actor perception receipts;
- `view` schema `SOROK_WP19_ENCOUNTER_VIEW@1`, every visible event has
  `perceived_by_user=true`;
- A has 18 perception receipts, U has 17; the accessible view exposes 15
  user-visible events.

The exact subject's `00_RETURN.md` says "The coordinator passes only
actor-accessible projections" and "actor-accessible projection." That is false
for this adapter. The later lead head `99e79810f` adds
`P2Owner.actor_experience` and its focused tests pass, but it is outside the
exact subject and is not accepted here.

### Required repair / re-review

Bind the retrospective input to the developing actor's actual perception
receipts (E1/action hash, store alias, receipt window), refuse with an explicit
HELD when actor receipts are missing, and never fall back to the portal user
view. Keep the default CLI output free of actor-private experience. Submit the
repaired cut for its own exact-cut review.

## R2 — Invalid grounding mutates interval state before native refusal

### Actual chain

```
P2Owner.validate_proposal
  checks only allowed circumstance keys                     p2_owner.py:86
  never inspects history_refs contents/existence
P2Owner._realize
  reserves operation in adapter DB
  applies interval: produce_interval(domain)                p2_owner.py:147-152
  then calls native admit_event(history_event_refs=refs)    p2_owner.py:159-161
```

A nonexistent `history_refs` entry passes validation. The interval is produced
and changes native state; `admit_event` then raises
`S42_HISTORY_REF_MISSING`. The engine's event row remains `RESERVED` with no
result. The engine journal has no record of the interval effect. A retry is
refused as `P2_AMBIGUOUS_PRIOR_OPERATION_HOLD`; the batch cannot progress.

### Reproduction

```
cd <exact-subject-scratch>
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_invalid_grounding.py
```

Observed (`logs/invalid-grounding.log`):

```
batch exception: RecursionRefusal OWNER_REALIZE_FAILED:S41EventRefusal:S42_HISTORY_REF_MISSING: does-not-exist
before clock/state 222 ...
after  clock/state 226 ...
state changed: True
history records: 0
verify: True
journal rows: [(0, 'RESERVED', None, 'S41EventRefusal:S42_HISTORY_REF_MISSING: does-not-exist')]
retry exception: RecursionRefusal P2_AMBIGUOUS_PRIOR_OPERATION_HOLD
```

The same result reproduces at later lead head `99e79810f`
(`logs/later-head-invalid-grounding.log`). This is a missed "inadequate event
grounding" explicit failure and an untracked relevant state change. It also
contradicts the subject's claim that qualified interval effects are recorded
with the event result.

### Required repair

Prevalidate every native-only grounding field before applying an interval or
committing the operation reservation: ref element types, ref existence,
branch/actor binding, ordering and no future refs. Add a negative test that
proves unchanged state/clock, zero history records, no stuck `RESERVED` row and
a clean typed refusal. If a native validation cannot be replicated read-only,
provide an owner-level reconciliation that records or compensates the interval
result instead of leaving it untracked.

## R3 — Out-of-order event times are accepted pre-effect and stick the batch

### Actual chain

```
BatchEngine._normalize_batch
  checks 3-5 proposals and duplicate event IDs only     engine.py:229-241
BatchEngine._validate_all
  owner.validate_proposal per proposal against start   engine.py:617-631
RecursionCycle._parse_proposals
  event_time integer check only                        model_cycle.py:534-536
```

No layer enforces nondecreasing batch chronology. Times `240, 230, 250` with a
starting clock of 222 all pass per-proposal validation. Event 1 realizes at
240; event 2 then fails `P2_EVENT_CLOCK_NOT_FUTURE`; event 1 is recorded and
event 2 remains `RESERVED`. The batch is stuck and every retry fails.

### Reproduction

```
cd <exact-subject-scratch>
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_time_inversion.py
```

Observed (`logs/time-inversion.log`):

```
exception: RecursionRefusal P2_EVENT_CLOCK_NOT_FUTURE
before 222 after 240 changed True
records ['t1']
rows [(0, 'COMPLETE', 1, None), (1, 'RESERVED', 0, 'RecursionRefusal:P2_EVENT_CLOCK_NOT_FUTURE')]
retry: RecursionRefusal P2_EVENT_CLOCK_NOT_FUTURE
```

The same result reproduces at later lead head `99e79810f`
(`logs/later-head-time-inversion.log`).

### Required repair

Enforce nondecreasing (or strictly increasing) `event_time` over the ordered
batch before any reservation/effect, or add an owner `validate_batch` hook that
can preflight future events against projected state. Add a negative test
proving zero owner effects, zero completed records and no `RUNNING` batch for
inverted times.

## What was independently verified as sound

- Generic engine: 3–5 structural validation, owner validation before effects,
  sequential current-state calls, root/actor/branch binding, clock regression
  refusal, immutable batch material, completed replay without owner re-call,
  hash-chain tamper detection, durable reservations, hard-crash recovery,
  cross-process exclusion, ambiguous-operation hold, `MISSING_RULE`/`HELD`
  preservation.
- Actual P2 valid-input integration: two 3-event batches, state carry-forward,
  actual-versus-scheduled material C9 difference, cold root/history reopen,
  terminal nonmutation, actor-experience repair at later head (spot-check).
- Recursion boundary: bootstrap has `previous=None`; ordinary returns both
  halves and persists retrospective completion before the next batch; terminal
  has no next batch. `BOOTSTRAP/ORDINARY/TERMINAL` once each; no provider call
  between events.
- Privacy walker: no `PRIVATE_KEYS`/`FORBIDDEN_VALUE_MARKERS` hits in the three
  accessible payloads. This does not cure R1; the payload is the wrong subject.
- Source custody: #697/#699 product trees unchanged; all subject source hashes
  match; architecture and commission hashes match.

## No finding issued

- **No source/authority bypass** or protected/PROGRAMMA rewrite was found. The
  only non-return change is an append-only candidate status note.
- **No `MISSING_RULE` → `NO_CHANGE` laundering** was found. P2 keeps
  `durable_psychological_transition=MISSING_RULE`; the engine keeps `HELD`
  distinct from `NO_CHANGE`.
- **No claim of native psychology or independent B** was accepted. The
  controlled P2 fixture and mock/file provider are labeled.
- **No fabricated objective history** was found in the valid path: the
  provider receives only the adapter's accessible payload; objective records
  and identities stay in the journal/owner custody.

## Exact replay commands

```
# full subject suite
cd <scratch>
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests

# unchanged P2 baseline suite
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1/tests

# cold witness (write receipt outside the subject)
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/run_cold_cli_witness.py <out.json>

# reproductions
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_invalid_grounding.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_time_inversion.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_actor_access.py
PYTHONDONTWRITEBYTECODE=1 python3 -B reproductions/repro_privacy.py
```

Sever/restore was performed on the scratch copy only: remove the persisted
pre-next-batch retrospective block or replace `s.produce_interval(domain)` with
`None`, run the named target, then restore exact bytes and verify the hashes
`af83f8f1...` / `c9566d18...`. Logs are in `logs/`.
