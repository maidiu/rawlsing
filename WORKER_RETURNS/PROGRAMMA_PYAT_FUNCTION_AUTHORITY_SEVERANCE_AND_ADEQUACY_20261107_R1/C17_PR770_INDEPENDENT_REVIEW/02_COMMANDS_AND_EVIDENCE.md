# C17 — exact commands, reproduction, and output hashes

## Exact PR / issue / source identity

```text
gh api repos/maidiu/rawlsing/pulls/770
  state=open, merged=false, reviews=[] at intake
  head_sha=392de04e86202a2a80361a91808ef06fd34c1cc8
  head_ref=agent/pyat753-r7-three-first-consumer-authority-falsifiers-20261107-r1
  base_ref=integration/pre-main-reconciliation-r1
gh api repos/maidiu/rawlsing/issues/765
  state=open; R7 three sourcefree first-consumer falsifiers
git ls-remote origin refs/heads/agent/pyat753-r7-three-first-consumer-authority-falsifiers-20261107-r1 refs/heads/integration/pre-main-reconciliation-r1
  392de04e86202a2a80361a91808ef06fd34c1cc8  refs/heads/agent/pyat753-r7-three-first-consumer-authority-falsifiers-20261107-r1
  7a5429ffbc48efd25e28c912da80c822e66bc182  refs/heads/integration/pre-main-reconciliation-r1
git -C hq merge-base --is-ancestor 7a5429ff 392de04e -> 0
git -C hq diff --name-status 7a5429ff 392de04e
  only WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/R7_SOURCEFREE_FIRST_CONSUMER_TESTS/*
  (no production module, existing-test, data or protected diff)
```

HQ `GOAL.md`, `C16_EXACT_C15_CORRECTIONS/PARENT_ISSUE_DISPOSITIONS.jsonl` (#765/#770 sourcefree scope, T01 RED, no production repair, A06/A07 holds), and `SECONDARY_AGENDA_FROZEN.jsonl` A06/A07 were read.

## Pinned source and sparse worktree

```text
state dir: /Users/matthewsmith/Desktop/Rawlsing_Controller/local-automation-state/pyat777-01a15c1e/pyat777-pr770-independent-sourcefree-review-r1
pinned worktree: .../pinned-source
git -C hq worktree add --no-checkout --detach <pinned> 392de04e86202a2a80361a91808ef06fd34c1cc8
git -C <pinned> sparse-checkout init --cone
git -C <pinned> sparse-checkout set rawlsing_next WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/R7_SOURCEFREE_FIRST_CONSUMER_TESTS
git -C <pinned> checkout
git -C <pinned> rev-parse HEAD -> 392de04e86202a2a80361a91808ef06fd34c1cc8
```

Sparse worktree contained only `rawlsing_next`, the authorized R7 return directory, README/.gitignore; **no respondent/data/SAV/DTA/DB directories**. It was clean and was removed after evidence/source-hash retention:

```text
git -C hq worktree remove --force <pinned> -> exit 0
pinned-source removed
```

Interpreter: `/usr/local/bin/python3`, Python `3.11.3`. No environment install.

## Focused test suite

From the pinned worktree root:

```text
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C17>/repro/tmp \
/usr/local/bin/python3 -B -m pytest -q -p no:cacheprovider --basetemp=<C17>/repro/tmp/pytest \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
```

Result: `97 passed in 2.33s`, exit `0`. Log SHA-256 `196f87871de5e018a45d5d8acb3025839867339354bf3dab1319e7da05fe39f5`.

## Exact runner reproduction

The exact `08_EXECUTION_RUNNER.py` was copied unchanged to `<C17>/repro/08_EXECUTION_RUNNER.py` (SHA-256 `21f695335e73839475e4321222fbf9ed28ae7d4889c903644c6d6c026a6ee4d4`). It was run with `PYTHONPATH` pointing at the pinned source; outputs were written only in the C17 lease:

```text
cd <C17>/repro
PYTHONPATH=<pinned> PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C17>/repro/tmp \
/usr/local/bin/python3 -B <C17>/repro/08_EXECUTION_RUNNER.py
exit 0
```

Reproduced outputs:

```text
54114666a2442a3a844184dd53acdb51d62120e455e940d0f94f1fa478ca20ef  R7_EXECUTION_TRACE.json
2342ec75ba97a652c08d5f3e984dcb7ab6a82107547e76c3ab06e248cba620c0  04_MUTATION_NEGATIVE_COLD_REPLAY.tsv
54114666a2442a3a844184dd53acdb51d62120e455e940d0f94f1fa478ca20ef  runner_stdout.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  runner_stderr.log (empty)
```

Both `R7_EXECUTION_TRACE.json` and `04_MUTATION_NEGATIVE_COLD_REPLAY.tsv` are **byte-identical** to the author artifacts at target `392de04e` (`cmp`/`diff` empty). The author's recorded trace hash `54114666...` and ledger hash `2342ec75...` match exactly.

## Source hashes at target (match R7 `05`)

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

## Observed T01/T02/T03 results

T01 baseline `SUPPORTED 2/2` fact `00cc5e59…`; wrong-kind/operation/scope ALLOW `SUPPORTED 2/2` facts `e931f6a3…`, `e072a0d5…`, `f5438214…`; DENY and positive-target controls `UNAVAILABLE 0/0`; cold restore baseline exact.

T02 baseline `SUPPORTED 2/2` fact `9ddfed96…`; target-only wrong-kind/operation/scope ALLOW pass `_parse_target_plan` but first consumer `UNAVAILABLE 0/0` facts `f5f61c20…`, `efad1de1…`, `6b088331…`; DENY `Pre553AuthorityError`/`UNAVAILABLE`; cold restore baseline exact.

T03 Q86 baseline `ADMITTED` relation `7c1c67cb…`; direct Q99B/Q99A call still labelled Q86 and `ADMITTED` (`fd3ee61c…`); cold restore baseline. Production search over `rawlsing_next` excluding tests:

```text
grep -R -n --exclude-dir=tests --exclude-dir=__pycache__ \
  -E 'produce_exact_conditional_support_profile|bridge_gt12_c_relation_to_d_evidence|admit_gt12_c_relation|field_forge_conditional_support|gt12_c_to_d_relation_bridge' rawlsing_next
```

Only producer definition/replay wrapper and bridge definitions/calls; no production alternate caller. Search log SHA-256 `7a2ae69eac96e496d45381e910fe30fe7c231bac4aa1257d5399fe3cb548ba63`.

## Scope and limits

T01/T02 are synthetic `TEST_ONLY` sourcefree fixtures; T03 has no production caller. The PR is **not** a genuinely demanded non-canary current-operation T2 demonstration, not original/native evidence, not a current issuer, not #748 parity and not a protected merge request. T2 demand/current-operation remains `UNPROVED`; A06/A07 holds remain open. No production patch, general FF build, CI waiver, merge or issue closure. No source/respondent/SAV/DTA/DB read; no data dirs in pinned worktree; no original scope/issuer minted; no worker/model change.
