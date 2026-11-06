# PYAT R53 P53T — NATIVE SOURCE-FREE FALSIFICATION — RETURN AND ASTRA FIRST READ

**Status:** COMPLETE_SCOPED_INVESTIGATION__ENGINEERING_RED_WITNESSES_REPRODUCED__NO_PRODUCTION_ADOPTION
**Branch:** `agent/rabochii-pyat-r53-p53t-native-sourcefree-defect-reproduction-r1`
**Startup:** `f6fd6cdfebe8f0d76a3aa0e2de150065f261709d`
**Runtime:** Python 3.11.3, pytest 9.0.2, macOS 13.2.1 x86_64
**Authority intake:** B53R R2 `39a06929f8ecc58f9854e156dcd04c32bc9a5ce3`; B53H R2 `026a6ba3075817b7f0370619843ee7227967bc8e`; U53A partial `9df2c40e51cefbff1f68dedf85556c9b0e326d3f`; U53F forensic `fdc4d03537e649cd56c19a458ebeb3292298ff3f`. Worker opinions are kept separate from observed executions.
**Isolation:** own worktree `/Users/matthewsmith/Desktop/Rawlsing/R53-P53T-native-sourcefree-wt`; no production or worker source edited; synthetic fixtures only; no SAV/DTA, original35, network source, actor, model, or scientific issuance.

## Astra first read

The two highest-impact allegations are actual, not static paragraphs:

1. **G50 arbitrary item IDs:** unchanged `g50/enumerate.py` blob `f610ef2dea39519a51a5b57fd35bbe245fb9dc9b` raises `KeyError('ID')` at `enumerate.py:151` from the unconditional literal insert at `enumerate.py:193` for a valid COMPLETE bundle containing only non-reserved item IDs. With `ID` present but `Y` absent it raises `KeyError('Y')` at line 194. This is direct execution of the frozen G50 module, not the full B49→G50→I05 engine.
2. **J42 requested-condition identity:** unchanged `E41ProviderAdapter.step()` at blob `40f1e9f69fafff37f6bc44474b0189543d4997b3` returns the real E41 `Y|(A=1)` slice for a request `Y|(C=1)`; `P41Service.progressive()` then emits `query.ordered_conditions=[["C",1]]` and `query_identity_hash` naming C while `n10e_steps[0].conditioners=[["A",1]]` and `evidence_ref` name A. Unchanged E04 `product/nonparent.consume` emits `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED`.

## Confirmed actual source-free witnesses

| Case | Observed | Grade |
|---|---|---|
| G50 arbitrary IDs | `KeyError('ID')`; all eligible work lost | `REPRODUCED_NATIVE_SOURCEFREE__G50_MODULE_BOUNDARY` |
| G50 `administered=False` on Y | Y still `ELIGIBLE`; `e_pre_count=432` unchanged | `REPRODUCED_NATIVE_SOURCEFREE__G50_MODULE_BOUNDARY` |
| G50 all-missing administered / held Y | Same eligibility as unadministered; no missingness gate | `REPRODUCED_NATIVE_SOURCEFREE__G50_MODULE_BOUNDARY` |
| G50 duplicate Y identity | Silent last-wins; DIST(Y) unit becomes `household`; eligible count `432→114`; `u_item_root` still includes both | `REPRODUCED_NATIVE_SOURCEFREE__G50_MODULE_BOUNDARY` |
| G50 Y vs Z conditioner | Y prohibited `REVERSE_ROLE_RISK_NOT_AUTHORIZED`; identical Z eligible; policy has no `reverse_authorized` field | `REPRODUCED_NATIVE_SOURCEFREE__G50_MODULE_BOUNDARY` |
| J42/P41 C-vs-A | Request C names C but dereferences A evidence/denominator 32; `Y|(A=0)` also returns A=1 | `REPRODUCED_NATIVE_SOURCEFREE__FRESH_E41_AND_PINNED_CONSUMERS` |
| J42/E04 zero-support step | Empirical step `ZERO_SUPPORT`; J42 aggregate `PRODUCTIVE_TEST_ONLY`; E04 `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` | `REPRODUCED_NATIVE_SOURCEFREE__PINNED_J42_E04` |
| P41 ROUTING_UNKNOWN | `progressive_chain_state=TYPED_PARTIAL_OR_UNKNOWN` but `unknown.evidence_state=EXACT_SUPPORT_ON_CONDITIONED_RISK_SET` | `REPRODUCED_NATIVE_SOURCEFREE__PINNED_P41` |
| J42 absent structural state | Defaults to `SUPPORTED_TEST_ONLY`; E04 route ELIGIBLE and top-level success | `REPRODUCED_NATIVE_SOURCEFREE__PINNED_J42_E04` |
| U43 discovery ingress | Same issued discovery ref enters `execute_route_b_production` and later `execute_i05` in Batch | `REPRODUCED_ISOLATED_HELPER__MOCKED_U43_OWNERS` |
| B53H R2 prefilter | 8 published controls pass; self-asserted native booleans, trace IDs, and consumer events pass; caller can self-pin a forged policy | `REPRODUCED_ISOLATED_HELPER__STRUCTURAL_PREFILTER_ONLY` |

## Confirmed positives / non-regressions

- Stock G50 fixture enumerates successfully: 432 eligible, 248 prohibited, 4 deferred, 3 unresolved, 3 unsupported-runtime.
- Padded G50 fixture with reserved literals and renamed `Qa/Qb/Qy` enumerates and produces eligible Q operations; the main grammar is name-generic, the failure is in the explicit literal ledger.
- Fresh E41 driver produced real synthetic E04 slices: `Y/1` 32 `{0:14,1:18}`, `Y/2` 16 `{0:6,1:10}`, `Y/3` 8 `{0:2,1:6}`, `A/1` 29 `{0:11,1:18}`.
- Normal `Y|(A=1)` J42/P41 path binds A to A and succeeds; normal all-supported E04 produces the same named success without a negative step.
- Explicit `UNAVAILABLE_AUTHORITY_OR_CLOCK` structural state yields `PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT`.
- B53H R2 rejects output-operation swaps, roster omissions, policy-pin mismatch, false original zero, and missing I05 claims when the expected set is actually pinned.

## Falsified or limited allegations

- **Not falsified:** B53R R2 D8, D9, D10, D11, D12, D13, D14 all reproduced; the static diagnoses were directionally correct and understated the duplicate frontier collapse.
- **Falsified:** any claim that B53H R2's prefilter is a trusted evidence verifier or trusted native CI. It explicitly disclaims native/attestation validation, and a forged result with invented native booleans passes. Its structural anti-join is real but only as strong as an external protected policy and an authenticated runner result.
- **Falsified:** a blanket "J42 is broken" reading. The ordinary A/B/C supported path is coherent; the defect appears when requested condition identity/value differs from the stored depth slice, or when a step is non-supported.
- **Not established:** U43 duplicate surface is not proof of duplicate receipt, replay corruption, or data corruption. Only two call surfaces on the same discovery ref were observed with mocked owners.
- **Not established:** any original35, N11, source-right, scientific, FF/F6/F7, actor, J52/W52, or universal-execution status.

## NOT_RUN limitations

- Full B49→G50→U43→I05 native joined execution.
- Actual BatchExecutionRunner replay/receipt behavior for the U43 duplicate path.
- Full W41×E41×P41 84-view join and its sourcefree consumer matrix.
- Original35/source-licensed SAV/DTA measurement or E_pre acceptance.
- Original J52/W52 restart, repair, adoption, or production implementation.
- B53H protected CI, protected-ref policy, authenticated runner result, signature/attestation verification, or installed required workflow.

## Evidence

`tests/` contains 23 sourcefree tests; all pass because they assert the vulnerable current behavior or its positive control.
`receipts/` contains the full pytest JUnit/log, the eight published B53H controls, and the fresh E41 run.
`02_NATIVE_SOURCEFREE_REPRODUCTION_MATRIX.tsv` is the row-level matrix; documents 03–07 give the consumer and custody detail.
