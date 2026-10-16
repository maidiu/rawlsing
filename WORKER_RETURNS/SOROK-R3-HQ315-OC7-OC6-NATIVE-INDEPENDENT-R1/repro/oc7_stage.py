#!/usr/bin/env python3
"""OC7 independent staging of the native custody source+test closure.

Reviewer-authored. Stages exact bytes from pinned commits, computing Git blob
SHA-1 from the true binary preimage and SHA-256, and re-verifying the declared
blobs rather than trusting any author manifest.

Two closure members are .tar.xz archive members and are extracted, not
script-transcribed.
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile

REPO = os.environ["OC7_REPO"]
OUT = os.environ["OC7_STAGE"]

# (commit, repo_path, staged_name, expected_git_blob_sha1, expected_sha256)
CLOSURE = [
    (
        "0caaec590f6a8bf6744f22dc9c948c5fe233bc94",
        "WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py",
        "custody_protocol.ORIGINAL_OC4.py",
        "af2b7e943018077cb36808b5af1cd67704624bec",
        "447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a",
    ),
    (
        "19438890e43153e2bc4a1ad271b5e19bcef33e1e",
        "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/dummy_corpus.py",
        "dummy_corpus.py",
        "770efe72190e35d1bc34065b5a55c183bf1320f5",
        "143137d985826aad185c8081d4f62094345cd46b693a6f9f3e521535c99c4c58",
    ),
    (
        "19438890e43153e2bc4a1ad271b5e19bcef33e1e",
        "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_custody_hostiles.py",
        "test_custody_hostiles.py",
        "94ad944997cb9d1a8d6527e91c17416120c5108d",
        "5075b3a40efec6d05b5e734d2d2fed8934fe429982168724b6e91ee10def128d",
    ),
    (
        "a61d5794271038fb20c94a75eaee401a66613ce9",
        "WORKER_RETURNS/SOROK-R3-HQ308-OC2-CUSTODY-RED-REPAIR-R1/repro/test_oc2_regressions.py",
        "test_oc2_regressions.py",
        "402f04ef7d6b8119f72df9355b554e797b9a501e",
        "f5a3ca376ff1c527c66911abc33fdb6bdbd3f483874a8f4b390a3513349ebad7",
    ),
    (
        "0caaec590f6a8bf6744f22dc9c948c5fe233bc94",
        "WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/test_oc4_repair_controls.py",
        "test_oc4_repair_controls.py",
        "c139a877aa4586ec5ab729d333c40037840721d4",
        "3b34bdb61c7ca0da6eae50a8bfa636a38a1dff6704dbacaee5fa1dd0808f445a",
    ),
    (
        "8185d2ca41ac5c5711b3f3f528e6f644dbab185d",
        "WORKER_RETURNS/SOROK-R3-HQ311-OC5-OC4-INDEPENDENT-R1/03_TESTS/test_oc5_candidate_hostiles.py",
        "test_oc5_prior_predictions.py",
        "588f91c712fc4000cebf7b9fa7b05e36ab01a126",
        "848c7c0cb31c31d9d4d99b0c7fb055bcaacf2f825ee3d3b69a7fcb767ba25c20",
    ),
    (
        "67a4f1561cdad40192f00797d66b24fc4cd91589",
        "WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py",
        "test_oc5e_native_hostiles.py",
        "9837579ebb5b2fbf3a41c967e584a166786e46b9",
        "a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512",
    ),
    (
        "19438890e43153e2bc4a1ad271b5e19bcef33e1e",
        "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_positive_lifecycle.py",
        "test_positive_lifecycle.py",
        "4b665a2a9d6999071624d580f2d2ae193daf59f4",
        "f231bf42a23d5e82bbdddef1a95b1aef2d6b11e217e553de3df0f156d0bef064",
    ),
]

# Archive-member extractions: (commit, tarpath, member_suffix, staged_name, expected_sha256)
ARCHIVE_CLOSURE = [
    (
        "9cd47a829473a6e92392582b4f01f2c564aa5dce",
        "WORKER_RETURNS/SOROK-R3-HQ309-OC3-CUSTODY-INDEPENDENT-R1/OC3_REMOTE_CORE_EVIDENCE.tar.xz",
        "source/test_oc3_independent_hostile.py",
        "test_oc3_independent_hostile.py",
        "994b9750c2b17867cec9d0cc2a9826209542998f65d2a8aa4fabcf4a7cad192b",
    ),
    (
        "aba637265bea2358790fea50d0e7abc98141e472",
        "WORKER_RETURNS/SOROK-R3-HQ307-OCR1-CUSTODY-HOSTILE-INDEPENDENT-R1/OCR1_EXECUTED_EVIDENCE.tar.xz",
        "source/test_ocr1_independent_hostile.py",
        "test_ocr1_independent_hostile.py",
        "ed73f0721ae0ff8b93da97043e1d12eb7658a360f3e03f1ea4a4919230437865",
    ),
]


def git_blob_sha1(data: bytes) -> str:
    hdr = b"blob " + str(len(data)).encode() + b"\x00"
    return hashlib.sha1(hdr + data).hexdigest()


def git_cat(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", REPO, "cat-file", "blob", f"{commit}:{path}"],
        check=True, capture_output=True,
    ).stdout


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    ledger = []
    failures = []

    for commit, path, staged, eblob, esha in CLOSURE:
        data = git_cat(commit, path)
        blob = git_blob_sha1(data)
        sha = hashlib.sha256(data).hexdigest()
        # Independent cross-check against git's own object store.
        git_blob = subprocess.run(
            ["git", "-C", REPO, "rev-parse", f"{commit}:{path}"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        ok = (blob == eblob == git_blob) and (sha == esha)
        if not ok:
            failures.append(staged)
        with open(os.path.join(OUT, staged), "wb") as fh:
            fh.write(data)
        ledger.append({
            "kind": "git_blob", "commit": commit, "repo_path": path,
            "staged": staged, "bytes": len(data),
            "computed_git_blob_sha1": blob, "git_store_blob_sha1": git_blob,
            "declared_git_blob_sha1": eblob,
            "computed_sha256": sha, "declared_sha256": esha,
            "all_match": ok,
        })
        print(f"{'OK  ' if ok else 'FAIL'} {staged:38s} blob={blob} sha256={sha[:16]}...")

    for commit, tarpath, member, staged, esha in ARCHIVE_CLOSURE:
        blob = subprocess.run(
            ["git", "-C", REPO, "rev-parse", f"{commit}:{tarpath}"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        raw = git_cat(commit, tarpath)
        # Read compressed bytes via lzma to avoid writing a temp file.
        import lzma
        plain = lzma.decompress(raw)
        tf = tarfile.open(fileobj=io.BytesIO(plain))
        member_name = None
        for m in tf.getmembers():
            if m.name.endswith(member):
                member_name = m.name
                break
        if member_name is None:
            failures.append(staged)
            print(f"FAIL {staged}: member {member} not found in {tarpath}")
            continue
        data = tf.extractfile(member_name).read()
        sha = hashlib.sha256(data).hexdigest()
        ok = sha == esha
        if not ok:
            failures.append(staged)
        with open(os.path.join(OUT, staged), "wb") as fh:
            fh.write(data)
        ledger.append({
            "kind": "tar_xz_archive_member", "commit": commit,
            "repo_path": tarpath, "tar_blob_sha1": blob,
            "archive_member": member_name, "staged": staged,
            "bytes": len(data), "computed_sha256": sha,
            "declared_sha256": esha, "all_match": ok,
            "note": "git blob SHA-1 is the archive blob, not the member; "
                    "member identity is pinned by SHA-256 of extracted bytes",
        })
        print(f"{'OK  ' if ok else 'FAIL'} {staged:38s} member={member_name} sha256={sha[:16]}...")

    print(json.dumps({"ledger": ledger}, indent=2))
    with open(os.path.join(OUT, "_stage_ledger.json"), "w") as fh:
        json.dump({"ledger": ledger, "failures": failures}, fh, indent=2)
    if failures:
        print("STAGING FAILURES:", failures)
        return 1
    print("ALL STAGED OBJECTS VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
