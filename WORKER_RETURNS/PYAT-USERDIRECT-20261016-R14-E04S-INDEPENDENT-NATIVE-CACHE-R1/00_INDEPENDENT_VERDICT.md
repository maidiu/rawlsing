# R14 E04S — independent full-native cache court

**Verdict: RED_SOURCEFREE_NATIVE_AUTHORITY_LIFECYCLE.** E04R `97254d0b215b5dd45580dd94608a8ec95ff8b76f` independently repairs both original E04N cache-corruption/foreign-release failures and preserves the complete native positive. A new, independently executed grant-registry lifecycle counterexample prevents `ACCEPT_SOURCEFREE_FULL_NATIVE_E04_CACHE_METHOD_ONLY`. This is an executed defect, not a missing-native-import HOLD.

**E04S-A1:** after a successful native production, replace only the attached original native `AuthorityRegistry` with a registry containing the same source authorities but omitting the exact query grant (also independently tested with an empty registry). The native registry's own exact resolution now refuses the required query authority, while E04R's source/request identity is unchanged. Both warm-cache clients still return complete **18/32,10/16,6/8** products. Clearing only the cache makes the actual same owner chain return **UNAVAILABLE, denominator0, empty cells**. Four new pytest cases fail: both original clients × both registry-loss fixtures. No owner function, private cache attestation, source rows or canonical authority record is modified by this attack.

The omission is at the cache-hit current-grant boundary: `product/empirical.py` binds qauth/permits, source metadata and the sealed release object, but `_identity()` / `_validate()` do not bind or revalidate the currently attached native authority registry. Complete equality with immutable original projection bytes is a strong content-integrity repair; it cannot alone certify fresh use when the active exact query grant is unavailable. This witness concerns attached fixture grant availability, not a claim to have revoked a competent real-world issuer.

| Actually rerun in this separate court | PASS | FAIL | ERROR | SKIP |
|---|---:|---:|---:|---:|
| Exact original E04 37 on E04R | 37 | 0 | 0 | 0 |
| Exact native regression selection | 231 | 0 | 0 | 0 |
| Exact unchanged E04N 51 on E04R | 51 | 0 | 0 | 0 |
| Exact E04R implementer hostiles, independently rerun | 37 | 0 | 0 | 0 |
| **Inherited subtotal** | **356** | **0** | **0** | **0** |
| **New E04S hostile/science cases** | **53** | **4** | **0** | **0** |
| **Candidate total** | **409** | **4** | **0** | **0** |

Before testing the repaired candidate, the unchanged E04N51 was independently rerun on exact old E04: **49 PASS / 2 FAIL**, exit1, reproducing the original defects. Those baseline cases are separate and not added to candidate totals. Original/native/inherited candidate suite subprocesses exit0; new E04S court exits1. No xfail, skip, altered frozen expectation or collection/runtime test error hides a defect. The eight dedicated F1/F2 client controls and scientific/cold probes are separately labeled executable controls, not added pytest passes.

## Restored original cache guards and full native positive

All 51 original E04N test bodies and original common/oracle bytes are unchanged. Original F1 cached18→999 and F2 cached foreign well-formed C11 release now refuse. A dedicated independent probe executes each attack against each actual client with stale and coherently recomputed local hashes: eight controls refuse before empirical value reads. The nonparent client can read legitimate structural premises before refusal; the scenario client begins with empirical proof. Neither returns a product from the corrupted projection. Original private owner material stays unchanged.

The separate scientific probe independently reconstructs **58 respondents and232 actual C11 events**, all eight frozen strata, forward/minority geometry, separate reverse18/29, source-change19/32,11/16,7/8, both actual client profiles, native modeled access/fee/sanction effects, historical clocks, selective catalog revocation and support24/8/0 with terminal ZERO_SUPPORT. It observes **385 named native entries** and **22 actual concrete C1 evidence objects entering F8**, with exact I03 query/fact/evidence refs. It also proves a deleted deep cache projection re-enters real I03/C1/F8 and preserves unrelated structural products/private anchors/history. Normal mutation of source/native fact carriers refuses; returned-client aliases do not corrupt the retained immutable bytes.

Both cold interpreters exit0, PIDs79695 and80555, with bit-identical common records including the new authority lifecycle counterexample. Cross-process public projection injection refuses without a private native-produced attestation; fresh real owners then recreate lawful fixture results. Reconstructing a fresh fixture resets in-memory grants and is explicitly not a durable permission-renewal proof.

## Provenance and reproduction

Exact startup `d50b6acec57713e1589b5950c0f0778c52d387f8` matched direct remote ref on branch `agent/userdirect-pyat-20261016-r14-e04s-independent-native-cache-r1` before work. An isolated authorized sparse worktree was created; quota was available. The reviewer expectation freeze was committed at **40d0a5e82330bb7a68954a2066e0c9a0de83f224 before execution**, SHA256 `fbf69c566200ebe4b346bb6c62febaa03cc7056509f779f91847a4415254e631`. It reuses the original E04I frozen preimage unchanged and adds reviewer-authored cache/source/client invariants without using E04R's expected helper.

`source_manifest.json` verifies all100 independently staged Git objects: E04N's94-file exact original selector, including all51 native dependency objects, plus six exact E04R product files. All commissioned N10E/C1/F8/I03/M4/M5 blobs match; C11 pins are recorded from the original selector. Actual per-process `module.__file__`, Git NUL hashes and callee frames reconcile to this register. Five product files remain exact original E04; only empirical.py differs. `reviewed_candidate/` is a byte-identical review copy, not a product edit. A declared preload adapter selects E04R before frozen author tests prepend their old directory; no owner or expected helper is mocked.

The entire E04R00–05, source/test/JUnit/import evidence, changed-path proof, E04N original oracle/failures, E04 and E04I evidence are pinned by `input_manifest.json` and read inventory. E04R's actual diff from its own sealed startup is independently rechecked under `observations/independent_candidate_changed_paths.txt`. `frozen_E04N/` preserves original51/common/oracle and original first-run failure XML/stdout. Ignored runtime/input copies are exactly reconstructible via Git; no author's runtime or original survey estate is copied.

One scientific probe harness initially confused the service's REVOKED read state with the native M4 denial state stored in its snapshot. Initial logs/source are retained and the harness now checks both layers. This was not a candidate defect or a frozen-test change. The actual original F1/F2 and new E04S-A1 failures remain distinct from that setup diagnostic.

## Deliverables and bounded next edge

- `01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json`: preexecution reviewer freeze and original native selectors.
- `02_ACTUAL_NATIVE_IMPORTS_OLD_F1_F2_AND_NEW_HOSTILES.json`: fresh JUnit case results, exact imports, restored original negatives, new grant-registry RED, source/evidence/cold controls.
- `03_TWO_CONSUMERS_COLD_REVOCATION_AND_SOURCE_TRACE.md`: exact physical science, consumer and lifecycle reasoning.
- `04_N9_SOURCE_ISSUER_AND_ADOPTION_CEILING.md`: actual OC05 refusal and unissued authority boundaries.
- `tests/`, `repro/`, `observations/`, manifests and `environment_passport_delta.json`: runnable independent evidence and declared process exits.

The smallest productive repair is to bind and revalidate the native authority registry's exact grant closure on every fresh cache read, refusing or returning typed absence when required query/source/operation grants are unavailable. Preserve the immutable producer-bound content repair and all positive/frozen oracles; do not flush unrelated structural channels or replace accepted owners. This reviewer does not implement that repair. A later distinct adjudication and competent HQ/adopter retain method accession. No canonical/CURRENT adoption, real source rights, operative N9/OC05, EE14/N10W, all35/N11/N12 or V3 is granted. Publication receipt records direct remote readback of the evidence commit; final delivery reports the final branch SHA.
