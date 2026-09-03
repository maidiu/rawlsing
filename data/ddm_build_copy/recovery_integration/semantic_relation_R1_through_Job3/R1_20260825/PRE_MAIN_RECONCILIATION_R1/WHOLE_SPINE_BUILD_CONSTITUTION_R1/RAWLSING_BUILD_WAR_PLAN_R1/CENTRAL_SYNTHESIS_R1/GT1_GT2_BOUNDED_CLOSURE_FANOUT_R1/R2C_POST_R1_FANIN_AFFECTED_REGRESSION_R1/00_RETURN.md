# GT12 R2C — POST-R1 FAN-IN AFFECTED REGRESSION R1

## Terminal

`PASS__GT12_R2C_POST_R1_FANIN_AFFECTED_REGRESSION_GREEN__E3_01_STILL_OPEN`

## Exact candidate

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-gt12-r2c-post-fanin-regression-r1`
- exact starting/candidate SHA: `57a062fb262336764f4db2d7e19819b4a954db14`
- candidate verified before execution: YES
- Library used: NO
- governed source/respondent materialization: NO
- genuine-data GT2 rerun: NO
- production code modified: NO
- E2B: NOT PERFORMED
- final hostile audit: NOT PERFORMED
- GT1/GT2 adoption: NOT ISSUED
- PRE-MAIN / main moved: NO

The candidate deliberately contains R1B, R1C disposition documentation, E1 fixture corrections/regression evidence, and E2A return/transport evidence. It deliberately does not contain an R1A M1->M4 permission-binding repair.

Therefore E3-01 remains open.

## Execution environment

Ordinary GitHub Actions execution was used through a temporary side-branch harness that explicitly checked out the immutable candidate SHA. The harness was not placed on the worker branch and was removed from the side-branch tree after the run.

GitHub Actions run: `33808886910`

Job: `100825804497`

Environment:

- GitHub-hosted runner
- Ubuntu 24.04.4 LTS
- runner image: `ubuntu-24.04`
- runner image version: `20260831.293.1`
- Azure region: `southcentralus`
- kernel: `Linux 6.17.0-1022-azure`
- architecture: `x86_64`
- git: `2.55.0`
- CPython: `3.11.16`
- pytest: `9.1.1`
- repository checkout: detached exact SHA `57a062fb262336764f4db2d7e19819b4a954db14`
- pre-test `git status --short`: clean / no output

Only pytest and its ordinary Python dependencies were installed for this bounded court. No source-data dependency was required by the selected suite.

## Exact tests invoked

```sh
python -m pytest -q \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_pre553_replay_audit.py \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc_gt0_protocol.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wsc_gt0_end_to_end_integrated.py \
  rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py
```

## Result

- passed: **222**
- failed: **0**
- collection errors: **0**
- pytest exit code: **0**
- pytest summary time: **0.78 s**

The bounded set exposed no broader coupling, so Closure-D's larger exact regression court was not re-run.

## E3-02 explicit hostile verification

At the current production surface:

`POSITIVE_RELATION_STATES == frozenset({"SUPPORTED"})`

Production maps:

`OBSERVED_ZERO -> UNRESOLVED`

before the later negative/blocker-ref check.

The directly bound hostile test constructs:

- `relation_typed_state="OBSERVED_ZERO"`
- `relation_negative_or_limit_refs=()`

and verifies that the result is:

- decision: `UNRESOLVED`
- reason: `UPSTREAM_RELATION_OBSERVED_ZERO`
- target-use permissions: `()`
- never `ADMITTED`

The C->D hostile test also begins from a real C-side `OBSERVED_ZERO` relation, strips the blocker refs from the bridged evidence, and again verifies the exact same fail-closed result.

Typed-state tamper resistance also remains live: mutating a C relation's typed state changes its semantic projection hash and the bridge rejects the object for exact hash mismatch.

Disposition:

`E3_02_CLOSED_AND_REGRESSION_GREEN`

## Proven green at the affected grain

- R1B `OBSERVED_ZERO` conservation: GREEN.
- blocker-stripping resistance: GREEN.
- typed-state tamper resistance: GREEN.
- E1 replay fixture compatibility: GREEN. The previously banked E1 test refresh is present; replay fixtures patch the current `_candidate_projection_semantic_hash` helper and retain the same exact source/hash/authority/replay assertions.
- E1 V3 leakage sentinel: GREEN. It rejects actual `V3_` / `ACTOR_` semantic keys and V3/actor authority namespaces without falsely rejecting lawful `PREV3_` identities.
- C->D ownership/identity preservation: GREEN. The exact relation ref and FIELD FORGE semantic owner survive admission without reownership, with exact lineage/dependency closure preserved.
- relation-M1 route executability at its existing bounded grain: GREEN.
- V3 zero-positive guard: GREEN and inert. The authoritative guard binding remains `IG_PSEPF_ZERO_POSITIVE_GUARD / ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE@1`, the default accepted positive-transition authority registry is empty, outcome is zero-effect denial, and before/after state is identical.
- M1 admitted FIELD FORGE relation ingress sentinel: GREEN.
- M4 V557/V558 publication/repository sentinel: GREEN.
- current GT1/GT2 positive PRE-V3 integration sentinel: GREEN.

## Fixture status

No fixture correction was required in R2C.

The candidate already contains the separately banked E1 test-only corrections to:

- `rawlsing_next/tests/test_pre553_replay_audit.py`
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py`

Those corrected fixtures passed unchanged in this run.

## E3-01 remains explicitly unresolved

`E3-01 upstream->M4 permission translation/binding` is NOT proven or repaired by this regression.

The passing relation-M1/M4 route test manually supplies:

`producer_allowed_uses=("REVIEW",)`

That proves only that the already bounded route remains executable when an allowed-use set is supplied. It does **not** prove that `REVIEW` lawfully descends from the exact upstream FIELD FORGE/PRE-V3 permission object, and it must not be narrated as such.

No permission translation was invented or adopted here.

Disposition:

`E3_01_STILL_OPEN__NO_UPSTREAM_PERMISSION_DESCENT_PROVEN`

## Terminal

`PASS__GT12_R2C_POST_R1_FANIN_AFFECTED_REGRESSION_GREEN__E3_01_STILL_OPEN`
