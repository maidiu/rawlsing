# EE-R4A — WVS authority-complete proving-pair selection

You are **EE-R4A — WVS SELECTION-CRITICAL AUTHORITY-COMPLETE PROVING PAIR**.

Repository: `maidiu/rawlsing`
Library: `NO`.

Exact grain: `SELECT_ONE_NEW_PROSPECTIVE_WVS7_TWO_QID_PROVING_PAIR_FOR_OP003_THROUGH_OP006_USING_ACCEPTED_AUTHORITY_COMPLETENESS_ONLY`.

Read current canonical HQ authority from `HQ_HANDOFF/LATEST.json`, then this commission.

Binding inputs:
- EE-R3F premise freeze `9082b85d0963c6505e2b9dc9b417cfb881b8cb1b`;
- EE-R3D court `fbd151af338c6b56c5d8072015425ab6cb05bbc3` proving the first frozen pair unresolved;
- accepted WVS7 exact source/universe identity and current qid/source-coordinate authority;
- accepted current routing/applicability and response-category semantic authority;
- EE-W1 OP003–OP006 semantic definitions/oracles.

## Purpose

R3F's first two-qid pair was prospectively selected from a known routing-residual set and then correctly failed when R3D preserved both qids as unresolved. This commission may select a replacement proving pair because the pair is a physical-comparison fixture, not a substantive empirical hypothesis. Selection must nevertheless be prospective and outcome-blind.

## Selection law

Construct the eligible WVS7 qid set using **only accepted pre-result authority**. A qid is eligible only if all required facts are already governed:
1. exact membership in the adopted WVS7 proving universe and exact source variable/coordinate identity;
2. positive/known routing/applicability/risk-set authority sufficient for OP003;
3. exact response-category/raw-state semantic authority sufficient for OP004–OP006 at the intended RAW/descriptive grain;
4. respondent-bound/codistribution identity sufficient for same-respondent joint evaluation;
5. no unresolved state that would have to be inferred away.

Do not inspect marginal distributions, joint values, conditional results, association strength, effect size, model performance, or A/B/C performance when deciding eligibility or pair order.

Sort eligible qids by canonical `question_implementation_id`. Select the **lexicographically first pair** satisfying the complete authority predicates above and exact same-source/same-respondent coadministration needed for OP005.

If fewer than two qids satisfy the complete predicate, return the smallest exact blocker. Do not relax a requirement and do not select from unresolved rows.

## Freeze after selection

For qid-0 and qid-1, freeze exact:
- implementation IDs;
- WVS7 source-variable/coordinate refs;
- response semantic refs;
- routing/applicability/risk-set refs;
- denominator identities;
- same-respondent/coadministration identity;
- OP003 routing/denominator query;
- OP004 qid-0 marginal query;
- OP005 qid-0 × qid-1 exact joint query;
- OP006 qid-1 conditional/subgroup query using only an already-governed applicability/risk-set condition, unless an exact governed response-category conditioner is already independently authorized;
- replay determinants and candidate-neutral semantic oracle procedures.

Produce a machine-readable eligible-set receipt proving outcome-blind selection and a deterministic replay of the selection rule.

Do not run empirical results except where strictly required to verify identity/risk-set mechanics after the pair has already been frozen. Do not inspect or compare A/B/C. Do not create new routing or response semantics. Do not touch MAIN or semantic PRE-MAIN.

PASS means WVS7 OP003–OP006 have one exact lawful proving pair ready for final oracle materialization. Return the smallest exact blocker otherwise.
