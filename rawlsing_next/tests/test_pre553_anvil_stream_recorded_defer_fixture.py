"""Canonical persisted-DEFER fixture for the q103 recorded-only entry.

The fixture is built with the same physical _Sink/_IndexSink format as
test_pre553_anvil_stream_native_i03.py. It writes a historical
SOURCE_SEMANTICS_TOPOLOGY DEFER AuthoritySnapshot and an EmpiricalUniverse that
references it at construction. No reader/index/authority monkeypatch is used.

At exact cut 851cdc0d the candidate recorded module no longer exports
HeldRecordedOperation; this test intentionally reaches that actual earliest
fault after building the canonical fixture. No product code is changed.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import struct

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalUniverse, semantic_hash
from rawlsing_next.pre553_source_direct_parquet_estate import _Sink, _IndexSink, _row
from rawlsing_next.tests import test_pre553_direct_estate_i03 as native_fixture
from rawlsing_next.tests import test_pre553_empirical_query as native
_ORIGINAL_EVENT = native.RespondentEvent


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _shaped_event(**kwargs):
    """Keep the seven source codes and explicit missing in the fixture only."""
    raw = kwargs.get("raw_response_value")
    if raw in {"None", None}:
        kwargs["raw_response_value"] = {"$raw_physical_value": {"token": {"t": "none"}}}
        kwargs["typed_state"] = "MISSING"
        kwargs["response_state"] = "MISSING"
    else:
        numeric = float(raw)
        kwargs["raw_response_value"] = {"$raw_physical_value": {"token": {
            "t": "float64_finite", "bits": struct.pack(">d", numeric).hex(),
        }}}
        if raw in {"97", "98", 97, 98}:
            kwargs["typed_state"] = "DK"
            kwargs["response_state"] = "DK"
        elif raw in {"99", 99}:
            kwargs["typed_state"] = "SUBSTANTIVE_RESPONSE"
            kwargs["response_state"] = "SUBSTANTIVE_RESPONSE"
    return _ORIGINAL_EVENT(**kwargs)


def _defer_stream(tmp_path, monkeypatch, tag="RECORDED-DEFER"):
    rows = [
        {"id": f"R{i}", "responses": {"Y": code}}
        for i, code in enumerate((1, 2, 3, 4, 97, 98, 99, None), 1)
    ]
    rows.append({"id": "R9", "responses": {}})
    holder = {}
    original_ingest = native.ingest_c11_source_release
    original_build = native._build_source
    def capture(candidate, repo):
        holder["candidate"] = candidate
        return original_ingest(candidate, repo)
    def build_with_rows(tag_arg, rows_arg, **kwargs):
        return original_build(tag_arg, rows, **kwargs)
    with monkeypatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        patch.setattr(native, "_build_source", build_with_rows)
        patch.setattr(native, "RespondentEvent", _shaped_event)
        source = native._build_source(tag, rows)
    candidate = holder["candidate"]

    # Persisted historical DEFER is part of the stream construction, not a
    # post-open mutation. The universe stores its exact authority ref.
    base_auth = source["authorities"][0]
    history_fields = dict(base_auth.semantic_fields)
    history_fields.update({
        "authority_id": "Q103-HISTORICAL-DEFER",
        "authority_version": "1.0.0",
        "authority_content_hash": semantic_hash({"q103": "historical-defer", "tag": tag}),
        "authority_kind": "SOURCE_SEMANTICS_TOPOLOGY",
        "decision_state": "DEFER",
        "governed_operations": ("Q103-OP-RECORDED-RESPONSE-ONLY",),
        "governed_object_families": ("EmpiricalUniverse@1.0.0",),
        "scope_envelope": {
            "semantic_scope": "EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY",
            "source_universe_refs": [source["universe"].ref.as_dict()],
        },
    })
    historical = AuthoritySnapshot(
        typed_state="DEFER",
        authority_snapshot_refs=base_auth.authority_snapshot_refs,
        dependency_refs=base_auth.dependency_refs,
        producer_replay_locator_or_reference_root=base_auth.producer_replay_locator_or_reference_root,
        **history_fields,
    )
    base_universe = source["universe"]
    universe_fields = dict(base_universe.semantic_fields)
    universe = EmpiricalUniverse(
        typed_state=base_universe.typed_state,
        authority_snapshot_refs=(historical.authority_ref, *base_universe.authority_snapshot_refs),
        dependency_refs=base_universe.dependency_refs,
        producer_replay_locator_or_reference_root=base_universe.producer_replay_locator_or_reference_root,
        **universe_fields,
    )
    source["universe"] = universe
    source["authorities"] = (*source["authorities"], historical)

    root = tmp_path / tag
    root.mkdir(mode=0o700)
    release = root / "releases" / ("stream-" + tag)
    release.parent.mkdir(mode=0o700)
    release.mkdir(mode=0o700)

    family_objects = {
        "AuthoritySnapshot": (*candidate.authority_snapshots, historical),
        "ComparatorReplayBinding": (),
        "DiscoveryBranchReplayBinding": (),
        "EmpiricalCoordinateFact": tuple(candidate.empirical_coordinate_facts),
        "EmpiricalPredicateReplayBinding": (),
        "EmpiricalUniverse": (universe,),
        "QuestionVariableBinding": tuple(candidate.question_variable_bindings),
        "RespondentEvent": tuple(candidate.respondent_events),
        "RespondentIdentity": tuple(candidate.respondent_identities),
        "RoutingEligibilityFact": tuple(candidate.routing_eligibility_facts_or_exact_rules),
        "SourceUniverseRelation": (),
        "StructuralAdmissionReplayBinding": (),
        "WeightMeasureFact": (),
    }
    locator = _IndexSink(release / "event_locator.parquet", 2)
    for family, objects in family_objects.items():
        sink = _Sink(release / (family + ".parquet"), family, 2)
        for obj in objects:
            gid, offset = sink.add(obj)
            if family == "RespondentEvent":
                locator.add(_row(family, obj), gid, offset)
        sink.close()
    locator.close()

    source_sha = sha256(("source-" + tag).encode()).hexdigest()
    roots = {
        "logical": sha256(("logical-" + tag).encode()).hexdigest(),
        "physical": sha256(("physical-" + tag).encode()).hexdigest(),
        "release": "C11_STREAM_SOURCEFREE_RELEASE|" + tag + "|" + sha256(("release-" + tag).encode()).hexdigest(),
        "source": "SOURCE_ARTIFACT|sourcefree|" + source_sha,
        "replay": sha256(("replay-" + tag).encode()).hexdigest(),
        "universe": universe.ref.key,
        "schema": "ANVIL_STREAM_C11_ESTATE@1",
    }
    manifest_doc = {
        "schema": "ANVIL_STREAM_C11_ESTATE@1",
        "body_format": "legacy_exact_object_row_json_in_same_parquet_member",
        "proof_version": "STREAM_TYPED_IDENTITY_COVERAGE@1",
        "read_back_audit": False,
        "sqlite_proof_built": False,
        "legacy_i02": None,
        "manifest_sha256": "a" * 64,
        "roots": roots,
        "family_counts": {k: len(v) for k, v in family_objects.items()},
        "event_locator_count": len(family_objects["RespondentEvent"]),
        "members": {p.name: _digest(p) for p in release.glob("*.parquet")},
    }
    manifest = release / "manifest.json"
    manifest.write_text(json.dumps(manifest_doc, sort_keys=True), encoding="utf-8")
    manifest.chmod(0o600)
    held = HeldStreamPins(
        source_id="SRC04", source_sha256=source_sha,
        manifest_sha256=_digest(manifest), exact_release_path=str(release),
        roots=roots,
    )
    return source, candidate, root, release, held, historical, universe


def test_persisted_defer_recorded_entry_reaches_actual_earliest_fault(tmp_path, monkeypatch):
    source, candidate, root, release, held, historical, universe = _defer_stream(
        tmp_path, monkeypatch,
    )
    # Canonical fixture is persisted before the product import.
    assert historical.decision_state == "DEFER"
    assert historical.authority_ref in universe.authority_snapshot_refs
    assert (release / "manifest.json").exists()
    # Actual cut 851c has no HeldRecordedOperation class. This import is the
    # exact earliest product fault after canonical fixture construction.
    from rawlsing_next.pre553_anvil_stream_recorded import HeldRecordedOperation  # noqa: F401
