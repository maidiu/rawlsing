"""RFA-06B R2 contract and identity-aligned transport; offline helpers, no API calls."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / "render_inputs_r1"
LAB = HERE.parent / "lab_fixture"
RAW = HERE / "results" / "raw"
BLINDED = HERE / "results" / "blinded"
RECEIPTS = HERE / "results" / "receipts"
FREEZE = HERE / "EXPERIMENT_FREEZE_R2.json"
IDS = [f"RF{i:03d}" for i in range(1, 11)]
FORBIDDEN = (
    "audit_metadata_NOT_FOR_MODEL", "evaluator_only_oracle",
    "evaluator_only_hidden_causal_summary", "objective_truth_register",
    "user_phenomenal_output", "user_attention_recognition_access",
    "Mara accepted a job", "closing 18:00",
)
RUN_RE = re.compile(r"^(R2RUN-\d{4}|R2SMOKE-0001)-A(\d{4})\.json$")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(value):
    """Stable UTF-8 encoding; preserves inherited JSON object-key order, no changes to content."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def file_sha256(path):
    return sha256(Path(path).read_bytes())


def git_blob_sha1(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_blob(path, expected):
    require(Path(path).is_file(), f"MISSING_SOURCE: {path.name}")
    actual = git_blob_sha1(Path(path).read_bytes())
    require(actual == expected, f"SOURCE_BLOB_MISMATCH: {path.name}: expected {expected}, got {actual}")


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def sdk_version():
    try:
        return version("anthropic")
    except PackageNotFoundError:
        return "NOT_INSTALLED"


def config():
    c = read(HERE / "EXPERIMENT_CONFIG_R2.json")
    require(c["model"] == "claude-opus-5-5" and c["effort"] == "high", "MODEL_OR_EFFORT_DRIFT")
    require(c["sdk_version"] == "1.13.0" and c["primary_runs"] == 60 and c["api_version"] == "2023-06-01", "CONFIG_DRIFT")
    require(c["temperature"] is None and c["top_p"] is None and c["top_k"] is None
            and c["system_message"] is None, "UNAPPROVED_SAMPLING_OR_SYSTEM_MESSAGE")
    require(c["provider_seed_status"] == "UNSUPPORTED_BY_PINNED_BINDING", "PROVIDER_SEED_DRIFT")
    require(c["court_revision"] == "R2" and c["run_id_prefix"] == "R2RUN-"
            and c["smoke_run_id"] == "R2SMOKE-0001", "COURT_NAMESPACE_DRIFT")
    require(c["transport_wrapper_keys"] == ["required_fixture_id", "transport_instruction", "model_payload"]
            and c["identity_instruction"] == "Set output.fixture_id exactly equal to required_fixture_id.",
            "IDENTITY_TRANSPORT_CONTRACT_DRIFT")
    return c


def original_schema(c):
    path = HERE / c["output_schema_path"]
    verify_blob(path, c["output_schema_git_blob_sha1"])
    s = read(path)
    Draft202012Validator.check_schema(s)
    return s


def transport_schema(s):
    """API-supported grammar projection; unsupported limits remain binding locally."""
    allowed = {"type", "properties", "items", "required", "additionalProperties",
               "const", "enum", "description", "pattern", "$defs", "$ref",
               "anyOf", "allOf"}
    nontransport = {"minimum", "maximum", "multipleOf", "minLength", "maxLength",
                    "minItems", "maxItems", "uniqueItems"}
    def convert(obj):
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        if not isinstance(obj, dict):
            return obj
        result = {}
        for k, v in obj.items():
            if k in ("properties", "$defs", "definitions"):
                # Keys in a schema's property/definition table are field names,
                # not JSON Schema keywords; NEVER filter those names.
                result[k] = {name: convert(member) for name, member in v.items()}
            elif k in allowed:
                result[k] = convert(v)
        extra = {k: obj[k] for k in nontransport if k in obj}
        if extra:
            # The same schema guidance goes to both arms. Full constraint validation
            # against untouched original_schema is mandatory after the response.
            label = "Original-schema constraints (enforced locally): " + json.dumps(
                extra, sort_keys=True, separators=(",", ":"))
            result["description"] = ((result.get("description", "") + " " + label).strip())
        if "properties" in obj:
            require("properties" in result and
                    set(result["properties"]) == set(obj["properties"]),
                    "TRANSPORT_NESTED_PROPERTIES_LOST")
        return result
    t = convert(s)
    require(t["type"] == "object" and t["additionalProperties"] is False, "INVALID_TRANSPORT_SCHEMA")
    require(set(t["properties"]) == set(s["properties"]), "TRANSPORT_PROPERTY_DRIFT")
    return t


def execution_manifest(c):
    e = read(HERE / "EXECUTION_MANIFEST_PRIVATE_R2.json")
    b = read(HERE / "BLINDED_SCORING_MANIFEST_R2.json")
    runs = e["runs"]
    require(e["run_count"] == b["run_count"] == len(runs) == 60, "BAD_MANIFEST_SIZE")
    require(e["seed"] == c["order_seed"] and e["source_r1_sealed_start"] == c["identity_repair_from"], "ORDER_SEED_DRIFT")
    require([r["run_id"] for r in runs] == [f"R2RUN-{i:04d}" for i in range(1,61)],
            "NONOPAQUE_OR_NONCONTIGUOUS_RUN_IDS")
    require(b["runs"] == [{"run_id": r["run_id"]} for r in runs], "BLINDING_MISMATCH")
    require(Counter((r["case_id"], r["condition"]) for r in runs) ==
            Counter({(id_, arm): 3 for id_ in IDS for arm in ("WP", "N")}), "PAIR_REPLICATION_MISMATCH")
    require(Counter((r["case_id"], r["condition"], r["replicate"]) for r in runs) ==
            Counter({(id_, arm, rep): 1 for id_ in IDS for arm in ("WP", "N") for rep in range(1,4)}),
            "DUPLICATE_REPLICATION")
    # Reproduce the scheduling shuffle, independent from provider stochasticity.
    proposed = [(id_, arm, rep) for id_ in IDS for arm in ("WP", "N") for rep in range(1,4)]
    state = int(c["order_seed"], 16)
    for i in range(59, 0, -1):
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        j = state % (i + 1)
        proposed[i], proposed[j] = proposed[j], proposed[i]
    require([(r["case_id"], r["condition"], r["replicate"]) for r in runs] == proposed,
            "RANDOMIZED_ORDER_MISMATCH")
    require(set(b) == {"kind", "run_count", "runs"}, "BLIND_MANIFEST_EXTRA_FIELDS")
    require(all(set(row) == {"run_id"} and isinstance(row["run_id"], str)
                for row in b["runs"]), "PRIVATE_MAPPING_IN_BLIND_MANIFEST")
    return runs


def verify_inputs(c):
    rows = read(INPUT / "INPUT_PARITY_MANIFEST_R1.json")["cases"]
    verify_blob(INPUT / "INPUT_PARITY_MANIFEST_R1.json", c["parity_manifest_git_blob_sha1"])
    input_schema_path = INPUT / "RENDER_INPUT_SCHEMA_R1.json"
    verify_blob(input_schema_path, c["input_git_blob_sha1"][input_schema_path.name])
    packet_validator = Draft202012Validator(read(input_schema_path))
    schema = original_schema(c)
    require(len(rows) == 10 and {r["case_id"] for r in rows} == set(IDS), "PARITY_CASES_INCOMPLETE")
    payload_hashes = {}
    packet_hashes = {}
    for id_ in IDS:
        source = LAB / f"{id_}.json"
        verify_blob(source, c["source_case_git_blob_sha1"][source.name])
        origin = read(source)
        packets = {}
        for arm in ("N", "WP"):
            filename = f"{id_}_{arm}.json"
            p = INPUT / filename
            verify_blob(p, c["input_git_blob_sha1"][filename])
            packet = read(p)
            errors = list(packet_validator.iter_errors(packet))
            require(not errors, f"PACKET_SCHEMA_FAIL: {filename}: {errors[0].message if errors else ''}")
            require(packet["packet_id"] == f"{id_}_{arm}", f"PACKET_ID_DRIFT: {filename}")
            require(packet["condition"] ==
                    ("WHOLE_PERSON_UPPER_BOUND" if arm == "WP" else "NARROW_CONTEXT_ABLATION"),
                    f"PACKET_CONDITION_DRIFT: {filename}")
            require(packet["audit_metadata_NOT_FOR_MODEL"]["send_only"] == "model_payload",
                    f"WRONG_SEND_PARTITION: {filename}")
            payload = packet["model_payload"]
            require(set(payload) == ({"shared", "whole_person_extension"} if arm == "WP" else {"shared"}),
                    f"PAYLOAD_EXTENSION_DRIFT: {filename}")
            require(payload["shared"]["output_schema"] == {k: v for k, v in schema.items() if k != "x-local-admission-contract"}, f"OUTPUT_SCHEMA_DRIFT: {filename}")
            transmitted = canonical(payload)
            for marker in FORBIDDEN:
                require(marker not in transmitted.decode("utf-8"), f"FORBIDDEN_INPUT: {id_} {marker}")
            packet_hashes[filename] = file_sha256(p)
            payload_hashes[filename] = sha256(transmitted)
            packets[arm] = packet
        n, w = packets["N"], packets["WP"]
        ns, ws = n["model_payload"]["shared"], w["model_payload"]["shared"]
        require(canonical(ns) == canonical(ws), f"PAIR_SHARED_PARITY_FAIL: {id_}")
        assert_source = origin["expression_action_constraints"]["value"]["actor_safe_projection"]
        require(ns["actor_projection_exact_from_RFA05"] == assert_source, f"NARROW_CHANGED: {id_}")
        require(ns["exact_user_event"]["exact_speech"] == origin["exact_user_event"]["value"]["exact_speech"],
                f"EXACT_EVENT_CHANGED: {id_}")
        refs = [v["source_ref"] for v in ns["scene"]["facts"]]
        require(refs == assert_source["scene_documented_refs"] and
                not (set(refs) & {"W09", "W10", "W11"}), f"WORLD_ACCESS_FAIL: {id_}")
        row = next(x for x in rows if x["case_id"] == id_)
        require(row["source_case_sha"] == c["source_case_git_blob_sha1"][f"{id_}.json"],
                f"SOURCE_CASE_MANIFEST_DRIFT: {id_}")
        for arm in ("N", "WP"):
            expected_bytes = row["sizes"][arm]["bytes"]
            got_bytes = len(canonical(packets[arm]["model_payload"]))
            require(expected_bytes == got_bytes,
                    f"MODEL_PAYLOAD_PARITY_SIZE_FAIL {id_}_{arm}: {got_bytes} vs {expected_bytes}")
    require(read(INPUT / "RF008_N.json")["model_payload"]["shared"]["exact_user_event"]["exact_speech"] ==
            read(INPUT / "RF009_N.json")["model_payload"]["shared"]["exact_user_event"]["exact_speech"],
            "RF008_RF009_UTTERANCE_MISMATCH")
    return packet_hashes, payload_hashes


def request_specific_provider_schema(case_id, transport):
    """Execution-only const binding; never mutate the authoritative source schema."""
    require(case_id in IDS, f"UNKNOWN_REQUIRED_FIXTURE_ID: {case_id}")
    p = copy.deepcopy(transport)
    fixture = p["properties"]["fixture_id"]
    require(set(fixture) == {"enum"} and fixture["enum"] == IDS,
            "GLOBAL_FIXTURE_ENUM_SOURCE_CHANGED")
    p["properties"]["fixture_id"] = {"const": case_id}
    require(p["required"] == read(LAB / "OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json")["required"],
            "REQUEST_PROVIDER_SCHEMA_REQUIRED_KEYS_DRIFT")
    return p


def identity_alignment(run, c, transport):
    """Assert visible ID == provider const == manifest case == local validator target."""
    request, request_sha, transmitted_sha, packet = request_for(run, c, transport)
    msg = json.loads(request["messages"][0]["content"])
    binding = request["output_config"]["format"]["schema"]["properties"]["fixture_id"]
    require(set(msg) == set(c["transport_wrapper_keys"]), "TRANSPORT_WRAPPER_FIELD_DRIFT")
    require(msg["required_fixture_id"] == binding["const"] == run["case_id"],
            f"IDENTITY_ALIGNMENT_FAILURE: {run['run_id']}")
    require(msg["transport_instruction"] == c["identity_instruction"], "IDENTITY_INSTRUCTION_DRIFT")
    require(msg["model_payload"] == read(INPUT / packet)["model_payload"],
            f"SEMANTIC_PAYLOAD_CHANGED: {run['run_id']}")
    require("condition" not in msg and "replicate" not in msg,
            "TRANSPORT_REVEALS_EXPERIMENT_ASSIGNMENT")
    require(request_sha == sha256(canonical(request))
            and transmitted_sha == sha256(request["messages"][0]["content"].encode("utf-8")),
            "REQUEST_IDENTITY_HASH_MISMATCH")
    return True


def request_for(run, c, t):
    packet_name = run["case_id"] + "_" + run["condition"] + ".json"
    payload = read(INPUT / packet_name)["model_payload"]
    identity = run["case_id"]
    require(identity in IDS and run["condition"] in ("WP", "N"), "BAD_INPUT_ID_OR_ARM")
    # Only transport bookkeeping is new. The decoded model_payload remains exact RFA-05B.
    envelope = {"required_fixture_id": identity,
                "transport_instruction": c["identity_instruction"],
                "model_payload": payload}
    require(list(envelope) == c["transport_wrapper_keys"], "ENVELOPE_KEYS_DRIFT")
    content = canonical(envelope).decode("utf-8")
    require(json.loads(content)["model_payload"] == payload, "SEMANTIC_PAYLOAD_SERIALIZER_DRIFT")
    require(not any(x in content for x in FORBIDDEN), "PROHIBITED_MODEL_INPUT")
    bound_schema = request_specific_provider_schema(identity, t)
    request = {
        "model": c["model"], "max_tokens": c["max_tokens"],
        "output_config": {"effort": c["effort"], "format": {"type": "json_schema", "schema": bound_schema}},
        "messages": [{"role": "user", "content": content}]
    }
    require(set(request) == {"model", "max_tokens", "output_config", "messages"},
            "EXTRA_PROVIDER_PARAMETER")
    return request, sha256(canonical(request)), sha256(content.encode("utf-8")), packet_name


def deterministic_candidate(candidate, case_id, refs):
    """Structural checks only; not an admission decision or character score."""
    problems = []
    if candidate.get("fixture_id") != case_id:
        problems.append("WRONG_FIXTURE_ID")
    atoms = candidate.get("atoms", [])
    times = [a.get("relative_ms") for a in atoms if isinstance(a, dict)]
    if len(times) != len(atoms) or any(type(n) is not int or n < 0 or n > 30000 for n in times):
        problems.append("ATOM_TIME_OUT_OF_BOUNDS")
    if times != sorted(times):
        problems.append("ATOM_TIME_NONMONOTONIC")
    if len([a.get("atom_id") for a in atoms]) != len(set(a.get("atom_id") for a in atoms)):
        problems.append("ATOM_ID_DUPLICATE")
    permitted = set(refs) | {"NADIA", "P0"}
    for a in atoms:
        if not set(a.get("referent_ids", [])) <= permitted:
            problems.append("UNKNOWN_ATOM_REFERENT")
    for effect in candidate.get("world_effect_proposals", []):
        if effect.get("referent_id") not in refs:
            problems.append("UNKNOWN_WORLD_EFFECT_REFERENT")
    speech = [a.get("content") for a in atoms if a.get("kind") == "SPEECH"]
    prose = candidate.get("realization_prose", "")
    quoted = [a or b for a, b in re.findall(r"\u201c([^\u201d]*)\u201d|\"([^\"]*)\"", prose)]
    if quoted != speech:
        problems.append("SPEECH_PROSE_EXACT_QUOTATION_MISMATCH")
    return sorted(set(problems))


def evidence_files():
    RAW.mkdir(parents=True, exist_ok=True)
    BLINDED.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    paths = sorted(RAW.glob("*.json"))
    for p in paths:
        require(RUN_RE.fullmatch(p.name), f"UNRECOGNIZED_RAW_EVIDENCE_FILENAME: {p.name}")
        r = read(p)
        require(p.name == r.get("attempt_id", "") + ".json",
                f"ATTEMPT_FILE_ID_COLLISION: {p.name}")
        require(r.get("run_id") == r["attempt_id"].rsplit("-A", 1)[0],
                f"ATTEMPT_RUN_MISMATCH: {p.name}")
    return paths


def atomic_new_json(path, value):
    """Exclusive atomic publish: never overwrite prior evidence, even under concurrent processes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(tmp, path)  # fails if target exists, without replacement
    finally:
        Path(tmp).unlink(missing_ok=True)


def freeze_inputs(c, packet_hashes, payload_hashes, transport):
    files = ("run_anthropic_renderer_court_r2.py", "court_common_r2.py",
             "validate_renderer_court_r2.py", "requirements.txt", "README.md",
             "ANTHROPIC_BINDING_RECEIPT_R2.md",
             "R1_ABORT_AND_DEFECT_RECEIPT_R1.md",
             "OUTPUT_REQUIREMENT_AUDIT_R2.md",
             "STATIC_VERIFICATION_RECEIPT_R2.md",
             "LOCAL_EXECUTION_INSTRUCTIONS_R2.md",
             "EXPERIMENT_CONFIG_R2.json", "EXECUTION_MANIFEST_PRIVATE_R2.json",
             "BLINDED_SCORING_MANIFEST_R2.json")
    return {
        "experiment": c["experiment"], "model": c["model"], "effort": c["effort"],
        "max_tokens": c["max_tokens"], "sdk_version": sdk_version(),
        "api_contract": c["api_endpoint"], "api_version": c["api_version"], "provider_binding": "ANTHROPIC",
        "packet_raw_sha256": packet_hashes, "model_payload_sha256": payload_hashes,
        "output_schema_sha256": file_sha256(HERE / c["output_schema_path"]),
        "api_transport_schema_sha256": sha256(canonical(transport)),
        "file_sha256": {f: file_sha256(HERE / f) for f in files},
    }


def assert_freeze(fingerprint):
    require(FREEZE.is_file(), "MISSING_FREEZE: run --freeze before any primary/smoke call")
    frozen = read(FREEZE)
    require(frozen["fingerprints"] == fingerprint, "FROZEN_EXPERIMENT_DRIFT: close this version")
    return frozen


def verify_static(key_required=False, sdk_required=False):
    c = config()
    runs = execution_manifest(c)
    packet_hashes, payload_hashes = verify_inputs(c)
    schema = original_schema(c)
    t = transport_schema(schema)
    if sdk_required:
        require(sdk_version() == c["sdk_version"], f"SDK_VERSION_MISMATCH: install requirements.txt")
    if key_required:
        require(bool(os.getenv("ANTHROPIC_API_KEY")),
                "ANTHROPIC_API_KEY absent: export it in the local shell; never save it to the repository")
    for p in (RAW, BLINDED, RECEIPTS):
        p.mkdir(parents=True, exist_ok=True)
        require(os.access(p, os.W_OK), f"RESULT_DIRECTORY_NOT_WRITABLE: {p}")
    files = evidence_files()
    # The R2 identity must be triple-bound for every primary run and smoke,
    # before any provider call is permitted.
    for run in runs:
        identity_alignment(run, c, t)
    identity_alignment({"run_id": "R2SMOKE-0001", "case_id": "RF001",
                        "condition": "N", "replicate": 0}, c, t)
    # Resume gate: every existing attempt must still belong to this exact
    # sealed request and input. Never mingle receipts from a different freeze.
    by_id = {r["run_id"]: r for r in runs}
    by_id["R2SMOKE-0001"] = {"run_id": "R2SMOKE-0001", "case_id": "RF001",
                           "condition": "N", "replicate": 0}
    seen_provider_ids = set()
    for path in files:
        prior = read(path)
        rid = prior["run_id"]
        require(rid in by_id, f"FOREIGN_RUN_COLLISION: {path.name}")
        planned = by_id[rid]
        _, expected_hash, expected_payload_hash, expected_packet = request_for(planned, c, t)
        require(prior.get("request_identity_sha256") == expected_hash and
                prior.get("transmitted_user_message_sha256") == expected_payload_hash and
                prior.get("model_payload_sha256") ==
                sha256(canonical(read(INPUT / expected_packet)["model_payload"])) and
                prior.get("input_packet_file") == expected_packet and
                prior.get("input_packet_raw_sha256") ==
                file_sha256(INPUT / expected_packet), f"REQUEST_IDENTITY_COLLISION: {path.name}")
        require(prior.get("model") == c["model"] and prior.get("effort") == c["effort"] and
                prior.get("max_tokens") == c["max_tokens"] and
                prior.get("api_version") == c["api_version"] and
                prior.get("sdk_version") == c["sdk_version"] and
                prior.get("case_id") == planned["case_id"] and
                prior.get("condition") == planned["condition"] and
                prior.get("replicate_ordinal") == planned["replicate"],
                f"ATTEMPT_BINDING_COLLISION: {path.name}")
        pid = prior.get("provider_message_id")
        if pid:
            require(pid not in seen_provider_ids, f"REUSED_PROVIDER_MESSAGE_ID: {pid}")
            seen_provider_ids.add(pid)
    # If the key is present, ensure it has not accidentally been serialized into static artifacts.
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if key and len(key) >= 8:
        static_names = ["EXPERIMENT_CONFIG_R2.json", "EXECUTION_MANIFEST_PRIVATE_R2.json",
                        "BLINDED_SCORING_MANIFEST_R2.json", "ANTHROPIC_BINDING_RECEIPT_R2.md",
                        "run_anthropic_renderer_court_r2.py", "court_common_r2.py",
                        "validate_renderer_court_r2.py"]
        for name in static_names:
            require(key not in (HERE / name).read_text(encoding="utf-8"),
                    f"API_KEY_SERIALIZED_IN_{name}")
    return c, runs, t, packet_hashes, payload_hashes, files
