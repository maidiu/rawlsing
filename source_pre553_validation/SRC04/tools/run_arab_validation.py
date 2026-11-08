"""Exercise frozen R157 factory/native C11 validator for the ARAB lane."""
from __future__ import annotations

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
from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config  # noqa: E402
from rawlsing_next.source_configuration import evidence as E  # noqa: E402

CODEC = R5TypedValueCodec()
SOURCE_IDS = ("SRC04", "SRC05", "SRC06", "SRC07")
EXPECTED_KIND = {
    "scalar": "SCALAR", "binary_factual": "BINARY_FACTUAL", "binary_contrast": "BINARY_CONTRAST",
    "ordinal_context": "ORDINAL_CONTEXT", "nominal_choice": "NOMINAL_CHOICE",
    "ranked_choice": "RANKED_CHOICE",
}


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_raw(witness: Any) -> Any:
    return CODEC.decode(witness["$raw_physical_value"]["token"])


def slot_from_event(event: RespondentEvent) -> str:
    if event.component_or_subitem_ref is not None:
        return exact_ref(event.component_or_subitem_ref).object_id.rsplit(":", 1)[-1]
    return exact_ref(event.response_topology_ref).object_id.split(":")[-2]


def topology_assertions(source_id: str, original: Any) -> dict[str, Any]:
    inherited = {x["source_variable_code"]: x for x in E.iter_item_evidence(source_id)}
    phys = {p["name"]: p for p in E.iter_physical_slots(source_id)}
    config_items = {i["source_variable_code"]: i for i in original.document["items"]}
    response_by_q = defaultdict(list)
    for slot in original.document["response_slots"]:
        response_by_q[slot["question_id"]].append(slot)
    entries = []
    for code, item in inherited.items():
        relation = item.get("relation") or {}
        topology = relation.get("manual_response_topology")
        if topology in {"administrative", "continuous_numeric"}:
            continue
        p = phys[code]
        labels = p.get("value_labels") or {}
        substantive = {int(float(k)) for k, v in labels.items()
                       if str(v).casefold().strip() and not any(t in str(v).casefold() for t in
                           ("missing", "don't know", "dont know", "refus", "declined", "not asked", "not applicable"))}
        if topology == "multiselect":
            expected = "MULTISELECT_INDICATOR" if substantive and substantive <= {0, 1} else "MULTISELECT_SINGLE_COLUMN"
        else:
            expected = EXPECTED_KIND.get(topology, "SCALAR")
        slots = response_by_q.get(code, [])
        kinds = set()
        occurrence_counts = []
        for slot in slots:
            occurrence_counts.append(len(slot["values"][0]["occurrences"]))
            for value in slot["values"]:
                for occ in value["occurrences"]:
                    kinds.add(occ["multiplicity_order_rank_fields"].get("kind"))
        config_topology = (config_items.get(code, {}).get("relation") or {}).get("manual_response_topology")
        passed = (len(slots) == 1 and config_topology == topology and kinds == {expected}
                  and occurrence_counts == [1] and "UNORDERED_MULTISELECT_SET" not in kinds)
        entries.append({
            "source_variable_code": code, "implementation_id": item["implementation_id"],
            "inherited_topology": topology, "config_item_topology": config_topology,
            "response_slots": [s["slot"]["name"] for s in slots],
            "occurrence_kinds": sorted(k for k in kinds if k is not None),
            "occurrences_per_value": occurrence_counts,
            "expected_occurrence_kind": expected, "pass": passed,
            "evidence_refs": config_items.get(code, {}).get("evidence_refs", []),
        })
    return {"schema": "PYAT_R157_TOPOLOGY_ASSERTIONS@1.0.0", "source_id": source_id,
            "entries": entries,
            "counts": {"affected": len(entries), "pass": sum(1 for e in entries if e["pass"]),
                       "fail": sum(1 for e in entries if not e["pass"])},
            "limits": ["Compares inherited H48/P2 topology to serialized config occurrence kind.",
                       "Single-column nominal/status/topology is not emitted as multiselect unless inherited topology is multiselect."]}


def run_source(source_id: str) -> dict[str, Any]:
    data = ROOT / "rawlsing_next/source_configuration/data" / source_id
    val = ROOT / "source_pre553_validation" / source_id
    original_path = data / "source.config.json"
    fixture_path = val / "fixture.json"
    fixture_config_path = val / "fixture.config.json"
    oracle_path = val / "fixture_oracle.json"
    result: dict[str, Any] = {"source_id": source_id, "status": "RUNNING", "calls": [], "checks": [],
                              "failures": [], "skips": [], "hashes": {},
                              "paths": {k: str((data if k in {"original_config", "crosswalk", "field_evidence"}
                                                else val) / name)
                                        for k, name in (("original_config", "source.config.json"),
                                                        ("crosswalk", "crosswalk.json"),
                                                        ("field_evidence", "field_evidence.json"),
                                                        ("fixture_config", "fixture.config.json"),
                                                        ("fixture", "fixture.json"),
                                                        ("fixture_oracle", "fixture_oracle.json"),
                                                        ("manifest", "manifest.json"))}}
    for name, path in (("original_config_file", original_path),
                       ("crosswalk_file", data / "crosswalk.json"),
                       ("field_evidence_file", data / "field_evidence.json"),
                       ("fixture_config_file", fixture_config_path),
                       ("fixture_file", fixture_path),
                       ("fixture_oracle_file", oracle_path)):
        result["hashes"][name] = file_sha(path)
    original = load_source_config(original_path)
    fixture_config = load_source_config(fixture_config_path)
    fixture_doc = json.loads(fixture_path.read_text(encoding="utf-8"))
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    result["hashes"]["original_config_canonical"] = canonical_config_hash(original)
    result["hashes"]["fixture_config_canonical"] = canonical_config_hash(fixture_config)
    result["hashes"]["fixture_source"] = fixture_doc["fixture_source_sha256"]

    topology = topology_assertions(source_id, original)
    result["topology_assertions"] = topology
    for entry in topology["entries"]:
        result["checks"].append({"check": f"topology_{entry['source_variable_code']}", "pass": entry["pass"],
                                 "actual": entry["occurrence_kinds"],
                                 "expected": [entry["expected_occurrence_kind"]],
                                 "inherited_topology": entry["inherited_topology"]})
    result["checks"].append({"check": "topology_all_response_shapes", "pass": topology["counts"]["fail"] == 0,
                             "actual": topology["counts"], "expected": "all response items match inherited topology"})

    routing = original.document["routing"]
    qids = [q["question_id"] for q in original.document["questions"]]
    by_q = defaultdict(list)
    for r in routing:
        by_q[r["question_id"]].append(r)
    routing_ok = (len(routing) == len(qids) and set(by_q) == set(qids)
                  and all(len(v) == 1 and v[0]["row_selector"] == "ALL"
                          and v[0]["typed_state"] == "ROUTING_UNKNOWN" for v in by_q.values()))
    result["calls"].append({"call": "static original routing recipe validation",
                            "input": "ORIGINAL_SOURCE config (not physically expanded)",
                            "config_id": original.config_id,
                            "config_sha256": result["hashes"]["original_config_canonical"],
                            "result": "ROUTING_RECIPE_VALIDATED", "questions": len(qids),
                            "routing_entries": len(routing), "row_selector": "ALL",
                            "typed_state": "ROUTING_UNKNOWN", "physical_row_expansion": "NOT_PERFORMED"})
    result["checks"].extend([
        {"check": "original_identity_is_original_source",
         "pass": original.original_source_sha256 == original.document["identity"]["expected_source_sha256"],
         "actual": original.original_source_sha256,
         "expected": original.document["identity"]["expected_source_sha256"]},
        {"check": "original_has_no_fixture_provenance", "pass": original.fixture_provenance is None,
         "actual": original.fixture_provenance, "expected": None},
        {"check": "original_respondent_rows_match_source",
         "pass": original.active_row_count == original.document["binding"]["row_count"]
                 == original.document["identity"]["source_row_count"],
         "actual": original.active_row_count, "expected": original.document["identity"]["source_row_count"]},
        {"check": "original_fixture_sha_absent_from_config_bytes",
         "pass": fixture_doc["fixture_source_sha256"] not in original_path.read_text(encoding="utf-8"),
         "actual": "absent", "expected": "absent"},
        {"check": "original_routing_recipe_ALL_unknown", "pass": routing_ok,
         "actual": {"questions": len(qids), "routing": len(routing),
                    "selectors": sorted({r["row_selector"] for r in routing}),
                    "states": sorted({r["typed_state"] for r in routing})},
         "expected": "one ALL/ROUTING_UNKNOWN entry per response question; no physical row expansion"},
    ])
    auths = original.document["authority"]["snapshots"]
    result["checks"].append({"check": "original_authority_is_not_fixture_allow",
                             "pass": all(a["decision_state"] != "ALLOW" for a in auths
                                         if a["authority_kind"] != "REPLAY_PROTOCOL"),
                             "actual": dict(Counter(a["decision_state"] for a in auths)),
                             "expected": "DEFER source authorities; ALLOW only local replay"})

    stream = load_fixture_stream(fixture_path)
    fixture_projection = build_governed_c11_projection(fixture_config)
    result["calls"].append({"call": "rawlsing_next.source_configuration.fixture.load_fixture_stream",
                            "input": str(fixture_path.relative_to(ROOT)),
                            "fixture_id": fixture_doc["fixture_id"],
                            "fixture_source_sha256": stream.source_sha256,
                            "row_count": stream.row_count, "transport_identity": stream.transport_identity})
    result["calls"].append({"call": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
                            "input": "NONRESPONDENT_FIXTURE config",
                            "config_id": fixture_config.config_id,
                            "config_sha256": result["hashes"]["fixture_config_canonical"],
                            "result": "GovernedC11Projection",
                            "source_sha256": fixture_projection.expected_source_sha256,
                            "respondents": len(fixture_projection.respondents),
                            "response_slots": len(fixture_projection.response_slots),
                            "coordinate_slots": len(fixture_projection.coordinate_slots),
                            "routing_facts": len(fixture_projection.routing),
                            "questions": len(fixture_projection.questions)})
    result["checks"].extend([
        {"check": "fixture_identity_is_distinct_from_original",
         "pass": fixture_config.active_source_sha256 != fixture_config.original_source_sha256,
         "actual": fixture_config.active_source_sha256,
         "expected": "different from " + fixture_config.original_source_sha256},
        {"check": "fixture_binding_matches_stream_sha",
         "pass": fixture_projection.expected_source_sha256 == stream.source_sha256,
         "actual": fixture_projection.expected_source_sha256, "expected": stream.source_sha256},
        {"check": "fixture_rows_match_binding",
         "pass": len(fixture_projection.respondents) == fixture_config.active_row_count,
         "actual": len(fixture_projection.respondents), "expected": fixture_config.active_row_count},
        {"check": "fixture_only_authority",
         "pass": all(x.decision_state == "ALLOW" and x.scope_envelope.get("fixture_only") is True
                     for x in fixture_projection.authority_snapshots),
         "actual": dict(Counter(f"{x.decision_state}:{x.scope_envelope.get('fixture_only')}"
                                for x in fixture_projection.authority_snapshots)),
         "expected": "all ALLOW fixture_only"},
    ])

    release = build_validated_c11_release_from_config(fixture_config, stream=stream)
    result["calls"].append({"call": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
                            "input": "NONRESPONDENT_FIXTURE config + ExactPhysicalCellStream",
                            "config_id": fixture_config.config_id,
                            "config_sha256": result["hashes"]["fixture_config_canonical"],
                            "fixture_source_sha256": stream.source_sha256,
                            "result": "C11LogicalRelease", "release_id": release.release_id,
                            "release_ref": release.release_ref.as_dict(),
                            "semantic_release_hash": release.semantic_release_hash,
                            "source_release_manifest_hash": release.source_release_manifest_hash})
    events = [x for x in release.public_objects if isinstance(x, RespondentEvent)]
    coords = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    routing_facts = [x for x in release.public_objects if isinstance(x, RoutingEligibilityFact)]
    row_by_resp = {exact_ref(b.respondent_ref).key: b.row_ordinal for b in fixture_projection.row_bindings}
    slot_states = defaultdict(list)
    slot_raws = defaultdict(list)
    slot_canon = defaultdict(list)
    for event in events:
        slot = slot_from_event(event)
        row = row_by_resp[exact_ref(event.scoped_respondent_ref).key]
        slot_states[slot].append((row, event.response_state))
        slot_raws[slot].append((row, decode_raw(event.raw_response_value)))
        slot_canon[slot].append((row, event.canonical_response_value_if_authorized))
    for slot in list(slot_states):
        slot_states[slot] = [v for _, v in sorted(slot_states[slot])]
        slot_raws[slot] = [v for _, v in sorted(slot_raws[slot])]
        slot_canon[slot] = [v for _, v in sorted(slot_canon[slot])]
    expected = oracle["expected"]
    actual_counts = {"response_event_count": len(events), "coordinate_fact_count": len(coords),
                     "routing_fact_count": len(routing_facts)}
    for name, actual in actual_counts.items():
        result["checks"].append({"check": f"fixture_{name}", "pass": actual == expected[name],
                                 "actual": actual, "expected": expected[name]})
    for slot, states in expected["response_states_by_slot"].items():
        result["checks"].append({"check": f"fixture_states_{slot}", "pass": slot_states.get(slot) == states,
                                 "actual": slot_states.get(slot), "expected": states})
    for slot, raws in expected["raw_values_by_slot"].items():
        result["checks"].append({"check": f"fixture_raw_values_{slot}", "pass": slot_raws.get(slot) == raws,
                                 "actual": slot_raws.get(slot), "expected": raws})
    for slot, canons in expected["canonical_values_by_slot"].items():
        result["checks"].append({"check": f"fixture_canonical_values_{slot}", "pass": slot_canon.get(slot) == canons,
                                 "actual": slot_canon.get(slot), "expected": canons})
    result["checks"].extend([
        {"check": "fixture_release_artifact_sha_is_fixture_sha",
         "pass": release.source_artifact_ref.content_hash == stream.source_sha256,
         "actual": release.source_artifact_ref.content_hash, "expected": stream.source_sha256},
        {"check": "fixture_release_does_not_claim_original_sha",
         "pass": release.source_artifact_ref.content_hash != original.original_source_sha256,
         "actual": release.source_artifact_ref.content_hash, "expected": "different from " + original.original_source_sha256},
        {"check": "fixture_routing_all_unresolved",
         "pass": all(x.typed_state == "ROUTING_UNKNOWN" for x in routing_facts),
         "actual": dict(Counter(x.typed_state for x in routing_facts)),
         "expected": {"ROUTING_UNKNOWN": len(routing_facts)}},
        {"check": "fixture_coordinates_all_observed",
         "pass": all(x.typed_state == "OBSERVED_COORDINATE" for x in coords),
         "actual": dict(Counter(x.typed_state for x in coords)),
         "expected": {"OBSERVED_COORDINATE": len(coords)}},
    ])
    result["actual"] = {"counts": actual_counts,
                        "response_state_counts": dict(Counter(x.response_state for x in events)),
                        "response_states_by_slot": dict(slot_states),
                        "routing_state_counts": dict(Counter(x.typed_state for x in routing_facts)),
                        "coordinate_state_counts": dict(Counter(x.typed_state for x in coords)),
                        "release_ref": release.release_ref.as_dict(),
                        "semantic_release_hash": release.semantic_release_hash,
                        "m01_m18_coverage": {k: len(v) for k, v in release.m01_m18_coverage.items()}}

    refusals = []
    bad_sha = "f" * 64 if stream.source_sha256 != "f" * 64 else "e" * 64
    try:
        build_governed_c11_projection(original, source_sha256=bad_sha)
    except Exception as exc:
        refusals.append({"case": "original config + wrong active SHA (pre-expansion)",
                         "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "original config + wrong active SHA (pre-expansion)",
                         "type": "NO_ERROR", "message": "unexpected acceptance"})
    from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
    bad_stream = ExactPhysicalCellStream(source_sha256=bad_sha, row_count=stream.row_count,
                                         cell_iter_factory=stream.cell_iter_factory,
                                         transport_identity="R157_WRONG_FIXTURE_SHA_REFUSAL")
    try:
        build_validated_c11_release_from_config(fixture_config, stream=bad_stream)
    except Exception as exc:
        refusals.append({"case": "fixture config + wrong fixture SHA", "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "fixture config + wrong fixture SHA", "type": "NO_ERROR", "message": "unexpected acceptance"})
    key_doc = json.loads(json.dumps(original.document))
    slot = original.document["response_slots"][0]["slot"]
    key_doc["respondents"]["source_native_key_slot"] = {"ordinal": slot["ordinal"], "name": slot["name"]}
    try:
        build_governed_c11_projection(key_doc)
    except Exception as exc:
        refusals.append({"case": "configured source_native_key_slot without row_native_keys",
                         "type": type(exc).__name__, "message": str(exc)})
    else:
        refusals.append({"case": "configured source_native_key_slot without row_native_keys",
                         "type": "NO_ERROR", "message": "unexpected acceptance"})
    result["refusals"] = refusals
    result["checks"].append({"check": "wrong_identity_refusals_are_actual_errors",
                             "pass": all(r["type"] != "NO_ERROR" for r in refusals),
                             "actual": refusals, "expected": "all dependent calls refuse"})
    result["failures"] = [c for c in result["checks"] if not c["pass"]]
    result["status"] = "PASS" if not result["failures"] else "FAIL"
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
    overall = True
    for source_id in SOURCE_IDS:
        result = run_source(source_id)
        val = ROOT / "source_pre553_validation" / source_id
        (val / "VALIDATION_RESULTS.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (val / "TOPOLOGY_ASSERTIONS.json").write_text(json.dumps(result["topology_assertions"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        exceptions = build_exceptions(source_id, result)
        (val / "EXCEPTIONS.json").write_text(json.dumps(exceptions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        update_manifest(source_id, result, exceptions)
        print(f"{source_id}: {result['status']} checks={len(result['checks'])} failures={len(result['failures'])} "
              f"release={result['actual']['release_ref']['object_id']} hash={result['actual']['semantic_release_hash']} "
              f"topology={result['topology_assertions']['counts']} exceptions={exceptions['counts']['entries']}")
        if result["status"] != "PASS":
            overall = False
    return 0 if overall else 1


def build_exceptions(source_id: str, result: Mapping[str, Any]) -> dict[str, Any]:
    data = ROOT / "rawlsing_next/source_configuration/data" / source_id
    config = json.loads((data / "source.config.json").read_text(encoding="utf-8"))
    crosswalk = json.loads((data / "crosswalk.json").read_text(encoding="utf-8"))
    item_by_code = {i["source_variable_code"]: i for i in config["items"]}
    slot_by_name = {p["name"]: f"physical_slots[{p['ordinal']}]:{p['name']}" for p in config["physical_slots"]}
    source_ref = {"kind": "SOURCE_SNAPSHOT", "object_id": f"urn:rawlsing:r157:source-snapshot:{source_id}",
                  "content_hash": config["identity"]["expected_source_sha256"]}
    metadata_ref = {"kind": "R154_PHYSICAL_METADATA",
                    "object_id": config["identity"]["metadata_witness_ref"]["object_id"],
                    "content_hash": config["identity"]["metadata_witness_ref"]["content_hash"]}
    entries = []

    def add(item: str, field: str, current: str, refs: list[Any], missing: str, affected: str,
            unaffected: str, owner: str, step: str, status: str) -> None:
        entries.append({"source_id": source_id, "implementation_id_or_physical_slot": item,
                        "required_native_field": field, "current_value_or_typed_unknown": current,
                        "exact_evidence_refs": refs, "contradiction_or_missing_fact": missing,
                        "affected_operation_or_slice": affected, "unaffected_usable_slices": unaffected,
                        "acquisition_fix_owner_and_step": f"{owner}: {step}", "status": status,
                        "resolution_evidence": None})

    for residual in config["residuals"]:
        item_label = "SOURCE_LEVEL"
        refs = [source_ref, metadata_ref]
        if "-EXCLUDED-" in residual["residual_id"]:
            code = residual["scope"].split("/", 1)[-1]
            if code in item_by_code:
                item_label = f"{item_by_code[code]['implementation_id']} @ {code}"
                refs = list(item_by_code[code]["evidence_refs"]) + [metadata_ref]
            else:
                item_label = slot_by_name.get(code, f"source_item:{code}")
                refs = [metadata_ref]
        add(item_label, residual["field"], f"{residual['status']}: {residual['reason']}", refs,
            residual["reason"], residual["dependent_operation"], residual["unaffected_scope"],
            residual["owner"], residual["next_step"], residual["status"])
    return {"schema": "PYAT_R157_SOURCE_EXCEPTION_LEDGER@1.0.0", "source_id": source_id,
            "source_sha256": config["identity"]["expected_source_sha256"], "entries": entries,
            "counts": {"entries": len(entries), "residuals": len(config["residuals"]),
                       "excluded_slots": len(config["coverage"]["physical_slots_excluded"]),
                       "excluded_items": len(config["coverage"]["items_excluded"])},
            "limits": ["Exact IDs/slots and evidence are preserved; fixture success is not original authority.",
                       "No generic unselected/future-expansion exception is used."]}


def update_manifest(source_id: str, result: Mapping[str, Any], exceptions: Mapping[str, Any]) -> None:
    val = ROOT / "source_pre553_validation" / source_id
    path = val / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    keep = [a for a in manifest["artifacts"]
            if a["path"] not in {f"source_pre553_validation/{source_id}/VALIDATION_RESULTS.json",
                                 f"source_pre553_validation/{source_id}/EXCEPTIONS.json",
                                 f"source_pre553_validation/{source_id}/TOPOLOGY_ASSERTIONS.json"}]
    for rel in (f"source_pre553_validation/{source_id}/VALIDATION_RESULTS.json",
                f"source_pre553_validation/{source_id}/EXCEPTIONS.json",
                f"source_pre553_validation/{source_id}/TOPOLOGY_ASSERTIONS.json"):
        p = ROOT / rel
        keep.append({"path": rel, "sha256": file_sha(p), "bytes": p.stat().st_size})
    manifest["artifacts"] = keep
    manifest["validation"] = {"status": result["status"],
                              "native_release_ref": result["actual"]["release_ref"],
                              "semantic_release_hash": result["actual"]["semantic_release_hash"],
                              "actual_counts": result["actual"]["counts"],
                              "no_drop": result["no_drop"], "refusals": result["refusals"]}
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
