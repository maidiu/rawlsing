"""R61-R08V R6 independent probes at the configured public consumer grain.

Uses the pinned source-free AT07/n10e fixture authority and the unchanged
provider/evaluator. Positive values are recomputed from the fixture rows, not
author assertions. Hostile probes expect the SAME configured reader/export/
import/re-export paths to refuse; a failing test records a defect.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_SCHEMA,
    PROVENANCE_CACHE,
    PROVENANCE_CANONICAL,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceResolver,
    TrustedAdmissionAuthority,
    TrustedCacheIssuer,
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
    (OUTCOMES / "r6_observations.json").write_text(
        json.dumps(
            {
                "schema": "R61_R08V_R6_INDEPENDENT_OBSERVATIONS@1",
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


def test_independent_positive_54_6_60_signed_original():
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in at07_rows()
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 6
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 60

    case, request, resolver, result = _resolve_canonical("r6-independent-positive")
    provider = _provider_direct(case)
    composition = provider.composition_result
    direct_cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in composition.complete_cell_geometry
    }
    assert composition.raw_denominator_support == 60
    assert direct_cells == {"yes": 54, "no": 6}
    read = _reader(request, result).read()
    step = _reader(request, result).e04_step()
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 60
    assert read["denominator"] == 60
    assert read["consumer_result_state"] == "EXACT_SUPPORTED"
    assert read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "cache_trust_grade" not in read
    assert step["denominator"] == 60
    _record(
        "independent_positive_54_6_60",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 6, "denominator": 60},
            "provider_denominator": composition.raw_denominator_support,
            "provider_cells": direct_cells,
            "consumer_hash": result.consumer_result_hash,
            "original_execution_provenance": read["original_execution_provenance"],
            "original_execution_mode": read["original_execution_mode"],
            "observed": "SUPPORTED 54/6/60",
        },
    )


def test_changed_native_54_16_70():
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in changed_source_rows()
    )
    assert counts[("P1", "yes")] == 54
    assert counts[("P1", "no")] == 16
    assert counts[("P1", "yes")] + counts[("P1", "no")] == 70

    case = build_provider_case("forward", variant=CHANGED_SOURCE_VARIANT)
    request = _request(case, request_id="r6-independent-changed")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    read = _reader(request, result).read()
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 70
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == {
        "yes": 54,
        "no": 16,
    }
    assert read["denominator"] == 70
    _record(
        "changed_native_54_16_70",
        {
            "fixture_counts": {"P1_yes": 54, "P1_no": 16, "denominator": 70},
            "observed_denominator": result.denominator,
            "read_denominator": read["denominator"],
        },
    )


def test_no_config_wrong_root_attacker_and_missing_pin_refuse():
    case = build_provider_case("forward")
    request = _request(case, request_id="r6-independent-no-config")
    unconfigured = EvidenceResolver()
    unconfigured.bind(_binding(request, case))
    refused = unconfigured.resolve(request)
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "NO_CONFIGURED_TRUST_ROOT"
    with pytest.raises(EvidenceCacheIntegrityError):
        unconfigured.import_authenticated_cache({"schema": CACHE_SCHEMA, "entries": []})
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, refused).read()

    case, request, resolver, produced = _resolve_canonical("r6-independent-wrong-root")
    attacker = TrustedAdmissionAuthority()
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, produced, verifier=attacker.verifier()).read()
    forged = replace(
        produced, envelope_signature=attacker.issue_envelope(produced.execution_envelope)
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged).read()

    calls: list[str] = []

    def substituted_producer(**kwargs):
        calls.append("called")
        raise RuntimeError("SUBSTITUTED_PRODUCER_EXECUTED")

    no_pin = EvidenceResolver(admission_verifier=_R4_VERIFIER, executor=_R4_ISSUER)
    no_pin.bind(_binding(request, case, producer=substituted_producer))
    pin_refused = no_pin.resolve(request)
    assert calls == []
    assert pin_refused.result_state == "UNKNOWN"
    assert pin_refused.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"
    _record(
        "no_config_wrong_root_attacker_missing_pin",
        {
            "no_config_refusal": refused.typed_refusal,
            "wrong_root_refused": True,
            "attacker_signature_refused": True,
            "substituted_call_count": len(calls),
            "missing_pin_refusal": pin_refused.typed_refusal,
        },
    )


def test_provenance_semantics_signed_original_and_unsigned_local_label():
    case, request, resolver, produced = _resolve_canonical("r6-independent-provenance")
    live_read = _reader(request, produced).read()
    assert live_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert live_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert live_read["local_delivery_context_unsigned"] == "LIVE_TRUSTED_EXECUTION"
    assert "cache_trust_grade" not in live_read

    canonical_mutated = replace(produced, provenance=PROVENANCE_CACHE)
    canonical_read = _reader(request, canonical_mutated).read()
    assert canonical_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert canonical_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert canonical_read["local_delivery_context_unsigned"] == "VERIFIED_REPLAY"
    assert "cache_trust_grade" not in canonical_read

    cache = resolver.export_cache()
    cold = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    cache_read = _reader(request, restored).read()
    assert cache_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert cache_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert cache_read["local_delivery_context_unsigned"] == "VERIFIED_REPLAY"
    assert "cache_trust_grade" not in cache_read

    mislabeled = replace(restored, provenance=PROVENANCE_CANONICAL)
    mislabeled_read = _reader(request, mislabeled).read()
    assert mislabeled_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert mislabeled_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "cache_trust_grade" not in mislabeled_read
    _record(
        "provenance_semantics",
        {
            "live_original_provenance": live_read["original_execution_provenance"],
            "live_original_mode": live_read["original_execution_mode"],
            "canonical_mutated_original_provenance": canonical_read[
                "original_execution_provenance"
            ],
            "canonical_mutated_local_label": canonical_read[
                "local_delivery_context_unsigned"
            ],
            "cache_original_provenance": cache_read["original_execution_provenance"],
            "cache_original_mode": cache_read["original_execution_mode"],
            "cache_mislabeled_local_label": mislabeled_read[
                "local_delivery_context_unsigned"
            ],
            "cache_trust_grade_present": any(
                "cache_trust_grade" in x
                for x in (live_read, canonical_read, cache_read, mislabeled_read)
            ),
        },
    )


def test_export_refuses_each_mutated_object_and_restores():
    case, request, resolver, produced = _resolve_canonical("r6-independent-objects")
    original_cell = produced.evidence_object.geometry["cells"][0][
        "raw_numerator_support"
    ]
    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.evidence_object.geometry["cells"][0][
        "raw_numerator_support"
    ] = original_cell

    original_kind = produced.consumer_query_object.requested_projection["kind"]
    produced.consumer_query_object.requested_projection["kind"] = "FORGED"
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.consumer_query_object.requested_projection["kind"] = original_kind

    forged_rule = replace(
        produced.model_rule_object,
        source_universe_refs=(
            _ref("R61_SOURCE", "forged-rule-source", {"source": "FORGED"}),
        ),
    )
    forged_result = replace(produced, model_rule_object=forged_rule)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged_result).read()

    resolver.export_cache()
    assert _reader(request, produced).read()["denominator"] == 60
    _record(
        "export_mutated_objects",
        {
            "evidence_refused": True,
            "query_refused": True,
            "rule_reader_refused": True,
            "restored_export_succeeded": True,
            "restored_denominator": 60,
        },
    )


def _ref(kind: str, tag: str, material) -> object:
    from rawlsing_next.pre553_empirical_objects import ExactRef

    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:r6:{tag}:sha256:{digest}", digest)


def test_verifier_only_reexport_round_trip():
    case, request, resolver, produced = _resolve_canonical("r6-independent-reexport")
    cache = resolver.export_cache()
    first = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    first.import_authenticated_cache(cache)
    restored = first.resolve(request)
    first_read = _reader(request, restored).read()
    assert first_read["denominator"] == 60
    assert first_read["original_execution_provenance"] == PROVENANCE_CANONICAL

    reexported = first.export_cache()
    assert reexported["entries"][0]["envelope_signature"] == (
        cache["entries"][0]["envelope_signature"]
    )
    second = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    second.import_authenticated_cache(reexported)
    again = second.resolve(request)
    again_read = _reader(request, again).read()
    assert again_read["denominator"] == 60
    assert again_read["consumer_result_hash"] == produced.consumer_result_hash
    assert again_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    _record(
        "verifier_only_reexport_round_trip",
        {
            "first_read_denominator": first_read["denominator"],
            "second_read_denominator": again_read["denominator"],
            "same_consumer_hash": again_read["consumer_result_hash"]
            == produced.consumer_result_hash,
            "signature_preserved": True,
            "original_execution_provenance": again_read[
                "original_execution_provenance"
            ],
        },
    )


def test_cold_process_positive_and_reexport():
    case, request, resolver, produced = _resolve_canonical("r6-independent-cold")
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
request = _request(case, request_id="r6-independent-cold")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
resolver = EvidenceResolver(admission_verifier=verifier)
resolver.import_authenticated_cache(cache)
result = resolver.resolve(request)
values = EvidenceConsumerReader(request, result, verifier=verifier).read()
reexported = resolver.export_cache()
second = EvidenceResolver(admission_verifier=verifier)
second.import_authenticated_cache(reexported)
rewritten = second.resolve(request)
rewritten_values = EvidenceConsumerReader(request, rewritten, verifier=verifier).read()
print(json.dumps({{"provenance": result.provenance, "state": result.result_state,
"denominator": result.denominator, "consumer_denominator": values["denominator"],
"consumer_hash": result.consumer_result_hash,
"original_execution_provenance": rewritten_values["original_execution_provenance"],
"reexport_denominator": rewritten.denominator}}, sort_keys=True))
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
    assert observed["state"] == "SUPPORTED"
    assert observed["denominator"] == 60
    assert observed["consumer_denominator"] == 60
    assert observed["consumer_hash"] == produced.consumer_result_hash
    assert observed["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert observed["reexport_denominator"] == 60
    _record("cold_process_positive", observed)


def test_old_cache_schema_and_old_envelope_refuse():
    case, request, resolver, produced = _resolve_canonical("r6-independent-old")
    cache = resolver.export_cache()

    old_schema = copy.deepcopy(cache)
    old_schema["schema"] = "R61_AUTHENTICATED_EVIDENCE_CACHE@3"
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(old_schema)

    old_envelope = copy.deepcopy(cache)
    envelope = old_envelope["entries"][0]["execution_envelope"]
    envelope["schema"] = "R61_EXECUTED_EVIDENCE_ENVELOPE@1"
    envelope.pop("execution_provenance", None)
    envelope.pop("execution_mode", None)
    old_envelope["entries"][0]["seal"] = semantic_hash(
        {k: v for k, v in old_envelope["entries"][0].items() if k != "seal"}
    )
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(old_envelope)
    _record(
        "old_versions_refuse",
        {"old_cache_schema_refused": True, "old_envelope_refused": True},
    )


def test_cache_result_projection_mutation_and_swapped_envelope_refuse():
    case, request, resolver, produced = _resolve_canonical("r6-independent-cache-mut")
    cache = resolver.export_cache()
    tampered = copy.deepcopy(cache)
    tampered["entries"][0]["result"]["denominator"] = 999
    tampered["entries"][0]["seal"] = semantic_hash(
        {k: v for k, v in tampered["entries"][0].items() if k != "seal"}
    )
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(tampered)

    other = _resolve_canonical("r6-independent-cache-mut-other")[3]
    swapped = replace(
        produced,
        execution_envelope=other.execution_envelope,
        envelope_signature=other.envelope_signature,
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, swapped).read()
    _record(
        "cache_projection_and_swap_refuse",
        {"result_projection_mutation_refused": True, "swapped_envelope_refused": True},
    )


def test_producer_binding_metadata_must_not_survive_altered():
    case, request, resolver, produced = _resolve_canonical("r6-independent-binding")
    cache = resolver.export_cache()
    entry = cache["entries"][0]

    altered = copy.deepcopy(entry)
    altered["producer_binding"]["producer_query_ref"] = {
        "kind": "FORGED_PRODUCER_QUERY",
        "object_id": "urn:forged:producer-query",
        "content_hash": semantic_hash({"forged": "producer-query"}),
    }
    altered["producer_binding"]["binding_hash"] = semantic_hash(
        {
            k: v
            for k, v in altered["producer_binding"].items()
            if k != "binding_hash"
        }
    )
    altered["seal"] = semantic_hash(
        {k: v for k, v in altered.items() if k != "seal"}
    )

    accepted = False
    reexported_metadata = None
    second_denominator = None
    try:
        verifier_only = EvidenceResolver(admission_verifier=_R4_VERIFIER)
        verifier_only.import_authenticated_cache(
            {"schema": cache["schema"], "entries": [altered]}
        )
        accepted = True
        reexported = verifier_only.export_cache()
        reexported_metadata = reexported["entries"][0]["producer_binding"][
            "producer_query_ref"
        ]
        second = EvidenceResolver(admission_verifier=_R4_VERIFIER)
        second.import_authenticated_cache(reexported)
        second_denominator = second.resolve(request).denominator
    except EvidenceCacheIntegrityError as exc:
        refusal = str(exc)
    else:
        refusal = None

    altered_admission = copy.deepcopy(entry)
    altered_admission["producer_binding"]["admission"]["token"] = "0" * 64
    altered_admission["producer_binding"]["binding_hash"] = semantic_hash(
        {
            k: v
            for k, v in altered_admission["producer_binding"].items()
            if k != "binding_hash"
        }
    )
    altered_admission["seal"] = semantic_hash(
        {k: v for k, v in altered_admission.items() if k != "seal"}
    )
    admission_accepted = False
    try:
        admission_only = EvidenceResolver(admission_verifier=_R4_VERIFIER)
        admission_only.import_authenticated_cache(
            {"schema": cache["schema"], "entries": [altered_admission]}
        )
        admission_accepted = True
    except EvidenceCacheIntegrityError:
        pass

    _record(
        "producer_binding_metadata_mutation",
        {
            "altered_producer_query_import_accepted": accepted,
            "reexported_producer_query_ref": reexported_metadata,
            "second_import_denominator": second_denominator,
            "altered_admission_token_import_accepted": admission_accepted,
            "refusal": refusal,
            "original_producer_query_ref": entry["producer_binding"][
                "producer_query_ref"
            ],
        },
    )
    assert not accepted
    assert not admission_accepted


def test_verifier_only_cannot_execute_new_producer():
    case = build_provider_case("forward")
    request = _request(case, request_id="r6-independent-verifier-only")
    verifier_only = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    verifier_only.bind(_binding(request, case))
    refused = verifier_only.resolve(request)
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"
    _record(
        "verifier_only_no_live_producer",
        {"state": refused.result_state, "refusal": refused.typed_refusal},
    )
