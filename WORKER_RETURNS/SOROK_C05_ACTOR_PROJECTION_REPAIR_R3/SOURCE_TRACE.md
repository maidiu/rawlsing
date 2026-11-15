# C05 R3 source-owner and first-consumer trace

**Base source:** `5d771dd86767655534b23576075e5da2db4fba78`
**Corrected product blob:** `8006440bd420ce8526bb2f333cd201ac077cbd22`
**Corrected source-256:** `a9e0595f92005fffb0c93720b7d63881994df71ed14fbbd140a723cd78f965d1`
**Hostile court:** `df4e51e75298bc1393c6f4b3640449e678bc44ff`

## Actual readers and data paths

### Event perception proof

`read_actor_relative_context(session, viewer, event_id)`
→ `_access_or_hold` → C01 `supporting_actor.read_actor_access`
→ C12 perception receipt + (for supporting actors) participation episode.

This path is unchanged. It proves whether *this viewer* perceived the actual BP4
event. The projection correction now copies that status into
`context_effect.event_perception` with
`event_perception_source: "VIEWER_EVENT_ACCESS"` and
`event_perception_scope: "VIEWER_ONLY"`. `C12_EVENT_PERCEPTION` is appended to
`context_effect.basis` only when that viewer status is `PERCEIVED`.

### Relation-history path

`read_actor_relative_context`
→ `read_relation_history(... as_of_clock=event.clock)`
→ `_history_envelope`
→ `_all_scopes` / `_verify_scope`
→ `_representation`
→ append-only C12 `P2_CONTINUING_RELATION_CHANGE` / `P2_CONTINUING_RELATION_HEAD`
episodes.

No relation write is an owner operation receipt. The change/head chain is a
self-hash custody chain over caller-authorized illustrative input. It is not C4/
ADP-015 actor authority, perception, or a qualified relation-knowledge receipt.

### Consumer search

A repository search for `read_actor_relative_context`, `read_relation_history`,
`context_effect`, `relation_temporal`, and `continuing_relations` outside the
module, its original tests, the prior C05 probes, and this R3 return found no
product/D02/D03/J2/persona/UI/model consumer. The actual first consumer remains
`read_relation_history` / `read_actor_relative_context` themselves. No executed
downstream hallucination or downstream event-time misuse can be claimed.

## Hidden-count noninterference

Removed from both actor-facing envelopes:

- `read_relation_history().withheld_relation_count`
- `read_actor_relative_context().relation_scope.withheld_relation_count`

No controller-only count API was invented. Status, custody, qualified
relations, private-state boundary, event access and temporal labels remain.

The absent-scope and fully-unexposed-scope statuses are unified as
`HOLD_NOT_EXPOSED`. A live named query for an absent relation token and a live
named query for an unexposed relation token now return the same document. The
new R3 test checks exact equality, including after severance of the unexposed
relation; the unexposed viewer receives no custody disclosure. This is the
actual controlled noninterference, not only field-name deletion.

## Same-clock temporal ordering

The relation reader still selects relation entries by
`body.clock <= event.clock`. It does not consult the C12 world-event sequence,
the relation episode sequence, or a within-clock owner operation receipt. The
C12 store has separate `world_event` and `episode` sequence spaces, and relation
writes are not in the owner operations table.

Therefore same-clock relation writes appended after an event can appear in that
event's **retrospective** context. The corrected ABI states this explicitly:

- `relation_scope.temporal_scope = RETROSPECTIVE_AS_OF_EVENT_CLOCK`
- `relation_temporal.relation_projection = RETROSPECTIVE_AS_OF_EVENT_CLOCK`
- `event_time_relation_knowledge = NOT_AVAILABLE`
- `event_time_relation_status = HOLD_SOURCE_AUTHORITY`
- `within_clock_cutoff = UNAVAILABLE`
- `usable_as_prior_event_cause = false`
- reason `NO_SOURCE_QUALIFIED_WITHIN_CLOCK_ORDERING_OR_RECEIPT_RULE`

Later-clock relation changes remain excluded from an earlier event by the clock
filter. No later relation was deleted to fake temporal stability. No event was
rewritten. No timestamp precision or new ordering rule was invented.

## Residual owner decision

True event-time relation knowledge (what the actor knew before a same-clock
later relation write) requires a source-qualified within-clock ordering/receipt
rule from the original C05/CAN/ADP issuer. None was found in the qualified owner
ABI. That edge is `HOLD_SOURCE_AUTHORITY`; this return supplies only the bounded
retrospective projection label and the viewer-specific perception provenance.
No native actor knowledge, psychology, generated language, selection, J1/J2,
human or protected authority is issued.
