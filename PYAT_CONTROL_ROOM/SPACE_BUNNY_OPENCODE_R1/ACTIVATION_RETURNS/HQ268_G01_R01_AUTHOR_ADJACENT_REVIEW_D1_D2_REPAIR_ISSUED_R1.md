# HQ268 — author-adjacent HQ267 review disqualified for independence; D1/D2 independently source-verified, narrow correction issued

**Decision:** `HQD-2026-10-09-268`.
**Canonical control parent:** `10499013efc1033e33719146d4fa07f5c2d3b943` (HQ267).
**Inherited immutable HQ267 handoff:** `27d534fc04412205b17e66561c4c71cd256af7d5`.
**Semantic PRE-MAIN:** `1f47063c3205a45888b3c55e81e7485943ed1390` unchanged.
**No G1 adoption, no G0b, no T1/T2, no production/security certification.**

## 1. Return identity, source and actual independence

HQ267 R01 review branch `agent/reviewer-pyat-hq267-g01-authentic-g2-xor-final-hostile-r1` advanced **one ahead/zero behind** exact commission tip `b48b5b4fb7cec83b1977aaeaeaab37ce74aba94f` to return HEAD `2678a10d9abb397682333bddddd24b24f9e9761c`. Changes exactly FOUR documentary files under `WORKER_RETURNS/PYAT-HQ267-R01-G1-AUTHENTIC-G2-XOR-FINAL-INDEPENDENT-HOSTILE-REVIEW-R1/`. No code/test, accepted owner, source fixture, control or other branch edit. Return is valid for documentary **intake**.

**INDEPENDENCE DISQUALIFIER (binding):** R01 voluntarily disclosed that the SAME session had previously executed the HQ266 author engineering lane, and it was actually `opencode/mimo-v2.6-flash-free`, not the assigned GPT-6 Sol High. Regardless of fresh clone or independently written probe code, it is an **author-adjacent self-review**, NOT the required distinct-agent independent adversarial acceptance. It may NOT issue or support `PASS_AT_DECLARED_G1_DEVELOPMENT_GRAIN`. Its source-static `FAIL_REQUIRED_CORRECTION` is a worker proposal, not independently adopted reviewer judgment. Future genuine review MUST occur in a wholly separate GPT-6 Sol High session/workflow with no author participation. Label/model selection alone does not satisfy independence.

This self-review did re-execute Mac CPython 3.11.3 pytest 9.1.1 in a fresh clean clone pinned to exact code SHA `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`, same host/interpreter as author, NOT HQ-provisioned separate runtime. Report A 75, B 199, C 80, combined 354, all exit 0 and zero skips, plus HQ253 STEP A. These are **same-session cross-checks**, stronger than repeated authored claims but not independent review. One character `99` in author final commit prose is inconsistent with frozen return JSON showing `199`; R01 reran 199, so adjudicate this as a supported documentary typo, without treating self-review as independent certification.

## 2. HQ's own direct source-static verification of two precise defects

HQ independently fetched immutable G01 code `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py @ 4ec0038d218a20cc92f114e28fd6c1de4ebd71f5` at `3829fc4e63fc9fb0d802e8af237dfab2febc3d23`. It also fetched adopted SA owner `pre553_service_source_applicability.py @ 3e40caca29e8c96ee1f412f919cfc7dba63f96c4`. **No independent HQ runtime probe was executed**; executed counterexamples are author-adjacent evidence only.

- **D1: REQUIRED OWNER-IDENTITY AUTH COMPLETENESS FLOOR.** Lines 595–596: `sorted(k for k,v in observed.items() if k in expected and expected[k]!=v)`. Missing owner-held expected keys are silently ignored; the method never requires full key set, even though full C1 provenance authentication is asserted. The self-review's `owner_identity={"q1":{},"q2":{}}` and single-key accepted traces are plausible and code-static absence is conclusive. No external data-only client can supply this field, so describe as owner-setup completeness flaw, NOT deployed exploit. Require exact full-key comparison and missing-key zero-F8 tests.
- **D2: REQUIRED CANONICAL G2 RECEIPT IDENTITY.** Lines 690–702 hand-roll a six-key `g2_receipt_hash`, excluding `receipt_id`, `no_applicable_source`, `candidate_class_binding`, `request_key`, `canonical_replay_only_order`, `authorised_authority`. The technical `origin_receipt_hash` embeds this incomplete hash, contradicting full canonical G2 receipt/replay identity claim. The accepted SA owner supplies `CandidateClassApplicabilityReceipt.replay_identity()` at lines 629–631 = `semantic_hash(self._material())`, providing complete owner-native replay identity. Require that exact method, zero invented permission and discrimination tests.

The other self-review findings are **nonadopted residual observations**: R1 owner_identity recomputes producer fixture identity from same trusted source-free owner objects, not independently sourced custody root; code correctly declares NOT A TRUST ROOT. R2 mutable `_source` and `_cells` while `_owner_identity` / read-only `owner_scope_material()` snapshot are deeply frozen: either safe shallow container-only freeze or scope the immutability claim, no new root or architecture.

Original positive *candidate* remains technically substantial but unadopted: C1→accepted SA→G2→bound F8, q1/q2 exact same-four XOR n2/n1, provenance counterexample and ingress pre-F8 refusal in properly populated owner setup, genuine `ZERO_SUPPORT` and typed negatives, exact builtin caller request, hostiles/no bypass. No independent adoption grade.

## 3. Next commission exactly two defects, no redesign

Issued **HQ268 G01**:
- Branch `agent/space-bunny-pyat-hq268-g01-d1-d2-auth-and-replay-identity-repair-r1` from exact HQ266 G01 author return HEAD `bdc65ff897a8e6a61988fc2bb3a325e7f198222a`.
- Commission tip `e64f53a70a5167a7c79712038c9b1e14ae6c747c`.
- Commission `WORKER_COMMISSIONS/PYAT-HQ268-G01-D1-D2-AUTH-COMPLETENESS-AND-G2-REPLAY-IDENTITY-MINIMAL-REPAIR-R1/00_COMMISSION.md`.
- Agent: existing Space Bunny/OpenCode SOURCE-FREE AUTHOR lane.
- **MODEL / INTELLIGENCE:** MiMo V2.6-Flash (`opencode/mimo-v2.6-flash-free`), actual reported configuration. This is deliberately an author **repair**, not another purported independent review. At launch worker must report actual runtime/model; HQ has not launched it.
- ONLY edit the same TWO unadopted G01 ingress/test files, add FOUR own return docs. Accepted C1/F8/SA/G2/B5/G3, original fixture, user data and semantic PRE-MAIN untouched.
- D1 requires exact complete identity-key floor and full comparison before SA/G2/F8, with new empty/single/partial owner expectations and honest positive non-vacuity. D2 requires `receipt.replay_identity()` and origin receipt full binding, with exact tests. Preserve F1–F6 and native XOR. R1/R2 limitation documented and at most safe shallow container hardening.
- Final committed-SHA tests and honest author report, NOT self-review or self-adoption. Then HQ must commission a **genuinely independent Sol High** separate reviewer with separate qualified runtime status before G1 acceptance. No real EE14 G0b or T1 grant.

**Status:** `ISSUED_NEEDS_HUMAN_LAUNCH`, not running merely because GitHub branch exists.

## 4. Inherited holds intact

G2 HQ259 accepted and G3 HQ262 local lifecycle accepted only at original grades; actual CURRENT/as-of selected T1 and G0b operative service model-use remain UNISSUED. Ghana R5/R9 original SAV carriers absent on inspected Mac; canonical LiTS 3.4GB P1 object absent. No same-host re-search or unwarranted raw survey execution. No EE12 temporal pair, FF02 LiTS source relation grant, N9/N10W two-family world, T2 empirical service, native F7/AT07 service root or V3 actor.

**NEXT:** launch HQ268 G01 author D1/D2 minimum repair; then true independent Sol review on final committed candidate. Physical custody separately.
**TERMINAL:** `HQ268_HQ267_SELF_REVIEW_INDEPENDENCE_REJECTED__D1_D2_HQ_SOURCE_STATIC_VERIFIED__MINIMAL_REPAIR_ISSUED__NO_G1_PASS_G0B_T1_T2`.
