# Universal35 D r5 — independent two-defect closure

**VERDICT: REVISE** at frozen D head `cc0a0e39ef2d05cca3a92f045cec8830386cf647`.

- Code: `608be7780d0eee93a8e0d06aade4ff2f67081026`
- Prior input: `43d35eed654d2fc98ea0f176bf5c4bd92f524da1`
- Prior F review read: `f2d2bdea7e7c1073421bc8cdd3e3545aa0291a66`
- Actual D r5 return read: `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/05_R5_RETURN.md`
- Review branch: `codex/pyat-universal35-d-r5-review-20261106-r1`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Blocking — the post-consumer comparison is not the decision actually used for decode

`execute_native_compiler_source` captures an extra pre-call (`before_decision`, line 301), but `decode_with_source_read_permission` independently resolves its own pre-decode decision (line 302). The post-consumer check (line 332) compares against the extra call, not the decision used by the decoder.

A stateful resolver sequence `A, B, B, A` — A/B both `CURRENT_GRANTED`, B differing only in `decision_ref` — is accepted. The read is authorized under B, while the post-consumer equality only proves A == A. This fails the exact pre/post decision requirement for changed refs (and analogous metadata/scope changes that survive `_assert_current`).

Independent sourcefree production-wrapper probe: positive run 30 facts / 15 expected operations / 18 candidates, anti/op-anti true; changed post-consumer decision refused; the `A,B,B,A` resolver sequence **accepted** with the same 30/15/18 output.

The observation owner should capture the actual decision used by the admission call (or have the admission owner return it) and compare the post-consumer decision to that exact object. No code repair is made here.

### Held/unselected Y repair — PASS

The selected-frontier alias restriction closes the false `PHYSICAL_CODE_NOT_IN_BUNDLE:Y` failure without dropping eligible operations. The B suite's held-Y positive and selected-missing/full-plan partial refusal pass; the full sourcefree positive remains 15 expected operations (no eligible drop). Exact extra-frontier refusal remains from the prior accepted repair.

## GRADES / PROOFS

- **Postdecision exactness: FAIL.** Changed decision ref between wrapper pre-call and decode pre-call is accepted if the post-consumer call returns the wrapper pre-decision.
- **Held/unselected alias: PASS_SCOPED.** 9 B tests pass; held/unselected Y does not require a native ref; selected-missing/full-plan partial case refuses.
- **Sourcefree positive: PASS_SCOPED.** Actual production wrapper 30 facts / 15 ops / 18 candidates, anti/op-anti true, `native=false`; F receipt and its `fdc6f3f9…` compilation receipt remain the exact historical positive.
- **Current scope: PRESERVED.** 7 sources / 694 frontier operations / 683 eligible / 11 held; 28 no explicit route-qualified frontier. Historical 20/991 non-F1 scope remains historical; route 676/4,705/249; plan 18,276 items / 18,413 slots / 18,467 operations.
- **D tests: PASS_SCOPED_NEGATIVES.** 3 passed (manifest/path/no resolver), not positive wrapper proof.
- **Extra frontier: PASS.** Exact plan-derived frontier extras remain refused.

## LIMITS

- Actual original facts, E/N10E handoff, native/all35 facts, science and protected acceptance remain **NOT_RUN/HOLD**.
- No original data read, 600 s decode rerun, full-estate fixture floor, code repair, A/C/E/guide/progress/controller edit, or native/science grant.
- F prior negatives/sourcefree positive preserved. Sourcefree probes are TEST_ONLY_SOURCEFREE.
