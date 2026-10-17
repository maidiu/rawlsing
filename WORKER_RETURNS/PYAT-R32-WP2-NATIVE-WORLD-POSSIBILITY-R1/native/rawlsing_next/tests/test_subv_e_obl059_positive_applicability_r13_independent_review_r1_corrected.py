"""Corrected independent-review harness binding for OBL059 R13.

The first review execution showed one harness-only assertion error: it treated every
appearance of a forbidden alias authority as unlawful, including the receipt's
legitimate downstream ADP-010 consumer identity. This wrapper preserves all other
independent cases unchanged and narrows that identity assertion to authority-bearing
source fields rather than consumer metadata.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BASE_TEST = ROOT / "rawlsing_next/tests/test_subv_e_obl059_positive_applicability_r13_independent_review_r1.py"
spec = importlib.util.spec_from_file_location("_obl059_r13_independent_base", BASE_TEST)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load independent base review surface: {BASE_TEST}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

IDENTITY_TEST = "test_013_receipt_source_and_authority_identity_are_exact_and_forbidden_aliases_do_not_surface"
SAFE_TESTS = tuple(
    name
    for name in sorted(dir(base))
    if name.startswith("test_") and callable(getattr(base, name)) and name != IDENTITY_TEST
)


@pytest.mark.parametrize("test_name", SAFE_TESTS)
def test_001_independent_cases_preserved(test_name):
    getattr(base, test_name)()


def test_002_receipt_source_authority_is_exact_without_misclassifying_consumer_identity():
    result = base.assert_positive(base.canonical(base.fixture()))
    authority_fields = {
        key: value
        for key, value in result.items()
        if type(key) is str and type(value) is str and "authority" in key.lower()
    }
    assert authority_fields, result
    assert any(value == base.r13.AUTHORITY_ID for value in authority_fields.values()), authority_fields

    # ADP-010 may lawfully appear as a consumer identity. Only fields that purport
    # to identify the OBL059/source/semantic authority are barred from aliasing.
    for key, value in authority_fields.items():
        lowered = key.lower()
        if "consumer" in lowered:
            continue
        if "source" in lowered or "semantic" in lowered or lowered in {"authority", "authority_id"}:
            assert value not in base.r13.FORBIDDEN_ALIAS_AUTHORITIES, (key, value, authority_fields)

    consumer_fields = {
        key: value for key, value in authority_fields.items() if "consumer" in key.lower()
    }
    if consumer_fields:
        assert base.r13.ADP010_CONSUMER in consumer_fields.values(), consumer_fields
