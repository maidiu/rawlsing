# CC-F05 verifier test receipts

Runner: `/usr/local/bin/python3` 3.11.3. No source, respondent, SAV/DTA/DB,
native, science, actor, protected merge or environment install.

## New focused validator tests

```
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  CROSS_HQ_CONTROL_ROOM/test_verify_copy_paste_commission_r1.py \
  --junitxml=WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/mcr/VERIFIER_R1/logs/verifier_tests_junit.xml
```

Result: `4 passed in 1.09s` (`logs/verifier_tests.log`).

The tests exercise:

- launch artifact single-fenced prompt with 12 MCR obligations;
- frozen contract baseline RED;
- external evidence accepted;
- evidence tracked at the candidate rejected (`MCR_C_EVIDENCE_TRACKED_AT_CANDIDATE`);
- wrong candidate rejected;
- forged output digest rejected;
- restoration to a valid external evidence path after each negative.

## Existing validator self-test

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
```

Result: `PASS_SELF_TEST`; 5 positive kinds; 32 negative mutations rejected
(`logs/validator_self_test.log`). This is format readiness, not authority.

## Launch artifact validation

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/MCR_EXECUTABLE_LAUNCH.md
```

Result: `PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH`; 12 obligations;
`mcr_completion_contract_sha256=1e7d6a905bb702c289708d636627625759cee38f883851c60a502126f5b47583`
(`logs/launch_validate.log`).

## Frozen contract baseline

```
python3 CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py \
  PYAT_W03_W04_MCR_C_Commission.md
```

Result: `RED_INVALID_FOR_DISPATCH` / `REQUIRES_EXACTLY_ONE_COMPLETE_FENCED_COPY_PASTE_BLOCK`
(`logs/frozen_contract_red.log`). The frozen commission bytes are unchanged:
SHA-256 `ddc6273adcc9aeb1b7e75c7d82897dde929adffea152e7f57dc5254fa32f0166`.

## Baseline / restoration

The prior independent RED is preserved in review
`2959dda3c95b05db40a399d6d746401f434f5a38`, combined-code finding `CC-F05` and
its probes/logs. This repair does not modify that review or claim its RED passed.
The new tests retain the negative result and restore the positive external
evidence result after each negative.
