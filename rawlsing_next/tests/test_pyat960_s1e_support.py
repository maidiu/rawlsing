"""Shared sourcefree fixtures for the Q2 B-role body/anti-join courts."""
from __future__ import annotations

from collections import Counter
from dataclasses import replace
import sqlite3
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_r157_projection_adapter import (
    CURRENT_GRANTED,
    IssuedSourceReadDecision,
    SourceConfig,
)
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
from rawlsing_next.tests.test_pyat940_s1b_support import (
    make_config,
    ref,
    sha256_text,
    write_fixture,
)
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import (
    _frontier,
    _inventory,
    _occurrence,
    _policy,
)


def source_fixture(
    root: Path,
    *,
    source_format: str = "SAV",
    keyed: bool = False,
    routing_state: str = "ELIGIBLE_APPLICABLE",
    values: Sequence[Any] = (0.0, 1.0, 2.0, 0.0, 1.0),
    extra_physical_slots: Sequence[Mapping[str, Any]] = (),
    inventory_occurrences: Sequence[Any] | None = None,
    policy_kwargs: Mapping[str, Any] | None = None,
    config_kwargs: Mapping[str, Any] | None = None,
    original: bool = False,
):
    path, source_sha, rows = write_fixture(
        root / f"src-{source_format}",
        source_format=source_format,
        values=values,
    )
    document = make_config(
        source_format=source_format,
        active_source_sha256=source_sha,
        row_count=rows,
        values=values,
        keyed=keyed,
        routing_state=routing_state,
        original=original,
        **dict(config_kwargs or {}),
    )
    document["physical_slots"] = list(document["physical_slots"]) + list(
        extra_physical_slots)
    config = SourceConfig(document)
    occurrences = tuple(
        inventory_occurrences
        if inventory_occurrences is not None
        else (_occurrence("q101"), _occurrence("country"))
    )
    inventory = replace(
        _inventory(occurrences, complete=True),
        source_id=document["identity"]["source_id"],
        wave=document["identity"]["wave"],
        edition=document["identity"]["instrument_release_id"],
        source_sha256=source_sha,
        inventory_id=f"PYAT960-S1E-B-{id(root)}",
    )
    policy = _policy(**dict(policy_kwargs or {"j": 1, "k": 1, "d": 0}))
    frontier = _frontier(inventory, policy)
    census = _freeze_packet(frontier)
    return {
        "path": path,
        "source_sha": source_sha,
        "rows": rows,
        "config": config,
        "document": document,
        "inventory": inventory,
        "policy": policy,
        "frontier": frontier,
        "census": census,
    }


def build(
    tmp_path: Path,
    fixture: Mapping[str, Any],
    *,
    name: str = "out.sqlite",
    config: SourceConfig | None = None,
    census: Any = None,
    inventory: Any = None,
    policy: Any = None,
    frontier: Any = None,
    **kwargs: Any,
):
    return build_source_i02_handoff(
        config=config or fixture["config"],
        source_path=fixture["path"],
        destination=tmp_path / name,
        census=census if census is not None else fixture["census"],
        inventory=inventory if inventory is not None else fixture["inventory"],
        policy=policy if policy is not None else fixture["policy"],
        frontier=frontier if frontier is not None else fixture["frontier"],
        **kwargs,
    )


class RecordingBodySink:
    """Test-only body consumer: stages exact bodies in memory, not a store."""

    def __init__(self, fail_at: str | None = None):
        self.fail_at = fail_at
        self.begin_args: dict[str, Any] | None = None
        self.begin_calls = 0
        self.counts: Counter[str] = Counter()
        self.absences: dict[str, str] = {}
        self.bodies: list[tuple[str, object]] = []
        self.events: dict[str, object] = {}
        self.refs: dict[str, list[str]] = {}
        self.finished = False
        self.aborted = False
        self.abort_exc: BaseException | None = None
        self.finish_roots = None
        self.finish_manifest = None
        self.finish_counts: Mapping[str, int] | None = None
        self.finish_transport: Mapping[str, Any] | None = None

    def begin(self, **kwargs: Any) -> None:
        self.begin_calls += 1
        self.begin_args = kwargs
        if self.fail_at == "begin":
            raise RuntimeError("test sink begin failure")

    def emit(self, family: str, obj: object) -> None:
        if self.fail_at == "emit":
            raise RuntimeError("test sink emit failure")
        assert type(obj).__name__ == family, (family, type(obj).__name__)
        assert semantic_hash(obj.semantic_projection()) == obj.ref.content_hash
        self.counts[family] += 1
        self.bodies.append((family, obj))
        self.refs.setdefault(family, []).append(obj.ref.key)
        if family == "RespondentEvent":
            self.events[obj.ref.key] = obj

    def absence(self, family: str, absence: Any) -> None:
        self.absences[family] = absence.state

    def finish(self, **kwargs: Any) -> None:
        if self.fail_at == "finish":
            raise RuntimeError("test sink finish failure")
        self.finish_roots = kwargs["roots"]
        self.finish_manifest = kwargs["manifest"]
        self.finish_counts = kwargs["counts"]
        self.finish_transport = kwargs["transport"]
        self.finished = True

    def abort(self, exc: BaseException) -> None:
        self.aborted = True
        self.abort_exc = exc
        # A real staging sink must discard its staged bodies here.
        self.bodies.clear()
        self.events.clear()
        self.refs.clear()


class DenyResolver:
    def resolve_current(self, request):
        return IssuedSourceReadDecision(
            decision_ref=ref("SOURCE_READ_DECISION", "urn:s1e:denied"),
            source_permission_refs=(
                ref("SOURCE_PERMISSION", "urn:s1e:denied"),
            ),
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
            effective_interval="S1E",
            currentness="EXPIRED",
            revocation_ref=None,
            retention_export_limits={"retention": "NONE"},
        )


class GrantResolver:
    def resolve_current(self, request):
        return IssuedSourceReadDecision(
            decision_ref=ref("SOURCE_READ_DECISION", "urn:s1e:granted"),
            source_permission_refs=(
                ref("SOURCE_PERMISSION", "urn:s1e:granted"),
            ),
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
            effective_interval="S1E",
            currentness=CURRENT_GRANTED,
            revocation_ref=None,
            retention_export_limits={"retention": "NONE"},
        )


def certificate_counts(path: Path) -> tuple[dict[str, int], dict[str, str]]:
    connection = sqlite3.connect(path)
    try:
        counts = dict(connection.execute(
            "SELECT family,COUNT(*) FROM main.objects GROUP BY family"))
        header = dict(connection.execute(
            "SELECT name,value FROM main.header"))
    finally:
        connection.close()
    return counts, header


def event_refs_from_certificate(path: Path) -> set[str]:
    connection = sqlite3.connect(path)
    try:
        return {row[0] for row in connection.execute(
            "SELECT ref FROM main.objects WHERE family='RespondentEvent'")}
    finally:
        connection.close()


def orphan_slot() -> Mapping[str, Any]:
    return {
        "ordinal": 3,
        "name": "orphan",
        "label": "Orphan preparation slot",
        "storage_type": "double",
        "original_type": "F8.0",
        "storage_width": "8",
        "measure": "nominal",
        "value_labels": {},
        "missing_declarations": None,
        "mr_declarations": None,
        "codebook_mapping": {
            "var_name": "orphan",
            "row_hash": sha256_text("codebook:orphan"),
            "status": "HELD",
        },
        "disposition": "HELD_NOT_SUPPORTED",
        "disposition_reason": "Q2 B-role orphan anti-join fixture.",
    }


__all__ = [
    "source_fixture",
    "build",
    "RecordingBodySink",
    "DenyResolver",
    "GrantResolver",
    "certificate_counts",
    "event_refs_from_certificate",
    "orphan_slot",
]
