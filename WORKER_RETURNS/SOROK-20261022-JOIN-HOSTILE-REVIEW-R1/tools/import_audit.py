import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
DEFAULT_CANDIDATE = REPO / "WORKER_RETURNS" / "SOROK-20261022-SAME-PERSON-JOIN-R1"
CANDIDATE = Path(
    os.environ.get("SOROK_JOIN_CANDIDATE_ROOT", str(DEFAULT_CANDIDATE))
).resolve()
EVIDENCE = RETURN / "evidence"

PROBE = """
import hashlib, json, sys
sys.path.insert(0, sys.argv[1])
if sys.argv[2] == "e_first":
    sys.path.insert(0, sys.argv[1] + "/vendor/e")
    from r31e.session import R31ESession
from joined.session import JoinedSession
names = ["bp4", "bp4.world", "bp2p4", "bp2p4.product", "r29p", "r29p.product",
         "r26e", "r26e.c12_integrity", "r30a", "r30a.first_session",
         "r31j", "r31j.build", "r31j.product", "r31e", "r31e.session",
         "joined.session"]
rows = {}
for name in names:
    mod = sys.modules.get(name)
    path = getattr(mod, "__file__", None)
    if not path:
        rows[name] = None
        continue
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()
    rows[name] = {"path": path, "sha256": digest}
print(json.dumps(rows, sort_keys=True))
"""


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = {}
    for mode in ("normal", "e_first"):
        run = subprocess.run(
            [sys.executable, "-B", "-c", PROBE, str(CANDIDATE), mode],
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
        )
        if run.returncode != 0:
            result[mode] = {
                "returncode": run.returncode,
                "stderr": run.stderr,
            }
            continue
        result[mode] = {
            "returncode": 0,
            "modules": json.loads(run.stdout),
        }
    path = EVIDENCE / "import_audit.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        mode: {
            name: (row["path"].split("/vendor/")[-1] if row else None)
            for name, row in value.get("modules", {}).items()
            if name in {"bp4", "bp2p4", "r29p", "r26e", "r30a", "r31j", "r31e"}
        }
        for mode, value in result.items()
    }, indent=2))


if __name__ == "__main__":
    main()
