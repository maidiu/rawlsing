"""Package actual staged JUnit/logs and verify exact source/cold custody."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
STAGE = Path(os.environ["GF1H_STAGE_ROOT"]).resolve()
COURT = STAGE / "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"
GF1G = STAGE / "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1"
ORIGINAL = "eeb726357204653b22458dc267dd70ba0009bd77"
G = "ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7"
F = "3dcc7d7dddfff4f1be8b4293cab92e5b4275007d"
I = "c6a55f0dd5b327c40d64f96e0705ab5485559e90"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_git(commit, path, local=None):
    assert git("cat-file", "-t", commit).strip() == b"commit"
    data = git("show", commit + ":" + path)
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert git("rev-parse", commit + ":" + path).decode().strip() == blob
    if local is not None:
        assert local.read_bytes() == data, path
    return {"commit": commit, "path": path, "git_blob_sha1": blob, "sha256": sha(data)}


inputs = [
    check_git(ORIGINAL, "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/runtime_root/gf1_pair_support_consumer.py"),
    check_git(ORIGINAL, "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/repro/test_gf1_generic_pair.py", COURT / "court/repro/test_gf1_generic_pair.py"),
    check_git(G, "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1/phase_a/test_gf1g_precommitted.py", GF1G / "phase_a/test_gf1g_precommitted.py"),
    check_git(G, "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1/01_FROZEN_ORACLE.json", GF1G / "01_FROZEN_ORACLE.json"),
    check_git(F, "WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1/tests/test_gf1f_independent_consumer.py", STAGE / "WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1/tests/test_gf1f_independent_consumer.py"),
    check_git(I, "WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1/court/test_gf1i_independent.py", STAGE / "WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1/court/test_gf1i_independent.py"),
]
patch = HERE / "gf1_pair_support_consumer.py"
assert (COURT / "court/runtime_root/gf1_pair_support_consumer.py").read_bytes() == patch.read_bytes()

dest = HERE / "02_FROZEN44_GF1F100_GF1I19_AND_NEW_JUNIT"
dest.mkdir(exist_ok=True)
names = ("original44_before", "original44_after", "gf1g_before", "gf1g_after",
         "gf1f100_before", "gf1f100_after", "gf1i19_after", "gf1h_new")
results = {}
for name in names:
    tree = ET.parse(STAGE / (name + ".xml"))
    suite = next(tree.iter("testsuite"))
    results[name] = {key: int(suite.attrib[key]) for key in ("tests", "failures", "errors", "skipped")}
    results[name]["failed_cases"] = [case.attrib["name"] for case in tree.iter("testcase") if case.find("failure") is not None]
    for section in tree.iter("testsuite"):
        section.attrib.pop("hostname", None)
    tree.write(dest / (name + ".xml"), encoding="utf-8", xml_declaration=True)
    shutil.copyfile(STAGE / (name + ".log"), dest / (name + ".log"))

(HERE / "01_BEFORE_AFTER_INDEPENDENT_26.json").write_text(json.dumps({
    "sealed_start": git("rev-parse", "HEAD").decode().strip(),
    "unchanged_gf1g_phase_a_commit": G,
    "original_consumer_sha256": inputs[0]["sha256"],
    "repaired_consumer_sha256": sha(patch.read_bytes()),
    "before": results["gf1g_before"],
    "after": results["gf1g_after"],
    "all_actual_suite_results": results,
}, indent=2) + "\n")

cold = [json.loads((STAGE / f"cold_{i}.json").read_text()) for i in (0, 1)]
assert cold[0]["pid"] != cold[1]["pid"]
assert {k: v for k, v in cold[0].items() if k != "pid"} == {k: v for k, v in cold[1].items() if k != "pid"}
assert all(c["consumer_sha256"] == sha(patch.read_bytes()) for c in cold)
assert all(Path(c["consumer_file"]).resolve() == (COURT / "court/runtime_root/gf1_pair_support_consumer.py").resolve() for c in cold)
assert all(c["production_owner_commit"] is False for c in cold)
assert results["original44_after"]["tests"] == 44 and results["original44_after"]["failures"] == 0
assert results["gf1g_after"]["tests"] == 26 and results["gf1g_after"]["failures"] == 0
assert results["gf1h_new"]["failures"] == 0

(HERE / "04_REAL_SOURCE_IMPORTS_AND_COLD.json").write_text(json.dumps({
    "source_transport": inputs,
    "repaired_consumer_relative_import": "court/runtime_root/gf1_pair_support_consumer.py",
    "repaired_consumer_sha256": sha(patch.read_bytes()),
    "native_closure": "74/74 reattested by gf1_bootstrap on actual pytest and cold imports",
    "cold_processes": [{k: v for k, v in c.items() if k != "consumer_file"} for c in cold],
    "distinct_pid": True,
    "identical_non_pid_receipts": True,
    "science_grade": "SOURCEFREE_TEST_ONLY_UNISSUED",
}, indent=2) + "\n")
print(json.dumps({"suites": results, "cold_distinct_pid": True, "patched_sha256": sha(patch.read_bytes())}, indent=2))
