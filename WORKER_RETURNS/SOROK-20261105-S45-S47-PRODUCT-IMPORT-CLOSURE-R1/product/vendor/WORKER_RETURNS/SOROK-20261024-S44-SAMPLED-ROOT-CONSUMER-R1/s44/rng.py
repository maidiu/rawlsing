"""Minimal ADP-020 v1 causal RNG for S44 explicit synthetic roots."""
from __future__ import annotations

import hashlib
import hmac
import json
import unicodedata
from typing import Any, Mapping

from .errors import S44Refusal

AUTHORITY_ID = "ADP-020"
AUTHORITY_VERSION = "1.0.0"
SEED_SCHEME_ID = "V3_CAUSAL_HMAC_SHA256_COUNTER_V1"
SEED_SCHEME_VERSION = "1.0.0"
SAMPLER_ID = "ADP020_HMAC_SHA256_UNIFORM_BELOW_V1"
SAMPLER_VERSION = "1.0.0"
DOMAIN = (
    b"RAWLSING\0ADP-020\0V3_CAUSAL_HMAC_SHA256_COUNTER_V1\0"
)
STREAM_PREFIX = "v3.causal."
MAX_U64 = 2**64


def _nfc(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, Mapping):
        return {_nfc(key): _nfc(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_nfc(item) for item in value]
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        _nfc(value), ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    if isinstance(value, (bytes, bytearray)):
        payload = bytes(value)
    elif isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = canonical_json(value)
    return hashlib.sha256(payload).hexdigest()


def seed_bytes(root_seed: str) -> bytes:
    if not isinstance(root_seed, str) or len(root_seed) != 64:
        raise S44Refusal("S44_ROOT_SEED_INVALID")
    try:
        value = bytes.fromhex(root_seed)
    except ValueError as exc:
        raise S44Refusal("S44_ROOT_SEED_INVALID") from exc
    if len(value) != 32 or root_seed != root_seed.lower():
        raise S44Refusal("S44_ROOT_SEED_INVALID")
    return value


def _hmac(key: bytes, material: Any) -> bytes:
    return hmac.new(key, DOMAIN + canonical_json(material), hashlib.sha256).digest()


def scope_seed(root: bytes, scope_kind: str, scope_id: str) -> bytes:
    if scope_kind not in {"RUN", "ACTOR", "JOINT", "GENEALOGY"}:
        raise S44Refusal("S44_SCOPE_KIND_INVALID", scope_kind)
    return _hmac(root, {
        "kind": "scope", "scope_kind": scope_kind, "scope_id": scope_id,
    })


def stream_seed(scope: bytes, stream_name: str) -> bytes:
    if not stream_name.startswith(STREAM_PREFIX):
        raise S44Refusal("S44_STREAM_NAME_INVALID", stream_name)
    return _hmac(scope, {"kind": "stream", "stream_name": stream_name})


def _uniform_below(stream: bytes, coordinate: Mapping[str, Any], n: int) -> tuple[int, int, int]:
    if not isinstance(n, int) or isinstance(n, bool) or not (1 <= n < MAX_U64):
        raise S44Refusal("S44_DRAW_BOUND_INVALID", str(n))
    limit = MAX_U64 - (MAX_U64 % n)
    blocks = 0
    while True:
        digest = hmac.new(
            stream,
            DOMAIN + canonical_json({
                "coordinate": dict(coordinate), "block_index": blocks,
            }),
            hashlib.sha256,
        ).digest()
        raw = int.from_bytes(digest[:8], "big")
        if raw < limit:
            return raw % n, blocks, raw
        blocks += 1


def _coordinate(rule: Mapping[str, Any], anchor_id: str, draw_index: int = 0) -> dict:
    return {
        "scope_kind": rule["scope_kind"],
        "scope_id": rule["scope_id"],
        "stream_name": rule["stream"],
        "anchor_event_index": -1,
        "anchor_event_id_or_init_checkpoint_hash": anchor_id,
        "rule_invocation_id": "s44.root.initial",
        "decision_slot": rule["rule_id"],
        "occurrence_index": 0,
        "draw_index": draw_index,
    }


REQUIRED_CANDIDATE_FIELDS = (
    "candidate_id",
    "candidate_replay_hash",
    "candidate_authority_id",
    "candidate_authority_version",
    "eligibility_or_admission_receipt_hash",
    "weight_units",
)


def candidate_payload(candidate: Mapping[str, Any]) -> dict:
    return {
        key: value for key, value in candidate.items()
        if key != "candidate_replay_hash"
    }


def candidate_replay_hash(candidate: Mapping[str, Any]) -> str:
    return sha256_hex(candidate_payload(candidate))


def _candidate_set(rule: Mapping[str, Any]) -> dict:
    entries = []
    seen = set()
    for candidate in rule.get("candidates") or []:
        if not isinstance(candidate, Mapping):
            raise S44Refusal("S44_CANDIDATE_INVALID")
        cid = candidate.get("candidate_id")
        if not isinstance(cid, str) or not cid or cid in seen:
            raise S44Refusal("S44_CANDIDATE_INVALID")
        seen.add(cid)
        for field in REQUIRED_CANDIDATE_FIELDS:
            if field not in candidate or candidate.get(field) in (None, ""):
                raise S44Refusal("S44_CANDIDATE_FIELD_MISSING", f"{cid}:{field}")
        weight = candidate.get("weight_units")
        if not isinstance(weight, int) or isinstance(weight, bool) or weight < 0:
            raise S44Refusal("S44_CANDIDATE_WEIGHT_INVALID", cid)
        if candidate["candidate_replay_hash"] != candidate_replay_hash(candidate):
            raise S44Refusal("S44_CANDIDATE_REPLAY_HASH_MISMATCH", cid)
        eligibility_payload = candidate.get("eligibility_payload")
        eligibility_hash = candidate.get("eligibility_or_admission_receipt_hash")
        if isinstance(eligibility_payload, Mapping):
            for field in (
                "candidate_id", "value", "source_ref",
                "candidate_authority_id", "candidate_authority_version",
            ):
                if eligibility_payload.get(field) != candidate.get(field):
                    raise S44Refusal(
                        "S44_CANDIDATE_ELIGIBILITY_PAYLOAD_MISMATCH",
                        f"{cid}:{field}",
                    )
            if eligibility_hash != sha256_hex(eligibility_payload):
                raise S44Refusal(
                    "S44_CANDIDATE_ELIGIBILITY_HASH_MISMATCH", cid
                )
        entries.append(dict(candidate))
    if not rule.get("candidate_owner_authority"):
        raise S44Refusal("S44_CANDIDATE_AUTHORITY_MISSING", rule.get("rule_id", ""))
    if not entries:
        raise S44Refusal("S44_CANDIDATE_SET_EMPTY", rule.get("rule_id", ""))
    if not any(int(row.get("weight_units", 1)) > 0 for row in entries):
        raise S44Refusal("S44_CANDIDATE_SET_ZERO_WEIGHT", rule.get("rule_id", ""))
    entries.sort(key=lambda row: (row["candidate_id"], canonical_json(row)))
    body = {
        "identity_mode": "SET_CANONICAL",
        "candidate_owner_authority": rule.get("candidate_owner_authority", ""),
        "entries": entries,
    }
    body["candidate_set_hash"] = sha256_hex(
        b"ADP020_CANDIDATE_SET_V1\0" + canonical_json(body)
    )
    return body


def _replay_identity(
    *, root_hash: str, scope_hash: str, stream_hash: str, coord: dict,
    rule: Mapping[str, Any], operation: str, params_hash: str,
    candidate_set_hash: str,
) -> str:
    material = {
        "authority_id": AUTHORITY_ID,
        "authority_version": AUTHORITY_VERSION,
        "seed_scheme_id": SEED_SCHEME_ID,
        "seed_scheme_version": SEED_SCHEME_VERSION,
        "sampler_id": SAMPLER_ID,
        "sampler_version": SAMPLER_VERSION,
        "root_seed_sha256": root_hash,
        "scope_seed_sha256": scope_hash,
        "stream_seed_sha256": stream_hash,
        "coordinate": coord,
        "semantic_rule_id": rule["rule_id"],
        "semantic_rule_version": rule["rule_version"],
        "semantic_rule_registry_hash": rule.get("registry_hash", ""),
        "operation": operation,
        "stochastic_parameters_hash": params_hash,
        "candidate_set_hash": candidate_set_hash,
    }
    return sha256_hex(b"ADP020_DECISION_REPLAY_V1\0" + canonical_json(material))


def _base_receipt(
    *, root: bytes, bundle_hash: str, rule: Mapping[str, Any],
    operation: str, params: Mapping[str, Any], candidate_set: dict | None,
) -> tuple[dict, bytes, dict, bytes]:
    root_hash = hashlib.sha256(root).hexdigest()
    scope = scope_seed(root, rule["scope_kind"], rule["scope_id"])
    stream = stream_seed(scope, rule["stream"])
    coord = _coordinate(rule, "INIT:" + hashlib.sha256(root).hexdigest())
    params_hash = sha256_hex(params)
    candidate_hash = (candidate_set or {}).get("candidate_set_hash", "")
    replay_hash = _replay_identity(
        root_hash=root_hash,
        scope_hash=hashlib.sha256(scope).hexdigest(),
        stream_hash=hashlib.sha256(stream).hexdigest(),
        coord=coord,
        rule=rule,
        operation=operation,
        params_hash=params_hash,
        candidate_set_hash=candidate_hash,
    )
    receipt = {
        "schema": "ADP020_DECISION_RECEIPT_V1",
        "authority": {"id": AUTHORITY_ID, "version": AUTHORITY_VERSION},
        "seed_scheme": {"id": SEED_SCHEME_ID, "version": SEED_SCHEME_VERSION},
        "sampler": {"id": SAMPLER_ID, "version": SAMPLER_VERSION},
        "root_seed_sha256": root_hash,
        "scope_kind": rule["scope_kind"],
        "scope_id": rule["scope_id"],
        "scope_seed_sha256": hashlib.sha256(scope).hexdigest(),
        "stream_name": rule["stream"],
        "stream_seed_sha256": hashlib.sha256(stream).hexdigest(),
        "coordinate": coord,
        "semantic_rule_id": rule["rule_id"],
        "semantic_rule_version": rule["rule_version"],
        "semantic_rule_registry_hash": rule.get("registry_hash", ""),
        "operation": operation,
        "stochastic_parameters_hash": params_hash,
        "candidate_set_hash": candidate_hash,
        "decision_replay_identity_hash": replay_hash,
        "native": False,
        "psychology_claim": False,
    }
    return receipt, scope, coord, stream


def draw_candidate(
    root_seed: str, *, bundle_hash: str, rule: Mapping[str, Any],
    conditional_value: Any = None,
) -> tuple[dict, Any]:
    root = seed_bytes(root_seed)
    cset = _candidate_set(rule)
    weights = [int(row.get("weight_units", 1)) for row in cset["entries"]]
    total = sum(weights)
    params = {"operation": "WEIGHTED_CANDIDATE_INTEGER", "total_weight": total}
    receipt, scope, coord, stream = _base_receipt(
        root=root, bundle_hash=bundle_hash, rule=rule,
        operation="WEIGHTED_CANDIDATE_INTEGER", params=params,
        candidate_set=cset,
    )
    receipt["candidate_set"] = cset
    if total <= 1:
        selected = next(row for row in cset["entries"]
                        if int(row.get("weight_units", 1)) > 0)
        receipt.update({
            "draw_consumed": False,
            "selected_candidate_id": selected["candidate_id"],
            "selected_candidate_replay_hash": selected["candidate_replay_hash"],
            "selected_value": selected.get("value"),
            "entropy_block_count": 0,
        })
    else:
        value, blocks, raw = _uniform_below(stream, coord, total)
        cursor = 0
        selected = None
        for row in cset["entries"]:
            cursor += int(row.get("weight_units", 1))
            if value < cursor:
                selected = row
                break
        if selected is None:
            raise S44Refusal("S44_DRAW_SELECTION_MISSING")
        receipt.update({
            "draw_consumed": True,
            "uniform_value": value,
            "selected_candidate_id": selected["candidate_id"],
            "selected_candidate_replay_hash": selected["candidate_replay_hash"],
            "selected_value": selected.get("value"),
            "entropy_block_count": blocks,
            "accepted_raw_u64": raw,
            "uniform_below_n": total,
            "mapped_result": selected["candidate_id"],
            "draw_coordinate_hash": sha256_hex(coord),
            "draw_receipt": {
                "schema": "ADP020_DRAW_RECEIPT_V1",
                "draw_index": 0,
                "entropy_block_count": blocks,
                "uniform_below_n": total,
                "accepted_raw_u64": raw,
                "mapped_result": selected["candidate_id"],
                "draw_coordinate_hash": sha256_hex(coord),
            },
        })
        receipt["draw_receipt"]["draw_replay_hash"] = sha256_hex({
            "coordinate": coord,
            "draw_receipt": receipt["draw_receipt"],
        })
    if conditional_value is not None:
        receipt["conditioned_on_value"] = conditional_value
    return receipt, receipt["selected_value"]


def draw_bernoulli(
    root_seed: str, *, bundle_hash: str, rule: Mapping[str, Any],
    numerator: int, denominator: int, conditional_value: Any = None,
) -> tuple[dict, bool]:
    if (
        not isinstance(numerator, int) or not isinstance(denominator, int)
        or isinstance(numerator, bool) or isinstance(denominator, bool)
        or denominator <= 0 or numerator < 0 or numerator > denominator
    ):
        raise S44Refusal("S44_BERNOULLI_INVALID")
    root = seed_bytes(root_seed)
    params = {"operation": "BERNOULLI_RATIONAL",
              "numerator": numerator, "denominator": denominator}
    receipt, _, coord, stream = _base_receipt(
        root=root, bundle_hash=bundle_hash, rule=rule,
        operation="BERNOULLI_RATIONAL", params=params, candidate_set=None,
    )
    if numerator in {0, denominator}:
        value = numerator == denominator
        receipt.update({
            "draw_consumed": False, "selected_value": value,
            "entropy_block_count": 0,
        })
    else:
        draw, blocks, raw = _uniform_below(stream, coord, denominator)
        value = draw < numerator
        receipt.update({
            "draw_consumed": True, "uniform_value": draw,
            "selected_value": value, "entropy_block_count": blocks,
            "uniform_below_n": denominator, "accepted_raw_u64": raw,
            "mapped_result": value, "draw_coordinate_hash": sha256_hex(coord),
            "draw_receipt": {
                "schema": "ADP020_DRAW_RECEIPT_V1",
                "draw_index": 0,
                "entropy_block_count": blocks,
                "uniform_below_n": denominator,
                "accepted_raw_u64": raw,
                "mapped_result": value,
                "draw_coordinate_hash": sha256_hex(coord),
            },
        })
        receipt["draw_receipt"]["draw_replay_hash"] = sha256_hex({
            "coordinate": coord,
            "draw_receipt": receipt["draw_receipt"],
        })
    if conditional_value is not None:
        receipt["conditioned_on_value"] = conditional_value
    return receipt, value


__all__ = [
    "AUTHORITY_ID", "AUTHORITY_VERSION", "SEED_SCHEME_ID", "SAMPLER_ID",
    "canonical_json", "sha256_hex", "seed_bytes", "scope_seed", "stream_seed",
    "candidate_payload", "candidate_replay_hash", "REQUIRED_CANDIDATE_FIELDS",
    "draw_candidate", "draw_bernoulli",
]
