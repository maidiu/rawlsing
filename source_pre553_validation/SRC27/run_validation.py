"""Execute and record the actual R157 LITS native validation traces.

This runner reads only the committed lane configs/fixtures and the frozen
factory/native owners.  It does not read original respondent files, decode an
original source, or issue an original workload.  It writes per-source
validation_results.json, exception_ledger.json and build_manifest.json, then a
lane-wide LANE_RETURN.json.
"""
from __future__ import annotations

import copy
import hashlib
import json
import traceback
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.source_configuration.errors import (
    SourceConfigurationBindingError,
    SourceConfigurationFactoryError,
    SourceConfigurationSchemaError,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.reader import reader_configuration_from_config
from rawlsing_next.source_configuration.schema import (
    canonical_config_hash,
    load_source_config,
    validate_source_config,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "rawlsing_next" / "source_configuration" / "data"
VALIDATION_ROOT = ROOT / "source_pre553_validation"
SOURCES = ("SRC27", "SRC28", "SRC29", "SRC30")
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
BASE_HEAD = "91441c34ee58c4c3b13dae37db70a23bb4d4c2b8"
P0_DEPENDENCY = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
P3_DEPENDENCY = "519355ec2215409b40d566ef13c3b21f611e0726"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bytes_of(path: Path) -> int:
    return len(path.read_bytes())


def event_truth(release: Any, fixture_config: Any) -> dict[str, Any]:
    question_id_by_native: dict[str, str] = {}
    for question in fixture_config.document["questions"]:
        question_id_by_native[question["native_question_ref"]["object_id"]] = question["question_id"]
    respondent_key_by_ref: dict[str, str] = {}
    for record in release.internal_records:
        if getattr(record, "RECORD_FAMILY", None) == "RespondentIdentity":
            respondent_key_by_ref[record.ref.key] = record.respondent_key
    events = [obj for obj in release.public_objects if obj.schema_id == "RespondentEvent"]
    rows: dict[str, list[tuple[int, str, Any]]] = {}
    for event in events:
        qid = question_id_by_native[exact_ref(event.native_question_ref).object_id]
        respondent_key = respondent_key_by_ref[exact_ref(event.scoped_respondent_ref).key]
        row = int(respondent_key.rsplit(":", 1)[-1])
        rows.setdefault(qid, []).append(
            (row, event.typed_state, event.canonical_response_value_if_authorized)
        )
    states: dict[str, list[str]] = {}
    canonical: dict[str, list[Any]] = {}
    for qid, values in rows.items():
        values.sort(key=lambda item: item[0])
        states[qid] = [item[1] for item in values]
        canonical[qid] = [item[2] for item in values]
    return {"states": states, "canonical": canonical, "event_count": len(events)}


def check_raises(fn, expected_type, label: str) -> dict[str, Any]:
    expected_name = (
        "/".join(item.__name__ for item in expected_type)
        if isinstance(expected_type, tuple)
        else expected_type.__name__
    )
    try:
        fn()
    except expected_type as exc:
        return {
            "check": label,
            "status": "PASS",
            "expected_exception": expected_name,
            "actual_exception": type(exc).__name__,
            "message": str(exc)[:500],
        }
    except Exception as exc:  # noqa: BLE001 - recorded as an actual failed check
        return {
            "check": label,
            "status": "FAIL",
            "expected_exception": expected_name,
            "actual_exception": type(exc).__name__,
            "message": str(exc)[:500],
        }
    return {
        "check": label,
        "status": "FAIL",
        "expected_exception": expected_name,
        "actual_exception": None,
        "message": "no exception raised",
    }


def source_validation(source_id: str) -> dict[str, Any]:
    data_dir = DATA_ROOT / source_id
    validation_dir = VALIDATION_ROOT / source_id
    original_path = data_dir / f"{source_id.lower()}.config.json"
    accounting_path = data_dir / f"{source_id.lower()}.item_accounting.jsonl"
    correspondence_path = data_dir / f"{source_id.lower()}.correspondence.json"
    fixture_path = validation_dir / "fixture.json"
    fixture_config_path = validation_dir / "fixture.config.json"
    expected_path = validation_dir / "expected_results.json"

    original = load_source_config(original_path)
    fixture_config = load_source_config(fixture_config_path)
    fixture_stream = load_fixture_stream(fixture_path)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    identity = original.document["identity"]
    coverage = original.document["coverage"]
    serialized_slots = {
        (slot["ordinal"], slot["name"]) for slot in original.document["physical_slots"]
    }
    included_slots = set(coverage["physical_slots_included"])
    excluded_slots = {item["ordinal"] for item in coverage.get("physical_slots_excluded", [])}
    serialized_items = {
        item["implementation_id"] for item in original.document["items"]
    }
    included_items = set(coverage["items_included"])
    excluded_items = {
        item["implementation_id"] for item in coverage.get("items_excluded", [])
    }
    no_drop = {
        "physical_slots_serialized": len(serialized_slots),
        "physical_slots_expected": identity["source_column_count"],
        "physical_slots_included": len(included_slots),
        "physical_slots_excluded": len(excluded_slots),
        "physical_slots_covered": len(included_slots | excluded_slots),
        "physical_slots_complete": (
            len(serialized_slots) == identity["source_column_count"]
            and included_slots | excluded_slots == set(range(1, identity["source_column_count"] + 1))
            and not (included_slots & excluded_slots)
        ),
        "items_serialized": len(serialized_items),
        "items_expected": identity["original_item_count"],
        "items_included": len(included_items),
        "items_excluded": len(excluded_items),
        "items_covered": len(included_items | excluded_items),
        "items_complete": (
            len(serialized_items) == identity["original_item_count"]
            and included_items | excluded_items == serialized_items
            and not (included_items & excluded_items)
        ),
    }
    slot_dispositions = Counter(
        slot["disposition"] for slot in original.document["physical_slots"]
    )
    item_dispositions = Counter(
        item["disposition"] for item in original.document["items"]
    )
    original_states = Counter(
        snapshot["typed_state"] for snapshot in original.document["authority"]["snapshots"]
    )
    fixture_states = Counter(
        snapshot["typed_state"] for snapshot in fixture_config.document["authority"]["snapshots"]
    )
    fixture_scope_grades = sorted(
        {
            str((snapshot.get("scope_envelope") or {}).get("grade"))
            for snapshot in fixture_config.document["authority"]["snapshots"]
        }
    )

    binding_separation = {
        "original_identity_class": original.document["binding"]["identity_class"],
        "original_source_sha256": original.document["binding"]["source_sha256"],
        "fixture_identity_class": fixture_config.document["binding"]["identity_class"],
        "fixture_source_sha256": fixture_config.document["binding"]["source_sha256"],
        "fixture_stream_sha256": fixture_stream.source_sha256,
        "fixture_sha_distinct_from_original": (
            fixture_config.document["binding"]["source_sha256"]
            != original.document["binding"]["source_sha256"]
        ),
        "fixture_stream_matches_config": (
            fixture_stream.source_sha256
            == fixture_config.document["binding"]["source_sha256"]
        ),
        "fixture_provenance_original_source_id": (
            fixture_config.document["binding"]["fixture_provenance"]["original_source_id"]
        ),
        "fixture_provenance_original_source_sha256": (
            fixture_config.document["binding"]["fixture_provenance"]["original_source_sha256"]
        ),
        "fixture_no_original_respondents": (
            fixture_config.document["binding"]["fixture_provenance"]["no_original_respondents"]
        ),
        "original_has_fixture_provenance": (
            "fixture_provenance" in original.document["binding"]
        ),
        "fixture_authority_scope_grades": fixture_scope_grades,
    }

    reader = reader_configuration_from_config(original)
    fixture_reader_refusal = check_raises(
        lambda: reader_configuration_from_config(fixture_config),
        SourceConfigurationBindingError,
        "fixture config must refuse original source-read transport",
    )
    keys = row_native_keys_from_transport(fixture_config, stream=fixture_stream)
    key_kinds = sorted({key.kind for key in keys.values()}) if keys else []
    key_witnesses = {
        "configured_key_slot": fixture_config.document["respondents"].get("source_native_key_slot"),
        "witness_count": len(keys) if keys else 0,
        "row_count": fixture_stream.row_count,
        "witness_kinds": key_kinds,
        "one_witness_per_row": bool(keys) and set(keys) == set(range(1, fixture_stream.row_count + 1)),
    }

    release = build_validated_c11_release_from_config(
        fixture_config, stream=fixture_stream
    )
    repo, repo_release = build_source_backed_c11_repository_from_config(
        fixture_config, fixture_stream
    )
    truth = event_truth(release, fixture_config)
    expected_states = expected["response_states_by_question"]
    expected_canonical = expected["canonical_values_by_question"]
    states_match = truth["states"] == expected_states
    canonical_match = truth["canonical"] == expected_canonical
    family_counts = Counter(obj.schema_id for obj in release.public_objects)
    internal_counts = Counter(record.RECORD_FAMILY for record in release.internal_records)
    m01_m18 = {key: list(value) for key, value in release.m01_m18_coverage.items()}

    # Representative ORIGINAL_IDENTITY projection construction.  The full
    # original routing set would materialize millions of facts; this positive
    # construction uses the exact original identity/authority plus the same
    # representative source rules that the fixture exercises.
    original_slice = copy.deepcopy(dict(original.document))
    fixture_qids = {
        question["question_id"] for question in fixture_config.document["questions"]
    }
    fixture_vars = {
        slot["slot"]["name"] for slot in fixture_config.document["response_slots"]
    }
    country_slot = fixture_config.document["coordinate_slots"][0]["slot"]["name"]
    original_slice["questions"] = [
        q for q in original_slice["questions"] if q["question_id"] in fixture_qids
    ]
    original_slice["response_slots"] = [
        s for s in original_slice["response_slots"] if s["slot"]["name"] in fixture_vars
    ]
    original_slice["coordinate_slots"] = [
        s for s in original_slice["coordinate_slots"] if s["slot"]["name"] == country_slot
    ]
    original_slice["routing"] = [
        r for r in original_slice["routing"] if r["question_id"] in fixture_qids
    ]
    original_slice["supported_scope"]["supported_question_ids"] = sorted(fixture_qids)
    original_projection = build_governed_c11_projection(original_slice)
    original_projection_counts = {
        "universes": len(original_projection.universes),
        "respondents": len(original_projection.respondents),
        "questions": len(original_projection.questions),
        "response_slots": len(original_projection.response_slots),
        "coordinate_slots": len(original_projection.coordinate_slots),
        "routing": len(original_projection.routing),
        "weight_slots": len(original_projection.weight_slots),
        "authority_snapshots": len(original_projection.authority_snapshots),
        "expected_source_sha256": original_projection.expected_source_sha256,
        "cache_identity": original_projection.cache_identity,
    }

    # Identity and authority refusal checks.
    wrong_sha_stream = ExactPhysicalCellStream(
        source_sha256="0" * 64,
        row_count=fixture_stream.row_count,
        cell_iter_factory=lambda: fixture_stream.iter_cells(),
        transport_identity="R157_WRONG_SHA_REFUSAL_PROBE",
    )
    wrong_rows_stream = ExactPhysicalCellStream(
        source_sha256=fixture_stream.source_sha256,
        row_count=fixture_stream.row_count + 1,
        cell_iter_factory=lambda: fixture_stream.iter_cells(),
        transport_identity="R157_WRONG_ROW_COUNT_REFUSAL_PROBE",
    )
    original_with_fixture_stream = check_raises(
        lambda: build_validated_c11_release_from_config(
            original, stream=fixture_stream
        ),
        SourceConfigurationBindingError,
        "original config must refuse fixture transport",
    )
    fixture_with_wrong_sha = check_raises(
        lambda: build_validated_c11_release_from_config(
            fixture_config, stream=wrong_sha_stream
        ),
        SourceConfigurationBindingError,
        "fixture config must refuse wrong source SHA",
    )
    fixture_with_wrong_rows = check_raises(
        lambda: build_validated_c11_release_from_config(
            fixture_config, stream=wrong_rows_stream
        ),
        (SourceConfigurationBindingError, SourceConfigurationFactoryError),
        "fixture config must refuse wrong row count",
    )
    original_with_fixture_authority = copy.deepcopy(dict(original.document))
    for snapshot in original_with_fixture_authority["authority"]["snapshots"]:
        snapshot["scope_envelope"]["fixture_only"] = True
        snapshot["scope_envelope"]["grade"] = "NONRESPONDENT_FIXTURE_ONLY"
    schema_original_fixture_authority = check_raises(
        lambda: validate_source_config(original_with_fixture_authority),
        SourceConfigurationSchemaError,
        "original config must refuse fixture-only authority",
    )
    fixture_with_original_sha = copy.deepcopy(dict(fixture_config.document))
    fixture_with_original_sha["binding"]["source_sha256"] = identity["expected_source_sha256"]
    fixture_with_original_sha["binding"]["source_snapshot_ref"]["content_hash"] = identity["expected_source_sha256"]
    schema_fixture_original_sha = check_raises(
        lambda: validate_source_config(fixture_with_original_sha),
        SourceConfigurationSchemaError,
        "fixture config must refuse original source SHA",
    )
    fixture_with_original_authority = copy.deepcopy(dict(fixture_config.document))
    for snapshot in fixture_with_original_authority["authority"]["snapshots"]:
        snapshot["scope_envelope"].pop("fixture_only", None)
        snapshot["scope_envelope"]["grade"] = "SOURCE_REVIEWED_SOURCE_LOCAL_EVIDENCE__PREPARATION_ONLY"
    schema_fixture_original_authority = check_raises(
        lambda: validate_source_config(fixture_with_original_authority),
        SourceConfigurationSchemaError,
        "fixture config must refuse non-fixture authority",
    )

    negative_checks = [
        original_with_fixture_stream,
        fixture_with_wrong_sha,
        fixture_with_wrong_rows,
        schema_original_fixture_authority,
        schema_fixture_original_sha,
        schema_fixture_original_authority,
        fixture_reader_refusal,
    ]
    passed = sum(1 for check in negative_checks if check["status"] == "PASS")
    failed = sum(1 for check in negative_checks if check["status"] == "FAIL")

    skips = [
        {
            "check": "decode_config_with_source_read_permission",
            "status": "SKIP",
            "reason": (
                "No original source read decision/resolver or source path is present under "
                "R157 preparation; original respondent decode is not authorized. Reader "
                "configuration extraction succeeded without source I/O."
            ),
        },
        {
            "check": "full_original_routing_projection",
            "status": "SKIP",
            "reason": (
                "The full prepared routing set would materialize millions of routing facts. "
                "The actual factory is positively exercised on the original-identity "
                "representative slice and on the nonrespondent fixture release; the full "
                "original config is schema/coverage validated. No original read occurred."
            ),
        },
    ]

    result = {
        "schema": "PYAT_R157_LITS_SOURCE_NATIVE_VALIDATION@1.0.0",
        "source_id": source_id,
        "lane_id": "LITS",
        "plan_seal": PLAN_SEAL,
        "lane_base_head": BASE_HEAD,
        "p0_dependency_commit": P0_DEPENDENCY,
        "p3_dependency_commit": P3_DEPENDENCY,
        "commands": {
            "regenerate": "PYTHONPATH=. python3 rawlsing_next/source_configuration/data/SRC27/lits_full_bindings.py",
            "validate": "PYTHONPATH=. python3 source_pre553_validation/SRC27/run_validation.py",
            "tests": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts=''",
        },
        "files": {
            "original_config": str(original_path.relative_to(ROOT)),
            "original_config_sha256": sha256(original_path),
            "original_config_canonical_hash": canonical_config_hash(original),
            "item_accounting": str(accounting_path.relative_to(ROOT)),
            "item_accounting_sha256": sha256(accounting_path),
            "item_accounting_bytes": bytes_of(accounting_path),
            "correspondence": str(correspondence_path.relative_to(ROOT)),
            "correspondence_sha256": sha256(correspondence_path),
            "fixture": str(fixture_path.relative_to(ROOT)),
            "fixture_sha256": sha256(fixture_path),
            "fixture_source_sha256": fixture_stream.source_sha256,
            "fixture_config": str(fixture_config_path.relative_to(ROOT)),
            "fixture_config_sha256": sha256(fixture_config_path),
            "fixture_config_canonical_hash": canonical_config_hash(fixture_config),
            "expected_results": str(expected_path.relative_to(ROOT)),
            "expected_results_sha256": sha256(expected_path),
        },
        "schema_validation": {
            "original": "PASS",
            "fixture_config": "PASS",
            "fixture_stream": "PASS",
            "original_questions": len(original.document["questions"]),
            "original_response_slots": len(original.document["response_slots"]),
            "original_coordinate_slots": len(original.document["coordinate_slots"]),
            "original_weight_slots": len(original.document["weight_slots"]),
            "original_routing": len(original.document["routing"]),
            "original_declared_supported_questions": len(
                original.document["supported_scope"]["supported_question_ids"]
            ),
            "original_prepared_questions": len(original.document["questions"]),
            "fixture_questions": len(fixture_config.document["questions"]),
            "fixture_response_slots": len(fixture_config.document["response_slots"]),
            "fixture_coordinate_slots": len(fixture_config.document["coordinate_slots"]),
            "fixture_routing": len(fixture_config.document["routing"]),
        },
        "no_drop": no_drop,
        "dispositions": {
            "physical_slots": dict(sorted(slot_dispositions.items())),
            "items": dict(sorted(item_dispositions.items())),
        },
        "original_authority_states": dict(sorted(original_states.items())),
        "fixture_authority_states": dict(sorted(fixture_states.items())),
        "binding_separation": binding_separation,
        "reader_transport": {
            "call": "rawlsing_next.source_configuration.reader.reader_configuration_from_config",
            "original_config": "PASS",
            "source_sha256": reader.source_sha256,
            "encoding": reader.encoding,
            "authority_status": reader.authority_status,
            "configuration_ref": reader.configuration_ref.as_dict() if reader.configuration_ref else None,
            "fixture_config_refusal": fixture_reader_refusal,
            "decode_call": "NOT_CALLED__NO_ORIGINAL_READ_PERMISSION_OR_SOURCE_PATH",
        },
        "fixture_key_path": key_witnesses,
        "native_calls": [
            {
                "call": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
                "input": "ORIGINAL_IDENTITY_REPRESENTATIVE_SLICE (same source rules as fixture; original identity/authority)",
                "result": "GovernedC11Projection",
                "counts": original_projection_counts,
                "original_source_sha256": original_projection.expected_source_sha256,
                "original_sha_preserved": (
                    original_projection.expected_source_sha256
                    == identity["expected_source_sha256"]
                ),
            },
            {
                "call": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
                "input": "NONRESPONDENT_FIXTURE config + ExactPhysicalCellStream",
                "result": "C11LogicalRelease",
                "release_ref": release.release_ref.as_dict(),
                "semantic_release_hash": release.semantic_release_hash,
                "source_release_manifest_hash": release.source_release_manifest_hash,
                "fixture_source_sha256": fixture_stream.source_sha256,
                "public_object_count": len(release.public_objects),
                "internal_record_count": len(release.internal_records),
                "public_families": dict(sorted(family_counts.items())),
                "internal_families": dict(sorted(internal_counts.items())),
                "m01_m18_coverage_keys": sorted(m01_m18),
            },
            {
                "call": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
                "input": "NONRESPONDENT_FIXTURE config + ExactPhysicalCellStream",
                "result": "C11Repository",
                "repository_length": len(repo),
                "repository_release_refs": [ref.as_dict() for ref in repo.release_refs],
                "repository_release_matches_validated_release": (
                    repo_release.release_ref.key == release.release_ref.key
                ),
            },
        ],
        "expected_vs_actual": {
            "response_event_count_expected": expected["response_event_count"],
            "response_event_count_actual": truth["event_count"],
            "response_states_match": states_match,
            "canonical_values_match": canonical_match,
            "expected_response_states": expected_states,
            "actual_response_states": truth["states"],
            "expected_canonical_values": expected_canonical,
            "actual_canonical_values": truth["canonical"],
            "coordinate_fact_count_expected": expected["coordinate_fact_count"],
            "coordinate_fact_count_actual": family_counts.get("EmpiricalCoordinateFact", 0),
            "routing_fact_count_expected": expected["routing_fact_count"],
            "routing_fact_count_actual": family_counts.get("RoutingEligibilityFact", 0),
            "universe_count_actual": family_counts.get("EmpiricalUniverse", 0),
            "authority_snapshot_count_expected": expected["authority_snapshot_count"],
            "authority_snapshot_count_actual": family_counts.get("AuthoritySnapshot", 0),
        },
        "negative_checks": negative_checks,
        "pass_count": passed,
        "fail_count": failed,
        "skip_count": len(skips),
        "skips": skips,
        "original_respondent_rows_read": 0,
        "original_source_io_performed": False,
        "original_workload_issued": False,
        "limits": [
            "The native release is a nonrespondent fixture release; it is not original respondent data.",
            "Original source execution and original workload issuance are not performed or claimed.",
            "The full original config is schema/coverage validated; its full routing projection is not materialized because it would create millions of facts. The representative original-identity projection and the fixture release are actual factory calls.",
            "Fixture authority is NONRESPONDENT_FIXTURE_ONLY and cannot be promoted to original-source authority.",
        ],
    }
    return result


def write_exception_ledger(source_id: str, original: Any) -> Path:
    path = VALIDATION_ROOT / source_id / "exception_ledger.json"
    document = {
        "schema": "PYAT_R157_LITS_EXCEPTION_LEDGER@1.0.0",
        "source_id": source_id,
        "lane_id": "LITS",
        "residuals": original.document["residuals"],
        "api_limitations": [
            {
                "field": "coordinate.normalization_ref",
                "native_owner": "rawlsing_next.pre553_empirical_objects.EmpiricalCoordinateFact canonicalization",
                "observed_counterexample": (
                    "A TypedAbsence in CoordinateSlotRule.normalization_ref is serialized by the "
                    "validator but rejected at native projection with Pre553IntegrityError: "
                    "'unsupported semantic identity type: TypedAbsence'."
                ),
                "representation_used": (
                    "normalization_ref is null; no crosswalk/canonical geography is asserted, and "
                    "the no-crosswalk premise is carried in notes/residuals."
                ),
                "dependent_operation": "coordinate fact projection",
                "unaffected_scope": "raw coordinate value witness and all response bindings",
                "owner": "shared P0/P3 native owner; not modified by the lane",
                "status": "PRESERVED_NOT_FIXED_IN_SHARED_RUNTIME",
            }
        ],
        "fixture_limits": [
            "Fixture cells are nonrespondent and cannot be used as original respondent observations.",
            "Fixture-only authority and fixture SHA are not original-source meaning.",
            "Native fixture validation does not establish original scientific results or execution permission.",
        ],
        "original_access": {
            "original_respondent_rows_read": 0,
            "original_source_io_performed": False,
            "original_workload_issued": False,
        },
    }
    path.write_text(
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    results = []
    for source_id in SOURCES:
        source_result = source_validation(source_id)
        validation_path = VALIDATION_ROOT / source_id / "validation_results.json"
        validation_path.write_text(
            json.dumps(source_result, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        original = load_source_config(
            DATA_ROOT / source_id / f"{source_id.lower()}.config.json"
        )
        ledger_path = write_exception_ledger(source_id, original)
        files = {
            "original_config": DATA_ROOT / source_id / f"{source_id.lower()}.config.json",
            "item_accounting": DATA_ROOT / source_id / f"{source_id.lower()}.item_accounting.jsonl",
            "correspondence": DATA_ROOT / source_id / f"{source_id.lower()}.correspondence.json",
            "fixture": VALIDATION_ROOT / source_id / "fixture.json",
            "fixture_config": VALIDATION_ROOT / source_id / "fixture.config.json",
            "expected_results": VALIDATION_ROOT / source_id / "expected_results.json",
            "validation_results": validation_path,
            "exception_ledger": ledger_path,
        }
        if source_id == "SRC27":
            files["lane_builder"] = DATA_ROOT / "SRC27" / "lits_lane_build.py"
            files["full_builder"] = DATA_ROOT / "SRC27" / "lits_full_bindings.py"
            files["validation_runner"] = VALIDATION_ROOT / "SRC27" / "run_validation.py"
        manifest = {
            "schema": "PYAT_R157_LITS_SOURCE_BUILD_MANIFEST@1.0.0",
            "source_id": source_id,
            "files": {
                name: {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path),
                    "bytes": bytes_of(path),
                }
                for name, path in files.items()
                if path.is_file()
            },
        }
        manifest_path = VALIDATION_ROOT / source_id / "build_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        source_result["build_manifest"] = str(manifest_path.relative_to(ROOT))
        source_result["build_manifest_sha256"] = sha256(manifest_path)
        results.append(source_result)
        print(
            source_id,
            "PASS" if source_result["fail_count"] == 0 else "FAIL",
            "native release",
            source_result["native_calls"][1]["release_ref"]["content_hash"][:16],
            "pass/fail/skip",
            source_result["pass_count"],
            source_result["fail_count"],
            source_result["skip_count"],
        )

    lane_return = {
        "schema": "PYAT_R157_LITS_LANE_RETURN@1.0.0",
        "lane_id": "LITS",
        "branch": "agent/pyat-pre553-r157-lits",
        "plan_seal": PLAN_SEAL,
        "lane_base_head": BASE_HEAD,
        "p0_dependency_commit": P0_DEPENDENCY,
        "p3_dependency_commit": P3_DEPENDENCY,
        "artifact_commit": None,
        "sources": [
            {
                "source_id": result["source_id"],
                "original_config": result["files"]["original_config"],
                "original_config_sha256": result["files"]["original_config_sha256"],
                "original_config_canonical_hash": result["files"]["original_config_canonical_hash"],
                "item_accounting": result["files"]["item_accounting"],
                "item_accounting_sha256": result["files"]["item_accounting_sha256"],
                "correspondence": result["files"]["correspondence"],
                "correspondence_sha256": result["files"]["correspondence_sha256"],
                "fixture": result["files"]["fixture"],
                "fixture_sha256": result["files"]["fixture_sha256"],
                "fixture_source_sha256": result["files"]["fixture_source_sha256"],
                "fixture_config": result["files"]["fixture_config"],
                "fixture_config_sha256": result["files"]["fixture_config_sha256"],
                "validation_results": str((VALIDATION_ROOT / result["source_id"] / "validation_results.json").relative_to(ROOT)),
                "validation_results_sha256": sha256(VALIDATION_ROOT / result["source_id"] / "validation_results.json"),
                "exception_ledger": str((VALIDATION_ROOT / result["source_id"] / "exception_ledger.json").relative_to(ROOT)),
                "exception_ledger_sha256": sha256(VALIDATION_ROOT / result["source_id"] / "exception_ledger.json"),
                "build_manifest": result["build_manifest"],
                "build_manifest_sha256": result["build_manifest_sha256"],
                "scope_counts": {
                    "physical_slots": result["no_drop"]["physical_slots_serialized"],
                    "items": result["no_drop"]["items_serialized"],
                    "questions": result["schema_validation"]["original_questions"],
                    "response_slots": result["schema_validation"]["original_response_slots"],
                    "coordinate_slots": result["schema_validation"]["original_coordinate_slots"],
                    "weight_slots": result["schema_validation"]["original_weight_slots"],
                    "routing_rules": result["schema_validation"]["original_routing"],
                    "prepared_questions": result["schema_validation"]["original_prepared_questions"],
                    "declared_supported_questions": result["schema_validation"]["original_declared_supported_questions"],
                    "response_bound": result["dispositions"]["items"].get("INCLUDED_RESPONSE_SLOT", 0)
                    + result["dispositions"]["items"].get("INCLUDED_REPEATED_RESPONSE_SLOT", 0),
                    "response_authority_gap": result["dispositions"]["items"].get("HELD_RESPONSE_AUTHORITY_GAP", 0),
                    "coordinate_items": result["dispositions"]["items"].get("INCLUDED_COORDINATE_SLOT", 0),
                    "key_held": result["dispositions"]["items"].get("SOURCE_NATIVE_KEY_SLOT_HELD_UNTIL_DECODE", 0),
                    "weight_held": result["dispositions"]["items"].get("WEIGHT_HELD_NO_DESIGN_AUTHORITY", 0),
                },
                "native_release_ref": result["native_calls"][1]["release_ref"],
                "native_pass": result["fail_count"] == 0,
                "negative_checks_pass": result["pass_count"],
                "negative_checks_fail": result["fail_count"],
                "skips": result["skip_count"],
                "residuals": [residual["residual_id"] for residual in load_source_config(
                    DATA_ROOT / result["source_id"] / f"{result['source_id'].lower()}.config.json"
                ).document["residuals"]],
            }
            for result in results
        ],
        "native_calls_summary": {
            "governed_projection_calls": 4,
            "validated_release_calls": 4,
            "repository_calls": 4,
            "reader_config_extractions": 4,
            "reader_fixture_refusals": 4,
            "row_key_extractions": 4,
            "negative_checks_pass": sum(result["pass_count"] for result in results),
            "negative_checks_fail": sum(result["fail_count"] for result in results),
            "skips": sum(result["skip_count"] for result in results),
        },
        "no_drop_summary": {
            "sources": len(results),
            "physical_slots": sum(result["no_drop"]["physical_slots_serialized"] for result in results),
            "items": sum(result["no_drop"]["items_serialized"] for result in results),
            "physical_slots_complete": all(result["no_drop"]["physical_slots_complete"] for result in results),
            "items_complete": all(result["no_drop"]["items_complete"] for result in results),
        },
        "original_access": {
            "original_respondent_rows_read": 0,
            "original_source_io_performed": False,
            "original_workload_issued": False,
        },
        "blockers": [],
        "next_integration_edge": (
            "P3/P5 integration owner consumes these four source configs and fixture traces; "
            "the remaining shared edge is the coherent all35 reader/config integration and "
            "final distinct review, not another LITS source survey."
        ),
        "limits": [
            "Original source execution and original workload issuance are NOT performed.",
            "Native releases are nonrespondent fixture releases with fixture-only authority.",
            "Routing for bound items without exact O06 clauses is typed ROUTING_UNKNOWN; administrative routes are NOT_ASKED.",
            "Response-authority-gap items are held with exact P2 status, not called unselected.",
            "Weights/native keys/forms/admin remain exact scoped unknowns or held; no default is invented.",
        ],
    }
    lane_return_path = VALIDATION_ROOT / "SRC27" / "LANE_RETURN.json"
    lane_return_path.write_text(
        json.dumps(lane_return, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    print("LANE_RETURN", lane_return_path.relative_to(ROOT), sha256(lane_return_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
