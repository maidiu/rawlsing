from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

import pytest

import rawlsing_next.pre553_repo_native_current_payload as current
import rawlsing_next.pre553_repo_native_seal as seal
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
    semantic_hash,
)


@pytest.fixture(scope="module")
def actual_current_objects():
    return seal.load_current_gt2_query_fact()


def _transport_bytes():
    return current._read_committed_transport()


def test_fixed_manifest_and_all_binary_payload_commitments_are_exact():
    manifest_bytes, payloads = _transport_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest() == current._MANIFEST_SHA256
    assert set(payloads) == set(current._BINARY_SPECS)
    for name, spec in current._BINARY_SPECS.items():
        raw = payloads[name]
        assert len(raw) == spec["bytes"]
        assert len(raw) // 32 == spec["count"]
        assert hashlib.sha256(raw).hexdigest() == spec["sha256"]


def test_binary_hash_closures_reconstruct_exact_canonical_refs():
    _, payloads = _transport_bytes()
    for name, spec in current._BINARY_SPECS.items():
        refs = current._decode_exact_ref_hashes(name, payloads[name])
        assert len(refs) == spec["count"]
        assert len(refs) == len(set(refs))
        assert refs == tuple(sorted(refs, key=lambda ref: ref.key))
        for ref in (refs[0], refs[-1]):
            assert ref.kind == spec["kind"]
            assert ref.object_id == spec["object_id_template"].format(hash=ref.content_hash)


def test_no_argument_current_loader_returns_ordinary_exact_current_objects(actual_current_objects):
    query, fact = actual_current_objects
    assert type(query) is EmpiricalQuerySpec
    assert type(fact) is EmpiricalFact
    assert query.content_hash == current.CURRENT_QUERY_HASH
    assert fact.content_hash == current.CURRENT_FACT_HASH
    assert semantic_hash(query.semantic_projection()) == current.CURRENT_QUERY_HASH
    assert semantic_hash(fact.semantic_projection()) == current.CURRENT_FACT_HASH

    predicate = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    replay = exact_ref(fact.replay_ref, "fact.replay_ref")
    assert predicate.content_hash == current.CURRENT_PREDICATE_HASH
    assert replay.content_hash == current.CURRENT_REPLAY_HASH
    assert exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref") == query.ref
    assert exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref") == predicate

    assert fact.raw_denominator_support == 19_210
    assert len(fact.risk_set_member_refs) == 19_210
    assert len(fact.denominator_member_refs) == 19_210
    assert fact.risk_set_member_refs == fact.denominator_member_refs
    assert len(fact.source_empirical_provenance_refs) == 76_843
    assert len(fact.dependency_refs) == 76_846


def test_exact_provenance_and_dependency_closures_are_reconstructed(actual_current_objects):
    query, fact = actual_current_objects
    provenance = tuple(
        exact_ref(ref, "fact.source_empirical_provenance_refs")
        for ref in fact.source_empirical_provenance_refs
    )
    dependencies = tuple(fact.dependency_refs)
    predicate = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    replay = exact_ref(fact.replay_ref, "fact.replay_ref")

    assert len(provenance) == 76_843
    assert len(set(provenance)) == 76_843
    assert dependencies == tuple(sorted(set(dependencies), key=lambda ref: ref.key))
    assert {query.ref, predicate, replay, *provenance} == set(dependencies)


def test_manifest_tamper_fails_before_rehydration():
    manifest_bytes, payloads = _transport_bytes()
    tampered = bytearray(manifest_bytes)
    tampered[-2] ^= 1
    with pytest.raises(current.CurrentGT2RehydrationError, match="manifest sha256"):
        current._rehydrate_verified_transport(bytes(tampered), payloads)


@pytest.mark.parametrize("name", ["respondent_refs", "routing_refs", "event_refs"])
def test_any_binary_payload_tamper_fails(name):
    manifest_bytes, payloads = _transport_bytes()
    damaged = dict(payloads)
    raw = bytearray(damaged[name])
    raw[len(raw) // 2] ^= 1
    damaged[name] = bytes(raw)
    with pytest.raises(current.CurrentGT2RehydrationError, match="payload sha256"):
        current._rehydrate_verified_transport(manifest_bytes, damaged)


@pytest.mark.parametrize("mode", ["truncate", "extra"])
def test_truncated_or_extra_payload_fails_exact_byte_count(mode):
    manifest_bytes, payloads = _transport_bytes()
    damaged = dict(payloads)
    raw = damaged["respondent_refs"]
    damaged["respondent_refs"] = raw[:-1] if mode == "truncate" else raw + b"\x00"
    with pytest.raises(current.CurrentGT2RehydrationError, match="byte count"):
        current._rehydrate_verified_transport(manifest_bytes, damaged)


def test_wrong_manifest_ref_count_fails_reconstruction_law():
    manifest_bytes, _ = _transport_bytes()
    manifest = json.loads(manifest_bytes)
    manifest["closure_rehydration"]["respondent_refs"]["count"] += 1
    with pytest.raises(current.CurrentGT2RehydrationError, match="metadata drift"):
        current._verify_binary_manifest(manifest)


def test_wrong_fixed_identity_and_historical_a3_cannot_impersonate_current():
    manifest_bytes, _ = _transport_bytes()
    manifest = json.loads(manifest_bytes)

    wrong = json.loads(json.dumps(manifest))
    wrong["identity"]["query"] = "0" * 64
    with pytest.raises(current.CurrentGT2RehydrationError, match="fixed current"):
        current._require_manifest_identity(wrong)

    historical = json.loads(json.dumps(manifest))
    historical["identity"]["query"] = current._HISTORICAL_A3_QUERY_HASH
    historical["identity"]["fact"] = current._HISTORICAL_A3_FACT_HASH
    historical["identity"]["replay"] = current._HISTORICAL_A3_REPLAY_HASH
    with pytest.raises(current.CurrentGT2RehydrationError, match="historical A3"):
        current._require_manifest_identity(historical)


def test_current_entrypoints_expose_no_path_authority_permission_or_identity_selector():
    for fn in (
        seal.load_current_gt2_query_fact,
        current.load_current_gt2_query_fact_from_committed_transport,
    ):
        assert not inspect.signature(fn).parameters

    for forbidden in (
        "path",
        "root",
        "authority",
        "permission",
        "identity",
        "query_hash",
        "fact_hash",
        "replay_hash",
        "predicate_hash",
    ):
        assert forbidden not in inspect.signature(seal.load_current_gt2_query_fact).parameters


def test_runtime_reads_only_four_fixed_repo_transport_resources(monkeypatch):
    real_read_bytes = Path.read_bytes
    seen: list[str] = []
    allowed = {
        "02_CONSTRUCTOR_COMPLETE_MANIFEST.json",
        "payload/respondent_ref_hashes.bin",
        "payload/routing_ref_hashes.bin",
        "payload/event_ref_hashes.bin",
    }

    def guarded_read_bytes(path: Path) -> bytes:
        rendered = path.as_posix()
        seen.append(rendered)
        assert "Library" not in rendered
        assert ".sav" not in rendered
        assert "source_rows" not in rendered
        assert "carrier" not in rendered.lower()
        assert any(rendered.endswith(suffix) for suffix in allowed)
        return real_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", guarded_read_bytes)
    query, fact = current.load_current_gt2_query_fact_from_committed_transport()
    assert query.content_hash == current.CURRENT_QUERY_HASH
    assert fact.content_hash == current.CURRENT_FACT_HASH
    assert len(seen) == 4
    assert {next(suffix for suffix in allowed if item.endswith(suffix)) for item in seen} == allowed


def test_binary_payload_set_is_fixed_and_missing_member_fails():
    manifest_bytes, payloads = _transport_bytes()
    missing = dict(payloads)
    missing.pop("event_refs")
    with pytest.raises(current.CurrentGT2RehydrationError, match="payload set"):
        current._rehydrate_verified_transport(manifest_bytes, missing)


def test_o1_current_gt2_and_q86_identity_pins_remain_exact(actual_current_objects):
    query, fact = actual_current_objects
    assert current.CURRENT_PREDICATE_HASH == (
        "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3"
    )
    assert current.CURRENT_QUERY_HASH == (
        "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
    )
    assert current.CURRENT_FACT_HASH == (
        "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
    )
    assert current.CURRENT_REPLAY_HASH == (
        "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"
    )
    assert query.content_hash == current.CURRENT_QUERY_HASH
    assert fact.content_hash == current.CURRENT_FACT_HASH
    assert semantic_hash(query.semantic_projection()) == current.CURRENT_QUERY_HASH
    assert semantic_hash(fact.semantic_projection()) == current.CURRENT_FACT_HASH

    manifest_bytes, _ = _transport_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    assert manifest["release"]["ref"] == {
        "kind": "C11LogicalRelease",
        "object_id": "R5_GT12_Q86A_Q86B_FROZEN",
        "content_hash": "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295",
    }
    assert manifest["release"]["replay_manifest_ref"]["content_hash"] == (
        "c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa"
    )
