# WIDTH512 bounded construction — capped at 600 s

**Status:** `CAPPED_WALL_600S_PARTIAL_WRITING`; **not sealed**, no contract/publication. One bounded run; no retry after the cap.

- Shape: **512 respondents x 600 populated bindings** (four times WIDTH128 respondent count)
- Tag: `PYAT-1006-WIDTH512-600-20261118`
- Writer/source snapshot: exact `68aa7cac...` (product sha `6dcb875bfdf15bd430e14b8ba406a489549a7458e717f70746494c2eff316836`)
- New unique root: `/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_WIDTH512_BOUNDED_CONSTRUCTION_20261118/.local-data-width512`; zero-byte scratch baseline
- Free space before start: ≥8 GiB; caps: 600 s child, 6 GiB RSS, 4 GiB scratch

## Stage outcome

| Stage | Result |
|---|---|
| Fixture context generation | **0.00133 s** |
| Width population | **0.12537 s** |
| Writer/publication | **capped during `writing`**; publication not reached |
| Partial estate bytes | **1,951,192,968 B** |
| Sampled peak RSS | **128,729,088 B** |
| Sampled peak scratch | **1,951,192,968 B** |
| Wall / exit | **600.250 s / -15 (SIGTERM)** |

Width audit: 304,640 extra cells; 243,712 valid substantive; 30,464 MISSING; 30,464 NOT_ASKED; 274,176 extra events; 275,839 total events; 307,200 routing facts; 512 weights; 600 bindings. No query stage was run.

Partial stage preserved at `.local-data-width512/.s2c-stage-f5vlsu4x/` with parquet files plus an interrupted writer temp/journal. The exact per-file sizes and SHA-256 values are in `PARTIAL_TREE.json`; estate bytes are intentionally not in Git.

**Conclusion:** the combined 512 x 600 construction does not complete within the 600 s child wall on this host; writer publication is the first blocking stage. Do not retry, treat the partial tree as sealed, or run a 10k x 600 attempt from this result.
