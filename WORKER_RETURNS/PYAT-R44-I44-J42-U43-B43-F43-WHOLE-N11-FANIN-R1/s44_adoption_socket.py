"""Executable S44 source-positive adoption socket into the frozen A42 assessor.

Purpose: a later lawful S44 current original-source product can populate A42
without another reimplementation. This module owns *validation and transport
only*. It never issues a source, host, purpose, U/E_pre, operation or
scientific right; a real adoption requires an external competent issuance
attestation that this socket verifies but cannot create.

Fail-closed rules (all typed):

* source wave and axes must exist in the frozen A42 scope;
* the receipt must name a current, unrevoked, host/purpose/operation-scoped grant;
* U/E_pre must be issued and independently attested for the exact wave/scope and
  cover every measured operation;
* the clock must be CURRENT and inside both the declared estate clock and the
  grant window;
* every consumer ref must be a declared consumer in the frozen scope;
* every artifact must verify as a Git blob + SHA-256 + byte preimage;
* measured operations must be SUPPORTED with positive denominators, and no
  route probability may be present;
* a synthetic witness is accepted only with ``allow_synthetic_witness=True`` and
  is explicitly marked as not a real issuance (never used by the real artifacts).
"""
from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime
import hashlib
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Mapping

import bootstrap  # noqa: F401

if not bootstrap.path_for("A42").is_dir():
    bootstrap.materialize("A42")
bootstrap.ensure_sys_path()

from a42 import core as a42core  # noqa: E402
from frozen_a41.a41.gitpreimage import GitPreimage, PreimageError  # noqa: E402

S44_SCHEMA = "S44_CURRENT_SOURCE_POSITIVE_RECEIPT@1"
S44_ISSUANCE_SCHEMA = "S44_COMPETENT_U_EPRE_ISSUANCE@1"
S44_A42_GRADE = "ORIGINAL_MEASURED_OCCUPANCY"
SYNTHETIC_SENTINEL = "SYNTHETIC_WITNESS_NOT_ISSUED"


class S44AdoptionRefused(ValueError):
    """Typed refusal; nothing reaches A42 acceptance on this path."""

    def __init__(self, code: str, detail: str = ""):
        self.code = code
        super().__init__(code + (":" + detail if detail else ""))


def _require(cond: bool, code: str, detail: str = "") -> None:
    if not cond:
        raise S44AdoptionRefused(code, detail)


def _parse_day(value: Any, code: str) -> date:
    _require(isinstance(value, str) and len(value) >= 10, code, "exact date required")
    try:
        return date.fromisoformat(value[:10])
    except ValueError as exc:
        raise S44AdoptionRefused(code, str(exc)) from exc


def _scope_maps(scope: Mapping[str, Any]):
    waves = {w["source_id"] for w in scope["waves"]}
    cells = {}
    for cell in scope["cells"]:
        cells.setdefault(cell["source_id"], set()).add(cell["axis_id"])
    return waves, cells


def _declared_consumers(scope: Mapping[str, Any]) -> set[str]:
    return set(scope.get("declared_consumers", []))


def validate_s44_source_positive(
    receipt: Mapping[str, Any],
    scope: Mapping[str, Any],
    *,
    issuance_attestation: Mapping[str, Any] | None = None,
    allow_synthetic_witness: bool = False,
    preimage: GitPreimage | None = None,
) -> dict[str, Any]:
    """Validate one S44 source-positive receipt against the frozen A42 scope."""

    _require(receipt.get("schema") == S44_SCHEMA, "S44_SCHEMA_MISMATCH")
    _require(receipt.get("receipt_id"), "S44_RECEIPT_ID_REQUIRED")
    _require(receipt.get("origin_commit"), "S44_ORIGIN_COMMIT_REQUIRED")
    waves, wave_axes = _scope_maps(scope)
    consumers = _declared_consumers(scope)

    source = receipt.get("source") or {}
    wave = source.get("wave") or source.get("source_id")
    _require(wave in waves, "S44_WAVE_OUT_OF_SCOPE", str(wave))
    _require(source.get("source_edition"), "S44_SOURCE_EDITION_MISSING")
    _require(source.get("source_sha256"), "S44_SOURCE_HASH_MISSING")
    _require(source.get("release_tag"), "S44_RELEASE_TAG_MISSING")
    _require(source.get("native_item_ids"), "S44_NATIVE_ITEM_IDS_MISSING")

    measured = receipt.get("measured") or {}
    operations = measured.get("operations") or []
    _require(operations, "S44_NO_MEASURED_PRODUCT")
    measured_axis = set()
    measured_ops = set()
    for op in operations:
        _require(op.get("operation_id"), "S44_OPERATION_ID_REQUIRED")
        measured_ops.add(op["operation_id"])
        _require(op.get("fact_state") == "SUPPORTED", "S44_NON_SUPPORTED_FACT")
        denominator = op.get("denominator")
        _require(isinstance(denominator, int) and denominator > 0, "S44_NON_POSITIVE_DENOMINATOR")
        _require("route_probability" not in op, "S44_ROUTE_PROBABILITY_FORBIDDEN")
        for axis in op.get("axis_ids") or []:
            _require(axis in wave_axes.get(wave, set()), "S44_AXIS_OUT_OF_SCOPE", str(axis))
            measured_axis.add(axis)
    _require(len(measured_axis) > 0, "S44_NO_SCOPE_AXIS_MEASURED")

    grant = receipt.get("grant") or {}
    _require(grant.get("grant_ref"), "S44_MISSING_GRANT")
    grant_issuer = str(grant.get("issuer_ref") or "")
    _require(grant_issuer, "S44_GRANT_ISSUER_REQUIRED")
    if grant_issuer.startswith(SYNTHETIC_SENTINEL):
        _require(
            allow_synthetic_witness,
            "S44_SYNTHETIC_GRANT_REQUIRES_EXPLICIT_WITNESS_MODE",
        )
    _require(grant.get("revoked") is not True, "S44_GRANT_REVOKED")
    _require(grant.get("host"), "S44_GRANT_HOST_REQUIRED")
    _require(grant.get("purpose"), "S44_GRANT_PURPOSE_REQUIRED")
    granted_ops = set(grant.get("operations") or [])
    _require(measured_ops <= granted_ops, "S44_GRANT_SCOPE_MISSING_OPERATION",
             ",".join(sorted(measured_ops - granted_ops)))

    u_e_pre = receipt.get("u_e_pre") or {}
    _require(u_e_pre.get("issued") is True, "S44_U_E_PRE_NOT_ISSUED")
    _require(u_e_pre.get("issuer_ref") and u_e_pre.get("issuance_ref") and u_e_pre.get("scope_hash"),
             "S44_U_E_PRE_IDENTITY_REQUIRED")
    _require(u_e_pre.get("wave") == wave, "S44_U_E_PRE_SCOPE_MISMATCH")
    eligible = set(u_e_pre.get("eligible_operation_ids") or [])
    _require(measured_ops <= eligible, "S44_U_E_PRE_OPERATION_NOT_ELIGIBLE",
             ",".join(sorted(measured_ops - eligible)))

    _require(issuance_attestation is not None, "S44_COMPETENT_U_E_PRE_ISSUANCE_ATTESTATION_REQUIRED")
    _require(issuance_attestation.get("schema") == S44_ISSUANCE_SCHEMA,
             "S44_ISSUANCE_SCHEMA_MISMATCH")
    _require(issuance_attestation.get("competent_issuer") is True,
             "S44_ISSUANCE_NOT_COMPETENT")
    synthetic_issuer = str(issuance_attestation.get("issuer_ref", "")).startswith(SYNTHETIC_SENTINEL)
    _require(
        not synthetic_issuer or allow_synthetic_witness,
        "S44_SYNTHETIC_ISSUANCE_REQUIRES_EXPLICIT_WITNESS_MODE",
    )
    for key in ("issuer_ref", "issuance_ref", "scope_hash", "wave"):
        _require(issuance_attestation.get(key) == u_e_pre.get(key),
                 "S44_ISSUANCE_IDENTITY_MISMATCH", key)
    attested = set(issuance_attestation.get("eligible_operation_ids") or [])
    _require(measured_ops <= attested, "S44_ISSUANCE_OPERATION_NOT_ELIGIBLE")

    clock = receipt.get("clock") or {}
    _require(clock.get("archive_or_current") == "CURRENT", "S44_CLOCK_NOT_CURRENT")
    as_of = _parse_day(clock.get("as_of"), "S44_CLOCK_INVALID")
    estate_clock = _parse_day(scope.get("declared_clock", "9999-12-31"), "S44_SCOPE_CLOCK_INVALID")
    _require(as_of <= estate_clock, "S44_CLOCK_VIOLATION")
    if grant.get("valid_from"):
        _require(_parse_day(grant["valid_from"], "S44_GRANT_CLOCK_INVALID") <= as_of,
                 "S44_GRANT_NOT_YET_VALID")
    if grant.get("valid_until"):
        _require(as_of <= _parse_day(grant["valid_until"], "S44_GRANT_CLOCK_INVALID"),
                 "S44_GRANT_EXPIRED")

    consumers_named = set(measured.get("consumer_read_refs") or [])
    _require(consumers_named, "S44_NO_CONSUMER_READ")
    _require(consumers_named <= consumers, "S44_UNKNOWN_USER_CONSUMER_REF",
             ",".join(sorted(consumers_named - consumers)))

    artifacts = receipt.get("artifacts") or []
    _require(artifacts, "S44_ARTIFACT_REQUIRED")
    gp = preimage or GitPreimage(bootstrap.ROOT)
    for artifact in artifacts:
        gp.verify(
            artifact.get("commit") or receipt["origin_commit"],
            artifact.get("path", ""),
            expect_blob_sha1=artifact.get("blob_sha1"),
            expect_sha256=artifact.get("sha256"),
            expect_bytes=artifact.get("bytes"),
        )

    return {
        "schema": "S44_SOURCE_POSITIVE_VALIDATION@1",
        "receipt_id": receipt["receipt_id"],
        "wave": wave,
        "axis_ids": sorted(measured_axis),
        "operation_ids": sorted(measured_ops),
        "as_of": clock["as_of"],
        "issuance_ref": issuance_attestation["issuance_ref"],
        "synthetic_witness": synthetic_issuer,
        "counted_in_real_artifacts": False if synthetic_issuer else True,
    }


def to_a42_original_receipt(receipt: Mapping[str, Any], validation: Mapping[str, Any]) -> dict[str, Any]:
    """Transport a validated S44 receipt into the exact A42 receipt schema."""

    return {
        "receipt_id": receipt["receipt_id"],
        "origin_commit": receipt["origin_commit"],
        "claim_id": receipt["claim_id"],
        "grade": S44_A42_GRADE,
        "coverage": {
            "wave_ids": [validation["wave"]],
            "axis_ids": list(validation["axis_ids"]),
            "f_gate_ids": [],
            "functional_gates": [],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "global_contributions": [],
            "occupancy_grain_note": (
                "S44 current original-source positive receipt; exact measured scope only"
            ),
        },
        "currentness": {
            "archive_or_current": "CURRENT",
            "as_of": validation["as_of"],
            "note": "current source-positive execution",
        },
        "artifacts": receipt["artifacts"],
        "unknown_bounds": receipt.get("unknown_bounds", {}),
        "downstream_consumer_read_refs": receipt["measured"]["consumer_read_refs"],
    }


def scope_with_issuance_overlay(
    scope: Mapping[str, Any], issuance_attestation: Mapping[str, Any]
) -> dict[str, Any]:
    """Return a copy of the frozen scope with only the attested wave marked issued.

    The frozen ``scope_digest`` is preserved as the base-scope digest; the overlay
    is explicitly recorded so no reader mistakes it for the frozen record.
    """

    overlay = deepcopy(scope)
    wave = issuance_attestation["wave"]
    if overlay["wave_expected_u_e_pre"].get(wave) != "ISSUED_AND_RECONCILED":
        overlay["wave_expected_u_e_pre"][wave] = "ISSUED_AND_RECONCILED"
    overlay["_s44_issuance_overlay"] = {
        "schema": "S44_SCOPE_ISSUANCE_OVERLAY@1",
        "wave": wave,
        "issuer_ref": issuance_attestation["issuer_ref"],
        "issuance_ref": issuance_attestation["issuance_ref"],
        "scope_hash": issuance_attestation["scope_hash"],
        "competent_issuer": issuance_attestation.get("competent_issuer") is True,
        "synthetic_witness": str(issuance_attestation.get("issuer_ref", "")).startswith(
            SYNTHETIC_SENTINEL
        ),
        "base_scope_digest": scope["scope_digest"],
    }
    return overlay


__all__ = [
    "S44_SCHEMA",
    "S44_ISSUANCE_SCHEMA",
    "S44_A42_GRADE",
    "SYNTHETIC_SENTINEL",
    "S44AdoptionRefused",
    "validate_s44_source_positive",
    "to_a42_original_receipt",
    "scope_with_issuance_overlay",
]


# ---------------------------------------------------------------------------
# executable socket self-test / report (never contributes to real artifacts)
# ---------------------------------------------------------------------------

A42_ARTIFACT_COMMIT = "843175b0587b54db3df1f461ad9f7f1314894372"
A42_ARTIFACT_PATH = (
    "WORKER_RETURNS/PYAT-R42-A42-WHOLE-ESTATE-RETURN-FANIN-AND-N11-CANDIDATE-R1/"
    "j42_addon_endpoint.json"
)


def _witness(scope: Mapping[str, Any], artifact: Mapping[str, Any]) -> tuple[dict, dict]:
    wave = "SRC01"
    axes = sorted({c["axis_id"] for c in scope["cells"] if c["source_id"] == wave})
    axis = "S01" if "S01" in axes else axes[0]
    scope_hash = hashlib.sha256(
        f"{SYNTHETIC_SENTINEL}:{wave}:{axis}:S44-WITNESS-OP".encode()
    ).hexdigest()
    issuance = {
        "schema": S44_ISSUANCE_SCHEMA,
        "competent_issuer": True,
        "issuer_ref": SYNTHETIC_SENTINEL + ":U_EPRE_ISSUER",
        "issuance_ref": SYNTHETIC_SENTINEL + ":ISSUANCE-1",
        "scope_hash": scope_hash,
        "wave": wave,
        "eligible_operation_ids": ["S44-WITNESS-OP"],
        "note": "SYNTHETIC SOCKET WITNESS ONLY; not a real issuance and never counted",
    }
    receipt = {
        "schema": S44_SCHEMA,
        "receipt_id": "S44-WITNESS-SRC01-S01",
        "origin_commit": A42_ARTIFACT_COMMIT,
        "claim_id": "SYNTHETIC_SOCKET_MECHANICS_WITNESS__NOT_SOURCE_SCIENCE",
        "source": {
            "source_id": wave,
            "wave": wave,
            "source_edition": "SYNTHETIC_EDITION",
            "source_sha256": hashlib.sha256(b"SYNTHETIC_SOURCE_WITNESS").hexdigest(),
            "release_tag": "SYNTHETIC_RELEASE",
            "native_item_ids": ["SYNTHETIC_ITEM"],
        },
        "grant": {
            "grant_ref": SYNTHETIC_SENTINEL + ":GRANT-1",
            "issuer_ref": SYNTHETIC_SENTINEL + ":GRANT_ISSUER",
            "host": "SYNTHETIC_HOST",
            "purpose": "SYNTHETIC_PURPOSE",
            "operations": ["S44-WITNESS-OP"],
            "valid_from": "2026-01-01",
            "valid_until": "2026-12-31",
            "revoked": False,
        },
        "u_e_pre": {
            "issued": True,
            "issuer_ref": SYNTHETIC_SENTINEL + ":U_EPRE_ISSUER",
            "issuance_ref": SYNTHETIC_SENTINEL + ":ISSUANCE-1",
            "scope_hash": scope_hash,
            "wave": wave,
            "eligible_operation_ids": ["S44-WITNESS-OP"],
        },
        "clock": {"archive_or_current": "CURRENT", "as_of": "2026-10-19"},
        "measured": {
            "operations": [
                {
                    "operation_id": "S44-WITNESS-OP",
                    "fact_state": "SUPPORTED",
                    "denominator": 10,
                    "cells": [{"cell": "1", "raw_numerator_support": 7}],
                    "axis_ids": [axis],
                }
            ],
            "consumer_read_refs": ["product.nonparent.consume"],
        },
        "artifacts": [dict(artifact)],
        "unknown_bounds": {"synthetic_socket_witness": True},
    }
    return receipt, issuance


def socket_report(scope: Mapping[str, Any]) -> dict[str, Any]:
    gp = GitPreimage(bootstrap.ROOT)
    materialized = gp.verify(A42_ARTIFACT_COMMIT, A42_ARTIFACT_PATH)
    receipt, issuance = _witness(scope, materialized)

    validation = validate_s44_source_positive(
        receipt, scope, issuance_attestation=issuance, allow_synthetic_witness=True, preimage=gp
    )
    a42receipt = to_a42_original_receipt(receipt, validation)
    overlay_scope = scope_with_issuance_overlay(scope, issuance)
    accepted = a42core.ingest_r41_bank({"receipts": [a42receipt]}, gp, overlay_scope)
    w41register = a42core.load_w41_register(gp)
    old_manifest = json.loads(
        gp.blob_at(a42core.A41_COMMIT, a42core.A41_DIR + "/estate_acceptance_manifest.json")
    )
    witness_assessment = a42core.assess_v2(
        overlay_scope, accepted, w41register, old_manifest
    )
    populated = [
        c
        for c in witness_assessment["cells"]
        if c.get("consumed_grade") == S44_A42_GRADE
    ]
    witness_only_original_cells = len(populated)

    refusals = {}

    def expect(code: str, mutated_receipt, mutated_iss="default", synthetic_ok=True, preimage=gp):
        if mutated_iss == "default":
            mutated_iss = issuance
        try:
            validate_s44_source_positive(
                mutated_receipt,
                scope,
                issuance_attestation=mutated_iss,
                allow_synthetic_witness=synthetic_ok,
                preimage=preimage,
            )
        except S44AdoptionRefused as exc:
            refusals[code] = exc.code
        except PreimageError as exc:
            refusals[code] = "PREIMAGE_ERROR:" + str(exc)[:120]
        else:
            refusals[code] = "ACCEPTED_UNEXPECTEDLY"

    r = deepcopy(receipt)
    r["grant"] = {}
    expect("missing_grant", r)
    r = deepcopy(receipt); r["grant"]["revoked"] = True
    expect("revoked_grant", r)
    r = deepcopy(receipt); r["grant"]["host"] = ""
    expect("missing_host", r)
    r = deepcopy(receipt); r["grant"]["purpose"] = ""
    expect("missing_purpose", r)
    r = deepcopy(receipt); r["grant"]["operations"] = []
    expect("operation_not_granted", r)
    r = deepcopy(receipt); r["u_e_pre"]["issued"] = False
    expect("u_e_pre_not_issued", r)
    expect("issuance_missing", receipt, None)
    expect("synthetic_issuance_without_witness_mode", receipt, issuance, synthetic_ok=False)
    r = deepcopy(receipt); r["clock"]["archive_or_current"] = "ARCHIVE"
    expect("clock_not_current", r)
    r = deepcopy(receipt); r["clock"]["as_of"] = "2027-01-01"
    expect("clock_after_estate", r)
    r = deepcopy(receipt); r["measured"]["consumer_read_refs"] = ["FORGED_ACTOR_CONSUMER"]
    expect("forged_consumer", r)
    r = deepcopy(receipt); r["source"]["wave"] = "SRC99"; r["u_e_pre"]["wave"] = "SRC99"
    expect("wave_out_of_scope", r)
    r = deepcopy(receipt); r["measured"]["operations"] = []
    expect("no_measured_product", r)
    r = deepcopy(receipt); r["artifacts"] = [
        {**materialized, "sha256": "0" * 64}
    ]
    expect("artifact_preimage_changed", r)
    return {
        "schema": "I44_S44_RECEIVING_INTERFACE_REPORT@1",
        "state": "EXECUTABLE_SOCKET_READY__NO_REAL_S44_RECEIPT_PRESENT",
        "contract": S44_SCHEMA,
        "issuance_contract": S44_ISSUANCE_SCHEMA,
        "a42_grade_produced": S44_A42_GRADE,
        "validation": validation,
        "a42_intake_accepted_receipts": [r["receipt_id"] for r in accepted],
        "scope_overlay": overlay_scope["_s44_issuance_overlay"],
        "synthetic_witness_only": True,
        "synthetic_witness_counted_in_real_artifacts": False,
        "synthetic_witness_original_cells_in_witness_assessment": witness_only_original_cells,
        "synthetic_witness_cell_ids": [c["cell_id"] for c in populated],
        "real_artifacts_original_measured": 0,
        "refusal_codes": refusals,
        "note": (
            "The synthetic witness proves socket mechanics only. It is gated by an explicit "
            "witness flag and is never part of the real merged bank or N11 artifacts. A real "
            "S44 receipt requires a competent external issuance attestation this worker "
            "cannot create."
        ),
    }
