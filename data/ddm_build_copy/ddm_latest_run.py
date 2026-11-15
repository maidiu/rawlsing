from __future__ import annotations

from pathlib import Path


def latest_dir(root: str | Path, pattern: str) -> Path | None:
    root = Path(root)
    if not root.exists():
        return None
    candidates: list[tuple[int, int, Path]] = []
    for path in root.glob(f"**/{pattern}"):
        if not path.is_dir():
            continue
        if not ((path / "manifest").exists() or (path / "manifest.json").exists()):
            continue
        try:
            stat = path.stat()
        except Exception:
            continue
        candidates.append((int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))), -len(path.parts), path))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]
