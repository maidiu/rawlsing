from rawlsing_next import rabochii_return_beacon as rb
from rawlsing_next import rabochii_return_beacon_actionable as action


def cert(branch: str, result: str = "FAIL", task_id: str = "LEGACY_RETURN") -> rb.Certification:
    return rb.Certification(
        branch=branch,
        tip_sha="a" * 40,
        task_id=task_id,
        result=result,
        terminal="RABOCHII_EXAMPLE__RETURN_TO_SUB_VOZHD_E",
        return_packet_path="data/return.md",
        evidence_run_id=34264406739,
        mode="LEGACY_STRICT",
    )


def test_review_worker_label_is_human_actionable():
    c = cert("agent/rabochii-subv-e-obl058-causal-use-permission-r7-independent-review-r1")
    assert action.worker_label(c) == "OBL058 R7 INDEPENDENT REVIEW"


def test_repair_worker_label_is_human_actionable():
    c = cert("agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r9", result="PASS")
    assert action.worker_label(c) == "OBL059 R9 BOUNDED REPAIR"


def test_certified_fail_explicitly_says_safe_to_cancel():
    c = cert("agent/rabochii-subv-e-obl058-causal-use-permission-r7-independent-review-r1")
    body = action.actionable_comment_body(c)
    assert "SAFE TO CANCEL WORKER CHAT — OBL058 R7 INDEPENDENT REVIEW — FAIL" in body
    assert "Cancel/close the corresponding ChatGPT worker turn now" in body
    assert "certifiably complete" in body


def test_certified_pass_also_explicitly_says_safe_to_cancel():
    c = cert("agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r9", result="PASS")
    body = action.actionable_comment_body(c)
    assert "SAFE TO CANCEL WORKER CHAT — OBL059 R9 BOUNDED REPAIR — PASS" in body


def test_manifest_task_id_is_fallback_label():
    c = cert("agent/custom-worker", result="BLOCKED", task_id="MY_TASK_R1")
    assert action.worker_label(c) == "MY TASK R1"
