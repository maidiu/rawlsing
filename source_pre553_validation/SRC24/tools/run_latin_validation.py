"""Exercise the frozen R157 factory/native C11 validator for the LATIN lane.

This script performs only nonrespondent fixture native releases.  It builds the
ORIGINAL_SOURCE projection (no respondent/value witnesses are pre-invented) and
keeps the original and fixture identities separate.  It does not read any
original source stream and does not issue an original workload.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_c11_integrity import RespondentEvent, RoutingEligibilityFact  # noqa: E402
from rawlsing_next.pre553_empirical_objects import EmpiricalCoordinateFact, exact_ref  # noqa: E402
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec  # noqa: E402
from rawlsing_next.source_configuration.factory import (  # noqa: E402
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream  # noqa: E402
from rawlsing_next.source_configuration.schema import (  # noqa: E402
    canonical_config_hash,
    load_source_config,
)
CODEC = R5TypedValueCodec()
SOURCE_IDS = ("SRC24", "SRC25", "SRC26")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_raw_witness(witness: Any) -> Any:
    if not isinstance(witness, Mapping):
        raise AssertionError("raw witness is not a mapping")
    material = witness["$raw_physical_value"]
    return CODEC.decode(material["token"])


def slot_from_event(event: RespondentEvent) -> str:
    if event.component_or_subitem_ref is not None:
        object_id = exact_ref(event.component_or_subitem_ref).object_id
        return object_id.rsplit(":", 1)[-1]
    object_id = exact_ref(event.response_topology_ref).object_id
    # urn:rawlsing:r157:topology:<source>:<slot>:<topology>
    parts = object_id.split(":")
    return parts[-2]


def run_source(source_id: str) -> dict[str, Any]:
    data_dir = ROOT / "rawlsing_next/source_configuration/data" / source_id
    val_dir = ROOT / "source_pre553_validation" / source_id
    original_path = data_dir / "source.config.json"
    crosswalk_path = data_dir / "crosswalk.json"
    field_evidence_path = data_dir / "field_evidence.json"
    fixture_path = val_dir / "fixture.json"
    fixture_config_path = val_dir / "fixture.config.json"
    oracle_path = val_dir / "fixture_oracle.json"
    manifest_path = val_dir / "manifest.json"

    result: dict[str, Any] = {
        "source_id": source_id,
        "status": "RUNNING",
        "calls": [],
        "checks": [],
        "failures": [],
        "skips": [],
        "paths": {
            "original_config": str(original_path.relative_to(ROOT)),
            "crosswalk": str(crosswalk_path.relative_to(ROOT)),
            "field_evidence": str(field_evidence_path.relative_to(ROOT)),
            "fixture_config": str(fixture_config_path.relative_to(ROOT)),
            "fixture": str(fixture_path.relative_to(ROOT)),
            "fixture_oracle": str(oracle_path.relative_to(ROOT)),
            "manifest": str(manifest_path.relative_to(ROOT)),
        },
        "hashes": {},
    }
    for name, path in (("original_config_file", original_path),
                       ("crosswalk_file", crosswalk_path),
                       ("field_evidence_file", field_evidence_path),
                       ("fixture_config_file", fixture_config_path),
                       ("fixture_file", fixture_path),
                       ("fixture_oracle_file", oracle_path)):
        result["hashes"][name] = file_sha(path)

    original = load_source_config(original_path)
    fixture_config = load_source_config(fixture_config_path)
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    fixture_doc = json.loads(fixture_path.read_text(encoding="utf-8"))
    result["hashes"]["original_config_canonical"] = canonical_config_hash(original)
    result["hashes"]["fixture_config_canonical"] = canonical_config_hash(fixture_config)
    result["hashes"]["fixture_source"] = fixture_doc["fixture_source_sha256"]

    # ---- original-source projection construction (no stream/values read) ----
    original_projection = build_governed_c11_projection(original)
    result["calls"].append({
        "call": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
        "input": "ORIGINAL_SOURCE config (no physical stream)",
        "config_id": original.config_id,
        "config_sha256": result["hashes"]["original_config_canonical"],
        "result": "GovernedC11Projection",
        "source_sha256": original_projection.expected_source_sha256,
        "respondents": len(original_projection.respondents),
        "response_slots": len(original_projection.response_slots),
        "coordinate_slots": len(original_projection.coordinate_slots),
        "routing_facts": len(original_projection.routing),
        "questions": len(original_projection.questions),
        "authority_snapshots": len(original_projection.authority_snapshots),
    })
    result["checks"].extend([
        {
            "check": "original_identity_is_original_source",
            "pass": original_projection.expected_source_sha256 == original.original_source_sha256,
            "actual": original_projection.expected_source_sha256,
            "expected": original.original_source_sha256,
        },
        {
            "check": "original_has_no_fixture_provenance",
            "pass": original.fixture_provenance is None,
            "actual": original.fixture_provenance,
            "expected": None,
        },
        {
            "check": "original_respondent_rows_match_source",
            "pass": len(original_projection.respondents) == original.active_row_count,
            "actual": len(original_projection.respondents),
            "expected": original.active_row_count,
        },
        {
            "check": "original_fixture_sha_absent_from_config_bytes",
            "pass": fixture_doc["fixture_source_sha256"] not in original_path.read_text(encoding="utf-8"),
            "actual": "absent",
            "expected": "absent",
        },
    ])
    original_authority_states = Counter(x.decision_state for x in original_projection.authority_snapshots)
    result["checks"].append({
        "check": "original_authority_is_not_fixture_allow",
        "pass": "ALLOW" not in {x.decision_state for x in original_projection.authority_snapshots if x.authority_kind != "REPLAY_PROTOCOL"},
        "actual": dict(original_authority_states),
        "expected": "DEFER source authorities; ALLOW only for local replay protocol",
    })

    # ---- fixture stream and fixture projection/release ----
    stream = load_fixture_stream(fixture_path)
    fixture_projection = build_governed_c11_projection(fixture_config)
    result["checks"].extend([
        {
            "check": "fixture_identity_is_distinct_from_original",
            "pass": fixture_config.active_source_sha256 != fixture_config.original_source_sha256,
            "actual": fixture_config.active_source_sha256,
            "expected": "different from " + fixture_config.original_source_sha256,
        },
        {
            "check": "fixture_binding_matches_stream_sha",
            "pass": fixture_projection.expected_source_sha256 == stream.source_sha256,
            "actual": fixture_projection.expected_source_sha256,
            "expected": stream.source_sha256,
        },
        {
            "check": "fixture_rows_match_binding",
            "pass": len(fixture_projection.respondents) == fixture_config.active_row_count,
            "actual": len(fixture_projection.respondents),
            "expected": fixture_config.active_row_count,
        },
        {
            "check": "fixture_only_authority",
            "pass": all(x.decision_state == "ALLOW" and x.scope_envelope.get("fixture_only") is True
                        for x in fixture_projection.authority_snapshots),
            "actual": dict(Counter(f"{x.decision_state}:{x.scope_envelope.get('fixture_only')}"
                                  for x in fixture_projection.authority_snapshots)),
            "expected": "all ALLOW fixture_only",
        },
    ])
    result["calls"].append({
        "call": "rawlsing_next.source_configuration.fixture.load_fixture_stream",
        "input": str(fixture_path.relative_to(ROOT)),
        "fixture_id": fixture_doc["fixture_id"],
        "fixture_source_sha256": stream.source_sha256,
        "row_count": stream.row_count,
        "transport_identity": stream.transport_identity,
    })
    result["calls"].append({
        "call": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
        "input": "NONRESPONDENT_FIXTURE config",
        "config_id": fixture_config.config_id,
        "config_sha256": result["hashes"]["fixture_config_canonical"],
        "result": "GovernedC11Projection",
        "source_sha256": fixture_projection.expected_source_sha256,
        "respondents": len(fixture_projection.respondents),
        "response_slots": len(fixture_projection.response_slots),
        "coordinate_slots": len(fixture_projection.coordinate_slots),
        "routing_facts": len(fixture_projection.routing),
        "questions": len(fixture_projection.questions),
    })

    release = build_validated_c11_release_from_config(fixture_config, stream=stream)
    result["calls"].append({
        "call": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
        "input": "NONRESPONDENT_FIXTURE config + ExactPhysicalCellStream",
        "config_id": fixture_config.config_id,
        "config_sha256": result["hashes"]["fixture_config_canonical"],
        "fixture_source_sha256": stream.source_sha256,
        "result": "C11LogicalRelease",
        "release_id": release.release_id,
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "source_release_manifest_hash": release.source_release_manifest_hash,
    })

    response_events = [x for x in release.public_objects if isinstance(x, RespondentEvent)]
    coordinate_facts = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    routing_facts = [x for x in release.public_objects if isinstance(x, RoutingEligibilityFact)]
    row_by_respondent = {exact_ref(b.respondent_ref).key: b.row_ordinal for b in fixture_projection.row_bindings}
    slot_states: dict[str, list[str]] = defaultdict(list)
    slot_raws: dict[str, list[Any]] = defaultdict(list)
    slot_canonicals: dict[str, list[Any]] = defaultdict(list)
    for event in response_events:
        slot = slot_from_event(event)
        row = row_by_respondent[exact_ref(event.scoped_respondent_ref).key]
        slot_states[slot].append((row, event.response_state))
        slot_raws[slot].append((row, decode_raw_witness(event.raw_response_value)))
        slot_canonicals[slot].append((row, event.canonical_response_value_if_authorized))
    for slot in slot_states:
        slot_states[slot] = [state for _, state in sorted(slot_states[slot])]
        slot_raws[slot] = [value for _, value in sorted(slot_raws[slot])]
        slot_canonicals[slot] = [value for _, value in sorted(slot_canonicals[slot])]

    expected = oracle["expected"]
    actual_counts = {
        "response_event_count": len(response_events),
        "coordinate_fact_count": len(coordinate_facts),
        "routing_fact_count": len(routing_facts),
    }
    for name, actual in actual_counts.items():
        result["checks"].append({
            "check": f"fixture_{name}",
            "pass": actual == expected[name],
            "actual": actual,
            "expected": expected[name],
        })
    for slot, expected_states in expected["response_states_by_slot"].items():
        result["checks"].append({
            "check": f"fixture_states_{slot}",
            "pass": slot_states.get(slot) == expected_states,
            "actual": slot_states.get(slot),
            "expected": expected_states,
        })
    for slot, expected_raws in expected["raw_values_by_slot"].items():
        result["checks"].append({
            "check": f"fixture_raw_values_{slot}",
            "pass": slot_raws.get(slot) == expected_raws,
            "actual": slot_raws.get(slot),
            "expected": expected_raws,
        })
    for slot, expected_canonicals in expected["canonical_values_by_slot"].items():
        result["checks"].append({
            "check": f"fixture_canonical_values_{slot}",
            "pass": slot_canonicals.get(slot) == expected_canonicals,
            "actual": slot_canonicals.get(slot),
            "expected": expected_canonicals,
        })
    result["checks"].extend([
        {
            "check": "fixture_release_artifact_sha_is_fixture_sha",
            "pass": release.source_artifact_ref.content_hash == stream.source_sha256,
            "actual": release.source_artifact_ref.content_hash,
            "expected": stream.source_sha256,
        },
        {
            "check": "fixture_release_does_not_claim_original_sha",
            "pass": release.source_artifact_ref.content_hash != original.original_source_sha256,
            "actual": release.source_artifact_ref.content_hash,
            "expected": "different from " + original.original_source_sha256,
        },
        {
            "check": "fixture_routing_all_unresolved",
            "pass": all(x.typed_state == "ROUTING_UNKNOWN" for x in routing_facts),
            "actual": dict(Counter(x.typed_state for x in routing_facts)),
            "expected": {"ROUTING_UNKNOWN": len(routing_facts)},
        },
        {
            "check": "fixture_coordinates_all_observed",
            "pass": all(x.typed_state == "OBSERVED_COORDINATE" for x in coordinate_facts),
            "actual": dict(Counter(x.typed_state for x in coordinate_facts)),
            "expected": {"OBSERVED_COORDINATE": len(coordinate_facts)},
        },
    ])
    result["actual"] = {
        "counts": actual_counts,
        "response_state_counts": dict(Counter(x.response_state for x in response_events)),
        "response_states_by_slot": slot_states,
        "routing_state_counts": dict(Counter(x.typed_state for x in routing_facts)),
        "coordinate_state_counts": dict(Counter(x.typed_state for x in coordinate_facts)),
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "m01_m18_coverage": {k: len(v) for k, v in release.m01_m18_coverage.items()},
    }

    # ---- wrong-source / wrong-row / native-key refusals ----
    refusals = []
    try:
        build_validated_c11_release_from_config(original, stream=stream)
    except Exception as exc:  # exact exception type/message recorded
        refusals.append({"case": "original config + fixture stream", "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "original config + fixture stream", "type": "NO_ERROR", "message": "unexpected acceptance"})

    bad_sha = "f" * 64 if stream.source_sha256 != "f" * 64 else "e" * 64
    from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
    bad_stream = ExactPhysicalCellStream(
        source_sha256=bad_sha, row_count=stream.row_count,
        cell_iter_factory=stream.cell_iter_factory,
        transport_identity="R157_WRONG_FIXTURE_SHA_REFUSAL")
    try:
        build_validated_c11_release_from_config(fixture_config, stream=bad_stream)
    except Exception as exc:
        refusals.append({"case": "fixture config + wrong fixture SHA", "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "fixture config + wrong fixture SHA", "type": "NO_ERROR", "message": "unexpected acceptance"})

    key_doc = copy.deepcopy(original.document)
    key_doc["respondents"]["source_native_key_slot"] = {
        "ordinal": original_projection.response_slots[0].slot.ordinal,
        "name": original_projection.response_slots[0].slot.name,
    }
    try:
        build_governed_c11_projection(key_doc)
    except Exception as exc:
        refusals.append({"case": "configured source_native_key_slot without row_native_keys", "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "configured source_native_key_slot without row_native_keys", "type": "NO_ERROR", "message": "unexpected acceptance"})

    result["refusals"] = refusals
    result["checks"].append({
        "check": "wrong_identity_refusals_are_actual_errors",
        "pass": all(r["type"] != "NO_ERROR" for r in refusals),
        "actual": refusals,
        "expected": "all three dependent calls refuse",
    })
    failures = [c for c in result["checks"] if not c["pass"]]
    result["failures"] = failures
    result["status"] = "PASS" if not failures else "FAIL"
    result["no_drop"] = {
        "physical_slots_total": original.document["identity"]["source_column_count"],
        "physical_slots_included": len(original.document["coverage"]["physical_slots_included"]),
        "physical_slots_excluded": len(original.document["coverage"]["physical_slots_excluded"]),
        "items_total": original.document["identity"]["original_item_count"],
        "items_included": len(original.document["coverage"]["items_included"]),
        "items_excluded": len(original.document["coverage"]["items_excluded"]),
    }
    return result


def main() -> int:
    all_results = {}
    overall_pass = True
    for source_id in SOURCE_IDS:
        result = run_source(source_id)
        all_results[source_id] = result
        out = ROOT / "source_pre553_validation" / source_id / "VALIDATION_RESULTS.json"
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        exceptions = build_exceptions(source_id, result)
        exceptions_path = ROOT / "source_pre553_validation" / source_id / "EXCEPTIONS.json"
        exceptions_path.write_text(json.dumps(exceptions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        manifest = update_manifest(source_id, result, exceptions)
        print(f"{source_id}: {result['status']} checks={len(result['checks'])} failures={len(result['failures'])} "
              f"release={result['actual']['release_ref']['object_id']} "
              f"hash={result['actual']['semantic_release_hash']} "
              f"exceptions={exceptions['counts']['entries']} manifest={file_sha(ROOT / 'source_pre553_validation' / source_id / 'manifest.json')[:12]}")
        if result["status"] != "PASS":
            overall_pass = False
    return 0 if overall_pass else 1



def build_exceptions(source_id: str, result: Mapping[str, Any]) -> dict[str, Any]:
    data_dir = ROOT / "rawlsing_next/source_configuration/data" / source_id
    val_dir = ROOT / "source_pre553_validation" / source_id
    config = json.loads((data_dir / "source.config.json").read_text(encoding="utf-8"))
    crosswalk = json.loads((data_dir / "crosswalk.json").read_text(encoding="utf-8"))
    source_sha = config["identity"]["expected_source_sha256"]
    source_ref = {
        "kind": "SOURCE_SNAPSHOT",
        "object_id": f"urn:rawlsing:r157:source-snapshot:{source_id}",
        "content_hash": source_sha,
    }
    metadata_ref = {
        "kind": "R154_PHYSICAL_METADATA",
        "object_id": "urn:rawlsing:r157:metadata:" + config["identity"]["metadata_witness_ref"]["object_id"].split("urn:rawlsing:r157:metadata:", 1)[-1],
        "content_hash": config["identity"]["metadata_witness_ref"]["content_hash"],
    }
    entries: list[dict[str, Any]] = []

    def add(
        *, slice_id: str, item: str, field: str, current: str, refs: list[Any],
        missing: str, affected: str, unaffected: str, owner: str, step: str,
        status: str, resolution: Any = None,
    ) -> None:
        entries.append({
            "source_id": source_id,
            "implementation_id_or_physical_slot": item,
            "required_native_field": field,
            "current_value_or_typed_unknown": current,
            "exact_evidence_refs": refs,
            "contradiction_or_missing_fact": missing,
            "affected_operation_or_slice": affected,
            "unaffected_usable_slices": unaffected,
            "acquisition_fix_owner_and_step": f"{owner}: {step}",
            "status": status,
            "resolution_evidence": resolution,
            "slice_id": slice_id,
        })

    item_by_code = {i["source_variable_code"]: i["implementation_id"] for i in config["items"]}
    slot_by_name = {p["name"]: f"physical_slots[{p['ordinal']}]:{p['name']}" for p in config["physical_slots"]}
    item_docs_by_code = {i["source_variable_code"]: i for i in config["items"]}
    for residual in config["residuals"]:
        item_label = "SOURCE_LEVEL"
        refs = [source_ref, metadata_ref]
        if "-EXCLUDED-" in residual["residual_id"]:
            code = residual["scope"].split("/", 1)[-1]
            item_label = item_by_code.get(code) or slot_by_name.get(code) or f"source_item:{code}"
            if code in item_docs_by_code:
                refs = list(item_docs_by_code[code]["evidence_refs"]) + [metadata_ref]
            elif code in {p["name"] for p in config["physical_slots"]}:
                refs = [metadata_ref]
        add(
            slice_id=residual["residual_id"],
            item=item_label,
            field=residual["field"],
            current=f"{residual['status']}: {residual['reason']}",
            refs=refs,
            missing=residual["reason"],
            affected=residual["dependent_operation"],
            unaffected=residual["unaffected_scope"],
            owner=residual["owner"],
            step=residual["next_step"],
            status=residual["status"],
        )

    codebook_by_name = {e["codebook_var_name"]: e for e in crosswalk["codebook_entries"]}
    unmatched = [i for i in config["items"] if i["mapping_status"] == "UNMATCHED_EXPLICIT_ID"]
    for item in unmatched:
        codebook_name = item["source_variable_code"]
        ce = codebook_by_name.get(codebook_name)
        physical = ce["physical_names"] if ce else []
        add(
            slice_id=f"{source_id}-UNMATCHED-{item['implementation_id']}",
            item=item["implementation_id"],
            field="items.relation",
            current="UNMATCHED_EXPLICIT_ID",
            refs=item["evidence_refs"],
            missing="No exact full-relation row exists for this exact implementation ID; preserved, not promoted.",
            affected="relation-scoped semantic use of this item",
            unaffected="item accounting, matched items and the declared supported slice",
            owner="LATIN lane / P3 integration owner",
            step="Retain exact unmatched identity; never substitute a last row, casefold alias or nearest relation.",
            status="HELD_UNMATCHED_RELATION",
        )

    for entry in crosswalk["entries"]:
        if entry["relation_kind"] != "PHYSICAL_ONLY_EXTRA":
            continue
        selected = entry.get("selected_for_supported_slice", False)
        add(
            slice_id=f"{source_id}-PHYSICAL-ONLY-{entry['physical_name']}",
            item=f"physical_slots[{entry['physical_ordinal']}]:{entry['physical_name']}",
            field="physical_slots.codebook_mapping",
            current=("SOURCE_NATIVE_COORDINATE_WITHOUT_CODEBOOK_ROW" if selected else "PHYSICAL_ONLY_EXTRA"),
            refs=[metadata_ref],
            missing=entry.get("held_reason") or "No exact codebook counterpart in current evidence.",
            affected=("codebook-linked semantic use; not used for raw coordinate observation"
                      if selected else "codebook-linked semantic use of this physical slot"),
            unaffected=("raw source-native country coordinate" if selected else
                        "explicit crosswalk, supported slice and all other accounted slots"),
            owner="LATIN lane / P3 integration owner",
            step="Preserve physical-only status; acquire exact edition/codebook evidence before any alias.",
            status=("USED_RAW_COORDINATE" if selected else "HELD_UNMAPPED"),
        )

    # Bulk no-drop entries.  Exact IDs/ordinals are carried, not just counts.
    excluded_slots = config["coverage"]["physical_slots_excluded"]
    if excluded_slots:
        add(
            slice_id=f"{source_id}-EXCLUDED-PHYSICAL-SLOTS",
            item=f"physical_slots: {len(excluded_slots)} ordinals",
            field="coverage.physical_slots_excluded",
            current=",".join(str(x["ordinal"]) for x in excluded_slots),
            refs=[metadata_ref],
            missing=config["coverage"]["partial_scope_reason"],
            affected="scope outside the declared supported slice",
            unaffected="declared supported slice and included slots",
            owner="LATIN lane / P3 integration owner",
            step="Widen only with exact evidence; every excluded slot remains accounted in source.config.json.",
            status="EXCLUDED_ACCOUNTED",
        )
    excluded_items = config["coverage"]["items_excluded"]
    if excluded_items:
        add(
            slice_id=f"{source_id}-EXCLUDED-ITEMS",
            item=f"items: {len(excluded_items)} implementation IDs",
            field="coverage.items_excluded",
            current=",".join(x["implementation_id"] for x in excluded_items),
            refs=[source_ref],
            missing=config["coverage"]["partial_scope_reason"],
            affected="scope outside the declared supported slice",
            unaffected="declared supported slice and included items",
            owner="LATIN lane / P3 integration owner",
            step="Widen only with exact evidence; every excluded item remains accounted in source.config.json.",
            status="EXCLUDED_ACCOUNTED",
        )
    return {
        "schema": "PYAT_R157_SOURCE_EXCEPTION_LEDGER@1.0.0",
        "source_id": source_id,
        "source_sha256": source_sha,
        "entries": entries,
        "counts": {
            "entries": len(entries),
            "residuals": len(config["residuals"]),
            "unmatched_relation_items": len(unmatched),
            "physical_only_extra_slots": sum(1 for e in crosswalk["entries"]
                                             if e["relation_kind"] == "PHYSICAL_ONLY_EXTRA"),
            "excluded_slots": len(excluded_slots),
            "excluded_items": len(excluded_items),
        },
        "limits": [
            "The ledger preserves exact IDs/ordinals and evidence; fixture success is not original-source authority.",
            "Excluded rows are accounted, not deleted or silently aliased.",
        ],
    }


def update_manifest(source_id: str, result: Mapping[str, Any], exceptions: Mapping[str, Any]) -> dict[str, Any]:
    val_dir = ROOT / "source_pre553_validation" / source_id
    manifest_path = val_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = [a for a in manifest["artifacts"]
                 if a["path"] not in ("source_pre553_validation/%s/VALIDATION_RESULTS.json" % source_id,
                                      "source_pre553_validation/%s/EXCEPTIONS.json" % source_id)]
    for rel in (f"source_pre553_validation/{source_id}/VALIDATION_RESULTS.json",
                f"source_pre553_validation/{source_id}/EXCEPTIONS.json"):
        path = ROOT / rel
        artifacts.append({"path": rel, "sha256": file_sha(path), "bytes": path.stat().st_size})
    manifest["artifacts"] = artifacts
    manifest["validation"] = {
        "status": result["status"],
        "native_release_ref": result["actual"]["release_ref"],
        "semantic_release_hash": result["actual"]["semantic_release_hash"],
        "actual_counts": result["actual"]["counts"],
        "no_drop": result["no_drop"],
        "refusals": result["refusals"],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    raise SystemExit(main())
