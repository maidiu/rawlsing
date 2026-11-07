# EXACT COMMANDS, EXITS, AND SOURCE HASHES

## Identity
- Branch: `agent/pyat753-r7-three-first-consumer-authority-falsifiers-20261107-r1`
- Base commit: `7a5429ffbc48efd25e28c912da80c822e66bc182`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat753-r7-first-consumer-falsifiers-20261107-r1`
- Model: `opencode-go/deepseek-v4.1-flash`
- Host: `mainMac.lan`, Darwin 22.3.0, macOS 13.2.1, x86_64
- Python: `/usr/local/bin/python3`, `Python 3.11.3`
- Disk: about 14 GiB free at execution time

## Commands
```text
$ git branch --show-current
agent/pyat753-r7-three-first-consumer-authority-falsifiers-20261107-r1
exit 0

$ git rev-parse HEAD
7a5429ffbc48efd25e28c912da80c822e66bc182
exit 0

$ python3 -m pytest rawlsing_next/tests/test_pre553_c11_repository_ingest.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_field_forge_conditional_support.py rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py -q
97 passed in 2.24s
exit 0

$ PYTHONPATH="$PWD" python3 WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/R7_SOURCEFREE_FIRST_CONSUMER_TESTS/08_EXECUTION_RUNNER.py
exit 0
stdout: 539-line JSON trace
output: R7_EXECUTION_TRACE.json
output: 04_MUTATION_NEGATIVE_COLD_REPLAY.tsv (17 lines including header)

$ grep -R -n --exclude-dir=tests --exclude-dir=__pycache__ "produce_exact_conditional_support_profile\|bridge_gt12_c_relation_to_d_evidence\|admit_gt12_c_relation\|field_forge_conditional_support\|gt12_c_to_d_relation_bridge" rawlsing_next
only producer definition/replay wrapper and bridge definition/bridge calls; no production caller
exit 0
```

## Source and evidence hashes
```text
0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf  rawlsing_next/pre553_c11_ingest.py
969fb4c38eb86bb7a9be72c9af98e410c7130d74d4816618c9062e6e7c0b4913  rawlsing_next/_pre553_query_common.py
7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf  rawlsing_next/pre553_source_backed_c11_facade.py
ec9558c68a2138de7d44796986db39df28a679ccc1506785b79929d624d32034  rawlsing_next/field_forge_conditional_support.py
3360a93574750aaa1a67b43966e67b08d3ff89ea022bc0e59a69273dab920910  rawlsing_next/gt12_c_to_d_relation_bridge.py
ab14f87d25a05c8b3463fceb47763d977aea6470798422ec3058f73a71ad5635  rawlsing_next/wave1_gt12_i03_positive_facts.py
3a6537d6b5de4a00363c025220c03e24ebd3f6483573d0d949ce456b254cb25a  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py
f1a93e83dd8b9f749523b0249e3796f8d13bb0d2909622e14023f09c07851b15  rawlsing_next/tests/test_pre553_empirical_query.py
58ebc00a039fd56c91d15d731459e1802cfa4106e156b365a9e713ccc9028b03  rawlsing_next/tests/test_field_forge_conditional_support.py
```

Evidence hashes:
```text
21f695335e73839475e4321222fbf9ed28ae7d4889c903644c6d6c026a6ee4d4  08_EXECUTION_RUNNER.py
2342ec75ba97a652c08d5f3e984dcb7ab6a82107547e76c3ab06e248cba620c0  04_MUTATION_NEGATIVE_COLD_REPLAY.tsv
54114666a2442a3a844184dd53acdb51d62120e455e940d0f94f1fa478ca20ef  R7_EXECUTION_TRACE.json
```

The runner is reproducible from the committed files. It has no production imports beyond the tested public modules and test fixtures.

## Expected negatives vs suite failure
- T01 DENY and all target-only T02 mutations are expected typed negatives; they returned `UNAVAILABLE 0/0`.
- T01 wrong-kind/wrong-operation/wrong-scope ALLOW show the counterexample `SUPPORTED 2/2`; these are findings, not pytest failures.
- T03 direct-call Q99 is a latent direct-call mislabel; no production caller was found.
- The focused pytest suite passed 97/97. No unexpected suite failure was observed.

## Scope note
No production module was modified. No original Mac/respondent data, native source asset, issuer, CAS, or protected branch was used. Sourcefree synthetic fixtures only.
