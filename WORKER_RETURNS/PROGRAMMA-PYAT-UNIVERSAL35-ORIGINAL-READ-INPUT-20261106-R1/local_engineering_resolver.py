"""Local, user-directed engineering-RAW source-read resolver.

This is a private-runtime binding, not an original/native/science issuer. It
authenticates an exact local engineering-read grant, exact source identity,
host, purpose, consumer use and semantic scope before the existing admission
transport opens any source bytes.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_read_admission import (
    CURRENT_GRANTED,
    EXACT_FILE,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
    SourceReadRequest,
)

DEFAULT_GRANT = Path(
    ".local-logs/pyat-universal35/original-read-input/local-engineering-read-grant.json"
)
EXPECTED_GRANT_SHA256 = "9e433cd95600c0634b38a08781eea851086fc8208739a6f29e6c83bbe58a88c7"
EXPECTED_USER_AUTHORIZATION_SHA256 = "18b2b57188a91a4af25c53b67c0e1ff1c8b848ac823c2d3391a1a72e5517edb4"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ref(kind: str, object_id: str, content_hash: str) -> ExactRef:
    return ExactRef(kind, object_id, content_hash)


def _ref_dict(ref: ExactRef) -> dict[str, Any]:
    return ref.as_dict()


class LocalEngineeringResolver:
    """Authenticate the exact private engineering-read grant."""

    def __init__(
        self,
        grant_path: str | Path = DEFAULT_GRANT,
        *,
        expected_grant_sha256: str | None = EXPECTED_GRANT_SHA256,
        expected_user_authorization_sha256: str | None = EXPECTED_USER_AUTHORIZATION_SHA256,
    ) -> None:
        self.grant_path = Path(grant_path)
        self.expected_grant_sha256 = expected_grant_sha256
        self.expected_user_authorization_sha256 = expected_user_authorization_sha256
        if not self.grant_path.is_file():
            raise SourceReadAdmissionRefusal("SOURCE_READ_LOCAL_ENGINEERING_GRANT_MISSING")
        self.raw = self.grant_path.read_bytes()
        self.grant = json.loads(self.raw.decode("utf-8"))
        actual = _sha256(self.raw)
        if expected_grant_sha256 is not None and actual != expected_grant_sha256:
            raise SourceReadAdmissionRefusal(
                "SOURCE_READ_LOCAL_ENGINEERING_GRANT_CHANGED_OR_REVOKED")
        if self.grant.get("authority_class") != "USER_DIRECTED_LOCAL_ENGINEERING_RAW_READ_ONLY":
            raise SourceReadAdmissionRefusal("SOURCE_READ_LOCAL_ENGINEERING_GRANT_WRONG_CLASS")
        if self.grant.get("native_science_authority") is not False:
            raise SourceReadAdmissionRefusal("SOURCE_READ_LOCAL_ENGINEERING_GRANT_NATIVE_SCOPE")
        if self.grant.get("currentness") != CURRENT_GRANTED:
            raise SourceReadAdmissionRefusal("SOURCE_READ_NOT_CURRENT", str(self.grant.get("currentness")))
        if self.grant.get("revocation_ref") is not None:
            raise SourceReadAdmissionRefusal("SOURCE_READ_REVOKED")
        user = self.grant.get("user_authorization") or {}
        user_path = self.grant_path.parent / str(user.get("path", "USER_ENGINEERING_READ_AUTHORIZATION.txt"))
        if self.expected_user_authorization_sha256 is not None:
            if not user_path.is_file():
                raise SourceReadAdmissionRefusal("SOURCE_READ_USER_AUTHORIZATION_MISSING")
            if _sha256(user_path.read_bytes()) != self.expected_user_authorization_sha256:
                raise SourceReadAdmissionRefusal("SOURCE_READ_USER_AUTHORIZATION_CHANGED")
        self.grant_sha = actual
        self.user_sha = str(user.get("sha256"))
        self.rows = {row["source_id"]: row for row in self.grant.get("sources", ())}

    def _current(self) -> None:
        interval = str(self.grant.get("effective_interval", ""))
        try:
            start, end = interval.split("/", 1)
            now = datetime.now(timezone.utc)
            lo = datetime.fromisoformat(start.replace("Z", "+00:00"))
            hi = datetime.fromisoformat(end.replace("Z", "+00:00"))
        except Exception as exc:
            raise SourceReadAdmissionRefusal("SOURCE_READ_LOCAL_INTERVAL_INVALID") from exc
        if not lo <= now < hi:
            raise SourceReadAdmissionRefusal("SOURCE_READ_NOT_CURRENT", interval)

    def _permission_refs(self) -> tuple[ExactRef, ...]:
        durable = self.grant.get("durable_refs") or {}
        commission = durable.get("commission") or {}
        custody = durable.get("custody") or {}
        return (
            _ref("USER_LOCAL_ENGINEERING_READ_GRANT",
                 "urn:rawlsing:user-grant:universal35:local-engineering-read:20261106",
                 self.grant_sha),
            _ref("USER_LOCAL_ENGINEERING_READ_AUTHORIZATION",
                 "urn:rawlsing:user-authorization:universal35:local-engineering-read:20261106",
                 str(self.user_sha)),
            _ref("UNIVERSAL35_COMMISSION",
                 "urn:rawlsing:commission:" + str(commission.get("commit")) + ":F_COMMISSION",
                 str(commission.get("sha256"))),
            _ref("UNIVERSAL35_SOURCE_CUSTODY",
                 "urn:rawlsing:custody:" + str(custody.get("commit")) + ":01_LOCAL_SOURCE_CUSTODY",
                 str(custody.get("sha256"))),
        )

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        if not isinstance(request, SourceReadRequest):
            raise SourceReadAdmissionRefusal("SOURCE_READ_REQUEST_REQUIRED")
        self._current()
        row = self.rows.get(request.source_id)
        if row is None:
            raise SourceReadAdmissionRefusal("SOURCE_READ_SOURCE_NOT_IN_LOCAL_GRANT")
        expected = (
            ("source_sha256", request.source_sha256, row["source_sha256"]),
            ("source_format", request.source_format, row["source_format"]),
            ("custody_locator_binding", request.custody_locator_binding, row["custody_locator_binding"]),
            ("host", request.host, self.grant["host"]),
            ("purpose", request.purpose, self.grant["purpose"]),
            ("consumer_use", request.consumer_use, self.grant["consumer_use"]),
            ("read_operation", request.read_operation, SOURCE_RESPONSE_DECODE),
            ("physical_read_extent", request.physical_read_extent, EXACT_FILE),
            ("semantic_use_scope", tuple(request.semantic_use_scope),
             tuple(self.grant["semantic_use_scope"])),
            ("metadata_freeze_refs", tuple(ref.as_dict() for ref in request.metadata_freeze_refs),
             tuple(row["metadata_freeze_refs"])),
        )
        for name, actual, wanted in expected:
            if actual != wanted:
                raise SourceReadAdmissionRefusal("SOURCE_READ_LOCAL_" + name.upper() + "_MISMATCH")
        material = {
            "grant": self.grant_sha,
            "source_id": request.source_id,
            "source_sha256": request.source_sha256,
            "host": request.host,
            "purpose": request.purpose,
            "consumer_use": request.consumer_use,
            "semantic_use_scope": list(request.semantic_use_scope),
        }
        decision_sha = _sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode())
        decision = IssuedSourceReadDecision(
            decision_ref=_ref(
                "USER_LOCAL_ENGINEERING_READ_DECISION",
                "urn:rawlsing:user-decision:universal35:local-engineering-read:" + request.source_id,
                decision_sha,
            ),
            source_permission_refs=self._permission_refs(),
            source_id=request.source_id,
            source_sha256=request.source_sha256,
            source_format=request.source_format,
            custody_locator_binding=request.custody_locator_binding,
            host=request.host,
            purpose=request.purpose,
            consumer_use=request.consumer_use,
            read_operation=request.read_operation,
            physical_read_extent=request.physical_read_extent,
            metadata_freeze_refs=request.metadata_freeze_refs,
            semantic_use_scope=request.semantic_use_scope,
            effective_interval=self.grant["effective_interval"],
            currentness=CURRENT_GRANTED,
            revocation_ref=None,
            retention_export_limits={
                "retention": "SESSION_LOCAL_ONLY",
                "export": "DENY",
                "publication": "DENY",
                "raw_records": "NOT_COMMITTED",
                "authority_ceiling": "LOCAL_ENGINEERING_RAW_ONLY",
                "native_science": "NOT_GRANTED",
            },
        )
        return decision


__all__ = ["LocalEngineeringResolver"]
