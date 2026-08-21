"""Inactive transactional publication and isolated CAS state tests for R5 V1.

No production active selector is implemented here.  The publisher can only place
fully sealed content-addressed roots into an inactive shadow namespace.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_r5_carrier import R5LongShardedBuilder, R5LongShardedReader
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5Error, R5IntegrityError, R5ReleaseIdentity


PUBLICATION_VERSION = "PRE553_R5_INACTIVE_SHADOW_PUBLICATION@1.0.0"


class R5InjectedFault(RuntimeError):
    pass


@dataclass(frozen=True)
class R5ShadowPublicationReceipt:
    physical_root_id: str
    semantic_release_id: str
    inactive_release_path: str
    canonical_rows: int
    logical_stream_digest: str
    publication_state: str = "SHADOW_CANDIDATE__NON_SERVING__NONAUTHORITATIVE"


def _fsync_dir(path: Path) -> None:
    flags = getattr(os, "O_DIRECTORY", 0) | os.O_RDONLY
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class R5InactiveShadowPublisher:
    def __init__(self, shadow_root: str | Path, *, config: R5BuildConfig | None = None,
                 fault_hook: Callable[[str, Mapping[str, Any]], None] | None = None) -> None:
        self.shadow_root = Path(shadow_root)
        self.config = config or R5BuildConfig()
        self.fault_hook = fault_hook or (lambda _phase, _detail: None)

    def publish(self, rows: Iterable[R5CanonicalRow], *, release_identity: R5ReleaseIdentity,
                semantic_validator: Callable[[R5LongShardedReader], None]) -> R5ShadowPublicationReceipt:
        if not callable(semantic_validator):
            raise R5Error("inactive publication requires an explicit semantic validator")
        self.shadow_root.mkdir(parents=True, exist_ok=True)
        releases = self.shadow_root / "releases"; releases.mkdir(exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".r5-staging-", dir=self.shadow_root))
        payload = staging / "payload"
        self.fault_hook("staging_created", {"staging": str(staging)})
        try:
            builder = R5LongShardedBuilder(self.config, fault_hook=self.fault_hook)
            telemetry = builder.build(rows, release_identity=release_identity, target_directory=payload)
            self.fault_hook("staging_built", dict(telemetry))

            staged_reader = R5LongShardedReader(payload, expected_physical_root_id=telemetry["physical_root_id"],
                                                fault_hook=self.fault_hook)
            staged_audit = staged_reader.full_audit()
            self.fault_hook("staging_integrity_verified", staged_audit)
            semantic_validator(staged_reader)
            self.fault_hook("staging_semantic_validated", {"physical_root_id": telemetry["physical_root_id"]})

            # Durability domain: all payload files are fsynced by builder; persist directories.
            _fsync_dir(payload / "members"); _fsync_dir(payload); _fsync_dir(staging); _fsync_dir(self.shadow_root)
            self.fault_hook("before_inactive_promote", {"physical_root_id": telemetry["physical_root_id"]})
            target = releases / telemetry["physical_root_id"]
            if target.exists():
                existing = R5LongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"])
                existing.full_audit()
                shutil.rmtree(payload)
            else:
                os.replace(payload, target)
                _fsync_dir(releases)
            self.fault_hook("after_inactive_promote", {"path": str(target)})

            # A promoted root still has zero serving authority.  Reopen and verify.
            reopened = R5LongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"],
                                           fault_hook=self.fault_hook)
            final_audit = reopened.full_audit()
            semantic_validator(reopened)
            self.fault_hook("sealed_reopen_verified", final_audit)
            return R5ShadowPublicationReceipt(
                physical_root_id=telemetry["physical_root_id"],
                semantic_release_id=release_identity.semantic_release_hash,
                inactive_release_path=str(target),
                canonical_rows=final_audit["canonical_rows"],
                logical_stream_digest=final_audit["logical_stream_digest"],
            )
        finally:
            shutil.rmtree(staging, ignore_errors=True)


@dataclass(frozen=True)
class R5SelectorState:
    generation: int
    physical_root_id: str | None
    semantic_release_id: str | None
    admission_binding: str | None


@dataclass(frozen=True)
class R5QueryPin:
    generation: int
    physical_root_id: str
    semantic_release_id: str
    admission_binding: str


class R5GenerationStampedCASSimulator:
    """Isolated test-only selector state machine; not a production serving switch."""

    def __init__(self) -> None:
        self._state = R5SelectorState(0, None, None, None)

    @property
    def state(self) -> R5SelectorState:
        return self._state

    def compare_and_swap(self, *, expected_generation: int, expected_root: str | None,
                         new_root: str, semantic_release_id: str, admission_binding: str) -> R5SelectorState:
        if self._state.generation != expected_generation or self._state.physical_root_id != expected_root:
            raise R5IntegrityError("stale selector CAS authorization")
        if not all(isinstance(v, str) and v for v in (new_root, semantic_release_id, admission_binding)):
            raise R5IntegrityError("selector CAS requires exact root/semantic/admission bindings")
        self._state = R5SelectorState(self._state.generation + 1, new_root, semantic_release_id, admission_binding)
        return self._state

    def pin_query(self, *, expected_semantic_release_id: str, expected_admission_binding: str) -> R5QueryPin:
        state = self._state
        if state.physical_root_id is None:
            raise R5IntegrityError("selector has no root")
        if (state.semantic_release_id != expected_semantic_release_id
                or state.admission_binding != expected_admission_binding):
            raise R5IntegrityError("wrong semantic/admission binding")
        return R5QueryPin(state.generation, state.physical_root_id, state.semantic_release_id, state.admission_binding)

    def validate_query_end(self, pin: R5QueryPin) -> None:
        state = self._state
        if (state.generation != pin.generation or state.physical_root_id != pin.physical_root_id
                or state.semantic_release_id != pin.semantic_release_id
                or state.admission_binding != pin.admission_binding):
            raise R5IntegrityError("query root/generation changed during pinned read")


__all__ = [
    "PUBLICATION_VERSION", "R5InjectedFault", "R5ShadowPublicationReceipt",
    "R5InactiveShadowPublisher", "R5SelectorState", "R5QueryPin",
    "R5GenerationStampedCASSimulator",
]
