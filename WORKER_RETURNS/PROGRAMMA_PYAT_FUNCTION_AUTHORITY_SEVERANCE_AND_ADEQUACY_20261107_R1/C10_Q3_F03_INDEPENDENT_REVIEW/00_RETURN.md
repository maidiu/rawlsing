# C10 Q3 F03 independent review

**Verdict:** `REVISE_SCOPED`

**Review target:** C10 `fdda847507936f5e2cd32cf8c57326f0f65200d6`, author cut `0d548b033a0a20c9738fa4a3412ba5acd01217c5`
**Historical cut:** `9ba4764bef551b1ce498e5772d60b73d69337d4b`
**Reviewer:** existing C6 independent nonauthor, same OpenCode Go DeepSeek V4.1 Flash MAX; distinct from the C10 author.
**Review lease:** `C10_Q3_F03_INDEPENDENT_REVIEW/` only, on `agent/pyat777-c6-historical-independent-review-20261107-r1`.

## What is accepted

The Q3 historical replay is independently reproduced exactly, using the pinned historical module and authority bytes in a disposable review root and the actual public entrypoints. I did not use the author's replay output as proof; I re-ran the focused checks over the exact bytes.

| Check | Independent result |
|---|---|
| Historical module | `2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c`, 38,858 bytes |
| AR-0005 full authority | `0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13`, 47,874,248 bytes, 18,518 rows |
| AR-0006 registry | `a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b`, 1,119,028 bytes, 700 rows |
| Entrypoints | `apply_question_relation_authority:727`, `load_question_relation_authority:564`, `active_closed_35_waves:570`, `resolve_question_relation_authority:584`, `validate_active_universe:861`, `derive_legacy_latinobarometro_1995_residual:441` |
| Full audit | 18,518 rows; 12,611 context-only, 4,622 directional, 952 administrative, 60 explicit block, 259 Asian W6, 14 ambiguous; relation statuses sum to 18,518 |
| Scope | 35 active source/wave scopes; 36 pairs before W6 exclusion; W6 rows 259; active rows 18,259 |
| Nine positive families | Same selected rows and output hashes as C10; all six structural coordinates present |
| Negatives | Explicit block `cee3ab67...`; ambiguous `80736f70...`; suffix-derived missing row `13c9dbe3...`; 700-row limited registry `40d0b122...`; missing file `FileNotFoundError` |
| Cold restore | Reproduces `c511a6e8...` from identical module/authority bytes |
| AR-0006 residual | 20 Latinobarómetro 1995 rows; CSV `634d4a3e...`; registry 700 rows; narrow residual scope |
| Script integrity | Exact module loaded by path; no `setattr`/mock/MagicMock; only a comment mentions "monkeypatch"; no manufactured authority |
| Execution scope | Test-time replay only; original historical invocation `NOT_OBSERVED`; downstream V550 bridge/V551 atoms `NOT_RUN`; current acceptance not promoted |
| Q4 bounded pin | WVS7 materializer `a88d623f...` pins FQRA `0f7fa1c...` at `QRA35V1::WVS::W7::B_COUNTRY`, `FROZEN_P2_ROUTING_ONLY`, `substantive_evidence_use=false`; routing-only, not a full substantive adapter |

The nine positive rows are a one-row-per-source-family sample, not a substitute for all 35 positive wave traces; the author states this correctly. The AR-0006 residual is distinct from the full AR-0005 authority. The absent C6 candidate filename is not evidence of current absence by function.

## Required corrections

**C10R-01 — severance wording (reporting).** The 00 verdict token `NO_SEVERANCE` and the phrase "No severance is claimed" can be read as affirmative non-severance. The replay proves only that the unchanged historical consumer works on exact present bytes; it does not prove that the current consumer selects or enforces those bytes. Current F03 remains `UNPROVED_CURRENT_SELECTION`. Replace the token with `NO_POSITIVE_SEVERANCE_FINDING__CURRENT_SELECTION_UNPROVED` (or the trace's `NOT_PROVED__NO_GOVERNING_INPUT_LOSS_DEMONSTRATED`) and state explicitly that absence of a severance finding is not evidence of non-severance.

**C10R-02 — Q4 functional-responsibility mapping (scoped revise).** The Q4 section maps generic current consumers, one bounded routing-only WVS7 pin, and an absent C6 candidate filename. That is a bounded location map, not the required full F03 owner/equivalent walk across the whole PRE-V3/existing authority producer/carrier/FF/post-FF. The absent C6 filename is not a Q4 basis. Complete the functional-responsibility map using existing records and existing owners; preserve `F03=UNPROVED_CURRENT_SELECTION` until a current selected consumer/adapter is demonstrated. Do not install the C6 candidate merely because the filename is absent.

**C10R-03 — production-read claim (reporting).** The 00 says no production module was read. The replay script reads the current Q4 files (`rawlsing_next/pre553_source_backed_c11_facade.py`, `pre553_empirical_query.py`, `pre553_empirical_authority.py`, `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py`) to compute their SHA-256 at `scripts/replay_f03.py:473-486`; it does not execute them. Correct this to: "no production module was executed; current Q4 files were read-only hashed for pin identification."

## Limits

- Test-time replay only; original historical invocation/run manifest remains `NOT_OBSERVED`.
- Nine positive family rows, not a full 35-wave positive matrix.
- Downstream V550 bridge and V551 relation-evidence atoms remain `NOT_RUN`.
- No respondent, SAV/DTA/DB, source microdata, S3/native/science/actor execution or effect.
- No current full-F03 selection/equivalence; current adoption remains `UNPROVED_CURRENT_SELECTION`.
- The bounded WVS7 FQRA pin is routing-only, not a full substantive F03 adapter.

## Minimum existing owner action

1. Correct the C10 00 verdict/wording per C10R-01 and C10R-03; this is reporting only, no production/data repair.
2. Complete the F03 Q4 current owner/equivalent functional-responsibility walk across the whole PRE-V3, existing authority producer/carrier, FF and post-FF, using existing records; no new engine, production install or original execution.
3. Preserve the distinction between "no positive severance finding" and "proven non-severance"; keep `F03=UNPROVED_CURRENT_SELECTION` until a current selected consumer/adapter is demonstrated.

## Evidence

- `REVIEW.json` — structured verdict, checks, corrections, limits.
- `scripts/verify_c10.py` — independent focused verifier over the exact pinned bytes.
- `logs/verify_c10.json` — full independent results.
- Author evidence: C10 `TRACE.jsonl` SHA-256 `53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184` (matches the author's declared trace hash); `logs/replay_results.json` schema `C10_Q3_F03_REPLAY_RESULTS_V1`.
