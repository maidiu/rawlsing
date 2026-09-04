# GT12 R3C POST-REPAIR INTEGRATED REGRESSION COURT R1 — RETURN

## Disposition

`PASS__GT12_R3C_POST_REPAIR_INTEGRATED_REGRESSION_GREEN__E3_01_E3_02_CLOSED`

This was an independent bounded regression court only. No production semantics were changed. No FIELD FORGE reopening, E2B, final hostile audit, GT1/GT2 adoption, PRE-MAIN movement, or main movement occurred.

## Exact candidate tested

`3ca5b1479e42cd8fc56de522b3f7bba9f5552edc`

The disposable GitHub Actions harness explicitly checked out this immutable SHA in detached-HEAD state and asserted `git rev-parse HEAD` equals the candidate before execution. The harness commit itself was not the candidate under test.

## Environment

- GitHub Actions hosted runner
- OS: Ubuntu 24.04.4 LTS
- runner image: `ubuntu-24.04`, image version `20260831.293.1`
- Git: 2.55.0
- CPython: 3.11.16
- pytest: 9.1.1
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`
- `PYTHONHASHSEED=0`

## Exact regression command

```bash
python -m pytest -q \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_pre553_replay_audit.py \
  rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py \
  rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py \
  rawlsing_next/tests/test_m4_v557_v558_publication_repository.py \
  rawlsing_next/tests/test_wsc002r_a_typed_negative_conservation.py \
  rawlsing_next/tests/test_psepf_zero_positive_guard.py \
  rawlsing_next/tests/test_wsc002r_b_v3_authoritative_guard_binding.py \
  rawlsing_next/tests/test_wsc_gt0_prev3_bridge.py \
  rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py
```

`test_wsc_gt0_prev3_bridge.py` is the relevant GT0 PRE-V3 protocol sentinel already included in the mandatory set. The D→M4 bridge suite directly imports the R3B permission-translation authority module, so no separate authority-import test file was required.

## Exact counts

- collected: 236
- passed: 236
- failed: 0
- skipped: 0
- execution result: success

No test-only fixture or harness correction was required: `NONE`.

## Explicit E3 seam assertions

A separate post-pytest assertion step executed against the same candidate and passed:

- `POSITIVE_RELATION_STATES == frozenset({"SUPPORTED"})`
- relation M4 helper signature contains no caller `producer_allowed_uses`
- adopted producer allowed uses are exactly `("CONTEXT",)`
- adopted V557 allowed uses are exactly `("CONTEXT",)`
- adopted V558 requested uses are exactly `("CONTEXT",)`
- adopted V557 state is exactly `ALLOW_CONTEXT_ONLY`
- translation authority semantic hash is exactly `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c`
- adoption receipt semantic hash is exactly `fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f`

The assertion step emitted `EXPLICIT_E3_ASSERTIONS_PASS`.

## Mandatory semantic assertion dispositions

1. **PASS** — positive PRE-V3 relation-state set is exactly `frozenset({"SUPPORTED"})`.
2. **PASS** — `OBSERVED_ZERO` remains nonpositive with blocker/negative refs stripped and cannot become `ADMITTED`.
3. **PASS** — typed-state tampering changes exact identity / fails closure authority checks.
4. **PASS** — relation-specific M4 helper does not accept caller `producer_allowed_uses`.
5. **PASS** — lawful positive GT2 derives exactly `("CONTEXT",)`.
6. **PASS** — `REVIEW` substitution is rejected.
7. **PASS** — `ACTIVE_CAUSAL` substitution is rejected.
8. **PASS** — larger use sets cannot be inferred from `ALLOW_CONTEXT_ONLY`.
9. **PASS** — wrong translation authority ID/version/hash fails closed.
10. **PASS** — wrong adoption receipt identity/hash fails closed.
11. **PASS** — PRE-V3 admission authority/rule/current-selection drift fails closed.
12. **PASS** — relation/risk-set/source/participant-order drift fails closed.
13. **PASS** — relation M1 remains exact SIG-004 / V554-only.
14. **PASS** — empirical-direct/I04/V553 substitution remains rejected.
15. **PASS** — no V555/V556 fabrication occurs.
16. **PASS** — CAN-003 monotone permission narrowing remains enforced after producer permission derivation.
17. **PASS** — CAN-004/V558 packaging and integrity behavior remains unchanged.
18. **PASS** — E1 replay fixture remains bound to the current semantic-hash helper.
19. **PASS** — E1 V3 leakage sentinel still distinguishes lawful `PREV3_` provenance from actual actor/V3 authority.
20. **PASS** — current GT1/GT2 integrated acceptance remains green.
21. **PASS** — successful GT2 V558 resolution conveys no comparator/PSEPF authority.
22. **PASS** — successful GT2 V558 resolution conveys no actor applicability or actor-state mutation.
23. **PASS** — authoritative V3 guard remains zero-positive-effect for GT2.

## E3 closure disposition

- E3-01 caller-minted relation producer permission: **CLOSED**.
- E3-02 `OBSERVED_ZERO` PRE-V3 positivity laundering: **CLOSED**.

The centrally integrated candidate preserved the directly bound GT1/GT2, PRE-V3, relation-M1, permission-descent, M4, and V3-zero-effect invariants required by R3C.

## Test-only correction

`NONE`

## Court terminal

`PASS__GT12_R3C_POST_REPAIR_INTEGRATED_REGRESSION_GREEN__E3_01_E3_02_CLOSED`
