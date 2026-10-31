from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class IntegrityStatus:
    CLEAN = "clean"
    DEGRADED = "degraded"
    BLOCKED = "blocked"


class GenerationIntegrityAccumulator:
    def __init__(self) -> None:
        self.diagnostics: list[dict[str, Any]] = []

    def record(
        self,
        stage: str,
        status: str,
        *,
        source_inputs: dict[str, Any] | None = None,
        fallback_used: bool = False,
        fallback_reason: str | None = None,
        fields_impacted: list[str] | None = None,
        chat_surface_impact: str = "none",
        details: dict[str, Any] | None = None,
        exc: BaseException | None = None,
    ) -> None:
        entry: dict[str, Any] = {
            "stage": stage,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_inputs": source_inputs or {},
            "fallback_used": fallback_used,
            "fallback_reason": fallback_reason,
            "fields_impacted": fields_impacted or [],
            "chat_surface_impact": chat_surface_impact,
            "details": details or {},
        }
        if exc is not None:
            entry["exception_type"] = type(exc).__name__
            entry["exception_message"] = str(exc)
        self.diagnostics.append(entry)

    def verdict(self, field_provenance: dict[str, Any] | None = None) -> dict[str, Any]:
        statuses = [d.get("status") for d in self.diagnostics]
        blocked = [d for d in self.diagnostics if d.get("status") == IntegrityStatus.BLOCKED]
        degraded = [d for d in self.diagnostics if d.get("status") == IntegrityStatus.DEGRADED]
        if blocked:
            overall = IntegrityStatus.BLOCKED
        elif degraded:
            overall = IntegrityStatus.DEGRADED
        else:
            overall = IntegrityStatus.CLEAN
        field_integrity = None
        field_integrity_source = None
        if field_provenance is not None:
            field_integrity = classify_field_provenance(field_provenance)
            field_integrity_source = field_integrity
            if field_integrity == IntegrityStatus.BLOCKED:
                overall = IntegrityStatus.BLOCKED
            elif field_integrity == IntegrityStatus.DEGRADED and overall == IntegrityStatus.CLEAN:
                overall = IntegrityStatus.DEGRADED
        grade = "blocked" if overall == IntegrityStatus.BLOCKED else (
            "degraded" if overall == IntegrityStatus.DEGRADED else "clean"
        )
        return {
            "overall_status": overall,
            "grade": grade,
            "degraded_stages": [d.get("stage") for d in degraded],
            "blocked_stages": [d.get("stage") for d in blocked],
            "blocking_reasons": [d.get("fallback_reason") or d.get("stage") for d in blocked],
            "total_diagnostics": len(self.diagnostics),
            "clean_count": sum(1 for s in statuses if s == IntegrityStatus.CLEAN),
            "degraded_count": len(degraded),
            "blocked_count": len(blocked),
            "field_provenance_status": field_integrity_source,
        }


def classify_field_provenance(field_provenance: dict[str, Any]) -> str:
    """
    Classify field-level provenance into an integrity status.

    Personhood-defining fallbacks should visibly degrade the overall status,
    and missing provenance for core fields is treated as blocked.
    """
    if not field_provenance:
        return IntegrityStatus.BLOCKED
    personhood_fields = ("ethnicity", "religion", "language")
    degraded = False
    language_integrity = field_provenance.get("language_integrity") or (field_provenance.get("language") or {}).get("language_integrity")
    if isinstance(language_integrity, dict) and str(language_integrity.get("status") or "").strip().lower() == "invalid_labels_found":
        degraded = True
    for field in personhood_fields:
        prov = field_provenance.get(field) or {}
        source = str(prov.get("source") or prov.get("source_family") or "").strip().lower()
        fallback_used = bool(prov.get("fallback_used"))
        if source in ("", "none", "unknown", "defaulted"):
            return IntegrityStatus.BLOCKED
        if source in ("factbook",) and fallback_used:
            degraded = True
        if fallback_used and source in ("defaulted", "factbook"):
            degraded = True
    return IntegrityStatus.DEGRADED if degraded else IntegrityStatus.CLEAN
