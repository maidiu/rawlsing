#!/usr/bin/env python3
"""Apply/restore the narrow SOROK launch-attestation hook."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original"
PATCHED = HERE / "patched"
TARGET = Path("/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127")
FILES = ("launch.py", "completion_events.py")
EXPECTED_ORIGINAL = {
    "launch.py": "4c5004ef91ee56ac056aca2921d4239cbf95d866ff015e7eae7d4deaf10ae829",
    "completion_events.py": "503f7b410343b1227cae9bf7cbbe130807e20a444915c12881030cdf19e02da2",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def receipt(state):
    return {
        "schema": "SOROK_CONTROLLER_HOOK_INSTALL_R1",
        "state": state,
        "target": str(TARGET),
        "files": {name: {"original_sha256": EXPECTED_ORIGINAL[name],
                         "installed_sha256": sha(TARGET / name),
                         "patched_sha256": sha(PATCHED / name)}
                  for name in FILES},
        "scope": "SOROK_ONLY_OPTIONAL_BINDING_FIELD_SOROK_CURRENTNESS",
        "pyat_behavior_changed": False,
    }


def apply():
    for name in FILES:
        if sha(TARGET / name) != EXPECTED_ORIGINAL[name]:
            raise SystemExit("REFUSE_APPLY_UNEXPECTED_INSTALLED_HASH " + name)
    for name in FILES:
        shutil.copy2(TARGET / name, HERE / "backup_at_apply" / name)
        shutil.copy2(PATCHED / name, TARGET / name)
    data = receipt("APPLIED")
    (HERE / "INSTALL_RECEIPT.json").write_text(json.dumps(data, indent=2) + "\n")
    return data


def restore():
    for name in FILES:
        shutil.copy2(HERE / "backup_at_apply" / name, TARGET / name)
    data = receipt("RESTORED")
    (HERE / "RESTORE_RECEIPT.json").write_text(json.dumps(data, indent=2) + "\n")
    return data


def verify():
    return receipt("VERIFIED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("apply", "restore", "verify"))
    args = parser.parse_args()
    result = {"apply": apply, "restore": restore, "verify": verify}[args.action]()
    print(json.dumps(result, indent=2))
