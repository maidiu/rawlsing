# COMMANDS AND LOGS — distinct independent C

All commands were run from
`/Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/INDEPENDENT_C`
unless noted. Product, protected PROGRAMMA, candidate and specialist trees were
read-only. Temporary test data was kept under this review root via
`--basetemp`.

## Ref / tag / status

```
git rev-parse HEAD
git rev-parse anvil-architecture-candidate-20261117-r1^{tag}
git rev-parse anvil-architecture-candidate-20261117-r1^{}
git ls-remote origin refs/heads/agent/anvil-integrated-architecture-20261117-r1 \
  refs/tags/anvil-architecture-candidate-20261117-r1
git status --porcelain
```

Log: `RUNS/refs_and_status.txt`.

## Candidate manifest

```
python3 - <<'PY'
# read PACKAGE_MANIFEST.json; hash every listed file; compare sha256/bytes
PY
```

Result: 61/61 match, 0 missing, 0 unlisted. Log: `RUNS/refs_and_status.txt`.

## Frame / inventory / source rows

```
python3 - <<'PY'
# count S1/FRAME.json requirements, FRAME_V2_ADDENDUM new_requirements,
# SOURCE_IDENTITY_INVENTORY entries/counts
PY
awk -F'\t' 'NR>1{print $1}' S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv | sort | uniq -c
wc -l SOURCE_118/K3_CAP_29.tsv SOURCE_118/K3_PC_26.tsv SOURCE_118/K3_P4R_14.tsv
```

Result: 16 base / 4 v2 / 118 identities; crosswalk 141 rows
(118 identity + 16 requirement + 4 addendum + 3 separate). Log:
`RUNS/frame_counts.txt`.

## Focused sourcefree tests (existing product code)

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  rawlsing_next/tests/test_pre553_prepared_saved_i03.py \
  rawlsing_next/tests/test_pre553_direct_estate_i03.py \
  rawlsing_next/tests/test_pyat997_s1e_saved_native_first_consumer.py \
  --basetemp=WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/TMP/focused
```

Result: 34 passed in 18.59s. Log: `RUNS/focused_sourcefree_tests.txt`.
This is sourcefree existing-code execution, not native/100k/science/H1.

## Bounded ABI witness (new test in this review root only)

```
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/WITNESS/test_prepared_abi.py \
  --basetemp=WORKER_RETURNS/ANVIL_ARCHITECTURE_C_20261117/TMP
```

Result: 2 passed in 2.24s; both assert the candidate's
`PreparedSavedC11Admission` is rejected by the named `execute_saved_i03` and
`BatchExecutionRunner` exact-type guards. Log: `RUNS/prepared_abi_witness.txt`.
This proves the ABI gap, not a failure of a correctly wired prepared Batch path.

## Structural guard and its v2 omission

Guard on the unmodified final decision (accepted instrument tool, read-only):

```
cd /Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/ACCEPTED_INSTRUMENT/ANVIL_R7/tools
PYTHONDONTWRITEBYTECODE=1 python3 r7_integrated.py DECISION \
  .../INDEPENDENT_C/WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117/S2_S3/FINAL_DECISION.json \
  --evidence-root .../INDEPENDENT_C/WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117 \
  --source-root .../INDEPENDENT_C/WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117/SOURCE_118 \
  --repo /Users/matthewsmith/s2b-work/rawlsing \
  --zip /Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip
```

Result: `PASS_LOCAL_INTEGRATED_DECISION_PENDING_C`, covered 16,
requirement_total 16, identity_dispositions 118. Log:
`RUNS/decision_consistency.txt`.

The same guard was then run on a copy in this review root with
`candidate_requirement_addendum_dispositions` and `frame_v2_addendum` removed:

```
WITNESS/FINAL_DECISION_without_v2_addendum.json
```

Result: the same PASS 16/16/118. Log:
`RUNS/guard_omission_witness.txt`. This is the counterexample: the guard cannot
detect omission of the four v2 requirements.

## Decision consistency observations

```
python3 - <<'PY'
# print specialist_dependency.status, specialist_consumption.status,
# physical_architecture.name, implementation_sequence, selected effects
PY
```

Result: `specialist_dependency.status = PENDING_TWO_FROZEN_SPECIALIST_RETURNS`
while `specialist_consumption.status =
BOTH_RETURNS_RECEIVED_AND_ADJUDICATED`; `physical_architecture.name` is the
SC-ESTATE with derived index; `implementation_sequence[4]` adds the index
unconditionally. Log: `RUNS/decision_consistency.txt`.

## Scope / no-product-edit checks

`git status --porcelain` outside this review root was empty. No product file,
schema, evaluator, protected PROGRAMMA, candidate or specialist tree was
modified. No native/100k/6 GiB benchmark, no install, no raw respondent read,
no protected merge, no H1.
