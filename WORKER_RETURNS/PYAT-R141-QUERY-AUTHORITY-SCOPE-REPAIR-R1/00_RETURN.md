# R141 — exact query-authority scope repair

**Status:** `QUERY_AUTHORITY_SCOPE_REPAIRED_ON_SYNTHETIC_HARNESS__NOT_SOURCE`
**Base:** `ccf97c89d276e3b1460b9bc65d380ff79d8fd97b`
**R138 witness:** `3f35210eadd9891100b6aae2ac01bb9b05d3406a`
**R141 commission:** `f67b4f2a5aae4da8869b7994f468f53d69ceb658`
**Source reads:** 0. Synthetic harness only; no source/scientific/current grant.

## Narrow fix

`_exact_external_query_authority` now validates every supplied applicable query
scope constraint against actual native context instead of ignoring it:

- `target_use_refs` must be the native explicit-unrestricted value; empty,
  foreign refs, or a foreign string refuse.
- `measure` / `measure_kind` / `measure_kinds` must be within the exact native
  measure set for the actual operation (`RAW` for the focused query; the
  frontier's actual SAMPLE/POPULATION mapping for discovery).
- `as_of` must equal the actual operation as-of.
- `grammar` / `frontier` scope constraints are unsupported by this native query
  authority contract and refuse (`SUPPLIED_QUERY_AUTHORITY_UNSUPPORTED_CONSTRAINT`)
  rather than being accepted or replaced by invented refs.
- Unknown query scope fields refuse; source SHA/universe/risk/role/operation
  checks and all previous source/descriptor/currentness refusals are preserved.

No duplicate R138 implementation or new science/rules/engine. R138's original
RED and R140's original return are untouched.

## R138 exact successor replay

The versioned R141 test replays the R138 six-change witness:

| Change | Actual result |
|---|---|
| `target_use_refs=[]` | `SUPPLIED_QUERY_AUTHORITY_TARGET_USE_MISMATCH` |
| `target_use_refs=FOREIGN_TARGET_USE` | same refusal |
| `measure=GOVERNED_WEIGHTED` | `SUPPLIED_QUERY_AUTHORITY_MEASURE_MISMATCH` |
| `as_of=1999-01-01` | `SUPPLIED_QUERY_AUTHORITY_AS_OF_MISMATCH` |
| `grammar=FOREIGN_GRAMMAR` | `SUPPLIED_QUERY_AUTHORITY_UNSUPPORTED_CONSTRAINT` |
| `frontier=FOREIGN_FRONTIER` | same refusal |

All six fail closed before production catalog construction. The previous actual
repeated-event native `SUPPORTED` fact remains: numerator 2, denominator 2, six
cells, value change differs, exact restore matches refs and manifest.

## Preserved R140 controls

R140 focused tests remain green in the same suite: predecode source-read
transport (5 tests, authorized synthetic whole-file R04 custody and 14
zero-open refusals) and external-authority bounded discovery (150/150
candidates, 98 supported + 52 valid-empty receipts, 330 facts, no-drop,
restore). This repair adds one focused successor test; it does not replace or
weaken those controls.

## Actual counts

- Focused production + source-read suites: **19 passed**.
- Listed repeated-positive/test-only regression: **4 passed**.
- R138 successor scope test: **passed** (6/6 foreign changes refused).
- No skip counted as pass.

## Limits

Synthetic SAV values and test-harness authorities only. `ORIGINAL_SOURCE_GRANTED`
is a transport label, not actual source/scientific issuance. No real source,
original 35/1890/F1–F8/global, learned/FF/V553, actor/M1-for-all, R09/CI/prod,
N11/N12, Sorok/J52/W52 or all35 claim. Distinct reviewer required.

## Code pins

- `rawlsing_next/pre553_native_workload_binding.py`: `94ef81792ad2db7895b33dbbdaddc7e3b6b9306b`
- `rawlsing_next/tests/test_pre553_production_binding.py`: `b0309b51b6ae23581b74af8fc0819e230636bca1`
