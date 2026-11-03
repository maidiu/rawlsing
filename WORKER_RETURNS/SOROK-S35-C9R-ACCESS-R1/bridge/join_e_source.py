"""Extract the pinned JOIN-E source from Git objects into a local runtime tree.

No external checkout is read. The extraction exists only to execute the
compatibility proof; it is gitignored and is not part of the public receipt.
"""
from __future__ import annotations

import hashlib
import io
import subprocess
import tarfile
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
JOIN_E_COMMIT = "5e63672543973ce2533129e1ca3224d82af0dffc"
JOIN_E_RETURN = "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"
RUNTIME = RETURN / ".runtime" / "join-e"
EXTRACTED = RUNTIME / JOIN_E_RETURN
_PATHS = (
    JOIN_E_RETURN + "/joined",
    JOIN_E_RETURN + "/vendor/j",
    JOIN_E_RETURN + "/vendor/e",
    JOIN_E_RETURN + "/SOURCE_MANIFEST.json",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_source() -> dict:
    manifest = EXTRACTED / "SOURCE_MANIFEST.json"
    joined = EXTRACTED / "joined" / "session.py"
    if not manifest.is_file() or not joined.is_file():
        archive = subprocess.run(
            ["git", "archive", JOIN_E_COMMIT, *_PATHS],
            cwd=str(REPO),
            capture_output=True,
            check=True,
        )
        RUNTIME.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
            bundle.extractall(RUNTIME)
    if not manifest.is_file() or not joined.is_file():
        raise RuntimeError("S35_JOIN_E_SOURCE_EXTRACTION_INCOMPLETE")
    return {
        "schema": "S35_JOIN_E_SOURCE_RUNTIME@1",
        "commit": JOIN_E_COMMIT,
        "return_path": str(EXTRACTED),
        "source_manifest_sha256": _sha256(manifest),
        "joined_session_sha256": _sha256(joined),
        "external_checkout_read": False,
        "staged": False,
    }


__all__ = [
    "EXTRACTED",
    "JOIN_E_COMMIT",
    "JOIN_E_RETURN",
    "REPO",
    "RUNTIME",
    "ensure_source",
]
