"""Verified in-process DuckDB sessions over canonical Parquet relations."""
from __future__ import annotations

import re
from typing import Any

from rawlsing_next.pre553_parquet_carrier import (
    ParquetC11Carrier, ParquetCarrierError, RELATION_SPECS, _sha_bytes, _sha_file,
    verify_semantic_release_root,
)
from rawlsing_next.pre553_empirical_objects import canonical_json


class VerifiedDuckDBSession:
    """A lightweight analytical session; it never reconstructs C11 objects."""
    def __init__(self, carrier: ParquetC11Carrier, *, source_sha256: str, release_id: str, semantic_hash: str):
        self.carrier = carrier
        self.source_sha256, self.release_id, self.semantic_hash = source_sha256, release_id, semantic_hash
        self.directory, self.manifest = self._verify_manifest()
        import pyarrow.parquet as pq
        identity_rows = pq.read_table(self.directory / "release_identity.parquet").to_pylist()
        replay_rows = pq.read_table(self.directory / "replay_manifest.parquet").to_pylist()
        if len(identity_rows) != 1 or len(replay_rows) != 1:
            raise ParquetCarrierError("direct-session identity-root relation cardinality mismatch")
        verify_semantic_release_root(
            identity_row=identity_rows[0], replay_row=replay_rows[0], manifest=self.manifest,
            supplied_source_sha256=self.source_sha256, supplied_release_id=self.release_id,
            supplied_semantic_hash=self.semantic_hash,
        )
        import duckdb
        self._connection = duckdb.connect(database=":memory:")
        try:
            for member in ("release_identity.parquet", *[f"{name}.parquet" for name in RELATION_SPECS]):
                path = str(self.directory / member).replace("'", "''")
                self._connection.execute(f"CREATE VIEW {member[:-8]} AS SELECT * FROM read_parquet('{path}')")
        except Exception:
            self.close()
            raise

    def _verify_manifest(self):
        if not re.fullmatch(r"[0-9a-f]{64}", self.source_sha256 or ""):
            raise ParquetCarrierError("source selector must be lowercase 64-hex SHA-256")
        if not re.fullmatch(r"[0-9a-f]{64}", self.semantic_hash or ""):
            raise ParquetCarrierError("semantic selector must be lowercase 64-hex SHA-256")
        if not isinstance(self.release_id, str) or not self.release_id or any(c in self.release_id for c in "/\\"):
            raise ParquetCarrierError("release selector is malformed or path-traversing")
        directory = self.carrier.root / "releases" / self.source_sha256 / self.release_id / self.semantic_hash
        try:
            import json
            manifest = json.loads((directory / "manifest.json").read_text())
        except Exception as exc:
            raise ParquetCarrierError("direct-session manifest unavailable") from exc
        unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
        if manifest.get("schema_version") != self.carrier.SCHEMA_VERSION or manifest.get("manifest_hash") != _sha_bytes(canonical_json(unsigned).encode()):
            raise ParquetCarrierError("direct-session manifest identity/hash mismatch")
        expected_members = {"release_identity.parquet", *[f"{name}.parquet" for name in RELATION_SPECS]}
        if set(manifest["members"]) != expected_members:
            raise ParquetCarrierError("direct-session required member inventory mismatch")
        for member, digest in manifest["members"].items():
            path = directory / member
            if not path.is_file() or _sha_file(path) != digest:
                raise ParquetCarrierError(f"missing or corrupt Parquet member: {member}")
        if (manifest["source_artifact_ref"].get("content_hash") != self.source_sha256
                or manifest["release_ref"].get("content_hash") != self.semantic_hash
                or manifest["release_ref"].get("object_id") != self.release_id):
            raise ParquetCarrierError("direct-session supplied selectors do not match manifest identity")
        return directory, manifest

    @property
    def release_ref(self) -> dict[str, Any]:
        return dict(self.manifest["release_ref"])

    def query(self, sql: str) -> list[tuple[Any, ...]]:
        if ".duckdb" in sql.lower() or "database_url" in sql.lower():
            raise ParquetCarrierError("DuckDB-file and DATABASE_URL authority paths are forbidden")
        return [tuple(row) for row in self._connection.execute(sql).fetchall()]

    def close(self) -> None:
        if getattr(self, "_connection", None) is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> "VerifiedDuckDBSession":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def open_direct_session(carrier: ParquetC11Carrier, *, source_sha256: str, release_id: str, semantic_hash: str) -> VerifiedDuckDBSession:
    return VerifiedDuckDBSession(carrier, source_sha256=source_sha256, release_id=release_id, semantic_hash=semantic_hash)


def query_canonical_release(carrier: ParquetC11Carrier, *, source_sha256: str, release_id: str,
                            semantic_hash: str, sql: str) -> list[tuple[Any, ...]]:
    with open_direct_session(carrier, source_sha256=source_sha256, release_id=release_id, semantic_hash=semantic_hash) as session:
        return session.query(sql)


__all__ = ["VerifiedDuckDBSession", "open_direct_session", "query_canonical_release"]
