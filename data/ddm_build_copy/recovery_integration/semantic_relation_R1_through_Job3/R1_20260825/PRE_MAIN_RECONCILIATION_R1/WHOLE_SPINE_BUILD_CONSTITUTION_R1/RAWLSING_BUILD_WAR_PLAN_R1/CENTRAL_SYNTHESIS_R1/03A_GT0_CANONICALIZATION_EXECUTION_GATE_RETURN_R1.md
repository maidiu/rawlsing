# GT0 CANONICALIZATION REAL-CHECKOUT EXECUTION GATE RETURN R1

## Terminal

`PASS__GT0_CANONICALIZATION_REAL_CHECKOUT_EXECUTION_GATE__214_PASSED__NO_CANDIDATE_CAUSED_IMPORT_TYPE_SIGNATURE_FAILURE__READY_FOR_SEPARATE_CANONICALIZATION_ACT`

Candidate SHA executed:

`ed1482517e0eebe2228e838dc6a24b97db879fc9`

Instruction/evidence ref:

`3454b15ff7ef388f6e028f78fad4e229c9aa969f`

Gate instruction:

`CENTRAL_SYNTHESIS_R1/03_GT0_CANONICALIZATION_EXECUTION_GATE.md`

This was execution only. No semantic rereview, redesign, FIELD FORGE R2 reopening, PRE-MAIN movement, or `main` movement was performed.

## Real checkout execution

A temporary execution-only GitHub Actions branch was created solely to obtain a full authenticated repository checkout. The workflow itself explicitly checked out the candidate SHA, not the temporary workflow commit:

```text
actions/checkout@v4
ref: ed1482517e0eebe2228e838dc6a24b97db879fc9
fetch-depth: 1
```

Runner log confirms:

```text
git fetch --no-tags --prune --no-recurse-submodules --depth=1 origin ed1482517e0eebe2228e838dc6a24b97db879fc9
git checkout --progress --force ed1482517e0eebe2228e838dc6a24b97db879fc9
Updating files: 100% (4106/4106), done.
HEAD is now at ed14825 WSC002R: bank bounded repair integration return
git log -1 --format=%H
ed1482517e0eebe2228e838dc6a24b97db879fc9
```

GitHub Actions run:

`33692285640`

Job:

`100453454544`

## Environment identity

```text
Runner version: 2.337.0
Runner image: ubuntu-24.04
Runner image version: 20260823.283.1
Operating system: Ubuntu 24.04.4 LTS
Kernel: Linux 6.17.0-1022-azure x86_64
Git: 2.55.0
Python: 3.12.3
pip: 24.0
pytest: 9.1.1
```

## Exact pytest command

```bash
python3 -m pytest -q \
  rawlsing_next/tests/test_wsc_gt0_protocol.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc002r_c_m6_render_authoritative_binding.py \
  rawlsing_next/tests/test_pre553_structural_admission.py \
  rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_m6_actor_safe_expression.py \
  rawlsing_next/tests/test_render_bounded_expression.py
```

Before pytest, the job asserted:

```bash
test "$(git rev-parse HEAD)" = "ed1482517e0eebe2228e838dc6a24b97db879fc9"
```

## Result

Exact terminal pytest output:

```text
........................................................................ [ 33%]
........................................................................ [ 67%]
......................................................................   [100%]
214 passed in 0.82s
```

All required focused GT0 protocol/bridge/integrated tests passed.

All three WSC002R repair regressions passed.

The smallest directly relevant inherited regression files for:

- PRE553 structural admission;
- M1 temporal/V554 admission-dedup;
- V3 PSEPF zero-positive guard;
- M6 actor-safe expression;
- bounded rendering;

all passed in the same real checkout and same pytest process.

No candidate-caused import failure, runtime type mismatch, signature mismatch, or repair-requiring failure occurred.

No additional broad test campaign was required.

## Disposition

The execution-only gate is closed PASS at the audited GT0 grain.

`NEXT_ACTION__SEPARATE_CENTRAL_CANONICALIZATION_ADOPTION_ACT_MAY_PROCEED_FOR_GT0_AT_EXACT_CANDIDATE_ed1482517e0eebe2228e838dc6a24b97db879fc9__THIS_WORKER_DOES_NOT_MOVE_PRE_MAIN_OR_MAIN`
