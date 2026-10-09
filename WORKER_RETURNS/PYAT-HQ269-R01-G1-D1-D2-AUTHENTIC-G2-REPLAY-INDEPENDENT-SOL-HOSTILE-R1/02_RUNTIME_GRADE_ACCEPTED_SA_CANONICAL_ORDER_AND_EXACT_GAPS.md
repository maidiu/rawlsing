# HQ269 R01 — independent runtime grade, accepted SA canonical replay order, and exact next edges

**Disposition:** `HOLD_EXACT_UNPROVED_EDGE` for independent FINAL G1 acceptance. The implementation has a **source-static affirmative assessment** at bounded source-free G1 development grain; it does **not** have a reviewer's independently verified 375-test run, a separate source-custody root, or an operative T1 permission. Do not adopt.

## 1. Reviewer's actual tools, model, and independent execution grade

The reviewer is a **new GPT-6 ChatGPT session**, not the HQ266/HQ268 MiMo/OpenCode author session and not the disqualified HQ267 author-adjacent self-review. The product model family is GPT-6; the precise *Sol High* product runtime/effort selection is **not independently inspectable** via the connected GitHub API. This does not establish a special computational configuration and is not claimed to.

**Actual accessible environment:** connected GitHub read/write API and ephemeral programmatic source-inspection JavaScript (via the API). The commissioned independent controlled local Python 3.11.3 worktree, checked-out SHA, approved dependencies and test runner were **not available** in this session. No Python pytest, clean worktree, verified interpreter, checkout, nor source-free test was executed by the reviewer. The source-static detector independently fetched immutable Git blobs and inspected the literal code/data; this is **not executable substitution** for accepted tests.

**Truthful evidence table:**

| Test or fact | What author reported | Independently established here |
|---|---|---|
| HQ268 code HEAD | `46a95a8e...` | Verified exact commit and immutable candidate module/test blobs |
| HQ268 author-return HEAD | `f10523e...` | Verified exact SHA, two commits ahead/zero behind author commission, two code/test modifications and four documentary additions |
| G01 court | 96 passed | Source contains 82 named `test_` functions; parametrization may produce 96 collected; **not collected/executed here** |
| Four SA/G2 courts | 199 passed | Adopted SA/G2 source read and behavior traced; **not executed here** |
| C1/query regressions | 80 passed | Accepted C1 and source-free XOR fixture inspected; **not executed here** |
| Combined | 375 passed, no skips | Author arithmetic `96+199+80=375`; **no independent test result/skip accounting** |
| STEP A | PASS | Author claim; underlying grammar authority and fixture construction independently traced at source level only |
| Independent hostility | separate review demanded | New reviewer generated and examined static adversarial cases, with no author code edits; **executable results still HOLD** |

**Missing execution protocol:** an *already authorized independent* runtime pins code commit `46a95a8e62e3e790da3b84dfa7ab1ae4d5bce6bd`, verifies ingress blob `74e6ee826e8b6a2adebe84969fedcea5716d5b63` and test blob `64b6c747f76a1909b676566e6b529ed10456d33b`, clean worktree and actual configured interpreter; runs focused G01, accepted four G2/SA, C1/query regression, combined and STEP A plus at least the independent D1/D2/R1/R2 discriminators in `01_...` JSON; captures exact commands, pytest collection, pass/fail/skip/xfail, exit codes and clean status. No numerical pass count should be inferred from code names.

## 2. Independent D1 finding — completeness repaired, custody authority unchanged

**Verified:** `REQUIRED_IDENTITY_KEYS` is exactly 19 unique fields (ingress L151–171) and `IDENTITY_KEY_TYPES` is its exact same 19-key map L176–196. `_require_complete_identity` L199–249 refuses missing, extraneous and mistyped fields, including `bool` for the `int` denominator. It runs in constructor for each q1/q2 (L538–558) and again in `_authenticate` (L761–770). The observed preimage builder has a symmetrical closed-key drift guard and L815–823 compares every required key unconditionally. Old `if k in expected` loophole no longer exists. The guard executes after C1 but before SA/G2/F8 (serve L634–661), so the source clearly enforces **pre-applicability refusal**.

**Independent static discriminators:** empty expectation, single-key expectation, missing provenance, missing C1 identity, missing q1-only field, extra field, wrong exact type, post-construction replacement and complete-but-wrong release all confront explicit source refusal. Positive complete material follows a separately present C1→SA→G2→bound F8 route. Author tests cover these (test L1155–1332), but nothing in this review claims observed runtime exits.

**R1 ceiling:** expected owner material is computed by executing the *same* `fx.direct_condition_composition` via `_compose` (test L142–196), and then stored as an internal reference. The check proves consistency with that trusted fixture identity; it does not prove an independently issued source-authorized preimage. An attacker who owns the producer and expected material in the same process can re-author both. This is outside HQ262's external DATA-ONLY threat model and should be retained as an explicit LIMITATION, not disguised as a trust-root security fix.

## 3. Independent D2 finding — local replay binding repaired; exact SA-wide nonsemantic-order residual

Source audit of **accepted SA blob `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`**:

- `CandidateClassApplicabilityReceipt` at SA L560–575 declares **12 dataclass fields**: `receipt_id`, `service_request_set_identity`, `service_id`, `candidate_class_ref`, `candidate_class_coverage`, `decisions`, `outcome`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `canonical_replay_only_order`, `authorised_authority`.
- Its `_material()` at SA L614–627 includes **11**: `receipt_id`, `service_request_set_identity`, `service_id`, `candidate_class_ref`, `candidate_class_coverage`, `outcome`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `decisions`, `authorised_authority`. It excludes `canonical_replay_only_order`.
- `replay_identity() = semantic_hash(self._material())` L629–631. Therefore replacing **only** `canonical_replay_only_order` in a frozen receipt object (e.g. `dataclasses.replace`) necessarily leaves its accepted SA `replay_identity()` invariant. This is a **source-derived logical consequence**, not a claim to have executed that mutation.
- SA `as_dict()` L633–652 **does** carry `canonical_replay_only_order`. The SA resolver L791–805 derives it deterministically from `_sorted_replay_only(receipt.admissible_source_universe_refs())`. The SA authority explicitly says serialization ordering is **REPLAY_ONLY** and has ZERO rank/selection/priority semantics; this is distinct from the source-admission set used by G2.
- Corrected ingress `_build_receipt` L911–921 does **not** hand-hash the old six-field subset: `g2_receipt_hash = receipt.replay_identity()` is the **actual adopted owner primitive**. The canonical-origin preimage includes `"g2_receipt_hash": g2_receipt_hash` L951 and **separately includes** `"g2_canonical_replay_only_order": list(receipt.canonical_replay_only_order)` L957; final origin hash is `semantic_hash(origin_material)` L1007. Thus changing that field in the **origin material** changes the local technical origin hash even though it does not change accepted SA replay identity. This is the source-static **local closure** of D2.
- The public `SelectedIngressReceipt` dataclass L368–415 does not expose the canonical-order list as its own field, only the resulting local `origin_receipt_hash`. Accordingly an external verifier possessing only the returned dataclass cannot reconstruct its entire origin preimage. That is consistent with its stated **owner-held local technical witness** ceiling; it is not proof of independent remote receipt verification. No claimed universal full-material replay identity.
- **OPEN OWNER-NATIVE NORMATIVE QUESTION:** is canonical replay order intentionally a derived *presentation* artifact excluded from the authority-bearing semantic identity, or is every replay field required to change the accepted replay identity? The adopted SA law favors the first interpretation (deterministic, no ranking), while the name `replay_identity` and inclusion of order in `as_dict` create a plausible exact-contract concern for downstream consumers. **No silent SA rewrite or G1-specific grant.** If HQ requires replay-byte identity across every field, authorize a separate *SA owner semantic derivation and compatibility court* (including change effects on other consumers), NOT an ingress-only patch. A change to accepted `_material` is OUTSIDE this commission. If HQ affirms order is only deterministic nonsemantic serialization, retain the local additive binding and document that SA replay identity intentionally omits it.

**Classification:** local D2 implementation source-static **corrected**, accepted SA global semantics **NORMATIVE_HOLD**. Not automatically a counterexample to bounded G1 positive because the owner itself deterministically derives the order and G2 admission is set-like, not ordered-selection.

## 4. Independent R2 finding and F1–F6 status

- Ingress L529–558 copies top-level source/cell maps into `MappingProxyType`, deeply freezes owner identity, validates original query authority, and rejects client request subclasses. Nested `_source["universe"]`, `_source["release_ref"]`, registry, producer callable and model-rule objects are still trusted references. A principal executing privileged arbitrary Python within the owner process can potentially mutate shared objects or monkeypatch code; no remote isolation is deployed, and this possibility must not be passed off as a closed threat. The author explicitly documents this limitation, correctly.
- F1 real accepted path `_call_c1`→`_authenticate`→`SA.resolve_service_source_applicability`→`B.bind_service_applicability_to_f8_scope`→`B.evaluate_bound_positioned_subject_possibility`. No locally hashed scope substitute or direct raw F8. Exact `target_use_permission_refs` relation from SA request to G2 binding, release and source coherence; `requested_currentness_claim=None`.
- F2 original frozen `xor_fixture` builds the **same four synthetic respondents R00,R01,R10,R11 with C=A^B**; q1 C|A=1 has denominator 2 with (C0,C1)=(1,1); q2 C|A=1,B=0 has denominator 1 with (0,1). Per-cell plans are different producer conditions on one release, with corresponding original C1 fact, query, predicate and denominator lineage; no marginal-product estimate.
- F3 at ingress `_authenticate` checks original evidence authority/provenance refs, C1 identity, denominator and source/release pre-F8. Test L670–720 distinguishes same F8 numeric hash from altered provenance at low level; candidate source is wired to refuse substituted evidence before bound-F8. This is an owner expectation check, not signer authentication.
- F4 native zero-support is driven by same source-free C1 with impossible condition (test L724–758); no admitted source is from actual SA decision (test L774–787). Other typed negatives are *handler-staged*, not natural producers on the XOR. No mislabeling as missing G0b.
- F5 exact plain dataclass/tuple/string request and read-only owner top-level containers; not deployed IPC security.
- F6 actual G2 refusal guard probes cover wrong permission/release/source, low-level F8 lacks selected origin receipt, and positive counter non-vacuity (`f8_calls=1` in test source L390–395). These remain **source-static verifications of test intent, not observed independent test runs**.

## 5. Exact HQ disposition / minimal next edge

**Proposed HQ posture:** keep corrected source-free G1 code **CANDIDATE_PENDING_INDEPENDENT_QUALIFIED_RUNTIME_AND_SA_NORMATIVE_CLARIFICATION**. Accept the *technical mechanism source-static* assessment for independent design feedback only; do not issue `PASS_AT_DECLARED_G1_DEVELOPMENT_GRAIN` as an executed certification from this review.

Smallest edges:
1. **Independent runtime witness**: a qualified independent, already-authorized environment runs at pinned code SHA and returns count/exits/skip/clean proof and the D1/D2/R1/R2 attack court. The missing element is a runtime witness, **not** a demonstrated need to redesign corrected ingress.
2. **SA owner semantic interpretation**: determine whether `canonical_replay_only_order` belongs in accepted `CandidateClassApplicabilityReceipt.replay_identity()` or remains intentionally nonsemantic, then prove/record compatibility for all consumers; if change necessary, issue separately authorized owner-native court.
3. **First actual T1 connection after G1 (distinct jurisdiction):** operative EE14 **G0b model-use and selected-service grant** tied to exact serving purpose/source/authority, followed by the accepted G3/B5 actual selected-service current/as-of consumption join and independent acceptance. Source-free G1 development does not provide either; cannot manufacture G0b through fixture `AuthorityRef` or G2 source-admission.

**Terminal:** `HQ269_R01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.
