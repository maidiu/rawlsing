"""WG0P7 — environment passport delta and artifact SHA256 manifest."""
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
from datetime import datetime, timezone

RET = pathlib.Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def counts(p):
    import xml.etree.ElementTree as ET
    root = ET.parse(p).getroot()
    s = [x for x in root.iter("testsuite")][0] if root.tag != "testsuite" else root
    return {k: int(s.get(k)) for k in ("tests", "failures", "errors", "skipped")}


courts = {}
for f in sorted((RET / "observations" / "junit").glob("*.xml")):
    courts[f.stem] = counts(f)

passport = dict(
    schema="WG0P7_SANITIZED_ENVIRONMENT_PASSPORT_DELTA@1",
    environment_id="WG0P7_LOCAL_AUTHOR",
    epoch_id="WG0P7_R29",
    surface="S2_LOCAL_HOST",
    status="LIVE_VERIFIED",
    observed_at_utc=datetime.now(timezone.utc).isoformat(),
    interpreter=platform.python_version(),
    pytest=subprocess.check_output([sys.executable, "-m", "pytest", "--version"], text=True).strip(),
    branch="agent/rabochii-pyat-r29-wg0p7-immutable-authority-body-binding-r1",
    sealed_startup="a72e75a011468a1f0ea7b251f5b07969f59488e0",
    parent_implementation="WG0P6 e7e429c3dfb649233e74e0e5106e51ff25024806",
    independent_court_answered="WG0O 3ee5d6a4e246fca89740d4d36ab26206230c83bf",
    repaired_module_sha256="89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643",
    pristine_module_sha256="3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e",
    courts=courts,
    model=dict(observed="DeepSeek Harness", actual_model="deepseek-flash",
               actual_reasoning_effort="NOT_EXPOSED"),
    privacy="synthetic TEST_ONLY fixtures only; no SAV/DTA, credentials, source or issuer grant",
)
(RET / "environment_passport_delta.json").write_text(json.dumps(passport, indent=1, sort_keys=True) + "\n")

artifacts = {}
for p in sorted(RET.rglob("*")):
    if not p.is_file():
        continue
    rel = str(p.relative_to(RET))
    if rel in ("artifact_sha256.json",) or "__pycache__" in rel or rel.endswith(".pyc"):
        continue
    if rel.startswith(("candidate/observations/", "candidate/runtime/", "candidate/court/runtime/")):
        continue
    artifacts[rel] = sha(p)
(RET / "artifact_sha256.json").write_text(json.dumps(artifacts, indent=1, sort_keys=True) + "\n")
print("artifacts", len(artifacts), "courts", courts)
