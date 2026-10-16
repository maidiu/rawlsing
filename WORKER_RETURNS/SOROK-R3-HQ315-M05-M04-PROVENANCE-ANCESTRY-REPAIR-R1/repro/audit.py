"""Audit saved executions, literal case continuity and actual imported source bytes."""

from pathlib import Path
import json, hashlib, subprocess, sys, os, re, datetime, platform
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
M2 = R / "runtime/m02"
M1 = M2 / "runtime/m01"
SEAL = "92b9fa8b29f85ad77576da39a8765a666a5ab37f"
M01 = "02187a14e75ff30dd953d3c7185d689b80e62304"
M02 = "0216d9036a87e2f60f42fd5b2870556027808419"
MP = "WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def load(p):
    return json.loads((R / p).read_text())


def write(p, data):
    (R / p).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


# Preserve raw metadata locally, export only portable presentations; no assertion changes.
raw = R / "runtime/raw_final_portable"
raw.mkdir(exist_ok=True)
changes = []
for p in (R / "evidence").rglob("*"):
    if not p.is_file() or p.suffix not in (".xml", ".json", ".log", ".stdout", ".txt"):
        continue
    s = p.read_text()
    clean = (
        s.replace(str(R), "[RETURN]")
        .replace(str(ROOT), "[WORKTREE]")
        .replace(str(Path.home()), "[HOME]")
    )
    if p.suffix == ".xml":
        clean = re.sub(r'hostname="[^"]*"', 'hostname="[HOST]"', clean)
    if s != clean:
        dest = raw / p.relative_to(R / "evidence")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(s)
        changes.append(
            {
                "path": str(p.relative_to(R)),
                "raw_sha256": sha(s.encode()),
                "portable_sha256": sha(clean.encode()),
                "change": "portable path/hostname metadata only",
            }
        )
        p.write_text(clean)
if changes:
    write(
        "evidence/FINAL_PORTABILITY_SANITIZATION.json",
        {"changes": changes, "raw_metadata_retained_in_ignored_runtime": True},
    )


def cases(folder):
    rows = {}
    for p in sorted((R / folder).rglob("junit.xml")):
        for c in ET.parse(p).getroot().iter("testcase"):
            key = (str(p.relative_to(R / folder)), c.get("classname"), c.get("name"))
            assert key not in rows, key
            rows[key] = (
                "FAIL"
                if c.find("failure") is not None
                else (
                    "ERROR"
                    if c.find("error") is not None
                    else "SKIP" if c.find("skipped") is not None else "PASS"
                )
            )
    return rows


b = cases("evidence/before")
a = cases("evidence/after")
author = cases("evidence/author")
historical = cases("evidence/historical_nine")
assert len(b) == len(a) == 513 and b.keys() == a.keys()
assert list(b.values()).count("PASS") == 511 and list(b.values()).count("FAIL") == 2
assert (
    set(a.values()) == {"PASS"}
    and len(author) == 74
    and set(author.values()) == {"PASS"}
)
assert len(historical) == 9 and set(historical.values()) == {"FAIL"}
closure = []
for k in b:
    closure.append(
        {
            "junit": k[0],
            "classname": k[1],
            "literal_test_name": k[2],
            "before": b[k],
            "after": a[k],
        }
    )
write("04_LITERAL_513_CASE_CLOSURE.json", closure)
red = [x for x in closure if x["before"] == "FAIL"]
assert {x["literal_test_name"] for x in red} == {
    "test_lawful_future_claim_cannot_condition_an_earlier_response",
    "test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence",
}

factorial = []
for p in sorted(
    (R / "evidence/before/independent_100/observations").glob("factorial_*.json")
):
    before = json.loads(p.read_text())
    after = load("evidence/after/independent_100/observations/" + p.name)
    assert before["arm"] == after["arm"]
    for data in [before, after]:
        assert (
            data["pre"]["owner_state"]
            == data["actual_result"]["read"]["actual_state"]
            == data["post"]["owner_state"]
        )
    assert before["pre"]["owner_state"] == after["pre"]["owner_state"]
    assert before["pre"]["owner_hash"] == after["pre"]["owner_hash"]
    assert before["pre"]["history"] == after["pre"]["history"]
    for field in ["streams", "history_stored", "history_delivered"]:
        assert before["actual_result"][field] == after["actual_result"][field]
    proof = after["actual_result"]["read"]["claim_selection_provenance"]
    assert (
        proof["selected_claim_ref"]
        == proof["verified_binding"]["basis"]["canonical_claim_ref"]
    )
    assert proof["response_as_of"] == "1998-11-20T09:00:00Z"
    factorial.append(
        {
            "arm": after["arm"],
            "actual_streams": after["actual_result"]["streams"],
            "owner_state_sha256": sha(
                json.dumps(after["pre"]["owner_state"], sort_keys=True).encode()
            ),
            "same_before_after_owner_bytes": True,
            "same_before_after_history_bytes": True,
            "actual_as_of": proof["response_as_of"],
            "actual_disposition": proof["disposition"],
            "actual_effect_provenance": proof["actual_effect_provenance"],
            "before_receipt": str(p.relative_to(R)),
            "after_receipt": "evidence/after/independent_100/observations/" + p.name,
        }
    )
assert len(factorial) == 36
write("05_FACTORIAL_AND_TEMPORAL_RECEIPTS.json", factorial)

admissibility = []
for p in sorted((R / "evidence/author/observations").glob("*.json")):
    d = json.loads(p.read_text())
    if "typed_refusal" in d:
        assert d["rollback_exact"] is True and d["before"] == d["after"]
        admissibility.append(
            {
                "case": p.stem,
                "typed_refusal": d["typed_refusal"],
                "exact_checkpoint_rollback": True,
                "receipt": str(p.relative_to(R)),
            }
        )
write(
    "06_ADMISSIBILITY_AND_ROLLBACK.json",
    {
        "observed_denials": admissibility,
        "all_74_author_case_status": [
            {"name": k[2], "status": v} for k, v in author.items()
        ],
        "literal_provenance_red_closure": red,
        "internal_rollback_correction": "evidence/author_initial_rollback_failure",
        "initial_author_result": {"tests": 70, "pass": 69, "fail": 1},
        "public_restore": "reject invalid binding and restore its own pre-call snapshot atomically",
        "outer_selector_hint": "may be quarantined by restore; must refuse at consumption if unknown/foreign",
        "internal_rollback": "restore exact internally captured snapshot without endorsing corrupt preexisting metadata",
    },
)

# Exact frozen code and expectations remain unchanged. The candidate overlay is explicit.
identities = load("01_INPUT_SOURCE_IDENTITIES.json")
input_rows = identities["source_files"]
for row in input_rows:
    p = R / row["local"]
    assert (
        sha(p.read_bytes()) == row["sha256"]
        and blob(p.read_bytes()) == row["blob_sha1"]
    )
for p in (M1 / "repro").glob("*.py"):
    if p.name in ("cell.py", "claim_provenance.py"):
        continue
    assert p.read_bytes() == git("show", M01 + ":" + MP + "/repro/" + p.name), p.name
assert (
    sha((M2 / "repro/test_independent.py").read_bytes())
    == "2aff8954d22ea8124e7fc9242a93b93f0322ccf5c451a3f17796ed9a38860f99"
)
assert (
    sha((M2 / "01_INDEPENDENT_EXPECTATIONS.json").read_bytes())
    == "00e7090baacc67f845936f1e40bc2b602202bae5019d11b79f92d0df557fa4a4"
)
inherited_refs = json.loads((M1 / "02_SOURCE_IDENTITIES.json").read_text())
known = {row["blob_sha1"]: row for row in inherited_refs}
known[blob((M1 / "repro/test_m01.py").read_bytes())] = {
    "commit": M01,
    "path": MP + "/repro/test_m01.py",
}
can2_test = {
    "commit": "ee6a48b40247b113c614fe2099d4c443e8dd7bb7",
    "path": "WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/repro/test_repair.py",
}
known[blob(git("show", can2_test["commit"] + ":" + can2_test["path"]))] = can2_test
literal_source_refs = []
for suite in ("new", "can3", "author", "owners"):
    execution = load("evidence/after/original_413/" + suite + "/execution.json")
    for arg in execution["pytest_args"]:
        if not arg.endswith(".py"):
            continue
        rel = arg.split("RETURN>/", 1)[-1].split("RETURN]/", 1)[-1]
        p = M1 / rel
        data = p.read_bytes()
        row = known[blob(data)]
        assert data == git("show", row["commit"] + ":" + row["path"])
        literal_source_refs.append(
            {
                "suite": suite,
                "actual_executed_file": str(p.relative_to(R)),
                "source_commit": row["commit"],
                "source_path": row["path"],
                "blob_sha1": blob(data),
                "sha256": sha(data),
            }
        )
write("evidence/LITERAL_EXECUTED_TEST_SOURCE_REFS.json", literal_source_refs)
original_imports = {
    x["module"]: x
    for x in load("evidence/before/original_413/new/execution.json")["imports"]
}
patched_imports = load("evidence/after/original_413/new/execution.json")["imports"]
imports = []
for row in patched_imports:
    p = M1 / row["file"]
    data = p.read_bytes()
    assert blob(data) == row["blob_sha1"] and sha(data) == row["sha256"]
    if row["module"] != "cell":
        assert row["blob_sha1"] == original_imports[row["module"]]["blob_sha1"]
        assert data == git("cat-file", "blob", row["blob_sha1"])
    imports.append(
        dict(
            row,
            actual_import_file=str(p.relative_to(R)),
            source_kind=(
                "M03_OWNED_PATCH"
                if row["module"] == "cell"
                else "EXACT_PINNED_ORIGINAL"
            ),
        )
    )
installation = load("evidence/CANDIDATE_INSTALLATION.json")
for row in installation["files"]:
    assert (R / row["candidate"]).read_bytes() == (
        R / row["effective_module"]
    ).read_bytes()
    assert blob((R / row["candidate"]).read_bytes()) == row["blob_sha1"]
actual = load("evidence/author/observations/actual_imports.json")
for name, row in actual["files"].items():
    data = (R / row["file"]).read_bytes()
    assert blob(data) == row["blob_sha1"] and sha(data) == row["sha256"]
trace = load("evidence/after/independent_100/actual_function_calls.json")
assert trace["no_response_monkeypatch"] is True
assert (
    trace["production_guard"]["registry_empty"]
    and trace["production_guard"]["byte_unchanged"]
)
assert (
    trace["production_guard"]["blob_sha1"] == "e0528d65215cb431196570c38bac4eae94217a1b"
)
for path, row in trace["physical_function_sources"].items():
    assert blob((M2 / path).read_bytes()) == row["git_blob_sha1"]
for law, pin in [
    ("CAN008_R2", "b80dd6925066510ecbbfec7b427bf9f688475663"),
    ("ADP016", "c6619a286e115d060ab4830889e7fc23762167a5"),
    ("ADP017", "eece4f3f2f3f9288ab9bbc645dc81e20a99e1280"),
]:
    assert (M1 / "runtime/can3/runtime/law" / f"{law}.txt").read_bytes() == git(
        "cat-file", "blob", pin
    )
write(
    "07_SOURCE_AND_IMPORT_AUDIT.json",
    {
        "imports": imports,
        "helper_actual_import": actual["files"]["claim_provenance"],
        "actual_rule_source_hash": actual["source_hash"],
        "installation": installation,
        "unchanged_frozen_M02_test_sha256": sha(
            (M2 / "repro/test_independent.py").read_bytes()
        ),
        "original_test_and_rule_bytes_unchanged": True,
        "production_guard": trace["production_guard"],
        "physical_source_traces_verified": True,
        "source_hash_includes_helper_body": True,
        "actual_body_mutation_receipt": "evidence/author/observations/provenance_source_body_mutation.json",
        "pinned_input_source_manifest": "01_INPUT_SOURCE_IDENTITIES.json",
    },
)

# Bounds and writes are checked against the sealed start, including untracked return files.
changed = set(git("diff", "--name-only", SEAL).decode().splitlines()) | set(
    git("ls-files", "--others", "--exclude-standard").decode().splitlines()
)
assert all(p.startswith(str(R.relative_to(ROOT)) + "/") for p in changed), changed
write(
    "03_EXECUTED_RESULTS.json",
    {
        "verdict": "SOURCEFREE_CLAIM_PROVENANCE_REPAIR_CANDIDATE_ONLY",
        "baseline": {
            "original_413": {"pass": 413, "fail": 0},
            "independent_100": {"pass": 98, "fail": 2},
        },
        "final": {
            "original_413": {"pass": 413, "fail": 0},
            "independent_100": {"pass": 100, "fail": 0},
            "new_author": {"pass": 74, "fail": 0},
            "literal_total": 513,
            "literal_pass": 513,
            "all_current_pass": 587,
            "historical_nine_separate": {"pass": 0, "fail": 9, "errors": 0},
        },
        "two_red_closure": red,
        "source_owner_bytes_and_factorial_unchanged": True,
        "factorial_arms": 36,
        "production_guard_empty": True,
        "new_semantic_issuance": False,
        "serial_mediation": "HOLD",
        "real_competent_production_owner": "HOLD",
        "human_calibrated_behavior": "HOLD",
        "future_independent_reviewer": "HQ_M04_REQUIRED; current worker is author, also previously authored M02 review in this chat",
        "changed_paths_within_assigned_return": True,
        "current_candidate_source_hash": actual["source_hash"],
    },
)

marker = (R / "runtime/runtime_marker.json").read_bytes()
m = json.loads(marker)
probes = {}
for name, cmd in [
    ("python", [sys.executable, "--version"]),
    ("pytest", [sys.executable, "-m", "pytest", "--version"]),
    ("git", ["git", "--version"]),
    ("shell", ["zsh", "--version"]),
]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    probes[name] = {
        "capability": "VERIFIED" if p.returncode == 0 else "UNAVAILABLE",
        "result": (p.stdout + p.stderr).strip(),
        "exit": p.returncode,
    }
refs = []
for row in imports:
    if row["module"] == "cell":
        commit = None
        path = "candidate/cell.py"
        kind = "M03_OWNED_PATCH_PENDING_RETURN_COMMIT"
    elif row["module"] == "bootstrap":
        commit = M01
        path = MP + "/repro/bootstrap.py"
        kind = "PINNED_ORIGINAL"
    else:
        source = known[row["blob_sha1"]]
        commit = source["commit"]
        path = source["path"]
        kind = "PINNED_ORIGINAL"
        assert (
            git("rev-parse", commit + ":" + path).decode().strip() == row["blob_sha1"]
        )
    refs.append(
        {
            "module": row["module"],
            "local_relative_staging_path": row["actual_import_file"],
            "module_file_verified": row["actual_import_file"],
            "git_blob_sha1": row["blob_sha1"],
            "source_kind": kind,
            "source_commit": commit,
            "source_path": path,
        }
    )
refs.append(
    {
        "module": "claim_provenance",
        "local_relative_staging_path": actual["files"]["claim_provenance"]["file"],
        "module_file_verified": actual["files"]["claim_provenance"]["file"],
        "git_blob_sha1": actual["files"]["claim_provenance"]["blob_sha1"],
        "source_kind": "M03_OWNED_PATCH_PENDING_RETURN_COMMIT",
        "source_commit": None,
        "source_path": "candidate/claim_provenance.py",
    }
)

write(
    "environment_passport_delta.json",
    {
        "passport_schema": "SOROK_00D_R1",
        "environment_id": m["environment_id"],
        "epoch_id": m["epoch_id"],
        "owner_session_alias": "M03_AUTHOR_SINGLE_AGENT",
        "surface": "LOCAL_SHARED_STORE",
        "machine_alias": "LOCAL_AUTHORIZED_HOST",
        "conversation_or_account_affinity": "THIS_CHAT; no external account continuity assertion",
        "status": "LIVE_VERIFIED",
        "last_live_probe_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runtime_marker_digest": sha(marker),
        "probe_command_and_result": probes,
        "node": {"capability": "UNKNOWN", "reason": "not required; not probed"},
        "filesystem": {
            "capability": "VERIFIED",
            "scope": "owned sparse worktree return and synthetic runtime",
        },
        "dependency_versions": {
            "python": platform.python_version(),
            "pytest": probes["pytest"]["result"],
        },
        "git_object_store_alias": "AUTHORIZED_EXISTING_REPO_SHARED_OBJECT_STORE",
        "worktree_alias": "M03_ISOLATED_SPARSE",
        "branch": git("branch", "--show-current").decode().strip(),
        "checkout_base": SEAL,
        "observed_head": git("rev-parse", "HEAD").decode().strip(),
        "clean_dirty_state": "AUTHOR_RETURN_PENDING_COMMIT; final clean check in direct remote verification",
        "source_family": "M01/M02/CAN3/CAN2 finite sourcefree",
        "materialized_source_refs": refs,
        "candidate_and_helper_refs": "07_SOURCE_AND_IMPORT_AUDIT.json",
        "dependency_closure_status": "BOUNDED",
        "fixture_source_permission": "USER_COMMISSION_SOURCEFREE_TEST_ONLY",
        "covered_test_suites": [
            {
                "run_junit_ref": str(p.relative_to(R)),
                "command_receipt": str(p.parent.relative_to(R)) + "/command.json",
            }
            for p in (R / "evidence/after").rglob("junit.xml")
        ]
        + [
            {
                "run_junit_ref": "evidence/author/junit.xml",
                "command_receipt": "evidence/author/command.json",
            },
            {
                "run_junit_ref": "evidence/historical_nine/junit.xml",
                "command_receipt": "evidence/historical_nine/command.json",
                "status": "9 literal historical FAIL, expected and separate",
            },
        ],
        "science_grade": "SOURCEFREE_REPAIR_CANDIDATE_ONLY",
        "model_provider": "OpenAI/Codex; user-selected model",
        "model": "GPT-6.1 High as commissioned; no switches or helpers",
        "effort": "High",
        "pricing_class": "UNKNOWN",
        "credits_usage": None,
        "cash": "UNKNOWN",
        "quota_reset": "UNKNOWN",
        "independent_review_separation": "M03_AUTHOR; previously M02 reviewer in same chat; future M04 by HQ distinct required",
        "privacy_source_grant": "private repository, local synthetic fixture closure only",
        "assignments_completed": [
            "M03 sourcefree candidate implementation and author verification; pending final push verification"
        ],
        "next_good_affinity_tags": [
            "CAN008",
            "TEMPORAL",
            "CLAIM_PROVENANCE",
            "AUTHOR_REPAIR",
        ],
        "staged_state_preservation": {
            "status": "WARM_STATIC_MODULES_VERIFIED; subprocess owner states reconstructed per case",
            "reuse": identities["warm_source_status"],
            "mutable_process_continuity_claim": False,
            "available_for_more_work": "local runtime present at probe; next worker must re-probe marker/imports",
        },
        "retire_or_rebuild_reason": None,
    },
)
print(
    "AUDIT_OK: 513 literal PASS; 74 author PASS; 9 historical RED; 36 unchanged owner-state arms; exact imports and scope verified"
)
