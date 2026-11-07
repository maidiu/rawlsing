# C1 test receipts — Q86 R5 source-semantic first consumer

## Identity and deterministic environment

- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer`
- Branch: `agent/pyat777-source-consumer-20261107-r1`
- Startup: `03d054f1c693524e781767d96a287ca9e937e3ff`
- Protected observation: `7a5429ffbc48efd25e28c912da80c822e66bc182`
- Host: `mainMac.lan`, Darwin 22.3.0 x86_64
- Python: `3.11.3`
- Runner: existing local OpenCode; actual model id `opencode-go/deepseek-v4.1-flash`; separate effort telemetry is not exposed by this runtime. Commission target remains DeepSeek V4.1 Flash MAX.
- Seed: `PYTHONHASHSEED=0`
- `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` and pytest basetemp under this C1 output root.

## Commands and exits

### 1. Inherited focused 97-test suite — PASS

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B -m pytest -q -p no:cacheprovider --basetemp=<C1>/tmp/pytest-97 \
  rawlsing_next/tests/test_pre553_c11_repository_ingest.py \
  rawlsing_next/tests/test_pre553_source_backed_c11_facade.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_field_forge_conditional_support.py \
  rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py \
  rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py
```

Result: exit `0`; `97 passed in 3.02s`. Log SHA-256: `1b2cbb19e5ac4a0f00a25fdd1f147a6b04878208947eb70aac6a866f14868809`.

### 2. Direct Q86 sourcefree/canary tests — PASS

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B -m pytest -q -p no:cacheprovider --basetemp=<C1>/tmp/pytest-q86 \
  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py
```

Result: exit `0`; `8 passed in 0.32s`. Log SHA-256: `cf3877f5a0006b0cfe5842a91c99c70d59a6ac6d7e439551f7f664fc7cfe8886`.

These 8 tests are sourcefree synthetic Q86 fixtures. They prove the current first reader mechanics, not original issuer selection.

### 3. R7 T01 named falsifier rerun at current protected source — RED + restoration PASS

```sh
git show 392de04e86202a2a80361a91808ef06fd34c1cc8:WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/R7_SOURCEFREE_FIRST_CONSUMER_TESTS/08_EXECUTION_RUNNER.py > <C1>/probes/r7_t01_runner.py
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/r7_t01_runner.py
```

Result: exit `0`. Reused named falsifier: wrong-kind, wrong-operation, and wrong-scope ALLOW authorities each reach `SUPPORTED 2/2`; DENY is `UNAVAILABLE 0/0`; cold restore matches baseline.

- Runner SHA-256: `21f695335e73839475e4321222fbf9ed28ae7d4889c903644c6d6c026a6ee4d4`
- Trace SHA-256: `54114666a2442a3a844184dd53acdb51d62120e455e940d0f94f1fa478ca20ef`
- Mutation ledger SHA-256: `2342ec75ba97a652c08d5f3e984dcb7ab6a82107547e76c3ab06e248cba620c0`
- Severance RED: `T01_WRONG_KIND_OPERATION_SCOPE_SUPPORTED_2/2`
- Restoration PASS: cold restore fact ref `00cc5e59...` matches baseline.
- Scope: generic C11/I03 falsifier; **not** a Q86 selected-original proof.

### 4. Q86 selected-authority/source-semantic probe — PASS (SOURCEFREE_COMPARE_ONLY)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp \
python3 -B <C1>/probes/q86_source_semantics_probe.py
```

Result: exit `0`. Selected AR-0033 CSV is present, 15,498,257 bytes, SHA-256 `305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332`, matching accepted AR-0033. Q86A/Q86B each have 6 selected rows, `context_only`, `recommended_computation=none`, contract hashes `198f189a...` / `01ceeb78...`. Substantive 0/1 rows are `curated_packet`; specials -1/9/997/998 are `curated_special`. Current `rawlsing_next` contains neither selected contract hash. Current Q86 module pins source SHA `c9200ba...` but not the selected AR-0033 response contract; it has a code-created candidate substitute `GT12-A-R5-Q86-SOURCE-SEMANTICS` at `wave1_r5_q86_c11_projection.py:334`, whose competence/provenance is UNPROVED, not disproved. Literal hash absence alone is not severance. `context_only`/`recommended_none` does not by itself demonstrate a raw-count ban.

- Probe SHA-256: `1484506c8a794ff987e357d01171c86adb4caf4785725cf2fbebb55acec86412`
- Output SHA-256: `1b3ed2379bbdd6c4425b91053b83d2416f21537fd19c7964f8258460e4ccd77c`
- Raw log SHA-256 (retained; superseded wording): `6e2499141fed1a02f003a6bf37edbc21dbf83a595cc17ed0d33ab030c7a0a87a`
- `PROVENANCE_RED`: `SELECTED_AR0033_Q86_CONTRACT_HASH_NOT_BOUND__CURRENT_CANDIDATE_SUBSTITUTE_UNPROVED` (not a proved severance).
- `RESTORATION_PASS`: baseline Q86 sourcefree first-reader positive still `SUPPORTED 3/3` under the synthetic fixture.

### 5. Q86 exact negative/restoration probe — PASS

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/q86_negative_probe.py
```

Result: exit `0`. Baseline `SUPPORTED 3/3`. Typed refusal observed for:

- wrong source SHA;
- wrong QIMPL;
- wrong source-structure/wave grain;
- wrong common risk-set count;
- wrong target-use operation;
- widened GT1 permission ceiling.

Restoration: `true`; baseline `SUPPORTED 3/3` after all mutations are undone.

Selected Q86 version/shadow/withdrawal/cold-restore at the actual selected row: `NOT_RUN`. Exact blocker: no actual selected Q86 version fixture or competent issuer is supplied in this lease; the current test source is synthetic.

- Probe SHA-256: `403fd84765052308bd98c01f4a1031722bb3740c825195ff24686feafb6fb38f`
- Output SHA-256: `b0f013381ef6ae167403a5cc508c5dd84018f0371e1bfd34d6ab237140aae294`
- Log SHA-256: `b0f013381ef6ae167403a5cc508c5dd84018f0371e1bfd34d6ab237140aae294`
- Seed: `PYTHONHASHSEED=0`

### 6. Case builder / anti-join

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 TMPDIR=<C1>/tmp PYTHONPATH="$PWD" \
python3 -B <C1>/probes/build_case_outputs.py
```

Result: exit `0`; 212 register rows preserved, 17 matched, 195 unmatched; one case `C1-Q86-R5-RAW-001`.

- Builder SHA-256: `8f684884c68ecefae8972d9588466c46789d1e8137e77baff5bbb5477ae3c1ae`
- `01_CASES.jsonl` SHA-256: `1a494391d0e1cf817efde6aad5878d3fc1dec12969e58af805ebdeb6d883a767`
- `02_CASES.tsv` SHA-256: `861dbea0b415c9bb634fafd4c85cad6fb6505e6f0be4cd3ba268e74aeb6772b3`
- `04_MINIMAL_OWNER_ACTIONS.tsv` SHA-256: `44153bcc716838490cab290654ee43d62af529b070801c68c9a8023ae3debcfc`
- `05_REGISTER_ANTIJOIN.tsv` SHA-256: `2f7975d2463bc83601ddce8e6700c64f2e99520e5a35ee667a03267f264b48b4`
- Corrected build log SHA-256: `0c02bc0b3899d257ef58a109d594bd9c4bca3403e093ff2b85589629329ec3be`

## Source hashes used

```text
ab14f87d25a05c8b3463fceb47763d977aea6470798422ec3058f73a71ad5635  rawlsing_next/wave1_gt12_i03_positive_facts.py
0c56a0f6f656547a096982a6adab21c9b47d749385411a5d159f2b5390eec8bf  rawlsing_next/pre553_c11_ingest.py
969fb4c38eb86bb7a9be72c9af98e410c7130d74d4816618c9062e6e7c0b4913  rawlsing_next/_pre553_query_common.py
9c7613a55d434eb9e1e8fa2101d303ccf933370c5266ea1118e352c66066098c  rawlsing_next/_pre553_query_eval.py
7788feb514ad5eceb71e7d76191b1b80a66688dc64a56b0dc05f4a1b19bbdfcf  rawlsing_next/pre553_source_backed_c11_facade.py
7cd7fd4f8ccf79cb07b037ef9cdda5e60ed3c3ba0631c9f4030d09f4d666be94  rawlsing_next/pre553_empirical_query.py
ec9558c68a2138de7d44796986db39df28a679ccc1506785b79929d624d32034  rawlsing_next/field_forge_conditional_support.py
3360a93574750aaa1a67b43966e67b08d3ff89ea022bc0e59a69273dab920910  rawlsing_next/gt12_c_to_d_relation_bridge.py
79d99a1c9e6056cfb03b1478048e74e679562c868d1b49e8d895ceea763eafec  rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py
```

## Explicit NOT_RUN / limits

- No original respondent/SAV/DTA/DB read, no native original35 workload, no current native/science/actor issuance.
- No actual selected Q86 version/shadow/withdrawal/cold-restore fixture; no selected AR-0033 fixture/issuer. Current `GT12-A-R5-Q86-SOURCE-SEMANTICS` candidate competence/provenance is unproved, not disproved. This is the named blocker for the missing provenance test.
- No production/C11/runtime/source patch; no protected/HQ/peer writes.
- No claim of proved severance, proved equivalence, or full #777 completion.
- No claim that T01 wrong-kind/op/scope proves the Q86 historical row was selected.
- Reporting corrections are mapped in `06_REPORTING_CORRECTIONS.md`; no 97/8 suite was repeated for this reporting-only pass.
