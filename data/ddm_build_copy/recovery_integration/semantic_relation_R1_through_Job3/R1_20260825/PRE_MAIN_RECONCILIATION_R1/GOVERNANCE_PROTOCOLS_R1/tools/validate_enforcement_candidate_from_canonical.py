#!/usr/bin/env python3
"""Fail-closed governance-enforcement predecessor gate.

SECURITY PROPERTY:
This file is intentionally self-contained and must be launched under Python
isolated + no-site + safe-path mode. Before importing any shadowable module it
checks the interpreter flags using only the built-in `sys` module. After that
barrier it imports only Python standard-library modules, imports no Rawlsing
helper module, and reads every repository governance dependency it trusts from
the immutable LIVE CANONICAL predecessor commit via
`git show <live>:<path>`.

Required invocation shape:
    python3 -I -S validate_enforcement_candidate_from_canonical.py ...

A normal `python3 script.py` or direct shebang launch MUST fail before argparse,
csv, json, pathlib, subprocess, typing, or any other path-resolved module is
imported. Candidate worktree modules, PYTHONPATH, user-site/sitecustomize, local
sibling modules, schemas, manifests, and helpers are therefore outside the
trusted execution dependency closure.
"""
from __future__ import annotations

# `sys` is a built-in module. It is the only runtime import permitted before the
# isolation barrier because it cannot be shadowed by a repository-local sys.py.
import sys

_required_flags = {
    "isolated": bool(getattr(sys.flags, "isolated", 0)),
    "ignore_environment": bool(getattr(sys.flags, "ignore_environment", 0)),
    "no_user_site": bool(getattr(sys.flags, "no_user_site", 0)),
    "no_site": bool(getattr(sys.flags, "no_site", 0)),
    "safe_path": bool(getattr(sys.flags, "safe_path", False)),
}
if not all(_required_flags.values()):
    sys.stderr.write(
        "FAIL_PYTHON_EXECUTION_NOT_ISOLATED: invoke with `python3 -I -S "
        "validate_enforcement_candidate_from_canonical.py ...`; "
        + ",".join(f"{k}={int(v)}" for k, v in _required_flags.items())
        + "\n"
    )
    raise SystemExit(97)

# Only after the fail-closed interpreter barrier may normal stdlib imports occur.
import argparse
import csv
import json
import re
import subprocess
from pathlib import Path
from typing import Any

CANONICAL_REF = "integration/pre-main-reconciliation-r1"
ROOT_REL = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1"
GOV_REL = ROOT_REL + "/GOVERNANCE_PROTOCOLS_R1"
SELF_REL = GOV_REL + "/tools/validate_enforcement_candidate_from_canonical.py"
MANIFEST_REL = GOV_REL + "/GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv"
AUTH_SCHEMA_REL = GOV_REL + "/HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json"
RESULT_SCHEMA_REL = GOV_REL + "/HOSTILE_AUDIT_RESULT_SCHEMA_R1.json"
AUTH_PREFIX = ROOT_REL + "/AUDIT_AUTHORIZATIONS/"
IMMUTABLE_REF_RE = re.compile(r"^(?P<sha>[0-9a-f]{40}):(?P<path>[^\n]+)$")

SCRIPT_PATH = Path(__file__).resolve()

def _git_cwd() -> Path:
    p = subprocess.run(["git", "-C", str(SCRIPT_PATH.parent), "rev-parse", "--show-toplevel"], text=True, capture_output=True)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError("repository root unresolved")
    return Path(p.stdout.strip())

REPO = _git_cwd()

def _path_under_repo(entry: str) -> bool:
    if not entry:
        return True
    try:
        p = Path(entry).resolve()
        return p == REPO or REPO in p.parents
    except Exception:
        return True

# Defense in depth: -I -S -P semantics should already keep the script directory,
# cwd, user-site, and PYTHONPATH entries out of sys.path. Refuse execution if any
# active import-search entry nevertheless resolves inside the repository.
REPO_IMPORT_PATHS = [x for x in sys.path if _path_under_repo(x)]
if REPO_IMPORT_PATHS:
    sys.stderr.write(
        "FAIL_CANDIDATE_CONTROLLED_IMPORT_PATH_PRESENT: "
        + repr(REPO_IMPORT_PATHS)
        + "\n"
    )
    raise SystemExit(98)

def git(*args: str) -> tuple[bool, str]:
    try:
        p = subprocess.run(["git", "-C", str(REPO), *args], text=True, capture_output=True, timeout=15)
        return p.returncode == 0, p.stdout.strip()
    except Exception:
        return False, ""

def git_lines(*args: str) -> tuple[bool, list[str]]:
    ok, out = git(*args)
    return ok, [x for x in out.splitlines() if x]

def live_canonical() -> tuple[bool, str, str]:
    lo, ls = git("rev-parse", "--verify", f"refs/heads/{CANONICAL_REF}")
    ro, rs = git("rev-parse", "--verify", f"refs/remotes/origin/{CANONICAL_REF}")
    if lo and ro and ls != rs:
        return False, "", "DIVERGED"
    if lo:
        return True, ls, "LOCAL" + ("+REMOTE_MATCH" if ro else "")
    if ro:
        return True, rs, "REMOTE_ONLY"
    return False, "", "UNRESOLVED"

def canonical_text(live: str, rel: str) -> tuple[bool, str]:
    """Read trusted dependency bytes from exact canonical predecessor tree."""
    return git("show", f"{live}:{rel}")

def canonical_json(live: str, rel: str) -> Any:
    ok, text = canonical_text(live, rel)
    if not ok:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None

def immutable_json(ref: str) -> Any:
    m = IMMUTABLE_REF_RE.fullmatch(ref or "")
    if not m:
        return None
    target = f"{m.group('sha')}:{m.group('path')}"
    ok, _ = git("cat-file", "-e", target)
    if not ok:
        return None
    ok, text = git("show", target)
    if not ok:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None

def split_ref(v: str) -> tuple[str, str]:
    m = IMMUTABLE_REF_RE.fullmatch(v or "")
    return (m.group("sha"), m.group("path")) if m else ("", "")

def branch_tip(name: str) -> tuple[bool, str, str]:
    lo, ls = git("rev-parse", "--verify", f"refs/heads/{name}")
    ro, rs = git("rev-parse", "--verify", f"refs/remotes/origin/{name}")
    if lo and ro and ls != rs:
        return False, "", "DIVERGED"
    if lo:
        return True, ls, "LOCAL" + ("+REMOTE_MATCH" if ro else "")
    if ro:
        return True, rs, "REMOTE_ONLY"
    return False, "", "UNRESOLVED"

def direct_child_of(commit: str, parent: str) -> bool:
    ok, out = git("rev-list", "--parents", "-n", "1", commit)
    parts = out.split() if ok else []
    return len(parts) == 2 and parts[0] == commit and parts[1] == parent

def _type_ok(v: Any, t: str) -> bool:
    return {
        "object": isinstance(v, dict),
        "array": isinstance(v, list),
        "string": isinstance(v, str),
        "boolean": isinstance(v, bool),
        "integer": isinstance(v, int) and not isinstance(v, bool),
        "number": isinstance(v, (int, float)) and not isinstance(v, bool),
        "null": v is None,
    }.get(t, False)

def schema_errors(inst: Any, s: dict, path: str = "$") -> list[str]:
    """Embedded schema subset sufficient for the canonical hostile-audit schemas."""
    e: list[str] = []
    if "type" in s:
        ts = s["type"] if isinstance(s["type"], list) else [s["type"]]
        if not any(_type_ok(inst, t) for t in ts):
            return [f"{path}:type"]
    if "const" in s and inst != s["const"]:
        e.append(f"{path}:const")
    if "enum" in s and inst not in s["enum"]:
        e.append(f"{path}:enum")
    if isinstance(inst, str):
        if len(inst) < s.get("minLength", 0):
            e.append(f"{path}:minLength")
        if "pattern" in s and not re.search(s["pattern"], inst):
            e.append(f"{path}:pattern")
    if isinstance(inst, list):
        if len(inst) < s.get("minItems", 0):
            e.append(f"{path}:minItems")
        if s.get("uniqueItems") is True:
            try:
                if len({json.dumps(x, sort_keys=True) for x in inst}) != len(inst):
                    e.append(f"{path}:uniqueItems")
            except Exception:
                e.append(f"{path}:uniqueItems")
        if "items" in s:
            for i, x in enumerate(inst):
                e += schema_errors(x, s["items"], f"{path}[{i}]")
    if isinstance(inst, dict):
        for k in s.get("required", []):
            if k not in inst:
                e.append(f"{path}:missing:{k}")
        props = s.get("properties", {})
        if s.get("additionalProperties") is False:
            for k in inst:
                if k not in props:
                    e.append(f"{path}:additional:{k}")
        for k, ss in props.items():
            if k in inst:
                e += schema_errors(inst[k], ss, f"{path}.{k}")
    return e

def canonical_schema_check(inst: Any, live: str, rel: str) -> tuple[bool, list[str]]:
    """Schema itself must come from canonical predecessor, never candidate tree."""
    schema = canonical_json(live, rel)
    if not isinstance(schema, dict):
        return False, ["canonical-schema-unavailable"]
    errs = schema_errors(inst, schema)
    return not errs, errs

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate_sha")
    ap.add_argument("audit_evidence_ref")
    ap.add_argument("audit_authorization_ref")
    a = ap.parse_args()

    ok, live, source = live_canonical()
    C: dict[str, bool] = {"LIVE_CANONICAL_REF_RESOLVED": ok}
    D: dict[str, Any] = {
        "live_sha": live,
        "live_source": source,
        "python_execution_flags": dict(_required_flags),
        "repo_import_paths": list(REPO_IMPORT_PATHS),
    }
    if not ok:
        print(json.dumps({"checks": C, "EXTERNAL_INTEGRATION_ELIGIBLE": False, "details": D}, sort_keys=True))
        return 1

    C["PYTHON_EXECUTION_ISOLATED"] = all(_required_flags.values())
    C["NO_REPOSITORY_IMPORT_PATHS"] = not REPO_IMPORT_PATHS

    # The executable authority is one self-contained canonical blob operating
    # behind the interpreter-isolation barrier above.
    ok1, canon_blob = git("rev-parse", f"{live}:{SELF_REL}")
    ok2, current_blob = git("hash-object", str(SCRIPT_PATH))
    C["EXECUTING_COPY_IS_CANONICAL_PREDECESSOR"] = bool(ok1 and ok2 and canon_blob == current_blob)
    C["NO_RAWLSING_RUNTIME_IMPORTS"] = True

    cok, _ = git("cat-file", "-e", f"{a.candidate_sha}^{{commit}}")
    C["CANDIDATE_COMMIT_EXISTS"] = cok
    anc, _ = git("merge-base", "--is-ancestor", live, a.candidate_sha)
    C["CANDIDATE_DESCENDS_FROM_LIVE_CANONICAL"] = anc

    # Manifest and schemas are trusted only when read from live canonical tree.
    mok, mtext = canonical_text(live, MANIFEST_REL)
    protected: set[str] = set()
    if mok:
        try:
            protected = {r.get("path", "") for r in csv.DictReader(mtext.splitlines(), delimiter="\t") if r.get("path")}
        except Exception:
            protected = set()
    C["CANONICAL_PROTECTED_MANIFEST_LOADED"] = bool(protected)
    dependency_closure = {SELF_REL, MANIFEST_REL, AUTH_SCHEMA_REL, RESULT_SCHEMA_REL}
    C["CANONICAL_DEPENDENCY_CLOSURE_DECLARED"] = bool(dependency_closure <= protected)
    C["CANONICAL_AUTH_SCHEMA_AVAILABLE"] = isinstance(canonical_json(live, AUTH_SCHEMA_REL), dict)
    C["CANONICAL_RESULT_SCHEMA_AVAILABLE"] = isinstance(canonical_json(live, RESULT_SCHEMA_REL), dict)
    D["trusted_dependency_sources"] = {x: f"{live}:{x}" for x in sorted(dependency_closure)}

    dok, diff = git_lines("diff", "--name-only", live, a.candidate_sha)
    changed = set(diff)
    pchanged = sorted(changed & protected)
    C["PROTECTED_CHANGE_DETECTED"] = bool(dok and pchanged)
    D["protected_changed_paths"] = pchanged

    auth = immutable_json(a.audit_authorization_ref)
    C["AUDIT_AUTHORIZATION_IMMUTABLE_JSON"] = bool(auth)
    auth_schema_ok, auth_schema_errs = canonical_schema_check(auth, live, AUTH_SCHEMA_REL) if auth else (False, ["no-auth"])
    C["AUDIT_AUTHORIZATION_SCHEMA_VALID"] = auth_schema_ok
    D["authorization_schema_errors"] = auth_schema_errs
    auth_sha, auth_path = split_ref(a.audit_authorization_ref)
    C["AUTHORIZATION_PATH_IS_EXTERNAL_AUDIT_PREFIX"] = bool(auth_path.startswith(AUTH_PREFIX))
    C["AUTHORIZATION_DIRECT_CHILD_OF_LIVE_CANONICAL"] = bool(auth_sha and direct_child_of(auth_sha, live))
    cand_to_auth, _ = git("merge-base", "--is-ancestor", a.candidate_sha, auth_sha) if auth_sha else (False, "")
    C["AUTHORIZATION_OUTSIDE_CANDIDATE_LINEAGE"] = bool(auth_sha and not cand_to_auth)
    arok, ardiff = git_lines("diff", "--name-only", live, auth_sha) if auth_sha else (False, [])
    auth_changed = set(ardiff)
    C["AUTHORIZATION_COMMIT_JURISDICTION_PURE"] = bool(arok and auth_changed and all(x.startswith(AUTH_PREFIX) for x in auth_changed) and not (auth_changed & protected))
    D["authorization_changed_paths"] = sorted(auth_changed)
    C["AUTHORIZATION_BINDS_CANONICAL_HEAD"] = bool(auth and auth.get("canonical_head") == live)
    C["AUTHORIZATION_BINDS_EXACT_CANDIDATE"] = bool(auth and auth.get("candidate_sha") == a.candidate_sha)

    audit = immutable_json(a.audit_evidence_ref)
    C["AUDIT_EVIDENCE_IMMUTABLE_JSON"] = bool(audit)
    audit_schema_ok, audit_schema_errs = canonical_schema_check(audit, live, RESULT_SCHEMA_REL) if audit else (False, ["no-audit"])
    C["AUDIT_RESULT_SCHEMA_VALID"] = audit_schema_ok
    D["audit_schema_errors"] = audit_schema_errs
    audit_sha, audit_path = split_ref(a.audit_evidence_ref)
    branch = str((audit or {}).get("audit_branch", ""))
    expected_branch = str((auth or {}).get("expected_audit_branch", ""))
    prefix = str((auth or {}).get("audit_write_prefix", ""))
    C["AUDIT_RESULT_PATH_WITHIN_AUTHORIZED_PREFIX"] = bool(prefix and audit_path.startswith(prefix))
    bok, btip, bsource = branch_tip(expected_branch) if expected_branch else (False, "", "")
    D["audit_branch_source"] = bsource
    C["AUTHORIZED_AUDIT_BRANCH_RESOLVES"] = bok
    C["AUDIT_EVIDENCE_COMMIT_IS_AUTHORIZED_BRANCH_TIP"] = bool(bok and audit_sha and btip == audit_sha)
    C["AUDIT_RESULT_BRANCH_MATCHES_AUTHORIZATION"] = bool(audit and branch == expected_branch)
    aok, _ = git("merge-base", "--is-ancestor", a.candidate_sha, audit_sha) if audit_sha else (False, "")
    C["AUDIT_DESCENDS_FROM_CANDIDATE"] = aok
    adok, adiff = git_lines("diff", "--name-only", a.candidate_sha, audit_sha) if audit_sha else (False, [])
    audit_changed = set(adiff)
    C["AUDIT_COMMIT_JURISDICTION_PURE"] = bool(adok and audit_changed and prefix and all(x.startswith(prefix) for x in audit_changed) and not (audit_changed & protected))
    D["audit_changed_paths"] = sorted(audit_changed)
    C["AUDIT_BINDS_EXACT_AUTHORIZATION_REF"] = bool(audit and audit.get("authorization_ref") == a.audit_authorization_ref)
    C["AUDIT_CHALLENGE_MATCH"] = bool(audit and auth and audit.get("challenge_nonce") == auth.get("challenge_nonce"))
    C["AUDIT_BINDS_EXACT_CANDIDATE"] = bool(audit and audit.get("candidate_sha") == a.candidate_sha)
    C["AUDIT_MODE_HOSTILE_INDEPENDENT"] = bool(audit and audit.get("audit_mode") == "HOSTILE_INDEPENDENT_AUDIT")
    ruling = str((audit or {}).get("overall_ruling", ""))
    token = str((audit or {}).get("terminal_token", ""))
    allowed = set((auth or {}).get("allowed_pass_rulings", []))
    token_prefixes = list((auth or {}).get("allowed_terminal_token_prefixes", []))
    C["AUDIT_RULING_EXACTLY_AUTHORIZED_PASS"] = bool(ruling and ruling in allowed)
    C["AUDIT_TERMINAL_TOKEN_PREFIX_AUTHORIZED"] = bool(token and any(token.startswith(x) for x in token_prefixes))

    eligible = all(C.values())
    print(json.dumps({"checks": C, "EXTERNAL_INTEGRATION_ELIGIBLE": eligible, "details": D}, sort_keys=True))
    return 0 if eligible else 1

if __name__ == "__main__":
    sys.exit(main())
