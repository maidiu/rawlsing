"""Rebuild the read-only BP2P4J target tree from its exact return commit."""
from __future__ import annotations

import io
import shutil
import subprocess
import tarfile
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
TARGET_COMMIT = "5b3e6577400ea1d88971ae6b48e41a118b8059ae"
PREFIX = "WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1"


def main() -> int:
    out = RET / "runtime" / "target"
    if out.exists():
        shutil.rmtree(out)
    archive = subprocess.run(
        ["git", "archive", TARGET_COMMIT, PREFIX],
        cwd=str(REPO), capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(RET / "runtime" / "_extract")
    shutil.move(str(RET / "runtime" / "_extract" / PREFIX), str(out))
    shutil.rmtree(RET / "runtime" / "_extract")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
