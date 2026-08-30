import hashlib
import json
import subprocess
import sys

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, Pre553IntegrityError
from rawlsing_next.pre553_component_authority_vector import (
    FAMILY,
    ComponentAuthorityBinding,
    authoritative_value_digest,
    build_component_authority_vector_receipt,
    reload_component_authority_vector_receipt,
)
from rawlsing_next import m4_v557_v558_publication_repository as m4


def _h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind, object_id, _h(f"{kind}|{object_id}"))


def _auth(authority_id: str) -> AuthorityRef:
    return AuthorityRef(authority_id, "1.0.0", _h(f"authority|{authority_id}"))


def _binding(component_id: str, *, value=None, state="VALUE", producer="V551J",
             ordinal=1, role="MEMBER", negative_refs=()):
    return ComponentAuthorityBinding(
        component_id=component_id,
        component_ref=_ref(f"{producer}_COMPONENT", component_id),
        producer_family=producer,
        role=role,
        ordinal_or_null=ordinal,
        multiplicity_index=0,
        authority_state=state,
        authoritative_value_digest=authoritative_value_digest(value) if state == "VALUE" else None,
        value_authority_ref=_auth("COMPONENT_VALUE_AUTHORITY"),
        negative_or_limit_refs=tuple(negative_refs),
    )


def _receipt(bindings, governed=("c1", "c2")):
    return build_component_authority_vector_receipt(
        vector_subject_ref=_ref("VECTOR_SUBJECT", "packet-1"),
        authority_dimension_contract_ref=_ref("AUTHORITY_DIMENSION", "finite-stratum"),
        vector_rule_authority_ref=_auth("COMPONENT_VECTOR_SCALARIZATION_RULE"),
        governed_component_ids=governed,
        component_bindings=bindings,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "component-vector-root"),
    )


def test_complete_heterogeneous_stays_vector():
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", value="stratum:B", producer="V552", ordinal=2),
    ])
    assert r.complete_coverage is True
    assert r.all_governed_components_nonempty is True
    assert r.unanimous_authoritative_value is False
    assert r.projection_disposition == "VECTOR_HETEROGENEOUS_COMPLETE"
    assert r.scalar_value_digest is None


def test_incomplete_unanimous_subset_cannot_scalarize():
    r = _receipt([_binding("c1", value="stratum:A", ordinal=1)])
    assert r.complete_coverage is False
    assert r.missing_component_ids == ("c2",)
    assert r.projection_disposition == "VECTOR_INCOMPLETE_COVERAGE"
    assert r.scalar_value_digest is None


def test_governed_empty_cannot_scalarize():
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", state="GOVERNED_EMPTY", producer="V552", ordinal=2),
    ])
    assert r.complete_coverage is True
    assert r.governed_empty_component_ids == ("c2",)
    assert r.projection_disposition == "VECTOR_GOVERNED_EMPTY_COMPONENT"
    assert r.scalar_value_digest is None


@pytest.mark.parametrize("state", ["DENIED", "NONCOMPARABLE"])
def test_denied_or_noncomparable_cannot_scalarize(state):
    negative = _ref("NEGATIVE_AUTHORITY", state.lower())
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", state=state, producer="V552", ordinal=2, negative_refs=(negative,)),
    ])
    assert r.complete_coverage is True
    assert r.projection_disposition == "VECTOR_DENIED_OR_NONCOMPARABLE_COMPONENT"
    assert r.scalar_value_digest is None
    assert negative in r.negative_or_limit_refs


def test_complete_unanimous_nonempty_scalarizes_but_retains_vector():
    a = authoritative_value_digest("stratum:A")
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", value="stratum:A", producer="V552", ordinal=2),
    ])
    assert r.complete_coverage and r.all_governed_components_nonempty
    assert r.unanimous_authoritative_value is True
    assert r.projection_disposition == "SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY"
    assert r.scalar_value_digest == a
    assert len(r.component_bindings) == 2


def test_ambiguous_duplicate_binding_is_incomplete_not_consensus():
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c1", value="stratum:A", producer="V552", ordinal=1),
        _binding("c2", value="stratum:A", producer="V552", ordinal=2),
    ])
    assert r.ambiguous_component_ids == ("c1",)
    assert r.projection_disposition == "VECTOR_INCOMPLETE_COVERAGE"
    assert r.scalar_value_digest is None


def test_fresh_process_reload_reproduces_identity_and_projection(tmp_path):
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", value="stratum:A", producer="V552", ordinal=2),
    ])
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(r.as_dict(), sort_keys=True), encoding="utf-8")
    code = (
        "import json,sys; "
        "from rawlsing_next.pre553_component_authority_vector import reload_component_authority_vector_receipt as rr; "
        "x=rr(json.load(open(sys.argv[1],encoding='utf-8'))); "
        "print(json.dumps({'id':x.object_id,'hash':x.content_hash,'disposition':x.projection_disposition,'scalar':x.scalar_value_digest},sort_keys=True))"
    )
    got = json.loads(subprocess.check_output([sys.executable, "-c", code, str(path)], text=True))
    assert got == {
        "id": r.object_id,
        "hash": r.content_hash,
        "disposition": r.projection_disposition,
        "scalar": r.scalar_value_digest,
    }


def test_reload_rejects_tampered_derived_scalar():
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", value="stratum:B", producer="V552", ordinal=2),
    ])
    raw = r.as_dict()
    raw["scalar_value_digest"] = authoritative_value_digest("stratum:A")
    with pytest.raises(Pre553IntegrityError):
        reload_component_authority_vector_receipt(raw)


def _m4_authority(name):
    return m4.AuthorityRef(name, "1.0.0", _h(f"m4-authority|{name}"))


def _locator(obj, gov, name):
    return m4.make_producer_locator(
        obj, gov,
        logical_collection_kind="MX02_R2_COMPONENT_VECTOR_FIXTURE",
        authoritative_build_id=f"build:{name}",
        authoritative_build_hash=_h(f"build|{name}"),
        producer_contract_id=f"contract:{name}",
        producer_contract_version="1.0.0",
        producer_contract_hash=_h(f"contract|{name}"),
    )


def test_mixed_producer_repository_preserves_receipt_and_component_owners():
    r = _receipt([
        _binding("c1", value="stratum:A", ordinal=1),
        _binding("c2", value="stratum:B", producer="V552", ordinal=2),
    ])
    c1, c2 = r.component_bindings
    c1_obj = m4.StructuralObject(
        c1.producer_family, c1.component_ref.kind, c1.component_ref.object_id,
        c1.component_ref.content_hash, "V551J_COMPONENT", "2.2.3", c1.authority_state,
        ("REVIEW", "CONTEXT"), None, "MX02_R2_COMPONENT_PRODUCER",
    )
    c2_obj = m4.StructuralObject(
        c2.producer_family, c2.component_ref.kind, c2.component_ref.object_id,
        c2.component_ref.content_hash, "V552_COMPONENT", "2.1", c2.authority_state,
        ("REVIEW", "CONTEXT"), None, "MX02_R2_COMPONENT_PRODUCER",
    )
    receipt_obj = m4.StructuralObject(
        "PRE553_COMMON", FAMILY, r.object_id, r.content_hash, r.schema_id, r.schema_version,
        r.projection_disposition, ("REVIEW", "CONTEXT"), None,
        "PRE553_COMPONENT_AUTHORITY_VECTOR",
        (c1_obj.ref, c2_obj.ref), (),
    )
    root_obj = m4.make_structural_object(
        producer_family="V554", semantic_class="F1", object_id="mx02-r2-publication-root",
        schema_id="SCR554_MX02_R2_FIXTURE", schema_version="1.0.0",
        typed_state="MX02_R2_FIXTURE_ROOT", producer_allowed_uses=("REVIEW", "CONTEXT"),
        payload={"fixture":"mx02-r2-component-vector-publication-root"},
        source_stage="MX02_R2_TEST", required_dependency_refs=(receipt_obj.ref,),
    )
    objs = (root_obj, receipt_obj, c1_obj, c2_obj)
    govs = [m4.govern_v557(o, decision_state=m4.V557DecisionState.ALLOW_CONTEXT_ONLY,
                           v557_allowed_uses=("REVIEW", "CONTEXT"),
                           authority_ref=_m4_authority(f"gov-{i}")) for i,o in enumerate(objs)]
    locs = [_locator(o,g,f"o{i}") for i,(o,g) in enumerate(zip(objs,govs))]
    entries = [m4.RepositoryEntry(o,g,l) for o,g,l in zip(objs,govs,locs)]
    publication = m4.build_v557_publication_bundle((m4.V557PublicationEntry(root_obj, govs[0]),))
    edge_auth = _m4_authority("component-vector-reference")
    edges = [
        m4.make_reference_edge(locs[0], locs[1], reference_contract=edge_auth,
            edge_role="COMPONENT_VECTOR_RECEIPT", declared_cardinality="1"),
        m4.make_reference_edge(locs[1], locs[2], reference_contract=edge_auth,
            edge_role="COMPONENT", participant_role=c1.role, declared_cardinality="2",
            multiplicity_key=str(c1.multiplicity_index), order_significant=True,
            semantic_ordinal=c1.ordinal_or_null),
        m4.make_reference_edge(locs[1], locs[3], reference_contract=edge_auth,
            edge_role="COMPONENT", participant_role=c2.role, declared_cardinality="2",
            multiplicity_key=str(c2.multiplicity_index), order_significant=True,
            semantic_ordinal=c2.ordinal_or_null),
    ]
    external = [m4.make_external_resolution_binding(o, resolver_authority=_m4_authority(f"resolve-{i}"))
                for i,o in enumerate((receipt_obj,c1_obj,c2_obj), start=1)]
    repo = m4.build_v558_repository_bundle(
        publication, entries, reference_edges=edges, external_bindings=external,
    )
    by_id = {e.obj.object_id:e for e in repo.entries}
    assert by_id[r.object_id].obj.producer_family == "PRE553_COMMON"
    assert by_id[c1.component_ref.object_id].obj.producer_family == "V551J"
    assert by_id[c2.component_ref.object_id].obj.producer_family == "V552"
    component_edges = sorted((e for e in repo.reference_edges if e.edge_role == "COMPONENT"),
                             key=lambda e:e.semantic_ordinal)
    assert [e.semantic_ordinal for e in component_edges] == [1,2]
    assert all(e.order_significant and e.declared_cardinality == "2" for e in component_edges)
    assert all(set(e.governance.v557_allowed_uses) <= set(e.obj.producer_allowed_uses) for e in repo.entries)
