# PYAT S3 — negative, unverified and exact NOT_RUN inventory

## Method boundary

This investigation is a static Git-plumbing and Python-AST audit of the frozen S3 roster. It did **not** execute any branch tip, test file, production module, survey response or native source. The S0 path/blob index and the S1–S5 function/AST index were read as immutable GitHub Actions artifacts; their source-count claims are not independent test passes.

## Exact negatives

1. **Count mismatch would be incomplete.** The frozen roster has 174 names, 174 distinct tips and 24 unclassified names. This return has exactly 174 branch rows. The 24 unclassified names are preserved with `unclassified_roster_kind` and are not silently promoted to a Pyat disposition:
   - `agent/reviewer-r3-hq297-k9k10-sc0-pe-executable-court-r1`
   - `agent/v3court-review-rc-actual-consumer-r1`
   - `agent/v3court-review-rs-scientific-differential-r1`
   - `agent/v3court-review-rt04-secondwave-r1`
   - `agent/v3court-review-rx01-baseline-source-r1`
   - `agent/v3court-review-rx02-pressure-source-r1`
   - `agent/v3court-review-rx03-secondwave-r1`
   - `agent/v3court-review-rx04-secondwave-r1`
   - `agent/v3court-review-rx05-secondwave-r1`
   - `agent/v3court-t01-needs-care-power-life-r1`
   - `agent/v3court-t02-baselines-impressions-threat-r1`
   - `agent/v3court-t03-interpressure-development-r1`
   - `agent/v3court-t04-memory-ideology-recursion-r1`
   - `agent/v3court-t05-current-consumer-causality-r1`
   - `agent/v3court-x01-expectations-child-model-r1`
   - `agent/v3court-x02-pressure-flow-interpressure-r1`
   - `agent/v3court-x03-development-topology-r1`
   - `agent/v3court-x04-scheduler-llm-event-r1`
   - `agent/v3court-x05-material-actor-world-bridge-r1`
   - `codex/b2-indexed-event-custody`
   - `codex/b2-legacy-reentry-repair`
   - `codex/c12-perception-fork-repair-r1`
   - `maintenance/proof-integrity-r1-ci-smoke`
   - `proposal/cross-hq-stranded-branch-reconciliation-20261028-r1`
2. **168 of 174 branches have no production/test code path** in the S0 index. They are review, dispatch, intake, fan-in, candidate, proposal, control or historical branches. They are not treated as hidden implementations.
3. **111 branches have no branch-specific return/disposition document** in the index. They are `EVIDENCE_UNKNOWN`, not PASS. The 63 documented branches have exact return paths and verdict excerpts in `BRANCH_DISPOSITIONS.jsonl`.
4. **Only one source/test pair is exact current PRE-MAIN code:** `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` blob `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` and `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py` blob `2161c0fff86ecb7a2c9a40b29852075e802841fd`. The current file was not re-executed here.
5. **Four source candidates have no current path and no current consumer:** `pre553_selected_world_progressive_contract.py` (`e9caea543…`), `r3_s02_seam_witness.py` (`b1ec1814…`), `pre553_postastra_pe_generic_world_possibility.py` (`58484f4c…`) and `pre553_original_identity_v2k_successor_candidate.py` (`e3ef9a24…`). The S3 reviewer branches carry them; they are not authored/owned by this worker.
6. **PE generic complete-contract invalidity.** The independent HQ297 record says role-reversal issuer scope is unqualified and full SC0 K9 8/K10 28 are NOT_REACHED. The `serve_generic_world_situated_possibility` / `verify_generic_world_situated_replay` pair is classified `INVALID` as a complete contract; `_auth` is `TRASH_WITH_GROUNDS` because it shape-checks a non-null role-reversal ref without dereferencing competent reversed target/risk/denominator scope. Useful schema/arithmetic remains only after repair.
7. **V2K semantic adoption withheld.** The independent PV/V2K court reports bounded sourcefree links and replay, but foreign issuer refs and coherent removed-held-row selection can pass the candidate; original U/E/source authority and semantic correspondence remain unqualified. The identity machinery is `UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY`, not a ready production schema.
8. **Selected-world/seam/PE/V2K author tests are not independent replays.** The reported 24/18/21/24/111 counts come from author/reviewer returns. This investigation did not run them.
9. **HQ273 C01 is test-only evidence.** Its 19-test court demonstrates two conditioned facts on a sourcefree fixture through the current I03 executor; it is not a production consumer or native source result.
10. **HQ280 B2 is unexecuted and G0b-held.** The 8-case EE14 selected-lifecycle test candidate is not evidence of an installed current/as-of service or source-qualified C1-to-M2 producer.
11. **No source/production authority.** No original GT2/Afrobarometer/LiTS U/E, source-use permission, model-use issuer, N9 operative current, N10W joint model, FF/N9-N12 proof, actor/person, production consumer, PRE-MAIN integration or merge is established.
12. **No branch executable was run.** This is deliberate: the commission forbids arbitrary branch execution and original survey/response execution.

## Exact TESTS_NOT_RUN

These are the commands that would be needed for an independent replay. They were **not executed**. A later qualified reviewer must use an isolated checkout, verify the tip, and report actual exit codes; author reports are not substitutes.

```sh
# selected-world contract (tip ed34944e..., source e9caea543...)
git worktree add --detach /tmp/s3-selected ed34944e253b78714a28d72b8ca2a6521ce15930
cd /tmp/s3-selected
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py -q
# NOT_RUN

# seam witness (same tip, source b1ec1814...)
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_r3_s02_seam_witness.py -q
# NOT_RUN

# PE generic (tips e61a26ce... and f515188e...)
git worktree add --detach /tmp/s3-pe e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65
cd /tmp/s3-pe
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py -q
# NOT_RUN
# plus the 13 independent HQ297 tests and full K9 8/K10 28; NOT_REACHED in the author/reviewer record

# V2K successor (tip 694fb450...)
git worktree add --detach /tmp/s3-v2k 694fb45085cd5e4891949921a44edb77c3f603f2
cd /tmp/s3-v2k
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py   rawlsing_next/tests/test_hq294_a04b_actual_scope_variants.py   rawlsing_next/tests/test_hq294_a04b_identity_court.py   rawlsing_next/tests/test_postastra_pv_v2k_independent.py -q
# NOT_RUN

# HQ273 C01 (tip 2406a4d7...)
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_hq273_c01_true_i03_conditioned_denominators.py -q
# NOT_RUN

# HQ280 B2 EE14 (tip a159bff6...)
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_pre553_ee14_selected_lifecycle_source_free_integration.py -q
# NOT_RUN__UNEXECUTED_CANDIDATE__G0B_HELD

# current exact progressive file (PRE-MAIN 750548dd...)
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -m pytest   rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q
# NOT_RUN__ALREADY_CURRENT
```

## Exact unverified points

- The 24 unclassified names need an owner/name triage; no name-based inference was used.
- `current_symbol_name_matches` in `FUNCTION_COURT.jsonl` is a name match only. It is not equality proof. No function was marked `INDEPENDENTLY_REBUILT_EQUIVALENT` or `SUPERSEDED_BETTER` without an exact current blob or an independently proven behavioral comparison.
- No function is marked `UNIQUE_USEFUL_READY`: none of the four missing source candidates has a current consumer, independent test replay or owner adoption. `UNIQUE_USEFUL_NEEDS_ADAPTATION`/`HELD` are the strongest labels used for missing code.
- The four missing source candidates have no current consumer. Their author tests are not a current consumer.
- The PE complete contract is invalid on the independent record; the V2K schema is held by source/semantic authority.
- The selected-world/seam code is useful adaptation material, not a current equivalent.
- Historical `UNKNOWN` values are preserved. No oldMac/mainMac, provider URL, source issuer or model-effort claim is invented.
- PRE-MAIN may move; this comparison is frozen at `750548ddbb9b4392a16ce93097b856f349e16182` and was rechecked at build time.

## What would change a disposition

A source-owner-issued grant, a current path/consumer, an independent test replay with actual exit codes, a semantically reviewed successor mapping, or a new PRE-MAIN head could change a row. A branch name, age, blob name or author report alone cannot.
