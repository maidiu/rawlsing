# D r10 evidence and commands

## Actual production-wrapper probe

Sourcefree SAV/config, selected `A/B/Y`, coordinate `G`; actual
`execute_native_compiler_source` with state-root and explicit permission.

| Case | Result |
|---|---|
| Positive/restore | accepted; 30 facts / 30 envelopes / 15 ops / 18 candidates |
| `A,A,B`, new state root | refused `SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER`; no artifact |
| `A,A,B`, same root with valid prior artifact | refused; prior artifact bytes unchanged; no `.staged-tmp` |
| Positive artifact ceiling | all envelopes exactly `("FIELD_FORGE_RELATION_PRODUCTION",)` |
| Cold/helper E path | 30 one-target envelopes -> 30 typed arity refusals, 0 profiles, `structural_grant=false` |

## Helper failure behavior

- Missing query: existing valid artifact unchanged; no staged temp.
- Missing/empty/invalid permission: fails before artifact; existing artifact unchanged.
- Forced `os.replace` publication failure: existing artifact unchanged; no staged temp.

## Tests / reused proofs

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 1 passed in 2.03s
```

Reused accepted proofs: R9 actual positive/restore 30/30/30 arity refusals, 0
profiles, structural false; changed controlled sourcefree input changes actual
fact/envelope identity; E codec blob `6acba005…` exact at `f708b468…` and this
head. Prior G `e693359b…` artifact-ordering REVISE is closed.

## Preserved floors / limits

Plan 18,276/18,413/18,467; current frontier 7/694/683/11; historical 20/991;
route 676/4,705/249. Actual original facts, authentic E handshake, A/C scale,
full estate and 650 s remain **NOT_RUN/HOLD**. No original data read, code
repair, A/C/E/guide/progress/controller/protected/native/science change.
