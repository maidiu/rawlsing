#!/usr/bin/env python3
"""WG0P8 source-free transport verifier. Not an original-source or issuer grant.

Use inside the complete *private* maidiu/rawlsing Git checkout.  All input
hashes, the P5 import and the frozen tests are checked before any I03 request.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "candidate"
COURT = C / "court"
REVIEW = ROOT / "reviewer_frozen" / "02_WG0P7_STAGED" / "reviewer"
REPAIRED = "court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py"
DIRECT = "court/runtime_phase_b/candidate/repro/wg0p4_workload.py"
EXPECTED_P5 = "89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643"
EXPECTED_BLOB = "62895078908ff748771da9a9fbcec6b36d34a803"
# D1: the repaired nested P5 module declares this version, not the stale
# WG0P4_NATIVE_FRONTIER_COLD@1 that the shipped probe_import wrongly expected.
EXPECTED_P5_VERSION = "WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1"
EXPECTED_MODULE_SOURCE = (
    "WORKER_RETURNS/PYAT-R29-WG0P7-AUTHORITY-BODY-ADAPTER-REPAIR-R1/"
    "candidate/" + REPAIRED
)


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def refuse(message: str) -> None:
    raise RuntimeError("WG0P8_PRE_I03_REFUSE:" + message)


def require_exact(path: Path, expected_sha256: str, expected_blob: str) -> dict:
    if path.is_symlink() or not path.is_file():
        refuse("MISSING_OR_SYMLINK:" + str(path))
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    blob = git_blob(raw)
    if sha != expected_sha256 or blob != expected_blob:
        refuse("INPUT_HASH_OR_BLOB_CHANGED:" + str(path))
    return dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=sha, git_blob_sha1=blob)


def verify() -> dict:
    source_path = C / "SOURCE_INPUTS.json"
    if not source_path.is_file() or source_path.is_symlink():
        refuse("SOURCE_INPUTS_MISSING_OR_SYMLINK")
    source = json.loads(source_path.read_text())
    rows = source["files"]
    if len(rows) != 187 or len({r["staged_path"] for r in rows}) != 187:
        refuse("SOURCE_INPUT_COUNT_OR_DUPLICATION")
    body_rows = [r for r in rows if r["staged_path"] == REPAIRED]
    if len(body_rows) != 1:
        refuse("P5_MODULE_ALIAS_ABSENT_OR_AMBIGUOUS")
    body = body_rows[0]
    if (body["sha256"], body["git_blob_sha1"], body["source_path"]) != (
        EXPECTED_P5, EXPECTED_BLOB, EXPECTED_MODULE_SOURCE
    ):
        refuse("STALE_SOURCE_INPUTS_OR_WRONG_MODULE")
    if "06fadc7eb8c01fa832fa59beccfc2ea2f6e068216fdc8b04c95365065d492723" in source_path.read_text():
        refuse("STALE_SOURCE_INPUT_HASH_ALIAS")
    if (C / DIRECT).resolve() == (C / REPAIRED).resolve():
        refuse("DIRECT_AND_REPAIRED_MODULE_COLLAPSED")
    checked = []
    for row in rows:
        p = C / row["staged_path"]
        if not p.resolve().is_relative_to(C.resolve()):
            refuse("SOURCE_PATH_ESCAPE")
        hit = require_exact(p, row["sha256"], row["git_blob_sha1"])
        if hit["bytes"] != row["bytes"]:
            refuse("SOURCE_BYTE_LENGTH_CHANGED:" + row["staged_path"])
        checked.append(hit)
    pin = json.loads((C / "CANDIDATE_CODE_PIN.json").read_text())
    for row in pin["files"]:
        require_exact(C / row["staged_path"], row["sha256"], row["git_blob_sha1"])
    if pin["files"][0]["git_blob_sha1"] != EXPECTED_BLOB:
        refuse("CANDIDATE_CODE_PIN_WRONG_P5")
    for file in C.rglob("*"):
        if file.is_symlink():
            refuse("ABSOLUTE_OR_RELATIVE_SYMLINK:" + str(file))
    root_checkout = next((p for p in (ROOT, *ROOT.parents) if (p / ".git").exists()), None)
    if root_checkout is None:
        refuse("CLEAN_GIT_CHECKOUT_NOT_PROVEN")
    tracked = subprocess.run(
        ["git", "-C", str(root_checkout), "ls-files", "--error-unmatch", "--", str((C / REPAIRED).relative_to(root_checkout))],
        capture_output=True, text=True,
    )
    if tracked.returncode:
        refuse("REPAIRED_MODULE_NOT_VERSIONED_IN_GIT")
    return {"input_count":len(checked), "missing":0,"mismatched":0,"source_manifest_sha256":hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "module_sha256":EXPECTED_P5,"module_git_blob":EXPECTED_BLOB,"git_checkout_root":str(root_checkout),"validation":"PASS_SOURCEFREE_FILE_CUSTODY"}


def probe_import() -> dict:
    verify()
    bootstrap = COURT / "bootstrap_p6"
    p5_path = (C / REPAIRED).resolve()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
               PYTHONPATH=os.pathsep.join([str(bootstrap), str(COURT / "repro")]))
    # P6's original pinned sitecustomize fails closed with os._exit(86).
    code = "import wg0p4_workload as m,hashlib,json,pathlib; p=pathlib.Path(m.__file__).resolve(); print(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'version':m.VERSION}))"
    proc = subprocess.run([sys.executable,"-B","-c",code],cwd=COURT,env=env,text=True,capture_output=True)
    if proc.returncode:
        refuse("PINNED_BOOTSTRAP_IMPORT_FAILED:" + proc.stderr[-1500:])
    result = json.loads(proc.stdout.strip().splitlines()[-1])
    if (Path(result["path"]).resolve(), result["sha256"], result["version"]) != (
        p5_path, EXPECTED_P5, EXPECTED_P5_VERSION
    ):
        refuse("WRONG_DIRECT_OR_UNREPAIRED_RUNTIME_MODULE")
    return result


SUITES = {
    "wg0o17": [REVIEW / "tests/test_authority_seam_court.py"],
    "wg0q36": [REVIEW / "tests/test_authority_body_delta_court.py"],
    "wg0m33": [COURT / "tests/test_descriptor_delta_frozen.py"],
    "original65": [COURT / "tests/test_precommitted_phase_b.py"],
    "original3": [COURT / "tests/p5_mapping/test_original_three_adapter_v1.py"],
    "j44_k11": [COURT / "tests/phase_b/test_original_j_adapter_v1.py", COURT / "tests/phase_b/test_original_k_adapter_v1.py"],
    "owners80": [COURT / "runtime_phase_b/owner_tests"],
    "fresh42": [C / "tests/test_source_view_binding.py"],
}


def run_suites(names: list[str]) -> list[dict]:
    verify()
    imported = probe_import()
    logdir = ROOT / "04_JUNIT_LOGS"
    logdir.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
               PYTHONPATH=os.pathsep.join([str(COURT / "bootstrap_p6"), str(COURT / "repro")]),
               WG0O_WG0N_ROOT=str(ROOT / "reviewer_frozen" / "03_INHERITED" / "WG0N"),
               # D6 (WG0P10-discovered, not in the commissioned D1-D5 set):
               # test_precommitted_phase_b.py requires the versioned adapter name
               # via WG0L_PHASE_B_ADAPTER and refuses collection without it
               # (PHASE_B_NOT_AUTHORIZED_WITHOUT_PUBLISHED_CANDIDATE_READ_CUT_AND_
               # VERSIONED_ADAPTER). The candidate's own documented invocation in
               # court/02_ACTUAL_EXECUTION_OR_TYPED_HOLD.json supplies both; the
               # runner previously omitted them, so `run` could never reach
               # mandatory236 in a clean checkout.
               WG0L_PHASE_B_ADAPTER="phase_b_adapter_v1",
               WG0M_RUN="phase_b_P5")
    results = []
    for name in names:
        if name not in SUITES:
            refuse("UNKNOWN_SUITE:"+name)
        cmd=[sys.executable,"-B","-m","pytest","-c",str(COURT / "runtime_phase_b/candidate/pytest.ini"),"-vv","--tb=short",
             "--junitxml="+str(logdir / (name+".xml")), *map(str,SUITES[name])]
        proc=subprocess.run(cmd,cwd=COURT,env=env,capture_output=True,text=True)
        (logdir / (name+".stdout.log")).write_text(proc.stdout)
        (logdir / (name+".stderr.log")).write_text(proc.stderr)
        xml=logdir / (name+".xml")
        counts={"tests":None,"failures":None,"errors":None,"skips":None}
        if xml.is_file():
            tree=ET.parse(xml)
            counts={"tests":len(tree.findall('.//testcase')),"failures":len(tree.findall('.//failure')),
                    "errors":len(tree.findall('.//error')),"skips":len(tree.findall('.//skipped'))}
        results.append(dict(name=name,command=cmd,exit_code=proc.returncode,counts=counts,actual_module=imported,junit=xml.name if xml.exists() else None))
    (logdir / "run_receipt.json").write_text(json.dumps(results,indent=2)+"\n")
    return results


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("command", choices=["verify","probe-import","run"])
    parser.add_argument("suite",nargs="*")
    args=parser.parse_args()
    try:
        result=verify() if args.command=="verify" else probe_import() if args.command=="probe-import" else run_suites(args.suite or list(SUITES))
    except Exception as exc:
        print(str(exc),file=sys.stderr)
        raise SystemExit(86)
    print(json.dumps(result,indent=2))
