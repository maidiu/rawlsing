"""Sourcefree persisted SRC16-shaped recorded-only fixture.

The stream is built only from the existing nonrespondent sourcefree native
candidate. It carries SRC16 source identity, a structured owner scope, the
exact SRC16 historical grade and the actual saved BINARY_CONTRAST_SINGLE topology. No original SRC16
bytes, response bodies or private evidence are read.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import struct

import pytest

import sys
_TEST_DIR = Path(__file__).resolve().parent
if str(_TEST_DIR) not in sys.path:
    sys.path.insert(0, str(_TEST_DIR))
from src16_operator import HISTORICAL_GRADE, OPERATION, Src16OperatorError, materialize

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalUniverse, ExactRef, canonical_json, exact_ref, semantic_hash
from rawlsing_next.pre553_source_direct_parquet_estate import _Sink, _IndexSink, _row
from rawlsing_next.tests import test_pre553_direct_estate_i03 as native_fixture
from rawlsing_next.tests import test_pre553_empirical_query as native
_ORIGINAL_EVENT = native.RespondentEvent
_REAL_EVENT = native.RespondentEvent

def _actual_saved_event(**kwargs):
    kwargs["multiplicity_order_rank_fields"] = {
        "index": 0,
        "kind": "BINARY_CONTRAST_SINGLE",
        "source_manual_topology": "binary_contrast",
    }
    return _REAL_EVENT(**kwargs)

_ORIGINAL_EVENT = _actual_saved_event


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
        for i, code in enumerate((1, 2, 1, -98, -99, -100, None), 1)
    ]
    rows.append({"id": "R8", "responses": {}})
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
        "authority_id": "SRC16-HISTORICAL-DEFER",
        "authority_version": "1.0.0",
        "authority_content_hash": semantic_hash({"src16": "historical-defer", "tag": tag}),
        "authority_kind": "SOURCE_SEMANTICS_TOPOLOGY",
        "decision_state": "DEFER",
        "governed_operations": ("R157_SOURCE_PREPARATION_SOURCE_SEMANTICS",),
        "governed_object_families": ("EmpiricalUniverse@1.0.0",),
        "scope_envelope": {
            "evidence_bundle_sha256": "a" * 64,
            "grade": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
            "not_source_scientific_authority": True,
            "p2_authority_status": "DEFER",
            "source_id": "SRC16",
            "source_sha256": "a" * 64,
            "wave": "GSS1972",
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
        source_id="SRC16", source_sha256=source_sha,
        manifest_sha256=_digest(manifest), exact_release_path=str(release),
        roots=roots,
    )
    return source, candidate, root, release, held, historical, universe


def test_src16_persisted_defer_recorded_entry_uses_native_scalar(tmp_path, monkeypatch):
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
        build_recorded_operation, _translate_saved_scalar_topology,
    )
    from rawlsing_next.pre553_anvil_stream_issuance import issue_and_execute_stream_i03
    from rawlsing_next.pre553_anvil_stream_native_i03 import execute_anvil_stream_i03
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog

    codes = ("1", "2", "-98", "-99", "-100")
    interpretation = (
        ("1", "SUBSTANTIVE_RESPONSE"),
        ("2", "SUBSTANTIVE_RESPONSE"),
        ("-98", "DK"),
        ("-99", "MISSING"),
        ("-100", "INAPPLICABLE"),
    )
    scope = "SRC16_RACPRES_OBSERVED_STORED_CODE_FREQUENCIES"
    qref = source["qrefs"]["Y"]
    # Exact stream roots from the fixture source and universe.
    stream_roots = {
        "source": held.roots["source"], "release": held.roots["release"],
        "universe": universe.ref.key, "replay": held.roots["replay"],
    }
    owner_sha = sha256(b"q006-src16-sourcefree-fixture-owner").hexdigest()
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
            "governed_operations": ("SRC16-RACPRES-RECORDED-RESPONSE-ONLY",),
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
    canonical_scope = {
        "host": "sourcefree-host",
        "scope": scope,
        "question_id": "GSS:1972:racpres",
        "questionnaire_sha256": "d" * 64,
        "denominator": {
            "asked_risk": "HELD_ROUTING_UNKNOWN",
            "recorded_raw_codes": [1, 2, -98, -99, -100],
        },
    }
    positive_scope = {
        "source_universe_refs": [universe.ref.as_dict()],
        "scope": canonical_scope,
        "release": stream_roots["release"],
        "replay_root": stream_roots["replay"],
        "source_sha256": stream_roots["source"],
        "recorded_raw_codes": list(codes),
        "scope_kind": "OBSERVED_STORED_CODE_FREQUENCIES",
        "asked_eligibility": "HELD_NOT_PROVEN",
        "substantive_vote_denominator": False,
        "historical_scope_grade": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
        "historical_snapshot_ref": historical.ref.as_dict(),
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
        source_id="SRC16",
        source_root=stream_roots["source"],
        release_root=stream_roots["release"],
        universe_root=stream_roots["universe"],
        replay_root=stream_roots["replay"],
        question_ref=qref,
        authorized_operation="SRC16-RACPRES-RECORDED-RESPONSE-ONLY",
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
        approved_nonanswer_states=("DK", "MISSING", "INAPPLICABLE"),
        state_bearing_raw_codes=True,
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
        source_id="SRC16",
        source_root=stream_roots["source"],
        release_root=stream_roots["release"],
        universe_root=stream_roots["universe"],
        replay_root=stream_roots["replay"],
        question_ref=qref,
        query_ref=decision.query.ref,
        predicate_ref=decision.predicate.ref,
        operation="SRC16-RACPRES-RECORDED-RESPONSE-ONLY",
        risk_ref=risk,
        interpretation=interpretation,
        scope=canonical_scope,
        current_verifier=lambda: use_allowed["value"],
        historical_scope_grade="EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
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
    assert fact.raw_denominator_support == 6
    assert len(cells) == 5
    assert {canonical_json(row["cell"]) for row in cells} == {
        canonical_json(1), canonical_json(2),
        canonical_json({"typed_response_state": "DK"}),
        canonical_json({"typed_response_state": "MISSING"}),
        canonical_json({"typed_response_state": "INAPPLICABLE"}),
    }
    assert {
        canonical_json(row["cell"]): row["raw_numerator_support"]
        for row in cells
    } == {
        canonical_json(1): 2, canonical_json(2): 1,
        canonical_json({"typed_response_state": "DK"}): 1,
        canonical_json({"typed_response_state": "MISSING"}): 1,
        canonical_json({"typed_response_state": "INAPPLICABLE"}): 1,
    }
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
    with pytest.raises(RecordedResponseError, match="historical"):
        replace(
            use,
            historical_scope_grade="EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY",
        ).authorize(universe, decision.query, decision.predicate)
    with pytest.raises(RecordedResponseError, match="historical"):
        replace(use, historical_scope_grade="EXACT_UNKNOWN_GRADE").authorize(
            universe, decision.query, decision.predicate)
    from types import SimpleNamespace
    wrong_field = dict(historical.semantic_fields)
    wrong_field["scope_envelope"] = {
        "semantic_scope": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
        "source_universe_refs": [universe.ref.as_dict()],
    }
    wrong_field_historical = AuthoritySnapshot(
        typed_state="DEFER",
        authority_snapshot_refs=historical.authority_snapshot_refs,
        dependency_refs=historical.dependency_refs,
        producer_replay_locator_or_reference_root=historical.producer_replay_locator_or_reference_root,
        **wrong_field,
    )
    fake_universe = SimpleNamespace(
        ref=universe.ref,
        authority_snapshot_refs=(wrong_field_historical.authority_ref,),
    )
    fake_query = SimpleNamespace(ref=decision.query.ref, risk_set_ref=risk)
    fake_predicate = SimpleNamespace(ref=decision.predicate.ref)
    with pytest.raises(RecordedResponseError, match="historical"):
        replace(use, historical_snapshot=wrong_field_historical).authorize(
            fake_universe, fake_query, fake_predicate)

    wrong_historical_ref = dict(positive_scope)
    wrong_historical_ref["historical_snapshot_ref"] = {
        "kind": "AuthoritySnapshot@1.0.0",
        "object_id": "urn:rawlsing:pre553:AuthoritySnapshot:sha256:" + "0" * 64,
        "content_hash": "0" * 64,
    }
    wrong_ref_snapshot = clone_snapshot(
        source["authorities"][0], state="ALLOW",
        scope_envelope=wrong_historical_ref,
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        label="WRONG-HISTORICAL-REF",
    )
    with pytest.raises(RecordedResponseError, match="historical"):
        replace(use, positive_snapshot=wrong_ref_snapshot).authorize(
            universe, decision.query, decision.predicate)
    # The independent expected scope is the exact full owner scope: any
    # individual field or shape change must refuse before the native path.
    for bad_field, bad_value in (
        ("host", "different-host"),
        ("questionnaire_sha256", "e" * 64),
        ("denominator", {"asked_risk": "DIFFERENT"}),
    ):
        wrong_scope = dict(canonical_scope)
        wrong_scope[bad_field] = bad_value
        wrong_envelope = dict(positive_scope)
        wrong_envelope["scope"] = wrong_scope
        wrong_snapshot = clone_snapshot(
            source["authorities"][0], state="ALLOW", scope_envelope=wrong_envelope,
            kind="SOURCE_SEMANTICS_TOPOLOGY",
            families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
            label="WRONG-" + bad_field,
        )
        with pytest.raises(RecordedResponseError, match="scope"):
            replace(use, positive_snapshot=wrong_snapshot).authorize(
                universe, decision.query, decision.predicate)
    wrong_shape = dict(canonical_scope)
    wrong_shape.pop("denominator")
    wrong_envelope = dict(positive_scope)
    wrong_envelope["scope"] = wrong_shape
    wrong_snapshot = clone_snapshot(
        source["authorities"][0], state="ALLOW", scope_envelope=wrong_envelope,
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        label="WRONG-SHAPE",
    )
    with pytest.raises(RecordedResponseError, match="scope"):
        replace(use, positive_snapshot=wrong_snapshot).authorize(
            universe, decision.query, decision.predicate)
    use_allowed["value"] = False
    with pytest.raises(RecordedResponseError, match="authority"):
        use.authorize(universe, decision.query, decision.predicate)
    with pytest.raises(RecordedResponseError, match="authority"):
        build_recorded_operation(
            estate=estate, operation=replace(operation, authorities=()),
            question_ref=qref,
        )
    with pytest.raises(RecordedResponseError, match="unknown recorded raw code"):
        build_recorded_operation(
            estate=estate,
            operation=replace(
                operation,
                allowed_raw_codes=("1", "2"),
                interpretation=(
                    ("1", "SUBSTANTIVE_RESPONSE"),
                    ("2", "SUBSTANTIVE_RESPONSE"),
                ),
                approved_nonanswer_states=(),
            ),
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


def test_src16_driver_preflight_and_native_wiring(tmp_path, monkeypatch):
    source, candidate, root, release, held, historical, universe = _defer_stream(
        tmp_path, monkeypatch, tag="SRC16-DRIVER",
    )
    qref = source["qrefs"]["Y"]
    binding = {
        "custody_estate_path": "/sourcefree/src16-driver",
        "decision_ref": "USER_SOURCE_DECISION|sourcefree-src16-driver|" + "1" * 64,
        "manifest_sha256": held.manifest_sha256,
        "saved_i02": dict(held.roots),
        "source_sha256": held.source_sha256,
    }
    scope = {
        "host": "sourcefree-host",
        "scope": "SRC16_RACPRES_OBSERVED_STORED_CODE_FREQUENCIES",
        "question_id": "GSS:1972:racpres",
        "questionnaire_sha256": "d" * 64,
        "denominator": {
            "asked_risk": "HELD_ROUTING_UNKNOWN",
            "recorded_raw_codes": [1, 2, -98, -99, -100],
        },
    }
    owner = {
        "schema": "ANVIL_Q006_SRC16_OWNER_DECISION@1",
        "source_id": "SRC16",
        "source_binding": binding,
        "host": scope["host"],
        "scope": scope,
        "question_id": scope["question_id"],
        "native_question_ref": qref.as_dict(),
        "questionnaire_sha256": scope["questionnaire_sha256"],
        "denominator": scope["denominator"],
        "interpretation": {
            "1": ["SUBSTANTIVE_RESPONSE"],
            "2": ["SUBSTANTIVE_RESPONSE"],
            "-98": ["DK"],
            "-99": ["MISSING"],
            "-100": ["INAPPLICABLE"],
        },
        "authorized_operation": OPERATION,
        "historical_scope_grade": HISTORICAL_GRADE,
        "historical_snapshot_ref": historical.ref.as_dict(),
        "approved_nonanswer_states": ["DK", "MISSING", "INAPPLICABLE"],
    }
    owner_path = tmp_path / "src16-owner.json"
    owner_path.write_text(json.dumps(owner, sort_keys=True))
    r2_path = tmp_path / "src16-r2.json"
    r2_path.write_text(json.dumps({"waves": {"SRC16": binding}}, sort_keys=True))
    operation_path = tmp_path / "src16-operation.json"
    materialize(owner_path=owner_path, r2_path=r2_path, output=operation_path)
    operation_bytes = operation_path.read_bytes()
    use = {
        "owner_decision_sha256": sha256(owner_path.read_bytes()).hexdigest(),
        "operation_document_sha256": sha256(operation_bytes).hexdigest(),
        "historical_scope_grade": HISTORICAL_GRADE,
        "historical_snapshot_ref": historical.ref.as_dict(),
        "scope": scope,
        "operation": OPERATION,
        "recorded_raw_codes": [1, 2, -98, -99, -100],
    }
    use_path = tmp_path / "src16-use.json"
    use_path.write_text(json.dumps(use, sort_keys=True))
    closure_path = tmp_path / "src16-closure.json"
    closure_path.write_text(json.dumps([{
        "ref": historical.ref.as_dict(), "state": "DEFER",
        "semantic_scope": HISTORICAL_GRADE,
    }], sort_keys=True))
    from run_recorded_src16_private import prepare_and_run
    result = prepare_and_run(
        owner_path=owner_path, operation_path=operation_path, r2_path=r2_path,
        stream_root=root, release_path=release,
        universe_use_path=use_path, universe_closure_path=closure_path,
    )
    assert result["source_id"] == "SRC16"
    assert result["missing"] == {"system_missing": 1, "absent": 1}
    assert result["positive_counts_accepted"] is True
    fact = result["facts"][0]
    assert fact["typed_state"] == "SUPPORTED"
    assert fact["raw_denominator_support"] == 6
    assert result["scope_kind"] == "OBSERVED_STORED_CODE_FREQUENCIES"
    assert result["asked_eligibility"] == "HELD_NOT_PROVEN"
    assert result["substantive_vote_denominator"] is False
    assert result["stored_code_bins"] == [
        {"raw_code": "1", "state": "SUBSTANTIVE_RESPONSE", "cell": 1, "raw_numerator_support": 2},
        {"raw_code": "2", "state": "SUBSTANTIVE_RESPONSE", "cell": 2, "raw_numerator_support": 1},
        {"raw_code": "-98", "state": "DK", "cell": {"typed_response_state": "DK"}, "raw_numerator_support": 1},
        {"raw_code": "-99", "state": "MISSING", "cell": {"typed_response_state": "MISSING"}, "raw_numerator_support": 1},
        {"raw_code": "-100", "state": "INAPPLICABLE", "cell": {"typed_response_state": "INAPPLICABLE"}, "raw_numerator_support": 1},
    ]
    assert len(fact["cells"]) == 5
    assert {canonical_json(row[0]) for row in fact["cells"]} == {
        canonical_json(1), canonical_json(2),
        canonical_json({"typed_response_state": "DK"}),
        canonical_json({"typed_response_state": "MISSING"}),
        canonical_json({"typed_response_state": "INAPPLICABLE"}),
    }

    # Exercise the actual CLI/result writer, not only the in-process helper.
    import run_recorded_src16_private as driver_module
    result_path = tmp_path / "src16-private-result.json"
    with monkeypatch.context() as patch:
        patch.setattr(sys, "argv", [
            "run_recorded_src16_private.py",
            "--owner-decision", str(owner_path),
            "--operation-json", str(operation_path),
            "--r2-decision", str(r2_path),
            "--stream-root", str(root),
            "--release-path", str(release),
            "--universe-use-decision", str(use_path),
            "--universe-closure", str(closure_path),
            "--output", str(result_path),
        ])
        assert driver_module.main() == 0
    written = json.loads(result_path.read_text())
    assert written["positive_counts_accepted"] is True
    assert written["scope_kind"] == "OBSERVED_STORED_CODE_FREQUENCIES"
    assert written["facts"][0]["raw_denominator_support"] == 6
    assert oct(result_path.stat().st_mode & 0o777) == "0o600"

    # A stale operation/use document must refuse before the cold estate is
    # even constructed.  This is a wiring assertion, not a native run.
    import run_recorded_src16_private as driver_module
    stale_use = dict(use)
    stale_use["operation_document_sha256"] = "0" * 64
    stale_use_path = tmp_path / "src16-use-stale.json"
    stale_use_path.write_text(json.dumps(stale_use, sort_keys=True))
    def forbidden_estate(*_args, **_kwargs):
        raise AssertionError("estate constructed before SRC16 preflight refusal")
    with monkeypatch.context() as patch:
        patch.setattr(driver_module, "VerifiedAnvilStreamEstate", forbidden_estate)
        with pytest.raises(Src16OperatorError, match="USE_OPERATION_STALE"):
            driver_module.prepare_and_run(
                owner_path=owner_path, operation_path=operation_path,
                r2_path=r2_path, stream_root=root, release_path=release,
                universe_use_path=stale_use_path,
                universe_closure_path=closure_path,
            )
