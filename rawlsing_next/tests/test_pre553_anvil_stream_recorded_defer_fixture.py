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
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalUniverse, ExactRef, exact_ref, semantic_hash
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
    old_respondents = tuple(candidate.respondent_identities)
    new_respondents = tuple(
        replace(r, empirical_universe_ref=universe.ref) for r in old_respondents
    )
    respondent_ref = {
        old.ref.key: new.ref for old, new in zip(old_respondents, new_respondents)
    }

    def with_universe(obj):
        if not hasattr(obj, "semantic_fields"):
            return replace(obj, empirical_universe_ref=universe.ref)
        fields = dict(obj.semantic_fields)
        if "empirical_universe_ref" in fields:
            fields["empirical_universe_ref"] = universe.ref
        for name in ("scoped_respondent_ref", "respondent"):
            if name in fields:
                old = fields[name]
                old_key = exact_ref(old).key
                if old_key in respondent_ref:
                    fields[name] = respondent_ref[old_key]
        return type(obj)(
            typed_state=obj.typed_state,
            authority_snapshot_refs=obj.authority_snapshot_refs,
            dependency_refs=obj.dependency_refs,
            producer_replay_locator_or_reference_root=obj.producer_replay_locator_or_reference_root,
            **fields,
        )

    root = tmp_path / tag
    root.mkdir(mode=0o700)
    release = root / "releases" / ("stream-" + tag)
    release.parent.mkdir(mode=0o700)
    release.mkdir(mode=0o700)

    family_objects = {
        "AuthoritySnapshot": (*candidate.authority_snapshots, historical),
        "ComparatorReplayBinding": (),
        "DiscoveryBranchReplayBinding": (),
        "EmpiricalCoordinateFact": tuple(with_universe(x) for x in candidate.empirical_coordinate_facts),
        "EmpiricalPredicateReplayBinding": (),
        "EmpiricalUniverse": (universe,),
        "QuestionVariableBinding": tuple(with_universe(x) for x in candidate.question_variable_bindings),
        "RespondentEvent": tuple(with_universe(x) for x in candidate.respondent_events),
        "RespondentIdentity": new_respondents,
        "RoutingEligibilityFact": tuple(with_universe(x) for x in candidate.routing_eligibility_facts_or_exact_rules),
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
    # The exact cut must expose the recorded entry classes.  The scratch
    # corrected bfa cut restores only the exact earlier definitions.
    from rawlsing_next.pre553_anvil_stream_recorded import (
        HeldRecordedOperation, RecordedUniverseUse, RecordedResponseError,
        build_recorded_operation,
    )
    from rawlsing_next.pre553_anvil_stream_issuance import issue_and_execute_stream_i03
    from rawlsing_next.pre553_anvil_stream_native_i03 import execute_anvil_stream_i03
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog

    codes = ("1", "2", "3", "4", "97", "98", "99")
    interpretation = (
        ("1", "SUBSTANTIVE_RESPONSE"), ("2", "SUBSTANTIVE_RESPONSE"),
        ("3", "SUBSTANTIVE_RESPONSE"), ("4", "SUBSTANTIVE_RESPONSE"),
        ("97", "SOURCE_SPECIFIC_SPECIAL"), ("98", "DK"), ("99", "REFUSAL"),
    )
    scope = "Q103_RAW_UNWEIGHTED_RECORDED_RESPONSE_ONLY"
    qref = source["qrefs"]["Y"]
    # Exact stream roots from the fixture source and universe.
    stream_roots = {
        "source": held.roots["source"], "release": held.roots["release"],
        "universe": universe.ref.key, "replay": held.roots["replay"],
    }
    owner_sha = sha256(b"q006-sourcefree-fixture-owner").hexdigest()
    def clone_snapshot(base, *, state, scope_envelope, kind, families, label):
        fields = dict(base.semantic_fields)
        fields.update({
            "authority_id": "Q006-FIXTURE-" + label + "-" + state,
            "authority_version": "1.0.0",
            "authority_content_hash": semantic_hash({
                "state": state, "scope": scope_envelope,
                "owner": owner_sha, "label": label,
            }),
            "authority_kind": kind,
            "decision_state": state,
            "governed_operations": ("Q103-OP-RECORDED-RESPONSE-ONLY",),
            "governed_object_families": families,
            "scope_envelope": scope_envelope,
        })
        return AuthoritySnapshot(
            typed_state=state,
            authority_snapshot_refs=base.authority_snapshot_refs,
            dependency_refs=base.dependency_refs,
            producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
            **fields,
        )
    positive_scope = {
        "source_universe_refs": [universe.ref.as_dict()],
        "scope": scope,
        "release": stream_roots["release"],
        "replay_root": stream_roots["replay"],
        "source_sha256": stream_roots["source"],
        "recorded_raw_codes": list(codes),
    }
    positive_source = clone_snapshot(
        source["authorities"][0], state="ALLOW", scope_envelope=positive_scope,
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        label="SOURCE",
    )
    positive_routing = clone_snapshot(
        source["authorities"][0], state="ALLOW", scope_envelope=positive_scope,
        kind="ROUTING_RISK_SET", families=("RoutingEligibilityFact@1.0.0",),
        label="ROUTING",
    )
    positive_query = clone_snapshot(
        source["authorities"][0], state="ALLOW", scope_envelope=positive_scope,
        kind="PREDICATE_GRAMMAR",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
                  "EmpiricalFact@1.0.0"),
        label="QUERY",
    )
    positive = positive_source
    risk = ExactRef("RISK_SET", "recorded-response-fixture", semantic_hash({"codes": codes, "owner": owner_sha}))
    rule = ExactRef("ROUTING_RULE", "recorded-only-fixture", semantic_hash({"scope": scope, "owner": owner_sha}))
    member = ExactRef("MEMBER_SET", "recorded-members-fixture", semantic_hash({"codes": codes, "owner": owner_sha}))
    measure = ExactRef("MEASURE_BASIS", "RAW", semantic_hash({"measure": "RAW"}))
    semantics = ExactRef("RESPONSE_STATE_SEMANTICS", "recorded-only-fixture", semantic_hash({"interpretation": interpretation}))
    domain = ExactRef("TARGET_DOMAIN", "q103-recorded-fixture", semantic_hash({"question": qref.as_dict(), "codes": codes}))
    pred_replay = ExactRef("REPLAY_ROOT", "recorded-predicate-fixture", semantic_hash({"kind": "predicate"}))
    query_replay = ExactRef("REPLAY_ROOT", "recorded-query-fixture", semantic_hash({"kind": "query"}))
    transform = ExactRef("RECORDED_VALUE_TRANSFORM", "q103-fixture", semantic_hash({"transform": "R5_RAW_TO_RECORDED_OUTCOME"}))
    operation = HeldRecordedOperation(
        owner_decision_sha256=owner_sha,
        source_id="SRC04",
        source_root=stream_roots["source"],
        release_root=stream_roots["release"],
        universe_root=stream_roots["universe"],
        replay_root=stream_roots["replay"],
        question_ref=qref,
        authorized_operation="Q103-OP-RECORDED-RESPONSE-ONLY",
        allowed_raw_codes=codes,
        interpretation=interpretation,
        authorities=(positive_source, positive_routing, positive_query),
        query_authority_ref=positive_query.authority_ref,
        routing_authority_ref=positive_routing.authority_ref,
        source_authority_ref=positive_source.authority_ref,
        recorded_risk_ref=risk,
        routing_rule_ref=rule,
        member_set_replay_ref=member,
        measure_basis_ref=measure,
        response_state_semantics_ref=semantics,
        target_domain_replay_ref=domain,
        predicate_replay_root=pred_replay,
        query_replay_root=query_replay,
        transform_ref=transform,
        approved_nonanswer_states=("UNRESOLVED",),
    )
    estate = VerifiedAnvilStreamEstate(
        root, exact_path=release, independently_held=held,
        current_authorizer=lambda _pins: True,
    )
    decision, plan, missing = build_recorded_operation(
        estate=estate, operation=operation, question_ref=qref,
    )
    assert missing == {"system_missing": 1, "absent": 1}
    use_allowed = {"value": True}
    use = RecordedUniverseUse(
        historical_snapshot=historical,
        positive_snapshot=positive,
        owner_decision_sha256=owner_sha,
        operation_document_sha256=sha256(b"q006-fixture-operation").hexdigest(),
        source_id="SRC04",
        source_root=stream_roots["source"],
        release_root=stream_roots["release"],
        universe_root=stream_roots["universe"],
        replay_root=stream_roots["replay"],
        question_ref=qref,
        query_ref=decision.query.ref,
        predicate_ref=decision.predicate.ref,
        operation="Q103-OP-RECORDED-RESPONSE-ONLY",
        risk_ref=risk,
        interpretation=interpretation,
        scope=scope,
        current_verifier=lambda: use_allowed["value"],
    )
    assert use.authorize(universe, decision.query, decision.predicate) == (
        historical.authority_ref, positive_source.authority_ref,
    )
    plan = replace(plan, universe_use=use)
    first = issue_and_execute_stream_i03(
        estate=estate, decision=decision,
        decision_verifier=lambda candidate: candidate == decision,
        recorded_plan=plan,
    )
    second = issue_and_execute_stream_i03(
        estate=estate, decision=decision,
        decision_verifier=lambda candidate: candidate == decision,
        recorded_plan=plan,
    )
    fact = first.facts[0]
    cells = fact.target_topology.get("complete_cell_semantic_projection", ())
    assert fact.raw_denominator_support == 7
    assert len(cells) == 7
    assert {str(row["cell"]) for row in cells} == set(codes)
    assert missing["system_missing"] == 1 and missing["absent"] == 1
    assert fact.semantic_fields.get("replay_ref") == second.facts[0].semantic_fields.get("replay_ref")
    # Both exact refs are carried through the scoped use receipt.
    assert use.authorize(universe, decision.query, decision.predicate) == (
        historical.authority_ref, positive_source.authority_ref,
    )
    # Missing/revoked scope and ordinary native DEFER refuse.
    bad_positive = clone_snapshot(
        source["authorities"][0], state="ALLOW", scope_envelope={},
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        label="BAD",
    )
    bad_use = replace(use, positive_snapshot=bad_positive)
    with pytest.raises(RecordedResponseError, match="scope"):
        bad_use.authorize(universe, decision.query, decision.predicate)
    use_allowed["value"] = False
    with pytest.raises(RecordedResponseError, match="authority"):
        use.authorize(universe, decision.query, decision.predicate)
    with pytest.raises(RecordedResponseError, match="authority"):
        build_recorded_operation(
            estate=estate, operation=replace(operation, authorities=()),
            question_ref=qref,
        )
    catalog = RuntimeObjectCatalog(
        authorities=(positive_source, positive_routing, positive_query), predicates=(decision.predicate,),
        queries=(decision.query,), discovery_authorities=(),
    )
    ordinary = execute_anvil_stream_i03(
        estate=estate, runtime_catalog=catalog,
        query_ref=decision.query.ref, predicate_ref=decision.predicate.ref,
    )
    assert ordinary.facts[0].typed_state != "SUPPORTED"
