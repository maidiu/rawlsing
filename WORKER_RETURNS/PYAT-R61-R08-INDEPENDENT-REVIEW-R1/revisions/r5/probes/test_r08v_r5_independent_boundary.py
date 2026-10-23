"""R61-R08V R5 independent probes at the configured public consumer grain.

Uses the pinned source-free AT07/n10e fixture authority and the unchanged
provider/evaluator. Expected positive values are recomputed from the fixture
rows, not author assertions. Hostile probes expect the SAME configured public
reader/resolver/export path to refuse; a test failure is a recorded defect.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import json
import os
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
    CACHE_TRUST_ASSOCIATION,
    PROVENANCE_CACHE,
    PROVENANCE_CANONICAL,
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
    (OUTCOMES / "r5_observations.json").write_text(
        json.dumps(
            {
                "schema": "R61_R08V_R5_INDEPENDENT_OBSERVATIONS@1",
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


def _provider_direct(case):
    return provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )


def test_independent_positive_54_6_60_signed_projection():
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in at07_rows()
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 6
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 60

    case, request, resolver, result = _resolve_canonical("r5-independent-positive")
    provider = _provider_direct(case)
    composition = provider.composition_result
    direct_cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in composition.complete_cell_geometry
    }
    assert composition.raw_denominator_support == 60
    assert direct_cells == {"yes": 54, "no": 6}
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 60
    read = _reader(request, result).read()
    step = _reader(request, result).e04_step()
    assert read["denominator"] == 60
    assert read["cells"] == [
        dict(cell) for cell in result.execution_envelope.cells
    ]
    assert read["evidence_ref"] == result.execution_envelope.evidence_ref.as_dict()
    assert read["consumer_result_state"] == "EXACT_SUPPORTED"
    assert read["consumer_result_hash"] == result.consumer_result_hash
    assert step["denominator"] == 60
    assert step["state"] == "EXACT_SUPPORTED"
    _record(
        "independent_positive_54_6_60",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 6, "denominator": 60},
            "provider_denominator": composition.raw_denominator_support,
            "provider_cells": direct_cells,
            "consumer_hash": result.consumer_result_hash,
            "read_denominator": read["denominator"],
            "e04_denominator": step["denominator"],
            "observed": "SUPPORTED 54/6/60",
        },
    )


def test_changed_native_case_serves_54_16_70():
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in changed_source_rows()
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 16
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 70

    case = build_provider_case("forward", variant=CHANGED_SOURCE_VARIANT)
    request = _request(case, request_id="r5-independent-changed")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 70
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == {
        "yes": 54,
        "no": 16,
    }
    read = _reader(request, result).read()
    assert read["denominator"] == 70
    assert read["cells"] == [dict(cell) for cell in result.execution_envelope.cells]
    _record(
        "changed_native_54_16_70",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 16, "denominator": 70},
            "observed_denominator": result.denominator,
            "read_denominator": read["denominator"],
        },
    )


def test_no_config_wrong_root_attacker_issuer_refuse():
    case = build_provider_case("forward")
    request = _request(case, request_id="r5-independent-no-config")
    unconfigured = EvidenceResolver()
    unconfigured.bind(_binding(request, case))
    refused = unconfigured.resolve(request)
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "NO_CONFIGURED_TRUST_ROOT"
    with pytest.raises(EvidenceCacheIntegrityError):
        unconfigured.import_authenticated_cache({"schema": CACHE_SCHEMA, "entries": []})
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, refused).read()

    case, request, resolver, produced = _resolve_canonical("r5-independent-wrong-root")
    attacker = TrustedAdmissionAuthority()
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, produced, verifier=attacker.verifier()).read()
    forged = replace(
        produced, envelope_signature=attacker.issue_envelope(produced.execution_envelope)
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged).read()
    assert _reader(request, produced).read()["denominator"] == 60
    _record(
        "no_config_wrong_root_attacker",
        {
            "no_config_state": refused.result_state,
            "no_config_refusal": refused.typed_refusal,
            "wrong_root_refused": True,
            "attacker_signature_refused": True,
            "restored_denominator": 60,
        },
    )


def test_r4_reader_mutations_now_typed_refuse_and_restore():
    case, request, resolver, produced = _resolve_canonical("r5-independent-r4-closure")
    values = dict(produced.consumer_values_read)
    values["denominator"] = 999
    values["result_state"] = "ZERO_SUPPORT"
    values["cells"] = [
        {
            "cell": "yes",
            "cell_state": "FORGED",
            "raw_numerator_support": 999,
            "raw_probability_exact_fraction": {"$exact_fraction": [1, 1]},
        }
    ]
    values["evidence_ref"] = {
        "kind": "FORGED_EVIDENCE",
        "object_id": "urn:forged:evidence",
        "content_hash": semantic_hash({"forged": "evidence"}),
    }
    mutated_values = replace(produced, consumer_values_read=values)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated_values).read()
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated_values).e04_step()

    mutated_meta = replace(
        produced,
        producer_fact_state="FORGED_FACT_STATE",
        uncertainty_state="FORGED_UNCERTAINTY",
        producer_receipt_ref=None,
        producer_fact_ref=None,
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated_meta).read()
    assert _reader(request, produced).read()["denominator"] == 60
    _record(
        "r4_reader_mutations_closed",
        {
            "value_mutation_refused": True,
            "e04_mutation_refused": True,
            "metadata_mutation_refused": True,
            "restored_denominator": 60,
        },
    )


def test_missing_live_producer_pin_does_not_execute():
    case = build_provider_case("forward")
    request = _request(case, request_id="r5-independent-missing-pin")
    calls: list[str] = []

    def substituted_producer(**kwargs):
        calls.append("called")
        raise RuntimeError("SUBSTITUTED_PRODUCER_EXECUTED")

    resolver = EvidenceResolver(
        admission_verifier=_R4_VERIFIER,
        executor=_R4_ISSUER,
    )
    resolver.bind(_binding(request, case, producer=substituted_producer))
    refused = resolver.resolve(request)
    assert calls == []
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"

    legitimate = EvidenceResolver(
        admission_verifier=_R4_VERIFIER,
        executor=_R4_ISSUER,
    )
    legitimate.bind(_binding(request, case))
    refused_legitimate = legitimate.resolve(request)
    assert refused_legitimate.result_state == "UNKNOWN"
    assert refused_legitimate.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"
    _record(
        "missing_live_pin_fail_closed",
        {
            "substituted_call_count": len(calls),
            "state": refused.result_state,
            "refusal": refused.typed_refusal,
            "legitimate_without_pin_state": refused_legitimate.result_state,
        },
    )


def test_provenance_mutation_must_not_serve_unsigned_grade():
    case, request, resolver, produced = _resolve_canonical("r5-independent-provenance")
    assert produced.provenance == PROVENANCE_CANONICAL
    canonical_mutated = replace(produced, provenance=PROVENANCE_CACHE)
    canonical_read = _reader(request, canonical_mutated).read()

    cache = resolver.export_cache()
    cold = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    assert restored.provenance == PROVENANCE_CACHE
    cache_mutated = replace(restored, provenance=PROVENANCE_CANONICAL)
    cache_read = _reader(request, cache_mutated).read()

    _record(
        "provenance_grade_mutation",
        {
            "canonical_signed_provenance": produced.provenance,
            "canonical_supplied_provenance": canonical_mutated.provenance,
            "canonical_read_cache_trust_grade": canonical_read.get("cache_trust_grade"),
            "cache_signed_provenance": restored.provenance,
            "cache_supplied_provenance": cache_mutated.provenance,
            "cache_read_cache_trust_grade": cache_read.get("cache_trust_grade"),
            "expected_cache_grade": CACHE_TRUST_ASSOCIATION,
        },
    )
    assert canonical_read.get("cache_trust_grade") is None
    assert cache_read.get("cache_trust_grade") == CACHE_TRUST_ASSOCIATION


def test_export_must_reject_mutated_evidence_object():
    case, request, resolver, produced = _resolve_canonical("r5-independent-export-object")
    geometry = produced.evidence_object.geometry
    assert isinstance(geometry, dict)
    cell = geometry["cells"][0]
    cell["raw_numerator_support"] = 999

    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()

    try:
        cache = resolver.export_cache()
        exported = True
        exported_evidence_support = cache["entries"][0]["evidence"]["geometry"]["cells"][0].get(
            "raw_numerator_support"
        )
    except EvidenceCacheIntegrityError as exc:
        exported = False
        exported_evidence_support = None
        export_refusal = str(exc)
    else:
        export_refusal = None

    import_refused = False
    if exported:
        try:
            _resolver().import_authenticated_cache(cache)
        except EvidenceCacheIntegrityError:
            import_refused = True

    _record(
        "export_mutated_evidence_object",
        {
            "reader_refused_mutated_object": True,
            "export_accepted": exported,
            "exported_evidence_raw_support": exported_evidence_support,
            "export_refusal": export_refusal,
            "downstream_import_refused": import_refused,
            "signed_envelope_evidence_hash": produced.execution_envelope.evidence_content_hash,
        },
    )
    assert not exported
    assert import_refused


def test_verifier_only_replay_and_cold_process_positive():
    case, request, resolver, produced = _resolve_canonical("r5-independent-cold")
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
request = _request(case, request_id="r5-independent-cold")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
resolver = EvidenceResolver(admission_verifier=verifier)
resolver.import_authenticated_cache(cache)
result = resolver.resolve(request)
values = EvidenceConsumerReader(request, result, verifier=verifier).read()
try:
    resolver.export_cache()
    reexport = "ACCEPTED"
except Exception as exc:
    reexport = type(exc).__name__ + ": " + str(exc)
print(json.dumps({{"provenance": result.provenance, "state": result.result_state,
"denominator": result.denominator, "consumer_denominator": values["denominator"],
"consumer_hash": result.consumer_result_hash, "reexport": reexport}}, sort_keys=True))
"""
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            input=json.dumps({"key_hex": _R4_ISSUER.key_hex}),
            text=True,
            capture_output=True,
            check=False,
            env={"PYTHONDONTWRITEBYTECODE": "1", **os.environ},
        )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout.strip().splitlines()[-1])
    assert observed["provenance"] == "AUTHENTICATED_CACHE"
    assert observed["state"] == "SUPPORTED"
    assert observed["denominator"] == 60
    assert observed["consumer_denominator"] == 60
    assert observed["consumer_hash"] == produced.consumer_result_hash
    _record("cold_process_positive", observed)
