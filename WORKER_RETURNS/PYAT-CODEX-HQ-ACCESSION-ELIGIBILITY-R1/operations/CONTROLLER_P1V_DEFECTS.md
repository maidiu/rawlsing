# R59-P1V — exact defects

Candidate `c14d51abf524fb713ea0260db5d2560bb2865a8b`. All probes are in `REVIEW/probes/adversarial.ts` and the exact output is `REVIEW/receipts/ADVERSARIAL_PROBES.json`.

## D1 — CRITICAL — external authority anchor is a caller boolean

`src/grants.ts:78-91` accepts `anchor_verified: true` as sufficient for `HUMAN` and `GIT_ANCHOR` grants; `src/grants.ts:193` re-checks the same boolean. `GIT_ANCHOR` only checks a 40-hex string (`src/grants.ts:84`); there is no pinned issuer-root registry, Git object reachability check, signature/human-act verifier, or independent anchor lookup. The boolean is part of the grant hash (`src/grants.ts:46`) but is chosen by the same caller that registers the grant.

Probe: registered `git:ffffffffffffffffffffffffffffffffffffffff` with `anchor_verified: true`; a commission referencing it authorized to `AUTHORIZED`. The SHA is fabricated and unreachable. This is precisely the R2 §3 / A20 "verified competent immutable anchor vs candidate-owned boolean" threat. It also contradicts `GRANTS_AND_HOLDS.json:4` ("verified authority anchor") and the P1 claim in `REPORT.md:38,48`. The author's A20 test (`tests/scenarios.ts:401-403`) only rejects an `issuer_role` containing `MODEL`; it never tests a fabricated external anchor.

## D2 — HIGH — revocation/expiry/supersession are not rechecked at dispatch or retry

Grant checks happen at `authorize()` (`src/kernel.ts:347-375`). `enqueueDispatch` (`:380-399`), `claimWorker` (`:401-427`), and `retryRecovered` (`:667-679`) do not call `checkGrant` or revalidate the grant. A grant revoked after authorization but before the executable effect is still dispatched.

Probe: `authorize()` succeeded, then `revokeGrant()` succeeded, then `enqueueDispatch()` + `claimWorker()` returned `claimed: true`, state `STARTING`. This falsifies the broad "expired/revoked/superseded ... fail closed" claim in `REPORT.md:62,92` and A21 as written. A21 (`tests/scenarios.ts:413-428`) tests only direct `checkGrant` calls, not post-authorization revocation, expiry, or supersession at launch/retry.

## D3 — HIGH — forged all-passing receipts verify

`recordReturn` stores worker-supplied receipts (`src/kernel.ts:449-462`). `verifyReturn` (`:464-485`) recomputes a digest over those same worker-supplied receipts and compares it with the caller's expected digest; it checks only that each receipt is `passed` and has a 64-hex digest (`:475`). There is no external test-runner receipt, signature, Git artifact binding, or independent evidence source. A worker that fabricates a passing receipt and matching digest is verified.

Probe: fabricated `{name:"fabricated-all-pass", passed:true, digest:sha256("no such receipt")}` with an arbitrary result SHA verified to `VERIFIED_RETURN`. This falsifies the A05 "forged test receipts" claim (`REPORT.md:60,79`) as stated. The A05 scenario only uses a `passed:false` receipt (`tests/scenarios.ts:169-171`), which detects a failed receipt, not a forged passing one.

## D4 — HIGH — reviewer identity is not bound to the reviewer HQ record

`requireReview` (`src/kernel.ts:488-518`) checks that the reviewer HQ differs from the author HQ (`:500`) and that caller-supplied `reviewer_account_ref`/`reviewer_thread_ref` differ from the author record (`:505-506`). It never compares those values with the reviewer HQ row's own `account_ref`/`thread_ref` (the row is only checked for existence/status at `:501-503`). `recordReview` (`:531-543`) then trusts the returned thread ref against the same caller-supplied review field.

Probe: registered `hq_reviewer` with the author's exact account and thread, then supplied fabricated `claimed:fresh-account` / `claimed:fresh-thread`; `requireReview` accepted, and a GREEN self-review returned. This contradicts the "reviewer must differ ... in account, thread, and fresh context" claim (`REPORT.md:61`) and A06's independence presentation. A06 (`tests/scenarios.ts:182-189`) only manipulates the caller-supplied strings; it does not test registry binding.

## D5 — HIGH — stale/unauthenticated return accepted after lease recovery

`markRunning` (`src/kernel.ts:429-438`) takes no lease owner/token. `recordReturn` (`:449-462`) takes no lease owner or attempt token and does not check `lease_owner` or `lease_expires_at`. `claimReview` (`:521-529`) and `recordReview` (`:531-543`) likewise have no reviewer lease-owner check. `retryRecovered` (`:667-679`) reuses the same worker row and increments `attempt` but does not issue a new return token.

Probe: with an immediately expired lease, `recover()` moved the worker to `NEEDS_RECOVERY`; retry moved it to attempt 2 under `scheduler-B`; after a new `markRunning`, a `recordReturn` with no lease identity was accepted and verified. A stale or different caller can therefore complete a worker return. This undermines the A03/A23 crash/lease-recovery claims (`REPORT.md:65,66,77,94`) and the "durable lease/reconcile" P1 claim. Those tests count rows but do not test attempt/lease ownership.

## D6 — HIGH (accession/authority) — arbitrary human prefix and unrelated review appoint an HQ

`appointHq` (`src/kernel.ts:155-179`) requires only that `human_authorization_ref` starts with `human:` (`:164`) and that some completed review id exists (`:166-167`). There is no external human-act verifier, issuer/role check, domain match, candidate linkage, or review-target relation.

Probe: a completed TEST review plus `human:not-a-real-act` appointed new `hq_fake_pyat` domain PYAT as `incumbent: true`. This contradicts A25's "actual human appointment" presentation (`REPORT.md:96`) and the "typed, verified" authority claims. A25 (`tests/scenarios.ts:495-503`) tests only a model-prefixed human ref and a missing review; it never exercises a syntactically valid arbitrary `human:` value with a real review.

## D7 — MEDIUM — fixture grant can carry native source grade and ADOPT

`registerGrant` restricts `TEST_FIXTURE` grants only to domains INFRA/TEST (`src/grants.ts:78-80`); it does not restrict `source_grade` or couple actions to sourcefree grades. `checkGrant` (`:188-207`) checks equality with the requested grade, so a fixture grant declaring `ORIGINAL35` accepts an `ADOPT` request.

Probe: `TEST_FIXTURE`, domain TEST, `source_grade: ORIGINAL35`, action `ADOPT`, path `native/result` passed `checkGrant`. The commission layer still blocks ORIGINAL35 commissions (`src/kernel.ts:273-274`) and native claim flags (`:555-560`), so this is not a demonstrated full native acceptance path. It remains a grant-policy/source-grade-laundering defect in the primitive that the kernel exposes.

## D8 — HIGH (durability) — lifecycle transitions are not crash-atomic

Several state changes span multiple statements without a transaction:

- `authorize`: `reserveBudget()` at `src/kernel.ts:375` then state transition at `:376`; a crash or later failure can leave budget spent with the commission still DRAFT. The DRAFT check/authorization is also outside a write transaction, so concurrent authorizers can both pass the check.
- `claimReview`: review update at `:524-526` then commission transition at `:527`.
- `requireReview`: review insert at `:509-516` then commission transition at `:517`; a crash leaves a review the recovery path does not reconcile.
- `verifyReturn`: worker update at `:483` then commission transition at `:484`.
- `adjudicate`: multiple state transitions, revision-ledger/outbox writes, and decision insert at `:561-589`; a crash can leave ACCEPTED_SCOPED without a decision or an intermediate state.
- `recover`: query/update loops at `:623-665` are not one transaction.

The author's A03/A23 tests only check row counts and do not fault-inject between these statements, so "crash recovery" and "transactional" claims (`REPORT.md:38,47,66,94`) are not established. `claimWorker` itself is transactional, but that does not cover the other lifecycle paths.

## Claim/test mismatches (not separate kernel defects)

- A04 (`tests/scenarios.ts:117-137`) does not test out-of-order processing or an advanced unrelated Git branch; it tests a missing event, duplicate ingest/dispatch, and a wrong result SHA.
- A13 (`:294-309`) does not repair the same candidate; it uses a different commission.
- A27 (`:519-538`) uses two separate in-memory databases, not one controller with two noncolliding lanes.
- A22 remains PARTIAL (`REPORT.md:93`); network `NOT_RUN`, fake credential is a fake sibling file, no real worker containment.
