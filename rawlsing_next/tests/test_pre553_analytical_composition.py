import inspect
import json
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_analytical_composition import (
    SLICE_PROJECTION_SCHEMA_HASH,
    compose_positioned_subject_possibility,
    _build_evidence,
)

ROOT = Path(__file__).resolve().parents[2]
R3_EVIDENCE = (
    ROOT
    / "WORKER_RETURNS"
    / "PYAT-C1-00-CONTRACT-CORRECTION-R3"
    / "04_EVIDENCE_IDENTITY_PREIMAGE.json"
)
R2_RELATION = (
    ROOT
    / "WORKER_RETURNS"
    / "PYAT-C1-00-CONTRACT-CORRECTION-R2"
    / "02_VALUE_RELATION_ORACLE.json"
)

FORWARD_EVIDENCE_HASH = "fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5"
REVERSE_EVIDENCE_HASH = "b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72"
FORWARD_QUERY_HASH = "83727ca59eaf43085324ee7dc7db5ce4ecf4e4bf1f1284692cd3ad3f192df027"
REVERSE_QUERY_HASH = "cb2d085675c137848bb40f191ba8992100513eaa904a09cd54064f6ef51d3d8a"
FORWARD_WITNESS_HASH = "c93e840c06da9ab8de9ca237863d52858fe6765d5bfd7c7efb42b879440663c9"
REVERSE_WITNESS_HASH = "e81c4e19144a749877a6f6e7e48a213e869bfe5d04ba81372ca5384b7cf5e700"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_c1_00_evidence_oracles_are_noncircular_and_exact():
    oracle = _load(R3_EVIDENCE)
    expected = oracle["expected"]

    forward = expected["forward_P1"]
    reverse = expected["reverse_yes"]

    assert "evidence_ref" not in forward["preimage"]
    assert "evidence_ref" not in reverse["preimage"]
    assert semantic_hash(forward["preimage"]) == FORWARD_EVIDENCE_HASH
    assert semantic_hash(reverse["preimage"]) == REVERSE_EVIDENCE_HASH
    assert forward["preimage"]["raw_support"] == 60
    assert reverse["preimage"]["raw_support"] == 62
    assert oracle["projection_schema_hash"] == SLICE_PROJECTION_SCHEMA_HASH


def test_c1_00_identity_spine_matches_frozen_consumer_and_witness_refs():
    spine = _load(R3_EVIDENCE)["exact_identity_spine"]

    assert spine["forward"]["consumer_query_ref"]["content_hash"] == FORWARD_QUERY_HASH
    assert spine["reverse"]["consumer_query_ref"]["content_hash"] == REVERSE_QUERY_HASH
    assert (
        spine["forward"]["condition_value_witness_ref"]["content_hash"]
        == FORWARD_WITNESS_HASH
    )
    assert (
        spine["reverse"]["condition_value_witness_ref"]["content_hash"]
        == REVERSE_WITNESS_HASH
    )


def test_composer_has_no_preconstructed_possibility_slice_input():
    sig = inspect.signature(compose_positioned_subject_possibility)
    assert "evidence" not in sig.parameters
    assert "possibility_slice_evidence" not in sig.parameters
    assert set(sig.parameters) == {
        "repository",
        "empirical_query",
        "predicate",
        "authority_registry",
        "release_refs",
        "consumer_query",
        "model_rule",
        "condition_binding_witness",
    }


def test_relation_guard_is_before_evidence_construction_and_consumer_invocation():
    source = inspect.getsource(compose_positioned_subject_possibility)
    witness_pos = source.index("_verify_witness(")
    evidence_pos = source.index("_build_evidence(")
    consumer_pos = source.index("evaluate_positioned_subject_possibility(")
    assert witness_pos < evidence_pos < consumer_pos


def test_supported_evidence_uses_raw_denominator_not_target_numerator():
    source = inspect.getsource(_build_evidence)
    assert "raw_support=fact.raw_denominator_support" in source
    assert "raw_support=fact.raw_numerator_support" not in source
    assert "float(" not in source


@pytest.mark.parametrize(
    ("side", "expected_query_hash", "expected_witness_hash"),
    (
        ("forward", FORWARD_QUERY_HASH, FORWARD_WITNESS_HASH),
        ("reverse", REVERSE_QUERY_HASH, REVERSE_WITNESS_HASH),
    ),
)
def test_frozen_c1_00_exports_identity_preimages_required_for_c1_01(
    side, expected_query_hash, expected_witness_hash
):
    """Red contract test: C1-01 cannot reconstruct/verify an opaque frozen identity.

    The accepted relation law requires recomputing the consumer query ref and then
    hashing the full ConditionValueBindingWitness material.  The R3 evidence freeze
    currently exposes only those resulting refs.  A C1-01 implementation that simply
    trusts them would violate the accepted identity law and could not prove the
    mandatory witness-mutation/reidentification hostile.
    """

    evidence = _load(R3_EVIDENCE)
    relation = _load(R2_RELATION)
    role = "forward" if side == "forward" else "reverse"
    spine = evidence["exact_identity_spine"][role]

    assert spine["consumer_query_ref"]["content_hash"] == expected_query_hash
    assert spine["condition_value_witness_ref"]["content_hash"] == expected_witness_hash

    missing = []
    if "consumer_query_material" not in spine:
        missing.append("consumer_query_material")
    if "condition_value_witness_material" not in spine:
        missing.append("condition_value_witness_material")

    # R2 freezes the witness schema and equality law, but not the two exact witness
    # instances.  Schema material cannot invert SHA-256 into the missing instances.
    assert relation["witness_schema"]["material"]["identity_algorithm"] == (
        "sha256(canonical_json(full_material))"
    )
    assert not missing, (
        "C1_01_CONTRACT_COUNTEREXAMPLE__OPAQUE_FROZEN_IDENTITY_PREIMAGE: "
        f"{side} lacks {', '.join(missing)}; cannot recompute consumer query "
        "identity and exact witness identity without weakening C1-00"
    )
