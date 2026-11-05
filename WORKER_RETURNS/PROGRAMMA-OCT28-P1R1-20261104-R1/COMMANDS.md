# Executed independent commands and reproduction

Execution root was `/tmp/rawlsing-oct28-p1r1`; `base` and `p1` linked the clean detached managed worktrees recorded in `PROVENANCE.json`. The review branch stayed at the accepted baseline plus this return packet. Packages were installed only in the root's disposable venv.

```sh
python3 -m venv --system-site-packages /tmp/rawlsing-oct28-p1r1/venv
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pip install pyarrow==22.0.0 pyreadstat==1.3.2 duckdb==1.5.2
export PATH=/tmp/rawlsing-oct28-p1r1/venv/bin:$PATH
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
```

Inputs were extracted using `git show PIN:PATH` from the four pinned packets in `00_RETURN.md`. `PROVENANCE.json` records their verified SHA256s. The `inputs/` directory preserves the exact extracted bytes, including the synthetic SAV. The E1 fixture/harness, E4 capture and E3 command list were reused as specified; their assertions and outputs were independently executed. P1's `profile_p1.py`, `run_pairs.sh` and `compare.py` supplied measurement instrumentation only. All logs in this packet are from this reviewer run.

Actual test commands from the candidate directory:

```sh
bash /tmp/rawlsing-oct28-p1r1/inputs/related-suite-command.sh
python3 -m pytest rawlsing_next/tests/test_pre553_c11_execution_view.py rawlsing_next/tests/test_pre553_route_b_production.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py -q -o addopts= -p no:cacheprovider
python3 -m pytest /tmp/rawlsing-oct28-p1r1/packet/test_independent_review.py -v -s -o addopts= -p no:cacheprovider
PYTHONPATH=.:/tmp/rawlsing-oct28-p1r1/packet python3 -m pytest rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_query_frontier_hostile.py rawlsing_next/tests/test_pre553_discovery_exact.py -p force_compact -q -o addopts= -p no:cacheprovider
python3 /tmp/rawlsing-oct28-p1r1/packet/check_qualified_identity.py
python3 /tmp/rawlsing-oct28-p1r1/packet/cache_red_restore.py
RAWLSING_C11_ACCELERATOR_DIR=/tmp/rawlsing-oct28-p1r1/native-cache python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41 -q -o addopts= -p no:cacheprovider
```

The forced compact suite exits 1 at the single documented instance-identity assertion; its original log is preserved. The amended-identity script executes the complete original test with exactly one assertion changed in memory. The hash-check script deliberately demands pytest exit 1 while the body-hash comparison is severed in memory, then demands PASS after restoration. Neither script edits tracked code or tests. An initial development run of the independent reviewer test helper referred to a nonexistent `QueryExecutionResult.predicate_ref`; that reviewer-harness mistake was corrected before final receipts. It was not a P1 failure.

The final required reference-descendant court found an additional **material** defect, separate from those passing/nominal courts. From the candidate checkout, using the committed packet path:

```sh
packet=/Users/matthewsmith/.codex/worktrees/f935/Rawlsing/WORKER_RETURNS/PROGRAMMA-OCT28-P1R1-20261104-R1
python3 "$packet/probe_selector_ref_alias.py"
python3 -m pytest "$packet/test_selector_ref_integrity.py" -q -o addopts= -p no:cacheprovider
```

The probe obtains selectors through `_select_respondent_events`, changes their retained event/question ref dictionaries, executes the actual I03 entrypoint, and restores exact facts. It requires observable changed results to demonstrate the defect. The regression requires unchanged exact results and therefore exits **1** at the reviewed P1 SHA. `selector-ref-alias.log` and `selector-ref-regression-RED.log` preserve both outcomes. Running `probe_native_ref_baseline.py` from the baseline checkout is the native detached-ref control and exits **0**. No production correction was implemented.

Independent captures, in their respective baseline/candidate directories:

```sh
RAWLSING_C11_ACCELERATOR_DIR='' python3 /tmp/rawlsing-oct28-p1r1/inputs/capture_native.py /tmp/rawlsing-oct28-p1r1/inputs/same-source.sav /tmp/rawlsing-oct28-p1r1/evidence/native-base
RAWLSING_C11_ACCELERATOR_DIR=/tmp/rawlsing-oct28-p1r1/native-cache python3 /tmp/rawlsing-oct28-p1r1/inputs/capture_native.py /tmp/rawlsing-oct28-p1r1/inputs/same-source.sav /tmp/rawlsing-oct28-p1r1/evidence/native-p1
```

Their native and checkpoint bytes were independently compared with Python byte equality and SHA256. `native-court.log` records both equality checks and the actual source-determinant RED. One compressed native capture suffices because both captures are identical. Both empty stdout/stderr logs are retained as execution receipts; assertion failure would have produced a nonzero command and traceback.

Resource commands:

```sh
bash /tmp/rawlsing-oct28-p1r1/packet/run_pairs.sh /tmp/rawlsing-oct28-p1r1 /tmp/rawlsing-oct28-p1r1/inputs
python3 /tmp/rawlsing-oct28-p1r1/packet/compare.py /tmp/rawlsing-oct28-p1r1/evidence
bash /tmp/rawlsing-oct28-p1r1/packet/run_pairs.sh /tmp/rawlsing-oct28-p1r1/serial /tmp/rawlsing-oct28-p1r1/inputs
python3 /tmp/rawlsing-oct28-p1r1/packet/compare.py /tmp/rawlsing-oct28-p1r1/serial/evidence
```

The second root also has exact-pin `base`/`p1` symlinks. It was created fresh so the script's cache-absence check held. Each series runs baseline A, compact cold, compact warm, baseline B, corrupted members, deleted members in separate sequential processes. The second series began after all reviewer tests/captures finished. The first series's overlap with tests is expressly a timing confound. `timing-raw.tar.xz` keeps every raw JSON/stderr from both series; measurement summaries verify native output parity and cache counters before reporting timings.

To reproduce from this committed packet, use its directory as `packet`, point `PYTHONPATH` at the exact candidate checkout and add `packet` for `-p force_compact`, and use `packet/inputs` for the fixture. Create a fresh scratch root with `base` and `p1` worktrees at the exact pins. P41's pinned Git object and the tracked historical runtime authority files named in the P1 return must remain accessible. The independent test script supports either the original scratch `packet/../inputs` placement or this committed `packet/inputs` placement.

The full native capture and raw timing archive use lossless XZ packaging (`native.json.xz`, `timing-raw.tar.xz`); decompressed bytes retain their recorded identities. This reduced the oversized upload payload without dropping evidence.
