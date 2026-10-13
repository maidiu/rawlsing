"""HQ283 S05JR independent source-free P01 integration hostiles.

Tests must run on COMPLETE P01 composed tree at 73d45f3a or an exact
339-common +14-added blob-equal reconstruction. NOT executed by Browser/GitHub
reviewer; no runtime claim follows from this file alone.
"""
import json
from copy import deepcopy

from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.pre553_batch_runner import BatchManifest
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture


def test_s05jr_symmetric_expected_and_manifest_omission_can_still_structurally_pass(tmp_path):
    """Falsification: a complete declared local join need not be original U->E complete.

    Exact observed target: both local expectation and manifest omit one originally
    prepared X/Y query; frozen original respondent inventory stays unchanged.
    Existing code is expected to return local ok=True, two consumed results and
    external issuer/custody HOLD. This is a SCIENTIFIC AUTHORITY GAP, not proof
    that the supported local subset's execution misbehaves.
    """
    kwargs, calls = _fixture(tmp_path / "initial")
    documentary = json.loads(kwargs["expected"].payload_json)
    original_records = deepcopy(documentary["declarations"])
    candidates = [r for r in original_records if r.get("semantic_op_class") == "PAIR_RESPONSE_COTRAVEL"]
    assert len(candidates) == 2
    dropped = candidates[0]
    documentary["declarations"] = [r for r in original_records if r is not dropped]
    kwargs["expected"] = P.FrozenExpected.from_documentary_payload(documentary)
    original_session = kwargs["session"]
    retained = tuple(u for u in original_session.manifest.units
                     if u.job_ref.as_dict() != dropped["query_ref"])
    assert len(retained) == 2
    kwargs["session"] = G.open_session(
        manifest=BatchManifest(retained),
        repository=original_session.repository,
        executors=original_session.executors,
        root=tmp_path / "omitted",
        source_sha256=original_session.source_sha256,
    )
    result = P.run_integrated(**kwargs)
    assert result["ok"] is True
    assert len(calls) == 2
    assert len(result["consumer_products"]) == 2
    assert result["source_inventory"]  # original respondent/item rows still present
    assert any(h["code"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD" for h in result["holds"])
    assert any(h["code"] == "SOURCE_USE_AND_REAL_EXECUTION_NOT_GRANTED" for h in result["holds"])


def test_s05jr_structural_ok_must_not_be_confused_with_external_permission(tmp_path):
    """Exact expected: source-free local success AND absolute custody/source HOLD."""
    kwargs, calls = _fixture(tmp_path)
    result = P.run_integrated(**kwargs)
    assert result["ok"] is True
    assert len(result["consumer_products"]) == 3
    assert len(calls) == 3
    assert result["custodian"]["signature_trusted"] is False
    assert result["custodian"]["timestamp_trusted"] is False
    assert {"EXTERNAL_CUSTODIAN_ISSUER_HOLD",
            "SOURCE_USE_AND_REAL_EXECUTION_NOT_GRANTED"} <= {
                h["code"] for h in result["holds"]}


def test_s05jr_replay_does_not_repeat_durable_effects(tmp_path):
    """Exact expected: same consumer object references; zero additional owner calls."""
    kwargs, calls = _fixture(tmp_path)
    first = P.run_integrated(**kwargs)
    from rawlsing_next.pre553_empirical_objects import ExactRef
    refs = {r["expected_work_key"]: ExactRef(**r["consumer_ref"])
            for r in first["consumer_products"]}
    n = len(calls)
    second = P.run_integrated(**kwargs, prior_consumer_refs=refs)
    assert first["ok"] and second["ok"]
    assert second["run"]["executed"] == []
    assert len(calls) == n == 3
    assert second["consumer_products"] == first["consumer_products"]
