# R59-P1V — independent hostile review return

**Verdict:** `REVISE_EXACT_DEFECTS`
**Scope:** P1 sourcefree kernel only. No deployed authority, no P2, no P3 replay/implementation, no P4.
**Review startup:** `1e1156b0a6d432a324af43d5c686789546f398cf`
**Immutable candidate:** `c14d51abf524fb713ea0260db5d2560bb2865a8b`
**Branch/worktree:** `infra/r59-p1-independent-review-r1` at `.reviews/r59-p1-independent-review`
**Reviewer identity:** separate OpenCode session from the author; same user-approved OpenCode account is disclosed, not account separation. Observed transport: `opencode-go` / `deepseek-v4.1-flash`. MAX is the commissioned variant and is supported by the author's sanitized evidence, but this reviewer did not independently read the provider session DB or obtain a per-request effort receipt. Session ID: not exposed to this reviewer. No silent downgrade is claimed.
**Remote:** `NOT_CONFIGURED`. No push attempted.

## 1. Independently reproduced

| Check | Result | Receipt |
|---|---|---|
| Author suite `bun run tests/run.ts` | `24 PASS / 1 PARTIAL / 1 HOLD / 1 NOT_AUTHORIZED / 0 FAIL`, exit 0 | `receipts/REPRO_SUITE.txt` |
| `bun run typecheck` (`tsc --noEmit`) | PASS, no diagnostics | `receipts/TYPECHECK.txt` |
| Manifest exact-32 claim | PASS: 32 manifest entries + `MANIFEST.json`; all hashes/sizes match; no unlisted candidate file | `receipts/MANIFEST_CHECK.json` |
| Local/sourcefree character | PASS: probes used `:memory:` databases, no network, no Rawlsing source, no credentials | `receipts/ADVERSARIAL_PROBES.json` |

The author's green suite is real but narrower than the claims it is used to support. Reproduction does not rescue the defects below.

## 2. Material defects found

Seven probes used the candidate's public API against `src` at the exact candidate SHA; no candidate file was edited. D8 is an additional source-level durability finding. Exact probe output: `receipts/ADVERSARIAL_PROBES.json`. Details: `01_DEFECTS.md`.

1. **External authority anchors are not verified.** A fabricated unreachable `git:` anchor plus caller-supplied `anchor_verified: true` was accepted and authorized a launch. There is no external/pinned issuer-root or reachability check; `anchor_verified` is a candidate-owned input boolean. This is the exact R2 §3 / A20 threat and contradicts `GRANTS_AND_HOLDS.json`'s "verified authority anchor" claim.
2. **Revocation is not rechecked at the executable effect.** A grant revoked after `authorize()` but before dispatch was still claimed by a worker. `claimWorker`, `enqueueDispatch`, and `retryRecovered` do not recheck the grant; supersession/expiry-at-launch have the same gap. This contradicts A21's broad "revoked/superseded fail closed" claim.
3. **Forged all-passing receipts are accepted.** The verifier checks only caller-supplied receipt-digest consistency and 64-hex shape; a fabricated `passed: true` receipt with an arbitrary digest verified to `VERIFIED_RETURN`. This falsifies the A05 "forged test receipts" claim as stated.
4. **Reviewer identity can be spoofed.** `requireReview` compares caller-supplied account/thread strings only with the author HQ, never with the reviewer HQ's recorded account/thread. A reviewer HQ registered with the author's own account and thread, plus fabricated "fresh" strings, produced a GREEN `REVIEW_RETURN`. This contradicts the claimed account/thread independence guard.
5. **Lease/attempt recovery is not bound to the return.** After expiry, recovery, retry to attempt 2, and a new `markRunning`, an unauthenticated `recordReturn` was accepted and verified. `markRunning`/`recordReturn`/`recordReview` take no lease-owner or attempt token; `heartbeat` is the only owner check. This undermines A03/A23 crash/lease recovery claims.
6. **Human appointment is not externally verified.** An arbitrary `human:not-a-real-act` string plus an unrelated completed TEST review appointed a new PYAT "incumbent" HQ. This contradicts A25's "actual human act required" presentation.
7. **Fixture grants can carry native grade/actions.** A `TEST_FIXTURE` grant in domain TEST with `source_grade: ORIGINAL35` and action `ADOPT` passed `checkGrant`. The commission-layer still blocks ORIGINAL35 commissions and native claim flags, so this is a grant-layer/source-grade-laundering defect rather than a full native acceptance path.
8. **Lifecycle state is not crash-atomic.** Budget reservation, commission/review/worker transitions, review insert, and decision insert are separate statements outside one transaction in several paths (`authorize`, `requireReview`, `verifyReturn`, `claimReview`, `adjudicate`); recovery does not reconcile all split states. This is a source-level P1 durability defect, additional to the probes.

## 3. Green tests that do not prove their titles

- A04 does not test out-of-order event processing; it tests a missing event, duplicate ingest, duplicate dispatch, and a wrong result SHA. The "advanced unrelated branch" evidence is actually a result-SHA mismatch.
- A06's "poisoned oracle" only tests a findings-digest mismatch, not a poisoned expected-result oracle. Its account/thread check is the spoofable caller-string check in defect 4.
- A13 does not repair the same candidate; it creates a different commission and accepts it.
- A20 does not test a fabricated external anchor; it only rejects an `issuer_role` containing `MODEL`.
- A21 tests direct `checkGrant` for revoked/superseded, not revocation/supersession after authorization and before launch (defect 2).
- A25 tests only failure-looking inputs; it does not exercise the arbitrary-human-prefix plus unrelated-review success path (defect 6).
- A27 uses two separate databases/controllers, so it does not demonstrate two noncolliding lanes in one controller portfolio.

## 4. Bounded results and retained holds

- **A22:** PARTIAL. File read/write denial against a sibling fixture directory under `sandbox-exec` was reproduced. Network is `NOT_RUN`; the rejected listener/probe was not retried or substituted. The "fake credential" probe is a fake file, not a real credential-store path. No OS-level worker containment, credential scoping, or network denial is proven.
- **P2:** HOLD, not attempted. No worker/model/reviewer was launched by this review. A fake-HQ simulated lifecycle is not real Codex/OpenCode transport or a real child-process crash.
- **P0.5:** UNKNOWN/HOLD in the author return. Synthetic continuity is not incumbent continuity; this review does not claim it. The current director P0.5 same-ID read PASS / active-writer REFUSE is not treated as impossible or unauthorized.
- **P3:** `NOT_RUN / NOT_REACHED`. R59 permits documentary shadow, but actual anchors were not loaded. The author's `NOT_AUTHORIZED` label is more restrictive, not a defect; it is not evidence of a P3 pass.
- **Native effects:** none accepted. No original35/N11/N12, Sorok native, protected CI, J52/W52, R01/R08/R09, Browser auto transport, live Rawlsing dispatch, or P4 activation was performed.
- **Candidate integrity:** no candidate source/test modification by this review; no author worktree writes; no credentials read.

## 5. Return

`REVISE_EXACT_DEFECTS`. The candidate is not accepted even at `ACCEPT_SCOPED_TEST_ONLY_KERNEL` because the defects touch the kernel's central fail-closed grant, independence, receipt, and lease semantics. A new immutable candidate and fresh review are required. This return does not prescribe a replacement architecture or code patch, and it does not adjudicate the author's scientific/product authority.
