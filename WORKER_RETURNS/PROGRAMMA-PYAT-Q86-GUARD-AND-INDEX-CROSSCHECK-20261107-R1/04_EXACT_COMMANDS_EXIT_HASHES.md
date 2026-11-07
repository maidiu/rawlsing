# EXACT COMMANDS, EXITS, AND HASHES

## Identity
- Branch: `fix/pyat-r8-frozen-ff-q86-source-identity-guard-20261107-r1`
- Base: `integration/pre-main-reconciliation-r1@7a5429ffbc48efd25e28c912da80c822e66bc182`
- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-r8-frozen-ff-q86-source-identity-guard-20261107-r1`
- Final PR head: recorded in `05_INDEPENDENT_REVIEW_REQUEST.md` and the PR review comment.
- Runner: OpenCode, `opencode-go/deepseek-v4.1-flash`; host `mainMac.lan`, macOS 13.2.1, Darwin 22.3.0 x86_64; Python 3.11.3; free disk about 12 GiB.

## Commands and results
```text
$ git rev-parse HEAD
7a5429ffbc48efd25e28c912da80c822e66bc182
exit 0

$ python3 -m pytest rawlsing_next/tests/test_field_forge_conditional_support.py rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py -q -p no:warnings
140 passed in 117.78s
exit 0

$ python3 -m pytest rawlsing_next/tests/test_pre553_c11_repository_ingest.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_empirical_query.py -q -p no:warnings
58 passed in 2.25s
exit 0

$ python3 -m pytest rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q -p no:warnings
41 passed in 5.14s
exit 0

$ python3 -m pytest rawlsing_next/tests/test_gt12_e2b_publication_governance_binding.py -q -p no:warnings
29 passed in 11.20s
exit 0

$ PYTHONPATH="$PWD" python3 WORKER_RETURNS/PROGRAMMA-PYAT-Q86-GUARD-AND-INDEX-CROSSCHECK-20261107-R1/06_R8_PROOF_RUNNER.py
exit 0
stdout: 252-line JSON proof trace
output: R8_PROOF_TRACE.json

$ python3 -m pytest rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py rawlsing_next/tests/test_gt34_q2_q69b_q86a_source_materialization.py rawlsing_next/tests/test_gt34_q2_same_source_c11_release.py -q -p no:warnings
1 failed, 12 passed, 3 errors in 173.61s
exit 1
inherited: identical failure/errors on untouched R7 base at 172.41s; see 07_R7_GATE_AND_INHERITED_FAILURES.md

$ git grep -n -I -E 'Q86A|Q86B|Q69B|GT12|GT34|Afrobarometer|FIRST_GENUINE_CANARY' 7a5429ffbc48efd25e28c912da80c822e66bc182 -- rawlsing_next
946 literal lines across 55 rawlsing_next files
exit 0
scope: rawlsing_next only; not an exhaustive all-tree/all-ref census
```

## Exact source hashes
```text
ed2dbd2fff1d9f8ebab2c5c74b41af2444490f6645aa702fcdd03767bc1bd538  rawlsing_next/field_forge_conditional_support.py
3c6639109338eed4d84dccd203732f5238c72e240d2a4339f68e17cca88bc8bf  rawlsing_next/tests/test_field_forge_conditional_support.py
8ca3d3610285010d64c4870a54376def7829a4b73e4f6dc762f0ee02a59b9258  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py
93cdd81a56ce1075757c6259358c20f83f599679ac1e4f1df2ccb5f1043deb5b  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
```

## Evidence hashes
```text
58e29ed60e5b222b89ec5e15583d3587e3824a7b2cbc580b08a6c22568f1a2f5  06_R8_PROOF_RUNNER.py
a1481103ab1e711c01db155b45d140fba1261efcc33634c2f343a27bb701573a  R8_PROOF_TRACE.json
0e88ee8cad16309bacdb93d085e4f1fc5fbc59c10f46301258c95ab650696558  02_INDEXED_16_CHAIN_CROSSCHECK.tsv
```

## R7 gate status
- PR #770 head `392de04e86202a2a80361a91808ef06fd34c1cc8`, OPEN, no reviews.
- `governed-court` failed on three inherited packaging tests; `canonical-tree` passed.
- R7 independent acceptance is pending; this PR does not claim it.

## Expected/actual negatives
- Guard refusals are expected findings: Q99 pair, forged Q86 kind, wrong identity hash, swapped roles.
- Bridge refusals: wrong risk, wrong source family/wave/artifact, missing permission.
- Nonpositive: `OBSERVED_ZERO` remains nonpositive (`UNRESOLVED`).
- Cold restore: exact baseline ref reproduced.
- The inherited GT34/A2 failure is recorded separately and is not a guard regression.
