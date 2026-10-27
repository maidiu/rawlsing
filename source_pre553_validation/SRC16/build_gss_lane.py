"""Build and natively validate the R157 GSS source-configuration lane.

This helper lives inside the GSS lane write terrain.  It reads only the frozen
portable evidence package, writes only the assigned SRC16..SRC23 data and
validation directories, and never reads an original respondent file.

Run from the repository root:

    PYTHONPATH=. python3 source_pre553_validation/SRC16/build_gss_lane.py --all
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_ingest import INGEST_CONTRACT_VERSION
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    WeightMeasureFact,
    semantic_hash,
)
from rawlsing_next.pre553_r5_codec import CODEC_VERSION as R5_CODEC_VERSION
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.source_configuration.evidence import (
    iter_codebook_rows,
    iter_item_evidence,
    iter_physical_slots,
    load_manifest,
    source_roster_entry,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.source_configuration.fixture import (
    fixture_document_sha256,
    load_fixture_stream,
)
from rawlsing_next.source_configuration.reader import (
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import (
    canonical_config_hash,
    config_file_sha256,
    load_source_config,
    validate_source_config,
)

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "rawlsing_next/source_configuration/data"
VALIDATION_ROOT = ROOT / "source_pre553_validation"
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
P0_CORRECTION = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
P3_RUNTIME = "519355ec2215409b40d566ef13c3b21f611e0726"
SOURCE_IDS = tuple(f"SRC{i:02d}" for i in range(16, 24))
SELECTED_QUESTIONS = ("happy", "satfin", "abdefect")
FIXTURE_ID = "R157-GSS-{source_id}-NONRESPONDENT-SCALAR"
FIXTURE_ROWS = 6
FIXTURE_DATA = (
    # row, happy, satfin, abdefect, region, wtssall
    (1, 1.0, 1.0, 1.0, 1.0, 0.75),
    (2, 2.0, 2.0, 2.0, 2.0, 0.5),
    (3, 3.0, 3.0, 1.0, 3.0, 2.0),
    (4, -98.0, -90.0, -100.0, 4.0, 1.25),
    (5, -99.0, -97.0, -40.0, 1.0, 1.5),
    (6, None, -95.0, -96.0, 2.0, None),
)
MISSING_RESPONSE_STATES = {
    -100.0: "INAPPLICABLE",
    -40.0: "SOURCE_SPECIFIC_SPECIAL",
    -70.0: "NOT_ASKED",
    -80.0: "NOT_ASKED",
    -90.0: "REFUSAL",
    -94.0: "INVALID_UNRESOLVED",
    -95.0: "INVALID_UNRESOLVED",
    -96.0: "SOURCE_SPECIFIC_SPECIAL",
    -97.0: "NOT_ASKED",
    -98.0: "DK",
    -99.0: "MISSING",
}
ADMIN_SLOTS = {
    "ballot", "ballotformwt", "ballotformwtnr", "fileversion", "form",
    "oversamp", "sample", "version", "vpsu", "vstrat",
}
SUPPORTED_SCOPE_NOTE = (
    "Source-local scalar response rules are prepared. Original respondent "
    "execution is NOT performed or claimed under R157 preparation."
)


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str, material: Any) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


def _ref_dict(value: ExactRef) -> dict[str, str]:
    return value.as_dict()


def _auth_dict(value: AuthorityRef) -> dict[str, str]:
    return value.as_dict()


def _json_write(path: Path, document: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _file_identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _authority_snapshot(
    *,
    authority_id: str,
    authority_kind: str,
    decision: str,
    source_id: str,
    original_sha: str,
    wave: str,
    families: Sequence[str],
    operations: Sequence[str],
    bundle_sha256: str,
    fixture_id: str | None = None,
    fixture_sha: str | None = None,
    protocol: bool = False,
) -> dict[str, Any]:
    if fixture_id is not None:
        scope = {
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "fixture_id": fixture_id,
            "source_id": source_id,
            "source_sha256": original_sha,
            "fixture_source_sha256": fixture_sha,
            "original_source_sha256": original_sha,
            "evidence_bundle_sha256": bundle_sha256,
        }
        effective = "R157_NONRESPONDENT_FIXTURE"
    elif protocol:
        scope = {
            "source_id": source_id,
            "source_sha256": original_sha,
            "wave": wave,
            "grade": "R157_NATIVE_PROTOCOL_ONLY",
            "evidence_bundle_sha256": bundle_sha256,
            "not_source_scientific_authority": True,
        }
        effective = "R157_NATIVE_PRE553_PROTOCOL"
    else:
        scope = {
            "source_id": source_id,
            "source_sha256": original_sha,
            "wave": wave,
            "grade": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
            "p2_authority_status": "source_reviewed",
            "evidence_bundle_sha256": bundle_sha256,
            "not_source_scientific_authority": True,
        }
        effective = f"GSS_{wave}"
    content_hash = semantic_hash({
        "authority_id": authority_id,
        "authority_kind": authority_kind,
        "decision": decision,
        "source_id": source_id,
        "original_source_sha256": original_sha,
        "wave": wave,
        "bundle_sha256": bundle_sha256,
        "fixture_id": fixture_id,
        "fixture_source_sha256": fixture_sha,
        "protocol": protocol,
    })
    replay = _ref(
        "REPLAY_PROTOCOL",
        "urn:rawlsing:r157:native-replay-protocol:1.0.0",
        {
            "protocol": "PRE553_REPLAY",
            "ingest_contract": INGEST_CONTRACT_VERSION,
            "codec": R5_CODEC_VERSION,
        },
    )
    return {
        "typed_state": decision,
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _ref_dict(_ref(
            "REPLAY_ROOT",
            f"urn:rawlsing:r157:{source_id}:authority:{authority_id}",
            {"authority_id": authority_id, "bundle_sha256": bundle_sha256},
        )),
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": content_hash,
        "authority_kind": authority_kind,
        "decision_state": decision,
        "governed_operations": list(operations),
        "governed_object_families": list(families),
        "scope_envelope": scope,
        "effective_time_or_interval": effective,
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": semantic_hash({
            "authority_id": authority_id,
            "authority_kind": authority_kind,
            "decision": decision,
            "scope": scope,
        }),
        "replay_protocol_ref": _ref_dict(replay),
    }


def _authority_ref(snapshot: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(
        snapshot["authority_id"],
        snapshot["authority_version"],
        snapshot["authority_content_hash"],
    )


def _evidence_refs(item: Mapping[str, Any]) -> list[dict[str, str]]:
    relation = item["relation"]
    return [
        _ref_dict(ExactRef(
            "H48_ITEM_AUTHORITY",
            f"urn:rawlsing:r157:h48:{item['implementation_id']}",
            item["exact_identity_sha256"],
        )),
        _ref_dict(ExactRef(
            "P2_PHASE0_ROW",
            f"urn:rawlsing:r157:p2:{item['implementation_id']}",
            item["p2"]["exact_identity_sha256"],
        )),
        _ref_dict(ExactRef(
            "FULL_RELATION_ROW",
            f"urn:rawlsing:r157:relation:{relation['question_id']}",
            relation["governed_row_payload_hash"],
        )),
    ]


def _question_material(
    *, source_id: str, wave: str, original_sha: str, item: Mapping[str, Any],
    fixture_id: str | None,
) -> dict[str, Any]:
    material = {
        "source_id": source_id,
        "wave": wave,
        "source_sha256": original_sha,
        "implementation_id": item["implementation_id"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "source_variable_code": item["source_variable_code"],
        "question_text": item["p2"]["question_text"],
        "fixture_id": fixture_id,
    }
    return material


def _native_question_ref(
    *, source_id: str, wave: str, original_sha: str, item: Mapping[str, Any],
    fixture_id: str | None,
) -> ExactRef:
    suffix = "fixture" if fixture_id else "source"
    return _ref(
        "NATIVE_QUESTION",
        f"urn:rawlsing:r157:{suffix}:{source_id}:{item['implementation_id']}",
        _question_material(
            source_id=source_id, wave=wave, original_sha=original_sha,
            item=item, fixture_id=fixture_id),
    )


def _topology_ref(
    *, source_id: str, wave: str, original_sha: str, item: Mapping[str, Any],
    fixture_id: str | None,
) -> ExactRef:
    suffix = "fixture" if fixture_id else "source"
    return _ref(
        "RESPONSE_TOPOLOGY",
        f"urn:rawlsing:r157:{suffix}:{source_id}:{item['source_variable_code']}:topology",
        {
            "source_id": source_id,
            "wave": wave,
            "source_sha256": original_sha,
            "source_variable_code": item["source_variable_code"],
            "exact_identity_sha256": item["exact_identity_sha256"],
            "manual_response_topology": item["relation"]["manual_response_topology"],
            "fixture_id": fixture_id,
        },
    )


def _occurrence_kind(manual_topology: str) -> str:
    if manual_topology == "scalar":
        return "SCALAR_SINGULAR"
    if manual_topology == "binary_contrast":
        return "BINARY_CONTRAST_SINGLE"
    return "MANUAL_SINGLE_" + manual_topology.upper().replace(" ", "_")


def _occurrence(
    *, topology: ExactRef, manual_topology: str,
) -> dict[str, Any]:
    return {
        "key": "0",
        "topology_ref": topology.as_dict(),
        "multiplicity_order_rank_fields": {
            "kind": _occurrence_kind(manual_topology),
            "source_manual_topology": manual_topology,
            "index": 0,
        },
    }


def _response_values(
    *, slot: Mapping[str, Any], item: Mapping[str, Any], topology: ExactRef,
) -> list[dict[str, Any]]:
    occurrence = _occurrence(
        topology=topology,
        manual_topology=item["relation"]["manual_response_topology"],
    )
    values = []
    labels = slot.get("value_labels") or {}
    for raw_text, label in sorted(labels.items(), key=lambda pair: float(pair[0])):
        raw = float(raw_text)
        if raw in MISSING_RESPONSE_STATES:
            state = MISSING_RESPONSE_STATES[raw]
        elif raw >= 0:
            state = "SUBSTANTIVE_RESPONSE"
        else:
            state = "SOURCE_SPECIFIC_SPECIAL"
        values.append({
            "raw_value": raw,
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
            "response_state": state,
            "occurrences": [occurrence],
            "canonical_value": None,
            "transform_authority_ref": None,
            "extra_authority_refs": [],
        })
    values.append({
        "raw_value": None,
        "missing_state": "SYSTEM_MISSING",
        "source_missing_declaration": None,
        "response_state": "MISSING",
        "occurrences": [occurrence],
        "canonical_value": None,
        "transform_authority_ref": None,
        "extra_authority_refs": [],
    })
    return values


def _physical_payload(
    slot: Mapping[str, Any], disposition: str, reason: str,
) -> dict[str, Any]:
    missing = None
    if slot.get("missing_user_values") is not None or slot.get("missing_ranges") is not None:
        missing = {
            "user_values": slot.get("missing_user_values"),
            "ranges": slot.get("missing_ranges"),
        }
    return {
        "ordinal": slot["ordinal"],
        "name": slot["name"],
        "label": slot.get("label"),
        "storage_type": slot.get("readstat_type"),
        "original_type": slot.get("original_type"),
        "storage_width": slot.get("storage_width"),
        "measure": slot.get("measure"),
        "value_labels": slot.get("value_labels"),
        "missing_declarations": missing,
        "mr_declarations": None,
        "codebook_mapping": slot["codebook_mapping"],
        "disposition": disposition,
        "disposition_reason": reason,
    }


def _item_payload(item: Mapping[str, Any]) -> dict[str, Any]:
    p2 = item["p2"]
    relation = item["relation"]
    limits = [
        f"h48_binding_grade={item['h48']['binding_grade']}",
        f"p2_authority_status={p2['authority_status']}",
        f"full_relation_authority_status={relation['authority_status']}",
        f"relation_use_status_final={relation['relation_use_status_final']}",
        f"manual_response_topology={relation['manual_response_topology']}",
        f"manual_signed_polarity_status={relation['manual_signed_polarity_status']}",
        "R157 preparation does not issue original-source execution authority.",
    ]
    if relation["forbidden_inference"]:
        limits.append(f"forbidden_inference={relation['forbidden_inference']}")
    if relation["does_not_measure"]:
        limits.append(f"does_not_measure={relation['does_not_measure']}")
    mapping_status = relation["mapping_status"]
    return {
        "implementation_id": item["implementation_id"],
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "question_text": p2["question_text"],
        "disposition": p2["canonical_disposition"],
        "response_classes": p2["response_classes"],
        "mapping_status": mapping_status,
        "authority_status": relation["authority_status"],
        "evidence_refs": _evidence_refs(item),
        "limits": limits,
        "item_id": p2["question_id"],
        "relation": {
            "status": "EXACT",
            "question_id": relation["question_id"],
            "mapping_status": mapping_status,
            "manual_response_topology": relation["manual_response_topology"],
            "manual_response_normalization_rule": relation["manual_response_normalization_rule"],
            "manual_position_conditioning": relation["manual_position_conditioning"],
            "manual_semantic_role": relation["manual_semantic_role"],
            "manual_signed_polarity_status": relation["manual_signed_polarity_status"],
            "forbidden_inference": relation["forbidden_inference"] or "none recorded",
            "does_not_measure": relation["does_not_measure"] or "none recorded",
            "governed_row_payload_hash": relation["governed_row_payload_hash"],
            "p2_exact_identity_sha256": relation["p2_exact_identity_sha256"],
        },
    }


def _slot_disposition(name: str, selected: set[str], weight_name: str | None) -> tuple[str, str]:
    if name in selected:
        return (
            "SUPPORTED_RESPONSE",
            "Grounded scalar response slot selected for the source-local supported slice.",
        )
    if name == "id":
        return (
            "SOURCE_NATIVE_RESPONDENT_KEY",
            "Source-native respondent id slot; values require a permitted decode before row witnesses exist.",
        )
    if name == "year":
        return (
            "SUPPORTED_COORDINATE_TIME",
            "Source-native GSS survey-year coordinate; raw value copied only at permitted projection.",
        )
    if name == "region":
        return (
            "SUPPORTED_CONTEXT_COORDINATE",
            "Source-native region context coordinate retained as a coordinate, not a measurement target.",
        )
    if name == weight_name:
        return (
            "HELD_WEIGHT_DESIGN_UNRESOLVED",
            "Source weight slot exists, but no exact design/estimand/normalization authority is established.",
        )
    if name in ADMIN_SLOTS:
        return (
            "RETAINED_ADMINISTRATIVE",
            "Administrative/sample/form metadata retained for identity and no-drop accounting.",
        )
    return (
        "RETAINED_NOT_IN_SUPPORTED_SLICE",
        "Original item/slot identity and evidence retained; not part of the declared scalar response slice.",
    )


def _residuals(
    *, source_id: str, wave: str, weight_slot: Mapping[str, Any] | None,
) -> list[dict[str, str]]:
    residuals = [
        {
            "residual_id": f"{source_id}-NATIVE-ROW-KEY",
            "scope": f"{source_id}/respondents",
            "field": "respondents.source_native_key_slot",
            "status": "DECODE_REQUIRED",
            "reason": "The source-native id slot is bound, but no permitted decode-produced respondent keys are available during preparation.",
            "dependent_operation": "original build_governed_c11_projection / build_validated_c11_release_from_config",
            "unaffected_scope": "schema validation, nonrespondent fixture projection and native C11 validation",
            "owner": "R157 P3 integration owner with source-read decoder owner",
            "next_step": "Populate the frozen row_native_keys argument from permitted decoded id cells and verified edition/currentness checks.",
        },
        {
            "residual_id": f"{source_id}-ROUTING-UNKNOWN",
            "scope": f"{source_id}/routing",
            "field": "routing[].typed_state",
            "status": "ROUTING_UNKNOWN",
            "reason": "H48/O06 reports SOURCE_ROUTING_UNRESOLVED; exact form, ballot and administration routing was not recovered.",
            "dependent_operation": "eligibility-conditioned original source claims or subsets",
            "unaffected_scope": "raw scalar response decoding and fixture positive release",
            "owner": "GSS source evidence owner",
            "next_step": "Recover exact original route expressions/form assignment before any original eligibility claim.",
        },
        {
            "residual_id": f"{source_id}-SOURCE-AUTHORITY-DEFER",
            "scope": f"{source_id}/authority",
            "field": "authority.snapshots",
            "status": "DEFER",
            "reason": "H48/P2/full-relation evidence is source_reviewed candidate evidence, not an adopted ALLOW authority for original scientific execution.",
            "dependent_operation": "original scientific issuance or original-source semantic promotion",
            "unaffected_scope": "portable source preparation and nonrespondent fixture validation",
            "owner": "R157 authority owner",
            "next_step": "Adjudicate the exact source operation scope; never promote fixture-only authority into original meaning.",
        },
        {
            "residual_id": f"{source_id}-CANONICAL-VALUE",
            "scope": f"{source_id}/response_slots",
            "field": "response_slots[].values[].canonical_value",
            "status": "NOT_AUTHORIZED",
            "reason": "No exact positive NATIVE_CANONICAL_MAPPING_HARMONIZATION authority is present, so raw source values and states are retained without canonical recoding.",
            "dependent_operation": "canonicalized cross-source value analysis",
            "unaffected_scope": "raw response state and exact physical value projection",
            "owner": "R157 mapping authority owner",
            "next_step": "Adjudicate exact source-native to canonical mapping before setting canonical values.",
        },
        {
            "residual_id": f"{source_id}-FORM-ADMINISTRATION",
            "scope": f"{source_id}/form",
            "field": "supported_scope.supported_form_slice",
            "status": "UNKNOWN",
            "reason": "Split form/ballot assignment and administration are not recovered as exact source facts in the portable evidence rows.",
            "dependent_operation": "form-conditioned or administration-conditioned claims",
            "unaffected_scope": "unconditional scalar response-rule fixture validation",
            "owner": "GSS source evidence owner",
            "next_step": "Recover exact form/ballot assignment evidence for this wave if a form-conditioned slice is required.",
        },
        {
            "residual_id": f"{source_id}-SAMPLE-FRAME",
            "scope": f"{source_id}/universe",
            "field": "universe.sampling_design_regime",
            "status": "UNRESOLVED",
            "reason": "Country scope US is carried from the full-relation row; wave-specific sampling frame and design are not reconstructed from metadata alone.",
            "dependent_operation": "population, design or design-based inference claims",
            "unaffected_scope": "source-row identity and raw response-rule construction",
            "owner": "GSS source evidence owner",
            "next_step": "Recover exact wave sampling-frame/design evidence before population or design claims.",
        },
    ]
    if weight_slot is not None:
        residuals.insert(4, {
            "residual_id": f"{source_id}-WEIGHT-HELD",
            "scope": f"{source_id}/weight_slots",
            "field": f"physical_slots[{weight_slot['ordinal']}].name={weight_slot['name']}",
            "status": "HELD",
            "reason": "The source weight slot is identified, but exact weight basis, design, estimand and normalization authority are not established.",
            "dependent_operation": "weighted estimands and population inference",
            "unaffected_scope": "unweighted source-local raw sample configuration",
            "owner": "GSS weight/design evidence owner",
            "next_step": "Establish exact design/estimand/normalization authority before emitting an authorized weight lane.",
        })
    return residuals


def _pinned_inputs() -> list[dict[str, Any]]:
    manifest = load_manifest()
    return [
        {"kind": "R157_PLAN_SEAL", "commit": PLAN_SEAL},
        {
            "kind": "R157_P0_CORRECTED_INTERFACE",
            "commit": P0_CORRECTION,
        },
        {
            "kind": "R157_P3_TERMINAL_RUNTIME",
            "commit": P3_RUNTIME,
        },
        {
            "kind": "R154_METADATA_SNAPSHOT",
            "commit": "a02adc896264e1b46afd143cba9426182ec14802",
            "path": "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite",
            "sha256": "7d6421e6e50f7d249cf09e7ecf964757d6afa4a7926d7a31eb1aad3407a12a16",
        },
        {
            "kind": "H48_ITEM_INDEX",
            "commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
            "path": "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz",
            "sha256": "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5",
        },
        {
            "kind": "P2_PHASE0",
            "sha256": "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6",
        },
        {
            "kind": "FULL_RELATION_AUTHORITY",
            "commit": "9561723cfe0932869e781f2be27e9c80b050ad7a",
            "path": "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
            "sha256": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13",
        },
        {
            "kind": "PORTABLE_EVIDENCE_MANIFEST",
            "path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
            "sha256": _file_identity(
                ROOT / "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json")["sha256"],
        },
        {
            "kind": "PORTABLE_ITEM_EVIDENCE",
            "path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "sha256": manifest["files"]["ITEM_EVIDENCE.jsonl.gz"]["sha256"],
        },
        {
            "kind": "PORTABLE_PHYSICAL_SLOTS",
            "path": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
            "sha256": manifest["files"]["PHYSICAL_SLOTS.jsonl.gz"]["sha256"],
        },
        {
            "kind": "PORTABLE_CODEBOOK_ROWS",
            "path": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
            "sha256": manifest["files"]["CODEBOOK_ROWS.jsonl.gz"]["sha256"],
        },
    ]


def _runtime_section(*, fixture: bool) -> dict[str, Any]:
    return {
        "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
        "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
        "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
        "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
        "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
        "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
        "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
        "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
        "reader_encoding_transport": (
            "FIXTURE_ONLY_NO_ORIGINAL_READER" if fixture else
            "P3_QUALIFIED_READER_TRANSPORT_CONFIGURED_NO_ENCODING_OVERRIDE"
        ),
    }


def _source_profiles(source_id: str) -> dict[str, Any]:
    roster = source_roster_entry(source_id)
    physical_rows = list(iter_physical_slots(source_id))
    physical = {row["name"]: row for row in physical_rows}
    codebook_rows = list(iter_codebook_rows(source_id))
    items = list(iter_item_evidence(source_id))
    item_by_name = {row["source_variable_code"]: row for row in items}
    missing = sorted(set(SELECTED_QUESTIONS) - set(item_by_name))
    if missing:
        raise RuntimeError(f"{source_id} lacks selected items {missing!r}")
    selected_items = [item_by_name[name] for name in SELECTED_QUESTIONS]
    weight = physical.get("wtssall") or physical.get("wtssps")
    if weight is None:
        raise RuntimeError(f"{source_id} lacks both wtssall and wtssps")
    for name in (*SELECTED_QUESTIONS, "year", "region", "id"):
        if name not in physical:
            raise RuntimeError(f"{source_id} lacks physical slot {name!r}")
    return {
        "roster": roster,
        "physical_rows": physical_rows,
        "physical": physical,
        "codebook_rows": codebook_rows,
        "items": items,
        "item_by_name": item_by_name,
        "selected_items": selected_items,
        "weight": weight,
    }


def _build_original(source_id: str, profile: Mapping[str, Any]) -> dict[str, Any]:
    roster = profile["roster"]
    wave = str(roster["wave"])
    original_sha = roster["source_sha256"]
    metadata_sha = roster["metadata_witness"]["sha256"]
    physical = profile["physical"]
    weight = profile["weight"]
    selected_items = profile["selected_items"]
    selected_names = set(SELECTED_QUESTIONS)
    selected_ordinals = {
        physical[name]["ordinal"] for name in (*SELECTED_QUESTIONS, "year", "region", "id", weight["name"])
    }

    source_universe_id = f"urn:rawlsing:r157:source:{source_id}:universe"
    source_material = {
        "source_id": source_id,
        "wave": wave,
        "source_sha256": original_sha,
        "metadata_witness_sha256": metadata_sha,
        "implementation_ids": [item["implementation_id"] for item in selected_items],
        "physical_ordinals": sorted(selected_ordinals),
        "h48_grade": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
        "p2_authority_status": "source_reviewed",
    }
    source_bundle = semantic_hash(source_material)
    source_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-SOURCE-EVIDENCE",
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        operations=("R157_SOURCE_PREPARATION_SOURCE_SEMANTICS",),
        bundle_sha256=source_bundle,
    )
    routing_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-ROUTING-EVIDENCE",
        authority_kind="ROUTING_RISK_SET",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("RoutingEligibilityFact@1.0.0",),
        operations=("R157_SOURCE_PREPARATION_ROUTING",),
        bundle_sha256=semantic_hash({
            "source_bundle": source_bundle,
            "routing_status": "SOURCE_ROUTING_UNRESOLVED",
            "question_ids": [item["p2"]["question_id"] for item in selected_items],
        }),
    )
    coord_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-COORDINATE-EVIDENCE",
        authority_kind="COORDINATE_SEMANTICS",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("EmpiricalCoordinateFact@1.0.0",),
        operations=("R157_SOURCE_PREPARATION_COORDINATE",),
        bundle_sha256=semantic_hash({
            "source_bundle": source_bundle,
            "coordinates": ["year", "region"],
            "metadata_witness_sha256": metadata_sha,
        }),
    )
    replay_snapshot = _authority_snapshot(
        authority_id="R157-NATIVE-REPLAY-PROTOCOL",
        authority_kind="REPLAY_PROTOCOL",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("ReplayReceipt@1.0.0",),
        operations=("R157_NATIVE_REPLAY",),
        bundle_sha256=semantic_hash({
            "protocol": "PRE553_REPLAY",
            "ingest_contract": INGEST_CONTRACT_VERSION,
            "codec": R5_CODEC_VERSION,
            "tie_order": "CANONICAL_REF_SORT",
        }),
        protocol=True,
    )
    projection_identity = _ref(
        "C11_SEMANTIC_PROJECTION",
        f"urn:rawlsing:r157:source:{source_id}:projection",
        {
            "config_id": f"R157-GSS-{source_id}-ORIGINAL-SOURCE-PREPARATION",
            "source_id": source_id,
            "source_sha256": original_sha,
            "wave": wave,
            "question_ids": [item["p2"]["question_id"] for item in selected_items],
            "coordinate_slots": ["year", "region"],
        },
    )
    projection_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-PROJECTION-EVIDENCE",
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"),
        operations=("R157_SOURCE_PREPARATION_PROJECTION",),
        bundle_sha256=semantic_hash({
            "source_bundle": source_bundle,
            "projection_identity": projection_identity.as_dict(),
            "routing_unknown": True,
        }),
    )
    snapshots = [source_snapshot, routing_snapshot, coord_snapshot, replay_snapshot, projection_snapshot]
    source_auth = _authority_ref(source_snapshot)
    routing_auth = _authority_ref(routing_snapshot)
    coord_auth = _authority_ref(coord_snapshot)
    replay_auth = _authority_ref(replay_snapshot)
    projection_auth = _authority_ref(projection_snapshot)
    required = [source_auth, routing_auth, coord_auth, replay_auth, projection_auth]

    universe = {
        "typed_state": "UNIVERSE_IDENTIFIED",
        "authority_snapshot_refs": [source_auth.as_dict()],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _ref_dict(_ref(
            "REPLAY_ROOT", f"urn:rawlsing:r157:source:{source_id}:universe",
            {"source_id": source_id, "source_sha256": original_sha})),
        "raw_source_identity": f"GSS:{wave}:{source_id}",
        "source_family": "GSS",
        "study_product_release": f"GSS_{wave}_SOURCE_ARTIFACT",
        "instrument_release": f"SRC{source_id[-2:]}_METADATA_WITNESS_SHA256:{metadata_sha}",
        "country_geography": "US",
        "sampling_geography": "US_NATIONAL_FRAME_EVIDENCE_UNRESOLVED",
        "raw_wave": wave,
        "canonical_wave_if_governed": None,
        "field_or_reference_time": wave,
        "target_population_and_sample_frame": "GSS_RESPONDENT_SAMPLE_FRAME_NOT_RECONSTRUCTED_FROM_METADATA",
        "sampling_design_regime": "SOURCE_SAMPLE_DESIGN_UNRESOLVED",
        "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:respondent",
        "source_artifact_import_lineage": f"R154_PHYSICAL_METADATA_SHA256:{metadata_sha}",
        "harmonization_authority_ref": None,
        "source_relation_refs": [],
    }
    universe_ref = EmpiricalUniverse(**universe).ref

    questions = []
    response_slots = []
    routing = []
    for item in selected_items:
        name = item["source_variable_code"]
        slot = physical[name]
        native_question = _native_question_ref(
            source_id=source_id, wave=wave, original_sha=original_sha,
            item=item, fixture_id=None)
        topology = _topology_ref(
            source_id=source_id, wave=wave, original_sha=original_sha,
            item=item, fixture_id=None)
        question_id = item["p2"]["question_id"]
        questions.append({
            "question_id": question_id,
            "empirical_universe_ref": universe_ref.as_dict(),
            "native_question_ref": native_question.as_dict(),
            "instrument_question_version": f"GSS_{wave}",
            "canonical_question_ref_or_typed_absence": TypedAbsence(
                "NOT_AUTHORIZED",
                "No exact positive canonical mapping authority; raw source question identity retained.",
            ).as_dict(),
            "component_subitem_ref_or_typed_absence": TypedAbsence(
                "NOT_APPLICABLE",
                "Single source variable; no multiple-response component/subitem is asserted.",
            ).as_dict(),
            "semantic_authority_ref": source_auth.as_dict(),
            "topology_authority_ref": source_auth.as_dict(),
            "item_evidence": {
                "implementation_id": item["implementation_id"],
                "exact_identity_sha256": item["exact_identity_sha256"],
                "relation_join_status": "EXACT",
                "question_text": item["p2"]["question_text"],
                "source_variable_code": name,
            },
        })
        response_slots.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "question_id": question_id,
            "values": _response_values(slot=slot, item=item, topology=topology),
        })
        rule_material = {
            "source_id": source_id,
            "wave": wave,
            "source_sha256": original_sha,
            "question_id": question_id,
            "routing_status": "SOURCE_ROUTING_UNRESOLVED",
        }
        routing.append({
            "question_id": question_id,
            "row_selector": "ALL",
            "typed_state": "ROUTING_UNKNOWN",
            "risk_set_ref": _ref_dict(_ref(
                "RISK_SET", f"urn:rawlsing:r157:source:{source_id}:{name}:risk-set", rule_material)),
            "routing_rule_ref": _ref_dict(_ref(
                "ROUTING_RULE", f"urn:rawlsing:r157:source:{source_id}:{name}:routing-rule", rule_material)),
            "member_set_replay_ref": _ref_dict(_ref(
                "MEMBER_SET_REPLAY", f"urn:rawlsing:r157:source:{source_id}:{name}:member-set", rule_material)),
            "authority_ref": routing_auth.as_dict(),
            "parent_predicate_refs": [],
            "dependency_refs": [],
        })

    coordinates = []
    for name, unit_kind, object_kind in (
        ("year", "source_native_survey_year", "GSS_SURVEY_YEAR"),
        ("region", "source_native_region_code", "GSS_REGION_CODE"),
    ):
        slot = physical[name]
        coordinates.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "native_coordinate_ref": _ref_dict(_ref(
                "COORDINATE_NATIVE",
                f"urn:rawlsing:r157:source:{source_id}:coordinate:{name}",
                {
                    "source_id": source_id,
                    "wave": wave,
                    "source_sha256": original_sha,
                    "name": name,
                    "label": slot.get("label"),
                })),
            "unit_taxonomy_ref": _ref_dict(_ref(
                "UNIT_TAXONOMY",
                f"urn:rawlsing:r157:unit:{unit_kind}",
                {"unit": unit_kind, "source_native_object": object_kind})),
            "effective_time": wave if name == "year" else f"GSS_{wave}_INTERVIEW",
            "source_semantic_authority_ref": coord_auth.as_dict(),
            "canonical_coordinate_ref": None,
            "normalization_ref": None,
            "values": [],
            "copy_observed_raw": True,
        })

    physical_payloads = []
    for slot in profile["physical_rows"]:
        disposition, reason = _slot_disposition(slot["name"], selected_names, weight["name"])
        physical_payloads.append(_physical_payload(slot, disposition, reason))
    items_payload = [_item_payload(item) for item in profile["items"]]
    selected_ids = [item["implementation_id"] for item in selected_items]
    selected_id_set = set(selected_ids)
    excluded_slots = [
        {
            "ordinal": slot["ordinal"],
            "name": slot["name"],
            "reason": _slot_disposition(slot["name"], selected_names, weight["name"])[1],
        }
        for slot in profile["physical_rows"]
        if slot["ordinal"] not in selected_ordinals
    ]
    excluded_items = [
        {
            "implementation_id": item["implementation_id"],
            "reason": (
                f"retained with source disposition={item['p2']['canonical_disposition']}; "
                "exact identity and relation evidence retained outside the supported scalar slice"
            ),
        }
        for item in profile["items"]
        if item["implementation_id"] not in selected_id_set
    ]

    config_id = f"R157-GSS-{source_id}-ORIGINAL-SOURCE-PREPARATION"
    doc = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id,
        "config_revision": 1,
        "config_purpose": "SOURCE_PREPARATION",
        "identity": {
            "source_id": source_id,
            "family": roster["family"],
            "wave": wave,
            "source_family_id": "GSS",
            "study_product_id": f"GSS_{wave}",
            "release_id": f"GSS_{wave}_SOURCE_ARTIFACT",
            "instrument_release_id": f"SRC{source_id[-2:]}_METADATA_WITNESS_SHA256:{metadata_sha}",
            "source_artifact_id": roster["source_artifact_id"],
            "expected_source_sha256": original_sha,
            "source_format": roster["format"],
            "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"],
            "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"],
            "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": _ref_dict(ExactRef(
                "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", original_sha)),
            "metadata_witness_ref": _ref_dict(ExactRef(
                "R154_PHYSICAL_METADATA",
                f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                metadata_sha)),
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
            },
            "reader": {
                "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                "configuration_ref": _ref_dict(_ref(
                    "READER_CONFIGURATION",
                    f"urn:rawlsing:r157:reader:{source_id}:default_sav",
                    {
                        "source_id": source_id,
                        "decoder": "decode_sav",
                        "encoding": None,
                        "source_sha256": original_sha,
                    })),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "ORIGINAL_SOURCE",
            "source_sha256": original_sha,
            "row_count": roster["rows"],
            "source_snapshot_ref": _ref_dict(ExactRef(
                "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", original_sha)),
        },
        "authority": {
            "snapshots": snapshots,
            "required_refs": [ref.as_dict() for ref in required],
            "projection_authority_ref": projection_auth.as_dict(),
            "replay_authority_ref": replay_auth.as_dict(),
            "projection_identity_ref": projection_identity.as_dict(),
            "tie_order_ref": _ref_dict(_ref(
                "ORDER_RULE", "urn:rawlsing:r157:order:canonical-exact-ref",
                {"rule": "CANONICAL_REF_SORT"})),
            "replay_protocol_version": "1.0.0",
        },
        "universe": {"universes": [universe]},
        "respondents": {
            "subject_unit": "GSS_RESPONDENT_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:source:{source_id}:respondent",
            "respondent_key_pattern": f"{source_id}-ROW-{{row_ordinal:06d}}",
            "source_native_key_slot": {"ordinal": physical["id"]["ordinal"], "name": "id"},
            "identity_map_authority_ref": None,
            "row_identity_grade": "SOURCE_NATIVE_ID_SLOT_DECLARED_VALUE_DECODE_REQUIRED",
        },
        "questions": questions,
        "physical_slots": physical_payloads,
        "items": items_payload,
        "response_slots": response_slots,
        "coordinate_slots": coordinates,
        "weight_slots": [],
        "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
            "comparator": TypedAbsence("DEFERRED").as_dict(),
            "discovery": TypedAbsence("DEFERRED").as_dict(),
            "structural": TypedAbsence("NOT_APPLICABLE").as_dict(),
        },
        "supported_scope": {
            "scope_id": f"{source_id}-GSS-SCALAR-RESPONSE-PREPARATION",
            "purpose": "SOURCE_PREPARATION",
            "declared_supported": True,
            "supported_question_ids": [item["p2"]["question_id"] for item in selected_items],
            "native_validation_expectation": "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "GSS_RESPONDENT_ROW_SOURCE_LOCAL",
            "supported_form_slice": "SCALAR_SINGLE_OBSERVATION_PER_RESPONDENT_FORM_ASSIGNMENT_UNKNOWN",
            "notes": [
                SUPPORTED_SCOPE_NOTE,
                "The three source-local scalar variables are happy, satfin and abdefect; no cross-wave equivalence or pooling is asserted.",
                "Fixture validation uses a separate NONRESPONDENT_FIXTURE config and byte identity.",
            ],
        },
        "coverage": {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": sorted(selected_ordinals),
            "physical_slots_excluded": excluded_slots,
            "items_included": selected_ids,
            "items_excluded": excluded_items,
            "partial_scope_reason": (
                "Supported scalar slice is explicitly partial; all physical slots and original items remain serialized and accounted."
            ),
            "not_a_lane_config": False,
        },
        "residuals": _residuals(source_id=source_id, wave=wave, weight_slot=weight),
        "evidence": {
            "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
            "pinned_inputs": _pinned_inputs(),
            "field_evidence": _field_evidence(
                source_id=source_id, profile=profile, metadata_sha=metadata_sha),
            "limits": [
                "H48/P2/full-relation grades and limits are copied, not promoted.",
                "Original respondent execution and original-source scientific claims are NOT performed.",
                "The nonrespondent fixture has a distinct byte identity and fixture-only authority.",
            ],
        },
        "runtime": _runtime_section(fixture=False),
        "notes": [
            f"GSS wave {wave} source-local preparation; all {roster['physical_columns']} slots and {roster['original_items']} items are serialized.",
            "No original respondent file or value was read to build this configuration.",
        ],
    }
    return doc


def _field_evidence(
    *, source_id: str, profile: Mapping[str, Any], metadata_sha: str,
) -> list[dict[str, Any]]:
    roster = profile["roster"]
    selected = profile["selected_items"]
    item_refs = []
    for item in selected:
        item_refs.extend(_evidence_refs(item))
    metadata_ref = _ref_dict(ExactRef(
        "R154_PHYSICAL_METADATA",
        f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
        metadata_sha,
    ))
    return [
        {"field": "identity.*", "refs": [metadata_ref]},
        {"field": "physical_slots[*]", "refs": [metadata_ref]},
        {"field": "items[*]", "refs": item_refs},
        {"field": "questions[].item_evidence", "refs": item_refs},
        {"field": "response_slots[]", "refs": item_refs},
        {"field": "coordinate_slots[]", "refs": [metadata_ref]},
        {"field": "routing[].typed_state", "refs": item_refs},
        {"field": "authority.snapshots", "refs": item_refs},
        {"field": "supported_scope", "refs": item_refs},
    ]


def _fixture_expected(
    *, source_id: str, profile: Mapping[str, Any], doc: Mapping[str, Any],
) -> dict[str, Any]:
    response_state_by_key: dict[tuple[str, Any], str] = {}
    for section in doc["response_slots"]:
        name = section["slot"]["name"]
        for value in section["values"]:
            key = (name, "SYSTEM_MISSING" if value["raw_value"] is None else float(value["raw_value"]))
            response_state_by_key[key] = value["response_state"]
    question_ids = [f"FIXTURE:{source_id}:{name}" for name in SELECTED_QUESTIONS]
    response_counts: Counter[str] = Counter()
    by_question: dict[str, Counter[str]] = {qid: Counter() for qid in question_ids}
    for row, happy, satfin, abdefect, region, weight in FIXTURE_DATA:
        for name, raw in (("happy", happy), ("satfin", satfin), ("abdefect", abdefect)):
            key = (name, "SYSTEM_MISSING" if raw is None else float(raw))
            state = response_state_by_key[key]
            response_counts[state] += 1
            by_question[f"FIXTURE:{source_id}:{name}"][state] += 1
    weight_counts: Counter[str] = Counter()
    for row, happy, satfin, abdefect, region, weight in FIXTURE_DATA:
        if weight is None:
            weight_counts["WEIGHT_MISSING"] += 1
        else:
            weight_counts["WEIGHT_BASIS_UNRESOLVED"] += 1
    return {
        "fixture_only": True,
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "response_event_count": FIXTURE_ROWS * len(SELECTED_QUESTIONS),
        "coordinate_fact_count": FIXTURE_ROWS * 2,
        "routing_fact_count": FIXTURE_ROWS * len(SELECTED_QUESTIONS),
        "weight_fact_count": FIXTURE_ROWS,
        "response_state_counts": dict(sorted(response_counts.items())),
        "response_state_counts_by_question": {
            qid: dict(sorted(counts.items())) for qid, counts in by_question.items()
        },
        "coordinate_state_counts": {"OBSERVED_COORDINATE": FIXTURE_ROWS * 2},
        "weight_state_counts": dict(sorted(weight_counts.items())),
        "canonical_values": [None] * (FIXTURE_ROWS * len(SELECTED_QUESTIONS)),
        "source_relation_section": "DISTINCT_BY_DEFAULT",
    }


def _build_fixture(
    *, source_id: str, profile: Mapping[str, Any], original_doc: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    roster = profile["roster"]
    wave = str(roster["wave"])
    original_sha = roster["source_sha256"]
    metadata_sha = roster["metadata_witness"]["sha256"]
    physical = profile["physical"]
    weight = profile["weight"]
    selected_items = profile["selected_items"]
    fixture_id = FIXTURE_ID.format(source_id=source_id)
    fixture_cells = []
    for row, happy, satfin, abdefect, region, weight_value in FIXTURE_DATA:
        for name, raw in (("happy", happy), ("satfin", satfin), ("abdefect", abdefect)):
            slot = physical[name]
            fixture_cells.append({
                "row_ordinal": row,
                "variable_ordinal": slot["ordinal"],
                "variable_name": name,
                "raw_value": raw,
                "missing_state": "SYSTEM_MISSING" if raw is None else "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
            })
        id_slot = physical["id"]
        fixture_cells.append({
            "row_ordinal": row,
            "variable_ordinal": id_slot["ordinal"],
            "variable_name": "id",
            "raw_value": float(9000 + row),
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
        })
        for name, raw in (("year", float(wave)), ("region", region)):
            slot = physical[name]
            fixture_cells.append({
                "row_ordinal": row,
                "variable_ordinal": slot["ordinal"],
                "variable_name": name,
                "raw_value": raw,
                "missing_state": "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
            })
        fixture_cells.append({
            "row_ordinal": row,
            "variable_ordinal": weight["ordinal"],
            "variable_name": weight["name"],
            "raw_value": weight_value,
            "missing_state": "SYSTEM_MISSING" if weight_value is None else "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
        })
    fixture_id_value = fixture_id
    fixture_doc = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
        "fixture_id": fixture_id_value,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "row_count": FIXTURE_ROWS,
        "cells": fixture_cells,
        "expected_results": _fixture_expected(
            source_id=source_id, profile=profile, doc=original_doc),
    }
    fixture_sha = fixture_document_sha256(fixture_doc)
    fixture_doc["fixture_source_sha256"] = fixture_sha

    selected_names = set(SELECTED_QUESTIONS)
    selected_ordinals = {
        physical[name]["ordinal"]
        for name in (*SELECTED_QUESTIONS, "year", "region", "id", weight["name"])
    }
    source_bundle = semantic_hash({
        "source_id": source_id,
        "wave": wave,
        "source_sha256": original_sha,
        "fixture_id": fixture_id_value,
        "fixture_source_sha256": fixture_sha,
        "implementation_ids": [item["implementation_id"] for item in selected_items],
    })
    source_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-SOURCE",
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        operations=("R157_FIXTURE_SOURCE_SEMANTICS",),
        bundle_sha256=source_bundle,
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    routing_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-ROUTING",
        authority_kind="ROUTING_RISK_SET",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("RoutingEligibilityFact@1.0.0",),
        operations=("R157_FIXTURE_ROUTING",),
        bundle_sha256=semantic_hash({"source_bundle": source_bundle, "fixture": True}),
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    coord_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-COORDINATE",
        authority_kind="COORDINATE_SEMANTICS",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("EmpiricalCoordinateFact@1.0.0",),
        operations=("R157_FIXTURE_COORDINATE",),
        bundle_sha256=semantic_hash({"source_bundle": source_bundle, "coordinates": ["year", "region"]}),
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    weight_design_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-WEIGHT-DESIGN",
        authority_kind="WEIGHT_DESIGN_ESTIMAND",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("WeightMeasureFact@1.0.0",),
        operations=("R157_FIXTURE_WEIGHT_DESIGN",),
        bundle_sha256=semantic_hash({"source_bundle": source_bundle, "weight": weight["name"], "design": "UNRESOLVED"}),
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    weight_estimand_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-WEIGHT-ESTIMAND",
        authority_kind="WEIGHT_DESIGN_ESTIMAND",
        decision="DEFER",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("WeightMeasureFact@1.0.0",),
        operations=("R157_FIXTURE_WEIGHT_ESTIMAND",),
        bundle_sha256=semantic_hash({"source_bundle": source_bundle, "weight": weight["name"], "estimand": "UNRESOLVED"}),
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    replay_snapshot = _authority_snapshot(
        authority_id="R157-NATIVE-REPLAY-PROTOCOL",
        authority_kind="REPLAY_PROTOCOL",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("ReplayReceipt@1.0.0",),
        operations=("R157_NATIVE_REPLAY",),
        bundle_sha256=semantic_hash({
            "protocol": "PRE553_REPLAY",
            "ingest_contract": INGEST_CONTRACT_VERSION,
            "codec": R5_CODEC_VERSION,
            "tie_order": "CANONICAL_REF_SORT",
        }),
        protocol=True,
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    projection_identity = _ref(
        "C11_SEMANTIC_PROJECTION",
        f"urn:rawlsing:r157:fixture:{fixture_id_value}:projection",
        {
            "fixture_id": fixture_id_value,
            "fixture_source_sha256": fixture_sha,
            "source_id": source_id,
            "question_ids": [item["p2"]["question_id"] for item in selected_items],
        },
    )
    projection_snapshot = _authority_snapshot(
        authority_id=f"R157-{source_id}-FIXTURE-PROJECTION",
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision="ALLOW",
        source_id=source_id,
        original_sha=original_sha,
        wave=wave,
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0"),
        operations=("R157_FIXTURE_PROJECTION",),
        bundle_sha256=semantic_hash({
            "source_bundle": source_bundle,
            "projection_identity": projection_identity.as_dict(),
        }),
        fixture_id=fixture_id_value,
        fixture_sha=fixture_sha,
    )
    snapshots = [
        source_snapshot, routing_snapshot, coord_snapshot,
        weight_design_snapshot, weight_estimand_snapshot,
        replay_snapshot, projection_snapshot,
    ]
    source_auth = _authority_ref(source_snapshot)
    routing_auth = _authority_ref(routing_snapshot)
    coord_auth = _authority_ref(coord_snapshot)
    weight_design_auth = _authority_ref(weight_design_snapshot)
    weight_estimand_auth = _authority_ref(weight_estimand_snapshot)
    replay_auth = _authority_ref(replay_snapshot)
    projection_auth = _authority_ref(projection_snapshot)
    required = [
        source_auth, routing_auth, coord_auth, weight_design_auth,
        weight_estimand_auth, replay_auth, projection_auth,
    ]
    universe = {
        "typed_state": "UNIVERSE_IDENTIFIED",
        "authority_snapshot_refs": [source_auth.as_dict()],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _ref_dict(_ref(
            "REPLAY_ROOT", f"urn:rawlsing:r157:fixture:{fixture_id_value}:universe",
            {"fixture_id": fixture_id_value, "fixture_source_sha256": fixture_sha})),
        "raw_source_identity": f"R157-NONRESPONDENT-FIXTURE:{fixture_id_value}",
        "source_family": "GSS_NONRESPONDENT_FIXTURE",
        "study_product_release": f"R157_GSS_FIXTURE/{source_id}",
        "instrument_release": f"R157_GSS_FIXTURE_INSTRUMENT/{source_id}",
        "country_geography": "FIXTURE_US_SOURCE_SHAPE",
        "sampling_geography": "FIXTURE_NONPROBABILITY",
        "raw_wave": wave,
        "canonical_wave_if_governed": None,
        "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE",
        "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS",
        "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY",
        "respondent_namespace": f"urn:rawlsing:r157:fixture:{fixture_id_value}:respondent",
        "source_artifact_import_lineage": "R157_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE",
        "harmonization_authority_ref": None,
        "source_relation_refs": [],
    }
    universe_ref = EmpiricalUniverse(**universe).ref
    questions = []
    response_slots = []
    routing = []
    for item in selected_items:
        name = item["source_variable_code"]
        slot = physical[name]
        native_question = _native_question_ref(
            source_id=source_id, wave=wave, original_sha=original_sha,
            item=item, fixture_id=fixture_id_value)
        topology = _topology_ref(
            source_id=source_id, wave=wave, original_sha=original_sha,
            item=item, fixture_id=fixture_id_value)
        question_id = f"FIXTURE:{source_id}:{name}"
        questions.append({
            "question_id": question_id,
            "empirical_universe_ref": universe_ref.as_dict(),
            "native_question_ref": native_question.as_dict(),
            "instrument_question_version": f"GSS_{wave}_FIXTURE",
            "canonical_question_ref_or_typed_absence": TypedAbsence(
                "NOT_AUTHORIZED",
                "Fixture-only validation; no original canonical mapping authority is asserted.",
            ).as_dict(),
            "component_subitem_ref_or_typed_absence": TypedAbsence(
                "NOT_APPLICABLE",
                "Single fixture scalar variable; no multiple-response component/subitem is asserted.",
            ).as_dict(),
            "semantic_authority_ref": source_auth.as_dict(),
            "topology_authority_ref": source_auth.as_dict(),
            "item_evidence": {
                "implementation_id": item["implementation_id"],
                "exact_identity_sha256": item["exact_identity_sha256"],
                "relation_join_status": "EXACT",
                "fixture_id": fixture_id_value,
            },
        })
        response_slots.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "question_id": question_id,
            "values": _response_values(slot=slot, item=item, topology=topology),
        })
        rule_material = {
            "fixture_id": fixture_id_value,
            "fixture_source_sha256": fixture_sha,
            "question_id": question_id,
            "routing": "FIXTURE_ELIGIBLE",
        }
        routing.append({
            "question_id": question_id,
            "row_selector": "ALL",
            "typed_state": "ELIGIBLE_APPLICABLE",
            "risk_set_ref": _ref_dict(_ref(
                "RISK_SET", f"urn:rawlsing:r157:fixture:{fixture_id_value}:{name}:risk-set", rule_material)),
            "routing_rule_ref": _ref_dict(_ref(
                "ROUTING_RULE", f"urn:rawlsing:r157:fixture:{fixture_id_value}:{name}:routing-rule", rule_material)),
            "member_set_replay_ref": _ref_dict(_ref(
                "MEMBER_SET_REPLAY", f"urn:rawlsing:r157:fixture:{fixture_id_value}:{name}:member-set", rule_material)),
            "authority_ref": routing_auth.as_dict(),
            "parent_predicate_refs": [],
            "dependency_refs": [],
        })

    coordinates = []
    for name, unit_kind in (
        ("year", "source_native_survey_year"),
        ("region", "source_native_region_code"),
    ):
        slot = physical[name]
        coordinates.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "native_coordinate_ref": _ref_dict(_ref(
                "COORDINATE_NATIVE",
                f"urn:rawlsing:r157:fixture:{fixture_id_value}:coordinate:{name}",
                {
                    "fixture_id": fixture_id_value,
                    "source_id": source_id,
                    "wave": wave,
                    "name": name,
                    "label": slot.get("label"),
                })),
            "unit_taxonomy_ref": _ref_dict(_ref(
                "UNIT_TAXONOMY",
                f"urn:rawlsing:r157:unit:{unit_kind}",
                {"unit": unit_kind, "fixture_id": fixture_id_value})),
            "effective_time": "R157_NONRESPONDENT_FIXTURE",
            "source_semantic_authority_ref": coord_auth.as_dict(),
            "canonical_coordinate_ref": None,
            "normalization_ref": None,
            "values": [],
            "copy_observed_raw": True,
        })

    weight_values = []
    for row, happy, satfin, abdefect, region, weight_value in FIXTURE_DATA:
        if weight_value is None:
            exact = None
            state = "WEIGHT_MISSING"
            missing_state = "SYSTEM_MISSING"
        else:
            text = repr(float(weight_value))
            if text.endswith(".0"):
                text = text[:-2]
            exact = text
            state = "WEIGHT_BASIS_UNRESOLVED"
            missing_state = "OBSERVED_STORAGE_VALUE"
        weight_values.append({
            "raw_value": weight_value,
            "missing_state": missing_state,
            "source_missing_declaration": None,
            "exact_value": exact,
            "state": state,
        })
    weight_slots = [{
        "slot": {"ordinal": weight["ordinal"], "name": weight["name"]},
        "weight_basis_id": f"GSS_{weight['name'].upper()}_SOURCE_NATIVE_WEIGHT_VARIABLE",
        "weight_source_ref": _ref_dict(_ref(
            "WEIGHT_SOURCE",
            f"urn:rawlsing:r157:fixture:{fixture_id_value}:weight:{weight['name']}",
            {"source_id": source_id, "name": weight["name"], "metadata_witness_sha256": metadata_sha})),
        "design_authority_ref": weight_design_auth.as_dict(),
        "estimand_authority_ref": weight_estimand_auth.as_dict(),
        "effective_scope_ref": _ref_dict(_ref(
            "WEIGHT_EFFECTIVE_SCOPE",
            f"urn:rawlsing:r157:fixture:{fixture_id_value}:unweighted-validation-scope",
            {"fixture_id": fixture_id_value, "scope": "NOT_A_WEIGHTED_ESTIMAND"})),
        "normalization_ref": None,
        "values": weight_values,
        "copy_observed_numeric": False,
        "extra_authority_refs": [],
    }]

    physical_payloads = []
    for slot in profile["physical_rows"]:
        if slot["ordinal"] not in selected_ordinals:
            continue
        if slot["name"] == "id":
            disposition = "FIXTURE_ROW_KEY"
            reason = (
                "Synthetic nonrespondent fixture id cell used to exercise P3 exact row-key extraction; "
                "it is not an original respondent id."
            )
        else:
            disposition, reason = _slot_disposition(slot["name"], selected_names, weight["name"])
        physical_payloads.append(_physical_payload(slot, disposition, reason))
    items_payload = [_item_payload(item) for item in selected_items]

    config_id = f"R157-GSS-{source_id}-NONRESPONDENT-FIXTURE-VALIDATION"
    doc = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id,
        "config_revision": 1,
        "config_purpose": "NONRESPONDENT_FIXTURE",
        "identity": {
            "source_id": source_id,
            "family": roster["family"],
            "wave": wave,
            "source_family_id": "GSS",
            "study_product_id": f"GSS_{wave}",
            "release_id": f"GSS_{wave}_SOURCE_ARTIFACT",
            "instrument_release_id": f"SRC{source_id[-2:]}_METADATA_WITNESS_SHA256:{metadata_sha}",
            "source_artifact_id": roster["source_artifact_id"],
            "expected_source_sha256": original_sha,
            "source_format": roster["format"],
            "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"],
            "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"],
            "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": _ref_dict(ExactRef(
                "SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", original_sha)),
            "metadata_witness_ref": _ref_dict(ExactRef(
                "R154_PHYSICAL_METADATA",
                f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                metadata_sha)),
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
            },
            "reader": {
                "decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                "configuration_ref": _ref_dict(_ref(
                    "READER_CONFIGURATION",
                    f"urn:rawlsing:r157:reader:{source_id}:default_sav",
                    {
                        "source_id": source_id,
                        "decoder": "decode_sav",
                        "encoding": None,
                        "source_sha256": original_sha,
                    })),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "NONRESPONDENT_FIXTURE",
            "source_sha256": fixture_sha,
            "row_count": FIXTURE_ROWS,
            "source_snapshot_ref": _ref_dict(ExactRef(
                "FIXTURE_SNAPSHOT", f"urn:rawlsing:r157:fixture:{fixture_id_value}", fixture_sha)),
            "fixture_provenance": {
                "fixture_id": fixture_id_value,
                "provenance": "Repository-generated nonrespondent fixture for the R157 GSS lane; synthetic cells, no original respondents represented.",
                "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                "original_source_id": source_id,
                "original_source_sha256": original_sha,
                "no_original_respondents": True,
                "fixture_study_product_id": f"R157_GSS_FIXTURE/{source_id}",
                "fixture_release_id": f"R157_GSS_FIXTURE_RELEASE/{source_id}",
                "fixture_instrument_release_id": f"R157_GSS_FIXTURE_INSTRUMENT/{source_id}",
            },
        },
        "authority": {
            "snapshots": snapshots,
            "required_refs": [ref.as_dict() for ref in required],
            "projection_authority_ref": projection_auth.as_dict(),
            "replay_authority_ref": replay_auth.as_dict(),
            "projection_identity_ref": projection_identity.as_dict(),
            "tie_order_ref": _ref_dict(_ref(
                "ORDER_RULE", "urn:rawlsing:r157:order:canonical-exact-ref",
                {"rule": "CANONICAL_REF_SORT"})),
            "replay_protocol_version": "1.0.0",
        },
        "universe": {"universes": [universe]},
        "respondents": {
            "subject_unit": "NONRESPONDENT_FIXTURE_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:fixture:{fixture_id_value}:respondent",
            "respondent_key_pattern": f"R157-FIXTURE-{source_id}-ROW-{{row_ordinal:02d}}",
            "source_native_key_slot": {"ordinal": physical["id"]["ordinal"], "name": "id"},
            "identity_map_authority_ref": None,
            "row_identity_grade": "NONRESPONDENT_FIXTURE_KEY_EXTRACTION_ONLY",
        },
        "questions": questions,
        "physical_slots": physical_payloads,
        "items": items_payload,
        "response_slots": response_slots,
        "coordinate_slots": coordinates,
        "weight_slots": weight_slots,
        "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": TypedAbsence("NOT_APPLICABLE").as_dict(),
            "comparator": TypedAbsence("DEFERRED").as_dict(),
            "discovery": TypedAbsence("DEFERRED").as_dict(),
            "structural": TypedAbsence("NOT_APPLICABLE").as_dict(),
        },
        "supported_scope": {
            "scope_id": f"{source_id}-GSS-NONRESPONDENT-FIXTURE-VALIDATION",
            "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
            "declared_supported": True,
            "supported_question_ids": [f"FIXTURE:{source_id}:{name}" for name in SELECTED_QUESTIONS],
            "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS",
            "supported_form_slice": "SCALAR_SINGLE_OBSERVATION_FIXTURE_ONLY",
            "notes": [
                "Fixture authority is explicitly nonrespondent and does not establish original-source authority.",
                "The fixture exercises source-specific scalar response/missing rules, two raw coordinates and an unresolved-basis weight section.",
                "Original GSS respondent execution is NOT performed or claimed.",
            ],
        },
        "coverage": {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": sorted(selected_ordinals),
            "items_included": [item["implementation_id"] for item in selected_items],
            "partial_scope_reason": "Nonrespondent fixture exercises only the declared source-local scalar rule slice.",
        },
        "residuals": [
            {
                "residual_id": f"{source_id}-FIXTURE-IDENTITY",
                "scope": f"{source_id}/fixture",
                "field": "binding.identity_class",
                "status": "FIXTURE_ONLY",
                "reason": "Fixture bytes, universe, authority and row identities are distinct from the original source and are not promoted.",
                "dependent_operation": "original-source use",
                "unaffected_scope": "actual factory and native C11 validation",
                "owner": "R157 GSS lane author",
                "next_step": "Consume the original config only with permitted original bytes and decode-produced row witnesses.",
            },
            {
                "residual_id": f"{source_id}-FIXTURE-WEIGHT",
                "scope": f"{source_id}/weight_slots",
                "field": "weight_slots[].weight_basis_id",
                "status": "WEIGHT_BASIS_UNRESOLVED",
                "reason": "Fixture exercises exact numeric weight cells, but no weighted design/estimand claim is made.",
                "dependent_operation": "weighted inference",
                "unaffected_scope": "nonrespondent scalar/coordinate native validation",
                "owner": "R157 GSS lane author",
                "next_step": "Establish design/estimand/normalization authority before any weighted scope.",
            },
        ],
        "evidence": {
            "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
            "pinned_inputs": _pinned_inputs(),
            "field_evidence": _field_evidence(
                source_id=source_id, profile=profile, metadata_sha=metadata_sha),
            "limits": [
                "Fixture identity and fixture authority are separate from original-source identity.",
                "No original respondent row or original source byte is read.",
                "A native fixture release is not an original-source empirical workload.",
            ],
        },
        "runtime": _runtime_section(fixture=True),
        "notes": [
            "This is a clearly nonrespondent fixture config, not the original source config.",
            "Weight facts are emitted with unresolved basis, not as an authorized weighted estimand.",
        ],
    }
    return doc, fixture_doc


def _native_validation(
    *, source_id: str, fixture_doc: Mapping[str, Any], fixture_config_path: Path,
    original_config_path: Path,
) -> dict[str, Any]:
    original_cfg = load_source_config(original_config_path)
    fixture_cfg = load_source_config(fixture_config_path)
    stream = load_fixture_stream(fixture_config_path.parent / f"{source_id}.fixture.json")
    fixture_row_keys = row_native_keys_from_transport(fixture_cfg, stream=stream)
    projection = build_governed_c11_projection(
        fixture_cfg, row_native_keys=fixture_row_keys)
    release = build_validated_c11_release_from_config(fixture_cfg, stream=stream)
    repository, repository_release = build_source_backed_c11_repository_from_config(
        fixture_cfg, stream)

    reader_configuration = reader_configuration_from_config(original_cfg)
    read_request = source_read_request_from_config(
        original_cfg,
        host="R157_PREPARATION_HOST",
        purpose="SOURCE_CONFIGURATION_PREPARATION",
        consumer_use="R157_GSS_LANE_CONFIGURATION",
        semantic_use_scope=("response_rule_configuration", "coordinate_configuration"),
    )
    if release.release_ref != repository_release.release_ref:
        raise RuntimeError("stream and repository native releases differ")

    events = [obj for obj in release.public_objects if isinstance(obj, RespondentEvent)]
    coords = [obj for obj in release.public_objects if isinstance(obj, EmpiricalCoordinateFact)]
    weights = [obj for obj in release.public_objects if isinstance(obj, WeightMeasureFact)]
    universes = [obj for obj in release.public_objects if isinstance(obj, EmpiricalUniverse)]
    authority_objects = [obj for obj in release.public_objects if isinstance(obj, AuthoritySnapshot)]
    canonical_all_null = all(
        event.canonical_response_value_if_authorized is None for event in events)
    response_states = Counter(event.response_state for event in events)
    coordinate_states = Counter(coord.coordinate_state for coord in coords)
    weight_states = Counter(weight.weight_state for weight in weights)
    # Map exact native question refs from the fixture config without inference.
    native_question_by_key = {}
    for question in fixture_cfg.document["questions"]:
        native_question_by_key[
            f"{question['native_question_ref']['kind']}|{question['native_question_ref']['object_id']}|{question['native_question_ref']['content_hash']}"
        ] = question["question_id"]
    by_question: dict[str, Counter[str]] = {}
    for event in events:
        native_ref = event.native_question_ref
        native_key = (
            f"{native_ref['kind']}|{native_ref['object_id']}|{native_ref['content_hash']}")
        qid = native_question_by_key[native_key]
        by_question.setdefault(qid, Counter())[event.response_state] += 1
    expected = fixture_doc["expected_results"]
    expected_match = (
        len(events) == expected["response_event_count"]
        and len(coords) == expected["coordinate_fact_count"]
        and len(release.public_objects) > 0
        and canonical_all_null
        and dict(sorted(response_states.items())) == expected["response_state_counts"]
        and {qid: dict(sorted(c.items())) for qid, c in by_question.items()}
            == expected["response_state_counts_by_question"]
        and dict(sorted(coordinate_states.items())) == expected["coordinate_state_counts"]
        and dict(sorted(weight_states.items())) == expected["weight_state_counts"]
        and len(weights) == expected["weight_fact_count"]
    )
    if not expected_match:
        raise RuntimeError(f"{source_id} native fixture results differ from declared oracle")

    original_projection_refusal = None
    try:
        build_governed_c11_projection(original_cfg)
    except Exception as exc:  # exact expected refusal for undecoded row keys
        original_projection_refusal = {
            "call": "rawlsing_next.source_configuration.factory.build_governed_c11_projection(original_config)",
            "outcome": "REFUSED",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    if original_projection_refusal is None:
        raise RuntimeError("original config unexpectedly constructed without row-native keys")

    original_against_fixture_refusal = None
    try:
        build_validated_c11_release_from_config(original_cfg, stream=stream)
    except Exception as exc:  # exact wrong-source refusal; no original key is invented
        original_against_fixture_refusal = {
            "call": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config(original_config, stream=fixture_stream)",
            "outcome": "REFUSED",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    if original_against_fixture_refusal is None:
        raise RuntimeError("original config unexpectedly accepted the fixture stream")

    wrong_sha = "f" * 64
    wrong_sha_refusal = None
    try:
        build_validated_c11_release_from_config(
            fixture_cfg,
            stream=ExactPhysicalCellStream(wrong_sha, stream.row_count, stream.iter_cells),
        )
    except Exception as exc:
        wrong_sha_refusal = {
            "call": "build_validated_c11_release_from_config(fixture_config, stream=wrong_sha_stream)",
            "outcome": "REFUSED",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    if wrong_sha_refusal is None:
        raise RuntimeError("wrong fixture source SHA unexpectedly accepted")

    wrong_rows = stream.row_count - 1
    wrong_rows_refusal = None
    try:
        build_validated_c11_release_from_config(
            fixture_cfg,
            stream=ExactPhysicalCellStream(stream.source_sha256, wrong_rows, stream.iter_cells),
        )
    except Exception as exc:
        wrong_rows_refusal = {
            "call": "build_validated_c11_release_from_config(fixture_config, stream=wrong_row_count_stream)",
            "outcome": "REFUSED",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    if wrong_rows_refusal is None:
        raise RuntimeError("wrong row count unexpectedly accepted")

    return {
        "projection": {
            "type": type(projection).__name__,
            "projection_identity_ref": projection.projection_identity_ref.as_dict(),
            "expected_source_sha256": projection.expected_source_sha256,
            "respondents": len(projection.respondents),
            "questions": len(projection.questions),
            "response_slots": len(projection.response_slots),
            "coordinate_slots": len(projection.coordinate_slots),
            "weight_slots": len(projection.weight_slots),
            "routing_facts": len(projection.routing),
            "authority_snapshots": len(projection.authority_snapshots),
        },
        "release": {
            "type": type(release).__name__,
            "release_id": release.release_id,
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "source_artifact_ref": release.source_artifact_ref.as_dict(),
            "m01_m18_coverage": {k: list(v) for k, v in release.m01_m18_coverage.items()},
            "universes": len(universes),
            "respondent_events": len(events),
            "coordinate_facts": len(coords),
            "weight_facts": len(weights),
            "authority_snapshots": len(authority_objects),
        },
        "actual": {
            "response_state_counts": dict(sorted(response_states.items())),
            "response_state_counts_by_question": {
                qid: dict(sorted(counts.items())) for qid, counts in sorted(by_question.items())
            },
            "coordinate_state_counts": dict(sorted(coordinate_states.items())),
            "weight_state_counts": dict(sorted(weight_states.items())),
            "canonical_response_values_all_null": canonical_all_null,
        },
        "expected_match": expected_match,
        "p3_row_native_keys": {
            "configured_slot": fixture_cfg.document["respondents"]["source_native_key_slot"],
            "witness_count": len(fixture_row_keys),
            "kinds": sorted({type(value).__name__ for value in fixture_row_keys.values()}),
            "fixture_bound_object_prefix": f"urn:rawlsing:r157:r157_nonrespondent_fixture_key",
            "all_witnesses_fixture_bound": all(
                getattr(value, "kind", None) == "R157_NONRESPONDENT_FIXTURE_KEY"
                for value in fixture_row_keys.values()),
        },
        "p3_reader_transport": {
            "reader_configuration": {
                "source_sha256": reader_configuration.source_sha256,
                "configuration_ref": reader_configuration.configuration_ref.as_dict(),
                "encoding": reader_configuration.encoding,
                "authority_status": reader_configuration.authority_status,
            },
            "source_read_request": {
                "source_id": read_request.source_id,
                "source_sha256": read_request.source_sha256,
                "source_format": read_request.source_format,
                "custody_locator_binding": read_request.custody_locator_binding,
                "host": read_request.host,
                "purpose": read_request.purpose,
                "consumer_use": read_request.consumer_use,
                "semantic_use_scope": list(read_request.semantic_use_scope),
            },
            "source_bytes_read": False,
            "permission_decision": "NOT_REQUESTED_OR_EVALUATED_IN_PREPARATION",
        },
        "repository": {
            "release_refs": [ref.as_dict() for ref in repository.release_refs],
            "release_ref_matches_stream": repository_release.release_ref.as_dict() == release.release_ref.as_dict(),
        },
        "refusals": {
            "original_without_row_keys": original_projection_refusal,
            "original_with_fixture_stream": original_against_fixture_refusal,
            "fixture_wrong_source_sha": wrong_sha_refusal,
            "fixture_wrong_row_count": wrong_rows_refusal,
        },
    }


def _build_one(source_id: str) -> dict[str, Any]:
    profile = _source_profiles(source_id)
    original_doc = _build_original(source_id, profile)
    validate_source_config(original_doc)
    fixture_doc, fixture_bytes = _build_fixture(
        source_id=source_id, profile=profile, original_doc=original_doc)
    validate_source_config(fixture_doc)

    data_dir = DATA_ROOT / source_id
    validation_dir = VALIDATION_ROOT / source_id
    original_path = data_dir / f"{source_id}.source.config.json"
    evidence_path = data_dir / f"{source_id}.evidence-accounting.json"
    fixture_config_path = validation_dir / f"{source_id}.fixture.config.json"
    fixture_path = validation_dir / f"{source_id}.fixture.json"
    spec_path = validation_dir / f"{source_id}.fixture-spec.json"
    results_path = validation_dir / f"{source_id}.validation-results.json"
    exceptions_path = validation_dir / f"{source_id}.exceptions.json"
    manifest_path = validation_dir / f"{source_id}.manifest.json"

    _json_write(original_path, original_doc)
    _json_write(fixture_config_path, fixture_doc)
    _json_write(fixture_path, fixture_bytes)
    _json_write(spec_path, {
        "schema": "PYAT_R157_GSS_FIXTURE_SPEC@1.0.0",
        "source_id": source_id,
        "fixture_id": fixture_bytes["fixture_id"],
        "fixture_path": str(fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": config_file_sha256(fixture_path),
        "fixture_source_sha256": fixture_bytes["fixture_source_sha256"],
        "fixture_config_path": str(fixture_config_path.relative_to(ROOT)),
        "fixture_config_canonical_sha256": canonical_config_hash(fixture_doc),
        "fixture_config_file_sha256": config_file_sha256(fixture_config_path),
        "original_source_id": source_id,
        "original_source_sha256": profile["roster"]["source_sha256"],
        "identity_class": "NONRESPONDENT_FIXTURE",
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "row_count": FIXTURE_ROWS,
        "expected_results": fixture_bytes["expected_results"],
        "oracle_basis": "Expected counts/states are derived from the declared fixture cells and the serialized source response rules before the native call.",
        "limits": [
            "Synthetic nonrespondent fixture cells; no original respondent is represented.",
            "Fixture authority and fixture SHA are not original-source meaning.",
        ],
    })

    native = _native_validation(
        source_id=source_id,
        fixture_doc=fixture_bytes,
        fixture_config_path=fixture_config_path,
        original_config_path=original_path,
    )
    selected = profile["selected_items"]
    original_canonical = canonical_config_hash(original_doc)
    fixture_canonical = canonical_config_hash(fixture_doc)
    results = {
        "schema": "PYAT_R157_GSS_SOURCE_VALIDATION_RESULTS@1.0.0",
        "plan_seal": PLAN_SEAL,
        "p0_correction_consumed": P0_CORRECTION,
        "p3_terminal_runtime_consumed": P3_RUNTIME,
        "source_id": source_id,
        "source_format": profile["roster"]["format"],
        "wave": str(profile["roster"]["wave"]),
        "commands": [
            "PYTHONPATH=. python3 source_pre553_validation/SRC16/build_gss_lane.py --all",
            "PYTHONPATH=. python3 -m pytest source_pre553_validation/SRC16/test_gss_lane.py -q -o addopts=''",
        ],
        "config_validation": {
            "validator": "rawlsing_next.source_configuration.schema.validate_source_config",
            "original_path": str(original_path.relative_to(ROOT)),
            "original_config_canonical_sha256": original_canonical,
            "original_config_file_sha256": config_file_sha256(original_path),
            "fixture_path": str(fixture_config_path.relative_to(ROOT)),
            "fixture_config_canonical_sha256": fixture_canonical,
            "fixture_config_file_sha256": config_file_sha256(fixture_config_path),
            "passed": True,
        },
        "coverage": {
            "physical_slots_total": profile["roster"]["physical_columns"],
            "original_items_total": profile["roster"]["original_items"],
            "physical_slots_serialized": len(original_doc["physical_slots"]),
            "items_serialized": len(original_doc["items"]),
            "physical_slots_included": len(original_doc["coverage"]["physical_slots_included"]),
            "items_included": len(original_doc["coverage"]["items_included"]),
            "physical_slots_excluded": len(original_doc["coverage"]["physical_slots_excluded"]),
            "items_excluded": len(original_doc["coverage"]["items_excluded"]),
            "no_drop": (
                len(original_doc["physical_slots"]) == profile["roster"]["physical_columns"]
                and len(original_doc["items"]) == profile["roster"]["original_items"]
                and len(original_doc["coverage"]["physical_slots_included"])
                    + len(original_doc["coverage"]["physical_slots_excluded"])
                    == profile["roster"]["physical_columns"]
                and len(original_doc["coverage"]["items_included"])
                    + len(original_doc["coverage"]["items_excluded"])
                    == profile["roster"]["original_items"]
            ),
            "supported_question_ids": [item["p2"]["question_id"] for item in selected],
        },
        "native_validation": native,
        "identity_separation": {
            "original_source_sha256": profile["roster"]["source_sha256"],
            "fixture_source_sha256": fixture_bytes["fixture_source_sha256"],
            "distinct_bytes": profile["roster"]["source_sha256"] != fixture_bytes["fixture_source_sha256"],
            "original_binding_identity_class": original_doc["binding"]["identity_class"],
            "fixture_binding_identity_class": fixture_doc["binding"]["identity_class"],
            "original_authority_has_fixture_only": any(
                snapshot["scope_envelope"].get("fixture_only") is True
                for snapshot in original_doc["authority"]["snapshots"]),
            "fixture_authority_all_fixture_only": all(
                snapshot["scope_envelope"].get("fixture_only") is True
                and snapshot["scope_envelope"].get("grade") == "NONRESPONDENT_FIXTURE_ONLY"
                for snapshot in fixture_doc["authority"]["snapshots"]),
            "original_binding_matches_original_sha": (
                original_doc["binding"]["source_sha256"]
                == original_doc["identity"]["expected_source_sha256"]),
            "fixture_binding_differs_from_original_sha": (
                fixture_doc["binding"]["source_sha256"]
                != fixture_doc["identity"]["expected_source_sha256"]),
        },
        "residuals": original_doc["residuals"],
        "limits": [
            "Original GSS respondent execution is NOT performed or claimed.",
            "The positive native release is from a distinct nonrespondent fixture config and fixture bytes.",
            "Original construction requires permitted decode-produced row_native_keys and remains P3 reader/transport work.",
            "No cross-wave equivalence, pooling, canonical mapping, weight authorization or population claim is asserted.",
        ],
    }
    _json_write(results_path, results)
    _json_write(exceptions_path, {
        "schema": "PYAT_R157_GSS_EXCEPTION_LEDGER@1.0.0",
        "source_id": source_id,
        "source_config": str(original_path.relative_to(ROOT)),
        "residual_count": len(original_doc["residuals"]),
        "residuals": original_doc["residuals"],
        "fixture_limits": fixture_doc["residuals"],
        "blocking_lane_completion": False,
        "blocking_original_execution": True,
        "exact_next_operation": "P3 integration owner transports the qualified exact-SHA reader config and populates row_native_keys from permitted decoded id cells; original source execution remains separately authorized.",
    })

    evidence_accounting = {
        "schema": "PYAT_R157_GSS_EVIDENCE_ACCOUNTING@1.0.0",
        "source_id": source_id,
        "source_paths": {
            "source_config": str(original_path.relative_to(ROOT)),
            "fixture_config": str(fixture_config_path.relative_to(ROOT)),
            "fixture": str(fixture_path.relative_to(ROOT)),
            "fixture_spec": str(spec_path.relative_to(ROOT)),
            "validation_results": str(results_path.relative_to(ROOT)),
            "exceptions": str(exceptions_path.relative_to(ROOT)),
        },
        "counts": {
            "physical_columns": profile["roster"]["physical_columns"],
            "codebook_rows": profile["roster"]["codebook_rows"],
            "original_items": profile["roster"]["original_items"],
            "exact_relation_matches": profile["roster"]["exact_relation_matches"],
            "participating_implementation_ids": [item["implementation_id"] for item in selected],
        },
        "selected_items": [
            {
                "source_variable_code": item["source_variable_code"],
                "implementation_id": item["implementation_id"],
                "exact_identity_sha256": item["exact_identity_sha256"],
                "question_text": item["p2"]["question_text"],
                "p2_question_id": item["p2"]["question_id"],
                "relation_question_id": item["relation"]["question_id"],
                "h48_binding_grade": item["h48"]["binding_grade"],
                "relation_authority_status": item["relation"]["authority_status"],
                "mapping_status": item["relation"]["mapping_status"],
                "evidence_refs": _evidence_refs(item),
            }
            for item in selected
        ],
        "all_items_accounted": len(original_doc["items"]) == profile["roster"]["original_items"],
        "all_physical_slots_accounted": len(original_doc["physical_slots"]) == profile["roster"]["physical_columns"],
        "excluded_item_count": len(original_doc["coverage"]["items_excluded"]),
        "excluded_slot_count": len(original_doc["coverage"]["physical_slots_excluded"]),
        "weight_slot": {
            "ordinal": profile["weight"]["ordinal"],
            "name": profile["weight"]["name"],
            "status": "HELD_WEIGHT_DESIGN_UNRESOLVED",
        },
        "evidence_inputs": {
            "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "source_roster_sha256": _file_identity(
                ROOT / "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json")["sha256"],
            "item_evidence_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "item_evidence_sha256": load_manifest()["files"]["ITEM_EVIDENCE.jsonl.gz"]["sha256"],
            "physical_slots_path": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
            "physical_slots_sha256": load_manifest()["files"]["PHYSICAL_SLOTS.jsonl.gz"]["sha256"],
            "codebook_rows_path": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
            "codebook_rows_sha256": load_manifest()["files"]["CODEBOOK_ROWS.jsonl.gz"]["sha256"],
        },
        "limits": [
            "No original respondent row or original source byte was read.",
            "Evidence grades and limits are copied, not promoted.",
            "The fixture is a separate nonrespondent identity and source-specific rule exercise.",
        ],
    }
    _json_write(evidence_path, evidence_accounting)

    manifest = {
        "schema": "PYAT_R157_GSS_SOURCE_MANIFEST@1.0.0",
        "source_id": source_id,
        "paths": {
            "source_config": _file_identity(original_path),
            "evidence_accounting": _file_identity(evidence_path),
            "fixture_config": _file_identity(fixture_config_path),
            "fixture": _file_identity(fixture_path),
            "fixture_spec": _file_identity(spec_path),
            "validation_results": _file_identity(results_path),
            "exceptions": _file_identity(exceptions_path),
        },
        "config_hashes": {
            "original_config_canonical_sha256": original_canonical,
            "original_config_file_sha256": config_file_sha256(original_path),
            "fixture_config_canonical_sha256": fixture_canonical,
            "fixture_config_file_sha256": config_file_sha256(fixture_config_path),
            "fixture_source_sha256": fixture_bytes["fixture_source_sha256"],
        },
        "native_release_ref": native["release"]["release_ref"],
        "no_drop": results["coverage"]["no_drop"],
        "limits": results["limits"],
    }
    _json_write(manifest_path, manifest)
    return {
        "source_id": source_id,
        "manifest": manifest,
        "results": results,
        "paths": manifest["paths"],
    }


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=SOURCE_IDS, action="append")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)
    source_ids = list(SOURCE_IDS) if args.all or not args.source else list(args.source)
    outputs = [_build_one(source_id) for source_id in source_ids]
    print(json.dumps([{
        "source_id": output["source_id"],
        "manifest": output["paths"],
        "native_release_ref": output["results"]["native_validation"]["release"]["release_ref"],
        "no_drop": output["results"]["coverage"]["no_drop"],
    } for output in outputs], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
