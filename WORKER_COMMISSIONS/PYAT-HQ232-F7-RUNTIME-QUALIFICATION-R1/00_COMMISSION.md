# PYAT HQ232 — F7 SEALED OWNER-STATE GOVERNED RUNTIME QUALIFICATION — R1

**STATUS:** NEW — NEEDS LAUNCH  
**AGENT:** local governed-runtime evidence qualification worker  
**MODEL / INTELLIGENCE:** **GPT-5.6 Sol High**  
**MACHINE:** user's Mac / governed local Rawlsing runtime  
**WORKTREE:** not established  
**BRANCH:** `agent/rabochii-pyat-hq232-f7-runtime-qualification-r1`  
**EXACT STARTUP TIP:** `d6734e0150e91a60965e7db244ed2ef519ec831c`  
**CANDIDATE CODE-BEARING HEAD:** `62394d7ff817252d6d406c1e0ada96529697f5f2`  
**CANDIDATE DISPOSITION:** `F7_SEALED_OWNER_STATE_CUSTODY_COMPLETE__READY_FOR_FINAL_REREVIEW`  
**PRODUCTION MUTATION:** FORBIDDEN  
**SEMANTIC MUTATION:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

Read:
- `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`;
- `PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md`;
- `WORKER_RETURNS/PYAT-HQ231-F7-SEALED-OWNER-STATE-CUSTODY-R1/`;
- the exact current F7/source-relation/M1 courts.

## Mission

Qualify only the execution evidence missing from the HQ231 F7 repair return.

Do not alter F7 semantics, production code, accepted tests, authority material, or expectations.

## Governed interpreter

Use the governed CPython runtime already used by current Rawlsing local qualification if present:

`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/tooling/python/cpython-3.11.3-macos-x86_64-none/bin/python3.11`

If that exact interpreter is unavailable, stop and report the discrepancy. Do not silently substitute.

Record:
- absolute interpreter path;
- interpreter SHA-256;
- `python --version`;
- pytest version;
- OS/kernel identity;
- exact sparse worktree path;
- `git rev-parse HEAD`;
- `git status --short`.

Use the shared-store law: one canonical object store on the machine and one isolated sparse worktree for this branch. No broad fetch, no branch switching in a shared directory, no uncommissioned merge/rebase.

## Qualification A — exact F7 court

Run the current F7 court:

`rawlsing_next/tests/test_pre553_temporal_comparability.py`

Commit:
- exact command;
- exact collected node-id manifest;
- pass/fail/skip/error counts;
- exit code;
- compact stdout/stderr digest;
- explicit identification/results for the HQ231 custody-transplant witnesses.

Do not assume the candidate's static estimate of 155 tests. Report truthful collection.

## Qualification B — source-relation owner court

Run:

`rawlsing_next/tests/test_pre553_source_relations.py`

Record the same exact evidence.

## Qualification C — F7 historical M1 regression court

Run:

`rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`

Record the same exact evidence.

## Qualification D — combined commanded surface

Run exactly with the governed interpreter:

`PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=. <GOVERNED_PYTHON> -m pytest -q -p no:cacheprovider rawlsing_next/tests/test_pre553_temporal_comparability.py rawlsing_next/tests/test_pre553_source_relations.py rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`

Record exact aggregate counts and exit code.

## Hostile witness requirement

The executed F7 court must actually include and pass the new discriminating custody witnesses, including:
- source→empty-victim transplant;
- `object.__setattr__` attack on returned diagnostic/custody-like state;
- reflection-level recovered loader/ledger/sealer attack if present;
- visible `_by_ref` / `_by_key` / `_registry` replacement immunity;
- lawful positive cross-universe service;
- fail-capability against the actual authenticated custody seam.

If any expected witness is not collected, report it as an evidence gap rather than smoothing the result.

## Zero-mutation proof

Prove against startup tip:
- no production file differs;
- no accepted test is edited;
- only commission and evidence/return artifacts are added.

## Allowed dispositions

- `F7_RUNTIME_QUALIFIED__READY_FOR_FINAL_HQ_ADJUDICATION`
- `F7_RUNTIME_PARTIAL__NAMED_EVIDENCE_GAP`
- `F7_RUNTIME_DIVERGES__NAMED_FAILURE`
- `F7_RUNTIME_BLOCKED_BY_GOVERNED_ENVIRONMENT`

## Required return

Write only:

`WORKER_RETURNS/PYAT-HQ232-F7-RUNTIME-QUALIFICATION-R1/`

Required:
- `00_RETURN.md`
- `01_ENVIRONMENT_AND_INTERPRETER.json`
- `02_F7_COURT_RECEIPT.json`
- `03_SOURCE_RELATION_COURT_RECEIPT.json`
- `04_M1_REGRESSION_RECEIPT.json`
- `05_COMBINED_EXECUTION_RECEIPT.json`
- `06_ZERO_MUTATION_AND_WITNESS_AUDIT.json`
- `07_FINAL_DISPOSITION.json`

Compact node-id manifests are allowed. No caches, binaries, pyc files, or opaque large logs.

Commit/push only this branch and report exact remote SHA.
