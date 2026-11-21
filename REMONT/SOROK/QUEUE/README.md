# REMONT local-machine queue — runnable operating discipline

**Trigger:** When the user tells a local agent **“check the queue”**, **“run the REMONT queue”**, or equivalent while in `maidiu/rawlsing`, the agent executes this workflow, including hostile review. No new prompt or recurring user permission is needed for the already pinned sourcefree test/review tasks.

**One-command machine phase (from the repository root):**

```bash
python3 REMONT/SOROK/QUEUE/check_queue.py run --publish
```

This command requires a **Python 3.11** interpreter on `PATH` (pass `--python /absolute/path/to/python3.11` if needed), `git` origin access, and optionally an authenticated `gh` CLI for publishing comments. No GitHub Actions needed. The queue now checks **#1234, #1241, #1230, #1222, #1220, #1214, #1210, #1199 in that order** (exact immutable SHAs). **#1234** is SORACLE R3 × REMONT R18 integrated first-consumer execution, still COMMITTED_UNTESTED; #1241 and #1230 remain independently outstanding author-repaired candidates. The earlier five retain their historical local-machine scoped or REVISE/HOLD reviews at their immutable SHAs. It uses throwaway detached Git worktrees, verifies the Git branch's actual remote HEAD is still the pinned SHA, verifies each file in the source SHA-256/Git-blob manifest, and runs normal unittest, optimized unittest, pytest, a demo and SQLite two-process cold reopen. It records the exact results under root `LOCAL_COURTS/REMONT_QUEUE/` (already excluded by root `.gitignore`). **Nothing is committed automatically.**

**The command is phase one, not the entire agent task.** After source-identical green execution, the local agent must create **its own detached review worktree at the same exact SHA** (the runner removes only its temporary test worktree), then perform an independent hostile source review on the same exact SHA, author/execute additional negative and positive probes, and fill the generated `LOCAL_COURTS/REMONT_QUEUE/review_templates/prNNNN_SHA.md`. The agent must look for actual new defects, not simply rerun author tests. Source owner, frozen prior RED, historical obligations, other actor/world authority, original P070/P071 author conflict, and conserved first-fault ID status must be challenged. The agent independently writes full raw proof and a bounded `ACCEPT_SCOPED`, `REVISE_EXACT_DEFECT`, or `HOLD` verdict. Distinct execution does not imply credential-independent receiving.

Record completed engineering review evidence:

```bash
python3 REMONT/SOROK/QUEUE/check_queue.py record-review --pr 1222 \
  --reviewer 'independent-agent-id' \
  --independence-basis 'Who wrote this candidate and original P070/71 fixes, and why this reviewer is distinct' \
  --evidence LOCAL_COURTS/REMONT_QUEUE/review_templates/pr1222_7a8a18c153ee.md \
  --verdict REVISE_EXACT_DEFECT --publish
```

`ACCEPT_SCOPED` may only be recorded if machine compatibility passed against **the same source HEAD** and a distinct reviewer actually supplied substantive independent evidence. Even then it is a **sourcefree engineering** verdict, **not** native P2–P6/CAN/ADP, PYAT scientific acceptance, credential-independent G5, or authorized protected receiving. The original P070/P071 author must **not** independently accept their own fixes; independent actor evidence is required. For a missing Python 3.11 interpreter, changed remote SHA, source mismatch, failed tests, or broken SQLite chain, **record HOLD / REVISE and continue to the next candidate**; do not silently update the pinned SHA or mark success.

The runner saves immutable receipt files under `runs/`, separate review records under `reviews/`, and an additive local `ledger.json` index. Subsequent “check the queue” runs **skip previously green exact-head compatibility tests** unless `--force` is given, and instead continue unreviewed hostile tasks. `--pr N` isolates one candidate; `list` shows status; `run --force` reruns. To revise an exact SHA, amend `CHECK_QUEUE.json` on an additive documented source branch after investigating what moved; keep the old SHA receipt immutable. **Do not silently merge, fast-forward, delete worktrees belonging to others, rewrite `OPEN_DEFECTS`, or publish an acceptance from the automatic runner.**

When connected to GitHub, `--publish` attempts to post new test receipts/review evidence to the exact PR. If `gh` is unavailable, preserve the local evidence and flag publication pending—do not invent a successful upload. The agent should summarize only newly discovered defects, failed or held gates, scoped independent review verdicts, and any lost currentness. It should not ask the user to reissue a separate review commission for every candidate.

**Scope:** This queue is additive REMONT research/receiving logistics. It does **not** replace `REMONT/SOROK/OPEN_DEFECTS.md` + `.json`, `PROGRAMMA`, SOROK's `CURRENT_PROGRESS` pair, or the protected branch. It may not modify any frozen code candidate during review. Repairs require a fresh isolated branch with first-fault RED, full integration GREEN and new receiving.


## R17/R18 intake (2026-11-20)

The local-machine agent's completed R12–R16 reviewer ledger is already committed at `REMONT/SOROK/REVIEWS/LOCAL_MACHINE_R12_R16_20261120/LOCAL_MACHINE_VERIFICATION_LEDGER.md` on frozen R17 #1230. It found an independently reproduced P004 selected-means omission and a remaining P018 preflight bypass. **R17 #1230** repairs P018; **R18 #1241** repairs P004. Both are **author-tested and require separate independent hostile receiving**. Earlier R12 and R16 ACCEPT_SCOPED decisions are bounded; R13–R15 remain REVISE, and no blanket succession may be inferred. The new queue entries must not silently overwrite those prior dispositions. For a new PR head, explicitly update the pin only with a new immutable receipt and re-evaluate prior review scope.


## User-authorized SORACLE #1234 joined first-consumer runner intake (2026-11-20/21)

**Frozen SORACLE source:** [PR #1234](https://github.com/maidiu/rawlsing/pull/1234) HEAD **dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b** on branch **agent/soracle-remont-r16-r3-joined-organism-20261120-r1**. The current queue index 0 adds this candidate only; the seven historical entries and defect ledger remain unchanged.

This is **executable runner and independent first-fault review**, NOT a transfer of SORACLE builder ownership, an already-observed SR-P defect, new PROGRAMMA authority or an automatically accepted organism. The frozen joined candidate has no current complete SHA-256 manifest. Its explicit **PINNED_GIT_TREE** identity path checks every Python module and test against the pinned Git tree and recomputes content digests. It must not substitute inherited R3/R18 source manifests as if current.

The runner performs compilation, joined R3/R18/R16/R17/R13 focused courts in normal and optimized Python, complete inherited normal/-O unittest and pytest courts, the baseline SQLite demo with two cold interpreter reopens, and **14 days / 12 beats of two Nadia counterfactual lives** (father SPEAK versus REST), then independently cold-reopens each of their SQLite databases twice. Require a genuine Nadia actor-selected INSPECT, separate acquired cultural histories, stable source/event hashes and persisted child states.

Use the checkout of the **existing SOROK REMONT queue branch on PR #1171** containing these amendments; a stale default-branch controller will not recognize #1234. From that repository root, with Python 3.11:

```bash
python3 -m unittest discover -s REMONT/SOROK/QUEUE -p 'test_check_queue.py' -v
python3 REMONT/SOROK/QUEUE/check_queue.py run --pr 1234 --publish
```

To run all eight queue entries, omit **--pr 1234**; the standing full command remains **python3 REMONT/SOROK/QUEUE/check_queue.py run --publish**. If necessary supply **--python /absolute/path/to/python3.11**. A moved source branch must HOLD rather than silently advance the pin. Without authenticated gh, keep local proof and report PR publication pending.

**OpenCode return:** exact queue-controller SHA and source HEAD, original command exits and logs, compiled/focused/full normal/-O/pytest results, independently checked two-case SQLite chain details, first observed expected/actual difference and source owner, plus independently authored hostile positive/negative evidence where scope warrants. Distinguish P source first fault, T runner/fixture, E authority/currentness; author SORACLE owns ordinary integration repair. Independent REMONT challenge does not self-accept its original repairs or grant source/science/actor/protected receiving.


## 2026-11-21 R18 receiving finalization / moving SORACLE builder handling

**Do not conflate a frozen tested REMONT repair with a moving joined builder.** #1241 R18 remains exactly `a4a495bbb456bd211b4fbdbd29478c0f0052603f` with 296 sourcefree author tests from its original R17 parent `6f2e98433822a4fb1246ff72c388b2e901c6ab7f`. R17 subsequently moved by three descendant commits to `bd023cccea8912913ace132600c69a97b0eb6a44`, adding typed handling of malformed historical event envelopes; its separate sourcefree Python 3.11 court reports **289/289**. The queue now points **R17 #1230** to this new immutable HEAD, and records the old pin. This does **not** retroactively upgrade R18's older embedded storage blob.

**Concrete R18 review falsifier (static first-owner reading, not a falsely claimed run):** R18's `record_activity_afterlife` now preflights every selected project's existence/means, but still tests a **duplicate `event_ref` separately inside each sequential project append**. When project A is selected and clean but B is selected and already has the event, A's history may mutate before B rejects `DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT`. DeepSeek's independent R18 hostile review should execute that exact multi-selection red witness. The later SORACLE joined `activity.py` implements a global duplicate-event preflight; its test/receiving grade belongs only to its own current joined source HEAD, not R18. Keep P004 PARTIAL until source-accurate reviewed repair is received; no new production defect identity is minted on an unexecuted suspicion.

**Builder ownership and queue discipline:** The SORACLE joined #1234 original immutable pin `dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b` was independently run on local Python 3.11.3: 524 tests, 27 FAIL + 51 ERROR; basic joined demo also errored, then the SORACLE builder moved beyond that cut. It is now marked `execution_deferred: true` **for default runs only** (explicit `--pr 1234` remains available for a historical investigation). This prevents automatic redundant reruns and false currentness while SORACLE repairs its own ordinary first RED. When SORACLE freezes a new demonstrably executable candidate, authorize an additive **new exact SHA** with its own receipt; do not silently recycle any historical `EXECUTED_AT_SHA` result. Seven ordinary R12–R18 REMONT reviews remain active in default processing. No independent acceptance, protected merge, science or actor rights are inferred.

The agent may now run `python3 REMONT/SOROK/QUEUE/check_queue.py run --pr 1241 --publish` for R18 and `--pr 1230` for new R17. The full default command skips the deferred SORACLE joined builder and continues R18/R17/older exact-head reviews. The controller edit itself has not been machine-tested in this GitHub-only author environment; run its selftests first on the local Python agent. Historical sourcefree runner results and the 71 P + 6 E original #1171 ledger remain unchanged.
