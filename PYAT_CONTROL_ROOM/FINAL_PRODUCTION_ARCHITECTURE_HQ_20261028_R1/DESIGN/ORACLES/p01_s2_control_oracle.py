#!/usr/bin/env python3
"""P01-S2 source-free baseline oracle, intended for repo-root execution.

This runs the EXISTING I02 implementation and official test fixture. It does not
implement or prove a new streaming validator, nor access original respondents.
Execute: python PYAT_CONTROL_ROOM/FINAL_PRODUCTION_ARCHITECTURE_HQ_20261028_R1/DESIGN/ORACLES/p01_s2_control_oracle.py
Requires pytest to import the existing test module.
"""
from __future__ import annotations
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import runpy
import sys

repo = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(repo))
fixture = runpy.run_path(str(repo / "rawlsing_next/tests/test_pre553_c11_repository_ingest.py"))["_candidate"]
from rawlsing_next.pre553_c11_ingest import (
    _candidate_projection, _candidate_projection_semantic_hash,
    _all_nonmanifest_refs, build_candidate_replay_manifest,
    validate_c11_source_release, C11IngestValidationError,
)
from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash, ExactRef
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository

def canon_sections_stream_hash(c):
    """Separately stream canonical candidate projection without building a dict of ref dicts."""
    sections = {
        "empirical_universes": c.empirical_universes,
        "respondent_identities": c.respondent_identities,
        "question_variable_bindings": c.question_variable_bindings,
        "respondent_events": c.respondent_events,
        "routing_eligibility_facts_or_exact_rules": c.routing_eligibility_facts_or_exact_rules,
        "empirical_coordinate_facts": c.empirical_coordinate_facts,
        "weight_measure_facts_or_typed_absence": c.weight_measure_facts_or_typed_absence,
        "authority_snapshots": c.authority_snapshots,
        "source_universe_relations_or_explicit_distinct_default": c.source_universe_relations_or_explicit_distinct_default,
        "predicate_replay_bindings_when_retained_objects_require_them": c.predicate_replay_bindings_when_retained_objects_require_them,
        "comparator_replay_bindings_or_typed_deferred_state": c.comparator_replay_bindings_or_typed_deferred_state,
        "discovery_branch_replay_bindings_or_typed_deferred_state": c.discovery_branch_replay_bindings_or_typed_deferred_state,
        "structural_admission_replay_bindings_or_typed_not_applicable_state": c.structural_admission_replay_bindings_or_typed_not_applicable_state,
    }
    values = {
        "source_release_manifest": c.source_release_manifest.semantic_projection(),
        "ingest_contract_version": "PRE553_C11_INGEST@1.0.0",
    }
    sha = hashlib.sha256()
    def w(s): sha.update(s.encode("utf-8"))
    w("{")
    for i,key in enumerate(sorted((*sections, *values))):
        if i: w(",")
        w(canonical_json(key)); w(":")
        if key in values: w(canonical_json(values[key])); continue
        v = sections[key]
        if isinstance(v, TypedAbsence): w(canonical_json(v.as_dict())); continue
        w("[")
        for j, ref in enumerate(sorted((o.ref for o in v), key=lambda r:r.key)):
            if j: w(",")
            w(canonical_json(ref.as_dict()))
        w("]")
    w("}")
    return sha.hexdigest()

def full_manifest_stream_hash(m):
    """Same @1.0.0 logical record; stream exact closure array, not digest substitution."""
    proj=m.semantic_projection()
    sha=hashlib.sha256()
    def w(s): sha.update(s.encode("utf-8"))
    w("{")
    for i,key in enumerate(sorted(proj)):
        if i:w(",")
        w(canonical_json(key));w(":")
        if key!="semantic_fields":w(canonical_json(proj[key]));continue
        w("{")
        for j,k in enumerate(sorted(proj[key])):
            if j:w(",")
            w(canonical_json(k));w(":")
            if k!="closure_refs":w(canonical_json(proj[key][k]));continue
            w("[")
            for a,ref in enumerate(m.closure_refs):
                if a:w(",")
                w(canonical_json(ref.as_dict()))
            w("]")
        w("}")
    w("}")
    return sha.hexdigest()

def raises(fn, description):
    try:fn()
    except Exception as e:
        return {"name":description,"exception":type(e).__name__,
                "disposition":str(getattr(e,"disposition","n/a")),"message":str(e)[:180]}
    raise AssertionError("UNEXPECTED_ACCEPT:"+description)

def seal(c):
    old=c.candidate_replay_manifest
    m=build_candidate_replay_manifest(
        replace(c,candidate_replay_manifest=None),
        replay_protocol_authority_ref=old.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=old.deterministic_tie_order_rules_ref,
        replay_protocol_version=old.replay_protocol_version)
    return replace(c,candidate_replay_manifest=m)

def main():
    cases=[]
    for tag in ("p01-alpha", "p01-ñΩ中"):
        for order in (("e1","e2"),("e2","e1")):
            c=fixture(tag,event_order=order)
            expected=semantic_hash(_candidate_projection(c))
            assert _candidate_projection_semantic_hash(c)==expected==canon_sections_stream_hash(c)
            m=c.candidate_replay_manifest
            assert m.closure_refs==_all_nonmanifest_refs(c)
            assert m.content_hash==full_manifest_stream_hash(m)
            release=validate_c11_source_release(c)
            repo=C11Repository((release,))
            assert repo.resolve_release_exact(release.release_ref)==release
            assert all(repo.resolve_object_exact(o.ref)==o for o in (*release.public_objects,*release.internal_records,release.replay_manifest))
            cases.append({"tag":tag,"order":order,"release":release.semantic_release_hash,"replay":m.content_hash})
    assert cases[0]["release"]==cases[1]["release"]
    assert cases[2]["release"]==cases[3]["release"]
    c=fixture("p01-negative")
    negatives=[
        raises(lambda:validate_c11_source_release(replace(c,routing_eligibility_facts_or_exact_rules=())), "missing routing"),
        raises(lambda:validate_c11_source_release(replace(c,candidate_replay_manifest=replace(c.candidate_replay_manifest,closure_refs=c.candidate_replay_manifest.closure_refs[:-1]))),"bad replay closure"),
    ]
    doubled=replace(c, respondent_events=c.respondent_events + (c.respondent_events[0],))
    counts={**dict(c.source_release_manifest.declared_record_counts_by_logical_family),"RespondentEvent":len(doubled.respondent_events)}
    doubled=seal(replace(doubled,source_release_manifest=replace(c.source_release_manifest,declared_record_counts_by_logical_family=counts)))
    negatives.append(raises(lambda: validate_c11_source_release(doubled), "duplicate occurrence with updated count/replay"))
    # Demonstrates a limit of I02 alone, NOT a full source-backed source-byte proof.
    mismatch=replace(c,source_release_manifest=replace(c.source_release_manifest,
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT","urn:fixture:wrong-retention",
                                            hashlib.sha256(b"wrong").hexdigest())))
    mismatch=seal(mismatch)
    mismatch_release=validate_c11_source_release(mismatch)
    assert mismatch_release.source_artifact_ref.content_hash != mismatch.source_release_manifest.source_snapshot_retention_ref.content_hash
    print(json.dumps({"status":"SOURCEFREE_ORACLE_PASS","valid_cases":cases,
                      "negative_cases":negatives,
                      "I02_only_retention_mismatch_accepted":True,
                      "warning":"not a new streaming validator or original source run"},
                     ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":main()
