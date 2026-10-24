# R91 R05V R5 independent review — return

Verdict: **REVISE.** R5 genuinely links actual AT10 I05 discovery and AT11
MX01R2 recursive native compositions to learned M1/M2/B5 and the same N10E
consumer, and adds an actual native joint query. But this is demonstrated through
the raw compatibility graph path, not the trusted coordinator/custody path. The
`NativeGraphSlot`/coordinator interface still carries only source/release/query/
predicate/consumer/route metadata; it has no actual discovery result/receipt/
frontier, recursive handoff/lineage/root-parent, target arity/order, M1/M2/B5
currentness or E41 input association. The High decision's coordinator-owned
actual-input and complete retained-original boundary is therefore not implemented
for the materially different routes.

## Custody

- Stable root `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`;
  branch `agent/opencode-pyat-r91-r05v-r5-consumer-review-r1`; startup/HEAD
  `68b8f33fae7432e968e25f312f265f45c523718c`; clean at gate.
- R05V R5 commission `0846de52...`; High decision
  `c618dc28d722ba64f2f9d7bf39cbd9915b429ea8`; R5 contract
  `ee999a4aada1d779364dd4734d6d4763e99d3e4b`; R5 code
  `70d1d87417bad215234145ac1b587cbeec8f98d0`; R4 custody code
  `0b60f26db55119cfdbc68895e24cee9db6408d29`.
- Frozen EXPECTATIONS `7e2b8030f8bb8e77c01697369c34fdb9111835be`,
  committed before R5 code inspection.
- R5 module blob `1095f491...` unchanged from R4; R5 test blob `9c04f789...`;
  analytical composition R4 blob `ed2b1680...`; provider/evaluator/R08 accepted
  blobs unchanged (`23167aa2...`, `62e5eced...`, `3ca860e4...`/`5832ce05...`).
- R4 and R5 author manifests independently recomputed: 7/7 each, self-excluded.
- Only authorized five-path code plus own r4/r5 returns changed.

## What R5 actually establishes

- Author 40/40; exact R1/R2/R3 probes 15/15; provider 43/43 with exact AT07
  fixture; analytical composition 13/13.
- Actual AT10 I05 discovery + exact receipt builds an M1 disposition via the real
  discovery receipts/facts/queries/predicates; actual C1 discovery composition
  reaches the same N10E `EXACT_SUPPORTED`; wrong-predicate refusal and restore.
- Actual AT11 recursive handoff feeds MX01R2 C1 and the same learned consumer;
  handoff/parent lineage is returned; wrong-predicate refusal/restore.
- Actual joint query on the AT10 source gives target arity 2, distinct from two
  scalar slots.
- R4 direct two-slot coordinator/custody positive and typed status/Z16 fixes
  remain.

## Remaining productive defect

### R5-P1 — Coordinator/request cannot bind the actual native inputs used by the demonstrated discovery/recursive/joint routes

`NativeGraphSlot` fields are only:

```text
slot_id, source_universe_ref, release_ref, producer_query_ref,
producer_predicate_ref, consumer_query_ref, model_rule_hash, producer_route
```

Missing required High-decision associations include discovery result/receipt/
frontier, recursive handoff/lineage/root-parent, condition-value witness, target
arity/topology/order, M1 disposition, M2 release, B5 selection/currentness and
E41 input. `TrustedNativeGraphCoordinator.execute` source also has no discovery/
recursive/frontier/lineage/E41/M1/M2/B5/currentness binding; it trusts the
executor mapping to return a composition and retains only composition identity
material.

Independent probes (`probes/test_r05v_r5_coordinator_gap.py`):

```text
slot_fields: 14 required actual-input fields missing
coordinator_inputs: discovery, recursive, handoff, lineage, frontier, E41,
  M1, M2, B5, currentness terms absent
actual_discovery_recursive_use_trusted_coordinator:
  both R5 actual tests use raw evaluate_learned_world_consumer with no
  trusted_graph_reader
actual_source_sever_and_e41_route:
  discovery/recursive tests have no actual source/evidence sever and no E41
  extension route; only wrong predicate/ref
```

Thus the R5 actual discovery/recursive/joint consumer assertions are raw
compatibility-path claims, not the coordinator-owned full-graph custody required
by the High decision. The request cannot fix the actual native inputs, and the
coordinator original does not include them.

### R5-P2 — Actual source/evidence sever and E41 discovery/recursive route are unproven

R5 tests change only the requested predicate/ref, not actual source/native
evidence or a required upstream dependency; they do not exercise an E41
discovery/recursive result/receipt/route on those actual routes. The High
decision explicitly says wrong requested predicate/ref alone is insufficient and
requires actual source/native evidence severance and E41 route reconciliation.

## Exact missing function

1. Extend `NativeGraphSlot`/`NativeGraphExecutionRequest` (authorized
   `pre553_learned_world_composition.py`) to bind the actual native input
   associations for each admitted route: discovery result + exact receipt +
   frontier, recursive handoff + lineage/root-parent, condition-value witness,
   target arity/topology/order, M1 disposition, M2 release, B5 selection/
   currentness and E41 input/result identity.
2. Make `TrustedNativeGraphCoordinator.execute` execute the actual C1/E41/native
   owners from those admitted inputs, validate/capture before pinning, retain the
   complete original native input/output graph, and expose it through the fixed
   trusted reader. The actual discovery/recursive/joint positives must use this
   coordinator, not the raw compatibility path.
3. Demonstrate actual source/native evidence change and severed required upstream
   dependency changing/refusing the SAME consumer with exact restore, and an
   actual E41 discovery/recursive route/receipt reconciliation.

No new authority, evaluator, provider, signer/service or scientific aggregation
is required. The actual AT10/AT11 linkage itself is a genuine partial capability;
only the coordinator/input-association and source/E41 qualification are missing.

## Limits

Full live J42/P41/E04 remains NOT_REACHED; R04 independent. No original source/
science, F6/F7/FieldForge, CI/prod, N11/N12, Sorok, J52/W52 or adoption. The
local trusted-coordinator assumption remains explicit; no OS/R09 protection.
No candidate edit, self-adoption or author wake.

Artifacts: `EXPECTATIONS.md`, `defects.md`, `limits.md`, `RESUME.md`,
`proof_witness.json`, `SHA256manifest.json`, `outcomes/r05v_r5_observations.json`,
`probes/test_r05v_r5_coordinator_gap.py`, R1/R2/R3 probe copies, `junit/*.xml`,
`logs/stdout.jsonl`.
