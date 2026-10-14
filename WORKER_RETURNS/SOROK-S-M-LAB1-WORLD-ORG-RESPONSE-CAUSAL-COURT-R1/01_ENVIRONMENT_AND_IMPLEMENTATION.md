# 01 — exact environment and implementation

## Environment

| Item | Value |
|---|---|
| Host | local macOS darwin x86_64 (worktree `/Users/matthewsmith/Desktop/Rawlsing`) |
| Interpreter | Python 3.11.3, `/usr/local/bin/python3` |
| Node | v18.14.2 — used **only** to run S-M's own `repro/sm_court.mjs` schema/receipt gate |
| Authoring resource | OpenCode Go session, model id `opencode-go/mimo-v2.6-pro`; shared Go quota, account/counter state `UNKNOWN` |
| Actor-trial model surface | **ABSENT** — no pinned callable LLM API for the experiment → `MODEL_BEHAVIORAL_COMPARISON_HOLD`; no model outputs fabricated |
| RNG | named seeded RNG: `random.Random(int(sha256(canonical_json({"seed": name})), 16))`; seeds `S01..S12`; used for preregistered tie-breaks only |
| Survey/original data | none read |
| PRE-V3 / V3 production | none touched; no wake; no weld; no product release |
| Write terrain | only `WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/` |

## Implementation (source-free synthetic lab)

```
lab/
  hashutil.py            canonical JSON (float-free) + sha256 semantic identity + token estimates
  owners.py              typed durable owner state CAN010/CAN011/ADP015/ADP016/ADP017 +
                         WORLD_PUBLIC_RECORD; effects require destination owner + admitted
                         parents; monotonic history; owner-boundary enforcement
  world_fixtures.py      invented apprenticeship/certification world receipts (1998 W_SYNTH_001,
                         1999 position variant W_SYNTH_002), positions, relationships,
                         opportunities/routes, admitted events + authorized owner effects per K
  transition.py          bounded CAN-008-compatible lab rules T0-T8; arms A/B/C; route gates,
                         multi-stream recruitment, relation-view reconstruction (A/B) vs typed
                         index (C), event-local conation (B/C), history admission with
                         T4/T5/T6/T7 gates, selection law incl. DEFAULT_TO_NO_OP_WHEN_NO_RECRUITMENT
  opacity.py             actor-safe projection (ADP016/ADP017 derivative), evaluator metadata,
                         hidden-origin injection check, self-explanation testimony modes
  runner.py              machine-first trial receipts (exact S-M audit_schema.output_required
                         fields + lab_extension), cold replay, latency capture
  experiment.py          run order K1/K3/K5 -> integrity gate -> K2/K4/K6; per-K frozen
                         predicates; 15 null controls; opacity suite; cost aggregation; comparison
  liveness_controls.py   prereg-declared B/C mechanism liveness + K2 failure diagnosis
  test_lab.py            20 mechanism unit tests (pre-freeze)
  run_lab.py             primary battery CLI (post-freeze)
```

Rule dossiers (lab proposals, not adopted law): `T0_WORLD_CONTEXT_GATE`, `T1_RECEIVABILITY`, `T2_SITUATED_RECRUITMENT`, `T3_EVENT_LOCAL_CONATION` (B/C), `T4_RECOGNITION`, `T5_CORRECTIVE_REINTERPRETATION`, `T6_NONDECLARATIVE_TRACE`, `T7_CATEGORY_ENFORCEMENT`, `T8_TYPED_TOPOLOGY_OPTION` (C). Each has inputs, owner, positive transition and a negative/no-change branch (see `lab/transition.py` constants and the S-M T0–T8 dossier in `02_K1_K6_SPEC.json`, which this implementation binds).

## Arms (as implemented, matching the commission exactly)

- **A — MINIMAL BASELINE:** world-conditioned exact events/relationships; existing governed owner state; memory/trace; CAN-008-compatible recruitment; **no** new durable conation/recognition/attractor graph. Relation reading is reconstructed from admitted formation ancestry (fairness requirement), never stored.
- **B — EVENT-LOCAL ORGANIZATION:** A + per-event conation direction, witness stakes, pressure/conflict, route costs. Compiled per event, hash-excluded from durable state, never an effect parent (`persistence: EVENT_LOCAL_ONLY__NOT_PERSISTED__NOT_EFFECT_PARENT`).
- **C — TYPED RELATIONAL TOPOLOGY:** B + exactly two typed relations (`COMPENSATES_FOR`, `CONDITIONS_RECOGNITION`) with exact admitted formation parents. A forged edge without a formation parent in admitted history is refused (`NO_UNAUTHORIZED_C_GRAPH_EDGE`). No C state becomes canonical.

## Fairness accounting

Same world, admitted history, evidence objects, seeds and call count (0) across arms; A is never retrieval-starved (it receives the same admitted formation events and reconstructs the relation view); measured retrieval tokens and relation-scan counts reported per arm in `04`.

## Machine-first record

Every trial receipt contains: recruited stream refs with parent events, receivability/uptake refs, candidate routes with support and gate codes, proposed/authorized/committed destination-owner effects with pre/post state hashes, relation view + formation cost, memory/access/trace refs, actor claim permissions, public-standing effects, action effects, hold/invalid codes, replay digest — before any prose. `prose_optional` is a constant marker and is never scored; the adjective-only null confirms changed wording moves nothing.
