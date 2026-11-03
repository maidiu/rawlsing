# W8-V — negative receipts / hypothetical gate recomputation

**Pinned guide:** `a9ebf71e62d84e5dcc599662e976eca7fcd0e623`. **Method:** direct static parse of `14` gate records, exact member-ref equality, explicit selected mode, and all active same-target gates. A gate with all prerequisites is *eligible to attempt its target work*, never proof that the target is issued/completed. Hypothetical receipt is not a native issuer receipt. No S2/S3 work was run. Reviewer prior-subject proximity prevents independent acceptance.

## Counterfactual matrix

| Scenario | Gate result(s) at exact guide | Consequence |
|---|---|---|
| 1. C9 no mode (all other native fixtures green) | `G-C9-NATIVE-INTEGRATE: BLOCKED_MISSING_REQUIRED_RECEIPT`; `G-C9-T-ANY: MODE_UNSELECTED`; `G-C9-T-IF-ACQUIRED: NOT_APPLICABLE_NOT_TRUE`; `G-C9-T-IF-NOCHANGE: NOT_APPLICABLE_NOT_TRUE` | Not READY; explicit claim mode absent and IF not vacuously true. |
| 2. C9 positive selected, no original Rule T | `G-C9-NATIVE-INTEGRATE: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-C9-T-ANY: BLOCKED_SELECTED_MODE_UNISSUED`; `G-C9-T-IF-ACQUIRED: BLOCKED_MISSING_REQUIRED_RECEIPT` | Base syntactically eligible on hypothetical same-scope receipts; selected positive T missing => C9 native BLOCKED. |
| 3. C9 scoped O07 selected, no O05 | `G-C9-NATIVE-INTEGRATE: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-C9-T-ANY: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-C9-T-IF-NOCHANGE: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-C9-T-IF-ACQUIRED: NOT_APPLICABLE_NOT_TRUE` | Conditional only: if O07 is genuinely original-issued at matching scope and base verified, NO_CHANGE-only assertion may qualify, NEVER positive acquisition. |
| 4. A5 curated only; no generated Gate4 | `G-A5-RUN-COMMON: BLOCKED_MISSING_REQUIRED_RECEIPT` | Gate5 BLOCKED, even if safety and 0–3 proofs are green. |
| 5. A5 Gate4 true but no operated S14 | `G-A5-RUN-COMMON: BLOCKED_MISSING_REQUIRED_RECEIPT` | Gate5 BLOCKED: independent operational rights proof remains missing. |
| 6. A5 Gate4 true but no approved S15 | `G-A5-RUN-COMMON: BLOCKED_MISSING_REQUIRED_RECEIPT` | Gate5 BLOCKED: human-study protocol/consent owner not issued. |
| 7. Exact tuple matrix issued, no joint owner signoff | `G-E008-JOINT-OWNER-CONTRACT: BLOCKED_MISSING_REQUIRED_RECEIPT`; `G-E008-C9-COSPEC: BLOCKED_MISSING_REQUIRED_RECEIPT`; `G-E008-C12-COSPEC: BLOCKED_MISSING_REQUIRED_RECEIPT`; `G-E008-JOINT-BUILD: BLOCKED_MISSING_REQUIRED_RECEIPT` | Selected joint spec may be discussed; no signed contract, no READY adapter/VERIFY. |
| 8. Signed matrix AND matching co-spec receipts, independent C12 RED | `G-E008-JOINT-OWNER-CONTRACT: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-E008-C9-COSPEC: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-E008-C12-COSPEC: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-E008-JOINT-BUILD: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED`; `G-C12-SF-VERIFY: BLOCKED_MISSING_REQUIRED_RECEIPT`; `G-C12-NATIVE-INTEGRATE: BLOCKED_MISSING_REQUIRED_RECEIPT` | Only specified adapter BUILD prerequisites become conditionally eligible; cold/anchor/independent new-tuple VERIFY and native C12 still BLOCKED; RRIF 8090 RED persists. |
| 9. S10 design without historical E021 scoped review | `G-S10-SPECIFY: ELIGIBLE_ONLY_NOT_TARGET_ACCEPTED` | S10 design is READY_TO_SPECIFY from source-defined memory law, not implementation verified. |

## Exact conjunction semantics

The C9 positive branch requires **both** `G-C9-NATIVE-INTEGRATE` (all six actor/event/Rule A/selected writer/later actual E2/mode members) **and** `G-C9-T-ANY` (the selected O05 or O07). `G-C9-T-IF-ACQUIRED` / `G-C9-T-IF-NOCHANGE` are scoped `C9@ACCEPT` claim gates. Unselected IF has `NOT_APPLICABLE_NOT_TRUE`, not an empty-success value. An issued O07 cannot support `POSITIVE_ACQUISITION`. Qualification of a gate's prerequisites cannot be used as a synthetic receipt for that gate's target output.

A5 `G-A5-RUN-COMMON` has real conjuncts: `S11@VERIFY`, `S14:LOCAL_GUIDE:OPERATED_CONTROLS@VERIFY`, `S15:LOCAL_GUIDE:HUMAN_PROTOCOL@ACCEPT`, `S5:LOCAL_GUIDE:PLURAL_EVALUATION@ACCEPT`, `A5:LOCAL_GUIDE:CLAIM_MODE@SPECIFY`, `A0:LOCAL_GUIDE:GENERATED_GATE4_SUBSTITUTION@VERIFY`, `A1/A2/A3@VERIFY`, and `A5:LOCAL_GUIDE:ACTUAL_PRODUCT_SCOPE@VERIFY`. `G-A5-HUMAN-RECEIPT-VERIFY` then additionally requires actual human receipt; `G-A5-ALL-ACCEPT` does not erase these upstream constraints. Original Sorok 100 §8 is the primary Gate4→Gate5 authority.

`G-E008-JOINT-OWNER-CONTRACT` needs **both** the completed E008 matrix receipt and `J-E008-C9-C12:LOCAL_GUIDE:SIGNED_MATRIX@SPECIFY`. Even its eligibility is not an issued `J-E008-C9-C12@SPECIFY` output. If the joint owner supplies exact writer and reader specs, `G-E008-JOINT-BUILD` can become eligible at the selected sourcefree scope, but `G-C12-SF-VERIFY` separately needs independent same-tuple cold/severance/restore and anchor; `G-C12-NATIVE-INTEGRATE` separately requires C11,C10,C9 and external native anchor. A newly selected c784 reader must not inherit the old `7bf2da...` `4387dc...` acceptance. RRIF `598d...` independent `8090a1...` `REVISE_MATERIAL_DEFECTS` T1/M1/C1/D1 is a distinct persistent negative.

The S10 design counterexample uses two direct source-known KNOW leaves and deliberately removes E021 entirely: G-S10-SPECIFY remains eligible, while no cold fork/actor memory runtime follows. The alternative S12 `G-S12-SOCIAL-IF` likewise has no positive outcome when social mode is unselected; it does not block a selected single-user early scope.

## Independent-negative restoration test

**Hypothetical one-leaf positive:** source-qualified `E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY` for an exact selected writer/reader/root/version matrix. This changes the first member of `G-E008-JOINT-OWNER-CONTRACT`; it does not satisfy the second signed joint-owner member or either `C12@VERIFY` cold/anchor member. **Independent RED preserved:** `8090a1ea308ab17f302f55bb2639c3e4cd774c7a` reviewed `598d9e9eaba5143950c63317705fd09104fbf463` as REVISE_MATERIAL_DEFECTS. Even if an old 7bf status is restored at its *own* cut, it cannot turn the new c784 actor_meta/root/anchor tuple green. A proper reverse dependency query must therefore show eligible joint owner **discussion**, ready independent S5/S13/S14 design lanes, and held adapter verification/native C12.

## Integrity of static calculation

This calculation intentionally requires **complete exact receipts** in the hypothetical `Set` rather than merely checking that a predecessor gate can be attempted. It does not infer receipt freshness, same-root compatibility, signatures, human approval or owner adoption. Those are independent proof obligations. The six `S11` evidence pointers absent from the leaf table in the actual guide are explicitly unresolved and connected to held predecessor gates, not silently treated as satisfied.
