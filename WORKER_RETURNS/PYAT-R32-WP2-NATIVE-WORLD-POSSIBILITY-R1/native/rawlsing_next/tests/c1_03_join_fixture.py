"""Join integration fixture for the C1-03 three-trunk join.

Builds REAL accepted source-free artifacts from the three adopted trunks and wires
them into the REAL C1-03R lifecycle owner. Nothing here fabricates an accepted
identity: every dependent ref is an exact ref an accepted owner actually produced.
"""
from __future__ import annotations

from typing import Any

from rawlsing_next.pre553_authority_maintenance import (
    NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    NoncurrentDependentOutcome,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.tests import c1_at18_at19_fixture as at19
from rawlsing_next.tests import n10e_empirical_slice_fixture as n10e


def at17_provider_product(direction: str = "forward"):
    """One real AT17 provider product, driven through the public entry point."""
    case = n10e.build_provider_case(direction)
    kwargs = {
        "repository": case["source"]["repo"],
        "empirical_query": case["empirical_query"],
        "predicate": case["predicate"],
        "authority_registry": case["registry"],
        "release_refs": case["release_refs"],
        "consumer_query": case["consumer_query"],
        "model_rule": case["model_rule"],
        "condition_binding_witness": case["condition_binding_witness"],
    }
    return case, provide_empirical_possibility_slice(**kwargs)


def at17_generated_evidence_ref(result: Any) -> ExactRef:
    """The real exact ref of the provider-generated slice evidence."""
    evidence = result.generated_evidence_or_null
    assert evidence is not None and evidence.evidence_ref is not None
    return evidence.evidence_ref


def at17_composed_result_ref(result: Any) -> ExactRef:
    """A real exact ref anchored on the AT17 composition identity hash."""
    return ExactRef(
        "C1_ANALYTICAL_COMPOSED_RESULT@1",
        "urn:c1-03-join:at17:composed",
        result.composition_result.composed_result_identity_hash,
    )


def a_forward_composition():
    """A's accepted AT16 real composition on the 54/6 attitude grain."""
    from rawlsing_next.tests import c1_at08_at13_fixture as c1
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _query_authority,
        _registry,
    )

    tag = "c1-03-join-at16"
    source = c1.attitude_fixture(tag)
    qauth = _query_authority(tag)
    registry = _registry(source, qauth)
    composed, consumer_query, witness, query, predicate = (
        c1.direct_condition_composition(
            source=source, qauth=qauth, registry=registry,
            conditions=[("RESPONSE", "ATT1", "agree")],
            target_question="ATT2",
            tag="joinat16",
            target_domain=[["support", "oppose"]],
        )
    )
    return {
        "source": source, "qauth": qauth, "registry": registry,
        "composition": composed, "consumer_query": consumer_query,
        "witness": witness, "query": query, "predicate": predicate,
    }


def a_composed_result_ref(composition: Any) -> ExactRef:
    """A real exact ref anchored on A's own composition identity hash."""
    return ExactRef(
        "C1_ANALYTICAL_COMPOSED_RESULT@1",
        "urn:c1-03-join:a:composed",
        composition.composed_result_identity_hash,
    )


def real_accepted_dependents() -> dict[str, ExactRef]:
    """Three DISTINCT real accepted refs usable as R lifecycle dependents.

    - replaced:  the AT17 provider's real generated evidence ref
    - noncurrent: the AT17 provider's real composed-result identity ref
    - sibling:   A's own real composition identity ref on the reverse grain
    """
    _, at17 = at17_provider_product("forward")
    a_forward = a_forward_composition()
    deps = {
        "replaced": at17_generated_evidence_ref(at17),
        "noncurrent": at17_composed_result_ref(at17),
        # A's own real composition identity on its own AT16 grain.
        "sibling": a_composed_result_ref(a_forward["composition"]),
    }
    assert len({d.key for d in deps.values()}) == 3, "dependents must be distinct"
    return deps


def join_transition(deps: dict[str, ExactRef]):
    """A real R transition whose graph dependents are the real accepted refs above."""
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityMaintenanceExecutor,
        SemanticDeterminantGraph,
    )

    old_snapshot = at19.model_authority_snapshot("forward")
    old_auth = old_snapshot.authority_ref
    sibling_auth = at19.direction_model_authority("reverse")
    graph = SemanticDeterminantGraph(
        authority_edges=(
            (old_auth, deps["replaced"]),
            (old_auth, deps["noncurrent"]),
            (sibling_auth, deps["sibling"]),
        ),
        dependency_edges=(),
        known_dependent_refs=(deps["replaced"], deps["noncurrent"], deps["sibling"]),
    )
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(old_snapshot,),
        initial_current_selection={old_auth.authority_id: old_auth},
        determinant_graph=graph,
    )
    policy = ExactRef(
        "JOIN_NO_REPLACEMENT_POLICY@1", "urn:c1-03-join:no-replacement-source", "e" * 64)
    return {
        "executor": executor,
        "policy": policy,
        "old_snapshot": old_snapshot,
        "old_auth": old_auth,
        "sibling_auth": sibling_auth,
        "declarations": {
            deps["noncurrent"].key: NoncurrentDependentOutcome(
                old_ref=deps["noncurrent"],
                disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
                reason_code="NO_LAWFUL_REPLACEMENT_SOURCE",
                supporting_refs=(policy,),
            )
        },
    }


def join_seal(executor, old_snapshot):
    """Adjudicate + seal a real governed successor on the join authority."""
    old_auth = old_snapshot.authority_ref
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityCandidate,
        AuthorityEvidenceReceipt,
    )

    evidence = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(ExactRef("JOIN_EVID@1", "urn:c1-03-join:ev", "2" * 64),),
        provenance_refs=(ExactRef("JOIN_PROV@1", "urn:c1-03-join:pv", "3" * 64),),
        source_release_refs=(),
    )
    executor.intake_evidence(evidence)
    candidate = AuthorityCandidate(
        candidate_id="JOIN_CANDIDATE",
        candidate_revision=1,
        authority_id=old_auth.authority_id,
        authority_version="2.0.0",
        authority_kind=old_snapshot.authority_kind,
        proposed_decision_state="ALLOW",
        governed_operations=old_snapshot.governed_operations,
        governed_object_families=old_snapshot.governed_object_families,
        scope_envelope=dict(old_snapshot.scope_envelope),
        effective_time_or_interval=old_snapshot.effective_time_or_interval,
        interpretation_semantics={"join": "c1-03", "generation": 2},
        replay_protocol_ref=old_snapshot.replay_protocol_ref,
        evidence_receipt_refs=(evidence.ref,),
        proposed_parent_authority_refs=(old_auth,),
        proposed_negative_limit_refs=(),
        proposed_supersession_refs=(old_auth,),
    )
    executor.intake_candidate(candidate)
    adjudication = executor.adjudicate_candidate(
        candidate.ref,
        decision="APPROVED",
        adjudicator_ref=ExactRef("JOIN_ADJ@1", "urn:c1-03-join:adj", "4" * 64),
        adjudication_authority_ref=ExactRef(
            "JOIN_GOV@1", "urn:c1-03-join:gov", "5" * 64),
        findings_ref=ExactRef("JOIN_FIND@1", "urn:c1-03-join:find", "6" * 64),
    )
    return executor.seal_revision(
        candidate.ref,
        adjudication.ref,
        seal_attestation_ref=ExactRef(
            "JOIN_SEALATT@1", "urn:c1-03-join:sealatt", "7" * 64),
    ).ref


def join_recompiler(deps: dict[str, ExactRef], tag: str):
    """A deterministic recompiler that only rebuilds the designated dependent."""
    replaced_key = deps["replaced"].key

    def recompiler(old_ref: ExactRef, changed) -> ExactRef:
        assert old_ref.key == replaced_key, "only the replaced dependent recompiles"
        return ExactRef(
            "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1",
            old_ref.object_id,
            semantic_hash({"join": tag, "old": old_ref.key}),
        )

    return recompiler


__all__ = [
    "at17_provider_product",
    "at17_generated_evidence_ref",
    "at17_composed_result_ref",
    "a_forward_composition",
    "a_composed_result_ref",
    "real_accepted_dependents",
    "join_transition",
    "join_seal",
    "join_recompiler",
]
