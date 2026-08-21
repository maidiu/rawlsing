"""Small immutable model shared by PRE553 R5 shadow modules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


CARRIER_ID = "R5_LONG_SHARDED_TYPED_INCIDENCE_V1"
ROW_SCHEMA_VERSION = "PRE553_R5_CANONICAL_ROW@1.0.0"
ROOT_SCHEMA_VERSION = "PRE553_R5_ROOT@1.0.0"
INVENTORY_SCHEMA_VERSION = "PRE553_R5_MEMBER_INVENTORY@1.0.0"


class R5Error(ValueError):
    pass


class R5IntegrityError(R5Error):
    pass


class R5QuarantinedError(R5IntegrityError):
    pass


@dataclass(frozen=True)
class R5CanonicalRow:
    relation: str
    object_family: str
    object_id: str
    content_hash: str
    payload: Mapping[str, Any]

    @property
    def identity_key(self) -> tuple[str, str, str]:
        return self.relation, self.object_family, self.object_id


@dataclass(frozen=True)
class R5ReleaseIdentity:
    release_id: str
    semantic_release_hash: str
    source_artifact_ref: Mapping[str, Any]
    source_release_manifest_hash: str
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    decoder_receipt: Mapping[str, Any]
    compiler_contract_digest: str
    c11_authority_digest: str


@dataclass(frozen=True)
class R5BuildConfig:
    run_max_rows: int = 4096
    run_max_bytes: int = 4 * 1024 * 1024
    shard_max_rows: int = 16384
    shard_max_bytes: int = 16 * 1024 * 1024
    merge_fan_in: int = 8
    verified_spool_memory_bytes: int = 1024 * 1024

    def __post_init__(self) -> None:
        for name in ("run_max_rows", "run_max_bytes", "shard_max_rows", "shard_max_bytes",
                     "merge_fan_in", "verified_spool_memory_bytes"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise R5Error(f"{name} must be a positive integer")
        if self.merge_fan_in < 2:
            raise R5Error("merge_fan_in must be >= 2")


__all__ = [
    "CARRIER_ID", "ROW_SCHEMA_VERSION", "ROOT_SCHEMA_VERSION", "INVENTORY_SCHEMA_VERSION",
    "R5Error", "R5IntegrityError", "R5QuarantinedError", "R5CanonicalRow",
    "R5ReleaseIdentity", "R5BuildConfig",
]
