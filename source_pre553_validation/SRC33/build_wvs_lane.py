"""Build and natively validate the R157 WVS source-configuration lane.

Writes only SRC33/SRC34/SRC35 data and validation directories.  Reads only the
frozen portable evidence package and uses the existing factory/native owners.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

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
from rawlsing_next.source_configuration.fixture import fixture_document_sha256, load_fixture_stream
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
SOURCE_IDS = ("SRC33", "SRC34", "SRC35")
FIXTURE_ROWS = 6
FIXTURE_PROFILE = {
    "SRC33": {"key": "S007", "weight": "V236", "country": "V2", "time": "V1", "region": "N_REGION_ISO"},
    "SRC34": {"key": "V3", "weight": "V245", "country": "V2", "time": "V1", "region": "REGION_ISO"},
    "SRC35": {"key": "S007", "weight": "W_WEIGHT", "country": "B_COUNTRY", "time": "A_YEAR", "region": "N_REGION_ISO"},
}
HELD_ROLE_REASON = {
    "GEN_FORBIDDEN": (
        "P2 explicitly marks the item generation_forbidden; identity and evidence are retained but no response rule is promoted.",
        "questions[].response_slots",
        "generation/feature use",
    ),
    "ADMIN": (
        "The item is administrative metadata, not a respondent response target.",
        "physical_slots[].disposition",
        "administrative/metadata use",
    ),
    "UNKNOWN": (
        "P2 records an unknown semantic disposition; values are retained without response promotion.",
        "questions[].response_slots",
        "semantic response projection",
    ),
    "RANKED": (
        "manual_response_topology is ranked_choice, but the single physical column does not carry an exact component/rank map; rank order cannot be invented.",
        "response_slots[].values[].occurrences",
        "ranked response projection",
    ),
    "CONTINUOUS": (
        "The item has no substantive source value labels and is continuous/typed numeric; native ResponseSlotRule requires exact finite value keys.",
        "questions[].response_slots",
        "continuous response projection",
    ),
    "POSITION": (
        "The item is a position/context code, not a declared response target; raw codebook identity is retained.",
        "coordinate_slots[].native_coordinate_ref",
        "coordinate/context interpretation",
    ),
}


def _sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str, material: Any) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


def _json_write(path: Path, document: Mapping[str, Any], *, compact: bool | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact is None:
        compact = path.name.endswith((".source.config.json", ".fixture.config.json", ".fixture.json"))
    text = (json.dumps(document, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
            if compact else json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False))
    path.write_text(text + "\n", encoding="utf-8")


def _file_identity(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _positive_labels(slot: Mapping[str, Any]) -> list[float]:
    out = []
    for raw in (slot.get("value_labels") or {}):
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value >= 0:
            out.append(value)
    return sorted(set(out))


def _negative_labels(slot: Mapping[str, Any]) -> list[float]:
    out = []
    for raw in (slot.get("value_labels") or {}):
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        if value < 0:
            out.append(value)
    return sorted(set(out))


def _missing_state(raw: float, label: str) -> str | None:
    text = label.lower()
    if raw == -1 or "don't know" in text or "dont know" in text or "don´t know" in text:
        return "DK"
    if raw == -2 or "no answer" in text or "no contesta" in text:
        return "MISSING"
    if raw == -3 or "not applicable" in text or "inap" in text:
        return "INAPPLICABLE"
    if raw == -4 or "not asked" in text or "not available" in text:
        return "NOT_ASKED"
    if raw in {-5, -99, -999} or "missing" in text or "unknown" in text or "no data" in text:
        return "MISSING"
    return None


def _response_state(slot: Mapping[str, Any], raw: float) -> str:
    label = str((slot.get("value_labels") or {}).get(str(raw), ""))
    # tolerate key spelling variants such as 1 vs 1.0
    if not label:
        for key, value in (slot.get("value_labels") or {}).items():
            try:
                if float(key) == raw:
                    label = str(value)
                    break
            except (TypeError, ValueError):
                pass
    if raw >= 0:
        return "SUBSTANTIVE_RESPONSE"
    mapped = _missing_state(raw, label)
    return mapped or "SOURCE_SPECIFIC_SPECIAL"


def _item_role(item: Mapping[str, Any], slot: Mapping[str, Any], profile: Mapping[str, Any]) -> str:
    name = item["source_variable_code"]
    disposition = str(item["p2"]["canonical_disposition"]).lower()
    topology = str((item.get("relation") or {}).get("manual_response_topology") or "")
    if name == profile["key"]:
        return "KEY"
    if name == profile["weight"]:
        return "WEIGHT"
    if name in {profile["country"], profile["time"], profile["region"]}:
        return "COORDINATE"
    if "generation_forbidden" in disposition:
        return "GEN_FORBIDDEN"
    if "admin" in disposition:
        return "ADMIN"
    if "unknown" in disposition:
        return "UNKNOWN"
    if topology == "ranked_choice":
        return "RANKED"
    if topology == "multiselect_child":
        return "MULTI_CHILD"
    if "coordinate" in disposition or "structural_context" in disposition:
        return "POSITION"
    if not _positive_labels(slot):
        return "CONTINUOUS"
    return "BOUND"


def _source_profiles(source_id: str) -> dict[str, Any]:
    roster = source_roster_entry(source_id)
    physical_rows = list(iter_physical_slots(source_id))
    physical = {row["name"]: row for row in physical_rows}
    codebook_rows = list(iter_codebook_rows(source_id))
    raw_items = list(iter_item_evidence(source_id))
    items = sorted(raw_items, key=lambda item: physical[item["source_variable_code"]]["ordinal"])
    profile = FIXTURE_PROFILE[source_id]
    for name in (profile["key"], profile["weight"], profile["country"], profile["time"], profile["region"]):
        if name not in physical:
            raise RuntimeError(f"{source_id} lacks required source slot {name!r}")
    roles = {
        item["source_variable_code"]: _item_role(item, physical[item["source_variable_code"]], profile)
        for item in items
    }
    bound = [item for item in items if roles[item["source_variable_code"]] in {"BOUND", "MULTI_CHILD"}]
    held = [item for item in items if roles[item["source_variable_code"]] not in {"BOUND", "MULTI_CHILD"}]
    held_by_role: dict[str, list[Mapping[str, Any]]] = {}
    for item in held:
        held_by_role.setdefault(roles[item["source_variable_code"]], []).append(item)
    if not bound:
        raise RuntimeError(f"{source_id} has no response-bound items")
    return {
        "roster": roster, "physical_rows": physical_rows, "physical": physical,
        "codebook_rows": codebook_rows, "items": items, "bound": bound,
        "held": held, "held_by_role": held_by_role, "roles": roles,
        "profile": profile,
    }


def _authority_snapshot(
    *, authority_id: str, kind: str, decision: str, source_id: str, original_sha: str,
    wave: str, families: Sequence[str], operations: Sequence[str], bundle_sha: str,
    fixture_id: str | None = None, fixture_sha: str | None = None, protocol: bool = False,
) -> dict[str, Any]:
    if fixture_id is not None:
        scope = {
            "fixture_only": True, "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "fixture_id": fixture_id, "source_id": source_id,
            "source_sha256": original_sha, "original_source_sha256": original_sha,
            "fixture_source_sha256": fixture_sha, "evidence_bundle_sha256": bundle_sha,
        }
        effective = "R157_NONRESPONDENT_FIXTURE"
    elif protocol:
        scope = {
            "source_id": source_id, "source_sha256": original_sha, "wave": wave,
            "grade": "R157_NATIVE_PROTOCOL_ONLY", "evidence_bundle_sha256": bundle_sha,
            "not_source_scientific_authority": True,
        }
        effective = "R157_NATIVE_PRE553_PROTOCOL"
    else:
        scope = {
            "source_id": source_id, "source_sha256": original_sha, "wave": wave,
            "grade": "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION",
            "p2_authority_status": "source_reviewed", "evidence_bundle_sha256": bundle_sha,
            "not_source_scientific_authority": True,
        }
        effective = f"WVS_{wave}"
    content_hash = semantic_hash({
        "authority_id": authority_id, "kind": kind, "decision": decision,
        "source_id": source_id, "original_sha": original_sha, "wave": wave,
        "bundle": bundle_sha, "fixture_id": fixture_id, "fixture_sha": fixture_sha,
        "protocol": protocol,
    })
    replay = _ref("REPLAY_PROTOCOL", "urn:rawlsing:r157:native-replay-protocol:1.0.0", {
        "protocol": "PRE553_REPLAY", "ingest": INGEST_CONTRACT_VERSION, "codec": R5_CODEC_VERSION,
    })
    return {
        "typed_state": decision, "authority_snapshot_refs": [], "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _ref(
            "REPLAY_ROOT", f"urn:rawlsing:r157:{source_id}:authority:{authority_id}",
            {"authority_id": authority_id, "bundle": bundle_sha}).as_dict(),
        "authority_id": authority_id, "authority_version": "1.0.0",
        "authority_content_hash": content_hash, "authority_kind": kind,
        "decision_state": decision, "governed_operations": list(operations),
        "governed_object_families": list(families), "scope_envelope": scope,
        "effective_time_or_interval": effective,
        "parent_authority_refs": [], "negative_limit_refs": [], "supersession_refs": [],
        "interpretation_semantics_fingerprint": semantic_hash({
            "authority_id": authority_id, "kind": kind, "decision": decision, "scope": scope}),
        "replay_protocol_ref": replay.as_dict(),
    }


def _authority_ref(snapshot: Mapping[str, Any]) -> AuthorityRef:
    return AuthorityRef(snapshot["authority_id"], snapshot["authority_version"], snapshot["authority_content_hash"])


def _evidence_refs(item: Mapping[str, Any]) -> list[dict[str, str]]:
    rel = item["relation"]
    return [
        ExactRef("H48_ITEM_AUTHORITY", f"urn:rawlsing:r157:h48:{item['implementation_id']}", item["exact_identity_sha256"]).as_dict(),
        ExactRef("P2_PHASE0_ROW", f"urn:rawlsing:r157:p2:{item['implementation_id']}", item["p2"]["exact_identity_sha256"]).as_dict(),
        ExactRef("FULL_RELATION_ROW", f"urn:rawlsing:r157:relation:{rel['question_id']}", rel["governed_row_payload_hash"]).as_dict(),
    ]


def _physical_payload(slot: Mapping[str, Any], role: str) -> dict[str, Any]:
    dispositions = {
        "BOUND": ("SUPPORTED_RESPONSE", "Finite-label source response rule bound to this physical slot."),
        "MULTI_CHILD": ("SUPPORTED_RESPONSE_CHILD_COLUMN", "Single multiselect child column bound without inventing set aggregation/component semantics."),
        "KEY": ("SOURCE_NATIVE_RESPONDENT_KEY", "Source-native respondent key slot; values require permitted decode."),
        "COORDINATE": ("SUPPORTED_COORDINATE", "Source-native country/time/region coordinate copied raw."),
        "WEIGHT": ("HELD_WEIGHT_DESIGN_UNRESOLVED", "Weight slot identified; design/estimand/normalization authority is not established."),
        "GEN_FORBIDDEN": ("RETAINED_GENERATION_FORBIDDEN", "P2 generation_forbidden; retained identity only."),
        "ADMIN": ("RETAINED_ADMINISTRATIVE", "Administrative metadata retained."),
        "UNKNOWN": ("RETAINED_UNKNOWN_SEMANTICS", "P2 unknown disposition retained without response promotion."),
        "RANKED": ("RETAINED_RANK_MAP_MISSING", "Ranked topology retained; exact rank/component map is unavailable."),
        "CONTINUOUS": ("RETAINED_CONTINUOUS_NO_FINITE_RULE", "Continuous value retained; finite native response rule not forced."),
        "POSITION": ("RETAINED_POSITION_CONTEXT", "Position/context code retained without response promotion."),
    }
    disposition, reason = dispositions[role]
    missing = None
    if slot.get("missing_user_values") is not None or slot.get("missing_ranges") is not None:
        missing = {"user_values": slot.get("missing_user_values"), "ranges": slot.get("missing_ranges")}
    return {
        "ordinal": slot["ordinal"], "name": slot["name"], "label": slot.get("label"),
        "storage_type": slot.get("readstat_type"), "original_type": slot.get("original_type"),
        "storage_width": slot.get("storage_width"), "measure": slot.get("measure"),
        "value_labels": slot.get("value_labels"), "missing_declarations": missing,
        "mr_declarations": None, "codebook_mapping": slot["codebook_mapping"],
        "disposition": disposition, "disposition_reason": reason,
    }


def _item_payload(item: Mapping[str, Any], role: str) -> dict[str, Any]:
    p2 = item["p2"]
    rel = item["relation"]
    limits = [
        f"h48_binding_grade={item['h48']['binding_grade']}",
        f"p2_authority_status={p2['authority_status']}",
        f"full_relation_authority_status={rel['authority_status']}",
        f"relation_use_status_final={rel['relation_use_status_final']}",
        f"manual_response_topology={rel['manual_response_topology']}",
        f"manual_signed_polarity_status={rel['manual_signed_polarity_status']}",
        f"configuration_role={role}",
        "R157 preparation does not issue original-source execution authority.",
    ]
    if rel["forbidden_inference"]:
        limits.append(f"forbidden_inference={rel['forbidden_inference']}")
    if rel["does_not_measure"]:
        limits.append(f"does_not_measure={rel['does_not_measure']}")
    return {
        "implementation_id": item["implementation_id"],
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "question_text": p2["question_text"],
        "disposition": p2["canonical_disposition"],
        "response_classes": p2["response_classes"],
        "mapping_status": rel["mapping_status"],
        "authority_status": rel["authority_status"],
        "evidence_refs": _evidence_refs(item),
        "limits": limits,
        "item_id": p2["question_id"],
        "relation": {
            "status": "EXACT",
            "question_id": rel["question_id"],
            "mapping_status": rel["mapping_status"],
            "manual_response_topology": rel["manual_response_topology"],
            "manual_response_normalization_rule": rel["manual_response_normalization_rule"],
            "manual_position_conditioning": rel["manual_position_conditioning"],
            "manual_semantic_role": rel["manual_semantic_role"],
            "manual_signed_polarity_status": rel["manual_signed_polarity_status"],
            "forbidden_inference": rel["forbidden_inference"] or "none recorded",
            "does_not_measure": rel["does_not_measure"] or "none recorded",
            "governed_row_payload_hash": rel["governed_row_payload_hash"],
            "p2_exact_identity_sha256": rel["p2_exact_identity_sha256"],
        },
    }


def _topology_ref(source_id: str, wave: str, original_sha: str, item: Mapping[str, Any], fixture_id: str | None) -> ExactRef:
    suffix = "fixture" if fixture_id else "source"
    return _ref("RESPONSE_TOPOLOGY", f"urn:rawlsing:r157:{suffix}:{source_id}:{item['source_variable_code']}:topology", {
        "source_id": source_id, "wave": wave, "source_sha256": original_sha,
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "manual_response_topology": item["relation"]["manual_response_topology"],
        "fixture_id": fixture_id,
    })


def _occurrence(topology: ExactRef, item: Mapping[str, Any]) -> dict[str, Any]:
    top = item["relation"]["manual_response_topology"]
    kinds = {
        "scalar": "SCALAR_SINGULAR", "nominal_choice": "NOMINAL_SINGLE_CHOICE",
        "binary_factual": "BINARY_SINGLE", "binary_contrast": "BINARY_SINGLE",
        "binary_tradeoff": "BINARY_TRADEOFF_SINGLE", "ordinal_context": "ORDINAL_CONTEXT_SINGLE",
        "context_index": "CONTEXT_INDEX_SINGLE", "continuous_context": "CONTINUOUS_CONTEXT_SINGLE",
        "multiselect_child": "MULTISELECT_CHILD_COLUMN", "administrative": "ADMINISTRATIVE_SINGLE",
    }
    kind = kinds.get(top, "SOURCE_SINGLE_COLUMN")
    fields: dict[str, Any] = {"kind": kind, "source_manual_topology": top, "index": 0}
    if top == "multiselect_child":
        fields["aggregation"] = "NOT_INVENTED_SINGLE_COLUMN"
    if top in {"ordinal_context", "context_index"}:
        fields["order_basis"] = "SOURCE_VALUE_LABELS_ONLY_NOT_RECODED"
    return {"key": "0", "topology_ref": topology.as_dict(), "multiplicity_order_rank_fields": fields}


def _response_values(slot: Mapping[str, Any], item: Mapping[str, Any], topology: ExactRef) -> list[dict[str, Any]]:
    occurrence = _occurrence(topology, item)
    values = []
    for raw_text in sorted((slot.get("value_labels") or {}), key=lambda x: float(x)):
        raw = float(raw_text)
        values.append({
            "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None, "response_state": _response_state(slot, raw),
            "occurrences": [occurrence], "canonical_value": None,
            "transform_authority_ref": None, "extra_authority_refs": [],
        })
    values.append({
        "raw_value": None, "missing_state": "SYSTEM_MISSING",
        "source_missing_declaration": None, "response_state": "MISSING",
        "occurrences": [occurrence], "canonical_value": None,
        "transform_authority_ref": None, "extra_authority_refs": [],
    })
    return values


def _residuals(source_id: str, wave: str, profile: Mapping[str, Any], held_by_role: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, str]]:
    rows = [
        ("NATIVE-ROW-KEY", "respondents.source_native_key_slot", "DECODE_REQUIRED",
         "The source-native key slot is declared, but no permitted decode-produced row key witness exists in preparation.",
         "original build_governed_c11_projection / build_validated_c11_release_from_config",
         "fixture validation and schema preparation", "P3/source-read owner",
         "Populate row_native_keys from permitted decoded key cells; original execution stays separate."),
        ("ROUTING-UNKNOWN", "routing[].typed_state", "ROUTING_UNKNOWN",
         "H48/O06 routing status is SOURCE_ROUTING_UNRESOLVED; exact form/ballot/administration routes are unavailable.",
         "eligibility/form-conditioned original claims", "raw response rules and fixture positive release",
         "WVS source evidence owner", "Recover exact route/form evidence before eligibility claims."),
        ("SOURCE-AUTHORITY-DEFER", "authority.snapshots", "DEFER",
         "H48/P2/full-relation evidence is source_reviewed candidate evidence, not an adopted original ALLOW authority.",
         "original scientific issuance", "preparation and nonrespondent fixture validation",
         "R157 authority owner", "Adjudicate exact source operation scope; do not promote fixture authority."),
        ("CANONICAL-VALUE", "response_slots[].values[].canonical_value", "NOT_AUTHORIZED",
         "No exact positive canonical mapping authority is present; raw source values/states are retained.",
         "canonicalized analysis", "raw response projection", "R157 mapping authority owner",
         "Adjudicate exact mappings before canonicalization."),
        ("WEIGHT-HELD", f"physical_slots[{profile['profile']['weight']}].weight", "HELD",
         "A source weight slot is identified; design/estimand/normalization authority is not established.",
         "weighted estimands", "unweighted source-local raw configuration", "WVS weight/design owner",
         "Establish design/estimand/normalization authority before a weighted scope."),
        ("FORM-ADMINISTRATION", "routing/supported_form_slice", "UNKNOWN",
         "Exact form/ballot/administration assignment is not recovered in the portable evidence.",
         "form/administration-conditioned claims", "unconditional source response rules", "WVS source evidence owner",
         "Recover exact assignment evidence if required."),
        ("SAMPLE-FRAME", "universe.sampling_design_regime", "UNRESOLVED",
         "WVS source is multi-country and wave-specific sample frames/designs are not reconstructed from metadata alone.",
         "population/design claims", "source-row identity and response rules", "WVS source evidence owner",
         "Recover exact country/wave frame/design evidence before population claims."),
    ]
    result = [{
        "residual_id": f"{source_id}-{suffix}", "scope": f"{source_id}",
        "field": field, "status": status, "reason": reason,
        "dependent_operation": dependent, "unaffected_scope": unaffected,
        "owner": owner, "next_step": next_step,
    } for suffix, field, status, reason, dependent, unaffected, owner, next_step in rows]
    for role, items in held_by_role.items():
        if role in {"KEY", "COORDINATE", "WEIGHT"} or not items:
            continue
        reason, native_field, dependent = HELD_ROLE_REASON.get(
            role, ("Source role is retained without response promotion.", "questions[].response_slots", "response projection"))
        result.append({
            "residual_id": f"{source_id}-{role}-HELD",
            "scope": f"{source_id}/{role.lower()}",
            "field": native_field, "status": f"{role}_HELD",
            "reason": f"{len(items)} exact items are held: {reason} Exact item/evidence rows: source_pre553_validation/{source_id}/{source_id}.exceptions.json#held_items.",
            "dependent_operation": dependent,
            "unaffected_scope": "other source-local rules and nonrespondent native validation",
            "owner": "WVS source/native-representation owner",
            "next_step": "Consume exact held-item evidence; do not substitute a default category or invented rank/aggregation.",
        })
    multi_children = [item for item in profile["bound"]
                      if profile["roles"][item["source_variable_code"]] == "MULTI_CHILD"]
    if multi_children:
        result.append({
            "residual_id": f"{source_id}-MULTISELECT-AGGREGATION",
            "scope": f"{source_id}/multiselect_child",
            "field": "response_slots[].values[].occurrences[].component_ref",
            "status": "AGGREGATION_NOT_INVENTED",
            "reason": (
                f"{len(multi_children)} exact multiselect child columns are bound as single columns; "
                "the portable evidence does not provide an exact member-set component/aggregation map. "
                f"Exact rows: source_pre553_validation/{source_id}/{source_id}.exceptions.json#bound_items."
            ),
            "dependent_operation": "multiselect set/component aggregation",
            "unaffected_scope": "each child column response rule and native event projection",
            "owner": "WVS source/topology owner",
            "next_step": "Recover exact member-set/component topology before aggregation; do not infer it from labels.",
        })
    return result


def _pinned_inputs() -> list[dict[str, Any]]:
    manifest = load_manifest()
    return [
        {"kind": "R157_PLAN_SEAL", "commit": PLAN_SEAL},
        {"kind": "R157_P0_CORRECTED_INTERFACE", "commit": P0_CORRECTION},
        {"kind": "R157_P3_TERMINAL_RUNTIME", "commit": P3_RUNTIME},
        {"kind": "R154_METADATA_SNAPSHOT", "commit": "a02adc896264e1b46afd143cba9426182ec14802",
         "path": "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite",
         "sha256": "7d6421e6e50f7d249cf09e7ecf964757d6afa4a7926d7a31eb1aad3407a12a16"},
        {"kind": "H48_ITEM_INDEX", "commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
         "path": "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz",
         "sha256": "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5"},
        {"kind": "P2_PHASE0", "sha256": "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"},
        {"kind": "FULL_RELATION_AUTHORITY", "commit": "9561723cfe0932869e781f2be27e9c80b050ad7a",
         "path": "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
         "sha256": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"},
        {"kind": "PORTABLE_EVIDENCE_MANIFEST", "path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
         "sha256": _file_identity(ROOT / "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json")["sha256"]},
        {"kind": "PORTABLE_ITEM_EVIDENCE", "path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
         "sha256": manifest["files"]["ITEM_EVIDENCE.jsonl.gz"]["sha256"]},
        {"kind": "PORTABLE_PHYSICAL_SLOTS", "path": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
         "sha256": manifest["files"]["PHYSICAL_SLOTS.jsonl.gz"]["sha256"]},
        {"kind": "PORTABLE_CODEBOOK_ROWS", "path": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
         "sha256": manifest["files"]["CODEBOOK_ROWS.jsonl.gz"]["sha256"]},
    ]


def _field_evidence(manifest: Mapping[str, Any], metadata_sha: str, metadata_path: str) -> list[dict[str, Any]]:
    meta = ExactRef("R154_PHYSICAL_METADATA", f"urn:rawlsing:r157:metadata:{metadata_path}", metadata_sha).as_dict()
    item = ExactRef("PORTABLE_ITEM_EVIDENCE", "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
                    manifest["files"]["ITEM_EVIDENCE.jsonl.gz"]["sha256"]).as_dict()
    phys = ExactRef("PORTABLE_PHYSICAL_SLOTS", "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
                    manifest["files"]["PHYSICAL_SLOTS.jsonl.gz"]["sha256"]).as_dict()
    code = ExactRef("PORTABLE_CODEBOOK_ROWS", "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
                    manifest["files"]["CODEBOOK_ROWS.jsonl.gz"]["sha256"]).as_dict()
    return [
        {"field": "identity.*", "refs": [meta, phys]},
        {"field": "physical_slots[*]", "refs": [meta, phys]},
        {"field": "items[*]", "refs": [item, code]},
        {"field": "questions[].item_evidence", "refs": [item]},
        {"field": "response_slots[]", "refs": [item, phys]},
        {"field": "coordinate_slots[]", "refs": [meta, phys]},
        {"field": "routing[].typed_state", "refs": [item]},
        {"field": "authority.snapshots", "refs": [item, phys]},
        {"field": "supported_scope", "refs": [item, phys]},
    ]


def _runtime(fixture: bool) -> dict[str, Any]:
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
            "P3_QUALIFIED_READER_TRANSPORT_CONFIGURED_NO_ENCODING_OVERRIDE"),
    }


def _base_config(source_id: str, profile: Mapping[str, Any], fixture: bool) -> tuple[dict[str, Any], dict[str, Any] | None]:
    roster = profile["roster"]
    wave = str(roster["wave"])
    original_sha = roster["source_sha256"]
    metadata_sha = roster["metadata_witness"]["sha256"]
    p = profile["profile"]
    physical = profile["physical"]
    bound = profile["bound"]
    all_items = profile["items"]
    fixture_id = f"R157-WVS-{source_id}-NONRESPONDENT" if fixture else None
    fixture_sha = None
    if fixture:
        cells = []
        for row in range(1, FIXTURE_ROWS + 1):
            for idx, item in enumerate(bound):
                name = item["source_variable_code"]
                slot = physical[name]
                positives = _positive_labels(slot)
                negatives = _negative_labels(slot)
                if row <= 4:
                    raw = positives[(row - 1) % len(positives)]
                elif row == 5:
                    raw = negatives[idx % len(negatives)] if negatives else None
                else:
                    raw = None
                cells.append({
                    "row_ordinal": row, "variable_ordinal": slot["ordinal"], "variable_name": name,
                    "raw_value": raw, "missing_state": "SYSTEM_MISSING" if raw is None else "OBSERVED_STORAGE_VALUE",
                    "source_missing_declaration": None,
                })
            for name in (p["key"], p["country"], p["time"], p["region"]):
                slot = physical[name]
                if name == p["key"]:
                    raw = float(9000 + row)
                elif name == p["country"]:
                    raw = _positive_labels(slot)[0]
                elif name == p["time"]:
                    raw = _positive_labels(slot)[0]
                else:
                    raw = _positive_labels(slot)[(row - 1) % len(_positive_labels(slot))]
                cells.append({
                    "row_ordinal": row, "variable_ordinal": slot["ordinal"], "variable_name": name,
                    "raw_value": raw, "missing_state": "OBSERVED_STORAGE_VALUE",
                    "source_missing_declaration": None,
                })
            weight_slot = physical[p["weight"]]
            weight_value = (0.75, 0.5, 2.0, 1.25, 1.5, None)[row - 1]
            cells.append({
                "row_ordinal": row, "variable_ordinal": weight_slot["ordinal"], "variable_name": weight_slot["name"],
                "raw_value": weight_value,
                "missing_state": "SYSTEM_MISSING" if weight_value is None else "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
            })
        fixture_doc = {
            "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0",
            "fixture_id": fixture_id,
            "identity_class": "NONRESPONDENT_FIXTURE",
            "nonrespondent": True,
            "row_count": FIXTURE_ROWS,
            "cells": cells,
            "expected_results": _expected(source_id, profile),
        }
        fixture_sha = fixture_document_sha256(fixture_doc)
        fixture_doc["fixture_source_sha256"] = fixture_sha

    source_bundle = semantic_hash({
        "source_id": source_id, "wave": wave, "source_sha256": original_sha,
        "metadata_witness_sha256": metadata_sha,
        "implementation_ids": [item["implementation_id"] for item in bound],
        "fixture_id": fixture_id, "fixture_sha": fixture_sha,
    })
    if fixture:
        decisions = {"source": "ALLOW", "routing": "ALLOW", "coord": "ALLOW",
                     "weight_design": "DEFER", "weight_estimand": "DEFER",
                     "projection": "ALLOW", "replay": "ALLOW"}
    else:
        decisions = {"source": "DEFER", "routing": "DEFER", "coord": "DEFER",
                     "projection": "DEFER", "replay": "ALLOW"}
    snapshots = []
    for key, kind, families, ops in (
        ("source", "SOURCE_SEMANTICS_TOPOLOGY", ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"), ("R157_WVS_SOURCE_SEMANTICS",)),
        ("routing", "ROUTING_RISK_SET", ("RoutingEligibilityFact@1.0.0",), ("R157_WVS_ROUTING",)),
        ("coord", "COORDINATE_SEMANTICS", ("EmpiricalCoordinateFact@1.0.0",), ("R157_WVS_COORDINATE",)),
        ("weight_design", "WEIGHT_DESIGN_ESTIMAND", ("WeightMeasureFact@1.0.0",), ("R157_WVS_WEIGHT_DESIGN",)),
        ("weight_estimand", "WEIGHT_DESIGN_ESTIMAND", ("WeightMeasureFact@1.0.0",), ("R157_WVS_WEIGHT_ESTIMAND",)),
        ("replay", "REPLAY_PROTOCOL", ("ReplayReceipt@1.0.0",), ("R157_NATIVE_REPLAY",)),
        ("projection", "SOURCE_SEMANTICS_TOPOLOGY", ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0"), ("R157_WVS_PROJECTION",)),
    ):
        if not fixture and key in {"weight_design", "weight_estimand"}:
            continue
        snapshots.append(_authority_snapshot(
            authority_id=f"R157-{source_id}-{key.upper()}-{'FIXTURE' if fixture else 'SOURCE'}",
            kind=kind, decision=decisions[key], source_id=source_id, original_sha=original_sha,
            wave=wave, families=families, operations=ops,
            bundle_sha=semantic_hash({"source_bundle": source_bundle, "key": key}),
            fixture_id=fixture_id, fixture_sha=fixture_sha, protocol=(key == "replay")))
    by_key = {s["authority_id"]: _authority_ref(s) for s in snapshots}
    def ar(prefix: str) -> AuthorityRef:
        return by_key[f"R157-{source_id}-{prefix}-{'FIXTURE' if fixture else 'SOURCE'}"]
    source_auth, routing_auth, coord_auth = ar("SOURCE"), ar("ROUTING"), ar("COORD")
    project_auth, replay_auth = ar("PROJECTION"), ar("REPLAY")
    required = [source_auth, routing_auth, coord_auth, project_auth, replay_auth]
    if fixture:
        required[3:3] = [ar("WEIGHT_DESIGN"), ar("WEIGHT_ESTIMAND")]
    universe = {
        "typed_state": "UNIVERSE_IDENTIFIED", "authority_snapshot_refs": [source_auth.as_dict()],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _ref(
            "REPLAY_ROOT", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:universe",
            {"source_id": source_id, "wave": wave, "source_sha256": original_sha, "fixture_id": fixture_id}).as_dict(),
        "raw_source_identity": (f"R157-NONRESPONDENT-FIXTURE:{fixture_id}" if fixture else f"WVS:{wave}:{source_id}"),
        "source_family": "WVS" if not fixture else "WVS_NONRESPONDENT_FIXTURE",
        "study_product_release": (f"R157_WVS_FIXTURE/{source_id}" if fixture else f"WVS_{wave}"),
        "instrument_release": (f"R157_WVS_FIXTURE_INSTRUMENT/{source_id}" if fixture else f"SRC{source_id[-2:]}_METADATA_WITNESS_SHA256:{metadata_sha}"),
        "country_geography": "FIXTURE_MULTI_COUNTRY" if fixture else "WVS_MULTI_COUNTRY_SOURCE_NATIVE",
        "sampling_geography": "FIXTURE_NONPROBABILITY" if fixture else "SOURCE_COUNTRY_SAMPLE_FRAME_UNRESOLVED",
        "raw_wave": wave,
        "canonical_wave_if_governed": None,
        "field_or_reference_time": "R157_NONRESPONDENT_FIXTURE" if fixture else f"WVS_{wave}",
        "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE_ROWS" if fixture else "WVS_ADULT_RESPONDENT_SAMPLE_FRAME_NOT_RECONSTRUCTED",
        "sampling_design_regime": "NONRESPONDENT_FIXTURE_ONLY" if fixture else "SOURCE_SAMPLE_DESIGN_UNRESOLVED",
        "respondent_namespace": f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:respondent",
        "source_artifact_import_lineage": ("R157_NONRESPONDENT_FIXTURE_ONLY__NOT_ORIGINAL_SOURCE" if fixture else f"R154_PHYSICAL_METADATA_SHA256:{metadata_sha}"),
        "harmonization_authority_ref": None, "source_relation_refs": [],
    }
    universe_ref = EmpiricalUniverse(**universe).ref
    questions = []
    response_slots = []
    routing = []
    for item in all_items:
        name = item["source_variable_code"]
        role = profile["roles"][name]
        slot = physical[name]
        qid = (f"FIXTURE:{source_id}:{name}" if fixture else item["p2"]["question_id"])
        top = _topology_ref(source_id, wave, original_sha, item, fixture_id)
        native_q = _ref("NATIVE_QUESTION", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:{item['implementation_id']}", {
            "source_id": source_id, "wave": wave, "source_sha256": original_sha,
            "implementation_id": item["implementation_id"], "exact_identity_sha256": item["exact_identity_sha256"],
            "source_variable_code": name, "question_text": item["p2"]["question_text"],
            "fixture_id": fixture_id})
        questions.append({
            "question_id": qid, "empirical_universe_ref": universe_ref.as_dict(),
            "native_question_ref": native_q.as_dict(), "instrument_question_version": f"WVS_{wave}",
            "canonical_question_ref_or_typed_absence": TypedAbsence("NOT_AUTHORIZED", "No exact positive canonical mapping authority; raw source identity retained.").as_dict(),
            "component_subitem_ref_or_typed_absence": TypedAbsence("NOT_APPLICABLE", "Single physical source column; no component/subitem is asserted from the column alone.").as_dict(),
            "semantic_authority_ref": source_auth.as_dict(), "topology_authority_ref": source_auth.as_dict(),
            "item_evidence": {"implementation_id": item["implementation_id"], "exact_identity_sha256": item["exact_identity_sha256"],
                              "relation_join_status": "EXACT", "question_text": item["p2"]["question_text"],
                              "source_variable_code": name, "configuration_role": role},
        })
        if role not in {"BOUND", "MULTI_CHILD"}:
            continue
        response_slots.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "question_id": qid,
            "values": _response_values(slot, item, top),
        })
        rule_material = {"source_id": source_id, "wave": wave, "source_sha256": original_sha, "question_id": qid, "fixture_id": fixture_id}
        routing.append({
            "question_id": qid, "row_selector": "ALL",
            "typed_state": "ELIGIBLE_APPLICABLE" if fixture else "ROUTING_UNKNOWN",
            "risk_set_ref": _ref("RISK_SET", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:{name}:risk-set", rule_material).as_dict(),
            "routing_rule_ref": _ref("ROUTING_RULE", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:{name}:routing-rule", rule_material).as_dict(),
            "member_set_replay_ref": _ref("MEMBER_SET_REPLAY", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:{name}:member-set", rule_material).as_dict(),
            "authority_ref": routing_auth.as_dict(), "parent_predicate_refs": [], "dependency_refs": [],
        })
    coord_names = [p["country"], p["time"], p["region"]]
    coordinates = []
    for name in coord_names:
        slot = physical[name]
        coordinates.append({
            "slot": {"ordinal": slot["ordinal"], "name": name},
            "native_coordinate_ref": _ref("COORDINATE_NATIVE", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:coordinate:{name}", {
                "source_id": source_id, "wave": wave, "source_sha256": original_sha, "name": name, "fixture_id": fixture_id}).as_dict(),
            "unit_taxonomy_ref": _ref("UNIT_TAXONOMY", f"urn:rawlsing:r157:unit:wvs_{name.lower()}", {"unit": name, "source_native": True}).as_dict(),
            "effective_time": "R157_NONRESPONDENT_FIXTURE" if fixture else f"WVS_{wave}",
            "source_semantic_authority_ref": coord_auth.as_dict(),
            "canonical_coordinate_ref": None, "normalization_ref": None,
            "values": [], "copy_observed_raw": True,
        })
    weight_slots = []
    if fixture:
        weight_slot = physical[p["weight"]]
        weight_values = []
        for row in range(1, FIXTURE_ROWS + 1):
            val = (0.75, 0.5, 2.0, 1.25, 1.5, None)[row - 1]
            weight_values.append({
                "raw_value": val, "missing_state": "SYSTEM_MISSING" if val is None else "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
                "exact_value": None if val is None else (str(int(val)) if val == int(val) else repr(val)),
                "state": "WEIGHT_MISSING" if val is None else "WEIGHT_BASIS_UNRESOLVED",
            })
        weight_slots = [{
            "slot": {"ordinal": weight_slot["ordinal"], "name": weight_slot["name"]},
            "weight_basis_id": f"WVS_{weight_slot['name']}_SOURCE_NATIVE_WEIGHT",
            "weight_source_ref": _ref("WEIGHT_SOURCE", f"urn:rawlsing:r157:fixture:{fixture_id}:weight", {"source_id": source_id, "name": weight_slot["name"], "metadata_sha": metadata_sha}).as_dict(),
            "design_authority_ref": ar("WEIGHT_DESIGN").as_dict(),
            "estimand_authority_ref": ar("WEIGHT_ESTIMAND").as_dict(),
            "effective_scope_ref": _ref("WEIGHT_EFFECTIVE_SCOPE", f"urn:rawlsing:r157:fixture:{fixture_id}:scope", {"fixture_id": fixture_id}).as_dict(),
            "normalization_ref": None, "values": weight_values,
            "copy_observed_numeric": False, "extra_authority_refs": [],
        }]
    if fixture:
        physical_payloads = [
            _physical_payload(slot, "KEY" if slot["name"] == p["key"] else profile["roles"][slot["name"]])
            for slot in profile["physical_rows"]
            if slot["name"] in set([item["source_variable_code"] for item in bound] + coord_names + [p["key"], p["weight"]])
        ]
        item_payloads = [_item_payload(item, profile["roles"][item["source_variable_code"]]) for item in bound]
    else:
        physical_payloads = [_physical_payload(slot, profile["roles"][slot["name"]]) for slot in profile["physical_rows"]]
        item_payloads = [_item_payload(item, profile["roles"][item["source_variable_code"]]) for item in all_items]
    all_ordinals = [slot["ordinal"] for slot in profile["physical_rows"]]
    included_ordinals = sorted(all_ordinals if not fixture else
                               [slot["ordinal"] for slot in physical_payloads])
    included_items = [item["implementation_id"] for item in (bound if fixture else all_items)]
    held_items = [{
        "implementation_id": item["implementation_id"], "source_variable_code": item["source_variable_code"],
        "physical_slot": {"ordinal": physical[item["source_variable_code"]]["ordinal"], "name": item["source_variable_code"]},
        "configuration_role": profile["roles"][item["source_variable_code"]],
        "source_disposition": item["p2"]["canonical_disposition"],
        "native_field": HELD_ROLE_REASON.get(profile["roles"][item["source_variable_code"]], ("", "questions[].response_slots", ""))[1],
        "reason": HELD_ROLE_REASON.get(profile["roles"][item["source_variable_code"]], ("Source role retained without response promotion.",))[0],
        "evidence_refs": _evidence_refs(item),
    } for item in profile["held"]]
    residuals = _residuals(source_id, wave, profile, profile["held_by_role"])
    if fixture:
        residuals = [{
            "residual_id": f"{source_id}-FIXTURE-IDENTITY", "scope": f"{source_id}/fixture",
            "field": "binding.identity_class", "status": "FIXTURE_ONLY",
            "reason": "Fixture bytes, universe, authority and row identities are distinct from original source and are not promoted.",
            "dependent_operation": "original-source use", "unaffected_scope": "actual factory/native validation",
            "owner": "R157 WVS lane author", "next_step": "Use the original config only with permitted original bytes and decoded row keys.",
        }, {
            "residual_id": f"{source_id}-FIXTURE-WEIGHT", "scope": f"{source_id}/weight",
            "field": "weight_slots[].weight_basis_id", "status": "WEIGHT_BASIS_UNRESOLVED",
            "reason": "Fixture exercises explicit numeric weight cells; no weighted design/estimand claim is made.",
            "dependent_operation": "weighted inference", "unaffected_scope": "fixture response/coordinate validation",
            "owner": "R157 WVS lane author", "next_step": "Establish design/estimand before weighted scope.",
        }]
    config_id = f"R157-WVS-{source_id}-{'NONRESPONDENT-FIXTURE' if fixture else 'ORIGINAL-SOURCE'}"
    doc = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0", "config_id": config_id, "config_revision": 1,
        "config_purpose": "NONRESPONDENT_FIXTURE" if fixture else "SOURCE_PREPARATION",
        "identity": {
            "source_id": source_id, "family": roster["family"], "wave": wave, "source_family_id": "WVS",
            "study_product_id": f"WVS_{wave}", "release_id": f"WVS_{wave}_SOURCE_ARTIFACT",
            "instrument_release_id": f"SRC{source_id[-2:]}_METADATA_WITNESS_SHA256:{metadata_sha}",
            "source_artifact_id": roster["source_artifact_id"], "expected_source_sha256": original_sha,
            "source_format": roster["format"], "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"], "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"], "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": ExactRef("SOURCE_SNAPSHOT", f"urn:rawlsing:r157:source-snapshot:{source_id}", original_sha).as_dict(),
            "metadata_witness_ref": ExactRef("R154_PHYSICAL_METADATA", f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}", metadata_sha).as_dict(),
            "locator": {"root": "EXTERNAL_LOCATOR_ID", "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING"},
            "reader": {"decoder_owner": "rawlsing_next.pre553_physical_decoder.decode_sav",
                       "configuration_ref": _ref("READER_CONFIGURATION", f"urn:rawlsing:r157:reader:{source_id}:default_sav", {"source_id": source_id, "decoder": "decode_sav", "encoding": None, "source_sha256": original_sha}).as_dict(),
                       "encoding": None},
        },
        "binding": {
            "identity_class": "NONRESPONDENT_FIXTURE" if fixture else "ORIGINAL_SOURCE",
            "source_sha256": fixture_sha if fixture else original_sha,
            "row_count": FIXTURE_ROWS if fixture else roster["rows"],
            "source_snapshot_ref": ExactRef("FIXTURE_SNAPSHOT" if fixture else "SOURCE_SNAPSHOT",
                                            f"urn:rawlsing:r157:{'fixture' if fixture else 'source-snapshot'}:{fixture_id or source_id}",
                                            fixture_sha if fixture else original_sha).as_dict(),
        },
        "authority": {
            "snapshots": snapshots, "required_refs": [x.as_dict() for x in required],
            "projection_authority_ref": project_auth.as_dict(), "replay_authority_ref": replay_auth.as_dict(),
            "projection_identity_ref": _ref("C11_SEMANTIC_PROJECTION", f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:projection", {"config_id": config_id, "source_id": source_id, "source_sha256": original_sha, "fixture_id": fixture_id}).as_dict(),
            "tie_order_ref": _ref("ORDER_RULE", "urn:rawlsing:r157:order:canonical-exact-ref", {"rule": "CANONICAL_REF_SORT"}).as_dict(),
            "replay_protocol_version": "1.0.0",
        },
        "universe": {"universes": [universe]},
        "respondents": {
            "subject_unit": "NONRESPONDENT_FIXTURE_ROW" if fixture else "WVS_RESPONDENT_ROW",
            "respondent_namespace": f"urn:rawlsing:r157:{'fixture' if fixture else 'source'}:{source_id}:respondent",
            "respondent_key_pattern": (f"R157-FIXTURE-{source_id}-ROW-{{row_ordinal:02d}}" if fixture else f"{source_id}-ROW-{{row_ordinal:06d}}"),
            "source_native_key_slot": {"ordinal": physical[p["key"]]["ordinal"], "name": p["key"]},
            "identity_map_authority_ref": None,
            "row_identity_grade": "NONRESPONDENT_FIXTURE_KEY_EXTRACTION_ONLY" if fixture else "SOURCE_NATIVE_KEY_SLOT_DECLARED_VALUE_DECODE_REQUIRED",
        },
        "questions": questions, "physical_slots": physical_payloads, "items": item_payloads,
        "response_slots": response_slots, "coordinate_slots": coordinates, "weight_slots": weight_slots,
        "routing": routing, "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {"predicate": TypedAbsence("NOT_APPLICABLE").as_dict(), "comparator": TypedAbsence("DEFERRED").as_dict(),
                   "discovery": TypedAbsence("DEFERRED").as_dict(), "structural": TypedAbsence("NOT_APPLICABLE").as_dict()},
        "supported_scope": {
            "scope_id": f"{source_id}-WVS-{'FIXTURE' if fixture else 'RESPONSE'}-SCOPE",
            "purpose": "NONRESPONDENT_FIXTURE_VALIDATION" if fixture else "SOURCE_PREPARATION",
            "declared_supported": True,
            "supported_question_ids": [f"FIXTURE:{source_id}:{item['source_variable_code']}" for item in bound] if fixture else [item["p2"]["question_id"] for item in bound],
            "native_validation_expectation": "POSITIVE_RELEASE" if fixture else "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": "NONRESPONDENT_FIXTURE_ROWS" if fixture else "WVS_RESPONDENT_ROW_SOURCE_LOCAL",
            "supported_form_slice": "SINGLE_OBSERVATION_PER_FIXTURE_ROW_ALL_BOUND_RULES" if fixture else "SINGLE_OBSERVATION_PER_RESPONDENT_FORM_ASSIGNMENT_UNKNOWN",
            "notes": ["Original WVS respondent execution is NOT performed or claimed.",
                      "Fixture identity/authority are distinct from original source identity.",
                      "Multiselect child columns are single-column bindings only; set aggregation/components are not invented.",
                      "Ranked-choice items without exact rank maps are held."],
        },
        "coverage": {
            "physical_slots_total": roster["physical_columns"], "items_total": roster["original_items"],
            "physical_slots_included": included_ordinals, "physical_slots_excluded": [],
            "items_included": included_items, "items_excluded": [],
            "partial_scope_reason": "All items/slots are serialized; bound response rules cover every supported finite item, held roles are exact in exceptions.",
        },
        "residuals": residuals,
        "evidence": {"source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
                     "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
                     "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
                     "pinned_inputs": _pinned_inputs(),
                     "field_evidence": _field_evidence(load_manifest(), metadata_sha, roster["metadata_witness"]["path"]),
                     "limits": ["H48/P2/full-relation grades and limits are copied, not promoted.",
                                "No original respondent source byte was read.",
                                "Fixture authority is not original-source authority.",
                                "No cross-country canonicalization, weights or population claim is made."]},
        "runtime": _runtime(fixture),
        "notes": [f"WVS {wave} source-local preparation; all items/slots are serialized.",
                  "No original respondent file or source value was read."],
    }
    if fixture:
        doc["coverage"]["partial_scope_reason"] = "Nonrespondent fixture exercises all bound source rules plus country/time/region coordinates and unresolved-basis weight facts."
    return doc, fixture_doc if fixture else None


def _expected(source_id: str, profile: Mapping[str, Any]) -> dict[str, Any]:
    bound = profile["bound"]
    by_q = {f"FIXTURE:{source_id}:{item['source_variable_code']}": {} for item in bound}
    states = Counter()
    for row in range(1, FIXTURE_ROWS + 1):
        for idx, item in enumerate(bound):
            name = item["source_variable_code"]
            slot = profile["physical"][name]
            positives = _positive_labels(slot)
            negatives = _negative_labels(slot)
            if row <= 4:
                raw = positives[(row - 1) % len(positives)]
            elif row == 5:
                raw = negatives[idx % len(negatives)] if negatives else None
            else:
                raw = None
            state = "MISSING" if raw is None else _response_state(slot, float(raw))
            states[state] += 1
            by_q[f"FIXTURE:{source_id}:{name}"][state] = by_q[f"FIXTURE:{source_id}:{name}"].get(state, 0) + 1
    return {
        "fixture_only": True, "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "response_event_count": FIXTURE_ROWS * len(bound),
        "coordinate_fact_count": FIXTURE_ROWS * 3, "routing_fact_count": FIXTURE_ROWS * len(bound),
        "weight_fact_count": FIXTURE_ROWS,
        "response_state_counts": dict(sorted(states.items())),
        "response_state_counts_by_question": {k: dict(sorted(v.items())) for k, v in by_q.items()},
        "coordinate_state_counts": {"OBSERVED_COORDINATE": FIXTURE_ROWS * 3},
        "weight_state_counts": {"WEIGHT_BASIS_UNRESOLVED": 5, "WEIGHT_MISSING": 1},
        "canonical_values": [None] * (FIXTURE_ROWS * len(bound)),
        "source_relation_section": "DISTINCT_BY_DEFAULT",
    }


def _native_validation(source_id: str, fixture_cfg_path: Path, original_cfg_path: Path) -> dict[str, Any]:
    original_cfg = load_source_config(original_cfg_path)
    fixture_cfg = load_source_config(fixture_cfg_path)
    stream = load_fixture_stream(fixture_cfg_path.parent / f"{source_id}.fixture.json")
    fixture_doc = _read(fixture_cfg_path.parent / f"{source_id}.fixture.json")
    keys = row_native_keys_from_transport(fixture_cfg, stream=stream)
    projection = build_governed_c11_projection(fixture_cfg, row_native_keys=keys)
    release = build_validated_c11_release_from_config(fixture_cfg, stream=stream)
    repo, repo_release = build_source_backed_c11_repository_from_config(fixture_cfg, stream)
    reader = reader_configuration_from_config(original_cfg)
    request = source_read_request_from_config(original_cfg, host="R157_PREPARATION_HOST",
                                              purpose="SOURCE_CONFIGURATION_PREPARATION",
                                              consumer_use="R157_WVS_LANE_CONFIGURATION",
                                              semantic_use_scope=("response_rule_configuration", "coordinate_configuration"))
    events = [o for o in release.public_objects if isinstance(o, RespondentEvent)]
    coords = [o for o in release.public_objects if isinstance(o, EmpiricalCoordinateFact)]
    weights = [o for o in release.public_objects if isinstance(o, WeightMeasureFact)]
    auths = [o for o in release.public_objects if isinstance(o, AuthoritySnapshot)]
    qmap = {}
    for q in fixture_cfg.document["questions"]:
        r = q["native_question_ref"]
        qmap[f"{r['kind']}|{r['object_id']}|{r['content_hash']}"] = q["question_id"]
    by_q = {}
    for e in events:
        r = e.native_question_ref
        by_q.setdefault(qmap[f"{r['kind']}|{r['object_id']}|{r['content_hash']}"], Counter())[e.response_state] += 1
    expected = fixture_doc["expected_results"]
    actual = {
        "response_state_counts": dict(sorted(Counter(e.response_state for e in events).items())),
        "response_state_counts_by_question": {k: dict(sorted(v.items())) for k, v in sorted(by_q.items())},
        "coordinate_state_counts": dict(sorted(Counter(c.coordinate_state for c in coords).items())),
        "weight_state_counts": dict(sorted(Counter(w.weight_state for w in weights).items())),
        "canonical_response_values_all_null": all(e.canonical_response_value_if_authorized is None for e in events),
    }
    match = (
        len(events) == expected["response_event_count"]
        and len(coords) == expected["coordinate_fact_count"]
        and len(weights) == expected["weight_fact_count"]
        and actual["response_state_counts"] == expected["response_state_counts"]
        and actual["response_state_counts_by_question"] == expected["response_state_counts_by_question"]
        and actual["coordinate_state_counts"] == expected["coordinate_state_counts"]
        and actual["weight_state_counts"] == expected["weight_state_counts"]
        and actual["canonical_response_values_all_null"]
    )
    if not match:
        raise RuntimeError(f"{source_id} native fixture results differ from oracle")
    refusals = {}
    for label, fn in (
        ("original_without_row_keys", lambda: build_governed_c11_projection(original_cfg)),
        ("original_with_fixture_stream", lambda: build_validated_c11_release_from_config(original_cfg, stream=stream)),
        ("fixture_wrong_source_sha", lambda: build_validated_c11_release_from_config(
            fixture_cfg, stream=ExactPhysicalCellStream("f" * 64, stream.row_count, stream.iter_cells))),
        ("fixture_wrong_row_count", lambda: build_validated_c11_release_from_config(
            fixture_cfg, stream=ExactPhysicalCellStream(stream.source_sha256, stream.row_count - 1, stream.iter_cells))),
    ):
        try:
            fn()
        except Exception as exc:
            refusals[label] = {"outcome": "REFUSED", "exception_type": type(exc).__name__, "message": str(exc)}
        else:
            raise RuntimeError(f"{label} unexpectedly accepted")
    return {
        "projection": {"type": type(projection).__name__, "projection_identity_ref": projection.projection_identity_ref.as_dict(),
                       "expected_source_sha256": projection.expected_source_sha256, "respondents": len(projection.respondents),
                       "questions": len(projection.questions), "response_slots": len(projection.response_slots),
                       "coordinate_slots": len(projection.coordinate_slots), "weight_slots": len(projection.weight_slots),
                       "routing_facts": len(projection.routing), "authority_snapshots": len(projection.authority_snapshots)},
        "release": {"type": type(release).__name__, "release_id": release.release_id, "release_ref": release.release_ref.as_dict(),
                    "semantic_release_hash": release.semantic_release_hash, "source_artifact_ref": release.source_artifact_ref.as_dict(),
                    "m01_m18_coverage": {k: list(v) for k, v in release.m01_m18_coverage.items()},
                    "universes": sum(isinstance(o, EmpiricalUniverse) for o in release.public_objects),
                    "respondent_events": len(events), "coordinate_facts": len(coords),
                    "weight_facts": len(weights), "authority_snapshots": len(auths)},
        "actual": actual, "expected_match": match,
        "p3_row_native_keys": {"configured_slot": fixture_cfg.document["respondents"]["source_native_key_slot"],
                               "witness_count": len(keys), "kinds": sorted({type(v).__name__ for v in keys.values()}),
                               "all_witnesses_fixture_bound": all(v.kind == "R157_NONRESPONDENT_FIXTURE_KEY" for v in keys.values())},
        "p3_reader_transport": {"reader_configuration": {"source_sha256": reader.source_sha256, "configuration_ref": reader.configuration_ref.as_dict(),
                                                          "encoding": reader.encoding, "authority_status": reader.authority_status},
                                "source_read_request": {"source_id": request.source_id, "source_sha256": request.source_sha256,
                                                        "source_format": request.source_format, "custody_locator_binding": request.custody_locator_binding,
                                                        "host": request.host, "purpose": request.purpose, "consumer_use": request.consumer_use,
                                                        "semantic_use_scope": list(request.semantic_use_scope)},
                                "source_bytes_read": False, "permission_decision": "NOT_REQUESTED_OR_EVALUATED_IN_PREPARATION"},
        "calls": [
            {"call": "row_native_keys_from_transport(fixture_config, stream=fixture_stream)", "result": "PASS", "witness_count": len(keys)},
            {"call": "build_governed_c11_projection(fixture_config, row_native_keys=fixture_keys)", "result": "PASS"},
            {"call": "build_validated_c11_release_from_config(fixture_config, stream=fixture_stream)", "result": "PASS", "release_ref": release.release_ref.as_dict()},
            {"call": "build_source_backed_c11_repository_from_config(fixture_config, stream=fixture_stream)", "result": "PASS", "release_refs": [r.as_dict() for r in repo.release_refs]},
            {"call": "reader_configuration_from_config(original_config)", "result": "PASS", "encoding": reader.encoding, "source_bytes_read": False},
            {"call": "source_read_request_from_config(original_config)", "result": "PASS", "source_bytes_read": False},
        ],
        "repository": {"release_refs": [r.as_dict() for r in repo.release_refs], "release_ref_matches_stream": repo_release.release_ref.as_dict() == release.release_ref.as_dict()},
        "refusals": refusals,
    }


def _build_one(source_id: str) -> dict[str, Any]:
    profile = _source_profiles(source_id)
    original_doc, _ = _base_config(source_id, profile, False)
    validate_source_config(original_doc)
    fixture_doc, fixture_bytes = _base_config(source_id, profile, True)
    # fixture config uses the fixture byte identity and provenance
    fixture_doc["binding"]["fixture_provenance"] = {
        "fixture_id": fixture_bytes["fixture_id"], "provenance": "Repository-generated nonrespondent WVS lane fixture; synthetic cells, no original respondents represented.",
        "authority_grade": "NONRESPONDENT_FIXTURE_ONLY", "original_source_id": source_id,
        "original_source_sha256": profile["roster"]["source_sha256"], "no_original_respondents": True,
        "fixture_study_product_id": f"R157_WVS_FIXTURE/{source_id}",
        "fixture_release_id": f"R157_WVS_FIXTURE_RELEASE/{source_id}",
        "fixture_instrument_release_id": f"R157_WVS_FIXTURE_INSTRUMENT/{source_id}",
    }
    validate_source_config(fixture_doc)
    data_dir, val_dir = DATA_ROOT / source_id, VALIDATION_ROOT / source_id
    original_path = data_dir / f"{source_id}.source.config.json"
    accounting_path = data_dir / f"{source_id}.evidence-accounting.json"
    fixture_cfg_path = val_dir / f"{source_id}.fixture.config.json"
    fixture_path = val_dir / f"{source_id}.fixture.json"
    spec_path = val_dir / f"{source_id}.fixture-spec.json"
    results_path = val_dir / f"{source_id}.validation-results.json"
    exceptions_path = val_dir / f"{source_id}.exceptions.json"
    manifest_path = val_dir / f"{source_id}.manifest.json"
    _json_write(original_path, original_doc)
    _json_write(fixture_cfg_path, fixture_doc)
    _json_write(fixture_path, fixture_bytes)
    _json_write(spec_path, {
        "schema": "PYAT_R157_WVS_FIXTURE_SPEC@1.0.0", "source_id": source_id,
        "fixture_id": fixture_bytes["fixture_id"], "fixture_path": str(fixture_path.relative_to(ROOT)),
        "fixture_file_sha256": config_file_sha256(fixture_path), "fixture_source_sha256": fixture_bytes["fixture_source_sha256"],
        "fixture_config_path": str(fixture_cfg_path.relative_to(ROOT)),
        "fixture_config_canonical_sha256": canonical_config_hash(fixture_doc), "fixture_config_file_sha256": config_file_sha256(fixture_cfg_path),
        "original_source_id": source_id, "original_source_sha256": profile["roster"]["source_sha256"],
        "identity_class": "NONRESPONDENT_FIXTURE", "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "row_count": FIXTURE_ROWS, "expected_results": fixture_bytes["expected_results"],
        "oracle_basis": "Expected counts/states are derived from fixture cells and serialized source response rules before the native call.",
        "limits": ["Synthetic nonrespondent fixture cells; no original respondent represented.", "Fixture authority/SHA are not original-source meaning."],
    })
    native = _native_validation(source_id, fixture_cfg_path, original_path)
    bound = profile["bound"]
    original_hash = canonical_config_hash(original_doc)
    fixture_hash = canonical_config_hash(fixture_doc)
    results = {
        "schema": "PYAT_R157_WVS_SOURCE_VALIDATION_RESULTS@1.0.0", "plan_seal": PLAN_SEAL,
        "p0_correction_consumed": P0_CORRECTION, "p3_terminal_runtime_consumed": P3_RUNTIME, "source_id": source_id,
        "source_format": profile["roster"]["format"], "wave": str(profile["roster"]["wave"]),
        "commands": ["PYTHONPATH=. python3 source_pre553_validation/SRC33/build_wvs_lane.py --all",
                     "PYTHONPATH=. python3 -m pytest source_pre553_validation/SRC33/test_wvs_lane.py -q -o addopts=''"],
        "config_validation": {"validator": "rawlsing_next.source_configuration.schema.validate_source_config",
                              "original_path": str(original_path.relative_to(ROOT)), "original_config_canonical_sha256": original_hash,
                              "original_config_file_sha256": config_file_sha256(original_path), "fixture_path": str(fixture_cfg_path.relative_to(ROOT)),
                              "fixture_config_canonical_sha256": fixture_hash, "fixture_config_file_sha256": config_file_sha256(fixture_cfg_path), "passed": True},
        "coverage": {"physical_slots_total": profile["roster"]["physical_columns"], "original_items_total": profile["roster"]["original_items"],
                     "physical_slots_serialized": len(original_doc["physical_slots"]), "items_serialized": len(original_doc["items"]),
                     "physical_slots_included": len(original_doc["coverage"]["physical_slots_included"]), "items_included": len(original_doc["coverage"]["items_included"]),
                     "physical_slots_excluded": 0, "items_excluded": 0, "response_bound_items": len(bound), "held_items": len(profile["held"]),
                     "held_by_role": {k: len(v) for k, v in sorted(profile["held_by_role"].items())},
                     "no_drop": len(original_doc["physical_slots"]) == profile["roster"]["physical_columns"] and len(original_doc["items"]) == profile["roster"]["original_items"],
                     "supported_question_ids": [item["p2"]["question_id"] for item in bound]},
        "native_validation": native,
        "identity_separation": {"original_source_sha256": profile["roster"]["source_sha256"], "fixture_source_sha256": fixture_bytes["fixture_source_sha256"],
                                "distinct_bytes": profile["roster"]["source_sha256"] != fixture_bytes["fixture_source_sha256"],
                                "original_binding_identity_class": original_doc["binding"]["identity_class"], "fixture_binding_identity_class": fixture_doc["binding"]["identity_class"],
                                "original_authority_has_fixture_only": any(s["scope_envelope"].get("fixture_only") is True for s in original_doc["authority"]["snapshots"]),
                                "fixture_authority_all_fixture_only": all(s["scope_envelope"].get("fixture_only") is True and s["scope_envelope"].get("grade") == "NONRESPONDENT_FIXTURE_ONLY" for s in fixture_doc["authority"]["snapshots"]),
                                "original_binding_matches_original_sha": original_doc["binding"]["source_sha256"] == original_doc["identity"]["expected_source_sha256"],
                                "fixture_binding_differs_from_original_sha": fixture_doc["binding"]["source_sha256"] != fixture_doc["identity"]["expected_source_sha256"]},
        "residuals": original_doc["residuals"],
        "limits": ["Original WVS respondent execution is NOT performed or claimed.", "Positive native release is from a distinct nonrespondent fixture.",
                   "Original construction requires permitted decoded row keys and remains P3/source-read work.", "No cross-country canonicalization, weight authorization or population claim is asserted."],
    }
    _json_write(results_path, results)
    _json_write(exceptions_path, {
        "schema": "PYAT_R157_WVS_EXCEPTION_LEDGER@1.0.0", "source_id": source_id,
        "source_config": str(original_path.relative_to(ROOT)), "residual_count": len(original_doc["residuals"]),
        "residuals": original_doc["residuals"], "bound_item_count": len(bound), "held_item_count": len(profile["held"]),
        "held_by_role_counts": {k: len(v) for k, v in sorted(profile["held_by_role"].items())},
        "held_items": [{
            "implementation_id": item["implementation_id"], "source_variable_code": item["source_variable_code"],
            "physical_slot": {"ordinal": profile["physical"][item["source_variable_code"]]["ordinal"], "name": item["source_variable_code"]},
            "configuration_role": profile["roles"][item["source_variable_code"]], "source_disposition": item["p2"]["canonical_disposition"],
            "native_field": HELD_ROLE_REASON.get(profile["roles"][item["source_variable_code"]], ("", "questions[].response_slots", ""))[1],
            "reason": HELD_ROLE_REASON.get(profile["roles"][item["source_variable_code"]], ("Source role retained without response promotion.",))[0],
            "evidence_refs": _evidence_refs(item),
        } for item in profile["held"]],
        "fixture_limits": fixture_doc["residuals"], "blocking_lane_completion": False, "blocking_original_execution": True,
        "exact_next_operation": "P3 integration owner transports the qualified reader config and supplies permitted decoded source incidence for original execution.",
    })
    manifest = load_manifest()
    _json_write(accounting_path, {
        "schema": "PYAT_R157_WVS_EVIDENCE_ACCOUNTING@1.0.0", "source_id": source_id,
        "source_paths": {"source_config": str(original_path.relative_to(ROOT)), "fixture_config": str(fixture_cfg_path.relative_to(ROOT)),
                         "fixture": str(fixture_path.relative_to(ROOT)), "fixture_spec": str(spec_path.relative_to(ROOT)),
                         "validation_results": str(results_path.relative_to(ROOT)), "exceptions": str(exceptions_path.relative_to(ROOT))},
        "counts": {"physical_columns": profile["roster"]["physical_columns"], "codebook_rows": profile["roster"]["codebook_rows"],
                   "original_items": profile["roster"]["original_items"], "exact_relation_matches": profile["roster"]["exact_relation_matches"],
                   "response_bound_items": len(bound), "held_items": len(profile["held"]), "held_by_role_counts": {k: len(v) for k, v in sorted(profile["held_by_role"].items())}},
        "bound_items": [{"source_variable_code": item["source_variable_code"], "implementation_id": item["implementation_id"],
                         "exact_identity_sha256": item["exact_identity_sha256"], "p2_question_id": item["p2"]["question_id"],
                         "relation_question_id": item["relation"]["question_id"], "h48_binding_grade": item["h48"]["binding_grade"],
                         "relation_authority_status": item["relation"]["authority_status"], "mapping_status": item["relation"]["mapping_status"],
                         "evidence_refs": _evidence_refs(item)} for item in bound],
        "held_items": [{"source_variable_code": item["source_variable_code"], "implementation_id": item["implementation_id"],
                        "configuration_role": profile["roles"][item["source_variable_code"]], "source_disposition": item["p2"]["canonical_disposition"],
                        "evidence_refs": _evidence_refs(item)} for item in profile["held"]],
        "all_items_accounted": len(original_doc["items"]) == profile["roster"]["original_items"],
        "all_physical_slots_accounted": len(original_doc["physical_slots"]) == profile["roster"]["physical_columns"],
        "excluded_item_count": 0, "excluded_slot_count": 0,
        "weight_slot": {"ordinal": profile["physical"][profile["profile"]["weight"]]["ordinal"], "name": profile["profile"]["weight"], "status": "HELD_WEIGHT_DESIGN_UNRESOLVED"},
        "evidence_inputs": {"source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
                            "source_roster_sha256": _file_identity(ROOT / "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json")["sha256"],
                            "item_evidence_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
                            "item_evidence_sha256": manifest["files"]["ITEM_EVIDENCE.jsonl.gz"]["sha256"],
                            "physical_slots_path": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
                            "physical_slots_sha256": manifest["files"]["PHYSICAL_SLOTS.jsonl.gz"]["sha256"],
                            "codebook_rows_path": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
                            "codebook_rows_sha256": manifest["files"]["CODEBOOK_ROWS.jsonl.gz"]["sha256"]},
        "limits": ["No original respondent row or source byte was read.", "Evidence grades/limits are copied, not promoted.",
                   "Fixture is a separate nonrespondent identity and source-specific rule exercise."],
    })
    manifest_doc = {
        "schema": "PYAT_R157_WVS_SOURCE_MANIFEST@1.0.0", "source_id": source_id,
        "paths": {"source_config": _file_identity(original_path), "evidence_accounting": _file_identity(accounting_path),
                  "fixture_config": _file_identity(fixture_cfg_path), "fixture": _file_identity(fixture_path),
                  "fixture_spec": _file_identity(spec_path), "validation_results": _file_identity(results_path), "exceptions": _file_identity(exceptions_path)},
        "config_hashes": {"original_config_canonical_sha256": original_hash, "original_config_file_sha256": config_file_sha256(original_path),
                          "fixture_config_canonical_sha256": fixture_hash, "fixture_config_file_sha256": config_file_sha256(fixture_cfg_path),
                          "fixture_source_sha256": fixture_bytes["fixture_source_sha256"]},
        "native_release_ref": native["release"]["release_ref"], "no_drop": results["coverage"]["no_drop"], "limits": results["limits"],
    }
    _json_write(manifest_path, manifest_doc)
    return {"source_id": source_id, "manifest": manifest_doc, "results": results}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=SOURCE_IDS, action="append")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)
    ids = list(SOURCE_IDS) if args.all or not args.source else list(args.source)
    outputs = [_build_one(sid) for sid in ids]
    print(json.dumps([{"source_id": o["source_id"], "native": o["results"]["native_validation"]["release"]["release_ref"],
                       "no_drop": o["results"]["coverage"]["no_drop"]} for o in outputs], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
