# HQ188-A — OpenCode dispatcher/runtime fail-closed repair — R1

**Final disposition: `CANDIDATE_READY_FOR_INDEPENDENT_ACCEPTANCE`**

Terminal: `HQ188_A_DISPATCHER_REPAIR_CANDIDATE_RETURNED__INDEPENDENT_ACCEPTANCE_REQUIRED`

Role: RABOCHII / LOCAL-MACHINE IMPLEMENTER — SPACE BUNNY. This is an
implementation lane. This candidate is **not** adopted, **not** qualified, and
**not** cleared for autonomous publication. Independent hostile acceptance is
mandatory before HQ can adopt it.

| | |
|---|---|
| Worker branch | `agent/rabochii-pyat-hq188-a-opencode-dispatcher-runtime-repair-r1` |
| Commissioned startup SHA (verified against remote before any edit) | `ff7a06694b0391471b8e1223b2f881b3288f529e` |
| Commission "Exact base" | `6820160533859cf8dd283d10c043947dfe1dd5d4` (verified ancestor) |
| **Final remote SHA** | recorded in `07_FINAL_DISPOSITION.json` and verified equal to local `HEAD` before return |
| Repaired dispatcher blob | `f3067208f7a8b8ffc159bdc41c25309e9a14b5cb` |
| Audited (pre-repair) blob | `23b1fcc3c9e52838b4738efa3d6266b61f60df7a` — identical to the audit's, no drift |

## Startup gate (`HQ188-A_GITHUB_STARTUP_VERIFIED`)

Explicit `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` (no blind pull).
Remote worker branch resolved to `ff7a06694b0391471b8e1223b2f881b3288f529e`, matching
the commissioned startup SHA exactly. Commission read from that exact tip. Isolated
worktree created; local `HEAD`, remote ref and clean-tree state all verified before
the first edit.

## What was reproduced, then repaired

All eight audit defects were reproduced against the exact audited blob before repair,
using the audit's own `reproduce-probes.mjs`. Evidence:
`.../OPS-02-03-REPAIR-R1/harness/pre-repair-probes.json`.

| Audit probe | Pre-repair | Post-repair |
|---|---|---|
| P01 UNBOUND commission/acceptance | **accepted** | rejected (`PLACEHOLDER_FIELD`/`NON_FULL_IDENTITY`) |
| P02 missing candidate identities | **passed publication** | rejected; absent identities never compare equal |
| P03 duplicate at capacity | `SLOT_CAPACITY` | idempotent acknowledgement, dedup before capacity |
| P04 corrupt event log | silently dropped, `events=[]` | corruption surfaced, recovery **blocking** |
| P05 queue omits resume bindings | 5 bindings missing | full immutable binding persisted and reconstructed |
| P06 arbitrary ACCEPTED event | derived `ACCEPTED` | requires HQ adjudication receipt |
| P07 Q08 wrong-state map | wrong results accepted | every state discriminates; unknown fails closed |
| P08 launch argv-only | no execution evidence | real launch receipt, exit, session id |

Post-repair: **16/16** (8 audit + 8 additional required cases).

## Property-by-property

**A — fail-closed immutable task binding.** `validateTask` now requires task id, role,
exact 40-hex base, an existing worktree directory, nonempty terrain, frozen
acceptance inputs, commission path **and** a full commission identity, plus model and
reasoning variant as separate fields. Placeholders (`UNBOUND`, `TBD`, …), wrong-length
and non-hex identities are rejected. `requireSameIdentity` refuses to compare when
either side is absent. `verifyCommissionIdentity` resolves the commission blob with
`git hash-object` and fails closed on drift.

**B — acceptance requires adjudication.** A bare `ACCEPTED` event derives
`ACCEPTED_EVENT_SEEN__ADJUDICATION_REQUIRED`, never accepted. Only
`validateAdjudication` — a structurally valid receipt bound to the exact task,
candidate and review with a recognized disposition — reaches accepted state.

**C — git-derived publication gate.** `publicationGate` resolves base/candidate from
Git, derives changed paths from `git diff --name-only` (never from the caller),
enforces terrain from the task binding, validates candidate↔review↔adjudication
identity, and fetches the **actual** remote expected parent immediately before
publication.

**D — durable store, recovery, concurrency.** A single enforced writer lock makes
`append` the only mutation path, eliminating the read-then-append race. Malformed and
torn records are surfaced as a **blocking** recovery state and the store refuses to
append to a corrupt log. Deduplication is decided inside the lock, before capacity
accounting. `recover()` reconstructs exact task/session state from persisted
bindings, not a state label.

**E — real lifecycle and delivery.** `launch` spawns and observes, capturing pid,
argv, exit code, durations, output sizes and the **real** session id parsed from CLI
output. A process exit is recorded as `PROCESS_EXITED_NOT_YET_RETURNED`; `RETURNED` is
written only by `deliverReturn`, which requires a finished launch receipt and a full
candidate identity. `hqInbox` makes completions visible to HQ with no chat copying.

**F — OpenCode invocation correctness.** Verified on this host: CLI **1.18.34**,
`python3` 3.11.3, node v18.14.2. `--model provider/model` and `--variant
reasoning-effort` are separate flags; `--variant` takes `high`/`max`/`minimal`, so the
pre-repair `--variant space-bunny-free` was a category error. Commission content is
delivered with `--file`, not as a pathname in prompt text.

## Three defects I introduced and caught

Reported because they are the same failure family the audit warns about:

1. **`requireSameIdentity` applied sha-shape validation to `task_id`**, which is an
   identifier, not a git object id. This made two publication gates reject for the
   *wrong reason* (`NON_FULL_IDENTITY` on `FX-W1`) while the real gate — stale remote
   parent — was never reached. A passing test would have hidden it. Fixed; both gates
   now reject for their true reasons.
2. **`--file` is a yargs array option**, so a trailing prompt token is consumed as a
   second filename and the run dies with `File not found: <prompt>`. Discovered by
   running the real CLI, not by reading help. Fixed by ordering the prompt first.
3. **My own P07 probe reproduced the Q08 case-mismatch bug** (lowercase result keys,
   uppercase lookups). Rewritten to exercise the real state machine.

Also: `opencode run --help` writes to **stderr** on this host, not stdout, so the
first capability probe truthfully reported all-false. Fixed to read both streams.

## What was demonstrated (real processes, not argv construction)

- **Two fixture workers in distinct worktrees** — both produced real committed
  artifacts (`FIXTURE_OK`), distinct pids `34623`/`34736`, exit `0`, distinct commits
  `a3d9e65…`/`eb1c82b…`.
- **Separate reviewer in a third worktree** — actually ran, produced
  `REVIEW_APPROVE`, distinct pid `34860`.
- **Commission delivered as content** via `--file`, from a Git-bound path.
- **Completion delivered to the HQ queue** — 2 returns visible, 2 awaiting
  adjudication, zero user message copying.
- **Restart/recovery** — before launch (bindings intact) and after completion (launch
  receipts with exit codes reconstructed).
- **Candidate-change invalidation** — review bound `a3d9e65…` presented against
  `aff625d…` → `IDENTITY_MISMATCH`.
- **Competing publication** — remote genuinely moved `a71a7a6…`→`38fde96…` →
  `STALE_REMOTE_PARENT`.
- **Terrain from Git** — `forbidden/nope.txt` → `OUT_OF_TERRAIN`.
- **Corruption blocks recovery** — torn final record → `blocking: true`, honest
  refusal to report clean state.
- **Two genuine OS processes racing** — distinct pids `35438`/`35439`; same task queued
  exactly once with the other idempotent; four distinct processes racing a cap of 2
  yielded exactly 2 queued and 3 clean `SLOT_CAPACITY` refusals; store integrity clean,
  no duplicate keys, all bindings complete.

## Honest limitations — NOT qualified

Recorded in full in `06_LIMITATIONS_AND_UNQUALIFIED_CAPABILITIES.json`. The material
ones:

1. **No OS-level or process isolation is claimed.** Workers shared one host and user.
   Distinctness is distinct worktrees and distinct pids — nothing stronger was shown.
2. **The positive E2E required `--auto`** (auto-approve). Without it, OpenCode
   auto-rejected the fixture write with `external_directory`. Unattended operation
   therefore depends on blanket auto-approval, which is dangerous and must be scoped
   by HQ before any real use. This is a capability ceiling, not a detail.
3. **The reviewers are not independent.** The same model and variant ran worker and
   reviewer roles. Separate worktrees and separate processes are demonstrated;
   reviewer independence is **not**.
4. **`--file` attachments render as faux tool-call blocks**, so an attached commission
   is not a trustworthy instruction channel. A fixture agent flagged this itself as a
   prompt-injection pattern. Content delivery needs its own integrity control.
5. **Single-host, single-user, local filesystem.** No network, no remote runtime, no
   crash-consistent storage guarantee beyond fsync of one write.
6. **Adjudication receipts are fixtures.** The machinery is implemented and tested;
   **no real HQ authority was issued**, and this candidate cannot issue any.
7. The authorising `--model` value was not independently verified against the
   provider's billing/identity record — only that the CLI accepted it and the run
   succeeded.

## Hard holds observed

Zero raw-source access. Zero source locator discovery. Zero warrant issuance. Zero
live C4. `rawlsing_next/**` untouched. No production-semantic mutation. No C7 or actor
work. `HQ_HANDOFF/**` untouched. Not merged into
`integration/pre-main-reconciliation-r1`. No self-adoption. No independent-qualification
claim. Writes confined to the three declared terrain paths; `.pyat-state/` was created
by a CLI probe and **deleted** after being detected outside terrain.

## Next step for HQ

Run hostile independent end-to-end acceptance against this candidate, with particular
attention to limitations 2–4, before any adoption decision. Do not enable unattended
dispatch on the strength of this candidate alone.