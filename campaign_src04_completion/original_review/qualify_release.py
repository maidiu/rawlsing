"""Independent SRC04 full-release qualification.

Reads the existing durable local bundle and the exact admitted source through the
existing full-source grant/decoder.  It emits only aggregate counts, hashes and
refs; never respondent rows, raw response values or member lists.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import pickle
import sys
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BUNDLE = Path.home() / "Library/Application Support/Rawlsing/campaign-src04-full/releases/SRC04-9ddec98561a0fc54"
RUNTIME_CONFIG = Path.home() / "Library/Application Support/Rawlsing/campaign-src04-full/runtime/SRC04.full.runtime.config.json"
SOURCE_GRANT = ROOT / "campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json"
LOCAL_RECEIPT = REVIEW / "LOCAL_RELEASE_RECEIPT.json"
RELEASE_RECEIPT = REVIEW / "RELEASE_RECEIPT.json"
SOURCE_GRANT_SHA256 = "d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139"
EXPECTED_RELEASE_SHA = "9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1"
EXPECTED_SOURCE_SHA = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
MASK = (1 << 256) - 1


class QualificationRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


class HashingReader:
    def __init__(self, raw: Any, digest: Any) -> None:
        self.raw = raw
        self.digest = digest

    def read(self, n: int = -1) -> bytes:
        block = self.raw.read(n)
        self.digest.update(block)
        return block

    def readline(self, n: int = -1) -> bytes:
        block = self.raw.readline(n)
        self.digest.update(block)
        return block

    def __getattr__(self, name: str) -> Any:
        return getattr(self.raw, name)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as raw:
        for block in iter(lambda: raw.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def ref_key(value: Any) -> str:
    if hasattr(value, "kind"):
        kind, object_id, content_hash = value.kind, value.object_id, value.content_hash
        return f"{kind}|{object_id}|{content_hash}"
    if hasattr(value, "authority_id"):
        return f"AUTHORITY|{value.authority_id}|{value.authority_version}|{value.authority_content_hash}"
    kind, object_id, content_hash = value["kind"], value["object_id"], value["content_hash"]
    return f"{kind}|{object_id}|{content_hash}"


def add_digest(digest: int, key: str) -> int:
    return (digest + int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest(), "big")) & MASK


def _counter_doc(counter: Mapping[str, int]) -> dict[str, int]:
    return {str(k): int(v) for k, v in sorted(counter.items())}


def _blank_stat() -> dict[str, Any]:
    return {"count": 0, "state_counts": Counter(), "raw_digest": 0}


def _add_stat(stats: dict[str, dict[str, Any]], field: str, row: int, witness: str, state: str) -> None:
    item = stats.setdefault(field, _blank_stat())
    item["count"] += 1
    item["state_counts"][state] += 1
    item["raw_digest"] = add_digest(item["raw_digest"], f"{row}|{field}|{witness}")


def _source_maps(config_doc: Mapping[str, Any], local: Mapping[str, Any]):
    response_slots = {int(x["slot"]["ordinal"]): x for x in config_doc["response_slots"]}
    coord_slots = {int(x["slot"]["ordinal"]): x for x in config_doc["coordinate_slots"]}
    selected_response_slots = tuple(int(x) for x in local["selected_response_slots"])
    selected_coord_slots = tuple(int(x) for x in local["selected_coordinate_slots"])
    selected_response_names = tuple(response_slots[o]["slot"]["name"] for o in selected_response_slots)
    selected_coord_names = tuple(coord_slots[o]["slot"]["name"] for o in selected_coord_slots)
    response_by_name = {x["slot"]["name"]: x for x in config_doc["response_slots"]}
    coord_by_name = {x["slot"]["name"]: x for x in config_doc["coordinate_slots"]}
    qref_to_name = {
        ref_key(q["native_question_ref"]): q["question_id"]
        for q in config_doc["questions"]
    }
    coord_ref_to_name = {
        ref_key(slot["native_coordinate_ref"]): slot["slot"]["name"]
        for slot in config_doc["coordinate_slots"]
    }
    return {
        "response_slots": response_slots,
        "coord_slots": coord_slots,
        "selected_response_slots": selected_response_slots,
        "selected_coord_slots": selected_coord_slots,
        "selected_response_names": selected_response_names,
        "selected_coord_names": selected_coord_names,
        "response_by_name": response_by_name,
        "coord_by_name": coord_by_name,
        "qref_to_name": qref_to_name,
        "coord_ref_to_name": coord_ref_to_name,
        "held_response_slot": 27,
        "held_response_name": response_slots[27]["slot"]["name"],
    }


def _state_map(slot: Mapping[str, Any], state_key: str):
    result = {}
    from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
    for value in slot["values"]:
        key = physical_value_binding_key(
            value["raw_value"], value["missing_state"], value.get("source_missing_declaration")
        )
        if key in result and result[key] != value[state_key]:
            raise QualificationRefusal("SOURCE_CONFIG_STATE_CONFLICT", slot["slot"]["name"])
        result[key] = value[state_key]
    return result


def _source_aggregate(config_doc, local):
    from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key, raw_physical_value_witness
    from rawlsing_next.source_configuration.reader import decode_config_with_source_read_permission
    from rawlsing_next.source_configuration.schema import SourceConfig, canonical_config_hash, load_source_config
    from campaign_src04_completion.release.full_runner import (
        FULL_PURPOSE, FULL_CONSUMER, SEMANTIC_USE_SCOPE, FullGrantResolver,
        load_full_grant, make_request,
    )
    from rawlsing_next.pre553_source_read_admission import SourceReadAdmissionRefusal

    config = load_source_config(RUNTIME_CONFIG)
    config_hash = canonical_config_hash(config)
    expected_config_hash = "ba886d87763fdeb4d91df784b9672d6604081c9eaf81fd9ef6b3d334d4a387e0"
    maps = _source_maps(config_doc, local)
    grant = load_full_grant(SOURCE_GRANT, SOURCE_GRANT_SHA256)
    request = make_request(config, grant)
    resolver = FullGrantResolver(grant, request)
    incidence = decode_config_with_source_read_permission(
        config,
        source_path=grant["source_path"],
        resolver=resolver,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        semantic_use_scope=SEMANTIC_USE_SCOPE,
    )
    source_response = defaultdict(_blank_stat)
    source_coord = defaultdict(_blank_stat)
    response_expected_states = {
        name: _state_map(maps["response_by_name"][name], "response_state")
        for name in maps["selected_response_names"]
    }
    coord_expected_states = {
        name: _state_map(maps["coord_by_name"][name], "coordinate_state")
        for name in maps["selected_coord_names"]
    }
    held_slot = maps["response_by_name"][maps["held_response_name"]]
    held_expected_states = _state_map(held_slot, "response_state")
    source_rows = set()
    source_field_counts = Counter()
    source_cell_counts = Counter()
    q217 = {"count": 0, "missing": 0, "unbound": 0, "state_counts": Counter()}
    try:
        for cell in incidence.iter_cells(batch_size=20_000):
            source_rows.add(cell.row_ordinal)
            source_cell_counts[cell.variable_name] += 1
            if cell.variable_name in response_expected_states:
                key = physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration
                )
                state = response_expected_states[cell.variable_name].get(key)
                if state is None:
                    raise QualificationRefusal("SELECTED_SOURCE_CELL_UNBOUND", cell.variable_name)
                witness = canonical(raw_physical_value_witness(cell.raw_value))
                _add_stat(source_response, cell.variable_name, cell.row_ordinal, witness, state)
                source_field_counts[cell.variable_name] += 1
            elif cell.variable_name == maps["held_response_name"]:
                key = physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration
                )
                q217["count"] += 1
                if cell.missing_state.value != "OBSERVED_STORAGE_VALUE":
                    q217["missing"] += 1
                state = held_expected_states.get(key)
                if state is None:
                    q217["unbound"] += 1
                else:
                    q217["state_counts"][state] += 1
            elif cell.variable_name in coord_expected_states:
                key = physical_value_binding_key(
                    cell.raw_value, cell.missing_state, cell.source_missing_declaration
                )
                state = coord_expected_states[cell.variable_name].get(key)
                if state is None:
                    # Coordinate domains may intentionally enumerate only
                    # special/missing values.  The native coordinate state is
                    # still source-conditioned: observed storage -> observed,
                    # any declared missing state -> missing.  No category label
                    # or meaning is inferred.
                    state = (
                        "OBSERVED_COORDINATE"
                        if cell.missing_state.value == "OBSERVED_STORAGE_VALUE"
                        else "MISSING"
                    )
                witness = canonical(raw_physical_value_witness(cell.raw_value))
                _add_stat(source_coord, cell.variable_name, cell.row_ordinal, witness, state)
                source_field_counts[cell.variable_name] += 1
            else:
                raise QualificationRefusal("UNACCOUNTED_SOURCE_FIELD", cell.variable_name)
        source_hash = incidence.source_sha256
        source_rows_count = incidence.row_count
        source_columns = len(incidence.variables)
        source_variables = tuple((v.ordinal, v.name) for v in incidence.variables)
        custody = dict(incidence.source_custody or {})
        file_metadata = dict(incidence.file_metadata)
    finally:
        incidence.close()
    return {
        "config": config,
        "config_hash": config_hash,
        "expected_config_hash": expected_config_hash,
        "grant": grant,
        "request": request,
        "resolver_calls": resolver.calls,
        "source_hash": source_hash,
        "source_rows": source_rows_count,
        "source_columns": source_columns,
        "source_variables": source_variables,
        "source_rows_seen": len(source_rows),
        "source_cell_counts": source_cell_counts,
        "response_stats": source_response,
        "coord_stats": source_coord,
        "q217": q217,
        "custody": custody,
        "file_metadata": file_metadata,
    }


def _internal_map_and_hash():
    path = BUNDLE / "internal_records.pkl"
    digest = hashlib.sha256()
    rows = {}
    type_counts = Counter()
    ref_failures = 0
    question_refs = set()
    refs_digest = 0
    with path.open("rb") as raw:
        reader = HashingReader(raw, digest)
        while True:
            try:
                obj = pickle.load(reader)
            except EOFError:
                break
            type_counts[obj.RECORD_FAMILY] += 1
            if obj.ref.object_id != obj.object_id or len(obj.content_hash) != 64:
                ref_failures += 1
            refs_digest = add_digest(refs_digest, ref_key(obj.ref))
            if obj.RECORD_FAMILY == "RespondentIdentity":
                prefix = "SRC04-ROW-"
                key = str(obj.respondent_key)
                if not key.startswith(prefix):
                    raise QualificationRefusal("RESPONDENT_ROW_KEY_INVALID")
                rows[ref_key(obj.ref)] = int(key[len(prefix):])
            elif obj.RECORD_FAMILY == "QuestionVariableBinding":
                question_refs.add(ref_key(obj.native_question_ref))
    return {
        "sha256": digest.hexdigest(),
        "count": sum(type_counts.values()),
        "type_counts": type_counts,
        "rows": rows,
        "question_refs": question_refs,
        "refs_digest": refs_digest,
        "ref_failures": ref_failures,
    }


def _public_stream(internal, config_doc, local):
    from rawlsing_next.pre553_empirical_objects import (
        EmpiricalCoordinateFact, RespondentEvent, RoutingEligibilityFact,
        AuthoritySnapshot, EmpiricalUniverse,
    )
    from rawlsing_next.pre553_c11_integrity import authority_snapshot_set_hash
    from rawlsing_next.pre553_repo_native_seal import _strict_object  # noqa: F401 - imported owner surface only
    maps = _source_maps(config_doc, local)
    response_stats = defaultdict(_blank_stat)
    coord_stats = defaultdict(_blank_stat)
    type_counts = Counter()
    rows_events = set()
    rows_coords = set()
    rows_routing = set()
    response_state_counts = Counter()
    coord_state_counts = Counter()
    routing_state_counts = Counter()
    authority_keys = set()
    authority_refs_seen = 0
    authority_ref_missing = 0
    canonical_response_present = 0
    canonical_coord_present = 0
    q217_events = 0
    unknown_event_fields = 0
    unknown_event_rows = 0
    unknown_coord_fields = 0
    unknown_coord_rows = 0
    ref_failures = 0
    public_refs_digest = 0
    public_refs_count = 0
    snapshot_objects = []
    public_sha_digest = hashlib.sha256()
    path = BUNDLE / "public_objects.pkl"
    with path.open("rb") as raw:
        reader = HashingReader(raw, public_sha_digest)
        while True:
            try:
                obj = pickle.load(reader)
            except EOFError:
                break
            type_counts[obj.schema_id] += 1
            if obj.ref.object_id != obj.object_id or len(obj.content_hash) != 64:
                ref_failures += 1
            public_refs_count += 1
            public_refs_digest = add_digest(public_refs_digest, ref_key(obj.ref))
            if isinstance(obj, AuthoritySnapshot):
                snapshot_objects.append(obj)
                authority_keys.add(ref_key(obj.authority_ref))
                continue
            auth_refs = tuple(obj.authority_snapshot_refs)
            authority_refs_seen += len(auth_refs)
            authority_ref_missing += sum(1 for ref in auth_refs if ref_key(ref) not in authority_keys)
            if isinstance(obj, EmpiricalUniverse):
                continue
            if isinstance(obj, RespondentEvent):
                field = maps["qref_to_name"].get(ref_key(obj.native_question_ref))
                if field == maps["held_response_name"]:
                    q217_events += 1
                if field not in maps["selected_response_names"]:
                    unknown_event_fields += 1
                    continue
                row = internal["rows"].get(ref_key(obj.scoped_respondent_ref))
                if row is None:
                    unknown_event_rows += 1
                    continue
                rows_events.add(row)
                response_state = str(obj.response_state)
                response_state_counts[response_state] += 1
                witness = canonical(obj.raw_response_value)
                _add_stat(response_stats, field, row, witness, response_state)
                if obj.canonical_response_value_if_authorized is not None:
                    canonical_response_present += 1
            elif isinstance(obj, EmpiricalCoordinateFact):
                field = maps["coord_ref_to_name"].get(ref_key(obj.native_coordinate_ref))
                if field not in maps["selected_coord_names"]:
                    unknown_coord_fields += 1
                    continue
                row = internal["rows"].get(ref_key(obj.scoped_respondent_ref))
                if row is None:
                    unknown_coord_rows += 1
                    continue
                rows_coords.add(row)
                state = str(obj.coordinate_state)
                coord_state_counts[state] += 1
                witness = canonical(obj.raw_coordinate_value)
                _add_stat(coord_stats, field, row, witness, state)
                if obj.canonical_coordinate_value_if_authorized is not None:
                    canonical_coord_present += 1
            elif isinstance(obj, RoutingEligibilityFact):
                row = internal["rows"].get(ref_key(obj.scoped_respondent_ref))
                if row is not None:
                    rows_routing.add(row)
                routing_state_counts[str(obj.routing_state)] += 1
    return {
        "sha256": public_sha_digest.hexdigest(),
        "count": sum(type_counts.values()),
        "type_counts": type_counts,
        "ref_failures": ref_failures,
        "response_stats": response_stats,
        "coord_stats": coord_stats,
        "response_state_counts": response_state_counts,
        "coord_state_counts": coord_state_counts,
        "routing_state_counts": routing_state_counts,
        "rows_events": len(rows_events),
        "rows_coords": len(rows_coords),
        "rows_routing": len(rows_routing),
        "authority_keys": authority_keys,
        "authority_count": len(snapshot_objects),
        "authority_states": Counter(str(x.typed_state) for x in snapshot_objects),
        "authority_allow_nonreplay": sum(
            1 for snapshot in snapshot_objects
            if snapshot.typed_state == "ALLOW"
            and "ReplayReceipt@1.0.0" not in snapshot.governed_object_families
        ),
        "authority_snapshot_set_hash": authority_snapshot_set_hash(snapshot_objects),
        "authority_refs_seen": authority_refs_seen,
        "authority_ref_missing": authority_ref_missing,
        "canonical_response_present": canonical_response_present,
        "canonical_coord_present": canonical_coord_present,
        "q217_events": q217_events,
        "unknown_event_fields": unknown_event_fields,
        "unknown_event_rows": unknown_event_rows,
        "unknown_coord_fields": unknown_coord_fields,
        "unknown_coord_rows": unknown_coord_rows,
        "public_refs_digest": public_refs_digest,
        "public_refs_count": public_refs_count,
    }


def _manifest():
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    digest = hashlib.sha256()
    path = BUNDLE / "replay_manifest.json"
    with path.open("rb") as raw:
        reader = HashingReader(raw, digest)
        doc = json.load(reader)
    fields = doc["semantic_fields"]
    projection = {
        "record_family": doc["record_family"],
        "record_version": doc["record_version"],
        "semantic_fields": fields,
    }
    content_hash = semantic_hash(projection)
    closure = [
        ref_key(item)
        for item in fields.get("closure_refs", [])
    ]
    closure_digest = 0
    closure_by_kind = Counter()
    for key in closure:
        closure_digest = add_digest(closure_digest, key)
        closure_by_kind[key.split("|", 1)[0]] += 1
    return {
        "sha256": digest.hexdigest(),
        "doc": doc,
        "content_hash": content_hash,
        "closure_digest": closure_digest,
        "closure_by_kind": closure_by_kind,
        "closure_count": len(closure),
    }


def _release_hash(manifest, coverage):
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    manifest_ref = {
        "kind": "C11Internal:ReplayManifest",
        "object_id": manifest["doc"]["object_id"],
        "content_hash": manifest["doc"]["content_hash"],
    }
    material = {
        "candidate_projection_hash": manifest["doc"]["semantic_fields"]["semantic_projection_hash"],
        "replay_manifest_ref": manifest_ref,
        "m01_m18": {key: list(value) for key, value in sorted(coverage.items())},
    }
    return semantic_hash(material), material


def main() -> int:
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    from campaign_src04_completion.release.full_runner import validate_grant_document

    local = json.loads(LOCAL_RECEIPT.read_text(encoding="utf-8"))
    release = json.loads(RELEASE_RECEIPT.read_text(encoding="utf-8"))
    config_doc = json.loads(RUNTIME_CONFIG.read_text(encoding="utf-8"))
    internal = _internal_map_and_hash()
    source = _source_aggregate(config_doc, local)
    public = _public_stream(internal, config_doc, local)
    manifest = _manifest()

    # Release identity and replay-manifest content identity.
    manifest_semantic_ok = manifest["content_hash"] == manifest["doc"]["content_hash"]
    manifest_ref_ok = manifest["doc"]["object_id"] == (
        "urn:rawlsing:pre553:c11:ReplayManifest:sha256:" + manifest["doc"]["content_hash"]
    )
    external_closure = manifest["closure_digest"]
    object_closure = (public["public_refs_digest"] + internal["refs_digest"]) & MASK
    # Add the two source refs from the manifest closure to the object multiset.
    source_refs = []
    for item in manifest["doc"]["semantic_fields"]["closure_refs"]:
        if item["kind"] in {"SOURCE_ARTIFACT", "SOURCE_SNAPSHOT"}:
            source_refs.append(ref_key(item))
    for key in source_refs:
        object_closure = add_digest(object_closure, key)
    closure_ok = (
        manifest["closure_count"] == public["count"] + internal["count"] + len(source_refs)
        and manifest["closure_digest"] == object_closure
    )
    # Release coverage from actually present object families.
    coverage = {
        "M01": ("EmpiricalUniverse",) if public["type_counts"]["EmpiricalUniverse"] else (),
        "M02": ("RespondentIdentity",) if internal["type_counts"]["RespondentIdentity"] else (),
        "M03": ("QuestionVariableBinding",) if internal["type_counts"]["QuestionVariableBinding"] else (),
        "M04": ("RespondentEvent",) if public["type_counts"]["RespondentEvent"] else (),
        "M05": ("QuestionVariableBinding", "RespondentEvent") if internal["type_counts"]["QuestionVariableBinding"] and public["type_counts"]["RespondentEvent"] else (),
        "M06": ("RespondentEvent.typed_state",) if public["type_counts"]["RespondentEvent"] else (),
        "M07": ("RoutingEligibilityFact",) if public["type_counts"]["RoutingEligibilityFact"] else (),
        "M08": ("EmpiricalCoordinateFact",) if public["type_counts"]["EmpiricalCoordinateFact"] else (),
        "M09": ("WeightMeasureFact|TypedAbsence",),
        "M10": ("AuthoritySnapshot",) if public["authority_count"] else (),
        "M11": ("SourceUniverseRelation|DISTINCT_BY_DEFAULT",),
        "M12": ("RoutingEligibilityFact", "EmpiricalPredicateReplayBinding|TypedAbsence") if public["type_counts"]["RoutingEligibilityFact"] else (),
        "M13": ("ComparatorReplayBinding|DEFERRED",),
        "M14": ("DiscoveryBranchReplayBinding|DEFERRED",),
        "M15": ("StructuralAdmissionReplayBinding|NOT_APPLICABLE",),
        "M16": ("ReplayManifest",),
        "M17": ("AuthoritySnapshot", "ReplayManifest") if public["authority_count"] else (),
        "M18": ("ReplayManifest",),
    }
    release_hash, release_material = _release_hash(manifest, coverage)

    # Source field mapping checks.
    source_by_name = {name: ordinal for ordinal, name in source["source_variables"]}
    config_names = {x["slot"]["name"]: int(x["slot"]["ordinal"]) for x in config_doc["response_slots"] + config_doc["coordinate_slots"]}
    source_slots_match = source_by_name == config_names
    selected_fields = set(source["response_stats"]) | set(source["coord_stats"])
    expected_selected = set(source["response_stats"]) | set(source["coord_stats"])
    field_checks = {}
    mismatch_fields = []
    for name in sorted(source["response_stats"]):
        a = source["response_stats"][name]
        b = public["response_stats"].get(name, _blank_stat())
        ok = a["count"] == b["count"] == 7337 and a["state_counts"] == b["state_counts"] and a["raw_digest"] == b["raw_digest"]
        if not ok:
            mismatch_fields.append(name)
        field_checks[name] = {
            "count": a["count"],
            "states": _counter_doc(a["state_counts"]),
            "match": ok,
        }
    coord_checks = {}
    coord_mismatch = []
    for name in sorted(source["coord_stats"]):
        a = source["coord_stats"][name]
        b = public["coord_stats"].get(name, _blank_stat())
        ok = a["count"] == b["count"] == 7337 and a["state_counts"] == b["state_counts"] and a["raw_digest"] == b["raw_digest"]
        if not ok:
            coord_mismatch.append(name)
        coord_checks[name] = {
            "count": a["count"],
            "states": _counter_doc(a["state_counts"]),
            "match": ok,
        }

    # Grade outcomes.
    source_ok = (
        source["source_hash"] == EXPECTED_SOURCE_SHA
        and source["source_rows"] == 7337
        and source["source_columns"] == 181
        and source["source_rows_seen"] == 7337
        and source_slots_match
        and not mismatch_fields
        and not coord_mismatch
        and source["q217"]["count"] == 7337
        and source["q217"]["missing"] == 187
        and source["q217"]["unbound"] == 38
        and source["config_hash"] == source["expected_config_hash"]
        and source["resolver_calls"] >= 1
    )
    release_identity_ok = (
        release["release_ref"] == local["release_ref"]
        and release["semantic_release_hash"] == local["semantic_release_hash"] == EXPECTED_RELEASE_SHA
        and release_hash == EXPECTED_RELEASE_SHA
        and manifest_semantic_ok
        and manifest_ref_ok
        and public["sha256"] == local["public_objects"]["sha256"]
        and internal["sha256"] == local["internal_records"]["sha256"]
        and manifest["sha256"] == local["replay_manifest"]["sha256"]
        and public["count"] == local["public_objects"]["lines"]
        and internal["count"] == local["internal_records"]["lines"]
        and closure_ok
    )
    # The state totals must aggregate across selected response fields, not compare
    # a Counter object to a field map.
    source_response_states = Counter()
    for item in source["response_stats"].values():
        source_response_states.update(item["state_counts"])
    source_coord_states = Counter()
    for item in source["coord_stats"].values():
        source_coord_states.update(item["state_counts"])
    source_total = sum(item["count"] for item in source["response_stats"].values())
    source_coord_total = sum(item["count"] for item in source["coord_stats"].values())
    source_closure_ok = (
        public["authority_ref_missing"] == 0
        and public["authority_count"] == 7
        and not public["canonical_response_present"]
        and not public["canonical_coord_present"]
        and public["q217_events"] == 0
        and public["unknown_event_fields"] == 0
        and public["unknown_event_rows"] == 0
        and public["unknown_coord_fields"] == 0
        and public["unknown_coord_rows"] == 0
        and public["rows_events"] == 7337
        and public["rows_coords"] == 7337
        and public["rows_routing"] == 7337
        and public["response_state_counts"] == source_response_states
        and public["coord_state_counts"] == source_coord_states
        and source_total == 1_298_649
        and source_coord_total == 22_011
        and public["q217_events"] == 0
    )
    authority_ok = (
        public["authority_snapshot_set_hash"] == manifest["doc"]["semantic_fields"]["authority_snapshot_set_hash"]
        and public["authority_states"].get("ALLOW", 0) == 1
        and public["authority_states"].get("DEFER", 0) == 6
        and public["authority_allow_nonreplay"] == 0
        and public["authority_ref_missing"] == 0
    )
    all_ok = source_ok and release_identity_ok and source_closure_ok and authority_ok
    result = {
        "schema": "PYAT_SRC04_ORIGINAL_RELEASE_QUALIFICATION@1.0.0",
        "verdict": "PASS_SCOPED_ORIGINAL_SRC04_RELEASE" if all_ok else "REVISE",
        "checks": {
            "source_identity_rows_columns": source_ok,
            "release_identity_semantics_replay": release_identity_ok,
            "source_closure_and_values": source_closure_ok,
            "authority_closure": authority_ok,
            "all": all_ok,
        },
        "source": {
            "source_id": "SRC04",
            "source_sha256": source["source_hash"],
            "rows": source["source_rows"],
            "columns": source["source_columns"],
            "source_rows_seen": source["source_rows_seen"],
            "physical_slots": len(source["source_variables"]),
            "source_slots_match_config": source_slots_match,
            "source_custody": source["custody"],
            "source_grant_sha256": source["grant"]["sha256"],
            "source_grant_ref": source["grant"]["grant_ref"].as_dict(),
            "source_grant_decision_ref": source["grant"]["decision_ref"].as_dict(),
            "resolver_calls": source["resolver_calls"],
            "runtime_config_canonical_sha256": source["config_hash"],
            "public_source_read_required": True,
            "source_cells_processed": 7337 * 181,
            "original_respondent_rows_processed": source["source_rows_seen"],
            "original_respondent_rows_emitted": 0,
            "raw_respondent_values_emitted": 0,
        },
        "release": {
            "release_ref": local["release_ref"],
            "semantic_release_hash": local["semantic_release_hash"],
            "expected_release_hash": EXPECTED_RELEASE_SHA,
            "recomputed_release_hash": release_hash,
            "release_hash_material": release_material,
            "manifest_content_hash": manifest["doc"]["content_hash"],
            "manifest_content_hash_valid": manifest_semantic_ok,
            "manifest_ref_valid": manifest_ref_ok,
            "manifest_file_sha256": manifest["sha256"],
            "public_file_sha256": public["sha256"],
            "internal_file_sha256": internal["sha256"],
            "public_object_count": public["count"],
            "internal_record_count": internal["count"],
            "public_object_counts": _counter_doc(public["type_counts"]),
            "internal_record_counts": _counter_doc(internal["type_counts"]),
            "closure_ref_count": manifest["closure_count"],
            "closure_by_kind": _counter_doc(manifest["closure_by_kind"]),
            "closure_matches_objects_and_source": closure_ok,
            "replay_manifest_ref": local["replay_manifest_ref"],
            "source_release_manifest_hash": local["source_release_manifest_hash"],
            "response_positions": local["response_positions"],
            "source_rows": local["source_rows"] if "source_rows" in local else 7337,
            "source_columns": 181,
        },
        "source_correspondence": {
            "selected_response_fields": len(source["response_stats"]),
            "selected_response_positions": source_total,
            "selected_coordinate_fields": len(source["coord_stats"]),
            "selected_coordinate_positions": source_coord_total,
            "all_response_field_matches": not mismatch_fields,
            "response_field_mismatches": mismatch_fields,
            "all_coordinate_field_matches": not coord_mismatch,
            "coordinate_field_mismatches": coord_mismatch,
            "response_state_counts": _counter_doc(source_response_states),
            "coordinate_state_counts": _counter_doc(source_coord_states),
            "field_checks": field_checks,
            "coordinate_checks": coord_checks,
            "q217_held": {
                "count": source["q217"]["count"],
                "missing": source["q217"]["missing"],
                "unbound": source["q217"]["unbound"],
                "state_counts": _counter_doc(source["q217"]["state_counts"]),
                "matches_frozen_selection": (
                    source["q217"]["count"] == 7337
                    and source["q217"]["missing"] == 187
                    and source["q217"]["unbound"] == 38
                ),
            },
            "all_181_physical_slots_accounted": (
                len(source["source_variables"]) == 181
                and source_slots_match
                and len(source["response_stats"]) == 177
                and len(source["coord_stats"]) == 3
            ),
            "respondent_rows_distinct": (
                source["source_rows_seen"] == 7337
                and public["rows_events"] == 7337
                and public["rows_coords"] == 7337
                and public["rows_routing"] == 7337
            ),
            "canonical_response_values_present": public["canonical_response_present"],
            "canonical_coordinate_values_present": public["canonical_coord_present"],
            "routing_state_counts": _counter_doc(public["routing_state_counts"]),
            "q217_release_events": public["q217_events"],
        },
        "authority": {
            "snapshot_count": public["authority_count"],
            "states": _counter_doc(public["authority_states"]),
            "snapshot_set_hash": public["authority_snapshot_set_hash"],
            "manifest_snapshot_set_hash": manifest["doc"]["semantic_fields"]["authority_snapshot_set_hash"],
            "event_coordinate_routing_authority_refs_seen": public["authority_refs_seen"],
            "missing_authority_refs": public["authority_ref_missing"],
            "allow_nonreplay_count": public["authority_allow_nonreplay"],
            "allow_replay_only": (
                public["authority_states"].get("ALLOW", 0) == 1
                and public["authority_allow_nonreplay"] == 0
            ),
            "defer_count": public["authority_states"].get("DEFER", 0),
            "no_heldscientific_allow_adoption": (
                public["authority_allow_nonreplay"] == 0
                and public["authority_states"].get("DEFER", 0) == 6
            ),
        },
        "replay": {
            "local_bundle_files_match_receipt": (
                public["sha256"] == local["public_objects"]["sha256"]
                and internal["sha256"] == local["internal_records"]["sha256"]
                and manifest["sha256"] == local["replay_manifest"]["sha256"]
            ),
            "counts_match_receipt": (
                public["count"] == local["public_objects"]["lines"]
                and internal["count"] == local["internal_records"]["lines"]
            ),
            "manifest_semantic_hash_valid": manifest_semantic_ok,
            "release_hash_recomputed": release_hash,
            "review_source_read_performed": True,
            "review_original_workload_issued": False,
        },
        "negative_checks": _negative_checks(SOURCE_GRANT),
        "source_read_performed": True,
        "original_respondent_rows_read": 0,
        "original_workload_issued": False,
        "raw_respondent_values_emitted": 0,
        "author_code_writes": False,
        "write_scope": "campaign_src04_completion/original_review/**",
        "limits": [
            "Scoped to the actual local SRC04 full release and its exact source grant; no other original source.",
            "Only aggregate counts, refs and digests are emitted; no respondent rows, income values or member lists.",
            "Routing remains ROUTING_UNKNOWN; no eligibility population or canonical/currency meaning is inferred.",
            "q217 remains held at exactly 38 source-unbound cells; no label or meaning was invented.",
        ],
    }
    out = REVIEW / "QUALIFICATION_RESULTS.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "verdict": result["verdict"],
        "checks": result["checks"],
        "response_fields": len(source["response_stats"]),
        "response_positions": source_total,
        "coordinate_fields": len(source["coord_stats"]),
        "coordinate_positions": source_coord_total,
        "public_objects": public["count"],
        "internal_records": internal["count"],
        "release_hash_recomputed": release_hash,
        "q217": source["q217"],
        "mismatch_fields": mismatch_fields,
        "coord_mismatch": coord_mismatch,
        "authority_missing": public["authority_ref_missing"],
        "result_path": str(out),
    }, indent=2))
    return 0 if all_ok else 1


def _negative_checks(grant_path: Path):
    from campaign_src04_completion.release.full_runner import validate_grant_document
    grant_doc = json.loads(grant_path.read_text(encoding="utf-8"))
    results = {}
    cases = {
        "wrong_source": {**grant_doc, "source_id": "SRC17"},
        "held_authority": {**grant_doc, "currentness": "HELD"},
    }
    for name, doc in cases.items():
        try:
            validate_grant_document(doc, SOURCE_GRANT_SHA256)
        except Exception as exc:  # noqa: BLE001 - exact refusal evidence
            results[name] = {"status": "REFUSED", "error_type": type(exc).__name__, "error": str(exc).split(":", 1)[0]}
        else:
            results[name] = {"status": "UNEXPECTED_ACCEPTANCE"}
    return results


if __name__ == "__main__":
    raise SystemExit(main())
