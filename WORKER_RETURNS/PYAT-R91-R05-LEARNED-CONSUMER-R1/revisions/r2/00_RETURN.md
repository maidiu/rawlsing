# R91 R05 R2 full product-graph consumer return

**Verdict: CANDIDATE_FOR_INDEPENDENT_REVIEW. The R05V P1/P2 gaps are repaired at the callable grain; full live J42/P41/E04 remains NOT_REACHED.**

## Identity

- Startup `31d77fd37c501954c088c786db20d8056b6748f5`; same OpenCode DeepSeek
  V4.1-Flash MAX/Global author and branch
  `agent/opencode-pyat-r91-r05-learned-consumer-r1`.
- Contract commit `cde351f734143da2c1b3eab076ff35c080a60438` (before code).
- Code commit `09a0232f7bd6eac45ab835e62e6e4f55f8a06b44`.
- R05V review read/preserved: `eefc2e65f3d1e6d579b06e522f23b9cd6fc942b5`.

## Delivered

`NativeProductGraph` plus extended `evaluate_learned_world_consumer`:

- accepts one or more actual `AnalyticalCompositionResult` components plus an
  optional actual E41 extension result;
- requires shared consumer query/model, validates every component source universe
  and producer predicate against the M1 disposition;
- evaluates each component's actual evidence independently through the unchanged
  N10E evaluator (no invented aggregation/geometry);
- binds producer route(s), joint component count/order, discovery receipt/frontier,
  recursive handoff/lineage and E41 extension route into the result/values;
- preserves eligibility/execution/result axes, denominator/cells and
  `z_unresolved`; non-supported states return typed
  `LEARNED_CONSUMER_ZERO_SUPPORT` / `VALID_EMPTY` / `UNKNOWN` instead of generic
  REFUSED, with Z UNRESOLVED denominator 16 marked;
- retains working single-composition positive API and the actual native
  M01->M1->M2->C1->N10E positive.

## Evidence

```text
/usr/local/bin/python3 -m pytest -q \
  rawlsing_next/tests/test_universal_learned_consumer.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  --junitxml=WORKER_RETURNS/PYAT-R91-R05-LEARNED-CONSUMER-R1/revisions/r2/junit.xml
```

`36 passed`, `0 failed/errors/skipped`, `9.16s` (6 R05 tests + 30 learned-world
regressions).

Independent R05V probes replayed from the exact review blob:

```text
PYTHONPATH="$PWD" /usr/local/bin/python3 -m pytest -q \
  .r61/reconciliation/r05r2/probes/test_r05v_consumer_gap.py \
  --junitxml=.../revisions/r2/r05v_probes_replay.xml
```

`4 passed`, `0 failed/skipped`. Both former gap probes now pass: typed axes and
joint/discovery/recursive graph binding fields reach the same consumer.

Actual native positive: M01 execution -> discovery/facts -> M1 RULE_SATISFIED ->
M2 release -> C1 conditional evidence (denominator 1, cells 0=0/1=1) -> unchanged
N10E `EXACT_SUPPORTED`; E41 direct extension reaches the same consumer hash.

## Blobs / scope

| Path | Blob |
|---|---|
| `rawlsing_next/pre553_learned_world_composition.py` | `32631d17b2db87a16d2ac55d5c3faf2235d13be0` |
| `rawlsing_next/tests/test_universal_learned_consumer.py` | `3ae5e674265d12e3fad1761211db67dfd6017747` |

Only the authorized code/test paths plus own r2 return changed. E41 extension and
accepted C1/provider/native owners remain unchanged from R05/R03/R08.

## Limits

Full multi-component/actual joint/recursive fixture linkage is implemented and
validated generically; the qualification demonstrates the single-component graph
plus E41 route and the R05V graph-field mutations. Broader AT07 provider historical
fixtures are not materialized in this isolated checkout; no missing-fixture test is
counted as a pass. Full live J42/P41/E04 service, original science/source, F6/F7,
CI/prod, N11/N12, Sorok, J52/W52 and R04.joined remain NOT_REACHED/HOLD. Distinct
native review follows; no self-adoption.
