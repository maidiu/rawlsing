"""Cold restore: load the committed index and receive a release from an empty cwd."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from rawlsing_next.source_configuration.library import INDEX_PATH, ROOT, build_index

from .consumer import receive_fixture_release
from .registry import UniversalSourceRegistry


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cold_restore(source_id: str = "SRC26") -> dict[str, Any]:
    """Run from an unrelated empty cwd with only the committed repository path."""
    committed_index = (ROOT / INDEX_PATH).resolve()
    committed_bytes = committed_index.read_bytes()
    previous = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="pyat777-cold-restore-") as temporary:
        target = Path(temporary)
        try:
            os.chdir(target)
            registry = UniversalSourceRegistry(index_path=committed_index)
            receipt = receive_fixture_release(registry, source_id)
            rebuilt_path = target / "SOURCE_LIBRARY_INDEX.json"
            rebuilt = build_index(
                index_path=rebuilt_path,
                sqlite_path=target / "SOURCE_LIBRARY_INDEX.sqlite",
            )
            rebuilt_bytes = rebuilt_path.read_bytes()
            index_equal = rebuilt_bytes == committed_bytes
            return {
                "schema": "PYAT_777_UNIVERSAL_SOURCE_TO_C11_COLD_RESTORE@1.0.0",
                "cwd": str(target),
                "committed_index": str(committed_index),
                "committed_index_sha256": _sha256_bytes(committed_bytes),
                "rebuilt_index_sha256": _sha256_bytes(rebuilt_bytes),
                "rebuilt_index_byte_identical": index_equal,
                "rebuilt_counts": rebuilt["counts"],
                "source_id": source_id,
                "release_ref": receipt.release_ref,
                "semantic_release_hash": receipt.semantic_release_hash,
                "fixture_source_sha256": receipt.fixture_source_sha256,
                "ingest_disposition": receipt.ingest_disposition,
                "source_read_performed": receipt.source_read_performed,
                "original_execution": receipt.original_execution,
                "ok": index_equal and receipt.ingest_accepted,
            }
        finally:
            os.chdir(previous)
