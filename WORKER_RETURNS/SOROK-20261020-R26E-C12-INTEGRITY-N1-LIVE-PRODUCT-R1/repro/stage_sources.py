"""Rebuild the read-only BP2P4J and N1 staged trees from exact commits."""
from __future__ import annotations

import io
import shutil
import subprocess
import tarfile
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
SOURCES = {
    "target": ("5b3e6577400ea1d88971ae6b48e41a118b8059ae",
               "WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1"),
    "n1": ("cd6b0fb9358c5f7d3c344c84a148d3fee48d2e16",
           "WORKER_RETURNS/SOROK-20261020-N1-NATIVE-ELIGIBLE-PSYCHE-SCIENCE-R1"),
}


def main() -> int:
    runtime = RET / "runtime"
    for name, (commit, prefix) in SOURCES.items():
        out = runtime / name
        if out.exists():
            shutil.rmtree(out)
        archive = subprocess.run(
            ["git", "archive", commit, prefix],
            cwd=str(REPO), capture_output=True, check=True).stdout
        extract = runtime / f"_extract_{name}"
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(extract)
        shutil.move(str(extract / prefix), str(out))
        shutil.rmtree(extract)
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
