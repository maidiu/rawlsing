"""R7 semantic adapters for the prior R6/R5 removed-transport expectations.

These preserve the same invariant under the R61AF canonical descriptor:
- unsigned EvidenceResult.provenance cannot change signed original execution or
  produce a trusted local delivery label (R6/R5 provenance probe);
- no parallel producer_binding/admission transport survives; an altered
  canonical owner descriptor cannot import/read/re-export (R6 producer-binding
  probe);
- a mutated evidence object is not exported (R5 export probe; the old
  downstream-import assertion was unreachable once export refused).
"""
from __future__ import annotations

from dataclasses import replace
import copy

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_OWNER_DESCRIPTOR_FIELDS,
    PROVENANCE_CACHE,
    PROVENANCE_CANONICAL,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceResolver,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import (
    _R4_VERIFIER,
    _binding,
    _reader,
    _request,
    _resolver,
)

OUTCOMES = __import__("pathlib").Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    import json

    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r7_semantic_adapters.json").write_text(
        json.dumps(
            {
                "schema": "R61_R08V_R7_SEMANTIC_ADAPTERS@1",
                "probes": OBSERVATIONS,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _canonical(request_id):
    case = build_provider_case("forward")
    request = _request(case, request_id=request_id)
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    return case, request, resolver, resolver.resolve(request)


def test_r6_r5_provenance_adapter_no_unsigned_local_label():
    case, request, resolver, produced = _canonical("r7-adapter-provenance")
    live = _reader(request, produced).read()
    assert live["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert live["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "local_delivery_context_unsigned" not in live
    assert "cache_trust_grade" not in live

    mutated = replace(produced, provenance=PROVENANCE_CACHE)
    mutated_read = _reader(request, mutated).read()
    assert mutated_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert mutated_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "local_delivery_context_unsigned" not in mutated_read
    assert "cache_trust_grade" not in mutated_read

    cold = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    cold.import_authenticated_cache(resolver.export_cache())
    restored = cold.resolve(request)
    cache_read = _reader(request, restored).read()
    assert cache_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert cache_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "local_delivery_context_unsigned" not in cache_read
    assert "cache_trust_grade" not in cache_read

    mislabeled = replace(restored, provenance=PROVENANCE_CANONICAL)
    mislabeled_read = _reader(request, mislabeled).read()
    assert mislabeled_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert mislabeled_read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "local_delivery_context_unsigned" not in mislabeled_read
    assert "cache_trust_grade" not in mislabeled_read
    _record(
        "r6_r5_provenance_adapter",
        {
            "signed_original": PROVENANCE_CANONICAL,
            "signed_mode": "LIVE_TRUSTED_EXECUTION",
            "local_label_present": False,
            "cache_trust_grade_present": False,
            "restored_denominator": cache_read["denominator"],
        },
    )


def test_r6_producer_binding_adapter_canonical_descriptor_refuses_altered_owner():
    case, request, resolver, produced = _canonical("r7-adapter-owner")
    baseline = resolver.export_cache()
    entry = baseline["entries"][0]
    assert "producer_binding" not in entry
    assert "admission" not in entry
    descriptor = entry["cache_owner_descriptor"]
    assert set(descriptor) == CACHE_OWNER_DESCRIPTOR_FIELDS
    assert set(descriptor["owner_identity_material"]) == {
        "context_ref", "context", "actual_conditions", "producer_query_ref",
        "predicate_ref", "predicate_hash", "release_refs", "consumer_query_ref",
        "consumer_binding_fingerprint", "model_rule_hash", "source_universe_ref",
        "risk_set_ref", "target_ref",
    }

    altered = copy.deepcopy(baseline)
    desc = altered["entries"][0]["cache_owner_descriptor"]
    owner = desc["owner_identity_material"]
    owner["producer_query_ref"] = {
        "kind": "FORGED_PRODUCER_QUERY",
        "object_id": "urn:forged:producer-query",
        "content_hash": semantic_hash({"forged": "producer-query"}),
    }
    desc["owner_identity_hash"] = semantic_hash(owner)
    desc["descriptor_hash"] = semantic_hash(
        {k: v for k, v in desc.items() if k != "descriptor_hash"}
    )
    altered["entries"][0]["seal"] = semantic_hash(
        {
            k: v
            for k, v in altered["entries"][0].items()
            if k not in {"seal", "issuer_seal", "issuer_grade"}
        }
    )
    with pytest.raises(EvidenceCacheIntegrityError):
        EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(
            altered
        )

    # The original canonical descriptor still imports/reads/re-exports.
    first = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    first.import_authenticated_cache(baseline)
    assert _reader(request, first.resolve(request)).read()["denominator"] == 60
    again = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    again.import_authenticated_cache(first.export_cache())
    assert _reader(request, again.resolve(request)).read()["denominator"] == 60
    _record(
        "r6_producer_binding_adapter",
        {
            "parallel_producer_binding_absent": True,
            "admission_absent": True,
            "altered_owner_descriptor_refused": True,
            "original_chain_denominator": 60,
        },
    )


def test_r5_export_evidence_adapter_refuses_mutation_and_restores():
    case, request, resolver, produced = _canonical("r7-adapter-evidence")
    original = produced.evidence_object.geometry["cells"][0]["raw_numerator_support"]
    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.evidence_object.geometry["cells"][0][
        "raw_numerator_support"
    ] = original
    exported = resolver.export_cache()
    assert _reader(request, produced).read()["denominator"] == 60
    assert exported["entries"][0]["evidence"]["geometry"]["cells"][0][
        "raw_numerator_support"
    ] == original
    _record(
        "r5_export_evidence_adapter",
        {
            "mutated_reader_refused": True,
            "mutated_export_refused": True,
            "restored_denominator": 60,
            "restored_cell": original,
        },
    )
