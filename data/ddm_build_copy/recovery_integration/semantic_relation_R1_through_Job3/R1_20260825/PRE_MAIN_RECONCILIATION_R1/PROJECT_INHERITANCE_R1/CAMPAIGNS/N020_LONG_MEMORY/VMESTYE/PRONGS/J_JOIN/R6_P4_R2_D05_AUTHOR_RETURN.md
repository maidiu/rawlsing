# VMESTYE ZL-15 — R6 targeted canonical status correction after P4 R2 REVISE

**Author candidate, not independent acceptance.** R5 reviewed SHA `cc21762ac3c7b49e389835b669a578d48caa1fc4`; P4 reviewer R2 [issue #817](https://github.com/maidiu/rawlsing/issues/817#issuecomment-6752199337), independent review branch HEAD `a97a3dcb0366d642827a453826d3952792d252f2`; protected PRE-MAIN base `256d46bf425cc37e114465cddbe3c60e535766ab`. New R6 HEAD obtained from PR #864 after commit.

## R2-D05: canonical enum corrected, historical history conserved

Exactly **73** `DATA/FUNCTION_ATLAS.tsv` cells changed from R5 to R6, and they are all the `disposition` cells belonging to 44 LMX and 29 C6-F inherited source identities. Every now has canonical `OPEN_PROOF_GAP`, one of the exact ten dispositions in protected `04_EVIDENCE_AND_STATUS_LAW.md`. No other canonical atlas field or row changed, and **all 1,667 nonseed rows remain byte-for-byte identical**.

The existing `SEED_CURRENT_DISPOSITIONS_R5.tsv` retains the six earlier composite historical/source-qualification labels (30+8+5+1+9+20) in its descriptive `current_disposition` column. This sidecar column is **not** a second canonical status authority. It preserves what the older evidence reported, while `FUNCTION_ATLAS.disposition=OPEN_PROOF_GAP` is the legal present comparative status at the reviewed cut. Exact historical source locators, evidence/candidate joins, individual owner routes, original unreceived status, finite action and falsifier, and all negative limitations remain unchanged.

**Strict validator:** `VALIDATE_ZL15_R6.js` inherits R5 relation, stage, source and seed evidence checks; pins R4 source blobs and the exact R5 prior atlas blob `b6d9ecd62a1080eb9a27e91581a129facec626d3`; compares all 1,740 atlas rows, allows only the 73 disposition-cell replacements, demands exact `OPEN_PROOF_GAP` and membership in the ten protected statuses, and rejects alternative invented `__OPEN` variants, inappropriate legal-but-unproved `PARTIAL_SUCCESSION` and false `PROVED_CURRENT_SUCCESSOR`. It checks the 73 historical descriptive values against their unchanged R5 classifications. Author S0–S1 in-memory verification: **17/17 hostile modifications detected**, no project CI/host-native S2/S3 run, no independent P4 approval.

## An additional inherited vocabulary observation — *not silently remediated*

A whole-atlas status vocabulary scan at R5 uncovered **655 existing nonseed rows** with descriptive/noncanonical `disposition` labels (156 distinct strings). They were not among the 73 seed changes called out by the P4 R2 reviewer. Rewriting these rows requires a distinct source-preserving, owner-reviewed normalization; the bounded R6 D05 fix **does not mutate or claim to resolve them**. `INHERITED_NONCANONICAL_DISPOSITIONS_R6.tsv` enumerates every such row with exact ID, source locator, R5 literal, identical R6 literal and `R5_INHERITED_OUT_OF_VOCAB__R6_NOT_MODIFIED__SEPARATE_REVIEW_REQUIRED`. The validator checks exact 655-row audit completeness and rejects any loss/forgery. This is not a claim of *global* canonical vocabulary compliance: 73 repaired seed rows comply; the older 655 nonseed exceptions remain a transparent separate review question.

## P4-D01 accepted at R5 unchanged

All 8,503 normalized relation records are byte-for-byte unchanged from R5, with 4,841 reversible mappings, 7 ASTRA MUST and 26 IF branches, full original 82 seams, and all negative/candidate grades preserved. The R5 `RELATION_TYPE_MIGRATION_R5.tsv` and `RELATION_TYPE_NORMALIZATION_R5.md` are untouched.

## Still held

Actual non-test readers **332 open**, applied/refusal affirmative **0/370**, reciprocal Pyat owner decision events **884 NOT_RECEIVED**, 90 stage evidence holes, 49 different-cut GAP aliases, 48 Sorok historical source bodies, bounded 3,449 branch-name countersearch, D05 F06/F11, FIABC historical 144 PASS/3 FAIL, native original35, source/scientific/actor authority, consent, selection and a current-machine zero-loss claim. No frozen source changes, no new lost-function count, no protected write, no acceptance or merge.

**Route:** send the new author HEAD for independent P4 recheck of 73 canonical seed statuses; ask the reviewer to explicitly adjudicate whether the 655 inherited nonseed vocabulary exceptions create a further publication-blocking schema obligation. R4/R5 independent evidence continues to stand at its own exact cut; R6 is not auto-accepted.