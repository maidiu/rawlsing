"""S2-A H26 public-selector coverage and canonical-order repair tests.

The original H26 witness is preserved verbatim in
``WORKER_RETURNS/PYAT999_S2A_PUBLIC_REPAIR/baseline``.  These tests are the
assertive GREEN regression: public ``VerifiedDirectEstate.select_events`` must
complete every locator/body positional/selector check before filtering, refuse
coherently re-pinned poison, and preserve native ref-canonical order and
repeated occurrences.  Sourcefree fixtures only.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

import pyarrow.parquet as pq

from rawlsing_next._pre553_query_predicate import (
    _build_release_index, _select_respondent_events,
)
from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest, ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import (
    exact_ref, RespondentEvent,
)
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
import rawlsing_next.tests.test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_c11_repository_ingest import (
    _authority, _candidate, _ref,
)


def _capture_source(monkeypatch, tag, rows, **kwargs):
    holder = {}
    original = native.ingest_c11_source_release

    def capture(candidate, repository):
        holder["candidate"] = candidate
        return original(candidate, repository)

    with monkeypatch.context() as patch:
        patch.setattr(native, "ingest_c11_source_release", capture)
        source = native._build_source(tag, rows, **kwargs)
    return source, holder["candidate"]


def _open(root, receipt, grant=lambda _roots: True):
    return VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=grant,
    )


def _native_refs(source, respondent_ref, target):
    index = _build_release_index(
        source["repo"].resolve_release_exact(source["release_ref"]),
        source["universe"].ref,
    )
    return tuple(
        event.ref for event in _select_respondent_events(
            index, respondent_ref.key, target, native_only=True,
        )
    )


def _public_refs(estate, respondent_ref, target, **kwargs):
    return tuple(
        event.ref for event in estate.select_events(
            respondent_ref, target, **kwargs,
        )
    )


def _postings(receipt):
    pf = pq.ParquetFile(Path(receipt.path) / "event_locator.parquet")
    try:
        return [
            row for gid in range(pf.num_row_groups)
            for row in pf.read_row_group(gid).to_pylist()
        ]
    finally:
        pf.close()


def _poison(receipt, *, match_respondent, match_target, field, value):
    rows = _postings(receipt)
    index = next(
        i for i, row in enumerate(rows)
        if row["respondent"] == match_respondent.key
        and row["native"] == match_target.key
    )
    forged = [dict(row) for row in rows]
    forged[index][field] = value
    return s2c._repin_hostile_event_locator(
        receipt, forged, falsify_count=False,
    )


def _alias_candidate(tag):
    old = _candidate(tag, event_kind="UNORDERED_MULTISELECT_SET")
    mapping = _authority(
        tag + "-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    canonical = _ref("QUESTION_CANONICAL", tag + "-canonical")
    component = _ref("QUESTION_COMPONENT", tag + "-component")
    binding = replace(
        old.question_variable_bindings[0],
        canonical_question_ref_or_typed_absence=canonical,
        component_subitem_ref_or_typed_absence=component,
        semantic_authority_ref=mapping.authority_ref,
    )
    events = []
    for event in old.respondent_events:
        fields = dict(event.semantic_fields)
        fields.update(
            canonical_question_ref_if_authorized=canonical,
            component_or_subitem_ref=component,
            value_transform_authority_ref=mapping.authority_ref,
        )
        events.append(RespondentEvent(
            typed_state=event.typed_state,
            authority_snapshot_refs=(
                *event.authority_snapshot_refs, mapping.authority_ref,
            ),
            dependency_refs=event.dependency_refs,
            producer_replay_locator_or_reference_root=(
                event.producer_replay_locator_or_reference_root
            ),
            **fields,
        ))
    counts = dict(old.source_release_manifest.declared_record_counts_by_logical_family)
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        old.source_release_manifest,
        declared_authority_snapshot_refs=(
            *old.source_release_manifest.declared_authority_snapshot_refs,
            mapping.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        old, source_release_manifest=manifest,
        question_variable_bindings=(binding,),
        respondent_events=tuple(events),
        authority_snapshots=(*old.authority_snapshots, mapping),
        candidate_replay_manifest=None,
    )
    candidate = replace(
        candidate,
        candidate_replay_manifest=build_candidate_replay_manifest(
            candidate,
            replay_protocol_authority_ref=(
                old.candidate_replay_manifest.replay_protocol_authority_ref
            ),
            deterministic_tie_order_rules_ref=(
                old.candidate_replay_manifest.deterministic_tie_order_rules_ref
            ),
            replay_protocol_version=(
                old.candidate_replay_manifest.replay_protocol_version
            ),
        ),
    )
    return candidate, canonical, component


def test_h26_public_selector_refuses_coherent_target_poison_before_subset(
    tmp_path, monkeypatch,
):
    tag = "S2A-PUBLIC-H26"
    source, candidate = _capture_source(
        monkeypatch, tag,
        [
            {"id": "R1", "responses": {"Y": 1}},
            {"id": "R2", "responses": {"Y": 0}},
            {"id": "R3", "responses": {"Y": 1}},
            {"id": "R4", "responses": {"Y": 0}},
        ],
    )
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    oracle = native._run(source, qauth, predicate, query)
    respondent = source["respondents"]["R1"].ref
    target = source["qrefs"]["Y"]
    native_selected = _native_refs(source, respondent, target)
    assert len(native_selected) == 1

    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "public-h26",
    )
    baseline = _public_refs(_open(root, receipt), respondent, target,
                            native_only=True)
    assert baseline == native_selected
    baseline_fact = s2c._executor(
        root, receipt, source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert baseline_fact.facts == oracle.facts
    assert tuple(f.ref for f in baseline_fact.facts) == tuple(
        f.ref for f in oracle.facts
    )
    assert baseline_fact.release_refs == oracle.release_refs
    assert not list(root.glob(".s2a-public-select-*"))

    foreign = _ref("QUESTION_NATIVE", "S2A-PUBLIC-FOREIGN").key
    poison_root, poison_receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "public-h26-hidden",
    )
    hidden = _poison(
        poison_receipt, match_respondent=respondent, match_target=target,
        field="native", value=foreign,
    )
    hidden_estate = _open(poison_root, hidden)
    with pytest.raises(DirectEstateError, match="posting|coverage"):
        tuple(hidden_estate.select_events(
            respondent, target, native_only=True,
        ))
    # The empty state set must not bypass complete validation.
    with pytest.raises(DirectEstateError, match="posting|coverage"):
        tuple(hidden_estate.select_events(
            respondent, target, native_only=True, states=frozenset(),
        ))
    # The native I03 owner must still refuse the same poison.
    with pytest.raises(DirectEstateError):
        s2c._executor(
            poison_root, hidden, source, qauth, predicate, query,
        ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    # Untampered restoration is exact.
    restored = _open(root, receipt)
    assert _public_refs(restored, respondent, target, native_only=True) == native_selected
    restored_fact = s2c._executor(
        root, receipt, source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert restored_fact.facts == oracle.facts
    assert tuple(f.ref for f in restored_fact.facts) == tuple(
        f.ref for f in baseline_fact.facts
    )
    assert restored_fact.release_refs == baseline_fact.release_refs
    assert not list(root.glob(".s2a-public-select-*"))
    assert not list(poison_root.glob(".s2a-public-select-*"))


def test_h27_public_selector_alias_and_multiple_occurrence_order(tmp_path):
    candidate, canonical, component = _alias_candidate("S2A-PUBLIC-ALIAS")
    repo = C11Repository()
    accepted = ingest_c11_source_release(candidate, repo)
    assert accepted.accepted, accepted.errors
    release = repo.resolve_release_exact(accepted.release_ref)
    universe = candidate.empirical_universes[0].ref
    respondent = candidate.respondent_identities[0].ref
    target = candidate.question_variable_bindings[0].native_question_ref
    index = _build_release_index(release, universe)
    native_native = tuple(
        event.ref for event in _select_respondent_events(
            index, respondent.key, target, native_only=True,
        )
    )
    native_canonical = tuple(
        event.ref for event in _select_respondent_events(
            index, respondent.key, canonical,
        )
    )
    native_component = tuple(
        event.ref for event in _select_respondent_events(
            index, respondent.key, component, include_component=True,
        )
    )
    assert len(native_native) == 2
    assert native_native == native_canonical == native_component
    assert len(set(native_native)) == 2

    root, receipt = s2c._cold(tmp_path, candidate, universe, "public-alias")
    estate = _open(root, receipt)
    assert _public_refs(estate, respondent, target, native_only=True) == native_native
    assert _public_refs(estate, respondent, canonical) == native_canonical
    assert _public_refs(estate, respondent, component,
                        include_component=True) == native_component
    # native_only takes precedence over canonical/component aliases.
    assert _public_refs(estate, respondent, canonical, native_only=True) == ()
    assert _public_refs(estate, respondent, component) == ()
    assert _public_refs(estate, respondent, target, native_only=True,
                        include_component=True) == native_native
    assert _public_refs(estate, respondent, None) == native_native
    assert _public_refs(estate, respondent, target, native_only=True,
                        states=frozenset()) == ()

    # Coherent poison of each locator selector field must refuse, including
    # when the selected set would otherwise be empty.
    for field, value in (
        ("canonical", _ref("QUESTION_CANONICAL", "S2A-PUBLIC-FOREIGN-CAN").key),
        ("component", _ref("QUESTION_COMPONENT", "S2A-PUBLIC-FOREIGN-COMP").key),
        ("state", "DK"),
    ):
        hidden_root, hidden_receipt = s2c._cold(
            tmp_path, candidate, universe, "public-alias-" + field,
        )
        hidden = _poison(
            hidden_receipt, match_respondent=respondent,
            match_target=target, field=field, value=value,
        )
        hidden_estate = _open(hidden_root, hidden)
        with pytest.raises(DirectEstateError, match="posting|coverage"):
            tuple(hidden_estate.select_events(respondent, target))
        with pytest.raises(DirectEstateError, match="posting|coverage"):
            tuple(hidden_estate.select_events(
                respondent, target, states=frozenset(),
            ))
    assert _public_refs(_open(root, receipt), respondent, target,
                        native_only=True) == native_native
    assert not list(root.glob(".s2a-public-select-*"))


def test_h28_public_empty_is_not_routing_unknown(tmp_path, monkeypatch):
    tag = "S2A-PUBLIC-EMPTY"
    source, candidate = _capture_source(
        monkeypatch, tag,
        [
            {"id": "R1", "responses": {"Y": 1}},
            {"id": "R2", "responses": {}},
        ],
        risk_sets={"R": {"Y": {"R1"}}},
        nonmember_routing_state="ROUTING_UNKNOWN",
    )
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    fact = native._run(source, qauth, predicate, query).facts[0]
    assert fact.typed_state not in ("SUPPORTED", "OBSERVED_ZERO", "NOT_APPLICABLE")
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "public-empty",
    )
    estate = _open(root, receipt)
    respondent = source["respondents"]["R2"].ref
    target = source["qrefs"]["Y"]
    assert _public_refs(estate, respondent, target) == ()
    assert _public_refs(estate, respondent, target, states=frozenset()) == ()


def test_changed_public_selection_and_exact_restore(tmp_path, monkeypatch):
    tag = "S2A-PUBLIC-CHANGE"
    source, candidate = _capture_source(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 0}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    changed_source, changed_candidate = _capture_source(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 1}},
         {"id": "R2", "responses": {"Y": 1}}],
    )
    respondent = source["respondents"]["R1"].ref
    target = source["qrefs"]["Y"]
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("Y",), tag=tag)
    base_oracle = native._run(source, qauth, predicate, query)
    changed_oracle = native._run(changed_source, qauth, predicate, query)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "public-base",
    )
    changed_root, changed_receipt = s2c._cold(
        tmp_path, changed_candidate, changed_source["universe"].ref,
        "public-changed",
    )
    base_refs = _public_refs(_open(root, receipt), respondent, target)
    changed_refs = _public_refs(
        _open(changed_root, changed_receipt), respondent, target,
    )
    assert base_refs and changed_refs
    assert base_refs != changed_refs
    base_fact = s2c._executor(
        root, receipt, source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    changed_fact = s2c._executor(
        changed_root, changed_receipt, changed_source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert base_fact.facts == base_oracle.facts
    assert changed_fact.facts == changed_oracle.facts
    assert tuple(f.ref for f in base_fact.facts) == tuple(
        f.ref for f in base_oracle.facts
    )
    assert tuple(f.ref for f in changed_fact.facts) == tuple(
        f.ref for f in changed_oracle.facts
    )
    assert changed_fact.facts != base_fact.facts
    assert changed_fact.facts[0].ref != base_fact.facts[0].ref
    restored_refs = _public_refs(_open(root, receipt), respondent, target)
    assert restored_refs == base_refs
    restored_fact = s2c._executor(
        root, receipt, source, qauth, predicate, query,
    ).execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert restored_fact.facts == base_fact.facts
    assert restored_fact.release_refs == base_fact.release_refs


def test_public_selector_revocation_and_wrong_root_refuse(tmp_path, monkeypatch):
    tag = "S2A-PUBLIC-CURRENT"
    source, candidate = _capture_source(
        monkeypatch, tag,
        [{"id": "R1", "responses": {"Y": 1}}],
    )
    respondent = source["respondents"]["R1"].ref
    target = source["qrefs"]["Y"]
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "public-current",
    )
    allow = {"value": True}
    estate = _open(root, receipt, lambda _roots: allow["value"])
    baseline = _public_refs(estate, respondent, target, native_only=True)
    assert baseline
    allow["value"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        tuple(estate.select_events(respondent, target, native_only=True))
    allow["value"] = True
    assert _public_refs(estate, respondent, target, native_only=True) == baseline
    from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
    with pytest.raises(DirectEstateError):
        VerifiedDirectEstate(
            root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=replace(
                receipt.i02, source="SOURCE_ARTIFACT:wrong:0",
            ),
            current_authorizer=lambda _roots: True,
        )
