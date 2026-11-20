"""No source rows: hostile stream-schema metadata/pin/current qualification.

These tests do NOT prove stream physical member geometry or native I03 admission.
"""
from dataclasses import replace
from hashlib import sha256
import json

import pytest

from rawlsing_next.pre553_anvil_stream_carrier_qualification import (
    HeldStreamPins,
    StreamCarrierQualificationError,
    qualify_saved_stream_manifest,
)

SOURCE = "a" * 64
ROOTS = {
    "logical": "b" * 64,
    "physical": "c" * 64,
    "release": "C11_STREAM_SOURCEFREE_RELEASE|test-only|" + "d" * 64,
    "source": "SOURCE_ARTIFACT|synthetic fixture|" + SOURCE,
    "replay": "TEST_REPLAY|" + "e" * 64,
    "universe": "TEST_UNIVERSE|" + "f" * 64,
    "schema": "ANVIL_STREAM_C11_ESTATE@1",
}
FAMILIES = (
    "AuthoritySnapshot", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "EmpiricalCoordinateFact",
    "EmpiricalPredicateReplayBinding", "EmpiricalUniverse",
    "QuestionVariableBinding", "RespondentEvent", "RespondentIdentity",
    "RoutingEligibilityFact", "SourceUniverseRelation",
    "StructuralAdmissionReplayBinding", "WeightMeasureFact",
)


def _estate(tmp_path):
    root = tmp_path / "private"
    release = root / "release"
    root.mkdir(mode=0o700)
    release.mkdir(mode=0o700)
    doc = {
        "schema": "ANVIL_STREAM_C11_ESTATE@1",
        "i02": ROOTS,
        "source_sha256": SOURCE,
        "family_counts": {name: 0 for name in FAMILIES},
    }
    manifest = release / "manifest.json"
    manifest.write_text(json.dumps(doc, sort_keys=True), encoding="utf-8")
    manifest.chmod(0o600)
    pins = HeldStreamPins(
        source_id="SRC04", source_sha256=SOURCE,
        manifest_sha256=sha256(manifest.read_bytes()).hexdigest(),
        exact_release_path=str(release),
        roots=dict(ROOTS),
    )
    return root, release, manifest, pins


def test_exact_stream_schema_preflights_metadata_but_never_mints_native_reader(tmp_path):
    root, release, _, pins = _estate(tmp_path)
    calls = []
    def current(held):
        calls.append(held)
        return True
    receipt = qualify_saved_stream_manifest(
        root=root, exact_release_path=release,
        held=pins, current_authorizer=current,
    )
    assert receipt.schema == "ANVIL_STREAM_C11_ESTATE@1"
    assert receipt.source_id == "SRC04"
    assert receipt.manifest_sha256 == pins.manifest_sha256
    assert len(receipt.family_counts) == 13
    assert receipt.native_i03_admitted is False
    assert len(calls) == 2
    # Changing the original mutable roots dict cannot change pinned identity.
    with pytest.raises(TypeError):
        pins.roots["logical"] = "0" * 64


@pytest.mark.parametrize("replacement", [
    {"schema": "PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1"},
    {"logical": "0" * 64},
    {"release": "C11_STREAM_SOURCEFREE_RELEASE|wrong|" + "d" * 64},
    {"source": "SOURCE_ARTIFACT|different|" + SOURCE},
    {"replay": "TEST_REPLAY|other"},
    {"universe": "TEST_UNIVERSE|other"},
])
def test_false_schema_or_source_root_cannot_pass_held_stream_admission(
    tmp_path, replacement,
):
    root, release, _, pins = _estate(tmp_path)
    if replacement.get("schema") == "PYAT_S2B_DIRECT_SOURCEFREE_CANDIDATE_CERT@1":
        # Refuse while constructing the exact held-stream type itself.
        with pytest.raises(StreamCarrierQualificationError, match="stream schema"):
            replace(pins, roots={**ROOTS, **replacement})
        return
    bad = replace(pins, roots={**ROOTS, **replacement})
    with pytest.raises(StreamCarrierQualificationError, match="roots mismatch"):
        qualify_saved_stream_manifest(
            root=root, exact_release_path=release,
            held=bad, current_authorizer=lambda _: True,
        )


def test_mutated_manifest_refuses_even_if_its_new_json_is_self_consistent(tmp_path):
    root, release, manifest, pins = _estate(tmp_path)
    doc = json.loads(manifest.read_text())
    doc["family_counts"]["RespondentEvent"] = 1
    manifest.write_text(json.dumps(doc, sort_keys=True))
    with pytest.raises(StreamCarrierQualificationError, match="independent SHA-256"):
        qualify_saved_stream_manifest(
            root=root, exact_release_path=release,
            held=pins, current_authorizer=lambda _: True,
        )


@pytest.mark.parametrize("revoke_after", [0, 1])
def test_current_revocation_refuses_before_or_after_manifest_read(
    tmp_path, revoke_after,
):
    root, release, _, pins = _estate(tmp_path)
    calls = [0]
    def current(_pins):
        calls[0] += 1
        return calls[0] <= revoke_after
    with pytest.raises(StreamCarrierQualificationError, match="authority"):
        qualify_saved_stream_manifest(
            root=root, exact_release_path=release,
            held=pins, current_authorizer=current,
        )


def test_wrong_source_identity_or_source_scope_refuses_without_manifest_read(tmp_path):
    root, release, _, pins = _estate(tmp_path)
    with pytest.raises(StreamCarrierQualificationError, match="two explicitly selected"):
        replace(pins, source_id="SRC17")
    with pytest.raises(StreamCarrierQualificationError, match="source artifact"):
        replace(pins, source_sha256="9" * 64)
    with pytest.raises(StreamCarrierQualificationError, match="independently held release path"):
        qualify_saved_stream_manifest(
            root=root, exact_release_path=tmp_path / "another_release",
            held=pins, current_authorizer=lambda _: True,
        )


@pytest.mark.parametrize("source_id", ["SRC04", "SRC16"])
def test_r2_exact_saved_roots_remain_stream_not_direct_certificate(source_id):
    """The real worker's saved stream commitments cannot be relabeled direct."""
    from pathlib import Path
    from rawlsing_next._pre553_external_i02_certificate import (
        ExternalI02IntegrityError, ExternalI02Roots,
    )
    project = Path(__file__).resolve().parents[2]
    path = (project / "WORKER_RETURNS" /
            "ANVIL_P0_TWO_SAVED_WAVES_20261120" / "R2" /
            "R2_TYPED_DECISION_AND_REFUSALS.json")
    evidence = json.loads(path.read_text(encoding="utf-8"))
    wave = evidence["waves"][source_id]
    assert wave["currentness"] == "CURRENT_GRANTED"
    assert wave["saved_i02"]["schema"] == "ANVIL_STREAM_C11_ESTATE@1"
    assert wave["source_sha256"] == wave["saved_i02"]["source"].rsplit("|", 1)[1]
    assert wave["manifest_sha256"] and len(wave["manifest_sha256"]) == 64
    with pytest.raises(ExternalI02IntegrityError, match="unsupported externally held certificate schema"):
        ExternalI02Roots(**wave["saved_i02"])
