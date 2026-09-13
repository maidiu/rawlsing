import json

from rawlsing_next.objective_consumer_bounded_evidence import (
    OC01,
    OC02,
    OC03,
    OC04,
    OC05,
    installation_manifest,
)
from rawlsing_next.tests.d07_bounded_loss_harness import run_harness


def test_d07_loss_deletion_harness_passes_all_current_consumer_cases():
    result = run_harness()
    assert result["status"] == "PASS"
    assert result["case_count"] == 12
    assert result["pass_count"] == 12
    assert result["fail_count"] == 0
    assert result["executed_policy_ids"] == [OC01, OC02]
    assert result["not_yet_applicable_policy_ids"] == [OC03, OC04, OC05]


def test_d07_installation_manifest_is_finite_and_exact():
    manifest = installation_manifest()
    assert [x["policy_id"] for x in manifest] == [OC01, OC02, OC03, OC04, OC05]
    assert [x["current_applicability"] for x in manifest] == [
        "APPLICABLE_CURRENT",
        "APPLICABLE_CURRENT",
        "NOT_YET_APPLICABLE",
        "NOT_YET_APPLICABLE",
        "NOT_YET_APPLICABLE",
    ]
    assert manifest[0]["consumer_seam"] == "rawlsing_next.pre553_empirical_query.execute_empirical_query"
    assert manifest[1]["consumer_seam"] == "rawlsing_next.pre553_structural_admission"
    assert all(x["consumer_seam"] is None for x in manifest[2:])


def test_d07_harness_result_is_deterministic():
    left = run_harness()
    right = run_harness()
    assert json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )
