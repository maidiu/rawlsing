from __future__ import annotations

from types import SimpleNamespace

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError, admit


class _ForgedResolver:
    def resolve_current(self, decision_ref):
        return {"decision_ref": decision_ref, "scope": "ORIGINAL_SOURCE_GRANTED"}


def test_forged_issuer_record_is_refused_before_source_open():
    ref = ExactRef("IssuedWorkloadDecision", "urn:test:fabricated", "a" * 64)
    with pytest.raises(WorkloadAdmissionError, match="CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED"):
        admit(
            SimpleNamespace(decision_ref=ref),
            _ForgedResolver(),
            host="local-r03",
            purpose="TEST_ONLY_SOURCEFREE",
            allow_test_only=True,
        )
