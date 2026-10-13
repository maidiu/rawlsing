"""HQ283 S05JR independent source-free P01 integration hostiles.

Tests must run on COMPLETE P01 composed tree at 73d45f3a or an exact
339-common +14-added blob-equal reconstruction. NOT executed by Browser/GitHub
reviewer; no runtime claim follows from this file alone.
"""
import json
from copy import deepcopy

import pytest

from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.pre553_batch_runner import BatchManifest
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture


@pytest.mark.parametrize("omitted_kind", ("I03_XY", "I03_YX", "I05_DISCOVERY"))
def test_s05jr_symmetric_expected_and_manifest_omission_can_still_structurally_pass(
    tmp_path, omitted_kind
):
    """Blind spot across both directional I03 jobs and independent I05 dispatch.

    Local declared-E/manifest equality cannot prove original source U -> E_pre.
    Retain the entire originally enumerated synthetic respondent/item inventory,
    drop precisely one predeclared operation on BOTH local sides, and test
    expected local admission with external source/custody HOLD still present.
    These are synthetic proposed tests, NOT original-source scientific warrants.
    """
    kwargs, calls = _fixture(tmp_path / "initial")
    documentary = json.loads(kwargs["expected"].payload_json)
    original_records = deepcopy(documentary["declarations"])
    pair = [r for r in original_records
            if r.get("semantic_op_class") == "PAIR_RESPONSE_COTRAVEL"]
    discovery = [r for r in original_records
                 if r.get("semantic_op_class") == "BOUNDED_DISCOVERY"]
    assert len(pair) == 2 and len(discovery) == 1
    assert len([r for r in original_records if r["state"] == "RUNNABLE"]) == 3
    dropped = {"I03_XY": pair[0], "I03_YX": pair[1],
               "I05_DISCOVERY": discovery[0]}[omitted_kind]
    job_ref = dropped.get("query_ref", dropped.get("discovery_authority_ref"))
    original_inventory = deepcopy(documentary["source_inventory"])
    documentary["declarations"] = [r for r in original_records if r is not dropped]
    assert documentary["source_inventory"] == original_inventory
    kwargs["expected"] = P.FrozenExpected.from_documentary_payload(documentary)
    original_session = kwargs["session"]
    retained = tuple(u for u in original_session.manifest.units
                     if u.job_ref.as_dict() != job_ref)
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
    assert result["source_inventory"] == original_inventory
    assert any(h["code"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD" for h in result["holds"])
    assert any(h["code"] == "SOURCE_USE_AND_REAL_EXECUTION_NOT_GRANTED"
               for h in result["holds"])


def test_s05jr_caller_asserted_source_intrinsic_na_is_not_externally_issued(tmp_path):
    """A reason string plus local hash does not establish original NOT_FIELDED.

    The synthetic E author may relabel one HELD row as SOURCE_NONAPPLICABLE.
    This locally consistent row cannot be upgraded to independently warranted
    intrinsic NA; the source-science decision remains HOLD notwithstanding
    source-free successful execution of the three other runnable rows.
    """
    kwargs, calls = _fixture(tmp_path)
    documentary = json.loads(kwargs["expected"].payload_json)
    held = next(r for r in documentary["declarations"] if r["state"] == "HELD")
    held["state"] = "SOURCE_NONAPPLICABLE"
    held["hold_reason"] = "CALLER_ASSERTED_NA__ORIGINAL_SOURCE_WARRANT_ABSENT"
    kwargs["expected"] = P.FrozenExpected.from_documentary_payload(documentary)
    result = P.run_integrated(**kwargs)
    assert result["ok"] is True
    assert len(calls) == 3
    assert len(result["consumer_products"]) == 3
    assert any(r["state"] == "SOURCE_NONAPPLICABLE"
               and r["item"] == held["item"]
               for r in result["produced"]["held_export"])
    assert any(h["code"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
               for h in result["holds"])


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
