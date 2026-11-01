# Selective fan-in candidates — RRIF-D1

**Status:** proposals and contracts only. No merge, adoption, production mutation, source-native execution, permission issuance, actor wake or PREMAIN write. Each proposal requires an independent reviewer distinct from the author and this reconciler. Exact blob identity is not behavioral equivalence.

**No speculative patch was implemented.** The write scope is `WORKER_RETURNS/PYAT_RRIF_D1_20261031_R1/**` only. The only clearly superior C3 repair requires the PREMAIN physical-decoder/R5-codec owner and exact source authority; the other residuals require a real consumer, issuer or lifecycle owner. Writing a test-only wrapper or a production patch here would violate the scope or the authority boundary.

## Candidate table

| Candidate | Lineage | Decision | Why |
|---|---|---|---|
| P-01 | C1 analytical composition | No fan-in | C1-02 is exact current and green; C1-01 is superseded inside the lineage |
| P-02 | C1-M2 release binding | Hold / repair contract | Candidate absent, nonissuing, no consumer, caller provenance unauthenticated |
| P-03 | C3 decoder/R5/G01 | Adapt/repair candidate | D01/D02 are real current losses; G01 behavior present, authority absent |
| P-04 | C3/R9 source broker | Hold / successor contract | Historical code conflicts with PR526; no issuer/role or consumer |
| P-05 | C5/N5 structural context | No wrapper fan-in | Behavior reproduces from current owners; no consumer for the wrapper |
| P-06 | N10E empirical possibility | Provider retained; lifecycle/context repair contract | Provider exact current; lifecycle edges and fixture-context issuer unresolved |

## P-01 — C1 analytical composition

**Source:** C1-02 `bc661188b51e995d9f5d74e55c4e37d2ba358a17` (HQD-2026-10-01-145); C1-01 `5fafb499d53dddadaf8a7b4fd46506e91a09d270` (HQD-2026-09-30-139).
**Affected paths:** none. Current `pre553_analytical_composition.py` blob `604c8d591d4c`, test `2210fc1b4cb9`, higher-order test `c8a83d3deffa`, fixture `0393cc8c17a3`.
**Current receiver:** provider `:35`, analytical state/route `:939`; no production call site.
**Negative tests already current:** R6/R7 exact-key extra-field rejection; C1-02 pairing semantics; stale-ref rejection.
**Action:** no fan-in. If a production C1 consumer is required, a separate commission must name the call site and its negative tests. Do not re-import C1-01.
**Reviewer:** independent C1 analytical owner reviewer if a consumer is commissioned.

## P-02 — C1-M2 release binding

**Source:** F8E `2a4a90ec76d3400f98ba6fd3fd306f6ff977d042` module `36563ddee5b6`, test `1e972bf91992`; F8D `69bb0fc69175b2f6048b00cfa47dc852593798c0`.
**Affected path:** `rawlsing_next/pre553_c1_immutable_release_binding.py` (absent).
**Current receiver:** none. Current M2 release owner `pre553_learned_product_release.py` is imported by `pre553_learned_world_composition.py:40`, but that composition has no production importer.
**Repair contract:**
1. A real C1-to-M2/B5 consumer must be named and called.
2. The caller-supplied C1 result must be authenticated against a competent G1/owner-held source, not merely content-addressed.
3. The candidate must remain nonissuing until a competent external issuer exists.
4. Positive tests must include exact C1 result binding, M2 release construction and B5 stage/register without publication/currentness.
5. Fault/severance tests must include wrong release, changed predicate/query/witness, reverse numerator, risk-member substitution, source substitution, replay-grade overclaim and caller-forged C1 provenance.
**Negative history:** F8F 280/280 with B5 caller-supplied provenance open; F8D's q1/q2 shared risk-set defect repaired at F8E.
**Action:** keep held. No merge or adoption.
**Reviewer:** independent C1/M2/B5 reviewer plus a real consumer owner and issuer owner.

## P-03 — C3 D01/D02/G01 repair contract

**Source:** accepted C3 `30686b185d4ceb2c94f61815ef70d8c8e76255d6`; decoder `d3d828c171ea`, codec `6000a1704d71`, G01 `31a9afd7d91e`; historical C3/R9 return `24847592f6a40fde3c4932d0f26173012c037078`.
**Current code:** decoder `8732e34d0ea3` (PR526); codec `72f8f3c03ed0`; G01 absent; D01/D02 tests absent.
**Affected paths:** `rawlsing_next/pre553_physical_decoder.py`, `rawlsing_next/pre553_r5_codec.py`; G01 only if a receiver appears.
**Current receiver:** `ee_p2x_darwin_stage_backend.py:713` for the decoder; no D01/D02/G01 receiver.
**Required repair (not implemented here):**
1. Add the three accepted exact declared-encoding pairs (`ac0b8bc1 -> BIG5`, `5b703173 -> WINDOWS-1252`, `66252a92 -> WINDOWS-1252`) and the declared-only authority status to the current decoder, without weakening PR526 snapshot custody.
2. Add exact opaque date/time carriage on top of current `72f8f3c`: naive `datetime.datetime`, `datetime.date`, `datetime.time`, fold preserved; timezone-aware values refused; recursive normalization through tuple/list/mapping; no stringification.
3. Preserve `expected_source_sha256`, `/dev/fd` read, stability check, unlink/close, and the current compatibility lane.
4. Do not transplant the historical decoder/codec wholesale and do not replace PR526 with the old raw-path route.
5. G01 authority wrapper only if a current C11/receiving owner calls it; it must remain byte-exact `31a9afd7d91e` if reinstated.
**Positive tests:** declared BIG5/WINDOWS-1252 exact SHA/config admission; opaque naive date/time roundtrip preserving type and fold; nested normalization; current SAV representation lane unchanged.
**Fault/severance tests:** wrong SHA+encoding pair; automatic guess/fallback; timezone-aware direct and item-unwrapped refusal; date/time string masquerade; wrong G01 float key; source SHA drift before decode; snapshot tamper.
**Reviewer:** PREMAIN physical-decoder/R5-codec owner plus independent C3/physical-source reviewer, distinct from the C3 author.
**Action:** `ADAPT_REPAIR_CANDIDATE`, no patch in this return.

## P-04 — C3/R9 successor contract

**Source:** HQD-2026-10-03-199 and 198 at `4b6335ca5fc485108b0ffb1d682a29a02e1eee51`; hardened execution binding `deea40541cda0627d129dcb7d30e06e0682e0fed`; final review `0deb64784829661780ee3957f8070ccc2c241722`; accepted runtime placement `dfdf5659fd78e9bc996b07383349094059a5553d`.
**Affected paths:** `pre553_source_access_broker.py`, `pre553_source_session.py`, `pre553_execution_binding.py` (all absent current).
**Current receiver:** none; no real issuer/role owner; `TestOnlyDecisionResolver` is a test double.
**Required successor (not implemented here):**
1. Build on PR526 `_SourceSnapshot`, not a second raw-path broker.
2. Consume an externally authenticated issuer/role record; no self-asserted role.
3. Implement the selected-variable physical read operation honestly; do not treat `usecols` as physical restriction.
4. Preserve separate open/read/byte/retry accounts and route-pass applicability.
5. Name a real current consumer before adoption.
**Negative tests:** premature EOF ceiling instead of raise/hang; seek/tell; fresh broker per chunked invocation; usecols-is-post-read; retry/attempt/completion separation; forged issuer/role; raw-path escape; selected-read undercount; source substitution.
**Reviewer:** R61 current-issuer owner plus independent source-access reviewer.
**Action:** `HOLD_UNPROVED`; no transplant.

## P-05 — C5/N5 structural context

**Source:** accepted service `151d39260a803635f622323b14e42d96c7976d25` (HQD-2026-10-01-151).
**Affected path:** `rawlsing_next/current_gt2_structural_context.py` (absent).
**Current receiver:** none for the wrapper. The owner-level path is exercised by `gt12_e2b_actual_object_consumer_harness.py:321` and the HQ221 court.
**Reconstitution:** exact accepted floor from current owners; denominator 19,210; drift to 19,211 refused.
**Action:** do not re-import the wrapper without a named consumer. If a consumer appears, prefer the direct owner path or re-propose the zero-argument service with fresh tests. Negative tests: denominator drift, fact/query replay drift, wrong risk set, non-SUPPORTED state, reversed conditioner/target, permission widening, nonpositive admission, missing publication authority.
**Reviewer:** independent GT2/structural-context reviewer plus the receiver owner.

## P-06 — N10E lifecycle and context contract

**Source:** accepted provider `52e41a41e8bc3b77390016a049095b5aea1721d0` (HQD-2026-10-01-147); HQ222 review `bdf025b3a`/`ce1cce79f`; HQ237 review `71d6f77ca`.
**Affected paths:** provider is current and should not change for these defects. The lifecycle defect is in `pre553_analytical_replay_dependency.py:432-462`; the context defect is in the provider request/entrypoint boundary.
**Current receiver:** progressive candidate `:55`/`:327`, test-only.
**Required repair (not implemented here):**
1. Either connect every lifecycle-relevant exact determinant (query, predicate, consumer query, conditioner witness, release) to the accepted invalidation graph, or explicitly scope AT19 invalidation to authority-only with named owners for the other determinant classes. Do not invent a second lifecycle owner.
2. Constitute a competent fixture-context issuer/registrar and verify an exact use-site token before C1 construction and N10E provider/replay. Add `fixture_use_context_ref` only after that owner exists; the field alone is not authority.
3. Prove an actual recomputation that lawfully preserves identity, or prove identity movement is mandatory for every lifecycle-relevant determinant class.
4. Keep cache presence separate from currentness.
**Negative tests:** exact determinant mutation through the graph; unchanged-identity actual recomputation; wrong source/release/context; site-token swap; unregistered/forged context; stale receipt claiming fresh grade; cache presence does not restore currentness.
**Reviewer:** independent N10E/C1 model-authority reviewer plus the actual lifecycle/context owner.
**Action:** keep provider current; hold lifecycle/context. No speculative patch.

## Why no patch

- **C1:** exact current; no patch needed.
- **C1-M2:** production code would require a real consumer and issuer; a sourcefree candidate already exists and is nonissuing.
- **C3:** production decoder/codec changes are outside this return's write scope and require exact source authority; a test-only adapter would be a forbidden mock-as-production.
- **R9:** any new module would either duplicate PR526 custody or require a fake issuer/role; both are prohibited.
- **C5:** the accepted wrapper adds no semantics; re-importing it without a consumer would create a second surface.
- **N10E:** the provider is exact current; the defects are in lifecycle registration and context authority, not provider arithmetic.

No merge, adoption, self-review or PREMAIN mutation was performed.
