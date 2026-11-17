"""Distinct-C bounded ABI witness over existing sourcefree code.

No product edit. Uses the product's existing prepared-session fixture and
asserts whether the candidate's named first-consumer wrappers accept the
candidate's PreparedSavedC11Admission subclass.
"""
from __future__ import annotations

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11AdmissionError
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _prepared(tmp_path, monkeypatch, tag):
    source, qa, predicate, other, queries, admission = _fixture(
        monkeypatch, tmp_path / tag, tag,
    )
    assert type(admission).__name__ == "PreparedSavedC11Admission"
    return admission, queries, predicate, qa


def test_saved_i03_wrapper_rejects_prepared_subclass(tmp_path, monkeypatch):
    admission, queries, predicate, _qa = _prepared(tmp_path, monkeypatch, "ABI-I03")
    with pytest.raises(
        SavedC11AdmissionError, match="exact SavedC11Admission required",
    ):
        execute_saved_i03(
            admission,
            query_ref=queries["selected"].ref,
            predicate_ref=predicate.ref,
        )


def test_batch_runner_rejects_prepared_subclass(tmp_path, monkeypatch):
    admission, queries, _predicate, _qa = _prepared(tmp_path, monkeypatch, "ABI-BATCH")
    unit = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=queries["selected"].ref,
        release_refs=(admission.release_ref,),
    )
    manifest = BatchManifest(units=(unit,))
    with pytest.raises(
        BatchIntegrityError, match="repository must be accepted",
    ):
        BatchExecutionRunner(
            manifest=manifest,
            repository=admission,
            saved_mode=True,
        )
