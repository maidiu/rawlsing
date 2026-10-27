"""Focused A1 checks that do not require an original-source C11 build."""
from __future__ import annotations

import hashlib
from pathlib import Path

from rawlsing_next.source_configuration.schema import load_source_config

from campaign_a_src04 import run_campaign_a_src04 as runner


def test_committed_grant_is_the_pinned_human_grant():
    grant_path = runner.COMMITTED_GRANT_PATH
    assert grant_path.is_file()
    assert hashlib.sha256(grant_path.read_bytes()).hexdigest() == runner.EXPECTED_GRANT_SHA256
    grant = runner.load_grant()
    assert grant["document"]["source_id"] == "SRC04"
    assert grant["document"]["expected_source_sha256"] == runner.EXPECTED_SOURCE_SHA256
    assert grant["document"]["host"] == "USER_LOCAL_MAC"
    assert grant["program_sha256"] == runner.EXPECTED_PROGRAM_SHA256
    assert grant["control_commit"] == runner.CONTROL_COMMIT


def test_original_config_keeps_defer_semantic_authority():
    config = load_source_config(runner.CONFIG_PATH)
    snapshots = config.document["authority"]["snapshots"]
    assert sum(1 for snap in snapshots if snap["decision_state"] == "DEFER") >= 6
    semantic_kinds = {
        "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        "SOURCE_SEMANTICS_TOPOLOGY",
        "COORDINATE_SEMANTICS",
    }
    assert all(snap["decision_state"] == "DEFER"
               for snap in snapshots if snap["authority_kind"] in semantic_kinds)
    assert all(snap["decision_state"] == "DEFER"
               for snap in snapshots if snap["authority_kind"] == "ROUTING_RISK_SET")
    assert any(snap["authority_kind"] == "REPLAY_PROTOCOL" and snap["decision_state"] == "ALLOW"
               for snap in snapshots)


def test_wrong_source_refuses_before_source_open():
    config = load_source_config(runner.CONFIG_PATH)
    grant = runner.load_grant()
    result = runner.wrong_source_negative(config, grant)
    assert result["status"] == "REFUSED"
    assert result["refusal_code"] == "SOURCE_READ_SOURCE_SHA256_MISMATCH"
    assert result["source_read_performed"] is False
    assert result["before_source_io"] is True


def test_slice_descriptor_has_exact_config_counts():
    config = load_source_config(runner.CONFIG_PATH)
    assert len(config.document["physical_slots"]) == 181
    assert len(config.document["items"]) == 181
    assert len(config.document["response_slots"]) == 178
    assert len(config.document["coordinate_slots"]) == 3
    assert len(config.document["weight_slots"]) == 0
    assert config.document["coverage"]["physical_slots_total"] == 181
    assert config.document["coverage"]["items_total"] == 181


def test_slice_builder_withholds_canonical_values_without_mutating_source_config():
    config = load_source_config(runner.CONFIG_PATH)
    selection = {
        "selected_response_slots": [3],
        "selected_coordinate_slots": [1, 2],
    }
    sliced, withheld = runner.build_slice_config(config, selection, strip_canonical=True)
    assert withheld > 0
    assert len(sliced.document["response_slots"]) == 1
    assert len(sliced.document["coordinate_slots"]) == 2
    assert all(value["canonical_value"] is None
               for slot in sliced.document["response_slots"] for value in slot["values"])
    assert all(value["transform_authority_ref"] is None
               for slot in sliced.document["response_slots"] for value in slot["values"])
    original = load_source_config(runner.CONFIG_PATH)
    assert any(value.get("canonical_value") is not None
               for slot in original.document["response_slots"] for value in slot["values"])
