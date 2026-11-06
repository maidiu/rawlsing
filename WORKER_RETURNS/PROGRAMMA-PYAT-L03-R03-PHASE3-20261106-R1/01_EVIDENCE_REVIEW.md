# 01 — Phase-3 evidence review: identities, driver, and measurement classification

## Commits and unchanged production

- Frozen implementation: `409be32f7e4b4b961a360be1c8f44a17b5c62173`
- Author measurement commit: `a85df66ec93a951d8fd50d751822b70569df94ef`
- Author phase-3 evidence head: `141df637d49281fa1d33fa6ad275e09f0f6bd9d4`
  (child of `a85df66e`; updates only `00_RETURN.md` with the measurement SHA)
- Original R03 review commit: `e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3`
  (`ACCEPT_SCOPED_P2`; preserved, not rewritten)

`git diff --name-only 409be32..a85df66e -- rawlsing_next/` is empty: production and
tests are unchanged. All six production/test blobs are also identical at
`141df637`:

| File | Blob SHA at all three commits |
|---|---|
| `rawlsing_next/_pre553_query_eval.py` | `9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920` |
| `rawlsing_next/pre553_empirical_query.py` | `c3e80df8c44a2c9f41188ed85e9e7854fbd48ca1` |
| `rawlsing_next/pre553_carrier_execution.py` | `ee9b3af02bfca9238eb72ea45d94073d47769a07` |
| `rawlsing_next/pre553_discovery_exact.py` | `1b82b6df993bf14afa5e78782d988cba6e76b668` |
| `rawlsing_next/pre553_issued_workload.py` | `28174766f61a15f7296f575d615462d6410cfcb6` |
| `rawlsing_next/tests/test_pre553_i03_grouping.py` | `c92a032977173696467e6518765b5756d7aefb34` |

Phase-3 changes are artifact/tools only under
`WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/`. No source adoption is implied
by inspecting or referencing them.

## Author artifacts and blob identities at `a85df66e`

| Artifact | Git blob |
|---|---|
| `results/compact_current_summary.json` | `e50c6bf399ee5e63642dcea9bf64578efa03aad9` |
| `results/compact_current_commands.jsonl` | `559e7d26fa4f5ad592e56b75053f837cfd1fd236` |
| `tools/bench_compact_current.py` | `d520d4e1bfca2eaf3f64502e554dfa1c8557c36a` |
| `tools/finalize_compact_current.py` | `367c62f1ec1d15d838a098a06feaa15ea5263a2d` |
| `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl` | `78f1ca84a8d487ad01b15a81c71e012dd4fdd6db` |
| `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl` | `b0a2a78c632be365ced735772d94dbebe63c8ddb` |
| `00_RETURN.md` | `62062e91bddf23cd536de3d577caec2ac6d4bbe9` |
| `01_BASELINE_CURRENT_CODE_ABI.md` | `1cdae936b7d4517930b48144af687908ab16fc62` |
| `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md` | `11f0108b7377d8845d5c9aecc8533473c91368d6` |
| `06_INDEPENDENT_REVIEW_REQUEST.md` | `718a007aeb28235222edbb9deb63fa3d337e6165` |

Only the needed artifacts were exported to
`.local-logs/pyat-l03-r03/phase3/`: the summary, commands, driver, and finalizer.
No whole-tree archive was created.

## Driver correctness review

### V0/V1/V2 construction

`bench_compact_current.py` builds one fixture (`_source_fixture`) with the same
`source_sha256`, `GovernedC11Projection`, rows, and cells:

- **V0:** `build_validated_source_backed_c11_release_from_stream(source, projection)`
  then `C11Repository` and the actual `CarrierNeutralResearchExecutor.execute_i03`.
- **V1:** `build_source_backed_c11_repository(source, projection)` with the existing
  default compact Arrow view.
- **V2-cold / V2-warm:** the same V1 facade with
  `RAWLSING_C11_ACCELERATOR_DIR` set to an explicit workload-owned cache root. The
  source is an `ExactPhysicalCellStream` with non-empty `decoder_metadata_digest`.

The coordinator clears the V2 cache before cold, runs each variant in a fresh
subprocess, and compares the full `fact.as_dict()` lists loaded from the sidecars.
It separately requires equal `release_ref`, `source_sha256`, and projection
identity. `cache_checks` require V2-cold read miss + write, V2-warm read hit, and
the same cache file list. This is an actual source-backed facade/first-consumer
measurement, not a private benchmark label or a forged in-memory incidence.

The cache probe wraps the real `_read_bodies`/`_write_bodies` and records whether
the real read returned a hit; it does not replace the cache with a synthetic
counter.

### Grouped driver

The grouped path builds the compact release once, then runs no-scope and grouped
executors over the same compact release object. It uses the actual executor and
checks:

- full fact lists (`fact.as_dict()`), fact refs, and replay refs for cold, warm,
  single-operation, incompatible first pass, and capacity fallback;
- an independent row-level oracle over 16 operations (1/2/3/4 targets, forward and
  reverse conditionals, XOR, minority, routed/asymmetric risk, typed missing,
  zero support, unsupported/valid ordered targets, raw/weighted, siblings);
- separate `Counters` passes for routing/predicate/target/weight/fact/replay work.

The oracle derives expected states/cells/denominators/weights from fixture rows; it
is not the author’s expected fact list. It checks baseline facts, and candidate
facts are separately required equal to baseline.

## Measurement classification (clean vs instrumented, noise, RSS scope)

- **Compact comparison:** parent wall is a single fresh-process wall per variant,
  including interpreter/import, fixture, validation, compact conversion, query,
  fact, and replay. Phase times are instrumented function wrappers; the driver
  reports both. There is **one run per variant**, no repeated comparison rounds.
  The N=200 V2-warm total-wall difference (4.34 vs V0 6.18 s) is therefore not a
  stable economy claim; the N=1,000 result (21.03 vs 21.29 s) is the stronger
  observation and shows little total-wall change.
- **Compact grouped:** warm rounds time `executor.execute_i03` per operation, with
  `gc.collect()` and full `fact.as_dict()` materialization/hash for equality on
  both paths. There are three warm rounds; the headline is the median. Counters
  are a separate wrapped pass and are not the timing basis. N=1,000 round-1
  warm speedup is 1.97×; rounds 2–3 are 2.57×/2.48×. N=200 rounds are
  2.38×/2.40×/2.22×.
- **Peak RSS:** `ru_maxrss` is whole-process Darwin high-water, not per-phase or
  per-operation. Each comparison variant is a fresh process. V0/V1/V2 perform
  different construction work, so RSS is comparable only at the same
  source/release/setup scope, which the driver enforces. The grouped process RSS
  (172.1 MB N=200, 350.8 MB N=1,000) is not used as the compact-memory claim; the
  comparison variants are.
- **Capacity fallback:** the `max_groups=1` probe is a forced budget condition,
  not default behavior. It is exact but slower. The earlier P41 default-scope
  capacity-pressure observation remains a nonblocking limit; no repair code was
  reviewed.

## Evidence boundary

The author’s full per-op fact sidecars are untracked author-workspace paths
(`.../.local-logs/pyat-l03-c4/.../*_facts.jsonl`) and are not in the commits or
this checkout. I independently checked:

- the driver’s full-list comparison code;
- all 104 retained `compact_current_query` rows: zero mismatches across
  `exact_fact_material_sha256`, fact refs, replay refs, and typed states versus V0;
- all grouped per-op equality flags and oracle status;
- the selected full `raw_Y` facts for V0/V1/V2-warm and grouped baseline/candidate
  as complete dictionaries (equal, with full refs/provenance).

I did not inspect every full per-op sidecar byte for all 13 comparison operations.
That is the exact evidence boundary. The retained evidence is stronger than a
checksum-only oracle because full fact material is the comparison basis and a
selected full fact is retained, but it is not a complete archive of every raw
sidecar.

## NOT_RUN

- No reviewer timed benchmark or heavy fixture run.
- No author comparison/grouped rerun.
- No N=3,000, original35, production, cross-machine, or native-source measurement.
- No delete/corrupt/stale/revoke cache rerun (existing functional tests referenced
  by the author; not rerun here).
- No capacity-guard repair review: the repair is concurrently assigned and has not
  returned.
- No source/test/guide/protected branch edit, merge, or default-policy change.
