#!/usr/bin/env python3
"""Materialize isolated run trees from the exact staged closure."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
RUNS = RETURN / "runs"
S = RETURN / "staged"
P = RETURN / "proofs"
MANIFEST = RETURN / "01_SOURCE_CUSTODY_AND_IMPORT_MANIFEST.json"

VARIANTS = {
    "r3_red": ("r3_kernel.py", [
        "test_fresh_i2_adversarial.py", "test_heldout_actor_independence.py",
        "test_local_hostile.py"]),
    "r4_green": ("r4_kernel.py", [
        "test_m2.py", "test_m3_independent.py", "test_m3_unresolved.py",
        "test_source_preimages.py", "test_original_preimage.py",
        "test_local_hostile.py", "test_relation_custody.py",
        "test_heldout_actor_independence.py", "test_r3_counterpart_actor_custody.py",
        "test_fresh_i2_adversarial.py", "test_r4_owner_rule_hostile.py",
        "test_r4_i2_new_hostiles.py"]),
    "r3_new": ("r3_kernel.py", [
        "test_fresh_i2_adversarial.py", "test_heldout_actor_independence.py",
        "test_local_hostile.py", "test_r4_i2_new_hostiles.py"]),
    "r2_control": ("r2_kernel.py", ["test_heldout_actor_independence.py"]),
    "m1_on_r2": ("r2_kernel.py", ["test_kernel.py"]),
    "i2_on_r2": ("r2_kernel.py", ["test_i2_strict.py"]),
    "m1_original": ("m1_kernel.py", ["test_kernel.py"]),
    "i2_on_m1": ("m1_kernel.py", ["test_i2_strict.py"]),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    expected = {row["path"]: row["sha256"] for row in manifest["rows"]}
    if RUNS.exists():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True)
    prepared = {}
    for name, (kernel_name, tests) in VARIANTS.items():
        run = RUNS / name
        run.mkdir()
        kernel_src = S / "kernels" / kernel_name
        kernel_dst = run / "kernel.py"
        shutil.copyfile(kernel_src, kernel_dst)
        if sha(kernel_dst) != expected[f"staged/kernels/{kernel_name}"]:
            raise SystemExit("KERNEL_HASH_MISMATCH:" + name)
        files = {"kernel.py": sha(kernel_dst)}
        for test in tests:
            if test in ("test_kernel.py", "test_i2_strict.py"):
                src = S / "historical" / test
            elif test == "test_m2.py":
                src = S / "source" / "source_test_m2.py"
            else:
                src = S / "tests" / test
            dst = run / test
            shutil.copyfile(src, dst)
            rel = src.relative_to(RETURN).as_posix()
            if sha(dst) != expected[rel]:
                raise SystemExit("TEST_HASH_MISMATCH:" + name + ":" + test)
            files[test] = sha(dst)
        if name == "r4_green":
            for proof in P.glob("*.proof.json"):
                shutil.copyfile(proof, run / proof.name)
                files[proof.name] = sha(run / proof.name)
        prepared[name] = files
    (RUNS / "_prepared_manifest.json").write_text(
        json.dumps(dict(schema="R35_M2R4E_PREPARED_RUNS@1", variants=prepared),
                   sort_keys=True, indent=2) + "\n")
    print(json.dumps({name: len(files) for name, files in prepared.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
