"""R3 reviewer probes for the actual public owner/evidence admission boundary.

These probes intentionally use only the public default construction path
(`EvidenceResolver()`, `TrustedAdmissionAuthority()`, `issue_producer`,
`issue_evidence`) and the source-visible default admission authority.  They do
not use the author test helper that pre-signs the canonical context.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path

import pytest

CANDIDATE = "84704f4a775d0419ad4a08c8c687bc815df47adc"
ROOT = Path(__file__).resolve().parents[5]
FIXTURE_PATHS = {
    "R2/02_VALUE_RELATION_ORACLE.json": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json",
    "R2/03_SYNTHETIC_AUTHORITY_FREEZE.json": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json",
    "R2/04_SLICE_PROJECTION.json": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json",
    "R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json",
    "R8/04_CURRENT_AT07_IDENTITY_SPINE.json": "WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json",
}


def _bootstrap_fixtures() -> Path:
    base = Path(tempfile.mkdtemp(prefix="r61-r08v-r3-fixtures-"))
    for relative, source in FIXTURE_PATHS.items():
        target = base / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        data = subprocess.check_output(
            ["git", "show", f"{CANDIDATE}:{source}"], cwd=ROOT
        )
        target.write_bytes(data)
    return base


_BASE = _bootstrap_fixtures()
import rawlsing_next.tests.n10e_empirical_slice_fixture as _n10e  # noqa: E402

_n10e.R2 = _BASE / "R2"
_n10e.R3 = _BASE / "R3"
_n10e.R8 = _BASE / "R8"
_n10e.R2_RELATION = _n10e.R2 / "02_VALUE_RELATION_ORACLE.json"
_n10e.R2_AUTHORITIES = _n10e.R2 / "03_SYNTHETIC_AUTHORITY_FREEZE.json"
_n10e.R3_AUTHORITY = _n10e.R3 / "02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"
_n10e.R8_SPINE = _n10e.R8 / "04_CURRENT_AT07_IDENTITY_SPINE.json"

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash  # noqa: E402
from rawlsing_next.pre553_universal_evidence_binding import (  # noqa: E402
    CACHE_SCHEMA,
    EmpiricalProducerBinding,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceResolver,
    R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY,
    TrustedOwnerAdmission,
    _cell_core,
    _evidence_from_material,
    _evidence_material,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (  # noqa: E402
    evaluate_positioned_subject_possibility,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case  # noqa: E402
from rawlsing_next.tests.test_universal_evidence_binding import (  # noqa: E402
    _binding,
    _make_context,
    _ref,
    _request,
)


def _forged_context(case):
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
        permission_ref=_ref("R61_PERMISSION", "forged-permission", {"scope": "FORGED"}),
    )


def _forged_request(case, context):
    return _request(
        case,
        request_id="r61-r3-public-default-mint",
        source_id=context.source_id,
        dataset_id=context.dataset_id,
        wave_id=context.wave_id,
        edition=context.edition,
        byte_digest=context.byte_digest,
        instrument_version=context.instrument_version,
        sampled_unit=context.sampled_unit,
        reporting_unit=context.reporting_unit,
        estimand=context.estimand,
        weight_method=context.weight_method,
        design_ref=context.design_ref,
        uncertainty_method=context.uncertainty_method,
        direction=context.direction,
        role=context.role,
        consumer_use=context.consumer_use,
        grammar_version=context.grammar_version,
        custody_ref=context.custody_ref,
        observation_clock=context.observation_clock,
        reference_clock=context.reference_clock,
        as_of_clock=context.as_of_clock,
        publication_clock=context.publication_clock,
        permission_ref=context.permission_ref,
    )


def _binding_for(request, case, context):
    return EmpiricalProducerBinding(
        request=request,
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
        context=context,
    )


def test_default_public_authority_must_not_admit_forged_caller_context():
    case = build_provider_case("forward")
    context = _forged_context(case)
    request = _forged_request(case, context)
    binding = _binding_for(request, case, context)
    admission = R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY.issue_producer(
        context_ref=context.context_ref,
        owner_identity_material=binding.owner_identity_material(),
    )
    binding = replace(binding, admission=admission)
    resolver = EvidenceResolver()
    resolver.bind(binding)
    result = resolver.resolve(request)
    if result.result_state == "SUPPORTED":
        values = EvidenceConsumerReader(request, result).read()
        pytest.fail(
            "default public admission authority minted SUPPORTED for caller-forged "
            f"context: source={request.source_id!r}, edition={request.edition!r}, "
            f"role={request.role!r}, denominator={result.denominator}, "
            f"consumer={values.get('denominator')}"
        )
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, result).read()


def _forged_evidence_cache(produced, base, authority, denominator=999):
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
    evidence = _evidence_from_material(material)
    actual = evaluate_positioned_subject_possibility(
        query=produced.consumer_query_object,
        rule=produced.model_rule_object,
        evidence=(evidence,),
    )
    assert actual.result_state == "EXACT_SUPPORTED"
    producer_admission = TrustedOwnerAdmission.from_material(base["producer_admission"])
    evidence_admission = authority.issue_evidence(
        producer_admission=producer_admission, evidence=evidence
    )
    entry = {
        key: canonicalize(value)
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade"}
    }
    entry["evidence"] = canonicalize(material)
    entry["evidence_admission"] = canonicalize(evidence_admission.material())
    result_material = dict(canonicalize(entry["result"]))
    result_material["denominator"] = denominator
    result_material["cells"] = [canonicalize(_cell_core(cell)) for cell in cells]
    result_material["consumer_result_state"] = actual.result_state
    result_material["consumer_result_hash"] = actual.result_hash
    entry["result"] = canonicalize(result_material)
    entry["seal"] = semantic_hash(entry)
    return {"schema": CACHE_SCHEMA, "entries": [entry]}, actual


def test_default_ingress_must_reject_evidence_resigned_with_public_default_key():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r3-public-cache-resign")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED" and produced.denominator == 60
    base = resolver.export_cache()["entries"][0]
    forged_cache, forged_actual = _forged_evidence_cache(
        produced, base, R61_TEST_ONLY_OWNER_ADMISSION_AUTHORITY
    )
    cold = EvidenceResolver()
    try:
        cold.import_authenticated_cache(forged_cache)
    except EvidenceCacheIntegrityError:
        return
    restored = cold.resolve(request)
    values = None
    if restored.result_state == "SUPPORTED":
        values = EvidenceConsumerReader(request, restored).read()
    pytest.fail(
        "default ingress accepted evidence re-signed with the source-visible "
        f"default admission key: imported={restored.result_state}, "
        f"denominator={restored.denominator}, forged_hash={forged_actual.result_hash}, "
        f"consumer={None if values is None else values.get('denominator')}"
    )


def test_legitimate_canonical_admission_and_cold_replay_remain_positive():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r3-positive-cold-control")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"
    assert produced.denominator == 60
    assert {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in produced.consumer_values_read["cells"]
    } == {"no": 6, "yes": 54}
    cache = resolver.export_cache()
    cold = EvidenceResolver()
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    assert restored.result_state == "SUPPORTED"
    assert restored.denominator == 60
    assert restored.consumer_result_hash == produced.consumer_result_hash
    values = EvidenceConsumerReader(request, restored).read()
    assert values["denominator"] == 60
    assert values["admission_grade"] == "TRUSTED_OWNER_EVIDENCE_ADMISSION_HMAC_SHA256"


def test_missing_admission_still_refuses_old_r2_context_relabel():
    case = build_provider_case("forward")
    context = _forged_context(case)
    request = _forged_request(case, context)
    binding = _binding_for(request, case, context)
    resolver = EvidenceResolver()
    resolver.bind(binding)
    result = resolver.resolve(request)
    assert result.result_state != "SUPPORTED"
    assert result.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"
