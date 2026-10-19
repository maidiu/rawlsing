"""I44 return seal: SHA256SUMS + source/return manifests (relative paths only)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RETURN_DIR = Path(__file__).resolve().parent
SKIP_NAMES = {"__pycache__", "SHA256SUMS", "source_manifest.json", "return_manifest.json"}
SKIP_SUFFIXES = {".pyc"}


def iter_files():
    for path in sorted(RETURN_DIR.rglob("*")):
        if path.is_dir() or any(part == "__pycache__" for part in path.parts):
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
    entries = [(p.relative_to(RETURN_DIR).as_posix(), sha256(p)) for p in iter_files()]
    (RETURN_DIR / "SHA256SUMS").write_text(
        "\n".join(f"{digest}  {name}" for name, digest in entries) + "\n", encoding="utf-8"
    )
    source = [
        {"path": name, "sha256": digest} for name, digest in entries
        if name.endswith(".py") or name.endswith(".md") or name.endswith(".json")
        and not name.startswith("artifacts/") and not name.startswith("evidence/")
    ]
    (RETURN_DIR / "source_manifest.json").write_text(
        json.dumps({"schema": "I44_SOURCE_MANIFEST@1", "files": source},
                   indent=2, sort_keys=True) + "\n", encoding="utf-8")
    deliverables = {
        "f1_f8_acceptance_matrix.json": "artifacts/f1_f8_acceptance_matrix.json",
        "estate_acceptance_manifest.json": "artifacts/estate_acceptance_manifest.json",
        "final_maturity_adjudication.md": "artifacts/final_maturity_adjudication.md",
        "n11_r43_fanin_intake_and_delta.json": "artifacts/n11_r43_fanin_intake_and_delta.json",
        "i44_terminal_completion_delta.json": "artifacts/i44_terminal_completion_delta.json",
        "j42_addon_endpoint.json": "artifacts/j42_addon_endpoint.json",
        "merged_receipt_bank_i44.json": "artifacts/merged_receipt_bank_i44.json",
        "s44_receiving_interface_report.json": "artifacts/s44_receiving_interface_report.json",
        "courts": "test_i44_integration.py",
        "proof_contract": "test_i44_integration.py.proof.json",
        "proof_witness": "evidence/proof_witness.json",
        "junit": "evidence/i44_junit.xml",
        "environment_passport": "environment_passport_delta.json",
    }
    (RETURN_DIR / "return_manifest.json").write_text(
        json.dumps({
            "schema": "I44_RETURN_MANIFEST@1",
            "branch": "agent/rabochii-pyat-r44-i44-r43-four-return-native-world-n11-fanin-r1",
            "startup": "2e5a8693b2b48df5b2e1281e1d33ff2d5d5d2d2c",
            "pins": {
                "A42": "843175b0587b54db3df1f461ad9f7f1314894372",
                "J42": "f53cb0d2bce52640268c844c398bbd8007d28edc",
                "U43": "dcf71f1afbfdbe8a084844cea5fffbc73d9d91ef",
                "B43": "0fa15c1eda1ca36d89b0bbd948b655aa68f17370",
                "F43": "c0271e2b8d59018d3cf2af7b366258ea503295a6",
            },
            "deliverables": deliverables,
            "files": [{"path": name, "sha256": digest} for name, digest in entries],
            "no_authority_granted": True,
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"sealed {len(entries)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
