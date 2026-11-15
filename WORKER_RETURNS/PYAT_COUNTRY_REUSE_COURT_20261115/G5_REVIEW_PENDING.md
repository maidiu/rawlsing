# G5 — Independent review received; corrected handoff for recheck

**Status:** `INDEPENDENT_G5_COMPLETED__MEASUREMENT_ACCEPT_SCOPED__HANDOFF_REVISE_CORRECTED__RECHECK_PENDING`
**Review:** `c5a71fcc59a45aa470720159a334ae57f365de11`
**Review path:** `WORKER_REVIEWS/PYAT_COUNTRY_REUSE_G5_20261115/00_REVIEW.md`
**Measurement disposition:** `ACCEPT_SCOPED@SOURCEFREE_REUSE_COURT_REPRODUCED`
**Handoff disposition:** `REVISE_EXACT_DEFECT@G4_OPTIONS_AND_HANDOFF_CLAIMS`
**Production / security / science / new-QUERY-issuer acceptance:** none.
**Self-acceptance:** none.

> The filename `G5_REVIEW_PENDING.md` is retained from the pre-review freeze for stable links; its content is the received-review status, not a pending-review claim.

## 1. What the independent review accepted

The review copied the author probe byte-for-byte, changed only the disposable output root, and reproduced one sequential pass, exit 0, total 178.800 s:

- 100/100 distinct cold operations; 100/100 per-operation fact SHA-256, refs, core ids, denominators and cell-state counts identical.
- 80 exact condition/target cores + 20 governed-weighted measure variants; 100 unique query content hashes; no duplicate raw `(AST, targets)` pair.
- 43,130 row-group reads, 690,080 rows, 576,774,322 compressed-byte metadata sum, 2,363,218,327 uncompressed-byte metadata sum, 94,068 family rows/objects, 29,343 event objects — identical to the author.
- 100/100 exact cold-vs-native, grouped-256-vs-native, grouped-64-vs-native and grouped-256-vs-cold parity.
- Both public cold grouped guards refused with the exact messages; `_DirectReleaseIdentity` missing both hashes; two `indices_for` calls return different index objects.
- Grouped receipts 80 builds + 20 hits at 256; 64 builds + 20 hits + 16 capacity fallbacks at 64.
- 1,000-repeat invocation receipt 1 build + 999 hits, explicitly not distinct operations.
- State probe and 16 focused tests reproduced.
- Independent cold 100-op wall **65.661 s** versus author **51.929 s**, with identical facts/counters; both ambient-contended. The 1,000-distinct projection is **519.29 s author / 656.61 s review**, both over 300 s.

## 2. What the review required corrected

The review accepted the measurement but returned `REVISE_EXACT_DEFECT` for the handoff. This return corrects all of the following; see `CORRECTION_MAP.md` for exact cells.

1. **B was mislabeled as measured.** B has no implementation, no patch and no A/B run in the frozen evidence. It is now a **source-grounded, unmeasured hypothesis** with a measured cold-cost target. A bounded owner-approved implementation measurement is required before any B gain claim or production choice.
2. **#999 context was stale.** The accepted successor `ce7704253f6a2381310c3eb2c7412a2d85c5596c` / review `c18b7e087d5d5b178ed5acc92f9c82250a1743de` exists but is **not adopted** in `9d96a9c…`. The old baseline is a valid-fixture benchmark only, not adversarial security qualification. The finite action is now “adopt/qualify the accepted successor + exact reader/evaluator/file grant”, not “wait for #999 acceptance”.
3. **Wall stability / “three passes” was unfrozen.** 51.929 s is one author pass; the independent pass is 65.661 s under lower preflight load with identical counters. No clean/stable throughput claim. 1,000 distinct is not run; both projections are extrapolations. The 1,000-repeat probe is repeat-only.
4. **Source-open was mislabeled as a tripwire.** Source-open is **INAPPLICABLE** for the sourcefree fixture; the actual real tripwires are `C11Repository.__init__` = 0 and `pq.read_table` = 0.
5. **Process-tree RSS was mislabeled as a sampled high-water.** It is `max(before tree snapshot, after tree snapshot, self ru_maxrss)`. The author's tree sample 137,236,480 B versus self 136,503,296 B is a 733,184 B difference, not equality.
6. **Proxy counters were over-promoted.** Row-group read counts and byte sums are metadata-call/sum proxies, not physical I/O or decompression timing. The `_build` share is instrumentation-inclusive, not a full phase decomposition. Object materialization counts are native work, not negative tripwires.
7. **Measurement acceptance was conflated with broader qualification.** Real-measurement acceptance does **not** equal production, security, science, original35, J3/new governed QUERY issuer, optimized-engine or protected-merge acceptance.

## 3. Corrected finite owner action

1. Preserve the existing cold guards; no guard removal, no cold grouped positive, no new engine/store/layout choice, no production patch.
2. Independent recheck of this corrected documentary handoff.
3. If distinct-operation reuse is pursued: adopt/qualify the accepted #999 successor under the exact reader/evaluator/file grant, then authorize one bounded owner-approved B **measurement** (not a B implementation claim). Do not claim B gain before that measurement.
4. A remains narrow measure-variant/repeat grouping; C remains not demonstrated at this scale.
5. J3 governed QUERY issuance remains separate; the 100 queries are TEST_ONLY sourcefree operations.

## 4. Review surface

- `G4_OPTIONS.md` — corrected A/B/C handoff; B hypothesis only.
- `G1_SOURCE_CONTRACT.md` — source contract and #999 chronology.
- `00_RETURN.md` — corrected headline and scope.
- `SELF_CRITIQUE.md` — proxy/contention/qualification limits.
- `CORRECTION_MAP.md` — defect → exact changed cells.
- `evidence/`, `logs/`, `probe/` — frozen author measurement payloads, unchanged by this documentary correction.

No self-acceptance. A distinct reviewer should confirm the corrected handoff and may return `ACCEPT_SCOPED`, `REVISE_EXACT_DEFECT` or `HOLD`.
