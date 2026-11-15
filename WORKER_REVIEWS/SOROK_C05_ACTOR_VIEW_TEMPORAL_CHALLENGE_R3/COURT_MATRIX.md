# C05 R3 court matrix — actual RED, PASS, static risk, owner decision

**Source:** `5d771dd86767655534b23576075e5da2db4fba78` (product blob
`d2120fa9...`).
**Event:** real P2 owner `SPEECH` events; actual `read_relation_history` and
`read_actor_relative_context`; no toy reader.

## Challenge 1 — hidden relationship existence/cardinality

One real event (clock 228) is read for viewer Q before and after a hidden P/O
relation, then after a genuinely visible P/R relation.

| Class | Finding |
|---|---|
| Actual RED | The same actor-facing event/read changes `withheld_relation_count` from `0` to `1` when an unexposed P/O relation is added. In the history document and in `read_actor_relative_context.relation_scope`, every other compared actor-facing field is equal: status `HOLD_NOT_EXPOSED`, `relations=[]`, `context_effect` `{relation_aware:false, basis:["QUALIFIED_HOLD"]}`, event access `NOT_PERCEIVED`. The reader therefore supplies hidden existence/cardinality to the actor-facing consumer. |
| Actual PASS | Same event ID/hash/clock across A/B/C; the visible P/R relation exposes a genuinely qualified relation to Q; Q still does not perceive the event; change/head sever gives custody HOLD only to the exposed viewer; unexposed viewer gets no custody disclosure; restore and fresh-process cold are exact. |
| Static risk | The prior ABI described the count as a qualified-HOLD diagnostic; there is no separate controller-only API or capability in the module. The count is in the public actor-facing document. |
| Owner decision | C05 read-side projection owner. Smallest correction: remove `withheld_relation_count` from actor-facing `read_relation_history` / `read_actor_relative_context`, or expose it only through an explicit controller-only diagnostic. Keep status/custody/relations. No new psychology or ledger. |

## Challenge 2 — later same-clock relation knowledge in an earlier event

Real owner event E1 at clock 228 is read first with no relation, then after an
ENTER and PROMOTE appended at the same clock 228, then after a later event at
234 and a relation CHANGE at 234.

| Class | Finding |
|---|---|
| Actual RED | E1's actor-facing relation context changes from `HOLD_NOT_EXPOSED` to `QUALIFIED` (and depth 2 after promotion) when relation writes are appended **after** E1 at the same logical clock. The event document/hash/access are unchanged; this is not a past rewrite, but the same-event context is not event-time stable and has no explicit retrospective/within-clock boundary. |
| Actual PASS | E1 event document/hash/clock and `PERCEIVED` access are unchanged before/after; a relation CHANGE at later clock 234 is excluded from E1; cold replay of E1 is exact; C12 world-event seq and relation-episode seq are separate spaces; owner operations contain the real events but not the relation writes. |
| Static risk | `read_actor_relative_context` uses `event.clock` only (`continuing_relations.py:714-717`); `_representation` filters `body.clock <= as_of_clock` (`:459-462`); no operation/seq cutoff is consulted. The relation episode seq (54/56) is after the event world-event seq (14), but in a separate sequence space; relation writes are caller-appended C12 episodes, not P2 owner operations. The output is not labeled retrospective vs event-time. |
| Owner decision | Bounded projection fix: explicitly label the relation context `RETROSPECTIVE_AS_OF_EVENT_CLOCK` / event-time relation knowledge `NOT_AVAILABLE`; do not use it as prior event cause. A true within-clock event-time cutoff needs a source-qualified ordering/receipt rule, which is `HOLD_SOURCE_AUTHORITY` for the original C05/CAN/ADP issuer. Do not ban retrospective understanding or rewrite E1. |

## Challenge 3 — known relation versus perceived event; plural relations

P has two qualified prior relations (P/O and P/R) and does not perceive the
current event (focal/O).

| Class | Finding |
|---|---|
| Actual PASS | `event_access.status=NOT_PERCEIVED` is distinct from `relation_scope.status=QUALIFIED`; relation awareness is preserved without claiming event perception; two simultaneous relations are present in the plural output; the singular summary is the first relation key sorted, not a salience/psychology rule; cold and private-state boundaries are exact. |
| Static projection risk | `context_effect.basis` includes `C12_EVENT_PERCEPTION` while the same document's `event_access.status` is `NOT_PERCEIVED` and `both_parties_event_access` is false. No product downstream consumer of `C12_EVENT_PERCEPTION`/`relation_aware`/`context_effect` was found outside the C05 module and its tests/probes; the first consumer is the public reader. This is a projection ambiguity, not an executed downstream misinference. |
| Owner decision | Bounded projection fix: make `context_effect` viewer-specific, e.g. add `event_perception` from the viewer's own access and include `C12_EVENT_PERCEPTION` only when that status is `PERCEIVED`; keep `relation_aware` distinct. Do not invent a salience selector. Optionally label the singular summary as first-sorted relation key; the plural `relations` output remains authoritative. |

## Three separate courts

| Court | Verdict | Basis |
|---|---|---|
| Engineering | `REVISE_EXACT_DEFECT` | Actual actor-facing hidden-cardinality supply; unlabeled retrospective/event-time relation context under same-clock later writes; plus a static actor-facing `C12_EVENT_PERCEPTION` basis ambiguity for a `NOT_PERCEIVED` viewer. Bounded read-side/projection correction exists. Accepted mechanical custody/promotion fix is not reopened. |
| Scientific | `HELD` | No native actor relationship knowledge, event-time perception science, CAN/ADP/V3 rule or psychology was issued. The probes are sourcefree fixture behavior; actor-qualified knowledge remains unproved. |
| Authority | `HELD` for native/protected; `PASS_SCOPED_SOURCEFREE_TEST_ONLY` for this review | This hostile test review is within the user lease. No protected merge, native C4/ADP-015, actor/human grant or source-rights issuance. |

## Prior accepted mechanical custody

`c0cbe82f62a4e9516bf466575de3692c5c3081df` accepted the caller-authorized
illustrative relation record/custody, the repeat-promotion refusal-before-write
fix, normal later-consumer behavior and cold/sever controls at its stated
fixture boundary. Those files/claims are preserved. This court does not
retroactively revoke them; it produces contrary witnesses at the actor-view
projection/temporal boundary they did not establish.
