"""Generate S44 root-generation, replay, fault and live-consumer evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

RET = Path(__file__).resolve().parent
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = str(RET)
ENV.setdefault(
    "M35_JOIN_E_RETURN",
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
    "SOROK-20261022-SAME-PERSON-JOIN-R1",
)
for path in (str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s44.bootstrap import CUTS, install, roots  # noqa: E402

install()

from s42.session import S42Session  # noqa: E402
from s44.bundle import default_bundle, normalize_bundle  # noqa: E402
from s44.errors import S44Refusal  # noqa: E402
from s44.root import generate_root  # noqa: E402
from s44.session import ROOT_FILE, S44Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402

S43_RETURN = Path(roots()["s43_return"])
S42_RETURN = Path(roots()["s42_return"])
S43_FILES = [
    "s43/__init__.py", "s43/bootstrap.py", "s43/errors.py", "s43/fixtures.py",
    "s43/performer.py", "s43/planner.py", "s43/reader.py", "s43/registry.py",
    "s43/repertoire.py", "s43/session.py",
]
S44_FILES = [
    ".gitignore", "00_RETURN.md", "run_s44.py", "run_s44_evidence.py",
    "s44/__init__.py", "s44/bootstrap.py", "s44/bundle.py", "s44/errors.py",
    "s44/rng.py", "s44/root.py", "s44/session.py",
    "tests/conftest.py", "tests/test_s44_sampled_root.py",
]
STRUCTURAL_FILES = [
    "/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing/rawlsing_next/"
    "m5_runtime_rsc_peer_prior.py",
    "/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing/rawlsing_next/"
    "source_backed_positioned_subject_possibility.py",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(RET), capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, log_name: str, env=None):
    proc = subprocess.run(cmd, cwd=str(RET), env=env or ENV,
                          capture_output=True, text=True)
    (LOGS / log_name).write_text(proc.stdout + proc.stderr)
    return proc


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    cases = []
    for case in root.iter("testcase"):
        status = "PASS"
        if case.find("failure") is not None:
            status = "RED"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        cases.append({"classname": case.attrib.get("classname", ""),
                      "name": case.attrib.get("name", ""), "status": status})
    return {"tests": tests, "PASS": tests - failures - errors - skips,
            "RED": failures, "ERROR": errors, "SKIP": skips, "cases": cases}


def _bundle(seed="11" * 32):
    return default_bundle(root_seed=seed)


def _reverse_candidates(bundle):
    body = deepcopy(bundle)
    for rule in body["rules"].values():
        if isinstance(rule.get("candidates"), list):
            rule["candidates"] = list(reversed(rule["candidates"]))
    body.pop("bundle_hash", None)
    return normalize_bundle(body)


def _count_b_speech(session):
    return len([
        event for event in session.events()
        if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
    ])


def _draw_summary(root):
    return {
        "rule_name": root.receipt["draw_receipts"][0]["rule_name"],
        "draw_count": len(root.receipt["draw_receipts"]),
        "rules": [
            {
                "rule_name": row["rule_name"],
                "rule_id": row["semantic_rule_id"],
                "rule_version": row["semantic_rule_version"],
                "stream_name": row["stream_name"],
                "operation": row["operation"],
                "selected_value": row.get("selected_value"),
                "candidate_set_hash": row.get("candidate_set_hash", ""),
                "draw_consumed": row.get("draw_consumed"),
                "replay_identity": row["decision_replay_identity_hash"],
                "conditioned_on_value": row.get("conditioned_on_value"),
            }
            for row in root.receipt["draw_receipts"]
        ],
    }


def root_evidence():
    baseline = generate_root(_bundle("11" * 32))
    replayed = generate_root(_bundle("11" * 32))
    reordered = generate_root(_reverse_candidates(_bundle("11" * 32)))
    extra = _bundle("11" * 32)
    extra["rules"]["unused_observation"] = {
        "rule_id": "S44_UNUSED_OBSERVATION",
        "rule_version": "1",
        "registry_hash": "TEST_ONLY_UNUSED",
        "stream": "v3.causal.s44.unused.observation",
        "scope_kind": "RUN", "scope_id": "S44_ROOT",
        "operation": "WEIGHTED_CANDIDATE_INTEGER",
        "candidate_owner_authority": "TEST_ONLY_UNUSED",
        "candidates": [{"candidate_id": "unused_1", "value": 1,
                        "weight_units": 1,
                        "source_ref": "TEST_ONLY_UNUSED_SOURCE"}],
    }
    with_extra = generate_root(extra)
    seeds = {}
    for index in range(20):
        root = generate_root(_bundle(f"{index:02x}" * 32))
        seeds[f"{index:02x}" * 32] = {
            "root_hash": root.root_hash,
            "selected": [
                (row["rule_name"], row.get("selected_value"))
                for row in root.receipt["draw_receipts"]
            ],
            "branches": root.receipt["selected_branches"],
        }
    distinct = len({row["root_hash"] for row in seeds.values()})
    selected_distinct = len({
        tuple((name, str(value)) for name, value in row["selected"])
        for row in seeds.values()
    })
    return {
        "schema": "SOROK_S44_ROOT_EVIDENCE@1",
        "bundle_hash": baseline.bundle["bundle_hash"],
        "root_hash": baseline.root_hash,
        "root_id": baseline.receipt["root_id"],
        "root_seed_sha256": baseline.receipt["root_seed_sha256"],
        "actor_ids": baseline.receipt["actor_ids"],
        "source_hashes": baseline.receipt["source_hashes"],
        "event_refs": baseline.receipt["event_refs"],
        "g18_history_hashes": baseline.receipt["g18_history_hashes"],
        "snapshot_hashes": baseline.receipt["snapshot_hashes"],
        "selected_branches": baseline.receipt["selected_branches"],
        "initial_facts": baseline.receipt["initial_facts"],
        "joint": baseline.receipt["joint"],
        "draws": _draw_summary(baseline),
        "selected_finished_life": baseline.receipt["selected_finished_life"],
        "no_effect_branches": baseline.receipt["no_effect_branches"],
        "replay_exact": (
            baseline.root_hash == replayed.root_hash
            and baseline.receipt["event_refs"] == replayed.receipt["event_refs"]
            and baseline.receipt["draw_receipts"] == replayed.receipt["draw_receipts"]
        ),
        "candidate_order_isolated": (
            reordered.root_hash == baseline.root_hash
            and reordered.receipt["draw_receipts"] == baseline.receipt["draw_receipts"]
        ),
        "unrelated_stream_isolated": (
            with_extra.receipt["event_refs"] == baseline.receipt["event_refs"]
            and with_extra.receipt["snapshot_hashes"] == baseline.receipt["snapshot_hashes"]
            and [(r["rule_name"], r.get("selected_value"))
                 for r in with_extra.receipt["draw_receipts"]]
            == [(r["rule_name"], r.get("selected_value"))
                for r in baseline.receipt["draw_receipts"]]
        ),
        "seed_divergence": {
            "seeds_checked": len(seeds),
            "distinct_roots": distinct,
            "distinct_selected_sets": selected_distinct,
            "nondegenerate": distinct > 1 and selected_distinct > 1,
            "examples": {key: row["root_hash"] for key, row in list(seeds.items())[:4]},
        },
        "conditional_predecessors": baseline.receipt["selected_branches"]["conditions"],
        "product_model_calls": 0,
    }


def consumer_evidence(state):
    case = case_for(True)
    session = S44Session.start(
        state, bundle=_bundle("11" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )
    try:
        root = session.read_root()
        before_b = _count_b_speech(session)
        events = session.read_events()
        first_read = session.read_event(events[0]["e1_event_id"])
        second = session.admit_event(
            language_context={"milieu_id": "workshop"},
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        second_read = session.read_s43_event(second["event"]["e1_event_id"])
        after_b = _count_b_speech(session)
        verify = session.verify()
    finally:
        session.close()
    cold = S44Session.open(state)
    try:
        cold_root = cold.read_root()
        events = cold.read_events()
        third = cold.admit_event(
            language_context={"milieu_id": "workshop"},
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        cold_verify = cold.verify()
        final_events = cold.read_events()
        latest = cold.read_latest()
        clock = cold.clock()
        tools = cold.world().actor_state["A"]["tools_remaining"]
    finally:
        cold.close()
    lang = second["event"].get("language") or {}
    return {
        "schema": "SOROK_S44_CONSUMER_EVIDENCE@1",
        "root_hash": root["root_hash"],
        "bundle_hash": root["bundle_hash"],
        "actor_ids": root["actor_ids"],
        "source_hashes": root["source_hashes"],
        "root_event_ref_count": sum(len(v) for v in root["event_refs"].values()),
        "root_language_evidence": root["language_evidence"],
        "first_event": {
            "event_ordinal": events[0]["event_ordinal"],
            "status": events[0].get("status"),
            "selected_option": events[0].get("selected_option"),
            "e1_event_hash": events[0]["e1_event_hash"],
            "language_source_event_id": (
                first_read.get("language") or {}
            ).get("source_event_id", ""),
            "language_source_is_root_evidence": (
                (first_read.get("language") or {}).get("source_event_id")
                in {row["source_event_id"] for row in root["language_evidence"]}
            ),
        },
        "second_event": {
            "event_ordinal": second["event"]["event_ordinal"],
            "status": second["event"].get("status"),
            "selected_option": second["event"].get("selected_option"),
            "attempt_status": second["event"].get("attempt_status"),
            "performed": second["event"].get("performed"),
            "native_text": lang.get("native_text", ""),
            "translation_text": lang.get("translation_text", ""),
            "source_event_id": lang.get("source_event_id", ""),
            "source_is_root_evidence": lang.get("source_event_id")
            in {row["source_event_id"] for row in root["language_evidence"]},
            "c9": second["event"].get("c9"),
            "s43_selected_relation_ids": (
                second_read.get("s43") or {}
            ).get("selected_relation_ids", []),
        },
        "no_new_b_source_at_speaking": before_b == after_b,
        "cold_root_same": cold_root["root_hash"] == root["root_hash"],
        "cold_actor_ids_same": cold_root["actor_ids"] == root["actor_ids"],
        "third_event": {
            "event_ordinal": third["event"]["event_ordinal"],
            "status": third["event"].get("status"),
            "selected_option": third["event"].get("selected_option"),
            "attempt_status": third["event"].get("attempt_status"),
            "performed": third["event"].get("performed"),
        },
        "event_count": len(final_events),
        "latest_ordinal": latest["event_ordinal"],
        "clock": clock,
        "tools_remaining": tools,
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "target_proposals": [],
    }


def fault_evidence(state):
    case = case_for(True)
    session = S44Session.start(
        state, bundle=_bundle("66" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )
    root_hash = session.read_root()["root_hash"]
    session.close()
    root_path = state / ROOT_FILE
    original = root_path.read_text(encoding="utf8")
    document = json.loads(original)
    document["bundle"]["rules"]["a_material"]["candidates"][0]["weight_units"] = 99
    root_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                         encoding="utf8")
    try:
        S44Session.open(state)
        refused = ""
    except S44Refusal as exc:
        refused = exc.code
    root_path.write_text(original, encoding="utf8")
    restored = S44Session.open(state)
    try:
        restored_hash = restored.read_root()["root_hash"]
        restored_ok = restored.verify()["ok"]
    finally:
        restored.close()
    changed = _bundle("66" * 32)
    changed["rules"]["a_material"]["candidates"][0]["weight_units"] = 99
    changed_root = generate_root(changed)
    missing = _bundle("66" * 32)
    del missing["rules"]["a_material"]
    try:
        generate_root(missing)
        missing_code = ""
    except S44Refusal as exc:
        missing_code = exc.code
    return {
        "schema": "SOROK_S44_FAULT_EVIDENCE@1",
        "frozen_root_hash": root_hash,
        "changed_rule_refusal": refused,
        "restored_root_hash": restored_hash,
        "restored_exact": restored_hash == root_hash,
        "restored_verify": restored_ok,
        "changed_rule_root_changed": changed_root.root_hash != root_hash,
        "changed_rule_receipt_changed": (
            changed_root.receipt["selected_branches"]
            != generate_root(_bundle("66" * 32)).receipt["selected_branches"]
        ),
        "missing_rule_code": missing_code,
    }


def attention_evidence(state):
    case = case_for(True)
    session = S44Session.start(
        state, bundle=_bundle("77" * 32), case=case,
        source=source_for(case), attention="focused",
    )
    root = session.read_root()["root_hash"]
    first = session.read_events()[0]["e1_event_hash"]
    session.close()
    cold = S44Session.open(state, attention="distracted")
    try:
        return {
            "schema": "SOROK_S44_ATTENTION_EVIDENCE@1",
            "focused_root_hash": root,
            "distracted_root_hash": cold.read_root()["root_hash"],
            "root_unchanged": cold.read_root()["root_hash"] == root,
            "first_event_unchanged": cold.read_events()[0]["e1_event_hash"] == first,
            "verify_ok": cold.verify()["ok"],
        }
    finally:
        cold.close()


def test_evidence() -> dict:
    rows = {}
    for name, path, env in (
        ("s44", "tests", ENV),
        ("s43", str(S43_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S43_RETURN))),
        ("s42", str(S42_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S42_RETURN))),
    ):
        xml = JUNIT / f"{name}_full.xml"
        proc = _run(
            [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={xml}", path],
            f"{name}_full.log", env=env,
        )
        counts = _junit_counts(xml)
        rows[name] = {
            "exit": proc.returncode,
            "junit": str(xml.relative_to(RET)),
            "counts": {key: counts[key] for key in
                       ("tests", "PASS", "RED", "ERROR", "SKIP")},
        }
    return rows


def source_manifest():
    s43_rows = []
    for rel in S43_FILES:
        local = S43_RETURN / rel
        pinned = _git(
            "rev-parse",
            f"{CUTS['s43']}:WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1/{rel}",
        )
        local_blob = _git("hash-object", str(local))
        s43_rows.append({
            "path": rel,
            "pinned_git_blob_sha1": pinned,
            "local_git_blob_sha1": local_blob,
            "exact": pinned == local_blob,
            "sha256": _sha256(local),
        })
    local_rows = [{
        "path": rel,
        "sha256": _sha256(RET / rel),
        "git_blob_sha1": _git("hash-object", str(RET / rel)),
    } for rel in S44_FILES]
    structural = []
    for path in STRUCTURAL_FILES:
        p = Path(path)
        structural.append({
            "path": str(p),
            "sha256": _sha256(p) if p.is_file() else "",
            "used": False,
            "reason": "No structural prior was promoted into actor facts in this explicit test bundle.",
        })
    origins = {}
    for name in ("s37", "s39", "s40", "s41", "s42", "s43", "s44", "s44.session"):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S44_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s43_reused": s43_rows,
        "s43_all_exact": all(row["exact"] for row in s43_rows),
        "s44_local": local_rows,
        "model_bundle_hash": _bundle("11" * 32)["bundle_hash"],
        "root_hash": generate_root(_bundle("11" * 32)).root_hash,
        "structural_interfaces": structural,
        "imported_origins": origins,
        "s43_origin_accepted": "SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1"
        in origins.get("s43", ""),
        "s44_origin_local": "SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1"
        in origins.get("s44.session", ""),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s44-evidence-", dir=str(RET)))
    try:
        root = root_evidence()
        consumer = consumer_evidence(work / "consumer")
        faults = fault_evidence(work / "faults")
        attention = attention_evidence(work / "attention")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s44.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S44_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        bundle = _bundle("11" * 32)
        _write(EVID / "model_bundle.json", bundle)
        _write(EVID / "root.json", root)
        _write(EVID / "consumer.json", consumer)
        _write(EVID / "faults.json", faults)
        _write(EVID / "attention.json", attention)
        _write(EVID / "test_run.json", {
            "schema": "SOROK_S44_TEST_RUN@1", "rows": tests,
            "entrypoint_exit": entry.returncode,
        })
        _write(EVID / "source_manifest.json", source_manifest())
        print(json.dumps({
            "tests": {key: value["counts"] for key, value in tests.items()},
            "entrypoint_exit": entry.returncode,
            "replay_exact": root["replay_exact"],
            "candidate_order_isolated": root["candidate_order_isolated"],
            "unrelated_stream_isolated": root["unrelated_stream_isolated"],
            "seed_divergence": root["seed_divergence"],
            "consumer": {
                "root_hash": consumer["root_hash"],
                "cold_root_same": consumer["cold_root_same"],
                "source_is_root_evidence": consumer["second_event"][
                    "source_is_root_evidence"
                ],
                "no_new_b_source": consumer["no_new_b_source_at_speaking"],
                "verify_ok": consumer["verify_ok"],
            },
            "faults": faults,
            "attention": attention,
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
