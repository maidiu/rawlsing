"""R61-R08V R7 independent canonical-descriptor and consumer probes.

Setup uses the pinned native AT07/n10e fixture authority; positive values are
recomputed from the fixture rows. The 13 owner classes are driven from the
declared normal form, not from the latest named probe.
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
    CACHE_OWNER_DESCRIPTOR_FIELDS,
    CACHE_OWNER_FIELDS,
    CACHE_SCHEMA,
    PROVENANCE_CANONICAL,
    EvidenceAssociationError,
    EvidenceCacheIntegrityError,
    EvidenceResolver,
    TypedValue,
    reduce_required_support,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    CHANGED_SOURCE_VARIANT,
    at07_rows,
    build_consumer,
    build_model_rule,
    build_producer,
    build_provider_case,
    build_witness,
    changed_source_rows,
    frozen_at07_source,
)
from rawlsing_next.tests.test_universal_evidence_binding import (
    _R4_ISSUER,
    _R4_VERIFIER,
    _binding,
    _condition,
    _reader,
    _request,
    _resolver,
    _zero_case,
)

ROOT = Path(__file__).resolve().parents[5]
OUTCOMES = Path(__file__).resolve().parents[1] / "outcomes"
OBSERVATIONS: list[dict] = []
OWNER_CLASSES = (
    "context_ref", "context", "actual_conditions", "producer_query_ref",
    "predicate_ref", "predicate_hash", "release_refs", "consumer_query_ref",
    "consumer_binding_fingerprint", "model_rule_hash", "source_universe_ref",
    "risk_set_ref", "target_ref",
)


def _record(name: str, observed: dict) -> None:
    OBSERVATIONS.append({"probe": name, **observed})


@pytest.fixture(scope="module", autouse=True)
def _dump():
    yield
    OUTCOMES.mkdir(parents=True, exist_ok=True)
    (OUTCOMES / "r7_observations.json").write_text(
        json.dumps(
            {"schema": "R61_R08V_R7_INDEPENDENT_OBSERVATIONS@1", "probes": OBSERVATIONS},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


@pytest.fixture(scope="module")
def baseline():
    case = build_provider_case("forward")
    request = _request(case, request_id="r7-independent-baseline")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    cache = resolver.export_cache()
    return case, request, resolver, produced, cache


def _changed(value):
    if isinstance(value, dict):
        out = copy.deepcopy(value)
        key = next(iter(out))
        out[key] = _changed(out[key])
        return out
    if isinstance(value, list):
        return [_changed(value[0]), *copy.deepcopy(value[1:])] if value else ["FORGED"]
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if value is None:
        return "FORGED_NULL"
    return "FORGED:" + str(value)


def _reseal_entry(entry, *, owner=None):
    descriptor = entry["cache_owner_descriptor"]
    if owner is not None:
        descriptor["owner_identity_material"] = canonicalize(owner)
        descriptor["owner_identity_hash"] = semantic_hash(owner)
    descriptor["descriptor_hash"] = semantic_hash(
        {k: v for k, v in descriptor.items() if k != "descriptor_hash"}
    )
    entry["seal"] = semantic_hash(
        {k: v for k, v in entry.items() if k not in {"seal", "issuer_seal", "issuer_grade"}}
    )
    return entry


def _chain(request, cache):
    first = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    first.import_authenticated_cache(copy.deepcopy(cache))
    first_result = first.resolve(request)
    first_values = _reader(request, first_result).read()
    exported = first.export_cache()
    second = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    second.import_authenticated_cache(copy.deepcopy(exported))
    second_values = _reader(request, second.resolve(request)).read()
    assert first_values["denominator"] == second_values["denominator"] == 60
    assert first_values["cells"] == second_values["cells"]
    assert second_values["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert "local_delivery_context_unsigned" not in second_values
    assert exported["entries"][0]["envelope_signature"] == cache["entries"][0]["envelope_signature"]
    return exported, second_values


def test_independent_positive_and_changed_native(baseline):
    case, request, resolver, produced, cache = baseline
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
    cells = {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in provider.composition_result.complete_cell_geometry
    }
    counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"]) for row in at07_rows()
    )
    assert counts[("P1", "yes")] == 54 and counts[("P1", "no")] == 6
    assert cells == {"yes": 54, "no": 6}
    read = _reader(request, produced).read()
    assert read["denominator"] == 60
    assert {c["cell"]: c["raw_numerator_support"] for c in read["cells"]} == {
        "no": 6,
        "yes": 54,
    }

    changed = build_provider_case("forward", variant=CHANGED_SOURCE_VARIANT)
    changed_counts = Counter(
        (row["responses"]["POSITION"], row["responses"]["ANSWER"])
        for row in changed_source_rows()
    )
    assert changed_counts[("P1", "yes")] == 54 and changed_counts[("P1", "no")] == 16
    changed_request = _request(changed, request_id="r7-independent-changed")
    changed_resolver = _resolver()
    changed_resolver.bind(_binding(changed_request, changed))
    changed_result = changed_resolver.resolve(changed_request)
    assert changed_result.denominator == 70
    assert _reader(changed_request, changed_result).read()["denominator"] == 70
    _record(
        "independent_positive",
        {"at07": {"yes": 54, "no": 6, "denominator": 60},
         "changed": {"yes": 54, "no": 16, "denominator": 70}},
    )


def test_descriptor_normal_form_and_no_live_admission(baseline):
    _, _, _, _, cache = baseline
    assert cache["schema"] == CACHE_SCHEMA == "R61_AUTHENTICATED_EVIDENCE_CACHE@5"
    entry = cache["entries"][0]
    assert "producer_binding" not in entry
    assert "admission" not in entry
    descriptor = entry["cache_owner_descriptor"]
    assert set(descriptor) == CACHE_OWNER_DESCRIPTOR_FIELDS
    assert descriptor["schema"] == "R61_CACHE_OWNER_DESCRIPTOR@1"
    assert set(descriptor["owner_identity_material"]) == CACHE_OWNER_FIELDS == set(OWNER_CLASSES)
    assert descriptor["descriptor_hash"] == semantic_hash(
        {k: v for k, v in descriptor.items() if k != "descriptor_hash"}
    )
    assert "admission" not in descriptor and "binding_hash" not in descriptor
    _record(
        "descriptor_normal_form",
        {"entry_keys": sorted(entry), "descriptor_fields": sorted(descriptor),
         "owner_classes": len(CACHE_OWNER_FIELDS)},
    )


@pytest.mark.parametrize("owner_class", OWNER_CLASSES)
@pytest.mark.parametrize("attack", ("mutate", "remove", "duplicate", "type_alias"))
def test_every_owner_class_public_descriptor_mutation_refused(baseline, owner_class, attack):
    _, request, _, _, baseline_cache = baseline
    cache = copy.deepcopy(baseline_cache)
    entry = cache["entries"][0]
    descriptor = entry["cache_owner_descriptor"]
    owner = descriptor["owner_identity_material"]
    if attack == "mutate":
        owner[owner_class] = _changed(owner[owner_class])
    elif attack == "remove":
        del owner[owner_class]
    elif attack == "duplicate":
        descriptor[owner_class] = copy.deepcopy(owner[owner_class])
    else:
        owner[owner_class] = {"aliased_value": owner[owner_class]}
    _reseal_entry(entry, owner=owner)
    with pytest.raises(EvidenceCacheIntegrityError):
        EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(cache)
    _chain(request, baseline_cache)
    _record(
        "owner_class_public_mutation",
        {"owner_class": owner_class, "attack": attack, "refused": True},
    )


@pytest.mark.parametrize("owner_class", OWNER_CLASSES)
def test_signed_inconsistent_owner_class_refused(baseline, owner_class):
    _, request, _, original, baseline_cache = baseline
    owner = copy.deepcopy(original.execution_envelope.owner_identity_material)
    owner[owner_class] = _changed(owner[owner_class])
    envelope = replace(
        original.execution_envelope,
        owner_identity_material=owner,
        owner_identity_hash=semantic_hash(owner),
    )
    signature = _R4_ISSUER.issue_envelope(envelope)
    signed_result = replace(
        original, execution_envelope=envelope, envelope_signature=signature
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, signed_result).read()

    cache = copy.deepcopy(baseline_cache)
    entry = cache["entries"][0]
    entry["execution_envelope"] = canonicalize(envelope.material())
    entry["envelope_signature"] = signature
    _reseal_entry(entry, owner=owner)
    with pytest.raises(EvidenceCacheIntegrityError):
        EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(cache)
    _chain(request, baseline_cache)
    _record(
        "signed_inconsistent_owner_class",
        {"owner_class": owner_class, "reader_refused": True, "import_refused": True},
    )


def test_admission_unknown_and_descriptor_shape_refuse(baseline):
    _, request, _, _, baseline_cache = baseline
    for location in ("descriptor", "owner", "entry", "envelope"):
        for name in ("admission", "unknown_field"):
            cache = copy.deepcopy(baseline_cache)
            entry = cache["entries"][0]
            targets = {
                "descriptor": entry["cache_owner_descriptor"],
                "owner": entry["cache_owner_descriptor"]["owner_identity_material"],
                "entry": entry,
                "envelope": entry["execution_envelope"],
            }
            targets[location][name] = {"token": "0" * 64}
            _reseal_entry(entry)
            with pytest.raises(EvidenceCacheIntegrityError):
                EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(cache)
    for attack in ("null_descriptor", "wrong_schema", "wrong_owner_hash", "wrong_descriptor_hash", "old_binding"):
        cache = copy.deepcopy(baseline_cache)
        entry = cache["entries"][0]
        desc = entry["cache_owner_descriptor"]
        if attack == "null_descriptor":
            entry["cache_owner_descriptor"] = None
            entry["seal"] = semantic_hash(
                {k: v for k, v in entry.items() if k not in {"seal", "issuer_seal", "issuer_grade"}}
            )
        else:
            if attack == "wrong_schema":
                desc["schema"] = "R61_CACHE_OWNER_DESCRIPTOR@0"
            elif attack == "wrong_owner_hash":
                desc["owner_identity_hash"] = "0" * 64
            elif attack == "wrong_descriptor_hash":
                _reseal_entry(entry)
                desc["descriptor_hash"] = "0" * 64
                entry["seal"] = semantic_hash(
                    {k: v for k, v in entry.items() if k not in {"seal", "issuer_seal", "issuer_grade"}}
                )
            else:
                entry["producer_binding"] = {"admission": {"token": "0" * 64}}
            if attack != "wrong_descriptor_hash":
                _reseal_entry(entry)
        with pytest.raises(EvidenceCacheIntegrityError):
            EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(cache)
    _chain(request, baseline_cache)
    _record("admission_unknown_shape", {"all_refused": True})


def test_legacy_schema_pins_and_descriptor_pins(baseline):
    _, request, _, _, baseline_cache = baseline
    for legacy in ("R61_AUTHENTICATED_EVIDENCE_CACHE@4", "R61_AUTHENTICATED_EVIDENCE_CACHE@3", "UNKNOWN"):
        cache = copy.deepcopy(baseline_cache)
        cache["schema"] = legacy
        with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_OR_UNKNOWN_CACHE_SCHEMA"):
            EvidenceResolver(admission_verifier=_R4_VERIFIER).import_authenticated_cache(cache)

    legacy_pin = EvidenceResolver(
        admission_verifier=_R4_VERIFIER, trusted_binding_hashes=("a" * 64,)
    )
    with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_BINDING_PINS_REQUIRE_MIGRATION"):
        legacy_pin.import_authenticated_cache(baseline_cache)
    with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_BINDING_PINS_REQUIRE_MIGRATION"):
        legacy_pin.export_cache()

    descriptor_hash = baseline_cache["entries"][0]["cache_owner_descriptor"]["descriptor_hash"]
    correct = EvidenceResolver(
        admission_verifier=_R4_VERIFIER, trusted_descriptor_hashes=(descriptor_hash,)
    )
    correct.import_authenticated_cache(copy.deepcopy(baseline_cache))
    assert _reader(request, correct.resolve(request)).read()["denominator"] == 60
    correct.export_cache()
    wrong = EvidenceResolver(
        admission_verifier=_R4_VERIFIER, trusted_descriptor_hashes=("a" * 64,)
    )
    with pytest.raises(EvidenceCacheIntegrityError, match="CACHE_OWNER_DESCRIPTOR_NOT_PINNED"):
        wrong.import_authenticated_cache(copy.deepcopy(baseline_cache))
    _record(
        "legacy_and_pins",
        {"legacy_schema_refused": True, "legacy_binding_pin_refused": True,
         "descriptor_pin_refused": True},
    )


def test_legacy_binding_pin_cache_replay_has_explicit_migration_code(baseline):
    case, request, _, _, _ = baseline
    configured = _resolver(trusted_binding_hashes=("a" * 64,))
    configured.bind(_binding(request, case))
    first = configured.resolve(request)
    second = configured.resolve(request)
    assert first.result_state == "SUPPORTED"
    assert first.denominator == 60
    _record(
        "legacy_pin_cache_replay",
        {
            "first_state": first.result_state,
            "second_state": second.result_state,
            "second_typed_refusal": second.typed_refusal,
            "expected": "LEGACY_BINDING_PINS_REQUIRE_MIGRATION",
        },
    )
    assert second.typed_refusal == "LEGACY_BINDING_PINS_REQUIRE_MIGRATION"


def test_live_pin_counter_zero_and_replay_never_invokes_producer(baseline):
    case, request, _, _, _ = baseline
    calls: list[str] = []

    def forbidden(**kwargs):
        calls.append("called")
        raise RuntimeError("FORBIDDEN_LIVE_CALL")

    no_pin = EvidenceResolver(admission_verifier=_R4_VERIFIER, executor=_R4_ISSUER)
    no_pin.bind(_binding(request, case, producer=forbidden))
    refused = no_pin.resolve(request)
    assert calls == []
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"

    verifier_only = EvidenceResolver(
        admission_verifier=_R4_VERIFIER, admitted_producer=forbidden
    )
    verifier_only.import_authenticated_cache(_resolver().export_cache() if False else baseline[4])
    assert _reader(request, verifier_only.resolve(request)).read()["denominator"] == 60
    verifier_only.export_cache()
    assert calls == []
    _record(
        "live_pin_and_replay",
        {"substituted_calls": len(calls), "missing_pin_refusal": refused.typed_refusal},
    )


def test_evidence_query_rule_mutations_isolated_and_restored(baseline):
    _, request, resolver, produced, _ = baseline
    original = produced.evidence_object.geometry["cells"][0]["raw_numerator_support"]
    assert original == 6
    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = original

    kind = produced.consumer_query_object.requested_projection["kind"]
    produced.consumer_query_object.requested_projection["kind"] = "FORGED"
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.consumer_query_object.requested_projection["kind"] = kind

    from rawlsing_next.pre553_empirical_objects import ExactRef

    forged_rule = replace(
        produced.model_rule_object,
        source_universe_refs=(
            ExactRef("R61_SOURCE", "urn:test:r7:forged-rule", semantic_hash({"f": 1})),
        ),
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request, replace(produced, model_rule_object=forged_rule)).read()

    assert _reader(request, produced).read()["denominator"] == 60
    assert resolver.export_cache()["entries"][0]["evidence"]["geometry"]["cells"][0][
        "raw_numerator_support"
    ] == original
    _record(
        "evidence_query_rule_isolated",
        {"original_cell": original, "restored_denominator": 60},
    )


def test_cold_process_verifier_only_chain(baseline):
    _, request, _, produced, cache = baseline
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
request = _request(case, request_id="r7-independent-baseline")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
first = EvidenceResolver(admission_verifier=verifier)
first.import_authenticated_cache(cache)
one = first.resolve(request)
v1 = EvidenceConsumerReader(request, one, verifier=verifier).read()
second = EvidenceResolver(admission_verifier=verifier)
second.import_authenticated_cache(first.export_cache())
two = second.resolve(request)
v2 = EvidenceConsumerReader(request, two, verifier=verifier).read()
print(json.dumps({{"one": one.denominator, "two": two.denominator,
"consumer": v2["denominator"], "provenance": v2["original_execution_provenance"],
"local_label": "local_delivery_context_unsigned" in v2,
"hash_match": one.consumer_result_hash == two.consumer_result_hash}}, sort_keys=True))
"""
        completed = subprocess.run(
            [sys.executable, "-c", script], cwd=ROOT,
            input=json.dumps({"key_hex": _R4_ISSUER.key_hex}),
            text=True, capture_output=True, check=False,
            env={"PYTHONDONTWRITEBYTECODE": "1", **os.environ},
        )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout.strip().splitlines()[-1])
    assert observed == {
        "one": 60, "two": 60, "consumer": 60,
        "provenance": "CANONICAL_PRODUCER", "local_label": False,
        "hash_match": True,
    }
    _record("cold_chain", observed)


def test_currentness_identity_refused_and_restored(baseline):
    _, request, resolver, produced, _ = baseline
    changed = request.changed(as_of_clock="2027-01-01")
    assert changed.key != request.key
    refused = resolver.resolve(changed)
    assert refused.result_state == "UNKNOWN"
    with pytest.raises(EvidenceAssociationError):
        _reader(changed, produced).read()
    assert _reader(request, produced).read()["denominator"] == 60
    _record("currentness_identity", {"changed_key": changed.key != request.key, "restored": 60})


def test_actual_zero_support_and_observed_zero():
    case = build_provider_case("forward")
    zero = _zero_case(case)
    zero_request = _request(
        zero,
        conditions=(_condition("POSITION", "P3", "P3", "position"),),
        direction="POSITION_P3_TO_ANSWER",
        request_id="r7-independent-zero-support",
    )
    resolver = _resolver()
    resolver.bind(_binding(zero_request, zero))
    zero_result = resolver.resolve(zero_request)
    assert zero_result.result_state == "ZERO_SUPPORT"
    assert zero_result.denominator == 0
    with pytest.raises(EvidenceAssociationError):
        _reader(zero_request, zero_result).read()
    assert reduce_required_support([zero_result]).positive_support_count == 0

    rows = [
        {"id": f"P1Y{n:03d}", "responses": {"POSITION": "P1", "ANSWER": "yes"}}
        for n in range(1, 61)
    ] + [
        {"id": f"P2N{n:03d}", "responses": {"POSITION": "P2", "ANSWER": "no"}}
        for n in range(1, 41)
    ]
    with frozen_at07_source(
        tag="r7-observed-zero", rows=rows, scope_query_authority_to_universe=True
    ) as (source, query_authority, registry):
        predicate, producer_query = build_producer(source, query_authority, "forward")
        consumer_query, conditioner_binding = build_consumer(source, "forward")
        witness = build_witness(
            source, "forward", consumer_query, conditioner_binding, producer_query, predicate
        )
        observed_case = {
            "source": source,
            "query_authority": query_authority,
            "registry": registry,
            "predicate": predicate,
            "empirical_query": producer_query,
            "consumer_query": consumer_query,
            "condition_binding_witness": witness,
            "model_rule": build_model_rule(source),
            "release_refs": (source["release_ref"],),
        }
        observed_request = _request(observed_case, request_id="r7-independent-observed-zero")
        observed_resolver = _resolver()
        observed_resolver.bind(_binding(observed_request, observed_case))
        observed_result = observed_resolver.resolve(observed_request)
    assert observed_result.result_state == "SUPPORTED"
    assert observed_result.denominator == 60
    cells = {cell["cell"]: cell["raw_numerator_support"] for cell in observed_result.cells}
    assert cells == {"no": 0, "yes": 60}
    assert _reader(observed_request, observed_result).read()["denominator"] == 60
    _record(
        "actual_zero_controls",
        {"zero_support": 0, "observed_zero_denominator": 60, "observed_cells": cells},
    )


def test_typed_status_and_z_unresolved_controls():
    values = [TypedValue.build(True), TypedValue.build(1), TypedValue.build("1"), TypedValue.build(None)]
    assert len({semantic_hash(v.material()) for v in values}) == 4
    controls = [
        ("VALID_NULL", 10), ("DIFFUSE", 10), ("VALID_EMPTY", 10), ("OBSERVED_ZERO", 10)
    ]
    results = [
        __import__("rawlsing_next.pre553_universal_evidence_binding", fromlist=["EvidenceResult"]).EvidenceResult(
            request_key=semantic_hash({"control": state}),
            eligibility_state="ELIGIBLE", execution_state="COMPLETED",
            result_state=state, provenance="TYPED_REFUSAL", denominator=denom,
        )
        for state, denom in controls
    ]
    summary = reduce_required_support(results)
    assert summary.productive_all_required is True
    z = __import__("rawlsing_next.pre553_universal_evidence_binding", fromlist=["EvidenceResult"]).EvidenceResult(
        request_key=semantic_hash({"control": "Z"}),
        eligibility_state="ELIGIBLE", execution_state="COMPLETED",
        result_state="UNKNOWN", provenance="TYPED_REFUSAL", denominator=16,
        typed_refusal="Z_UNRESOLVED",
    )
    z_summary = reduce_required_support([z])
    assert z_summary.unresolved_denominator_support == 16
    _record("typed_status_z", {"typed_tags_distinct": 4, "z_denominator": 16})
