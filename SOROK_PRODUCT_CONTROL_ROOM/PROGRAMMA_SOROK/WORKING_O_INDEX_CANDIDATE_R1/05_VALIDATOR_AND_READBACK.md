# O-INDEX validator and readback

**Status:** WORKING CANDIDATE — NOT HQ-ADJUDICATED. The validator proves internal coverage and link honesty, not native product, science issuance or adoption.

## Files

- `validate_index.py` — sourcefree JSON/Markdown validator. No candidate module is imported or executed.
- `test_validate_index.py` — positive candidate test and six mutation checks: dropped `S16`, missing `PYAT_N11`, native `A5` promotion, orphan `M01`, untyped cycle, and a recorded priority decision.
- `01_SOURCE_OF_TRUTH_REGISTRY.json` — 144 rows and the R6/four-asset summaries.
- `02_L0_L5_LINKED_ORCHESTRATION_INDEX.json` — 188 nodes, 414 edges, three traversals and backward paths from A0–A5 and S0–S16.
- `04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json` — 40 owner/science/source slots, including Pyat N11/N12.

## Commands executed

```sh
python3 validate_index.py --output VALIDATION_RESULTS.json
python3 -m unittest -v test_validate_index.py
```

## What the validator checks

1. Exactly 144 unique Sorok rows: 19 C/A, 40 M, 12 Sorok N, 16 O, 15 E, 17 S0–S16 holds and 4 returned assets; exact inherited id set.
2. Exactly 23 separate Pyat rows: N0–N12 with `N8E`/`N8S` and `N10E`/`N10W`, plus F1–F8; no id collision, no actor psyche.
3. Coverage strings: `19/19`, `40/40`, `12/12`, `16/16`, `15/15`; S0–S16 explicitly `0/17`.
4. Every non-hold row has an exact 40-hex source commit, source path, source time and non-empty named first consumer.
5. S0–S16 must not fabricate a source; each is `RECOVERY_EXACT_HOLD…` with consumer `UNKNOWN`.
6. No row sets `native_product_accepted` or `source_science_issued` true; no `NATIVE_ISSUED` maturity.
7. Every row has typed owner/owner-type, engineering/science/authority/human grades, claim epoch and unresolved alternatives. Four returned assets are pinned, post-R7, candidate-only and unadopted.
8. R6 is 39 rows / 94 files / 0 exact-unrecoverable / 9 material families; R41 is 133 pinned files and 26 selected tests.
9. Every Sorok and Pyat ID appears in L0–L5; every L3 source function has an outgoing link; no dangling edge.
10. Backward paths resolve for A0–A5 and all 17 S0–S16 holds; exactly three traversals resolve; Sorok/Pyat/V3 namespace separation is explicit.
11. 40 owner slots, zero priority decisions, and explicit `S0_S16_SOURCE`, `F1CR_PATCH`, `V3_ZIP_CONTAINER`, `PYAT_NAMESPACE`, `PYAT_N11/N12`, `JOINT_TEST` and `PRIORITY` slots.
12. Circular index links are explicitly typed; unmarked cycles fail. Registry and orchestration remain `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED`.

## Readback result

Executed result: **PASS**. 144 Sorok rows, 23 Pyat rows, 4 returned assets, 188 L0–L5 nodes, 414 edges, 3 traversals, 40 owner slots, 0 priority decisions and 60 explicitly typed containment cycles. The seven-test suite passes; six mutations fail closed. Machine output is preserved in `WORKER_RETURNS/SOROK-PROGRAMMA-O-INDEX-R1/VALIDATION_RESULTS.json`.

## What PASS means

PASS means the candidate is internally complete, every inherited identifier is accounted for, every source function has a named consumer or an explicit hold, the four assets stay separate, and no row silently promotes native product or science.

## What PASS does not mean

- It does not prove the 102 definitions were scientifically issued.
- It does not close S0–S16, original F1CR bytes, the V3 archive identity, C9 external anchor, native B, native Pyat C11 or A5 human alpha.
- It does not adopt CP-A5-R2, C9C12-R2, B-F1CR-R2 or V3CORE-R1.
- It does not choose priority or a roadmap; those are `HQ_JUDGMENT_REQUIRED`.
- It does not execute candidate tests; their author-reported receipts remain separate, unpolled evidence.
