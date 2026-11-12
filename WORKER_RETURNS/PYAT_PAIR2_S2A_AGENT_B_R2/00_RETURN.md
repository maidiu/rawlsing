# PYAT Pair 2 — S2-A ONLY — Agent B R2 constructed adversarial return

**Disposition:** `SOURCEFREE_NATIVE_S2A_CORRECTED / NONAUTHOR_G5_PENDING`. This is **not** accepted S2-A, original35 authority, protected integration, or external-memory storage proof.

**Original governing contract:** [Issue #919](https://github.com/maidiu/rawlsing/issues/919), controlling R3 S2-A G1–G5. Sourcefree implementation is authorized on an isolated branch, but source/native survey rights, independent receiving, protected merges and the paused W03/W04 remain distinct. **Adversary source:** [PR #932](https://github.com/maidiu/rawlsing/pull/932), frozen tested final HEAD `3ab8037135e2393489e02ba3e1caa066e829626d`; protected PRE-MAIN source baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Our candidate:** [Draft PR #934](https://github.com/maidiu/rawlsing/pull/934), branch `review/pyat-s2a-alias-binding-r2-20261112`, stacked directly on the frozen #932 HEAD. Unique isolated branch; no Mac/local exclusive lease or HQ appointment asserted.

## 1. Reconstructed S2-A machine and source
- The native owners are `pre553_c11_ingest.py` (I02 closure, replay and exact native-question membership), `pre553_c11_integrity.py::QuestionVariableBinding`, `pre553_empirical_objects.py::RespondentEvent`, `_pre553_query_predicate.py::_select_respondent_events`, `pre553_empirical_query.py::_release_index_for`, and `_pre553_query_eval.py` (real I03 respondent, routing, facts, negative and replay).
- The S2-A exit is **genuinely I02-validated sourcefree selector completeness on the real I03 first reader**, with native/canonical/component and occurrence conservation, false-absence refusal, restoration and bounded selected reads. It is **not** the rest of Pair 2 and must not purport to issue original-source authority.
- The original I02 `_validate_questions_and_events` checks `(universe,native_question)` membership; `_validate_question_authorities` and `validate_public_carrier_object` require positive mapping authority. Neither independently ensures **the canonical target claimed by each event equals the exact question binding's canonical target**. The new S2-A witness originally reproduced this unverified event claim verbatim.

## 2. What Agent A genuinely accomplished (preserved)
- A complete source-derived selector-keyspace witness built from an already I02-sealed sourcefree release; independently held root rather than local cache self-hash.
- Full selected native/canonical/component alias ranges, exact ref/occurrence/state digest checked **before** state filtering; merge dedup preserves repeated distinct occurrences.
- Real `execute_empirical_query` comparisons including two identical-value occurrences, changed secondary index → `INTEGRITY_FAILURE` → restore exact original QueryExecutionResult.
- H28 typed routing UNKNOWN stays nonpositive; H29 source/release/root mismatch refuses; H30 bounded *selected-page* interface. These do **not** establish durable external-memory or full 100k memory.
- Agent A accurately disclosed that its tests installed a derived index by directly writing test-only cache and attestation fields; that is a lower integration grade than a qualified I03-owner API, **not** evidence that the I03 consumer was never exercised.

## 3. Native defect proved with an actual RED execution
**H31:** A genuinely I02-accepted candidate contains a `QuestionVariableBinding` authorizing canonical target `DECLARED`, while a `RespondentEvent` names `INVENTED` under an independently positive mapping authority. The original S2-A `I02SemanticRangeWitness.from_validated_release` certifies `INVENTED` as though it were authorized. **H32:** The question binding says canonical mapping `NOT_APPLICABLE`, but the event carries `INVENTED`; S2-A again certified it.

[GitHub Actions initial RED](https://github.com/maidiu/rawlsing/actions/runs/43177874759) at test-only commit `ce8c9d7ff585a3078aa6a56b714592105d7eddb6`: **56 PASS / 2 FAIL**. Both failures: `DID NOT RAISE SemanticRangeIntegrityError`. The fixtures first assert real `ingest_c11_source_release(...).accepted`. These are cross-record semantic contradictions *inside* an I02-accepted sourcefree release, not untrusted replacement objects or synthetic-only data structure models.

The point is not that an accepted source grant becomes counterfeit merely because one mapping differs; it is that **S2-A's additional claim of independently certified canonical selector meaning was unsound**.

## 4. Correction implemented, including a defect in my first repair
**Code:** `rawlsing_next/_pre553_verified_semantic_range.py`. Build the exact permitted canonical alias set from I02-sealed `QuestionVariableBinding` records scoped to the same universe and native question. Never trust an event's canonical reference as its own mapping grant. Fail closed before generating a witness if an event native question is not bound or if its claimed canonical alias is not among actual accepted binding aliases; a typed absent binding cannot be silently promoted.

My initial fix used `canonical in any(version_mapping)`. That was still unsound if multiple instrument versions for the same native question supply **conflicting canonical aliases** but `RespondentEvent` has no instrument-question-version field to choose between them. H37 independently proved that case against I02-accepted input. [Second RED](https://github.com/maidiu/rawlsing/actions/runs/43178909254) at `644e341819b7f79311b70c1f37ddd49adb1e217f`: **62 PASS / 1 FAIL**, again `DID NOT RAISE`. Final fix refuses the ambiguous canonical event when two or more distinct canonical aliases are asserted for one native question under the chosen universe.

**Preservation positive:** H36 adds a genuine I02-accepted second `QuestionVariableBinding` for a different instrument-question version sharing the same native ref but **not** claiming a conflicting canonical alias. The exact two-occurrence native selector remains intact. H35 preserves a genuinely authorized canonical alias; the original H26/H27 same-value and authorized component regressions remain green.

**Scope limitation:** This is a fail-closed check on the S2-A *additional certified selector*, not a retroactive rewrite of I02's authority rules or scientific issuance. If real original sources contain multiple conflicting native→canonical grants, their appropriate scientific disambiguation remains a separately competent source/version issue. Refusal here is correct: S2-A cannot guess which version applies.

## 5. Better actual native first-consumer installation
**Code:** `rawlsing_next/pre553_empirical_query.py::install_sourcefree_i02_certified_i03_range` is a narrow opt-in entrypoint owned by the existing I03 executor. It requires an exact `C11Repository`, exact release/universe, and original-source-derived `I02SemanticRangeWitness` compared to the separately provided held root. The owner authenticates the complete selector against the sealed I02 corpus, derives the existing native `_ReleaseIndex`, validates exact respondent-domain equality, and only then atomically swaps the cached index *and* its existing identity attestation under the repository lock. The ordinary `execute_empirical_query` path then uses that same accepted derived index; no fabricated release, duplicate statistical engine or general S2-D saved-store adapter.

H33: baseline full native query → install through real I03 owner → exact full result equality → mutate **only** installed selector posting (I02 release intact) → actual I03 returns typed `INTEGRITY_FAILURE` → re-install from original I02 → exact original QueryExecutionResult restored. H34: wrong held root refuses **without changing** either the previously attested index pointer or its attestation, and the native fact remains SUPPORTED. H35: genuine canonical alias and native-only override through owner-installed index.

The original test-only poison helper remains only for deliberately constructing hostile invalid indices; **normal admission no longer requires the test harness to fake cache attestation**. New owner function is included in `pre553_empirical_query.__all__`, and the sourcefree GitHub Actions path filter includes its file.

## 6. Verified GREEN and exact test ceiling
[GitHub Actions green run](https://github.com/maidiu/rawlsing/actions/runs/43179035819) at tested code/test HEAD `e14d287aca837633c7e6ffeeed4ee088e4dfdd08`: **63 PASS, 0 FAIL** across `test_pre553_verified_semantic_range.py`, `test_pre553_empirical_query.py` and `test_pre553_c11_repository_ingest.py`. This contains original Agent A's 56, H31–H32 and H33–H37. The workflow reports `63 passed in 1.47s` under Python 3.11, pytest and pyarrow. A separate canonical-tree check may be read on the final document-bearing HEAD; no extra proof promoted on the basis of metadata.

Full executed command:
```
PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_verified_semantic_range.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  --junitxml=s2a-pair2.xml
```

H30 remains a 64-respondent narrow proof of bounded *pages*, not an O(all-corpus) build-memory qualification. No read-store persisted disk across process boundaries, no fresh-source native host credentials, no 100k/6GiB claim.

## 7. Refuted accusations and regressions checked
- **No real I03 execution in original #932:** FALSE. Agent A executed actual native I03, but installed the certified index through a test-only private cache mutation. We improved the admission seam rather than denying their evidence.
- **A complete event-ref corpus ensures canonical grant consistency:** FALSE. Two native-I02 accepted contradictory cases and an instrument-version ambiguity proved otherwise.
- **One binding per native question is mandatory:** FALSE as a conservation rule for this S2-A stage. H36 passes with two instrument versions and intact native occurrences. Different *canonical grants* under the same native ref are a distinct, unresolved ambiguity.
- **Our new opt-in installer is an external issuer or production-default saved reader:** FALSE; neither attempted nor claimed. It is an in-process sourcefree owner API and preserves the default legacy index path.

## 8. Real surviving defects / authority HOLD
1. `QuestionVariableBinding.component_subitem_ref_or_typed_absence` and event-level component/subitem aliases do not yet receive the same exact cross-record equivalence check implemented for canonical mappings. Agent A's positive matched component tests and poisoned-secondary-omission tests remain valid; **a mismatched positive component binding remains an unresolved S2-A attack surface**, not falsely declared proved here.
2. Native `RespondentEvent` has no instrument-question-version discriminator; when true competing grants are legitimate, S2-A cannot decide source-meaning precedence. Correct scientific authority or a qualified richer source/lineage contract is needed, not guessed selection.
3. `certified_i03_events` and witness creation still traverse the complete existing in-memory I02 release; `_root_payload` holds the complete selector-keyspace digest dictionary. The selected-query cursor is bounded in extra memory but build memory remains O(all events/keys); no external physical persisted proof.
4. No external root publisher/current issuer, no source↔C11 P05 source equivalence or original35 native/science rights, no original 100k process-tree or restart proof. These are outside S2-A's present **sourcefree** grade.
5. The selector low-level method can return an empty sequence for a target with no postings, whether the target is instrument-admitted or not. Native scientific authority/routing remains separate: **empty event selection is not a warranted empirical negative**.
6. New code is opt-in only. It does not switch production-default I03 to the candidate. No saved-source carrier, Batch/I05/issued/learned completion can be inferred.

## 9. Immutable handoff / strongest challenge back to Agent A
- Frozen opponent: `3ab8037135e2393489e02ba3e1caa066e829626d`, #932. Our stacked draft: #934 / `review/pyat-s2a-alias-binding-r2-20261112`.
- Tested implementation and source tree: `e14d287aca837633c7e6ffeeed4ee088e4dfdd08` (63/63; independent G5 still pending). This document is a later report-only commit; **read back the final branch HEAD** rather than guessing it.
- Four code/workflow/test paths changed relative to Agent A: `rawlsing_next/_pre553_verified_semantic_range.py`, `rawlsing_next/pre553_empirical_query.py`, `rawlsing_next/tests/test_pre553_verified_semantic_range.py`, and `.github/workflows/pyat-pair2-s2a-semantic-range.yml`; this report fifth path. No protected or paused worker file changed.
- No full official independent receipt is claimed on behalf of HQ; same connected repository identity is not proof of independent human reviewer identity.
- **Challenge:** construct a *genuinely I02-accepted*, source-qualified component/subitem or conflicting-version variant where this sourcefree certified reader either overpromotes meaning or wrongly refuses legitimate history; repair the authority/lineage resolution without inventing an event question-version value absent from the actual object schema. Then test the real normal I03 first consumer with changed-result/typed-refusal/restore. If exact question-version resolution is unrepresentable, formally HOLD just that semantic promotion and preserve lawful native reads.

**Disposition: S2-A sourcefree native candidate materially strengthened; G5 nonauthor receiving pending. S2-B through S2-G untouched.**
