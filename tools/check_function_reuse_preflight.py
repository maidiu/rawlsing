#!/usr/bin/env python3
"""Enforce the *existing* 2026-10-19 build-or-reuse constitution before code.

Not a new capability catalogue, scientific arbiter or claim that a bounded
search proves global absence. Design receipts are per-function, not per test.

Two independent control points:
  preflight CARD.json [--online]  : before deciding/building; consult real
                                    existing owner, G4 and current PR heads.
  changed --base SHA --head SHA [--online] : PR acceptance; fail if any new
                                    implementation or commission was authored
                                    before its receipt was already committed.

Online mode fails closed on stale protected/PR HEAD or inaccessible GitHub.
Offline checks report OFFLINE_CANNOT_CERTIFY_CURRENTNESS, never GREEN.
The CI workflow is not a complete guarantee until branch protection makes
its status REQUIRED and agent launchers load the canonical front door.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any
from urllib.request import Request, urlopen

SCHEMA = "RAWLSING_FUNCTION_REUSE_DECISION@1"
RECEIPTS = "CROSS_HQ_CONTROL_ROOM/FUNCTION_REUSE_DECISIONS"
G4 = "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/FUNCTION_PARITY.jsonl"
LAW = "CROSS_HQ_CONTROL_ROOM/MISSING_FUNCTION_DISCOVERY_USER_CHECK_AND_BUILD_OR_REUSE_CONSTITUTION_R1.md"
PROTECTED_BRANCH = "integration/pre-main-reconciliation-r1"
DISPOSITIONS = {
    "REUSE_EXISTING", "EXTEND_EXISTING", "RECOVER_EXISTING",
    "NEW_AFTER_DOCUMENTED_GAP",
}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SAFE_ID = re.compile(r"^[A-Z0-9][A-Z0-9_-]{4,99}$")
CHECKABLE_TEXT = {".md", ".txt", ".yml", ".yaml", ".json", ".jsonl"}
MIN_DELTA = 36


class ReusePreflightError(ValueError):
    pass


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ReusePreflightError(code)


def run_git(root: Path, *args: str) -> str:
    p = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, check=False,
    )
    require(p.returncode == 0, "GIT_REQUIRED:" + " ".join(args) + ":" + p.stderr[:200])
    return p.stdout.strip()


def safe_path(root: Path, name: str) -> Path:
    require(type(name) is str and bool(name), "SOURCE_PATH_REQUIRED")
    p = PurePosixPath(name)
    require(not p.is_absolute() and ".." not in p.parts
            and "\\" not in name and name == p.as_posix(),
            "SOURCE_PATH_UNSAFE")
    target = (root / name).resolve()
    require(target.is_relative_to(root.resolve()), "SOURCE_PATH_ESCAPE")
    return target


def nonempty(value: Any, label: str, *, minimum: int = 1) -> str:
    require(type(value) is str and len(value.strip()) >= minimum,
            label + "_MUST_BE_SUBSTANTIVE")
    return value.strip()


def _git_blob(root: Path, name: str) -> str:
    p = safe_path(root, name)
    require(p.is_file(), "MISSING_INHERITED_SOURCE:" + name)
    return run_git(root, "hash-object", name)


def _symbol_exists(path: Path, symbol: str) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise ReusePreflightError("SOURCE_AST_CANNOT_BE_READ:" + str(path)) from exc
    # This is a *symbol presence* witness, not behavior/equivalence proof.
    def child_match(nodes: list[ast.stmt], parts: list[str]) -> bool:
        if not parts:
            return True
        for node in nodes:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == parts[0]:
                if len(parts) == 1:
                    return True
                if isinstance(node, ast.ClassDef):
                    return child_match(node.body, parts[1:])
        return False
    return child_match(tree.body, symbol.split("."))


def _parity_ids(root: Path) -> set[str]:
    path = safe_path(root, G4)
    require(path.is_file(), "G4_PARITY_MISSING")
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            if "obligation_id" in record:
                ids.add(record["obligation_id"])
    return ids


def github_get(path: str, token: str) -> Any:
    require(token != "", "GITHUB_TOKEN_REQUIRED_FOR_CURRENTNESS")
    request = Request(
        "https://api.github.com/repos/maidiu/rawlsing/" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "User-Agent": "rawlsing-function-reuse-stopoff-r1",
        },
    )
    try:
        with urlopen(request, timeout=12) as response:
            return json.load(response)
    except Exception as exc:
        raise ReusePreflightError("LIVE_CURRENTNESS_QUERY_FAILED:" + path + ":" + str(exc)) from exc


def validate_card(root: Path, card: dict[str, Any], *, online: bool) -> dict[str, Any]:
    require(type(card) is dict and card.get("schema") == SCHEMA,
            "INVALID_FUNCTION_REUSE_RECEIPT_SCHEMA")
    require(SAFE_ID.fullmatch(str(card.get("decision_id", ""))) is not None,
            "INVALID_DECISION_ID")
    require(card.get("stage") == "BEFORE_IMPLEMENTATION",
            "BEFORE_IMPLEMENTATION_RECEIPT_REQUIRED")
    require(card.get("disposition") in DISPOSITIONS,
            "NO_UNRECONCILED_OR_HOLD_DISPOSITION_CAN_LICENSE_BUILD")
    require(HEX40.fullmatch(str(card.get("protected_cut", ""))) is not None,
            "PROTECTED_CUT_REQUIRED")
    law = card.get("governing_law")
    parity = card.get("g4_parity")
    require(type(law) is dict and law.get("path") == LAW,
            "EXISTING_OCTOBER_LAW_MUST_BE_CONSULTED")
    require(type(parity) is dict and parity.get("path") == G4,
            "EXISTING_G4_FUNCTION_PARITY_MUST_BE_CONSULTED")
    for obj, label in [(law, "GOVERNING_LAW"), (parity, "G4_PARITY")]:
        require(HEX40.fullmatch(str(obj.get("blob", ""))) is not None,
                label + "_SOURCE_BLOB_REQUIRED")
        require(_git_blob(root, obj["path"]) == obj["blob"],
                label + "_STALE_OR_UNREAD_SOURCE")
    ids = parity.get("examined_ids")
    require(type(ids) is list and ids and all(type(x) is str for x in ids),
            "G4_SCOPED_IDS_REQUIRED")
    known_ids = _parity_ids(root)
    require(all(i in known_ids for i in ids), "G4_FALSE_OR_UNVERIFIED_PARITY_ID")
    nonempty(parity.get("function_relationship"), "G4_RELATIONSHIP", minimum=MIN_DELTA)

    function = card.get("function")
    require(type(function) is dict, "FUNCTION_TRANSFORMATION_REQUIRED")
    for key in ("inputs", "operation", "outputs", "first_consumer", "real_gap"):
        nonempty(function.get(key), "FUNCTION_" + key.upper(), minimum=MIN_DELTA)
    require(type(card.get("search_scope")) is dict, "BOUNDED_SEARCH_SCOPE_REQUIRED")
    for key in ("current_code", "historical_and_g4", "active_development", "uninspected"):
        nonempty(card["search_scope"].get(key), key.upper(), minimum=20)
    owners = card.get("existing_candidates")
    require(type(owners) is list and owners,
            "EXISTING_OWNER_CANDIDATES_REQUIRED")
    for candidate in owners:
        require(type(candidate) is dict, "OWNER_RECORD_REQUIRED")
        path = nonempty(candidate.get("path"), "OWNER_PATH")
        sha = nonempty(candidate.get("blob"), "OWNER_BLOB")
        require(HEX40.fullmatch(sha) is not None
                and _git_blob(root, path) == sha,
                "OWNER_SOURCE_NOT_CURRENT:" + path)
        kind = candidate.get("kind")
        require(kind in ("python_symbol", "text_contains"),
                "OWNER_INSPECTION_KIND_INVALID")
        source = safe_path(root, path)
        if kind == "python_symbol":
            symbol = nonempty(candidate.get("symbol"), "OWNER_SYMBOL")
            require(source.suffix == ".py" and _symbol_exists(source, symbol),
                    "INHERITED_SYMBOL_NOT_FOUND:" + path + ":" + symbol)
        else:
            needle = nonempty(candidate.get("needle"), "OWNER_TEXT_NEEDLE", minimum=12)
            require(source.suffix in CHECKABLE_TEXT
                    and needle in source.read_text(encoding="utf-8"),
                    "INHERITED_CARRIER_NOT_FOUND:" + path)
        nonempty(candidate.get("difference"), "OWNER_DIFFERENCE", minimum=20)
        nonempty(candidate.get("role"), "OWNER_ROLE", minimum=8)

    targets = card.get("implementation_targets")
    require(type(targets) is list and targets and len(targets) == len(set(targets)),
            "EXACT_IMPLEMENTATION_TARGETS_REQUIRED")
    for target in targets:
        require(type(target) is str and target == PurePosixPath(target).as_posix(),
                "IMPLEMENTATION_TARGET_PATH_INVALID")
        safe_path(root, target)  # file may not exist: a true prebuild record
    consumer = card.get("first_consumer")
    require(type(consumer) is dict, "ACTUAL_FIRST_CONSUMER_REQUIRED")
    cp = nonempty(consumer.get("path"), "FIRST_CONSUMER_PATH")
    require(safe_path(root, cp).is_file()
            and nonempty(consumer.get("needle"), "FIRST_CONSUMER_NEEDLE", minimum=12)
            in safe_path(root, cp).read_text(encoding="utf-8"),
            "FIRST_CONSUMER_CARRIER_NOT_FOUND")
    nonempty(consumer.get("expected_effect"), "FIRST_CONSUMER_EFFECT", minimum=30)
    nonempty(card.get("positive_proof"), "POSITIVE_PROOF", minimum=30)
    nonempty(card.get("negative_proof"), "NEGATIVE_PROOF", minimum=30)
    nonempty(card.get("user_answer"), "USER_CONSULTATION_EVIDENCE", minimum=20)
    nonempty(card.get("owner"), "DECISION_OWNER", minimum=20)
    nonempty(card.get("authority_limits"), "AUTHORITY_LIMITS", minimum=20)

    heads = card.get("active_pr_heads")
    require(type(heads) is list, "ACTIVE_PR_SEARCH_RESULTS_REQUIRED")
    for record in heads:
        require(type(record) is dict
                and type(record.get("number")) is int
                and record["number"] > 0
                and HEX40.fullmatch(str(record.get("head", ""))) is not None,
                "ACTIVE_PR_EXACT_HEAD_REQUIRED")
        nonempty(record.get("relevance"), "ACTIVE_PR_RELEVANCE", minimum=20)
    if online:
        token = os.environ.get("GITHUB_TOKEN", "")
        actual_protected = github_get(
            "branches/" + PROTECTED_BRANCH.replace("/", "%2F"), token
        )["commit"]["sha"]
        require(card["protected_cut"] == actual_protected,
                "PROTECTED_CODE_CUT_CHANGED__RECONSULT_BEFORE_BUILD")
        for item in heads:
            actual = github_get("pulls/" + str(item["number"]), token)["head"]["sha"]
            require(item["head"] == actual,
                    "ACTIVE_PR_HEAD_CHANGED__RECONSULT_BEFORE_BUILD:" + str(item["number"]))
    return {
        "decision_id": card["decision_id"],
        "checked_owners": len(owners),
        "checked_g4_function_ids": len(ids),
        "checked_active_prs": len(heads),
        "targets": len(targets),
        "state": "SOURCE_CHECKS_CURRENT__SEMANTIC_REUSE_REVIEW_STILL_REQUIRED"
        if online else "OFFLINE_SOURCE_CHECKS_ONLY__CURRENTNESS_NOT_CERTIFIED",
    }


def production_target(name: str) -> bool:
    p = PurePosixPath(name)
    if name.startswith("rawlsing_next/") and p.suffix == ".py":
        return not ("tests" in p.parts or p.name.startswith("test_"))
    if name.startswith("data/ddm_build_copy/") and p.suffix == ".py":
        return not ("tests" in p.parts or p.name.startswith("test_"))
    if name.startswith("tools/") and p.suffix == ".py":
        return not p.name.startswith("test_")
    if name.startswith("CROSS_HQ_CONTROL_ROOM/") and p.suffix == ".py":
        return not p.name.startswith("test_")
    if name.startswith("WORKER_COMMISSIONS/") and p.suffix in (".md", ".txt"):
        return True
    if name.startswith(".github/workflows/") and p.suffix in (".yml", ".yaml"):
        return True
    return False


def load_receipts(root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    folder = safe_path(root, RECEIPTS)
    require(folder.is_dir(), "NO_FUNCTION_REUSE_RECEIPT_DIRECTORY")
    ret: dict[str, tuple[str, dict[str, Any]]] = {}
    for file in sorted(folder.glob("*.json")):
        card = json.loads(file.read_text(encoding="utf-8"))
        for target in card.get("implementation_targets", []):
            require(target not in ret, "CONFLICTING_FUNCTION_REUSE_OWNER:" + target)
            ret[target] = (file.relative_to(root).as_posix(), card)
    return ret


def first_change_commit(root: Path, base: str, head: str, target: str) -> str:
    commits = run_git(root, "rev-list", "--reverse", "--first-parent", base + ".." + head).splitlines()
    for commit in commits:
        p = run_git(root, "diff-tree", "--no-commit-id", "--name-only", "-r", commit)
        if target in p.splitlines():
            return commit
    raise ReusePreflightError("FIRST_IMPLEMENTATION_COMMIT_UNDISCOVERABLE:" + target)


def verify_receipt_precedes_code(
    root: Path, base: str, head: str, name: str, cardpath: str, current: dict[str, Any]
) -> None:
    first = first_change_commit(root, base, head, name)
    parent = run_git(root, "rev-parse", first + "^")
    p = subprocess.run(
        ["git", "-C", str(root), "show", parent + ":" + cardpath],
        capture_output=True, text=True, check=False,
    )
    require(p.returncode == 0,
            "RECEIPT_COMMITTED_TOO_LATE__CARD_MUST_PRECEDE_CODE:" + name)
    prior = json.loads(p.stdout)
    require(prior.get("schema") == SCHEMA
            and prior.get("stage") == "BEFORE_IMPLEMENTATION"
            and name in prior.get("implementation_targets", [])
            and prior.get("decision_id") == current["decision_id"]
            and prior.get("disposition") == current["disposition"],
            "PREBUILD_DECISION_MISSING_AT_FIRST_CODE_PARENT:" + name)


def check_changed(root: Path, base: str, head: str, online: bool) -> dict[str, Any]:
    require(HEX40.fullmatch(base) and HEX40.fullmatch(head),
            "EXACT_GIT_DIFF_HEADS_REQUIRED")
    paths = run_git(root, "diff", "--diff-filter=ACMRT", "--name-only",
                    base, head, "--").splitlines()
    changed = [p for p in paths if production_target(p)]
    receipts = load_receipts(root)
    results = []
    validated_ids: dict[str, dict[str, Any]] = {}
    for path in changed:
        require(path in receipts, "MISSING_PREBUILD_OWNER_REUSE_RECEIPT:" + path)
        cardpath, card = receipts[path]
        if card["decision_id"] not in validated_ids:
            validated_ids[card["decision_id"]] = validate_card(root, card, online=online)
        verify_receipt_precedes_code(root, base, head, path, cardpath, card)
        results.append({"path": path, "receipt": cardpath,
                        "decision_id": card["decision_id"]})
    return {
        "state": "SOURCE_PREFLIGHTS_VERIFIED__INDEPENDENT_SEMANTIC_REVIEW_REQUIRED"
        if online else "OFFLINE_ONLY_NOT_CURRENTNESS_PROOF",
        "checked_implementation_files": len(changed),
        "decisions": list(validated_ids.values()),
        "files": results,
    }


def self_test() -> None:
    assert production_target("rawlsing_next/module.py")
    assert production_target("tools/check_new.py")
    assert production_target("WORKER_COMMISSIONS/candidate.md")
    assert production_target(".github/workflows/new.yml")
    assert not production_target("rawlsing_next/tests/test_module.py")
    assert not production_target("tests/test_gate.py")
    assert not production_target("PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md")
    assert not production_target("README.md")
    assert not production_target("../bad.py")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="mode", required=True)
    pre = sub.add_parser("preflight")
    pre.add_argument("card")
    pre.add_argument("--online", action="store_true")
    changed = sub.add_parser("changed")
    changed.add_argument("--base", required=True)
    changed.add_argument("--head", required=True)
    changed.add_argument("--online", action="store_true")
    sub.add_parser("self-test")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.mode == "self-test":
            self_test()
            result = {"state": "LOCAL_MECHANICAL_SELF_TEST_PASS_NOT_SEMANTIC_PROOF"}
        elif args.mode == "preflight":
            path = safe_path(root, args.card)
            require(path.is_file(), "PREBUILD_CARD_MISSING")
            result = validate_card(root, json.loads(path.read_text(encoding="utf-8")),
                                   online=args.online)
        else:
            result = check_changed(root, args.base, args.head, args.online)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ReusePreflightError, ValueError, json.JSONDecodeError) as exc:
        print("FUNCTION_REUSE_STOP_OFF_HOLD: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
