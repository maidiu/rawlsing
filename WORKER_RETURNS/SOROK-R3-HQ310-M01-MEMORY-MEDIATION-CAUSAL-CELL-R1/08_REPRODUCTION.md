# Reproduction and executed command record

From the repository's existing native Git object store, Python 3.11.3 and pytest 9.1.1:

```sh
python3 WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/repro/stage.py
python3 WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/repro/run.py
python3 WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/repro/summarize.py
python3 WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/repro/audit.py
```

Only the assigned return is written. Runtime and caches are ignored. No network or external model is used by the causal runner. `stage.py` acquires exact objects via git show/cat-file, verifies native Git blob preimages (with the actual NUL header), reconstructs the bounded closure, checks final CAN2 bytes against its source seal, and preserves CAN3's published evidence. `run.py` starts a fresh Python process for each suite; it returns nonzero if any suite fails and records actual pytest arguments, exit codes, imports and JUnit counts. `audit.py` verifies all imports/authority guard/prereg custody and creates portable metadata.

Actual scientific execution sequence:

1. Native branch switch at the sealed startup and local Python/pytest probe; complete governing/source reads; pinned CAN3 stage executed to inspect owner APIs. No M01 experiment existed yet.
2. Prospective freeze commit 845edf5d7c9c48b192b631dacf295afa6f587137, before `repro/cell.py` or M01 tests were authored.
3. New implementation and first `python3 …/repro/stage.py`; `python3 …/repro/run.py new`: 92 PASS, stdout preserved in `evidence/initial/new92.log`.
4. `python3 …/repro/run.py`: new 92, CAN3 97, CAN2 author 89, implicated owners 133 PASS. Full suite stdout/JUnit/import receipts retained under `evidence/<suite>/`.
5. Added actual owner-revision stale-state test and serial-reference diagnostic; narrowed corruption exception expectation. No candidate implementation or prereg changed. Executed `python3 …/repro/run.py new` again: **94 PASS**. Final new stdout/JUnit replaced the earlier identical-implementation 92-suite receipts; the initial 92 stdout remains separately retained.
6. `python3 …/repro/summarize.py` verifies the saved 36 cells, all 12 fixed-owner-state history triplets and strict isolated mediator contrasts. `python3 …/repro/audit.py`: **413 final cases**, exact imported blob verification and unchanged guard/prereg/CAN3 evidence. The selected inherited suites were not rerun after the two M01 test-only additions because their inputs did not change.

`03_RESULTS.json` is the final-count authority. Each suite's `execution.json` supplies actual Python command, expanded pytest args, exit code and module `__file__` as a return-relative path plus native blob/SHA256. Exact inherited commit/path identities are in `02_SOURCE_IDENTITIES.json`, resolved and checked by `05_AUDIT.json`. New source native identities are sealed in the evidence commit and included in the final artifact manifest.

For portable privacy, `audit.py` removes only pytest JUnit's host-name attribute. Raw original JUnit bytes remain in ignored local runtime with their hashes in `04_JUNIT_PORTABILITY.json`; testcase identities, counts, timestamps, durations and outcomes are unchanged. This is documented metadata sanitization, not test editing. Published CAN3 original bytes are preserved separately, never sanitized or rewritten by this operation.

The complete synthetic owner data, event bytes, actual history stored/delivered, memory/epistemic transitions, later reads and response-graph commit hashes are in `evidence/new/observations/`. A receipt can be inspected independently of chat. New K3 inaccessible/unknown memory probes are clearly labeled unapplied boundary objects; positive memory/epistemic causal results use actual commits and reads.

The final direct remote check uses `git ls-remote --heads origin` on the assigned branch and compares its result to `git rev-parse HEAD`. Remote custody metadata is committed after verifying the evidence commit; the containing metadata commit is verified again after push and its exact SHA is reported in chat. No PR, adoption or merge is implied.
