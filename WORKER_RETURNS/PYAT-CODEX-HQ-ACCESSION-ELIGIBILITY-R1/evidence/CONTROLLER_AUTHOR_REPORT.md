# R59 — Shared sourcefree controller P0/P0.5/P1/P2/P3 bounded return

**Date:** 2026-10-22. **Workspace:** `/Users/matthewsmith/Desktop/Rawlsing_Controller`
**Branch:** `infra/r59-shared-controller-p0-p2-r1`
**Startup SHA:** `d4d95c13eaa72827c1a4bd34d861ee041a775d8e`
**Remote:** `NOT_CONFIGURED` — no push attempted and none invented.
**P4:** `NO`.
**Terminal grade:** `SOURCEFREE_KERNEL_PASS__REAL_TEST_CLOSED_LOOP_HELD__INCUMBENT_CONTINUITY_UNKNOWN__LIVE_ACTIVATION_NO`.

## 1. Honest boundary

This return builds and tests the durable, non-sovereign sourcefree controller kernel. It does **not** claim full program completion, a native Rawlsing product, actual incumbent HQ continuity, P2 real-worker completion, or P4 activation. No Rawlsing production repository, `.codex/.opencode` credential file, J52/W52 work, R01/R08/R09 code, protected CI, or other worktree was accessed. Only this private local workspace was written.

The actual OpenCode worker/reviewer loop and child agents were held by operator direction. The earlier network-listener permission request was rejected; it was **not retried, substituted, or bypassed**. A22 network isolation is therefore `NOT_RUN`, not a denial claim.

## 2. MAX and startup verification

Observed before implementation:

- Live invocation: `opencode run --model opencode-go/deepseek-v4.1-flash --variant max --format json --file COMMISSION.md -- ...`
- Persisted session model field: `{"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"}`
- Model catalog reasoning options: `effort: low, high, max`
- Session reasoning tokens: `1963`; observed session cost: `$0.00810438`
- OpenCode `1.18.34`; Bun `1.3.13`; Node `20.19.1`; TypeScript `5.9.3`; Codex CLI `0.162.0-alpha.2`; macOS `13.2.1`
- Account quota and remaining budget: `UNKNOWN` (not exposed)
- Git clean start on the required branch at the sealed startup SHA; no remote.

Evidence: `evidence/MAX_VERIFICATION.json`, `CAPABILITY_MATRIX.json`.

**MAX is established** from the exact invocation, persisted variant, provider-exposed effort list, and nonzero reasoning tokens. The provider does not expose a separate per-request effort receipt; that residual limitation is recorded rather than hidden.

## 3. Phase grades

| Phase | Grade | Basis |
|---|---|---|
| P0 | `PASS_PARTIAL` | Local runtime, MAX, model limits, Git start, installed Codex/OpenCode CLIs, sandbox availability. Quota, incumbent IDs, Codex SDK and real documentary anchors remain `UNKNOWN`. |
| P0.5 | `HOLD` | No authorized real same-incumbent Codex probe. Synthetic A17/A18 transport tests pass; this is not incumbent continuity. |
| P1 | `PASS_SOURCEFREE_KERNEL` | Runnable TypeScript/SQLite kernel, schema, CLI, grants, idempotency, leases/recovery, review independence, budgets, kill/pause. 24 scenarios PASS; A22 partial. |
| P2 | `HOLD` | Test-HQ model/effort choice not supplied, actual loop/child agents held, network isolation `NOT_RUN`, P0.5 unknown. No worker or model was selected by the author. |
| P3 | `NOT_AUTHORIZED` | R59 surface is local sourcefree P0/P1/P2. Only synthetic documentary hold fixtures exist; no Rawlsing shadow replay. |

## 4. What was implemented

Code:

- `src/db.ts` — `bun:sqlite` schema, WAL, foreign keys, migrations, HQ/commission/worker/review/decision/inbox/outbox/audit/budget/control/policy/shadow tables.
- `src/kernel.ts` — durable commission state machine, exact idempotency keys, transactional outbox/inbox, leases/heartbeats, crash recovery, orphan preservation, review independence checks, budget stops, pause/kill/resume, adjudication.
- `src/grants.ts` — typed grant registry, immutable hashes, authority-kind checks, revocation/supersession, exact action/path/provider/model/effort matching, fail-closed errors.
- `src/audit.ts` — hash-chained audit events and chain verifier.
- `src/continuity.ts` — A17/A18/A25 synthetic thread classifier; actual incumbents remain `UNKNOWN`.
- `src/sandbox.ts` — macOS `sandbox-exec` profile and file/credential isolation probe. Network probe is deliberately `NOT_RUN`.
- `src/shadow.ts` — unreachable documentary anchors retained as `ANCHOR_UNVERIFIED_NO_AUTHORITY`.
- `src/cli.ts` — `status`, `inspect`, `explain-hold`, `pause`, `resume`, `kill`, `recover`, `audit`.
- `tests/run.ts` + `tests/scenarios.ts` + `tests/harness.ts` — sourcefree scenario harness.

Behavioral guarantees exercised:

- Duplicate dispatch returns the existing worker; one worker per commission revision.
- Duplicate events are deduplicated; un-ingested events fail.
- Wrong SHA, wrong base, unexpected paths, forged receipts quarantine; no acceptance.
- Reviewer must differ from author in HQ, account, thread, and fresh context; stale target and poisoned findings refuse.
- Cross-jurisdiction commissions, technical-delegate overreach, Sorok manual dispatch, J52/W52, stale checkpoints, model fallback, unknown quota, and source-grade laundering refuse.
- Kill leaves running processes untouched and blocks new claims; audit chain remains valid.
- Orphaned live processes are marked `ORPHANED_UNKNOWN`, never reset/killed.
- Two no-delta revisions trigger `portfolio.replan` and `ESCALATED_HUMAN`.
- Restart at reviewer wake yields one worker, one review, one decision, and one budget reservation.

## 5. Tests and exact results

Command: `bun run tests/run.ts` (also `bun run test`)

Result: **24 PASS, 1 PARTIAL, 1 HOLD, 1 NOT_AUTHORIZED, 0 FAIL**.
Machine-readable: `reports/TEST_RESULTS.json`.

- A01 fake HQ → worker → independent reviewer → same HQ: PASS.
- A03 crash STARTING/RUNNING/RETURN_PENDING/HQ_INTAKE: PASS, no duplicate worker.
- A04 duplicate/out-of-order event and unrelated branch: PASS.
- A05 wrong SHA/unexpected changes/forged receipts: PASS, quarantined.
- A06 self-review/poisoned oracle/stale target: PASS, refused.
- A07 cross-jurisdiction and technical-delegate overreach: PASS, denied.
- A08 Sorok manual dispatch: PASS, refused.
- A09 Pyat R56 outside allowlist and J52/W52: PASS, refused.
- A10 unverified MAX/unknown quota: PASS, held; no fallback.
- A11 sourcefree native/N11/N12 claim: PASS, blocked.
- A12 two no-delta revisions: PASS, diagnostic/replan triggered.
- A13 RED severance preserved; repaired candidate passes: PASS.
- A14 user stop/kill: PASS.
- A15 unreachable incumbent: PASS, no fake HQ, queue preserved.
- A17/A18 synthetic continuity: PASS_SYNTHETIC; actual incumbents `UNKNOWN`.
- A19 unresolvable Sorok anchor: PASS, refused.
- A20 model-authored grant: PASS, refused; scoped grant only exact actions.
- A21 expired/revoked/superseded/shifted/provider/stale: PASS, fail closed.
- A22 OS isolation: **PARTIAL** — read/write/fake-credential denial PASS; network `NOT_RUN` after operator rejection.
- A23 restart at reviewer wake: PASS, one worker/reviewer/decision.
- A24 R58/Sorok scoped accepts retain native/auto-launch holds: PASS.
- A25 accession candidate self-promotion: PASS, refused.
- A26 Browser auto transport: PASS, unavailable; local OpenCode cannot impersonate it.
- A27 two independent lanes while one review held: PASS; global stop holds.
- A02 real Codex/OpenCode closed loop: `HOLD` (see §6).
- A16 live slice: `NOT_AUTHORIZED` (P4).

Other checks:

- `bun run typecheck` → PASS.
- `CONTROLLER_DB=.worktrees/cli-check.sqlite bun run src/cli.ts status` → runnable JSON status.

## 6. P2 hold — exact blockers

P2 was **not** run and is not claimed. The exact remaining prerequisites are:

1. An explicit user choice of the disposable **test-HQ** provider/model/effort. The author did not select a model.
2. Authorization to run one actual sourcefree OpenCode worker and one fresh distinct reviewer, sequentially, in disposable subdirectories.
3. Real worker containment, including network isolation. A22 network is `NOT_RUN`; file/credential isolation is PASS.
4. No P0.5 incumbent claim; the test HQ would be a new synthetic test role, not an incumbent.

No child agents or live Rawlsing dispatch were started. Nothing in this return should be read as A02 or P2 success.

## 7. P3 / shadow boundary

P3 is not authorized by this R59 local sourcefree commission. `shadow.ts` records only unreachable documentary anchors (Pyat R58 C1, Sorok rev34 manual dispatch, Sorok appointment) and resolves them to `ANCHOR_UNVERIFIED_NO_AUTHORITY`. No real Rawlsing commission/return chain was replayed. See `GRANTS_AND_HOLDS.json`.

## 8. How to run

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Controller
bun install
bun run typecheck
bun run test
bun run src/sandbox-probe.ts .worktrees/sandbox-probe
CONTROLLER_DB=.worktrees/controller.sqlite bun run src/cli.ts status
CONTROLLER_DB=.worktrees/controller.sqlite bun run src/cli.ts recover
```

Public imports used by tests:

```ts
import { openDb } from "../src/db";
import { Controller } from "../src/kernel";
import { registerGrant, revokeGrant, checkGrant } from "../src/grants";
import { canonical, sha256 } from "../src/canonical";
import { probeSandbox } from "../src/sandbox";
import { verifyContinuity } from "../src/continuity";
import { recordShadowAnchor, shadowHolds } from "../src/shadow";
```

## 9. Artifacts

- `CAPABILITY_MATRIX.json` — versions, MAX proof, limits, grades, costs.
- `INCUMBENT_THREAD_CONTINUITY.json` — Pyat/Sorok `UNKNOWN`; synthetic tests only.
- `GRANTS_AND_HOLDS.json` — anchor/hold map.
- `reports/TEST_RESULTS.json` — exact scenario outcomes.
- `reports/SANDBOX_PROBE.json` — file isolation evidence; network `NOT_RUN`.
- `MANIFEST.json` — file hashes and commands.
- `RESUME.md` — exact next decision/action.
- `evidence/MAX_VERIFICATION.json` — sanitized session/runtime evidence.

## 10. Safe next action

Do not start P2 or P4 from this return. The lawful next step is a bounded user decision naming the disposable test-HQ model/effort and authorizing (or continuing to hold) one actual sourcefree worker + independent reviewer under real network containment. Separately, P0.5 still requires an authorized same-incumbent Codex probe; without it, no incumbent continuity claim may be made.
