from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "WORKER_RETURNS" / "EE-P2R6K"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def body_sha(body) -> str:
    data = (json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    return hashlib.sha256(data).hexdigest()


@pytest.fixture()
def surfaces():
    codec = load_module("ee_p2r6k_codec_test", OUT / "02_C11_VALIDATED_SNAPSHOT_CODEC.py")
    rehydrator = load_module("ee_p2r6k_rehydrator_test", OUT / "04_SNAPSHOT_REHYDRATOR.py")
    materializer = load_module("ee_p2r6k_materializer_test", OUT / "03_LOCAL_SNAPSHOT_MATERIALIZER.py")
    fixture_module = load_module(
        "ee_p2r6k_repo_native_fixture",
        ROOT / "rawlsing_next" / "tests" / "test_pre553_c11_repository_ingest.py",
    )
    from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
    candidate = fixture_module._candidate("ee-p2r6k", event_order=("e1",))
    release = validate_c11_source_release(candidate)
    data = codec.serialize_snapshot_bytes(candidate, release)
    snapshot = codec.parse_snapshot_bytes(data)
    return codec, rehydrator, materializer, candidate, release, data, snapshot


def test_roundtrip_uses_public_validation_and_exact_repository_resolution(surfaces):
    codec, rehydrator, _, candidate, release, data, snapshot = surfaces
    restored_candidate = codec.candidate_from_snapshot(snapshot)
    restored, repository, receipt = rehydrator.rehydrate_snapshot_bytes(data)

    assert restored.release_ref == release.release_ref
    assert restored.semantic_release_hash == release.semantic_release_hash
    assert restored.replay_manifest.ref == release.replay_manifest.ref
    assert restored.source_release_manifest_hash == candidate.source_release_manifest.content_hash
    assert restored.replay_manifest.semantic_projection_hash == candidate.candidate_replay_manifest.semantic_projection_hash
    assert {key: list(value) for key, value in restored.m01_m18_coverage.items()} == snapshot["validated_release_identity"]["m01_m18_coverage"]
    assert repository.resolve_release_exact(release.release_ref).release_ref == release.release_ref
    assert repository.snapshot_identity() == snapshot["validated_release_identity"]["repository_snapshot_identity"]
    assert receipt["repository"]["resolve_release_exact"] == "PASS"
    assert receipt["validation_path"] == [
        "SERIALIZED_CANONICAL_CANDIDATE_BODIES",
        "C11SourceReleaseCandidate",
        "validate_c11_source_release",
        "C11LogicalRelease",
        "C11Repository",
        "resolve_release_exact",
    ]
    assert restored_candidate.candidate_replay_manifest.ref == candidate.candidate_replay_manifest.ref


def test_mutated_public_body_fails_exact_identity_recomputation(surfaces):
    codec, rehydrator, *_rest, snapshot = surfaces
    mutated = copy.deepcopy(snapshot)
    wrapper = mutated["sections"]["respondent_events"]["records"][0]
    wrapper["canonical_body"]["semantic_fields"]["raw_response_value"] = "MUTATED"
    wrapper["canonical_body_sha256"] = body_sha(wrapper["canonical_body"])
    with pytest.raises(Exception):
        rehydrator.rehydrate_snapshot_bytes(codec.canonical_snapshot_bytes(mutated))


def test_omitted_body_fails_without_default_or_inference(surfaces):
    codec, rehydrator, *_rest, snapshot = surfaces
    omitted = copy.deepcopy(snapshot)
    omitted["sections"]["respondent_events"]["records"].pop()
    omitted["identity_summary"]["record_counts"]["RespondentEvent"] = 0
    with pytest.raises(Exception):
        rehydrator.rehydrate_snapshot_bytes(codec.canonical_snapshot_bytes(omitted))


def test_changed_typed_absence_fails_public_section_law(surfaces):
    codec, rehydrator, *_rest, snapshot = surfaces
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    changed = copy.deepcopy(snapshot)
    value = changed["sections"]["weight_measure_facts_or_typed_absence"]["value"]
    value["canonical_body"]["typed_absence_state"] = "DEFERRED"
    value["semantic_body_hash"] = semantic_hash(value["canonical_body"])
    with pytest.raises(Exception):
        rehydrator.rehydrate_snapshot_bytes(codec.canonical_snapshot_bytes(changed))


def test_changed_replay_body_fails_exact_replay_identity(surfaces):
    codec, rehydrator, *_rest, snapshot = surfaces
    changed = copy.deepcopy(snapshot)
    wrapper = changed["candidate_replay_manifest"]
    wrapper["canonical_body"]["semantic_fields"]["replay_protocol_version"] = "MUTATED"
    wrapper["canonical_body_sha256"] = body_sha(wrapper["canonical_body"])
    with pytest.raises(Exception):
        rehydrator.rehydrate_snapshot_bytes(codec.canonical_snapshot_bytes(changed))


def test_static_authority_shortcuts_absent_and_local_transport_deterministic(surfaces):
    _, _, materializer, *_ = surfaces
    forbidden = ("_" + "make_" + "validated_release", "_" + "C11_" + "VALIDATION_SEAL")
    for filename in (
        "02_C11_VALIDATED_SNAPSHOT_CODEC.py",
        "03_LOCAL_SNAPSHOT_MATERIALIZER.py",
        "04_SNAPSHOT_REHYDRATOR.py",
    ):
        source = (OUT / filename).read_text(encoding="utf-8")
        assert all(token not in source for token in forbidden)

    blobs = materializer.verify_vendored_r5b()
    assert blobs["SUPPORT/R5B/03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py"] == materializer.R5B_DRIVER_BLOB
    compressed_a = materializer.deterministic_gzip(b"tiny-browser-fixture\n")
    compressed_b = materializer.deterministic_gzip(b"tiny-browser-fixture\n")
    assert compressed_a == compressed_b
    assert gzip.decompress(compressed_a) == b"tiny-browser-fixture\n"

    packet = json.loads((OUT / "05_LOCAL_EXECUTION_PACKET.json").read_text(encoding="utf-8"))
    assert packet["execution_surface"] == "LOCAL-MACHINE CODEX"
    assert packet["maximum_intelligence"] == "LUNA"
    assert packet["library_access"] == "EXACT_ONLY"
    assert packet["authorized_source"]["sha256"] == materializer.SOURCE_SHA256
    assert packet["browser_qualification"]["source_or_carrier_access"] is False
    assert packet["forbidden"]["binding_activation_or_adoption"] is True
