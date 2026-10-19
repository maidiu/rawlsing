"""A41 native Git/content preimage verification. Fail closed, never guess."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


class PreimageError(ValueError):
    """Typed refusal: a declared Git or content preimage did not verify."""


class GitPreimage:
    """Read exact objects out of the shared object store and hash them.

    Every accepted receipt in the A41 estate is anchored to a real Git blob
    and a real byte SHA-256. Nothing in this assembler trusts a self-asserted
    hash: the object is read back through ``git`` and re-hashed here.
    """

    def __init__(self, repo: Path):
        self.repo = Path(repo).resolve()

    def _git(self, *args: str) -> bytes:
        p = subprocess.run(["git", *args], cwd=self.repo, capture_output=True)
        if p.returncode != 0:
            raise PreimageError(f"git {' '.join(args)} failed: {p.stderr.decode()[:200]}")
        return p.stdout

    def commit_exists(self, commit: str) -> bool:
        try:
            self._git("cat-file", "-t", commit)
        except PreimageError:
            return False
        return True

    def blob_at(self, commit: str, path: str) -> bytes:
        return self._git("show", f"{commit}:{path}")

    def blob_sha1_at(self, commit: str, path: str) -> str:
        return self._git("rev-parse", f"{commit}:{path}").decode().strip()

    def verify(self, commit: str, path: str, *, expect_blob_sha1=None, expect_sha256=None,
               expect_bytes=None) -> dict:
        """Return the verified preimage record or raise PreimageError."""
        if not self.commit_exists(commit):
            raise PreimageError(f"COMMIT_UNAVAILABLE:{commit}")
        raw = self.blob_at(commit, path)
        if not raw and not self.blob_sha1_at(commit, path).startswith("e69de29"):
            raise PreimageError(f"EMPTY_OR_MISSING_PATH:{path}")
        blob = self.blob_sha1_at(commit, path)
        sha = hashlib.sha256(raw).hexdigest()
        if expect_blob_sha1 is not None and expect_blob_sha1 != blob:
            raise PreimageError(f"BLOB_PREIMAGE_MISMATCH:{path}:{blob}")
        if expect_sha256 is not None and expect_sha256 != sha:
            raise PreimageError(f"CONTENT_PREIMAGE_MISMATCH:{path}:{sha}")
        if expect_bytes is not None and expect_bytes != len(raw):
            raise PreimageError(f"BYTE_LENGTH_MISMATCH:{path}:{len(raw)}")
        return {"commit": commit, "path": path, "blob_sha1": blob, "sha256": sha,
                "bytes": len(raw)}

    @staticmethod
    def content_hash(raw: bytes) -> str:
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def parse_json(raw: bytes):
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise PreimageError(f"NON_JSON_EVIDENCE:{exc}") from exc
