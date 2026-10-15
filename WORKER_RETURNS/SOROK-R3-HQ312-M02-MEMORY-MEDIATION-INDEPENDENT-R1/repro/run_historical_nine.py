"""Execute only the nine literal historical REDs, not all CAN3 585."""

from review_bootstrap import *
import sys, os, json, subprocess, xml.etree.ElementTree as ET

out = R / "evidence/historical_nine"
out.mkdir(exist_ok=True)
C = R / "runtime/m01/runtime/can3/runtime/author/runtime_root/court_repaired"
CAN = bootstrap.CAN
sys.path.insert(0, str(C / "repro"))
paths = []
names = []
for suite, path in [
    ("candidate", CAN / "candidate/test_hq300_court.py"),
    ("rcp3", C / "repro/test_independent.py"),
]:
    root = ET.parse(
        R / "runtime/m01/runtime/can3/evidence" / suite / "junit.xml"
    ).getroot()
    for case in root.iter("testcase"):
        if case.find("failure") is not None:
            names.append({"suite": suite, "name": case.attrib["name"]})
            paths.append(str(path) + "::" + case.attrib["name"])
assert len(paths) == 9
from rawlsing_next import v3_psepf_zero_positive_guard as G

before = Path(G.__file__).read_bytes()
assert not G.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
import pytest

args = [
    "-vv",
    "--tb=short",
    "--rootdir=" + str(R),
    "--confcutdir=" + str(R),
    "-p",
    "no:cacheprovider",
    *paths,
    "--junitxml=" + str(out / "junit.xml"),
]
code = pytest.main(args)
assert (
    Path(G.__file__).read_bytes() == before
    and not G.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
)
(out / "execution.json").write_text(
    json.dumps(
        {
            "exact_original_cases": names,
            "exit": int(code),
            "pytest_args": [s.replace(str(R), "<RETURN>") for s in args],
            "original_test_bytes_changed": False,
            "full_CAN3_585_rerun": False,
            "guard_empty_and_unchanged": True,
        },
        indent=2,
    )
    + "\n"
)
raise SystemExit(code)
