# SOROK P6 evidence-only assembly index

**Frozen runtime:** `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`.
**Assembly branch:** `codex/sorok-p6-proof-assembly-20261107-r1`.
**Scope:** evidence-only patch for selective integration into existing draft #779.
No runtime, shared progress, protected state, PR779 branch, or other program is
changed. PR779 author remains the sole runtime writer.

## Four proof sources, commands, actual results

| Proof | Exact source commit | Command (repository root) | Actual result |
|---|---|---|---|
| Gaze counterfactual | `a075232f56b55bcce138df755db20e77e3ec5f3c` | `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py` | `1 passed in 100.19s` |
| History order / unpursued detail | `cdf3a5bcf4838feead2783a95f613e045133748c` | `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py` | `1 passed in 203.37s` |
| Chronology reject/restore | `9657a7b65da56c3e0ef6ec7f0538ac2aebc023f6` | `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py` | `1 passed in 111.09s` |
| Actor boundary / private gaze | `86ad63006efd2682ada94ff4f0a806eebee36f1c` | `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py` | `1 passed in 31.23s` |

The proof files under those four directories are exact tree contents from the
listed source commits. Generated caches are not included.

## One-command all-four rerun

Collection across all four tests in one invocation succeeds; no proof-local
import fix was required (`4 tests collected in 0.10s`).

```sh
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py \
  WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py \
  WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py \
  WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py
```

```text
4 passed in 419.26s
exit status 0
```

## Cold demo evidence

Included exactly from `96a2e4fc1b0afba8260c87be30f61c7aad3c11da`:
`WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1`.

- The checked-in recording is the exact 13-record frozen-`41b21babf` transcript
  from original run head `5adcb372cfacea1281fe1a69f972a55bf0752992`.
- Recorded byte hashes: `TRANSCRIPT.md`
  `11da7a804aa3603997716794802ac4a65a90f490b3a6eea6a3151f0499496493`;
  `actual_run.jsonl`
  `7421fc2bd9dba4e08e3c00f39ec4943441d1eeb5e32101673e98b4f080924ae4`;
  `house_history.json`
  `87ca6dd35cdf29a5d97598f5bce855b27313ab12b0d45d95332795c7f4336e53`.
- Its focused fresh-output routing validation passed: default fresh temp output,
  protected evidence directory refused, pre-populated dirs refused, one-command
  routing exited `0`, `new` 9.23s and helper 2.90s; checked-in files remained
  byte-identical.
- **No full demo replay was run**; the 13-command recording is reused unchanged.
  Full replay waits for the integrated recognition head.

## Exact diff-path list versus frozen `41b21babf`

```text
WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/00_RETURN.md
WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/PROGRAMMA_DELTA.json
WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/run.log
WORKER_RETURNS/SOROK-P6-ACTOR-BOUNDARY-PROOF-20261107-R1/test_p6_actor_boundary_proof.py
WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/00_RETURN.md
WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/PROGRAMMA_DELTA.json
WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/run.log
WORKER_RETURNS/SOROK-P6-CHRONOLOGY-PROOF-20261107-R1/test_p6_chronology_proof.py
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/README.md
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/TRANSCRIPT.md
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/actual_run.jsonl
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/house_history.json
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/inspect_state.py
WORKER_RETURNS/SOROK-P6-COLD-DEMO-20261107-R1/run_demo.py
WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/00_RETURN.md
WORKER_RETURNS/SOROK-P6-GAZE-PROOF-20261107-R1/test_gaze_proof.py
WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/00_RETURN.md
WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py
WORKER_RETURNS/SOROK-P6-PROOF-ASSEMBLY-20261107-R1/00_RETURN.md
```

Runtime identity check versus `41b21babf`:

```sh
git diff --exit-code 41b21babf72c4c8b0b4b012d3c8b7d7f6247791f -- \
  rawlsing_next WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1 \
  WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1 \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1 \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1
# exit 0; runtime tree identical
```

## Boundary

Evidence-only; no merge/approval claim. Recognition fix and the actual cold demo
are separate active lanes for final joined acceptance; the demo is included as
recorded evidence only. P5/P6 remain unreceived candidates. No new framework,
native/scientific/human claim, or approval is made.
