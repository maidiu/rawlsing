"""GF1F — build the return artifact manifest and environment passport delta."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RET = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def xml_counts(p):
    import xml.etree.ElementTree as ET
    root = ET.parse(p).getroot()
    suite = [s for s in root.iter("testsuite")][0] if root.tag != "testsuite" else root
    return {k: int(suite.get(k)) for k in ("tests", "failures", "errors", "skipped")}


passport = dict(
    schema="GF1F_SANITIZED_ENVIRONMENT_PASSPORT_DELTA@1",
    environment_id="GF1F_LOCAL_REVIEWER",
    epoch_id="GF1F_R28",
    session_alias="GF1F_R28",
    surface="S2_LOCAL_HOST",
    machine_alias="LOCAL_SHARED_STORE_HOST",
    status="LIVE_VERIFIED",
    observed_at_utc=datetime.now(timezone.utc).isoformat(),
    interpreter=platform.python_version(),
    pytest=subprocess.check_output([sys.executable, "-m", "pytest", "--version"], text=True).strip(),
    git=subprocess.check_output(["git", "--version"], text=True).strip(),
    branch="agent/reviewer-pyat-r28-gf1f-implemented-consumer-independent-r1",
    sealed_startup="3686021a0f1c79e5e14c94fc736e1c36f51fddca",
    candidate=dict(
        branch="agent/rabochii-pyat-r27-gf1e-actual-native-consumer-implementation-r1",
        sha="eeb726357204653b22458dc267dd70ba0009bd77",
        consumer_sha256="06dd484b0e9b4b2c9fb0a1583453ac7ffa8c052135304eaaee167a34127cb402",
    ),
    courts=dict(
        independent=xml_counts(RET / "observations" / "gf1f_independent_court.xml"),
        frozen44=xml_counts(RET / "observations" / "frozen44.xml"),
        gf1i19=xml_counts(RET / "observations" / "gf1i19.xml"),
    ),
    model=dict(commissioned="GPT-6 High / capable Codex Medium/High genuine Python",
               observed="DeepSeek Harness", actual_model="deepseek-flash",
               actual_reasoning_effort="NOT_EXPOSED"),
    independence="different model/agent from the GF1E implementer, but SAME persisted session (disclosed in verdict)",
    privacy="synthetic fixtures only; no SAV/DTA, credentials, or source/actor grant",
)
(RET / "environment_passport_delta.json").write_text(json.dumps(passport, indent=1, sort_keys=True) + "\n")

artifacts = {}
for p in sorted(RET.rglob("*")):
    if not p.is_file():
        continue
    rel = str(p.relative_to(RET))
    if rel == "artifact_sha256.json" or "__pycache__" in rel or rel.endswith(".pyc"):
        continue
    artifacts[rel] = sha(p)
(RET / "artifact_sha256.json").write_text(json.dumps(artifacts, indent=1, sort_keys=True) + "\n")
print("artifacts", len(artifacts), "| courts", passport["courts"])
