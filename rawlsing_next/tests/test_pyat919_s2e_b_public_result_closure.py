"""Agent B hostile first-consumer census attack against #919 S2-E/P2-06.

The issued result has TWO output surfaces: the actual public native_outputs/output_refs
and the per-unit map consumed by the post-execution conservation census.
A complete census must not pass when either public result surface loses data
while the cached map and Batch receipts remain unchanged.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_s2e_exact_conservation import S2EOutputConservationError
from rawlsing_next.tests.test_pyat919_s2e_a_conservation import _full_query_run


def _issued_case(tmp_path):
    result = _full_query_run(tmp_path)
    assert result.native_outputs
    assert result.output_refs
    assert result.outputs_by_unit
    catalog_result = result.exact_s2e_output_census(require_complete=True)
    assert catalog_result.complete
    assert catalog_result.completed_count == len(result.manifest.units)
    return result, catalog_result


def test_b_missing_public_native_outputs_must_not_pass_complete_census(tmp_path):
    result, original = _issued_case(tmp_path)
    missing = replace(result, native_outputs=())
    # The actual issued consumer would now see no outputs even though the
    # private per-unit audit map still contains all of them.
    assert not missing.native_outputs and missing.outputs_by_unit
    with pytest.raises(S2EOutputConservationError, match="S2E_NATIVE_OUTPUT_VIEW_LOSS"):
        missing.exact_s2e_output_census(require_complete=True)
    restored = replace(missing, native_outputs=result.native_outputs)
    assert restored.exact_s2e_output_census(require_complete=True) == original


def test_b_missing_public_output_refs_must_not_pass_complete_census(tmp_path):
    result, original = _issued_case(tmp_path)
    missing = replace(result, output_refs=())
    assert not missing.output_refs and missing.outputs_by_unit
    with pytest.raises(S2EOutputConservationError, match="S2E_NATIVE_RESULT_REF_VIEW_LOSS"):
        missing.exact_s2e_output_census(require_complete=True)
    restored = replace(missing, output_refs=result.output_refs)
    assert restored.exact_s2e_output_census(require_complete=True) == original


def test_b_real_universal_first_consumer_refuses_lost_native_view_and_restores(
    tmp_path, monkeypatch,
):
    """The real R03 first reader uses result.native_outputs for fact_refs."""
    import rawlsing_next.pre553_universal_workload as machine
    from rawlsing_next.tests.test_universal_workload import (
        AS_OF, HOST, PURPOSE, build_s3, s3_rows,
    )

    bundle = build_s3(tmp_path / "s2e-b-first-reader.sav",
                      s3_rows(respondents=6, occasions=2))
    compiled = machine.compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    source_factory = lambda _ref: bundle.physical_stream
    baseline = machine.execute_universal_workload(
        compilation=compiled, source_factory=source_factory,
    )
    assert baseline.anti_join()["no_drop_ok"]
    assert baseline.fact_refs and not baseline.failed

    selected = next(item for item in compiled.compiled if item.issued is not None)
    original_executor = machine.execute_test_only_workload

    def missing_published_output(*, issued, source_factory, host, purpose):
        result = original_executor(
            issued=issued, source_factory=source_factory, host=host, purpose=purpose,
        )
        if issued.envelope_sha256 == selected.issued.envelope_sha256:
            assert result.native_outputs and result.outputs_by_unit
            return replace(result, native_outputs=())
        return result

    with monkeypatch.context() as m:
        m.setattr(machine, "execute_test_only_workload", missing_published_output)
        severed = machine.execute_universal_workload(
            compilation=compiled, source_factory=source_factory,
        )
    assert not severed.anti_join()["no_drop_ok"]
    assert selected.operation.operation_id not in severed.executed_operation_ids
    assert any(
        f["operation_id"] == selected.operation.operation_id
        and f["status"] == "ERROR"
        and f["reason"] == "S2EOutputConservationError"
        for f in severed.failed
    )

    restored = machine.execute_universal_workload(
        compilation=compiled, source_factory=source_factory,
    )
    assert restored.anti_join()["no_drop_ok"]
    assert restored.fact_refs == baseline.fact_refs
    assert restored.receipt_refs == baseline.receipt_refs
    assert restored.executed_operation_ids == baseline.executed_operation_ids
