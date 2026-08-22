"""Inactive publication path for the compact R5 LONG_SHARDED V2 carrier.

This is a physical-only sibling of the accepted R5 shadow publisher. The CAS
state machine and serving-law semantics remain owned by pre553_r5_shadow; only
the builder/reader pair changes to the compact carrier.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_r5_compact_carrier import (
    R5LongShardedBuilder,
    R5LongShardedReader,
)
from rawlsing_next.pre553_r5_model import (
    R5BuildConfig,
    R5CanonicalRow,
    R5Error,
    R5ReleaseIdentity,
)
from rawlsing_next.pre553_r5_shadow import (
    PUBLICATION_VERSION,
    R5GenerationStampedCASSimulator,
    R5InjectedFault,
    R5QueryPin,
    R5SelectorState,
)


@dataclass(frozen=True)
class R5CompactShadowPublicationReceipt:
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


class R5CompactInactiveShadowPublisher:
    def __init__(
        self,
        shadow_root: str | Path,
        *,
        config: R5BuildConfig | None = None,
        fault_hook: Callable[[str, Mapping[str, Any]], None] | None = None,
    ) -> None:
        self.shadow_root = Path(shadow_root)
        self.config = config or R5BuildConfig()
        self.fault_hook = fault_hook or (lambda _phase, _detail: None)

    def publish(
        self,
        rows: Iterable[R5CanonicalRow],
        *,
        release_identity: R5ReleaseIdentity,
        semantic_validator: Callable[[R5LongShardedReader], None],
    ) -> R5CompactShadowPublicationReceipt:
        if not callable(semantic_validator):
            raise R5Error("inactive publication requires an explicit semantic validator")
        self.shadow_root.mkdir(parents=True, exist_ok=True)
        releases = self.shadow_root / "releases"
        releases.mkdir(exist_ok=True)
        staging = Path(
            tempfile.mkdtemp(prefix=".r5-compact-staging-", dir=self.shadow_root)
        )
        payload = staging / "payload"
        self.fault_hook("staging_created", {"staging": str(staging)})
        try:
            builder = R5LongShardedBuilder(
                self.config, fault_hook=self.fault_hook
            )
            telemetry = builder.build(
                rows,
                release_identity=release_identity,
                target_directory=payload,
            )
            self.fault_hook("staging_built", dict(telemetry))

            staged = R5LongShardedReader(
                payload,
                expected_physical_root_id=telemetry["physical_root_id"],
                fault_hook=self.fault_hook,
            )
            audit = staged.full_audit()
            self.fault_hook("staging_integrity_verified", audit)
            semantic_validator(staged)
            self.fault_hook(
                "staging_semantic_validated",
                {"physical_root_id": telemetry["physical_root_id"]},
            )

            _fsync_dir(payload / "members")
            _fsync_dir(payload)
            _fsync_dir(staging)
            _fsync_dir(self.shadow_root)
            self.fault_hook(
                "before_inactive_promote",
                {"physical_root_id": telemetry["physical_root_id"]},
            )
            target = releases / telemetry["physical_root_id"]
            if target.exists():
                existing = R5LongShardedReader(
                    target,
                    expected_physical_root_id=telemetry["physical_root_id"],
                )
                existing.full_audit()
                shutil.rmtree(payload)
            else:
                os.replace(payload, target)
                _fsync_dir(releases)
            self.fault_hook("after_inactive_promote", {"path": str(target)})

            reopened = R5LongShardedReader(
                target,
                expected_physical_root_id=telemetry["physical_root_id"],
                fault_hook=self.fault_hook,
            )
            final_audit = reopened.full_audit()
            semantic_validator(reopened)
            self.fault_hook("sealed_reopen_verified", final_audit)
            return R5CompactShadowPublicationReceipt(
                physical_root_id=telemetry["physical_root_id"],
                semantic_release_id=release_identity.semantic_release_hash,
                inactive_release_path=str(target),
                canonical_rows=final_audit["canonical_rows"],
                logical_stream_digest=final_audit["logical_stream_digest"],
            )
        finally:
            shutil.rmtree(staging, ignore_errors=True)


__all__ = [
    "PUBLICATION_VERSION",
    "R5CompactShadowPublicationReceipt",
    "R5CompactInactiveShadowPublisher",
    "R5InjectedFault",
    "R5SelectorState",
    "R5QueryPin",
    "R5GenerationStampedCASSimulator",
]
