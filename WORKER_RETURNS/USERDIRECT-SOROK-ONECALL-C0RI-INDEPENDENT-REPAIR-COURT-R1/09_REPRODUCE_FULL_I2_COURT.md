# C0RI Phase B — fully Git-contained source-free independent court

**All source and tests here are exact, previously published Git objects, never source rewritten to match test expectations.** The original frozen C0RI Phase-A SHA remains `76be43f3cd65999c93371f28d41571d04a7399fb`. C0R author SHA `98fdbdf0794da76485b40b155fa4396370a04025`; exact repaired `onecall_c0.py` is reusable here as Git blob `76bd3a6ea26fd72ef59816d62013fd694bf8e774`. The new exact I2 14-case source Git blob `ef5d5e1aa712d2b6a64714289f39c6bbf0eb19e7` was physically run against that imported module; its JUnit contains **10 PASS / 4 RED**.

From the **repaired** directory in an authenticated checkout of this C0RI reviewer branch:

```sh
cd WORKER_RETURNS/USERDIRECT-SOROK-ONECALL-C0RI-INDEPENDENT-REPAIR-COURT-R1/repro/repaired
python -B frozen/materialize_frozen_matrix.py
python - <<'PY'
import lzma,pathlib
p=pathlib.Path('test_c0ri_blind_prereg.py.xz')
pathlib.Path('test_c0ri_blind_prereg.py').write_bytes(lzma.decompress(p.read_bytes()))
PY
python -B -m pytest -q --junitxml=author32.xml test_onecall_c0_part{1,2,3,4}.py
# 31 PASS, 1 historical R08 conflict, exit 1
python -B -m pytest -q --junitxml=independent_C0F_44.xml test_phase_b_preregistered_against_c0.py test_phase_b_postfreeze_distinct_hostiles.py
# 43 PASS, R42 ORIGINAL-C0-specific SHA assertion RED, exit 1
python -B -m pytest -q --junitxml=blind_18.xml test_c0ri_blind_prereg.py
# 17 PASS, H18 ORIGINAL-C0-specific SHA assertion RED, exit 1
python -B -m pytest -q --junitxml=addendum_4.xml test_c0ri_blind_addendum.py
# 4 PASS
python -B -m pytest -q --junitxml=new_independent_I01_I14.xml test_c0ri_independent_postfreeze.py
# 10 PASS, 4 new REDs I08/I10/I13/I14, exit 1
python -B -m pytest -q --junitxml=author_translations_54.xml test_c0r_hostiles.py
# Original author reports 54 PASS; this command is supplied for independent reproduction,
# but was NOT executed as part of the present independently observed suite.
```

For historical reproduction use the original source and original test copies under the reviewer return root `onecall_c0.py` and `test_*.py`. The Phase-A test harness cannot be said to be source-free accepted actor ownership. Actual newly executed raw JUnit XML and stdout including all failing test traces are present **in the attached conversation archive**, SHA-256 `51bcd0ce0a3e5ed543e860c7eedeb3b64f8fd02340ef33dd54a1959ea99954ef`. This Git tree publishes the exact code to regenerate those files; **do not mistake the author's Git-stored 54-case XML for newly executed I2 JUnit.**

## Evidence and non-grants

Authentic author JUnit `evidence/author_54_junit.xml` is copied by exact Git blob identity from C0R's return; it is documentary author test custody, **not I2 acceptance**. Independently verified source Git SHA-1 and SHA-256 and real Python `module.__file__` are in `06_PHASE_B_INDEPENDENT_VERDICT.md` and `07_EXECUTION_RECEIPTS_AND_COLD.json`.

The R42 original-source identity expectation stays ORIGINAL_ONLY; separate I01 positively verifies exact repaired source hash. Historic R08 expects bad cosmetic-hash coupling, therefore its 31/1 repaired run is an expected **real** original-test incompatibility, not a pass.

No production, B3/CAN008/CAN011, ADP016/017, native F1 original 17 REDs, original survey bytes, actor rights, or LLM provider calls used. Four NEW independent REDs require separate bounded repair/permission gate. Reviewer does not issue self-adoption.
