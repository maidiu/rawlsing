"""E41 return seal: SHA256SUMS + source/return manifests (no secrets; relative paths)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RETURN_DIR = Path(__file__).resolve().parent
SKIP_NAMES = {"__pycache__", "SHA256SUMS", "source_manifest.json", "return_manifest.json"}
SKIP_SUFFIXES = {".pyc"}


def iter_files():
    for path in sorted(RETURN_DIR.rglob("*")):
        if path.is_dir():
            continue
        if any(part == "__pycache__" for part in path.parts):
            continue
        if path.name in SKIP_NAMES or path.suffix in SKIP_SUFFIXES:
            continue
        yield path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    entries = []
    for path in iter_files():
        relative = path.relative_to(RETURN_DIR).as_posix()
        entries.append((relative, sha256(path)))
    sums = "\n".join(f"{digest}  {name}" for name, digest in entries) + "\n"
    (RETURN_DIR / "SHA256SUMS").write_text(sums, encoding="utf-8")

    source_files = [
        name
        for name, _ in entries
        if not name.startswith("artifacts/") and not name.startswith("evidence/")
    ]
    source_manifest = {
        "schema": "E41_SOURCE_MANIFEST@1",
        "files": [
            {"path": name, "sha256": digest}
            for name, digest in entries
            if name in source_files
        ],
    }
    (RETURN_DIR / "source_manifest.json").write_text(
        json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return_manifest = {
        "schema": "E41_RETURN_MANIFEST@1",
        "branch": "agent/rabochii-pyat-r41-e41-full-f1f4-n10e-empirical-r1",
        "startup": "c4934fd71120d37a4d06f7c830891e6e97fe4ecf",
        "deliverables": {
            "frozen_universe": "frozen/expected_use_universe.json",
            "freeze_receipt": "frozen/FREEZE_RECEIPT.json",
            "coverage_ledger": "artifacts/f1f4_coverage_ledger.json",
            "f2": "artifacts/f2_predictor_surface.json",
            "f3": "artifacts/f3_branch_alternatives.json",
            "f4": "artifacts/f4_cloud_joint.json",
            "computed_slice_evidence": "artifacts/computed_slice_evidence.json",
            "slice_consumer_receipt": "artifacts/slice_consumer_receipt.json",
            "anti_join": "artifacts/anti_join_expected_actual.json",
            "provider_contract": "empirical_slice_provider_contract.md",
            "courts": "test_e41_tranche.py",
            "proof_contract": "test_e41_tranche.py.proof.json",
            "proof_witness": "evidence/proof_witness.json",
            "junit": "evidence/e41_junit.xml",
            "environment_passport": "environment_passport_delta.json",
        },
        "files": [{"path": name, "sha256": digest} for name, digest in entries],
        "no_authority_granted": True,
    }
    (RETURN_DIR / "return_manifest.json").write_text(
        json.dumps(return_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"sealed {len(entries)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
