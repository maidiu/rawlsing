#!/usr/bin/env python3
"""Materialize exact historical courts and the 29-module runtime from Git."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
HIST = RETURN / "historical"
WR = HIST / "WORKER_RETURNS"
CAND = RETURN / "candidate"
RUNTIME = CAND / "stage" / "runtime"


def archive(commit: str, path: str):
    subprocess.run(["bash", "-lc",
                    f"git -C '{REPO}' archive {commit} '{path}' | tar -x -C '{HIST}'"],
                   check=True)


def stage_runtime():
    if not (RUNTIME / "product/nonparent.py").is_file():
        subprocess.run([sys.executable, "-B", str(CAND / "tools/c0p_stage_runtime.py")],
                       cwd=CAND, check=True,
                       env={**__import__("os").environ,
                            "C0P_REPO": str(REPO),
                            "C0P_RUNTIME": str(RUNTIME)})
    ledger = CAND / "stage/_c0p_runtime_ledger.json"
    data = json.loads(ledger.read_text())
    assert len(data["ledger"]) == 29 and all(row["all_match"] for row in data["ledger"])


def copy_runtime(dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(RUNTIME, dest)


def main() -> int:
    HIST.mkdir(exist_ok=True)
    stage_runtime()
    # Exact original returns.
    for commit, path in (
        ("55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f",
         "WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1"),
        ("2dacd87636352a6c805e03b3d07581193a06264b",
         "WORKER_RETURNS/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"),
        ("55d2daa4bab41c5ff4ffdc196c8d36d300c3d60f",
         "WORKER_RETURNS/SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"),
        ("b02deee1bac9393921845caa657841c40408eaf6",
         "WORKER_RETURNS/SOROK-20261019-C0X-C0-C10-DUAL-OWNER-RECEIVER-COMPLETION-R1"),
        ("9831293f9fd53813db04d33be5bbdc177542f8ce",
         "WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-SC0F3-REAL-OWNER-REPAIR-R1/repro/inputs/port"),
    ):
        if not (HIST / path.split("/", 1)[1]).exists():
            archive(commit, path)

    c0i = WR / "SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"
    variants = {
        "c0i_original": RETURN / "original/c0p_first_author.py",
        "c0i_repaired": RETURN / "original/c0p_repaired_author.py",
        "c0i_corrected": CAND / "upstream/c0p_two_contract_port.py",
    }
    for name, facade in variants.items():
        root = HIST / name / "SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1"
        if root.exists():
            shutil.rmtree(HIST / name)
        root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(c0i, root)
        (root / "staging/c0p/repro").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(facade, root / "staging/c0p/repro/c0p_two_contract_port.py")
        copy_runtime(root / "staging/runtime")
        oracles = WR / "SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/frozen_oracles/sc0"
        shutil.copytree(oracles, root / "staging/oracles/sc0", dirs_exist_ok=True)

    c0r2 = WR / "SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"
    for name, facade in (("c0r2_repaired", RETURN / "original/c0p_repaired_author.py"),
                         ("c0r2_corrected", CAND / "upstream/c0p_two_contract_port.py")):
        root = HIST / name / "SOROK-V2-HQ323-C0R2-GIT-BACKED-REPAIR-R1"
        if root.exists():
            shutil.rmtree(HIST / name)
        root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(c0r2, root)
        copy_runtime(root / "staging/runtime")
        sibling = (HIST / name / "SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1/repro")
        sibling.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(facade, sibling / "c0p_two_contract_port.py")

    c0x = WR / "SOROK-20261019-C0X-C0-C10-DUAL-OWNER-RECEIVER-COMPLETION-R1"
    copy_runtime(c0x / "stage/runtime")
    shutil.copyfile(CAND / "stage/_c0p_runtime_ledger.json",
                    c0x / "stage/_c0p_runtime_ledger.json")
    print(json.dumps(dict(runtime_modules=29, historical=str(HIST.relative_to(RETURN)))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
