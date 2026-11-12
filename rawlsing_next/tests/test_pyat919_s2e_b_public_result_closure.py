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
