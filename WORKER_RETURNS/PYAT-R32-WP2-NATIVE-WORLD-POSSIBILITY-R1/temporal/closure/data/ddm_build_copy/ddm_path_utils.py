#!/usr/bin/env python3
"""Path helpers for Rawlsing build outputs.

The goal is to keep manifests and reports repo-relative when possible so they do
not leak absolute local filesystem paths into the durable control-plane outputs.
"""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_relative_path_text(path: str | Path | None) -> str:
    if path is None:
        return ""
    candidate = Path(path)
    try:
        return str(candidate.resolve().relative_to(REPO_ROOT.resolve()))
    except Exception:
        try:
            return str(candidate.relative_to(REPO_ROOT))
        except Exception:
            return str(candidate)


__all__ = ["REPO_ROOT", "repo_relative_path_text"]
