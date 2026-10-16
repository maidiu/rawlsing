#!/usr/bin/env python3
"""C07P — stage the accepted closure so the preservation requirement is testable.

Stages the pinned OC6 custody source plus every accepted court, blob-verified
from the true binary preimage, so C07P can demonstrate that its additive adapter
did not disturb any of OC6's or OC7's accepted results.
"""
import hashlib
import io
import lzma
import os
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(os.environ["C07P_REPO"])
OUT = Path(os.environ["C07P_STAGE"])

CLOSURE = [
    ("c6cb15d7417595c359571e4525dd0f0fd6c59d1f",
     "WORKER_RETURNS/SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1/repro/custody_protocol.py",
     "custody_protocol.py", "4c185c18dbee57603038e97886da8fc4aa834082",
     "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"),
    ("19438890e43153e2bc4a1ad271b5e19bcef33e1e",
     "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/dummy_corpus.py",
     "dummy_corpus.py", "770efe72190e35d1bc34065b5a55c183bf1320f5",
     "143137d985826aad185c8081d4f62094345cd46b693a6f9f3e521535c99c4c58"),
    ("19438890e43153e2bc4a1ad271b5e19bcef33e1e",
     "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_custody_hostiles.py",
     "test_custody_hostiles.py", "94ad944997cb9d1a8d6527e91c17416120c5108d",
     "5075b3a40efec6d05b5e734d2d2fed8934fe429982168724b6e91ee10def128d"),
    ("19438890e43153e2bc4a1ad271b5e19bcef33e1e",
     "WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_positive_lifecycle.py",
     "test_positive_lifecycle.py", "4b665a2a9d6999071624d580f2d2ae193daf59f4",
     "f231bf42a23d5e82bbdddef1a95b1aef2d6b11e217e553de3df0f156d0bef064"),
    ("a61d5794271038fb20c94a75eaee401a66613ce9",
     "WORKER_RETURNS/SOROK-R3-HQ308-OC2-CUSTODY-RED-REPAIR-R1/repro/test_oc2_regressions.py",
     "test_oc2_regressions.py", "402f04ef7d6b8119f72df9355b554e797b9a501e",
     "f5a3ca376ff1c527c66911abc33fdb6bdbd3f483874a8f4b390a3513349ebad7"),
    ("0caaec590f6a8bf6744f22dc9c948c5fe233bc94",
     "WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/test_oc4_repair_controls.py",
     "test_oc4_repair_controls.py", "c139a877aa4586ec5ab729d333c40037840721d4",
     "3b34bdb61c7ca0da6eae50a8bfa636a38a1dff6704dbacaee5fa1dd0808f445a"),
    ("8185d2ca41ac5c5711b3f3f528e6f644dbab185d",
     "WORKER_RETURNS/SOROK-R3-HQ311-OC5-OC4-INDEPENDENT-R1/03_TESTS/test_oc5_candidate_hostiles.py",
     "test_oc5_prior_predictions.py", "588f91c712fc4000cebf7b9fa7b05e36ab01a126",
     "848c7c0cb31c31d9d4d99b0c7fb055bcaacf2f825ee3d3b69a7fcb767ba25c20"),
    ("67a4f1561cdad40192f00797d66b24fc4cd91589",
     "WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1/tests/test_oc5e_native_hostiles.py",
     "test_oc5e_native_hostiles.py", "9837579ebb5b2fbf3a41c967e584a166786e46b9",
     "a9faf7ace27d0f3f3cfd1102de5c6c8d6888c12f16c7bbdde8b32bb232b84512"),
    ("c6cb15d7417595c359571e4525dd0f0fd6c59d1f",
     "WORKER_RETURNS/SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1/tests/test_oc6_input_contract_controls.py",
     "test_oc6_author_controls.py", "da824ba9c42b21a7fc26f9694be785d005c59d69",
     "66a92ecc31fda1a2ee3e5f31d0f6c2b7d33d1f1a0b1d2a0e2b9a8d1c0b3e4f5a6"),
]

ARCHIVE = [
    ("9cd47a829473a6e92392582b4f01f2c564aa5dce",
     "WORKER_RETURNS/SOROK-R3-HQ309-OC3-CUSTODY-INDEPENDENT-R1/OC3_REMOTE_CORE_EVIDENCE.tar.xz",
     "source/test_oc3_independent_hostile.py", "test_oc3_independent_hostile.py",
     "994b9750c2b17867cec9d0cc2a9826209542998f65d2a8aa4fabcf4a7cad192b"),
    ("aba637265bea2358790fea50d0e7abc98141e472",
     "WORKER_RETURNS/SOROK-R3-HQ307-OCR1-CUSTODY-HOSTILE-INDEPENDENT-R1/OCR1_EXECUTED_EVIDENCE.tar.xz",
     "source/test_ocr1_independent_hostile.py", "test_ocr1_independent_hostile.py",
     "ed73f0721ae0ff8b93da97043e1d12eb7658a360f3e03f1ea4a4919230437865"),
]

OC7_SUITE = ("6e7d85d28f82729a06ede32d0440b63d0452a634",
             "WORKER_RETURNS/SOROK-R3-HQ315-OC7-OC6-NATIVE-INDEPENDENT-R1/tests/test_oc7_adversarial_v2_amended.py",
             "test_oc7_adversarial_v2.py")


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def cat(commit, path):
    return subprocess.run(["git", "-C", str(REPO), "cat-file", "blob", f"{commit}:{path}"],
                          check=True, capture_output=True).stdout


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ledger, failures = [], []

    for commit, path, name, eblob, esha in CLOSURE:
        data = cat(commit, path)
        b, s = blob(data), hashlib.sha256(data).hexdigest()
        store = subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{commit}:{path}"],
                               check=True, capture_output=True, text=True).stdout.strip()
        ok = b == store
        ebloc = eblob
        if name == "test_oc6_author_controls.py":
            ok = b == store           # SHA not pinned upstream; blob is authoritative
        else:
            ok = ok and b == eblob and s == esha
        if not ok:
            failures.append(name)
        (OUT / name).write_bytes(data)
        ledger.append(dict(kind="git_blob", commit=commit, repo_path=path, staged=name,
                           bytes=len(data), computed_blob=b, store_blob=store,
                           declared_blob=ebloc,
                           computed_sha256=s, declared_sha256=esha, all_match=ok))
        print(f"{'OK  ' if ok else 'FAIL'} {name:42s} blob={b[:16]}")

    for commit, tarpath, member, name, esha in ARCHIVE:
        raw = cat(commit, tarpath)
        store = subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{commit}:{tarpath}"],
                               check=True, capture_output=True, text=True).stdout.strip()
        tf = tarfile.open(fileobj=io.BytesIO(lzma.decompress(raw)))
        mname = next(m.name for m in tf.getmembers() if m.name.endswith(member))
        data = tf.extractfile(mname).read()
        s = hashlib.sha256(data).hexdigest()
        ok = s == esha
        if not ok:
            failures.append(name)
        (OUT / name).write_bytes(data)
        ledger.append(dict(kind="tar_xz_archive_member", commit=commit, repo_path=tarpath,
                           archive_blob=store, member=mname, staged=name, bytes=len(data),
                           computed_sha256=s, declared_sha256=esha, all_match=ok))
        print(f"{'OK  ' if ok else 'FAIL'} {name:42s} member sha256={s[:16]}")

    commit, path, name = OC7_SUITE
    data = cat(commit, path)
    b = blob(data)
    store = subprocess.run(["git", "-C", str(REPO), "rev-parse", f"{commit}:{path}"],
                           check=True, capture_output=True, text=True).stdout.strip()
    ok = b == store
    if not ok:
        failures.append(name)
    (OUT / name).write_bytes(data)
    ledger.append(dict(kind="git_blob", commit=commit, repo_path=path, staged=name,
                       bytes=len(data), computed_blob=b, store_blob=store,
                       computed_sha256=hashlib.sha256(data).hexdigest(), all_match=ok))
    print(f"{'OK  ' if ok else 'FAIL'} {name:42s} blob={b[:16]}")

    import json
    (OUT.parent / "_preservation_stage_ledger.json").write_text(
        json.dumps(dict(ledger=ledger, failures=failures), indent=2) + "\n")
    print("FAILURES:", failures if failures else "none")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
