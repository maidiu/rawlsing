from __future__ import annotations
import hashlib, json, unicodedata
from typing import Any

SET_LIKE_FIELDS = {
    "member_ids", "component_ids", "attachment_projection_ids", "diagnostic_flags",
    "closure_obligation_ids", "variant_ids", "exclusion_ids", "evidence_ids",
    "response_topologies", "collision_ids", "exact_evidence_links", "excluded_object_ids",
    "left_member_ids", "right_member_ids", "connectivity_projection_ids", "excluded_member_ids"
}

def _norm_string(value: str) -> str:
    return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))

def canonicalize(value: Any, field_name: str | None = None) -> Any:
    if isinstance(value, float):
        raise TypeError("canonical P3 authority serialization forbids binary floating-point values")
    if isinstance(value, str):
        return _norm_string(value)
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, dict):
        return {k: canonicalize(value[k], k) for k in sorted(value)}
    if isinstance(value, list):
        items=[canonicalize(v, None) for v in value]
        if field_name in SET_LIKE_FIELDS:
            encoded=[json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")) for v in items]
            if len(encoded)!=len(set(encoded)):
                raise ValueError(f"duplicate entry in set-like field {field_name}")
            items=[v for _,v in sorted(zip(encoded,items),key=lambda x:x[0])]
        return items
    raise TypeError(f"unsupported canonical JSON type: {type(value).__name__}")

def canonical_bytes(value: Any) -> bytes:
    normalized=canonicalize(value)
    return json.dumps(normalized,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")

def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()
