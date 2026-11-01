# Selective fan-in candidates

**Rule:** no merge, PRE-MAIN mutation, source issuance, native code or self-adoption.
A candidate is fan-in eligible only with a named current receiver, exact owner,
positive/fault tests and independent review. None is integrated here.

## 1. ADAPT — HQ282 durable batch / V2 consumer

**Candidate:** B01D `ef93f014...` + B01E `92cb2534...` + P01 `3f91dc22...`.
**Why:** current batch runner is an in-memory scheduler with deterministic
retry only when receipts are supplied. It has no durable write-ahead checkpoint,
no crash/restart recovery, and `execute_issued_workload` explicitly rejects
`prior_receipts`. B01D proves a real SIGKILL after a durable side effect but
before COMMIT leaves `UNKNOWN_OUTCOME`/HELD; P01 exercises 25 sourcefree
integration/consumer tests and three actual Field Forge products in its branch.

**Exact fan-in prerequisite:**

1. A named current durable batch consumer (not a test and not a branch-only P01).
2. Owner approval to port only B01D/B01E/P01; no current owner file rewrite.
3. Exact source-free tests:
   - real process kill after side-effect before COMMIT;
   - duplicate replay and completed-retry refusal;
   - partial checkpoint and resume with no-drop;
   - concurrent writer/lock exclusion;
   - wrong source/release, forged caller idempotence proof, stale release;
   - consumer result and replay identity.
4. Independent review of the exact ported SHA; no author self-review.
5. No source/scientific issuance and no exactly-once external-effect claim.

**Disposition:** `ADAPT_REPAIR_CANDIDATE`, not fan-in ready.

## 2. RETAIN — R61 grammar and bundle workload

Current grammar is R8-repaired and passes 32/32 tests. Current bundle workload
passes 16/16, including R5 capture rejection. Retain at test/owner scope. Do not
re-port the R7/R4 branch code. No fan-in until a current production consumer is
named.

**Disposition:** `CURRENT_RETAINED`, no fan-in candidate.

## 3. HOLD — R61 evidence binding

The authenticated evidence cache is absent current. It has one bounded R7-AF-01
defect (`LEGACY_BINDING_PINS_REQUIRE_MIGRATION` lost on resolve-cache replay) and
no consumer. If a current cache receiver is ever named, port the exact module and
fix that refusal; otherwise retire the branch-only cache.

**Disposition:** `HOLD_UNPROVED`, no fan-in.

## 4. HOLD — R61 production binding / source-read admission

R136 records six blocking findings: no actual native positive, unbound query/
source authority, unbound descriptor, undemonstrated predecode permission order,
undemonstrated discovery, and overstated tests. R140 adds synthetic transport
only, not source or production authority. Do not fan in.

**Disposition:** `HOLD_UNPROVED`, no fan-in.

## 5. SUPERSEDED — S06 trusted release replay wrapper

Current B5 lifecycle already owns exact event authority/rule, checkpoint export/
restore, replay identity, current/as-of and invalidation. S06 is a standalone
caller-trusted wrapper (`trusted=True`, nonempty token) with no current B5/M2
integration. It should not be ported. External custody, if ever required, needs
a new owner extension with independent authentication.

**Disposition:** `SUPERSEDED_PROVED`, no fan-in.

## 6. No speculative patch

No limited sourcefree patch is applied in this lane because every candidate
requires either a named current receiver or a multi-module owner port, and the
task forbids manufacturing a receiver. The only actionable next move is the
HQ282 receiver/owner decision above.
