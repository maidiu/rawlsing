#!/usr/bin/env python3
"""SOROK scoped operational-currentness checker; NOT a live event-intake agent.

This validator deliberately freezes a November 15, 2026 candidate evidence cut.
Changing an accepted fact requires an independently grounded new evidence revision,
not editing the status field until it looks green.
"""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json"
MARKDOWN = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md"
SOURCE = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1"
START = "<!-- SOROK_OPERATIONAL_CURRENT_START -->"
END = "<!-- SOROK_OPERATIONAL_CURRENT_END -->"

ORIGINAL_REF = "227ce149fc7864c83c179a7d3ecaef2b92c5bdab"
GMT_REF = "b066ef84750b99339faf197c8e34a7300f768a8e"
FROZEN_SOURCES = {
    "packet": ("original_task_packets_20261112.json", "17cfae53f9ca16640d5d3d500aa7dcb3b31cc89c"),
    "gmt": ("original_gmt_overlay_20261112.json", "474befcb4d9f6e3842b4d256d00d9c0ac0bf1a4d"),
}
EXPECTED = {f"{family}{n:02d}" for family, count in (
    ("B", 5), ("C", 5), ("D", 5), ("E", 4), ("F", 4), ("G", 4))
    for n in range(1, count + 1)}
EXPECTED_COUNTS = {"G": 6, "M": 12, "T": 9}

# Verified merged PR identities, actual merge commits, and PR heads (second parents).
# All three fields are checked, not just an arbitrary ancestor-of-HEAD SHA.
PROTECTED_PINS = {
    "P3": (746, "034bf8b6927bcd9c7c0b88b36368c1282a8f1f14", "fe51de7979108df3e922e69ea3fd1d5159c5e293"),
    "P4": (751, "ae3dd0922c5bf00a50071ed34f75798838ad4e95", "80bce19efeaeb98b1452e8b5995ebf80f83e166f"),
    "P5": (775, "5e266a80ccfc52da10741e15f6b9076138907758", "0d566510afd17ea395112fdb1a9f5713f88af835"),
    "P6": (779, "0232a28f519f56b45404c439f1cd2a007005d2f4", "ea72ce582e7e3d3b27f6e04bd560dae14b228f75"),
    "MI": (907, "1f77f2036427a410429184780ef884ec4f253ad0", "cb998b7d7752d8db972bce18471230d07f056939"),
    "MII": (905, "521ae459091c5d4e4009f442257d74d50b2c55db", "2be0cf252662ad021571db6f0d38b12c205c56ae"),
    "MIII": (891, "3e5b1611f5cb043b43ffd39b14c9d707923f1210", "724b505c2ab07eaa350a4582e317d1d71faa1d27"),
}
# Accepted R3 scoped provenance; these code SHAs were checked to be ancestors of
# their corresponding nonauthor G5 PR heads. No such branch is claimed protected.
SCOPED_PINS = {
    "B05": (1089, "cab1f2d6cdab6f6b653ed20e5b41afb90d9facbc", "5c83a8321dce70fcc40c8f210af06a9edb1f8999"),
    "C04": (1062, "ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9", "8bdfbdd22c19d865b5049bde8213eb3bcaea973b"),
    "C05": (1091, "4b33b8be1127c2186931a66f23e3a2b05feaf0a6", "24f532de43ab6d1ee8a6480a856ba6c6b56e7f53"),
}
HELD_OR_UNLAUNCHED = {
    "D04", "D05", "E02", "E03", "E04", "F01", "F02", "F03",
    "F04", "G01", "G02", "G03", "G04"
}
BROWSER_STATUS = {
    "issue_1008": "A_B_A_COMPLETED_C04_CHILD_CUSTODY_SCOPED",
    "issue_1010": "A_B_A_COMPLETED_G2_HELD",
    "issue_1012": "NOT_LAUNCHED_WAITING_J1",
}
CONTROLLER_STATUS = {
    "issue_939": "USER_STOP_AFTER_ORIGINAL_ASSIGNMENTS",
    "persistent_dispatch": False,
}
OUTSIDE_STATUS = {
    "G03_I0": "RECEIVED_SCOPED_UNMERGED_PR993",
    "CG_A": "RECEIVED_SCOPED_UNMERGED_PR1066",
    "portal_768": "DESIGN_CANDIDATE_NOT_IMPLEMENTED",
}
FRONTIER_STATUS = {
    "PROGRAMMA": "RECONCILIATION_REQUIRED",
    "G2": "HOLD_SOURCE_AUTHORITY",
    "C04/D03": "REPAIR_AND_OWNER_HOLD",
    "C05": "FULL_ACTOR_KNOWLEDGE_HELD",
    "E01/J1": "PARTIAL_DEPENDENCY_HOLD",
    "D04/D05": "WAITING_PERFORMED_J1",
    "E02/J2": "WAITING_E01_B05_C05_D04",
    "CG-A": "SCOPED_RECEIVED_UNMERGED",
    "G03": "I0_RECEIVED_FULL_COHORT_HELD",
}
EXPECTED_RECEIPT = "PR1063_TW0_JOB_RECEIVING_20261115"

def git_object_sha(data):
    """Git blob hash from exact UTF-8 bytes, works without a .git checkout."""
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def original_contracts(errors):
    data = {}
    for key, (filename, sha) in FROZEN_SOURCES.items():
        path = SOURCE / filename
        try:
            raw = path.read_bytes()
            if git_object_sha(raw) != sha:
                errors.append("SOURCE_BLOB_MISMATCH " + filename)
                continue
            data[key] = json.loads(raw)
        except (OSError, ValueError, TypeError) as exc:
            errors.append("SOURCE_NOT_READABLE " + filename + ": " + str(exc))
    if len(data) != 2:
        return {}, {}
    packet_list = data["packet"].get("tasks", [])
    gmt_list = data["gmt"].get("task_overlays", [])
    if not isinstance(packet_list, list) or not isinstance(gmt_list, list):
        errors.append("SOURCE_SCHEMA_MISMATCH expected list task manifests")
        return {}, {}
    edges = {p.get("id"): p.get("depends_on") for p in packet_list if isinstance(p, dict)}
    grades = {p.get("task_id"): p.get("implementation_class") for p in gmt_list if isinstance(p, dict)}
    if len(packet_list) != 27 or set(edges) != EXPECTED:
        errors.append("SOURCE_PACKET_DENOMINATOR not 27 original IDs")
    if len(gmt_list) != 27 or set(grades) != EXPECTED:
        errors.append("SOURCE_GMT_DENOMINATOR not 27 original IDs")
    if {g: list(grades.values()).count(g) for g in EXPECTED_COUNTS} != EXPECTED_COUNTS:
        errors.append("SOURCE_GMT_COUNTS not G6/M12/T9")
    return edges, grades

def run_git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                           text=True, check=False, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return (1, str(exc))
    return r.returncode, r.stdout.strip()

def validate(s, git=True):
    errors = []
    if not isinstance(s, dict):
        return ["STATE_NOT_OBJECT"]
    if s.get("schema") != "SOROK_OPERATIONAL_CURRENTNESS_R1":
        errors.append("SCHEMA_MISMATCH")
    if s.get("as_of") != "2026-11-15T19:45:00-05:00":
        errors.append("EVIDENCE_CUT_NOT_FROZEN")
    if s.get("adoption") != "PENDING_INDEPENDENT_RECEIVING":
        errors.append("ADOPTION_NOT_AUTHORIZED candidate is not adopted")
    if s.get("source_grades") != "SCOPED_SOURCEFREE_ONLY" or s.get("no_authority_promotion") is not True:
        errors.append("AUTHORITY_SCOPE_INFLATED")
    if s.get("original_packet_source") != ORIGINAL_REF or s.get("gmt_overlay_source") != GMT_REF:
        errors.append("SOURCE_COMMIT_PROVENANCE_CHANGED")
    if s.get("unreconciled_external_events") != "UNKNOWN_REQUIRES_LIVE_INTAKE":
        errors.append("UNVERIFIED_EXTERNAL_EVENT_COMPLETENESS")

    edge_contract, class_contract = original_contracts(errors)
    tasks = s.get("tasks")
    if not isinstance(tasks, list):
        errors.append("TASKS_NOT_LIST")
        tasks = []
    ids = [v.get("id") for v in tasks if isinstance(v, dict)]
    if len(tasks) != 27 or len(ids) != 27 or set(ids) != EXPECTED or len(set(ids)) != 27:
        errors.append("PACKET_ID_DENOMINATOR_MISMATCH")
    if {k: sum(t.get("class") == k for t in tasks if isinstance(t, dict))
            for k in EXPECTED_COUNTS} != EXPECTED_COUNTS:
        errors.append("G_M_T_CLASS_COUNT_MISMATCH")
    dag = {}
    for task in tasks:
        if not isinstance(task, dict):
            errors.append("TASK_NOT_OBJECT")
            continue
        key = task.get("id")
        deps = task.get("depends_on")
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
            errors.append(str(key) + " DEPENDENCY_TYPE_INVALID")
            deps = []
        dag[key] = deps
        if deps != edge_contract.get(key):
            errors.append(str(key) + " ORIGINAL_EDGES_MISMATCH")
        if task.get("class") != class_contract.get(key):
            errors.append(str(key) + " ORIGINAL_GMT_MISMATCH")
        expectation = ("SCOPED_RECEIVED_UNMERGED" if key in SCOPED_PINS else
                       "HELD_NOT_LAUNCHED" if key in HELD_OR_UNLAUNCHED else
                       "PARTIAL_CANDIDATE" if key == "E01" else "CANDIDATE")
        if task.get("sourcefree_state") != expectation:
            errors.append(str(key) + " SCOPED_ENG_STATE_CHANGED_WITHOUT_NEW_RECEIPT")
        if task.get("full_original_claim") != "NOT_ESTABLISHED":
            errors.append(str(key) + " FULL_ORIGINAL_CLAIM_INFLATED")
        if key in SCOPED_PINS:
            pr, code_sha, review_sha = SCOPED_PINS[key]
            if task.get("review_pr") != pr:
                errors.append(key + " REVIEW_PR_IDENTITY_MISMATCH")
            if task.get("code_sha") != code_sha:
                errors.append(key + " ACCEPTED_CODE_SHA_MISMATCH")
            if task.get("review_sha") != review_sha:
                errors.append(key + " INDEPENDENT_G5_SHA_MISMATCH")
        elif any(k in task for k in ("review_pr", "review_sha", "code_sha")):
            errors.append(str(key) + " UNSUPPORTED_ACCEPTANCE_PIN")

    # Original edges must be a closed acyclic DAG, not just a plausible 27-node list.
    visiting, visited = set(), set()
    def visit(k):
        if k in visiting:
            errors.append(str(k) + " DEPENDENCY_CYCLE")
            return
        if k in visited or k not in dag:
            return
        visiting.add(k)
        for d in dag[k]:
            if d not in EXPECTED:
                errors.append(str(k) + " DEPENDENCY_UNKNOWN " + str(d))
            else:
                visit(d)
        visiting.remove(k)
        visited.add(k)
    for key in dag:
        visit(key)

    foundations = s.get("protected_foundations")
    if not isinstance(foundations, dict):
        errors.append("PROTECTED_FOUNDATIONS_NOT_OBJECT")
        foundations = {}
    if set(foundations) != set(PROTECTED_PINS):
        errors.append("PROTECTED_SEVEN_MEMBER_DENOMINATOR_MISMATCH")
    for key, (pr, merge_sha, pr_head) in PROTECTED_PINS.items():
        actual = foundations.get(key)
        if not isinstance(actual, dict):
            errors.append(key + " PROTECTED_FOUNDATION_MISSING")
            continue
        if actual.get("pr") != pr:
            errors.append(key + " PROTECTED_PR_IDENTITY_MISMATCH")
        if actual.get("merge_sha") != merge_sha:
            errors.append(key + " PROTECTED_MERGE_SHA_MISMATCH")
        if actual.get("scope") != "SOURCEFREE_PROTECTED":
            errors.append(key + " PROTECTED_SCOPE_INVALID")
        if git:
            code, parents = run_git("show", "-s", "--format=%P", merge_sha)
            if code or len(parents.split()) != 2 or parents.split()[1] != pr_head:
                errors.append(key + " PROTECTED_MERGE_SECOND_PARENT_INVALID")
            if run_git("merge-base", "--is-ancestor", merge_sha, "HEAD")[0]:
                errors.append(key + " PROTECTED_MERGE_NOT_ANCESTOR")

    if s.get("browser") != BROWSER_STATUS:
        errors.append("BROWSER_TERMINAL_AND_HELD_STATUS_CHANGED")
    if s.get("controllers") != CONTROLLER_STATUS:
        errors.append("CONTROLLER_939_STOP_OR_DISPATCH_CHANGED")
    if s.get("outside_packets") != OUTSIDE_STATUS:
        errors.append("OUTSIDE_PACKET_SCOPE_INFLATED")
    execution = s.get("execution")
    if not isinstance(execution, dict):
        errors.append("LOCAL_EXECUTION_NOT_OBJECT")
    else:
        if execution.get("locally_verified_live_workers") is not None:
            errors.append("LIVE_WORKERS_CANNOT_BE_VERIFIED_BY_STATIC_SNAPSHOT")
        if execution.get("last_reported_oldmac_five_receipts") != EXPECTED_RECEIPT:
            errors.append("LAST_REPORTED_EXECUTION_EVIDENCE_CHANGED")

    frontier = s.get("work_frontier")
    if not isinstance(frontier, list):
        errors.append("FRONTIER_NOT_LIST")
        frontier = []
    names = [f.get("id") for f in frontier if isinstance(f, dict)]
    if len(frontier) != len(FRONTIER_STATUS) or len(names) != len(FRONTIER_STATUS) or set(names) != set(FRONTIER_STATUS) or len(set(names)) != len(FRONTIER_STATUS):
        errors.append("FRONTIER_ITEMS_MISSING_DUPLICATE_OR_EXTRA")
    for f in frontier:
        if not isinstance(f, dict):
            errors.append("FRONTIER_ITEM_NOT_OBJECT")
            continue
        key = f.get("id")
        if f.get("state") != FRONTIER_STATUS.get(key):
            errors.append(str(key) + " FRONTIER_STATE_UNAUTHENTICATED")
        if not isinstance(f.get("owner"), str) or not f["owner"].strip():
            errors.append(str(key) + " FRONTIER_OWNER_MISSING")
        if not isinstance(f.get("next_action"), str) or not f["next_action"].strip():
            errors.append(str(key) + " FRONTIER_NEXT_ACTION_MISSING")
    return errors

def render(s):
    """Only render after validated; malformed inputs must give typed RED, never traceback."""
    parts = [
        START,
        "## SOROK operational currentness — generated from paired JSON",
        "**Cut:** " + s["as_of"] + " | **Adoption:** " + s["adoption"],
        "**Evidence grade:** sourcefree engineering where stated; never native, scientific, human or protected integration by implication.",
        "",
        "**Protected:** " + ", ".join(name + " (#" + str(s["protected_foundations"][name]["pr"]) + ")"
                                     for name in ("P3", "P4", "P5", "P6", "MI", "MII", "MIII")) + ".",
        "**Scoped received, unmerged:** " + ", ".join(
            t["id"] + " (#" + str(t["review_pr"]) + ")" for t in s["tasks"]
            if t["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED") + ".",
        "",
        "**Current blockers and next owner actions:**",
    ]
    for x in s["work_frontier"]:
        parts.append("- " + x["id"] + " | " + x["state"] + " | owner: " +
                     x["owner"] + " | next: " + x["next_action"])
    parts += [
        "",
        "**None of the 27 whole original CG-B–G claims is marked complete.**",
        "**External PR/review events and local runner processes:** must be authenticated at each HQ intake; older comments and stored leases are history, not live state.",
        END,
    ]
    return "\n".join(parts)

def self_test(s, whole, md):
    """Explicit hostile mutations; require RED for every reviewed failure class."""
    failures = []
    def expected_red(name, change):
        t = copy.deepcopy(s)
        change(t)
        if not validate(t, git=False):
            failures.append("SELF_TEST_FALSE_GREEN " + name)

    by_task = lambda t, name: next(row for row in t["tasks"] if row["id"] == name)
    expected_red("B05 stale R2", lambda t: by_task(t, "B05").update(sourcefree_state="CANDIDATE"))
    expected_red("C04 acceptance removed", lambda t: by_task(t, "C04").update(sourcefree_state="CANDIDATE"))
    expected_red("C05 acceptance removed", lambda t: by_task(t, "C05").update(sourcefree_state="CANDIDATE"))
    for key in SCOPED_PINS:
        for attr, bad in (("code_sha", "0"*40), ("review_sha", "0"*40), ("review_pr", 999)):
            expected_red(key + " " + attr, lambda t, k=key, a=attr, b=bad:
                         by_task(t, k).update({a:b}))
    for key in PROTECTED_PINS:
        expected_red(key + " PR mismatch",
                     lambda t, k=key: t["protected_foundations"][k].update(pr=999))
        expected_red(key + " arbitrary ancestor",
                     lambda t, k=key: t["protected_foundations"][k].update(
                         merge_sha="6a5c12f04323d74001f9632063ec907f4fc4468e"))
    expected_red("MI missing", lambda t: t["protected_foundations"].pop("MI"))
    expected_red("duplicate task", lambda t: t["tasks"].append(copy.deepcopy(t["tasks"][0])))
    expected_red("original task edge", lambda t: by_task(t,"B05").update(depends_on=["B02"]))
    expected_red("original G/M/T label", lambda t: by_task(t,"B05").update({"class":"G"}))
    expected_red("full claim", lambda t: by_task(t,"B05").update(full_original_claim="ACCEPT"))
    for key, bad in (("issue_1008", "FULL_ACCEPT"), ("issue_1010", "FULL_ACCEPT"),
                     ("issue_1012", "LAUNCHED")):
        expected_red("browser " + key, lambda t, k=key, v=bad: t["browser"].update({k:v}))
    expected_red("939 running", lambda t: t["controllers"].update(issue_939="RUNNING"))
    expected_red("persistent dispatch", lambda t: t["controllers"].update(persistent_dispatch=True))
    for key, bad in (("G03_I0", "FULL_G03_ACCEPTED"), ("CG_A", "MERGED"),
                     ("portal_768", "IMPLEMENTED")):
        expected_red("outside " + key, lambda t, k=key, v=bad: t["outside_packets"].update({k:v}))
    expected_red("adoption forged", lambda t: t.update(adoption="ADOPTED_PROTECTED_CURRENTNESS"))
    expected_red("authority forged", lambda t: t.update(no_authority_promotion=False))
    expected_red("frontier erased", lambda t: t.update(work_frontier=[]))
    expected_red("frontier DONE", lambda t: t["work_frontier"][0].update(state="DONE"))
    expected_red("frontier owner erased", lambda t: t["work_frontier"][0].update(owner=""))
    expected_red("source commit spoof", lambda t: t.update(original_packet_source="0"*40))
    expected_red("live-workers fabricated", lambda t: t["execution"].update(locally_verified_live_workers=0))
    expected_red("unreconciled source feed", lambda t: t.update(unreconciled_external_events="NONE"))

    if md.replace("**Protected:**", "**Not-protected:**", 1) == md:
        failures.append("SELF_TEST_MD_MARKER_NOT_FOUND")
    else:
        altered = md.replace("**Protected:**", "**Not-protected:**", 1)
        if START not in altered or END not in altered:
            failures.append("SELF_TEST_MD_MARKERS_BROKEN")
        elif altered[altered.index(START): altered.index(END)+len(END)] == render(s):
            failures.append("SELF_TEST_MD_MISMATCH_NOT_DETECTED")

    # Exercise actual CLI, not just validate(); must not traceback if MI is missing.
    mutated = copy.deepcopy(whole)
    mutated["operational_currentness_r1"]["protected_foundations"].pop("MI")
    with tempfile.TemporaryDirectory() as td:
        state_path = Path(td) / "bad.json"
        state_path.write_text(json.dumps(mutated))
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--state-file",
             str(state_path), "--no-git", "--status"],
            capture_output=True, text=True, timeout=30)
        if (result.returncode != 1 or "SOROK_CURRENTNESS_RED:" not in result.stderr
                or "PROTECTED_FOUNDATION_MISSING" not in result.stderr
                or "Traceback" in result.stderr):
            failures.append("SELF_TEST_MISSING_MI_CLI_NOT_TYPED_RED")
    return failures

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--no-git", action="store_true",
                        help="Checks frozen SHA identity; skips local merge ancestry/parent proof.")
    parser.add_argument("--state-file", type=Path, default=PROGRESS,
                        help="Explicit fixture input; never adopts or writes the supplied state.")
    args = parser.parse_args()
    errors = []
    try:
        whole = json.loads(args.state_file.read_text())
        s = whole.get("operational_currentness_r1") if isinstance(whole,dict) else None
    except (OSError, ValueError, TypeError) as exc:
        whole, s = None, None
        errors.append("STATE_FILE_UNREADABLE " + str(exc))
    errors += validate(s, git=not args.no_git)
    try:
        md = MARKDOWN.read_text()
    except OSError as exc:
        md = ""
        errors.append("PAIRED_MD_UNREADABLE " + str(exc))
    valid_markers = (md.count(START) == 1 and md.count(END) == 1
                     and md.find(START) < md.find(END))
    if not valid_markers:
        errors.append("PAIRED_MD_MARKERS_MISSING_OR_DUPLICATE")
    elif not errors and md[md.index(START):md.index(END)+len(END)] != render(s):
        errors.append("PAIRED_MD_JSON_DRIFT")
    if args.self_test and not errors:
        errors += self_test(s, whole, md)
    if errors:
        for error in errors:
            print("SOROK_CURRENTNESS_RED: " + error, file=sys.stderr)
        return 1
    if args.status:
        print(render(s))
        print("SOROK_CURRENTNESS_NOT_LIVE: external PR/runner intake not implemented")
    print("SOROK_CURRENTNESS_PASS: frozen 27 source-backed packets, 7 exact protected merges, 3 scoped G5; NOT adopted/live")
    return 0

if __name__ == "__main__":
    sys.exit(main())
