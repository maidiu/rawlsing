import os, sys, tempfile, pathlib
from dataclasses import replace

sys.path.insert(0, os.environ.get("RAWLSING_ROOT", "."))

from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate, _authority, _ref, _root
from rawlsing_next.pre553_c11_ingest import (
    validate_c11_source_release, build_candidate_replay_manifest,
)
from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, SourceUniverseRelation
from rawlsing_next._pre553_direct_i02_sourcefree import (
    direct_sections_from_candidate, build_sourcefree_direct_i02,
)
from rawlsing_next._pre553_external_i02_certificate import VerifiedExternalI02

base = _candidate("probe-universe")
u1 = base.empirical_universes[0]
u2 = EmpiricalUniverse(
    typed_state=u1.typed_state,
    authority_snapshot_refs=u1.authority_snapshot_refs,
    dependency_refs=u1.dependency_refs,
    producer_replay_locator_or_reference_root=_root("universe-u2"),
    **{**dict(u1.semantic_fields),
       "raw_source_identity": "RAW-U2",
       "study_product_release": "STUDY-U2/REL-1",
       "instrument_release": "INST-U2",
       "respondent_namespace": "NS-U2",
       "source_artifact_import_lineage": "SRC-U2"},
)
relation_auth = _authority("relation", "SOURCE_UNIVERSE_RELATION",
                           families=("SourceUniverseRelation@1.0.0",))
relation = SourceUniverseRelation(
    typed_state="DISTINCT_BY_DEFAULT",
    authority_snapshot_refs=(relation_auth.authority_ref,),
    dependency_refs=(u1.ref, u2.ref),
    producer_replay_locator_or_reference_root=_root("relation"),
    relation_id="R-U1-U2",
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
counts = dict(base.source_release_manifest.declared_record_counts_by_logical_family)
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
d = pathlib.Path(tempfile.mkdtemp(prefix="probe-universe-"))
path = d / "cert.sqlite"
roots = build_sourcefree_direct_i02(direct, u1.ref, path, chunk_size=2)
with VerifiedExternalI02(path, roots=roots) as cert:
    header = dict(cert._rows("SELECT name,value FROM main.header"))
    assert header["candidate_projection_hash"] == historical.replay_manifest.semantic_projection_hash
    assert header["reconstructed_v1_replay_ref"] == historical.replay_manifest.ref.key
    assert header["reconstructed_v1_release_ref"] == historical.release_ref.key
    assert roots.replay == historical.replay_manifest.ref.key
    assert sum(1 for _ in cert.respondent_refs()) == 1
    assert cert._first("SELECT COUNT(*) FROM main.objects WHERE family='SourceUniverseRelation'")[0] == 1
    assert cert._first("SELECT COUNT(*) FROM main.objects WHERE family='EmpiricalUniverse'")[0] == 2
print("MULTI_UNIVERSE_RELATION_PARITY_OK", roots.logical[:12])
