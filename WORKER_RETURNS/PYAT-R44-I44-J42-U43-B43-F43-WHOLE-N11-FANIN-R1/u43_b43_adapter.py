"""Qualified I44 integration adapter: U43 issued descriptor -> B43 issuer-bound frontend.

The two R43 returns were authored independently:

* U43 transports a closed canonical 9-field descriptor envelope
  (``rawlsing_next.pre553_issued_workload.NativeWorkload.descriptor``);
* B43's ``IssuerBoundAdmission`` checks a plan's ``op_specs`` against an
  issuer-controlled contract before any native execution.

A raw U43 descriptor is not a B43 plan: B43 correctly refuses the direct shape.
This adapter is the commissioned *distinct integration adapter* that maps the
descriptor into the B43 frontend without changing either return. It preserves
the issuer contract as the comparison source (never the plan under test).

The compatibility court proves:
  BEFORE  raw descriptor object -> B43 typed shape refusal;
  AFTER   mapped plan -> B43 issuer-bound admission / typed field denials;
  FAULT   forged descriptor field -> typed denial with zero native calls.
"""
from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any, Mapping

import bootstrap

if not bootstrap.path_for("B43").is_dir():
    bootstrap.materialize("B43")
bootstrap.ensure_sys_path()

from b43.admission import (  # noqa: E402
    B43AdmissionDenied,
    IssuerBoundAdmission,
    IssuerDescriptorContract,
)
from rawlsing_next import pre553_issued_workload as u43  # noqa: E402


class AdapterShapeError(ValueError):
    """Typed adapter-shape failure (never a native execution)."""


def parse_descriptor(descriptor: bytes | str | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(descriptor, Mapping):
        material = dict(descriptor)
    else:
        raw = descriptor.encode("utf-8") if isinstance(descriptor, str) else descriptor
        try:
            material = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise AdapterShapeError("U43_DESCRIPTOR_NOT_CANONICAL_JSON") from exc
    if set(material) != set(u43.DESCRIPTOR_FIELDS):
        raise AdapterShapeError(
            "U43_DESCRIPTOR_FIELD_SET_MISMATCH:"
            + ",".join(sorted(set(material) ^ set(u43.DESCRIPTOR_FIELDS)))
        )
    if any(value is None or value == "UNBOUND" for value in material.values()):
        raise AdapterShapeError("U43_DESCRIPTOR_HAS_UNBOUND_REQUIRED_FIELD")
    return material


def raw_descriptor_frontend_probe(descriptor: bytes) -> dict[str, Any]:
    """BEFORE the adapter: a raw descriptor object is not a B43 plan."""

    raw = SimpleNamespace(descriptor=descriptor)
    try:
        return IssuerBoundAdmission(
            IssuerDescriptorContract.from_document(
                {"operations": {}}, issuer_ref="PROBE_ISSUER"
            )
        ).admit(raw)
    except B43AdmissionDenied as exc:
        return {"state": "B43_TYPED_REFUSAL", "code": exc.code}


def as_b43_plan(
    descriptor: bytes | str | Mapping[str, Any],
    *,
    op_ids: tuple[str, ...],
    releases: Mapping[str, Any] | None = None,
) -> SimpleNamespace:
    """AFTER the adapter: expose the descriptor as a B43-checkable plan.

    Only fields actually present in the issued descriptor are mapped. No grant,
    target, risk or member field is invented; if the B43 issuer contract requires
    such a field it will refuse as unbound rather than receive a fabricated value.
    """

    material = parse_descriptor(descriptor)
    if not op_ids:
        raise AdapterShapeError("U43_DESCRIPTOR_WITHOUT_OPERATIONS")
    spec_fields = {
        "source_edition": material["source_edition"],
        "native_item_ids": tuple(material["native_item_ids"]),
        "release_tag": material["release_tag"],
    }
    routing = material.get("routing_and_risk")
    if isinstance(routing, Mapping):
        for key in ("risk_name", "member_ids", "grant", "targets"):
            if key in routing:
                spec_fields[key] = routing[key]
    targets = material.get("target_conditioner_roles")
    if "targets" not in spec_fields and isinstance(targets, Mapping) and "targets" in targets:
        spec_fields["targets"] = targets["targets"]
    specs = {
        op_id: SimpleNamespace(op_id=op_id, **spec_fields) for op_id in op_ids
    }
    tag = material["release_tag"]
    release_map = dict(releases or {})
    release_map.setdefault(tag, SimpleNamespace(source_edition=material["source_edition"]))
    return SimpleNamespace(op_specs=specs, releases=release_map)


def issuer_contract_for_descriptor(
    descriptor: bytes | str | Mapping[str, Any],
    *,
    op_ids: tuple[str, ...],
    issuer_ref: str,
) -> IssuerDescriptorContract:
    """TEST_ONLY issuer contract binding the same issued descriptor.

    This is a compatibility fixture, not issuance: the caller must pass a clearly
    synthetic issuer_ref. Real adoption requires the competent issuer's own
    contract document.
    """

    if not issuer_ref.startswith("TEST_ONLY_") and not issuer_ref.startswith("SYNTHETIC_"):
        raise AdapterShapeError("REAL_ISSUER_CONTRACT_MUST_COME_FROM_COMPETENT_ISSUER")
    material = parse_descriptor(descriptor)
    rows = {
        op_id: {
            "source_edition": material["source_edition"],
            "native_item_ids": list(material["native_item_ids"]),
            "release_tag": material["release_tag"],
        }
        for op_id in op_ids
    }
    return IssuerDescriptorContract.from_document(
        {"operations": rows}, issuer_ref=issuer_ref
    )


def admit_via_b43(
    descriptor: bytes | str | Mapping[str, Any],
    *,
    op_ids: tuple[str, ...],
    issuer_ref: str = "TEST_ONLY_I44_COMPAT_ISSUER",
    candidate_descriptor: bytes | str | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Issuer contract comes from the issued descriptor; the plan is the candidate.

    ``descriptor`` is the issuer-bound, issued envelope; ``candidate_descriptor``
    is what the execution side actually presents (defaults to the issued one).
    A forged candidate must be refused by B43 before any native execution.
    """

    contract = issuer_contract_for_descriptor(
        descriptor, op_ids=op_ids, issuer_ref=issuer_ref
    )
    plan = as_b43_plan(candidate_descriptor or descriptor, op_ids=op_ids)
    return IssuerBoundAdmission(contract).admit(plan)


__all__ = [
    "AdapterShapeError",
    "parse_descriptor",
    "raw_descriptor_frontend_probe",
    "as_b43_plan",
    "issuer_contract_for_descriptor",
    "admit_via_b43",
]
