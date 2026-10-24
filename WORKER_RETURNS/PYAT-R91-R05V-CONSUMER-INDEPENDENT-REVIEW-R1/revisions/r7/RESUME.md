# R91 R05V R7 independent review — resume

State: complete; verdict **REVISE**. R7 fixes executor-only originals, adds the
request-recorded learned M1/M2/B5 check, and moves actual joint/changed evidence
through the trusted coordinator. One residual admission-equality gap remains:
request-supplied actual fields (M1/M2/B5/currentness/topology/discovery/recursive/
E41/inputs) can rewrite the retained original while admitted native inputs run.

## Custody

- Branch `agent/opencode-pyat-r91-r05v-r7-consumer-review-r1`; startup/HEAD
  `65f7acf226b7b21a1a8f3be23f14a93b3f3cfbcc`.
- High decision `c618dc28...`; R7 contract `ce225f207...`; code `6fa02ff85...`;
  module `a1421201...`; test `b0114a82...`.
- Frozen EXPECTATIONS `7ea6e9ad1e1cbef0ed051c7a2f35ee37bde62b4a`.
- R4/R5/R6 pins and prior reviews preserved; R7 manifest 7/7.

## Evidence

- Author 40/40; prior probes 22/22; provider 43/43; C1 13/13.
- Independent R7 dynamic probe fails: forged request M1 `049214...` against
  admitted `83220c...` yields exact trusted support.

## Missing function

Require full actual association equality between request and admitted slot (or
build original/slot records solely from admitted slots); no request-supplied
M1/M2/B5/currentness/topology/discovery/recursive/E41/actual-input rewrite.
No new authority; full J42/P41/E04 NOT_REACHED; R04 independent.

## Commands

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r7/junit/author_r7_replay.xml

/usr/local/bin/python3 -m pytest -q \
  WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r7/probes/test_r05v_r7_request_association_gap.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05V-CONSUMER-INDEPENDENT-REVIEW-R1/revisions/r7/junit/reviewer_r7_gap_probes.xml
```

## Boundaries

No candidate repair, adoption, author wake, new worker/session/provider/account.
Full J42/P41/E04 NOT_REACHED; source/science and all authority holds unchanged.
