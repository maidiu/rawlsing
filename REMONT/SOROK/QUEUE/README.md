# REMONT local-machine queue — runnable operating discipline

**Trigger:** When the user tells a local agent **“check the queue”**, **“run the REMONT queue”**, or equivalent while in `maidiu/rawlsing`, the agent executes this workflow, including hostile review. No new prompt or recurring user permission is needed for the already pinned sourcefree test/review tasks.

**One-command machine phase (from the repository root):**

```bash
python3 REMONT/SOROK/QUEUE/check_queue.py run --publish
```

This command requires a **Python 3.11** interpreter on `PATH` (pass `--python /absolute/path/to/python3.11` if needed), `git` origin access, and optionally an authenticated `gh` CLI for publishing comments. No GitHub Actions needed. The queue now checks **#1241, #1230, #1222, #1220, #1214, #1210, #1199 in that order** (exact immutable SHAs); **#1241 and #1230** are the newly outstanding author-repaired candidates, while the earlier five have already been independently tested/reviewed on the local machine with scoped or REVISE/HOLD findings, each at the queue's immutable SHA. It uses throwaway detached Git worktrees, verifies the Git branch's actual remote HEAD is still the pinned SHA, verifies each file in the source SHA-256/Git-blob manifest, and runs normal unittest, optimized unittest, pytest, a demo and SQLite two-process cold reopen. It records the exact results under root `LOCAL_COURTS/REMONT_QUEUE/` (already excluded by root `.gitignore`). **Nothing is committed automatically.**

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
