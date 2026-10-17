"""Post-freeze F6N diagnostics, not part of the Phase-A pass/fail oracle.

These verify the actual repaired producer's mixed-origin and consumer behaviour
that the inherited F6L P5B test never executed because of its world-alias
KeyError.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
STAGE = RET / "03_PHASE_B/F6M_STAGE"
F6L = RET / "01_INHERITED_F6L"
sys.dont_write_bytecode = True
sys.path.insert(0, str(STAGE))
sys.path.insert(0, str(F6L / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, semantic_hash)
import rawlsing_next.pre553_heterogeneous_synthesis as P  # noqa: E402
import f6l_worlds as W  # noqa: E402
import f6n_worlds as N  # noqa: E402


def run(world, admit=lambda *_: True):
    return synthesize(world["target"], world["sources"], world["policy"], admit=admit)


def ceilings(out):
    return {n.get("authority_ceiling") for n in out["evidence_graph"]}


def test_candidate_producer_and_dependency_blobs_are_exact():
    raw = Path(P.__file__).read_bytes()
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == \
        "2df811d76db258d98d89ffb43c830cb221ff9a7d"
    assert hashlib.sha256(raw).hexdigest() == \
        "2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871"
    assert P.IMPLEMENTATION_VERSION == "F6M_NATIVE_DECISION_ADMISSION_REPAIR@1"
    dep = Path(P.__file__).with_name("pre553_empirical_objects.py")
    assert hashlib.sha1(b"blob " + str(dep.stat().st_size).encode() + b"\0" + dep.read_bytes()).hexdigest() == \
        "a61365b994e5c3c50de0f598fcf40e90abf757b6"


def test_mixed_origin_actually_executes_and_is_not_real_use():
    # The inherited F6L P5B test never reached this behaviour: it looked up a
    # nonexistent world alias.  This is the same source mutation, executed.
    world = W.mixed_origin(W.positive_2x2())
    calls = []
    def admit(source, target, phase):
        calls.append((source["source_id"], phase))
        return True
    out = run(world, admit)
    assert out["test_origin"] is False
    assert out["origin_classification"] == "MIXED_TEST_AND_UNVERIFIED"
    assert out["real_use_authorized"] is False
    assert out["real_source_qualification"] == "UNVERIFIED_INTEGRATION_BOUNDARY"
    assert "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE" not in ceilings(out)
    assert out["candidate"] is not None
    # Only the declared-real source needs admission; the test source does not.
    assert {c[0] for c in calls} == {"S1"}
    real = conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE")
    assert real["state"] == "UNAVAILABLE"
    assert real["reason"] == "UNVERIFIED_OWNER_ADMISSION"
    assert real["real_use_authorized"] is False


def test_mixed_origin_reverse_order_is_also_experimental_only():
    world = W.mixed_origin(W.positive_2x2())
    world["sources"][0]["test_origin"] = True
    world["sources"][1]["test_origin"] = False
    calls = []
    def admit(source, target, phase):
        calls.append((source["source_id"], phase))
        return True
    out = run(world, admit)
    assert out["origin_classification"] == "MIXED_TEST_AND_UNVERIFIED"
    assert out["real_use_authorized"] is False
    assert "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE" not in ceilings(out)
    assert {c[0] for c in calls} == {"S2"}
    assert conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION", use="REAL_USE")["reason"] == \
        "UNVERIFIED_OWNER_ADMISSION"


def test_null_candidate_cannot_serve_a_real_point_consumer():
    out = run(W.novel_2x2_no_positivity())
    assert out["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    assert out["candidate"]["distribution"] is None
    assert out["target_joint_status"] == "NO_COMPLETE_TARGET_JOINT"
    assert conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")["state"] == "UNAVAILABLE"
    assert conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")["reason"] == \
        "NO_COMPLETE_TARGET_JOINT"


def test_rare_exclusion_is_partial_identification_not_false_complete():
    out = run(N.rare_renormalization(150))
    assert out["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    assert out["candidate"]["distribution"] is None
    assert F(out["candidate"]["uncovered_target_mass"]) == F(1, 2)
    assert out["candidate"]["support"]["Z1"]["excluded_sources"] == ["R1"]
    assert conditional(out, {"F6L_MATERIAL3": "HIGH"}, "F6L_ACTION3")["state"] == "UNAVAILABLE"


def test_positive_complete_and_consumer_preserved():
    out = run(W.positive_2x2())
    assert out["decision"] == "SYNTHETIC_CANDIDATE"
    assert out["candidate"]["distribution"] is not None
    assert F(out["candidate"]["uncovered_target_mass"]) == 0
    c = conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")
    assert c["state"] == "SUPPORTED_MODEL"
    assert F(c["probabilities"]["YES"]) == F(1, 3)
    assert c["real_use_authorized"] is False


def test_mutated_candidate_producer_is_rejected_by_identity_guard():
    raw = Path(P.__file__).read_bytes()
    good = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    def guard(data, expected):
        b = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if b != expected:
            raise RuntimeError("PRODUCER_IDENTITY_MISMATCH")
        return b
    assert guard(raw, good) == good
    with pytest.raises(RuntimeError, match="PRODUCER_IDENTITY_MISMATCH"):
        guard(raw[:-1] + bytes([raw[-1] ^ 1]), good)
