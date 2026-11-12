import os, sys, tempfile, pathlib, hashlib
from dataclasses import replace

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate, _authority, _ref, _h, _root
from rawlsing_next.pre553_c11_ingest import validate_c11_source_release, build_candidate_replay_manifest
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02
from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events

base = _candidate("alias")
mapping_auth = _authority("mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                          families=("RespondentEvent@1.0.0",))
canonical_q = _ref("QUESTION_CANONICAL", "alias-Q1-CANON")
component = _ref("COMPONENT", "alias-Q1-C1")
question = base.question_variable_bindings[0]
new_q = replace(question,
    canonical_question_ref_or_typed_absence=canonical_q,
    component_subitem_ref_or_typed_absence=component,
    semantic_authority_ref=mapping_auth.authority_ref)
new_events = []
for e in base.respondent_events:
    new_events.append(RespondentEvent(
        typed_state=e.typed_state,
        authority_snapshot_refs=(*e.authority_snapshot_refs, mapping_auth.authority_ref),
        dependency_refs=e.dependency_refs,
        producer_replay_locator_or_reference_root=e.producer_replay_locator_or_reference_root,
        **{**dict(e.semantic_fields),
           "canonical_question_ref_if_authorized": canonical_q,
           "component_or_subitem_ref": component,
           "canonical_response_value_if_authorized": "CANON-" + e.raw_response_value,
           "value_transform_authority_ref": mapping_auth.authority_ref}))
counts = dict(base.source_release_manifest.declared_record_counts_by_logical_family)
counts["AuthoritySnapshot"] = len(base.authority_snapshots) + 1
manifest = replace(base.source_release_manifest,
    declared_authority_snapshot_refs=(*base.source_release_manifest.declared_authority_snapshot_refs, mapping_auth.authority_ref),
    declared_record_counts_by_logical_family=counts)
cand = replace(base,
    question_variable_bindings=(new_q,),
    respondent_events=tuple(new_events),
    authority_snapshots=(*base.authority_snapshots, mapping_auth),
    source_release_manifest=manifest,
    candidate_replay_manifest=None)
cand = replace(cand, candidate_replay_manifest=build_candidate_replay_manifest(
    cand,
    replay_protocol_authority_ref=base.candidate_replay_manifest.replay_protocol_authority_ref,
    deterministic_tie_order_rules_ref=base.candidate_replay_manifest.deterministic_tie_order_rules_ref,
    replay_protocol_version=base.candidate_replay_manifest.replay_protocol_version))
historical = validate_c11_source_release(cand)
replay = cand.candidate_replay_manifest
direct_input = direct_sections_from_candidate(
    replace(cand, candidate_replay_manifest=None),
    replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
    replay_protocol_version=replay.replay_protocol_version,
    deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref)
d = pathlib.Path(tempfile.mkdtemp(prefix="probe-alias-"))
path = d / "cert.sqlite"
roots = build_sourcefree_direct_i02(direct_input, cand.empirical_universes[0].ref, path, chunk_size=1)
with VerifiedExternalI02(path, roots=roots) as cert:
    header = dict(cert._rows("SELECT name,value FROM main.header"))
    assert header["candidate_projection_hash"] == historical.replay_manifest.semantic_projection_hash
    assert header["reconstructed_v1_replay_ref"] == historical.replay_manifest.ref.key
    assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
    idx = _build_release_index(historical, cand.empirical_universes[0].ref)
    resp = next(iter(idx.respondents))
    targets = [new_q.native_question_ref, canonical_q, component]
    for t in targets:
        for native_only in (True, False):
            for include_component in (False, True):
                exp = [e.ref.key for e in _select_respondent_events(
                    idx, resp, t, native_only=native_only, include_component=include_component)]
                got = [r.key for r in cert.selector_refs(
                    resp, t, native_only=native_only, include_component=include_component)]
                print(t.kind, "native_only", native_only, "component", include_component, "exp", len(exp), "got", len(got))
                assert got == exp, (t.kind, native_only, include_component, got, exp)
    # state filters
    for states in (None, frozenset({"SUBSTANTIVE_RESPONSE"}), frozenset(), frozenset({"NOT_A_RESPONSE"})):
        exp = [e.ref.key for e in _select_respondent_events(idx, resp, new_q.native_question_ref, native_only=True, states=states)]
        got = [r.key for r in cert.selector_refs(resp, new_q.native_question_ref, native_only=True, states=states)]
        assert got == exp, (states, got, exp)
print("ALIAS_CLOSURE_PARITY_OK", roots.logical[:12])
