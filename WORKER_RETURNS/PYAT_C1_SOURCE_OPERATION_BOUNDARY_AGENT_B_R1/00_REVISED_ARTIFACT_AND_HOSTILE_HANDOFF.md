# PYAT C-1 — Agent B: repaired semantic cache collision and adversarial handback

**Candidate only; not original35, protected, scientific, or terminal acceptance.**  
Original independent C-1 brief [#918](https://github.com/maidiu/rawlsing/issues/918); parent hybrid architecture [#909](https://github.com/maidiu/rawlsing/issues/909); Agent A's immutable [6cf9dbd4d8883a34de8d3ff75582129e7cf1e18e](https://github.com/maidiu/rawlsing/commit/6cf9dbd4d8883a34de8d3ff75582129e7cf1e18e). Protected source baseline **`6a5c12f04323d74001f9632063ec907f4fc4468e`**; selected physical architecture October 28 **`315251451a6d112fb312a6a2e80b096d345c5de6`**. Agent B candidate [draft PR #922](https://github.com/maidiu/rawlsing/pull/922), isolated branch `review/pyat-c1-agent-b-cache-proof-20261112-r1`; initial repaired executable cut **`c2960b73c803c3c8005776cffc2b4a40f63a0910`**; final additional repair/test cut **`7673bb30a364bc8d728ddda96e136fdbbbdb84b7`** (contains all earlier tested source and tests). This report is appended after that executable cut; use immutable PR commit readback for the final report-containing HEAD. No protected merge, native input, original data use, scientific issuance, local host/lease certification, or independent receiving.

## 1. Exact revised artifact and provenance

- **Source:** `rawlsing_next/pre553_source_backed_c11_facade.py` (protected baseline blob `7c967b8227a2843971c7cd9f61f3deaa423af866`), minimally modified in isolated PR #922. Existing `GovernedC11Projection`, `build_source_backed_c11_repository`, I02 and C11 release formats retained.
- **Independent tests:** `rawlsing_next/tests/test_c1_agent_b_cache_differential.py` (new; two red-baseline tests, physical context negative, routing/occurrence and authority isolation, actual changed-value I03 first reader, deletion/restore); existing facade and multi-owner suites unmodified.
- **CI:** `.github/workflows/pyat-c1-agent-b-cache-proof.yml` (new bounded sourcefree Python 3.11 runner).
- **Reproducible red parent:** [`157509a0746bc9820ac79fb76c0b160409cbc962`](https://github.com/maidiu/rawlsing/commit/157509a0746bc9820ac79fb76c0b160409cbc962), before production fix. [Run 43161527958](https://github.com/maidiu/rawlsing/actions/runs/43161527958): **3 fail / 19 pass**, specific divergent-value, row-to-respondent, decoder-context failures.
- **Repaired code and tests:** Initial exact test cut [`c2960b73c803c3c8005776cffc2b4a40f63a0910`](https://github.com/maidiu/rawlsing/commit/c2960b73c803c3c8005776cffc2b4a40f63a0910) obtained [run 43162557160](https://github.com/maidiu/rawlsing/actions/runs/43162557160), **25/25 focused pass**. Final exact executable cut [`7673bb30a364bc8d728ddda96e136fdbbbdb84b7`](https://github.com/maidiu/rawlsing/commit/7673bb30a364bc8d728ddda96e136fdbbbdb84b7) obtained [run 43163084363](https://github.com/maidiu/rawlsing/actions/runs/43163084363), **26/26 focused plus 136/136 broader sourcefree preservation pass**, and [PROGRAMMA canonical run 43163084394](https://github.com/maidiu/rawlsing/actions/runs/43163084394) **PASS**. These are sourcefree S2 and CI, not native/scientific acceptance.
- **Intermediate self-critique:** A first expansion mistakenly used `dataclasses.replace` on the immutable *non-dataclass* `RoutingEligibilityFact`; [run 43161919637](https://github.com/maidiu/rawlsing/actions/runs/43161919637) correctly failed 1/24. Rebuilt the fixture as a canonical `RoutingEligibilityFact` rather than weakening/dropping the case, then obtained green. This intermediary error is not a source implementation defect.

## 2. Independently verified strengths of Agent A

The fundamental C-1 architectural position is correct at the inspected code scope:

- Source physical bytes/labels/missing declarations are not semantic question/topology/routing/estimand authority. The facade applies explicit `ResponseValueRule`, `OccurrenceRule`, `RoutingEligibilityFact` and independent authority closure. An exact SAV/DTA physical decoder cannot emit original-scientific U by inference.
- The accepted R157 historical `SourceConfigLibrary.load_original`/`source_configuration.factory` family is substantive reuse capital, not a second current original issuer. Its original-source, current read and protected-port rights are not established merely by a fixture.
- Protected `pre553_universal_workload.compile_governed_frontier` lowers an **already supplied** `ScientificFrontier`, and `execute_governed_frontier` only anti-joins the furnished operation universe. A complete local anti-join does not prove all original35 operations were furnished.
- The protected `pre553_issued_workload.admit` contract requires external competent `CurrentDecisionResolver`, exact source/host/purpose/job/envelope/issuer roots before source factory opens. Its existence is not evidence every caller correctly uses it.
- Candidate B `EXECUTABLE_RAW = 5,630` is a **label**, not 5,630 verified native executable operations: 4,705 routing-unknown + 249 rule-unavailable + 676 route-qualified = 5,630 at the recorded B cut. Nor is missing optional population weight an automatic refusal of properly scoped observed RAW.
- The historical full QSM corpus is real, but archival QSM presence does not prove current selected first-reader application. No legitimate reason was established to resurrect a new universal V550 authority engine, add a semantic sidecar/database or insert Field Forge as a global serial gate.

I reject “A did not run S2” as a deception charge: A explicitly marked S2 NOT_RUN and original-source science unissued. The valid challenge was to turn the *conditional F9* allegation into executed first-consumer evidence.

## 3. Established failures — exact producer, consumer, invariant

**C1-B-D01 / semantic-value collision.** Protected facade `GovernedC11Projection.cache_identity` formerly hashed the declared `projection_identity_ref`, source SHA, required authority refs, and optional slot-owner sets, not the actual `response_slots`, row bindings, routing, occurrence rules, weight/coordinate definitions or replay inputs. `source_backed_facade_key` used this weak identity, and `build_source_backed_c11_repository` returned a cache hit before re-projecting. Two syntactically valid sourcefree projections, same source SHA/nominal semantic ref/authority refs but distinct canonical response value, produced **different independently validated release content hashes**; same shared-session cached read wrongly returned the original. Red run 43161527958 captured both values. This is a real stale semantic output, not merely a missed cache optimization.

**C1-B-D02 / respondent-owner collision.** With source and projection ref unchanged, swap row 1/row 2 respondent ownership. Independent I02 C11 release changed; old cache returned the original release. Red run again proves differential. Corrected downstream I03 now selects R1, computes original Y=`1` versus altered Y=`0` under unchanged eligible denominator = 1, and reproduces old fact when the old projection is restored. The positive proof uses actual `execute_empirical_query`, not an ID-only test.

**C1-B-D03 / decoder and supplied authority cache context.** Distinct `ExactPhysicalCellStream.decoder_metadata_digest` values and changed supplied `current_authorities` reused the old session key. The physical release may legitimately have the same *logical* C11 release ref, but the context cannot silently inherit the wrong physical/authority binding. The repaired cache isolates these contexts, preserving identical logical release identity when source cells are identical. This is physical-evidence and cache isolation, **not external current-use reauthorization**.

**Other confirmed adjacent defect, not assigned to this patch:** Protected `pre553_issued_workload.resume_joined_workloads` at source cut L782–839 uses a historical `item.record` echo resolver for partial/absent paths, and serves COMPLETED without a fresh independent `admit`. This exists beyond the narrow C-1 facade seam and is already precisely covered in #910 R2 and C-2 #919; no competing patch into that actively assigned boundary was made here. A frozen old grant cannot confer current source-use entitlement.

## 4. Corrections actually implemented

1. Add private `_cache_projection_preimage`: recursively expand *every* field of the governed projection dataclass and all nested rule dataclasses, retain exact semantic-object `as_dict`/content refs and typed absence, and hash the complete semantic input. Nominal ref and authority set alone can no longer alias different real rules. No new source-science owner is created.
2. Extend `SourceBackedFacadeKey` with a backward-compatible optional `physical_binding_identity` field. Hash source row count, decoder metadata receipt, transport identity, and supplied current authority ref keys. Actual producer builder uses the qualified context-specific key.
3. Add permanent sourcefree mutation, independent uncached reconstruction, I03 fact/denominator, cache-clear/restore, routing/occurrence and authority-binding tests. Existing accepted C11 facade tests remain in the suite.
4. Self-review found a new iterable-consumption hazard: the newly added key read could exhaust a supplied `current_authorities` generator before `physical_binding()` consumed it. Normalize to one `tuple(current_authorities)` at the existing builder entry and share that fixed witness across both call sites. A private sourcefree Parquet cache test compares tuple and one-shot generator file-key production; both must be identical.
5. Preserve all exact C11 underlying object formats, provenance, source/response semantics, I02 validation and I03 query algorithms. Nothing rewrites C11 physical data or changes original-source permissions.

## 5. Proof of improvement, scope and honest negative

- **RED before repair:** independent Actions run 43161527958, three newly added tests failed while 19 existing assertions passed. Important because the failure was measured on existing protected code, not invented in a summary.
- **GREEN after final self-repair:** [Actions run 43163084363](https://github.com/maidiu/rawlsing/actions/runs/43163084363) at code cut `7673bb30a364bc8d728ddda96e136fdbbbdb84b7`: **26 focused + 136 wider sourcefree regressions PASS; zero failures**. Original I03 response-cell support is `Y=1: 1` for R1; after changed row assignment `Y=0: 1`; both exact denominator 1, and restoration returns the original fact ref. One-shot and tuple authority iterables write identical private Parquet cache filenames. [Canonical run 43163084394](https://github.com/maidiu/rawlsing/actions/runs/43163084394) PASS.
- **Native/product limitation:** This is sourcefree runtime evidence on synthetic, explicitly governed material. It does not establish original35 source edition or instrument permission, adequate QSM selection, original U/Epre issuance, real original35 I03/I05/Batch/FF occupancy, 6-GiB physical efficiency, or source-equivalence P01–P20/T01–T18.
- **Integrity limitation:** A same-ref/different-rules projection is a deliberate adversarial fixture showing the class validator and cache cannot assume an external issuer made that ID unforgeable. The cache now makes different results, but **issuer-level binding of a declared semantic identity to its complete authorized preimage remains a separate positive scientific/source contract**. Hashing is not permission.
- **No source-native test, no protected receiving, no other worker disturbed.** S2 sourcefree engineering candidate, not S3.

## 6. Challenges investigated and refuted

- **“Every projection semantic rule is already keyed.”** Refuted by the old property’s exact field set and red Action showing two different release hashes under the same key.
- **“A’s hypothesis was a proved exploit.”** Refuted in its original evidentiary form: A correctly wrote S1 *conditional*; B independently supplied the missing S2.
- **“A new semantic registry, universal ingestion compiler or field-specific engine is needed to fix cache misuse.”** Refuted at this scope. The existing facade, C11 and I03 owners suffice.
- **“C11 releases must get a different identity whenever decoder metadata changes.”** Incorrect: source cells/semantics can produce identical C11 logical identity while physical custody must be partitioned. Test retains that distinction.
- **“An in-memory cache race automatically demonstrates an unpermitted native-source read.”** Unsupported: current test shows sourcefree stale computation, not native-source entitlement abuse. Source permission still belongs to the external issuer.

## 7. Newly exposed or introduced attack surfaces

- Full projection hashing is **O(total projection input size)** per cache lookup. It may increase CPU/transient allocations on large original administration/routing estates; no credible all35 or 100k-resource performance estimate was measured. A lawful optimization needs immutable retained digest or incremental streaming hash plus mutation-safety proof; don't replace correctness with an unbound name for speed.
- Distinct but semantically equivalent input ordering/decoder contexts can over-partition the cache and raise memory occupancy; safety is preferable to an unproven equivalence collapse.
- The session cache is still an in-memory trusted object; direct hostile `put` of an otherwise valid release under an unrelated key, concurrency/mutation, or external authority-revocation races have not received independent hostile full-path proof. This correction is **not** an authenticated persisted carrier or owner-issued current decision.
- External source-reader/issuer source-native integrity remains outside this facade. A caller's forged `source_sha256` or invalid projection/authority ref may still pass local shape checks; those are not source-right certificates.
- This patch may influence performance-sensitive W03/W04 work; isolate and compare at the actual selected I03 Batch first consumer, never merge blindly.

## 8. Surviving material disagreements and authority holds

- Does the present original35 source/administration authority guarantee a canonical, immutable `projection_identity_ref` for **all** source-relevant semantic fields before projection/serving? The present facade validator did not enforce this; a competent issuer must answer, and a sourcefree host test cannot confer original rights.
- Whether selected R157 original configuration code is really integrated and emitted into the protected original35 S01→S02→S03 path at its expected first reader is **not proven** merely by historical source/fixture tests.
- The original U_item/U_unit/U_app/E_pre issuer, QSM source selection, exact negative/routing cases and complete original35 operation census remain distinct unsatisfied scientific/authority conditions. Historical B's 5,630 label cannot fill that gap.
- Independent current issuer for joined resume and saved results remains an implementation defect separately owned by C-2/P4/#910; full external source/host authorization cannot be minted inside a sourcefree cache.
- Qualified high-water memory and repeat-query economics of full-input hashing versus existing source-authoritative compact physical work remain undecided. FIABC 144 PASS / 3 FAIL historical negative is not changed by this patch.

## 9. Direct challenge to Agent A

**Attack this actual patch, not my rhetoric.** Starting from repaired code commit `7673bb30a364bc8d728ddda96e136fdbbbdb84b7` and the red baseline `157509a0746bc9820ac79fb76c0b160409cbc962`:

1. Construct a different semantically significant eligible `GovernedC11Projection` preimage producing the **same repaired key**—or prove source/issuer certified ref always prevents the original collision. Identify exact input field, source rule and changed I03 first-consumer fact. Same-name assertions don't count.
2. Construct a caller-valid cache-hit or `put` poisoning path with a different logical release but a matching SHA/binding key. Show a changed/unsupported I03 result, not only a hash; repair without making a second C11 store.
3. Demonstrate a material N=100k or full original35 query cost regression from the full hash and replace it with a **provably immutable** cheap digest (or streaming equivalent), without making same-ref changed semantic rules collapse again.
4. Verify current issuer revocation and changed source authorization across the real cold saved release/Batch/completed+partial+absent joined resume; prove refusal before opening/serving. A copied `item.record` is not acceptable.
5. Show actual applied QSM/routing/negative/occurrence/source edition obligations conserved into a qualified original frontier. A locally green anti-join of arbitrary supplied operations is not that demonstration.

The claim is limited but hard: **Agent A’s F9 boundary was not merely plausible; it was unsound under executable sourcefree mutation, and the minimal repaired key reaches the changed I03 first reader while preserving 26 focused and 136 broader sourcefree regressions, with one-shot authority witness equality.** The next agent should defeat the fix where it is actually weak, not reopen architecture by assertion.
