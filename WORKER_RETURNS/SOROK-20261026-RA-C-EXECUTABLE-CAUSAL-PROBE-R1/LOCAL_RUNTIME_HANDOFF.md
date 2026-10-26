# RA-C exact Mac/OpenCode sourcefree reproduction handoff — NOT EXECUTED HERE

**Do not change models/harness automatically.** The following requires a separately user-selected qualified Mac/OpenCode executor already authorized for bounded sourcefree reproduction, with repository access. This handoff is not a dispatch or native rule license. Run in a disposable archive **inside this RA-C return directory**; do not run `run_s52.py` against the live author branch, because it removes/recreates its own `runtime/` directory.

## Immutable read cuts
- Assigned RA-C branch starts at `5dccb742b00907da7ecb9e11640ea5a56fcb5827`.
- S52 candidate `c821b488b3a9a3f0fa01b1981989cc17af637dc1` (NOT accepted performer; regression target).
- S51 accepted component `2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65`.
- S49 accepted `6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43`.
- S52 exact `run_s52.py` Git blob `34f633fcc85e85d6acc525dd250601c51afc7b88`, `tests/test_s52.py` blob `8c2470405075a833bbc425976780d6a4b0bcdc0c`, `s52/session.py` blob `c347d8a902f4f451852aca1054e9a3cd99d4c3f0`.
- G18 is an **independently required local source** at `/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/candidate/vendor/bp2/vendor/g18`. S51/S52 hard-code this directory in their bootstrap. Verify source/manifest custody on the Mac; if missing/mismatched, HOLD. Do NOT change that import path to a fabricated G18 or run a replacement history.

## Prerequisite read-only checks
From an existing authenticated local checkout, inspect git status and ensure no active worker uses the proposed scratch directory. Do not use the currently active worktree for mutation. Check locally that `git cat-file -e <S52_SHA>^{commit}` succeeds and `git show <S52_SHA>:WORKER_RETURNS/.../s52/session.py` resolves. If absent, fetch the named **existing ref** through the user's authorized git setup. No blanket reset/clean/force operation.

The S52 branch's `s49/bootstrap.py` imports `s48`; S48 imports previous Sorok author closures. Use the original S52 commit's consistent on-tree source, not arbitrary current branches. Import-order verification should list every Python module's `__file__` and compare each against the selected archive plus separately verified G18.

## Actual commands for bounded isolated run
The committed `TEST_SOURCE_AND_LOGS/local_mac_runner.sh` performs gated environment/source checks and creates a disposable archive from only named S39–S52 Sorok return subtrees, not arbitrary raw datasets. Launch with `RAWLSING_REPO=/absolute/path/to/your/authenticated/Rawlsing bash WORKER_RETURNS/SOROK-20261026-RA-C-EXECUTABLE-CAUSAL-PROBE-R1/TEST_SOURCE_AND_LOGS/local_mac_runner.sh` from the RA-C checkout. It intentionally stops if the Mac G18 dependency or pinned S52 object is missing. It logs `python3 --version`, `pytest --version`, source file digests, module origins, command, exit codes and all stdout/stderr under the RA-C return directory.

Run the accepted S52 sourcefree fixture and focused unchanged tests first. Those tests include a **controlled counterpart** and must remain labeled TEST_ONLY even on PASS. Only then run the additional hostile probe `test_s52_postcondition_fault.py` as a **separate forensic diagnostic**, never as accepted product test. It asserts the correct invariant: unauthorized state divergence **must be rejected**. A failed assertion following `warm_ok=true` and `cold_ok=true` confirms S52's remaining RED; don't repair source.

## Interpretation
- `RUNNER_UNAVAILABLE`: no exact closure, missing G18, Python/pytest, package import, or permissions; capture full path and command.
- `S52_BOUNDED_EXECUTED`: current author fixture/tests are reproducible at named source, with outputs. Not CAN010/011.
- `S52_VERIFIER_RED_REPRODUCED`: controlled paid followed by unrelated note permits unauthorized altered B state. One sourcefree integrity defect, not a K1/K2/K4/K8 developmental verdict.
- `SCIENCE_RULE_UNISSUED`: actual learner formation still cannot be instantiated without competent rule. Do not create a fake positive CAN011 mediator or mark K4 pass.
- For K1, K2, K4, K8 later: require one *actual accepted* same-person before→event→admitted formation/NO_CHANGE→later state consumer test, null histories/relations, branch cold and access cut. Log all typed values and source identity; do not swap in isolated S50 pressure-flow.

## Stop conditions
No original respondent data, raw SAV/DTA, paid LLM call, engine rewrite, synthetic positive learner, native source/rule grant, or production adoption. No mutations outside this RA-C evidence/scratch area. Do not commit scratch copies of upstream author code; commit only minimal report/logs and source identity hashes after review. Stop on unexpected dependencies/large compute; report exact blocker.
