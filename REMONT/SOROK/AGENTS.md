# REMONT/SOROK — local agent task protocol

If the user says **"check the queue"**, **"run the queue"**, **"work through the REMONT reviews"**, or equivalent in the REMONT context:

1. Read `QUEUE/README.md`, `QUEUE/CHECK_QUEUE.json`, and current `OPEN_DEFECTS.json` and `.md`. Compare any current local/remote head movement. Do not ask the user to repeat the standing authorization for ordinary sourcefree test/review tasks.
2. Run from repo root: `python3 REMONT/SOROK/QUEUE/check_queue.py run --publish` (or `--python /path/to/python3.11`). Use the **current pinned exact SHA**; stop only each held candidate, continue the rest of the queue. Do not change the frozen candidate to make tests pass.
3. **Do not stop at green tests.** For every candidate lacking an actual distinct review, create a separate detached hostile-review worktree at the *same pinned SHA*, perform a hostile code/first-owner audit and invent/run independent negative/positive probes. The automatic runner deletes only its own temporary test worktree. Save original scripts, results and a comprehensive review of the exact SHA. Use the generated review template; record the verdict with `check_queue.py record-review ... --publish`.
4. Sourcefree `ACCEPT_SCOPED` requires actual author-independent analysis, separate source identity and tests; preserve exact original P070/P071 author conflict. A shared GitHub account is *not* evidence of credential independence. Never automatically grant G5, scientific/human/actor rights or protected receiving.
5. Record all returns in ignored `LOCAL_COURTS/REMONT_QUEUE/` and corresponding PR conversations if `gh` works. Keep the production P/T/E ledger intact, do not promote unresolved defects, and hand new bugs to a **new isolated REMONT repair branch**. Prioritize newest stack first, then older exact heads when distinct historical receiving requires it.

**User instruction phrase "check the queue" authorizes the work here; it does not authorize protected merges, other persons' credential use, destructive repository edits, or an agent to certify its own authored code.** No autonomous background daemon exists: execution starts when the local user invokes the agent.
