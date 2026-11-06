"""Read-only resource providers for the pinned R157 source pack.

The R157 configuration/fixture corpus is large and remains in its immutable
Git objects.  This module reads those exact blobs without materializing source
carriers or copying the corpus into a second checkout.  File-system providers
are retained for ordinary local packs and tests.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Protocol

R157_COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
R157_INDEX_PATH = "source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json"


class ResourceProvider(Protocol):
    def read_bytes(self, relative_path: str) -> bytes: ...
    def exists(self, relative_path: str) -> bool: ...
    def sha256(self, relative_path: str) -> str: ...


class ProviderError(ValueError):
    pass


class GitObjectProvider:
    """Read exact blobs from one immutable commit in the shared local store."""

    def __init__(self, commit: str = R157_COMMIT, repo: str | Path | None = None):
        self.commit = commit
        self.repo = Path(repo) if repo is not None else Path(__file__).resolve().parents[2]
        self._hashes: dict[str, str] = {}

    def _normalize(self, relative_path: str) -> str:
        path = str(relative_path).replace("\\", "/")
        if not path or path.startswith("/") or ".." in path.split("/"):
            raise ProviderError(f"unsafe repository-relative path: {relative_path!r}")
        return path

    def read_bytes(self, relative_path: str) -> bytes:
        path = self._normalize(relative_path)
        result = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "blob", f"{self.commit}:{path}"],
            capture_output=True, check=False)
        if result.returncode:
            raise ProviderError(f"pinned object unavailable: {self.commit}:{path}")
        return result.stdout

    def exists(self, relative_path: str) -> bool:
        path = self._normalize(relative_path)
        result = subprocess.run(
            ["git", "-C", str(self.repo), "cat-file", "-e", f"{self.commit}:{path}"],
            capture_output=True, check=False)
        return result.returncode == 0

    def sha256(self, relative_path: str) -> str:
        path = self._normalize(relative_path)
        cached = self._hashes.get(path)
        if cached is None:
            cached = hashlib.sha256(self.read_bytes(path)).hexdigest()
            self._hashes[path] = cached
        return cached


class FileSystemProvider:
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def _path(self, relative_path: str) -> Path:
        path = (self.root / str(relative_path)).resolve()
        if path != self.root and self.root not in path.parents:
            raise ProviderError(f"path escapes resource root: {relative_path!r}")
        return path

    def read_bytes(self, relative_path: str) -> bytes:
        return self._path(relative_path).read_bytes()

    def exists(self, relative_path: str) -> bool:
        return self._path(relative_path).is_file()

    def sha256(self, relative_path: str) -> str:
        return hashlib.sha256(self.read_bytes(relative_path)).hexdigest()


__all__ = [
    "R157_COMMIT", "R157_INDEX_PATH", "ProviderError", "ResourceProvider",
    "GitObjectProvider", "FileSystemProvider",
]
