# Supplemental executed Browser court — distinct independent source-free implementation

**STATUS:** BROWSER_ISOLATED_F2_EXECUTED__NOT_I2_REVIEW__NO_ADOPTION.
**ASSIGNED BRANCH:** `agent/rabochii-sorok-r3-hq298-sr-outbox-execution-r1`.
**USER SEALED LAUNCH:** `90f5735cbcb9d7bae37d118cc676a712e4b77fc7`.
**HQ COMMISSION REVISION:** `badd1768df4cb5a4377ee25ba9b0a7ffbd103cda` (advanced branch while work was underway).
**ANOTHER WORKER RETURN FOUND ON BRANCH:** `3c6e63924e03786939c54048aad07e34756e986f` (source files, tests and `00_RETURN.md` already committed). This supplemental packet does **not** overwrite that work or purport to independently review it. Its prototype and execution evidence were produced in a different Browser Python container. Reviewer independence remains unsatisfied.

## Separate concrete execution

- `python -m pytest test_sr_court.py -q --junitxml=junit.xml`: **31 passed in 2.15s** (28 frozen S01–S28 cases, plus 3 distinct crash/access checks); wall-clock command measure 6.20 seconds.
- `python run_court.py`: actual 28-case matrix: **28 executed, 28 PASS, 0 FAIL, 0 NOT_REACHED**; command wall-clock measure 2.58 seconds.
- Distinct immutable source of falsifier cases: `WORKER_RETURNS/SOROK-R3-POSTASTRA-SR-BINDING-OCCURRENCE-SURFACE-R1/03_CRASH_RETRY_GHOST_EVENT_FALSIFIERS.json` @ `99f2e7128a8417dfeaa39468c45ba65f6958c061`, Git blob `782ba75ee94f24908100b1f3464e7035497d546c`. Original case outcomes were read and hand-mapped, **not** claimed auto-imported into runner.
- Included cold-restart process check launches Python subprocess, commits event/outbox and calls `os._exit(79)`; new process reloads and replays same event, cursor remains 1. Other tests inject exact pre-/post-commit and after-client-display-before-ACK checkpoints.
- Actual JSON matrix preserves SHA256 before/after state for each case, observation traces, event and outbox counts, causal cursor; actual JUnit and chronological command log included.
- First preflight: Python 3.13.5, pytest 9.0.2, Node 22.16.0 and Git 2.47.3; Browser filesystem writable. No prior runtime marker, no local repo checkout. Initial prototype had syntax error during pytest collection, corrected; final 31-test and matrix runs passed.

## Archive and extracted contents

`BROWSER_SR_HQ298_EXECUTED_SOURCEFREE_BUNDLE.tar.xz` (Git blob SHA-1 `e233865b1fd2da66bb33de4e021121ef1e72b659`, SHA256 `73a07c93f2fa1559ff8dfae8b513377845e56a936f15189a41b4b8d60e46b063`; 11,620 bytes), includes standalone `sr_prototype.py`, `test_sr_court.py`, `run_court.py`, `28_case_status_matrix.json`, `junit.xml`, `environment_passport_delta.json`, `runner_log.txt`, `COUNTEREXAMPLE_AND_LIMITS.md`, `README_EXECUTION.md`.

Reproduce after extracting archive:
```bash
tar -xJf BROWSER_SR_HQ298_EXECUTED_SOURCEFREE_BUNDLE.tar.xz
python -m pytest test_sr_court.py -q --junitxml=junit.xml
python run_court.py
```

Tested source files' Git blob SHA-1: `sr_prototype.py` `45e2f37b9bf2d0fe73155473fcbe7db1a19b3c0e`; `test_sr_court.py` `1528154f03286cf8b3e85de3a4ec14e948d3cb43`; `run_court.py` `0f5d8107d0d21b649f6560db1dc47656e30322c3`.

## Hard ceilings / falsifying counterexample

Single local JSON `os.replace` groups admitted event, cursor, decision and outbox; it is not a distributed-world transaction, cross-process serialization, or parent-directory fsync proof. After external display but lost ACK, a retry using the same delivery ID can produce a second presentation; the server cannot determine if a human saw the first. **Client display, transport ACK, opportunity to perceive and human perception remain separate.** `human_perceived=UNPROVEN` throughout. No live client transport is actually exercised.

False actor utterance `I quit.` is a true admitted utterance but leaves `employment=fired`. Rejected drafts, invalid material/embodied transitions, unknown participants and missing causal time do not create an admitted event. A prepared user lens cannot manufacture observed speech through a closed door or infer a label from opaque object ID.

**No** imported accepted CAN022/CAN025/ADP019 owner modules, actual actor, renderer model, data source, physical world mutation or N12; no billable model API invocation (0). Observed incremental cash/quota/pricing: UNKNOWN. This packet is a second **candidate test**; an external **I2 reviewer** must separately inspect both branches of evidence and the original S01–S28 semantic alignment before adoption. F2 bounded logical fixture only, no owner-level F3/phenomenal evidence.
