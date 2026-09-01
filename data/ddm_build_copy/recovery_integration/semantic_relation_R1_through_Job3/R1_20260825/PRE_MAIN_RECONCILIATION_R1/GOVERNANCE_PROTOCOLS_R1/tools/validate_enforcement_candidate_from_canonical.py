#!/usr/bin/env python3
"""Fail-closed governance-enforcement canonical-predecessor gate.

Authoritative invocation:
  python3 -I -S validate_enforcement_candidate_from_canonical.py \
    --repository-root /absolute/trusted/repository/root \
    --trusted-git-executable /absolute/trusted/git \
    <candidate_sha> <audit_evidence_ref> <audit_authorization_ref>

Trust boundary:
- built-in ``sys`` is the only import before the Python isolation barrier;
- after that barrier, only Python stdlib is imported;
- repository root and Git executable are explicit trusted-host inputs;
- repository metadata is pinned to concrete ``<repository-root>/.git``;
- loose/packed ref storage used for authoritative refs cannot escape that root;
- every Git subprocess uses the exact absolute Git executable and a rebuilt
  environment with no inherited PATH;
- the object database passes full Git object-integrity verification before
  trust-bearing reads, and returned commit/blob bytes are re-hashed by Python;
- canonical schemas/manifests/evidence are read only through exact immutable
  commit/object addresses.
"""
from __future__ import annotations

import sys

_REQUIRED_FLAGS = {
    "isolated": bool(getattr(sys.flags, "isolated", 0)),
    "ignore_environment": bool(getattr(sys.flags, "ignore_environment", 0)),
    "no_user_site": bool(getattr(sys.flags, "no_user_site", 0)),
    "no_site": bool(getattr(sys.flags, "no_site", 0)),
    "safe_path": bool(getattr(sys.flags, "safe_path", False)),
}
if not all(_REQUIRED_FLAGS.values()):
    sys.stderr.write(
        "FAIL_PYTHON_EXECUTION_NOT_ISOLATED: invoke with `python3 -I -S`; "
        + ",".join(f"{k}={int(v)}" for k, v in _REQUIRED_FLAGS.items())
        + "\n"
    )
    raise SystemExit(97)

import argparse
import csv
import hashlib
import json
import os
import re
import stat
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
IMMUTABLE_REF_RE = re.compile(r"^(?P<sha>[0-9a-f]{40}):(?P<path>[^\n\r]+)$")
OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SCRIPT_PATH = Path(__file__).resolve()


class TrustFailure(RuntimeError):
    pass


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        p = path.resolve(strict=False)
        r = root.resolve(strict=False)
        return p == r or r in p.parents
    except Exception:
        return True


def _has_symlink_component(path: Path) -> bool:
    try:
        if not path.is_absolute():
            return True
        cur = Path(path.anchor)
        for part in path.parts[1:]:
            cur = cur / part
            if cur.is_symlink():
                return True
        return False
    except Exception:
        return True


def _require_concrete_dir(path: Path, label: str) -> None:
    if _has_symlink_component(path):
        raise TrustFailure(f"{label}-symlink-component")
    try:
        real = path.resolve(strict=True)
    except Exception as ex:
        raise TrustFailure(f"{label}-unresolvable:{ex}") from ex
    if real != path or not real.is_dir():
        raise TrustFailure(f"{label}-not-canonical-directory")


def _require_optional_regular(path: Path, label: str) -> None:
    if _has_symlink_component(path):
        raise TrustFailure(f"{label}-symlink-component")
    if not path.exists():
        return
    try:
        real = path.resolve(strict=True)
        st = real.stat()
    except Exception as ex:
        raise TrustFailure(f"{label}-unresolvable:{ex}") from ex
    if real != path or not stat.S_ISREG(st.st_mode):
        raise TrustFailure(f"{label}-not-canonical-regular-file")


def _validated_repository_root(raw: str) -> tuple[Path, Path]:
    p = Path(raw)
    if not p.is_absolute():
        raise TrustFailure("repository-root-not-absolute")
    if _has_symlink_component(p):
        raise TrustFailure("repository-root-symlink-component")
    try:
        real = p.resolve(strict=True)
    except Exception as ex:
        raise TrustFailure(f"repository-root-unresolvable:{ex}") from ex
    if real != p or not real.is_dir():
        raise TrustFailure("repository-root-not-canonical-directory")
    if not _path_is_within(SCRIPT_PATH, real):
        raise TrustFailure("executing-script-outside-declared-repository-root")

    git_dir = real / ".git"
    _require_concrete_dir(git_dir, "repository-git-dir")
    _require_concrete_dir(git_dir / "objects", "repository-object-dir")

    refs_dir = git_dir / "refs"
    if refs_dir.exists() or refs_dir.is_symlink():
        _require_concrete_dir(refs_dir, "repository-refs-dir")
    _require_optional_regular(git_dir / "packed-refs", "repository-packed-refs")

    if (git_dir / "commondir").exists() or (git_dir / "commondir").is_symlink():
        raise TrustFailure("repository-common-dir-indirection-rejected")

    # Reject storage selectors before the first Git subprocess. These paths are
    # checked even when the leaf is absent so a symlinked parent cannot hide it.
    for rel, label in (
        ("info/grafts", "repository-grafts-path"),
        ("objects/info/alternates", "repository-alternates-path"),
    ):
        path = git_dir / rel
        if _has_symlink_component(path):
            raise TrustFailure(f"{label}-symlink-component")
        if path.exists():
            try:
                payload = path.read_bytes()
            except Exception as ex:
                raise TrustFailure(f"{label}-unreadable:{ex}") from ex
            if payload.strip():
                raise TrustFailure(f"{label}-nonempty")

    pack_dir = git_dir / "objects" / "pack"
    if pack_dir.exists() or pack_dir.is_symlink():
        _require_concrete_dir(pack_dir, "repository-pack-dir")

    return real, git_dir


def _fingerprint_executable(path: Path) -> dict[str, Any]:
    try:
        st = path.stat()
        if not stat.S_ISREG(st.st_mode):
            raise TrustFailure("trusted-git-not-regular-file")
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return {
            "realpath": str(path),
            "sha256": h.hexdigest(),
            "device": int(st.st_dev),
            "inode": int(st.st_ino),
            "size": int(st.st_size),
            "mtime_ns": int(st.st_mtime_ns),
        }
    except TrustFailure:
        raise
    except Exception as ex:
        raise TrustFailure(f"trusted-git-fingerprint-failed:{ex}") from ex


def _validated_git_executable(raw: str, repo: Path) -> tuple[Path, dict[str, Any]]:
    p = Path(raw)
    if not p.is_absolute():
        raise TrustFailure("trusted-git-path-not-absolute")
    if _has_symlink_component(p):
        raise TrustFailure("trusted-git-path-has-symlink-component")
    try:
        real = p.resolve(strict=True)
    except Exception as ex:
        raise TrustFailure(f"trusted-git-unresolvable:{ex}") from ex
    if real != p:
        raise TrustFailure("trusted-git-path-not-canonical-absolute-path")
    if _path_is_within(real, repo):
        raise TrustFailure("trusted-git-resolves-inside-repository")
    if not real.is_file() or not os.access(real, os.X_OK):
        raise TrustFailure("trusted-git-not-executable-regular-file")
    return real, _fingerprint_executable(real)


def _repo_import_paths(repo: Path) -> list[str]:
    bad: list[str] = []
    for entry in sys.path:
        if not entry:
            bad.append(entry)
            continue
        try:
            if _path_is_within(Path(entry), repo):
                bad.append(entry)
        except Exception:
            bad.append(entry)
    return bad


def _git_env() -> dict[str, str]:
    env = {
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_CONFIG_COUNT": "0",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_PAGER": "",
        "PAGER": "",
        "GIT_OPTIONAL_LOCKS": "0",
    }
    if os.name == "nt":
        for key in ("SystemRoot", "WINDIR"):
            if os.environ.get(key):
                env[key] = os.environ[key]
    return env


def _object_oid(kind: str, data: bytes, oid_len: int) -> str:
    framed = kind.encode("ascii") + b" " + str(len(data)).encode("ascii") + b"\0" + data
    if oid_len == 40:
        return hashlib.sha1(framed).hexdigest()
    if oid_len == 64:
        return hashlib.sha256(framed).hexdigest()
    return ""


def _repo_path_ok(path: str) -> bool:
    if not path or path.startswith("/") or "\x00" in path or "\n" in path or "\r" in path:
        return False
    return all(part not in ("", ".", "..") for part in path.split("/"))


def _ref_name_ok(ref: str) -> bool:
    if not ref.startswith("refs/") or ref.endswith("/") or ref.endswith("."):
        return False
    if ".." in ref or "//" in ref or "@{" in ref:
        return False
    if any(ord(c) < 32 or ord(c) == 127 or c in " ~^:?*[\\" for c in ref):
        return False
    parts = ref.split("/")
    return all(p and not p.startswith(".") and not p.endswith(".lock") for p in parts)


class GitTrust:
    def __init__(self, executable: Path, repo: Path, git_dir: Path, fingerprint: dict[str, Any]):
        self.executable = executable
        self.repo = repo
        self.git_dir = git_dir
        self.fingerprint_before = fingerprint
        self.env = _git_env()

    def _base(self) -> list[str]:
        return [
            str(self.executable),
            "--no-pager",
            "--no-replace-objects",
            f"--git-dir={self.git_dir}",
            f"--work-tree={self.repo}",
        ]

    def run_bytes(self, *args: str, input_bytes: bytes | None = None, timeout: int = 20) -> tuple[bool, bytes, bytes]:
        try:
            p = subprocess.run(
                [*self._base(), *args],
                input=input_bytes,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env,
                timeout=timeout,
                check=False,
            )
            return p.returncode == 0, p.stdout, p.stderr
        except Exception:
            return False, b"", b""

    def run_text(self, *args: str, timeout: int = 20) -> tuple[bool, str]:
        ok, out, _ = self.run_bytes(*args, timeout=timeout)
        if not ok:
            return False, ""
        try:
            return True, out.decode("utf-8", "strict").strip()
        except UnicodeDecodeError:
            return False, ""

    def _ref_storage_safe(self, ref: str) -> bool:
        if not _ref_name_ok(ref):
            return False
        loose = self.git_dir.joinpath(*ref.split("/"))
        if _has_symlink_component(loose):
            return False
        if loose.exists():
            try:
                if not loose.is_file():
                    return False
            except Exception:
                return False
        packed = self.git_dir / "packed-refs"
        if _has_symlink_component(packed):
            return False
        if packed.exists():
            try:
                if packed.resolve(strict=True) != packed or not packed.is_file():
                    return False
            except Exception:
                return False
        return True

    def resolve_ref(self, ref: str) -> tuple[bool, str]:
        if not self._ref_storage_safe(ref):
            return False, ""
        ok, out = self.run_text("rev-parse", "--verify", f"{ref}^{{commit}}")
        if not ok or not OID_RE.fullmatch(out or ""):
            return False, ""
        cok, raw = self.read_commit(out)
        pok, _, _ = _parse_commit(raw) if cok else (False, "", [])
        return (True, out) if cok and pok else (False, "")

    def read_commit(self, sha: str) -> tuple[bool, bytes]:
        if not OID_RE.fullmatch(sha or ""):
            return False, b""
        ok, out, _ = self.run_bytes("cat-file", "commit", sha)
        if not ok or _object_oid("commit", out, len(sha)) != sha:
            return False, b""
        return True, out

    def read_blob(self, spec: str) -> tuple[bool, bytes]:
        if OID_RE.fullmatch(spec or ""):
            oid = spec
        else:
            m = IMMUTABLE_REF_RE.fullmatch(spec or "")
            if not m or not _repo_path_ok(m.group("path")):
                return False, b""
            commit_oid = m.group("sha")
            cok, craw = self.read_commit(commit_oid)
            pok, _, _ = _parse_commit(craw) if cok else (False, "", [])
            if not cok or not pok:
                return False, b""
            rok, oid = self.run_text("rev-parse", "--verify", spec)
            if not rok or not OID_RE.fullmatch(oid or ""):
                return False, b""
        ok, out, _ = self.run_bytes("cat-file", "blob", oid)
        if not ok or _object_oid("blob", out, len(oid)) != oid:
            return False, b""
        return True, out

    def commit_exists(self, sha: str) -> bool:
        ok, raw = self.read_commit(sha)
        pok, _, _ = _parse_commit(raw) if ok else (False, "", [])
        return bool(ok and pok)

    def changed_paths(self, base: str, head: str) -> tuple[bool, list[str]]:
        if not self.commit_exists(base) or not self.commit_exists(head):
            return False, []
        ok, out, _ = self.run_bytes(
            "diff-tree", "--no-commit-id", "--name-only", "-r", "-z",
            "--no-renames", "--no-ext-diff", "--no-textconv", base, head,
        )
        if not ok:
            return False, []
        try:
            raw = [x for x in out.split(b"\0") if x]
            paths = [x.decode("utf-8", "strict") for x in raw]
        except Exception:
            return False, []
        if any(not _repo_path_ok(x) for x in paths):
            return False, []
        return True, paths

    def git_path(self, rel: str) -> tuple[bool, Path]:
        ok, out = self.run_text("rev-parse", "--git-path", rel)
        if not ok or not out:
            return False, Path()
        p = Path(out)
        if not p.is_absolute():
            p = self.git_dir / p
        try:
            return True, p.resolve(strict=False)
        except Exception:
            return False, Path()

    def repository_hardening(self) -> tuple[bool, dict[str, Any]]:
        details: dict[str, Any] = {}
        ok, out = self.run_text("rev-parse", "--is-shallow-repository")
        details["is_shallow_repository"] = out if ok else "UNRESOLVED"
        if not ok or out != "false":
            return False, details

        rok, replace = self.run_text("for-each-ref", "--format=%(refname)", "refs/replace")
        details["replace_refs_present"] = [x for x in replace.splitlines() if x] if rok else ["UNRESOLVED"]
        if not rok or details["replace_refs_present"]:
            return False, details

        tok, top = self.run_text("rev-parse", "--show-toplevel")
        details["git_reported_worktree_root"] = top if tok else "UNRESOLVED"
        if not tok:
            return False, details
        try:
            if Path(top).resolve(strict=True) != self.repo:
                return False, details
        except Exception:
            return False, details

        gok, gitdir = self.run_text("rev-parse", "--absolute-git-dir")
        details["absolute_git_dir"] = gitdir if gok else "UNRESOLVED"
        if not gok:
            return False, details
        try:
            if Path(gitdir).resolve(strict=True) != self.git_dir:
                return False, details
        except Exception:
            return False, details

        cok, common = self.run_text("rev-parse", "--git-common-dir")
        details["git_common_dir"] = common if cok else "UNRESOLVED"
        if not cok:
            return False, details
        common_path = Path(common)
        if not common_path.is_absolute():
            common_path = self.git_dir / common_path
        try:
            if common_path.resolve(strict=True) != self.git_dir:
                return False, details
        except Exception:
            return False, details

        for rel, key in (("info/grafts", "grafts"), ("objects/info/alternates", "alternates")):
            pok, path = self.git_path(rel)
            if not pok or not _path_is_within(path, self.git_dir):
                details[key] = "UNRESOLVED_OR_OUTSIDE_GIT_DIR"
                return False, details
            try:
                payload = path.read_bytes() if path.exists() else b""
            except Exception:
                details[key] = "UNREADABLE"
                return False, details
            details[key] = {"path": str(path), "nonempty": bool(payload.strip())}
            if payload.strip():
                return False, details

        # Git's ordinary object reads do not necessarily recompute the object ID.
        # A full fsck is therefore a trust prerequisite before any canonical ref,
        # ancestry, schema, manifest, authorization, audit, or diff fact is used.
        fok, _, _ = self.run_bytes("fsck", "--full", "--no-reflogs", "--no-progress", timeout=120)
        details["full_object_database_fsck"] = "PASS" if fok else "FAIL"
        if not fok:
            return False, details
        return True, details

    def final_fingerprint_matches(self) -> tuple[bool, dict[str, Any]]:
        after = _fingerprint_executable(self.executable)
        return after == self.fingerprint_before, after


def _parse_commit(raw: bytes) -> tuple[bool, str, list[str]]:
    try:
        text = raw.decode("ascii", "strict")
    except UnicodeDecodeError:
        return False, "", []
    tree = ""
    parents: list[str] = []
    for line in text.splitlines():
        if line == "":
            break
        if line.startswith("tree "):
            oid = line[5:]
            if tree or not OID_RE.fullmatch(oid):
                return False, "", []
            tree = oid
        elif line.startswith("parent "):
            oid = line[7:]
            if not OID_RE.fullmatch(oid):
                return False, "", []
            parents.append(oid)
    return bool(tree), tree, parents


def direct_child_of(git: GitTrust, commit: str, parent: str) -> bool:
    ok, raw = git.read_commit(commit)
    pok, _, parents = _parse_commit(raw) if ok else (False, "", [])
    return bool(pok and parents == [parent])


def is_ancestor(git: GitTrust, ancestor: str, descendant: str, limit: int = 100000) -> bool:
    if not OID_RE.fullmatch(ancestor or "") or not OID_RE.fullmatch(descendant or ""):
        return False
    stack = [descendant]
    seen: set[str] = set()
    while stack:
        cur = stack.pop()
        if cur == ancestor:
            return True
        if cur in seen:
            continue
        seen.add(cur)
        if len(seen) > limit:
            return False
        ok, raw = git.read_commit(cur)
        pok, _, parents = _parse_commit(raw) if ok else (False, "", [])
        if not pok:
            return False
        stack.extend(parents)
    return False


def live_canonical(git: GitTrust) -> tuple[bool, str, str]:
    lo, ls = git.resolve_ref(f"refs/heads/{CANONICAL_REF}")
    ro, rs = git.resolve_ref(f"refs/remotes/origin/{CANONICAL_REF}")
    if lo and ro and ls != rs:
        return False, "", "DIVERGED"
    if lo:
        return True, ls, "LOCAL" + ("+REMOTE_MATCH" if ro else "")
    if ro:
        return True, rs, "REMOTE_ONLY"
    return False, "", "UNRESOLVED"


def branch_tip(git: GitTrust, name: str) -> tuple[bool, str, str]:
    lo, ls = git.resolve_ref(f"refs/heads/{name}")
    ro, rs = git.resolve_ref(f"refs/remotes/origin/{name}")
    if lo and ro and ls != rs:
        return False, "", "DIVERGED"
    if lo:
        return True, ls, "LOCAL" + ("+REMOTE_MATCH" if ro else "")
    if ro:
        return True, rs, "REMOTE_ONLY"
    return False, "", "UNRESOLVED"


def canonical_bytes(git: GitTrust, live: str, rel: str) -> tuple[bool, bytes]:
    return git.read_blob(f"{live}:{rel}")


def canonical_json(git: GitTrust, live: str, rel: str) -> Any:
    ok, data = canonical_bytes(git, live, rel)
    if not ok:
        return None
    try:
        return json.loads(data.decode("utf-8", "strict"))
    except Exception:
        return None


def immutable_json(git: GitTrust, ref: str) -> Any:
    m = IMMUTABLE_REF_RE.fullmatch(ref or "")
    if not m:
        return None
    ok, data = git.read_blob(ref)
    if not ok:
        return None
    try:
        return json.loads(data.decode("utf-8", "strict"))
    except Exception:
        return None


def split_ref(v: str) -> tuple[str, str]:
    m = IMMUTABLE_REF_RE.fullmatch(v or "")
    return (m.group("sha"), m.group("path")) if m else ("", "")


def _type_ok(v: Any, t: str) -> bool:
    return {
        "object": isinstance(v, dict), "array": isinstance(v, list), "string": isinstance(v, str),
        "boolean": isinstance(v, bool), "integer": isinstance(v, int) and not isinstance(v, bool),
        "number": isinstance(v, (int, float)) and not isinstance(v, bool), "null": v is None,
    }.get(t, False)


def schema_errors(inst: Any, s: dict, path: str = "$") -> list[str]:
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


def canonical_schema_check(git: GitTrust, inst: Any, live: str, rel: str) -> tuple[bool, list[str]]:
    schema = canonical_json(git, live, rel)
    if not isinstance(schema, dict):
        return False, ["canonical-schema-unavailable"]
    errs = schema_errors(inst, schema)
    return not errs, errs


def _emit_failure(reason: str, details: dict[str, Any] | None = None) -> int:
    print(json.dumps({
        "checks": {"TRUST_ROOT_INITIALIZATION": False},
        "EXTERNAL_INTEGRATION_ELIGIBLE": False,
        "details": {"trust_failure": reason, **(details or {})},
    }, sort_keys=True))
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repository-root", required=True)
    ap.add_argument("--trusted-git-executable", required=True)
    ap.add_argument("candidate_sha")
    ap.add_argument("audit_evidence_ref")
    ap.add_argument("audit_authorization_ref")
    a = ap.parse_args()

    try:
        repo, git_dir = _validated_repository_root(a.repository_root)
        git_exe, git_fp = _validated_git_executable(a.trusted_git_executable, repo)
    except TrustFailure as ex:
        return _emit_failure(str(ex))

    repo_import_paths = _repo_import_paths(repo)
    if repo_import_paths:
        return _emit_failure("candidate-controlled-import-path-present", {"repo_import_paths": repo_import_paths})

    git = GitTrust(git_exe, repo, git_dir, git_fp)
    hard_ok, hard_details = git.repository_hardening()
    if not hard_ok:
        return _emit_failure(
            "repository-object-or-ancestry-hardening-failed",
            {"repository_hardening": hard_details, "trusted_git": git_fp},
        )

    ok, live, source = live_canonical(git)
    C: dict[str, bool] = {"TRUST_ROOT_INITIALIZATION": True, "LIVE_CANONICAL_REF_RESOLVED": ok}
    D: dict[str, Any] = {
        "live_sha": live, "live_source": source,
        "python_execution_flags": dict(_REQUIRED_FLAGS),
        "repo_import_paths": list(repo_import_paths),
        "repository_root": str(repo), "repository_git_dir": str(git_dir),
        "trusted_git_executable": str(git_exe),
        "trusted_git_fingerprint_before": git_fp,
        "git_subprocess_environment_keys": sorted(git.env),
        "git_path_in_child_environment": git.env.get("PATH"),
        "repository_hardening": hard_details,
    }
    if not ok:
        print(json.dumps({"checks": C, "EXTERNAL_INTEGRATION_ELIGIBLE": False, "details": D}, sort_keys=True))
        return 1

    C["PYTHON_EXECUTION_ISOLATED"] = all(_REQUIRED_FLAGS.values())
    C["NO_REPOSITORY_IMPORT_PATHS"] = not repo_import_paths
    C["NO_PATH_AUTHORITY_FOR_GIT_EXECUTABLE"] = "PATH" not in git.env
    C["TRUSTED_GIT_OUTSIDE_REPOSITORY"] = not _path_is_within(git_exe, repo)
    C["TRUSTED_GIT_PATH_ABSOLUTE"] = git_exe.is_absolute()
    C["REPOSITORY_METADATA_ROOT_PINNED"] = git.git_dir == repo / ".git"
    C["OBJECT_DATABASE_HASH_INTEGRITY_VERIFIED"] = hard_details.get("full_object_database_fsck") == "PASS"

    cok, canon_self = canonical_bytes(git, live, SELF_REL)
    try:
        current_self = SCRIPT_PATH.read_bytes()
    except Exception:
        current_self = b""
    C["EXECUTING_COPY_IS_CANONICAL_PREDECESSOR"] = bool(cok and canon_self == current_self)
    C["NO_RAWLSING_RUNTIME_IMPORTS"] = True

    C["CANDIDATE_SHA_IS_EXACT_OID"] = bool(OID_RE.fullmatch(a.candidate_sha or ""))
    C["CANDIDATE_COMMIT_EXISTS"] = bool(C["CANDIDATE_SHA_IS_EXACT_OID"] and git.commit_exists(a.candidate_sha))
    C["CANDIDATE_DESCENDS_FROM_LIVE_CANONICAL"] = C["CANDIDATE_COMMIT_EXISTS"] and is_ancestor(git, live, a.candidate_sha)

    mok, mbytes = canonical_bytes(git, live, MANIFEST_REL)
    protected: set[str] = set()
    if mok:
        try:
            mtext = mbytes.decode("utf-8", "strict")
            protected = {r.get("path", "") for r in csv.DictReader(mtext.splitlines(), delimiter="\t") if r.get("path")}
        except Exception:
            protected = set()
    C["CANONICAL_PROTECTED_MANIFEST_LOADED"] = bool(protected)
    dependency_closure = {SELF_REL, MANIFEST_REL, AUTH_SCHEMA_REL, RESULT_SCHEMA_REL}
    C["CANONICAL_DEPENDENCY_CLOSURE_DECLARED"] = bool(dependency_closure <= protected)
    C["CANONICAL_AUTH_SCHEMA_AVAILABLE"] = isinstance(canonical_json(git, live, AUTH_SCHEMA_REL), dict)
    C["CANONICAL_RESULT_SCHEMA_AVAILABLE"] = isinstance(canonical_json(git, live, RESULT_SCHEMA_REL), dict)
    D["trusted_dependency_sources"] = {x: f"{live}:{x}" for x in sorted(dependency_closure)}

    dok, diff = git.changed_paths(live, a.candidate_sha)
    changed = set(diff)
    pchanged = sorted(changed & protected)
    C["PROTECTED_CHANGE_DETECTED"] = bool(dok and pchanged)
    D["protected_changed_paths"] = pchanged

    auth = immutable_json(git, a.audit_authorization_ref)
    C["AUDIT_AUTHORIZATION_IMMUTABLE_JSON"] = bool(auth)
    auth_schema_ok, auth_schema_errs = canonical_schema_check(git, auth, live, AUTH_SCHEMA_REL) if auth else (False, ["no-auth"])
    C["AUDIT_AUTHORIZATION_SCHEMA_VALID"] = auth_schema_ok
    D["authorization_schema_errors"] = auth_schema_errs
    auth_sha, auth_path = split_ref(a.audit_authorization_ref)
    C["AUTHORIZATION_PATH_IS_EXTERNAL_AUDIT_PREFIX"] = bool(auth_path.startswith(AUTH_PREFIX))
    C["AUTHORIZATION_DIRECT_CHILD_OF_LIVE_CANONICAL"] = bool(auth_sha and direct_child_of(git, auth_sha, live))
    C["AUTHORIZATION_OUTSIDE_CANDIDATE_LINEAGE"] = bool(auth_sha and not is_ancestor(git, a.candidate_sha, auth_sha))
    arok, ardiff = git.changed_paths(live, auth_sha) if auth_sha else (False, [])
    auth_changed = set(ardiff)
    C["AUTHORIZATION_COMMIT_JURISDICTION_PURE"] = bool(
        arok and auth_changed and all(x.startswith(AUTH_PREFIX) for x in auth_changed) and not (auth_changed & protected)
    )
    D["authorization_changed_paths"] = sorted(auth_changed)
    C["AUTHORIZATION_BINDS_CANONICAL_HEAD"] = bool(auth and auth.get("canonical_head") == live)
    C["AUTHORIZATION_BINDS_EXACT_CANDIDATE"] = bool(auth and auth.get("candidate_sha") == a.candidate_sha)

    audit = immutable_json(git, a.audit_evidence_ref)
    C["AUDIT_EVIDENCE_IMMUTABLE_JSON"] = bool(audit)
    audit_schema_ok, audit_schema_errs = canonical_schema_check(git, audit, live, RESULT_SCHEMA_REL) if audit else (False, ["no-audit"])
    C["AUDIT_RESULT_SCHEMA_VALID"] = audit_schema_ok
    D["audit_schema_errors"] = audit_schema_errs
    audit_sha, audit_path = split_ref(a.audit_evidence_ref)
    branch = str((audit or {}).get("audit_branch", ""))
    expected_branch = str((auth or {}).get("expected_audit_branch", ""))
    prefix = str((auth or {}).get("audit_write_prefix", ""))
    C["AUDIT_RESULT_PATH_WITHIN_AUTHORIZED_PREFIX"] = bool(prefix and audit_path.startswith(prefix))
    bok, btip, bsource = branch_tip(git, expected_branch) if expected_branch else (False, "", "")
    D["audit_branch_source"] = bsource
    C["AUTHORIZED_AUDIT_BRANCH_RESOLVES"] = bok
    C["AUDIT_EVIDENCE_COMMIT_IS_AUTHORIZED_BRANCH_TIP"] = bool(bok and audit_sha and btip == audit_sha)
    C["AUDIT_RESULT_BRANCH_MATCHES_AUTHORIZATION"] = bool(audit and branch == expected_branch)
    C["AUDIT_DESCENDS_FROM_CANDIDATE"] = bool(audit_sha and is_ancestor(git, a.candidate_sha, audit_sha))
    adok, adiff = git.changed_paths(a.candidate_sha, audit_sha) if audit_sha else (False, [])
    audit_changed = set(adiff)
    C["AUDIT_COMMIT_JURISDICTION_PURE"] = bool(
        adok and audit_changed and prefix and all(x.startswith(prefix) for x in audit_changed) and not (audit_changed & protected)
    )
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

    try:
        fp_ok, fp_after = git.final_fingerprint_matches()
    except TrustFailure:
        fp_ok, fp_after = False, {}
    C["TRUSTED_GIT_IDENTITY_STABLE_DURING_EXECUTION"] = fp_ok
    D["trusted_git_fingerprint_after"] = fp_after

    eligible = all(C.values())
    print(json.dumps({"checks": C, "EXTERNAL_INTEGRATION_ELIGIBLE": eligible, "details": D}, sort_keys=True))
    return 0 if eligible else 1


if __name__ == "__main__":
    sys.exit(main())
