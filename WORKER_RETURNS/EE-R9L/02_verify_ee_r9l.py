#!/usr/bin/env python3
"""Read-only verification for the bounded EE-R9L source and B16 evidence."""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
from pathlib import Path

SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
B16_COMMIT = "f43c4be11d4f8fa98f538727337ec075d99d03bc"
B16_ROOT = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/"
    "PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/"
    "CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/"
    "WORKERS/B16_C05R2B_REAL_LITS1_PRODUCTION_I05_R1/DRIVER_SOURCE_CHUNKS"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_show(repo: Path, path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{B16_COMMIT}:{path}"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    assert sha256_file(args.source) == SOURCE_SHA256
    parts = tuple(git_show(args.repo, f"{B16_ROOT}/{name}") for name in ("part_00.b64", "part_01.b64"))
    encoded = b"".join(parts)
    assert tuple(map(len, parts)) == (7001, 3052)
    assert len(encoded) == 10053 and len(encoded) % 4 == 1
    try:
        base64.b64decode(encoded, validate=True)
    except Exception as exc:
        assert "Excess data after padding" in str(exc)
    else:
        raise AssertionError("strict B16 base64 unexpectedly decoded")
    try:
        gzip.decompress(base64.b64decode(encoded, validate=False))
    except Exception as exc:
        assert "invalid distance too far back" in str(exc)
    else:
        raise AssertionError("permissive B16 transport unexpectedly decompressed")
    print("PASS__EE_R9L_SOURCE_HASH_AND_B16_STRICT_BOOTSTRAP_NEGATIVE_REPRODUCED")


if __name__ == "__main__":
    main()
