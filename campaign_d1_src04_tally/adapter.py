"""Bounded D1 SRC04 observed-sample tally over the accepted local C11 release.

This module reads only the accepted local C11 public-object bundle and committed
Campaign A metadata. It never reads the original SAV and never emits respondent
rows or raw cells.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = Path(__file__).resolve().parent
EVIDENCE = CAMPAIGN / "evidence"
A_EVIDENCE = ROOT / "campaign_a_src04/evidence"
D1_GRANT_PATH = ROOT / ".r61/d1_src04_observed_sample_tally/TRUE_HQ_GRANT.txt"
D1_PROGRAM_PATH = ROOT / ".r61/d1_src04_observed_sample_tally/PROGRAM.txt"
EXPECTED_D1_GRANT_SHA256 = "f51de87818f8fd1365d347da3aee73005fe9ab8ae0c8d2a607487395016d48ae"
EXPECTED_CONTROL_COMMIT = "3b703e878946a442b5c880f318b929365865ed00"
A_RECEIPT_PATH = A_EVIDENCE / "RELEASE_RECEIPT.json"
A_LOCAL_RECEIPT_PATH = A_EVIDENCE / "LOCAL_RELEASE_RECEIPT.json"
PROGRAM_PATH = A_EVIDENCE / "PROGRAM.txt"
SOURCE_CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
EXPECTED_PROGRAM_SHA256 = "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
EXPECTED_SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
EXPECTED_RELEASE_HASH = "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec"
EXPECTED_CONFIG_FILE_SHA256 = "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900"
EXPECTED_CONFIG_CANONICAL_SHA256 = "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
EXPECTED_BUNDLE_ID = "SRC04-fc111cfa78d0fc23"
EXPECTED_LOCAL_RECEIPT_SHA256 = "b1333a021c28f0a4fe3a8272d469d9dab2ecb619cf08fcae3fdf18246fb9d8c9"
EXPECTED_PUBLIC_SHA256 = "a47957a1d0b4e6df29195f70b1c3d122cc69b1a8a484b60bbe072d9eff126edd"
EXPECTED_INTERNAL_SHA256 = "2d9ea42a36e9b326f65f3ed5219ddf84a9fdb7d634ff8e459cc3e8892bc89538"
EXPECTED_REPLAY_SHA256 = "f13d893f363753ad0d17bbf58c5a8bd51fcb12334daf85232b4365d66f96d09e"
EXPECTED_PUBLIC_LINES = 630_990
EXPECTED_INTERNAL_LINES = 7_379
EXPECTED_EVENTS = 308_154
EXPECTED_RESPONSE_FIELDS = 42
EXPECTED_RECORDS = 7_337
CODEBOOK = R5TypedValueCodec()
RECORDED_RESPONSE_STATES = frozenset({"SUBSTANTIVE_RESPONSE", "DK", "REFUSAL", "SOURCE_SPECIFIC_SPECIAL"})
SUBSTANTIVE_STATE = "SUBSTANTIVE_RESPONSE"
NON_OBSERVED_STATES = frozenset({"MISSING", "INVALID_UNRESOLVED", "UNKNOWN", "IAP", "INAPPLICABLE", "NOT_ASKED"})
KNOWN_RESPONSE_STATES = frozenset({"SUBSTANTIVE_RESPONSE", "DK", "REFUSAL", "IAP", "INAPPLICABLE", "NOT_ASKED", "MISSING", "SOURCE_SPECIFIC_SPECIAL", "INVALID_UNRESOLVED"})


class TallyRefusal(ValueError):
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
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False).encode("utf-8")).hexdigest()


def jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def bundle_path() -> Path:
    return Path.home() / "Library/Application Support/Rawlsing/campaign-a-src04/releases" / EXPECTED_BUNDLE_ID


def _verify_source_metadata() -> tuple[dict[str, Any], dict[str, Any], str]:
    if not PROGRAM_PATH.is_file() or sha_file(PROGRAM_PATH) != EXPECTED_PROGRAM_SHA256:
        raise TallyRefusal("PROGRAM_SHA_MISMATCH")
    if not A_RECEIPT_PATH.is_file():
        raise TallyRefusal("RELEASE_RECEIPT_MISSING")
    receipt = load_json(A_RECEIPT_PATH)
    if not A_LOCAL_RECEIPT_PATH.is_file():
        raise TallyRefusal("LOCAL_RECEIPT_EVIDENCE_MISSING")
    local_committed = load_json(A_LOCAL_RECEIPT_PATH)
    if sha_file(A_LOCAL_RECEIPT_PATH) != EXPECTED_LOCAL_RECEIPT_SHA256:
        raise TallyRefusal("LOCAL_RECEIPT_SHA_MISMATCH")
    if local_committed.get("bundle_id") != EXPECTED_BUNDLE_ID:
        raise TallyRefusal("LOCAL_BUNDLE_ID_MISMATCH")
    if local_committed.get("public_objects", {}).get("sha256") != EXPECTED_PUBLIC_SHA256:
        raise TallyRefusal("LOCAL_PUBLIC_HASH_MISMATCH")
    if local_committed.get("internal_records", {}).get("sha256") != EXPECTED_INTERNAL_SHA256:
        raise TallyRefusal("LOCAL_INTERNAL_HASH_MISMATCH")
    if local_committed.get("replay_manifest", {}).get("sha256") != EXPECTED_REPLAY_SHA256:
        raise TallyRefusal("LOCAL_REPLAY_HASH_MISMATCH")
    if local_committed.get("release_ref", {}).get("content_hash") != EXPECTED_RELEASE_HASH:
        raise TallyRefusal("LOCAL_RELEASE_IDENTITY_MISMATCH")
    if receipt.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise TallyRefusal("SOURCE_IDENTITY_MISMATCH")
    if receipt.get("source_read_performed") is not True:
        raise TallyRefusal("ORIGINAL_SOURCE_READ_NOT_ATTESTED")
    if receipt.get("release", {}).get("release_ref", {}).get("content_hash") != EXPECTED_RELEASE_HASH:
        raise TallyRefusal("RELEASE_IDENTITY_MISMATCH")
    config = load_json(SOURCE_CONFIG_PATH)
    if sha_file(SOURCE_CONFIG_PATH) != EXPECTED_CONFIG_FILE_SHA256:
        raise TallyRefusal("SOURCE_CONFIG_FILE_SHA_MISMATCH")
    if receipt.get("config_file_sha256") != EXPECTED_CONFIG_FILE_SHA256:
        raise TallyRefusal("SOURCE_CONFIG_RECEIPT_BINDING_MISMATCH")
    if receipt.get("config_canonical_sha256") != EXPECTED_CONFIG_CANONICAL_SHA256:
        raise TallyRefusal("SOURCE_CONFIG_CANONICAL_SHA_MISMATCH")
    if receipt.get("canonicalization") != "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW":
        raise TallyRefusal("CANONICALIZATION_NOT_DEFER_WITHHELD")
    if receipt.get("selected_response_slots") != list(range(3, 27)) + list(range(28, 46)):
        raise TallyRefusal("SELECTED_RESPONSE_SLOTS_MISMATCH")
    if len(receipt.get("selected_question_ids", [])) != EXPECTED_RESPONSE_FIELDS:
        raise TallyRefusal("SELECTED_FIELD_COUNT_MISMATCH")
    if receipt.get("source_rows") != EXPECTED_RECORDS or receipt.get("source_columns") != 181:
        raise TallyRefusal("SOURCE_DENOMINATOR_MISMATCH")
    return receipt, config, sha_file(A_RECEIPT_PATH)


def _verify_local_bundle() -> dict[str, Any]:
    bundle = bundle_path()
    if not bundle.is_dir():
        raise TallyRefusal("LOCAL_RELEASE_BUNDLE_MISSING")
    receipt_path = bundle / "receipt.json"
    if sha_file(receipt_path) != EXPECTED_LOCAL_RECEIPT_SHA256:
        raise TallyRefusal("LOCAL_RECEIPT_HASH_MISMATCH")
    local = load_json(receipt_path)
    public_path = bundle / "public_objects.jsonl.gz"
    internal_path = bundle / "internal_records.jsonl.gz"
    replay_path = bundle / "replay_manifest.json"
    checks = {
        "public_size": public_path.stat().st_size == local["public_objects"]["bytes"],
        "public_sha": sha_file(public_path) == EXPECTED_PUBLIC_SHA256,
        "internal_size": internal_path.stat().st_size == local["internal_records"]["bytes"],
        "internal_sha": sha_file(internal_path) == EXPECTED_INTERNAL_SHA256,
        "replay_sha": sha_file(replay_path) == EXPECTED_REPLAY_SHA256,
        "release_ref": local["release_ref"]["content_hash"] == EXPECTED_RELEASE_HASH,
        "source_sha": local["source_sha256"] == EXPECTED_SOURCE_SHA256,
    }
    if not all(checks.values()):
        raise TallyRefusal("LOCAL_BUNDLE_CONTENT_IDENTITY_MISMATCH", repr(checks))
    return {"bundle": local, "checks": checks}


def classify_state(state: str) -> str:
    if state not in KNOWN_RESPONSE_STATES:
        raise TallyRefusal("UNKNOWN_RESPONSE_STATE", state)
    if state in RECORDED_RESPONSE_STATES:
        return "RECORDED"
    if state in NON_OBSERVED_STATES:
        return "NON_OBSERVED"
    return "NON_OBSERVED"


def _native_value(event: Any) -> tuple[Any, str]:
    raw = event.raw_response_value
    if not isinstance(raw, Mapping) or set(raw) != {"$raw_physical_value"}:
        raise TallyRefusal("NON_CANONICAL_RAW_VALUE_ENVELOPE")
    encoded = raw["$raw_physical_value"].get("token")
    value = CODEBOOK.decode(encoded)
    token = json.dumps(CODEBOOK.encode(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return value, token


def build_tally(*, receipt_override: Mapping[str, Any] | None = None) -> dict[str, Any]:
    receipt, config, receipt_sha = _verify_source_metadata()
    if receipt_override is not None:
        receipt = receipt_override
        if receipt.get("release", {}).get("release_ref", {}).get("content_hash") != EXPECTED_RELEASE_HASH:
            raise TallyRefusal("RELEASE_IDENTITY_MISMATCH")
    local_info = _verify_local_bundle()
    local = local_info["bundle"]
    question_by_id = {q["question_id"]: q for q in config["questions"]}
    response_by_id = {x["question_id"]: x for x in config["response_slots"]}
    selected = [str(x) for x in receipt["selected_question_ids"]]
    if len(selected) != EXPECTED_RESPONSE_FIELDS:
        raise TallyRefusal("SELECTED_FIELD_COUNT_MISMATCH")
    target_to_question = {
        exact_ref(question_by_id[qid]["native_question_ref"]).key: qid for qid in selected
    }
    field_state: dict[str, Counter] = {qid: Counter() for qid in selected}
    field_value: dict[str, Counter] = {qid: Counter() for qid in selected}
    field_value_state: dict[str, Counter] = {qid: Counter() for qid in selected}
    field_rows: dict[str, set[str]] = {qid: set() for qid in selected}
    field_topology: dict[str, Counter] = {qid: Counter() for qid in selected}
    field_component: dict[str, Counter] = {qid: Counter() for qid in selected}
    schema_counts = Counter()
    public_lines = 0
    event_count = 0
    materialized_events = 0
    with gzip.open(bundle_path() / "public_objects.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            public_lines += 1
            document = json.loads(line)
            schema = document.get("schema_id")
            schema_counts[schema] += 1
            if schema != "RespondentEvent":
                continue
            event = materialize_public_object(document)
            materialized_events += 1
            event_count += 1
            qid = target_to_question.get(exact_ref(event.native_question_ref).key)
            if qid is None:
                continue
            state = str(event.response_state)
            classify_state(state)
            value, token = _native_value(event)
            topology = event.multiplicity_order_rank_fields
            kind = topology.get("kind") if isinstance(topology, Mapping) else None
            component = event.component_or_subitem_ref
            field_state[qid][state] += 1
            field_value[qid][token] += 1
            field_value_state[qid][state + "\x1f" + token] += 1
            field_rows[qid].add(exact_ref(event.scoped_respondent_ref).key)
            field_topology[qid][str(kind)] += 1
            field_component[qid]["present" if component is not None else "none"] += 1
    expected_public = local["public_objects"]["lines"]
    expected_internal = local["internal_records"]["lines"]
    if public_lines != expected_public or public_lines != EXPECTED_PUBLIC_LINES:
        raise TallyRefusal("PUBLIC_OBJECT_LINE_COUNT_MISMATCH", f"{public_lines}")
    if materialized_events != EXPECTED_EVENTS or schema_counts["RespondentEvent"] != EXPECTED_EVENTS:
        raise TallyRefusal("RESPONDENT_EVENT_COUNT_MISMATCH")
    internal_lines = 0
    with gzip.open(bundle_path() / "internal_records.jsonl.gz", "rt", encoding="utf-8") as handle:
        for _ in handle:
            internal_lines += 1
    if internal_lines != expected_internal or internal_lines != EXPECTED_INTERNAL_LINES:
        raise TallyRefusal("INTERNAL_RECORD_LINE_COUNT_MISMATCH", f"{internal_lines}")
    expected_schema = {
        "RespondentEvent": EXPECTED_EVENTS,
        "RoutingEligibilityFact": EXPECTED_EVENTS,
        "EmpiricalCoordinateFact": 14_674,
        "AuthoritySnapshot": 7,
        "EmpiricalUniverse": 1,
    }
    if dict(schema_counts) != expected_schema:
        raise TallyRefusal("PUBLIC_SCHEMA_COUNT_MISMATCH", repr(dict(schema_counts)))
    field_records = []
    held_fields = []
    for qid in selected:
        source_question = question_by_id[qid]
        source_slot = response_by_id[qid]
        event_states = field_state[qid]
        event_total = sum(event_states.values())
        rows = field_rows[qid]
        topology = field_topology[qid]
        component = field_component[qid]
        status = "COUNTED"
        hold_reason = None
        if event_total != EXPECTED_RECORDS or len(rows) != EXPECTED_RECORDS:
            status = "HELD"
            hold_reason = "not one event/one source row per field"
        elif len(topology) != 1 or not next(iter(topology)):
            status = "HELD"
            hold_reason = "field does not have one exact response topology"
        elif any(k != "none" for k in component):
            status = "HELD"
            hold_reason = "field has a component/subitem identity"
        elif any(state not in KNOWN_RESPONSE_STATES for state in event_states):
            status = "HELD"
            hold_reason = "unknown response state"
        if status != "COUNTED":
            held_fields.append({"question_id": qid, "reason": hold_reason})
            field_records.append({
                "question_id": qid,
                "source_variable": source_slot["slot"]["name"],
                "response_slot_ordinal": source_slot["slot"]["ordinal"],
                "native_question_ref": exact_ref(source_question["native_question_ref"]).as_dict(),
                "status": status,
                "hold_reason": hold_reason,
            })
            continue
        observed = sum(n for state, n in event_states.items() if state in RECORDED_RESPONSE_STATES)
        answered = int(event_states.get(SUBSTANTIVE_STATE, 0))
        non_observed = event_total - observed
        state_counts = {state: int(n) for state, n in sorted(event_states.items())}
        values = []
        value_by_state = []
        for token, count in sorted(field_value[qid].items()):
            decoded = CODEBOOK.decode(json.loads(token))
            values.append({"native_value": jsonable(decoded), "native_value_token": token, "count": int(count)})
        for key, count in sorted(field_value_state[qid].items()):
            state, token = key.split("\x1f", 1)
            decoded = CODEBOOK.decode(json.loads(token))
            value_by_state.append({
                "state": state,
                "native_value": jsonable(decoded),
                "native_value_token": token,
                "count": int(count),
            })
        field_records.append({
            "question_id": qid,
            "source_variable": source_slot["slot"]["name"],
            "response_slot_ordinal": source_slot["slot"]["ordinal"],
            "native_question_ref": exact_ref(source_question["native_question_ref"]).as_dict(),
            "unit_identity": "SOURCE_RESPONSE_EVENT",
            "component_identity": "SINGLE_RESPONSE_COMPONENT:" + next(iter(topology)),
            "response_topology_kinds": sorted(topology),
            "component_presence": sorted(component),
            "source_record_denominator": EXPECTED_RECORDS,
            "event_presence_count": event_total,
            "observed_response_denominator": observed,
            "answered_substantive_denominator": answered,
            "missing_or_unobserved_count": non_observed,
            "state_counts": state_counts,
            "native_value_counts": values,
            "native_value_counts_by_state": value_by_state,
            "status": status,
            "hold_reason": None,
        })
    control_field = "q101"
    control_values = []
    for item in next(x for x in field_records if x["question_id"] == control_field)["native_value_counts"]:
        if item["native_value"] in (1, 1.0, 2, 2.0):
            control_values.append(item)
    if len(control_values) != 2 or control_values[0]["count"] == control_values[1]["count"]:
        raise TallyRefusal("CONTROL_DISCRIMINATION_FAILED")
    material = {
        "schema": "PYAT_D1_SRC04_OBSERVED_SAMPLE_TALLY@1.0.0",
        "source_id": "SRC04",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_records": EXPECTED_RECORDS,
        "source_columns": 181,
        "release_ref": {
            "kind": "C11LogicalRelease",
            "object_id": "SRC04_ARAB_BAROMETER_I_PREPARATION",
            "content_hash": EXPECTED_RELEASE_HASH,
        },
        "source_release_manifest_hash": receipt["release"]["source_release_manifest_hash"],
        "replay_manifest_ref": receipt["release"]["replay_manifest_ref"],
        "program_sha256": EXPECTED_PROGRAM_SHA256,
        "release_receipt_sha256": receipt_sha,
        "source_config_path": str(SOURCE_CONFIG_PATH.relative_to(ROOT)),
        "source_config_file_sha256": EXPECTED_CONFIG_FILE_SHA256,
        "source_config_canonical_sha256": EXPECTED_CONFIG_CANONICAL_SHA256,
        "local_bundle": {
            "bundle_id": EXPECTED_BUNDLE_ID,
            "receipt_sha256": EXPECTED_LOCAL_RECEIPT_SHA256,
            "public_objects_sha256": EXPECTED_PUBLIC_SHA256,
            "internal_records_sha256": EXPECTED_INTERNAL_SHA256,
            "replay_manifest_sha256": EXPECTED_REPLAY_SHA256,
            "public_objects_lines": EXPECTED_PUBLIC_LINES,
            "internal_records_lines": EXPECTED_INTERNAL_LINES,
        },
        "field_count": EXPECTED_RESPONSE_FIELDS,
        "held_fields": held_fields,
        "fields": field_records,
        "source_record_denominator": EXPECTED_RECORDS,
        "event_presence_count": EXPECTED_EVENTS,
        "observed_response_denominator_definition": "records whose source response state is SUBSTANTIVE_RESPONSE, DK, REFUSAL or SOURCE_SPECIFIC_SPECIAL; event presence alone is not an answered question",
        "answered_substantive_definition": "records whose source response state is SUBSTANTIVE_RESPONSE",
        "routing_state": "ROUTING_UNKNOWN",
        "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
        "canonical_values_emitted": 0,
        "weight_facts": 0,
        "population_or_eligibility_claims": "NONE",
        "control": {
            "field": control_field,
            "values": control_values,
            "discriminating": True,
            "source_release_unchanged": True,
        },
        "consumer_api": "rawlsing_next.pre553_carrier_execution.materialize_public_object",
        "value_api": "rawlsing_next.pre553_r5_codec.R5TypedValueCodec.decode",
        "materialized_event_count": materialized_events,
        "schema_counts": dict(sorted(schema_counts.items())),
    }
    tally_hash = canonical_sha(material)
    tally_ref = ExactRef("D1_OBSERVED_SAMPLE_TALLY", f"urn:rawlsing:d1:SRC04:observed-sample-tally:{tally_hash}", tally_hash)
    replay_hash = canonical_sha({"tally_ref": tally_ref.as_dict(), "local_bundle": material["local_bundle"]})
    replay_ref = ExactRef("D1_TALLY_REPLAY", f"urn:rawlsing:d1:SRC04:observed-sample-replay:{replay_hash}", replay_hash)
    return {**material, "tally_ref": tally_ref.as_dict(), "replay_ref": replay_ref.as_dict()}


def wrong_release_negative() -> dict[str, Any]:
    receipt = load_json(A_RECEIPT_PATH)
    tampered = deepcopy(receipt)
    tampered["release"]["release_ref"]["content_hash"] = "0" * 64
    try:
        build_tally(receipt_override=tampered)
    except TallyRefusal as exc:
        return {
            "schema": "PYAT_D1_SRC04_WRONG_RELEASE_NEGATIVE@1.0.0",
            "status": "REFUSED",
            "expected": "RELEASE_IDENTITY_MISMATCH",
            "actual_code": exc.code,
            "source_read_performed": False,
            "local_bundle_consumed": False,
        }
    raise TallyRefusal("WRONG_RELEASE_NOT_REFUSED")


def unknown_state_negative() -> dict[str, Any]:
    try:
        classify_state("UNKNOWN_NOT_ADOPTED")
    except TallyRefusal as exc:
        return {
            "schema": "PYAT_D1_SRC04_UNKNOWN_STATE_NEGATIVE@1.0.0",
            "status": "REFUSED",
            "expected": "UNKNOWN_RESPONSE_STATE",
            "actual_code": exc.code,
            "source_release_unchanged": True,
        }
    raise TallyRefusal("UNKNOWN_STATE_NOT_REFUSED")
