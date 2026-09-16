#!/usr/bin/env python3
from __future__ import annotations

import base64
import collections
import hashlib
import pathlib
import subprocess
import zlib

THIS = pathlib.Path(__file__).resolve()
REPO = next((p for p in [THIS.parent, *THIS.parents] if (p / ".git").exists()), None)
if REPO is None:
    raise RuntimeError("repository root not found")

R4A_COMMIT = "238800fe20f257194530916514289492601eeff1"
R4A_MASK = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N04-R4A/02_SELECTED_18012_MASK.zlib.b64"
)
R3_COMMIT = "8e0266703bbf3b060abcd6fbe53c7ef6c49062c5"
R3_VECTOR = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N04-R3/03_CURRENT_18276_BINDING_STATUS_VECTOR.zlib.b64"
)

R4A_EXPECTED_MASK_B64_SHA = "2b22305dda73bcf27d5d5de3c2adbd674e544ab09d7fbb35aa7a7138dc7674db"
R4A_EXPECTED_MASK_RAW_SHA = "58f5fc1288588874235288e046c1797968263303135af8ceb58cc37da48c112e"
R4A_EXPECTED_ORDINAL_BYTES = 98754
R4A_EXPECTED_ORDINAL_SHA = "c6092adb1a55233b8b372222639dcac0c7de8bb4ceff06a07d9e7d1ffe40db6c"

R3_EXPECTED_B64_SHA = "8241edb2bf043105e0eae12dfa8dd312ff14ca09d37141467834529404c161d7"
R3_EXPECTED_RAW_SHA = "f3bb9f06508f7eb26d1ee01e6bc865377637da34f5a60b4118006cc5d8a8d283"
R3_EXPECTED_COUNTS = {1: 41, 2: 22, 3: 18012, 4: 159, 5: 42}

DERIVED_MASK_SHA = "58f5fc12b968fad266e75e17be9f21d727d684535d0a78bb5e5ff5196d1c112e"
DERIVED_ORDINAL_BYTES = 97135
DERIVED_ORDINAL_SHA = "769fc7c501f60797dd91aae184517edd76b50740db66f9340b6d42884ff3e021"

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def run(*args: str) -> bytes:
    p = subprocess.run(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace"))
    return p.stdout

def ensure_commit(commit: str) -> None:
    p = subprocess.run(["git","cat-file","-e",commit+"^{commit}"],cwd=REPO)
    if p.returncode:
        subprocess.run(["git","fetch","--no-tags","--depth=1","origin",commit],cwd=REPO,check=True)

def show(commit: str, path: str) -> bytes:
    ensure_commit(commit)
    return run("git","show",f"{commit}:{path}")

def main() -> None:
    bad = show(R4A_COMMIT, R4A_MASK)
    assert len(bad) == 102
    bad_s = bad.strip()
    assert len(bad_s) == 101
    assert sha(bad_s) == "a1488b811a77c5a64f030c56bfa5a7e4a5d3ac6939f82b5690eb5630a2f22302"
    assert sha(bad_s) != R4A_EXPECTED_MASK_B64_SHA

    strict_failed = False
    try:
        base64.b64decode(bad_s, validate=True)
    except Exception:
        strict_failed = True
    assert strict_failed

    permissive = base64.b64decode(bad_s)
    zlib_failed = False
    try:
        zlib.decompress(permissive)
    except zlib.error:
        zlib_failed = True
    assert zlib_failed

    vec_b64 = show(R3_COMMIT, R3_VECTOR).strip()
    assert sha(vec_b64) == R3_EXPECTED_B64_SHA
    vec = zlib.decompress(base64.b64decode(vec_b64))
    assert len(vec) == 18276
    assert sha(vec) == R3_EXPECTED_RAW_SHA
    assert dict(sorted(collections.Counter(vec).items())) == R3_EXPECTED_COUNTS

    derived = bytes(1 if code == 3 else 0 for code in vec)
    assert len(derived) == 18276
    assert sum(derived) == 18012
    assert sha(derived) == DERIVED_MASK_SHA
    assert sha(derived) != R4A_EXPECTED_MASK_RAW_SHA

    ordinal = "".join(f"{i+1}\n" for i, bit in enumerate(derived) if bit).encode()
    assert len(ordinal) == DERIVED_ORDINAL_BYTES
    assert sha(ordinal) == DERIVED_ORDINAL_SHA
    assert len(ordinal) != R4A_EXPECTED_ORDINAL_BYTES
    assert sha(ordinal) != R4A_EXPECTED_ORDINAL_SHA

    print("EE-R2C BLOCKER PROVED: accepted R4A selector carrier/replay/receipt are internally inconsistent")

if __name__ == "__main__":
    main()
