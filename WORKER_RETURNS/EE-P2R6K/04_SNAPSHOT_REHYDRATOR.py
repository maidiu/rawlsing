#!/usr/bin/env python3
"""Public-validation rehydrator for EE-P2R6K validated C11 snapshots."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_c11_ingest import record_counts_for_candidate, validate_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository


class SnapshotRehydrationError(RuntimeError):
    pass


def _load_codec():
    path = HERE / "02_C11_VALIDATED_SNAPSHOT_CODEC.py"
    spec = importlib.util.spec_from_file_location("ee_p2r6k_snapshot_codec", path)
    if spec is None or spec.loader is None:
        raise SnapshotRehydrationError("snapshot codec could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _require_equal(observed: Any, expected: Any, label: str) -> None:
    if canonical_json(observed) != canonical_json(expected):
        raise SnapshotRehydrationError(f"{label} mismatch")


def rehydrate_snapshot_bytes(data: bytes) -> tuple[Any, C11Repository, dict[str, Any]]:
    codec = _load_codec()
    snapshot = codec.parse_snapshot_bytes(data)
    candidate = codec.candidate_from_snapshot(snapshot)

    release = validate_c11_source_release(candidate)
    expected = snapshot["validated_release_identity"]
    expected_keys = {
        "release_ref", "source_artifact_ref", "source_release_manifest_hash",
        "semantic_release_hash", "replay_manifest_ref", "m01_m18_coverage",
        "repository_snapshot_identity",
    }
    if set(expected) != expected_keys:
        raise SnapshotRehydrationError("validated release identity field set mismatch")

    if release.release_ref != exact_ref(expected["release_ref"]):
        raise SnapshotRehydrationError("validated release exact ref mismatch")
    if release.source_artifact_ref != exact_ref(expected["source_artifact_ref"]):
        raise SnapshotRehydrationError("validated release source artifact ref mismatch")
    if release.source_release_manifest_hash != expected["source_release_manifest_hash"]:
        raise SnapshotRehydrationError("validated release source manifest hash mismatch")
    if release.semantic_release_hash != expected["semantic_release_hash"]:
        raise SnapshotRehydrationError("validated release semantic hash mismatch")
    if release.replay_manifest.ref != exact_ref(expected["replay_manifest_ref"]):
        raise SnapshotRehydrationError("validated release replay manifest ref mismatch")

    observed_coverage = {key: list(value) for key, value in release.m01_m18_coverage.items()}
    _require_equal(observed_coverage, expected["m01_m18_coverage"], "M01-M18 coverage")

    repository = C11Repository((release,))
    resolved = repository.resolve_release_exact(exact_ref(expected["release_ref"]))
    if resolved.release_ref != release.release_ref or resolved.semantic_release_hash != release.semantic_release_hash:
        raise SnapshotRehydrationError("repository exact resolution differs from public-validation release")
    if repository.snapshot_identity() != expected["repository_snapshot_identity"]:
        raise SnapshotRehydrationError("repository one-release snapshot identity mismatch")

    summary = snapshot["identity_summary"]
    counts = dict(record_counts_for_candidate(candidate))
    _require_equal(counts, summary["record_counts"], "candidate record counts")

    receipt = {
        "schema": "EE_P2R6K_C11_SNAPSHOT_REHYDRATION_RECEIPT@1.0.0",
        "status": "PASS",
        "snapshot": {
            "byte_length": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "schema": snapshot["schema"],
        },
        "candidate": {
            "source_release_manifest_hash": candidate.source_release_manifest.content_hash,
            "candidate_projection_hash": candidate.candidate_replay_manifest.semantic_projection_hash,
            "replay_manifest_ref": candidate.candidate_replay_manifest.ref.as_dict(),
            "record_counts": counts,
        },
        "validated_release": {
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "source_release_manifest_hash": release.source_release_manifest_hash,
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "m01_m18_coverage": observed_coverage,
        },
        "repository": {
            "release_count": len(repository),
            "snapshot_identity": repository.snapshot_identity(),
            "resolve_release_exact": "PASS",
        },
        "validation_path": [
            "SERIALIZED_CANONICAL_CANDIDATE_BODIES",
            "C11SourceReleaseCandidate",
            "validate_c11_source_release",
            "C11LogicalRelease",
            "C11Repository",
            "resolve_release_exact",
        ],
    }
    return release, repository, receipt


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    data = args.snapshot.read_bytes()
    _, _, receipt = rehydrate_snapshot_bytes(data)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    _write_json(args.receipt, receipt)
    print(json.dumps({
        "status": "PASS",
        "release_ref": receipt["validated_release"]["release_ref"],
        "snapshot_sha256": receipt["snapshot"]["sha256"],
        "receipt": str(args.receipt),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
