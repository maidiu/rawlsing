"""GF1E — build the return manifest and sanitized environment passport delta."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
CONSUMER = RET.parent / "PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1" / "court" / "runtime_root" / "gf1_pair_support_consumer.py"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_blob(p):
    b = Path(p).read_bytes()
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode() + b"\0" + b)
    return h.hexdigest()


def xml_counts(p):
    import xml.etree.ElementTree as ET
    root = ET.parse(p).getroot()
    suite = root.find("testsuite") or root
    return {k: int(suite.get(k)) for k in ("tests", "failures", "errors", "skipped")}


passport = dict(
    schema="PYAT_R27_GF1E_ENVIRONMENT_PASSPORT_DELTA@1",
    environment_id="GF1E_LOCAL_CONSUMER_IMPLEMENTATION",
    epoch_id="GF1E_R27",
    session_alias="GF1E_R27",
    surface="S2_LOCAL_HOST",
    machine_alias="LOCAL_SHARED_STORE_HOST",
    status="LIVE_VERIFIED",
    observed_at_utc=datetime.now(timezone.utc).isoformat(),
    interpreter=platform.python_version(),
    pytest=subprocess.check_output([sys.executable, "-m", "pytest", "--version"], text=True).strip(),
    git=subprocess.check_output(["git", "--version"], text=True).strip(),
    platform=platform.system() + " " + platform.machine(),
    branch="agent/rabochii-pyat-r27-gf1e-actual-native-consumer-implementation-r1",
    sealed_startup="e9867879a0f0b3ac8d8afe21fced9e18a8a0a1fb",
    deliverable=dict(
        module="gf1_pair_support_consumer.py",
        sha256=sha(CONSUMER),
        git_blob_sha1=git_blob(CONSUMER),
    ),
    tests=dict(
        frozen44=xml_counts(RET / "observations" / "frozen44.xml"),
        differential=xml_counts(RET / "observations" / "gf1e_differential.xml"),
    ),
    cold_processes=2,
    model=dict(requested="Codex GPT-6.1 Sol High with sufficient Python time",
               observed_provider="DeepSeek Harness", actual_model="deepseek-v4-pro",
               actual_reasoning_effort="NOT_EXPOSED"),
    quota=dict(plan="UNKNOWN", incremental_cash="UNKNOWN"),
    independence="original GF1/GF1C/GF1D author continuation; independent corrected-delta review still required",
    privacy="synthetic fixtures only; no original SAV/DTA, credentials, source or actor grant",
    retire_or_reprobe="runtime reset, source/branch change, new rights, or unrelated task",
)
(RET / "environment_passport_delta.json").write_text(json.dumps(passport, indent=1, sort_keys=True) + "\n")

# artifact digests last (so every hashed file, including the passport, is final)
artifacts = {}
for p in sorted(RET.rglob("*")):
    if not p.is_file():
        continue
    rel = str(p.relative_to(RET))
    if rel == "artifact_sha256.json" or "__pycache__" in rel:
        continue
    artifacts[rel] = sha(p)
(RET / "artifact_sha256.json").write_text(json.dumps(artifacts, indent=1, sort_keys=True) + "\n")
print("artifacts", len(artifacts))
print("frozen44", passport["tests"]["frozen44"])
print("differential", passport["tests"]["differential"])
