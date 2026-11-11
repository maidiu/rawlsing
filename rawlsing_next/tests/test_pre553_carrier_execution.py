from dataclasses import fields

import pytest

from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError,
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
    bind_governed_c11_projection,
    bind_repository_builder,
)
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
    _registry,
    _run,
)


def test_governed_projection_binding_requires_complete_explicit_contract_and_delegates_validation():
    required = tuple(field.name for field in fields(GovernedC11Projection))
    with pytest.raises(CarrierExecutionBindingError, match="complete and exact"):
        bind_governed_c11_projection({})

    hostile_complete = {name: None for name in required}
    with pytest.raises(CarrierExecutionBindingError, match="rejected by existing contract"):
        bind_governed_c11_projection(hostile_complete)


def test_repository_builder_binding_accepts_standard_c11_repository_release_prefix():
    source = _build_source(
        "ee-p2r1-builder",
        [
            {"id": "R1", "responses": {"Y": 0}},
            {"id": "R2", "responses": {"Y": 1}},
        ],
    )
    release = source["repo"].resolve_release_exact(source["release_ref"])

    def accepted_owner_builder():
        return source["repo"], release, {"owner_descriptor": "PRESERVED"}

    catalog = RuntimeObjectCatalog(
        authorities=(),
        predicates=(),
        queries=(),
        discovery_authorities=(),
    )
    binding = bind_repository_builder(
        repository_builder=accepted_owner_builder,
        builder_kwargs={},
        builder_identity={
            "composition_kind": "ACCEPTED_OWNER_TO_COMMON_EXECUTOR",
            "owner_semantics_changed": False,
        },
        runtime_catalog=catalog,
    )
    assert binding.executor.repository.resolve_release_exact(binding.release_ref).release_ref == binding.release_ref
    receipt = binding.receipt()
    assert receipt["candidate_semantic_branching"] is False
    assert receipt["release_ref"] == binding.release_ref.as_dict()


def test_carrier_neutral_executor_i03_is_identity_equal_to_existing_exact_engine():
    source = _build_source(
        "ee-p2r1-i03",
        [
            {"id": "R1", "responses": {"Y": 0}},
            {"id": "R2", "responses": {"Y": 1}},
        ],
    )
    qauth = _query_authority("ee-p2r1-i03")
    predicate = _branch_predicate(source, qauth)
    query = _query(source, qauth, predicate, ("Y",), tag="ee-p2r1-i03")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(),
    )
    executor = CarrierNeutralResearchExecutor(
        repository=source["repo"],
        release_refs=(source["release_ref"],),
        runtime_catalog=catalog,
    )
    expected = _run(source, qauth, predicate, query, registry=_registry(source, qauth))
    observed = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
    assert observed.query_ref == expected.query_ref
    assert observed.release_refs == expected.release_refs
    assert tuple(f.ref for f in observed.facts) == tuple(f.ref for f in expected.facts)
    assert tuple(f.semantic_projection() for f in observed.facts) == tuple(
        f.semantic_projection() for f in expected.facts
    )


def test_carrier_neutral_executor_rejects_query_predicate_substitution():
    source = _build_source(
        "ee-p2r1-hostile",
        [
            {"id": "R1", "responses": {"Y": 0}},
            {"id": "R2", "responses": {"Y": 1}},
        ],
    )
    qauth = _query_authority("ee-p2r1-hostile")
    expected_predicate = _branch_predicate(source, qauth, tag="expected")
    wrong_predicate = _branch_predicate(source, qauth, members=(), tag="wrong")
    query = _query(source, qauth, expected_predicate, ("Y",), tag="ee-p2r1-hostile")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qauth)),
        predicates=(expected_predicate, wrong_predicate),
        queries=(query,),
        discovery_authorities=(),
    )
    executor = CarrierNeutralResearchExecutor(
        repository=source["repo"],
        release_refs=(source["release_ref"],),
        runtime_catalog=catalog,
    )
    with pytest.raises(CarrierExecutionBindingError):
        executor.execute_i03(query_ref=query.ref, predicate_ref=wrong_predicate.ref)
