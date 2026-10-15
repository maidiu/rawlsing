"""Requirement-scoped evidence audit; retain true REDs and source/actor ceilings."""

from pathlib import Path
from collections import Counter
import csv, datetime, hashlib, json, os, platform, shutil, subprocess, sys, uuid, xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
M = R / "runtime/m01"
PRE = "845edf5d7c9c48b192b631dacf295afa6f587137"
M01 = "02187a14e75ff30dd953d3c7185d689b80e62304"
SEAL = "6d0224d40a28d9a2f07b105b2ec3aef849c305ef"
FREEZE = "0c875790f"
P = "WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def read(rel):
    return json.loads((R / rel).read_text())


def write(rel, obj):
    (R / rel).write_text(json.dumps(obj, indent=2) + "\n")


def bh(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def sh(b):
    return hashlib.sha256(b).hexdigest()


def clean(text):
    return (
        text.replace(str(R), "<RETURN>")
        .replace(str(ROOT), "<WORKTREE>")
        .replace(str(Path.home()), "<HOME>")
    )


# Preserve raw artifacts locally; sanitize portable metadata, never test bodies.
raw = R / "runtime/raw_portable"
raw.mkdir(exist_ok=True)
privacy = (
    read("evidence/PORTABILITY_SANITIZATION.json")
    if (R / "evidence/PORTABILITY_SANITIZATION.json").exists()
    else []
)
log = R / "runtime/historical_nine_raw.log"
(R / "evidence/historical_nine/stdout.log").write_text(clean(log.read_text()))
for p in list((R / "evidence").rglob("*")):
    if not p.is_file():
        continue
    before = p.read_bytes()
    if p.suffix == ".xml":
        tree = ET.fromstring(before)
        changed = False
        for suite in tree.iter("testsuite"):
            if "hostname" in suite.attrib:
                suite.attrib.pop("hostname")
                changed = True
        after = ET.tostring(tree, encoding="utf-8", xml_declaration=True)
        after = clean(after.decode()).encode()
        if after != before:
            dest = raw / p.relative_to(R / "evidence")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(before)
            p.write_bytes(after)
            privacy.append(
                {
                    "file": str(p.relative_to(R)),
                    "raw_sha256": sh(before),
                    "portable_sha256": sh(after),
                    "changes": "remove hostname metadata; normalize local absolute prefixes; XML serialization only",
                }
            )
    elif p.suffix in (".log", ".json", ".md", ".txt", ".stdout"):
        after = clean(before.decode()).encode()
        if after != before:
            p.write_bytes(after)
            privacy.append(
                {
                    "file": str(p.relative_to(R)),
                    "raw_sha256": sh(before),
                    "portable_sha256": sh(after),
                    "changes": "normalize local absolute path prefixes only",
                }
            )
write("evidence/PORTABILITY_SANITIZATION.json", privacy)


def results(path):
    rows = []
    for case in ET.parse(R / path).getroot().iter("testcase"):
        node = next(
            (
                case.find(t)
                for t in ("failure", "error", "skipped")
                if case.find(t) is not None
            ),
            None,
        )
        rows.append(
            {
                "name": case.attrib["name"],
                "state": "PASS" if node is None else node.tag.upper(),
                "message": None if node is None else node.attrib.get("message"),
            }
        )
    return {"counts": dict(Counter(x["state"] for x in rows)), "cases": rows}


suites = {
    name: results("evidence/original_413/" + name + "/junit.xml")
    for name in ["new", "can3", "author", "owners"]
}
for name, n in [("new", 94), ("can3", 97), ("author", 89), ("owners", 133)]:
    assert suites[name]["counts"] == {"PASS": n}
ind = results("evidence/independent/junit.xml")
nine = results("evidence/historical_nine/junit.xml")
cor = results("evidence/corroboration/junit.xml")
assert (
    ind["counts"] == {"PASS": 98, "FAILURE": 2}
    and nine["counts"] == {"FAILURE": 9}
    and cor["counts"] == {"FAILURE": 2}
)
new_red = {x["name"] for x in ind["cases"] if x["state"] == "FAILURE"}
assert new_red == {
    "test_lawful_future_claim_cannot_condition_an_earlier_response",
    "test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence",
}
assert {x["name"] for x in nine["cases"]} == {
    x["name"]
    for x in read("evidence/historical_nine/execution.json")["exact_original_cases"]
}
write(
    "03_EXECUTED_RESULTS.json",
    {
        "verdict": "REVIEW_REVISE",
        "original_413": suites,
        "independent_100": ind,
        "fresh_process_two_RED_corroboration": cor,
        "nine_literal_historical_RED_rerun": nine,
        "full_CAN3_585_rerun": False,
        "original_tests_modified_or_inverted": False,
        "stronger_serial_and_production": "MECHANISM_IDENTIFICATION_HOLD",
    },
)
# Git chronology and source custody, not an external trusted time certificate.
prereg = git("show", PRE + ":" + P + "/01_PREREGISTRATION.md")
assert (
    prereg
    == git("show", M01 + ":" + P + "/01_PREREGISTRATION.md")
    == (M / "01_PREREGISTRATION.md").read_bytes()
)
assert (
    subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", PRE, M01]
    ).returncode
    == 0
)
for missing in ["repro/cell.py", "repro/test_m01.py"]:
    assert (
        subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", PRE + ":" + P + "/" + missing],
            capture_output=True,
        ).returncode
        != 0
    )
for p in (M / "repro").glob("*.py"):
    assert p.read_bytes() == git("show", M01 + ":" + P + "/repro/" + p.name), p
frozen_json = (R / "01_INDEPENDENT_EXPECTATIONS.json").read_bytes()
assert (
    sh(frozen_json)
    == "00e7090baacc67f845936f1e40bc2b602202bae5019d11b79f92d0df557fa4a4"
)
assert (
    git(
        "show",
        FREEZE + ":" + str((R / "01_INDEPENDENT_EXPECTATIONS.json").relative_to(ROOT)),
    )
    == frozen_json
)
write(
    "04_CHRONOLOGY_AND_CUSTODY.json",
    {
        "M01_prereg_commit": PRE,
        "M01_final": M01,
        "M01_prereg_blob": bh(prereg),
        "prereg_unchanged": True,
        "prereg_ancestor_of_final": True,
        "cell_and_new_test_absent_at_prereg": True,
        "first_published_new_source_and_evidence": "88a08925803a40eb3324da3013635ace6456f7e9",
        "git_history": git(
            "log", "--format=%H %aI %cI %s", "--reverse", PRE + ".." + M01, "--", P
        )
        .decode()
        .splitlines(),
        "reviewer_freeze_commit": git("rev-parse", FREEZE).decode().strip(),
        "reviewer_freeze_json_sha256": sh(frozen_json),
        "chronology_ceiling": "Git ancestry, exact blobs and recorded commit times; not a notarized external timestamp or proof of hidden pre-publication activity",
        "no_M01_source_edits": True,
    },
)
known = read("02_SOURCE_IDENTITIES.json")
by_blob = {}
for row in known:
    by_blob.setdefault(row["blob_sha1"], []).append(
        {k: row[k] for k in ("commit", "path", "blob_sha1", "sha256") if k in row}
    )
imports = []
for name in suites:
    ex = read("evidence/original_413/" + name + "/execution.json")
    assert ex["guard_byte_unchanged"] and ex["guard_empty"]
    for row in ex["imports"]:
        p = M / row["file"]
        b = p.read_bytes()
        assert bh(b) == row["blob_sha1"] and sh(b) == row["sha256"]
        assert bh(b) in by_blob, (name, row)
        imports.append(
            {
                "suite": name,
                "module": row["module"],
                "module_file": str(p.relative_to(R)),
                "blob_sha1": bh(b),
                "source_refs": by_blob[bh(b)],
            }
        )
observed = read("evidence/independent/actual_function_calls.json")
for row in observed["module_imports"]:
    p = R / row["module_file"]
    b = p.read_bytes()
    assert bh(b) == row["git_blob_sha1"] and sh(b) == row["sha256"]
    assert bh(b) in by_blob, row
    imports.append(
        {
            "suite": "independent",
            "module": row["module"],
            "module_file": row["module_file"],
            "blob_sha1": bh(b),
            "source_refs": by_blob[bh(b)],
        }
    )
for rel, identity in observed["physical_function_sources"].items():
    p = R / rel
    b = p.read_bytes()
    assert bh(b) == identity["git_blob_sha1"] and bh(b) in by_blob
assert (
    observed["production_guard"]["registry_empty"]
    and observed["production_guard"]["byte_unchanged"]
)
write(
    "05_PHYSICAL_IMPORT_AND_FUNCTION_AUDIT.json",
    {
        "imports": imports,
        "actual_function_event_count": len(observed["actual_function_events"]),
        "actual_function_sources": observed["physical_function_sources"],
        "no_response_monkeypatch_in_reviewer_science": True,
        "inherited_instrumentation": "Original unchanged CAN3/RCP tests include their historical observer/patch instrumentation; new reviewer state arms use actual methods with sys.setprofile observation only",
        "production_guard": observed["production_guard"],
    },
)
# Factorial values come from actual execution, checked against the unchanged freeze.
freeze = json.loads(frozen_json)
matrix = []
event_ids = set()
state_history = {}
for arm in freeze["arms"]:
    name = "factorial_" + arm["memory"] + "_" + arm["epistemic"] + "_" + arm["history"]
    d = read("evidence/independent/observations/" + name + ".json")
    o = d["actual_result"]
    assert (
        o["streams"] == arm["expected_streams"]
        and d["pre"]["owner_state"]
        == o["read"]["actual_state"]
        == d["post"]["owner_state"]
    )
    event_ids.add(
        (
            d["first_admitted_event"]["event_id"],
            d["first_admitted_event"]["event_hash"],
            o["receipt"]["payload"]["event"]["event_id"],
            o["receipt"]["payload"]["event"]["event_hash"],
        )
    )
    state_history.setdefault((arm["memory"], arm["epistemic"]), []).append(
        d["pre"]["owner_state"]
    )
    case = (
        "test_independent_36_arm_actual_state_to_response["
        + arm["memory"]
        + "_"
        + arm["epistemic"]
        + "_"
        + arm["history"]
        + "]"
    )
    calls = [r for r in observed["actual_function_events"] if r["case"] == case]
    assert any(
        x["function"] == "read_owner"
        and x["event"] == "return"
        and x.get("streams") == o["streams"]
        for x in calls
    )
    assert any(
        x["function"] == "commit"
        and x["event"] == "call"
        and x.get("kind") == "M01_CAN008_CURRENT_RESPONSE_GRAPH"
        for x in calls
    )
    matrix.append(
        {
            **{k: arm[k] for k in ("memory", "epistemic", "history")},
            "actual_memory_stream": o["streams"]["memory"],
            "actual_epistemic_stream": o["streams"]["epistemic"],
            "expected_match": True,
            "owner_hash": d["pre"]["owner_hash"],
            "response_entry_hash": o["receipt"]["entry_hash"],
            "history_stored_rows": len(o["history_stored"]),
            "history_delivered_rows": len(o["history_delivered"]),
        }
    )
assert (
    len(matrix) == 36
    and len(event_ids) == 1
    and all(v[0] == v[1] == v[2] for v in state_history.values())
)
with (R / "evidence/factorial_36.csv").open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(matrix[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(matrix)
exact_epi = []
for ep in ["NONE", "BELIEF", "INACCESSIBLE"]:
    d = read("evidence/independent/observations/same_id_content_" + ep + ".json")
    a = d["left"]["read"]["actual_state"]
    b = d["right"]["read"]["actual_state"]
    keys = [
        "claims",
        "emissions",
        "stances",
        "epistemic_transitions",
        "state_sets",
        "permissions",
    ]
    assert all(a[k] == b[k] for k in keys)
    exact_epi.append(
        {
            "epistemic": ep,
            "all_six_epistemic_components_identical": True,
            "memory_ids_identical": list(a["memories"]) == list(b["memories"]),
            "observed_memory_response": [
                d["left"]["streams"]["memory"],
                d["right"]["streams"]["memory"],
            ],
        }
    )
write(
    "06_CAUSAL_COUNTERFACTUALS.json",
    {
        "36_actual_arms": matrix,
        "identical_event_identity_and_time_across_arms": len(event_ids) == 1,
        "all_12_full_owner_history_invariance_contrasts": True,
        "full_epistemic_state_fixed_native_memory_contrasts": exact_epi,
        "lawful_parallel_construction_supported": True,
        "serial_ADP016_to_ADP017_identified": False,
        "serial_verdict": "MECHANISM_IDENTIFICATION_HOLD",
        "psychological_discovery": False,
        "new_RED_scope": "Adversarial outer Cell claim-selector/checkpoint binding; not a lawful mediator arm. Positive fixed-selector factorial does not cover this boundary.",
    },
)
# Accepted authority bytes and non-production scope.
law_rows = []
for name, pin in [
    ("CAN008_R2", "b80dd6925066510ecbbfec7b427bf9f688475663"),
    ("ADP016", "c6619a286e115d060ab4830889e7fc23762167a5"),
    ("ADP017", "eece4f3f2f3f9288ab9bbc645dc81e20a99e1280"),
]:
    p = M / "runtime/can3/runtime/law" / (name + ".txt")
    b = p.read_bytes()
    assert bh(b) == pin
    assert (
        subprocess.check_output(
            ["git", "-C", str(ROOT), "hash-object", "--stdin"], input=b
        )
        .decode()
        .strip()
        == pin
    )
    law_rows.append(
        {
            "authority": name,
            "git_blob_sha1": pin,
            "sha256": sh(b),
            "local": str(p.relative_to(R)),
            "authority_scope": "accepted normative semantics, not operative production implementation",
        }
    )
adoption = git("cat-file", "blob", "a6bc1555489271e1adb2271ed02d46bb7f888170")
assert bh(adoption) == "a6bc1555489271e1adb2271ed02d46bb7f888170"
(R / "evidence/CAN008_R2_ADOPTION_EXCERPT.md").write_text(adoption.decode())
write(
    "07_AUTHORITY_SCOPE_AND_REDS.json",
    {
        "verdict": "REVIEW_REVISE",
        "authority_blobs": law_rows,
        "CAN008_adoption_blob": "a6bc1555489271e1adb2271ed02d46bb7f888170",
        "nine_original_RED_cases": nine["cases"],
        "nine_original_adjudication_custody": "ef12349defe22a50e053a7a8080a67ab45673417:WORKER_RETURNS/SOROK-R3-HQ309-CAN3-CAN008-INDEPENDENT-R1/04_NINE_RED_ADJUDICATION.md",
        "new_RED_cases": [x for x in ind["cases"] if x["state"] == "FAILURE"],
        "operative_rule_issuer_registry_conditioning_and_target_owners": "NOT_ISSUED",
        "serial_memory_content_to_belief": "MECHANISM_IDENTIFICATION_HOLD",
        "real_actor_model_V3_permission": "NOT_GRANTED",
        "production_guard_empty": True,
    },
)
source = M / "runtime/can3/04_NINE_RED_ADJUDICATION.md"
shutil.copyfile(source, R / "evidence/historical_nine/original_CAN3_adjudication.md")
marker = (R / "runtime/runtime_marker.json").read_bytes()
mark = json.loads(marker)
import pytest

write(
    "environment_passport_delta.json",
    {
        "passport_schema": "SOROK_00D_ENVIRONMENT_PASSPORT_R1",
        "environment_id": mark["environment_id"],
        "epoch_id": mark["epoch_id"],
        "owner_session_alias": "M02_INDEPENDENT_REVIEW",
        "surface": "LOCAL_SHARED_STORE",
        "machine_alias": "AUTHORIZED_LOCAL",
        "conversation_or_account_affinity": "USER_SELECTED_CODEX",
        "status": "LIVE_VERIFIED",
        "last_live_probe_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runtime_marker_digest": sh(marker),
        "probe_command_and_result": {
            "python": platform.python_version(),
            "pytest": pytest.__version__,
            "git": git("--version").decode().strip(),
            "filesystem_shell": "VERIFIED isolated sparse worktree, local Python subprocess and assigned return writes",
            "node": "NOT_NEEDED_NOT_PROBED",
        },
        "capabilities": {
            "python": "VERIFIED",
            "pytest": "VERIFIED",
            "git": "VERIFIED",
            "authenticated_remote": "VERIFIED direct assigned startup ls-remote",
            "requested_model": "USER_REPORTED; no switch",
        },
        "git_object_store_alias": "EXISTING_SHARED_RAWLSING_STORE",
        "worktree_alias": "M02_MEMORY_CAUSAL_COURT",
        "branch": git("branch", "--show-current").decode().strip(),
        "checkout_base": SEAL,
        "head_at_probe": git("rev-parse", "HEAD").decode().strip(),
        "clean_dirty": "RETURN_PENDING_FINAL_COMMIT",
        "source_family": "SOURCEFREE_SYNTHETIC_ONLY",
        "materialized_source_refs": imports,
        "dependency_closure_status": "BOUNDED_FULL_FOR_COMMISSIONED_SUITES",
        "fixture_query_source_permission": "COMMISSION_TEST_ONLY_PRIVATE_REPO_LOCAL",
        "covered_test_suites": {
            "original_413": read("evidence/original_413_execution.json"),
            "independent_100": ind["counts"],
            "corroboration": cor["counts"],
            "nine_original_RED": nine["counts"],
        },
        "science_grade": "REVIEW_REVISE; fixed-selector sourcefree parallel construction positive, provenance boundary RED",
        "model_provider": "OpenAI Codex user-selected",
        "model": "GPT-6.1 High (USER_REPORTED commission)",
        "effort": "High (USER_REPORTED)",
        "pricing_class": "UNKNOWN",
        "credits_usage": None,
        "cash_known": False,
        "quota_known": False,
        "context_cache_reuse": "UNKNOWN",
        "estimated_total_evidence_cost": "UNKNOWN",
        "independent_review_separation": "Reviewer did not author M01 or CAN2. Separate new worktree/epoch; conversation had unrelated PYAT work earlier. Not a claim of an empty prior chat, institutional issuer independence or blindness to published results. No helpers/model calls/switches.",
        "privacy_source_grant": "Private repository sourcefree local review only; no source survey/human actor/model/V3 operation",
        "nearest_expected_reset": None,
        "assignments_completed": ["M02 independent scientific review"],
        "next_good_affinity_tags": [
            "CAN008",
            "ADP016",
            "ADP017",
            "CAUSAL_SELECTION_PROVENANCE",
            "K3",
            "K5",
        ],
        "staged_state_preservation": "Original source closure and evidence warm locally; synchronous per-cell state; no crash durability or cross-process state restoration claim",
        "retire_or_rebuild_reason": None,
    },
)
# Reproducible native-source/privacy/scope completion checks.
assert all(
    p.startswith(str(R.relative_to(ROOT)) + "/")
    for p in git("diff", "--name-only", SEAL).decode().splitlines()
)
for p in (R / "evidence").rglob("*"):
    if p.is_file():
        assert "/Users/" not in p.read_text(), p
print(
    "AUDIT_VERIFIED_413_PASS__INDEPENDENT_98_PASS_2_RED__HISTORICAL_9_RED__VERDICT_REVIEW_REVISE"
)
