"""Bind a private, independently pinned R157 source-read decision to construction.

Set PYAT_CONSTRUCTION_DECISION, PYAT_CONSTRUCTION_DECISION_SHA256 and
PYAT_CONSTRUCTION_SOURCE locally. The decision JSON uses the existing
IssuedSourceReadDecision fields. The SHA must come from the issuing custody
channel. This adapter does not issue decisions or supply S3 serving authority.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
import stat
from pathlib import Path

from rawlsing_next.pre553_r157_projection_adapter import (
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
    SourceReadRequest,
    _assert_current,
    source_read_request_from_config,
)


class PinnedConstructionResolver:
    """Reauthenticate the same decision bytes on every R157 read check."""

    def __init__(self, path: Path, expected_sha256: str):
        self.path = path
        self.expected_sha256 = expected_sha256

    def load(self) -> IssuedSourceReadDecision:
        try:
            if not self.path.is_absolute() or self.path.is_symlink():
                raise SourceReadAdmissionRefusal("PRIVATE_CONSTRUCTION_DECISION_PATH_REQUIRED")
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as handle:
                st = os.fstat(handle.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or st.st_mode & 0o077:
                    raise SourceReadAdmissionRefusal("PRIVATE_CONSTRUCTION_DECISION_REQUIRED")
                raw = handle.read()
        except OSError as exc:
            raise SourceReadAdmissionRefusal("CONSTRUCTION_DECISION_UNAVAILABLE") from exc
        if sha256(raw).hexdigest() != self.expected_sha256:
            raise SourceReadAdmissionRefusal("CONSTRUCTION_DECISION_PIN_MISMATCH")
        try:
            decision = IssuedSourceReadDecision(**json.loads(raw))
            start, end = (datetime.fromisoformat(value) for value in decision.effective_interval.split("/"))
            if start.utcoffset() is None or end.utcoffset() is None:
                raise ValueError("timezone required")
            if not start <= datetime.now(timezone.utc) < end:
                raise SourceReadAdmissionRefusal("CONSTRUCTION_DECISION_OUTSIDE_EFFECTIVE_INTERVAL")
        except SourceReadAdmissionRefusal:
            raise
        except (TypeError, ValueError) as exc:
            raise SourceReadAdmissionRefusal("CONSTRUCTION_DECISION_INVALID") from exc
        return decision

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        decision = self.load()
        _assert_current(decision, request)
        return decision


def construction_inputs(config):
    """Existing build_stream provider interface. Does not open source bytes."""
    try:
        decision_path = Path(os.environ["PYAT_CONSTRUCTION_DECISION"])
        decision_pin = os.environ["PYAT_CONSTRUCTION_DECISION_SHA256"]
        source_path = Path(os.environ["PYAT_CONSTRUCTION_SOURCE"])
    except KeyError as exc:
        raise SourceReadAdmissionRefusal("PINNED_LOCAL_CONSTRUCTION_INPUTS_REQUIRED") from exc
    if not source_path.is_absolute():
        raise SourceReadAdmissionRefusal("EXACT_LOCAL_SOURCE_PATH_REQUIRED")

    resolver = PinnedConstructionResolver(decision_path, decision_pin)
    decision = resolver.load()
    request = source_read_request_from_config(
        config,
        host=decision.host,
        purpose=decision.purpose,
        consumer_use=decision.consumer_use,
        semantic_use_scope=decision.semantic_use_scope,
    )
    _assert_current(decision, request)
    return source_path, request, resolver
