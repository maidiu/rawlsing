"""Read-only Python profiling of real functions; no response replacement."""

from pathlib import Path
import sys, json, hashlib, os
import pytest
import review_bootstrap as B

R = B.R
NAMES = {
    "adp016_form_causal_trace",
    "commit_memory",
    "adp017_apply_epistemic_effect",
    "adp017_first_person_check",
    "read_owner",
    "response_rule_apply",
    "coupline_evaluate",
    "later",
    "admit_event",
    "commit",
}
ACTIVE = None
CALLS = []
FILES = {}


def bh(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def profile(frame, event, arg):
    name = frame.f_code.co_name
    if name not in NAMES or event not in ("call", "return"):
        return
    path = Path(frame.f_code.co_filename).resolve()
    if not path.is_relative_to(R / "runtime/m01"):
        return
    rel = str(path.relative_to(R))
    if rel not in FILES:
        FILES[rel] = {
            "git_blob_sha1": bh(path.read_bytes()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    row = {
        "case": ACTIVE,
        "event": event,
        "function": name,
        "file": rel,
        "line": frame.f_code.co_firstlineno,
    }
    if event == "call":
        for k in (
            "actor_id",
            "expected_state",
            "at",
            "rule_version",
            "authority",
            "effective_causal_time",
            "claim_ref",
            "claim_accessibility",
            "stance_kind",
            "content_state",
        ):
            if k in frame.f_locals:
                row[k] = frame.f_locals[k]
        if name == "commit":
            row["kind"] = frame.f_locals.get("kind")
    elif isinstance(arg, dict):
        for k in (
            "status",
            "decision_state",
            "state_hash",
            "streams",
            "first_person_permission",
        ):
            if k in arg:
                row[k] = arg[k]
        if isinstance(arg.get("entry"), dict):
            row["committed_entry_hash"] = arg["entry"].get("entry_hash")
        if isinstance(arg.get("memory"), dict):
            row["memory_id"] = arg["memory"].get("memory_id")
    CALLS.append(row)


@pytest.hookimpl
def pytest_sessionstart(session):
    from rawlsing_next import v3_psepf_zero_positive_guard as G

    session._m02_guard = G
    session._m02_guard_bytes = Path(G.__file__).read_bytes()
    assert bh(session._m02_guard_bytes) == "e0528d65215cb431196570c38bac4eae94217a1b"
    assert not G.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
    sys.setprofile(profile)


def pytest_runtest_setup(item):
    global ACTIVE
    ACTIVE = item.name


def pytest_sessionfinish(session, exitstatus):
    sys.setprofile(None)
    g = session._m02_guard
    assert (
        Path(g.__file__).read_bytes() == session._m02_guard_bytes
        and not g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
    )
    imports = []
    for name, module in sorted(sys.modules.items()):
        p = getattr(module, "__file__", None)
        if not p or not name.startswith(
            ("candidate", "rawlsing_next", "cell", "bootstrap", "owner_effect_stub")
        ):
            continue
        p = Path(p).resolve()
        if p.suffix != ".py":
            continue
        assert p.is_relative_to(R)
        imports.append(
            {
                "module": name,
                "module_file": str(p.relative_to(R)),
                "git_blob_sha1": bh(p.read_bytes()),
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            }
        )
    subdir = os.environ.get("M02_EVIDENCE_SUBDIR", "independent")
    assert subdir in ("independent", "corroboration")
    (R / "evidence" / subdir / "actual_function_calls.json").write_text(
        json.dumps(
            {
                "actual_function_events": CALLS,
                "physical_function_sources": FILES,
                "module_imports": imports,
                "production_guard": {
                    "module_file": str(Path(g.__file__).relative_to(R)),
                    "blob_sha1": bh(session._m02_guard_bytes),
                    "byte_unchanged": True,
                    "registry_empty": True,
                },
                "no_response_monkeypatch": True,
                "observer": "sys.setprofile only",
            },
            indent=2,
        )
        + "\n"
    )
