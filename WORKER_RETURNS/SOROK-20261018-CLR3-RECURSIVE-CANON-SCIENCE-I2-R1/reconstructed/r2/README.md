# High reassessment — original experiment preserved

Read `00_RETURN.md` for the revised six-assertion adjudication and `01_HQ_SPECIFICATION_ADDENDUM.md` for the user's clarified target.

From this directory run:

```sh
python3 run_reassessment.py
```

Requires Python 3.11+ and pytest, plus the adjacent R1 return subtree, included in the portable archive. It imports the byte-frozen original source. It does not rewrite R1 or run the original runner that would overwrite R1 evidence.

Expected exit **1**: unchanged suites reproduce **47 PASS / 6 RED**; new audit observations give **18 PASS**. The old six REDs have been adjudicated, not repaired or hidden. Logs/JUnit and five semantic output comparisons are in `evidence/`; test commands include working directories relative to the repository root. Session metadata confirms the rerun uses High, while the original turn used Medium. The reassessment is not independent review.
