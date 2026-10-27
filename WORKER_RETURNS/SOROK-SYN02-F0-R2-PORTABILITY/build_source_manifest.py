"""Build the bounded F0-R2 source manifest from the current accepted checkout."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
S51 = REPO / "WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"


def _binding():
    path = S51 / "s51/source_binding.py"
    spec = importlib.util.spec_from_file_location("_f0_r2_manifest_binding", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SOURCE_BINDING_UNLOADABLE: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _entries(root: Path, label: str, subdir: str) -> list[dict[str, str]]:
    base = root / subdir
    return [
        {
            "root": label,
            "path": str(path.relative_to(root)),
            "sha256": _sha(path),
        }
        for path in sorted(base.rglob("*.py"))
        if path.is_file()
    ]


def main() -> int:
    binding = _binding()
    roots = binding.source_roots(S51, REPO)
    repo = Path(roots["repo"])
    g18 = Path(roots["g18"])
    r30a = Path(roots["r30a"])
    sources = []
    for package in (
        "SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/s48",
        "SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/s49",
        "SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51",
        "SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1/s52",
    ):
        sources.extend(
            _entries(repo, "repo", "WORKER_RETURNS/" + package)
        )
    sources.extend(_entries(g18, "g18", "lab_sgi1"))
    sources.extend(_entries(r30a, "r30a", "r30a"))
    manifest = {
        "schema": "SOROK_F0_R2_SOURCE_MANIFEST@1",
        "generated_by": "WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/build_source_manifest.py",
        "roots": binding.ROOT_PROVENANCE,
        "sources": sources,
    }
    target = repo / binding.MANIFEST_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf8")
    verified = binding.verify_sources(roots, check_cache=False)
    print(json.dumps({
        "manifest": str(target),
        "sources": len(sources),
        "verified": verified["verified"],
        "repo": roots["repo"],
        "g18": roots["g18"],
        "r30a": roots["r30a"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
