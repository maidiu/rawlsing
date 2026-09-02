"""WSC002B Golden Thread 0 source/PRE-FF implementation.

This module binds the exact F0 J01-A source-structure seed and carries it
through PRE-FF as a producer-preserving reference. It deliberately does not
claim executable-J authority, respondent values, a joint distribution,
measurement portability, or substantive structural meaning.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import inspect
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_replay_audit import assert_exact_source_content

F0_SOURCE_STRUCTURE_ID = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
F0_ADMITTED_UPSTREAM_GIT_SHA = "ba23b0fc1d22bb35abb8a6e8f9ab6100df8f7564"
F0_SOURCE_STRUCTURE_TYPE = "MATRIX_GRID"
F0_SOURCE_NATIVE_LABEL = "Current-versus-past freedoms and equality"
F0_MEMBERS = ("pfesol", "pfrsay", "pfrass", "pfrvot", "pfreql", "pfpsaf")
F0_MEMBER_IMPLEMENTATIONS = (
    "question_impl.phase0.8ba3e603375719d4aaec",
    "question_impl.phase0.918ff35a043d3b91ee30",
    "question_impl.phase0.f3f8a57abdc63672c950",
    "question_impl.phase0.ce222449ef2d9332ed8f",
    "question_impl.phase0.36e0483a24c1e427a739",
    "question_impl.phase0.4b39d3e67c9452c73174",
)
F0_R2_IDENTITY_SHA256 = "ef21f9f95c26e7ddd833401618e70cddcebdb7250ba7605de97a3387665843c6"
F0_SOURCE_DOCUMENT_SHA256 = "f603d9f5f95a3898dc42661b3cf8da749f874594b8770fe5fd5fb44f696eb537"
F0_CANDIDACY = "CURRENT_J_CANDIDATE"
F0_EXECUTABLE_J_CEILING = "CURRENT_J_CANDIDATE != EXECUTABLE_J"
F0_INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
F0_PERMISSION = "REFERENCE_ONLY__NO_RESPONDENT_VALUES__NO_EXECUTABLE_J"
F0_OWNER = "J01A_CURRENT_JOINT_SOURCE_CANDIDACY"
F0_SCOPE = "Afrobarometer|R1"
F0_FIXTURE_SOURCE = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/CURRENT_JOINT_AUTHORITY_CLOSURE_R1/J01A_RESIDUAL_CLOSURE_R2/"
    "LANE_D_ARAB_AFRO/CURRENT_SOURCE_STRUCTURE_UNIVERSE_R2.csv"
)
F0_FIXTURE_ROW_INDEX = 1

# Minimal exact non-respondent fixture projected from governed row 1 at the
# admitted immutable J01-A upstream ref. No respondent answer fields exist here.
F0_MINIMAL_GOVERNED_FIXTURE: Mapping[str, Any] = MappingProxyType({
    "index": "1",
    "current_source_structure_id": F0_SOURCE_STRUCTURE_ID,
    "source_family": "Afrobarometer",
    "wave_or_scope": "R1",
    "country": "",
    "form": "",
    "module": "",
    "split": "",
    "source_structure_type": F0_SOURCE_STRUCTURE_TYPE,
    "source_native_label_or_locator": F0_SOURCE_NATIVE_LABEL,
    "member_count": "6",
    "source_native_member_identities": "|".join(F0_MEMBERS),
    "current_question_implementation_ids": "|".join(F0_MEMBER_IMPLEMENTATIONS),
    "current_member_binding_status": "COMPLETE_EXACT_CURRENT_BINDING",
    "current_member_binding_gap": "",
    "source_document_identity": "merged_r1_codebook2.pdf",
    "source_document_sha256": F0_SOURCE_DOCUMENT_SHA256,
    "source_locator": (
        "native merged codebook p.53; explicit source block "
        "Current-versus-past freedoms and equality"
    ),
    "evidence_class": "NATIVE_CODEBOOK",
    "discovery_confidence": "SOURCE_NATIVE_EXPLICIT_RELATION",
    "candidacy_disposition": F0_CANDIDACY,
    "candidacy_rationale": (
        "Source-native respondent-facing multi-member relation may carry irreducible "
        "joint empirical information; executable J not adjudicated here."
    ),
    "binding_note": "EXACT_CASEFOLD:6",
    "r2_lineage_state": "R1_PRESERVED_EXACT",
    "r1_predecessor_id": F0_SOURCE_STRUCTURE_ID,
    "current_scope_authority": "R1 scope retained",
    "current_scope_resolution": "NO_CHANGE",
    "r2_review_note": (
        "R2 whole-surface recourt confirms R1 structure and disposition under "
        "current native authority."
    ),
    "r2_identity_sha256": F0_R2_IDENTITY_SHA256,
})

_FORBIDDEN_SELECTOR_TOKENS = frozenset({"latest", "default", "fuzzy", "nearest", "*"})


class GT0SourcePreFFError(ValueError):
    """F0 source/PRE-FF binding failed closed."""


class GT0SourcePreFFIntegrationError(GT0SourcePreFFError):
    """Shared protocol candidate API is absent or incompatible."""


@dataclass(frozen=True)
class GT0SourcePreFFResult:
    """Explicit protocol envelope/receipt plus exact producer ref."""

    envelope: Any
    receipt: Any
    producer_ref: ExactRef
    envelope_hash: str
    replay_hash: str


def _exact_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise GT0SourcePreFFError(f"{name} must be a non-empty exact string")
    if value.strip().lower() in _FORBIDDEN_SELECTOR_TOKENS:
        raise GT0SourcePreFFError(f"{name} may not use mutable/fuzzy selection")
    return value


def _verify_fixture(row: Mapping[str, Any]) -> Mapping[str, str]:
    if not isinstance(row, Mapping):
        raise GT0SourcePreFFError("F0 source row must be a mapping")
    missing = sorted(set(F0_MINIMAL_GOVERNED_FIXTURE) - set(row))
    if missing:
        raise GT0SourcePreFFError(f"F0 source row missing governed fields: {missing!r}")
    normalized: dict[str, str] = {}
    for key, expected in F0_MINIMAL_GOVERNED_FIXTURE.items():
        actual = row[key]
        if actual is None:
            actual = ""
        actual_text = str(actual)
        expected_text = str(expected)
        if actual_text != expected_text:
            raise GT0SourcePreFFError(
                f"F0 governed row mismatch for {key}: {actual_text!r} != {expected_text!r}"
            )
        normalized[key] = actual_text

    if normalized["candidacy_disposition"] != F0_CANDIDACY:
        raise GT0SourcePreFFError("F0 is not the frozen CURRENT_J_CANDIDATE seed")
    if "executable J not adjudicated here" not in normalized["candidacy_rationale"]:
        raise GT0SourcePreFFError("F0 executable-J ceiling text is absent")
    return MappingProxyType(normalized)


def _producer_ref(row: Mapping[str, str]) -> ExactRef:
    ref = ExactRef(
        kind="CURRENT_SOURCE_STRUCTURE",
        object_id=row["current_source_structure_id"],
        content_hash=row["r2_identity_sha256"],
    )
    assert_exact_source_content(actual=(ref,), expected=(ref,))
    return ref


def _replay_material(row: Mapping[str, str], producer_ref: ExactRef) -> Mapping[str, Any]:
    material = {
        "repository": "maidiu/rawlsing",
        "admitted_upstream_git_sha": F0_ADMITTED_UPSTREAM_GIT_SHA,
        "carrier_path": F0_FIXTURE_SOURCE,
        "carrier_row_index": F0_FIXTURE_ROW_INDEX,
        "producer_ref": producer_ref.as_dict(),
        "source_document_sha256": row["source_document_sha256"],
        "row_identity_sha256": row["r2_identity_sha256"],
        "selection_mode": "EXACT_IMMUTABLE_REF_ONLY",
    }
    return MappingProxyType(material)


def _protocol_module(protocol: Any | None) -> Any:
    if protocol is not None:
        return protocol
    try:
        return import_module("rawlsing_next.wsc_gt0_protocol")
    except ModuleNotFoundError as exc:
        raise GT0SourcePreFFIntegrationError(
            "rawlsing_next.wsc_gt0_protocol is supplied by WSC002A during central integration"
        ) from exc


def _status_pass(protocol: Any) -> Any:
    enum = getattr(protocol, "GT0StageStatus", None)
    if enum is None:
        raise GT0SourcePreFFIntegrationError("protocol must expose GT0StageStatus")
    try:
        return enum.PASS
    except AttributeError as exc:
        raise GT0SourcePreFFIntegrationError("GT0StageStatus must expose PASS") from exc


def _construct(cls: Any, material: Mapping[str, Any], object_name: str) -> Any:
    """Construct a shared candidate object using exact same-name fields only.

    This is not a semantic fallback. It lets this independent worker target the
    common protocol API without consuming a sibling branch; central integration
    may reconcile concrete constructor shape.
    """
    try:
        signature = inspect.signature(cls)
    except (TypeError, ValueError) as exc:
        raise GT0SourcePreFFIntegrationError(
            f"cannot inspect shared {object_name} constructor"
        ) from exc

    params = {name: param for name, param in signature.parameters.items() if name != "self"}
    accepts_kwargs = any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values())
    if accepts_kwargs:
        kwargs = dict(material)
    else:
        kwargs = {name: material[name] for name in params if name in material}
        required = {
            name
            for name, param in params.items()
            if param.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
            and param.default is inspect.Parameter.empty
        }
        missing = sorted(required - set(kwargs))
        if missing:
            raise GT0SourcePreFFIntegrationError(
                f"shared {object_name} requires unmatched fields {missing!r}"
            )
    try:
        return cls(**kwargs)
    except TypeError as exc:
        raise GT0SourcePreFFIntegrationError(
            f"shared {object_name} constructor rejected exact candidate material: {exc}"
        ) from exc


def _envelope_material(
    *,
    stage: str,
    producer_ref: ExactRef,
    replay: Mapping[str, Any],
    row: Mapping[str, str],
) -> Mapping[str, Any]:
    replay_hash = semantic_hash(replay)
    payload_hash = semantic_hash({
        "stage": stage,
        "producer_ref": producer_ref.as_dict(),
        "owner": F0_OWNER,
        "scope": F0_SCOPE,
        "permission": F0_PERMISSION,
        "typed_state": F0_CANDIDACY,
        "replay_hash": replay_hash,
        "information_loss": F0_INFORMATION_LOSS,
    })
    return {
        "stage": stage,
        "stage_id": stage,
        "semantic_owner": F0_OWNER,
        "producer": F0_OWNER,
        "producer_refs": (producer_ref,),
        "producer_ref": producer_ref,
        "upstream_refs": (F0_ADMITTED_UPSTREAM_GIT_SHA, producer_ref.key),
        "authority_refs": (F0_ADMITTED_UPSTREAM_GIT_SHA,),
        "authority_ref": F0_ADMITTED_UPSTREAM_GIT_SHA,
        "scope": F0_SCOPE,
        "scope_ref": F0_SCOPE,
        "risk_set": "UNASSERTED__SOURCE_STRUCTURE_ONLY",
        "permission": F0_PERMISSION,
        "permission_ceiling": F0_PERMISSION,
        "typed_state": F0_CANDIDACY,
        "state": F0_CANDIDACY,
        "dependencies": (
            producer_ref.key,
            F0_ADMITTED_UPSTREAM_GIT_SHA,
            row["source_document_sha256"],
        ),
        "dependency_refs": (
            producer_ref.key,
            F0_ADMITTED_UPSTREAM_GIT_SHA,
            row["source_document_sha256"],
        ),
        "information_loss": F0_INFORMATION_LOSS,
        "replay": dict(replay),
        "replay_material": dict(replay),
        "replay_hash": replay_hash,
        "payload_hash": payload_hash,
        "metadata": {
            "source_structure_type": F0_SOURCE_STRUCTURE_TYPE,
            "source_native_label": F0_SOURCE_NATIVE_LABEL,
            "members": F0_MEMBERS,
            "current_question_implementation_ids": F0_MEMBER_IMPLEMENTATIONS,
            "candidacy": F0_CANDIDACY,
            "executable_j_authorized": False,
            "authority_ceiling": F0_EXECUTABLE_J_CEILING,
            "respondent_values_present": False,
            "joint_distribution_asserted": False,
            "measurement_portability_asserted": False,
        },
    }


def _make_envelope(
    *,
    protocol: Any,
    stage: str,
    producer_ref: ExactRef,
    replay: Mapping[str, Any],
    row: Mapping[str, str],
) -> tuple[Any, str]:
    material = _envelope_material(
        stage=stage,
        producer_ref=producer_ref,
        replay=replay,
        row=row,
    )
    cls = getattr(protocol, "GT0ConservationEnvelope", None)
    if cls is None:
        raise GT0SourcePreFFIntegrationError("protocol must expose GT0ConservationEnvelope")
    return _construct(cls, material, "GT0ConservationEnvelope"), material["payload_hash"]


def _make_receipt(
    *,
    protocol: Any,
    stage: str,
    input_envelope: Any | None,
    input_envelope_hash: str | None,
    output_envelope: Any,
    output_envelope_hash: str,
    producer_ref: ExactRef,
    replay_hash: str,
    details: Mapping[str, Any],
) -> Any:
    status = _status_pass(protocol)
    receipt_hash = semantic_hash({
        "stage": stage,
        "status": "PASS",
        "producer_ref": producer_ref.as_dict(),
        "input_envelope_hash": input_envelope_hash,
        "output_envelope_hash": output_envelope_hash,
        "replay_hash": replay_hash,
        "details": dict(details),
    })
    material = {
        "stage": stage,
        "stage_id": stage,
        "status": status,
        "typed_status": status,
        "semantic_owner": F0_OWNER,
        "producer_refs": (producer_ref,),
        "upstream_refs": (F0_ADMITTED_UPSTREAM_GIT_SHA, producer_ref.key),
        "input_envelope": input_envelope,
        "output_envelope": output_envelope,
        "input_envelope_hash": input_envelope_hash,
        "output_envelope_hash": output_envelope_hash,
        "replay_hash": replay_hash,
        "details": dict(details),
        "metadata": dict(details),
        "receipt_hash": receipt_hash,
        "content_hash": receipt_hash,
    }
    cls = getattr(protocol, "GT0StageReceipt", None)
    if cls is None:
        raise GT0SourcePreFFIntegrationError("protocol must expose GT0StageReceipt")
    return _construct(cls, material, "GT0StageReceipt")


def bind_gt0_f0(
    source_row: Mapping[str, Any] = F0_MINIMAL_GOVERNED_FIXTURE,
    *,
    protocol: Any | None = None,
) -> GT0SourcePreFFResult:
    """Bind and verify the exact real F0 source-structure seed.

    The default is the minimal non-respondent fixture projected exactly from
    governed J01-A row 1 at ba23b0f... . No source answers are synthesized.
    """
    row = _verify_fixture(source_row)
    producer_ref = _producer_ref(row)
    replay = _replay_material(row, producer_ref)
    replay_hash = semantic_hash(replay)
    proto = _protocol_module(protocol)
    envelope, envelope_hash = _make_envelope(
        protocol=proto,
        stage="GT0_F0_BINDING",
        producer_ref=producer_ref,
        replay=replay,
        row=row,
    )
    receipt = _make_receipt(
        protocol=proto,
        stage="GT0_F0_BINDING",
        input_envelope=None,
        input_envelope_hash=None,
        output_envelope=envelope,
        output_envelope_hash=envelope_hash,
        producer_ref=producer_ref,
        replay_hash=replay_hash,
        details={
            "binding": "EXACT_GOVERNED_SOURCE_STRUCTURE_ROW",
            "candidacy": F0_CANDIDACY,
            "authority_ceiling": F0_EXECUTABLE_J_CEILING,
            "respondent_values_read": False,
            "respondent_values_fabricated": False,
        },
    )
    return GT0SourcePreFFResult(
        envelope=envelope,
        receipt=receipt,
        producer_ref=producer_ref,
        envelope_hash=envelope_hash,
        replay_hash=replay_hash,
    )


def run_gt0_preff(
    bound: GT0SourcePreFFResult | None = None,
    *,
    source_row: Mapping[str, Any] = F0_MINIMAL_GOVERNED_FIXTURE,
    protocol: Any | None = None,
) -> GT0SourcePreFFResult:
    """Carry F0 through PRE-FF as an exact producer-preserving reference.

    This stage intentionally does not execute a respondent-level J query because
    current authority establishes candidacy only. PASS therefore means exact
    reference/provenance/replay conservation, not EXECUTABLE_J.
    """
    proto = _protocol_module(protocol)
    if bound is None:
        bound = bind_gt0_f0(source_row, protocol=proto)
    if not isinstance(bound, GT0SourcePreFFResult):
        raise GT0SourcePreFFError("bound must be GT0SourcePreFFResult")

    row = _verify_fixture(source_row)
    expected = _producer_ref(row)
    assert_exact_source_content(actual=(bound.producer_ref,), expected=(expected,))
    if bound.producer_ref != expected:
        raise GT0SourcePreFFError("PRE-FF received a non-F0 producer ref")

    replay = _replay_material(row, expected)
    replay_hash = semantic_hash(replay)
    output, output_envelope_hash = _make_envelope(
        protocol=proto,
        stage="GT0_PREFF_REFERENCE",
        producer_ref=expected,
        replay=replay,
        row=row,
    )
    receipt = _make_receipt(
        protocol=proto,
        stage="GT0_PREFF_REFERENCE",
        input_envelope=bound.envelope,
        input_envelope_hash=bound.envelope_hash,
        output_envelope=output,
        output_envelope_hash=output_envelope_hash,
        producer_ref=expected,
        replay_hash=replay_hash,
        details={
            "operation": "PRODUCER_PRESERVING_REFERENCE_ONLY",
            "producer_ownership_transferred": False,
            "current_j_candidate": True,
            "executable_j_authorized": False,
            "authority_ceiling": F0_EXECUTABLE_J_CEILING,
            "respondent_values_read": False,
            "respondent_values_fabricated": False,
            "joint_distribution_asserted": False,
            "measurement_portability_asserted": False,
            "source_relation_promoted": False,
            "information_loss": F0_INFORMATION_LOSS,
        },
    )
    return GT0SourcePreFFResult(
        envelope=output,
        receipt=receipt,
        producer_ref=expected,
        envelope_hash=output_envelope_hash,
        replay_hash=replay_hash,
    )


__all__ = [
    "F0_ADMITTED_UPSTREAM_GIT_SHA",
    "F0_CANDIDACY",
    "F0_EXECUTABLE_J_CEILING",
    "F0_INFORMATION_LOSS",
    "F0_MEMBERS",
    "F0_MINIMAL_GOVERNED_FIXTURE",
    "F0_R2_IDENTITY_SHA256",
    "F0_SOURCE_NATIVE_LABEL",
    "F0_SOURCE_STRUCTURE_ID",
    "F0_SOURCE_STRUCTURE_TYPE",
    "GT0SourcePreFFError",
    "GT0SourcePreFFIntegrationError",
    "GT0SourcePreFFResult",
    "bind_gt0_f0",
    "run_gt0_preff",
]
