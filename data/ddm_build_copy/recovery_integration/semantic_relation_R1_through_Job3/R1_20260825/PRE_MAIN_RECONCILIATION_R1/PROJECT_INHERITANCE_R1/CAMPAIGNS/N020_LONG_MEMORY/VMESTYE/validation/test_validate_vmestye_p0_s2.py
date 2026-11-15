from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("validate_vmestye_p0_s2.py")
SPEC = importlib.util.spec_from_file_location("vmestye_p0_s2", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_digest_keys_uses_sorted_canonical_json_and_trailing_newline():
    keys = [("LMX-002",), ("LMX-001",)]
    material = '["LMX-001"]\n["LMX-002"]\n'
    import hashlib
    expected = "sha256:" + hashlib.sha256(material.encode()).hexdigest()
    assert MODULE.digest_keys(keys) == expected


def test_key_tuple_requires_json_array():
    assert MODULE.key_tuple('["A",1]') == ("A", 1)
    with pytest.raises(ValueError):
        MODULE.key_tuple('{"A":1}')


def test_parse_int_is_exact():
    assert MODULE.parse_int("42", "n") == 42
    with pytest.raises(ValueError):
        MODULE.parse_int("4.2", "n")


def test_p1_headers_have_frozen_widths():
    widths = {name: len(header) for name, header in MODULE.P1_HEADERS.items()}
    assert widths == {
        "OPERATION_TRACES.tsv": 21,
        "AUTHORITY_USE.tsv": 16,
        "EVIDENCE.tsv": 19,
        "COVERAGE.tsv": 16,
        "UNJOINS.tsv": 19,
    }
    for header in MODULE.P1_HEADERS.values():
        assert len(header) == len(set(header))


def test_stage_order_contains_required_transitions():
    assert list(MODULE.STAGES) == [
        "PREPARED", "DISPATCHED_BY_USER", "ACTIVE_VERIFIED",
        "RETURNED_AT_SHA", "INDEPENDENT_REVIEWED", "ACCEPTED_TO_VMESTYE",
    ]
