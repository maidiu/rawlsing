# Before/after failure record

All four rows below are the exact initial QF1 failure set. No additional source-independent failure was exposed by the repairs.

## 1. Production syntax defect

Original status: FAIL.

Original evidence:

    File rawlsing_next/ee_p2x_darwin_stage_backend.py, line 1102
      "parity":parity,"performance_admission":("NOT_ADMITTED" if stopped else\n            ("ADMITTED_AFTER_INDEPENDENT_ORACLE_MATCH" if state["performance_admitted"] else\n             "PENDING__INDEPENDENT_ORACLE_MATCH")),
    SyntaxError: unexpected character after line continuation character

Repair: restored the intended expression line breaks only. No surrounding state, parity, terminal, or accounting logic changed.

Repair commit: `c47398ccff4594be96c778ec1b2f8f830fbc64d4`.

Focused after status: `python3 -m compileall -q rawlsing_next` PASS; W3-I04 PASS, 6/6.

Full after status: PASS.

## 2. R35-I02 hostile helper setup

Original status: FAIL, 8 passed and 1 error.

Original failing test: `test_forged_derivative_with_correct_asserted_source_sha_is_rejected`.

Original error:

    File tests/test_fiabc_derivative_parentage.py, line 186, in _verify_wvs
      expected_source_receipt_identity=bundle["source_receipt"]["receipt_identity"],
    KeyError: 'source_receipt'

Repair: the helper now conditionally extracts dynamic receipt identities, passing `None` when the malformed bundle omits them. `verify_parentage_bundle` therefore receives the malformed object and produces the required rejection. Valid bundles still bind their receipt identities.

Repair commit: `7fa7c9fd772c71909b1def32385b7d890b1d0438`.

Focused after status: PASS, 9/9.

Full after status: PASS.

## 3. R35-I03 exact-numeric fixture

Original status: FAIL, 2 passed and 13 failed.

Original failing tests: the 13 tests listed in the QF1 failure report. They all failed during `expectation()` construction because `base_evidence()` used `weight: [1.0, 2.0]` and `canonicalize()` correctly raised:

    Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity

Repair: imported `Decimal` and changed only the fixture values to `Decimal("1.0")` and `Decimal("2.0")`. The production canonicalizer still rejects binary floats.

Repair commit: `4ee072b228b7bec1aeea1732d4aa019869a291b8`.

Focused after status: PASS, 15/15.

Full after status: PASS.

## 4. W3-I06A temporary-root setup

Original status: FAIL, 8 passed and 1 failed.

Original failing test: `test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails`.

Original error:

    File tests/test_fiabc_w3_i06a_process_isolation.py, line 30, in _freeze
      path.write_text(...)
    FileNotFoundError: [Errno 2] No such file or directory: '.../second/candidate-neutral-freeze.json'

Repair: `_freeze()` creates its requested temporary root with `parents=True, exist_ok=True` before writing the receipt.

Repair commit: `0bac08af6e57145c3c2dcd1a4e6b38fe1927aa62`.

Focused after status: PASS, 9/9.

Full after status: PASS.

