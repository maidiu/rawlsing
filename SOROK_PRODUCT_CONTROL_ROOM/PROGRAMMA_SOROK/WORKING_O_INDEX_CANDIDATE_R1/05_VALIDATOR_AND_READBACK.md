> **Source correction, 2026-10-30:** The O-INDEX original source-hold claim for S0–S16 was false. All 17 original Sorok program workstream definitions are documented at owner branch `865b5b01e1a27e99020cf2bb389af8cd4c874b57`, `SOROK_PRODUCT_CONTROL_ROOM/05_PROGRAM_MAP.md`, blob `2a0a3a42d66f566f92d5c333fbbea4a5adb383b2`. Historical exploratory source existence is distinct from current adopted priorities. Earlier validator results conditioned on 0/17 are superseded; source-corrected validator requires independent reexecution.

# O-INDEX validator and readback

**Status:** WORKING CANDIDATE — NOT HQ-ADJUDICATED. The validator proves internal coverage and link honesty, not native product, science issuance or adoption.

## Files

- `validate_index.py` — sourcefree JSON/Markdown validator over the frozen source manifest. No candidate module is imported or executed.
- `verify_source_manifest.py` — S2 Git refresh verifier; resolves every `commit:path`, object type/id and commit timestamp against real Git.
- `source_manifest.json` — 167 exact source rows plus 3 reference sources, digest-bound.
- `test_validate_index.py` — 21 positive/source-object/product-mutation tests.
- `01_SOURCE_OF_TRUTH_REGISTRY.json` — 144 rows and the R6/four-asset summaries.
- `02_L0_L5_LINKED_ORCHESTRATION_INDEX.json` — 219 nodes, 461 edges, three traversals and backward paths from A0–A5 and S0–S16.
- `04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json` — 46 owner/science/source slots, including Pyat N11/N12 and six product workstream owners.

## Commands executed

```sh
python3 validate_index.py --output /tmp/oindex-r3-validation.json
python3 -m pytest -o addopts='' -q test_validate_index.py
python3 -m unittest -v test_validate_index.py
python3 verify_source_manifest.py
```

## What the validator checks

1. Exactly 144 unique Sorok rows: 19 C/A, 40 M, 12 Sorok N, 16 O, 15 E, 17 verified historic S0–S16 exploratory definitions and 4 returned assets; exact inherited id set.
2. Exactly 23 separate Pyat rows: N0–N12 with `N8E`/`N8S` and `N10E`/`N10W`, plus F1–F8; no id collision, no actor psyche.
3. Coverage strings: `19/19`, `40/40`, `12/12`, `16/16`, `15/15`; S0–S16 source-defined `17/17`.
4. Every non-hold row matches the frozen source manifest: exact commit, path, object type, object id, source kind, timestamp and required/actual consumer state. `ACTUAL` requires callable/source evidence.
5. S0–S16 must each carry exact verified `05_PROGRAM_MAP.md` historic original source, matching blob, question and output; no native/adoption promotion.
6. No row sets `native_product_accepted` or `source_science_issued` true; no `NATIVE_ISSUED` maturity.
7. Every row has typed owner/owner-type, engineering/science/authority/human grades, claim epoch and unresolved alternatives. Four returned assets are pinned, post-R7, candidate-only and unadopted.
8. R6 is 39 rows / 94 files / 0 exact-unrecoverable / 9 material families; R41 is 133 pinned files and 26 selected tests.
9. Every Sorok and Pyat ID appears in L0–L5; every L3 source function has an outgoing link; no dangling edge.
10. Backward paths resolve for A0–A5 and all 17 source-defined S0–S16 workstreams; exactly three traversals resolve; Sorok/Pyat/V3 namespace separation is explicit.
11. 46 owner slots, zero priority decisions, and explicit `S0_S16_SOURCE`, `F1CR_PATCH`, `V3_ZIP_CONTAINER`, `PYAT_NAMESPACE`, `PYAT_N11/N12`, `JOINT_TEST` and `PRIORITY` slots.
12. Six product workstreams S5/S7/S11/S13/S14/S15 have specific L0-L5 paths, source alternatives, owner slots and falsifiers; generic-governance-only substitution fails.
13. Circular index links are explicitly typed; unmarked cycles fail. Registry and orchestration remain `WORKING_CANDIDATE_NOT_HQ_ADJUDICATED`.

## Readback result

Executed result: **PASS**. 144 Sorok rows, 23 Pyat rows, 4 returned assets, 219 L0–L5 nodes, 461 edges, 3 traversals, 46 owner slots, 0 priority decisions and 66 explicitly typed containment cycles. The 21-test suite passes; source-manifest, Git-object and product-link faults fail closed. The old `WORKER_RETURNS/SOROK-PROGRAMMA-O-INDEX-R1/VALIDATION_RESULTS.json` is superseded and not cited as proof.

## What PASS means

PASS means the candidate is internally complete, every inherited identifier is accounted for, every source row matches the frozen manifest, every source function has a named consumer or explicit hold, the six S product paths are present, the four assets stay separate, and no row silently promotes native product or science.

## What PASS does not mean

- It does not prove the 102 definitions were scientifically issued.
- It does not confer current adoption of source-defined S0–S16, recover original F1CR bytes, the V3 archive identity, C9 external anchor, native B, native Pyat C11 or A5 human alpha.
- It does not adopt CP-A5-R2, C9C12-R2, B-F1CR-R2 or V3CORE-R1.
- It does not choose priority or a roadmap; those are `HQ_JUDGMENT_REQUIRED`.
- It does not execute candidate tests; their author-reported receipts remain separate, unpolled evidence.
