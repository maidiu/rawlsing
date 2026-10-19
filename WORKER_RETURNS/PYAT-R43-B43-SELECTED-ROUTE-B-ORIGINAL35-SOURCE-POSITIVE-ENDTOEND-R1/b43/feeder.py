"""B43 executable source-positive feeder over the actual selected-B owner.

No raw SAV/DTA is read unless an exact current grant covers source + host +
purpose + scientific operation. Without a grant the feeder returns a finite
SOURCE_EXECUTION_PENDING_OWNER result; it never fabricates a measured value.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .admission import B43AdmissionDenied, IssuerBoundAdmission

CLOCK = "2026-10-19T00:00:00-0400"


class B43GrantDenied(PermissionError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        super().__init__(code + (":" + detail if detail else ""))


@dataclass(frozen=True)
class SourceGrant:
    grant_id: str
    source_id: str
    host_ref: str
    purpose_ref: str
    operation_ref: str
    issuer_ref: str
    valid_until: str
    source_editions: tuple[str, ...] = ()
    revoked: bool = False

    def validate(self, *, source_id: str, host_ref: str, purpose_ref: str,
                 operation_ref: str, clock: str = CLOCK, edition: str | None = None):
        if self.revoked:
            raise B43GrantDenied("B43_GRANT_REVOKED")
        if clock > self.valid_until:
            raise B43GrantDenied("B43_GRANT_EXPIRED")
        if self.source_id != source_id:
            raise B43GrantDenied("B43_GRANT_WRONG_SOURCE")
        if self.host_ref != host_ref:
            raise B43GrantDenied("B43_GRANT_WRONG_HOST")
        if self.purpose_ref != purpose_ref:
            raise B43GrantDenied("B43_GRANT_WRONG_PURPOSE")
        if self.operation_ref != operation_ref:
            raise B43GrantDenied("B43_GRANT_WRONG_OPERATION")
        if edition is not None and self.source_editions and edition not in self.source_editions:
            raise B43GrantDenied("B43_GRANT_WRONG_EDITION")
        return True


def owner_call_contract() -> dict:
    """Prove the real selected-B owner is imported with the expected call shape."""
    from rawlsing_next.pre553_route_b_production import execute_route_b_production
    params = list(inspect.signature(execute_route_b_production).parameters)
    required = ["source", "projection", "runtime_catalog", "i03_requests",
                "discovery_authority_ref"]
    if params[:len(required)] != required:
        raise RuntimeError("B43_SELECTED_B_OWNER_SIGNATURE_CHANGED:" + ",".join(params))
    return {"owner": "rawlsing_next.pre553_route_b_production.execute_route_b_production",
            "parameters": params, "contract": "B43_SELECTED_B_OWNER_CALL@1"}


def guard_raw_source_read(path: str, grant: SourceGrant | None):
    """A raw source path may only be touched under an explicit covering grant."""
    if grant is None:
        raise B43GrantDenied("B43_RAW_SOURCE_READ_WITHOUT_GRANT")
    return {"state": "RAW_SOURCE_READ_PERMITTED_UNDER_GRANT", "path": path,
            "grant_id": grant.grant_id, "issuer_ref": grant.issuer_ref}


def request_source_positive(*, grant: SourceGrant | None, request: Mapping[str, Any],
                            plan: Any, admission: IssuerBoundAdmission,
                            source: Any = None, projection: Any = None,
                            runtime_catalog: Any = None, i03_requests: Sequence[Any] = (),
                            discovery_authority_ref: Any = None,
                            clock: str = CLOCK) -> dict:
    base = {"schema": "B43_SOURCE_POSITIVE_FEEDER_RESULT@1",
            "requested_source": request.get("source_id"),
            "requested_operation": request.get("operation_ref")}
    try:
        if grant is None:
            raise B43GrantDenied("B43_NO_SOURCE_GRANT")
        grant.validate(source_id=request["source_id"], host_ref=request["host_ref"],
                       purpose_ref=request["purpose_ref"],
                       operation_ref=request["operation_ref"],
                       clock=clock, edition=request.get("source_edition"))
    except B43GrantDenied as exc:
        return {**base, "state": "SOURCE_EXECUTION_PENDING_OWNER",
                "reason": exc.code,
                "measured_output": None,
                "raw_source_read": False,
                "owner_action": "COMPETENT_SOURCE_HOST_PURPOSE_OPERATION_GRANT_REQUIRED"}
    # Issuer-bound admission BEFORE any native execution (WG0L repairs).
    admitted = admission.admit(plan)
    base["admission"] = admitted
    if source is None or projection is None or runtime_catalog is None or discovery_authority_ref is None:
        return {**base, "state": "SOURCE_STREAM_NOT_SUPPLIED",
                "reason": "B43_GRANTED_BUT_NO_EXACT_SOURCE_STREAM",
                "measured_output": None, "raw_source_read": False}
    from rawlsing_next.pre553_route_b_production import execute_route_b_production
    result = execute_route_b_production(
        source=source, projection=projection, runtime_catalog=runtime_catalog,
        i03_requests=i03_requests, discovery_authority_ref=discovery_authority_ref)
    return {**base, "state": "EXECUTED_UNDER_GRANT", "measured_output": result,
            "raw_source_read": True, "grant_id": grant.grant_id}


def b43_a42_receipt(frontier: dict, docket: dict) -> dict:
    """A42 v2-shaped receipt: a development blocker, never original occupancy."""
    return {
        "receipt_id": "B43-SELECTED-B-SOURCE-FEEDER",
        "origin_commit": "WORKTREE",
        "claim_id": "B43_SELECTED_B_SOURCE_POSITIVE_FEEDER_READY__SOURCE_GRANT_PENDING",
        "grade": "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
        "coverage": {
            "wave_ids": [], "axis_ids": [], "f_gate_ids": [],
            "functional_gates": [], "register_151_ids": [], "ledger_101_ids": [],
            "global_relations": [], "global_contributions": [],
            "occupancy_grain_note": ("executable selected-B feeder + WG0L provenance repairs; "
                                     "no raw source grant, so no original measured occupancy"),
        },
        "unknown_bounds": {
            "original_source_grant_present": False,
            "expected_original_operations_total": None,
            "executed_original_operations_total": 0,
            "wave_count_pending": frontier["wave_count"],
            "docket_rows": docket["wave_count"],
        },
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T13:30:00-0400"},
        "artifacts": [],
    }
