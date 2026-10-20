"""Rebuild the disposable repro/repaired court layouts from committed assets.

Usage: python repro/stage_courts.py
Writes only under runtime/repro and runtime/repaired (gitignored).
"""
from __future__ import annotations

import shutil
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
PREFIX = "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"


def stage(root: Path, candidate: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    dest = root / PREFIX
    (dest / "candidate").parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(candidate, dest / "candidate")
    shutil.copytree(RET / "runtime" / "c9p" / "tests", dest / "tests")
    shutil.copytree(RET / "runtime" / "native" / "rawlsing_next", root / "rawlsing_next")
    shutil.copytree(RET / "runtime" / "c9pi" / "review", root / "review")


def main() -> None:
    stage(RET / "runtime" / "repro", RET / "runtime" / "c9p" / "candidate")
    stage(RET / "runtime" / "repaired", RET / "candidate")
    print("staged runtime/repro (exact target) and runtime/repaired (C9R candidate)")


if __name__ == "__main__":
    main()
