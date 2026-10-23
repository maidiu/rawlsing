from __future__ import annotations

import subprocess

CANDIDATE = "ad9c3088096ce291d61dfdd292141073b515fbca"
J42 = "f53cb0d2bce52640268c844c398bbd8007d28edc"
P41 = "f27d1101048638bba395143a48efb7ef00bfcda4"


def _show(commit: str, path: str) -> str:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], text=True)


def test_candidate_binding_is_not_adopted_by_live_non_test_code():
    output = subprocess.check_output(
        [
            "git",
            "grep",
            "-l",
            "pre553_universal_evidence_binding",
            CANDIDATE,
            "--",
            "*.py",
        ],
        text=True,
    )
    paths = {
        line.split(":", 1)[1]
        for line in output.splitlines()
        if line.strip()
    }
    assert paths == {
        "rawlsing_next/pre553_universal_evidence_binding.py",
        "rawlsing_next/tests/test_universal_evidence_binding.py",
    }, paths


def test_historical_j42_provider_still_records_synthetic_evaluator_trace():
    source = _show(
        J42,
        "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1/runtime/j42_join.py",
    )
    assert 'call="evaluate_positioned_subject_possibility"' in source
    assert "same_evidence_object=True" in source
    assert "evaluate_positioned_subject_possibility(" not in source


def test_historical_p41_service_still_uses_trace_index_and_cache_fallback():
    source = _show(
        P41,
        "WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1/runtime/p41_service.py",
    )
    assert 'entry = trace_consumptions[index] if index < len(trace_consumptions) else None' in source
    assert 'source="CACHED_PRODUCTION_CONSUMPTION"' in source
    assert "same_evidence_object=True" in source
