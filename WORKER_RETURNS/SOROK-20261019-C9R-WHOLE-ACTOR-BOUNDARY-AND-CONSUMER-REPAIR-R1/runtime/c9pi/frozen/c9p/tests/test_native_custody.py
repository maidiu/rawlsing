"""Native module custody: exact imported __file__ and Git blob identity tests."""
from __future__ import annotations

from candidate.native_custody import (
    CustodyMismatch,
    candidate_import_graph,
    record_module_custody,
)


def test_native_guard_custody_records_real_file() -> None:
    custody = record_module_custody("rawlsing_next.v3_psepf_zero_positive_guard")
    assert custody.imported is True
    assert custody.module_file.endswith("v3_psepf_zero_positive_guard.py")
    assert custody.git_blob_sha1
    assert custody.content_sha256
    assert "rawlsing_next" in custody.relative_path


def test_import_graph_covers_candidate_native_dependencies() -> None:
    graph = candidate_import_graph()
    assert "rawlsing_next.v3_psepf_zero_positive_guard" in graph
    assert "rawlsing_next.wsc_gt0_v3_runtime" in graph
    for name, custody in graph.items():
        assert custody.imported, name
        assert custody.git_blob_sha1, name
        assert custody.content_sha256, name


def test_blob_mismatch_raises_custody_mismatch() -> None:
    try:
        record_module_custody(
            "rawlsing_next.v3_psepf_zero_positive_guard",
            expected_blob="0" * 40,
        )
    except CustodyMismatch as error:
        assert "v3_psepf_zero_positive_guard" in str(error)
    else:  # pragma: no cover - custody must fail on a wrong expected blob
        raise AssertionError("custody accepted a mismatched expected blob")


def test_guard_production_registry_is_empty() -> None:
    from rawlsing_next import v3_psepf_zero_positive_guard as native_guard

    assert dict(native_guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
