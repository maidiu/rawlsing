# PYAT R3 S2-B/P2-02 — Agent A R5 reciprocal adversarial return

**Status: \`REVISE_EXACT_DEFECT__DIRECT_SOURCEFREE_BUILDER_PROPOSED__NEW_NATIVE_TESTS_NOT_RUN__G5_NOT_RUN\`.**
This is a genuine direct-candidate construction advance, not an accepted whole S2-B terminal certificate. No source/actor/scientific/host/current or protected integration rights are issued.

## 1. Exact frozen lineage / sources / artifact

- Original scope: [#919 S2-B/P2-02 G1–G5](https://github.com/maidiu/rawlsing/issues/919), [#909 R3/R3C/R3S](https://github.com/maidiu/rawlsing/issues/909), [PROGRAMMA PYAT](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md), [adopted MCR-lite](https://github.com/maidiu/rawlsing/blob/6a5c12f04323d74001f9632063ec907f4fc4468e/CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md). Retain substantive whole-mission no-drop, actual native consumer, source/science/authority boundaries and genuinely independent G5; do not add new courts.
- Original A #952 \`d5d6577b557fa8ced2dbb42d190ab254ab983b19\` → B #954 \`f5ee89b8e700ac14cf266c2e3eae4c25f021c349\` → A #961 / #965 \`e82a7ee92a32cc8b327d0685267d4aaea1d86a1a\` → **B R4 #971** \`a11b92b767a9a16cc6ee4e312e67e9982fc01210\` → **this descendant** [draft PR #974](https://github.com/maidiu/rawlsing/pull/974).
- **Exact frozen CODE / TEST / WORKFLOW commit:** \`edd0611d1ea0e80a47692635fe3bd73a079f1bec\`. Later documentation-only commits on this branch must not be mistaken for tested source.
- **Branch:** \`agent/pyat-pair2-s2b-a-direct-candidate-20261112-r5\`, based directly on B R4's frozen commit, not a competing rewrite. This document and \`01_G1_G5_RECEIPT.json\` follow the code cut.
- Protected \`integration/pre-main-reconciliation-r1\` observed \`6a5c12f04323d74001f9632063ec907f4fc4468e\`, untouched. S2-A #944 G5-pending, Pair1 S1-B accepted sourcefree but live direct adapter not yet integrated, S2-C separate, W03/W04 remain paused.

**Changed source against B R4:**
1. \`rawlsing_next/_pre553_external_i02_certificate.py\` — new, separately named \`DIRECT_SCHEMA\` with canonical direct-only ancillary-table commitment. \`ExternalI02Roots.schema\` defaults to the old schema; original B root records/initializers remain valid. Cold verifier binds exact required schema; native I03 **refuses a direct-schema certificate as a private legacy I02 release**. Old materialized input path is preserved.
2. \`rawlsing_next/_pre553_direct_i02_sourcefree.py\` — a new direct sourcefree typed-section generator/producer, backed by the same SQLite whole-object+complete-semantic-selector commitment and independent roots. It requires an original \`SourceReleaseManifest\` and all 13 actual family iterators, typed absences, replay authority and tie-order fields. It **never** calls \`validate_c11_source_release\`, creates \`C11LogicalRelease\`, builds \`ReplayManifest.closure_refs\`, or constructs a Python all-object/all-ref list. Full source/authority, respondent/universe, duplicate occurrence, family census, instrument-version alias and routing/coordinate/weight membership checks are imposed as streamed objects are persisted. Core authority registry snapshots are materialized separately, not the entire respondent corpus. 
3. \`rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py\` — sourcefree typed-input and actual native historical I02/I03 comparator tests, changed+restore, same logical root under different chunk/row order, omitted family, duplicate occurrence, locally rehashed index, forged root, one-shot input reuse and 2,048 one-shot event-resource probe.
4. \`.github/workflows/pyat-pair2-s2b-external-i02.yml\` — the new direct tests join B/A's full inherited suite and run the direct material probe separately. No CI run can be counted green while a runner is unavailable.

## 2. Legitimate B R4 criticism and why it stays fixed

B demonstrated a real logical/API failure: \`ExternalI02Roots\` was a frozen dataclass but \`isinstance\` admitted an overrideable subclass whose release/source/replay persona could change between cold verification and native I03 binding. B replaced \`isinstance\` with exact-class admission, committed the hostile native test and maintained the older 88 cases. The frozen B R4 source retains this safeguard. I found **no legitimate source issuer requiring subclassed root records**; the existing certified builder constructs the concrete base dataclass. B's repair is retained unchanged. It is not native GREEN at B R4 HEAD because its CI job failed before execution.

A's earlier genuinely useful defenses (B fake-reader/subclass/DB swap/closed lifecycle, A SQL read-session/TEMP/BINARY-collation/no-clobber and oversized malformed-closure memory refusal) all remain in the ancestor. Their old historical sourcefree evidence must not be erased or transferred as test proof to this new commit.

## 3. New real implementation, not another read-session wrapper

The inherited fatal G4 problem was **construction required the old full \`C11LogicalRelease\` including heap-sized \`ReplayManifest.closure_refs\`**. This R5 delivers an actual alternative entry point:

\`SourcefreeDirectI02Sections\` (typed section streams) → source manifest and authority check → per-object original validators / exact reference verification → disk-backed global object census, respondent-namespace and occurrence uniqueness → complete native/canonical/component selector table and paired instrument-version check → deterministic whole-root → atomic no-clobber SQLite artifact → independently supplied physical and semantic cold verification.

The producer takes real typed C11 sourcefree candidate sections; a fixture adapter consumes a \`C11SourceReleaseCandidate\` even when \`candidate_replay_manifest=None\`. For genuine bounded *upstream* production, the caller instead supplies one-shot decoded section iterators; **an accepted live S1-B/E-to-this-input adapter is not yet proved**, and the legacy candidate test fixture itself is originally tuple-shaped. No S1-B source/current issuer is invented.

**Historical functional succession (most consequential addition):** the exact old \`_candidate_projection_semantic_hash\` and \`ReplayManifest.content_hash\` / \`C11LogicalRelease.release_ref\` formulas are reconstructed from sorted SQLite cursors by streaming canonical JSON. For each family the ref order is the original \`ExactRef.key\` order, and both exceptional source closure refs are explicit exact inputs. The original \`ReplayManifest\` **object/closure tuple is never built by this producer**. Old \`ReplayManifest\` record labels M16–M18 are retained in the reconstructed coverage map. The original C11 seal is **never issued**; only the computed historical hash is exposed in signed-by-nobody-yet direct-schema metadata. That distinction is enforced by the original native I03 installer's direct-schema refusal.

## 4. Hostile hypotheses, negatives and source-identity limits

**B R4 false-negative check:** no sourced requirement for subclasses of \`ExternalI02Roots\`; preserving an exact concrete immutable root is the narrower legitimate boundary. No speculative rights HOLD.

**New tests committed, to be executed at their exact HEAD:**
- Direct input with \`candidate_replay_manifest=None\` and valid original typed sections produces a cold-openable complete object/selector map.
- Historical \`validate_c11_source_release\` is invoked **only on the independent TEST oracle**. Test asserts exact direct \`candidate_projection_hash\`, replay ref and release ref equality and exercises actual \`_build_release_index\` / \`_select_respondent_events\` native first-selector parity of every respondent/event and native question selected ref.
- Changed real typed response with the same sourcefree source identity changes the complete external root and selected event ref. Reconstructed restored material yields exactly the old logical root. Any changed original-source content would require a new competent source-equivalence CURRENT decision before production, not this test.
- Missing event/coordinate/routing/question/respondent/authority family refuses declared original manifest census; duplicate occurrence refuses even if attacker changes declared counts.
- Attacker modifies saved index; a held original physical+logical root cannot be replaced by local rehash.
- One-shot section streams consumed twice cannot silently produce an acceptable second whole certificate; 2,048 unique occurrence events are generator-produced rather than pre-materialized in a tuple. This is one-respondent/event-cardinality resource pressure, not 100k respondents/6GiB original35.

**Reconstructed replay parity is a TESTABLE HYPOTHESIS until the repository native court executes.** A local independent 2,048-ref pure Python/SQLite semantic-shape reproduction found equal materialized-vs-streamed candidate and replay SHA256. That locally demonstrated algorithmic property **is not** proof that actual source classes and all native I02/I03 tests passed.

## 5. Actual execution and CI limit

Exact commands:

\`\`\`bash
git checkout edd0611d1ea0e80a47692635fe3bd73a079f1bec
python -m pip install pytest pyarrow pandas pyreadstat
PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_external_i02_certificate.py \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py
PYTHONPATH=. /usr/bin/time -v python -m pytest -q -s -o addopts='' \
  -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_direct_i02_sourcefree.py::test_s2b_a5_direct_2048_one_shot_event_stream_and_cold_memory
\`\`\`

**This branch's exact code/test suite has NOT EXECUTED.** [CI run #43301647636](https://github.com/maidiu/rawlsing/actions/runs/43301647636) at source cut \`edd0611d1ea0e80a47692635fe3bd73a079f1bec\` reports failure with no assigned runner, zero steps, no tests and no resource measurements. Other contemporaneous PYAT runs share the startup-only issue. It cannot be represented as code RED or GREEN. Old [B 88/88 historical GREEN](https://github.com/maidiu/rawlsing/actions/runs/43278005794) proves **only B #954's older source cut**, not #971/#974.

Independent local stdlib proof only: for 2,048 synthetic exact refs stored in SQLite, both candidate projection and replay SHA256 produced by the streaming shape equaled canonical JSON over a materialized array. This does not exercise the imported Rawlsing classes. Actual new native comparator remains committed but **NOT_RUN**.

## 6. Rejected alternatives / conservation

- Keep optimizing only the derived certificate/adding root-security wrappers: rejected as insufficient for original G4 direct source construction.
- Mark direct input as a v1 I02 validated \`C11LogicalRelease\`: rejected; would counterfeit authority and make B's 88 sourcefree tests meaningless.
- Create a fake legacy \`ReplayManifest\` by secretly materializing a 100k ref tuple: rejected; the historical hash is streamed, and no private validation seal is manufactured.
- Replace native I03's evaluator with an SQL statistics model: rejected; tests use real native selector owner, full native empirical fact owner stays unchanged.
- Treat successful local SQL/JSON primitive as full M01–M18/100k engineering acceptance: rejected.
- Preempt S2-C physical body-store, W03/W04 paused work, P01–P20/T01–T18 source-equivalence CURRENT decision or independent G5: rejected as separate owner authorities.

## 7. Most serious unresolved challenges and proof boundaries

1. **Immediate:** run exact R5 native sourcefree suite and 2,048 streamed-event memory bench on a functioning executor; repair any actual red (especially byte-identical original replay digest, old native selector ref equivalence and B's original 88 regression). A failed-to-start workflow is no answer.
2. **Source issuance:** prove a real qualified S1-B/E one-shot governed producer at this exact ABI. The current compatibility factory takes an original tuple-shaped sourcefree fixture; this does NOT establish end-to-end 100k input RSS, true original35 source equivalence, or competent CURRENT permission.
3. **M01–M18:** original semantic validation/typed negative/authority flows were ported, but *source-direct exhaustive parity* under all hostile and real native cases is not yet independently executed. Replay M16–M18 byte parity is executable test, not established by author prose.
4. **Physical/first consumer:** direct-schema roots are intentionally refused by legacy I03 *release installation*; the newly sourced native first-reader comparator checks actual selected refs without promoting direct input to a private seal. S2-C owns authenticated cold physical event-body store; full direct release native I03 facts and replay still need properly qualified integration.
5. **G4 resources:** real process-tree RSS, scratch, total retained C11+index, cold/repeated native query, crash/restart and 100k/6GiB integrated production test are unrun. A 2,048-event one-respondent test is not enough.
6. **Expected root:** producer returns logical and physical roots, but no external original35 competent issuer stores/attests them. Tests holding a returned root locally are engineering negatives, not source or authority certification.
7. **Hostile physical process:** arbitrary co-resident Python introspection/hostile kernel/active filesystem attacks beyond descriptor-pinned root/atomic no-clobber are not claimed to be impossible.

## 8. G1–G5 exact conclusion and next attack

| Gate | Author return | Why not terminal |
|---|---|---|
| G1 | **PARTIAL, substantial candidate** | All original family stream owners, typed absences, source/authority and reconstructed original M01–M18 replay semantics authored; historical native parity and S1-B/E real input still unexecuted/unwired |
| G2 | **PARTIAL** | Full cold rooted direct selector and actual I03 comparator tests committed, but no executed new full native fact/replay parity or direct native release issuance |
| G3 | **PARTIAL** | A/B hostile safeguards preserved; direct source omissions, duplicate occurrences and locally rehashed index cases committed, not run |
| G4 | **PARTIAL** | New builder no longer depends on the old materialized release/replay closure, but true end-to-end input economy, process-tree, scratch, 100k/6GiB and new 2,048 material test unproved |
| G5 | **NOT_RUN** | Neither duel agent may independently accept its own output; requires completed scoped G1–G4 at a frozen SHA |

**Decision: \`REVISE_EXACT_DEFECT\`.** This R5 is materially beyond root-hardening—a real alternative sourcefree bounded I02 construction path with testable original replay hash conservation—yet it is **not** an accepted whole source-direct I02 certificate. No protected merge, no source/current/science rights, no silent upstream S2-A promotion. Next agent should attack the historical hash-equivalence test FIRST and the live source→stream ABI NEXT; fix actual red cases, not add another board.
