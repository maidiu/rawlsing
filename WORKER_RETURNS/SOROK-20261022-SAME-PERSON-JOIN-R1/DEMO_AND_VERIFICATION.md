# JOIN-E runnable demo and verification

**Grade:** `TEST_ONLY_SOURCEFREE__NOT_NATIVE`.
No external model, provider, human participant, native CAN/ADP/C8/Pyat/C11/C12 grant or production service is used.

## 1. CLI demo

From the repository root:

```sh
cd ~/Desktop/Rawlsing/rawlsing-join-e
export PYTHONPATH="$PWD/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"
export PYTHONDONTWRITEBYTECODE=1
STATE=/tmp/join-e-demo

python3 -B -m joined.cli start --state "$STATE" --perform omit
python3 -B -m joined.cli say --state "$STATE" "Hello. I just moved in."
python3 -B -m joined.cli help --state "$STATE"
python3 -B -m joined.cli contact --state "$STATE"
python3 -B -m joined.cli attend --state "$STATE"
python3 -B -m joined.cli wait --state "$STATE" --hours 30
python3 -B -m joined.cli leave --state "$STATE"
python3 -B -m joined.cli offscreen --state "$STATE" --hours 30
python3 -B -m joined.cli messages --state "$STATE"
python3 -B -m joined.cli return --state "$STATE"
python3 -B -m joined.cli status --state "$STATE"
python3 -B -m joined.cli verify --state "$STATE"
```

`--perform omit` preserves A's tool, so E admits help; `--perform e2` performs J's material inspection first, exhausts the tool, and E refuses help. The difference is the actual persisted actor state, not a pressed/free-hours patch or the `SHARE_TOOL` label.

`verify` returns both the branch and root C12 verification plus the actual module-origin audit and the 444-file vendored-manifest summary.

## 2. Focused tests

New join tests:

```sh
cd ~/Desktop/Rawlsing/rawlsing-join-e
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests \
  -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/evidence/junit/join_new.xml
```

Expected: `18 passed`.

Frozen J test in its own process:

```sh
cd WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j
PYTHONPATH="$PWD:$PWD/r29m/source:$PWD/candidate:$PWD/candidate/vendor/bp2:$PWD/candidate/vendor/bp4:$PWD/r29p:$PWD/r26e:$PWD/n1:$PWD/../.." \
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_r31j.py \
  -p no:cacheprovider --junitxml=../../evidence/junit/j_r31j.xml
```

Expected: `8 passed`.

Frozen E expression test in its own process:

```sh
cd WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/e
PYTHONPATH="$PWD:$PWD/vendor/r30a:$PWD/vendor/r30a/vendor/r29p:$PWD/vendor/r30a/vendor/r29p/candidate:$PWD/vendor/r30a/vendor/r29p/candidate/vendor/bp2:$PWD/vendor/r30a/vendor/r29p/candidate/vendor/bp4:$PWD/vendor/r30a/vendor/r29p/r26e:$PWD/../..:$PWD/../../.." \
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_r31e_expression.py \
  -p no:cacheprovider --junitxml=../../evidence/junit/e_expression.xml
```

Expected: `15 passed`.

Frozen R30A baseline in its own process:

```sh
cd WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/e/vendor/r30a
PYTHONPATH="$PWD:$PWD/vendor/r29p:$PWD/vendor/r29p/candidate:$PWD/vendor/r29p/candidate/vendor/bp2:$PWD/vendor/r29p/candidate/vendor/bp4:$PWD/vendor/r29p/r26e:$PWD/../../../../.." \
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_r30a_first_session.py \
  -p no:cacheprovider --junitxml=../../../../evidence/junit/e_r30a.xml
```

Expected: `10 passed`.

These are 51 owned executed entries (18 join + 8 J + 15 E + 10 R30A). They do not establish a clean union with the historical 202/30 claims, and the full inherited suites were not rerun by this join.

## 3. Proof-integrity witness

The shared checker is not vendored on this branch. Use the exact PRE-MAIN law file at
`1abd6c6a613a5aaf78fe535b22c82e0ff10a1816:CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py`:

```sh
git show 1abd6c6a613a5aaf78fe535b22c82e0ff10a1816:CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py \
  > /tmp/proof_integrity_gate_r1.py
python3 /tmp/proof_integrity_gate_r1.py witness \
  WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/tests/test_join.py.proof.json \
  --root . \
  --receipt WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/evidence/proof_witness.json
```

Expected: baseline `PASS`, `fault_probe` `TARGET_ASSERTION_FAILED`, grade `BOUNDED_MUTATION_DETECTED`.
The first mutation changes the join implementation's `omit` path to perform E2 anyway. The second changes the targetless refusal seed to retain a tool despite B `REFUSE_TOOL`. Both named tests fail by assertion, not by import or build error. The B claim is bounded receiving-edge evidence, not original upstream B pre-C8 severance.

## 4. Expected result

A sourcefree first encounter that is materially conditioned by J's persisted C8/C9/E2 state and admitted through E before the user lens. Native C12/C11 and human A5 remain `NOT_RUN` / `HOLD`.


## 5. Independent JOIN-V frozen suite

The repaired candidate was tested against JOIN-V's frozen tests without editing them:

```sh
cd /path/to/JOIN-V-return
SOROK_JOIN_CANDIDATE_ROOT=/path/to/SOROK-20261022-SAME-PERSON-JOIN-R1 PYTHONPATH="$PWD/tests" PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py tests/test_join_v_hostile.py   -p no:cacheprovider
```

Actual: `30 passed` (10 positive + 7 hostile + 9 repaired-cut + 4 targetless-final) plus `5 passed` lineage-contract. Receipts: `evidence/junit/v_all_30.xml`, `evidence/junit/v_lineage_contract.xml`. The older targeted final-cut suite is 5 pass / 1 superseded E-first-refusal expectation (`evidence/junit/v_final_cut.xml`).
The independent reviewer still owns the final verdict; this is a frozen-suite execution result, not self-adoption.
