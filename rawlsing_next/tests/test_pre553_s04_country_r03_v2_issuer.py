"""R03 v2 exact-query-issuer binding: no injected country comparison jobs.

R03 v2 is SOURCEFREE TEST_ONLY. This test does not imply original authority.
Uses its actual existing one-pass sourcefree saved native fixture; no synthetic
replacement query issuer is allowed.
"""
import pytest
pytest.importorskip("pyarrow")

from rawlsing_next.pre553_governed_query_issuer_v2 import (
    _issue_compiled_governed_queries_v2,
)
from rawlsing_next.pre553_s04_country_refinement import (
    CountryRefinementError, CountryRequest, RefinementBudget,
    run_r03_v2_issued_country_refinement,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e


def _call(issue, *, operation_id, query_role, execution=None):
    return run_r03_v2_issued_country_refinement(
        issuance=issue, operation_id=operation_id, query_role=query_role,
        universe=None, execution=execution,
        request=CountryRequest("US", "SURVEY", "W1"),
        target_index=0, candidate_indices=(1,), context={},
        budget=RefinementBudget(
            max_input_cells=50, max_cell_visits=500,
            max_output_cells=50, max_candidates=1, wall_seconds=10,
        ),
    )


def test_r03_exact_issued_job_binding_refuses_unissued_operation(tmp_path):
    _, _, _, compilation, _, _ = s1e._full(tmp_path / "r03-s04-issuer")
    issue = _issue_compiled_governed_queries_v2(compilation)
    assert issue.operation_jobs
    with pytest.raises(CountryRefinementError, match="R03_ORIGINAL_QUERY_ROLE_NOT_ISSUED"):
        _call(issue, operation_id="INJECTED", query_role="BASE")


def test_r03_mismatched_issued_query_execution_refuses_before_s04(tmp_path):
    _, _, _, compilation, _, _ = s1e._full(tmp_path / "r03-s04-mismatch")
    issue = _issue_compiled_governed_queries_v2(compilation)
    job = issue.operation_jobs[0]
    # The sourcefree R03 job is real, but none of its scientific results may
    # be replaced by a caller-injected "execution" object.
    with pytest.raises(CountryRefinementError, match="R03_SOURCE_QUERY_PREDICATE_EXECUTION_DRIFT"):
        _call(issue, operation_id=job.operation_id, query_role=job.query_role,
              execution=None)
