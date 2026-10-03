# PYAT HQ190-A — DISPATCHER/RUNTIME HOSTILE INDEPENDENT ACCEPTANCE — R1

**Disposition:** `ACCEPT_AS_SUPERVISED_REPAIR_BASE__UNATTENDED_NOT_QUALIFIED`

**Terminal:** `HQ190_A_DISPATCHER_HOSTILE_ACCEPTANCE_RETURNED__HQ_ADJUDICATION_REQUIRED`

Review branch: `agent/reviewer-pyat-hq190-a-dispatcher-hostile-acceptance-r1`
Commissioned startup SHA: `2185e1dcf8d87acb74fe854a5196e7f2cf79cb6b`
Reviewed target tip: `f522af5a7a01432159830dfbf26325c0e320adaf`
Substantive candidate: `5f9a93af1cc98d75d392794534484e41248efb5f`
Repaired dispatcher blob: `f3067208f7a8b8ffc159bdc41c25309e9a14b5cb`

**Reviewer environment (observed, not invented):** DeepSeek Harness, DeepSeek V4.1 Flash,
standard mode. Node v22.23.3; git 2.39.1; macOS 13.7.8 (Darwin 22.6.0); installed OpenCode
CLI **1.18.34** at `~/.opencode/bin/opencode`.

---

## 1. Bottom line

The repair is a **real, substantial, fail-closed improvement** over the audited prototype.
Every load-bearing gate I attacked — identity binding, commission binding, adjudication
binding, terrain, publication, delivery, corruption recovery — **held**. The worker's own
return is unusually honest and pre-concedes the unattended blockers.

It is **not qualified for unattended source-free orchestration**, and I found one
**reviewer-authored counterexample the worker's own harness did not catch**:

> **The worker-slot capacity invariant is violated under real multi-process concurrency.**
> In 7/12 trials, 6 concurrent processes racing `SLOTS.worker = 2` admitted **3–4** tasks.
> The worker's own evidence claims "four distinct processes racing a cap of 2 yielded
> exactly 2 queued" — that result is **timing-dependent luck**, not an invariant.

Root cause: `submitTask()` performs `slotGate()` and `store.append()` in **two separate
`_withLock` acquisitions**, so admission is not atomic.

That is a correctness defect in an advertised concurrency property, not merely a missing
feature. It is bounded and repairable, so it does **not** make the repair unsound — hence
`ACCEPT_AS_SUPERVISED_REPAIR_BASE`, not `MATERIAL_COUNTEREXAMPLE__REPAIR_CLAIM_UNSOUND`.

## 2. Mandatory startup identity (all verified before any substantive review)

| # | Check | Result |
|---|---|---|
| 1 | `git fetch origin` (no blind pull) | OK |
| 3–4 | review branch == `2185e1dcf…` | **MATCH** |
| 5 | worker tip == `f522af5a7…` | **MATCH** |
| 6 | `5f9a93af1…` is ancestor of tip | **YES** |
| 7 | dispatcher blob at both commits == `f3067208f…` | **MATCH (both)** |
| 8 | isolated review worktree | `review-hq190a`, separate from all other lanes |

**Post-candidate commit lawfulness (verified independently, as required):** the three
commits after `5f9a93af1…` change **exactly one path**,
`WORKER_RETURNS/PYAT-HQ188-A-.../07_FINAL_DISPOSITION.json`. The dispatcher blob is
identical at `5f9a93af1…` and `f522af5a7…`. So the bookkeeping-only claim **holds**.

Candidate untouched by me: dispatcher still hashes `f3067208f7a8b8ffc159bdc41c25309e9a14b5cb`.
`rawlsing_next/**` and `HQ_HANDOFF/**` untouched.

## 3. Acceptance question, answered separately

**(1) Mechanically improved and fail-closed vs the audited prototype? — YES.**
All eight audited defect families are genuinely closed on the paths I could exercise: no
absent-identity equality, no bare-`ACCEPTED` acceptance, Git-derived terrain and
stale-remote-parent checks, blocking recovery on corruption, real launch receipts, and
separate model/variant binding.

**(2) Safe/qualified for unattended source-free orchestration? — NO.**
Three independent reasons, two of them the worker's own honest admissions and one mine:

- **Blanket `--auto`.** The installed CLI's own help text calls it
  `auto-approve permissions that are not explicitly denied (dangerous!)`. The worker's
  positive E2E *required* it. Unattended operation therefore rests on giving an
  LLM-driven process unrestricted tool approval.
- **No containment.** The dispatcher enforces Git/identity/terrain/state law only. It
  enforces **nothing** at OS or process level. Distinct worktrees and distinct pids are
  not containment, and were not claimed to be — correctly.
- **Capacity invariant violated (my counterexample).** Admission is not atomic.

**(3) Acceptable supervised repair base with explicit ceiling? — YES.**
That is this disposition. The gates that matter for a *supervised* lane hold, and the
defects are bounded and enumerated.

**(4) Minimal next repair that changes the answer** — see §8.

## 4. Findings inventory

| ID | Severity | Finding | Status |
|---|---|---|---|
| **R-1** | **Blocking (unattended)** | Capacity invariant violated under multi-process concurrency: 6 procs vs cap 2 admitted 3–4 in **7/12** trials (worker's own test got 2) | Reviewer counterexample |
| **R-2** | Material | `eventKey = task_id\|attempt\|seq` excludes `state`; a legitimate advance reusing a seq is **silently swallowed** | Reviewer finding |
| **R-3** | Material (unattended) | Blanket `--auto` required for any positive E2E; CLI self-labels it `(dangerous!)` | Worker-admitted, independently confirmed from CLI help |
| **R-4** | Material (unattended) | No OS/process containment; dispatcher is pure advisory/state law | Worker-admitted, confirmed by source review |
| **R-5** | Material | `--file` renders attachments as faux tool-call blocks; delivery integrity is prompt-level only | Worker-admitted; **not independently reproduced** (see §6) |
| **R-6** | Minor | Stale-lock reclaim is mtime-only (`>30s`); a live-but-slow writer cannot be distinguished from a dead one | Reviewer finding |
| **R-7** | Minor | `append` fsyncs the log file but never the containing directory; creation is not crash-durable | Reviewer finding |
| **R-8** | Review limitation | Live OpenCode E2E **not independently reproducible in this sandbox** | Environment constraint |

## 5. What held under attack (reviewer-authored, disposable fixtures)

Independently constructed cases — not the worker's harness:

- **Task binding:** 12/12 malformed bindings rejected (`MISSING_IDENTITY`,
  `PLACEHOLDER_IDENTITY`, `NON_FULL_IDENTITY`, `BAD_MODEL_ID`,
  `MODEL_VARIANT_CONFLATION`, `EMPTY_TERRAIN`, `WORKTREE_MISSING`, …); valid binding accepted.
- **Absent-identity equality:** `requireSameIdentity(undefined, undefined)` throws.
- **Commission binding:** wrong blob → `COMMISSION_IDENTITY_DRIFT`; mutated after binding →
  `COMMISSION_IDENTITY_DRIFT`; symlink escaping the repo → `COMMISSION_OUTSIDE_REPO`;
  missing file → `ENOENT`.
- **Adjudication:** bare `ACCEPTED` → `ACCEPTED_EVENT_SEEN__ADJUDICATION_REQUIRED`;
  wrong task/candidate/review → `IDENTITY_MISMATCH`; placeholder decision and unrecognized
  disposition rejected at construction.
- **Terrain:** in-terrain passes; outside, absolute, `..`-traversal, sibling-prefix
  (`out-evil`), empty, and backslash-containing git paths all rejected `OUT_OF_TERRAIN`.
- **Publication (real disposable Git repos):** in-terrain publishes; out-of-terrain
  rejected **from `git diff`**; review bound to another candidate → `IDENTITY_MISMATCH`;
  non-approving review → `REVIEW_NOT_APPROVING`; unresolvable base → `GIT_FAILED`.
- **Delivery:** no launch receipt → `NO_LAUNCH_RECEIPT`; unfinished → `LAUNCH_NOT_FINISHED`;
  placeholder candidate → `PLACEHOLDER_IDENTITY`; candidate-less `RETURNED` is counted as
  undelivered, never as a return.
- **Store:** torn log → `TORN_FINAL_RECORD` + `blocking: true` + append refusal;
  malformed middle record → `MALFORMED_JSON_LINE`; duplicate key deduped inside the lock;
  held fresh lock blocks to `WRITER_LOCK_TIMEOUT` (no silent concurrent write).
- **Concurrent duplicate submission:** 4 processes, same task → exactly **1** QUEUED row,
  3 idempotent acknowledgements. **This one genuinely works.**
- **Invocation argv:** prompt precedes `--file` (array-option fix works); `--model` and
  `--variant` are separate; bad model/variant and missing commission file rejected.
- **CLI facts confirmed from the installed binary:** version `1.18.34`; `run --help`
  writes to **stderr** (worker's fix is correct); `--file` is documented `[array]`;
  `--model` documented `provider/model`; `--variant` documented as *reasoning effort*.

## 6. Reviewer limitations (disclosed, not papered over)

- **Live E2E could not be reproduced here.** The authority sandbox denies writes outside
  the session workspace, and the OpenCode CLI needs to create/rotate
  `~/.local/share/opencode/log/opencode.log`. Observed verbatim:
  `Unknown: FileSystem.open (.../log/opencode.log)`; `touch` in that directory returns
  `Operation not permitted`. So I verified **L2/L4 statically and from CLI help text**,
  and did **not** independently reproduce the `--auto` escalation or the `--file`
  injection rendering. The worker's live-process claims (pids, session ids, exit codes)
  therefore remain **unverified by me** and should be treated as worker-reported.
- **Model/variant identity not independently verified:** I did not run a live model call,
  so the exact resolved provider/model identifier and reasoning variant for the *worker's*
  runs are unverified. My own reviewer identity is recorded in §1.
- **Capacity race is timing-dependent.** Reproduced in 7/12 and 3/12 trials across two
  independent harnesses plus the minimal reproducer; it is real but not every-run.

## 7. Capability ceiling actually justified

Justified: **supervised, single-lane, source-free, local-only repair base**, under the
following ceiling:

- human-supervised only; **no unattended operation**;
- `--auto` must **not** be enabled; if enabled, the lane is uncontained and its outputs
  must be treated as untrusted;
- **one active writer per role at a time**, because capacity admission is not atomic
  (R-1). Multi-worker concurrency must not be relied upon;
- event-`seq` allocation must be single-owner and monotonic, because a repeated seq
  silently swallows state advances (R-2);
- single-host, single-user, local filesystem; the store is **not** a transactional store
  (R-7);
- adjudication receipts are **fixtures**; no real HQ authority exists or can be minted
  by this candidate;
- reviewers are **not** independent (same model/variant for worker and reviewer).

## 8. Minimal next repair that changes the answer

1. **Make admission atomic (required).** Perform `slotGate` **and** the QUEUED append
   inside a **single** `_withLock` scope — e.g. an `admitTask(store, task)` that, under one
   lock, reads records, decides duplicate, enforces capacity, and appends. Add a
   reviewer-reproducible concurrency test that runs N≫cap processes and asserts
   `admitted == cap` over many trials, not one.
2. **Include `state` in event identity, or use a per-task monotonic `seq` allocator inside
   the lock (required).** Either makes a state advance impossible to silently drop.
3. **Add a scoped permission profile (required for unattended).** Replace blanket `--auto`
   with an allow-list covering exactly the task terrain, and demonstrate that an
   out-of-terrain write is *denied by the runtime*, not merely detected afterwards.
4. **Independent reviewer identity (required for unattended).** A different model/variant
   or a different authority must occupy the reviewer role.
5. **Commission delivery integrity (required for unattended).** Move instructions to a
   channel that cannot be confused with tool-call content, or add an explicit
   authenticated-instruction framing the agent is instructed to trust over attachments.
6. Minor: pid-liveness (not mtime) for lock reclaim; fsync the containing directory.

## 9. Answer to "is it safe?"

- **Safe to use supervised, locally, on fake/source-free fixtures, with one writer per
  role? — Yes, with the ceiling in §7.**
- **Safe to run unattended across two workers plus a reviewer? — No.** Blanket `--auto`
  (R-3), zero containment (R-4), and a violated capacity invariant (R-1) each independently
  disqualify it.

## 10. Hard holds observed

Zero raw-source access. Zero locator discovery. Zero warrant issuance. Zero live C4. Zero
production-semantic mutation. Zero C7/actor work. Candidate not modified. No merge into
control. No self-adoption. All fixtures disposable under `/tmp`; only the commissioned
return directory was written inside the repository.
