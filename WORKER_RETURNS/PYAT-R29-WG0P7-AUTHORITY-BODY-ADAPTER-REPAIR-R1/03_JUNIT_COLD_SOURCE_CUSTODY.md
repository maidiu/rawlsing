# WG0P7 — JUnit, cold, imports and source custody

All courts were run in fresh processes from the shared repository with
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and the
candidate's own `bootstrap_p6` identity transport on `PYTHONPATH`. The
bootstrap verifies every staged project file against the candidate pin before
import and refuses hard on mismatch.

## Exact commands (literal, from `candidate/observations/*.terminal.json`)

```sh
cd WORKER_RETURNS/PYAT-R29-WG0P7-AUTHORITY-BODY-ADAPTER-REPAIR-R1/candidate
python3 -B repro/run_court.py wg0m33      # jUnit candidate/observations/wg0m33.xml
python3 -B repro/run_court.py original65  # jUnit candidate/observations/original65.xml
python3 -B repro/run_court.py original3   # jUnit candidate/observations/original3.xml
python3 -B repro/run_court.py j44_k11     # jUnit candidate/observations/j44_k11.xml
python3 -B repro/run_court.py owners80    # jUnit candidate/observations/owners80.xml
python3 -B repro/run_court.py author26    # jUnit candidate/observations/author26.xml
python3 -B repro/run_court.py fresh       # jUnit candidate/observations/fresh.xml
```

```sh
cd WORKER_RETURNS/PYAT-R29-WG0P7-AUTHORITY-BODY-ADAPTER-REPAIR-R1
WG0O_RUN=wg0p7_repaired python3 repro/run_frozen14.py   # 14 WG0O controls
python3 repro/capture_preimage.py                       # full body preimage
```

## JUnit counts (raw, copied to `observations/junit/`)

| Court | tests | failures | errors | skipped | exit |
|---|---:|---:|---:|---:|---:|
| `wg0m33` | 33 | 0 | 0 | 0 | 0 |
| `original65` | 65 | 0 | 0 | 0 | 0 |
| `original3` | 3 | 0 | 0 | 0 | 0 |
| `j44_k11` | 55 | 0 | 0 | 0 | 0 |
| `owners80` | 80 | 0 | 0 | 0 | 0 |
| `author26` | 26 | 0 | 0 | 0 | 0 |
| `fresh` (WG0P6 source-view boundary) | 42 | 0 | 0 | 0 | 0 |
| **mandatory 236** (33+3+80+55+65) | **236** | **0** | **0** | **0** | — |
| WG0O frozen 14 (executed in-process, raw JSON) | 14 | 3 RED closed | 0 | 0 | 0 |

The WG0O frozen 14 raw outcomes are in
`observations/frozen14_execution.json`; A2 is `AuthorityCurrentnessHold`/HELD,
A3/A4 are `IdentityError`/REFUSED, each with 0 supported cells and 0 new I03
calls, while P1/P2/P3 serve 42 cells.

## Cold recovery

WG0L `cold/*` nodes are inside `original65` and pass 65/65:
`cold/actual_abrupt_exit23_after_one`,
`cold/fresh_process_exactly_two_I03_calls`,
`cold/three_original_consumer_values`,
`cold/full_frontier25_retained`,
`cold/source_edition_currentness_refuse`. Those are real fresh OS processes with
distinct PIDs, abrupt exit 23 after one unit, and exactly two I03 calls on
resume.

The WG0P6-only `cold_pointer` test is **not runnable in this checkout**: its
committed `cold_comparison.json` carries a literal `<WORKTREE>` placeholder and
the referenced cold directory has no `owner/` tree. It is a source-view pointer
test (WG0P6 domain), not part of the WG0O authority court, and the repair does
not touch that path. This is disclosed rather than papered over.

## Imported module identity

The candidate's own `bootstrap_p6` recorded 28 per-process receipts under
`candidate/observations/imports/`. Each records the candidate pin actually
loaded:

```
staged_path  court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py
sha256       89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643
git_blob     62895078908ff748771da9a9fbcec6b36d34a803
bytes        48953
```

and the six physically verified accepted native owners
`pre553_c11_repository`, `pre553_c11_ingest`, `pre553_empirical_query`,
`pre553_batch_runner`, `pre553_empirical_objects`, `pre553_c11_integrity`,
imported only from `pinned/rawlsing_next` inside the candidate runtime.

## Source custody

| Object | sha256 |
|---|---|
| repaired `wg0p4_workload.py` | `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643` |
| pristine WG0P6 `wg0p4_workload.py` | `3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e` |
| WG0O frozen 14 oracle | `1a57f97bc5ebcb394fd150acbfbc1e57a39039097057e310c2e8ba0078ce5656` |
| WG0O unchanged adapter | see `02_FROZEN_14_AND_ORIGINAL_NATIVE_POSITIVES.json` |
| candidate pin | `candidate/CANDIDATE_CODE_PIN.json` |

`candidate_change.patch` is the exact unified diff between the pristine WG0P6
module and the repaired module (68 lines). The two accepted native owners named
in the commission (`pre553_c11_repository`, `pre553_empirical_query`) and the
I03/Batch owners were not edited; no frozen oracle or inherited test was edited.

## Not run / not claimed

- WG0N hostiles 20: requires the separate WG0M reviewer return as
  `WG0N_PRESERVED_ROOT`, which is not in this lineage. The parent/WG0O record
  stands (12 executed PASS / 5 unconstructible NOT GREEN / 0 RED); the WG0M 33
  court itself was re-executed here 33/33.
- `author69` historical 29/36 and the two older characterisation scripts are
  author-side historical suites; not re-claimed here.
- No WG0N mandatory 236 beyond the physically re-run decomposition above is
  claimed as new research; 236/236 is the sum of the five courts actually run.
