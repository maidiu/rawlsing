# PROGRAMMA PYAT — Universal35 D r6: actual decode-approved decision capture

**STATUS:** `D_R6_EXTRA_PRECALL_REMOVED__ACTUAL_DECODE_DECISION_CAPTURED__POSTCONSUMER_EXACT_EQUALITY_BOUND__AUTHOR_EVIDENCE_FOR_G`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `cc0a0e39ef2d05cca3a92f045cec8830386cf647` / code `608be7780d0eee93a8e0d06aade4ff2f67081026`
**G R5 REVIEW:** `bc01712c111c7522d92bbd27e8a318453c4518e3`

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R6-1. The extra wrapper pre-decision call is removed.** The bridge now wraps the caller resolver in a recording delegating resolver and passes it unchanged into existing `decode_with_source_read_permission`. The first captured call is the exact decision the admission owner used for decode. | G's `A,B,B,A` bypass existed because the wrapper compared its own extra `A` pre-call with final `A`, not the decoder's actual `B`. Now the decode-approved `B` is the comparison baseline. | G focused exact closure. | D + source-read owner |
| **R6-2. Post-consumer comparison uses immutable captured decision material.** Captured decisions are converted with `dataclasses.asdict` at observation time; final resolver output is materialized the same way and compared exactly, including decision ref, host, purpose, scope, metadata refs, currentness and revocation. | No stale-decision cache, mutable alias, fabricated issuer or weakened admission. A changed still-current decision now refuses `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`. | Preserve exact equality. | D |
| **R6-3. Failed pre-decoding / no observed decision is typed.** Missing captured decode decision refuses `SOURCE_READ_DECODE_DECISION_NOT_OBSERVED`; no-consumer-decision path still refuses before I/O. | Failure is closed rather than accepted. | Keep typed refusal. | D |
| **R6-4. Held/unselected alias and exact frontier remain accepted subscopes.** Selected frontier aliases only; held/unselected `Y` remains plan/held accounting; selected missing physical still refuses. | No regression to accepted R5 alias behavior. | Preserve. | D/B + G |

## 2. FOCUSED TEST

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_recording_resolver_binds_actual_decode_decision_not_extra_precall \
  -p no:cacheprovider --tb=short
1 passed in 0.40s
```

The regression models G's former resolver sequence as it reaches the wrapper after removing the extra pre-call: `decode-B`, `decode-post-B`, `consumer-A`; first captured decision differs from final and would refuse. Exact `A,A,A` remains equal/positive.

## 3. PRESERVED EVIDENCE

- G sourcefree production-wrapper positive remains historical: 30 facts / 15 expected operations / 18 candidates / anti and op-anti true / `native=false`.
- B held-`Y` positive and selected-missing negative remain.
- Plan: 18,276 items / 18,413 slots / 18,467 operations; route 676/4,705/249; frontier 7/694/683/11 and 28 no-route sources.
- No actual original facts or E authentic handshake claimed; no native/science/protected authority.

## 4. CHANGED PATHS

`rawlsing_next/pre553_original35_execution.py`, `rawlsing_next/tests/test_pre553_original35_execution.py`, `06_R6_RETURN.md`, `evidence/native_bridge.json`. No A/B alias semantics, C/E, grammar/admission owner, guide/controller or protected edit.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r6 actual decision capture
- Identity: codex/pyat-universal35-d-20261106-r1@a286fe469f9622f6370af8993fca283b2f1af2c4; input cc0a0e39e.
- Function: existing decode admission called through recording delegating resolver; first captured decision is the decode-approved decision; final post-consumer decision material must equal it exactly.
- Evidence: focused ABBA-shaped regression passes; G/R5 30-fact sourcefree positive receipt preserved; held-Y/selected-missing preserved.
- Limits: actual original facts/E handshake NOT_RUN; no original current decision; no native/science/protected acceptance.
```

## 6. LIMITS / REQUEST

G focused closure is requested on this exact head for the actual production-wrapper ABBA sequence, changed-after/revoked refusals and exact restore. No original data, 600s decode, whole-estate floor, E/native handshake or protected merge was rerun.
