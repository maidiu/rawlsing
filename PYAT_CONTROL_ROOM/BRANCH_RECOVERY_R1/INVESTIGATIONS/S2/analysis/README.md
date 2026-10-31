# S2 investigation builder

`analyze.py` reads the frozen roster and the completed S2 machine-index artifact, then reads Git trees/blobs/returns and builds `BRANCH_DISPOSITIONS.jsonl` and `FUNCTION_COURT.jsonl`. `finalize.py` builds `FIRST_CONSUMER_AND_SUCCESSOR_MAP.json`, `NEGATIVE_AND_UNVERIFIED.md` and `00_RETURN.md`.

The scripts were run in this investigation with:

- repository: `/Users/matthewsmith/Desktop/rawlsing_r02v_r2_canonical`
- baseline: `750548ddbb9b4392a16ce93097b856f349e16182`
- roster: `becf0bfb04705b8fe0927dd56e7290e1dcd180a8` at `PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_S2_HEAD_ONLY_ROSTER.json`
- S2 artifact: GitHub Actions run `41142495040`, artifact `13019246227`
- current PREMAIN readback: `750548ddbb9b4392a16ce93097b856f349e16182`

The scripts contain absolute paths from the run host for the repository, the downloaded S2 artifact and the extracted current `.py` tree. Adjust `REPO`, `ART` and `CURRENT` at the top of `analyze.py` before rerunning on another host. The current index was extracted from the baseline tree with `git ls-tree` + `git show`; `current_paths.txt` records the exact 375 current Python paths used.

No branch executable or branch test is run by these scripts. They parse ASTs and read return/test text only.
