# PYAT HQ268 G01 — two-defect authentication completeness and G2 replay-identity correction — R1

**STATUS:** ISSUED_NEEDS_HUMAN_LAUNCH__NO_SELF_ADOPTION
**REPOSITORY:** `maidiu/rawlsing`
**BRANCH:** `agent/space-bunny-pyat-hq268-g01-d1-d2-auth-and-replay-identity-repair-r1`
**ORIGINAL ENGINEERING HEAD:** `bdc65ff897a8e6a61988fc2bb3a325e7f198222a`; corrected candidate code currently `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`.
**AUTHORITY:** Resolve actual canonical `integration/pre-main-reconciliation-r1:HQ_HANDOFF/LATEST.json` and sealed HQ268 packet, exact branch commission tip, correct worktree/interpreter before edit.
**AGENT:** Existing Space Bunny / OpenCode source-free engineering AUTHOR lane.
**MODEL / INTELLIGENCE:** MiMo V2.6-Flash (`opencode/mimo-v2.6-flash-free`), as actually reported in the same author/reviewer session. State actual model and effort; do not label it Sol.
**TEST ENVIRONMENT:** Existing qualified macOS CPython 3.11.3 source-free local checkout, if actually available. No new machine/worktree is provisioned by HQ.
**NO LIBRARY / RAW SURVEY / EXTERNAL SOURCE / EE14 G0b / SELECTED T1 / T2 / DEPLOYMENT / NATIVE F7 AT07 / V3.**

## Input and independence caveat

The HQ267 R01 review branch `agent/reviewer-pyat-hq267-g01-authentic-g2-xor-final-hostile-r1 @ 2678a10d9abb397682333bddddd24b24f9e9761c` legitimately returned exactly four review documents, one ahead/zero behind commission tip `b48b5b4fb7cec83b1977aaeaeaab37ce74aba94f`, no code changes.

**DISCLOSED MANDATORY DISQUALIFIER:** That review session had also authored the HQ266 candidate and actually ran `opencode/mimo-v2.6-flash-free`, not commissioned GPT-6 Sol High. It is **author-adjacent self-review**, not a separate independent hostile acceptance. NO G1 PASS or adoption can be based on it, even though the worker ran 75 + 199 + 80 = 354 green, zero skips, fresh checkout pinned to code SHA, same machine/interpreter, and wrote independent probe code. The 199-vs-99 commit-message discrepancy is a confirmed typo at this author-adjacent evidence grade.

Its proposed **negative counterexamples** D1 and D2 were separately checked by HQ against the immutable `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py @ 4ec0038d218a20cc92f114e28fd6c1de4ebd71f5` source and `rawlsing_next/pre553_service_source_applicability.py @ 3e40caca29e8c96ee1f412f919cfc7dba63f96c4`. HQ treats them as independently source-verified correction requirements, NOT acceptance of the self-review's independence.

Read all four HQ267 R01 return files at the pinned review commit under `WORKER_RETURNS/PYAT-HQ267-R01-G1-AUTHENTIC-G2-XOR-FINAL-INDEPENDENT-HOSTILE-REVIEW-R1/`, especially `02_ADVERSARIAL_FINDINGS_RUNTIME_GRADE_AND_MINIMAL_EDGE.md` D1/D2 and R1/R2.

**Frozen original positive**: HQ266 4-respondent AT09 original `xor_fixture()` and real source-applicability→accepted G2→bound F8 path MUST remain intact, with q1 C|A=1 n2 (C0=1,C1=1), q2 C|A=1,B=0 n1 (C0=0,C1=1); source free, same release. Existing 22 original and 53 newly-authored tests (75), G2/SA (199), C1/query (80) remain regression obligations. All those counts are author evidence, NOT independent QA.

## Correct exactly the two independently source-verified failures

**D1 REQUIRED — owner-identity completeness cannot be vacuous.**
At original ingress `_authenticate` lines 595–596:
`sorted(k for k,v in observed.items() if k in expected and expected[k] != v)`.
The `if k in expected` condition lets owner setup pass `owner_identity={"q1":{}, "q2":{}}` (or only `raw_denominator_support`) and still issue a selected technical receipt. No external data-only adversary can supply `owner_identity`; this is an internal owner-setup completeness defect, not a deployed-client exploit.

**Minimum**: enforce the exact required full observed identity-key set before any admitted serve; preferably validate per-cell trusted `owner_identity` at owner-construction AND fail closed again before compare; accept only exact necessary canonical keys (reject missing keys, wrong types, optionally unknown extraneous keys), then compare **every** required field without `if k in expected` holes. Raise `SelectedIngressAuthenticationError` with exact missing/mismatched keys and **no applicability/G2/F8 invocation** on incomplete material. Preserve original trusted source/grammar authority and real C1 evidence authentication. Add effective tests for empty q1, single-key q1, missing provenance, missing C1 identity and correctly complete control, positive F8 count >0 and no F8 count for all rejects. Do not create an independent cryptographic trust root.

**D2 REQUIRED — canonical complete accepted G2 receipt identity, no ad hoc 6-key subset.**
Original ingress `_build_receipt` lines 690–702 builds `g2_receipt_hash = semantic_hash({ six chosen fields })` omitting `receipt_id`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `canonical_replay_only_order`, and `authorised_authority`. The selected origin hash only transitively includes the truncated G2 value, contradicting the exact G2 receipt/replay-binding claim.

**Minimum**: replace handcrafted subset with real accepted `CandidateClassApplicabilityReceipt.replay_identity()`, which is `semantic_hash(self._material())` (adopted SA owner lines 629–631) and binds the complete canonical receipt. Keep technical `g2_receipt_hash` field only if it now equals the exact `receipt.replay_identity()`, and ensure `origin_receipt_hash` includes it. Test semantic-hash parity with accepted primitive and discrimination for omitted receipt identity/material (through a legitimately constructible receipt test or a clearly labeled isolated record-construction test, never forged operative G0b authority). Preserve exact source/release/permission, technical `authorizing=False`, no fake CURRENT.

**R1/R2 residue — calibration, NOT authority to redesign.** R1 owner identity is recomputed from owner-held source-free fixture and is not independent custody root; preserve that limitation explicitly. R2 notes live `_source` and `_cells` dictionaries remain mutable even though `_owner_identity` and returned scope snapshots are frozen. If you can do safe shallow container-only freezing without breaking original C1/G2 tests, do so and test; otherwise correct any inaccurate blanket `deeply immutable owner material` prose to mean only genuinely frozen fields, and retain R2 as a precisely bounded trusted-harness limitation. Do NOT change source objects' semantic refs, mutate original AT09 fixture, silently broaden scope or reclassify this as deployed security.

## Preserve exact remaining G1 behavior and trust ceiling

F1 source-free actual accepted C1→SA→G2 binder→bound-F8; F2 original same-respondent q1/q2; F3 provenance substitution refused BEFORE F8 despite accepted F8 hash parity; F4 actual `ZERO_SUPPORT` native pre-F8 negative, separate `NO_ADMITTED_SOURCE` outcome, handler-only cases named as such; F5 exact builtins; F6 real binder permission/source/release hostiles and positive non-vacuity. `SelectedRequest` is data-only. F8 parity does not itself prove custody. Same-process arbitrary Python, independently certified root and real deployment remain UNPROVED.

**ONLY EDIT** exactly:
- `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py`
- `rawlsing_next/tests/test_pre553_ee14_c1_owner_authenticated_ingress_hq262.py`

**ONLY ADD** the FOUR return documents:
- `WORKER_RETURNS/PYAT-HQ268-G01-D1-D2-AUTH-COMPLETENESS-AND-G2-REPLAY-IDENTITY-MINIMAL-REPAIR-R1/00_D1_D2_EXACT_IMPLEMENTATION_AND_PRESERVED_G1_GRAPH.md`
- `WORKER_RETURNS/PYAT-HQ268-G01-D1-D2-AUTH-COMPLETENESS-AND-G2-REPLAY-IDENTITY-MINIMAL-REPAIR-R1/01_COMMITTED_SOURCE_FREE_TESTS_AND_NEW_COUNTEREXAMPLES.json`
- `WORKER_RETURNS/PYAT-HQ268-G01-D1-D2-AUTH-COMPLETENESS-AND-G2-REPLAY-IDENTITY-MINIMAL-REPAIR-R1/02_AUTHORITY_INDEPENDENCE_CEILING_AND_UNRESOLVED_RISKS.md`
- `WORKER_RETURNS/PYAT-HQ268-G01-D1-D2-AUTH-COMPLETENESS-AND-G2-REPLAY-IDENTITY-MINIMAL-REPAIR-R1/03_DISPOSITION.json`

No adopted C1/F8/SA/G2/B5/G3 or fixture/code/witness changes, no extra files/branch mutations, no grants. Execute qualified actual source-free tests on **final committed SHA**, compare exact changed files, record actual model/interpreter SHA/commands/exits/skip counts, and commit+push own branch. No self-review, self-adoption, G1 PASS, trust root or T1 claim.

**AFTER RETURN, HQ MUST USE A NEW GPT-6 SOL HIGH SESSION UNCONNECTED TO THIS AUTHOR, FOR REAL INDEPENDENT HOSTILE REVIEW.** Model label alone does not establish independence; disclose prior author involvement and ensure the reviewer did not write or execute the author lane.

**STOP:** `HQ268_G01_RETURNED_FOR_HQ__NO_SELF_ADOPTION`.
