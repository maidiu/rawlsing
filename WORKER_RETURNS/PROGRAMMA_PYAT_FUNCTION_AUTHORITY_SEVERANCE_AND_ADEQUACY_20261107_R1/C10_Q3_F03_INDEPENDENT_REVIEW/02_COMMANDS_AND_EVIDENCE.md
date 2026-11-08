# C10 Q3 F03 independent review — commands and evidence

## Environment

```
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-c6-historical-independent-review
git status --short --branch
git rev-parse HEAD
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer rev-parse HEAD
```

- Review branch: `agent/pyat777-c6-historical-independent-review-20261107-r1`.
- Review base: prior C6 review `333ade4e4c003595630d7f53eaeece85902d6759`.
- C10 target: `fdda847507936f5e2cd32cf8c57326f0f65200d6`; author cut inside the C10 return: `0d548b033a0a20c9738fa4a3412ba5acd01217c5`.
- Historical cut: `9ba4764bef551b1ce498e5772d60b73d69337d4b`.
- Write lease used: `WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C10_Q3_F03_INDEPENDENT_REVIEW/` only.

## Exact pin checks

```
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 9ba4764:data/ddm_build_copy/ddm_v550_question_relation_authority.py | shasum -a 256
# 2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c
# 38,858 bytes

git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 9ba4764:data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv | shasum -a 256
# 0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13
# 47,874,248 bytes

git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer \
  show 9ba4764:data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv | shasum -a 256
# a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b
# 1,119,028 bytes / 700 data rows
```

The same three files are present at the C10 author cut `0d548b0` with identical SHA-256 values. The historical module `ROOT` is `Path(__file__).resolve().parents[2]`; placing the exact module at `tmp/replay_root/data/ddm_build_copy/ddm_v550_question_relation_authority.py` makes `ROOT` resolve to the disposable replay root without monkeypatching a reader or constant.

## Independent focused verifier

```
python3 WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C10_Q3_F03_INDEPENDENT_REVIEW/scripts/verify_c10.py \
  > WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C10_Q3_F03_INDEPENDENT_REVIEW/logs/verify_c10.json
```

The verifier materializes the exact pinned module/authority/registry bytes in this review lease's `tmp/`, imports the historical module, and calls the actual public entrypoints. It does not use the author's replay output as proof and does not read respondents, SAV/DTA/DB or source microdata.

### Reproduced results

- 18,518 audit rows.
- Resolver statuses: 12,611 context-only; 4,622 directional; 952 administrative; 60 explicit block; 259 Asian W6 excluded; 14 ambiguous.
- Relation statuses: 12,611 governed context-only; 4,622 governed directional; 952 administrative; 273 blank; 41 structural-mapping block; 10 source-authority block; 9 identity/authority-join block. Both status totals sum to 18,518.
- 35 active source/wave scopes; 36 pairs before W6 exclusion; W6 259 rows; active 18,259 rows.
- 18,245 directional-coordinate-complete rows; 4,673 current-directional-atom-eligible rows.
- Full audit digest: `e18b9a8eba70dc5debc6d6f9387d844f456299b8bb880559151e7ad29f82daf6`.
- Nine positive family rows reproduce the C10 selected rows and output hashes exactly:
  - Afrobarometer `c511a6e8...`
  - Arab Barometer `087e07b0...`
  - Asian Barometer `d4224d2b...`
  - EVS `af254911...`
  - GSS `a16c8e48...`
  - Latinobarómetro `0f146ae9...`
  - LiTS `6ee8e60c...`
  - South Asia `609f60f7...`
  - WVS `9e01969f...`
- Explicit block: `RESOLVED_EXPLICIT_BLOCK`, semantic role `UNKNOWN`, coordinates cleared, `cee3ab67...`.
- Ambiguous LiTS III DURATION1: `BLOCKED_AMBIGUOUS_AUTHORITY`, semantic role `UNKNOWN`, `80736f70...`.
- Suffix-derived missing row: `BLOCKED_MISSING_AUTHORITY`, semantic role `UNKNOWN`, coordinates cleared, `13c9dbe3...`; negative fixture only.
- 700-row limited registry supplied for the full AR-0005 row: `BLOCKED_MISSING_AUTHORITY`, no directional promotion, `40d0b122...`.
- Missing authority file: `FileNotFoundError`.
- Cold restore from identical module/authority bytes: `c511a6e8...`, matching the first positive.
- AR-0006 residual: 20 Latinobarómetro 1995 rows, CSV `634d4a3e...`, registry 700 rows; narrow residual scope, not an all35 witness substitute.
- Replay script scan: no `setattr`/`unittest.mock`/`MagicMock`; the only "monkeypatch" token is a comment at `scripts/replay_f03.py:377`. The script imports no V550 bridge or V551 relation-evidence atoms; those remain `NOT_RUN`.

## Q4 current pins

All current Q4 hashes were verified from `0d548b0`:

- `rawlsing_next/pre553_source_backed_c11_facade.py` — `7788feb5...`
- `rawlsing_next/pre553_empirical_query.py` — `7cd7fd4f...`
- `rawlsing_next/pre553_empirical_authority.py` — `c32b96cd...`
- `rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py` — `a88d623f...`
- `rawlsing_next/pre553_historical_authority.py` — absent at `0d548b0`.

The bounded WVS7 materializer contains `FQRA_SHA256 = 0f7fa1c...`, `QRA35V1::WVS::W7::B_COUNTRY`, `FROZEN_P2_ROUTING_ONLY` and `substantive_evidence_use=false`; it is routing-only, not a full substantive F03 adapter. The C6 candidate filename absence is not a Q4 functional-responsibility finding.

## Author evidence hashes

- `00_RETURN.md` `21fa39e0...`
- `TRACE.jsonl` `53c2b4ed0ae775682f4ae7b7cd477868d6dc9dadd4d70bf802ce45670cb97184` (matches the declared trace hash)
- `logs/replay_results.json` `e7df00d7...`
- `logs/replay_stdout.txt` `ca9f03a4...`
- `scripts/replay_f03.py` `9834eb12...`

## Review output hashes

```
shasum -a 256 REVIEW.json 00_RETURN.md scripts/verify_c10.py logs/verify_c10.json logs/read_counts_and_hashes.txt
# e1fe8a4ffa0d01e7531290ef5bcd227b60639c55b7d66dc28e6068eb8a682179  REVIEW.json
# 5b4668ac4e607a9b3a5bae96dd8d2f2bb1ea13c2014d78e6c91964c952130caf  00_RETURN.md
# c83d4452fd579108d4007e07cc057f517ae8f9844018a7b2d33bc426646d3cb3  scripts/verify_c10.py
# 4a4028861d962637a11ad813b80432407b6252009b7f6a04076095ed6c11415b  logs/verify_c10.json
# acc24c0fbe21f44171fc41d347710638e13515cb755a1175ad5f1e78c670088d  logs/read_counts_and_hashes.txt
```

## Prohibited-action check

- No respondent, SAV/DTA/DB, source microdata, S3/native/science/actor execution or effect.
- No production, existing-test, HQ, peer or protected write.
- No environment install, CI/merge, new worker or engine build; this review reused the existing C6 reviewer/session/model.
- No broad archaeology or recensus; only the C10 target and retained current Q4 pins were inspected.
- Only the `C10_Q3_F03_INDEPENDENT_REVIEW` lease was written.
- The independent verifier's `tmp/` copies are disposable and are not part of the committed evidence.

## Limits

Test-time historical replay only; original historical invocation/run manifest remains `NOT_OBSERVED`. Nine positive rows are a source-family sample, not a full 35-wave positive matrix. Downstream V550 bridge/V551 atoms remain `NOT_RUN`. Current full-F03 selection/equivalence remains `UNPROVED_CURRENT_SELECTION`; the bounded WVS7 pin is routing-only.
