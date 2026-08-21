"""Ephemeral DuckDB reads directly over canonical Parquet members."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError


def query_canonical_release(carrier: ParquetC11Carrier, *, source_sha256: str, release_id: str,
                            semantic_hash: str, sql: str) -> list[tuple[Any, ...]]:
    if ".duckdb" in sql.lower() or "database_url" in sql.lower():
        raise ParquetCarrierError("DuckDB-file and DATABASE_URL authority paths are forbidden")
    directory = carrier.root / "releases" / source_sha256 / release_id / semantic_hash
    carrier.reopen(source_sha256, release_id, semantic_hash)
    import duckdb
    connection = duckdb.connect(database=":memory:")
    try:
        def parquet_view(name: str) -> str:
            path = str(directory / name).replace("'", "''")
            return f"CREATE VIEW {name[:-8]} AS SELECT * FROM read_parquet('{path}')"
        for member in ("release_identity.parquet", "empirical_universes.parquet", "respondent_identities.parquet",
                       "question_variable_bindings.parquet", "respondent_events.parquet", "routing_eligibility.parquet",
                       "empirical_coordinates.parquet", "weight_measure.parquet", "authority_snapshots.parquet",
                       "source_universe_relations.parquet", "replay_bindings.parquet", "replay_manifest.parquet"):
            connection.execute(parquet_view(member))
        return [tuple(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


__all__ = ["query_canonical_release"]
