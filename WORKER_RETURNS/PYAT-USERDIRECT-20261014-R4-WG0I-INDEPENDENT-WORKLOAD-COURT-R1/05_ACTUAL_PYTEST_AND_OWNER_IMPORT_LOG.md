# WG0I — actual host, exact Python import, original JUnit and acceptance log

**Real independent execution, not a copied WG0P author result.**

- Sealed startup GitHub branch `bd91d30efb35c9ad39b45ae81a065e7e1a479b27` verified before beginning.
- WG0P candidate pinned `e19099460eed10a4d3da31a917af539aef87e485`, original file `repro/wg0p_executable_workload.py`; directly fetched **12,325 bytes**, actual reconstructed `git hash-object` **`c88182bed5c521a05a462778b76ffd40cf87a248`**, actual binary SHA-256 `d8cff0c8b46a4c13a96392993a84b704f883bab67531432269b1d598e4f8fa8d`.
- Independent WG0I exact executed test file `repro/test_wg0i_hostiles.py`, **8,658 bytes**, verified local Git SHA-1 `ed41a46c9300dcad2b8128020368b744f3093807` equal to pushed GitHub blob. Its own SHA-256 `b048edad89277f8ad7345e406eb115ec16aaff1ed2a8fd96aa7c0ef0929fae5e`.
- Python 3.13.5; pytest 9.0.2; git 2.47.3; `__file__=/mnt/data/wg0i_court/wg0p_executable_workload.py`.
- Real host command `python -m py_compile wg0p_executable_workload.py test_wg0i_hostiles.py` → exit **0**.
- Real host command (from `/mnt/data/wg0i_court`):
  ```sh
  python -m pytest -q test_wg0i_hostiles.py --junitxml=wg0i_hostiles.junit.xml > wg0i_hostiles.stdout 2> wg0i_hostiles.stderr
  ```
  Exit **1**, summary:
  ```text
  .....FFFFFFFFFFFFFFF                                                     [100%]
  15 failed, 5 passed in 0.17s
  ```
- Real original JUnit generated: `/mnt/data/wg0i_court/wg0i_hostiles.junit.xml`, **15,203 bytes**, SHA-256 `0d4f0fe5b53e1fef98545df1ab557e6b04c08b1dbc5004e31b8cfd54abda2b79`. JUnit XML metadata `tests=20; failures=15; errors=0; skipped=0; time=0.166`. The XML bytes were **not** pushed to GitHub; this report preserves the actual local artifact, digest and exact command to reproduce.
- Stdout real file `wg0i_hostiles.stdout`, **14,597 bytes**, SHA-256 `1b1dc9dc62e077ae63d0d336204bd1155ac03eb04b090c2d8267f0c127856406`; stderr real **zero bytes**. The full failure names and observed defects are copied into `02_INDEPENDENT_HOSTILES_AND_ACTUAL_BATCH_RUN.json`, not made-up tracebacks.
- Git CLI private checkout `git ls-remote https://github.com/maidiu/rawlsing.git HEAD` failed, **Could not resolve host github.com**. Authenticated GitHub connector did fetch exact accepted owner source texts; it did not materialize the entire source/dependency closure in this Python host.
- **CRITICAL limitation:** the test file openly injects `rawlsing_next` **unqualified test doubles** (including a `BatchExecutionRunner` that refuses to construct) before importing the exact WG0P candidate, exercising *only the exact candidate's source-free methods*, not accepted batch owner imports or the original 14 WG0P tests. Never describe the JUnit as BatchExecutionRunner acceptance or I03/I05 execution.
- The independently frozen expectation file `04_PRE_RUN_INDEPENDENT_EXPECTATIONS.json` was committed at `6951ff523bda9ecf1eeb3ef6aacd4cb1b67c4f36` **before the local hostile court was run**.

## Original versus independent test boundary

| Suite | Source custody | Executed here? | Result |
|---|---|---|---|
| WG0P author 14 tests `2fb25148343e46a923acd88c6f6203b89489124f` | Fetched/read from GitHub, 6,993 bytes | **NO**, complete accepted PRE553 closure unavailable | Author **reports** 14/14; WG0I **HOLD** verification |
| WG0I independent 20 tests `ed41a46c9300dcad2b8128020368b744f3093807` | Independently written/pushed, exact local SHA matched | **YES**, against exact WG0P source under conspicuous stubs | **5 PASS / 15 acceptance REDs** |
| Accepted `BatchExecutionRunner` `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | Source inspected exact, not importable in current host | **NO** | **NOT_EXECUTED**, no owner defect asserted |
| Accepted I03 / I05 | Exact public owner code inspected | **NO** | **NOT_EXECUTED**, no original empirical values computed |

**Recommendation:** a qualified next execution host must stage exact transitive accepted imports, assert each `module.__file__` and `git hash-object`, and rerun the unchanged author 14 separately from the frozen WG0I hostiles. A surrogate suite passing or failing cannot resolve the owner-run HOLD; the explicit WG0P sourcefree bypasses remain direct candidate REDs.
