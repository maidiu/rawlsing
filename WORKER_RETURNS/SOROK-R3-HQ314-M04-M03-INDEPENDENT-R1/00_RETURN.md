# M04 independent M03 causal court

**Verdict: REVIEW_REVISE.** The unchanged published expectation reproduces exactly: **587/587 PASS**. The **51 new independently frozen tests yield 41 PASS / 10 FAIL**, exposing three provenance failures. The original **nine CAN3 historical REDs execute as nine separate FAILs**. No skipped, xfailed or errored cases enter any denominator.

## Independent custody and execution

This is a fresh reviewer conversation with no authorship of M01, M02 or M03. No author conversation history was imported or read. One reviewer completed source review, test design, execution, adjudication and return; no assistants, model switches, external model/actor calls, semantic issuance or V3 operation occurred. The administrative dispatch supplied no review findings.

Checkout and direct `git ls-remote` both initially resolved the assigned branch to **2f4482ae23960037da4ebee84501916dc6e5b422**. The supplied worktree was detached and non-sparse; it was attached to the assigned branch and made sparse in place, reusing the existing Git object store. Writes are confined to this reviewer return. Exact source was reconstructed from Git, never from another author's live worktree.

The full commission, Sorok read-me, 00B, 00C §§3A/3B/5A, 00D, HQ314 intake, M01 preregistration, M03 return/source audit/all author test source, and accepted CAN008/ADP016/ADP017 source blobs informed the court. The exact immutable CAN008 candidate-named blob is accepted via its separate HQ adoption record; its historical label does not demote the adopted content.

The fresh expectations and executable source were committed at **3b529996ddd05c3c84225d2054428ff943091aef before their first execution**. Their SHA-256 identities remain unchanged. [Preregistration](02_FROZEN_EXPECTATIONS.md), [freeze manifest](03_FREEZE_MANIFEST.json), [frozen tests](review/test_falsifiers.py), [actual invocation](evidence/fresh/command.json) and [JUnit/stdout](evidence/fresh) preserve the falsification record. No failed expectation was edited, skipped or reclassified into a pass.

## Reproduction

| Court | Observed result |
| --- | ---: |
| M01 controls | 94 PASS |
| CAN3 inherited controls | 97 PASS |
| CAN2 inherited controls | 89 PASS |
| Relevant owner controls | 133 PASS |
| Unchanged M02 independent controls | 100 PASS |
| M03 author controls | 74 PASS |
| Published current denominator | **587 PASS** |
| Fresh M04 controls | **41 PASS / 10 FAIL** |
| Separate original historical CAN3 court | **9 FAIL** |

Before installing the M03 overlay, the same 413 tests passed and the unchanged M02 100 produced **98 PASS / 2 FAIL**. Both original M02 failures change to PASS under M03: unknown outer claim selection refuses as `CLAIM_SELECTION_UNKNOWN`, and the admitted 1999 claim selected for a 1998 response refuses as `CLAIM_SELECTION_AFTER_RESPONSE`. Those repairs are independently reproduced and remain accepted as bounded findings.

The [literal 587-case matrix](04_LITERAL_587_CASE_MATRIX.json), [fresh 51-case matrix](05_FRESH_51_CASE_MATRIX.json), [separate historical identities](06_SEPARATE_HISTORICAL_NINE.json), [execution totals](11_REVIEW_RESULTS.json), full stdout/JUnit, and actual native-state/function-source observations accompany this return. The historical nine are not part of either the 587 or the 51. The entire CAN3 585-case historical suite was not claimed rerun.

## Blocking findings

1. **P1 — coherent cross-cell owner substitution erases committed BELIEF (four failures).** Keep the original BELIEF cell's first-event journal and selection binding but replace its current owner checkpoint with the matching memory cell's legitimate NONE owner checkpoint. Restore accepts it; later evaluation emits epistemic **AMPLIFY**. The real first-event commitment still contains BELIEF, and no withdrawal occurred. `committed_binding` checks only equality of the canonical claim inside the committed and current owner states; `validate_consumption` treats missing snapshot/active/transition/permission together as lawful NONE without proving descent from the committed owner state. This is not the legitimate NONE positive control. [Four saved packet/response proofs](10_FAILURE_PROOFS.json); first concrete receipt: [CERTAIN owner splice](evidence/fresh/observations/erase_owner_CERTAIN.json). Relevant immutable source: `claim_provenance.py` lines 123–126 and 286–291.
2. **P1 — partial rollback resurrects revoked or withdrawn permission (four failures).** Make a real native SUPERSEDE_EXACT_RECORD to inaccessible BELIEF or a real WITHDRAW. Keep both native transitions, then restore only old active stance/snapshot/permission fields. Public restore and direct read both accept it, returning **REROUTE** with `PERMIT_FIRST_PERSON_BELIEF`, despite the retained later transition. `last_transition_ref` is verified against any matching historical transition, without proving it is the terminal applicable transition. [Supersession proof](evidence/fresh/observations/resurrect_SUPERSEDE_EXACT_RECORD_False.json), [withdrawal proof](evidence/fresh/observations/resurrect_WITHDRAW_True.json). Source lines 339–349. This is a hybrid snapshot, not lawful full checkpoint rewind.
3. **P1 — coherent digest validity substitutes for actual pre-state ancestry (two failures).** Replace a native effect's transition pre-state with an unrelated digest, then coherently recompute effect ID, stance map, transition ID, snapshot and permission binding. Leave the real ADP017 commit in the original journal. Both direct and transactional consumption accept **REROUTE** although the declared transition pre-state differs from the actual committed pre-state. Identity checks establish internal consistency but never compare the claimed ancestry to the real owner trajectory. [Outer response proof](evidence/fresh/observations/forged_ancestry_False.json), [direct read proof](evidence/fresh/observations/forged_ancestry_True.json). Source lines 206–226.

All ten failures reached an actual read; seven outer cases also committed a later response. These are executable finite checkpoint/restore counterexamples, not claims of OS-level compromise. Full valid same-contract checkpoint replay remains a passing control. [Independent evidence audit](review/audit_review.py) checks the original journal contradictions in the saved packets without replacing the failing assertions.

Required correction belongs to the candidate implementer: validate current owner-state descent and terminal applicable transitions against authoritative first-state/transition provenance, including genuine absence, revocation/withdrawal and pre-state identity. Preserve legitimate native addition/supersession/withdrawal, NONE and complete replay. Rejection must occur before productive consumption and remain atomic. This reviewer supplies no implementation patch or new semantic rule.

## Scientific interpretation and authority

The unchanged **36-arm 4 memory × 3 epistemic × 3 history factorial** remains causally intact at the constructed sourcefree grain. Actual E1 admission, native owner commit, later E2 admission, actual owner checkpoint read and response commit are verified. Memory content changes Ym at fixed epistemic state; epistemic state/access changes Ye at fixed memory. History stored/omitted/withheld changes delivery receipts while leaving both M01 outputs unchanged. The original CAN3 history comparator remains a separate positive history mechanism: stored history DEFLECT versus omitted history AMPLIFY with identical native owner state. [Factorial and comparator audit](09_FACTORIAL_AND_COMPARATOR.json); [causal interpretation/DAG](12_CAUSAL_INTERPRETATION.md).

This supports **finite constructed parallel conditioning**, with a failed adversarial restoration boundary. It does not demonstrate serial ADP016→ADP017 mediation: factorial BELIEF formation uses direct actor-facing event basis and empty memory basis, and reference attachment does not constitute a content-sensitive causal rule. It does not calibrate human psychology, autonomous person development or open-world generalization. The hand-authored event family, synthetic actor/world, intervention grants and categorical response maps are held fixed. Warranted rung is F3 for reproduced finite behavior, not F4/F5 for the intended product.

Lawful canonical claim without applied stance still yields NONE/AMPLIFY. BUFFER, DEFLECT, REROUTE, BLOCK and negative access-unknown/refusal remain executable. Naive/invalid/earlier/equal/source/outside-scope time cuts refuse, aware equivalent cuts pass, and genuinely later admitted response cuts in 1999/2000 pass. A future *unselected* native claim does not poison lawful NONE. No test demands a new future claim replace the fixed E1 claim under a rule that never grants that selection. Broader future content-sensitive revision remains outside this finite implementation's demonstrated scope.

CAN008 R2 §§5.2/14/17 require exact owner state, effective-time validity and replayable source identity; ADP017 belief_gate, active-until-exact-transition, historical receipts and snapshot-bound permission require actual provenance. The three failures violate those requirements; they do not reveal a contradiction between accepted authorities. **I3 escalation: not triggered.** CAN008 retains response jurisdiction; ADP016 retains memory; ADP017 retains epistemic state/access/permission. Real operative owner authority, serial mediation and human calibration remain HOLD.

The production EMPTY guard remains byte-identical at **e0528d65215cb431196570c38bac4eae94217a1b**, verified in actual imports and executions. All original test and law preimages remain exact. M03 effective cell blob **3eb2d02aee8dc840e7cac1f99230d7c69adc2f58**, helper blob **2434bda6f4b00e6ea5881291f5422227e8045e74**. [Test source identities](07_LITERAL_TEST_SOURCE_IDENTITIES.json), [actual imports](08_SOURCE_AND_IMPORT_AUDIT.json), [pinned source index](13_SOURCE_AND_AUTHORITY_INDEX.json).

[Reproduction](14_REPRODUCTION.md) and [sanitized environment passport](environment_passport_delta.json) describe the warm local runner, setup relocation correction, exact commands and unknown cash/quota. Commit/push/direct remote verification completes this court; it conveys neither adoption nor canonical branch authority. The final commit's own hash is reported after direct remote verification, outside its own immutable tree.
