"""Campaign B0 SRC04 consumer preparation adapter.

This module reads only committed Campaign A metadata/configuration and the
existing SRC04 nonrespondent fixture.  It never opens the original SAV, never
reads the local original release bundle, and never issues an original query.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture,
    WorkloadBindingRefusal,
    build_projection_catalog,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import (
    SourceConfig,
    canonical_config_hash,
    load_source_config,
)

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = Path(__file__).resolve().parent
EVIDENCE = CAMPAIGN / "evidence"
A_EVIDENCE = ROOT / "campaign_a_src04/evidence"
A_RECEIPT_PATH = A_EVIDENCE / "RELEASE_RECEIPT.json"
A_PROGRAM_PATH = A_EVIDENCE / "PROGRAM.txt"
SOURCE_CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
FIXTURE_CONFIG_PATH = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE_PATH = ROOT / "source_pre553_validation/SRC04/fixture.json"
QUALIFIED_FIXTURE_CONFIG_PATH = ROOT / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
QUALIFIED_FIXTURE_PATH = ROOT / "source_pre553_validation/foundation/fixtures/SRC09_q101_nonrespondent.json"

SOURCE_ID = "SRC04"
EXPECTED_SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
EXPECTED_RELEASE_HASH = "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec"
EXPECTED_RELEASE_ID = "SRC04_ARAB_BAROMETER_I_PREPARATION"
EXPECTED_CONFIG_FILE_SHA256 = "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900"
EXPECTED_CONFIG_CANONICAL_SHA256 = "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
EXPECTED_PROGRAM_SHA256 = "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
EXPECTED_FIXTURE_SOURCE_SHA256 = "506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b"
EXPECTED_FIXTURE_RELEASE_HASH = "9026fa33bb5739b87b06309f12e1d31fe6fd21fb471237eda870d6d278d47f42"
EXPECTED_QUALIFIED_FIXTURE_SOURCE_SHA256 = "a93b4dab00a2b7cbd559d8a0bb1ca498caaa87f27bd1bd73e9fceb0f2820a491"
EXPECTED_QUALIFIED_FIXTURE_RELEASE_HASH = "9a6db7b4aa8b5d7bbd8d366dec55e60fd07cb956d2935f1d7d705ecf99f10e3f"
EXPECTED_SELECTED_RESPONSE_SLOTS = tuple(
    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
     21, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
     39, 40, 41, 42, 43, 44, 45])
EXPECTED_SELECTED_QUESTION_IDS = (
    "q101", "q102", "q103", "q2011", "q2012", "q2013", "q2014", "q2015",
    "q202", "q204", "q205", "q206", "q207", "q210", "q211", "q212", "q2131",
    "q2132", "q2133", "q2134", "q2135", "q214", "q215", "q216", "q219",
    "q221", "q222", "q224", "q2251", "q2252", "q226", "q227", "q228",
    "q2301", "q2302", "q2311", "q2312", "q2321", "q2322", "q2323", "q2324",
    "q234")
EXPECTED_SELECTED_COORDINATE_SLOTS = (1, 2)


class ConsumerPreparationRefusal(ValueError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False).encode("utf-8")).hexdigest()


def jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def _verify_program() -> str:
    if not A_PROGRAM_PATH.is_file():
        raise ConsumerPreparationRefusal("PROGRAM_EVIDENCE_MISSING")
    actual = sha_file(A_PROGRAM_PATH)
    if actual != EXPECTED_PROGRAM_SHA256:
        raise ConsumerPreparationRefusal("PROGRAM_SHA_MISMATCH", actual)
    return actual


def _config_and_receipt() -> tuple[SourceConfig, dict[str, Any], str, str]:
    program_sha = _verify_program()
    if not A_RECEIPT_PATH.is_file():
        raise ConsumerPreparationRefusal("SOURCE_RELEASE_RECEIPT_MISSING")
    receipt = load_json(A_RECEIPT_PATH)
    receipt_sha = sha_file(A_RECEIPT_PATH)
    config = load_source_config(SOURCE_CONFIG_PATH)
    config_file_sha = sha_file(SOURCE_CONFIG_PATH)
    config_canonical = canonical_config_hash(config)
    if config_file_sha != EXPECTED_CONFIG_FILE_SHA256:
        raise ConsumerPreparationRefusal("SOURCE_CONFIG_FILE_SHA_MISMATCH", config_file_sha)
    if config_canonical != EXPECTED_CONFIG_CANONICAL_SHA256:
        raise ConsumerPreparationRefusal("SOURCE_CONFIG_CANONICAL_SHA_MISMATCH", config_canonical)
    if config.source_id != SOURCE_ID or config.active_source_sha256 != EXPECTED_SOURCE_SHA256:
        raise ConsumerPreparationRefusal("SOURCE_CONFIG_IDENTITY_MISMATCH")
    if receipt.get("source_id") != SOURCE_ID or receipt.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise ConsumerPreparationRefusal("RECEIPT_SOURCE_IDENTITY_MISMATCH")
    if receipt.get("config_file_sha256") != config_file_sha:
        raise ConsumerPreparationRefusal("RECEIPT_CONFIG_FILE_BINDING_MISMATCH")
    if receipt.get("config_canonical_sha256") != config_canonical:
        raise ConsumerPreparationRefusal("RECEIPT_CONFIG_CANONICAL_BINDING_MISMATCH")
    if receipt.get("source_read_performed") is not True:
        raise ConsumerPreparationRefusal("ORIGINAL_SOURCE_READ_NOT_ATTESTED")
    release = receipt.get("release")
    if not isinstance(release, Mapping):
        raise ConsumerPreparationRefusal("RELEASE_METADATA_MISSING")
    release_ref = exact_ref(release.get("release_ref"), "release_ref")
    if release_ref.kind != "C11LogicalRelease" or release_ref.object_id != EXPECTED_RELEASE_ID:
        raise ConsumerPreparationRefusal("RELEASE_IDENTITY_MISMATCH")
    if release_ref.content_hash != EXPECTED_RELEASE_HASH:
        raise ConsumerPreparationRefusal("RELEASE_HASH_MISMATCH", release_ref.content_hash)
    if release.get("passed") is not True:
        raise ConsumerPreparationRefusal("RELEASE_RECEIPT_NOT_VALIDATED")
    if release.get("source_artifact_ref", {}).get("content_hash") != EXPECTED_SOURCE_SHA256:
        raise ConsumerPreparationRefusal("RELEASE_SOURCE_ARTIFACT_MISMATCH")
    if release.get("source_release_manifest_hash") != receipt.get("release", {}).get("source_release_manifest_hash"):
        raise ConsumerPreparationRefusal("RELEASE_MANIFEST_BINDING_MISMATCH")
    if receipt.get("canonicalization") != "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW":
        raise ConsumerPreparationRefusal("CANONICAL_AUTHORITY_NOT_DEFER_WITHHELD")
    if receipt.get("selected_response_slots") != list(EXPECTED_SELECTED_RESPONSE_SLOTS):
        raise ConsumerPreparationRefusal("SELECTED_RESPONSE_SLOT_BINDING_MISMATCH")
    if receipt.get("selected_question_ids") != list(EXPECTED_SELECTED_QUESTION_IDS):
        raise ConsumerPreparationRefusal("SELECTED_QUESTION_BINDING_MISMATCH")
    if receipt.get("selected_coordinate_slots") != list(EXPECTED_SELECTED_COORDINATE_SLOTS):
        raise ConsumerPreparationRefusal("SELECTED_COORDINATE_BINDING_MISMATCH")
    counts = release.get("public_counts", {})
    if counts.get("RespondentEvent") != 308_154 or counts.get("RoutingEligibilityFact") != 308_154:
        raise ConsumerPreparationRefusal("RELEASE_EVENT_COUNT_BINDING_MISMATCH")
    if counts.get("EmpiricalCoordinateFact") != 14_674:
        raise ConsumerPreparationRefusal("RELEASE_COORDINATE_COUNT_BINDING_MISMATCH")
    if release.get("canonical_response_values") != 0 or release.get("canonical_coordinate_values") != 0:
        raise ConsumerPreparationRefusal("CANONICAL_MATERIAL_PRESENT")
    if release.get("canonical_questions") != 0:
        raise ConsumerPreparationRefusal("CANONICAL_QUESTIONS_PRESENT")
    if counts.get("WeightMeasureFact", 0) != 0:
        raise ConsumerPreparationRefusal("WEIGHT_FACT_PRESENT")
    return config, receipt, receipt_sha, program_sha


def prepare_original_request_plan(
    receipt: Mapping[str, Any] | None = None,
    config: SourceConfig | None = None,
) -> dict[str, Any]:
    """Prepare exact request identities, or a typed missing-authority plan.

    This function never constructs an `EmpiricalQuerySpec` without an adopted
    predicate/operation authority. It returns a blocked request plan rather than
    a fake usable query.
    """
    if receipt is None or config is None:
        config, canonical_receipt, receipt_sha, program_sha = _config_and_receipt()
    else:
        canonical_receipt = receipt
        if not A_RECEIPT_PATH.is_file() or not A_PROGRAM_PATH.is_file():
            raise ConsumerPreparationRefusal("PINNED_EVIDENCE_MISSING")
        receipt_sha = sha_file(A_RECEIPT_PATH)
        program_sha = sha_file(A_PROGRAM_PATH)
        if program_sha != EXPECTED_PROGRAM_SHA256:
            raise ConsumerPreparationRefusal("PROGRAM_SHA_MISMATCH")
        if canonical_config_hash(config) != EXPECTED_CONFIG_CANONICAL_SHA256:
            raise ConsumerPreparationRefusal("SOURCE_CONFIG_CANONICAL_SHA_MISMATCH")
    receipt = canonical_receipt
    release = receipt["release"]
    release_ref = exact_ref(release["release_ref"], "release_ref")
    if release_ref.content_hash != EXPECTED_RELEASE_HASH:
        raise ConsumerPreparationRefusal("RELEASE_HASH_MISMATCH", release_ref.content_hash)
    if release["public_counts"].get("RespondentEvent") != 308_154:
        raise ConsumerPreparationRefusal("RELEASE_EVENT_COUNT_BINDING_MISMATCH")
    questions = {q["question_id"]: q for q in config.document["questions"]}
    response_slots = {x["question_id"]: x for x in config.document["response_slots"]}
    routing = {x["question_id"]: x for x in config.document["routing"]}
    selected_ids = [str(x) for x in receipt["selected_question_ids"]]
    if selected_ids != list(EXPECTED_SELECTED_QUESTION_IDS):
        raise ConsumerPreparationRefusal("SELECTED_QUESTION_BINDING_MISMATCH")
    target_refs = []
    request_set = []
    universe_refs = set()
    risk_set_refs = set()
    for question_id in selected_ids:
        question = questions.get(question_id)
        slot = response_slots.get(question_id)
        route = routing.get(question_id)
        if question is None or slot is None or route is None:
            raise ConsumerPreparationRefusal("SELECTED_FIELD_NOT_IN_CONFIG", question_id)
        target_ref = exact_ref(question["native_question_ref"], "target_ref")
        if target_ref in target_refs:
            raise ConsumerPreparationRefusal("DUPLICATE_TARGET_REF")
        target_refs.append(target_ref)
        universe = exact_ref(question["empirical_universe_ref"], "empirical_universe_ref")
        universe_refs.add(universe)
        risk_ref = exact_ref(route["risk_set_ref"], "risk_set_ref")
        risk_set_refs.add(risk_ref)
        values = slot.get("values", ())
        raw_domain = [
            {"raw_value": value.get("raw_value"), "missing_state": value.get("missing_state")}
            for value in values
        ]
        response_states = sorted({value.get("response_state") for value in values})
        topology_kinds = sorted({
            occurrence.get("multiplicity_order_rank_fields", {}).get("kind")
            for value in values for occurrence in value.get("occurrences", ())
        })
        request_set.append({
            "request_id": f"B0-SRC04-UNARY-{question_id}",
            "question_id": question_id,
            "source_variable": slot["slot"]["name"],
            "response_slot_ordinal": slot["slot"]["ordinal"],
            "target_ref": target_ref.as_dict(),
            "source_universe_ref": universe.as_dict(),
            "risk_set_ref": risk_ref.as_dict(),
            "routing_state": route["typed_state"],
            "raw_source_value_domain": raw_domain,
            "source_response_states": response_states,
            "source_topology_kinds": topology_kinds,
            "measure_kind": "RAW",
            "source_scope_mode": "SINGLE_UNIVERSE",
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
            "status": "BLOCKED_MISSING_ADOPTED_PREDICATE_AND_RISK_SET_AUTHORITY",
            "query_spec": None,
        })
    if len(universe_refs) != 1:
        raise ConsumerPreparationRefusal("SOURCE_UNIVERSE_SCOPE_NOT_SINGLE", str(len(universe_refs)))
    if len(request_set) != 42:
        raise ConsumerPreparationRefusal("REQUEST_SET_NOT_42", str(len(request_set)))
    universe_ref = next(iter(universe_refs))
    authority_requirements = [
        {
            "role": "predicate_grammar_and_operation",
            "status": "MISSING",
            "required_authority_kind": "PREDICATE_GRAMMAR",
            "required_decision_state": "ALLOW",
            "operation": {
                "status": "UNRESOLVED",
                "existing_source_native_unary_distribution_operation_token": None,
                "note": "No SRC04-specific adopted operation token or issuer exists in committed evidence; do not invent one.",
            },
            "required_governed_object_families": [
                "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"
            ],
            "required_scope": {
                "source_universe_refs": [universe_ref.as_dict()],
                "predicate_or_risk_set_refs": [x.as_dict() for x in sorted(risk_set_refs, key=lambda r: r.key)],
            },
        },
        {
            "role": "target_use_permission",
            "status": "MISSING",
            "required_authority_kind": "TARGET_USE_PERMISSION",
            "required_decision_state": "ALLOW",
            "required_object_family": "EmpiricalFact@1.0.0",
            "note": "Required only if the prepared unary distribution is consumed as an EmpiricalFact; no target-use grant is present.",
        },
        {
            "role": "runtime_object_catalog_and_historical_parent",
            "status": "MISSING",
            "required": [
                "exact EmpiricalPredicate@1.0.0 preimage",
                "exact EmpiricalQuerySpec@1.0.0 preimage",
                "exact RuntimeObjectCatalog containing those preimages",
                "exact runtime_catalog_identity",
                "exact ALLOW PREDICATE_GRAMMAR historical_parent_snapshot",
            ],
            "current_release_ref": release_ref.as_dict(),
            "historical_parent": None,
        },
        {
            "role": "routing_risk_set",
            "status": "ROUTING_UNKNOWN",
            "required": "exact eligible/applicability membership or explicitly adopted raw-sample policy",
            "routing_states": sorted({x["routing_state"] for x in request_set}),
            "risk_set_refs": [x.as_dict() for x in sorted(risk_set_refs, key=lambda r: r.key)],
        },
        {
            "role": "response_state_semantics",
            "status": "MISSING",
            "required": "exact adopted response-state semantics authority for the source-native unary distribution",
        },
    ]
    plan = {
        "schema": "PYAT_CAMPAIGN_B0_SRC04_CONSUMER_REQUEST_PLAN@1.0.0",
        "campaign": "B0",
        "status": "BLOCKED_MISSING_EXACT_CONSUMER_AUTHORITY",
        "source_id": SOURCE_ID,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_release_receipt_path": str(A_RECEIPT_PATH.relative_to(ROOT)),
        "source_release_receipt_sha256": receipt_sha,
        "program_sha256": program_sha,
        "source_config_path": str(SOURCE_CONFIG_PATH.relative_to(ROOT)),
        "source_config_file_sha256": sha_file(SOURCE_CONFIG_PATH),
        "source_config_canonical_sha256": canonical_config_hash(config),
        "source_release_ref": release_ref.as_dict(),
        "source_release_manifest_hash": release["source_release_manifest_hash"],
        "replay_manifest_ref": release["replay_manifest_ref"],
        "source_read_performed_by_a1": receipt["source_read_performed"],
        "source_read_performed_by_b0": False,
        "local_original_release_read_by_b0": False,
        "accepted_response_slots": list(receipt["selected_response_slots"]),
        "accepted_question_ids": selected_ids,
        "accepted_coordinate_slots": list(receipt["selected_coordinate_slots"]),
        "request_count": len(request_set),
        "request_set": request_set,
        "request_set_sha256": canonical_sha(request_set),
        "authority_requirements": authority_requirements,
        "missing_authority": [x for x in authority_requirements if x["status"] not in {"PRESENT"}],
        "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
        "canonical_response_values": 0,
        "canonical_question_values": 0,
        "weight_slots": 0,
        "query_constructed": False,
        "empirical_query_spec_ref": None,
        "runtime_catalog_identity": None,
        "historical_parent_snapshot_ref": None,
        "minimal_remaining_authority": {
            "actual_indispensable_substantive_decision": {
                "decision": "EXTERNAL_COMPETENT_ISSUER_MUST_SUPPLY_EXACT_EXISTING_SOURCE_NATIVE_UNARY_DISTRIBUTION_OPERATION_AND_ROUTING_POLICY",
                "not_fabricated": True,
                "operation_token_selected": False,
                "required_substantive_inputs": [
                    "exact adopted PREDICATE_GRAMMAR ALLOW authority and its existing source-native unary-distribution operation token/predicate semantics",
                    "exact TARGET_USE_PERMISSION ALLOW if an EmpiricalFact will be consumed",
                    "exact eligible/applicability routing or an explicitly adopted raw-sample policy; current SRC04 routing is ROUTING_UNKNOWN",
                    "exact response-state semantics authority for the prepared unary request",
                ],
                "not_required_from_user": [
                    "manual catalog hashes or object preimages",
                    "manually authored EmpiricalQuerySpec/predicate refs",
                    "a new semantic predicate, eligibility rule, canonical mapping, estimand, or population",
                ],
            },
            "mechanically_constructible_after_decision": [
                "EmpiricalPredicate@1.0.0 and EmpiricalQuerySpec@1.0.0 preimages through the existing owners",
                "RuntimeObjectCatalog and catalog_identity through the existing catalog constructor",
                "historical-parent and operation-successor refs once the exact adopted parent is supplied",
            ],
            "engine_constraint": {
                "api": "rawlsing_next._pre553_query_eval._risk_membership",
                "constraint": "raises EmpiricalQueryResolutionError for unresolved ROUTING_UNKNOWN/RULE_UNAVAILABLE; it cannot be coerced to nonmembership or inferred eligibility",
                "raw_count_note": "raw response values are available in the C11 event carrier; canonical adoption is not required for raw counts, but the original routing/authority gate remains unresolved",
                "canonical_authority": "DEFER; not required for raw counts and not promoted",
            },
        },
        "next_invocation": {
            "function": "rawlsing_next.pre553_empirical_query.execute_empirical_query",
            "current_status": "NOT_INVOKED__BLOCKED_ON_ABOVE_INPUTS",
            "required_context": "sealed SRC04 C11 release + exact EmpiricalQuerySpec/predicate/catalog/historical parent + current original authority",
            "downstream": "existing I05 owner only after exact I05 authority; not this preparation",
        },
    }
    return plan


def build_src04_fixture_held() -> dict[str, Any]:
    """Preserve the SRC04 construction-only fixture as a typed UNAVAILABLE negative."""
    fixture_config = load_source_config(FIXTURE_CONFIG_PATH)
    fixture_stream = load_fixture_stream(FIXTURE_PATH)
    if fixture_stream.source_sha256 != EXPECTED_FIXTURE_SOURCE_SHA256:
        raise ConsumerPreparationRefusal("FIXTURE_SOURCE_SHA_MISMATCH")
    projection = build_governed_c11_projection(
        fixture_config, source_sha256=fixture_stream.source_sha256,
        row_count=fixture_stream.row_count)
    release = build_validated_c11_release_from_config(fixture_config, stream=fixture_stream)
    if release.release_ref.content_hash != EXPECTED_FIXTURE_RELEASE_HASH:
        raise ConsumerPreparationRefusal("FIXTURE_RELEASE_HASH_MISMATCH")
    question_refs = {
        q["question_id"]: exact_ref(q["native_question_ref"], "fixture_target_ref")
        for q in fixture_config.document["questions"]
    }
    q101_slot = next(x for x in fixture_config.document["response_slots"]
                     if x["question_id"] == "q101")
    q101_route = next(x for x in fixture_config.document["routing"]
                      if x["question_id"] == "q101")
    risk_ref = exact_ref(q101_route["risk_set_ref"], "fixture_risk_set_ref")
    bundle = SimpleNamespace(
        projection=projection,
        source_sha256=fixture_stream.source_sha256,
        question_refs=question_refs,
        administered_ids=tuple(question_refs),
        risk_set_ref=risk_ref,
        source_format="SAV",
        physical_stream=fixture_stream,
        release=release,
        administered=(),
        held=(),
        excluded=(),
        unknown=(),
        bundle_hash="fixture-bundle",
        respondent_rows=(),
        occurrence_bindings=(),
    )
    catalog, request = build_projection_catalog(
        bundle=bundle,
        operation=OperationFixture(
            fixture_id="B0-SRC04-FIXTURE-Q101",
            target_variable_code="q101",
            response_value="1",
            measure_kind="RAW",
        ),
        as_of="2026-10-27",
    )
    query = catalog.resolve_query_exact(request.query_ref)
    predicate = catalog.resolve_predicate_exact(request.predicate_ref)
    registry = AuthorityRegistry(catalog.authorities)
    try:
        execution = execute_empirical_query(
            repository=C11Repository((release,)),
            query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(release.release_ref,),
        )
        execution_result = {
            "status": "EXECUTED",
            "fact_count": len(execution.facts),
            "typed_states": sorted({fact.typed_state for fact in execution.facts}),
            "raw_numerator_support": [fact.raw_numerator_support for fact in execution.facts],
            "raw_denominator_support": [fact.raw_denominator_support for fact in execution.facts],
        }
    except Exception as exc:
        execution_result = {
            "status": "REFUSED_OR_TYPED_UNAVAILABLE",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    return {
        "schema": "PYAT_CAMPAIGN_B0_SRC04_FIXTURE_HELD@1.0.0",
        "scope": "SRC04_NONRESPONDENT_FIXTURE_ONLY__UNAVAILABLE_HELD",
        "fixture_config_path": str(FIXTURE_CONFIG_PATH.relative_to(ROOT)),
        "fixture_config_file_sha256": sha_file(FIXTURE_CONFIG_PATH),
        "fixture_path": str(FIXTURE_PATH.relative_to(ROOT)),
        "fixture_source_sha256": fixture_stream.source_sha256,
        "fixture_release_ref": release.release_ref.as_dict(),
        "fixture_projection_identity": projection.projection_identity_ref.as_dict(),
        "catalog_identity": catalog.receipt()["catalog_identity"],
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "request_ref": request.query_ref.as_dict(),
        "target_ref": question_refs["q101"].as_dict(),
        "requested_output_grain": jsonable(query.requested_output_grain),
        "authority_grades": [
            {"authority_id": a.authority_id, "authority_kind": a.authority_kind,
             "decision_state": a.decision_state, "grade": a.scope_envelope.get("grade")}
            for a in catalog.authorities
        ],
        "test_only_query_authority_used": any(
            a.authority_id == "B49-TEST-ONLY-QUERY-AUTH" for a in catalog.authorities),
        "execution": execution_result,
        "product_positive": False,
        "actual_existing_api_calls": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.pre553_native_workload_binding.build_projection_catalog",
            "rawlsing_next.pre553_empirical_query.execute_empirical_query",
        ],
        "original_source_or_release_read": False,
    }


def build_qualified_fixture_positive() -> dict[str, Any]:
    """Construct and execute an existing qualified SRC09 P0 fixture positive.

    This is a separately labelled nonrespondent/tests-only consumer check.  It
    is not the SRC04 original request and its test-only authority is never used
    for an original request.
    """
    fixture_config = load_source_config(QUALIFIED_FIXTURE_CONFIG_PATH)
    fixture_stream = load_fixture_stream(QUALIFIED_FIXTURE_PATH)
    if fixture_stream.source_sha256 != EXPECTED_QUALIFIED_FIXTURE_SOURCE_SHA256:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_SOURCE_SHA_MISMATCH")
    projection = build_governed_c11_projection(
        fixture_config, source_sha256=fixture_stream.source_sha256,
        row_count=fixture_stream.row_count)
    release = build_validated_c11_release_from_config(fixture_config, stream=fixture_stream)
    if release.release_ref.content_hash != EXPECTED_QUALIFIED_FIXTURE_RELEASE_HASH:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_RELEASE_HASH_MISMATCH")
    question_refs = {
        q["question_id"]: exact_ref(q["native_question_ref"], "qualified_fixture_target_ref")
        for q in fixture_config.document["questions"]
    }
    q101_route = next(x for x in fixture_config.document["routing"]
                      if x["question_id"] == "q101")
    risk_ref = exact_ref(q101_route["risk_set_ref"], "qualified_fixture_risk_set_ref")
    bundle = SimpleNamespace(
        projection=projection,
        source_sha256=fixture_stream.source_sha256,
        question_refs=question_refs,
        administered_ids=tuple(question_refs),
        risk_set_ref=risk_ref,
        source_format="SAV",
        physical_stream=fixture_stream,
        release=release,
        administered=(),
        held=(),
        excluded=(),
        unknown=(),
        bundle_hash="qualified-fixture-bundle",
        respondent_rows=(),
        occurrence_bindings=(),
    )
    catalog, request = build_projection_catalog(
        bundle=bundle,
        operation=OperationFixture(
            fixture_id="B0-SRC09-P0-FIXTURE-Q101",
            target_variable_code="q101",
            response_value="1",
            measure_kind="RAW",
        ),
        as_of="2026-10-27",
    )
    query = catalog.resolve_query_exact(request.query_ref)
    predicate = catalog.resolve_predicate_exact(request.predicate_ref)
    execution = execute_empirical_query(
        repository=C11Repository((release,)),
        query=query,
        predicate=predicate,
        authority_registry=AuthorityRegistry(catalog.authorities),
        release_refs=(release.release_ref,),
    )
    if len(execution.facts) != 1:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_FACT_COUNT_NOT_ONE")
    fact = execution.facts[0]
    expected_numerator = sum(
        1 for cell in fixture_stream.iter_cells()
        if cell.variable_name == "q101"
        and cell.raw_value == 1.0
        and cell.missing_state.value == "OBSERVED_STORAGE_VALUE")
    expected_denominator = expected_numerator
    if fact.typed_state != "SUPPORTED":
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_NOT_SUPPORTED", fact.typed_state)
    if fact.raw_numerator_support != expected_numerator:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_NUMERATOR_MISMATCH")
    if fact.raw_denominator_support != expected_denominator:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_DENOMINATOR_MISMATCH")
    if expected_numerator <= 0:
        raise ConsumerPreparationRefusal("QUALIFIED_FIXTURE_ZERO_SUPPORT")
    return {
        "schema": "PYAT_CAMPAIGN_B0_QUALIFIED_FIXTURE_POSITIVE@1.0.0",
        "scope": "SRC09_P0_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_NOT_SRC04",
        "fixture_config_path": str(QUALIFIED_FIXTURE_CONFIG_PATH.relative_to(ROOT)),
        "fixture_config_file_sha256": sha_file(QUALIFIED_FIXTURE_CONFIG_PATH),
        "fixture_path": str(QUALIFIED_FIXTURE_PATH.relative_to(ROOT)),
        "fixture_source_sha256": fixture_stream.source_sha256,
        "fixture_release_ref": release.release_ref.as_dict(),
        "fixture_projection_identity": projection.projection_identity_ref.as_dict(),
        "catalog_identity": catalog.receipt()["catalog_identity"],
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "target_ref": question_refs["q101"].as_dict(),
        "requested_output_grain": jsonable(query.requested_output_grain),
        "authority_grades": [
            {"authority_id": a.authority_id, "authority_kind": a.authority_kind,
             "decision_state": a.decision_state, "grade": a.scope_envelope.get("grade")}
            for a in catalog.authorities
        ],
        "test_only_query_authority_used": any(
            a.authority_id == "B49-TEST-ONLY-QUERY-AUTH" for a in catalog.authorities),
        "execution": {
            "status": "EXECUTED_SUPPORTED",
            "fact_count": len(execution.facts),
            "typed_states": [fact.typed_state],
            "raw_numerator_support": [fact.raw_numerator_support],
            "raw_denominator_support": [fact.raw_denominator_support],
            "fact_ref": fact.ref.as_dict(),
        },
        "independent_count_check": {
            "source_fixture_rows": fixture_stream.row_count,
            "target_variable": "q101",
            "target_raw_value": 1.0,
            "expected_numerator": expected_numerator,
            "expected_denominator": expected_denominator,
            "matches_empirical_fact": True,
        },
        "actual_existing_api_calls": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.pre553_native_workload_binding.build_projection_catalog",
            "rawlsing_next.pre553_empirical_query.execute_empirical_query",
        ],
        "product_positive": True,
        "original_source_or_release_read": False,
    }


def fixture_target_mismatch() -> dict[str, Any]:
    fixture_config = load_source_config(FIXTURE_CONFIG_PATH)
    fixture_stream = load_fixture_stream(FIXTURE_PATH)
    projection = build_governed_c11_projection(
        fixture_config, source_sha256=fixture_stream.source_sha256,
        row_count=fixture_stream.row_count)
    question_refs = {
        q["question_id"]: exact_ref(q["native_question_ref"], "fixture_target_ref")
        for q in fixture_config.document["questions"]
    }
    q101_route = next(x for x in fixture_config.document["routing"]
                      if x["question_id"] == "q101")
    bundle = SimpleNamespace(
        projection=projection, source_sha256=fixture_stream.source_sha256,
        question_refs=question_refs, administered_ids=tuple(question_refs),
        risk_set_ref=exact_ref(q101_route["risk_set_ref"], "fixture_risk_set_ref"),
        source_format="SAV", physical_stream=fixture_stream, release=None,
        administered=(), held=(), excluded=(), unknown=(), bundle_hash="fixture-bundle",
        respondent_rows=(), occurrence_bindings=(),
    )
    try:
        build_projection_catalog(
            bundle=bundle,
            operation=OperationFixture("B0-SRC04-FIXTURE-MISSING", "q999", "1", "RAW"),
            as_of="2026-10-27",
        )
    except WorkloadBindingRefusal as exc:
        return {
            "schema": "PYAT_CAMPAIGN_B0_SRC04_FIXTURE_MISMATCH@1.0.0",
            "status": "REFUSED",
            "expected": "FIXTURE_TARGET_NOT_ADMINISTERED",
            "actual_code": exc.code,
            "actual_detail": exc.detail,
            "original_source_or_release_read": False,
        }
    raise ConsumerPreparationRefusal("FIXTURE_TARGET_MISMATCH_NOT_REFUSED")


def original_release_mismatch_negative() -> dict[str, Any]:
    config, receipt, receipt_sha, _ = _config_and_receipt()
    tampered = deepcopy(receipt)
    tampered["release"]["release_ref"]["content_hash"] = "0" * 64
    try:
        prepare_original_request_plan(tampered, config)
    except ConsumerPreparationRefusal as exc:
        return {
            "schema": "PYAT_CAMPAIGN_B0_SRC04_RELEASE_MISMATCH_NEGATIVE@1.0.0",
            "status": "REFUSED",
            "expected": "RELEASE_HASH_MISMATCH",
            "actual_code": exc.code,
            "source_release_receipt_sha256": receipt_sha,
            "source_read_performed": False,
        }
    raise ConsumerPreparationRefusal("RELEASE_MISMATCH_NOT_REFUSED")
