import os, sys, tempfile, pathlib
from dataclasses import replace

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate, _ref, _h
from rawlsing_next.pre553_c11_ingest import (
    validate_c11_source_release, build_candidate_replay_manifest,
)
from rawlsing_next.pre553_c11_integrity import (
    EmpiricalPredicateReplayBinding, ComparatorReplayBinding,
    DiscoveryBranchReplayBinding, StructuralAdmissionReplayBinding,
)
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02

base = _candidate("probe-optional")
auth = base.authority_snapshots[0].authority_ref
u = base.empirical_universes[0].ref
predicate = EmpiricalPredicateReplayBinding(
    predicate_grammar_authority_ref=auth,
    typed_predicate_ast_ref=_ref("PREDICATE_AST", "P1"),
    predicate_hash=_h("predicate:P1"),
    coordinate_question_value_refs=(_ref("QUESTION_NATIVE", "probe-optional-Q1"),),
    risk_set_ref=_ref("RISK_SET", "probe-optional-R"),
    target_ref=_ref("TARGET", "probe-optional-T"),
    scope_ref=_ref("SCOPE", "probe-optional-S"),
    measure_basis_ref=_ref("MEASURE", "probe-optional-M"),
)
comparator = ComparatorReplayBinding(
    state="PRESENT",
    actor_fact_ref_or_typed_absence=_ref("ACTOR_FACT", "A1"),
    actor_fact_effective_time_or_typed_absence="2026-01",
    comparator_rule_ref_or_typed_absence=auth,
    resolved_empirical_predicate_ref_or_typed_absence=predicate.ref,
    cardinality_ambiguity_state="NONE",
    source_scope_refs=(u,),
)
discovery = DiscoveryBranchReplayBinding(
    state="PRESENT",
    search_family_id_or_typed_absence="SEARCH-1",
    candidate_universe_ref_or_typed_absence=u,
    grammar_authority_ref_or_typed_absence=auth,
    source_risk_topology_measure_scope_ref_or_typed_absence=_ref("SCOPE", "D1"),
    algorithm_identity_ref_or_typed_absence=_ref("ALGORITHM", "D1"),
    coverage_pruning_contract_ref_or_typed_absence=_ref("PRUNING", "D1"),
    deterministic_parameters_ref_or_typed_absence=_ref("PARAMS", "D1"),
    rng_state_ref_or_typed_absence=_ref("RNG", "D1"),
    parent_branch_ref_or_typed_absence=_ref("BRANCH", "D0"),
    winning_predicate_ref_or_typed_absence=predicate.ref,
    pruned_trace_ref_or_typed_absence=_ref("TRACE", "D1"),
)
structural = StructuralAdmissionReplayBinding(
    state="PRESENT",
    empirical_query_or_fact_ref_or_typed_absence=_ref("QUERY", "S1"),
    predicate_risk_target_scope_measure_ref_or_typed_absence=_ref("SCOPE", "S1"),
    source_empirical_provenance_ref_or_typed_absence=_ref("PROVENANCE", "S1"),
    structural_admission_authority_ref_or_typed_absence=auth,
    target_structural_producer_use_ref_or_typed_absence=_ref("USE", "S1"),
    negative_limit_authority_refs=(),
    transformation_replay_ref_or_typed_absence=_ref("TRANSFORM", "S1"),
)
counts = dict(base.source_release_manifest.declared_record_counts_by_logical_family)
counts["EmpiricalPredicateReplayBinding"] = 1
counts["ComparatorReplayBinding"] = 1
counts["DiscoveryBranchReplayBinding"] = 1
counts["StructuralAdmissionReplayBinding"] = 1
manifest = replace(base.source_release_manifest,
                   declared_record_counts_by_logical_family=counts)
candidate = replace(
    base,
    source_release_manifest=manifest,
    predicate_replay_bindings_when_retained_objects_require_them=(predicate,),
    comparator_replay_bindings_or_typed_deferred_state=(comparator,),
    discovery_branch_replay_bindings_or_typed_deferred_state=(discovery,),
    structural_admission_replay_bindings_or_typed_not_applicable_state=(structural,),
    candidate_replay_manifest=None,
)
replay = build_candidate_replay_manifest(
    candidate,
    replay_protocol_authority_ref=base.candidate_replay_manifest.replay_protocol_authority_ref,
    deterministic_tie_order_rules_ref=base.candidate_replay_manifest.deterministic_tie_order_rules_ref,
    replay_protocol_version=base.candidate_replay_manifest.replay_protocol_version,
)
candidate = replace(candidate, candidate_replay_manifest=replay)
historical = validate_c11_source_release(candidate)
direct = direct_sections_from_candidate(
    replace(candidate, candidate_replay_manifest=None),
    replay_protocol_authority_ref=replay.replay_protocol_authority_ref,
    replay_protocol_version=replay.replay_protocol_version,
    deterministic_tie_order_rules_ref=replay.deterministic_tie_order_rules_ref,
)
d = pathlib.Path(tempfile.mkdtemp(prefix="probe-optional-"))
path = d / "cert.sqlite"
roots = build_sourcefree_direct_i02(direct, u, path, chunk_size=1)
with VerifiedExternalI02(path, roots=roots) as cert:
    header = dict(cert._rows("SELECT name,value FROM main.header"))
    assert header["candidate_projection_hash"] == historical.replay_manifest.semantic_projection_hash
    assert header["reconstructed_v1_replay_ref"] == historical.replay_manifest.ref.key
    assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
    for family in ("EmpiricalPredicateReplayBinding", "ComparatorReplayBinding",
                   "DiscoveryBranchReplayBinding", "StructuralAdmissionReplayBinding"):
        assert cert._first("SELECT COUNT(*) FROM main.objects WHERE family=?", (family,))[0] == 1
print("ALL_OPTIONAL_INTERNAL_FAMILY_PARITY_OK", roots.logical[:12])
