# PYAT S2-B / Agent A — first-turn adversarial handoff

**State:** \`DELIVERED_TO_AGENT_B__FULL_S2B_INCOMPLETE__G5_NOT_RUN__UNMERGED\`.
**Original task:** #919 S2-B / P2-02, reconciled #909 R3/R3C/R3S, G1–G5.
**Scope:** SOURCEFREE S2, isolated branch, no new native/source/science/actor/rights claims.
**First-turn code/test frozen cut:** \`2d217c63653f98a56ac23182f766a059460e8d68\`. This return is documentary-only after that tested cut; the final branch HEAD will include this handoff.
**Branch:** \`agent/pyat-pair2-s2b-a-ext-i02-20261112-r1\`.
**Draft PR:** https://github.com/maidiu/rawlsing/pull/952, stacked on S2-A #944 at \`d3814d08dbe03b8464ac6fff4164765179869213\`. S2-A **G5 PENDING**, not accepted upstream.
**Protected PRE-MAIN observed:** \`6a5c12f04323d74001f9632063ec907f4fc4468e\`; left untouched.

## 1. Exact changed artifacts and how to run

- \`rawlsing_next/_pre553_external_i02_certificate.py\`: transactional disk-sorted whole-I02-closure/semantic-selector certificate, physical+logical external roots, independent cold verifier, bounded selected-ref iterator, native I03 bridge.
- \`rawlsing_next/_pre553_query_predicate.py\`: one narrowly allowlisted selector type in the actual \`_select_respondent_events\` native dispatch; existing native evaluator/science remains unchanged.
- \`rawlsing_next/tests/test_pre553_external_i02_certificate.py\`: real legacy I02→I03 fact/replay, valid changed/restoration, real authorized paired canonical/component, multi-occurrence, empty-state, source/release/universe, missing events/coordinates/routing/authorities/respondents, weights, locally rehashed selectors, cold full-root, chunk determinism, crash-orphan, resource sampling.
- \`.github/workflows/pyat-pair2-s2b-external-i02.yml\`: executable test and resource receipts; also existing S2-A workflow triggered by the native selector dispatch change.
- This \`WORKER_RETURNS/PYAT_PAIR2_S2B_AGENT_A_R1/00_ADVERSARIAL_HANDOFF.md\` and adjacent machine receipt.

Source checkout at frozen cut:

\`\`\`bash
git checkout 2d217c63653f98a56ac23182f766a059460e8d68
python -m pip install pytest pyarrow pandas pyreadstat
PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -s -o addopts='' \
  -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py::test_s2b_material_sourcefree_resource_probe
\`\`\`

## 2. Governing contract and direct source grounds

- [Full PYAT PROGRAMMA](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md) requires no-drop original35→F1–F8→N9/N10W→N11/N12 and real first consumer, not a green isolated canary.
- [Adopted MCR-lite](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md) governs actionable whole-tranche construction, causal falsification, bounded independent receiving, and truthful grade; no new tribunal.
- [#919 S2-B](https://github.com/maidiu/rawlsing/issues/919) freezes G1–G5 and the specific omitted event/coordinate/weight/routing/alias, forged-root, replay/occurrence, external-memory and first-reader oracles. [#909](https://github.com/maidiu/rawlsing/issues/909) controls rights, W03/W04 pause, end-of-round and separate G5.
- \`rawlsing_next/pre553_c11_ingest.py\` \`validate_c11_source_release\`, \`_validate_sections\`, \`_validate_declared_manifest\`, \`_validate_authorities\`, \`_validate_universe_and_respondent_scope\`, \`_validate_questions_and_events\`, \`_validate_question_authorities\`, \`_validate_source_relations\`, \`_validate_replay\`, \`build_candidate_replay_manifest\`, \`_all_nonmanifest_refs\`; \`rawlsing_next/pre553_c11_integrity.py\` \`make_m01_m18_coverage\`, semantic object/authority/topology validators.
- \`rawlsing_next/pre553_source_equivalence.py\` \`certify_source_to_c11\` remains a **separate P01–P20/T01–T18 original-source equivalence** contract; success here never issues CURRENT source permission. S1-B independently scoped accepted code \`dedd2fb8a1f5842910a0dc842fe75b3618c23443\` was subsequently assembled in unmerged #948. It is not silently present in this PR's #944 base.
- Native real owner: \`rawlsing_next/_pre553_query_predicate.py::_select_respondent_events\`, \`pre553_empirical_query.py::execute_empirical_query\` and \`_build_release_index\`; inherited S2-A #944 \`_pre553_verified_semantic_range.py\` is **not** a complete disk I02 certificate.

### Exact M01–M18 conservation audit

The **full existing v1 I02 validator** supplies this original, checked \`m01_m18_coverage\` from a genuinely sealed \`C11LogicalRelease\`. Our new external builder verifies all 18 nonempty coverage atoms, streams every public/internal identity, recomputes each semantic projection against its ExactRef, verifies the old \`ReplayManifest.closure_refs\` against the actual streamed complete object set, and binds the original replay/source/release/universe identities into the root. This preserves the inherited v1 *grade*, **not** independent reconstruction of all scientific/semantic original-source validations.

| Original atom | Native I02 owner evidence carried into the whole-root certificate |
|---|---|
| M01 | EmpiricalUniverse exact identity and selected-universe presence |
| M02 | RespondentIdentity exact scoped identity and event respondent join |
| M03 | QuestionVariableBinding (native, version, paired authorized canonical/component) |
| M04 | Every RespondentEvent ExactRef and per-object semantic digest |
| M05 | QuestionVariableBinding→RespondentEvent native association |
| M06 | Each event typed state; selector root includes unfiltered states before filtered reading |
| M07 | Every RoutingEligibilityFact is in object corpus/closure; no fabricated nonmember zero |
| M08 | Every EmpiricalCoordinateFact is in object corpus/closure |
| M09 | All WeightMeasureFact objects or original v1 TypedAbsence coverage |
| M10 | AuthoritySnapshot ExactRefs and bodies, inherited authority registry acceptance |
| M11 | SourceUniverseRelation or declared v1 DISTINCT_BY_DEFAULT state |
| M12 | RoutingEligibilityFact plus original predicate-replay record/typed absence |
| M13 | ComparatorReplayBinding or original DEFERRED typed absence |
| M14 | DiscoveryBranchReplayBinding or original DEFERRED typed absence |
| M15 | StructuralAdmissionReplayBinding or original NOT_APPLICABLE typed absence |
| M16 | Exact replay manifest identity and its complete closure set |
| M17 | AuthoritySnapshot/replay manifest linkage inherited from v1 |
| M18 | Deterministic replay manifest identity retained; chunk-independent logical root |

**Boundary:** For M09/M11–M15 the v1 \`C11LogicalRelease\` does not separately retain every original candidate TypedAbsence section. The derived certificate carries the verified M01–M18 coverage values and replay manifest, **not** independent new source-science/typed-absence issuance. The original legacy in-memory I02 still builds \`ReplayManifest.closure_refs\` as a complete tuple; S2-B has **not replaced** that upstream unbounded construction. This is the most important outstanding in-scope gap.

## 3. Strongest achieved behavior and immutable evidence

- **Real first consumer, not a toy statistics function:** from genuine \`ingest_c11_source_release\` / existing I02 releases, \`VerifiedExternalI02\` confirms both external roots and full corpus+keyspace; \`install_sourcefree_external_i02_i03\` installs an explicitly typed, lazily resolved external-selector sequence into the actual native I03 index. \`execute_empirical_query\` preserves its full fact and replay result on the tested positive case, with valid changed upstream event changing support 2→3, old input restoring exactly.
- **Complete derived keyspace:** native/canonical/component paired question grants are checked across instrument versions. A missing selector entry under an internally rehashed index refuses; a zero-row query can only return EMPTY against the externally anchored **complete** keyspace, never as a silent undercount. Multi-occurrence same-response refs remain two refs; states \`None\` vs \`frozenset()\`, \`native_only\` and component selection are exercised.
- **Corpus-versus-index independent binding:** every event/coordinate/routing/authority/respondent QuestionVariableBinding ExactRef is present in the same global root and original v1 replay closure; forging only the selector index while keeping complete corpus fails. Both physical SHA256 and canonical logical SHA256 are **required inputs at cold open**; no self-hashed manifest may be used instead.
- **Transactional output:** sourcefree stage in same trusted directory, SQLite disk indexes with bounded cursor/commit batches, full check, SQLite close+fsync, atomic final rename+directory fsync; stage crash/orphan does not publish a valid \`.sqlite\` artifact. Bounded cursor does not call \`inventory_refs()->tuple\`.
- **Actual red→green repair:** [initial CI RED](https://github.com/maidiu/rawlsing/actions/runs/43272630296), 74 inherited PASS / 6 new FAIL due serialized public \`ExactRef\` mappings being misinterpreted as absent; repaired source normalization at \`293fef62d2a2e7e5e6026e2e3c4f26ad3b2f5efb\`; [subsequent CI](https://github.com/maidiu/rawlsing/actions/runs/43272942550) 80/80 PASS. Further self-attack removed the fake \`CertifiedRespondentEvents(all_events=())\` masquerade and replaced it with a real private \`Sequence\` explicitly dispatched by native I03.
- [**Latest S2-B sourcefree CI**](https://github.com/maidiu/rawlsing/actions/runs/43274142763) at code SHA \`2d217c63653f98a56ac23182f766a059460e8d68\`: **84/84 PASS**. [**S2-A original selector regression**](https://github.com/maidiu/rawlsing/actions/runs/43274142789) also PASS on the same cut. Author CI is **not independent G5**.

**2048-respondent isolated sourcefree probe**, extracted from the latest CI job:

\`\`\`text
input: existing genuinely I02-sealed sourcefree fixture; 2048 respondents
logical root:  025e17afa43b083a1aa557cab257f63d06716761da25e8575efb431996a88277
physical root: 15be249f8da207d63c45e2999e9238c879b367d809b738bcb97cc8c99da16575
retained SQLite certificate: 24,801,280 bytes
build wall: 5.7709 s
fresh full cold verification wall: 0.1473 s
Python allocation peak during builder only (tracemalloc): 2,112,161 bytes
standalone resource-test process peak RSS (/usr/bin/time -v): 101,288 KB
complete 84-test suite peak RSS (/usr/bin/time -v): 192,768 KB
peak scratch footprint: NOT_MEASURED
independently aggregated process-tree peak: NOT_MEASURED
integrated 100k / 6 GiB C11 native+saved+I03 pipeline: NOT_RUN
physical C11 source-direct build: NOT_BUILT
source native/source-equivalence/CURRENT permission: NOT_ISSUED
\`\`\`

This is an honest bounded **derived certification pass**. It is *not* 100k or production source-direct full I02 validation. These timings do not imply an acceptable production-size physical layout or external issuer.

## 4. Own hostile findings, repairs and rejected alternatives

- **Found/reproduced:** object reference fields sometimes expose serialized canonical mappings rather than \`ExactRef\` instances; my original join rejected genuine I02 respondents. Repaired by using the original exact-ref parser, not treating serialized refs as missing. CI RED and GREEN above.
- **Found/repaired:** subclassing S2-A \`CertifiedRespondentEvents\` with an empty fabricated \`all_events\` attribute would advertise a false sequence. Replaced with the concrete \`_DiskSelectedRespondent(Sequence)\` and the exact two-line native dispatcher allowlist, preserving other dispatch modes.
- **Verified attacker-visible:** locally rehashed missing alias still fails both independently held original roots and the verifier's explicit complete-keyspace check. Omitted original object families likewise fail ReplayManifest closure despite forged local hashes. Hard-crashed partial staging cannot be opened as certified.
- **Rejected:** object-ref inventory membership as proof of *selector completeness* (H26/H27), \`inventory_refs()->tuple\`, a fake logical release/private validation seal, JSON-loaded full corpus at cold verification, posthoc self-generated trust roots, SQL replacing native scientific query semantics, a second public ontology, and a new W03/W04 writer.
- **Rejected premature claim:** old I02 in-memory seal + a new bounded downstream derived index ≠ full external-memory I02 certification. This is a real in-scope remaining implementation obligation, not a scientific-rights HOLD.

## 5. Unresolved in-scope defects and attack surfaces for B

1. **Highest priority — S2-B hard-exit not met:** \`build_sourcefree_external_i02\` begins from a **fully materialized legacy \`C11LogicalRelease\`**, whose ingest constructs an O(all refs) \`ReplayManifest.closure_refs\` and eager public/internal tuples. A genuinely bounded *source-direct* validated I02 construction of equivalent M01–M18 semantic oracle from S1-B/E without this prerequisite is not implemented. B should reproduce memory-scale failure with a legitimate sourcefree candidate and repair the root contract, not rename it an external HOLD.
2. **First cold consumer still uses existing in-memory v1 source:** \`install_sourcefree_external_i02_i03\` calls \`_build_release_index\` and resolves exact event bodies from \`C11Repository\`, so although **selector proof is cold disk**, a complete native *C11 from disk without full canonical rehydration* awaits S2-C; do not call this a cold source-direct I03 product. B must distinguish what S2-B actually owns from S2-C's separate physical release. Add a real saved-reader comparator if required by existing S2-B first-reader contract.
3. **Independent trust/provenance:** the external roots are supplied by a test caller after construction. Root input cannot be replaced by a manifest inside the same file, but no separately competent real issuer/publication source holds them yet; valid source rights/current permission and Pair 1 external root remain separately HELD. B should attack forged root provenance and observed selected root/time/corpus mismatch.
4. **TOCTOU/custody:** after cold full-file verification, a hostile actor swapping/changing the underlying SQLite bytes while a reader remains open is not fully formally proved safe across platforms. Exact counterexample needed; do not add a speculative universal lock protocol unless native I03 emits a false fact. Closing the verifier before further I03 use must refuse, not count incomplete data.
5. **Economics:** 2048 sourcefree respondents consumed ~24.8 MB retained certificate; 100k and total physically compact C11+indexes, peak scratch, real process-tree aggregation, cold query cost, multi-tenant cost, large one-respondent cardinality and crash/reattachment remain unproved. Current \`Sequence.__getitem__\` uses SQL OFFSET; native bulk selection uses indexed ordered scans instead, but random-access O(offset) may become unacceptable in a future adapter.
6. **M01–M18 original scientific coverage:** source equivalence P01–P20/T01–T18, original sample/weights/route authority, crosswave science, replay expiry/currentness and actual original35 native material are not issued by sourcefree tests. Original \`m01_m18_coverage\` is inherited and carried, **not rebuilt from an independent scientific source oracle**.
7. **S2-A G5/Pair 1 S1-B:** S2-A #944 is G5-pending, and S1-B accepted sourcefree code in #948 is unmerged into this ancestry. No cross-pair equivalence, upstream G5, protected CAS, physical S2-C, or authorized original/native operations have been manufactured.

**Most consequential B challenge:** Make the **entire I02 validator and its full semantics/selector/closure proof genuinely streaming from a real sourcefree governed input** with no old all-ref and all-object materialization, then prove normal I03 first-consumer equivalence, typed negative, changed/restored root and resource behavior against a nontrivial fixture. Avoid unrelated refactoring; conserve this candidate's proven external selector/root/hostile tests if correct, and replace them if a superior simpler solution is demonstrably better.

## 6. Explicit G1–G5 limits

- **G1 PARTIAL:** all original M01–M18 inherited I02 atoms identified and closure/semantic-selector sourcefree proof bound; complete independent source-direct external-memory validation and current source equivalence not established.
- **G2 PARTIAL:** real I02 + native I03 changed/restored fact/replay and cold certificate select; full source-direct saved cold native C11 is a separate S2-C dependency, while the old required in-memory I02 construction remains an S2-B defect.
- **G3 PARTIAL:** coherent self-rehash, omitted members, duplicate/paired selectors, state, authority/body/ref/route cases checked at sourcefree inherited scope; not an independent comprehensive original35/100k negative court.
- **G4 PARTIAL:** disk-sorted bounded *new index* algorithm and 2048 fixture resource/cold/crash evidence, but not upstream full build, peak scratch, fully aggregated process-tree or 100k integration.
- **G5 NOT_RUN:** requires another nonauthor reviewer **other than A and B** after their final descendant; no self-acceptance.

**Provisional return:** \`REVISE_EXACT_DEFECT\` at full original S2-B contract, while preserving the runnable **S2_SOURCEFREE_DERIVED_EXTERNAL_CERTIFICATE** contribution. Not \`ACCEPT_SCOPED\` for the entire packet. No protected merge, no source rights, no claim of native full physical or N11/Sorok readiness.

Agent B must read this full handoff **and** independently examine exact code diff, original #919/909, source and CI evidence. The disclosed defects are attack leads, not claims that no better design exists.
