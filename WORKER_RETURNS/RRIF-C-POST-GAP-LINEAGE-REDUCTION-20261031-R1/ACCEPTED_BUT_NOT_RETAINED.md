# Accepted but not retained — nine historical integration branches

**Scope:** canonical PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`; source map A `84182f9fa7044d67689ea4f80eabf7e9337f15c2`; decision map B `59e6e62600814d82cfefd1a2137b7aa63316bc95`; E8 `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`. No PRE-MAIN, PR, worker or source-native mutation.

Acceptance and retention are different records. None of the nine accepted `integration/pyat-hq*-accepted-r1` tips is an ancestor of current PRE-MAIN. Four retain all changed code blobs exactly at the same paths, one is partial, three retain no exact code blob, and AT07 has no code delta. Exact blob retention is source identity, not behavioral equivalence, adoption or a live consumer.

| Branch | Decision | Accepted implementation / tip | Reviewer | Current exact status | Finding |
|---|---|---|---|---|---|
| `integration/pyat-hq130-c3-source-free-accepted-r1` | `HQD-2026-09-30-131` | `30686b185d4ceb2c94f61815ef70d8c8e76255d6` | C3 independent integration review | 0 exact code; 2 modified; 1 absent; 3 tests absent | **not retained exactly** |
| `integration/pyat-hq139-c1-01-source-free-accepted-r1` | `HQD-2026-09-30-139` | `5fafb499d53dddadaf8a7b4fd46506e91a09d270` | `agent/reviewer-pyat-hq138-c1-01-r8-r1 @ 98825f710e5238e794c78bf0acbb43faaea355e4` | 0 exact; composition/test differ | **not retained exactly** |
| `integration/pyat-hq145-c1-02-source-free-accepted-r1` | `HQD-2026-10-01-145` | `bc661188b51e995d9f5d74e55c4e37d2ba358a17` | `agent/reviewer-pyat-hq144-c1-02-witness-pairing-rereview-r1 @ 59d69ba31b8de2d028bd44048e8d7b75f2d82538` | 5 exact | retained exact |
| `integration/pyat-hq147-n10e-at17-source-free-accepted-r1` | `HQD-2026-10-01-147` | `52e41a41e8bc3b77390016a049095b5aea1721d0` | `agent/reviewer-pyat-hq145-n10e-proof-provenance-rereview-r1 @ 43cdc1a8d1077be78a879ef06232a454736084d9` | 3 exact; 3 absent | **partial** |
| `integration/pyat-hq151-c5-n5-source-free-accepted-r1` | `HQD-2026-10-01-151` | `151d39260a803635f622323b14e42d96c7976d25` | `agent/reviewer-pyat-hq150-c5-n5-r1 @ 294d8935ccab6f0f3c0d462a0f6f78e2e5f4a4ae` | 0 exact; code and test absent | **not retained exactly** |
| `integration/pyat-hq159-c1-03r-source-free-accepted-r1` | `HQD-2026-10-01-159` | implementation `c690bb0b1e6f071c9a640a6825769b96f30dd79a` on tip `9ec7eaff2646c1effd5192002967407a5c66bbef` | `agent/reviewer-pyat-hq158-c1-03r-r3-final-rereview-r1 @ aebb12a160c21b3b1000ab96700120e1c4821f79` | 11 exact | retained exact |
| `integration/pyat-hq162-c1-03a-source-free-accepted-r1` | `HQD-2026-10-01-162` | implementation `4f5555459e5ffdb240fc9e6e94178ec5e4b3eff1` on tip `26976201b3cf14f4cf89a45a909c780591f54bcb` | `agent/reviewer-pyat-hq161-c1-03a-r6-final-acceptance-r1 @ 54b8018d2ba93c61bb418d515adf33b04311a878` | 8 exact | retained exact |
| `integration/pyat-hq166-at07-successor-spine-accepted-r1` | `HQD-2026-10-01-166` | oracle freeze `92ddee2241a78b46394665d325e5ebf0e75adf40` on tip `069ac61b5c90486e5b7bb633135b4743dfbd55df` | `agent/reviewer-pyat-hq165-at07-successor-spine-independent-review-r1 @ 2a454f4cd6359d149269dbbbe5497ea1c263f9c8` | no code delta; identity data | not a code-retention case |
| `integration/pyat-hq168-c1-03-successor-join-accepted-r1` | `HQD-2026-10-01-168` | code `933a3d31aa961719c73e6ce7eebcfe40bc8cd45e` on tip `149c3d2636160d8de9b5a8be0c8b87195158077d` | `agent/reviewer-pyat-hq167-c1-03-successor-join-final-integration-review-r1 @ c8ce0ea81a2165f37d566f37de788fecedf85051` | 21 exact | retained exact |

## 1. C3 / HQ130 — accepted source-free integration, no exact current code

- Exact source cut: `integration/pyat-hq130-c3-source-free-accepted-r1 @ 30686b185d4ceb2c94f61815ef70d8c8e76255d6`.
- Decision: `HQD-2026-09-30-131`; accepted six commissioned files at the declared grain, with prior 20/20 protocol and 55/55 six-file court.
- Current code comparison: `rawlsing_next/pre553_physical_decoder.py` modified, `rawlsing_next/pre553_r5_codec.py` modified, `rawlsing_next/closed35_g01_sav_numeric_representation_authority.py` absent. The three associated tests are absent.
- Why no exact retention: current PRE-MAIN contains later physical-decoder/R61 source custody changes at the same path and no exact G01 authority file. The archive does not prove whether the accepted blob was adapted, superseded or never integrated.
- The historical C3/R9 return `24847592f6a40fde3c4932d0f26173012c037078` still contains exact G01 `31a9afd7…`, decoder `d3d828c1…` and R5 codec `6000a170…`; current D01/D02/R9 paths `pre553_source_access_broker.py`, `pre553_source_session.py`, `pre553_execution_binding.py` and `closed35_g01…` are absent.
- First current static receiver: `rawlsing_next/ee_p2x_darwin_stage_backend.py` imports `decode_dta`/`decode_sav` from the current decoder. This is not a G01/R9 consumer.
- Required comparison: accepted C3 D01/D02/G01/R5 vs current R61 decoder/source-custody path. Do not run raw survey or native source.

## 2. C1-01 / HQ139 — accepted predecessor, current composition differs

- Exact source cut: `integration/pyat-hq139-c1-01-source-free-accepted-r1 @ 5fafb499d53dddadaf8a7b4fd46506e91a09d270`.
- Decision: `HQD-2026-09-30-139`; reviewer `agent/reviewer-pyat-hq138-c1-01-r8-r1 @ 98825f710e5238e794c78bf0acbb43faaea355e4`, `APPROVE_AT_DECLARED_GRAIN`.
- Current code comparison: the accepted `pre553_analytical_composition.py` blob is not present exactly; the same path and its test differ from the accepted C1-01 blobs.
- C1-02 / HQ145 is exact-current at `bc661188b51e995d9f5d74e55c4e37d2ba358a17`. The later C1-02 acceptance is not a retroactive rejection of C1-01, but it is the strongest current successor candidate.
- Required comparison: C1-01 release/predicate/preimage custody vs C1-02/current composition. Determine whether C1-01 is a superseded accepted predecessor or a still-required unmerged release spine. No hash inversion or synthetic preimage issuance.

## 3. C5/N5 / HQ151 — accepted service, current file absent

- Exact source cut: `integration/pyat-hq151-c5-n5-source-free-accepted-r1 @ 151d39260a803635f622323b14e42d96c7976d25`.
- Decision: `HQD-2026-10-01-151`; reviewer `agent/reviewer-pyat-hq150-c5-n5-r1 @ 294d8935ccab6f0f3c0d462a0f6f78e2e5f4a4ae`.
- Current code comparison: `rawlsing_next/current_gt2_structural_context.py` and its test are absent.
- Why no exact retention: the accepted bounded GT2 structural-context service has no same-path current code blob. This does not prove the capability is missing; current service paths may supersede it, but no comparative evidence was located.
- First current static receiver: none found for the accepted module. A real current consumer must be named before any revival.
- Required comparison: accepted C5/N5 service contract vs current GT2/structural-context service and a real receiver. Negative cases: context substitution, denominator drift, missing consumer, and source-authority widening.

## 4. N10E/AT17 / HQ147 — partial exact retention

- Exact source cut: `integration/pyat-hq147-n10e-at17-source-free-accepted-r1 @ 52e41a41e8bc3b77390016a049095b5aea1721d0`.
- Decision: `HQD-2026-10-01-147`; reviewer `agent/reviewer-pyat-hq145-n10e-proof-provenance-rereview-r1 @ 43cdc1a8d1077be78a879ef06232a454736084d9`.
- Current code comparison: `pre553_empirical_possibility_provider.py` and its fixture/runner are exact; `pre553_analytical_composition.py` and the provider test differ from the accepted AT17 blobs.
- Why partial: the provider core survives exactly; the composition/test surface does not. The accepted AT17 grain is therefore partly current and partly historical.
- First current static receiver: `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` imports the provider.
- Required comparison: accepted AT17 provider/contract vs current provider plus progressive consumer; include wrong-source, authority-refusal and replay/cache negatives. Do not widen to N10W live world or source science.

## Exact controls and limits

- C1-02/HQ145, C1-03R/HQ159, C1-03A/HQ162 and C1-03 join/HQ168 retain all changed code blobs exactly at current paths. This is **source identity**, not proof of a live consumer, behavioral equivalence or current scientific authority.
- AT07/HQ166 is identity data, not a code-retention case.
- Do not infer that an accepted branch was merged because it is named `accepted`; do not infer that a modified current path is semantically equivalent; do not retire a branch solely because E8 labels a family `RETIRE` or `HOLD_EXACT_DECISION`.
