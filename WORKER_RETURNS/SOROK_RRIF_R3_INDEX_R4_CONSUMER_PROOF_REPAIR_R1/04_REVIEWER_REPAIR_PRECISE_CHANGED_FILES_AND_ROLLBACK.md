# R4 precise changed files and rollback

## Scope

Only `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1/**` and `WORKER_RETURNS/SOROK_RRIF_R3_INDEX_R4_CONSUMER_PROOF_REPAIR_R1/**` changed. No O-LIVE, Programma, Pyat, PREMAIN, source-owner or original R3 author file changed. No new 845-branch census and no 47 MB source transplant.

## Changed files (SHA-256 before `4f9214a` -> after)

| File | Before | After |
|---|---|---|
| `01_SOURCE_OF_TRUTH_REGISTRY.json` | `be9fcf6492c77b6fbe34260d7fac20c7e13d795a5934655f70d560bc2f083a17` | `8b54941df6b1d823b593cbd8dc0ad436062be283e58eaf45924a705bbe725504` |
| `02_L0_L5_LINKED_ORCHESTRATION_INDEX.json` | `946b978d12656e40a76d8428fbf89d4dc524cdb1f1990f7496917fd7a6c38200` | `d75dac59287444f370d02b6dddfc9e498af2400adb8b89b79f8c5b565f5041dd` |
| `source_manifest.json` | `b3d359f1bfe97a23b2c3fb356fde84c452ffe38ca874facbec7d5df086fdfa5c` | `d3f1069784717ef2b4909d3f9d3fac0e55d4df61dd42a6b784629928bc4e83e8` |
| `validate_index.py` | `54c2e60fbf050a006c77d29a3c1b243c903d5f9db60354515361e49bc5ccd225` | `2e89c6495f9a2a91d15649324a288b0d900214ab61fd3b05ef91256425df4749` |
| `verify_source_manifest.py` | `269669d01ca893100aacc6fbc4112a027102328b5b58357dcb4778391ec6e319` | `c31a89a5609e946c2af37f5987986af100d1c3cc243f3bd010c20ed7d6296afd` |
| `test_validate_index.py` | `e7621b1e38f2874c75755f5d1c9e47cb7f5ecf624ddd6ee3ebccd727df54e417` | `e89b0b30c99139780a9b2f2196454a7d695d27c600a63d5819e9aa9a5832ec52` |
| `00_START_HERE.md` | `15a87e23ecb1a5be0431d39927428fa51ade111f0b819c142593e3cce341b4b5` | `6de1c6f4a6b733735bf81e3ad1841356251801f3f6185e1e65ae89dad0556cab` |
| `03_RECOVERY_AND_FOUR_RETURN_ASSET_INDEX.md` | `9d8267e1e2f6af945e5b855d7ddbf2fce592df9d5c7ddd534e1a33575b7e2213` | `bd219257fd6f61049e3cfcf8a93d3e99adee628efe8593baa6cc7174d57edad9` |
| `05_VALIDATOR_AND_READBACK.md` | `aaf6c650ee79e0c1473036bec824ba6e34895a773ddf21a3a090272f0147f6fa` | `1604ae8b17e2dae95c26563e8bbcfc3417af74afaadf7cc0661b4141ed40211c` |
| `06_PRIMARY_SOURCE_CORRECTION_AND_HQ_ADJUDICATION.md` | `f8f9b00fb7bbb7fe2e5d34501f760f0d3bf042ea2b5fcbb54879c40faf0f8256` | `855d5c514ddcd592385a2bdd6cb0e203182d00269b75f4bd39d4ded15529b313` |

## Exact semantic edits

- `source_manifest.json`: 167 rows + 3 references retained; no source `object_id`, `commit`, `path`, `object_type` or timestamp changed (`source_object_ids_unchanged: true`). `source_kind` is derived from object type/path; `required_consumer` for C4/C9/O15/E02/E11/E12/E14 is prefixed `REQUIRED_ONLY:`; added `source_object_grade`, `source_semantic_grade`, `source_owner_anchor`, `consumer_semantic_grade`, `consumer_claim_grade`, and the consumer policy. Manifest digest changed `ec223ad4...` -> `f8dc9d60...`, reflecting metadata changes, not source substitution.
- `01_SOURCE_OF_TRUTH_REGISTRY.json`: same 144/23 rows; no IDs, native/science flags, source objects or S questions changed. Added the same claim grades and `consumer_evidence_policy`; seven prose labels prefixed; source kinds derived.
- `02_L0_L5_LINKED_ORCHESTRATION_INDEX.json`: preserved all 219 nodes and forward six product chains; added six `reverse_product_paths` (`L5->L4->L3->L1->L0`) and 24 reverse edges (`PRODUCT_REVERSE_LINK`, cycle class `PRODUCT_BACKWARD_LINK`); marked the six forward chains `PRODUCT_FORWARD_LINK`; updated source-terminal notes. Edge count 461 -> 485.
- `validate_index.py`: hard-rejects ACTUAL; checks 112/23/135/0; checks derived source kind, claim grades, source-manifest policy, seven REQUIRED_ONLY labels, specific six reverse paths/edges; previous source/manifest and forward-path checks retained.
- `verify_source_manifest.py`: retains all 167+3 Git object/type/id/time/tree checks; adds ACTUAL/evidence, 135/0 and derived-source-kind checks.
- `test_validate_index.py`: 28 tests plus 4 subtests; seven new R4 negatives (fake ACTUAL, real-unrelated ACTUAL, source_kind relabel, owner-anchor promotion, NONE-count drift, missing reverse edge, missing reverse path).
- Markdown files: 461 -> 485 and test counts updated to 28; exact ACTUAL semantics; no `L5_SOURCE_HOLD` as current S source terminal; seven labels are REQUIRED_ONLY.

## Rollback

To discard only R4 (not other branches or workers):

```sh
git checkout 4f9214a798b753092d35430f354c2a593658ce8a -- \
  SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/WORKING_O_INDEX_CANDIDATE_R1 \
  WORKER_RETURNS/SOROK_RRIF_R3_INDEX_R4_CONSUMER_PROOF_REPAIR_R1
```

Do not use `git reset --hard` or force-push. The return remains a candidate until a distinct reviewer re-executes it and a competent Sorok owner accepts a bounded static-index scope.
