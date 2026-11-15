# C05 R3 source trace and shortest causal defects

**Source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Product blob:** `d2120fa9f691042336b8ec1f0b7aa9e150ea0b3a`
**Module:** `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/continuing_relations.py`

## Actual RED 1 — actor-facing hidden relation cardinality

- `_history_envelope` iterates all verified scopes and increments `withheld`
  for every scope that yields no viewer representation (`:549-564`).
- It returns `"withheld_relation_count": withheld` in the actor-facing read
  document (`:573-585`).
- `read_actor_relative_context` copies the count into
  `relation_scope["withheld_relation_count"]` (`:718-728`).
- There is no controller capability/role check or separate controller-only
  diagnostic function in the module. The header `read_boundary` marks
  `unexposed_scope: QUALIFIED_HOLD`, not the count as controller-only.
- Controlled A/B fixture: same real event/state, A no relation, B hidden P/O
  relation. Actor-facing history/context are equal except the count changes
  `0 -> 1`. Positive C exposes a P/R relation to Q and still returns hidden
  count `1`.
- **Shortest correction:** omit `withheld_relation_count` from
  `read_relation_history`/`read_actor_relative_context`, or expose it only
  through an explicit controller-only diagnostic. Keep status/custody/relations.
  No new ledger, psychology or owner receipt.

## Actual RED 2 — same-clock later relation enters an earlier event context

- `_representation` filters relation changes with
  `body.clock <= as_of_clock` (`:455-462`); no operation/sequence/owner cutoff.
- `read_actor_relative_context` takes `event.clock` and calls
  `read_relation_history(..., as_of_clock=event_clock)` (`:698-728`).
- `record_relation_change` admits `clock == session.world().clock`
  (`:960-964`), so a relation write after a real event can share the event
  clock.
- The C12 store has separate `episode` and `world_event` sequence counters
  (`bp4/store.py:145-193`). The real event's world-event seq is 14; the later
  same-clock relation episodes are seq 54/56; they are separate sequence spaces.
  The owner operations DB contains the real events but not the caller-appended
  relation writes.
- Controlled fixture: event E1 at 228 is read before/after ENTER and PROMOTE at
  228. The event document/hash/access are unchanged; E1's relation context
  changes from `HOLD_NOT_EXPOSED` to `QUALIFIED` (depth 2). A later-clock CHANGE
  at 234 is excluded; cold replay is exact. No retrospective/within-clock label
  exists.
- **Shortest correction:** label the relation context
  `RETROSPECTIVE_AS_OF_EVENT_CLOCK` (or equivalent) and do not use it as prior
  event cause. A true event-time cutoff needs a source-qualified within-clock
  ordering/receipt rule (`HOLD_SOURCE_AUTHORITY` for the original C05/CAN/ADP
  issuer). Do not ban retrospective understanding or rewrite E1.

## Static projection risk — context effect basis versus own perception

- `_context_effect` selects `relations[0]` (`:675`) and sets
  `relation_aware: true` with `basis:
  ["DATED_RELATION_HISTORY", "C12_EVENT_PERCEPTION"]` (`:683-695`).
- It does not consult the viewer's own `event_access.status`; it only computes
  `both_parties_event_access` for a party (`:676-682`).
- Challenge 3: P has two prior relations, current event is `NOT_PERCEIVED`, but
  `context_effect.basis` still contains `C12_EVENT_PERCEPTION`;
  `event_access.status` remains correctly `NOT_PERCEIVED`, and the plural
  `relations` list has both relations. The singular summary is the first sorted
  relation key, not a salience/psychology rule.
- No product downstream consumer of `C12_EVENT_PERCEPTION`/`relation_aware`/
  `context_effect` exists outside the C05 module and tests/probes
  (`evidence/downstream_consumers.txt`). The first consumer is the public
  actor-facing reader. This is a projection ambiguity, not an executed
  downstream misinference.
- **Owner decision:** add viewer-specific `event_perception` from the viewer's
  own access; include `C12_EVENT_PERCEPTION` only when `PERCEIVED`; keep
  `relation_aware` distinct. Optionally label the singular summary as first-
  sorted relation key. The plural `relations` output remains authoritative; no
  salience selector is invented.

## First consumer / downstream

- Actual first consumer: `read_relation_history` and
  `read_actor_relative_context` in the C05 module.
- No D02/D03/J2/persona/UI/model consumer imports these fields in this checkout.
  The next actor/person consumer is not built.
- Therefore the withheld count is an actual public actor-facing API supply; the
  basis/plural fields are public projection output but have no executed
  downstream consumer.
