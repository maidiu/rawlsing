# C0RI Phase A frozen independent test court — before any C0R implementation read

**Blind sealed startup:** `b48837d84d01077091386dfa14c1eedae9955ad5`. The original C0 source and both original C0F independent test suites are physically staged with their **exact historical Git blob identities**. C0R's sealed commission only (blob `2889c9beb578d98373dff4625bd5aac87fab509d`) was read before this freeze; not its implementation or return.

## Physical real Python tests against original C0

- Original author's **32/32 PASS**, `original_author_junit.xml` SHA256 `2124a5e4a0fcd629a67e66498246778d6648801e8d61effeda0a6406530c4471`.
- Unchanged historical C0F suites: **44 tests, 26 PASS / 18 RED**, `original_18_junit.xml` SHA256 `c8cf6a8b5eb399383a511c6d69fd76dd896d4e3946611b0cc60657ddd81aaab5`. The 18 exact test IDs are A02, A07, A11, A13, A16, A17, A18, A23, A26, A27, R32–R39.
- New, preregistered independent C0RI Phase A tests: **18 executed / 6 PASS / 12 RED** against the original, `blind_new_original_junit.xml` SHA256 `69d177e0f0e437eaf412b6a892feaf192bf51e043e6bb70945a4a06b608c469d`. New source `test_c0ri_blind_prereg.py`, 7,692 bytes, Git blob `82566deb6a378e75253166937e483ff40e1a1967`, SHA256 `5956dd846e6112dfcaa7a9045484c210b72c950886f89ea223e6da9e0f2b8531`. The exact frozen source is in compressed Git transport `test_c0ri_blind_prereg.py.xz` (Git blob `94ca0f978dad9576a9f7ded1b88f15914b8b1ccc`). Decompress only; **do not edit the frozen tests**.

## New pre-C0R independent hostiles (H01–H18)

H01 source substitution between validation and append; H02 historical duplicate ID with replaced contents; H03 unconstructed counterpart vs existing peer availability; H04 forged external issuer; H05 falsely asserted provider/scientific provenance; H06 label-only invariance of exact causal-history hashes; H07 admitted same-year parent then child prerequisite; H08 refused same-year parent must not admit child; H09 Python `-O` must not erase source authorization; H10 midyear partial prestate must not backdate old event; H11 empty rule registry must authorize no events; H12 missing per-event source permission; H13 unconstructed teacher; H14 render-private-memory forgery; H15 genuine valid-empty; H16 no unauthorized individual behavior score; H17 onecall render-only nonmutation; H18 frozen ORIGINAL source identity test **ORIGINAL_ONLY**.

**Scientific grading caveat:** A16/A23 may be closed by a **typed, explicit fail-closed UNSUPPORTED result**; refusing unsupported subannual/midyear capability is not an implementation of a time-sensitive scheduler. H18/R42 must remain ORIGINAL_ONLY, while a repaired module gets independent new SHA checks. Missing psychological or CAN/ADP grants remain HOLD even if every sourcefree test becomes green.

## Runnable reproduction from the sourcefree court directory

```sh
python -c "import lzma,pathlib; p=pathlib.Path('test_c0ri_blind_prereg.py.xz'); pathlib.Path('test_c0ri_blind_prereg.py').write_bytes(lzma.decompress(p.read_bytes()))"
python -m pytest -q --junitxml=original_author_junit.xml test_onecall_c0_part{1,2,3,4}.py
python -m pytest -q --junitxml=original_18_junit.xml test_phase_b_preregistered_against_c0.py test_phase_b_postfreeze_distinct_hostiles.py
python -m pytest -q --junitxml=blind_new_original_junit.xml test_c0ri_blind_prereg.py
```

No real model, actor, original source or psychological rule was used. The original expected failure statuses are not converted into an implementation or used as a candidate-specific generated lookup.
