"""G50 seal: SHA256SUMS + source/return manifests (relative paths)."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
RETURN_DIR = Path(__file__).resolve().parent
SKIP = {"__pycache__", "SHA256SUMS", "source_manifest.json", "return_manifest.json"}
def files():
    for p in sorted(RETURN_DIR.rglob("*")):
        if p.is_dir() or any(x == "__pycache__" for x in p.parts):
            continue
        if p.name in SKIP or p.suffix == ".pyc":
            continue
        yield p
def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()
def main():
    entries = [(p.relative_to(RETURN_DIR).as_posix(), sha(p)) for p in files()]
    (RETURN_DIR / "SHA256SUMS").write_text("\n".join(f"{d}  {n}" for n, d in entries) + "\n")
    (RETURN_DIR / "source_manifest.json").write_text(json.dumps({
        "schema": "G50_SOURCE_MANIFEST@1",
        "files": [{"path": n, "sha256": d} for n, d in entries
                  if n.endswith((".py", ".md", ".json", ".csv")) and not n.startswith(("artifacts/", "evidence/"))],
    }, indent=2, sort_keys=True) + "\n")
    (RETURN_DIR / "return_manifest.json").write_text(json.dumps({
        "schema": "G50_RETURN_MANIFEST@1",
        "branch": "agent/rabochii-pyat-r50-g50-governed-operation-grammar-native-producer-r1",
        "startup": "5a67ab44fc9d96f8040d89557ba462a74df2cecc",
        "deliverables": {
            "frontier": "artifacts/frontier_summary.json",
            "expected_root": "artifacts/expected_frontier_root.json",
            "native_receipts": "artifacts/native_i05_receipts.json",
            "canaries": "artifacts/28_CANARY_DISPOSITION.csv",
            "census": "artifacts/original35_census.json",
            "decisions": "artifacts/DECISION_DEMANDS.json",
            "plan": "artifacts/native_construction_plan.json",
            "b49_plan": "B49_INTERFACE_PLAN.md",
            "proof_witness": "evidence/proof_witness.json",
            "junit": "evidence/g50_junit.xml",
        },
        "files": [{"path": n, "sha256": d} for n, d in entries],
        "no_authority_granted": True,
    }, indent=2, sort_keys=True) + "\n")
    print(f"sealed {len(entries)} files")
if __name__ == "__main__":
    main()
