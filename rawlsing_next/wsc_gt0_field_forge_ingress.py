"""WSC002C Golden Thread 0 PRE-FF -> FIELD FORGE ingress glue.

This module is deliberately nonsemantic glue. It takes an already governed
PRE-FF GT0 envelope/receipt and records one actor-independent, reference-only
FIELD FORGE ingress hop without transferring semantic ownership or minting a
FIELD FORGE relation.

WSC002C does not own the shared protocol classes. They are imported lazily
from rawlsing_next.wsc_gt0_protocol so this sibling-blind worker can define
and test its import contract independently; central WSC002 integration binds
this module to the WSC002A implementation.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
import hashlib
import importlib
import inspect
import json
import re
from typing import Any, Mapping, Sequence


CONTRACT_ID = "WSC002C_GT0_FIELD_FORGE_INGRESS@1.0.0"
STAGE_ID = "GT0_FIELD_FORGE_INGRESS"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
INGRESS_KIND = "ACTOR_INDEPENDENT_REFERENCE_ONLY"

_FORBIDDEN_STRONG_NOUNS = frozenset({
    "FIELD",
    "FIELD_SPECIFIC_CAPITAL",
    "CAPITAL",
    "HEGEMONY",
    "SUBHEGEMONY",
    "HOMOLOGY",
    "PRESSURE",
    "PRESSURE_FOOTPRINT",
    "PRESSURE_PATHWAY",
    "STRUCTURAL_MECHANISM",
    "MECHANISM",
})
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class GT0FieldForgeIngressError(ValueError):
    """The PRE-FF -> FIELD FORGE GT0 handoff cannot be conserved exactly."""


def _protocol_module():
    try:
        return importlib.import_module("rawlsing_next.wsc_gt0_protocol")
    except ImportError as exc:
        raise GT0FieldForgeIngressError(
            "rawlsing_next.wsc_gt0_protocol is required at integration/runtime"
        ) from exc


def _plain(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise GT0FieldForgeIngressError("floats are forbidden in GT0 conserved identity")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise GT0FieldForgeIngressError("GT0 mapping keys must be strings")
        return {k: _plain(v) for k, v in value.items()}
    if is_dataclass(value):
        return {f.name: _plain(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_plain(v) for v in value]
    if hasattr(value, "as_dict") and callable(value.as_dict):
        return _plain(value.as_dict())
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _plain(value.to_dict())
    if hasattr(value, "__dict__"):
        return {
            k: _plain(v)
            for k, v in vars(value).items()
            if not k.startswith("_")
        }
    raise GT0FieldForgeIngressError(
        f"unsupported GT0 protocol material type: {type(value).__name__}"
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _plain(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _fallback_hash(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _protocol_hash(protocol: Any, value: Any) -> str:
    for name in (
        "deterministic_content_hash",
        "content_hash",
        "semantic_hash",
        "gt0_content_hash",
    ):
        helper = getattr(protocol, name, None)
        if callable(helper):
            digest = helper(value)
            if isinstance(digest, str) and _SHA256.fullmatch(digest):
                return digest
            raise GT0FieldForgeIngressError(
                f"{name} did not return a lowercase sha256 digest"
            )
    return _fallback_hash(value)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    material = _plain(value)
    if not isinstance(material, Mapping):
        raise GT0FieldForgeIngressError(f"{name} must expose mapping-like protocol material")
    return material


def _first(material: Mapping[str, Any], aliases: Sequence[str], name: str) -> Any:
    for key in aliases:
        if key in material:
            return material[key]
    raise GT0FieldForgeIngressError(f"{name} missing from GT0 conservation envelope")


def _optional(material: Mapping[str, Any], aliases: Sequence[str]) -> Any:
    for key in aliases:
        if key in material:
            return material[key]
    return None


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT0FieldForgeIngressError(f"{name} must be a non-empty string")
    out = value.strip()
    if out.lower() in {"latest", "default", "*", "nearest", "fuzzy"}:
        raise GT0FieldForgeIngressError(f"{name} may not use mutable/fuzzy selection")
    return out


def _exact_ref_material(ref: Any) -> dict[str, str]:
    material = _mapping(ref, "upstream ref")
    kind = _optional(material, ("kind", "object_type", "type", "family"))
    object_id = _optional(material, ("object_id", "id", "object_ref", "semantic_id"))
    content_hash = _optional(material, ("content_hash", "hash", "sha256"))
    kind = _text(kind, "upstream ref kind")
    object_id = _text(object_id, "upstream ref object_id")
    content_hash = _text(content_hash, "upstream ref content_hash")
    if not _SHA256.fullmatch(content_hash):
        raise GT0FieldForgeIngressError("upstream ref content_hash must be lowercase sha256")
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def _validate_exact_upstream_refs(protocol: Any, refs: Any) -> tuple[dict[str, str], ...]:
    if isinstance(refs, (str, bytes, bytearray)) or not isinstance(refs, Sequence):
        raise GT0FieldForgeIngressError("exact_upstream_refs must be a sequence")
    canonical = tuple(_exact_ref_material(ref) for ref in refs)
    if not canonical:
        raise GT0FieldForgeIngressError("at least one exact upstream producer ref is required")
    if len({(r["kind"], r["object_id"], r["content_hash"]) for r in canonical}) != len(canonical):
        raise GT0FieldForgeIngressError("duplicate upstream refs are forbidden")

    for name in (
        "validate_exact_upstream_refs",
        "validate_exact_upstream_references",
        "require_exact_upstream_refs",
    ):
        helper = getattr(protocol, name, None)
        if callable(helper):
            helper(refs)
            break
    return canonical


def _status_value(value: Any) -> str:
    if isinstance(value, Enum):
        value = value.value
    return _text(value, "GT0 stage status")


def _status_member(protocol: Any, value: str) -> Any:
    for name in ("GT0StageStatus", "GT0Status", "StageStatus"):
        enum_cls = getattr(protocol, name, None)
        if enum_cls is None:
            continue
        try:
            return enum_cls(value)
        except Exception:
            member = getattr(enum_cls, value, None)
            if member is not None:
                return member
    return value


def _scan_forbidden_strong_nouns(envelope_material: Mapping[str, Any]) -> None:
    fields_to_scan = (
        "semantic_family",
        "semantic_class",
        "relation_query_identity",
        "relation_identity",
        "structural_relation",
        "semantic_claim",
        "claim_kind",
    )
    for field in fields_to_scan:
        if field not in envelope_material:
            continue
        text = _canonical_json(envelope_material[field]).upper()
        tokens = set(re.findall(r"[A-Z][A-Z0-9_]*", text))
        hit = sorted(tokens & _FORBIDDEN_STRONG_NOUNS)
        if hit:
            raise GT0FieldForgeIngressError(
                "GT0 baseline may not mint strong FIELD FORGE nouns: " + ",".join(hit)
            )


def _receipt_refs(receipt_material: Mapping[str, Any]) -> tuple[dict[str, str], ...] | None:
    raw = _optional(
        receipt_material,
        (
            "output_refs",
            "producer_refs",
            "exact_producer_refs",
            "upstream_refs",
            "upstream_references",
        ),
    )
    if raw is None:
        return None
    if isinstance(raw, (str, bytes, bytearray)) or not isinstance(raw, Sequence):
        raise GT0FieldForgeIngressError("PRE-FF receipt refs must be a sequence")
    return tuple(_exact_ref_material(v) for v in raw)


def _construct_receipt(protocol: Any, payload: Mapping[str, Any]) -> Any:
    cls = getattr(protocol, "GT0StageReceipt", None)
    if cls is None:
        raise GT0FieldForgeIngressError("shared protocol does not expose GT0StageReceipt")

    for builder_name in ("from_mapping", "from_dict", "build", "create"):
        builder = getattr(cls, builder_name, None)
        if callable(builder):
            try:
                return builder(dict(payload))
            except TypeError:
                pass

    try:
        sig = inspect.signature(cls)
    except (TypeError, ValueError) as exc:
        raise GT0FieldForgeIngressError("cannot inspect GT0StageReceipt constructor") from exc

    aliases: dict[str, tuple[str, ...]] = {
        "contract_id": ("contract_id",),
        "stage": ("stage", "stage_id", "stage_name"),
        "status": ("status", "typed_status", "stage_status"),
        "upstream_refs": ("upstream_refs", "upstream_references", "input_refs"),
        "output_refs": ("output_refs", "producer_refs", "exact_producer_refs"),
        "input_envelope_hash": ("input_envelope_hash", "envelope_hash"),
        "output_envelope_hash": ("output_envelope_hash",),
        "semantic_owner": ("semantic_owner", "owner", "producer_owner"),
        "scope": ("scope", "scope_identity", "scope_universe_risk_set"),
        "permission": ("permission", "consumer_permission", "permission_ceiling"),
        "typed_state": ("typed_state", "semantic_state"),
        "replay_recipe": ("replay_recipe", "replay", "replay_root"),
        "information_loss": ("information_loss", "information_loss_declaration"),
        "target_use": ("target_use",),
        "details": ("details", "metadata", "payload"),
        "receipt_id": ("receipt_id", "object_id"),
        "content_hash": ("content_hash", "receipt_hash"),
    }

    reverse: dict[str, str] = {}
    for canonical, names in aliases.items():
        for name in names:
            reverse[name] = canonical

    kwargs: dict[str, Any] = {}
    accepts_kwargs = any(
        p.kind is inspect.Parameter.VAR_KEYWORD
        for p in sig.parameters.values()
    )
    for name, param in sig.parameters.items():
        if name == "self" or param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue
        canonical = reverse.get(name)
        if canonical is not None and canonical in payload:
            kwargs[name] = payload[canonical]
        elif param.default is inspect.Parameter.empty:
            raise GT0FieldForgeIngressError(
                f"GT0StageReceipt required field is not covered by WSC002C import contract: {name}"
            )

    if accepts_kwargs:
        for canonical, value in payload.items():
            preferred = aliases.get(canonical, (canonical,))[0]
            kwargs.setdefault(preferred, value)

    try:
        return cls(**kwargs)
    except Exception as exc:
        raise GT0FieldForgeIngressError(
            f"GT0StageReceipt construction failed: {exc}"
        ) from exc


def run_gt0_field_forge_ingress(
    envelope: Any,
    preff_receipt: Any,
    exact_upstream_refs: Sequence[Any],
) -> tuple[Any, Any]:
    """Record baseline F0 FIELD FORGE ingress without creating new meaning.

    Returns (envelope, field_forge_ingress_receipt). The exact same
    conservation-envelope object is returned intentionally: WSC002C is a
    reference-preserving handoff and has no authority to change semantic owner,
    scope, permission, typed state, replay, or information-loss declaration.
    """

    protocol = _protocol_module()
    envelope_cls = getattr(protocol, "GT0ConservationEnvelope", None)
    receipt_cls = getattr(protocol, "GT0StageReceipt", None)
    if envelope_cls is not None and not isinstance(envelope, envelope_cls):
        raise GT0FieldForgeIngressError("envelope must be GT0ConservationEnvelope")
    if receipt_cls is not None and not isinstance(preff_receipt, receipt_cls):
        raise GT0FieldForgeIngressError("preff_receipt must be GT0StageReceipt")

    env = _mapping(envelope, "GT0ConservationEnvelope")
    prior = _mapping(preff_receipt, "GT0StageReceipt")
    refs = _validate_exact_upstream_refs(protocol, exact_upstream_refs)

    semantic_owner = _first(env, ("semantic_owner", "owner", "producer_owner"), "semantic owner")
    scope = _first(env, ("scope", "scope_identity", "scope_universe_risk_set"), "scope/universe/risk-set identity")
    permission = _first(env, ("consumer_permission", "permission", "permission_ceiling"), "consumer permission")
    typed_state = _first(env, ("typed_state", "semantic_state", "status"), "typed state")
    replay_recipe = _first(env, ("replay_recipe", "replay", "replay_root"), "replay recipe")
    information_loss = _first(
        env,
        ("information_loss_declaration", "information_loss"),
        "information-loss declaration",
    )
    if _text(information_loss, "information-loss declaration") != INFORMATION_LOSS:
        raise GT0FieldForgeIngressError(
            "baseline FIELD FORGE ingress requires information-loss=" + INFORMATION_LOSS
        )

    target_use = _optional(env, ("target_use",))
    _scan_forbidden_strong_nouns(env)

    prior_refs = _receipt_refs(prior)
    if prior_refs is not None:
        a = tuple(sorted((r["kind"], r["object_id"], r["content_hash"]) for r in prior_refs))
        b = tuple(sorted((r["kind"], r["object_id"], r["content_hash"]) for r in refs))
        if a != b:
            raise GT0FieldForgeIngressError(
                "exact upstream refs do not match PRE-FF receipt producer/reference closure"
            )

    prior_status = _first(prior, ("status", "typed_status", "stage_status"), "PRE-FF receipt status")
    status_text = _status_value(prior_status)
    status = _status_member(protocol, status_text)

    envelope_hash = _protocol_hash(protocol, envelope)
    details = {
        "ingress_kind": INGRESS_KIND,
        "producer_owner_preserved": True,
        "scope_preserved": True,
        "permission_preserved": True,
        "typed_state_preserved": True,
        "replay_preserved": True,
        "information_loss": INFORMATION_LOSS,
        "new_field_forge_relation_minted": False,
        "strong_noun_admission_minted": False,
        "actor_semantics_minted": False,
    }
    stable_material = {
        "contract_id": CONTRACT_ID,
        "stage": STAGE_ID,
        "status": status_text,
        "upstream_refs": refs,
        "output_refs": refs,
        "input_envelope_hash": envelope_hash,
        "output_envelope_hash": envelope_hash,
        "semantic_owner": semantic_owner,
        "scope": scope,
        "permission": permission,
        "typed_state": typed_state,
        "replay_recipe": replay_recipe,
        "information_loss": INFORMATION_LOSS,
        "target_use": target_use,
        "details": details,
    }
    digest = _protocol_hash(protocol, stable_material)
    payload = dict(stable_material)
    payload["status"] = status
    payload["receipt_id"] = "urn:rawlsing:gt0:field-forge-ingress:sha256:" + digest
    payload["content_hash"] = digest

    receipt = _construct_receipt(protocol, payload)
    return envelope, receipt
