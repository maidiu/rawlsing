#!/usr/bin/env python3
"""ZAK-00 v2 MCR-C: source-frozen original-task and output identity conservation.
This is a pre-dispatch contract court; it does NOT certify descendants' work.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLIGHTS = Path(__file__).resolve().parent / "FLIGHT_LAUNCHES"
FROZEN_AUTHOR = "9d24323494cc852ada078010f09bfcf9ceb911d9"
R2_INHERITANCE = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/ZAKONCHILOC/ZAK_INHERITED_OBLIGATIONS.tsv"
AR_SEED = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/DATA/LEGACY_AR58_SEED.tsv"
FULL_FAMILY_FLIGHTS = {1: (58, "release_id", AR_SEED),
                       8: (182, "zak_evidence_key", R2_INHERITANCE),
                       10: (182, "zak_evidence_key", R2_INHERITANCE),
                       11: (182, "zak_evidence_key", R2_INHERITANCE)}
BAD = re.compile("[\u00ad\u200b\u200c\u200d\u2060\ufeff]")
FLIGHT_RE = re.compile(r"^\d+\. (WORKER_RETURNS/[^\n]+)$", re.M)
TASK_RE = re.compile(r"^[1-4]\. (.+)$", re.M)

def git(*args):
    p = subprocess.run(["git", "-C", str(ROOT), *args],
                       capture_output=True, text=True, check=False)
    if p.returncode:
        raise AssertionError("git " + " ".join(args) + ": " + p.stderr[:220])
    return p.stdout

def source_bytes(path, commit):
    return git("show", commit + ":" + path)

def load_contract(text):
    match = re.search(r"MCR_COMPLETION_CONTRACT_BEGIN\n(.*?)\nMCR_COMPLETION_CONTRACT_END", text, re.S)
    if not match:
        raise AssertionError("missing completion contract")
    contract = {"MCR_SCOPE": [], "MCR_OBLIGATION": [], "MCR_RECEIVING": []}
    for line in match.group(1).splitlines():
        k, sep, obj = line.partition(": ")
        if not sep or k not in contract:
            raise AssertionError("unknown MCR-C record " + k)
        contract[k].append(json.loads(obj, object_pairs_hook=_reject_duplicate_keys))
    if len(contract["MCR_SCOPE"]) != 1 or len(contract["MCR_RECEIVING"]) != 1:
        raise AssertionError("one scope and receiving required")
    return contract, match.group(1)

def _reject_duplicate_keys(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise AssertionError("duplicate JSON key " + k)
        d[k] = v
    return d

def flight_path(n):
    return FLIGHTS / ("ZAK_%02d_FULL_COPY_PASTE_MCR.md" % n)

def required_ids(n, contract=None):
    if contract is None:
        contract, _ = load_contract(flight_path(n).read_text(encoding="utf-8"))
    scope = contract["MCR_SCOPE"][0]
    s = scope["source"]
    if n in FULL_FAMILY_FLIGHTS:
        expected, col, source = FULL_FAMILY_FLIGHTS[n]
        assert scope["expected_count"] == expected and scope["identity_columns"] == [col]
        assert s["path"] == source, (n, s["path"], source)
        rows = list(csv.DictReader(source_bytes(s["path"], s["commit"]).splitlines(), delimiter="\t"))
        ids = [json.dumps([row[col]], ensure_ascii=False, separators=(",", ":")) for row in rows]
    else:
        assert "identity_columns" not in scope
        ids = [item["id"] for item in contract["MCR_OBLIGATION"]]
        assert scope["expected_count"] == len(ids)
    assert len(set(ids)) == len(ids) == scope["expected_count"], (n, len(ids), scope["expected_count"])
    return ids

def validate_one(n, text=None):
    path = flight_path(n)
    current = text if text is not None else path.read_text(encoding="utf-8")
    old = source_bytes(path.relative_to(ROOT).as_posix(), FROZEN_AUTHOR)
    orig_tasks = TASK_RE.findall(old[old.index("REQUIRED POSITIVE/NEGATIVE/CONSUMER CHALLENGE"):
                                 old.index("DELIVERABLE FILES")])
    orig_outputs = FLIGHT_RE.findall(old[old.index("DELIVERABLE FILES"):old.index("ENGINEERING COURT")])
    orig_outputs = [p.replace("\u00ad", "") for p in orig_outputs]
    assert len(orig_tasks) == 4 and 3 <= len(orig_outputs) <= 4
    contract, raw = load_contract(current)
    assert not BAD.search(current), "hidden Unicode"
    assert "315251451a6d112fb312a6e80b096d345c5de6" not in current, "D01 invalid commit"
    assert not re.search(r"(?<![0-9a-f])[0-9a-f]{30,39}(?![0-9a-f])", current, re.I), "truncated source hash"
    assert not re.search(r"(?<![A-Za-z0-9])[0-9a-f]{8}\.\.\.", current, re.I), "abbreviated digest"
    assert len(contract["MCR_OBLIGATION"]) == 5 + len(orig_outputs), (n, "task or output omitted")
    records = {item["id"]: item for item in contract["MCR_OBLIGATION"]}
    assert len(records) == len(contract["MCR_OBLIGATION"]), "duplicate obligation"
    for j, task in enumerate(orig_tasks, 1):
        key = "ZAK%02d-TASK-%02d" % (n, j)
        assert records[key].get("baseline_requirement") == task, (key, "old task modified, omitted, or truncated")
        assert records[key]["positive"].startswith("PASS=")
        assert records[key]["negative"].startswith("RED=")
        assert records[key]["positive"] != records[key]["negative"]
        assert records[key]["failure"] == "INCOMPLETE"
        assert records[key]["source"].get("blob") and len(records[key]["source"]["blob"]) == 40
    hostile = records["ZAK%02d-HOSTILE" % n]
    assert hostile.get("baseline_requirement", "").startswith("NEW REVIEW NEGATIVE"), "hostile case absent"
    for j, opath in enumerate(orig_outputs, 1):
        key = "ZAK%02d-OUTPUT-%02d" % (n, j)
        rec = records[key]
        assert rec["baseline_output"] == opath and rec["output"] == opath, (key, "original deliverable omitted/renamed")
        assert rec["positive"].startswith("PASS=") and rec["negative"].startswith("RED=")
        assert rec["failure"] == "INCOMPLETE"
    ids = required_ids(n, contract)
    assert contract["MCR_RECEIVING"][0]["author_ceiling"] == "DELIVERED_PENDING_RECEIVING"
    assert contract["MCR_RECEIVING"][0]["on_any_failure"] == "INCOMPLETE"
    if n == 1:
        assert "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13" in current, "D03 AR0005 absent"
        assert "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b" in current, "D03 AR0006 absent"
    if n in (2, 8):
        assert "V552J" in raw and "12" in raw and "F03" in raw, "D05-D07 J/F03 near positive omitted"
    if n == 2:
        assert "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR" in raw, "D07 V552 scoring/coverage separation missing"
    if n == 8:
        assert "LMX-043" in raw and "LMQ-001" in raw and "LMQ-009" in raw, "D04 lifecycle and parity debts dropped"
    return {"flight": n, "tasks": 4, "hostile": 1, "outputs": len(orig_outputs),
            "obligations": len(records), "coverage_identity_count": len(ids), "status": "PASS_AUTHOR_CONTRACT_COMPLETENESS_NOT_EXECUTED_DESCENDANTS"}


def validate_parent(text=None):
    parent_path = Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md"
    current = text if text is not None else parent_path.read_text(encoding="utf-8")
    old = source_bytes(parent_path.relative_to(ROOT).as_posix(), FROZEN_AUTHOR)
    section = old[old.index("DELIVERABLES / TERMINAL HANDOFF"):old.index("\nSTOP:")]
    baseline = re.findall(r"^- (.+)$", section, re.M)
    assert len(baseline) == 6, "six original parent results must remain"
    assert not BAD.search(current)
    contract, raw = load_contract(current)
    rows = contract["MCR_OBLIGATION"]
    assert len(rows) == 24 and len({ob["id"] for ob in rows}) == 24, "24 parent result requirements"
    byid = {ob["id"]: ob for ob in rows}
    for j, req in enumerate(baseline, 1):
        ob = byid["ZAK00-PARENT-%02d" % j]
        assert ob["baseline_requirement"] == req, ("parent scope shrunk", j)
        assert ob["positive"].startswith("PASS=") and ob["negative"].startswith("RED=")
        assert ob["failure"] == "INCOMPLETE"
    for n in range(1, 12):
        ob = byid["ZAK00-FLIGHT-%02d" % n]
        assert ob["output"] == flight_path(n).relative_to(ROOT).as_posix()
        assert ob["baseline_output"] == ob["output"]
        assert "four" in ob["result"] or "4 exact" in ob["result"], n
        assert ob["failure"] == "INCOMPLETE"
    required_parent_files = [
        "00_RETURN.md", "01_CUSTODY_SOURCE_IDENTITY_AND_GRADE.md",
        "02_MCR_ORACLE_NEGATIVE_AND_INDEPENDENT_STRESS.md",
        "03_FULL_FLIGHT_DEPENDENCY_AND_OWNER_MAP.md",
        "04_AUTHOR_STRUCTURAL_PREFLIGHT_AND_NEGATIVE_RECEIPT.md",
        "05_EXACT_HEAD_INDEPENDENT_RECEIVING_HANDOFF.md",
        "06_FIXED_HIGH_IMPACT_NO_INVERSE_PANEL.md",
    ]
    for j, filename in enumerate(required_parent_files, 1):
        ob = byid["ZAK00-OUTPUT-%02d" % j]
        assert ob["output"] == ("WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/" + filename)
        assert ob["baseline_output"] == ob["output"]
    scope = contract["MCR_SCOPE"][0]
    assert scope["identity_columns"] == ["zak_evidence_key"] and scope["expected_count"] == 182
    assert scope["source"]["path"] == R2_INHERITANCE
    def inherited(commit):
        return list(csv.DictReader(source_bytes(R2_INHERITANCE, commit).splitlines(), delimiter="\t"))
    r1 = inherited("480a3e211814705eac6cada7257e8187f46eb5f0")
    r2 = inherited("1ebd603aa8f5b6d551363336a632a0c364b85f17")
    assert len(r1) == len(r2) == 182
    keys1 = list(r1[0].keys())
    assert len(keys1) == 14
    a = {row["zak_evidence_key"]: tuple(row[key] for key in keys1) for row in r1}
    b = {row["zak_evidence_key"]: tuple(row[key] for key in keys1) for row in r2}
    assert len(a) == len(b) == 182 and a == b, "182 inherited IDs or first-14 original cells changed"
    pins_path = R2_INHERITANCE.replace("ZAK_INHERITED_OBLIGATIONS.tsv", "ZAK_SOURCE_BASELINE.tsv")
    pins = list(csv.DictReader(source_bytes(pins_path, "1ebd603aa8f5b6d551363336a632a0c364b85f17").splitlines(), delimiter="\t"))
    assert len(pins) == 47 and len({row["source_key"] for row in pins}) == 47
    for p in pins:
        actual = git("rev-parse", p["frozen_commit_sha"] + ":" + p["repository_path"]).strip()
        assert actual == p["git_blob_sha"], ("47 source pin mismatch", p["source_key"])
    _validate_claim_contract_bindings(byid)
    assert all(ob["failure"] == "INCOMPLETE" and ob["owner"] and ob["consumer"]
               and ob["negative"].startswith("RED=") for ob in rows)
    return {"parent": "ZAK00", "obligations": 24, "identity_count": 182,
            "first_14_equal": 182, "exact_source_pins": 47,
            "status": "PASS_AUTHOR_PARENT_CONTRACT_NOT_INDEPENDENT_RECEIVING"}


# Exact original-claim domain binding: not merely a 24-row hash census.
# This is distinct from the independent-science/authority review.
CLAIM_OUTPUTS = {
    "ZAK00-PARENT-01": "WORKER_COMMISSIONS/VMESTYE_ZAKONCHILOS_ZAK00_V2_MCR/00_MCR_SOURCE_CONSTRUCTION_AND_WHOLE_MISSION.md",
    "ZAK00-PARENT-02": "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/01_CUSTODY_SOURCE_IDENTITY_AND_GRADE.md",
    "ZAK00-PARENT-03": "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/03_FULL_FLIGHT_DEPENDENCY_AND_OWNER_MAP.md",
    "ZAK00-PARENT-06": "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/05_EXACT_HEAD_INDEPENDENT_RECEIVING_HANDOFF.md",
    "ZAK00-OUTPUT-05": "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/04_AUTHOR_STRUCTURAL_PREFLIGHT_AND_NEGATIVE_RECEIPT.md",
}
FLIGHT_MAP = "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/03_FULL_FLIGHT_DEPENDENCY_AND_OWNER_MAP.md"
FROZEN_PYTHON_COURT = "42906583428"
FROZEN_PYTHON_HEAD = "61e23d77d72dd349c48a106636336403f3caed86"
RECEIVING_ISSUES = (814, 815, 816, 817)
FROZEN_R3_SOURCE_HEAD = "b07a24da517016d91da7ddcd92a0b6c54d07911d"
ORIGINAL_AUTHOR_ACCOUNT = "maidiu"


def _contract_obligations(prompt_text=None):
    path = Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md"
    current = prompt_text if prompt_text is not None else path.read_text(encoding="utf-8")
    contract, _ = load_contract(current)
    return {ob["id"]: ob for ob in contract["MCR_OBLIGATION"]}


def _artifact_text(path, substitutions=None):
    if substitutions and path in substitutions:
        return substitutions[path]
    p = ROOT / path
    assert p.is_file(), "required output absent: " + path
    return p.read_text(encoding="utf-8")


def _flight_rows(map_text, *, compare_frozen=True):
    # Read the primary-jurisdiction table only. The same flight may lawfully
    # appear later in the readiness/hold table; that is not duplicate ownership.
    section = map_text.split("## Eligibility and genuine dependencies", 1)[0]
    rows = {}
    for line in section.splitlines():
        m = re.match(r"^\| ZAK-(\d\d) \| (.+)$", line)
        if not m:
            continue
        num = int(m.group(1))
        assert 1 <= num <= 11 and num not in rows, "duplicate/out-of-universe flight owner"
        fields = [x.strip() for x in line.strip("|").split("|")]
        assert len(fields) == 5, "every flight must have 5 explicit jurisdiction/consumer columns"
        assert all(fields[1:]), "owner/consumer/dispatch field cannot be blank"
        rows[num] = fields
    assert set(rows) == set(range(1, 12)), "missing or extra whole-mission jurisdiction"
    # Freeze each substantively distinct primary role independently of the 11 IDs.
    assert len({row[1] for row in rows.values()}) == 11, "duplicate substantive jurisdiction despite 11 IDs"
    if compare_frozen:
        canonical = _flight_rows(source_bytes(FLIGHT_MAP, FROZEN_R3_SOURCE_HEAD),
                                 compare_frozen=False)
        for n in range(1, 12):
            assert rows[n][1] == canonical[n][1], (
                "source-qualified primary jurisdiction changed or swapped", n)
    return rows


def _validate_claim_contract_bindings(obligations):
    for oid, output in CLAIM_OUTPUTS.items():
        ob = obligations[oid]
        assert ob["output"] == output, (oid, "wrong completion evidence domain")
        assert ob["evidence"].startswith("WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/")
        assert ob["positive"].startswith("PASS=") and ob["negative"].startswith("RED=")
        assert ob["failure"] == "INCOMPLETE"
        assert "source" in ob and set(ob["source"]) == {"path", "commit", "blob"}
    for oid in ("ZAK00-PARENT-01", "ZAK00-PARENT-02", "ZAK00-PARENT-03", "ZAK00-OUTPUT-05"):
        ob = obligations[oid]
        assert ob["check_kind"] == "EXEC" and ob["check"].startswith("RUN: python3 ")
        assert ("--claim " + oid) in ob["check"]
    ack = obligations["ZAK00-PARENT-06"]
    assert ack["check_kind"] == "INDEPENDENT" and ack["minimum_grade"] == "AUTHORITY"
    assert all(("#%d" % n) in ack["consumer"] for n in RECEIVING_ISSUES)
    assert all(str(n) in ack["result"] for n in RECEIVING_ISSUES)
    assert "acknowledg" in ack["positive"].lower()
    return True



def _current_ci_provenance(ctx=None):
    """Bind current source/CI proof to the *running* exact HEAD, not an old run number."""
    ctx = os.environ if ctx is None else ctx
    if ctx.get("GITHUB_ACTIONS") != "true":
        return None
    run = ctx.get("GITHUB_RUN_ID", "")
    assert run.isdecimal() and int(run) > 0, "missing actual Actions run ID"
    assert run not in (FROZEN_PYTHON_COURT, "42922393484"), "stale run is not current"
    assert ctx.get("GITHUB_REPOSITORY") == "maidiu/rawlsing"
    assert "ZAK-00 v2 MCR-C" in ctx.get("GITHUB_WORKFLOW", "")
    candidate = git("rev-parse", "HEAD").strip()
    event_path = ctx.get("GITHUB_EVENT_PATH", "")
    # The host GITHUB_SHA for pull_request events is a synthetic merge commit:
    # use the *actual* event pull request head instead, not the merge SHA.
    if event_path:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        ehead = (event.get("pull_request", {}).get("head", {}).get("sha")
                 or event.get("after"))
    else:
        ehead = ctx.get("GITHUB_SHA")
    assert ehead == candidate, ("current CI event HEAD diverges from checkout", ehead, candidate)
    return {"candidate_sha": candidate, "github_run_id": run,
            "event": ctx.get("GITHUB_EVENT_NAME", "unknown"),
            "trusted_origin": "RUNNING_GITHUB_ACTIONS_SOURCE_CHECK_NOT_INDEPENDENT_REVIEW"}


def evaluate_acknowledgments(acks=None, candidate_sha=None, qualification_verifier=None):
    """Real negative -> externally verifiable positive eligibility, NEVER author approval.

    The verifier is a competency/credential decision furnished by an INDEPENDENT
    receiving host. Author-controlled JSON flags are not trusted. Validity of a
    synthetic test verifier does not confer rights in the real repository.
    """
    blocked = {"id": "ZAK00-PARENT-06", "status": "BLOCKED_EXACT_DEPENDENCY",
               "reason": "NO_QUALIFIED_INDEPENDENT_RECEIVING_ACKNOWLEDGMENT",
               "required_issues": list(RECEIVING_ISSUES),
               "scientific_actor_issuer": "NOT_GRANTED"}
    if not acks or not candidate_sha or qualification_verifier is None:
        return blocked
    if not isinstance(acks, list) or len(acks) != 4:
        return {**blocked, "reason": "EXACTLY_FOUR_INDEPENDENT_RECEIPTS_REQUIRED"}
    if not re.fullmatch("[0-9a-f]{40}", candidate_sha):
        return {**blocked, "reason": "INVALID_FROZEN_CANDIDATE_SHA"}
    seen = set()
    for a in acks:
        if not isinstance(a, dict):
            return {**blocked, "reason": "INVALID_RECEIVING_RECORD"}
        issue = a.get("issue")
        if issue not in RECEIVING_ISSUES or issue in seen:
            return {**blocked, "reason": "DUPLICATE_OR_UNQUALIFIED_ISSUE"}
        seen.add(issue)
        if a.get("candidate_sha") != candidate_sha:
            return {**blocked, "reason": "WRONG_SHA_ACKNOWLEDGMENT"}
        login = a.get("github_actor")
        if not isinstance(login, str) or not login.strip() or login.lower() == ORIGINAL_AUTHOR_ACCOUNT:
            return {**blocked, "reason": "SELF_AUTHORED_OR_NO_REVIEWER_ID"}
        if a.get("scope") != "ZAK00_R3_SCOPED_SOURCE_HANDOFF" or a.get("decision") not in (
            "RECEIVED_FOR_REVIEW", "ACCEPT_SCOPED_S0_S1", "HOLD_WITH_NAMED_SCOPE"
        ):
            return {**blocked, "reason": "WRONG_SCOPE_OR_UNSIGNED_DECISION"}
        receipt = a.get("comment_url", "")
        if not (isinstance(receipt, str) and
                receipt.startswith("https://github.com/maidiu/rawlsing/issues/" + str(issue) + "#issuecomment-")):
            return {**blocked, "reason": "MISSING_EXISTING_RECEIVING_SURFACE"}
        # An actual reviewer-owned, externally checked credential/issue-comment
        # verifier must return a structured authentication result.
        adjudication = qualification_verifier(a)
        if not isinstance(adjudication, dict) or not all(
            adjudication.get(k) is True for k in (
                "independently_authenticated_comment", "competent_issue_owner",
                "credential_distinct_from_author", "same_candidate_and_scope"
            )
        ):
            return {**blocked, "reason": "INDEPENDENT_ISSUER_NOT_VERIFIED"}
    if seen != set(RECEIVING_ISSUES):
        return {**blocked, "reason": "INCOMPLETE_JURISDICTIONS"}
    return {"id": "ZAK00-PARENT-06",
            "status": "ELIGIBLE_FOR_SEPARATE_AUTHORITY_COURT",
            "receiving_issues": sorted(seen),
            "candidate_sha": candidate_sha,
            "not_author_CERTIFIED_PASS": True,
            "scientific_actor_issuer": "NOT_GRANTED"}

def prove_parent_claim(oid, prompt_text=None, substitutions=None, *, acknowledgments=None, candidate_sha=None, qualification_verifier=None, ci_context=None):
    obs = _contract_obligations(prompt_text)
    _validate_claim_contract_bindings(obs)
    assert oid in CLAIM_OUTPUTS, "unsupported gate " + oid
    output = CLAIM_OUTPUTS[oid]
    doc = _artifact_text(output, substitutions)
    assert doc.strip(), "required artifact empty " + oid
    if oid == "ZAK00-PARENT-01":
        charter = doc
        map_text = _artifact_text(FLIGHT_MAP, substitutions)
        rows = _flight_rows(map_text)
        for n in range(1, 12):
            # Whole mission including distinct territory, not just 11 counted files.
            assert ("ZAK-%02d" % n) in charter
            assert rows[n][1] and rows[n][3] and rows[n][4]
            validate_one(n)
        for token in ("**Primary:**", "**Secondary:**", "Dva/Trii/Chetiri",
                      "ZAK-00R", "#814", "#815", "#816", "#817"):
            assert token in charter or token in map_text, "missing charter/receiving function " + token
        for n in (1, 2, 3, 4, 8):
            assert "parallel" in rows[n][2].lower(), ("independent flight serially barred", n)
        assert "not pilot completion" in map_text and "not blocked by one F03" in charter
        return {"id": oid, "status": "PASS_SOURCE_GRADED_DOCUMENTARY_CHARter_AND_FULL_MAP",
                "actual_flight_ids": sorted(rows), "first_consumer": "ZAK00R then PROGRAMMA dispatcher"}
    if oid == "ZAK00-PARENT-02":
        assert "182" in doc and "47" in doc and "first-14" in doc
        stats = validate_parent()
        assert stats["first_14_equal"] == 182 and stats["exact_source_pins"] == 47
        assert "not 47 original-runtime" in doc
        return {"id": oid, "status": "PASS_SOURCE_CUSTODY_ONLY", "first14_equal": 182, "source_pins": 47}
    if oid == "ZAK00-PARENT-03":
        rows = _flight_rows(doc)
        for n in range(1, 12):
            validate_one(n)
        for token in ("ZAK-01/02/03/04/08", "ZAK-05", "ZAK-06", "ZAK-07", "ZAK-09",
                      "ZAK-10", "ZAK-11", "ZAK00R", "#814", "#815", "#816", "#817"):
            assert token in doc, "missing owner/consumer " + token
        assert "not pilot completion" in doc
        assert "original35" in doc
        return {"id": oid, "status": "PASS_SOURCE_GRADED_COMPLETE_DISPATCH_MAP",
                "flight_count": 11, "held_grades_not_promoted": True}
    if oid == "ZAK00-OUTPUT-05":
        # Three separate epochs; a prior NOT_RUN does not contradict later execution.
        for token in ("Historical author construction", "Python CLI: NOT_RUN",
                      FROZEN_PYTHON_COURT, FROZEN_PYTHON_HEAD,
                      "MCR-C", "12/12", "182", "47", "postcommit",
                      "same candidate SHA", "NO native"):
            assert token in doc, "missing historical/current CI receipt distinction " + token
        ci = _current_ci_provenance(ci_context)
        if ci is None:
            return {"id": oid, "status": "INCOMPLETE_CURRENT_CANDIDATE_CI_NOT_ATTESTED",
                    "historical_python": "NOT_RUN", "later_verified_run": FROZEN_PYTHON_COURT}
        return {"id": oid, "status": "PASS_AUTHOR_EXEC_CURRENT_CI_SOURCE_PROVENANCE",
                "historical_python": "NOT_RUN", "later_verified_run": FROZEN_PYTHON_COURT,
                "candidate_ci": ci}
    # The live authority state is NOT a constant or a keyword in an author document.
    assert oid == "ZAK00-PARENT-06"
    for n in RECEIVING_ISSUES:
        assert ("#%d" % n) in doc, "no named receiving jurisdiction #%d" % n
    return evaluate_acknowledgments(acknowledgments, candidate_sha, qualification_verifier)


def run_claim_gates(prompt_text=None, substitutions=None, *, acknowledgments=None, candidate_sha=None, qualification_verifier=None, ci_context=None):
    obs = _contract_obligations(prompt_text)
    _validate_claim_contract_bindings(obs)
    ids = list(CLAIM_OUTPUTS)
    results = [prove_parent_claim(oid, prompt_text, substitutions,
             acknowledgments=acknowledgments, candidate_sha=candidate_sha,
             qualification_verifier=qualification_verifier, ci_context=ci_context) for oid in ids]
    blocked = [r["id"] for r in results if r["status"] == "BLOCKED_EXACT_DEPENDENCY"]
    assert not any(r["status"] == "PASS" for r in results), "unqualified author self-approval"
    assert set(blocked) <= {"ZAK00-PARENT-06"}, "unexpected or hidden authority blocker"
    return {"stage": "AUTHOR_CONTRACT_REPAIR_TEST_NOT_INDEPENDENT_RECEIVING",
            "results": results, "blocked_obligations": blocked,
            "author_whole_parent_ready": False,
            "zero_false_positive_authority_proof": True}



def audit_author_evidence_vector(entries, *, ci_context=None):
    """Evidence authenticity: never let author PASS a reviewer-owned result."""
    obs = _contract_obligations()
    indexed = {}
    for item in entries:
        oid = item.get("id")
        assert oid in obs and oid not in indexed, ("unknown/duplicate evidence", oid)
        indexed[oid] = item
    assert set(indexed) == set(obs), "missing/excess claim evidence"
    author_pass = []
    independent_held = []
    for oid, ob in obs.items():
        item = indexed[oid]
        if ob["check_kind"] != "EXEC":
            assert item.get("status") == "INCOMPLETE", (
                "AUTHOR_FORGED_INDEPENDENT_PASS", oid, item.get("status"))
            independent_held.append(oid)
            continue
        if item.get("status") == "PASS":
            proof = prove_parent_claim(oid, ci_context=ci_context)
            assert proof["status"].startswith("PASS_"), (
                "UNEXECUTED_AUTHOR_PROOF_MASQUERADING_AS_PASS", oid, proof["status"])
            assert item.get("grade") == "S1", ("wrong author-exec grade", oid)
            author_pass.append(oid)
        else:
            assert item.get("status") == "INCOMPLETE", ("unknown author state", oid)
    assert len(independent_held) == 20
    return {"status": "PASS_AUTHOR_EVIDENCE_BOUNDARY_NOT_INDEPENDENT_ACCEPTANCE",
            "author_executed_pass": author_pass,
            "independent_pending": independent_held,
            "independent_pass_issued": 0}


def near_positive_regressions():
    # Retain all 11 IDs and five populated cells while destroying 10 jurisdictions.
    original = _artifact_text(FLIGHT_MAP)
    lines = original.splitlines()
    first = _flight_rows(original)[1][1]
    mutant = []
    in_table = True
    for line in lines:
        if line.startswith("## Eligibility and genuine dependencies"):
            in_table = False
        m = re.match(r"^\| ZAK-(\d\d) \| ", line) if in_table else None
        if m and int(m.group(1)) > 1:
            cells = [c.strip() for c in line.strip("|").split("|")]
            cells[1] = first
            line = "| " + " | ".join(cells) + " |"
        mutant.append(line)
    corrupted = "\n".join(mutant) + "\n"
    assert corrupted != original
    checks = 0
    for oid in ("ZAK00-PARENT-01", "ZAK00-PARENT-03"):
        try:
            prove_parent_claim(oid, substitutions={FLIGHT_MAP: corrupted})
        except AssertionError:
            checks += 1
        else:
            raise AssertionError("eleven ids but one jurisdiction passed: " + oid)

    # Near-positive: a swap also destroys source-qualified ownership despite uniqueness.
    mutated = original.replace(_flight_rows(original)[2][1], "@@TEMP-JURIS@@", 1)
    mutated = mutated.replace(_flight_rows(original)[3][1], _flight_rows(original)[2][1], 1)
    mutated = mutated.replace("@@TEMP-JURIS@@", _flight_rows(original)[3][1], 1)
    try:
        prove_parent_claim("ZAK00-PARENT-03", substitutions={FLIGHT_MAP: mutated})
    except AssertionError:
        checks += 1
    else:
        raise AssertionError("swapped semantic jurisdictions passed")

    # Positive eligibility transition uses an externally supplied qualification
    # verdict only in this CONTROLLED SYNTHETIC TEST. Never constitutes receipt.
    candidate = git("rev-parse", "HEAD").strip()
    def fixture_verifier(entry):
        return dict.fromkeys(("independently_authenticated_comment", "competent_issue_owner",
             "credential_distinct_from_author", "same_candidate_and_scope"), True)
    receipts = [{"issue": n, "candidate_sha": candidate,
        "github_actor": "external-reviewer-%d" % n,
        "scope": "ZAK00_R3_SCOPED_SOURCE_HANDOFF",
        "decision": "RECEIVED_FOR_REVIEW",
        "comment_url": "https://github.com/maidiu/rawlsing/issues/%d#issuecomment-%d" % (n, n+1200)}
        for n in RECEIVING_ISSUES]
    result = evaluate_acknowledgments(receipts, candidate, fixture_verifier)
    assert result["status"] == "ELIGIBLE_FOR_SEPARATE_AUTHORITY_COURT"
    assert result["not_author_CERTIFIED_PASS"] is True
    checks += 1
    negatives = [
        (receipts[:-1], candidate, fixture_verifier),
        ([{**a, "candidate_sha": "0"*40} if i == 0 else a for i, a in enumerate(receipts)],
         candidate, fixture_verifier),
        ([{**a, "github_actor": ORIGINAL_AUTHOR_ACCOUNT} if i == 0 else a for i, a in enumerate(receipts)],
         candidate, fixture_verifier),
        ([{**a, "scope": "UNRESTRICTED"} if i == 0 else a for i, a in enumerate(receipts)],
         candidate, fixture_verifier),
        (receipts, candidate, lambda _: {"independently_authenticated_comment": True}),
        (receipts, candidate, None),
    ]
    for rows, sha, verify in negatives:
        r = evaluate_acknowledgments(rows, sha, verify)
        assert r["status"] == "BLOCKED_EXACT_DEPENDENCY"
        checks += 1
    # A self-authored forged PASS/AUTHORITY record is caught by the claim/authority
    # court even when the underlying official structural verifier would accept hashes.
    obs = _contract_obligations()
    records = [{"id": oid, "status": "INCOMPLETE", "grade": "S0"} for oid in obs]
    baseline = audit_author_evidence_vector(records)
    assert baseline["independent_pass_issued"] == 0
    checks += 1
    forged = [dict(r) for r in records]
    for r in forged:
        if r["id"] == "ZAK00-PARENT-06":
            r.update({"status": "PASS", "grade": "AUTHORITY"})
    try:
        audit_author_evidence_vector(forged)
    except AssertionError as e:
        assert "AUTHOR_FORGED_INDEPENDENT_PASS" in str(e)
        checks += 1
    else:
        raise AssertionError("forged authority record passed author proof guard")
    # Historical 429065... old-run description survives; missing new trusted
    # GitHub CI context MUST NOT produce current candidate source-evidence PASS.
    without = prove_parent_claim("ZAK00-OUTPUT-05", ci_context={"GITHUB_ACTIONS": "false"})
    assert without["status"] == "INCOMPLETE_CURRENT_CANDIDATE_CI_NOT_ATTESTED"
    checks += 1
    for fake in [
        {"GITHUB_ACTIONS": "true", "GITHUB_RUN_ID": FROZEN_PYTHON_COURT,
         "GITHUB_REPOSITORY": "maidiu/rawlsing", "GITHUB_SHA": candidate,
         "GITHUB_WORKFLOW": "ZAK-00 v2 MCR-C"},
        {"GITHUB_ACTIONS": "true", "GITHUB_RUN_ID": "99999999991",
         "GITHUB_REPOSITORY": "maidiu/rawlsing", "GITHUB_SHA": "0"*40,
         "GITHUB_WORKFLOW": "ZAK-00 v2 MCR-C"},
    ]:
        try:
            prove_parent_claim("ZAK00-OUTPUT-05", ci_context=fake)
        except AssertionError:
            checks += 1
        else:
            raise AssertionError("stale or wrong candidate CI falsely qualified")
    assert checks == 15, checks
    return {"status": "PASS_15_OF_15_NEAR_POSITIVE_AND_FORGED_AUTHORITY_REGRESSIONS",
            "original_jurisdictions": 11, "corrupted_jurisdictions": 1,
            "synthetic_authority_positive": "ELIGIBLE_FOR_SEPARATE_AUTHORITY_COURT_ONLY",
            "actual_authority_received": False}



def make_postcommit_author_evidence(destination, *, ci_context=None):
    """Build SHA-bound source-evidence ONLY for personally executed author tests.

    All independent checks remain INCOMPLETE regardless of output/file/hash
    existence. The official MCR-C return checker is not an authority issuer.
    """
    prompt = Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md"
    scope, contract = load_contract(prompt.read_text(encoding="utf-8"))
    obs = scope["MCR_OBLIGATION"]
    candidate = git("rev-parse", "HEAD").strip()
    ci = _current_ci_provenance(ci_context)
    assert ci is not None and ci["candidate_sha"] == candidate, "same candidate current Actions execution required"
    contract_digest = hashlib.sha256(contract.strip().encode("utf-8")).hexdigest()
    def attached(path):
        p = ROOT / path
        assert p.is_file(), "uncommitted evidence path " + path
        digest = git("hash-object", path).strip()
        actual = git("rev-parse", candidate + ":" + path).strip()
        assert digest == actual, "uncommitted or modified evidence " + path
        return hashlib.sha256(p.read_bytes()).hexdigest()
    records = []
    lines = ["MCR_COMPLETION_EVIDENCE_BEGIN"]
    for o in obs:
        oid = o["id"]
        # The only eligible author PASS comes from a real current-CI executed
        # check. Independent means qualified external court, never author.
        status, grade = "INCOMPLETE", "S0"
        if o["check_kind"] == "EXEC":
            r = prove_parent_claim(oid, ci_context=ci_context)
            if r["status"].startswith("PASS_"):
                status, grade = "PASS", "S1"
        record = {"id": oid, "candidate_sha": candidate,
                  "contract_sha256": contract_digest,
                  "status": status, "grade": grade,
                  "output_file": o["output"], "output_sha256": attached(o["output"]),
                  "evidence_file": o["evidence"], "evidence_sha256": attached(o["evidence"])}
        records.append(record)
        lines.append("MCR_EVIDENCE: " + json.dumps(record, sort_keys=True))
    audit = audit_author_evidence_vector(records, ci_context=ci_context)
    assert len(audit["author_executed_pass"]) == 4
    assert len(audit["independent_pending"]) == 20
    coverage = "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/MCRC_DELIVERED_182_IDS.txt"
    lines.append("MCR_COVERAGE: " + json.dumps({
        "candidate_sha": candidate, "contract_sha256": contract_digest,
        "delivered_ids_file": coverage, "delivered_ids_sha256": attached(coverage)}, sort_keys=True))
    lines.append("MCR_COMPLETION_EVIDENCE_END")
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    Path(destination).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"candidate_sha": candidate, "contract_sha256": contract_digest,
            "github_actions_run_id": ci["github_run_id"],
            "author_exec_pass": audit["author_executed_pass"],
            "independent_unreceived": audit["independent_pending"],
            "authority_ceiling": "INCOMPLETE_UNTIL_GENUINE_INDEPENDENT_RECEIVING"}


def audit_postcommit_evidence_file(path):
    source = Path(path).read_text(encoding="utf-8")
    records = [json.loads(line.split(": ", 1)[1]) for line in source.splitlines()
               if line.startswith("MCR_EVIDENCE: ")]
    return audit_author_evidence_vector(records)

def claim_mutation_test():
    prompt_path = Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    assert run_claim_gates()["blocked_obligations"] == ["ZAK00-PARENT-06"]
    checks = 0
    for oid, bad_output in [
        ("ZAK00-PARENT-01", CLAIM_OUTPUTS["ZAK00-PARENT-02"]),
        ("ZAK00-PARENT-02", CLAIM_OUTPUTS["ZAK00-PARENT-03"]),
        ("ZAK00-PARENT-03", CLAIM_OUTPUTS["ZAK00-OUTPUT-05"]),
        ("ZAK00-PARENT-06", "WORKER_RETURNS/VMESTYE_ZAK00_V2_MCR_AUTHOR_EXECUTION_20261110_R1/06_FIXED_HIGH_IMPACT_NO_INVERSE_PANEL.md"),
        ("ZAK00-OUTPUT-05", CLAIM_OUTPUTS["ZAK00-PARENT-02"]),
    ]:
        old = _contract_obligations()[oid]
        lines = prompt.splitlines()
        current_lines = []
        for line in lines:
            if line.startswith("MCR_OBLIGATION: "):
                item = json.loads(line.split(": ", 1)[1])
                if item["id"] == oid:
                    item["output"] = bad_output
                    line = "MCR_OBLIGATION: " + json.dumps(item, separators=(",", ":"))
            current_lines.append(line)
        current = "\n".join(current_lines) + "\n"
        assert current != prompt, "mutation not applied " + oid
        try:
            prove_parent_claim(oid, current)
        except (AssertionError, KeyError, ValueError):
            checks += 1
        else:
            raise AssertionError("false-positive wrong-evidence mutant " + oid)
    for oid, artifact in [
        ("ZAK00-PARENT-01", CLAIM_OUTPUTS["ZAK00-PARENT-01"]),
        ("ZAK00-PARENT-01", FLIGHT_MAP),
        ("ZAK00-PARENT-02", CLAIM_OUTPUTS["ZAK00-PARENT-02"]),
        ("ZAK00-PARENT-03", FLIGHT_MAP),
        ("ZAK00-OUTPUT-05", CLAIM_OUTPUTS["ZAK00-OUTPUT-05"]),
    ]:
        try:
            prove_parent_claim(oid, substitutions={artifact: "THIS FILE HAS ONLY VALID SOURCE HASHES AND 182 IDENTITIES"})
        except (AssertionError, KeyError, ValueError):
            checks += 1
        else:
            raise AssertionError("false-positive required-effect-withheld mutant " + oid)
    assert checks == 10
    return {"status": "PASS_10_OF_10_WRONG_OUTPUT_AND_REQUIRED_OUTCOME_MUTANTS_REJECTED",
            "authority_acknowledgment_negative": "BLOCKED_EXACT_DEPENDENCY",
            "not_scientific_acceptance": True}

def self_test():
    s = flight_path(11).read_text(encoding="utf-8")
    assert validate_one(11)["obligations"] == 8
    assert validate_parent()["obligations"] == 24
    for mutant in [
        s.replace("ZAK11-TASK-01", "ZAK11-OMITTED-01", 1),
        s.replace("EPISTEMIC_GRADE_MATRIX.tsv", "EPIS\u00adTEMIC_GRADE_MATRIX.tsv", 1),
        s.replace("ZAK11-OUTPUT-02", "ZAK11-TASK-01", 1),
    ]:
        try:
            validate_one(11, mutant)
        except (AssertionError, KeyError, ValueError):
            pass
        else:
            raise AssertionError("negative mutant passed")
    for mutant in [
        (Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md").read_text(encoding="utf-8").replace("ZAK00-PARENT-01", "ZAK00-LOST-01", 1),
        (Path(__file__).resolve().parent / "01_FULL_COPY_PASTE_LAUNCH.md").read_text(encoding="utf-8").replace("ZAK00-FLIGHT-08", "ZAK00-FLIGHT-03", 1),
    ]:
        try:
            validate_parent(mutant)
        except (AssertionError, KeyError, ValueError):
            pass
        else:
            raise AssertionError("parent completion mutant passed")
    assert claim_mutation_test()["status"].startswith("PASS_10_OF_10")
    assert near_positive_regressions()["status"].startswith("PASS_15_OF_15")
    return "PASS 5/5 original + 10/10 semantic + 15/15 near-positive/forged authority mutants; no independent issuance"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--flight", type=int, choices=range(1, 12))
    p.add_argument("--all", action="store_true")
    p.add_argument("--parent", action="store_true")
    p.add_argument("--claim", choices=list(CLAIM_OUTPUTS))
    p.add_argument("--claim-all", action="store_true")
    p.add_argument("--claim-mutations", action="store_true")
    p.add_argument("--near-positive", action="store_true")
    p.add_argument("--generate-author-evidence")
    p.add_argument("--audit-evidence")
    p.add_argument("--enumerate-expected", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        print(self_test())
        return
    if args.generate_author_evidence:
        print(json.dumps(make_postcommit_author_evidence(args.generate_author_evidence), indent=2))
        return
    if args.audit_evidence:
        print(json.dumps(audit_postcommit_evidence_file(args.audit_evidence), indent=2))
        return
    if args.near_positive:
        print(json.dumps(near_positive_regressions(), indent=2))
        return
    if args.claim_mutations:
        print(json.dumps(claim_mutation_test(), indent=2))
        return
    if args.claim_all:
        print(json.dumps(run_claim_gates(), indent=2))
        return
    if args.claim:
        result = prove_parent_claim(args.claim)
        print(json.dumps(result, indent=2))
        if result["status"] == "BLOCKED_EXACT_DEPENDENCY":
            raise SystemExit(2)
        return
    if args.parent:
        print(json.dumps(validate_parent(), indent=2))
        return
    if args.enumerate_expected:
        assert args.flight
        print("\n".join(required_ids(args.flight)))
        return
    reports = [validate_one(n) for n in (range(1, 12) if args.all else [args.flight])]
    if args.all:
        reports.append(validate_parent())
    print(json.dumps(reports, indent=2))

if __name__ == "__main__":
    main()
