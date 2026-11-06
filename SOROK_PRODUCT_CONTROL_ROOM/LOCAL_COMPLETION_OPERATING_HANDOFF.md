# SOROK HQ finite dispatch and completion return

Operational qualification: 2026-11-01 (America/New_York). Existing HQ: `01a161c5-a44a-7b13-ad50-49e10112874d`; permitted worktree `/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing`.

## Installed route

Source `maidiu/rawlsing-controller`, branch `infra/local-completion-restoration-20261101`, exact commit `64d52127b6a24bab5faf2461d75da5141c3baac2`, `LOCAL_AUTOMATION/HANDOFF.md`. All five installed files matched pinned Git bytes at activation.

- Helpers: `/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/`.
- Machine setup and binding template: `/Users/matthewsmith/.config/rawlsing-controller/sorok-01a161c5/{setup.json,binding.example.json}`.
- Actual bindings, commissions and argv: the same config directory's `jobs/`.
- Current operating receipt: the same config directory's `activation-current.json`.
- Persistent per-job state: `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/`.

## Launch future authorized commissions

1. Establish actual user-authorized scope, permitted worktree and current provider/model/effort. The helpers confer no account, source, science or product authority.
2. Use a fresh job ID and appropriate current grant. Bind the exact worker session; do not reuse spent qualification sessions or touch unrelated jobs. A new session can be allocated without inference using OpenCode's local session.create API; stop any temporary allocation server afterward. The real qualification used a fresh tools-disabled session and explicit `opencode-go/deepseek-v4.1-flash`, variant `max`.
3. Build the exact absolute-executable argv array, with no shell. Import the installed `launch.command_digest(argv)` and put its result in `grant.argv_sha256`. Complete the exact recipient/worktree/session/state-root, grant ID/scope/expiry/job IDs, and matching job JSON. The example binding alone is not authorization.
4. Invoke once: `python3 /Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/launch.py --binding /absolute/binding.json --job /absolute/job.json`.
5. Inspect `launch.json` and `events/ready.json` for the exact recipient and `KQUEUE_OS_FILE_EVENTS_NO_PERIODIC_POLLING`. The per-job supervisor waits for its exact child and atomically writes `completion.json`. The finite observer uses OS file events, attempts one ordinary `codex queue`, and exits. No periodic wake prompts or polling service are needed.
6. On the automatic notification in this same HQ, read the exact completion receipt and actual stdout/stderr. Match job/session/PID/grant/argv and provider terminal output. Record actual intake separately in the job's `hq-intake.json`; a queue acknowledgement alone never proves intake. Decide acceptance only at the demonstrated scope.

Never delete reservations to retry. Inspect and reconcile an ambiguous launch/send under its exact existing job; do not launch or notify again. A known nonzero child exit is a failed process outcome, not success. Queue timeout/nonzero/unrecognized acknowledgement is AMBIGUOUS_HOLD with no automatic retry. A supervisor crash does not prove child exit. Preserve all failed outcomes.

## Actual observed qualification

Harmless notification: job `sorok-notification-qualification-3e37880aea89`, session `LOCAL_NOTIFICATION_TEST_3e37880aea89`, PID68069, exit0, expected marker verified. Queue message `01a19a5a-cd32-7ff3-8ae4-b94eb5524e0b`; actual same-HQ intake recorded in that job's `hq-intake.json`.

Real OpenCode commission: job `sorok-opencode-roundtrip-5c69dd22ed58`, exact session `ses_e65a2fc2cffeNnmFUn19p4oZ83`, PID68726; model-authored operating checklist, no tools or source edits. Exit0, provider terminal `stop`, exact commission ID in returned JSON. Argv digest `f65c48cf4a8fc865ff0ccc9770cb825c2dff0b7402fa40877605f9b6ae50e280`. Queue message `01a19a5d-f89f-7ab3-b6b6-7bf1188c8a01` actually arrived in the original HQ; receipt and actual return were processed here. One notification reservation, observer ready and finished, no human transfer. Full durable custody is in that job directory: `job.json`, `binding.json`, `process.json`, `completion.json`, `stdout.jsonl`, `stderr.log`, `events/`, `model-return.json`, `hq-intake.json`. Raw return SHA256 `15a005ed38b081321b78b26d7dffe7e205f5a29ad0abfb556801cffb248b212c`.

This establishes finite infrastructure dispatch/return, not automatic work acceptance, OS isolation, scientific validity, PROGRAMMA acceptance or acceptance of the old engineering candidate. The returned checklist is advisory: its generic “no activation claimed” statement describes its source packet, not this subsequently observed activation; its ambiguity wording does not turn a known child failure into success or require replay.

## Optional HQ reasoning-level switching

The existing app `send_message_to_thread` tool exposes `model` and `thinking` overrides for a subsequent turn. The completion helpers do not: their ordinary queue message has no override. No reasoning-level switch was exercised by this qualification and no changed host-selected level is claimed. Do not add model turns merely to demonstrate switching or wait for jobs.

Periodic automations remain paused. The former generic-controller repair, historical scenarios, app UI crash and PROGRAMMA/person-science work were not resumed for this activation.


## Current construction dispatch — 2026-11-05 P2

Three actual controller launches extend the independently accepted sourcefree product at `41bf45813fd0adeffd9b54e1306c2022abe96514`; PR #697 is unchanged and unmerged. Current PROGRAMMA reconciliation is `f9b4595a8f6ddb2fe31f7b350f25df2afeef7340` (published isolated patch, not adopted PRE-MAIN).

- `sorok-p2-encounter-lifecycle-20261105-r1` | `codex/sorok-p2-encounter-lifecycle-20261105-r1` | session `ses_e52b17161ffe7omlNtc0EddtAB` | process `77831` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-r1`. Exact commission and binding: controller `sorok-p2-encounter-lifecycle-20261105-r1/job.json` and `binding.json`.
- `sorok-p2-explicit-interval-flow-20261105-r1` | `codex/sorok-p2-explicit-interval-flow-20261105-r1` | session `ses_e52a51ef1ffeNtPTpxKAP6J37a` | process `77835` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-s35-c9r-access-review-r1`. Exact commission and binding: controller `sorok-p2-explicit-interval-flow-20261105-r1/job.json` and `binding.json`.
- `sorok-p2-later-event-continuation-20261105-r1` | `codex/sorok-p2-later-event-continuation-20261105-r1` | session `ses_e52a51c43ffeuVe7ZZhNcga5YP` | process `77840` observed alive with no terminal receipt at dispatch readback | assigned checkout `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/workspaces/sorok-join-e-b-event-review-r1`. Exact commission and binding: controller `sorok-p2-later-event-continuation-20261105-r1/job.json` and `binding.json`.

Scopes respectively: persistent local exit/return with no actor/world mutation; explicit qualified interval activity to later public consequence with no automatic WAIT-as-action substitution; existing S41–S43 later-event producer/consumer continuation. New separate return directories only; no shared product/vendor/PROGRAMMA writes. DeepSeek V4.1-Flash MAX unchanged, existing session-scoped permissions only. Per-job supervisors and completion observers launched. Receive actual results, fan in compatible code on a later isolated integration branch, independently review consequential new boundaries, and write material results through PROGRAMMA. No new native/B-purpose/human/merge authority.


### P2 returns received and next three commissions dispatched

Lifecycle79b90e4a57cbd1b738a9b9484677736d1b6415ab independently ACCEPT_SCOPED_TEST_ONLY at6398888f1d28152b5d29fef816f0bb45e77dd43b (5tests+5probe groups). Intervalbdadbc57c2664d3155a97853422e74b6128261f8 (6author tests) and later-event76fdb624afc7674f088d10c349bfe15ffd0b865a (5author tests) are remote-verified candidates, not accepted. Actual terminal receipts and returns read in this HQ; intake records saved in original controller job directories.

- `sorok-p2-product-fanin-20261105-r1`: launched existing controller/session; PID84916 observed live without terminal receipt; exact prompt and binding in controller job directory.
- `sorok-p2-interval-later-independent-review-20261105-r1`: launched existing controller/session; PID84920 observed live without terminal receipt; exact prompt and binding in controller job directory.
- `sorok-p2-programma-return-intake-20261105-r1`: launched existing controller/session; PID84924 observed live without terminal receipt; exact prompt and binding in controller job directory.

Fan-in scope: one compatible same-root product CLI with lifecycle, qualified interval activity and later-event consumers. Separate independent review checks actual action/perception distinction and source-cut/cold boundaries. Guide worker owns direct affected-record write-through on existing PROGRAMMA branch; no competing guide edits. PR697/protected branch unchanged; no native/human/B grants.
