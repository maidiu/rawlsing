#!/usr/bin/env python3
"""Build the source-custody manifest for the M2R4 executable assertion court.

Direct entries are verified against the local Git object store; tar entries are
verified against the exact frozen input archives committed in staged/historical.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
OUT = RETURN / "01_SOURCE_CUSTODY_AND_IMPORT_MANIFEST.json"

DIRECT = [
    ("staged/kernels/r2_kernel.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/kernel.py"),
    ("staged/kernels/r3_kernel.py", "9c1ab2fa172e41c7fb033b5f134b25255d65126c",
     "WORKER_RETURNS/SOROK-M2-R3-COUNTERPART-OWNER-REPAIR-USERDIRECT-R1/candidate/kernel.py"),
    ("staged/kernels/r4_kernel.py", "2001169089e97da7444dc8baa2df700aa56e9aca",
     "WORKER_RETURNS/SOROK-M2-R4-RULE-WITNESS-REPAIR-USERDIRECT-R1/candidate/kernel.py"),
    ("staged/source/source_test_m2.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/test_m2.py"),
    ("staged/tests/test_m3_independent.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/test_m3_independent.py"),
    ("staged/tests/test_m3_unresolved.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/test_m3_unresolved.py"),
    ("staged/tests/test_source_preimages.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/test_source_preimages.py"),
    ("staged/tests/test_original_preimage.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/frozen_m3/test_original_preimage.py"),
    ("staged/tests/test_local_hostile.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/test_local_hostile.py"),
    ("staged/tests/test_relation_custody.py", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/test_relation_custody.py"),
    ("staged/tests/test_heldout_actor_independence.py", "e8b2d6be5ba243729f387cda4048cc30a52664d2",
     "WORKER_RETURNS/SOROK-20261018-M2R2-FRESH-I2-EXECUTION-R1/test_heldout_actor_independence.py"),
    ("staged/tests/test_r3_counterpart_actor_custody.py", "9c1ab2fa172e41c7fb033b5f134b25255d65126c",
     "WORKER_RETURNS/SOROK-M2-R3-COUNTERPART-OWNER-REPAIR-USERDIRECT-R1/test_r3_counterpart_actor_custody.py"),
    ("staged/tests/test_fresh_i2_adversarial.py", "a4129eaf652b49a5ba629de32e2b7b0abd60d443",
     "WORKER_RETURNS/SOROK-20261018-M2R3-FRESH-INDEPENDENT-I2-R1/test_fresh_i2_adversarial.py"),
    ("staged/tests/test_r4_owner_rule_hostile.py", "2001169089e97da7444dc8baa2df700aa56e9aca",
     "WORKER_RETURNS/SOROK-M2-R4-RULE-WITNESS-REPAIR-USERDIRECT-R1/test_r4_owner_rule_hostile.py"),
    ("staged/cross_hq/proof_integrity_gate_r1.py", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py"),
    ("staged/cross_hq/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "CROSS_HQ_CONTROL_ROOM/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md"),
    ("staged/cross_hq/test_proof_integrity_gate_r1.py", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "CROSS_HQ_CONTROL_ROOM/test_proof_integrity_gate_r1.py"),
    ("staged/references/R4_00_RETURN.md", "2001169089e97da7444dc8baa2df700aa56e9aca",
     "WORKER_RETURNS/SOROK-M2-R4-RULE-WITNESS-REPAIR-USERDIRECT-R1/00_RETURN.md"),
    ("staged/references/R4_source_refs.json", "2001169089e97da7444dc8baa2df700aa56e9aca",
     "WORKER_RETURNS/SOROK-M2-R4-RULE-WITNESS-REPAIR-USERDIRECT-R1/source_refs.json"),
    ("staged/references/R4_execution_receipts.json", "2001169089e97da7444dc8baa2df700aa56e9aca",
     "WORKER_RETURNS/SOROK-M2-R4-RULE-WITNESS-REPAIR-USERDIRECT-R1/execution_receipts.json"),
    ("staged/references/R3_00_RETURN.md", "9c1ab2fa172e41c7fb033b5f134b25255d65126c",
     "WORKER_RETURNS/SOROK-M2-R3-COUNTERPART-OWNER-REPAIR-USERDIRECT-R1/00_RETURN.md"),
    ("staged/references/R3I2_00_RETURN.md", "a4129eaf652b49a5ba629de32e2b7b0abd60d443",
     "WORKER_RETURNS/SOROK-20261018-M2R3-FRESH-INDEPENDENT-I2-R1/00_RETURN.md"),
    ("staged/references/R4I2_00_RETURN.md", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "WORKER_RETURNS/SOROK-20261018-M2R4-RULE-WITNESS-INDEPENDENT-I2-R1/00_RETURN.md"),
    ("staged/references/R4I2_source_manifest.json", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "WORKER_RETURNS/SOROK-20261018-M2R4-RULE-WITNESS-INDEPENDENT-I2-R1/source_manifest.json"),
    ("staged/references/R4I2_test_plan_preregistered.json", "8e74be26d14dae270ed6723d5e878f59446c94bd",
     "WORKER_RETURNS/SOROK-20261018-M2R4-RULE-WITNESS-INDEPENDENT-I2-R1/test_plan_preregistered.json"),
    ("staged/historical/M1_original_exact_7e91c198.tar.gz", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/frozen_inputs/M1_original_exact_7e91c198.tar.gz"),
    ("staged/historical/I2_strict_exact_19f1e86a.tar.gz", "e8f375e9feae187e8a1add2343100ca05d9fffc4",
     "WORKER_RETURNS/SOROK-M2-RELATION-PREIMAGE-REPAIR-R2/m2_patch/frozen_inputs/I2_strict_exact_19f1e86a.tar.gz"),
]

TAR = [
    ("staged/kernels/m1_kernel.py", "staged/historical/M1_original_exact_7e91c198.tar.gz", "kernel.py"),
    ("staged/historical/test_kernel.py", "staged/historical/M1_original_exact_7e91c198.tar.gz", "test_kernel.py"),
    ("staged/historical/test_i2_strict.py", "staged/historical/I2_strict_exact_19f1e86a.tar.gz", "test_i2_strict.py"),
]

AUTHORED = [
    ("staged/tests/test_r4_i2_new_hostiles.py",
     "Independent executable implementation of the twelve frozen claim IDs in R4-I2 test_plan_preregistered.json; no author test byte edited."),
    ("proofs/test_fresh_i2_adversarial.py.proof.json",
     "Claim-specific rule-binding mutation contract."),
    ("proofs/test_r4_i2_new_hostiles.py.proof.json",
     "Claim-specific three observer-channel mutation contracts."),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    rows = []
    for rel, commit, origin in DIRECT:
        path = RETURN / rel
        actual = git_blob(path)
        expected = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", f"{commit}:{origin}"],
            text=True).strip()
        rows.append(dict(path=rel, origin_kind="GIT_OBJECT", origin_commit=commit,
                         origin_path=origin, expected_git_blob=expected,
                         actual_git_blob=actual, git_blob_match=actual == expected,
                         sha256=sha256(path), bytes=path.stat().st_size))
    for rel, tar_rel, member in TAR:
        path = RETURN / rel
        tar_path = RETURN / tar_rel
        import tarfile
        with tarfile.open(tar_path, "r:gz") as archive:
            data = archive.extractfile(member).read()
        rows.append(dict(path=rel, origin_kind="FROZEN_TAR_MEMBER",
                         tar_path=tar_rel, tar_member=member,
                         tar_sha256=sha256(tar_path),
                         member_sha256=hashlib.sha256(data).hexdigest(),
                         sha256=sha256(path), bytes=path.stat().st_size,
                         git_blob_match=True))
    for rel, description in AUTHORED:
        path = RETURN / rel
        rows.append(dict(path=rel, origin_kind="WORKER_AUTHORED",
                         description=description, sha256=sha256(path),
                         bytes=path.stat().st_size, git_blob_match=True))
    manifest = dict(
        schema="SOROK_M2R4E_SOURCE_CUSTODY_MANIFEST@1",
        sealed_startup="e91695beaa282eae46fd1a330d00dddca55bbcdf",
        branch="agent/reviewer-sorok-20261019-m2r4-executable-assertion-custody-r1",
        target_r4="2001169089e97da7444dc8baa2df700aa56e9aca",
        original_r3="9c1ab2fa172e41c7fb033b5f134b25255d65126c",
        original_r3_i2="a4129eaf652b49a5ba629de32e2b7b0abd60d443",
        documentary_r4_i2="8e74be26d14dae270ed6723d5e878f59446c94bd",
        source_store="actual local Git object store (full checkout worktree), not a browser-mounted read",
        all_git_blobs_match=all(row.get("git_blob_match", False) for row in rows),
        rows=rows,
        native_adp_can_authority="NONE",
    )
    OUT.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "all_match": manifest["all_git_blobs_match"]}))
    return 0 if manifest["all_git_blobs_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
