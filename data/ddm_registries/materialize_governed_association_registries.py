#!/usr/bin/env python3
"""Materialize the exact governed V550J association registries into canonical paths."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

LANE_RELATIVE = Path("data/ddm_registries/association_lane_registry.yaml")
THRESHOLD_RELATIVE = Path("data/ddm_registries/association_threshold_profiles.yaml")
LANE_SHA256 = "1848ae6b1c0823cfe7d34e34f71076543484a67a4721ea4de0d9ffef25b5d138"
LANE_SIZE = 5_539_418
THRESHOLD_SHA256 = "8d4e11b507bb4626e4c08fe508b0ea1fd196cfdeb211f90fb08634ac0c82259b"
THRESHOLD_SIZE = 2_558


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_exact(path: Path, expected_sha256: str, expected_size: int, label: str) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"{label}_MISSING: {path}")
    size = path.stat().st_size
    sha256 = sha256_file(path)
    if size != expected_size or sha256 != expected_sha256:
        raise RuntimeError(
            f"{label}_INTEGRITY_MISMATCH: path={path} size={size} sha256={sha256} "
            f"expected_size={expected_size} expected_sha256={expected_sha256}"
        )
    return {"path": str(path), "size_bytes": size, "sha256": sha256}


def materialize_lane(source: Path, destination: Path, replace_existing: bool) -> str:
    verify_exact(source, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_SOURCE")
    if destination.exists():
        try:
            verify_exact(destination, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_CANONICAL")
            return "already_exact"
        except RuntimeError:
            if not replace_existing:
                raise RuntimeError(
                    "ASSOCIATION_LANE_CANONICAL_CONFLICT: canonical path exists with non-governed bytes; "
                    "refusing replacement without --replace-existing"
                )

    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=destination.name + ".", suffix=".tmp", dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        verify_exact(temporary, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_STAGED")
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()
    verify_exact(destination, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_CANONICAL")
    return "materialized_exact"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Install the externally governed association lane registry only after exact byte verification, "
            "and verify the inline threshold-profile authority."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Rawlsing repository root (defaults from this script location).",
    )
    parser.add_argument(
        "--lane-source",
        type=Path,
        default=None,
        help=(
            "Path to the externally retained association_lane_registry.yaml. Required unless the canonical "
            "repository path already contains the exact governed bytes."
        ),
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace a conflicting canonical lane file, but only from an exact verified governed source.",
    )
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    lane = repo / LANE_RELATIVE
    threshold = repo / THRESHOLD_RELATIVE
    threshold_result = verify_exact(threshold, THRESHOLD_SHA256, THRESHOLD_SIZE, "ASSOCIATION_THRESHOLD_PROFILE")

    if lane.exists():
        try:
            lane_result = verify_exact(lane, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_CANONICAL")
            lane_action = "already_exact"
        except RuntimeError:
            if args.lane_source is None:
                raise
            lane_action = materialize_lane(args.lane_source.resolve(), lane, args.replace_existing)
            lane_result = verify_exact(lane, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_CANONICAL")
    else:
        if args.lane_source is None:
            raise RuntimeError(
                "ASSOCIATION_LANE_EXTERNAL_DEPENDENCY_REQUIRED: canonical governed registry is absent. "
                f"Supply --lane-source containing exactly sha256={LANE_SHA256}, size={LANE_SIZE}."
            )
        lane_action = materialize_lane(args.lane_source.resolve(), lane, args.replace_existing)
        lane_result = verify_exact(lane, LANE_SHA256, LANE_SIZE, "ASSOCIATION_LANE_CANONICAL")

    print(
        json.dumps(
            {
                "status": "PASS_GOVERNED_ASSOCIATION_REGISTRIES_MATERIALIZED",
                "lane_action": lane_action,
                "association_lane_registry": lane_result,
                "association_threshold_profiles": threshold_result,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
