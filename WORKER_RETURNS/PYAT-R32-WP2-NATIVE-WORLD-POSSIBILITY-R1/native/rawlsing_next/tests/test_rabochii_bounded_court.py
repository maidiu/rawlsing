import json
from types import SimpleNamespace

from rawlsing_next import rabochii_bounded_court as court


SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40


def _spec():
    return {
        "schema_id": "RABOCHII_COURT_SPEC@1.0.0",
        "semantic_candidate_sha": SHA_A,
        "python_version": "3.12",
        "determinism_mode": "EXACT",
        "tests": ["rawlsing_next/tests/test_pre553_empirical_query.py"],
        "env": {
            "PYTHONHASHSEED": "0",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        },
    }


def test_receipt_separates_candidate_execution_and_synthetic_sha(tmp_path, monkeypatch):
    spec_path = tmp_path / "court.json"
    receipt_path = tmp_path / "receipt.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")

    seen = {}

    def fake_run(command, *, env, check):
        seen["command"] = command
        seen["env"] = env
        seen["check"] = check
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(court.subprocess, "run", fake_run)
    monkeypatch.setenv("RABOCHII_EVIDENCE_EXECUTION_SHA", SHA_B)
    monkeypatch.setenv("RABOCHII_PR_SYNTHETIC_SHA", SHA_C)

    assert court.run_court(spec_path, receipt_path) == 0
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert receipt["result"] == "PASS"
    assert receipt["semantic_candidate_sha"] == SHA_A
    assert receipt["evidence_execution_sha"] == SHA_B
    assert receipt["pr_synthetic_merge_sha"] == SHA_C
    assert seen["command"][:4] == [
        court.sys.executable,
        "-m",
        "pytest",
        "-q",
    ]
    assert seen["env"]["PYTHONHASHSEED"] == "0"
    assert seen["check"] is False


def test_invalid_spec_fails_without_running_pytest(tmp_path, monkeypatch):
    spec = _spec()
    spec["tests"] = ["../../etc/passwd"]
    spec_path = tmp_path / "court.json"
    receipt_path = tmp_path / "receipt.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    def forbidden(*args, **kwargs):
        raise AssertionError("pytest must not run for invalid court spec")

    monkeypatch.setattr(court.subprocess, "run", forbidden)

    assert court.run_court(spec_path, receipt_path) == 2
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["result"] == "INVALID_SPEC"
    assert receipt["errors"]
