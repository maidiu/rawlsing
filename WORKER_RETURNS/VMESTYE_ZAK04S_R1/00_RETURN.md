# ZAK-04S — Field Forge / R05 world authority execution attempt and bounded repair

**Commission:** user-selected ZAK-04S, November 14, 2026. **Mission:** real trusted R05→P41 baseline, forged FF STRUCTURAL (NEG-07), selected C→D→M1→V558 relation severance (NEG-08), restore, minimum correct repair if demonstrated.
**Grade:** `S1_SOURCE_REPAIR_AND_REPRODUCIBLE_TESTS_COMMITTED__S2_NOT_RUN`. **Terminal:** `ZAK04S_PARTIAL_WITH_EXACT_RUNNER_BLOCKER`.
**Protected source cut (GitHub verified):** `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`; unchanged by this PR.
**Author branch:** `agent/zak04s-ff-world-authority-20261114`. **Parent:** ZAK-04 R2 PR #901 HEAD `5789a8a5ef179966640490b9d03df96c34847385`, unchanged.

## 1. Governing contract and preserved capital

Source: user ZAK-04S commission; ZAK-00 flight matrix at `e725ec39d021f4f7d8080298a95ea519ada2de01`; ZAK-04 R2 `WORKER_RETURNS/VMESTYE_ZAK04_MCR_R1/00_RETURN.md` and `FALSE_PERMISSION_AND_ACTOR_NEGATIVES.md` at `5789a8a5ef179966640490b9d03df96c34847385`. Preserve: real pinned trusted P41 learned/source/root and actual consumer, ordinary sourcefree `STRUCTURAL` reception, existing `CONTEXT` refusal, existing cross-unit/clock/currentness/receipt guards, FF CONTEXT custody and no FF/SOROK science promotion. This is MCR-lite engineering, not a rewritten ZAK-04 R2 or full-MCR-C closure.

Existing code:
- `rawlsing_next/pre553_universal_world_binding.py` original blob `fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d`: R05 trusted coordinator, P41 service and receipt checks are actual; original `_validate_ff_admission` only inspected `role=CONTEXT`.
- `rawlsing_next/tests/test_universal_world_binding.py` original blob `de921044f19a7ad31d4c5b49a390b6153f590933`: `_build_r05_learned_inprocess`, `_actual_execution_for`, `_r05_request` and `test_r06r2_actual_r05_learned_to_p41_world_with_synthetic_pair` constitute the real test fixture and owner path. These are inherited tests, not newly executed here.
- `rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py` lines 267–293 proves the upstream *test-defined* V558 relation permission ceiling is `producer_allowed_uses == ["CONTEXT"]`. It is **not** a selected R05 N9 STRUCTURAL grant.

## 2. Exact artifact, narrow changes and commands

Changed only world-owner code, its tests, the dedicated job and this return. The patch adds one fail-closed check at existing `_validate_ff_admission`: requests carrying FF authority, admission object, relation/field refs, transport ref or transport-authorized flag are rejected `R05_FF_ANCESTRY_NOT_TRUSTED` because no selected verified FF closure exists in R05's host-retained `R06TrustedExecutionContext`. It retains ordinary no-FF P41 STRUCTURAL and prior CONTEXT refusal. **It does not grant or revoke scientific/source authority.**

Files:
- `rawlsing_next/pre553_universal_world_binding.py` — new blob `217d8fe5bda7b662b3dbb052b7786533bee3c222`
- `rawlsing_next/tests/test_zak04s_ff_world_authority.py` — fixture/NEG-07 variants/unqualified reference swap/restore/CONTEXT/cross-unit/handle controls, blob `fb7d452f855ee7fb8e88af739248c0a7c0986714`
- `.github/workflows/zak04s-world-authority.yml` — actual test runner and adjacent existing regressions, blob `b3a2ef2ed151613c64192b7c676c65179c7885de`

Reproduce with a Python 3.11 runner from the repository root:

```bash
python -m pip install pytest pandas pyreadstat pyarrow duckdb
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python -m pytest rawlsing_next/tests/test_zak04s_ff_world_authority.py -q -s -o addopts=''
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python -m pytest rawlsing_next/tests/test_universal_world_binding.py -q -o addopts=''
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python -m pytest rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py::test_actual_c_relation_admits_without_reownership_and_is_lossless rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py::test_positive_relation_m1_derives_adopted_context_and_reaches_v558 -q -o addopts=''
```

## 3. Strongest achieved result vs unexecuted claims

- **Direct S1 source finding:** the original R05 world selector's FF guard inspected CONTEXT only; it did not use `ff_structural_authority_ref`, `ff_structural_admission`, `relation_transport_ref`, `relation_transport_authorized`, `R05WorldField.relation_ref`, or `R05WorldField.field_ref`. After this patch, those claims cannot be silently ignored and represented as a qualified FF world. This source-level difference is exact; a pre-repair runtime exploit is **not executed**.
- **Actual-path test fixture authored:** pulls a qualified learned object, creates a host-retained `R06TrustedExecutionContext` with a real `TrustedNativeGraphCoordinator`, executes R05's actual P41 service without a callback or canned receipt, and asserts source, release, rows, root, T0/T1 clocks, producer content hash and routes. Test *code* is present; its results are **NOT_RUN**.
- **NEG-07 authored:** eight authority/field/relation/transport variants, all with the same valid trusted handle and legitimate P41 source inputs; expects `R05_FF_ANCESTRY_NOT_TRUSTED` and baseline restore. NOT_RUN_S2.
- **NEG-08 not counterfeit:** the included unqualified relation-ref A/B/A swap deliberately asserts refusal, but is expressly **not** a selected admitted C→D→M1→V558 relation-severance success. Genuine NEG-08 requires a selected structural FF relation and trusted-world binding that do not exist in this source cut. NOT_RUN_S2.
- **Existing regressions scheduled:** P41 baseline/cold receipt, CONTEXT refusal, valid structural read, cross-unit refusal, trusted-handle mismatch; two upstream C→D and M1→V558 CONTEXT positives. None newly executed by this author.

## 4. Exact execution blocker (independently inspectable GitHub job metadata)

Pre-repair test-branch run `43631299272` and same-commit canonical `43631299228`: both concluded failure **without starting any step**. Each job has `runner_id=0`, `runner_name=""`, `steps=[]`, completion within approximately two seconds. No pytest, checkout, environment setup or source execution occurred.

Post-repair run `43631723693` and canonical `43631723708`: same absence of runner/steps. Subsequent `43631971133` and `43631971204`: also reported failure. GitHub workflow metadata and jobs show this is pre-step execution unavailability, **not a code-test failure and not a green test**. No local credentialed checkout is available to the author environment; git network lookup from the local container also fails. Running a fake callback or a rewritten P41 would be a false substitute. The next worker must obtain a runner that actually starts steps and retain JUnit/log/source SHA before promoting grades.

## 5. Own hostile findings, rejected alternatives and attack surface

1. **FF attribute laundering:** caller-supplied `STRUCTURAL` with unverified relation/field/authority labels previously reached only role-specific CONTEXT check; patch now rejects every declared FF claim until host source authority can validate it. A source-level short circuit is not yet an executed bypass proof.
2. **False-positive baseline risk:** an invalid P41 handle would make every attack fail before FF. The fixture uses the repo's actual trained learned consumer/coordinator and asserts a productive R05 world baseline before mutations.
3. **Meaningless severance risk:** altering arbitrary FF refs while native P41 world remains unchanged is not proof of causal FF dependence; A/B/A is explicitly diagnostic, **not** NEG-08 executed.
4. **Authority ceiling:** the existing test-defined GT12 V558 relation is CONTEXT only; upgrading it to STRUCTURAL for a green test would manufacture an issuer. Existing positive context behavior must remain available upstream.
5. **What may still break:** a future legitimate selected FF-to-world structural bridge would currently be rejected until an actual owner supplies verified host-retained lineage and first-reader semantics. The test shows ordinary valid P41 STRUCTURAL preservation only, not all hypothetical future FF-positive cases.
6. **Likely adversarial scrutiny:** source/role equality, forged `SimpleNamespace` admission, ref/hash substitution, transport boolean, role defaulting, unqualified field ID collision with a P41-owned rule, handle validation order, world receipt hash continuity, trusted-context registration and closure, and whether the first P41 reader ever actually consumes selected FF relations.

Rejected: blanket refusal of all `role=STRUCTURAL` (destroys valid P41 sourcefree behavior); accepting a positive-looking `ff_structural_admission` from the request (self-issued authority); merging FF `CONTEXT` into N9 as STRUCTURAL (permission widening); fake P41 receipts/callbacks (not actual reader); adding a new world engine or editing C11/PYAT source/SOROK actor ownership (outside mission).

## 6. Independent courts and honest terminal

- **Engineering:** S1 exact source inspection, minimal code repair, reproducible test/workflow committed; **S2 NOT_RUN** because no GitHub Actions job obtains a runner. No observed selected FF→world first-reader effect. Not COMPLETE_AT_EXECUTED_SCOPE.
- **Scientific:** no native original35/causal/temporal psychological issuer, no claim that conditioning proves social causality, no actual source-qualified FF STRUCTURAL grant. **NOT_ISSUED**.
- **Authority:** user-authorized isolated author branch and draft only; no independent same-HEAD review, no protected CAS, no S3, no human approval or whole-machine zero loss. **NOT_RECEIVED/NOT_MERGED**.

**Required future bounded action:** run the exact targeted fixture with an actual Python runner; inspect whether the baseline/negatives reach P41; if qualified FF STRUCTURAL issuance is selected by competent source/FF/world owners, pass its immutable admission/transport to a host-trusted R05 context and rerun a genuine selected C→D→M1→V558 A/B/A first-reader causal severance. Preserve the current CONTEXT ceiling until such issuance. No broad PROGRAMMA archaeology or recensus is necessary.

**Terminal:** `ZAK04S_PARTIAL_WITH_EXACT_RUNNER_BLOCKER`. No fabricated executed NEG-07/08, no invented independent acceptance.
