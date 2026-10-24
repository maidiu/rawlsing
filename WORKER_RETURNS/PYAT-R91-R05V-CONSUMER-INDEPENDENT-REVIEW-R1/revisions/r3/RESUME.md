# R91 R05V R3 independent review — resume

State: complete; verdict **REVISE**. R3 fixes false-exact status and duplicate
definitions and adds a two-direct-component positive, but native graph provenance
and actual discovery/recursive linkage remain missing. No adoption.

## Custody

- Branch `agent/opencode-pyat-r91-r05v-r3-consumer-review-r1`;
  startup/HEAD `737f1b143963352f201973140002d6f66dbabcaa`.
- R3 contract `45cf09d55f80109114454d859aeb9b68ba6d2184`; code
  `0c416bed7fdae59cbb57a190d1ea215eae8de44a`; module blob `4e013062...`,
  test blob `b942370e...`.
- Frozen EXPECTATIONS `d6b4b3482fbc2863e3ddf4fb2ff1ff67b01c4fb1`.
- Accepted R08 `3ca860e4...`/`5832ce05...`; accepted C1/provider/evaluator/
  empirical owners unchanged.

## Evidence

- Author 37/37; R05V R1 exact 4/4; R2 exact 5/5; provider 43/43; C1 13/13.
- Independent R3 graph probes: 2 pass (two-direct positive, status disagreement),
  4 fail (forged joint topology, forged discovery route, forged recursive route,
  real-type E41 forged route).

## Missing function

Reconcile graph topology/joint count/order, discovery receipt/frontier,
recursive parent/handoff/lineage/root-parent, source/operation and currentness
with actual native owner objects/results; validate E41 route against the actual
component route/evidence; exercise a real materially different discovery/
recursive C1 linkage to the same learned disposition. If the linkage requires an
outside-five-path fixture/caller, name that exact dependency; do not echo
internally consistent invented labels.

## Commands

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r3/junit/author_r3_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r3/probes/test_r05v_r3_actual_graph_gap.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r3/junit/reviewer_r3_gap_probes.xml
```

## Boundaries

No candidate repair, adoption, author wake, new worker/session/provider/account.
Full J42/P41/E04 NOT_REACHED; source/science and all authority holds unchanged.
