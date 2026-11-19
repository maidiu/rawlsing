#!/usr/bin/env python3
"""Localized single-pass adapter: exact projected sections -> existing writer.

This mirrors the accepted OWNER proof path.  It does not alter the core writer,
schema, Q2 paths, or source/config/grant artifacts.  The explicit first I02 proof
and duplicate replay body journal are omitted; the existing direct writer still
co-produces its own I02 proof and Parquet from the exact one-shot sections.
"""
from __future__ import annotations
import tempfile
from pathlib import Path
from typing import Any, Callable, Mapping

def build_single_pass(
    *,
    config: Any,
    source_path: Any,
    private_root: Any,
    resolver: Any = None,
    host: str | None = None,
    purpose: str | None = None,
    consumer_use: str | None = None,
    semantic_use_scope: tuple[str, ...] | None = None,
    expected_i02: Any = None,
    batch_size: int = 512,
    chunk_rows: int = 512,
    progress: Callable[[Mapping[str, Any]], None] | None = None,
):
    """One admitted decode, exact projected sections, one existing writer pass."""
    from rawlsing_next import pre553_source_i02_handoff as handoff
    from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
    doc = config.document if hasattr(config, "document") else config
    original = doc["binding"]["identity_class"] == "ORIGINAL_SOURCE"
    if original:
        if resolver is None:
            raise handoff.SourceI02Hold("SOURCE_READ_RESOLVER_REQUIRED")
        incidence = handoff.decode_config_with_source_read_permission(
            config, source_path=source_path, resolver=resolver,
            host=host, purpose=purpose, consumer_use=consumer_use,
            semantic_use_scope=semantic_use_scope)
    else:
        fmt = doc["identity"]["source_format"]
        decoder = handoff.decode_sav if fmt == "SAV" else handoff.decode_dta
        incidence = decoder(source_path, encoding=None)
    try:
        if incidence.source_sha256 != doc["binding"]["source_sha256"]:
            raise handoff.SourceI02Refusal("DECODED_SOURCE_SHA_MISMATCH")
        if incidence.row_count != doc["binding"]["row_count"]:
            raise handoff.SourceI02Refusal("DECODED_SOURCE_ROWS_MISMATCH")
        projection = handoff.build_governed_c11_projection(
            config, source_sha256=doc["binding"]["source_sha256"],
            row_count=doc["binding"]["row_count"], row_native_keys=None)
        universe_ref = projection.universes[0].ref
        root = Path(private_root).absolute()
        spool_dir = Path(tempfile.mkdtemp(prefix=".s1e-i02-spool-", dir=root))
        spool_dir.chmod(0o700)
        spool_paths = {family: spool_dir / f"{family}.jsonl"
                       for family in handoff.SPOOL_FAMILIES}
        try:
            counts, _metrics, _slots, _key = handoff._project_spooled_families(
                config=config, projection=projection, incidence=incidence,
                spool_paths=spool_paths, batch_size=batch_size,
                row_native_keys=None)
            manifest, source, declared_counts, _absences = handoff._manifest_and_sections(
                projection=projection, incidence=incidence,
                spool_paths=spool_paths, counts=counts,
                universe_ref=universe_ref)
            if progress:
                progress({"phase": "sections_ready", "rows": incidence.row_count,
                          "families": len(declared_counts),
                          "records": int(sum(declared_counts.values()))})
            receipt = write_direct_estate(
                source, universe_ref, root, chunk_rows=chunk_rows,
                expected_i02=expected_i02)
            if progress:
                progress({"phase": "published", "families": len(receipt.family_counts),
                          "records": int(sum(receipt.family_counts.values())),
                          "retained_bytes": int(receipt.retained_bytes)})
            return receipt
        finally:
            cleanup_ok, leftovers = handoff._cleanup_spool(spool_paths, spool_dir)
            if not cleanup_ok:
                raise handoff.SourceI02Refusal("SPOOL_CLEANUP_INCOMPLETE", leftovers)
    finally:
        incidence.close()
