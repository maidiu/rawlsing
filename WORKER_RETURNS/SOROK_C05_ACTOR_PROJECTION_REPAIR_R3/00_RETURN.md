# SOROK C05 R3 — actor-facing projection and retrospective temporal correction

**Terminal disposition:** `AUTHOR_C05_R3_CANDIDATE_FOR_SAME_NONAUTHOR`
**Candidate SHA:** `4b33b8be1127c2186931a66f23e3a2b05feaf0a6`
**Frozen start:** `1cf1a37113cb7a48137734648b523a0a6deccd92`
**Accepted mechanical source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Hostile court:** `df4e51e75298bc1393c6f4b3640449e678bc44ff`
**Branch:** `codex/sorok-c05-actor-projection-repair-20261115-r3`
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1037-b-receipt-repair/Rawlsing`

This is the original author’s one bounded C05 projection correction after the
same nonauthor’s hostile actor-view/temporal court. It preserves the accepted
mechanical relation write/custody and repeated-promotion refusal. It is not
native actor knowledge, CAN/ADP/V3 science, generated language, G2 selection,
J1/J2, human, source-rights or protected acceptance.

## Exact correction

Only
`WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/continuing_relations.py`
changed.

- Base blob `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
- Corrected blob `8006440bd420ce8526bb2f333cd201ac077cbd22`
- Corrected SHA-256 `a9e0595f92005fffb0c93720b7d63881994df71ed14fbbd140a723cd78f965d1`
- `supporting_actor.py` unchanged `98cb4ceb3e5e201815c0ac46ba93f773601d818c`

### 1. Hidden-relation noninterference

Actor-facing `withheld_relation_count` is removed from
`read_relation_history` and from the nested
`read_actor_relative_context.relation_scope`. No controller-only count API was
invented. Absent and fully unexposed scopes now return the same
`HOLD_NOT_EXPOSED` document; status, custody, qualified relations, private-state
boundary and event access remain.

The new tests compare the same real event/viewer with and without a hidden
unexposed relation and require byte-identical permitted outputs, including named
absent/unexposed queries and unexposed-relation severance. The unexposed viewer
receives no custody disclosure.

### 2. Viewer-specific perception provenance and plural relations

`context_effect` now carries:

- `event_perception` from **this viewer’s** `event_access.status`;
- `event_perception_source = VIEWER_EVENT_ACCESS`;
- `event_perception_scope = VIEWER_ONLY`;
- `C12_EVENT_PERCEPTION` in `basis` only when that status is `PERCEIVED`;
- `relation_aware` as the known-relation indicator;
- both logical relations retained in `relation_scope.relations` and
  `relation_count`;
- the singular summary explicitly labeled
  `summary_selection = MECHANICAL_FIRST_SORTED_RELATION_KEY`,
  `summary_is_salience_or_psychology = false`.

No salience selector or psychology is invented. Another actor’s event access is
not used to set the viewer’s `event_perception`.

### 3. Retrospective as-of-event-clock label and event-time HOLD

`read_actor_relative_context` now exposes:

- `relation_scope.temporal_scope = RETROSPECTIVE_AS_OF_EVENT_CLOCK`;
- `relation_temporal.relation_projection = RETROSPECTIVE_AS_OF_EVENT_CLOCK`;
- `event_time_relation_knowledge = NOT_AVAILABLE`;
- `event_time_relation_status = HOLD_SOURCE_AUTHORITY`;
- `within_clock_cutoff = UNAVAILABLE`;
- `usable_as_prior_event_cause = false`;
- reason `NO_SOURCE_QUALIFIED_WITHIN_CLOCK_ORDERING_OR_RECEIPT_RULE`.

Same-clock relation writes appended after an event can still enter that event’s
**retrospective** context. They are not event-time prior knowledge and are not
usable as prior-event cause. Later-clock changes remain excluded from earlier
events. No later relation was deleted, no event rewritten, no timestamp
precision fabricated and no new ordering rule invented.

True same-clock event-time relation knowledge remains
`HOLD_SOURCE_AUTHORITY` for the original C05/CAN/ADP issuer. The exact first
consumer is the C05 public reader itself; no downstream product consumer of
these fields was found.

## Base RED (unchanged hostile probes)

The three probes and both helpers were copied byte-identically; their SHA-256
values equal the court’s `PROBE_PINS.json`. The hardcoded reviewer scratch path
was redirected by a temporary symlink into the leased R3 scratch; probe bytes
and oracles were not edited.

| Probe | RED literal exit | Actual RED |
|---|---:|---|
| Challenge 1 | 0 | same event/viewer; `withheld_relation_count 0→1`, all other permitted fields equal |
| Challenge 2 | 0 | same-clock ENTER/PROMOTE after event 228 enters event 228 relation context; event doc/access unchanged |
| Challenge 3 | 0 | `NOT_PERCEIVED` viewer with QUALIFIED relations; `basis` includes `C12_EVENT_PERCEPTION`; plural relations present |

Raw RED reports:
`c05_challenge1_report_RED_at_5d771dd.json`
(`bfdd1d754fb253d69260a3711a7dc586fbde88d1213430bef6f75ff97ab1e0b1`),
`c05_challenge2_report_RED_at_5d771dd.json`
(`07d138e40d769e96d9cb5a1fd770dc77e21f99657d259503fb04be072b0c653d`),
`c05_challenge3_report_RED_at_5d771dd.json`
(`cacca579a30879913b579cf38ff4eddaf94aff9bdfaaddfd4c90ba2c86e2edc3`).

The first challenge-3 RED report was overwritten by the post-fix run; the same
byte-identical probe was re-executed against the base product blob to preserve a
raw RED report. The original RED stdout/time log is also retained. This is
disclosed.

## Post-fix unchanged-probe outcomes

| Probe | Post-fix literal exit | Actual observation |
|---|---:|---|
| Challenge 1 | 1 | obsolete oracle `KeyError: withheld_relation_count`; field intentionally removed |
| Challenge 2 | 0 | same-clock retrospective inclusion still observed; new context labels it and holds event-time knowledge |
| Challenge 3 | 2 | only obsolete `C12_EVENT_PERCEPTION`-without-own-perception check fails; viewer-specific provenance, plural/cold/private checks pass |

Post-fix reports:
`c05_challenge2_report_POST_FIX.json`
(`4044256df12401d832a635cd49104f85014820b4d50a6489d21213543a0e1c44`) and
`c05_challenge3_report_POST_FIX.json`
(`6868143a43d277c752aff57d03875a08dde20aad5a0e2487bc84b52298a18e6c`).
Challenge 1 produced no post-fix report because its old oracle crashed on the
removed key.

## New GREEN assertions

`tests/test_c05_actor_projection_repair_r3.py` — **4 passed**, exit 0, 30.41 s,
max RSS 61,845,504 B. It proves:

- hidden unexposed relation changes no permitted actor-facing field; named
  absent/unexposed queries are equal; hidden severance is not disclosed; visible
  positive relation still works; sever/restore and fresh-process cold exact;
- viewer-specific `event_perception`/`basis`; a `NOT_PERCEIVED` viewer with known
  relations has no `C12_EVENT_PERCEPTION` basis, a `PERCEIVED` viewer does;
  plural relations and mechanical summary preserved;
- event doc/hash/access immutable under same-clock retrospective writes; later
  clock excluded; cold exact; explicit temporal labels and event-time HOLD;
- ENTER/CHANGE/LEAVE history, depth promotion, same-operation retry
  `UNCHANGED`, different-operation depth-2 refusal-before-write, real P2 event
  access and private boundaries preserved.

## Preserved / obsolete historical tests

| Suite | Result | Exit |
|---|---|---:|
| C05 R3 new assertions | 4 passed | 0 |
| C05 R2 focused promotion repair | 1 passed | 0 |
| Original C05 author suite (bytes immutable) | 3 passed, 2 failed | 1 |
| Prior 89-check independent probe (bytes immutable) | obsolete failed, `KeyError` | 1 |
| C01 supporting actor | 6 passed | 0 |
| C04 first-consumer identity | 6 passed | 0 |
| C04 custody | 12 passed | 0 |
| P2 owner | 5 passed | 0 |

The two original C05 failures are exactly the intentionally corrected actor
ABI: old `withheld_relation_count` (`KeyError`) and old
`HOLD_UNKNOWN_SCOPE` (now the intentionally indistinguishable
`HOLD_NOT_EXPOSED`). The old challenge-3 oracle also fails only its obsolete
`C12_EVENT_PERCEPTION`-without-perception assertion. The prior 89-check
independent probe was copied byte-identically and post-fix exits 1 with
`KeyError: withheld_relation_count` at its first unexposed assertion; that is
the same intentional ABI removal. Original test/probe bytes were not modified,
skipped or rewritten.

## Proved / inherited / unproved

**Proved (sourcefree author candidate):** hidden-cardinality noninterference;
viewer-specific perception provenance; plural relation retention with mechanical
summary label; retrospective as-of-event-clock projection with explicit
event-time HOLD; event/access immutability under same-clock retrospective writes;
later-clock exclusion; cold exactness; preserved accepted relation mechanics.

**Inherited:** C01 registration/access and private boundaries; C04 child-facing
custody (regressions pass, not extended); P2 owner/world; BP4 event seal; C12
store; accepted C05 write/custody and promotion fix.

**Unproved / held:** native ADP-015/C4 relation authority, household/genealogy,
maternal psychology, independent volition/autonomy, generated language, G2
selection, complete J1/Nadia response, D04/D05, durable acquisition, human/
scientific/source-rights receiving, protected merge, #939 fleet, concurrent
same-operation uniqueness, branch-fork replay, depth > 2, and true same-clock
event-time relation knowledge (`HOLD_SOURCE_AUTHORITY`).

## Three verdicts

- **Engineering:** `AUTHOR_PASS_BOUNDED_SOURCEFREE_PROJECTION_CANDIDATE` —
  actual source correction, RED→GREEN probes, new assertions, preserved
  mechanics and regressions; independent receiving still required.
- **Scientific:** `HELD` — no native actor relation knowledge, event-time
  perception science, CAN/ADP/V3 rule or psychology is issued.
- **Authority:** `SCOPED_SOURCEFREE_AUTHOR_EXECUTION_ONLY__NATIVE_PROTECTED_HELD`
  — bounded execution under the user lease; no protected merge, source right,
  human grant or native authority.

## Scope compliance / STOP

Only the leased `continuing_relations.py` and this own R3 return were committed.
All other product, `supporting_actor.py`, C04/P3/P2/B/G2, protected PRE-MAIN and
#939 remained read-only/STOP. No provider/model/account/auth/global-permission
change, paid fallback, installation, CI/GitHub Actions, new agent/server/
controller, PYAT/Browser/SEAM operation, protected merge or B05 reopen. No
`/tmp` write. No self-G5.

HQ routes this frozen candidate back to the same nonauthor reviewer for focused
rereceiving. No automatic further repair, duel or campaign. STOP.
