# 01 — Review scope, exact identities, and evidence method

## Role and authority boundary

This is an independent sourcefree R03 engineering review. The reviewer is distinct
from implementation author `ses_e50ee2de8ffeVZ5fDDwTyiegq1`, wrote none of the
implementation or author tests/measurements, and is not an original35 respondent,
source authority, actor/human/Sorok authority, or protected-merge authority. The
review accepts or rejects only the bounded P2 engineering claim. It does not
create a scientific owner, cache-policy grant, native-source truth, or second guide.

No production source, source guide, protected branch, cache policy, scheduler, or
global configuration was edited. The only writes are:
`WORKER_RETURNS/PROGRAMMA-PYAT-L03-R03-20261106-R1/` and
`.local-logs/pyat-l03-r03/`.

## Frozen identities

- Branch: `review/programma-pyat-l03-r03-grouped-20261106-r1`
- Frozen implementation: `409be32f7e4b4b961a360be1c8f44a17b5c62173`
- Protected base: `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`
- Evidence final head: `f3dcdf4d92d85897e1db360e70445b0cf170e986`
- Binding commission: `66cedcdf01cd156d0024419957b5c34832ebf8a5`
- C4 artifact directory: `WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/`

The evidence final head `f3dcdf4d` records the frozen SHA and adds only
`results/implementation_sha.txt` plus two artifact text updates. It does not
change production/test code. I verified the six production/test blobs at
`f3dcdf4d` are identical to `409be32`:

| File | Blob SHA at both commits |
|---|---|
| `rawlsing_next/_pre553_query_eval.py` | `9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920` |
| `rawlsing_next/pre553_empirical_query.py` | `c3e80df8c44a2c9f41188ed85e9e7854fbd48ca1` |
| `rawlsing_next/pre553_carrier_execution.py` | `ee9b3af02bfca9238eb72ea45d94073d47769a07` |
| `rawlsing_next/pre553_discovery_exact.py` | `1b82b6df993bf14afa5e78782d988cba6e76b668` |
| `rawlsing_next/pre553_issued_workload.py` | `28174766f61a15f7296f575d615462d6410cfcb6` |
| `rawlsing_next/tests/test_pre553_i03_grouping.py` | `c92a032977173696467e6518765b5756d7aefb34` |

## Exact implementation scope

`git diff --numstat 8ffec40a...409be32 -- rawlsing_next/` contains only the six
production/test files:

```
333  1   rawlsing_next/_pre553_query_eval.py
 28  1   rawlsing_next/pre553_carrier_execution.py
  4  0   rawlsing_next/pre553_discovery_exact.py
238  1   rawlsing_next/pre553_empirical_query.py
 29 15   rawlsing_next/pre553_issued_workload.py
667  0   rawlsing_next/tests/test_pre553_i03_grouping.py
```

The implementation commit also updates its own C4 artifact files under
`WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/`. Those are evidence, not
production semantics. No P41, selector-v1 ABI, source-ingest, compact-view,
authority, scheduler, or default cache-policy source was rewritten.

## Artifacts inspected

All seven C4 artifacts were read, plus retained results and tools:

- `00_RETURN.md`, `01_BASELINE_CURRENT_CODE_ABI.md`,
  `02_EXACT_COST_AND_MEMORY_RESULTS.jsonl`,
  `03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl`,
  `04_REPLAY_AND_AUTHORITY_INVALIDATION.md`,
  `05_OPTION_MATRIX_AND_MINIMAL_DELTA.md`, `06_INDEPENDENT_REVIEW_REQUEST.md`.
- `results/phase2_summary.json`, `results/phase2_commands.jsonl`,
  `results/commands.jsonl`, `results/driver_summary.json`,
  `results/repeat_summary.json`.
- `tools/bench_common.py`, `tools/bench_grouped_phase2.py` (the paired runner
  uses the actual `CarrierNeutralResearchExecutor.execute_i03`; the baseline is
  the unchanged no-scope path).
- The `03` JSONL contains 52 `baseline_exact_fact`, 44 `same_fact_relation`,
  39 `phase2_op_exact_parity` (13 operations × 3 sizes), 12 pass-parity, 12
  selected-full-fact-digest, 6 selected-full-fact-parity, and smaller
  fixture/cache/negative entries. I audited the per-op fields (cells, raw and
  weighted support, member counts/digests, provenance/dependency digests,
  fact/replay refs), not only a checksum.

The author-referenced untracked raw logs under `.local-logs/pyat-l03-c4/` were
not present in the assigned checkout. I did not attempt to reconstruct or
redirect them. Retained tracked artifacts and independent reruns were used
instead. This is listed as a missing-evidence limit, not a defect.

## Method

1. Read the commission and all seven C4 artifacts; verified the exact six-file
   source/test diff and blob identities.
2. Ran the author’s 11 new grouping tests, then the bounded 100-test focused
   suite and the P41 same-source test with the verified runner.
3. Wrote a reviewer-only script (`.local-logs/pyat-l03-r03/reviewer_checks.py`)
   that builds the same sealed source, computes a row-level oracle directly from
   the fixture rows, and exercises the real `CarrierNeutralResearchExecutor`
   first consumer. It independently checked:
   - all 13 operations (RAW/weighted, 1/2/3/4 targets, both conditional
     directions, XOR, minority, risk-set separation) against the oracle;
   - same-world index cut and exact restore with the same scope;
   - five poisoned-core variants;
   - W2 weight-basis refusal, zero support, and the special typed-state fixture.
4. Instrumented the issued/P41 path only to observe owned-scope receipts, then
   ran P41 grouped vs forced-unshared and compared hashes/view/consumer values.
5. Probed W03/W04 physical behavior: default compact Arrow selection when
   pyarrow is installed, and caller-configured Parquet/Zstd slot creation/reuse.
6. Ran one paired N=200 benchmark through the actual consumer (three warm
   rounds) and audited retained N=1,000/3,000 artifacts rather than rerunning
   them.

No new statistical truth engine, architecture bakeoff, whole-estate run, or
native/original35 measurement was performed.

## Environment

`oldMac.lan`, macOS 13.7.8 (build 22H730), Darwin 22.6.0 x86_64, 16 logical CPUs,
17,179,869,184 bytes physical memory; Python 3.11.3, pyarrow 22.0.0,
pandas 3.0.6, pytest 9.1.1; runner
`/tmp/rawlsing-oct28-p1r1/venv/bin/python`. All timed work was single-runner and
sequential; no new packages or `/tmp` redirects were used.
