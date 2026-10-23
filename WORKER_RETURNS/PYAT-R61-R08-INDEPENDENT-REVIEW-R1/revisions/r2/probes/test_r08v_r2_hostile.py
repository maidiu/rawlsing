from __future__ import annotations

import json
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.source_backed_positioned_subject_possibility import (
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_SCHEMA,
    AdmittedEvidenceContext,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceResolver,
    _cell_core,
    _evidence_from_material,
    _evidence_material,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import (
    _binding,
    _condition,
    _make_context,
    _ref,
    _request,
)

OBSERVATIONS: dict[str, object] = {}


def _forged_context(case) -> AdmittedEvidenceContext:
    return replace(
        _make_context(case),
        source_id="FORGED_SOURCE",
        dataset_id="FORGED_DATASET",
        wave_id="FORGED_WAVE",
        edition="1999-01",
        byte_digest=semantic_hash({"forged": "source-bytes"}),
        instrument_version="FORGED_INSTRUMENT@9",
        sampled_unit="FORGED_SAMPLED_UNIT",
        reporting_unit="FORGED_REPORTING_UNIT",
        estimand="FORGED_ESTIMAND",
        weight_method="FORGED_WEIGHT_METHOD",
        design_ref=_ref("R61_DESIGN", "forged-design", {"design": "FORGED"}),
        uncertainty_method="FORGED_UNCERTAINTY_METHOD",
        direction="ANSWER_YES_TO_POSITION",
        role="REVERSE_AUTHORIZED",
        consumer_use="FORGED_CONSUMER_USE",
        grammar_version="FORGED_GRAMMAR@9",
        custody_ref=_ref("R61_CUSTODY", "forged-custody", {"custody": "FORGED"}),
        observation_clock="1999-01",
        reference_clock="1999-01",
        as_of_clock="1999-01-31",
        publication_clock="1999-02-01",
        permission_ref=_ref(
            "R61_PERMISSION", "forged-permission", {"scope": "FORGED"}
        ),
    )


def _forged_request(case):
    forged = _forged_context(case)
    case["_r61_context"] = forged
    return _request(
        case,
        request_id="r08v-r2-forged-caller-context",
        source_id=forged.source_id,
        dataset_id=forged.dataset_id,
        wave_id=forged.wave_id,
        edition=forged.edition,
        byte_digest=forged.byte_digest,
        instrument_version=forged.instrument_version,
        sampled_unit=forged.sampled_unit,
        reporting_unit=forged.reporting_unit,
        estimand=forged.estimand,
        weight_method=forged.weight_method,
        design_ref=forged.design_ref,
        uncertainty_method=forged.uncertainty_method,
        direction=forged.direction,
        role=forged.role,
        consumer_use=forged.consumer_use,
        grammar_version=forged.grammar_version,
        custody_ref=forged.custody_ref,
        observation_clock=forged.observation_clock,
        reference_clock=forged.reference_clock,
        as_of_clock=forged.as_of_clock,
        publication_clock=forged.publication_clock,
        permission_ref=forged.permission_ref,
        ordered_conditions=(
            _condition("POSITION", "P1", "P1", "position"),
        ),
    )


def test_caller_owned_context_labels_cannot_relabel_real_producer():
    case = build_provider_case("forward")
    request = _forged_request(case)
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    OBSERVATIONS["forged_context"] = {
        "result_state": result.result_state,
        "provenance": result.provenance,
        "denominator": result.denominator,
        "source_id": request.source_id,
        "edition": request.edition,
        "direction": request.direction,
        "role": request.role,
        "permission_scope": request.permission_ref.object_id,
        "consumer_accepted": None,
    }
    if result.result_state == "SUPPORTED":
        values = EvidenceConsumerReader(request, result).read()
        OBSERVATIONS["forged_context"]["consumer_accepted"] = values["denominator"]
    assert result.result_state != "SUPPORTED", (
        "caller-owned AdmittedEvidenceContext changed source/dataset/wave/edition/"
        "digest/instrument/units/estimand/weight/design/uncertainty/direction/role/"
        "consumer-use/grammar/custody/clocks/permission while the unchanged real "
        f"producer was accepted: {result.result_state}, denominator {result.denominator}"
    )
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, result).read()


def _forged_evidence_cache(produced, base, denominator=999):
    material = dict(canonicalize(_evidence_material(produced.evidence_object)))
    material["raw_support"] = denominator
    geometry = dict(material["geometry"])
    cells = []
    for raw_cell in geometry["cells"]:
        cell = dict(canonicalize(raw_cell))
        if cell.get("cell") == "yes":
            cell["raw_numerator_support"] = denominator
            cell["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 1]}
        else:
            cell["raw_numerator_support"] = 0
            cell["raw_probability_exact_fraction"] = {"$exact_fraction": [0, 1]}
        cells.append(cell)
    geometry["cells"] = cells
    material["geometry"] = geometry
    forged_evidence = _evidence_from_material(material)
    actual = evaluate_positioned_subject_possibility(
        query=produced.consumer_query_object,
        rule=produced.model_rule_object,
        evidence=(forged_evidence,),
    )
    assert actual.result_state == "EXACT_SUPPORTED"

    entry = {
        key: canonicalize(value)
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade"}
    }
    entry["evidence"] = canonicalize(material)
    result_material = dict(canonicalize(entry["result"]))
    result_material["denominator"] = denominator
    result_material["cells"] = [
        canonicalize(_cell_core(cell)) for cell in cells
    ]
    result_material["consumer_result_state"] = actual.result_state
    result_material["consumer_result_hash"] = actual.result_hash
    entry["result"] = canonicalize(result_material)
    entry["seal"] = semantic_hash(canonicalize(entry))
    return {"schema": CACHE_SCHEMA, "entries": [entry]}, actual


def test_self_sealed_same_source_denominator_999_must_refuse():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-r2-forged-cache-victim")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"
    assert produced.denominator == 60

    base = resolver.export_cache()["entries"][0]
    forged_cache, forged_actual = _forged_evidence_cache(produced, base)
    cold = EvidenceResolver()
    accepted = False
    restored = None
    try:
        cold.import_authenticated_cache(forged_cache)
        accepted = True
        restored = cold.resolve(request)
    except EvidenceCacheIntegrityError as exc:
        OBSERVATIONS["forged_cache"] = {
            "import_accepted": False,
            "refusal": type(exc).__name__,
        }
        return
    values = None
    consumer_error = None
    if restored.result_state == "SUPPORTED":
        try:
            values = EvidenceConsumerReader(request, restored).read()
        except EvidenceAssociationError as exc:
            consumer_error = str(exc)
    OBSERVATIONS["forged_cache"] = {
        "import_accepted": accepted,
        "result_state": restored.result_state,
        "denominator": restored.denominator,
        "forged_actual_hash": forged_actual.result_hash,
        "consumer_denominator": None if values is None else values["denominator"],
        "consumer_error": consumer_error,
    }
    assert restored.result_state != "SUPPORTED", (
        "default self-sealed cache ingress accepted a forged same-source evidence "
        f"preimage and resolved {restored.result_state}"
    )
    assert restored.denominator != 999, (
        "default self-sealed cache ingress served forged denominator 999 "
        f"through the intended public API; values={values}"
    )
    assert values is not None and values["denominator"] != 999, (
        f"actual consumer read served forged denominator 999: {values}"
    )


def test_authenticated_issuer_still_rejects_plain_self_seal_but_default_accepts_preimage():
    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-r2-default-vs-issuer")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    cache = resolver.export_cache()
    assert cache["entries"][0]["seal_algorithm"] == "SHA256_CANONICAL_FULLK_PRODUCER_CONSUMER_PREIMAGE"
    cold = EvidenceResolver()
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    OBSERVATIONS["default_cache_trust"] = {
        "provenance": restored.provenance,
        "cache_trust_grade": restored.consumer_values_read.get("cache_trust_grade"),
    }
    assert (
        restored.consumer_values_read["cache_trust_grade"]
        == "FULL_K_PRODUCER_ASSOCIATION_SHA256"
    )
