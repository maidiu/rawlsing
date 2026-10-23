# R61-R01V R2 independent review — resume / reproduction

Branch: `agent/opencode-pyat-r61-r01v-r2-independent-review-r1`
Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01v-r2`
Candidate/startup: `f0c602eddaee14a58d6f0935a587a46fcf96c6db`
Candidate code: `d56e53301aaa0203e83fc1b60a0bcafb86b17892`
Verdict: **REVISE**; R03 remains NOT_STARTED.

All commands below are read-only against candidate/native code. Own artifacts
are written only under this directory.

## 1. Verify identity and allowlist

```sh
git ls-remote origin refs/heads/agent/opencode-pyat-r61-r01-generic-grammar-r1
git show --no-patch --format='%H %P %s' f0c602ed
git diff --name-only fcf9fe9f..f0c602ed
git diff --name-status fcf9fe9f..f0c602ed -- \
  WORKER_COMMISSIONS/PYAT-R61-GENERIC-REPAIR-FLIGHT-R1/INPUTS \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1 \
  WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/00_RETURN.md \
  WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/manifest.json
```

Expected: author remote `f0c602ed`; only four R01 allowlist code paths plus the
author R2 report root changed; immutable v1/reviewer/INPUTS diff empty.

## 2. Replay author suite with reviewer JUnit

```sh
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/replay/author_suite_junit.xml \
  -o addopts=''
```

Expected: exit 0, 18 passed.

## 3. Retained/adapted prior reviewer probes

```sh
PYTHONPATH="$PWD:$PWD/WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes" \
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes/prior_test_r01v_independent.py \
  -q -o addopts='' --junitxml=WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/replay/adapted_prior_probes_junit.xml
```

Expected: exit 0, 20 passed. Adaptations are limited to R2 behavior/path:
topology now lowers via catalog, forged direction now refuses, MULTI_SELECT_SET
is eligible at the frontier, and the cold helper REPO_ROOT is corrected.

## 4. Own hostile probes (3 expected defect failures)

```sh
PYTHONPATH="$PWD:$PWD/WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes" \
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 -B -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes/test_r01v_r2_reviewer.py \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/replay/own_probes_junit.xml
```

Expected: exit 1, 2 passed / 3 failed. The three failures are the required
contract assertions for A1 (conditional JOINT condition drop), A2 (forged op_id
accepted), A3 (unsupported-only declared empty).

## 5. Own native positive / mutation / restoration / cold

```sh
PYTHONPATH="$PWD:$PWD/WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes" \
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 -B -m pytest \
  WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/probes/test_r01v_r2_reviewer.py \
  -q -o addopts='' -k 'condition_mutation or cold_deterministic' -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-INDEPENDENT-REVIEW-R1/revisions/r2/replay/native_positive_junit.xml
```

Expected: exit 0, 2 passed. The test runs the real imported
`execute_exact_bounded_discovery`; the reviewer compiles expected candidates
from the current native owner/catalog, mutates a condition atom with the same
rule id, checks join failure, restores, and repeats in a cold subprocess.

## 6. Primary defect reproduction text

```sh
PYTHONPATH="$PWD" /usr/local/bin/python3 - <<'PY'
# see evidence/conditional_joint_repro.txt for the committed exact output;
# it selects an eligible SAMPLE JOINT on (q_alpha,q_beta) with one q_gamma
# condition and inspects lower_frontier(...).records[0].
PY
```

See `evidence/conditional_joint_repro.txt` and `evidence/recursion_diagnostic.txt`.

## 7. Boundary

This review does not repair or adopt the candidate. R03 remains blocked by A1
(conditioned JOINT/CO_TRAVEL semantic drop) until R01 is repaired and
independently requalified. A2–A4 should be fixed in the same R01 repair. No
original source/science, F6/F7/F8, N11/N12, production/CI, J52/W52 or Browser
runtime claim.
