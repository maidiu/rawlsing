# PROGRAMMA PYAT Pair 2 / S2-A — Agent A counterattack R3

**Court:** SOURCEFREE S2-A CONSTRUCTED CANDIDATE; **G1–G4 PARTIAL, G5 PENDING; NO S2-A ACCEPTANCE**. This is the adversarial successor to B's improvement, not a rollback to A's original implementation.

**Governing:** #919 HQR-20261112-R3 S2-A only, #909 HQ exact-head programme; G1 nonloss/source-qualified aliases, G2 real native first consumer changed→refused→restored, G3 hostile negatives, G4 bounded resource/custody, G5 independent nonauthor receiving. S2-B–G and original35 rights/science/issuer/protected merge are outside this return.

## 1. Immutable ancestry, writer and test receipts

- Protected *read-only* original base: 6a5c12f04323d74001f9632063ec907f4fc4468e.
- Agent A original: PR #932, HEAD 3ab8037135e2393489e02ba3e1caa066e829626d.
- Agent B verified correction: PR #934, HEAD **c651c3519e83d2399717718ccff71a908e28a899**.
- This successor: PR #941, unique branch **agent/pyat-pair2-s2a-counterattack-r3-20261112**, based *directly* on B's immutable commit and with compare-and-swap branch head updates. No writer use of B's branch, #932, PRE-MAIN or paused W03/W04. This branch is not an external worker lease; no Mac/process/runtime lease is asserted.
- **Hostile RED:** commit **6febd930139888e8c71a295e65359ec335d94558**; [run 43181090722](https://github.com/maidiu/rawlsing/actions/runs/43181090722): **4 failed, 67 passed**. Test fixtures first successfully invoked actual I02 ingest.
- **Repair GREEN:** commit **d85349f7a667bf06b2ae8d545332dbf5f082d6be**; [run 43181373887](https://github.com/maidiu/rawlsing/actions/runs/43181373887): **71 passed**.
- **Broader nonloss GREEN:** commit **64f93fc155ec4244c545f7b87503432e7de50cd2**; [run 43182502362](https://github.com/maidiu/rawlsing/actions/runs/43182502362): **105 passed in 7.37s**. Its predecessor's expanded run 43182323396 was 104 passed / 1 missing dependency (pyreadstat), corrected in the workflow, *not* a production failure.
- Final frozen HEAD is the later report-only commit carrying this document; code is identical to 64f93fc. Do not substitute the baseline #934 CI as proof of our changes.
- All code, tests, workflow and report changes are on one successor ancestry; protected merge/independent review have **not** occurred.

Run with Python 3.11, pytest, pyarrow, pandas, pyreadstat:

    PYTHONPATH=. python -m pytest -q -o addopts='' -p no:cacheprovider \
      rawlsing_next/tests/test_pre553_verified_semantic_range.py \
      rawlsing_next/tests/test_pre553_empirical_query.py \
      rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
      rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
      rawlsing_next/tests/test_pre553_c11_execution_view.py \
      rawlsing_next/tests/test_pre553_i03_grouping.py \
      --junitxml=s2a-pair2.xml

Changed vs B: rawlsing_next/_pre553_verified_semantic_range.py, rawlsing_next/tests/test_pre553_verified_semantic_range.py, .github/workflows/pyat-pair2-s2a-semantic-range.yml, and this report. Unmodified from B: rawlsing_next/pre553_empirical_query.py owner installer, original _pre553_query_predicate.py selector, existing I02 and native science.

## 2. B's genuine victories retained, no false counterattack

B proved with genuinely I02-accepted H31/H32 RED that a positively mapped RespondentEvent could claim canonical target B when exact QuestionVariableBinding asserted A or typed absence. B's canonical cross-record check is necessary. B also discovered H37: an event lacks instrument_question_version and cannot choose freely between conflicting *version* grants. Both repaired and retained.

B's install_sourcefree_i02_certified_i03_range is an actual I03-owner, exact-root-checked opt-in cache-attestation publication; original Agent A did exercise production I03 but only via test-only injected cache. B correctly strengthened this. Preserve the full native fact/replay/ref equality and poison/refusal/reinstall test.

We find **no substantiated basis for calling these achievements false**. One broad restriction needed refinement: the B implementation rejected any two distinct canonical aliases for the same native question even when they were legitimate disjoint subitems of the **same instrument version** and an event identified a specific component. H43 is a real I02-accepted preservation counterexample, not an attempt to undo H37's competing-version refusal.

## 3. New native sourcefree defects, with RED first

H38: QVB component A, event claims B; I02 accepts, B S2-A certifies B, where none was granted.

H39: QVB component typed NOT_APPLICABLE, event claims A; I02 accepts, B certifies that component anyway.

H40: two versions of one native question grant different components A/B, event supplies A without a version identifier; B certifies A despite the undecidable origin version.

H43: same version has two separately admitted pairs (canonical C1, component A) and (canonical C2, component B); event asserts (C1,A). I02 accepts, but B's unversioned union cardinality check falsely treats these as conflicting instrument versions.

RED: 4 failed / 67 passed at 6febd930..., run 43181090722. H42 also guards a subtler false authorization: separately admitted canonical C1 and component B can be combined from *different* QVB rows to fabricate (C1,B). B already rejected that case accidentally through len(canonical aliases)>1; the successor must reject it by the correct relational reason while permitting H43.

## 4. Actual repair

Replaced the flat per-native canonical alias set in _pre553_verified_semantic_range._bindings with the exact original **universe/native → instrument version → set of (canonical-ref-or-absence, component-ref-or-absence)** bindings. At every event with any claimed alias, all possible source instrument versions must contain at least one **single** binding row jointly supporting every claimed alias. Sourcefree RespondentEvent has no instrument-question-version field: never choose only the convenient version. Distinct same-version component rows are valid and retained.

This rejects H38/H39/H40, the cross-row H42, and preserves original B H31/H32/H37, while allowing H41 same-version component siblings, H43 same-version paired canonical/component siblings, H44 repeated compatible grants across versions.

Original native selection remains unchanged: full native/canonical/component union with native_only override, typed state and occurrence multiplicity, exact original I03 facts/negatives/risk/replay and owner installer. H45 tests changed sourcefree I02 source values through the owner and actual native I03 result, then restores the earlier fact; the source release labels differ between variants, so it is changed-source response evidence, NOT a claim of a single isolated physical-cell-delta P05 result.

## 5. Independently discovered conservation limit — source-backed occurrence provenance

Production source-backed pre553_source_backed_c11_facade._event explicitly uses:

    component = occ.component_ref or _opt_ref(q.component_subitem_ref_or_typed_absence, "component")

That is a lawful *additional source projection route*, not identical by definition to a QVB component field. H46 uses the **real source-backed projection + physical sourcefree cells**, with an occurrence component ref and a typed-absent QVB component. I02 accepts it and the incumbent native I03 selector resolves the component. The corrected opt-in S2-A witness refuses certification because the sealed QVB alone does not contain the independently governed occurrence grant.

This is an **incomplete victory and a live nonloss boundary**, NOT a license to accept self-proclaimed event components. Within the I02-only release, no positive occurrence-rule sidecar/authority reference identifies the extra source-granted component; that evidence exists upstream in the projection but is not conveyed as an independently anchored component selector grant. Accepting arbitrary event.component would resurrect H38/H39. Making QVB the sole component grant universally would wrongly declare the source-backed projected occurrence invalid.

**Immediate safe behavior:** sourcefree opt-in certification refuses this unmatched component; incumbent native I03/release remains intact, and the reviewer must not claim universal source-backed component certification. **Required interface repair:** a Pair 1 qualified occurrence→component semantic sidecar/provenance ABI and independent I02 root/issuer, followed by a native query/read proof. No Pair 1 authority/physical source permission was fabricated in this turn.

## 6. Strong preservation and negative controls

- Real I02 acceptance for adversarial H38–H44, not toy ref maps; H26–H37 inherited tests remain green.
- Actual I03 owner installation, SUPPORTED fact identical to oracle, postinstall secondary-selector omission -> native INTEGRITY_FAILURE -> reinstall original equality.
- H27 mapped canonical/component aliases; H28 certified EMPTY events but ROUTING_UNKNOWN never observed zero; H29 mismatched release/source/root/semantic keyspace RED; H30 bounded 64-respondent pilot pages; H31/H32 binding contradictions refused; H37 conflicting versions refused.
- H41 legitimate component siblings and H43 component-qualified multiple canonical siblings positive.
- H42 attempted cross-binding canonical×component forgery refused.
- H45 sourcefree changed-value actual I03 cell effect and restoration.
- H46 real source-backed occurrence-level component survives native reader; extra S2-A certificate refuses unsupported QVB-only promotion.
- Expanded 105 tests include physical source-backed C11 projection, compact native event view, grouped I03 reuse, original empirical I03 and I02 ingest.

## 7. Still unfulfilled; what not to claim

G1: Full source-qualified component semantics remains **open** for occurrence-rule grants not persisted in current I02 component QVB; P1 source/sidecar contract required. Semantic native/canonical/component *QVB-supported* cases now proved. The original sidecar is not manufactured here.

G2: Actual native I03 owner/first-consumer negative and restoration proven; H45 changed sourcefree producer input and changed fact, but no externally authenticated physical source-byte severance or original35 source rights.

G3: Relevant internal H26–H46 hostile sourcefree positives/negatives proven at this grade. Current source issuer/as-of revocation and semantic authorization beyond QVB/replay are not proven and cannot be inferred from test green.

G4: I02 witness construction still expands full sourcefree sealed corpus and builds whole selector keyspace O(N). Native exact fact and denominator/replay have inherent large outputs. H30 64-row tracemalloc/page test is NOT whole process-tree 100k/6GiB, disk, scratch, crash/recovery or durable index proof. This S2-A packet creates no persisted estate to benchmark; none of S2-B/C physical work is claimed.

G5: Truly independent **nonauthor** receiving, including exact current PR ancestry and all original obligations, has NOT occurred. No protected merge, source-science/actor authority or HQ acceptance.

**Engineering:** meaningful sourcefree correction with 105 regressions. **Science:** no new positive original-source or structural grant. **Current permissions:** branch writes compare-and-swap only; no trusted current source/host issuer.

## 8. Next adversary's strongest falsifiers, and rejected inferior approaches

The reviewer should test genuine source-backed component occurrences against the new QVB-only gate, challenge whether multiple same-version canonical grants are science-qualified as subitems, and examine whether any one instrument-version grant with typed absence can coexist with an asserted alias from another. Demand exact original occurrence grants, not a convenient ref union. Try mutating index postings *after* I03 installation, and test wrong universe, source and as-of issuer freshness at the normal consumer.

Rejected:
- Keep B's flat canonical allowlist + component allowlist: H38/H39/H40 and cross-binding H42 are not authenticated; wrong.
- Require globally unique canonical and component ref for each native question: fails real I02-accepted same-version component siblings H43, erases functionality.
- Trust occurrence component because event has positive source semantic authority: H39 proves positive general authority is not an exact component-binding grant.
- Ban source-backed occurrence overrides by retroactively rewriting I02 or source-backed producer: violates existing lawful native source projection; a qualified sidecar is needed instead.
- Invent a new statistics or storage engine, or skip to S2-B/C/100k: unnecessary and beyond this exact task.
- Claim process-tree/cold persistence from local page measurements: false; held.

**Disposition:** S2-A still OPEN/REVISE–HOLD for comprehensive source-qualified component and G4/G5; successor R3 candidate is materially stronger than #934 at sourcefree QVB-backed selector grade. Freeze head for independent Agent B and nonauthor review; do not merge protected.
