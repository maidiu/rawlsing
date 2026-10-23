from __future__ import annotations

import pytest

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_SCHEMA,
    CACHE_SEAL_ALGORITHM,
    EvidenceBindingError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceResolver,
    _evidence_material,
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    build_consumer,
    build_model_rule,
    build_producer,
    build_provider_case,
    build_witness,
    frozen_at07_source,
)
from rawlsing_next.tests.test_universal_evidence_binding import (
    _binding,
    _condition,
    _ref,
    _request,
)


def _rebind(case, request):
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    return resolver.resolve(request)


def test_wrong_condition_rebind_must_not_authenticate_p1_producer():
    case = build_provider_case("forward")
    request = _request(
        case,
        conditions=(_condition("POSITION", "P2", "P2", "position"),),
        request_id="r08v-hostile-wrong-condition",
    )
    result = _rebind(case, request)
    assert result.result_state != "SUPPORTED", (
        "request K names POSITION occurrence/value P2 but the bound actual "
        f"producer is P1; got {result.result_state}, denominator {result.denominator}, "
        f"values={result.consumer_values_read}"
    )


def test_wrong_typed_value_rebind_must_not_authenticate_p1_producer():
    case = build_provider_case("forward")
    request = _request(
        case,
        conditions=(_condition("POSITION", "P1", True, "position"),),
        request_id="r08v-hostile-wrong-typed-value",
    )
    result = _rebind(case, request)
    assert result.result_state != "SUPPORTED", (
        "request K names a BOOLEAN True condition value but the bound actual "
        f"producer conditions on string P1; got {result.result_state}, "
        f"denominator {result.denominator}"
    )


def test_null_and_integer_value_rebind_must_not_authenticate_p1_producer():
    case = build_provider_case("forward")
    for index, value in enumerate((None, 1)):
        request = _request(
            case,
            conditions=(_condition("POSITION", "P1", value, "position"),),
            request_id=f"r08v-hostile-wrong-scalar-{index}",
        )
        result = _rebind(case, request)
        assert result.result_state != "SUPPORTED", (
            f"request K names typed value {value!r} but the bound actual "
            f"producer conditions on string P1; got {result.result_state}"
        )


def test_wrong_edition_direction_role_design_clock_rebind_must_refuse():
    case = build_provider_case("forward")
    request = _request(
        case,
        edition="2025-12",
        byte_digest=semantic_hash({"fixture": "r08v-other-edition"}),
        as_of_clock="2026-02-28",
        direction="ANSWER_YES_TO_POSITION",
        role="REVERSE_AUTHORIZED",
        design_ref=_ref("R61_DESIGN", "r08v-other-design", {"design": "OTHER"}),
        weight_method="GOVERNED_WEIGHTED",
        source_id="R08V_OTHER_SOURCE",
        request_id="r08v-hostile-labels",
    )
    result = _rebind(case, request)
    assert result.result_state != "SUPPORTED", (
        "request K changed edition/digest/as-of/direction/role/design/weight/"
        "source but the same forward P1 actual producer was accepted; "
        f"got {result.result_state}, denominator {result.denominator}"
    )


def test_extra_and_reordered_conditions_must_refuse():
    case = build_provider_case("forward")
    first = _condition("POSITION", "P1", "P1", "position")
    second = _condition("ANSWER", "yes", "yes", "answer")
    for index, conditions in enumerate(((first, second), (second, first))):
        request = _request(
            case,
            conditions=conditions,
            request_id=f"r08v-hostile-ordered-{index}",
        )
        result = _rebind(case, request)
        assert result.result_state != "SUPPORTED", (
            "a request with an extra/reordered condition tuple was bound to the "
            f"single-conditioner P1 producer; got {result.result_state}, "
            f"values={result.consumer_values_read}"
        )


def _forge_cross_source_cache(victim_request, other_result):
    actual = evaluate_positioned_subject_possibility(
        query=other_result.consumer_query_object,
        rule=other_result.model_rule_object,
        evidence=(other_result.evidence_object,),
    )
    forged_cell = {
        "cell": "yes",
        "cell_state": "SUPPORTED",
        "raw_numerator_support": 999,
        "raw_probability_exact_fraction": {"$exact_fraction": [1, 1]},
    }
    forged_values = {
        "schema": "R61_EVIDENCE_CONSUMER_VALUES_READ@1",
        "request_key": victim_request.key,
        "target_ref": victim_request.target_ref.as_dict(),
        "ordered_conditions": [
            condition.material() for condition in victim_request.ordered_conditions
        ],
        "direction": victim_request.direction,
        "role": victim_request.role,
        "consumer_query_ref": victim_request.consumer_query_ref.as_dict(),
        "evidence_ref": other_result.evidence_ref.as_dict(),
        "result_state": actual.result_state,
        "result_hash": actual.result_hash,
        "retained_conditioner_ids": list(
            other_result.evidence_object.retained_conditioner_ids
        ),
        "denominator": 999,
        "cells": [canonicalize(forged_cell)],
        "model_rule_hash": victim_request.model_rule_hash,
    }
    result_material = dict(other_result.material())
    result_material.update(
        {
            "request_key": victim_request.key,
            "denominator": 999,
            "cells": [canonicalize(forged_cell)],
            "evidence_ref": other_result.evidence_ref.as_dict(),
            "consumer_query_ref": victim_request.consumer_query_ref.as_dict(),
            "consumer_result_state": actual.result_state,
            "consumer_result_hash": actual.result_hash,
            "consumer_values_read": forged_values,
        }
    )
    payload = {
        "schema": CACHE_SCHEMA,
        "seal_algorithm": CACHE_SEAL_ALGORITHM,
        "request_key": victim_request.key,
        "result": canonicalize(result_material),
        "evidence": _evidence_material(other_result.evidence_object),
        "consumer_query": canonicalize(
            other_result.consumer_query_object.material()
        ),
        "model_rule": canonicalize(other_result.model_rule_object.material()),
    }
    return {
        "schema": CACHE_SCHEMA,
        "entries": [{**payload, "seal": semantic_hash(payload)}],
    }


def test_self_sealed_cross_source_cache_forgery_must_refuse():
    case = build_provider_case("forward")
    victim_request = _request(case, request_id="r08v-hostile-cache-victim")
    victim_resolver = EvidenceResolver()
    victim_resolver.bind(_binding(victim_request, case))
    assert victim_resolver.resolve(victim_request).result_state == "SUPPORTED"

    other_case = build_provider_case("forward", variant="CHANGED_SOURCE_LAW")
    other_request = _request(other_case, request_id="r08v-hostile-cache-other")
    other_resolver = EvidenceResolver()
    other_resolver.bind(_binding(other_request, other_case))
    other_result = other_resolver.resolve(other_request)
    assert other_result.result_state == "SUPPORTED"
    assert other_result.denominator == 70

    forged = _forge_cross_source_cache(victim_request, other_result)
    cold = EvidenceResolver()
    try:
        cold.import_authenticated_cache(forged)
    except EvidenceCacheIntegrityError:
        return
    restored = cold.resolve(victim_request)
    assert restored.result_state != "SUPPORTED", (
        "self-sealed cache bound the victim K to the changed-source producer/"
        "evidence and resolved SUPPORTED"
    )
    assert restored.denominator != 999, (
        "self-sealed cache served forged denominator 999 through the intended "
        "public API and actual consumer reader"
    )
    values = EvidenceConsumerReader(victim_request, restored).read()
    assert values["denominator"] != 999


def test_cache_entry_must_carry_full_k_not_only_hash():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-hostile-cache-preimage")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    resolver.resolve(request)
    entry = resolver.export_cache()["entries"][0]
    assert any(
        key in entry for key in ("request", "request_material", "request_preimage")
    ), (
        "cache entry carries only request_key plus result/evidence/query/rule; "
        "it has no full K preimage to verify the producer association"
    )


def _observed_zero_case():
    rows = [
        {"id": f"P1Y{n:03d}", "responses": {"POSITION": "P1", "ANSWER": "yes"}}
        for n in range(1, 61)
    ] + [
        {"id": f"P2N{n:03d}", "responses": {"POSITION": "P2", "ANSWER": "no"}}
        for n in range(1, 41)
    ]
    with frozen_at07_source(
        tag="r08v-observed-zero",
        rows=rows,
        scope_query_authority_to_universe=True,
    ) as (source, query_authority, registry):
        predicate, producer_query = build_producer(source, query_authority, "forward")
        consumer_query, conditioner_binding = build_consumer(source, "forward")
        witness = build_witness(
            source,
            "forward",
            consumer_query,
            conditioner_binding,
            producer_query,
            predicate,
        )
        model_rule = build_model_rule(source)
        return {
            "source": source,
            "query_authority": query_authority,
            "registry": registry,
            "predicate": predicate,
            "empirical_query": producer_query,
            "consumer_query": consumer_query,
            "conditioner_binding": conditioner_binding,
            "condition_binding_witness": witness,
            "model_rule": model_rule,
            "release_refs": (source["release_ref"],),
        }


def test_observed_zero_with_positive_denominator_is_typed_not_crash_or_zero_support():
    case = _observed_zero_case()
    request = _request(case, request_id="r08v-hostile-observed-zero")
    try:
        result = _rebind(case, request)
    except EvidenceBindingError as exc:
        pytest.fail(
            "observed-zero (positive denominator, zero target cell) raised "
            f"{type(exc).__name__}: {exc}"
        )
    assert result.denominator == 60
    assert result.result_state in {"SUPPORTED", "OBSERVED_ZERO"}, (
        "observed zero with positive denominator was collapsed to "
        f"{result.result_state!r} denominator {result.denominator!r}"
    )
