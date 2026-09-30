# C1-01 R7 exact-patch source-free execution qualification

Disposition: `FAIL_SOURCE_FREE_QUALIFICATION`

Terminal: `C1_01_R7_EXECUTION_QUALIFICATION_RETURNED__HQ_ADJUDICATION_REQUIRED`

I executed the commissioned command at exact R7 head `0da3c9c13ffd91cf50ab93f6280949eb960792c0` in an isolated Python 3.12.14 virtual environment on macOS 13.7.8. The checkout was clean before and after the run. The production blob and prescribed analytical-composition test blob match the commission's exact SHA-1 values. No production or test files were changed, and no raw survey files were materialized or opened.

The final run returned exit code 1: 48 passed and 10 errors. All 10 errors arise from the shared `at07` setup in `test_pre553_analytical_composition.py:129`. The exact R7 code computes release content hash `dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`, while the frozen R3 identity fixture expects `8afa807cc06a3a10e660d13bbd831f4f758ae829e835a454c62831bfd8f4d939`. The complete unedited pytest output is retained in `04_PYTEST_OUTPUT.txt`.

An initial sparse run omitted synthetic fixture files and produced setup errors. I expanded the sparse checkout only to the five exact synthetic JSON fixtures referenced by the tests, then reran the identical command. That nonqualifying setup attempt is preserved separately in `05_INCOMPLETE_SPARSE_SETUP_ATTEMPT.txt`. The final disposition reflects the complete-fixture run.

No code or tests were modified to obtain a pass. No Candidate A/B/C, measured P2X, real-source C11, or C1-02 work was performed.
