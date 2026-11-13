"""Q2 S1-E — actual native I03/Batch fact from a sourcefree Q2 config.

The fixture is engineering/sourcefree only: R157-shaped nonrespondent SAV bytes,
a TEST_ONLY query/predicate authority, and an engineering correction of two
fixture omissions (routing authority kind and canonical value spelling).  It is
not original35 science or a production CURRENT permission.

On Linux the existing VerifiedExternalI02 -> install_direct_sourcefree_i02_i03
native selector path consumes the Q2 certificate and executes the existing
native empirical query.  On non-Linux hosts the cold reader capability is an
explicit HOLD; no monkeypatched Darwin cold path is claimed.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path

import pytest

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
    decode_fixture_config,
)
from rawlsing_next.pre553_source_i02_handoff import open_direct_native_i03
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _query,
    _query_authority,
    _run,
)


def _native_document(document):
    """Correct only sourcefree fixture omissions; no scientific widening."""
    doc = deepcopy(document)
    for snapshot in doc["authority"]["snapshots"]:
        if snapshot["authority_id"] == "S1B-ROUTING-AUTH":
            snapshot["authority_kind"] = "ROUTING_RISK_SET"
    for slot in doc["response_slots"]:
        for value in slot["values"]:
            if value.get("raw_value") in (0.0, 1.0):
                value["canonical_value"] = str(int(value["raw_value"]))
    return doc


def _native_source(fixture, config):
    projection = build_governed_c11_projection(config)
    return {
        "universe": projection.universes[0],
        "respondents": {row.ref.key: row for row in projection.respondents},
        "qrefs": {"q101": projection.questions[0].native_question_ref},
        "risk_refs": {"R": projection.routing[0].risk_set_ref},
        "authorities": projection.authority_snapshots,
        "source_auth": projection.authority_snapshots[0],
        "repo": None,
        "release_ref": None,
        "projection": projection,
    }


def _build_native(tmp_path: Path, fixture, document, name: str):
    config = SourceConfig(document)
    handoff = build(tmp_path, fixture, name=name, config=config)
    incidence = decode_fixture_config(config, fixture["path"])
    try:
        legacy = build_validated_c11_release_from_config(
            config, incidence=incidence, batch_size=4)
    finally:
        incidence.close()
    source = _native_source(fixture, config)
    source["repo"] = C11Repository((legacy,))
    source["release_ref"] = legacy.release_ref
    return handoff, legacy, source


def _native_fact(tmp_path: Path, fixture, document, name: str, *, members=None):
    handoff, legacy, source = _build_native(tmp_path, fixture, document, name)
    tag = "q2-native"
    authority = _query_authority(tag)
    predicate = _branch_predicate(
        source, authority, members=members, tag=tag)
    query = _query(
        source, authority, predicate, ("q101",), tag=tag,
        target_authority_refs=(source["projection"].questions[0].semantic_authority_ref,),
    )
    reader = open_direct_native_i03(handoff, source["repo"], legacy.release_ref)
    try:
        result = _run(source, authority, predicate, query)
    finally:
        reader.close()
    assert len(result.facts) == 1
    return result.facts[0], handoff


@pytest.mark.skipif(
    not os.path.isdir("/proc/self/fd"),
    reason="existing VerifiedExternalI02 cold reader requires Linux /proc/self/fd",
)
def test_s1e_native_i03_batch_fact_supported_changed_restore(tmp_path):
    fixture = source_fixture(
        tmp_path / "native", values=(0.0, 1.0, 0.0, 1.0, 0.0))
    original_document = _native_document(fixture["document"])
    base_fact, base_handoff = _native_fact(
        tmp_path / "native", fixture, original_document, "base.sqlite")
    assert base_fact.typed_state == "SUPPORTED"
    assert base_fact.semantic_fields.get("p02_failure_state") is None
    base_raw = (
        base_fact.semantic_fields["raw_numerator_support"],
        base_fact.semantic_fields["raw_denominator_support"],
    )
    assert base_raw == (5, 5)
    assert base_handoff.roots.logical

    # Changed valid operation: a strict same-source branch subset changes the
    # conservative native fact without changing the source body or authority.
    source_rows = tuple(sorted(
        (row for row in build_governed_c11_projection(
            SourceConfig(original_document)).respondents),
        key=lambda row: row.respondent_key,
    ))
    changed_fact, _ = _native_fact(
        tmp_path / "native", fixture, deepcopy(original_document),
        "changed.sqlite", members=source_rows[:3])
    assert changed_fact.typed_state == "SUPPORTED"
    changed_raw = (
        changed_fact.semantic_fields["raw_numerator_support"],
        changed_fact.semantic_fields["raw_denominator_support"],
    )
    assert changed_raw != base_raw or changed_fact.ref != base_fact.ref

    restored_fact, restored_handoff = _native_fact(
        tmp_path / "native", fixture, deepcopy(original_document), "restored.sqlite")
    assert restored_fact.ref == base_fact.ref
    assert (
        restored_fact.semantic_fields["raw_numerator_support"],
        restored_fact.semantic_fields["raw_denominator_support"],
    ) == base_raw
    assert restored_handoff.roots.logical == base_handoff.roots.logical

    # The fixture correction is an authority-kind/canonical-spelling repair,
    # not a new scientific issuer: the same existing query owner now resolves.
    assert base_fact.semantic_fields["execution_detail"] == (
        "exact governed target distribution resolved")
