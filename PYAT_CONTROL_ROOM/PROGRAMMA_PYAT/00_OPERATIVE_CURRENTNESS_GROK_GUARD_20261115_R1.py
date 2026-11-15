#!/usr/bin/env python3
"""Read-only PYAT cold-grok self-check.

This does not establish live GitHub issue/review status or authority to merge.
Default checks the frozen snapshot's protected + integration source branch
against the remote; if they move, FAIL CLOSED and refresh the currentness.
No survey bytes, source rights, service credentials or model provider used.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PYAT = ROOT / "PYAT_CONTROL_ROOM" / "PROGRAMMA_PYAT"
STEM = "00_OPERATIVE_MISSION_AND_CURRENTNESS_20261115_R1"
DOC = PYAT / f"{STEM}.md"
MANIFEST = PYAT / f"{STEM}.json"
FRONT = PYAT / "00_PROGRAMMA_PYAT.md"
ROADMAP = PYAT / "05_ROADMAP" / "README.md"
PRODUCT = PYAT / "05_ROADMAP" / "REMAINING_REAL_PYAT_WORK.md"
MANDATORY_NODES = {
    "PYAT_PRIORITY", "S1E_R6", "S2A", "PHYSICAL_BASELINE", "LOCALITY_R2",
    "J5_100_DISTINCT", "STAGED_COMBINED", "DUAL_PREP", "SOURCE_RIGHTS",
    "FIELD_FORGE", "PERSON_PILOT", "BACKWARD_SEAM", "SEAM_SUMMIT",
    "VOSKRES", "VMESTYE", "W05_PHYSICAL_CODE_CANDIDATE",
    "R03_GOVERNED_ISSUER_V2_CANDIDATE", "PREFF_COMPOSED_AUTHOR_TREE",
}
MANDATORY_TOKENS = [
    "Nov 13", "S04", "FF01", "N10E", "N10W", "FIABC", "backward",
    "mother", "father", "child", "R03", "100k", "not protected",
]

def fail(message: str) -> None:
    raise SystemExit("CURRENTNESS_GROK_HOLD: " + message)

def live_branch_sha(name: str) -> str:
    proc = subprocess.run(
        ["git", "ls-remote", "--exit-code", "--heads", "origin", name],
        cwd=ROOT, text=True, capture_output=True, timeout=45, check=False
    )
    if proc.returncode != 0:
        fail(f"cannot verify live origin/{name}: {proc.stderr.strip()}")
    matches = [x.split()[0] for x in proc.stdout.splitlines()
               if x.endswith("refs/heads/" + name)]
    if len(matches) != 1:
        fail(f"cannot uniquely resolve live origin/{name}")
    return matches[0]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="only check documentary consistency; ALWAYS reports OFFLINE_NOT_CURRENT")
    args = ap.parse_args()
    for path in (DOC, MANIFEST, FRONT, ROADMAP, PRODUCT):
        if not path.is_file():
            fail(f"missing required currentness frontdoor: {path.relative_to(ROOT)}")
    state = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if state.get("schema") != "PYAT_OPERATIVE_CURRENTNESS@1":
        fail("unexpected currentness schema")
    if state.get("protected", {}).get("progress_revision") != 8:
        fail("revision changed; rebuild snapshot + paired protected progress")
    if state["protected"]["latest_protected_is_latest_operation"] is not False:
        fail("mistakes latest protected for latest operational programme")
    if state["protected"]["doc_only_cas_grant"] != "NOT_OBTAINED":
        fail("claims unsupported protected CAS authority")
    ids = [x["id"] for x in state["items"]]
    if len(ids) != len(set(ids)) or not MANDATORY_NODES <= set(ids):
        fail("duplicate/missing required dispositions")
    for item in state["items"]:
        for key in ("id", "ref", "grade", "integration", "owner", "need"):
            if not item.get(key):
                fail(f"{item.get('id','?')} lacks {key}")
    ordered = state["execution_sequence"]
    if ordered != [
        "GENERIC_13F_SRC_TO_PERSIST_C11_997_1006", "JOINED_S01_S05_998",
        "TWO_SERIES_GENERIC_1007", "GENERIC_FF01_N10E_1009",
        "FIRST_CONTINUING_PERSON_1011"
    ]:
        fail("source-first P0 order silently changed")
    paths = state["stage_dag"]["direct_s04_consumers"]
    if set(paths) != {"S05_LEARNED_FIABC_M1_M2_B5", "FF01_DESCRIPTIVE", "N10E_EMPIRICAL_POSSIBILITY"}:
        fail("S04's three direct first consumers lost")
    if state["stage_dag"]["n10w"] != "N9_AND_N10E_COMPATIBLE_JOIN_WHEN_SELECTED":
        fail("N10W claim lost N9 and N10E required conjunction")
    if state["stage_dag"]["seam_grade"] != "RESEARCH_PROPOSAL_NOT_NATIVE_EXECUTION":
        fail("scientific SEAM proposal promoted to production")
    items = {x["id"]: x for x in state["items"]}
    if items["STAGED_COMBINED"]["integration"] != "UNMERGED_JOINED_G5_NOT_RUN":
        fail("sourcefree #1073 unverified joined G5 falsely advanced")
    if items["LOCALITY_R2"]["integration"] != "NOT_IMPLEMENTED_IN_PRODUCTION":
        fail("#1006 candidate locality promoted without actual native reader proof")
    if items["S1E_R6"]["grade"] != "ACCEPT_SCOPED_REAL_0_QUERY_1_DISCOVERY":
        fail("original 0 QUERY / 1 DISCOVERY scope missing")
    if items["J5_100_DISTINCT"]["integration"] != "PR_TARGETS_MAIN_TOO_LARGE_NOT_PRODUCT":
        fail("J5 documentary candidate presented as product adoption")
    w05 = items["W05_PHYSICAL_CODE_CANDIDATE"]
    r03 = items["R03_GOVERNED_ISSUER_V2_CANDIDATE"]
    comp = items["PREFF_COMPOSED_AUTHOR_TREE"]
    if (w05["grade"] != "AUTHOR_CODE_CANDIDATE_NOT_TESTED_NOT_INDEPENDENT_G5"
            or r03["grade"] != "AUTHOR_TEST_ONLY_GOVERNED_QUERY_CODE_NOT_TESTED"
            or comp["grade"] != "COMPOSITE_AUTHOR_ONLY_NEITHER_CODE_PATCH_TESTED"
            or r03["code"] != comp["code"]):
        fail("new R03/W05 unreceived code promoted or composite split")
    doc = DOC.read_text(encoding="utf-8").lower()
    for token in MANDATORY_TOKENS:
        if token.lower() not in doc:
            fail("read-first mission omitted "+token)
    for path in (FRONT, ROADMAP, PRODUCT):
        body=path.read_text(encoding="utf-8")
        if STEM+".md" not in body or not body.index(STEM+".md") < 4000:
            fail(f"required first-screen navigation absent: {path.relative_to(ROOT)}")
    if args.offline:
        print("PASS_STATIC_DOC_CONSISTENCY; OFFLINE_NOT_CURRENT; LIVE_REVIEW_ISSUE_STATUS_UNVERIFIED")
        return 0
    baseline = state["protected"]["head_at_read"]
    actual = live_branch_sha(state["protected"]["branch"])
    if actual != baseline:
        fail(f"protected HEAD advanced from {baseline} to {actual}; RENEW CURRENTNESS")
    source = items["STAGED_COMBINED"]
    integration = live_branch_sha("integration/pyat998-r6-s2a-joined-staging-20261115-r1")
    if integration != source["code"]:
        fail(f"#1073 branch moved from {source['code']} to {integration}; RENEW EVIDENCE")
    for name, item in (
        ("implementation/pyat1006-verified-native-physical-traversal-20261115-r1", w05),
        ("implementation/pyat997-r03-governed-query-issuer-v2-20261115-r1", r03),
    ):
        current = live_branch_sha(name)
        if current != item["code"]:
            fail(f"new pre-Forge branch {name} moved from {item['code']} to {current}; RENEW EVIDENCE")
    print("PASS_PINNED_BRANCH_HEADS_AND_STATIC_DOC; G5/RIGHTS/ISSUE_COMMENTS_STILL_REQUIRE_LIVE_RECHECK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        fail(repr(exc))
