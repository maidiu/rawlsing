#!/usr/bin/env python3
"""Apply/restore the narrow SOROK-only hook on the existing installed controller.

No behavior changes for bindings without a `sorok_currentness` object.
"""
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
    "launch.py": "7712bbe36735bd572db4fe785290a1b4ba9c9a7fd42f441a6bd3e6b6a2bc15a1",
    "completion_events.py": "a96293e3a6a77a20910e05752c34e8e912d2eab3e6fbaf95c2229a7910546a63",
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
    backup = HERE / "backup_at_apply"
    backup.mkdir(exist_ok=True)
    for name in FILES:
        shutil.copy2(TARGET / name, backup / name)
    for name in FILES:
        shutil.copy2(PATCHED / name, TARGET / name)
    data = receipt("APPLIED")
    (HERE / "INSTALL_RECEIPT.json").write_text(json.dumps(data, indent=2) + "\n")
    return data


def restore():
    backup = HERE / "backup_at_apply"
    for name in FILES:
        shutil.copy2(backup / name, TARGET / name)
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
