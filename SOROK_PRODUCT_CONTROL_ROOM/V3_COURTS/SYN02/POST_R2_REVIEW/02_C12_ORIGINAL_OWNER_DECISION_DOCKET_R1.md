# C12 O1 source-owner decision — unsafe fork must not be represented as clean

**Priority RED.** Independent RRP0-R2 review `8df1712b665917b1dbeb1c0d7526830e167b4833` reproduced at actual JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`. Parent perception clocks 10/11, fork cut 10 copies only one; both original `QualifiedC12Store.verify` return `ok`. Current proposed mirror sidecar count-based detection false-cleans substituted perception, `SYNC_HELD`, wrong parent root.

**Only actual C12 BP4/r26e source owner may authorize original code edits and choose**:
- A: transactional perception-inclusive fork (cut max over episode/world/checkpoint/perception; exact copied perception identities/root/count, verified ancestry/root/hashes, direct API and wrapper), plus tests for clock11, same-count substitution, tampered root, fork crash, replay/cold, no phantom suffix.
- B: immediate fail-closed `FORK_HELD` at every original direct/wrapped fork path whenever source clock/perception set/root/ancestry cannot be proved. Do not rely on current count-only sidecar; if sidecar retained, exact base perception identity/hash, actual root, receipt C12 root/clock and watermark CLEAN must be checked.
- C: HOLD code until original owner identified, no clean fork and no F1.1.

No code edit and no storage freeze are authorized by this docket. Source owner must state branch/sha, writer identity, exact permission, protection of legacy accepted receipts, tests and independent reviewer. SCIENCE/Rule A/T and native person remain separate.
