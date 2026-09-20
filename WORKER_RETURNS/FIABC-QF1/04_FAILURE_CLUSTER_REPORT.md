# FIABC-QF1 failure cluster report

The first pass did not modify production code. The paths and line numbers below are from the exact QF1 checkout at HEAD 44255e97119c83be86cefec032d0f0a244b00258.

## FC-1 — live backend syntax error

Classification: implementation defect. Obligation owner: live stage backend. Affected commands: compileall and W3-I04 runtime packaging/rebind.

The exact compiler error was:

    *** Error compiling 'rawlsing_next/ee_p2x_darwin_stage_backend.py'...
      File "rawlsing_next/ee_p2x_darwin_stage_backend.py", line 1102
        "parity":parity,"performance_admission":("NOT_ADMITTED" if stopped else\n            ("ADMITTED_AFTER_INDEPENDENT_ORACLE_MATCH" if state["performance_admitted"] else\n             "PENDING__INDEPENDENT_ORACLE_MATCH")),
                                                                                ^
    SyntaxError: unexpected character after line continuation character

The two W3-I04 failures reached the same parse error through ast.parse:

    Traceback (most recent call last):
      File "rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py", line 72, in test_backend_uses_only_stable_current_runtime_bindings
        const = assigned_constants(BACKEND)
      File "rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py", line 36, in assigned_constants
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
      File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/ast.py", line 50, in parse
        return compile(source, filename, mode, flags, _feature_version=feature_version)
      File "rawlsing_next/ee_p2x_darwin_stage_backend.py", line 1102
        "parity":parity,"performance_admission":("NOT_ADMITTED" if stopped else\n            ("ADMITTED_AFTER_INDEPENDENT_ORACLE_MATCH" if state["performance_admitted"] else\n             "PENDING__INDEPENDENT_ORACLE_MATCH")),
                                                                               ^
    SyntaxError: unexpected character after line continuation character

The second failing W3-I04 test is RuntimePackagingRebindTests.test_governed_runtime_identities_and_dependency_hashes_are_unchanged; it has the identical traceback with its test method at line 94. Four W3-I04 tests passed.

## FC-2 — R35-I02 malformed forged fixture stops in helper

Classification: unknown, with a test fixture/helper construction defect observed. Obligation owner: derivative-parentage hostile court. The hostile law must remain: an asserted source SHA without a valid source receipt must be rejected.

Command result: 8 tests passed, one error. Failing test:

DerivativeParentageContractTests.test_forged_derivative_with_correct_asserted_source_sha_is_rejected

Complete observed traceback:

    Traceback (most recent call last):
      File "tests/test_fiabc_derivative_parentage.py", line 219, in test_forged_derivative_with_correct_asserted_source_sha_is_rejected
        self._verify_wvs(forged, wvs_doc())
      File "tests/test_fiabc_derivative_parentage.py", line 186, in _verify_wvs
        expected_source_receipt_identity=bundle["source_receipt"]["receipt_identity"],
                                         ~~~~~~^^^^^^^^^^^^^^^^^^^
    KeyError: 'source_receipt'

The supplied forged object contains source_sha256, rows, variables, and structural_input_identity, but no source_receipt. The helper dereferences that absent field before verify_parentage_bundle can emit the intended ParentageError.

## FC-3 — R35-I03 exact-numeric fixture mismatch

Classification: unknown, with a fixture/accepted-contract mismatch observed. Obligation owner: R35-I03 synthetic physical-equivalence court. The production canonicalizer explicitly rejects binary floats in semantic identity; the fixture supplies them.

All 13 failures reached the same construction error. The failing test identities and distinct expectation call sites were:

| Test | Call site |
|---|---:|
| test_positive_direct_raw_receipt_is_physical_only | line 161 |
| test_source_without_mr_or_weight_edges_does_not_require_meaningless_fields | line 171 |
| test_wrong_reader_version_fails_even_when_source_and_semantic_digest_match | line 180 |
| test_all_missing_column_drop_is_physical_nonequivalence | line 218 |
| test_display_metadata_may_not_replace_raw_storage_magnitude | line 234 |
| test_raw_header_dictionary_stream_mismatch_must_survive_metadata_digest | line 248 |
| test_mr_topology_flattening_fails_with_identical_raw_vectors | line 267 |
| test_weight_candidates_are_physical_facts_not_default_selection | line 284 |
| test_candidate_subset_cache_cannot_drop_canonical_extra_dimension | line 300 |
| test_equal_semantic_projection_does_not_rescue_unequal_physical_metadata | line 310 |
| test_derivative_with_asserted_source_sha_but_no_parentage_receipt_is_rejected | line 331 |
| test_derivative_parentage_wrong_ancestor_is_rejected | line 341 |
| test_verified_derivative_parentage_can_close_to_same_canonical_expectation | line 351 |

Complete common traceback tail, with the listed test-specific first frame:

    Traceback (most recent call last):
      File "rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py", line <TEST_CALL_LINE>, in <test_method>
        expected = expectation(...)
      File "rawlsing_next/tests/test_fiabc_r35_i03_physical_equivalence.py", line 91, in expectation
        return build_canonical_expectation(
      File "rawlsing_next/fiabc_whole_source_physical_equivalence.py", line 270, in build_canonical_expectation
        evidence = _evidence_digests(evidence_material, metadata["physical_metadata_digest"])
      File "rawlsing_next/fiabc_whole_source_physical_equivalence.py", line 238, in _evidence_digests
        digests = {str(key): canonical_digest(value) for key, value in evidence.items()}
      File "rawlsing_next/fiabc_whole_source_physical_equivalence.py", line 238, in <dictcomp>
        digests = {str(key): canonical_digest(value) for key, value in evidence.items()}
      File "rawlsing_next/fiabc_whole_source_physical_equivalence.py", line 83, in canonical_digest
        return semantic_hash(canonicalize(material))
      File "rawlsing_next/pre553_empirical_objects.py", line 206, in canonicalize
        return {k: canonicalize(value[k]) for k in sorted(value)}
      File "rawlsing_next/pre553_empirical_objects.py", line 206, in <dictcomp>
        return {k: canonicalize(value[k]) for k in sorted(value)}
      File "rawlsing_next/pre553_empirical_objects.py", line 211, in canonicalize
        return [canonicalize(v) for v in value]
      File "rawlsing_next/pre553_empirical_objects.py", line 211, in <listcomp>
        return [canonicalize(v) for v in value]
      File "rawlsing_next/pre553_empirical_objects.py", line 190, in canonicalize
        raise Pre553IntegrityError("float/NaN/Infinity forbidden in semantic identity")
    rawlsing_next.pre553_empirical_objects.Pre553IntegrityError: float/NaN/Infinity forbidden in semantic identity

The exact fixture source is base_evidence() line 66: "weight": [1.0, 2.0]. The two R35-I03 tests not in this cluster passed.

## FC-4 — W3-I06A temporary-root setup error

Classification: unknown, with a test setup defect observed. Obligation owner: process-isolation test fixture. The foreign-candidate-state rejection assertion was not reached in the failing test.

Failing test: test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails.

Complete observed traceback:

    Traceback (most recent call last):
      File "rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py", line 251, in test_scratch_and_durable_state_are_cell_local_and_foreign_marker_fails
        controller = _controller(tmp_path / "second")
      File "rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py", line 133, in _controller
        freeze_receipt_path=_freeze(tmp_path),
      File "rawlsing_next/tests/test_fiabc_w3_i06a_process_isolation.py", line 30, in _freeze
        path.write_text(
      File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/pathlib.py", line 1078, in write_text
        with self.open(mode='w', encoding='utf-8', errors=errors, newline=newline) as f:
      File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/pathlib.py", line 1044, in open
        return io.open(self, mode, buffering, encoding, errors, newline)
    FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pytest-of-matthewsmith/pytest-3/test_scratch_and_durable_state0/second/candidate-neutral-freeze.json'

Eight W3-I06A tests passed.

## Non-failures and boundary observations

- R35-Q01 hostile cases all passed, including physical/semantic/source-certification claim separation.
- The static identity court passed all expected blobs; no lookalike substitution occurred.
- No failure was caused by opening a prohibited real survey carrier.
- The absent python alias is an environment observation, not the qualification terminal: python3 and pytest were available and executed the suites. It is retained as BLOCKED command evidence rather than silently normalized.
