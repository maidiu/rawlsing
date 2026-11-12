# PYAT C-1 — Agent A reciprocal construction after Agent B

**Grade:** DELIVERED_PENDING_INDEPENDENT_RECEIVING — SOURCEFREE S2 ENGINEERING CANDIDATE. Scientific: HELD; original35/source/host/actor/consent authority: NOT GRANTED. No protected merge, no W03/W04 resumption, no amendment to original C-1 historical custody. MCR-lite applies prospectively; full frozen predecessor contracts remain intact.

## Exact source/custody
- Protected PRE-MAIN frozen input: `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`.
- Agent B's inherited *unchanged* complete candidate: [PR #922](https://github.com/maidiu/rawlsing/pull/922) at `b0ebb531bc61d7ce0435eb6e0a2d85d66f5c3819`. Original Agent A candidate `6cf9dbd4d8883a34de8d3ff75582129e7cf1e18e`.
- Isolated successor branch: `repair/pyat-c1-agent-a-toc-tou-20261112-r1`; [draft PR #926](https://github.com/maidiu/rawlsing/pull/926). No write to either predecessor or protected branch.
- Frozen tested *code+tests* HEAD: `5b55040f3f73f7d9e47a4ff35626a496fa73d439`; the final report-containing HEAD must be checked from GitHub at receiving.
- Modified production path: `rawlsing_next/pre553_source_backed_c11_facade.py`, revised Git blob `96b40af03d0ad6e181b0f28ecd8a4be9535452e9`. Modified original B test path `rawlsing_next/tests/test_c1_agent_b_cache_differential.py`, revised blob `eb80de73b04ab926bf152d71955265fe794d879c`. No second C11 engine, new authority, alternate persistence carrier, or source ingestion changes.

## 1. Agent B's actual victories preserved
1. Prior key relied on nominal projection/source/authority references while omitting semantic rules and respondent binding. Agent B independently demonstrated three RED differences and repaired the full semantic projection key, physical decoder/context partition, and one-shot authority iterable reuse.
2. Agent B's post-repair 26 focused plus 136 preservation tests demonstrated an actual I03 first-reader change on altered respondent ownership, with exact restoration and an unchanged denominator.
3. R157/source-config, source-owned projector, accepted C11/I02 and R03 workload compiler remain existing capital. No new semantic registry, second source engine, or global mandatory Field Forge stage is warranted.
4. Original Agent A's S2 NOT_RUN was a truthful evidence grade; it must not be retroactively presented as an executed falsifier.

## 2. Independent new defect and executed red
A `GovernedC11Projection` is `@dataclass(frozen=True)`, but nested semantic maps such as `ResponseValueRule.canonical_value` remain mutable. Existing `build_source_backed_c11_repository` calculates `source_backed_facade_key` before `cell_iter_factory` runs. A deterministic sourcefree factory mutates the governed response mapping from `before` to `after` during this interval; the I02-validated release can then be placed under the original `before` cache key. The pre-repair code lacks an admission-side postcondition and does not raise.

RED precommitted test-only commit: `487c8220fc7551cef37fe902db7720c8cfa6b33a`. [Independent Actions execution #43164694674](https://github.com/maidiu/rawlsing/actions/runs/43164694674): **1 FAILED / 26 PASSED**. The failure is explicitly `Failed: DID NOT RAISE SourceBackedC11FacadeError` in `test_c1_projection_mutation_during_source_read_must_not_poison_cache_key`, not a malformed fixture or missing test library. Agent B had not covered time-of-check/time-of-use mutation between complete-preimage calculation and cache admission.

## 3. Repair made (not merely proposed)
At `7774ccd2bfa63b6f4b45f5f12dc0c5b9bf13a3b7` the existing facade now rechecks the same *complete semantic projection, source decoder/transport and supplied authority-binding context* immediately before `SourceBackedC11SessionCache.put`. A mismatch refuses rather than storing an I02-valid new result under the old preimage. Warm `cache.get` paths also recheck before serving, preventing an injected callback from changing the projection while the old cache hit is being selected. The repair retains Agent B's full projection hashing, I02 validation, exact C11 identities, I03 engine, and scope-limited physical binding. It adds no new issuer or schema.

At `5b55040f3f73f7d9e47a4ff35626a496fa73d439`, the additional test `test_c1_cache_hit_callback_cannot_change_governed_input_while_serving` injects mutation inside `cache.get`, asserts refusal, and restores the original exact release. The cold-miss test separately confirms the aborted build leaves the session cache empty, then builds the *genuinely changed* projection and establishes a different validated release.

## 4. Executed regression, differential, negative and restore
- [GitHub Actions #43165003484](https://github.com/maidiu/rawlsing/actions/runs/43165003484), at frozen tested HEAD above: **28 focused PASS + 136 broader preservation PASS**, with actual sourcefree pytest executions, not merely format checks.
- [PROGRAMMA integrity #43165003495](https://github.com/maidiu/rawlsing/actions/runs/43165003495): PASS at same tested HEAD.
- Agent B's unchanged I03 changed-value/row-owner and restoration tests remain included in the 28 focused suite. The extra two tests refuse an in-progress changed-projection miss and warm hit. No contradictory claim of independent S3 or original35 performance is made.
- Positive: stable projections reuse the same accepted release. Negative: changed semantic input during construction/lookup refuses. Restoration: original projection admits exact previous release; changed *stable* input builds its own different validated release.

## 5. Criticism adjudication
- **Genuine B victories:** stale semantic key and decoder context partition solved at their demonstrated sourcefree scope; preserve unchanged.
- **False accusation refused:** Agent A did not assert S2 evidence it lacked. Nor does a valid logical C11 identity require a distinct identity solely because decoder metadata changes; physical custody and logical content are separate.
- **Incomplete B victory:** full-preimage hashes at an instant do not guarantee the input remains the same before cache admission or serving. This was measured and fixed here.
- **New potential regression from our fix:** a second complete key calculation on cache hits and misses increases CPU/allocations by an unmeasured O(projection size) factor. We did **not** prove 6-GiB or 100k-economy success, and the optimization cannot bypass the guard without an immutable input/epoch scheme and own mutation/severance tests.

## 6. Unfulfilled obligations (not disguised as complete)
- The source can be maliciously changed and changed back across both checks; this is not transactional external-source verification or an immutable projection object. Cross-thread mutation around the final guard is not proven excluded.
- A separately compromised cache object can still inject a mismatched but sealed same-source release through `put`. This repair rejects time-of-check changes; it does not authenticate arbitrary in-process cache writers.
- Derived disk accelerator work may be produced before a postconstruction mismatch refuses session admission; its own replay/content keys and cold/torn-write guarantees require a separate actual physical court.
- Trusted current issuer/revocation, source SHA authenticity, source/administration semantic identity issuance, QSM applied selection, R157 original35 operation enumeration, and `resume_joined_workloads` completed/partial/absent fresh authorization remain distinct original-owner tasks. Do not overwrite C-2/W03/W04 leases.
- Production C11 persistence/currentness, full all35 cost and actual native source→I03/Batch→Field Forge evidence are NOT RUN/NOT ACCEPTED here.

## 7. Next hostile challenge
1. Use concurrent mutation or mutate-then-restore to try to defeat our postcondition; independently establish whether the original producer accepts concurrent input at all.
2. Poison `SourceBackedC11SessionCache.put` with another same-source validated release; demonstrate wrong I03 output and decide whether the solution belongs in builder-only private cache API rather than another authority.
3. Measure end-to-end sourcefree large projection CPU and peak RSS with and without the postcheck, then investigate a provably immutable canonical preimage/snapshot that avoids repeated full hashing. Do not silently undo Agent B's collision repair for speed.
4. Examine the current true first-reader and current-issuer source cut, independent source-config holder and exactly selected original35 Epre fates. No full scientific-source claim follows from these tests.

**Receiving:** One independent nonauthor review at immutable report-containing HEAD; challenge exact Git blobs, full pytest logs, first consumer, economic downside, and retained failure surfaces. The author neither self-accepts nor merges into PRE-MAIN.
