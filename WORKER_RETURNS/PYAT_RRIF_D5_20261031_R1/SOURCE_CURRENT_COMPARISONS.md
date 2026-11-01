# Source/current comparisons — RRIF-D5 six world lineages

**Current cut:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**RRIF-C:** `b75addf621c3a6c1a3b196bd92a810fad77ae3ae`
**RRIF-V hostile:** `bec050449f0b38606718e4e9691caa1721fcd94f`
**A:** `84182f9fa7044d67689ea4f80eabf7e9337f15c2`
**B:** `59e6e62600814d82cfefd1a2137b7aa63316bc95`
**A×B:** `f5a9facd189af6756c2b15c8daebe680016f658a`
**E8:** `e95d6edb9300b2cc8b0ad2c70dff3953c8afe1ba`

No whole-estate recount was performed. The RRIF-V corrections are treated as controls, not as dispositions:

- 1,333 branch-only implementation records are branch locations, not current integration.
- 291 exact-other-path copies need owner/path/ABI proof before being called current.
- B has 155 branch rows, not 155 distinct acceptances; HQ274 is documentary intake, not code adoption.
- Exact blob identity is not behavioral equivalence, adoption or a live consumer.

## 1. Source cut verification

| Cut | Commit subject read | Use |
|---|---|---|
| `8e44ca9c75` | Accept scoped S7FIX structural source identity, preserve hostile PE RED and V2K R61 retirement (#563) | current PRE-MAIN |
| `b75addf621` | Return RRIF-C post-gap implementation lineage reduction and residual accounting | six unresolved rows |
| `bec050449f` | RRIF-V hostile custody A×B: reject false current subtraction and decision-count overreach | corrections |
| `84182f9fa7` | PYAT RRIF custody A: map 845 branches and 3135 variant locations | source locations |
| `59e6e62600` | Return RRIF custody-B recent decision provenance and 845-branch fate ledger | decision provenance |
| `f5a9facd18` | RRIF HQ reconcile A/B recent branch source locations and decision provenance, nonadopting | crossjoin |
| `e95d6edb93` | RRIF: pin revised dispatch head in final return | E8 |

The six RRIF-C rows used are the exact `LIN-I01_WORLD_LIFECYCLE`, `LIN-N9_N10W_PROGRESSIVE`, `LIN-N9_TWO_FIELD_READER`, `LIN-PE_GENERIC_WORLD`, `LIN-R3_SEAM_WITNESS` and `LIN-WORLD_BINDING` records. Their introduced paths, source cuts, receiver fields and unresolved questions were read from `GENUINELY_UNRESOLVED_IMPLEMENTATIONS.jsonl` and `UNIQUE_IMPLEMENTATION_LINEAGES.jsonl`.

## 2. Blob identity map

| Lineage | Historical path | Historical cut / blob | Current path | Current blob |
|---|---|---|---|---|
| I01 lifecycle | `rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py` | `5eb51c68` / `1e26a60d985ef489e62d01cf4020f3202f2f774f`; `a1dc5941` / `7899846394f079c14eae4864c8200697bd9dee4a` | ABSENT | — |
| N9/N10W progressive | `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | `0e0ed50d` / `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` | PRESENT | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` |
| N9/N10W selected world | `rawlsing_next/pre553_selected_world_progressive_contract.py` | `c98e8881`/`aba2f6a6` / `e9caea543bcc4e1418905f1442d2c7c97eef04b2` | ABSENT | — |
| N9/N10W seam | `rawlsing_next/r3_s02_seam_witness.py` | `208bca30` / `60bdaee9fc4dae2d0e98b33d26309ef229554fe3`; `aba2f6a6` / `b1ec1814c4616f61a1e3fc8bbc0b102d690a577f` | ABSENT | — |
| N9/N10W world-conditioned | `rawlsing_next/pre553_world_conditioned_progressive_service.py` | `849a76de` / `db573027a2416f1b43f2bc47d6f2e3b9d5cd3b31` | ABSENT | — |
| N9 two-field reader | `rawlsing_next/pre553_hq297_n9c_two_field_reader.py` | `9ab4a019` / `03eb46efccadd6880cb34b2e2ac609ffc9b16c59` | ABSENT | — |
| PE generic world | `rawlsing_next/pre553_postastra_pe_generic_world_possibility.py` | `b497f857` / `58484f4c3d9aae148d4116dcf00420c432aefcbd` | ABSENT | — |
| R3 seam witness | `rawlsing_next/r3_s02_seam_witness.py` | `aba2f6a6` / `b1ec1814c4616f61a1e3fc8bbc0b102d690a577f` | ABSENT | — |
| World binding | `rawlsing_next/pre553_universal_world_binding.py` | `359ffcef`; R117 `849a76de` / `dfb1e9fb72f1ee4b50fd7138fe978ce50db49f37` | ABSENT | — |

Current owner blobs used for comparison:

| Owner | Current blob |
|---|---|
| `pre553_learned_product_lifecycle.py` | `a11c9eb73abab9be118ef4f0b6e325e676059f27` |
| `pre553_learned_product_release.py` | `f76c390665f06ef126968ccf1a6b2d816f43ae92` |
| `pre553_learned_world_composition.py` | `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` |
| `pre553_batch_runner.py` | `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` |
| `pre553_analytical_composition.py` | `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b` |
| `pre553_empirical_possibility_provider.py` | `23167aa25291fb148b1e3cf210ac33fe7769b783` |
| `source_backed_positioned_subject_possibility.py` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` |
| `pre553_universal_workload.py` | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` |
| `pre553_native_workload_binding.py` | `dac73e484f8619088f5c6701b2b6991c07540f3b` |
| E03 test/CI | test `2161c0fff86ecb7a2c9a40b29852075e802841fd`; CI `28f7004c5b004f8fd95d9b977802c70b954d54a6` |

## 3. Per-lineage comparison

### I01 world lifecycle

**Historical source.** HQ287 `5eb51c68` introduced the I01 glue plus selected-world, seam and durable checkpoint candidates. HQ292 `a1dc5941` repaired the selection-key restore path with a typed `I01Error('SAVED_SELECTION_KEY_IDENTITY_MISMATCH')` for absent, foreign, malformed or duplicate keys. HQ288 independently accepted the product at `SOURCE_FREE_ONLY / LOCAL_UNAUTHENTICATED` scope. HQ293 banked the patch and preserved one frozen module-blob governance failure.

**Current ownership.** The I01 path is absent. Current B5 is blob `a11c9eb7`; current M2 release is blob `f76c3906`. The I01 branch's actual B5/M2 blobs are `dadf2362` and `1cb76923`, and its ancestry includes five branch-only S06F commits (`dc4443672`, `c118114e9`, `a1a47e7f9`, `e2ecfb009`, `0ff13995c`) that are not ancestors of current. The current B5 has no `verify_m2_release_subject_exact`; the I01 code calls it. A direct overlay of the exact I01/selected/seam/durable files onto current `rawlsing_next` fails at `build_product` with `AttributeError: 'LearnedProductLifecycleExecutor' object has no attribute 'verify_m2_release_subject_exact'`.

**Negative / dependency severance.** The branch author/reviewer tests pass at the branch cut (10 + 7 author; 26 independent). They cover foreign release/index, missing artifact, rehashed artifact, native consumer hostiles, invalidation, cold restart and as-of. They do not cover current B5/M2 drift. The current overlay failure is the missing interface.

**Consumer.** Historical `I01.serve()` and reviewer/author tests; no production importer. Current: UNKNOWN.

**Competing successor.** Current B5/M2 lifecycle primitives plus current E03 are not an integrated successor. No current code performs saved-world → M2 → B5 → consumer.

**Disposition.** `ADAPT_REPAIR_CANDIDATE`. Comparative merit is high for lifecycle integration, but only under a versioned current-B5/M2 decision. No patch was made.

### N9/N10W progressive

**Historical source.** HQ281 `0e0ed50d` introduced E03; HQ282 `c98e8881` added the synthetic selected-world contract; `208bca30` added the seam; R112/R117 `849a76de` added the world-conditioned service and universal binding. The E03 code itself states N9 and N10W are not implemented anywhere in the repository.

**Current ownership.** E03 module and test are exact current (`84d40414`, `2161c0ff`) and the CI workflow `pyat-programma-n10w-sourcefree.yml` runs the test on path changes. Selected world, seam, world-conditioned service and universal world binding are absent. The module is a 58-row synthetic fixture with `real_current=False`; the test proves 32/16/8 denominators and 9/16, 5/8, 3/4 fractions, minority survival, production/consumption separation and no rights.

**Negative / missing joint.** One-conditioner joint probe returns `E03ProgressiveError` ("joint step requires two or more conditioners"). A caller-supplied foreign world mapping fails with KeyError because there is no external world parameter or N9 resolver. The test/CI receiver is real but test-only.

**Consumer.** Test import + path-triggered CI. No production consumer.

**Competing successor.** R117 world-conditioned service is stronger for world consumption but branch-only, P41-runtime-dependent and not current. Current E03 is the exact retained fixture, not an N9/N10W owner.

**Disposition.** `CURRENT_RETAINED` at exact E03/test/CI scope; N9/N10W capability remains absent and HOLD.

### N9 two-field reader

**Historical source.** HQ297 `9ab4a019` code `03eb46ef`, test `e4fc9dd0`. It reads two test-only published values from a defensive-copy registry, checks roles/families/units/geography/definitions/dates/permissions, refuses CURRENT, pooling, person exposure and model use, and implements publication-aware as-of.

**Independent negative.** D2R found the real producer's refs (`D2P_TESTONLY_FIELD:...`) and the reader's refs (`TESTONLY_FIELD:...`) have zero intersection; the reader receives `UNKNOWN_EXACT_FIELD_REF` for the producer fields. Seven mandatory REDs were independently reproduced: producer ref downstream, stale content ref, forged issuer signature, invented subtype label, native unit check, spoofed publisher, parallel registry. D2P2 returned `TYPED_HOLD__...REPAIR_NOT_IMPLEMENTED` and listed the exact one-registry repair.

**Current ownership.** Reader path absent; no current N9/OC05 owner; OC05 `NOT_YET_APPLICABLE`/`seam=None`. No issued N5/N6 fields, EE13 or publisher byte custody.

**Local positive.** The 47-test local court passes and 11 targeted as-of/nonpooling/revocation cases pass. This is local fixture math, not producer-to-reader lineage.

**Consumer.** Branch test only. Current: UNKNOWN.

**Disposition.** `HOLD_UNPROVED` at integration scope. The smallest next action is the exact D2P2 one-registry repair and independent rerun of the 7 REDs; no N9 installation.

### PE generic world

**Historical source.** `b497f857` code `58484f4c`, test `92f59875`, fixture `c9674d5f`. PE2 `b94f0f981` qualified 21/21 probes and 373 owner tests, and explicitly held operative N9.

**Current ownership.** Module absent. Current C1 composition, F8 consumer and N10E provider exist and are used. The PE/SC0 owner-bound successor `a48c6acb` is a different value-bearing overlay lineage, not a successor to this generic facade.

**Negative.** 21 tests pass; targeted future-time, invalidated-current, missing-denominator, new-unit, unauthorized-reverse, fake-model-use and source-hash cases pass. However, a fabricated never-issued N9 world marked `SELECTED_IMMUTABLE` is accepted and returns `EXACT_SUPPORTED`; the facade carries caller-declared world identity and does not resolve N9. This is a limitation, not a claim of N9 service.

**Consumer.** Branch tests only. Current: UNKNOWN.

**Disposition.** `ADAPT_REPAIR_CANDIDATE`. It has useful query/refusal and role-reversal law but needs an operative N9 resolver and a named consumer. No patch.

### R3 seam witness

**Historical source.** `54f14553` S00C, `ac75c6fc` S00E, `5e6e802f` S00V2, `aba2f6a6` S00V3. Final code `b1ec1814`, test `190076a9`, selected world `e9caea54`.

**Current ownership.** Seam and selected world absent. Current E03 present. No current seam consumer.

**Negative.** 50 tests pass, including scope/risk mismatch, zero denominator, false S00 semantics, unissued real GT2 and unused-read. One preserved stale positive fails: `test_s00c_change_source_owned_synthetic_numeric_values_changes_result` expects coherent changed values to recompute; the S00V3 offline binding correctly refuses changed values under old producer roots. This is a stale test expectation, not a reason to weaken the binding.

**Consumer.** Branch tests and historical I01 import; no production importer. Current: UNKNOWN.

**Disposition.** `ADAPT_REPAIR_CANDIDATE` as a test harness/consumer boundary. It is synthetic and needs selected-world ownership. No patch.

### World binding

**Historical source.** R100 `79309093` and R107 `22280a3f` are return-bearing cuts; R110 `359ffcef` is the binding repair cut. R112/R117 `849a76de` is the competing later cut: `pre553_universal_world_binding.py` `dfb1e9fb` and `pre553_world_conditioned_progressive_service.py` `db573027`. PYATWORLD-R3 at `a9d84389d` records R119 ACCEPT_SCOPED for the narrow sourcefree software grain, not original source/science/actor/PRE-MAIN authority.

**Current ownership.** Binding and world-conditioned service absent. Current R61 universal workload (`8e7fe00a`) and native workload binding (`dac73e48`) are different owners and have no production importer found. The R117 runtime calls `git archive f27d1101` for the P41 packet; that packet path is absent from current PRE-MAIN.

**Negative.** 30 self-contained tests pass; 4 J42 full-repo fixture tests error in the sparse checkout (terrain, not candidate failure). Targeted foreign-world, empirical revocation, rows hash, source repository, mixed model and step severance all pass. R117 still uses a test-only pinned P41 runtime and sets `route_probability=null`.

**Consumer.** Branch tests and R112/R117 qualification; no production importer. Current: UNKNOWN.

**Disposition.** `ADAPT_REPAIR_CANDIDATE` at scoped software level. It is the strongest world-consuming adapter but branch-only, test-only, P41-runtime-dependent and without a real receiver. No patch.

## 4. Cross-cutting result

The current repository has **no** released source → world → selected possibility edge. It has:

1. A current exact synthetic progressive fixture (E03) with test/CI receiver.
2. Current empirical/analytical owners (N10E provider, C1 composition, F8 consumer, B5/M2 lifecycle).
3. Branch-only candidates that bind those owners to a synthetic world or saved product.
4. A real producer-to-reader RED in N9C that must be repaired before any N9 reader claim.
5. No operative N9 selected-world owner, no N10W world-conditioned owner and no real non-test world/person receiver.

The missing interface is therefore not a single patch but an ownership decision: original Pyat/P41/N9/B5 owners must either issue a versioned selected-world input contract with a named receiver, or return a typed STOP. Until then, no candidate should be merged as a current world service.
