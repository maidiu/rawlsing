# REMONT local queue bootstrap — local sourcefree verification

- Executed on 2026-11-20, Python 3.13.5 tool environment (not an R12–R16 Python 3.11 certification).
- Queue controller self-test: **14/14 PASS**. Includes pinned 5-PR head identities and order, malformed/duplicate PR refusal, tampered/missing/out-of-scope source refusal, wrong Python minor-version HOLD, moved-ref HOLD, receipt state atomic writes, failed-status requeue, no review acceptance without separately recorded evidence, and review template HOLD.
- Source-manifest smoke test on actual R16 executable package: **47/47** source/test files match SHA-256 and Git blob manifest.
- Integrated runner smoke: created a throwaway local Git bare remote, committed the real R16 package to a fixture branch, then executed detached worktree, full normal unittest, `python -O` unittest, pytest, 9-event demo, two separate SQLite cold reopen interpreters, and cleanup. **PASS**. Test harness bypassed only the Python-3.11 *version gate* because this test environment provides 3.13.5; it did not assert Python-3.11 compatibility.
- Demo exact last hash: `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363`; SQLite `PRAGMA integrity_check=ok`; separate processes independently reported identical event IDs and hashes.
- Queue controller performs **no automatic hostile source review**, **no acceptance decision**, **no unattended background work**, **no protected merge**, and **no edits to the P/T/E ledger**. An agent responding to “check the queue” is required by `AGENTS.md` to execute independent hostile review and write its own evidence after the runner completes.
- Local GitHub Actions were not used; account billing is known to block runners. The queue is explicitly designed for ordinary local `python3.11`, `git` and optionally `gh`.

**Not yet demonstrated:** This queue script has not run on the user's local Python 3.11 machine or authenticated real private Git remote; its 14 controller self-tests and local Git end-to-end smoke test are author-side engineering evidence only. Actual queued candidate reviews remain pending until executed by a separate local agent.
