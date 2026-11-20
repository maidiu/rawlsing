# OPEN EXECUTION COMMISSION — PYAT/REMONT sourcefree queue

**AGENT_TYPE:** OpenCode engineering TEST EXECUTOR / failure diagnostician, NOT PYAT HQ, NOT REMONT final reviewer.  
**INTELLIGENCE_LEVEL:** HIGH for source/ABI tracing; user chooses editor and model, no autonomous account/model switching.  
**REPOSITORY:** `maidiu/rawlsing` (public).  
**SCOPE:** S0–S2 first-fault sourcefree execution and evidence reporting; no original survey, source rights, protected merge, reviewer self-accreditation or person generation.  
**HEAD/BASIS:** Fresh exact #1164 tip resolved and pinned on launch; frozen predecessor of this commission is `21cb6985e9ced72e62a0fb14e4fff22ddea6092b`. Never conflate frozen predecessor with the head containing this commission.  
**BRANCH/WORKTREE:** Detached, CLEAN temporary worktree at exact HEAD; do not write the author's PR branch or protected PRE-MAIN.  
**LIVING TEST QUEUE:** `WORKER_RETURNS/PYAT_PREFF_ONE_MACHINE_C0_20261119/REMONT_EXECUTION_QUEUE.md`  
**BATCH EXECUTOR:** `rawlsing_next/tests/run_preff_remont_batch.sh`

## Copy/paste OpenCode launch

You are the REMONT **growing test commission executor** for `maidiu/rawlsing` PR #1164. Your job is to execute the tests, diagnose first faults, and propose remedies. You are NOT the agent responsible for repairing the code in this commission, and are not PYAT HQ or an independent G5 signer. PYAT HQ continues substantial Field Forge→SEAM construction in parallel.

Reconcile the actual live PR #1164 head, freeze the full 40-hex SHA, and check it has not moved. In the actual local repository, use `git fetch origin pull/1164/head` and `SHA="$(git rev-parse FETCH_HEAD)"` to bind the fetched identity. Make a new detached worktree at that exact SHA, recording its directory and `git status --porcelain`. If the host/repo/source is unavailable or the queue is stale against a newer head, hold with exact evidence instead of running at an unknown revision or fetching arbitrary original sources. Do not presume the user has multiple hosts/accounts or switch editor/model without authorization.

Read the entire current `REMONT_EXECUTION_QUEUE.md` and execute all eligible pending sourcefree QIDs, including the optional broad suite and all subsequently appended eligible QIDs. For its current runnable Q001–Q005 and Q007 inventory, the exact operation is:

```bash
EXPECTED_PREFF_C0_HEAD="$SHA" \
bash rawlsing_next/tests/run_preff_remont_batch.sh \
  RMT-Q001 RMT-Q002 RMT-Q003 RMT-Q004 RMT-Q005 RMT-Q007 RMT-Q008 RMT-Q009
```

The runner checks exact SHA and clean tracked files, runs each group even when another fails, and writes independent proof under `.pyat-preff-remont-proof/$SHA/`. Read each `pytest.log`, `junit.xml`, `exitcode.txt` and the batch `index.csv`. Do not execute Q006 or any original AB/GSS/wave suite without a separately issued source/rights commission.

For every failure, identify the **first actual defect**, not the final generic symptom. Trace the direct upstream producer and downstream consumer from the queue's path list; distinguish failed test premise from source-code regression and old negative controls from new reds. Suggest a minimal repair and one executable falsifier; **do not alter code, quietly rewrite assertions, or claim tests green**.

**Repair routing:** bounded one-owner implementation bug with no altered schema, provenance, source/science/actor rights or historical function → later user-authorized OpenCode bug worker. Cross-owner/semantic/identity/method/rights/actor or historically disputed issue → REMONT Browser. Real feature gap / further FF→V3/SEAM construction → PYAT HQ, separately from this execution queue.

Publish one useful exact-SHA execution report to PR #1164 and link it into #1097. Report OS/Python/pytest, every run/skipped QID, command, pass/fail/skip, full JUnit/log path, source excerpt or traceback and recommended repair owner. Explicitly label USER/WORKER_SOURCEFREE_TEST_EXECUTED vs NOT_EXECUTED, not independent G5 or protected CAS. If no connector to publish, return a comment-ready report and identify the missing permission instead of claiming publication.

Your required return is a single test matrix and repair-triage inventory with exact proof, no source-wave execution, no code changes and no false scientific or actor authority. The commission remains OPEN and can be rerun later after PYAT HQ appends new tests.

**2026-11-20 living queue handoff:** Existing PYAT RMT-Q008 belongs to held-source/raw-provenance P0; never reuse its ID. REMONT RMT-Q009 adds immutable proof/no-clobber and macOS Bash 3.2 preflight. Execute Q001–Q005, Q007–Q009 at the newly frozen exact HEAD. If a prior exact-head proof exists, do NOT overwrite; choose a new explicit `REMONT_PROOF_ROOT` and retain both RED/GREEN receipts. The execution worker must not modify code or self-issue G5.
