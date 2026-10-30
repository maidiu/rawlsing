#!/usr/bin/env python3
"""Offline schema, locator and custody consistency only.

This validator cannot verify a Mac UI title, a provider session URL, a user
identity or source authority. It can reject structurally false attribution,
detect rewritten historical rows when a prior registry snapshot is supplied,
and verify that a published return SHA actually exists in a local Git clone.
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import re
import subprocess
import sys
import tempfile

P = pathlib.Path(__file__).resolve().parent
REPO = next((parent for parent in (P, *P.parents) if (parent / ".git").exists()),
            P.parent)
SHA = re.compile(r"^[a-f0-9]{40}$")
SCHEMA = "CROSS_HQ_SESSION_LOCATOR_REGISTRY@1"
POLICY = "SESSION_LOCATOR_INTEGRITY@2"
DEV = {"oldMac", "mainMac", "BROWSER", "OTHER_VERIFIED", "UNKNOWN"}
HAR = {"Codex", "OpenCode", "DeepSeek-Harness", "Browser", "OTHER_VERIFIED",
       "UNKNOWN"}
STATUS = {"SEALED_NOT_LAUNCHED", "ACTIVE_VERIFIED", "RETURNED", "HOLD"}
LOCATOR_TYPE = {"APP_TITLE", "APP_SESSION_ID", "APP_URL",
                "WORKTREE_AND_OPERATOR_NOTE", "UNKNOWN"}
CONFIRMER = {"USER", "WORKER", "REVIEWER", "UNVERIFIED"}
MACHINE_CLAIM = {"SELF_REPORTED", "SELF_REPORTED_BROWSER_CONTEXT", "VERIFIED",
                 "UNVERIFIED"}
LOCATOR_STATUS = {"APP_TITLE_AND_SESSION_ID_VERIFIED", "APP_TITLE_VERIFIED",
                  "APP_SESSION_ID_VERIFIED", "WORKTREE_AND_OPERATOR_NOTE",
                  "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
                  "UNKNOWN"}
SESSION_EVIDENCE = {"INSPECTED_IN_APP", "OPERATOR_SUPPLIED", "SUGGESTED",
                    "UNKNOWN"}
CONFIRM_EVIDENCE = {"USER_DIRECT", "USER_CONFIRMED", "OPERATOR_SELF_REPORT",
                    "REVIEWER_READBACK", "NONE", "UNVERIFIED"}
AUTHORITY_KEYS = {"source_authority", "adoption", "authority_grant",
                  "native_authority", "source_grant", "merge_authority"}
REQUIRED = (
    "registry_id", "revision", "commission_id", "branch", "status", "device",
    "device_evidence", "harness", "agent_name", "agent_id", "agent_role",
    "model_id", "reasoning_effort_requested", "reasoning_effort_verified",
    "session_name", "session_locator_type", "return_sha", "return_directory",
    "confirmed_by", "machine_claim", "locator_status",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _present(value):
    return value is not None and value != ""


def check_sha_readback(repo, sha, branch=None, require_branch=False):
    """Return an explicit readback status, never a bare format pass."""
    if not repo:
        return {"status": "UNAVAILABLE", "detail": "no local repository supplied"}
    repo_path = pathlib.Path(repo)
    if not (repo_path / ".git").exists():
        return {"status": "REPO_NOT_FOUND", "detail": str(repo_path)}
    probe = subprocess.run(
        ["git", "-C", str(repo_path), "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True, text=True)
    if probe.returncode != 0:
        return {"status": "NOT_LOCAL", "detail": probe.stderr.strip()}
    if not branch:
        return {"status": "LOCAL_UNBOUND", "detail": "commit exists; no branch supplied"}
    ref = None
    for candidate in (f"refs/heads/{branch}", f"refs/remotes/origin/{branch}"):
        found = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--verify", candidate],
            capture_output=True, text=True)
        if found.returncode == 0:
            ref = found.stdout.strip()
            break
    if ref is None:
        return {"status": "BRANCH_REF_NOT_LOCAL", "detail": str(branch)}
    ancestor = subprocess.run(
        ["git", "-C", str(repo_path), "merge-base", "--is-ancestor", sha, ref],
        capture_output=True, text=True)
    if ancestor.returncode == 0:
        return {"status": "VERIFIED", "ref": ref}
    return {"status": "NOT_ON_BRANCH", "ref": ref}


def check_append_only(previous, current):
    """All prior rows must remain an exact ordered prefix; new rows append."""
    errors = []
    if not isinstance(previous, dict) or not isinstance(current, dict):
        return ["BASELINE_INVALID"]
    if previous.get("schema") != current.get("schema"):
        errors.append("BASELINE_SCHEMA_MISMATCH")
    old = previous.get("records")
    new = current.get("records")
    if not isinstance(old, list) or not isinstance(new, list):
        return errors + ["BASELINE_RECORDS_INVALID"]
    if len(new) < len(old):
        errors.append("HISTORICAL_ROWS_TRUNCATED")
    for index, row in enumerate(old):
        if index >= len(new):
            errors.append(f"row{index}:HISTORICAL_ROW_MISSING")
        elif canonical(row) != canonical(new[index]):
            errors.append(f"row{index}:HISTORICAL_ROW_REWRITTEN")
    return errors


def _nested_session(value, prefix, errors):
    if value is None:
        return
    if isinstance(value, str):
        if not value.strip():
            errors.append(prefix + "ORIGINAL_SESSION_EMPTY_REFERENCE")
        return
    if not isinstance(value, dict):
        errors.append(prefix + "ORIGINAL_SESSION_NOT_OBJECT")
        return
    if "device" in value and value["device"] not in DEV:
        errors.append(prefix + "ORIGINAL_DEVICE")
    if "harness" in value and value["harness"] not in HAR:
        errors.append(prefix + "ORIGINAL_HARNESS")
    if "return_sha" in value and value["return_sha"] is not None:
        if not SHA.fullmatch(str(value["return_sha"])):
            errors.append(prefix + "ORIGINAL_RETURN_SHA")
    if "session_locator_type" in value:
        kind = value["session_locator_type"]
        if kind not in LOCATOR_TYPE:
            errors.append(prefix + "ORIGINAL_LOCATOR_TYPE")
        if kind == "UNKNOWN" and (
                _present(value.get("session_name")) or
                _present(value.get("session_id")) or
                _present(value.get("session_url"))):
            errors.append(prefix + "ORIGINAL_UNKNOWN_WITH_FIELDS")
    if _present(value.get("session_name")) and value.get("session_name_evidence") in (
            None, "SUGGESTED", "UNKNOWN"):
        errors.append(prefix + "ORIGINAL_TITLE_EVIDENCE")


def _check_locator_type(row, prefix, errors):
    kind = row.get("session_locator_type")
    name = row.get("session_name")
    session_id = row.get("session_id")
    url = row.get("session_url")
    if kind not in LOCATOR_TYPE:
        errors.append(prefix + "LOCATOR_TYPE")
        return
    if kind == "UNKNOWN":
        if _present(name) or _present(session_id) or _present(url):
            errors.append(prefix + "LOCATOR_TYPE_UNKNOWN_WITH_FIELDS")
    elif kind == "APP_TITLE":
        if not _present(name):
            errors.append(prefix + "LOCATOR_TYPE_TITLE_MISSING")
    elif kind == "APP_SESSION_ID":
        if not _present(session_id):
            errors.append(prefix + "LOCATOR_TYPE_SESSION_ID_MISSING")
    elif kind == "APP_URL":
        if not _present(url):
            errors.append(prefix + "LOCATOR_TYPE_URL_MISSING")
        elif not str(url).startswith(("https://", "http://")):
            errors.append(prefix + "LOCATOR_URL_SCHEME")
    elif kind == "WORKTREE_AND_OPERATOR_NOTE":
        if not _present(row.get("worktree_path")) and not _present(row.get("notes")):
            errors.append(prefix + "LOCATOR_TYPE_WORKTREE_MISSING")
    if _present(url) and not str(url).startswith(("https://", "http://")):
        errors.append(prefix + "SESSION_URL_SCHEME")


def _check_title(row, prefix, errors):
    name = row.get("session_name")
    evidence = row.get("session_name_evidence")
    suggested = row.get("suggested_session_name")
    if _present(name):
        if not _text(name):
            errors.append(prefix + "EMPTY_TITLE")
        if row.get("confirmed_by") == "UNVERIFIED":
            errors.append(prefix + "UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED")
        if evidence is None:
            errors.append(prefix + "SESSION_NAME_EVIDENCE_MISSING")
        elif evidence not in SESSION_EVIDENCE:
            errors.append(prefix + "SESSION_NAME_EVIDENCE")
        elif evidence in {"SUGGESTED", "UNKNOWN"}:
            errors.append(prefix + "SESSION_NAME_EVIDENCE_NOT_OBSERVED")
        if row.get("session_locator_type") == "UNKNOWN":
            errors.append(prefix + "TITLE_WITH_UNKNOWN_LOCATOR_TYPE")
    elif evidence not in (None, "UNKNOWN"):
        errors.append(prefix + "TITLE_EVIDENCE_WITHOUT_TITLE")
    if _present(suggested) and name == suggested and evidence in (
            None, "SUGGESTED", "UNKNOWN"):
        errors.append(prefix + "PROPOSED_TITLE_AS_OBSERVED")


def _check_locator_status(row, prefix, errors):
    status = row.get("locator_status")
    if status not in LOCATOR_STATUS:
        errors.append(prefix + "LOCATOR_STATUS")
        return
    name = row.get("session_name")
    session_id = row.get("session_id")
    evidence = row.get("session_name_evidence")
    if status == "APP_TITLE_AND_SESSION_ID_VERIFIED":
        if not _present(name) or not _present(session_id):
            errors.append(prefix + "VERIFIED_LOCATOR_FIELDS_MISSING")
        if not _present(evidence):
            errors.append(prefix + "VERIFIED_LOCATOR_EVIDENCE_MISSING")
        if row.get("confirmed_by") == "UNVERIFIED":
            errors.append(prefix + "VERIFIED_LOCATOR_UNCONFIRMED")
    elif status == "APP_TITLE_VERIFIED":
        if not _present(name) or not _present(evidence):
            errors.append(prefix + "VERIFIED_TITLE_FIELDS_MISSING")
    elif status == "APP_SESSION_ID_VERIFIED":
        if not _present(session_id):
            errors.append(prefix + "VERIFIED_SESSION_ID_MISSING")
    elif status == "WORKTREE_AND_OPERATOR_NOTE":
        if not _present(row.get("worktree_path")) and not _present(row.get("notes")):
            errors.append(prefix + "VERIFIED_WORKTREE_MISSING")
    elif status == "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION":
        if _present(name) or _present(session_id) or _present(row.get("session_url")):
            errors.append(prefix + "NOT_FOUND_WITH_OBSERVED_FIELDS")


def _check_confirmation(row, prefix, errors):
    confirmer = row.get("confirmed_by")
    evidence = row.get("confirmation_evidence")
    if confirmer not in CONFIRMER:
        errors.append(prefix + "CONFIRMED_BY")
        return
    if confirmer == "USER":
        if evidence not in {"USER_DIRECT", "USER_CONFIRMED"}:
            errors.append(prefix + "USER_CONFIRMATION_EVIDENCE")
        if row.get("device") == "UNKNOWN":
            errors.append(prefix + "USER_CONFIRMATION_WITHOUT_DEVICE")
        device_evidence = str(row.get("device_evidence", "")).lower()
        if "user" not in device_evidence and "confirm" not in device_evidence:
            errors.append(prefix + "USER_CONFIRMATION_WITHOUT_EVIDENCE")
    elif confirmer == "REVIEWER":
        if evidence != "REVIEWER_READBACK":
            errors.append(prefix + "REVIEWER_CONFIRMATION_EVIDENCE")
    elif confirmer == "UNVERIFIED":
        if row.get("machine_claim") != "UNVERIFIED":
            errors.append(prefix + "UNVERIFIED_WITH_MACHINE_CLAIM")
        if row.get("status") not in {"SEALED_NOT_LAUNCHED", "HOLD"}:
            errors.append(prefix + "UNVERIFIED_WITH_RETURN_STATUS")
    elif confirmer == "WORKER":
        if evidence in {"USER_DIRECT", "USER_CONFIRMED", "REVIEWER_READBACK"}:
            errors.append(prefix + "WORKER_CLAIMS_HIGHER_CONFIRMATION")


def _check_machine(row, prefix, errors):
    claim = row.get("machine_claim")
    device = row.get("device")
    evidence = str(row.get("device_evidence", "")).lower()
    if claim not in MACHINE_CLAIM:
        errors.append(prefix + "MACHINE_CLAIM")
    if claim == "VERIFIED":
        if device not in {"oldMac", "mainMac", "OTHER_VERIFIED"}:
            errors.append(prefix + "VERIFIED_CLAIM_WITHOUT_DEVICE")
        if not any(token in evidence for token in
                   ("scutil", "hostname", "user", "confirm", "verified",
                    "local-machine-name")):
            errors.append(prefix + "VERIFIED_CLAIM_WITHOUT_EVIDENCE")
    if claim == "UNVERIFIED" and device != "UNKNOWN":
        errors.append(prefix + "UNVERIFIED_CLAIM_WITH_DEVICE")
    if device in {"oldMac", "mainMac"}:
        if evidence in {"local_mac_reported_which_machine_unverified",
                        "unverified"}:
            errors.append(prefix + "MAC_GUESSED")
        if not any(token in evidence for token in
                   ("scutil", "hostname", "user", "confirm", "verified",
                    "local-machine-name")):
            errors.append(prefix + "MAC_EVIDENCE_WEAK")


def _check_sha(row, prefix, repo, require_sha, require_sha_branch, errors):
    sha = row.get("return_sha")
    if sha is None:
        if row.get("status") == "RETURNED" and not _present(
                row.get("return_sha_resolution")):
            errors.append(prefix + "RETURN_SHA_RESOLUTION_MISSING")
        return
    if not SHA.fullmatch(str(sha)):
        errors.append(prefix + "RETURN_SHA")
        return
    if repo:
        report = check_sha_readback(repo, sha, row.get("branch"),
                                    require_sha_branch)
        if report["status"] == "NOT_LOCAL":
            if require_sha:
                errors.append(prefix + "SHA_NOT_LOCAL")
            else:
                errors.append(prefix + "WARN_SHA_NOT_LOCAL")
        elif report["status"] == "NOT_ON_BRANCH":
            if require_sha_branch:
                errors.append(prefix + "SHA_NOT_ON_DECLARED_BRANCH")
            else:
                errors.append(prefix + "WARN_SHA_NOT_ON_DECLARED_BRANCH")
        elif report["status"] in {"UNAVAILABLE", "REPO_NOT_FOUND",
                                  "BRANCH_REF_NOT_LOCAL", "LOCAL_UNBOUND"}:
            if require_sha or require_sha_branch:
                errors.append(prefix + "SHA_READBACK_" + report["status"])
            else:
                errors.append(prefix + "WARN_SHA_READBACK_" + report["status"])
    elif require_sha:
        errors.append(prefix + "SHA_READBACK_REQUIRED")
    else:
        errors.append(prefix + "WARN_SHA_READBACK_UNAVAILABLE")


def check(obj, previous=None, repo=None, require_sha=False,
          require_sha_branch=False):
    """Return errors; WARN_ prefixed entries are holds, not hard failures."""
    errors = []
    if obj.get("schema") != SCHEMA or not isinstance(obj.get("records"), list):
        return ["INVALID_SCHEMA"]
    if previous is not None:
        errors.extend(check_append_only(previous, obj))
    rows = obj["records"]
    seen_registry = set()
    seen_revision = set()
    latest = {}
    for index, row in enumerate(rows):
        prefix = f"row{index}:"
        if not isinstance(row, dict):
            errors.append(prefix + "NOT_OBJECT")
            continue
        for key in REQUIRED:
            if key not in row:
                errors.append(prefix + "MISSING_" + key)
        registry_id = row.get("registry_id")
        if not _text(registry_id):
            errors.append(prefix + "REGISTRY_ID")
        elif registry_id in seen_registry:
            errors.append(prefix + "DUPLICATE_REGISTRY_ID")
        else:
            seen_registry.add(registry_id)
        commission_id = row.get("commission_id")
        if not _text(commission_id):
            errors.append(prefix + "COMMISSION_ID")
        if not _text(row.get("branch")):
            errors.append(prefix + "BRANCH")
        revision = row.get("revision")
        if not isinstance(revision, int) or revision < 1:
            errors.append(prefix + "REVISION")
        else:
            key = (commission_id, revision)
            if key in seen_revision:
                errors.append(prefix + "DUPLICATE_REVISION")
            seen_revision.add(key)
            previous_revision = latest.get(commission_id, 0)
            if revision != previous_revision + 1:
                errors.append(prefix + "NON_APPEND_REVISION")
            latest[commission_id] = revision
            if revision > 1:
                if (index == 0
                        or rows[index - 1].get("commission_id") != commission_id
                        or row.get("supersedes") != rows[index - 1].get("registry_id")):
                    errors.append(prefix + "SUPERSEDES")
            elif row.get("supersedes") not in (None, ""):
                errors.append(prefix + "SUPERSEDES_ON_FIRST_REVISION")
        if row.get("status") not in STATUS:
            errors.append(prefix + "STATUS")
        if row.get("device") not in DEV:
            errors.append(prefix + "DEVICE")
        if row.get("harness") not in HAR:
            errors.append(prefix + "HARNESS")
        if not _text(row.get("agent_name")):
            errors.append(prefix + "AGENT_NAME")
        if not _text(row.get("agent_role")):
            errors.append(prefix + "AGENT_ROLE")
        if row.get("agent_id") is not None and not isinstance(
                row.get("agent_id"), str):
            errors.append(prefix + "AGENT_ID")
        if "agent_mode" in row and not _text(row.get("agent_mode")) and \
                row.get("agent_mode") not in (None, "UNKNOWN"):
            errors.append(prefix + "AGENT_MODE")
        if not isinstance(row.get("model_id"), str):
            errors.append(prefix + "MODEL_ID")
        if row.get("harness") == "DeepSeek-Harness" and str(
                row.get("model_id", "")).startswith("opencode-go/"):
            errors.append(prefix + "MODEL_CONFUSED_WITH_HARNESS")
        _check_title(row, prefix, errors)
        _check_locator_type(row, prefix, errors)
        _check_locator_status(row, prefix, errors)
        _check_confirmation(row, prefix, errors)
        _check_machine(row, prefix, errors)
        _check_sha(row, prefix, repo, require_sha, require_sha_branch, errors)
        if row.get("sealed_commission_sha") is not None and not SHA.fullmatch(
                str(row["sealed_commission_sha"])):
            errors.append(prefix + "SEALED_COMMISSION_SHA")
        directory = row.get("return_directory")
        if _present(directory):
            text = str(directory)
            if text.startswith("/") or ".." in pathlib.PurePosixPath(text).parts \
                    or not text.startswith("WORKER_RETURNS/"):
                errors.append(prefix + "RETURN_DIRECTORY")
        _nested_session(row.get("original_implementing_session"), prefix, errors)
        for key in AUTHORITY_KEYS:
            if key in row and row[key] not in (
                    False, None, "NONE", "NOT_GRANTED", "false"):
                errors.append(prefix + "LOCATOR_CANNOT_GRANT_AUTHORITY:" + key)
    return errors


def _load_previous(args):
    if args.baseline:
        return json.loads(pathlib.Path(args.baseline).read_text())
    if args.baseline_ref:
        shown = subprocess.run(
            ["git", "-C", str(args.repo or REPO), "show",
             f"{args.baseline_ref}:CROSS_HQ_CONTROL_ROOM/SESSION_LOCATORS.json"],
            capture_output=True, text=True)
        if shown.returncode != 0:
            return None
        return json.loads(shown.stdout)
    return None


def _selftest(obj):
    trials = [
        ("MAC_GUESSED",
         lambda x: x["records"][1].update(device="oldMac")),
        ("MODEL_CONFUSED_WITH_HARNESS",
         lambda x: x["records"][1].update(harness="DeepSeek-Harness")),
        ("DUPLICATE_REVISION",
         lambda x: x["records"].append(copy.deepcopy(x["records"][0]))),
        ("RETURN_SHA",
         lambda x: x["records"][0].update(return_sha="fake")),
        ("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED",
         lambda x: x["records"][0].update(
             session_name="same", suggested_session_name="same",
             confirmed_by="UNVERIFIED")),
        ("AGENT_NAME",
         lambda x: x["records"][0].update(agent_name="")),
    ]
    for required, mutator in trials:
        other = copy.deepcopy(obj)
        mutator(other)
        found = check(other)
        assert any(required in item for item in found), (required, found)
    print("PASS 6 adversarial locator integrity witnesses")

    # G1: historical rewrite / deletion / reorder is a prefix mismatch.
    for name, mutate in (
        ("G1_REWRITE",
         lambda x: x["records"][0].update(device_evidence="rewritten")),
        ("G1_DELETE", lambda x: x["records"].pop(0)),
        ("G1_REORDER", lambda x: x["records"].insert(0, x["records"].pop(1))),
    ):
        other = copy.deepcopy(obj)
        mutate(other)
        found = check(other, previous=obj)
        assert any("HISTORICAL" in item for item in found), (name, found)
    print("PASS G1 historical append-only custody")

    # G1 positive: a legal appended revision after the baseline prefix.
    other = copy.deepcopy(obj)
    base = copy.deepcopy(other["records"][-1])
    other["records"].append({
        **base,
        "registry_id": base["registry_id"] + "-R2",
        "revision": 2,
        "supersedes": base["registry_id"],
        "status": "RETURNED",
        "confirmed_by": "WORKER",
        "machine_claim": "SELF_REPORTED",
        "confirmation_evidence": "OPERATOR_SELF_REPORT",
        "return_sha": None,
        "return_sha_resolution": "external readback after push",
        "locator_status": "SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION",
    })
    assert not [item for item in check(other, previous=obj)
                if "WARN_" not in item], check(other, previous=obj)
    print("PASS legitimate append revision")

    # G2: fabricated observed title without evidence.
    other = copy.deepcopy(obj)
    other["records"][0].update(
        session_name="Fabricated observed title",
        suggested_session_name="different proposed title",
        session_locator_type="APP_TITLE", confirmed_by="WORKER")
    found = check(other)
    assert any("SESSION_NAME_EVIDENCE_MISSING" in item for item in found), found
    print("PASS G2 fabricated observed title")

    # G3: strict locator type.
    other = copy.deepcopy(obj)
    other["records"][0].update(session_locator_type="SCREENSHOT")
    found = check(other)
    assert any("LOCATOR_TYPE" in item for item in found), found
    print("PASS G3 invalid locator type")

    # G4: duplicate registry id.
    other = copy.deepcopy(obj)
    duplicate = copy.deepcopy(other["records"][0])
    duplicate["commission_id"] = "OTHER-COMMISSION"
    duplicate["revision"] = 1
    other["records"].append(duplicate)
    found = check(other)
    assert any("DUPLICATE_REGISTRY_ID" in item for item in found), found
    print("PASS G4 duplicate registry ID")

    # G5: confirmer enum and contradiction.
    other = copy.deepcopy(obj)
    other["records"][0]["confirmed_by"] = "ADMIN"
    found = check(other)
    assert any("CONFIRMED_BY" in item for item in found), found
    other = copy.deepcopy(obj)
    other["records"][0].update(confirmed_by="USER")
    found = check(other)
    assert any("USER_CONFIRMATION_EVIDENCE" in item for item in found), found
    print("PASS G5 bogus confirmation authority")

    # G6: forged valid-format SHA, and a real local commit.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.email",
                        "locator@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(tmp_path), "config", "user.name",
                        "Locator Test"], check=True)
        (tmp_path / "seed.txt").write_text("seed\n")
        subprocess.run(["git", "-C", str(tmp_path), "add", "seed.txt"],
                       check=True)
        subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "seed"],
                       check=True)
        real = subprocess.run(
            ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        single = {"schema": obj["schema"],
                  "records": [copy.deepcopy(obj["records"][0])]}
        branch = single["records"][0]["branch"]
        subprocess.run(["git", "-C", str(tmp_path), "branch", branch],
                       check=True)
        single["records"][0]["return_sha"] = "0" * 40
        found = check(single, repo=tmp_path, require_sha=True)
        assert any("SHA_NOT_LOCAL" in item for item in found), found
        single["records"][0]["return_sha"] = real
        found = check(single, repo=tmp_path, require_sha=True)
        assert not any("SHA_NOT_LOCAL" in item or "SHA_READBACK" in item
                       for item in found), found
    print("PASS G6 forged valid-format SHA")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--repo", default=None)
    parser.add_argument("--baseline", default=None)
    parser.add_argument("--baseline-ref", default=None)
    parser.add_argument("--require-sha", action="store_true")
    parser.add_argument("--require-sha-branch", action="store_true")
    parser.add_argument("--require-baseline", action="store_true")
    args = parser.parse_args(argv)
    if args.repo is None:
        args.repo = str(REPO)
    obj = json.loads((P / "SESSION_LOCATORS.json").read_text())
    previous = _load_previous(args)
    if previous is None and args.require_baseline:
        print("FAIL BASELINE_REQUIRED")
        return 1
    issues = check(obj, previous=previous, repo=args.repo,
                   require_sha=args.require_sha,
                   require_sha_branch=args.require_sha_branch)
    hard = [item for item in issues if "WARN_" not in item]
    warnings = [item for item in issues if "WARN_" in item]
    if hard:
        print("FAIL", hard)
        return 1
    print("PASS", len(obj["records"]), "locators, no host/session identity or authority attested")
    if previous is None:
        print("HOLD append-only baseline unavailable; supply --baseline or --baseline-ref")
    else:
        print("PASS append-only baseline prefix preserved")
    if warnings:
        print("HOLD", warnings)
    if args.selftest:
        return _selftest(obj)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
