"""P0 sourcefree ANVIL stream -> ORIGINAL native I03 first-reader court.

The 14 test Parquets are emitted only from an already existing tiny,
nonrespondent sourcefree native C11 candidate. No S2B direct certificate is
fabricated; the test models a genuine ANVIL stream manifest and independently
holds its distinct roots. No original SRC04/SRC16 bytes are used.
"""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_anvil_stream_carrier_qualification import (
    HeldStreamPins, StreamCarrierQualificationError,
)
from rawlsing_next.pre553_anvil_stream_native_i03 import (
    VerifiedAnvilStreamEstate, execute_anvil_stream_i03,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_source_direct_parquet_estate import (
    _Sink, _IndexSink, _row, DirectEstateError,
)
from rawlsing_next.tests import test_pre553_direct_estate_i03 as native_fixture
from rawlsing_next.tests import test_pre553_empirical_query as native


def _digest(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def _stream(tmp_path, monkeypatch, tag="STREAM-READER", *, source_id="SRC04", grant=None):
    source, candidate = native_fixture._source_with_candidate(
        monkeypatch, tag, 1
    )
    auth = native._query_authority(tag)
    predicate = native._branch_predicate(source, auth)
    query = native._query(source, auth, predicate, ("Y",), tag=tag)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], auth)),
        predicates=(predicate,), queries=(query,), discovery_authorities=(),
    )
    root = tmp_path / tag
    root.mkdir(mode=0o700)
    release = root / "releases" / ("stream-" + tag)
    release.parent.mkdir(mode=0o700)
    release.mkdir(mode=0o700)

    from rawlsing_next.pre553_c11_integrity import TypedAbsence

    def actual(section):
        return () if type(section) is TypedAbsence else tuple(section)

    family_objects = {
        "AuthoritySnapshot": candidate.authority_snapshots,
        "ComparatorReplayBinding": actual(
            candidate.comparator_replay_bindings_or_typed_deferred_state
        ),
        "DiscoveryBranchReplayBinding": actual(
            candidate.discovery_branch_replay_bindings_or_typed_deferred_state
        ),
        "EmpiricalCoordinateFact": candidate.empirical_coordinate_facts,
        "EmpiricalPredicateReplayBinding": actual(
            candidate.predicate_replay_bindings_when_retained_objects_require_them
        ),
        "EmpiricalUniverse": candidate.empirical_universes,
        "QuestionVariableBinding": candidate.question_variable_bindings,
        "RespondentEvent": candidate.respondent_events,
        "RespondentIdentity": candidate.respondent_identities,
        "RoutingEligibilityFact": candidate.routing_eligibility_facts_or_exact_rules,
        "SourceUniverseRelation": actual(
            candidate.source_universe_relations_or_explicit_distinct_default
        ),
        "StructuralAdmissionReplayBinding": actual(
            candidate.structural_admission_replay_bindings_or_typed_not_applicable_state
        ),
        "WeightMeasureFact": actual(
            candidate.weight_measure_facts_or_typed_absence
        ),
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
        "release": ("C11_STREAM_SOURCEFREE_RELEASE|" + tag + "|"
                    + sha256(("release-" + tag).encode()).hexdigest()),
        "source": "SOURCE_ARTIFACT|sourcefree|" + source_sha,
        "replay": sha256(("replay-" + tag).encode()).hexdigest(),
        "universe": source["universe"].ref.key,
        "schema": "ANVIL_STREAM_C11_ESTATE@1",
    }
    m = {
        "schema": "ANVIL_STREAM_C11_ESTATE@1",
        "body_format": "legacy_exact_object_row_json_in_same_parquet_member",
        "proof_version": "STREAM_TYPED_IDENTITY_COVERAGE@1",
        "read_back_audit": False,
        "sqlite_proof_built": False,
        "legacy_i02": None,
        "manifest_sha256": "a" * 64,  # embedded proof marker, not file digest
        "roots": roots,
        "family_counts": {k: len(v) for k, v in family_objects.items()},
        "event_locator_count": len(candidate.respondent_events),
        "members": {
            p.name: _digest(p) for p in release.glob("*.parquet")
        },
    }
    manifest = release / "manifest.json"
    manifest.write_text(json.dumps(m, sort_keys=True), encoding="utf-8")
    manifest.chmod(0o600)
    held = HeldStreamPins(
        source_id=source_id, source_sha256=source_sha,
        manifest_sha256=_digest(manifest), exact_release_path=str(release),
        roots=roots,
    )
    if grant is None:
        grant = lambda _: True
    return (source, auth, predicate, query, catalog, root, release,
            manifest, held, grant)


@pytest.mark.parametrize("source_id", ["SRC04", "SRC16"])
def test_actual_native_i03_consumes_verified_stream_without_historical_v1(
    tmp_path, monkeypatch, source_id,
):
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(
         tmp_path, monkeypatch, "ST-NATIVE-" + source_id, source_id=source_id,
     )
    oracle = native._run(source, auth, predicate, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"
    estate = VerifiedAnvilStreamEstate(
        root, exact_path=release, independently_held=held,
        current_authorizer=grant,
    )
    result = execute_anvil_stream_i03(
        estate=estate, runtime_catalog=catalog,
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    assert result.query_ref == oracle.query_ref
    assert result.facts[0].typed_state == oracle.facts[0].typed_state
    assert result.facts[0].target_topology == oracle.facts[0].target_topology
    assert result.release_refs == (estate.native_release_ref,)
    assert result.release_refs != oracle.release_refs
    assert estate.native_replay_ref.kind == "ANVILStreamReplayRoot@1"
    assert estate.native_replay_ref.content_hash == held.roots["replay"]
    with pytest.raises(TypeError):
        estate.manifest["members"]["RespondentEvent.parquet"] = "0" * 64
    with pytest.raises(DirectEstateError, match="immutable"):
        estate.native_release_ref = source["release_ref"]
    assert not list(root.glob(".s2c-native-i03-*"))
    assert not list(release.glob("*.sqlite"))


def test_native_stream_refuses_altered_member_before_query(tmp_path, monkeypatch):
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(tmp_path, monkeypatch, "ST-MEMBER")
    with (release / "RespondentEvent.parquet").open("ab") as handle:
        handle.write(b"POISON")
    with pytest.raises(DirectEstateError, match="member differs"):
        VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=held,
            current_authorizer=grant,
        )


def test_native_stream_refuses_foreign_root_even_if_manifest_self_consistent(
    tmp_path, monkeypatch,
):
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(tmp_path, monkeypatch, "ST-ROOT")
    from dataclasses import replace
    bad = replace(held, roots={**dict(held.roots), "universe": (
        "EmpiricalUniverse@1.0.0|foreign|" + "c" * 64
    )})
    with pytest.raises(StreamCarrierQualificationError, match="roots mismatch"):
        VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=bad,
            current_authorizer=grant,
        )


def test_native_stream_revoked_before_and_after_admission(tmp_path, monkeypatch):
    allowed = {"yes": True}
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(
         tmp_path, monkeypatch, "ST-REVOKE",
         grant=lambda _: allowed["yes"],
     )
    allowed["yes"] = False
    with pytest.raises(StreamCarrierQualificationError, match="authority"):
        VerifiedAnvilStreamEstate(
            root, exact_path=release, independently_held=held,
            current_authorizer=grant,
        )
    allowed["yes"] = True
    estate = VerifiedAnvilStreamEstate(
        root, exact_path=release, independently_held=held,
        current_authorizer=grant,
    )
    allowed["yes"] = False
    with pytest.raises(DirectEstateError, match="authority refused"):
        execute_anvil_stream_i03(
            estate=estate, runtime_catalog=catalog,
            query_ref=query.ref, predicate_ref=predicate.ref,
        )


def test_native_stream_wrong_issued_query_cannot_be_substituted(
    tmp_path, monkeypatch,
):
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(tmp_path, monkeypatch, "ST-ISSUER")
    estate = VerifiedAnvilStreamEstate(
        root, exact_path=release, independently_held=held,
        current_authorizer=grant,
    )
    with pytest.raises(Exception):
        execute_anvil_stream_i03(
            estate=estate, runtime_catalog=catalog,
            query_ref=source["universe"].ref, predicate_ref=predicate.ref,
        )



def test_native_stream_detects_member_changed_after_initial_verification(
    tmp_path, monkeypatch,
):
    (source, auth, predicate, query, catalog, root, release, manifest,
     held, grant) = _stream(tmp_path, monkeypatch, "ST-TOCTOU")
    estate = VerifiedAnvilStreamEstate(
        root, exact_path=release, independently_held=held,
        current_authorizer=grant,
    )
    with (release / "RespondentEvent.parquet").open("ab") as handle:
        handle.write(b"ALTERED_AFTER_VERIFIED")
    with pytest.raises(DirectEstateError, match="member changed"):
        estate._recheck_unchanged_members()
