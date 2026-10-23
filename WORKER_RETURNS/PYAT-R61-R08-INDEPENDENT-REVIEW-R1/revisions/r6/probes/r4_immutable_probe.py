"""R61-R08V R4 independent probes at the configured public consumer grain.

Setup uses the pinned source-free AT07/n10e native fixture (`build_provider_case`)
and the candidate's public request/context/binding adapters.  Expected positive
values are recomputed here from the fixture response table and the actual
provider/evaluator, not from author assertions.  Hostile probes expect the same
preconfigured consumer to refuse; a test failure is a recorded defect, not a
harness error.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_SCHEMA,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceResolver,
    TrustedAdmissionAuthority,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    CHANGED_SOURCE_VARIANT,
    at07_rows,
    build_provider_case,
    changed_source_rows,
)
from rawlsing_next.tests.test_universal_evidence_binding import (
    _R4_ISSUER,
    _R4_VERIFIER,
    _binding,
    _reader,
    _request,
    _resolver,
)

ROOT = Path(__file__).resolve().parents[5]
OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump_observations():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r4_observations.json").write_text(
        json.dumps(
            {
                "schema": "R61_R08V_R4_INDEPENDENT_OBSERVATIONS@1",
                "probes": OBSERVATIONS,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _resolve_canonical(request_id: str):
    case = build_provider_case("forward")
    request = _request(case, request_id=request_id)
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    return case, request, resolver, resolver.resolve(request)


def _evaluate_provider_directly(case):
    provider = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    return provider


def test_independent_fixture_positive_54_6_60_and_actual_provider():
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in at07_rows()
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 6
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 60

    case, request, resolver, result = _resolve_canonical("r4-independent-positive")
    provider = _evaluate_provider_directly(case)
    composition = provider.composition_result
    direct_cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in composition.complete_cell_geometry
    }
    assert composition.raw_denominator_support == 60
    assert direct_cells == {"yes": 54, "no": 6}
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 60
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == {
        "yes": 54,
        "no": 6,
    }
    read = _reader(request, result).read()
    assert read["denominator"] == 60
    assert read["consumer_result_state"] == "EXACT_SUPPORTED"
    assert read["consumer_result_hash"] == result.consumer_result_hash
    _record(
        "independent_positive_54_6_60",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 6, "denominator": 60},
            "provider_denominator": composition.raw_denominator_support,
            "provider_cells": direct_cells,
            "consumer_result_hash": result.consumer_result_hash,
            "observed": "SUPPORTED 60",
        },
    )


def test_changed_native_case_serves_own_values_not_canonical():
    rows = changed_source_rows()
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"]) for row in rows
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 16
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 70

    case = build_provider_case("forward", variant=CHANGED_SOURCE_VARIANT)
    request = _request(case, request_id="r4-independent-changed")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 70
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == {
        "yes": 54,
        "no": 16,
    }
    assert _reader(request, result).read()["denominator"] == 70
    _record(
        "changed_native_case",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 16, "denominator": 70},
            "observed_denominator": result.denominator,
            "observed_cells": {
                cell["cell"]: cell["raw_numerator_support"] for cell in result.cells
            },
        },
    )


def test_no_config_default_resolver_and_reader_refuse():
    case = build_provider_case("forward")
    request = _request(case, request_id="r4-independent-no-config")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "NO_CONFIGURED_TRUST_ROOT"
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, result).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        EvidenceResolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": []}
        )
    _record(
        "no_config_refusal",
        {"result_state": result.result_state, "refusal": result.typed_refusal},
    )


def test_wrong_root_and_attacker_issuer_are_refused_by_real_reader():
    case, request, resolver, produced = _resolve_canonical("r4-independent-wrong-root")
    attacker = TrustedAdmissionAuthority()
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(
            request, produced, verifier=attacker.verifier()
        ).read()
    forged_signature = attacker.issue_envelope(produced.execution_envelope)
    forged = replace(produced, envelope_signature=forged_signature)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged).read()
    assert _reader(request, produced).read()["denominator"] == 60
    _record(
        "wrong_root_and_attacker_issuer",
        {
            "wrong_verifier_refused": True,
            "attacker_signature_refused": True,
            "restored_denominator": 60,
        },
    )


def test_forged_consumer_values_read_must_refuse_or_serve_signed_values():
    case, request, resolver, produced = _resolve_canonical("r4-independent-values")
    values = dict(produced.consumer_values_read)
    forged_cells = [
        {
            "cell": "yes",
            "cell_state": "EXACT",
            "raw_numerator_support": 999,
            "raw_probability_exact_fraction": "1",
        }
    ]
    forged_ref = {
        "kind": "FORGED_EVIDENCE",
        "object_id": "urn:forged:evidence",
        "content_hash": semantic_hash({"forged": "evidence"}),
    }
    values["denominator"] = 999
    values["cells"] = forged_cells
    values["evidence_ref"] = forged_ref
    values["result_state"] = "ZERO_SUPPORT"
    mutated = replace(produced, consumer_values_read=values)
    read = _reader(request, mutated).read()
    step = _reader(request, mutated).e04_step()
    _record(
        "forged_consumer_values_read",
        {
            "signed_envelope_denominator": produced.execution_envelope.denominator,
            "read_denominator": read["denominator"],
            "read_cells": read["cells"],
            "read_evidence_ref": read["evidence_ref"],
            "read_result_state": read["result_state"],
            "e04_state": step["state"],
            "e04_denominator": step["denominator"],
            "observed": "SAME reader served unsigned mutated values",
        },
    )
    assert read["denominator"] == produced.execution_envelope.denominator
    assert read["cells"] == [dict(cell) for cell in produced.cells]
    assert read["evidence_ref"] == produced.execution_envelope.evidence_ref.as_dict()
    assert step["state"] == produced.execution_envelope.evaluator_result_state
    assert step["denominator"] == produced.execution_envelope.denominator


def test_mutated_result_metadata_must_refuse():
    case, request, resolver, produced = _resolve_canonical("r4-independent-meta")
    mutated = replace(
        produced,
        producer_fact_state="FORGED_FACT_STATE",
        uncertainty_state="FORGED_UNCERTAINTY",
        producer_receipt_ref=None,
        producer_fact_ref=None,
    )
    read = _reader(request, mutated).read()
    _record(
        "mutated_result_metadata",
        {
            "signed_producer_fact_state": produced.execution_envelope.producer_fact_state,
            "supplied_result_fact_state": mutated.producer_fact_state,
            "result_accepted": True,
            "read_denominator": read["denominator"],
        },
    )
    assert mutated.producer_fact_state == produced.execution_envelope.producer_fact_state
    assert mutated.uncertainty_state == produced.execution_envelope.uncertainty_state
    assert mutated.producer_receipt_ref == produced.execution_envelope.producer_receipt_ref
    assert mutated.producer_fact_ref == produced.execution_envelope.producer_fact_ref


def test_substituted_producer_without_optional_pin_must_not_execute():
    case = build_provider_case("forward")
    request = _request(case, request_id="r4-independent-callable")
    calls: list[str] = []

    def substituted_producer(**kwargs):
        calls.append("called")
        raise RuntimeError("SUBSTITUTED_PRODUCER_EXECUTED")

    binding = _binding(request, case, producer=substituted_producer)
    resolver = EvidenceResolver(
        admission_verifier=_R4_VERIFIER,
        executor=_R4_ISSUER,
    )
    resolver.bind(binding)
    try:
        result = resolver.resolve(request)
        observed = {"returned_state": result.result_state, "calls": len(calls)}
    except RuntimeError as exc:
        observed = {"exception": str(exc), "calls": len(calls)}
    _record("substituted_producer_without_pin", observed)
    assert calls == []


def test_cache_forged_evidence_and_missing_envelope_refuse():
    case, request, resolver, produced = _resolve_canonical("r4-independent-cache")
    base = resolver.export_cache()["entries"][0]

    no_envelope = {
        key: value
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade", "execution_envelope", "envelope_signature"}
    }
    no_envelope["seal"] = semantic_hash(no_envelope)
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [no_envelope]}
        )

    forged = {
        key: value
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade"}
    }
    forged["evidence"] = json.loads(json.dumps(forged["evidence"]))
    forged["evidence"]["raw_support"] = 999
    forged["seal"] = semantic_hash(forged)
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [forged]}
        )
    _record(
        "cache_forgery_refusal",
        {"missing_envelope_refused": True, "forged_evidence_999_refused": True},
    )


def test_cold_process_positive_same_consumer_hash():
    case, request, resolver, produced = _resolve_canonical("r4-independent-cold")
    cache = resolver.export_cache()
    with tempfile.TemporaryDirectory() as tmp:
        cache_path = Path(tmp) / "cache.json"
        cache_path.write_text(json.dumps(cache), encoding="utf-8")
        script = f"""
import json, sys
from pathlib import Path
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import _request
from rawlsing_next.pre553_universal_evidence_binding import (
    EvidenceConsumerReader, EvidenceResolver, TrustedAdmissionAuthority,
)
config = json.loads(sys.stdin.read())
issuer = TrustedAdmissionAuthority(bytes.fromhex(config["key_hex"]))
verifier = issuer.verifier()
case = build_provider_case("forward")
request = _request(case, request_id="r4-independent-cold")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
resolver = EvidenceResolver(admission_verifier=verifier)
resolver.import_authenticated_cache(cache)
result = resolver.resolve(request)
values = EvidenceConsumerReader(request, result, verifier=verifier).read()
print(json.dumps({{"provenance": result.provenance, "state": result.result_state,
"denominator": result.denominator, "consumer_denominator": values["denominator"],
"consumer_hash": result.consumer_result_hash}}, sort_keys=True))
"""
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            input=json.dumps({"key_hex": _R4_ISSUER.key_hex}),
            text=True,
            capture_output=True,
            check=False,
            env={"PYTHONDONTWRITEBYTECODE": "1", **__import__("os").environ},
        )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout.strip().splitlines()[-1])
    assert observed["provenance"] == "AUTHENTICATED_CACHE"
    assert observed["state"] == "SUPPORTED"
    assert observed["denominator"] == 60
    assert observed["consumer_denominator"] == 60
    assert observed["consumer_hash"] == produced.consumer_result_hash
    _record("cold_process_positive", observed)
