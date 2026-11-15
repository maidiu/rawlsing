"""Generate S39 generation/choice/boundary/source evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parent
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = str(RET)
for path in (Ret := str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s39.bootstrap import CUTS, install, roots  # noqa: E402

install()

from s39.model import FULL_RULE, ComparisonRule, S39GenerationRefusal  # noqa: E402
from s39.producer import GeneratedProducer  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from run_s39 import run_one  # noqa: E402
from test_s39_boundaries import _tamper_generation_episode  # noqa: E402
from s39.session import S39GeneratedSession  # noqa: E402

S37_RETURN = Path(roots()["s37_return"])
S37_MANIFEST = S37_RETURN / "evidence" / "source_manifest.json"
S37_FILES = [
    "s37/__init__.py",
    "s37/bootstrap.py",
    "s37/harness.py",
    "s37/producer.py",
    "s37/product.py",
    "s37/reader.py",
    "s37/session.py",
]
LOCAL_FILES = [
    ".gitignore",
    "00_RETURN.md",
    "run_s39.py",
    "run_s39_evidence.py",
    "s39/__init__.py",
    "s39/bootstrap.py",
    "s39/model.py",
    "s39/performer.py",
    "s39/producer.py",
    "s39/reader.py",
    "s39/session.py",
    "s39/sources.py",
    "tests/conftest.py",
    "tests/test_s39_generation.py",
    "tests/test_s39_boundaries.py",
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


def _run(cmd, log_name: str):
    proc = subprocess.run(cmd, cwd=str(RET), env=ENV, capture_output=True, text=True)
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
        cases.append({
            "classname": case.attrib.get("classname", ""),
            "name": case.attrib.get("name", ""),
            "status": status,
        })
    return {
        "tests": tests,
        "PASS": tests - failures - errors - skips,
        "RED": failures,
        "ERROR": errors,
        "SKIP": skips,
        "cases": cases,
    }


def test_evidence() -> dict:
    xml = JUNIT / "s39_full.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s39_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S39_TEST_RUN@1",
        "command": f"{PY} -B -m pytest -q -p no:cacheprovider --junitxml={xml} tests",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def _records(producer, **flags):
    values = dict(
        actor_id=producer.occurrence.actor_id,
        branch_id="first_session",
        as_of=producer.as_of,
    )
    values.update(flags)
    return context_records(**values)


def choices_evidence(root: Path) -> dict:
    case = case_for(True)
    producer = GeneratedProducer(root / "source", case=case, source=source_for(case))
    try:
        producer.stage_m35()
        p = producer.generate(source_records=_records(
            producer, repair_urgent=True, avoid_debt=True, prior_b_share=True))
        c1 = producer.generate(source_records=_records(
            producer, avoid_debt=True, prefer_independent=True))
        c2 = producer.generate(source_records=_records(
            producer, prior_b_refusal=True))
        open_choice = producer.generate(source_records=_records(producer))
        cycle = producer.generate(source_records=_records(
            producer, repair_urgent=True, avoid_debt=True,
            prior_b_share=True, prefer_independent=True, prior_b_refusal=True))
        missing_rule = ComparisonRule(
            "S39_GUARDED_CONTEXTUAL_COMPARISON", "1-missing",
            (FULL_RULE.comparisons[0],), ("missing-coverage test",), "PARTIAL")
        missing = producer.generate(
            source_records=_records(
                producer, repair_urgent=True, avoid_debt=True,
                prior_b_share=True),
            rule=missing_rule)
        labels = producer.generate(source_records=_records(
            producer, repair_urgent=True, avoid_debt=True,
            prior_b_share=True, labels={"class": "X", "Enneagram": "Y"}))
        no_prior = producer.generate(source_records=_records(
            producer, repair_urgent=True, avoid_debt=True))
        tampered = [dict(row) for row in _records(
            producer, repair_urgent=True, avoid_debt=True, prior_b_share=True)]
        tampered[0] = dict(tampered[0])
        tampered[0]["content"] = {"tampered": True}
        try:
            producer.generate(source_records=tampered)
            tamper_status = "ACCEPTED"
            tamper_code = ""
        except S39GenerationRefusal as exc:
            tamper_status = "REFUSED"
            tamper_code = exc.code

        def summary(label, receipt):
            return {
                "label": label,
                "selection_status": receipt["selection_status"],
                "selected_option": receipt["selected_option"],
                "unresolved_reason": receipt["unresolved_reason"],
                "undominated_options": receipt["undominated_options"],
                "attempt_action": (
                    (receipt.get("attempt_request") or {}).get("action", "")
                ),
                "contrary_predicates": [
                    row["predicate"] for row in receipt["contrary_reasons"]
                ],
                "supporting_predicates": [
                    row["predicate"] for row in receipt["supporting_reasons"]
                ],
                "rule_hash": receipt["rule"]["content_hash"],
                "input_contains_desired_action": receipt["input_contains_desired_action"],
            }

        return {
            "schema": "SOROK_S39_CHOICE_EVIDENCE@1",
            "grade": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
            "choices": [
                summary("P_REQUEST", p),
                summary("C1_ATTEND", c1),
                summary("C2_REFUSAL", c2),
                summary("OPEN", open_choice),
                summary("CYCLE", cycle),
                summary("MISSING_COMPARISON", missing),
                summary("LABELS", labels),
                summary("MISSING_PRIOR_SHARE", no_prior),
            ],
            "label_invariance": {
                "same_selected_option": labels["selected_option"] == p["selected_option"],
                "same_attempt_action": (
                    (labels.get("attempt_request") or {}).get("action")
                    == (p.get("attempt_request") or {}).get("action")
                ),
                "same_supporting_predicates": [
                    row["predicate"] for row in labels["supporting_reasons"]
                ] == [row["predicate"] for row in p["supporting_reasons"]],
                "same_contrary_predicates": [
                    row["predicate"] for row in labels["contrary_reasons"]
                ] == [row["predicate"] for row in p["contrary_reasons"]],
                "ignored_label_count": labels["ignored_label_count"],
            },
            "tampered_source": {
                "status": tamper_status,
                "code": tamper_code,
            },
            "open_cycle_no_attempt": (
                open_choice.get("attempt_request") is None
                and cycle.get("attempt_request") is None
            ),
        }
    finally:
        producer.close()


def chain_evidence(root: Path) -> dict:
    chains = [run_one(root, share=True), run_one(root, share=False)]
    return {
        "schema": "SOROK_S39_CHAIN_EVIDENCE@1",
        "grade": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "native": False,
        "provider_calls": 0,
        "chains": chains,
        "share_generated_positive": (
            chains[0]["selected_option"] == "REQUEST_TOOL"
            and chains[0]["attempt_status"] == "ADMITTED"
            and chains[0]["performed"] is True
            and chains[0]["s36_outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        ),
        "refuse_performer_denied": (
            chains[1]["selected_option"] == "REQUEST_TOOL"
            and chains[1]["attempt_status"] == "DENIED"
            and chains[1]["performed"] is False
            and chains[1]["s36_outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        ),
        "both_no_target": all(
            row["target_branch"] == "NO_CHANGE"
            and row["target_reason"] == "NO_PROPOSAL"
            and row["target_proposals"] == []
            and row["target_state_rows"] == 0
            for row in chains
        ),
        "same_neutral_speech": (
            chains[0]["language"]["native_text"] == chains[1]["language"]["native_text"]
            and chains[0]["language"]["english_text"] == chains[1]["language"]["english_text"]
        ),
        "both_cold_verify": all(row["cold"]["verify_ok"] for row in chains),
    }


def mismatch_evidence(root: Path) -> dict:
    state = root / "mismatch"
    case = case_for(True)
    session = S39GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        original = session.meta["s39_generation_hash"]
        session.meta["s39_generation_hash"] = "0" * 64
        try:
            session.read_generation()
            meta_status = "ACCEPTED"
            meta_code = ""
        except Exception as exc:
            meta_status = "REFUSED"
            meta_code = getattr(exc, "code", type(exc).__name__)
        session.meta["s39_generation_hash"] = original
        restored = session.read_generation()["status"]
    finally:
        session.close()
    _tamper_generation_episode(state)
    try:
        S39GeneratedSession.open(state)
        c12_status = "ACCEPTED"
        c12_code = ""
    except Exception as exc:
        c12_status = "REFUSED"
        c12_code = getattr(exc, "code", type(exc).__name__)
    return {
        "schema": "SOROK_S39_MISMATCH_EVIDENCE@1",
        "meta_binding": {"status": meta_status, "code": meta_code},
        "restored_status": restored,
        "persisted_c12_duplicate_binding": {
            "status": c12_status, "code": c12_code,
            "error_contains_s39_generation": "S39_GENERATION" in str(c12_code)
            or c12_status == "REFUSED",
        },
    }


def source_manifest() -> dict:
    s37_manifest = json.loads(S37_MANIFEST.read_text()) if S37_MANIFEST.is_file() else {}
    s37_rows = []
    for rel in S37_FILES:
        local = RET.parent / "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1" / rel
        # The S37 return is a sibling under WORKER_RETURNS.
        local = RET.parent / "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1" / rel
        pinned = _git("rev-parse", f"{CUTS['s37']}:WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1/{rel}")
        local_blob = _git("hash-object", str(local))
        s37_rows.append({
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
    } for rel in LOCAL_FILES]
    origins = {}
    for name in (
        "candidate", "bp2_joined", "joined.session", "language_mediation.session",
        "s37", "s37.session", "s37.producer", "s37.reader",
        "s39", "s39.session", "s39.producer", "s39.reader",
    ):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S39_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s37_reused": s37_rows,
        "s37_all_exact": all(row["exact"] for row in s37_rows),
        "s37_accepted_manifest": {
            "path": str(S37_MANIFEST),
            "m35_all_exact": s37_manifest.get("m35_all_exact"),
            "s36_all_exact": s37_manifest.get("s36_all_exact"),
            "language_all_exact": s37_manifest.get("language_all_exact"),
            "join_e_all_exact": s37_manifest.get("join_e_all_exact"),
        },
        "s39_local": local_rows,
        "imported_origins": origins,
        "candidate_origin_s36": "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1" in origins.get("candidate", ""),
        "s37_origin_accepted": "SOROK-20261024-S37-INTEGRATED-CONSUMER-R1" in origins.get("s37.session", ""),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s39-evidence-", dir=str(RET)))
    try:
        chains = chain_evidence(work / "chains")
        choices = choices_evidence(work / "choices")
        mismatch = mismatch_evidence(work / "mismatch")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s39.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S39_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain.json", chains)
        _write(EVID / "choices.json", choices)
        _write(EVID / "mismatch.json", mismatch)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "source_manifest.json", manifest)
        print(json.dumps({
            "tests": tests["counts"],
            "entrypoint_exit": entry.returncode,
            "share_generated_positive": chains["share_generated_positive"],
            "refuse_performer_denied": chains["refuse_performer_denied"],
            "both_no_target": chains["both_no_target"],
            "same_neutral_speech": chains["same_neutral_speech"],
            "both_cold_verify": chains["both_cold_verify"],
            "open_cycle_no_attempt": choices["open_cycle_no_attempt"],
            "label_invariance": choices["label_invariance"],
            "tampered_source": choices["tampered_source"],
            "mismatch_meta": mismatch["meta_binding"],
            "mismatch_persisted": mismatch["persisted_c12_duplicate_binding"],
            "s37_all_exact": manifest["s37_all_exact"],
            "source_roots": manifest["candidate_origin_s36"]
            and manifest["s37_origin_accepted"],
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
