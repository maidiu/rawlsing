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
from rawlsing_next.source_configuration import evidence as E  # noqa: E402
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


def topology_assertions(source_id: str, original: Any) -> dict[str, Any]:
    inherited = {x["source_variable_code"]: x for x in E.iter_item_evidence(source_id)}
    config_items = {i["source_variable_code"]: i for i in original.document["items"]}
    response_by_question: dict[str, list[dict[str, Any]]] = {}
    for slot in original.document["response_slots"]:
        response_by_question.setdefault(slot["question_id"], []).append(slot)
    affected = {"nominal_choice", "nominal_position", "response_status"}
    expected_kind = {
        "nominal_choice": "NOMINAL_CHOICE",
        "nominal_position": "NOMINAL_POSITION",
        "response_status": "RESPONSE_STATUS",
    }
    entries = []
    for code, item in inherited.items():
        relation = item.get("relation") or {}
        topology = relation.get("manual_response_topology")
        if topology not in affected:
            continue
        slots = response_by_question.get(code, [])
        kinds = set()
        for slot in slots:
            for value in slot["values"]:
                for occurrence in value["occurrences"]:
                    kinds.add(occurrence["multiplicity_order_rank_fields"].get("kind"))
        config_item = config_items.get(code, {})
        config_topology = (config_item.get("relation") or {}).get("manual_response_topology")
        expected = expected_kind[topology]
        passed = (
            len(slots) == 1
            and config_topology == topology
            and kinds == {expected}
            and "UNORDERED_MULTISELECT_SET" not in kinds
        )
        entries.append({
            "source_id": source_id,
            "source_variable_code": code,
            "implementation_id": item["implementation_id"],
            "inherited_topology": topology,
            "config_item_topology": config_topology,
            "response_slots": [s["slot"]["name"] for s in slots],
            "occurrence_kinds": sorted(k for k in kinds if k is not None),
            "expected_occurrence_kind": expected,
            "pass": passed,
            "evidence_refs": config_item.get("evidence_refs", []),
        })
    return {
        "schema": "PYAT_R157_TOPOLOGY_ASSERTIONS@1.0.0",
        "source_id": source_id,
        "entries": entries,
        "counts": {
            "affected": len(entries),
            "pass": sum(1 for e in entries if e["pass"]),
            "fail": sum(1 for e in entries if not e["pass"]),
        },
        "limits": [
            "Assertions compare each item's inherited H48/P2 topology to the serialized config occurrence kind.",
            "A single-response nominal item must not be emitted as UNORDERED_MULTISELECT_SET.",
        ],
    }


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

    topology = topology_assertions(source_id, original)
    result["topology_assertions"] = topology
    for entry in topology["entries"]:
        result["checks"].append({
            "check": f"topology_{entry['source_variable_code']}",
            "pass": entry["pass"],
            "actual": entry["occurrence_kinds"],
            "expected": [entry["expected_occurrence_kind"]],
            "inherited_topology": entry["inherited_topology"],
        })
    result["checks"].append({
        "check": "topology_single_response_count_and_shapes",
        "pass": topology["counts"]["fail"] == 0,
        "actual": topology["counts"],
        "expected": "all affected single-response items use their inherited single-response topology",
    })

    # ---- original-source portable recipe validation (no row expansion) ----
    # The original config declares row_selector=ALL with ROUTING_UNKNOWN for every
    # response question.  We validate that recipe statically instead of expanding
    # original rows into a physical response workload.
    original_questions = original.document["questions"]
    original_routing = original.document["routing"]
    original_qids = [q["question_id"] for q in original_questions]
    routing_by_qid = {}
    for entry in original_routing:
        routing_by_qid.setdefault(entry["question_id"], []).append(entry)
    routing_recipe_ok = (
        len(original_routing) == len(original_questions)
        and set(routing_by_qid) == set(original_qids)
        and all(len(v) == 1 for v in routing_by_qid.values())
        and all(v[0]["row_selector"] == "ALL" for v in routing_by_qid.values())
        and all(v[0]["typed_state"] == "ROUTING_UNKNOWN" for v in routing_by_qid.values())
    )
    result["calls"].append({
        "call": "static original routing recipe validation",
        "input": "ORIGINAL_SOURCE config (not physically expanded)",
        "config_id": original.config_id,
        "config_sha256": result["hashes"]["original_config_canonical"],
        "result": "ROUTING_RECIPE_VALIDATED",
        "questions": len(original_questions),
        "routing_entries": len(original_routing),
        "row_selector": "ALL",
        "typed_state": "ROUTING_UNKNOWN",
        "physical_row_expansion": "NOT_PERFORMED",
    })
    original_authority_snapshots = original.document["authority"]["snapshots"]
    result["checks"].extend([
        {
            "check": "original_identity_is_original_source",
            "pass": original.original_source_sha256 == original.document["identity"]["expected_source_sha256"],
            "actual": original.original_source_sha256,
            "expected": original.document["identity"]["expected_source_sha256"],
        },
        {
            "check": "original_has_no_fixture_provenance",
            "pass": original.fixture_provenance is None,
            "actual": original.fixture_provenance,
            "expected": None,
        },
        {
            "check": "original_respondent_rows_match_source",
            "pass": original.active_row_count == original.document["binding"]["row_count"]
                    == original.document["identity"]["source_row_count"],
            "actual": original.active_row_count,
            "expected": original.document["identity"]["source_row_count"],
        },
        {
            "check": "original_fixture_sha_absent_from_config_bytes",
            "pass": fixture_doc["fixture_source_sha256"] not in original_path.read_text(encoding="utf-8"),
            "actual": "absent",
            "expected": "absent",
        },
        {
            "check": "original_routing_recipe_covers_all_questions_with_ALL_unknown",
            "pass": routing_recipe_ok,
            "actual": {
                "questions": len(original_questions),
                "routing_entries": len(original_routing),
                "selectors": sorted({v[0]["row_selector"] for v in routing_by_qid.values()}) if routing_by_qid else [],
                "states": sorted({v[0]["typed_state"] for v in routing_by_qid.values()}) if routing_by_qid else [],
            },
            "expected": "one ALL/ROUTING_UNKNOWN routing entry per response question; no physical row expansion",
        },
    ])
    original_authority_states = Counter(a["decision_state"] for a in original_authority_snapshots)
    result["checks"].append({
        "check": "original_authority_is_not_fixture_allow",
        "pass": all(a["decision_state"] != "ALLOW" for a in original_authority_snapshots
                    if a["authority_kind"] != "REPLAY_PROTOCOL"),
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
    key_slot = original.document["response_slots"][0]["slot"]
    key_doc["respondents"]["source_native_key_slot"] = {
        "ordinal": key_slot["ordinal"],
        "name": key_slot["name"],
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
        topology_path = ROOT / "source_pre553_validation" / source_id / "TOPOLOGY_ASSERTIONS.json"
        topology_path.write_text(json.dumps(result["topology_assertions"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
    cbmap = {e["codebook_var_name"]: e["physical_names"] for e in crosswalk["codebook_entries"]}
    slot_by_name = {p["name"]: f"physical_slots[{p['ordinal']}]:{p['name']}" for p in config["physical_slots"]}
    item_docs_by_code = {i["source_variable_code"]: i for i in config["items"]}
    for residual in config["residuals"]:
        item_label = "SOURCE_LEVEL"
        refs = [source_ref, metadata_ref]
        if "-EXCLUDED-" in residual["residual_id"]:
            code = residual["scope"].split("/", 1)[-1]
            if code in item_by_code:
                item_label = f"{item_by_code[code]} @ {','.join(cbmap.get(code, []))}"
            else:
                item_label = slot_by_name.get(code) or f"source_item:{code}"
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
            item=f"{item['implementation_id']} @ {','.join(cbmap.get(codebook_name, []))}",
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
            "excluded_slots": len(config["coverage"]["physical_slots_excluded"]),
            "excluded_items": len(config["coverage"]["items_excluded"]),
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
                                      "source_pre553_validation/%s/EXCEPTIONS.json" % source_id,
                                      "source_pre553_validation/%s/TOPOLOGY_ASSERTIONS.json" % source_id)]
    for rel in (f"source_pre553_validation/{source_id}/VALIDATION_RESULTS.json",
                f"source_pre553_validation/{source_id}/EXCEPTIONS.json",
                f"source_pre553_validation/{source_id}/TOPOLOGY_ASSERTIONS.json"):
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
