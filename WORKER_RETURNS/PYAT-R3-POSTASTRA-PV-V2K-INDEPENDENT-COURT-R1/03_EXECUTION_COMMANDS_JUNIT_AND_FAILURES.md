# Actual execution, commands, JUnit and failures

**EXECUTED:** fixed-composite local Python tests and independent cold replay. **NOT_EXECUTED:** raw original surveys, competent real original U/E/custody issuance, science/source-use admission, semantic adoption, canonical merge, full historical/full-estate suites beyond the five named selected owner suites, N9/N10E/N10W operative service, N11/N12 wake, V3 actor/model or V2/persona production.

## Runtime and selector

Bootstrap: `bash /Users/matthewsmith/.cache/rawlsing/prepare_sparse_worktree.sh /Users/matthewsmith/Desktop/as2b-lits1-DiSDJn/repository /Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent agent/reviewer-pyat-r3-postastra-pv-v2k-independent-r1 ce760f231cb5ae0678e39f9d12798997f8b6da27 /WORKER_COMMISSIONS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/ /WORKER_RETURNS/PYAT-R3-HQ295-V2K-ORIGINAL-IDENTITY-SUCCESSOR-R1/ /WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/ /rawlsing_next/ /AGENTS.md`. It fetched and matched the remote, created only the isolated assigned branch, and checked clean exact HEAD. No tracked AGENTS.md existed at the start tree. Read-only Git blob reads, source hashes and live branch comparisons are indexed in `documentary_sources_and_remote_cut.json`; resource telemetry is in `resource_preflight.json`.

`repro/run_court.py` reconstructs exact owner archive + candidate blobs, checks every materialized selected source against Git and SHA256, copies only the new independent test, and runs all three named suites in fresh subprocesses. Actual `PYTHONPATH` and cwd point exclusively to that isolated composite. A pytest plugin rejects foreign rawlsing_next module paths and records imported source paths/blob/SHA256; a Python profile hook separately records executed source files, and a read-only startup audit verifies actual helper execution/imports in child processes (`child_audits/`), including `a04t_join_worker.py`. All final imported/executed source bytes match the selector. Instrumentation adds overhead and is not a production latency measurement. No installed library source is upgraded into a project owner.

Reproduce from an exact checkout containing this return: `python3 WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/run_court.py`, then `python3 WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/run_cold.py`. Use a fresh copy of the return to preserve this run's evidence. The runtime locations in manifests are actual temporary execution terrain, not persistent production services. `repro/retry_independent.py` documents reviewer development reruns against the original isolated archive; final reproduction does not depend on those development retries.

## Every retained JUnit result

| Artifact | Tests | Failures | Errors | Skips |
|---|---:|---:|---:|---:|
| repro/candidate.xml | 24 | 0 | 0 | 0 |
| repro/independent.xml | 21 | 0 | 0 | 0 |
| repro/initial_independent.xml | 21 | 7 | 0 | 0 |
| repro/owners.xml | 111 | 0 | 0 | 0 |
| repro/pre_child_owners.xml | 111 | 0 | 0 | 0 |
| repro/pre_profile_candidate.xml | 24 | 0 | 0 | 0 |
| repro/pre_profile_independent.xml | 21 | 0 | 0 | 0 |
| repro/pre_profile_owners.xml | 111 | 0 | 0 | 0 |
| repro/pre_trace_candidate.xml | 24 | 0 | 0 | 0 |
| repro/pre_trace_independent.xml | 21 | 0 | 0 | 0 |
| repro/pre_trace_owners.xml | 111 | 0 | 0 | 0 |
| repro/second_independent.xml | 21 | 1 | 0 | 0 |
| repro/third_independent.xml | 21 | 0 | 0 | 0 |

The final 21 independent passes include affirmative observation of candidate limitations. They are not 21 semantic-adoption approvals. The 24 candidate and 111 owner tests are original unmodified suite files, checked against exact fixed Git blobs. Repeated runs are repeat verification, never extra independent proof. Full failure bodies and tracebacks remain in corresponding `.log` and `.xml`; no failure was hidden by a skipped/xfail marker. There are no skips/xfails in final named suites.

## Development and instrumentation diagnoses

- First independent run: 7 failed /14 passed. Reviewer constructed documentary discovery rows from the full dataclass serializer, preserving `query_ref:null`. The existing P01 adapter selects `raw.get('query_ref', raw.get('discovery_authority_ref'))`, so discovery became a foreign manifest unit. Changed only reviewer input serialization to omit optional None fields, consistent with owner input convention. Frozen roster/arithmetic/case hypotheses unchanged; no owner repair.
- Second independent run: 1 failed /20 passed. Reviewer assertion assumed flat `conditioner_ref`/`target_ref` export fields; actual material uses `roles.CONDITIONER.ref`/`roles.TARGET.ref`. Corrected assertion path, with the same exact refs and arithmetic. Both failed-run artifacts retained.
- Third independent run: 21 passed. Strengthened independent original key reconstruction before production; reran reviewer tests, still 21 passed.
- Added executed-file audit because dynamically loaded helper execution deserved evidence beyond normal sys.modules imports. First instrumentation pass missed path aliases (`/var` versus `/private/var`), yielding empty executed-source lists, even though imported-source hashes and all tests passed. These empty audit artifacts are retained as `pre_trace_*`; they are not claimed as executed-source proof. Resolved runtime path before instrumentation and reran all named suites. Final nonempty parent source audits cover in-process owners. The helper runs in child processes; parent profiling does not cover them. A further startup exec/import audit inherited by real child processes verifies the actual helper and every imported selected project source against the same selector. Its full 111-owner rerun and per-process receipts are retained; no owner code or verifier import blocker was changed.
- Original candidate and owner suites passed on every executed attempt here. The HQ295 worker's older failure history is distinct and is not counted as this reviewer's runs.

## Cold terminal

Two fresh independent processes, identical complete independently frozen preimages before producer reconstruction. First calls [3,3], replay [0,0], six exact same original/result/consumer links, two held rows. Actual logs/JSON/source audits in `cold_first*` and `cold_replay*`. No durable-call suppression monkeypatch and no worker positive emitter/fixture import. The synthetic producer reconstruction in both processes is explicitly retained; no claim of zero total computation.

## Exact commands and exit statuses

The following are the actual subprocess commands, working directories, elapsed times and terminal exit statuses. Shell entrypoints and the data-source reconstruction are saved as runnable scripts; output is actual stdout/stderr and pytest JUnit.

### execution.json

```json
[
  {
    "suite": "independent",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 1,
    "seconds": 6.522892951965332
  },
  {
    "suite": "candidate",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/candidate.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 3.6755211353302
  },
  {
    "suite": "owners",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py",
      "rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py",
      "rawlsing_next/tests/test_pre553_route_b_production.py",
      "rawlsing_next/tests/test_pre553_empirical_query.py",
      "rawlsing_next/tests/test_pre553_discovery_exact.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/owners.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 23.57855486869812
  },
  {
    "suite": "independent_corrected_fixture",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 1,
    "seconds": 6.461653232574463
  },
  {
    "suite": "independent_corrected_fixture",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 6.558609247207642
  },
  {
    "suite": "cold_first",
    "command": [
      "/usr/local/bin/python3",
      "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/cold_independent.py",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/cold-independent-ledger",
      "first"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 0.8989429473876953
  },
  {
    "suite": "cold_replay",
    "command": [
      "/usr/local/bin/python3",
      "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/cold_independent.py",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/cold-independent-ledger",
      "replay"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 0.6580369472503662
  },
  {
    "suite": "independent_corrected_fixture",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-uywnr_k9",
    "exit_code": 0,
    "seconds": 6.712518930435181
  }
]
```

### profile_execution.json

```json
[
  {
    "suite": "independent",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17",
    "exit_code": 0,
    "seconds": 28.108892917633057
  },
  {
    "suite": "candidate",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/candidate.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17",
    "exit_code": 0,
    "seconds": 15.505474090576172
  },
  {
    "suite": "owners",
    "command": [
      "/usr/local/bin/python3",
      "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py",
      "rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py",
      "rawlsing_next/tests/test_pre553_route_b_production.py",
      "rawlsing_next/tests/test_pre553_empirical_query.py",
      "rawlsing_next/tests/test_pre553_discovery_exact.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/owners.xml"
    ],
    "cwd": "/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-t6akku17",
    "exit_code": 0,
    "seconds": 51.81975078582764
  }
]
```

### final_execution.json

```json
[
  {
    "suite": "independent",
    "command": [
      "/usr/local/bin/python3",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_postastra_pv_v2k_independent.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/independent.xml"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 34.5209801197052
  },
  {
    "suite": "candidate",
    "command": [
      "/usr/local/bin/python3",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/candidate.xml"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 18.51173496246338
  },
  {
    "suite": "owners",
    "command": [
      "/usr/local/bin/python3",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py",
      "rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py",
      "rawlsing_next/tests/test_pre553_route_b_production.py",
      "rawlsing_next/tests/test_pre553_empirical_query.py",
      "rawlsing_next/tests/test_pre553_discovery_exact.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/owners.xml"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 57.13498401641846
  }
]
```

### cold_execution.json

```json
[
  {
    "suite": "cold_first",
    "command": [
      "/usr/local/bin/python3",
      "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/cold_independent.py",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/cold-independent-ledger",
      "first"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 2.7577641010284424
  },
  {
    "suite": "cold_replay",
    "command": [
      "/usr/local/bin/python3",
      "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/cold_independent.py",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/cold-independent-ledger",
      "replay"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 2.5150067806243896
  }
]
```

### child_execution.json

```json
[
  {
    "suite": "owners_child_import_audit",
    "command": [
      "/usr/local/bin/python3",
      "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6/pv_pytest.py",
      "-q",
      "rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py",
      "rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py",
      "rawlsing_next/tests/test_pre553_route_b_production.py",
      "rawlsing_next/tests/test_pre553_empirical_query.py",
      "rawlsing_next/tests/test_pre553_discovery_exact.py",
      "--import-mode=importlib",
      "--junitxml=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/postastra-pv-v2k-independent/WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1/repro/owners.xml"
    ],
    "cwd": "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/postastra-pv-runtime-vgp53lc6",
    "exit_code": 0,
    "seconds": 70.44021105766296
  }
]
```

## Write and proof boundary

All new tracked files are under this own return and the one new independent test path. Candidate, published V2, owner code, frozen original tests and production CURRENT were not edited. `02_EXACT_COMPOSITE_SOURCE_SELECTOR.json` includes every materialized original source/test/helper Git blob and SHA256. `verification_summary.json` summarizes exact final terminals. The manifest binds saved evidence without a self-hash. Commit/push use only the assigned reviewer branch, and exact direct remote readback is reported outside the commit's own bytes.
