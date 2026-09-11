"""Frozen-owner OBL063 terminal DriverPolicy/vector constructor candidate R1."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.bounded_empirical_runtime import (
    BoundedEmpiricalRuntimeError,
    ClaimCeiling,
    ContributionClass,
    DriverPolicy,
    DriverRuntimeState,
    EvidenceChannelPolicy,
    EvidenceContribution,
    EvidenceTier,
    ExactRef,
    canonical_json,
    resolve_driver_runtime,
    semantic_hash,
)

STAGE_ID = "EMPIRICAL_TO_DRIVER_VECTOR_PRE_V3"
CONSTRUCTOR_ID = "RAWLSING_EMPIRICAL_TO_DRIVER_VECTOR_PRE_V3_R1@1.0.0"
SOFTMAX_TEMPERATURE = Decimal("1.0")
OWNER_LAW_GIT_BLOB_SHA1 = "6fcb0959fa22c554a9772e7014030dd1f2a84f92"
MATRIX_GIT_BLOB_SHA1 = "b399ab6c0fcf19351b63c35fb99aabc582ddbbd9"
LEGACY_WEIGHT_SOURCE_SHA256 = "7d1eb56b4dc50f037c01976fe9eaace6e43130da3bdf7ea02591d02fe04d90cc"
SOURCE_DECISION_PACKET_RETURN = "77228b758b49b9c7f5cfdf7260dda9dea6107d98"
DIRECT_TRANSFORM = "DIRECT_UNIT_INTERVAL_FROM_0_100"
INVERSE_TRANSFORM = "INVERSE_UNIT_INTERVAL_FROM_0_100"
NORMALIZATION_ID = "SOFTMAX"
FALLBACK_POLICY = "NO_FALLBACK"

AUTHORITY_DIR = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "BOUNDED_EMPIRICAL_INCOMPLETENESS_RUNTIME_R1/MODEL_SEMANTIC_OWNER_DISPOSITION_R1"
)
OWNER_LAW_PATH = AUTHORITY_DIR / "00_HQ_MODEL_OWNER_DISPOSITION.json"
MATRIX_PATH = AUTHORITY_DIR / "01_DRIVER_TYPE_WEIGHT_MATRIX_R1.json"

ACTIVE_DRIVER_ORDER = (
    "materialSecurity", "economicInequality", "collectivism", "hierarchy",
    "secularization", "moralGrammar", "education", "genderEquality", "tightness",
    "politicalStability", "colonialTrauma", "urbanization", "trustEcology",
    "authorityStyle", "moralElasticity", "temporalOrientation", "existentialLocus",
    "postColonialIdentity", "genderSystemCoherence", "collectiveAffectTone",
    "institutionalMemory", "culturalPlasticity",
)
PENDING_DRIVER_ORDER = (
    "trustEcologyExtended", "aestheticOrientation", "conflictExpression", "timePressure",
    "fatalism", "ritualDensity", "environmentalRelation", "narrativeCoherence",
    "memoryOfCatastrophe", "humorOrientation", "hospitality", "shameAesthetics",
    "eschatologicalMood", "playfulness", "symbolicSubstitution",
    "intergenerationalReciprocity", "thresholdManagement", "emotionalLiteracy",
)
CONCEPTUAL_REGISTRY_ORDER = ACTIVE_DRIVER_ORDER + PENDING_DRIVER_ORDER
TYPE_IDS = ("t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9")

# driver -> (channel, transform). Coefficient=1.0, OPTIONAL, SOURCE_LOCAL_STATISTIC, NO_FALLBACK.
BINDINGS = {
    "collectivism": ("hofstede.Individualism", INVERSE_TRANSFORM),
    "hierarchy": ("hofstede.PowerDistance", DIRECT_TRANSFORM),
    "tightness": ("hofstede.UncertaintyAvoidance", DIRECT_TRANSFORM),
    "urbanization": ("urban_pop_percent", DIRECT_TRANSFORM),
    "authorityStyle": ("hofstede.PowerDistance", DIRECT_TRANSFORM),
    "temporalOrientation": ("hofstede.LongTermOrientation", DIRECT_TRANSFORM),
}
SELECTED_CHANNEL_IDS = frozenset(channel for channel, _ in BINDINGS.values())
EXPLICIT_EMPTY_ACTIVE_DRIVERS = tuple(d for d in ACTIVE_DRIVER_ORDER if d not in BINDINGS)


class TerminalConstructorError(BoundedEmpiricalRuntimeError):
    pass


@dataclass(frozen=True)
class TerminalChannelObservation:
    channel_id: str
    raw_value: Any
    evidence_tier: EvidenceTier
    source_ref: ExactRef | None
    population_authority_ref: ExactRef | None = None
    weight_authorized: bool | None = None
    estimand_authorized: bool | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.channel_id, str) or not self.channel_id.strip():
            raise TerminalConstructorError("channel_id must be non-empty text")
        object.__setattr__(self, "channel_id", self.channel_id.strip())
        if not isinstance(self.evidence_tier, EvidenceTier):
            object.__setattr__(self, "evidence_tier", EvidenceTier(self.evidence_tier))


@dataclass(frozen=True)
class TerminalConstructionResult:
    payload: Mapping[str, Any]
    result_hash: str

    def as_dict(self) -> dict[str, Any]:
        return {**json.loads(canonical_json(self.payload)), "result_hash": self.result_hash}

    def canonical_bytes(self) -> bytes:
        return canonical_json(self.as_dict()).encode("utf-8")

    @property
    def driver_slots(self):
        return self.payload["driver_slots"]

    @property
    def driver_coverage_receipt(self):
        return self.payload["driver_coverage_receipt"]

    @property
    def type_scores(self):
        return self.payload["type_scores"]

    @property
    def type_distribution(self):
        return self.payload["type_distribution"]

    @property
    def terminal_status(self):
        return self.payload["terminal_status"]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def _load_exact(path: Path, blob_sha1: str) -> tuple[dict[str, Any], bytes]:
    try:
        raw = (_repo_root() / path).read_bytes()
    except OSError as exc:
        raise TerminalConstructorError(f"required authority missing: {path}") from exc
    if _git_blob_sha1(raw) != blob_sha1:
        raise TerminalConstructorError(f"authority drift: {path}")
    try:
        data = json.loads(raw.decode(), parse_float=Decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TerminalConstructorError(f"invalid authority JSON: {path}") from exc
    if not isinstance(data, dict):
        raise TerminalConstructorError(f"authority must be object: {path}")
    return data, raw


def _load_and_validate_owner_law() -> tuple[dict[str, Any], dict[str, Any]]:
    owner, raw = _load_exact(OWNER_LAW_PATH, OWNER_LAW_GIT_BLOB_SHA1)
    if owner.get("schema") != "OBL063_MODEL_SEMANTIC_OWNER_DISPOSITION_R1@1.0.0":
        raise TerminalConstructorError("owner schema drift")
    if owner.get("source_decision_packet_return") != SOURCE_DECISION_PACKET_RETURN:
        raise TerminalConstructorError("owner source decision packet drift")
    if owner.get("accepted_boundary") != STAGE_ID:
        raise TerminalConstructorError("owner boundary drift")
    if owner.get("D01_CONSTRUCTOR", {}).get("constructor_id") != CONSTRUCTOR_ID.rsplit("@", 1)[0]:
        raise TerminalConstructorError("constructor identity drift")
    d02 = owner.get("D02_DRIVER_SCOPE", {})
    if (d02.get("registry_size"), d02.get("r1_active_type_producing_size"), d02.get("pending_size")) != (40, 22, 18):
        raise TerminalConstructorError("40/22/18 topology drift")
    if d02.get("driver_type_weight_basis", {}).get("sha256") != LEGACY_WEIGHT_SOURCE_SHA256:
        raise TerminalConstructorError("matrix source identity drift")
    d03 = owner.get("D03_CHANNEL_TRANSFORM_COEFFICIENT", {})
    expected = {
        d: [{"channel_id": ch, "transform": tr, "coefficient": Decimal("1.0"),
             "requiredness": "OPTIONAL_FOR_RUNTIME", "required_claim_ceiling": "SOURCE_LOCAL_STATISTIC"}]
        for d, (ch, tr) in BINDINGS.items()
    }
    if d03.get("selected_channels") != expected or tuple(d03.get("explicit_empty_r1_channel_sets", ())) != EXPLICIT_EMPTY_ACTIVE_DRIVERS:
        raise TerminalConstructorError("selected/empty channel law drift")
    if owner.get("D05_TYPE_NORMALIZATION", {}).get("softmax_temperature") != SOFTMAX_TEMPERATURE:
        raise TerminalConstructorError("softmax temperature drift")
    if owner.get("D07_FALLBACK", {}).get("owner_default_choice") != FALLBACK_POLICY:
        raise TerminalConstructorError("fallback law drift")
    if owner.get("D08_TYPED_DIMENSIONALITY", {}).get("active_driver_slots") != 22:
        raise TerminalConstructorError("typed dimensionality drift")
    return owner, {
        "owner_law_git_blob_sha1": OWNER_LAW_GIT_BLOB_SHA1,
        "owner_law_raw_sha256": hashlib.sha256(raw).hexdigest(),
        "source_decision_packet_return": SOURCE_DECISION_PACKET_RETURN,
    }


def _load_and_validate_matrix() -> tuple[dict[str, dict[str, Decimal]], dict[str, Any]]:
    data, raw = _load_exact(MATRIX_PATH, MATRIX_GIT_BLOB_SHA1)
    if data.get("schema") != "OBL063_DRIVER_TYPE_WEIGHT_MATRIX_R1@1.0.0":
        raise TerminalConstructorError("matrix schema drift")
    if data.get("source_sha256") != LEGACY_WEIGHT_SOURCE_SHA256 or data.get("active_driver_count") != 22:
        raise TerminalConstructorError("matrix identity drift")
    if tuple(data.get("type_ids", ())) != TYPE_IDS or tuple(data.get("weights", {})) != ACTIVE_DRIVER_ORDER:
        raise TerminalConstructorError("matrix shape/order drift")
    out: dict[str, dict[str, Decimal]] = {}
    for driver in ACTIVE_DRIVER_ORDER:
        row = data["weights"].get(driver)
        if not isinstance(row, dict) or tuple(row) != TYPE_IDS:
            raise TerminalConstructorError(f"matrix row drift: {driver}")
        out[driver] = {}
        for type_id in TYPE_IDS:
            try:
                value = row[type_id] if isinstance(row[type_id], Decimal) else Decimal(str(row[type_id]))
            except (InvalidOperation, ValueError) as exc:
                raise TerminalConstructorError("non-numeric matrix weight") from exc
            if not value.is_finite():
                raise TerminalConstructorError("non-finite matrix weight")
            out[driver][type_id] = value
    if data.get("law") != {"missing_driver_not_zero": True, "renormalize_on_missing": False, "pending_18_absent_from_matrix_not_zero": True}:
        raise TerminalConstructorError("matrix missingness law drift")
    return out, {
        "matrix_git_blob_sha1": MATRIX_GIT_BLOB_SHA1,
        "matrix_raw_sha256": hashlib.sha256(raw).hexdigest(),
        "legacy_weight_source_sha256": LEGACY_WEIGHT_SOURCE_SHA256,
        "matrix_shape": "22x9",
    }


def policy_manifest() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "constructor_id": CONSTRUCTOR_ID,
        "conceptual_registry_order": CONCEPTUAL_REGISTRY_ORDER,
        "active_driver_order": ACTIVE_DRIVER_ORDER,
        "pending_driver_order": PENDING_DRIVER_ORDER,
        "bindings": {
            d: {"channel_id": ch, "transform": tr, "coefficient": Decimal("1.0"),
                "claim_ceiling": "SOURCE_LOCAL_STATISTIC", "requiredness": "OPTIONAL_FOR_RUNTIME",
                "fallback": FALLBACK_POLICY}
            for d, (ch, tr) in BINDINGS.items()
        },
        "explicit_empty_active_drivers": EXPLICIT_EMPTY_ACTIVE_DRIVERS,
        "owner_law_git_blob_sha1": OWNER_LAW_GIT_BLOB_SHA1,
        "matrix_git_blob_sha1": MATRIX_GIT_BLOB_SHA1,
        "normalization": NORMALIZATION_ID,
        "temperature": SOFTMAX_TEMPERATURE,
        "coefficient_reallocation": False,
        "driver_weight_renormalization_on_missing": False,
    }


POLICY_SEMANTIC_HASH = semantic_hash(policy_manifest())


def build_driver_policies() -> dict[str, DriverPolicy]:
    return {
        driver: DriverPolicy(
            driver,
            (EvidenceChannelPolicy(channel, Decimal("1.0"), ClaimCeiling.SOURCE_LOCAL_STATISTIC, False, None),),
            allow_typed_no_numeric_driver=True,
            policy_version="1.0.0",
        )
        for driver, (channel, _) in BINDINGS.items()
    }


def _transform_raw(raw: Any, transform: str) -> tuple[Decimal | None, str]:
    if raw is None:
        return None, "MISSING_INPUT"
    if isinstance(raw, bool):
        return None, "NON_NUMERIC_INPUT"
    try:
        value = raw if isinstance(raw, Decimal) else Decimal(str(raw).strip())
    except (InvalidOperation, ValueError, AttributeError):
        return None, "NON_NUMERIC_INPUT"
    if not value.is_finite():
        return None, "NON_NUMERIC_INPUT"
    if value < 0 or value > 100:
        return None, "OUT_OF_DOMAIN_0_100"
    if transform == DIRECT_TRANSFORM:
        return value / Decimal("100"), "TRANSFORM_ACCEPTED"
    if transform == INVERSE_TRANSFORM:
        return Decimal("1") - value / Decimal("100"), "TRANSFORM_ACCEPTED"
    raise TerminalConstructorError(f"unauthorized transform: {transform}")


def _selected_slot(driver: str, observation: TerminalChannelObservation | None, policy: DriverPolicy) -> dict[str, Any]:
    channel, transform = BINDINGS[driver]
    contribution = None
    disposition = "MISSING_INPUT"
    if observation is not None:
        value, disposition = _transform_raw(observation.raw_value, transform)
        if value is not None and observation.evidence_tier in {EvidenceTier.SOURCE_LOCAL_CERTIFIED, EvidenceTier.POPULATION_CERTIFIED}:
            contribution = EvidenceContribution(
                driver, channel, observation.evidence_tier, ClaimCeiling.SOURCE_LOCAL_STATISTIC,
                value, observation.source_ref, observation.population_authority_ref,
                observation.weight_authorized, observation.estimand_authorized,
            )
            disposition = "TRANSFORM_AND_AUTHORITY_ACCEPTED"
        elif value is not None and observation.evidence_tier is EvidenceTier.PARTIAL_AUTHORITY:
            disposition = "INSUFFICIENT_SOURCE_LOCAL_AUTHORITY"
        elif value is not None and observation.evidence_tier is EvidenceTier.UNAVAILABLE:
            disposition = "EVIDENCE_UNAVAILABLE"
    envelope = resolve_driver_runtime(policy, [] if contribution is None else [contribution])
    if envelope.state is DriverRuntimeState.ADMISSIBLE_WITH_NUMERIC_CONTRIBUTIONS:
        if len(envelope.effective_contributions) != 1:
            raise TerminalConstructorError("selected driver contribution cardinality drift")
        effective = envelope.effective_contributions[0]
        if effective.contribution_class is not ContributionClass.EMPIRICAL or effective.coefficient != Decimal("1.0"):
            raise TerminalConstructorError("R1 fallback/coefficient drift")
        state, scalar = "NUMERIC", effective.value
    elif envelope.state is DriverRuntimeState.ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION:
        state, scalar = "TYPED_NO_NUMERIC", None
    else:
        state, scalar = "BLOCKED_TERMINAL_REQUIREMENT", None
    return {
        "driver_id": driver, "state": state, "value": scalar,
        "selected_channel_id": channel, "transform_id": transform,
        "input_disposition": disposition, "generic_runtime_envelope": envelope.as_dict(),
    }


def _coverage(slots: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    numeric = tuple(s["driver_id"] for s in slots if s["state"] == "NUMERIC")
    missing = tuple(s["driver_id"] for s in slots if s["state"] == "TYPED_NO_NUMERIC")
    blocked = tuple(s["driver_id"] for s in slots if s["state"] == "BLOCKED_TERMINAL_REQUIREMENT")
    core = {
        "active_driver_order": ACTIVE_DRIVER_ORDER, "numeric_driver_ids": numeric,
        "typed_no_numeric_driver_ids": missing, "blocked_driver_ids": blocked,
        "numeric_count": len(numeric), "typed_no_numeric_count": len(missing),
        "blocked_count": len(blocked), "coefficient_reallocated": False,
        "driver_weights_renormalized": False, "missing_encoded_as_zero": False,
        "policy_semantic_hash": POLICY_SEMANTIC_HASH,
    }
    return {**json.loads(canonical_json(core)), "coverage_hash": semantic_hash(core)}


def _scores(slots: Sequence[Mapping[str, Any]], matrix: Mapping[str, Mapping[str, Decimal]]) -> dict[str, Decimal]:
    scores = {t: Decimal("0") for t in TYPE_IDS}
    for slot in slots:
        if slot["state"] != "NUMERIC":
            continue
        for type_id in TYPE_IDS:
            scores[type_id] += slot["value"] * matrix[slot["driver_id"]][type_id]
    return scores


def _softmax(scores: Mapping[str, Decimal]) -> dict[str, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 50
        maximum = max(scores.values())
        exp = {t: ((scores[t] - maximum) / SOFTMAX_TEMPERATURE).exp() for t in TYPE_IDS}
        denom = sum(exp.values(), Decimal("0"))
        if denom <= 0 or not denom.is_finite():
            raise TerminalConstructorError("invalid softmax denominator")
        return {t: +(exp[t] / denom) for t in TYPE_IDS}


def construct_terminal_driver_vector(
    observations: Mapping[str, TerminalChannelObservation] | Sequence[TerminalChannelObservation],
) -> TerminalConstructionResult:
    _, owner_receipt = _load_and_validate_owner_law()
    matrix, matrix_receipt = _load_and_validate_matrix()
    policies = build_driver_policies()
    if isinstance(observations, Mapping):
        by_channel = dict(observations)
        if any(key != item.channel_id for key, item in by_channel.items()):
            raise TerminalConstructorError("observation key/channel mismatch")
    else:
        by_channel = {}
        for item in observations:
            if item.channel_id in by_channel:
                raise TerminalConstructorError(f"duplicate channel: {item.channel_id}")
            by_channel[item.channel_id] = item
    excluded = set(by_channel) - SELECTED_CHANNEL_IDS
    if excluded:
        raise TerminalConstructorError("nonselected R1 terminal channels are excluded: " + ",".join(sorted(excluded)))

    slots = []
    for driver in ACTIVE_DRIVER_ORDER:
        if driver in BINDINGS:
            channel, _ = BINDINGS[driver]
            slots.append(_selected_slot(driver, by_channel.get(channel), policies[driver]))
        else:
            slots.append({
                "driver_id": driver, "state": "TYPED_NO_NUMERIC", "value": None,
                "selected_channel_id": None, "transform_id": None,
                "input_disposition": "OWNER_EXPLICIT_EMPTY_R1_CHANNEL_SET",
                "generic_runtime_envelope": None,
            })
    coverage = _coverage(slots)
    if coverage["blocked_count"]:
        status, scores, distribution = "BLOCKED_TERMINAL_REQUIREMENT", None, None
    elif coverage["numeric_count"] == 0:
        status, scores, distribution = "BLOCKED_ALL_ACTIVE_DRIVERS_NO_NUMERIC", None, None
    else:
        status = "ADMISSIBLE_PARTIAL_OR_COMPLETE_NUMERIC_DRIVER_VECTOR"
        scores = _scores(slots, matrix)
        distribution = _softmax(scores)
    payload = {
        "stage_id": STAGE_ID, "constructor_id": CONSTRUCTOR_ID,
        "policy_semantic_hash": POLICY_SEMANTIC_HASH, "terminal_status": status,
        "registry": {"conceptual_driver_count": 40, "active_driver_count": 22, "pending_driver_count": 18,
                     "active_driver_order": ACTIVE_DRIVER_ORDER, "pending_driver_order": PENDING_DRIVER_ORDER},
        "driver_slots": tuple(slots), "driver_coverage_receipt": coverage,
        "type_scores": scores, "type_distribution": distribution,
        "normalization": NORMALIZATION_ID, "softmax_temperature": SOFTMAX_TEMPERATURE,
        "owner_binding_receipt": {**owner_receipt, **matrix_receipt,
                                  "policy_semantic_hash": POLICY_SEMANTIC_HASH,
                                  "constructor_id": CONSTRUCTOR_ID},
    }
    return TerminalConstructionResult(payload, semantic_hash(payload))
