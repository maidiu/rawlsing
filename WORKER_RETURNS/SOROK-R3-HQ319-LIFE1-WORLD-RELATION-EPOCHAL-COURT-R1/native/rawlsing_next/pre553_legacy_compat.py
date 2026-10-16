"""Fail-closed PRE553 legacy compatibility/parity adapter.

R14 migrates intentionally retained *meaning*, never legacy runtime behavior.
The adapter deliberately does not import, discover, parse, or execute V550-V552
modules/artifacts. A caller must first produce a canonical semantic projection
and an exact parity receipt under a named, pinned authority. Artifact shape,
ancestry, filenames, field names, numeric coincidence, or provenance reachability
cannot create parity here.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from types import MappingProxyType
from typing import Any, Mapping

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

P04_ACCEPTED_RETURN_COMMIT = "03b2feb6fb9a55c2481f04fd7f996cabf208252d"
P04_COMPATIBILITY_CONTRACT_ID = "PRE553_P04_CURRENT_PRODUCER_COMPATIBILITY_MATRIX"
P04_COMPATIBILITY_CONTRACT_VERSION = "R1"

V550_V551_AUTHORITY_ID = "V550_V551_RESPONSE_SEMANTICS_INFRASTRUCTURE_SEAM_R1"
V550_V551_AUTHORITY_VERSION = "v1"
V550_V551_AUTHORITY_SHA256 = "3a04a9e689b5d027e501a1cc165093773407338313feb25e86c2356ea752b704"

R1_AUTHORITY_ID = "22_shared_respondent_relation_manifest.R1.json"
R1_AUTHORITY_VERSION = "R1"
R1_STUDY_KEY = "ATP_W135"
R1_SOURCE_FILE_SHA256 = "6cec90ec72df360341236f7634d5d76c9a0604168d4174a03e8b8efd388bbbae"
R1_AUTHORITY_MANIFEST_SHA256 = "84009652424d200ced06933173eb8b2f8fb89d51f7909d3da40f6f59ad5da9d9"
R1_RESPONDENT_LINKAGE_MODE = "SOURCE_BACKED_EXACT_KEYS"


class LegacyFamily(str, Enum):
    V550 = "V550"
    V550J = "V550J"
    V551 = "V551"
    V551J = "V551J"
    V552 = "V552"
    V552J = "V552J"
    R1 = "R1"


class ParityClass(str, Enum):
    EXACT_PARITY = "EXACT_PARITY"
    DENIED = "DENIED"
    DEFERRED = "DEFERRED"
    NONPARITY = "NONPARITY"


@dataclass(frozen=True)
class AuthorityPin:
    authority_id: str
    authority_version: str
    authority_content_hash: str


@dataclass(frozen=True)
class MappingRule:
    mapping_id: str
    legacy_family: LegacyFamily
    target_semantic_kind: str
    authority_pin: AuthorityPin | None
    enabled: bool
    deferred_reason: str | None = None


_V550_V551_PIN = AuthorityPin(
    V550_V551_AUTHORITY_ID,
    V550_V551_AUTHORITY_VERSION,
    V550_V551_AUTHORITY_SHA256,
)
_R1_PIN = AuthorityPin(
    R1_AUTHORITY_ID,
    R1_AUTHORITY_VERSION,
    R1_AUTHORITY_MANIFEST_SHA256,
)

# Only mappings for which P04 names a sufficient exact authority are enabled.
# J/non-J and V552-family carrier equivalence remains deliberately deferred.
_MAPPING_RULES = {
    "V550_RESPONSE_SEMANTICS_EXACT": MappingRule(
        "V550_RESPONSE_SEMANTICS_EXACT",
        LegacyFamily.V550,
        "PRE553_RESPONSE_SEMANTIC_PROJECTION",
        _V550_V551_PIN,
        True,
    ),
    "V551_METRIC_SOURCE_STATE_EXACT": MappingRule(
        "V551_METRIC_SOURCE_STATE_EXACT",
        LegacyFamily.V551,
        "PRE553_METRIC_SOURCE_STATE_PROJECTION",
        _V550_V551_PIN,
        True,
    ),
    "R1_ATP_W135_SHARED_RESPONDENT_RELATION_EXACT": MappingRule(
        "R1_ATP_W135_SHARED_RESPONDENT_RELATION_EXACT",
        LegacyFamily.R1,
        "PRE553_SHARED_RESPONDENT_RELATION_PROJECTION",
        _R1_PIN,
        True,
    ),
    "V550J_OBJECT_PARITY": MappingRule(
        "V550J_OBJECT_PARITY", LegacyFamily.V550J, "PRE553_SEMANTIC_PROJECTION",
        None, False, "P04_DOES_NOT_NAME_OBJECT_SPECIFIC_J_NEUTRALITY_AUTHORITY",
    ),
    "V551J_OBJECT_PARITY": MappingRule(
        "V551J_OBJECT_PARITY", LegacyFamily.V551J, "PRE553_SEMANTIC_PROJECTION",
        None, False, "P04_DOES_NOT_NAME_OBJECT_SPECIFIC_J_NEUTRALITY_AUTHORITY",
    ),
    "V552_OBJECT_PARITY": MappingRule(
        "V552_OBJECT_PARITY", LegacyFamily.V552, "PRE553_SEMANTIC_PROJECTION",
        None, False, "P04_NAMES_NO_BLANKET_V552_CARRIER_EQUIVALENCE_AUTHORITY",
    ),
    "V552J_OBJECT_PARITY": MappingRule(
        "V552J_OBJECT_PARITY", LegacyFamily.V552J, "PRE553_SEMANTIC_PROJECTION",
        None, False, "P04_NAMES_NO_J_OR_V552J_CARRIER_EQUIVALENCE_AUTHORITY",
    ),
}
MAPPING_RULES: Mapping[str, MappingRule] = MappingProxyType(_MAPPING_RULES)


@dataclass(frozen=True)
class LegacyParityReceipt:
    receipt_id: str
    p04_return_commit: str
    p04_contract_id: str
    p04_contract_version: str
    legacy_family: LegacyFamily | str
    mapping_id: str
    source_carrier_id: str
    source_carrier_content_hash: str
    authority_id: str
    authority_version: str
    authority_content_hash: str
    source_semantic_projection_hash: str
    target_semantic_projection_hash: str
    source_scope_hash: str
    target_scope_hash: str
    source_state_model_hash: str
    target_state_model_hash: str
    source_provenance_hash: str
    target_provenance_hash: str
    source_universe_hash: str
    target_universe_hash: str
    generated_content_proved: bool
    negative_semantics_preserved: bool
    carrier_substitution: bool = False
    carrier_neutrality_proof_hash: str | None = None
    uses_retired_runtime: bool = False
    uses_v558_current_runtime_context: bool = False
    profile_or_persona_shortcut: bool = False
    study_key: str | None = None
    source_file_sha256: str | None = None
    authority_manifest_sha256: str | None = None
    respondent_linkage_mode: str | None = None
    source_level_exclusions_preserved: bool | None = None


@dataclass(frozen=True)
class ParityDecision:
    parity_class: ParityClass
    decision_code: str
    mapping_id: str
    legacy_family: str
    target_semantic_kind: str | None
    authority_id: str | None
    receipt_id: str
    reason: str

    @property
    def admitted(self) -> bool:
        return self.parity_class is ParityClass.EXACT_PARITY


@dataclass(frozen=True)
class AdaptedParityProjection:
    receipt_id: str
    legacy_family: str
    mapping_id: str
    target_semantic_kind: str
    authority_id: str
    semantic_projection_hash: str
    semantic_projection: Any


class LegacyParityError(ValueError):
    """Malformed receipt or payload; semantic nonparity is returned as a decision."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LegacyParityError(f"{name} must be a non-empty string")
    return value.strip()


def _sha256(value: Any, name: str) -> str:
    value = _text(value, name)
    if not _SHA256_RE.fullmatch(value):
        raise LegacyParityError(f"{name} must be a lowercase sha256")
    return value


def _canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise LegacyParityError("binary float forbidden in parity semantic projection")
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise LegacyParityError("semantic projection mapping keys must be strings")
        return {key: _canonicalize(value[key]) for key in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    raise LegacyParityError(f"unsupported semantic projection type: {type(value).__name__}")


def semantic_projection_hash(value: Any) -> str:
    payload = json.dumps(
        _canonicalize(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _family(value: LegacyFamily | str) -> LegacyFamily | None:
    try:
        return value if isinstance(value, LegacyFamily) else LegacyFamily(value)
    except (ValueError, TypeError):
        return None


def _decision(
    receipt: LegacyParityReceipt,
    parity_class: ParityClass,
    code: str,
    reason: str,
    *,
    rule: MappingRule | None = None,
) -> ParityDecision:
    family = _family(receipt.legacy_family)
    return ParityDecision(
        parity_class=parity_class,
        decision_code=code,
        mapping_id=receipt.mapping_id,
        legacy_family=family.value if family else str(receipt.legacy_family),
        target_semantic_kind=rule.target_semantic_kind if rule else None,
        authority_id=rule.authority_pin.authority_id if rule and rule.authority_pin else None,
        receipt_id=receipt.receipt_id,
        reason=reason,
    )


def _validate_receipt_shape(receipt: LegacyParityReceipt) -> None:
    _text(receipt.receipt_id, "receipt_id")
    if not _GIT_SHA_RE.fullmatch(_text(receipt.p04_return_commit, "p04_return_commit")):
        raise LegacyParityError("p04_return_commit must be a lowercase 40-character git sha")
    _text(receipt.p04_contract_id, "p04_contract_id")
    _text(receipt.p04_contract_version, "p04_contract_version")
    _text(receipt.mapping_id, "mapping_id")
    _text(receipt.source_carrier_id, "source_carrier_id")
    for name in (
        "source_carrier_content_hash", "authority_content_hash",
        "source_semantic_projection_hash", "target_semantic_projection_hash",
        "source_scope_hash", "target_scope_hash",
        "source_state_model_hash", "target_state_model_hash",
        "source_provenance_hash", "target_provenance_hash",
        "source_universe_hash", "target_universe_hash",
    ):
        _sha256(getattr(receipt, name), name)
    _text(receipt.authority_id, "authority_id")
    _text(receipt.authority_version, "authority_version")
    if receipt.carrier_neutrality_proof_hash is not None:
        _sha256(receipt.carrier_neutrality_proof_hash, "carrier_neutrality_proof_hash")
    if receipt.source_file_sha256 is not None:
        _sha256(receipt.source_file_sha256, "source_file_sha256")
    if receipt.authority_manifest_sha256 is not None:
        _sha256(receipt.authority_manifest_sha256, "authority_manifest_sha256")


def classify_legacy_parity(receipt: LegacyParityReceipt) -> ParityDecision:
    """Classify a parity receipt without inspecting or executing a legacy carrier."""
    _validate_receipt_shape(receipt)
    family = _family(receipt.legacy_family)
    rule = MAPPING_RULES.get(receipt.mapping_id)

    if family is None or rule is None or rule.legacy_family is not family:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_AMBIGUOUS_CARRIER_IDENTITY",
            "legacy family and named mapping are not an exact registered pair", rule=rule,
        )
    if receipt.profile_or_persona_shortcut:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_FORBIDDEN_PROFILE_PERSONA_SHORTCUT",
            "legacy profile/persona shortcuts are outside PRE553 empirical parity", rule=rule,
        )
    if receipt.uses_retired_runtime:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_RETIRED_RUNTIME_FALLBACK",
            "migration cannot invoke V550-V552 runtime as a fallback", rule=rule,
        )
    if receipt.uses_v558_current_runtime_context:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_V558_CURRENT_RUNTIME_FALLBACK",
            "V558 repository/metadata state is not current empirical runtime authority", rule=rule,
        )
    if (
        receipt.p04_return_commit != P04_ACCEPTED_RETURN_COMMIT
        or receipt.p04_contract_id != P04_COMPATIBILITY_CONTRACT_ID
        or receipt.p04_contract_version != P04_COMPATIBILITY_CONTRACT_VERSION
    ):
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_PROVENANCE_MISMATCH",
            "receipt is not bound to the accepted P04 compatibility return", rule=rule,
        )
    if not rule.enabled:
        return _decision(
            receipt, ParityClass.DEFERRED, "DEFER_NO_ACCEPTED_NAMED_PARITY_AUTHORITY",
            rule.deferred_reason or "no accepted exact parity authority is pinned", rule=rule,
        )

    pin = rule.authority_pin
    assert pin is not None
    if (
        receipt.authority_id != pin.authority_id
        or receipt.authority_version != pin.authority_version
        or receipt.authority_content_hash != pin.authority_content_hash
    ):
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_PROVENANCE_MISMATCH",
            "named authority id/version/hash does not match the pinned mapping authority", rule=rule,
        )

    if family in {LegacyFamily.V550, LegacyFamily.V551} and not receipt.generated_content_proved:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_UNPROVEN_PARITY",
            "bound generated empirical meaning requires producer-generation proof", rule=rule,
        )
    if not receipt.negative_semantics_preserved:
        return _decision(
            receipt, ParityClass.NONPARITY, "REJECT_NEGATIVE_SEMANTICS_COLLAPSE",
            "negative/absence states are not preserved distinctly from valid zero/false", rule=rule,
        )
    if receipt.carrier_substitution and receipt.carrier_neutrality_proof_hash is None:
        return _decision(
            receipt, ParityClass.DENIED, "REJECT_UNPROVEN_PARITY",
            "carrier substitution requires an exact artifact-class neutrality proof", rule=rule,
        )

    if family is LegacyFamily.R1:
        if (
            receipt.study_key != R1_STUDY_KEY
            or receipt.source_file_sha256 != R1_SOURCE_FILE_SHA256
            or receipt.authority_manifest_sha256 != R1_AUTHORITY_MANIFEST_SHA256
            or receipt.respondent_linkage_mode != R1_RESPONDENT_LINKAGE_MODE
            or receipt.source_level_exclusions_preserved is not True
        ):
            return _decision(
                receipt, ParityClass.DENIED, "REJECT_SOURCE_UNIVERSE_MISMATCH",
                "R1 parity is exact ATP_W135 finite-universe authority only", rule=rule,
            )

    dimension_checks = (
        ("semantic projection", receipt.source_semantic_projection_hash, receipt.target_semantic_projection_hash,
         "REJECT_UNPROVEN_PARITY"),
        ("scope", receipt.source_scope_hash, receipt.target_scope_hash, "REJECT_SCOPE_DOWNCAST"),
        ("state model", receipt.source_state_model_hash, receipt.target_state_model_hash,
         "REJECT_NEGATIVE_SEMANTICS_COLLAPSE"),
        ("provenance", receipt.source_provenance_hash, receipt.target_provenance_hash,
         "REJECT_PROVENANCE_MISMATCH"),
        ("source universe", receipt.source_universe_hash, receipt.target_universe_hash,
         "REJECT_SOURCE_UNIVERSE_MISMATCH"),
    )
    for dimension, source_hash, target_hash, code in dimension_checks:
        if source_hash != target_hash:
            return _decision(
                receipt, ParityClass.NONPARITY, code,
                f"exact {dimension} fingerprints differ", rule=rule,
            )

    return _decision(
        receipt,
        ParityClass.EXACT_PARITY,
        "ADMIT_R1_EXACT_AUTHORITY" if family is LegacyFamily.R1 else "ADMIT_EXACT_PARITY",
        "all pinned authority and exact semantic parity dimensions are satisfied",
        rule=rule,
    )


def adapt_semantic_projection(
    semantic_projection: Any,
    receipt: LegacyParityReceipt,
) -> AdaptedParityProjection:
    """Pass an already-canonical semantic projection only after exact parity.

    This function never reconstructs meaning from a legacy artifact. The payload
    itself must hash to the target projection hash named in the accepted receipt.
    """
    decision = classify_legacy_parity(receipt)
    if not decision.admitted:
        raise LegacyParityError(
            f"parity not admitted: {decision.parity_class.value}/{decision.decision_code}"
        )
    payload_hash = semantic_projection_hash(semantic_projection)
    if payload_hash != receipt.target_semantic_projection_hash:
        raise LegacyParityError("semantic projection payload does not match exact target projection hash")
    assert decision.target_semantic_kind is not None
    assert decision.authority_id is not None
    return AdaptedParityProjection(
        receipt_id=receipt.receipt_id,
        legacy_family=decision.legacy_family,
        mapping_id=decision.mapping_id,
        target_semantic_kind=decision.target_semantic_kind,
        authority_id=decision.authority_id,
        semantic_projection_hash=payload_hash,
        semantic_projection=_canonicalize(semantic_projection),
    )


def supported_mappings() -> tuple[MappingRule, ...]:
    return tuple(rule for rule in MAPPING_RULES.values() if rule.enabled)


def deferred_mappings() -> tuple[MappingRule, ...]:
    return tuple(rule for rule in MAPPING_RULES.values() if not rule.enabled)
