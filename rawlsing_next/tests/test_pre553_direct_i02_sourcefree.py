"""S2-B A5: executable direct sourcefree I02 construction contract.

These tests intentionally NEVER pass a C11LogicalRelease or instantiate the
legacy full ReplayManifest.closure_refs in the direct builder. The old source
candidate fixture is used solely as a trustworthy typed sourcefree input
generator. Current/full source issuer, native S2-C physical and M16–M18 legacy
replay parity are intentionally NOT claimed.
"""
from dataclasses import replace
from pathlib import Path
from itertools import islice
from types import MappingProxyType
import sqlite3

import pytest

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections, direct_sections_from_candidate,
    build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import (
    DIRECT_SCHEMA, SCHEMA, ExternalI02IntegrityError, VerifiedExternalI02,
    ExternalI02Roots, _DiskSelectedRespondent, _digest_file,
    install_direct_sourcefree_i02_i03, install_sourcefree_external_i02_i03,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate
from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate, build_candidate_replay_manifest,
    ingest_c11_source_release, validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    ComparatorReplayBinding, DiscoveryBranchReplayBinding,
    EmpiricalPredicateReplayBinding, StructuralAdmissionReplayBinding,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalUniverse, SourceUniverseRelation, exact_ref,
    RespondentEvent,
)


def _direct(tag):
    candidate = _candidate(tag)
    replay = candidate.candidate_replay_manifest
    assert replay is not None
    # No v1 ReplayManifest is allowed into the input of the new builder.
    no_legacy_closure = replace(candidate, candidate_replay_manifest=None)
    direct = direct_sections_from_candidate(
        no_legacy_closure,
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    return candidate, no_legacy_closure, direct


def _build_direct(candidate, path, *, chunk_size=1):
    replay = candidate.candidate_replay_manifest
    assert replay is not None
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    return build_sourcefree_direct_i02(
        direct, candidate.empirical_universes[0].ref, path,
        chunk_size=chunk_size,
    )


def _alias_candidate(tag):
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import (
        _authority, _ref,
    )
    base = _candidate(tag)
    mapping = _authority(
        tag + "-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    canonical_q = _ref("QUESTION_CANONICAL", tag + "-Q1")
    component = _ref("COMPONENT", tag + "-C1")
    question = replace(
        base.question_variable_bindings[0],
        canonical_question_ref_or_typed_absence=canonical_q,
        component_subitem_ref_or_typed_absence=component,
        semantic_authority_ref=mapping.authority_ref,
    )
    events = tuple(
        RespondentEvent(
            typed_state=event.typed_state,
            authority_snapshot_refs=(
                *event.authority_snapshot_refs, mapping.authority_ref,
            ),
            dependency_refs=event.dependency_refs,
            producer_replay_locator_or_reference_root=(
                event.producer_replay_locator_or_reference_root
            ),
            **{
                **dict(event.semantic_fields),
                "canonical_question_ref_if_authorized": canonical_q,
                "component_or_subitem_ref": component,
                "canonical_response_value_if_authorized": (
                    "CANON-" + event.raw_response_value
                ),
                "value_transform_authority_ref": mapping.authority_ref,
            },
        )
        for event in base.respondent_events
    )
    counts = dict(
        base.source_release_manifest.declared_record_counts_by_logical_family
    )
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        base.source_release_manifest,
        declared_authority_snapshot_refs=(
            *base.source_release_manifest.declared_authority_snapshot_refs,
            mapping.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        base,
        question_variable_bindings=(question,),
        respondent_events=events,
        authority_snapshots=(*base.authority_snapshots, mapping),
        source_release_manifest=manifest,
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=(
            base.candidate_replay_manifest.replay_protocol_authority_ref
        ),
        deterministic_tie_order_rules_ref=(
            base.candidate_replay_manifest.deterministic_tie_order_rules_ref
        ),
        replay_protocol_version=(
            base.candidate_replay_manifest.replay_protocol_version
        ),
    )
    return replace(candidate, candidate_replay_manifest=replay), canonical_q, component


def _multi_universe_candidate(tag):
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import (
        _authority, _root,
    )
    base = _candidate(tag)
    u1 = base.empirical_universes[0]
    u2 = EmpiricalUniverse(
        typed_state=u1.typed_state,
        authority_snapshot_refs=u1.authority_snapshot_refs,
        dependency_refs=u1.dependency_refs,
        producer_replay_locator_or_reference_root=_root(tag + "-u2"),
        **{
            **dict(u1.semantic_fields),
            "raw_source_identity": "RAW-" + tag + "-U2",
            "study_product_release": "STUDY-" + tag + "-U2/REL-1",
            "instrument_release": "INST-" + tag + "-U2",
            "respondent_namespace": "NS-" + tag + "-U2",
            "source_artifact_import_lineage": "SRC-" + tag + "-U2",
        },
    )
    relation_auth = _authority(
        tag + "-relation", "SOURCE_UNIVERSE_RELATION",
        families=("SourceUniverseRelation@1.0.0",),
    )
    relation = SourceUniverseRelation(
        typed_state="DISTINCT_BY_DEFAULT",
        authority_snapshot_refs=(relation_auth.authority_ref,),
        dependency_refs=(u1.ref, u2.ref),
        producer_replay_locator_or_reference_root=_root(tag + "-relation"),
        relation_id="R-" + tag,
        relation_kind="HARMONIZATION_ALIAS",
        source_universe_refs=(u1.ref, u2.ref),
        relation_authority_ref=relation_auth.authority_ref,
        effective_scope="ALL",
        overlap_or_nonduplication_evidence_refs=(),
        composition_estimand_refs=(),
        deduplication_rule_ref_if_any=None,
        negative_limit_refs=(),
        decision="NOT_APPLICABLE",
    )
    counts = dict(
        base.source_release_manifest.declared_record_counts_by_logical_family
    )
    counts["EmpiricalUniverse"] = 2
    counts["SourceUniverseRelation"] = 1
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        base.source_release_manifest,
        declared_universe_refs=(u1.ref, u2.ref),
        declared_authority_snapshot_refs=(
            *base.source_release_manifest.declared_authority_snapshot_refs,
            relation_auth.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        base,
        empirical_universes=(u1, u2),
        source_universe_relations_or_explicit_distinct_default=(relation,),
        authority_snapshots=(*base.authority_snapshots, relation_auth),
        source_release_manifest=manifest,
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=(
            base.candidate_replay_manifest.replay_protocol_authority_ref
        ),
        deterministic_tie_order_rules_ref=(
            base.candidate_replay_manifest.deterministic_tie_order_rules_ref
        ),
        replay_protocol_version=(
            base.candidate_replay_manifest.replay_protocol_version
        ),
    )
    return replace(candidate, candidate_replay_manifest=replay)


def _optional_family_candidate(tag):
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import (
        _h, _ref,
    )
    base = _candidate(tag)
    authority = base.authority_snapshots[0].authority_ref
    universe = base.empirical_universes[0].ref
    predicate = EmpiricalPredicateReplayBinding(
        predicate_grammar_authority_ref=authority,
        typed_predicate_ast_ref=_ref("PREDICATE_AST", tag + "-P1"),
        predicate_hash=_h("predicate:" + tag),
        coordinate_question_value_refs=(
            base.question_variable_bindings[0].native_question_ref,
        ),
        risk_set_ref=_ref("RISK_SET", tag + "-R"),
        target_ref=_ref("TARGET", tag + "-T"),
        scope_ref=_ref("SCOPE", tag + "-S"),
        measure_basis_ref=_ref("MEASURE", tag + "-M"),
    )
    comparator = ComparatorReplayBinding(
        state="PRESENT",
        actor_fact_ref_or_typed_absence=_ref("ACTOR_FACT", tag + "-A1"),
        actor_fact_effective_time_or_typed_absence="2026-01",
        comparator_rule_ref_or_typed_absence=authority,
        resolved_empirical_predicate_ref_or_typed_absence=predicate.ref,
        cardinality_ambiguity_state="NONE",
        source_scope_refs=(universe,),
    )
    discovery = DiscoveryBranchReplayBinding(
        state="PRESENT",
        search_family_id_or_typed_absence="SEARCH-" + tag,
        candidate_universe_ref_or_typed_absence=universe,
        grammar_authority_ref_or_typed_absence=authority,
        source_risk_topology_measure_scope_ref_or_typed_absence=_ref(
            "SCOPE", tag + "-D1"),
        algorithm_identity_ref_or_typed_absence=_ref(
            "ALGORITHM", tag + "-D1"),
        coverage_pruning_contract_ref_or_typed_absence=_ref(
            "PRUNING", tag + "-D1"),
        deterministic_parameters_ref_or_typed_absence=_ref(
            "PARAMS", tag + "-D1"),
        rng_state_ref_or_typed_absence=_ref("RNG", tag + "-D1"),
        parent_branch_ref_or_typed_absence=_ref("BRANCH", tag + "-D0"),
        winning_predicate_ref_or_typed_absence=predicate.ref,
        pruned_trace_ref_or_typed_absence=_ref("TRACE", tag + "-D1"),
    )
    structural = StructuralAdmissionReplayBinding(
        state="PRESENT",
        empirical_query_or_fact_ref_or_typed_absence=_ref(
            "QUERY", tag + "-S1"),
        predicate_risk_target_scope_measure_ref_or_typed_absence=_ref(
            "SCOPE", tag + "-S1"),
        source_empirical_provenance_ref_or_typed_absence=_ref(
            "PROVENANCE", tag + "-S1"),
        structural_admission_authority_ref_or_typed_absence=authority,
        target_structural_producer_use_ref_or_typed_absence=_ref(
            "USE", tag + "-S1"),
        negative_limit_authority_refs=(),
        transformation_replay_ref_or_typed_absence=_ref(
            "TRANSFORM", tag + "-S1"),
    )
    counts = dict(
        base.source_release_manifest.declared_record_counts_by_logical_family
    )
    counts["EmpiricalPredicateReplayBinding"] = 1
    counts["ComparatorReplayBinding"] = 1
    counts["DiscoveryBranchReplayBinding"] = 1
    counts["StructuralAdmissionReplayBinding"] = 1
    candidate = replace(
        base,
        source_release_manifest=replace(
            base.source_release_manifest,
            declared_record_counts_by_logical_family=counts,
        ),
        predicate_replay_bindings_when_retained_objects_require_them=(
            predicate,
        ),
        comparator_replay_bindings_or_typed_deferred_state=(comparator,),
        discovery_branch_replay_bindings_or_typed_deferred_state=(discovery,),
        structural_admission_replay_bindings_or_typed_not_applicable_state=(
            structural,
        ),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=(
            base.candidate_replay_manifest.replay_protocol_authority_ref
        ),
        deterministic_tie_order_rules_ref=(
            base.candidate_replay_manifest.deterministic_tie_order_rules_ref
        ),
        replay_protocol_version=(
            base.candidate_replay_manifest.replay_protocol_version
        ),
    )
    return replace(candidate, candidate_replay_manifest=replay)


def test_s2b_a5_direct_real_sourcefree_candidate_without_v1_release(tmp_path):
    candidate, stripped, streams = _direct("s2b-a5-direct")
    assert type(stripped) is C11SourceReleaseCandidate
    assert stripped.candidate_replay_manifest is None
    path = tmp_path / "direct-i02.sqlite"
    expected = build_sourcefree_direct_i02(
        streams, candidate.empirical_universes[0].ref, path, chunk_size=1,
    )
    assert expected.schema == DIRECT_SCHEMA and expected.schema != SCHEMA
    with VerifiedExternalI02(path, roots=expected) as certified:
        assert list(certified.respondent_refs())
        first_event = candidate.respondent_events[0]
        respondent = exact_ref(first_event.scoped_respondent_ref).key
        native = exact_ref(first_event.native_question_ref)
        assert len(list(certified.selector_refs(
            respondent, native,
        ))) > 0
        for family in ("EmpiricalUniverse", "RespondentIdentity",
                       "QuestionVariableBinding", "RespondentEvent",
                       "RoutingEligibilityFact", "EmpiricalCoordinateFact",
                       "AuthoritySnapshot"):
            assert certified._first(
                "SELECT COUNT(*) FROM main.objects WHERE family=?", (family,)
            )[0] >= 1
        header = dict(certified._rows("SELECT name,value FROM main.header"))
        assert header["legacy_replay_m16_m18_equivalence"].startswith("STREAMED_HASH_")
        assert header["original_source_current_issuer"] == "NOT_ISSUED"
        # Strong independent native historical functional comparator:
        # only the TEST oracle uses full old in-memory ReplayManifest/C11.
        # The direct producer above never constructed or consumed them.
        historical = validate_c11_source_release(candidate)
        assert header["candidate_projection_hash"] == historical.replay_manifest.semantic_projection_hash
        assert header["reconstructed_v1_replay_ref"] == historical.replay_manifest.ref.key
        assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
        assert expected.replay == historical.replay_manifest.ref.key
        # Trace the actual native I03 first selector owner, not an abstract
        # expected-number model. Full native facts are covered in inherited
        # I03 tests; here compare direct-produced complete selected refs.
        from rawlsing_next._pre553_query_predicate import (
            _build_release_index, _select_respondent_events,
        )
        native_index = _build_release_index(
            historical, candidate.empirical_universes[0].ref,
        )
        for respondent in native_index.respondents:
            old_all = {x.ref.key for x in native_index.events_by_respondent[respondent]}
            new_all = {x.key for x in certified.event_refs(respondent)}
            assert new_all == old_all
            for q in candidate.question_variable_bindings:
                expected_events = {
                    x.ref.key for x in _select_respondent_events(
                        native_index, respondent, q.native_question_ref,
                        native_only=True,
                    )
                }
                selected = {x.key for x in certified.selector_refs(
                    respondent, q.native_question_ref, native_only=True,
                )}
                assert selected == expected_events
    # No direct-candidate roots may be smuggled into the old sealed-release
    # native I03 loader, even if it has an otherwise valid physical root.
    repo = C11Repository()
    admission = ingest_c11_source_release(candidate, repo)
    assert admission.accepted
    with VerifiedExternalI02(path, roots=expected) as direct_reader:
        # The actual native selector consumer must consume direct postings and
        # resolve exact event bodies from the independent repository. The
        # legacy release-installation identity path must still refuse them.
        selector = MappingProxyType({
            key: _DiskSelectedRespondent(key, direct_reader, repo)
            for key in native_index.respondents
        })
        direct_index = replace(native_index, events_by_respondent=selector)
        for respondent in native_index.respondents:
            assert [event.ref.key for event in
                    direct_index.events_by_respondent[respondent]] == [
                event.ref.key for event in
                native_index.events_by_respondent[respondent]
            ]
            for q in candidate.question_variable_bindings:
                for native_only in (True, False):
                    for include_component in (False, True):
                        for states in (
                            None, frozenset({"SUBSTANTIVE_RESPONSE"}),
                            frozenset(),
                        ):
                            expected_events = [
                                event.ref.key for event in
                                _select_respondent_events(
                                    native_index, respondent,
                                    q.native_question_ref,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            selected_events = [
                                event.ref.key for event in
                                _select_respondent_events(
                                    direct_index, respondent,
                                    q.native_question_ref,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            assert selected_events == expected_events
        with pytest.raises(ExternalI02IntegrityError, match="cannot impersonate"):
            install_sourcefree_external_i02_i03(
                repo, admission.release_ref,
                candidate.empirical_universes[0].ref, direct_reader,
            )


def test_s2b_a5_direct_chunk_determinism_cold_root_wrong_source(tmp_path):
    candidate, _, _ = _direct("s2b-a5-determinism")
    universe = candidate.empirical_universes[0].ref
    def build(path, chunk):
        _, _, source = _direct("s2b-a5-determinism")
        return build_sourcefree_direct_i02(
            source, universe, path, chunk_size=chunk,
        )
    small = tmp_path / "c1.sqlite"
    large = tmp_path / "c257.sqlite"
    r1 = build(small, 1)
    r257 = build(large, 257)
    assert r1.logical == r257.logical
    with VerifiedExternalI02(small, roots=r1) as left:
        a = list(left.respondent_refs())
    with VerifiedExternalI02(large, roots=r257) as right:
        assert a == list(right.respondent_refs())
    wrong = build(tmp_path / "wrong-source.sqlite", 5)
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(large, roots=replace(
            wrong, source="SOURCE_ARTIFACT|forged|" + "0" * 64,
        ))
    # Sourcefree restore exactly replays the same logical commitment.
    assert build(tmp_path / "restored.sqlite", 19).logical == r1.logical


@pytest.mark.parametrize("omitted", (
    "RespondentEvent", "EmpiricalCoordinateFact", "RoutingEligibilityFact",
    "QuestionVariableBinding", "RespondentIdentity", "AuthoritySnapshot",
))
def test_s2b_a5_direct_declared_census_refuses_family_omission(tmp_path, omitted):
    candidate, _, source = _direct("s2b-a5-omission-" + omitted)
    sections = dict(source.sections)
    # Deliberately remove exactly one valid object from original typed source;
    # leave original independently declared census/source refs unchanged.
    sections[omitted] = islice(sections[omitted], 1, None)
    spoiled = replace(source, sections=sections)
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_direct_i02(
            spoiled, candidate.empirical_universes[0].ref,
            tmp_path / (omitted + ".sqlite"),
        )
    assert not (tmp_path / (omitted + ".sqlite")).exists()


def test_s2b_a5_direct_duplicate_manifest_declarations_refused(tmp_path):
    for label in ("universe", "authority"):
        candidate, _, source = _direct("s2b-a5-dup-manifest-" + label)
        manifest = candidate.source_release_manifest
        if label == "universe":
            universe = manifest.declared_universe_refs[0]
            manifest = replace(
                manifest, declared_universe_refs=(universe, universe),
            )
        else:
            authority = manifest.declared_authority_snapshot_refs[0]
            manifest = replace(
                manifest, declared_authority_snapshot_refs=(
                    *manifest.declared_authority_snapshot_refs, authority,
                ),
            )
        target = tmp_path / (label + ".sqlite")
        with pytest.raises(ExternalI02IntegrityError):
            build_sourcefree_direct_i02(
                replace(source, manifest=manifest),
                candidate.empirical_universes[0].ref, target,
            )
        assert not target.exists()


def test_s2b_a5_direct_legacy_valid_manifest_without_replay_count(tmp_path):
    candidate, _, _ = _direct("s2b-a5-no-replay-count")
    counts = dict(
        candidate.source_release_manifest.declared_record_counts_by_logical_family
    )
    counts.pop("ReplayManifest")
    base = replace(
        candidate,
        source_release_manifest=replace(
            candidate.source_release_manifest,
            declared_record_counts_by_logical_family=counts,
        ),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        base,
        replay_protocol_authority_ref=(
            candidate.candidate_replay_manifest.replay_protocol_authority_ref
        ),
        deterministic_tie_order_rules_ref=(
            candidate.candidate_replay_manifest.deterministic_tie_order_rules_ref
        ),
        replay_protocol_version=(
            candidate.candidate_replay_manifest.replay_protocol_version
        ),
    )
    candidate = replace(base, candidate_replay_manifest=replay)
    historical = validate_c11_source_release(candidate)
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    path = tmp_path / "no-replay-count.sqlite"
    roots = build_sourcefree_direct_i02(
        direct, candidate.empirical_universes[0].ref, path, chunk_size=2,
    )
    with VerifiedExternalI02(path, roots=roots) as certified:
        header = dict(certified._rows("SELECT name,value FROM main.header"))
        assert header["candidate_projection_hash"] == (
            historical.replay_manifest.semantic_projection_hash
        )
        assert header["reconstructed_v1_replay_ref"] == (
            historical.replay_manifest.ref.key
        )
        assert header["reconstructed_v1_release_ref"] == historical.release_ref.key


def test_s2b_a5_direct_duplicate_occurrence_and_changed_state_refused(tmp_path):
    candidate, _, source = _direct("s2b-a5-duplicate-occurrence")
    sections = dict(source.sections)
    # Repeat a real event in the same source identity/rank/occurrence slot.
    events = candidate.respondent_events
    sections["RespondentEvent"] = iter((*events, events[0]))
    # Attacker tries to align claimed count with the repeated row:
    declared = dict(candidate.source_release_manifest.declared_record_counts_by_logical_family)
    declared["RespondentEvent"] = len(events) + 1
    manifest = replace(candidate.source_release_manifest,
                       declared_record_counts_by_logical_family=declared)
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_direct_i02(
            replace(source, manifest=manifest, sections=sections),
            candidate.empirical_universes[0].ref,
            tmp_path / "duplicate.sqlite",
        )
    assert not (tmp_path / "duplicate.sqlite").exists()


def test_s2b_a5_direct_no_saved_local_rehash_authenticates_cold(tmp_path):
    candidate, _, source = _direct("s2b-a5-root-attack")
    path = tmp_path / "direct.sqlite"
    expected = build_sourcefree_direct_i02(
        source, candidate.empirical_universes[0].ref, path,
    )
    with sqlite3.connect(path) as attacker:
        attacker.execute("""
            DELETE FROM main.selectors WHERE rowid=(
                SELECT rowid FROM main.selectors LIMIT 1
            )
        """)
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=expected)
    # Even replacing only the external *physical* root leaves semantic
    # closure/complete-index/held logical identity violated.
    locally_rehashed_physical = replace(expected, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=locally_rehashed_physical)


def test_s2b_a5_direct_one_shot_iterators_cannot_silently_replay(tmp_path):
    candidate, _, input_once = _direct("s2b-a5-one-pass")
    universe = candidate.empirical_universes[0].ref
    first = build_sourcefree_direct_i02(
        input_once, universe, tmp_path / "first.sqlite", chunk_size=3,
    )
    assert first.logical
    # No reused iterator is considered a successful second source census;
    # native record counts hold even if the local output could self-rehash.
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_direct_i02(
            input_once, universe, tmp_path / "second.sqlite", chunk_size=3,
        )
    assert not (tmp_path / "second.sqlite").exists()



def test_s2b_a5_sourcefree_direct_changed_restore_without_legacy_release(tmp_path):
    """New direct certificate responds to real typed sourcefree event changes.

    The sourcefree fixture is not an original35 source-equivalence claim.
    Source/content rights remain held separately; changed bytes must be
    independently issued before any native production consumer accepts them.
    """
    candidate, _, original = _direct("s2b-a5-change")
    universe = candidate.empirical_universes[0].ref
    original_path = tmp_path / "before.sqlite"
    original_roots = build_sourcefree_direct_i02(original, universe, original_path, chunk_size=1)
    event = candidate.respondent_events[0]
    changed_event = RespondentEvent(
        typed_state=event.typed_state,
        authority_snapshot_refs=event.authority_snapshot_refs,
        dependency_refs=event.dependency_refs,
        producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
        **{**dict(event.semantic_fields), "raw_response_value": "A_DIFFERENT_TYPED_RESPONSE"},
    )
    assert changed_event.ref != event.ref
    changed_candidate = replace(candidate,
        respondent_events=(changed_event, *candidate.respondent_events[1:]),
        candidate_replay_manifest=None,
    )
    replay = candidate.candidate_replay_manifest
    changed_stream = direct_sections_from_candidate(
        changed_candidate,
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    changed_path = tmp_path / "changed.sqlite"
    changed_roots = build_sourcefree_direct_i02(
        changed_stream, universe, changed_path, chunk_size=7,
    )
    assert changed_roots.logical != original_roots.logical
    respondent = exact_ref(event.scoped_respondent_ref).key
    question = exact_ref(event.native_question_ref)
    with VerifiedExternalI02(original_path, roots=original_roots) as reader:
        old_refs = {r.key for r in reader.selector_refs(respondent, question)}
        assert event.ref.key in old_refs
    with VerifiedExternalI02(changed_path, roots=changed_roots) as reader:
        new_refs = {r.key for r in reader.selector_refs(respondent, question)}
        assert changed_event.ref.key in new_refs
        assert event.ref.key not in new_refs
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(changed_path, roots=original_roots)
    _, _, restored_input = _direct("s2b-a5-change")
    restored_roots = build_sourcefree_direct_i02(
        restored_input, universe, tmp_path / "restored.sqlite", chunk_size=3,
    )
    assert restored_roots.logical == original_roots.logical


def test_s2b_a5_direct_historical_identity_installs_native_i03_selectors(tmp_path):
    from rawlsing_next._pre553_query_predicate import (
        _build_release_index, _select_respondent_events,
    )
    candidate, _, _ = _direct("s2b-a5-direct-install")
    historical = validate_c11_source_release(candidate)
    universe = candidate.empirical_universes[0].ref
    path = tmp_path / "direct-install.sqlite"
    roots = _build_direct(candidate, path, chunk_size=3)
    repo = C11Repository()
    admission = ingest_c11_source_release(candidate, repo)
    assert admission.accepted
    native = _build_release_index(historical, universe)
    with VerifiedExternalI02(path, roots=roots) as reader:
        install_direct_sourcefree_i02_i03(
            repo, admission.release_ref, universe, reader,
        )
        index = repo._i03_release_indices[(admission.release_ref, universe)]
        for respondent in native.respondents:
            assert [event.ref.key for event in
                    index.events_by_respondent[respondent]] == [
                event.ref.key for event in
                native.events_by_respondent[respondent]
            ]
            for q in candidate.question_variable_bindings:
                for native_only in (True, False):
                    for include_component in (False, True):
                        for states in (
                            None, frozenset({"SUBSTANTIVE_RESPONSE"}),
                            frozenset(),
                        ):
                            expected = [
                                event.ref.key for event in
                                _select_respondent_events(
                                    native, respondent,
                                    q.native_question_ref,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            selected = [
                                event.ref.key for event in
                                _select_respondent_events(
                                    index, respondent,
                                    q.native_question_ref,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            assert selected == expected
        event = candidate.respondent_events[0]
        changed_event = RespondentEvent(
            typed_state=event.typed_state,
            authority_snapshot_refs=event.authority_snapshot_refs,
            dependency_refs=event.dependency_refs,
            producer_replay_locator_or_reference_root=(
                event.producer_replay_locator_or_reference_root
            ),
            **{
                **dict(event.semantic_fields),
                "raw_response_value": "A_DIFFERENT_TYPED_RESPONSE",
            },
        )
        changed_base = replace(
            candidate,
            respondent_events=(
                changed_event, *candidate.respondent_events[1:]
            ),
            candidate_replay_manifest=None,
        )
        changed_replay = build_candidate_replay_manifest(
            changed_base,
            replay_protocol_authority_ref=(
                candidate.candidate_replay_manifest
                .replay_protocol_authority_ref
            ),
            deterministic_tie_order_rules_ref=(
                candidate.candidate_replay_manifest
                .deterministic_tie_order_rules_ref
            ),
            replay_protocol_version=(
                candidate.candidate_replay_manifest.replay_protocol_version
            ),
        )
        changed_candidate = replace(
            changed_base, candidate_replay_manifest=changed_replay,
        )
        changed_path = tmp_path / "direct-install-changed.sqlite"
        changed_roots = _build_direct(changed_candidate, changed_path)
        with VerifiedExternalI02(
            changed_path, roots=changed_roots,
        ) as changed_reader:
            with pytest.raises(ExternalI02IntegrityError):
                install_direct_sourcefree_i02_i03(
                    repo, admission.release_ref, universe, changed_reader,
                )


def test_s2b_a5_direct_changed_restored_native_i03_eligible_output(tmp_path):
    from rawlsing_next._pre553_query_predicate import _select_respondent_events
    candidate, _, _ = _direct("s2b-a5-native-change")
    universe = candidate.empirical_universes[0].ref
    event = candidate.respondent_events[0]
    respondent = exact_ref(event.scoped_respondent_ref).key
    target = exact_ref(event.native_question_ref)

    def selected(candidate_input, tag):
        path = tmp_path / (tag + ".sqlite")
        roots = _build_direct(candidate_input, path, chunk_size=2)
        repo = C11Repository()
        admission = ingest_c11_source_release(candidate_input, repo)
        assert admission.accepted
        reader = VerifiedExternalI02(path, roots=roots)
        try:
            install_direct_sourcefree_i02_i03(
                repo, admission.release_ref, universe, reader,
            )
            index = repo._i03_release_indices[
                (admission.release_ref, universe)
            ]
            return [
                selected_event.ref.key for selected_event in
                _select_respondent_events(
                    index, respondent, target, native_only=True,
                )
            ]
        finally:
            reader.close()

    original = selected(candidate, "before")
    assert event.ref.key in original
    changed_event = RespondentEvent(
        typed_state=event.typed_state,
        authority_snapshot_refs=event.authority_snapshot_refs,
        dependency_refs=event.dependency_refs,
        producer_replay_locator_or_reference_root=(
            event.producer_replay_locator_or_reference_root
        ),
        **{
            **dict(event.semantic_fields),
            "raw_response_value": "A_DIFFERENT_TYPED_RESPONSE",
        },
    )
    changed_base = replace(
        candidate,
        respondent_events=(changed_event, *candidate.respondent_events[1:]),
        candidate_replay_manifest=None,
    )
    changed_replay = build_candidate_replay_manifest(
        changed_base,
        replay_protocol_authority_ref=(
            candidate.candidate_replay_manifest.replay_protocol_authority_ref
        ),
        deterministic_tie_order_rules_ref=(
            candidate.candidate_replay_manifest
            .deterministic_tie_order_rules_ref
        ),
        replay_protocol_version=(
            candidate.candidate_replay_manifest.replay_protocol_version
        ),
    )
    changed_candidate = replace(
        changed_base, candidate_replay_manifest=changed_replay,
    )
    changed = selected(changed_candidate, "changed")
    assert changed_event.ref.key in changed
    assert event.ref.key not in changed
    restored_candidate, _, _ = _direct("s2b-a5-native-change")
    assert selected(restored_candidate, "restored") == original


def test_s2b_a5_direct_original_semantic_event_order_is_invariant(tmp_path):
    candidate, _, _ = _direct("s2b-a5-ordered")
    left_replay = candidate.candidate_replay_manifest
    def from_candidate(event_stream):
        original = replace(
            candidate, respondent_events=event_stream, candidate_replay_manifest=None,
        )
        return direct_sections_from_candidate(
            original,
            replay_protocol_authority_ref=left_replay.replay_protocol_authority_ref,
            replay_protocol_version=left_replay.replay_protocol_version,
            deterministic_tie_order_rules_ref=left_replay.deterministic_tie_order_rules_ref,
        )
    universe = candidate.empirical_universes[0].ref
    a = build_sourcefree_direct_i02(
        from_candidate(candidate.respondent_events), universe,
        tmp_path / "original-order.sqlite", chunk_size=5,
    )
    b = build_sourcefree_direct_i02(
        from_candidate(tuple(reversed(candidate.respondent_events))), universe,
        tmp_path / "reversed-order.sqlite", chunk_size=1,
    )
    assert a.logical == b.logical



def test_s2b_a5_direct_selector_alias_order_and_state_parity(tmp_path):
    candidate, canonical_q, component = _alias_candidate("s2b-a5-alias-order")
    historical = validate_c11_source_release(candidate)
    replay = candidate.candidate_replay_manifest
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    path = tmp_path / "alias-order.sqlite"
    roots = build_sourcefree_direct_i02(
        direct, candidate.empirical_universes[0].ref, path, chunk_size=1,
    )
    from rawlsing_next._pre553_query_predicate import (
        _build_release_index, _select_respondent_events,
    )
    native_index = _build_release_index(
        historical, candidate.empirical_universes[0].ref,
    )
    targets = (
        candidate.question_variable_bindings[0].native_question_ref,
        canonical_q, component,
    )
    with VerifiedExternalI02(path, roots=roots) as certified:
        for respondent in native_index.respondents:
            for target in targets:
                for native_only in (True, False):
                    for include_component in (False, True):
                        for states in (
                            None, frozenset({"SUBSTANTIVE_RESPONSE"}), frozenset(),
                        ):
                            expected = [
                                event.ref.key for event in _select_respondent_events(
                                    native_index, respondent, target,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            selected = [
                                ref.key for ref in certified.selector_refs(
                                    respondent, target,
                                    native_only=native_only,
                                    include_component=include_component,
                                    states=states,
                                )
                            ]
                            assert selected == expected, (
                                target.kind, native_only, include_component,
                                states, selected, expected,
                            )


def test_s2b_a5_direct_multi_universe_relation_historical_parity(tmp_path):
    candidate = _multi_universe_candidate("s2b-a5-multi-universe")
    historical = validate_c11_source_release(candidate)
    replay = candidate.candidate_replay_manifest
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    path = tmp_path / "multi-universe.sqlite"
    roots = build_sourcefree_direct_i02(
        direct, candidate.empirical_universes[0].ref, path, chunk_size=2,
    )
    with VerifiedExternalI02(path, roots=roots) as certified:
        header = dict(certified._rows("SELECT name,value FROM main.header"))
        assert header["candidate_projection_hash"] == (
            historical.replay_manifest.semantic_projection_hash
        )
        assert header["reconstructed_v1_replay_ref"] == (
            historical.replay_manifest.ref.key
        )
        assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
        assert roots.replay == historical.replay_manifest.ref.key
        assert certified._first("""
            SELECT COUNT(*) FROM main.objects WHERE family='EmpiricalUniverse'
        """)[0] == 2
        assert certified._first("""
            SELECT COUNT(*) FROM main.objects
            WHERE family='SourceUniverseRelation'
        """)[0] == 1


def test_s2b_a5_direct_all_optional_internal_families_historical_parity(tmp_path):
    candidate = _optional_family_candidate("s2b-a5-optional-families")
    historical = validate_c11_source_release(candidate)
    replay = candidate.candidate_replay_manifest
    direct = direct_sections_from_candidate(
        replace(candidate, candidate_replay_manifest=None),
        replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
        replay_protocol_version=replay.replay_protocol_version,
        deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
    )
    path = tmp_path / "optional-families.sqlite"
    roots = build_sourcefree_direct_i02(
        direct, candidate.empirical_universes[0].ref, path, chunk_size=1,
    )
    with VerifiedExternalI02(path, roots=roots) as certified:
        header = dict(certified._rows("SELECT name,value FROM main.header"))
        assert header["candidate_projection_hash"] == (
            historical.replay_manifest.semantic_projection_hash
        )
        assert header["reconstructed_v1_replay_ref"] == (
            historical.replay_manifest.ref.key
        )
        assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
        for family in (
            "EmpiricalPredicateReplayBinding", "ComparatorReplayBinding",
            "DiscoveryBranchReplayBinding",
            "StructuralAdmissionReplayBinding",
        ):
            assert certified._first("""
                SELECT COUNT(*) FROM main.objects WHERE family=?
            """, (family,))[0] == 1


def test_s2b_a5_direct_unlawful_typed_absence_refused(tmp_path):
    candidate, _, source = _direct("s2b-a5-unlawful-absence")
    absences = dict(source.typed_absences)
    absences["WeightMeasureFact"] = TypedAbsence("DISTINCT_BY_DEFAULT")
    target = tmp_path / "unlawful-absence.sqlite"
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_direct_i02(
            replace(source, typed_absences=absences),
            candidate.empirical_universes[0].ref, target,
        )
    assert not target.exists()


def test_s2b_a5_direct_wrong_authority_is_typed_refusal(tmp_path):
    candidate, _, source = _direct("s2b-a5-wrong-authority")
    event = candidate.respondent_events[0]
    forged = AuthorityRef("FORGED-AUTHORITY", "1.0.0", "0" * 64)
    changed_event = RespondentEvent(
        typed_state=event.typed_state,
        authority_snapshot_refs=(forged,),
        dependency_refs=event.dependency_refs,
        producer_replay_locator_or_reference_root=(
            event.producer_replay_locator_or_reference_root
        ),
        **dict(event.semantic_fields),
    )
    sections = dict(source.sections)
    sections["RespondentEvent"] = iter(
        (changed_event, *candidate.respondent_events[1:]),
    )
    target = tmp_path / "wrong-authority.sqlite"
    with pytest.raises(ExternalI02IntegrityError):
        build_sourcefree_direct_i02(
            replace(source, sections=sections),
            candidate.empirical_universes[0].ref, target,
        )
    assert not target.exists()


def test_s2b_a5_direct_forged_selector_posting_refused(tmp_path):
    candidate, _, source = _direct("s2b-a5-forged-selector")
    path = tmp_path / "forged-selector.sqlite"
    roots = build_sourcefree_direct_i02(
        source, candidate.empirical_universes[0].ref, path,
    )
    event = candidate.respondent_events[0]
    with sqlite3.connect(path) as attacker:
        attacker.execute("""
            INSERT INTO main.selectors VALUES(?,?,?,?)
        """, (
            exact_ref(event.scoped_respondent_ref).key, "native",
            exact_ref(event.native_question_ref).key, "FORGED|event|" + "0" * 64,
        ))
    forged = replace(roots, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=forged)


def test_s2b_a5_direct_cold_verifier_typed_refusal_on_missing_direct_tables(tmp_path):
    candidate, _, source = _direct("s2b-a5-missing-direct-table")
    path = tmp_path / "direct.sqlite"
    roots = build_sourcefree_direct_i02(
        source, candidate.empirical_universes[0].ref, path,
    )
    with sqlite3.connect(path) as attacker:
        attacker.execute("DROP TABLE main.event_occurrences")
    forged = replace(roots, physical=_digest_file(path))
    with pytest.raises(ExternalI02IntegrityError):
        VerifiedExternalI02(path, roots=forged)


def test_s2b_a5_direct_publication_oserror_typed_no_clobber(tmp_path, monkeypatch):
    import rawlsing_next._pre553_direct_i02_sourcefree as impl
    candidate, _, source = _direct("s2b-a5-publish-oserror")
    target = tmp_path / "target.sqlite"
    def broken_link(*args, **kwargs):
        raise OSError("simulated link failure")
    monkeypatch.setattr(impl.os, "link", broken_link)
    with pytest.raises(ExternalI02IntegrityError, match="no-clobber"):
        build_sourcefree_direct_i02(
            source, candidate.empirical_universes[0].ref, target, chunk_size=1,
        )
    assert not target.exists()
    assert not any(tmp_path.glob(".s2b-direct-stage-*.tmp"))


def test_s2b_a5_direct_2048_one_shot_event_stream_and_cold_memory(tmp_path):
    """Actual typed event generator, not a pre-materialized 2048-object tuple.

    The original fixture builds only two sourcefree events; the direct
    producer consumes 2048 additional valid event instances one at a time.
    This is a material-scale one-respondent occurrence sample, NOT
    original35 100k-person or full integrated 6GiB release proof.
    """
    import time
    import tracemalloc
    import resource
    base_candidate, _, base_source = _direct("s2b-a5-material")
    base = base_candidate.respondent_events[0]
    n = 2048
    counts = dict(base_candidate.source_release_manifest.declared_record_counts_by_logical_family)
    counts["RespondentEvent"] = n
    manifest = replace(base_candidate.source_release_manifest,
                       declared_record_counts_by_logical_family=counts)
    def events():
        for i in range(n):
            yield RespondentEvent(
                typed_state=base.typed_state,
                authority_snapshot_refs=base.authority_snapshot_refs,
                dependency_refs=base.dependency_refs,
                producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
                **{**dict(base.semantic_fields),
                   "response_event_id_or_deterministic_index": f"bounded-{i:05d}"},
            )
    sections = dict(base_source.sections)
    sections["RespondentEvent"] = events()
    input_stream = replace(base_source, manifest=manifest, sections=sections)
    universe = base_candidate.empirical_universes[0].ref
    path = tmp_path / "direct-material.sqlite"
    tracemalloc.start()
    started = time.monotonic()
    try:
        roots = build_sourcefree_direct_i02(
            input_stream, universe, path, chunk_size=31,
        )
        build_s = time.monotonic() - started
        _live, peak_python = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    started = time.monotonic()
    with VerifiedExternalI02(path, roots=roots) as certified:
        target = exact_ref(base.native_question_ref)
        respondent = exact_ref(base.scoped_respondent_ref).key
        assert sum(1 for _ in certified.selector_refs(
            respondent, target, native_only=True,
        )) == n
    cold_verify_s = time.monotonic() - started
    print({
        "schema": roots.schema,
        "event_generator": n,
        "respondents": 1,
        "retained_bytes": path.stat().st_size,
        "build_s": round(build_s, 4),
        "cold_verify_plus_2048_select_s": round(cold_verify_s, 4),
        "python_builder_peak_bytes": peak_python,
        "peak_process_rss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "scratch_peak": "NOT_MEASURED",
        "complete_source_native_100k": "NOT_RUN",
        "historical_replay_manifest_m16_m18": "NOT_PROVEN",
    })
    assert peak_python < 32 * 1024 * 1024
