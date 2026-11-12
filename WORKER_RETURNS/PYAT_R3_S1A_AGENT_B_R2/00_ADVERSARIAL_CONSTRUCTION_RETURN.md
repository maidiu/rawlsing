# PROGRAMMA PYAT R3 · S1-A only · Agent B bounded adversarial construction

**Provisional disposition:** `READY_FOR_RECEIVING@S2_SOURCEFREE`. **Not independent acceptance.** This is the single additional bounded correction authorized by the R3S stop-and-advance rule for a demonstrated original G2/G4 first-reader / clear-recovery regression. Stop coding and send frozen HEAD for **one genuinely independent nonauthor G5**. No S1-B/C/D/E, W03/W04, protected merge, original35 scientific/issuer/host/actor grant.

## 1. Exact starting contract and opponent provenance

- Controlling original S1-A G1–G5: [Pair 1 #918](https://github.com/maidiu/rawlsing/issues/918); [R3C five-gate law](https://github.com/maidiu/rawlsing/issues/909#issuecomment-6817606383); [R3S mandatory stop](https://github.com/maidiu/rawlsing/issues/909#issuecomment-6817926106). The relevant frozen obligations are source/projection/decoder/authority cache identity, real positive/changed-value/restored I03, hostile negative conservation and bounded cache invalidation/recompute. NOT original35 scientific issuance or 100k pipeline performance.
- Original protected read source: `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Original B #922: `b0ebb531bc61d7ce0435eb6e0a2d85d66f5c3819`; A #926: `4ec042b2139dafabe386b6cdb24a4275d5b816f5`; B #935: `f3c18b4920bebc77e803dcb67abc380c4f9fcaa5`.
- **Immediate opponent** [draft PR #937](https://github.com/maidiu/rawlsing/pull/937) at immutable `29ddbb44a5d30f7bf287e594cee57f360b286e99` (tested code `906ac2875f91664e5f3e0f7280d127b49b48ddf6`). Reconstructed by reading the actual facade and tests before judging the report.
- **This B isolated descendant** [draft PR #942](https://github.com/maidiu/rawlsing/pull/942), `review/pyat-r3-s1a-b-recovery-race-20261112-r1`, born directly from #937 exact HEAD. RED test-only `97b1eba95266cb6dc0340022a35f945aaa2c9b38`; **tested code+test+workflow GREEN `6286ea700a253ff142104f2e3ee62c9352a07644`**. Report/receipt commits after this SHA change only documents. Verify live PR exact HEAD before receiving.
- Changed production blob: `rawlsing_next/pre553_source_backed_c11_facade.py@f29247b33cb78e5f1e620620d6968ab433ce407a`; test blob `rawlsing_next/tests/test_c1_agent_b_cache_differential.py@d94946349e7f353df3f46adf4c60160db022d5c7`; scoped workflow blob `.github/workflows/pyat-c1-agent-b-cache-proof.yml@f740e6a10ac573a9de85d2666d4c4b6c3c25c897`. No other code changed.

## 2. Opponent's valid victories conceded

A correctly proved and repaired first insertion under a previously empty cache key: public `put(key_A, sealed_release_B)` can no longer claim producer provenance merely because both source SHAs match. It correctly preserved my earlier occupied-key conflicting-rebind refusal, one-shot authority handling, Agent A's detached immutable governed input, final TOCTOU checks, the real I03 changed-value and exact restoration, and all C11/I02 original validators. Its 33 focused and 136 preservation tests really exercised those cited cases. This is superior to my #935 first-admission behavior; this B descendant retains it.

No code or scientific owner was reselected. In particular, the nominal source SHA, a hash of governed semantics and an I02 seal are not themselves a competent current-source/measurement-use grant. A did **not** claim that they were, and I do not manufacture that criticism.

## 3. New exact defect established in A #937 — G2/G4 false first-reader refusal

A's `_admit_from_source_backed_producer` split its decision into `if key in self._entries` followed by `self.put(key, release)`. Public `put` rejects first insertion. With two **legitimate, concurrently running** sourcefree producers under the same source SHA, fully identical projection/decoder and valid source events, B can finish first while A is still reading. Once A has independently validated its identical C11, a lawful `cache.clear()` between A's membership check and `put` empties the key. The second producer then throws `SourceBackedC11FacadeError("producer-only cache admission")` instead of delivering its valid I03 fact.

This is not arbitrary hostile Python mutation, a forged authority, different source bytes, or a simulated wrong SHA. It is normal in-memory cache eviction concurrent with one I02-valid producer, violating S1-A's already-frozen **G4 clear/recompute** and **G2 actual first-consumer** requirement. It is **SEV-2 recovery/parity**, with a real downstream refusal (not a false positive or a new scientific claim).

**Executed sourcefree RED:** [Actions #43181257077](https://github.com/maidiu/rawlsing/actions/runs/43181257077), exact test-only `97b1eba95266cb6dc0340022a35f945aaa2c9b38`: **33 PASS, 1 FAIL**. New deterministic two-thread test `test_c1_concurrent_clear_during_legitimate_producer_reinsertion_still_serves_i03` failed specifically `legitimate I03 build refused after clear: [SourceBackedC11FacadeError('producer-only cache admission')]`. It uses real `execute_empirical_query`, not only direct cache key checks.

## 4. Implemented bounded replacement, not a cosmetic wrapper

Only the existing session cache changed. Its `get`, public idempotent `put`, producer admission, `clear` and `entry_count` now synchronize small dictionary metadata via one per-cache `RLock`. The source-backed producer performs one locked **check-and-admit-or-check-conflict** decision: empty slot gets its I02-validated release; occupied slot must match exact release ref, source manifest and replay manifest. It **does not** call public `put` in between these decisions. The occupied-key original object remains intact.

The patch retains:
- A's prohibition on public first insert, with no new credential, authority or persistence layer.
- B's refusal to rebind a valid but semantically different release to an occupied key.
- All semantic preimage, nested freeze, physical/decoder and authority keys.
- I02 source read, validation, compact view and I03 computation **outside the cache lock**; no second engine, extra source open or statistics recomputation introduced by the lock.

The hostile test no longer requires the repaired implementation to execute its former defective `contains→public put` step: it exercises that interleaving if present, then checks the real reader and legitimate clear/recompute on the atomic path. This test change is an oracle correction, not a relaxed assertion about output: a false first-reader refusal still fails it.

## 5. Green proof, restoration and resource custody

**GREEN exact tested commit:** `6286ea700a253ff142104f2e3ee62c9352a07644`; [GitHub Actions #43182074662](https://github.com/maidiu/rawlsing/actions/runs/43182074662), **SUCCESS**: **34/34 focused PASS** (2.93s) and **136/136 preservation PASS** (85.67s); no failure. Inherited real row-owner R1/Y fact changed support 1 → 0 with denominator 1 and exact restoration still passes. The new real-thread clear/recompute test passes and verifies post-eviction actual I03 equality, not simply absence of exceptions.

The unchanged workflow's original two suites were retained. A new short, scoped, sourcefree G4 step measured: 3 fixture rows; 2 cell-factory calls (cold and after clear, none on warm hit); 1 cache entry after restoration; 224 bytes shallow entry dictionary; five cache-identity hashes 0.029707529s; cold 0.055720088s; warm hit 0.012360418s; clear/recompute 0.063838365s; single-process maximum RSS 170196 KiB (Python and imported libraries included). These are **one three-row runner observations, not statistically stable benchmark averages**, no process-tree/multi-worker measurement, no durable-CAS or 100k/6-GiB evidence. Neither full-source science nor physical economics is promoted.

Commands: existing [workflow](https://github.com/maidiu/rawlsing/blob/6286ea700a253ff142104f2e3ee62c9352a07644/.github/workflows/pyat-c1-agent-b-cache-proof.yml) invokes 3 focused facade suites and 4 preservation suites with `PYTHONPATH=. python -B -m pytest -q -o addopts='' -p no:cacheprovider`; full commands/results and machine-readable gates in [01_PACKET_RECEIPT.json](01_PACKET_RECEIPT.json). 

## 6. Accusations rejected / shared assumptions re-examined

- **Rejected:** A's first-insertion correction was merely cosmetic. It protects the normal public API, and its I03 poisoning test demonstrates a real false-fact risk; retain.
- **Rejected:** A's deep freeze is undone by an ordinary callback changing an external mapping. Its detachment closes that mode, and inherited mutability/restore tests remain green.
- **Rejected:** A's private Python method must be a cryptographic capability. Neither the frozen S1-A contract nor A's claim establishes that. Arbitrary malicious in-process reflection is a separate trust boundary, not a defect automatically chargeable to this cache.
- **Shared limitation exposed, not falsely repaired:** B and A both treat caller-declared `ExactPhysicalCellStream.source_sha256` and decoder metadata as scoped cache context. These are not evidence of original35 source-byte authentication or scientific permission. The protected source-qualified issuer and genuine native source-handling requirements remain outside this packet. Adding a semantic authority DB or re-reading all physical cells on every cache hit would not satisfy the selected compact route, and has no demonstrated S1-A requirement.
- **Earlier shared implementation error corrected here:** both B and A fixed local cache identity/admission while allowing concurrent `clear` to turn a validated output into an illegitimate rejection. Single metadata critical sections eliminate this internal split.

## 7. Self-attack, scope, and possible regressions

A mutex per in-memory cache creates a small Python-object overhead and makes the session-cache instance not trivially pickleable. No accepted persistent-cache serialization owner or pickle-based first consumer has been identified; this is **NONBLOCKING_DEFERRED** unless such a consumer is shown. A subclass overriding `put` no longer intercepts internal producer admission; that method is explicitly the external/replay API and overriding it as a mandatory producer hook is not a documented source of science or permission. No supported feature was shown broken; 170 preservation/focused checks are green.

The G4 benchmark measures process RSS and shallow dict bytes, **not** production process-tree peak, hidden retained Parquet bytes, native source rights or full-scale acceleration. Full O(projection size) key hash cost remains; 100k integrated resource gate remains downstream, not a new S1-A finish condition. In-flight source-currentness revocation and native source/host permission belong to the separately assigned current-issuer/source lanes; do not launder them here.

## 8. Exact remaining blockers and receiving state

Engineering `READY_FOR_RECEIVING@S2_SOURCEFREE`; G1–G4 scoped evidenced by source-pinned code, RED/GREEN and strict first-consumer tests. **G5: NOT_RUN.** No true independent third reviewer has accepted #942, and no author self-acceptance is claimed. A GitHub branch is exclusive to this return, with exact source and file CAS verification; external process/host lease registry was not independently observed and no entitlement to protected merge is asserted. Production original35 scientific authority, native source rights, source-read current issuer and 100k resource proof remain separate correctly scoped HOLDS.

**R3S STOP:** This was one justified bounded defect-specific repair after A→B→A. No more A/B hardening should be opened on S1-A absent a reproducible *new* violation of the already-frozen S1-A contract at an actual reader. Send this immutable descendant to one independent G5 court. When accepted at S2, mark `TERMINAL_CLOSED@SHA` and stop; integration is separate.

## 9. Challenge to Agent A and independent nonauthor receiver

Reproduce the RED at `97b1eba95266cb6dc0340022a35f945aaa2c9b38`, including the real threaded clear and the `producer-only cache admission` exception. Freeze to `6286ea700a253ff142104f2e3ee62c9352a07644`; verify that the *same* sourcefree I03 outcome survives both producer scheduling and legal eviction, while wrong first insertion and conflicting occupied-key rebind still refuse. Attack the locked same-key conflict path without forging authority, altering source SHA or overriding private cache memory. Check actual first consumer and preserved slots/decoder/routing/weight cases, not merely whether a counter reaches a new code branch. Reject hypothetical out-of-scope portability or a generalized adversarial Python sandbox as G5 blockers.

If no in-scope SEV-0/1/2 is reproduced, **stop** and request nonauthor `ACCEPT_SCOPED@S2` at the final report-containing HEAD. If a real breach remains, supply one `REVISE_EXACT_DEFECT` with executed input, expected/actual and first reader; no open-ended return to cache hardening.
