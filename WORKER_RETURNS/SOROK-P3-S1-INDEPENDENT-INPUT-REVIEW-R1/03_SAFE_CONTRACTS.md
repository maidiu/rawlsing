# Safe contracts and promotion boundaries

These are review-added guardrails for using S1 as TEST_ONLY design capital. They are not new CAN/ADP fields, not a new P2 proposal grammar and not issued psychology.

## H1 — compression evidence

H1 may be implemented only as an immutable external sidecar/evidence envelope bound to the existing P2 event.

Required contract:

```text
envelope_id       SHA256(canonical payload excluding id)
event_id          existing actual P2 event ID
event_hash        exact existing event hash
actor_id          exact developing actor
root/branch/clock exact owner identity and represented window
representation_form
                  SINGULAR_OCCURRENCE | REPRESENTATIVE_EPISODE |
                  ACCUMULATED_INTERVAL | RETROSPECTIVE_CRYSTALLIZATION |
                  RUPTURE_CANDIDATE
represented_window.from_clock/to_clock
coverage_basis    exact source/sampling basis, not a free-text claim
source_refs[]     immutable source identity + hash
actor_participation_refs[]
other_actor_contribution_refs[]
material_relation_refs[]
observed[] / unobserved[]
content_hash / integrity_state
```

Rules:

- read-only external evidence, never a state writer;
- no fabricated witness count, no synthetic act ledger, no global multiplier;
- no new `EventProposal`/`P2Owner` fields;
- the event ledger remains authoritative;
- actual participation and other-actor contribution remain distinguishable.

A candidate envelope missing exact event hash, root/branch/clock, source hashes or coverage basis is not a safe implementation contract.

## H2 — read-time activation and contradiction

H2 may be implemented only as a pure read-time query against already-committed records.

Required input:

```text
actor_id + root + branch + clock
exact prior CAN-010/CAN-011/ADP-015 record IDs and hashes
current material/access/relationship context
current interlocutor/role/permission
```

Required output vocabulary:

```text
ELIGIBLE
INHIBITED
UNKNOWN
CONTRADICTION
```

Rules:

- no state mutation from reading/evaluation;
- no automatic `REACTIVATE`, `DORMANT`, `WEAKEN`, `REINFORCE`, `TRANSFORM` or other lifecycle change;
- no scalar winner, personality type or demographic selector;
- contradictory records remain independently addressable;
- missing/unauthorized CAN-008 Rule A yields a diagnostic counterfactual, not an authorized response;
- activation state is not persisted unless a separately qualified rule owns a transition.

## H3 — memory, claims and opacity

H3 may be implemented only as a read/projection boundary over objective history and, where separately issued, ADP-016/ADP-017 state.

Rules:

- objective event ledger and hashes remain immutable under reinterpretation;
- no LLM prose creates ADP-016 memory or ADP-017 claim permission;
- `UNAVAILABLE`/inaccessible content is not rehydrated from analyst history;
- actor view and user view are separate projections;
- renderer reads an exact `ActorAccessibleRenderEnvelope`, never the analyst ledger;
- first-person claim output requires an issued ADP-017 state and exact claim accessibility;
- `MISSING_RULE`/deferred memory basis remains distinct from evaluated NO_CHANGE;
- no hidden confession, analyst diagnosis or forced self-explanation.

## Promotion gates

| Gate | Required before promotion |
|---|---|
| H1 | owner-validated immutable envelope schema and validator; no P2 grammar change |
| H2 | owner-validated pure-read adapter/readset and current consumer test |
| H3 | issued ADP-016/017 semantics or explicit HOLD; actor-access envelope test |
| P3 A–E | actual sourcefree vertical slice, P3 A–H counterfactuals, cold/severance/restore |
| Economy | measured bytes, reads, context, calls, latency and cold reopen |
| Source | immutable scholarly artifacts/page locators or explicit non-warrant grade |

No gate is satisfied by S1 prose alone.
