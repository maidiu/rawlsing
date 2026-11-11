# CCF5-R01 test receipts

Runner: `/usr/local/bin/python3` 3.11.3. Synthetic local Git/evidence fixtures
only; no source, respondent, native, science, actor, install or protected merge.

## Focused validator tests

```
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/mcr/API_BINDING_R2/logs/verifier_tests_junit.xml
```

Result: `5 passed in 1.80s` (`logs/verifier_tests.log`).

The added test covers valid evidence text plus external junk path, missing path,
and restoration with the valid external path.

## Existing self-test and contracts

- `verify_copy_paste_commission_r1.py --self-test`: `PASS_SELF_TEST`; 32 negative
  mutations rejected (`logs/validator_self_test.log`).
- `MCR_EXECUTABLE_LAUNCH.md`: `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH`; 12
  obligations (`logs/launch_validate.log`).
- Frozen original: historical `RED_INVALID_FOR_DISPATCH`
  (`logs/frozen_contract_red.log`).

## Direct API/CLI counterexample

`logs/api_text_path_probe.log` records:

- API valid evidence text + external junk path: `RED_INCOMPLETE`,
  `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH`;
- API valid text + valid external path: `READY_FOR_INDEPENDENT_RECEIVING`;
- CLI valid external path: `READY_FOR_INDEPENDENT_RECEIVING`, exit 0;
- CLI junk path: `RED_INCOMPLETE`, exit 2.

The prior RED is retained in independent recheck
`f250bded334fd7a300113e7b9a9118f841e597d4`; no review artifact was rewritten.
