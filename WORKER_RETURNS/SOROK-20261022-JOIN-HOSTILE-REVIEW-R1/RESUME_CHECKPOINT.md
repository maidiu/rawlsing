# JOIN-V resume checkpoint — final cut c367777

**STATUS:** `FINAL_CUT_REVISE__c367777__PERSISTENCE_ROOT_BRANCH_C12_SOURCE_NOT_PROVEN__AWAIT_NEXT_REPAIR_SHA`
**BRANCH:** `codex/sorok-join-v-20261022`
**FINAL CUT:** `c367777f83367240352c267a2d3750abb7f09397` (read-only detached worktree)
**PRELIMINARY CUT:** `13dfd6bad54ec19b4bdf31159e54fb6052d5440d`
**STARTUP:** `3fe8444b4a0374d95fa9f7e60dd295049a5d3172`
**CONTINUATION:** `141b5fe1e393621862791281e980c450715bbb9a:.../continuations/02_JOIN_V_FINAL_CUT.md`; HQ intake `00_HQ_INTAKE.md`
**WRITE SCOPE:** own return only; no candidate/J/E edit.

## Results against c367777

| Suite | Result |
|---|---|
| Frozen independent positives | 9 passed, 1 intentional E-first import-closure refusal |
| Frozen independent hostiles | 4 passed, 3 failed |
| Targeted final-cut tests | 3 passed, 3 failed |
| JOIN-E own suite | 10/10 passed |
| Inherited J / E / R30A | 8/8, 15/15, 10/10 passed |
| Source manifest | 444/444 verified |

Frozen test hashes were checked first and match `FROZEN_ORACLES.json`; no frozen test was edited. `FINAL_CUT_ADJUDICATION.md` has full details; `evidence/final_cut/` has JUnit and JSON.

## Repaired

- Different-source foreign product root is refused.
- Plain R29P donor root is refused and no longer mutated (`ReadOnlyR31JProduct`).
- Single-sidecar `r31j_source` tamper is refused.
- Moved session root is a typed `COLD_REOPEN_REFUSED`.
- Lawful `fork_alt` continuation works and cold-reopens.
- J-first closure is enforced; E-first is intentionally refused with `IMPORT_CLOSURE_INVALID`.
- B refusal/share with the same A omission is a source-derived consumer contrast; B refusal remains a lawful no-tool/no-target boundary, not a help-accept expectation.

## Still failing / new counterexamples

1. Same-source foreign product root is accepted; source equality is not root identity.
2. Metadata-only branch selection (`root`, frozen `alt`) is accepted; no branch/fork receipt.
3. Double sidecar+meta source tampering is accepted with `verify=true` while C12 `GM01_SOURCE` says `SHARE_TOOL`; meta-to-sidecar equality is insufficient.
4. Missing `session.json` still raises raw `FileNotFoundError`.
5. Orphan product root after session loss still raises raw `RuntimeError: R31J_PREC9_REFUSED...`.

## Next safe move

When human/HQ supplies the next repair SHA:

1. Use an immutable read-only worktree of that cut; do not edit the candidate.
2. Verify frozen test hashes against `FROZEN_ORACLES.json` before running.
3. Run the unchanged frozen positives/hostiles and `tests/test_join_v_final_cut.py` with `SOROK_JOIN_CANDIDATE_ROOT` set to the cut.
4. Run `tools/collect_final_cut.py` for candidate/inherited counts and source manifest.
5. Publish the next adjudication; preserve lawful fork/cold/B-source positives; do not impose cross-root target determinism; no polling, extra worker, or native grant.

## Exact commands

```text
cd WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1
SOROK_JOIN_CANDIDATE_ROOT=<cut>/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_positive.py -p no:cacheprovider
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_hostile.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q tests/test_join_v_final_cut.py -p no:cacheprovider --tb=short
SOROK_JOIN_CANDIDATE_ROOT=... PYTHONDONTWRITEBYTECODE=1 python3 -B tools/collect_final_cut.py
```

## Flight / model

One accountable reviewer on this branch; local OpenCode, user-selected harness; no subagents, provider calls, native operations or model swaps. Remote head is reported after the ordinary non-force push and `git ls-remote` readback.
