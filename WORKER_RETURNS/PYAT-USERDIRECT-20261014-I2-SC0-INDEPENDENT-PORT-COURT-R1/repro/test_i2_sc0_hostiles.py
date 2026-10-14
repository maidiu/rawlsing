"""I2 independent hostile probes for HQ298 SC0 — NOT EXECUTED in this browser court.

Run only after independently materializing the exact candidate branch
b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59 into an authorized isolated
source-free workspace:
  SC0_PORT_ROOT=/absolute/path/to/WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1 \
    python -m pytest -q test_i2_sc0_hostiles.py --junitxml=i2_hostiles.junit.xml

These are NEW adversarial expectations. Do not count them as the author's
frozen K9/K10 suite or as an original-survey / actor / model-use test.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import sys

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(os.environ.get("SC0_PORT_ROOT", "/__NO_QUALIFIED_CANDIDATE_ROOT__"))
if not (ROOT / "port" / "adapter.py").is_file():
    pytest.skip("NO_QUALIFIED_EXACT_CANDIDATE_SOURCE_TREE: NOT_EXECUTED", allow_module_level=True)
sys.path.insert(0, str(ROOT))

from port.adapter import TwoContractAdapter, provider_equivalence_report
from port.contracts import PortContractError
from port.provider_a import ProviderA
from port.provider_b import ProviderB
from port.world_baseline import BASELINE_WORLD, EMPIRICAL, REVERSAL_GRANT_SCOPED


def test_00_pinned_oracles_real_git_blob_preimages():
    pins = {
        "01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json":
            "610ac870fde6cfe63796592b3c6b1e1bf1e37150",
        "02_K9_PROVIDER_SWAP_ORACLES.json":
            "9ccb66f9b08a4aa8b96582295bb2966d250fd72d",
        "03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json":
            "e78b3ee91da1fb18deaf8d8f226800ad855adbae",
    }
    for name, expected in pins.items():
        raw = (ROOT / "oracles" / name).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest() == expected


def test_01_two_exact_frozen_receipt_shapes_not_just_same_names():
    schema = json.loads((ROOT / "oracles" / "01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json").read_text())
    Draft202012Validator.check_schema(schema)
    adapter = TwoContractAdapter(ProviderA())
    emitted = adapter.run()
    validator = Draft202012Validator(schema)
    # Both distinct owners must produce legitimate schema receipts, not
    # a differently shaped record with the same contract name.
    validator.validate(emitted["world_receipt"])
    validator.validate(emitted["possibility_receipt"])


def test_02_demand_asof_2009_must_not_serve_rule_published_2010_as_known():
    # Explicit 2009 KNOWLEDGE_AS_OF is earlier than baseline source publication.
    world = copy.deepcopy(BASELINE_WORLD)
    assert world["clock_mode"] == "KNOWLEDGE_AS_OF"
    assert world["time_axes"]["as_of"] == "2009"
    assert world["time_axes"]["published"] == "2010"
    # No issuer-qualified earlier-publication alternative was supplied.
    with pytest.raises(PortContractError):
        TwoContractAdapter(ProviderA(world=world)).run({"as_of": "2009", "mode": "KNOWLEDGE_AS_OF"})


def test_03_revoked_world_read_must_block_actual_adapter_consumer():
    world = copy.deepcopy(BASELINE_WORLD)
    world["permission_ceiling"]["revoked_atoms"] = ["WORLD_READ"]
    with pytest.raises(PortContractError) as exc:
        TwoContractAdapter(ProviderA(world=world)).run()
    assert exc.value.code == "DENIED_USE"


def test_04_partial_selected_world_must_not_become_positive_bundle():
    class PartialProvider(ProviderA):
        def resolve_world_selection(self, demand):
            selection = super().resolve_world_selection(demand)
            selection["selection_state"] = "PARTIAL"
            return selection
    with pytest.raises(PortContractError):
        TwoContractAdapter(PartialProvider()).run()


def test_05_caller_forged_issuer_name_and_wrong_target_scope_must_refuse():
    provider = ProviderA()
    bundle = TwoContractAdapter(provider).run()
    forged = copy.deepcopy(REVERSAL_GRANT_SCOPED)
    # Copy the expected string, but WITHOUT an independent issued warrant.
    forged["grant_id"] = "urn:test:forged-not-issued"
    forged["issuer"] = bundle["world_receipt"]["world"]["authority_ref"]
    forged["scope"] = "fx:OTHER-universe|fx:DIFFERENT-release"
    forged["binds"]["target"] = "fx:response:WRONG_TARGET"
    with pytest.raises(PortContractError) as exc:
        provider.request_role_reversal(bundle["world_receipt"], bundle["possibility_receipt"], forged)
    assert exc.value.code == "HELD_AUTHORITY"


def test_06_empirical_cells_cannot_silently_inherit_independent_world_support():
    empirical = copy.deepcopy(EMPIRICAL)
    empirical["cells"] = [{"value": "YES", "n": 50}, {"value": "NO", "n": 10}]
    provider = ProviderA(empirical=empirical)
    try:
        bundle = TwoContractAdapter(provider).run()
    except PortContractError:
        return
    # 54/6 from a WORLD fixture is not a lawful result of independent
    # empirical evidence containing 50/10.
    assert bundle["possibility_receipt"]["support"]["target_yes"] == 50
    assert bundle["possibility_receipt"]["support"]["target_no"] == 10


def test_07_numeric_world_route_value_changes_both_readers_not_unrelated_route():
    first = TwoContractAdapter(ProviderA()).run()
    changed = copy.deepcopy(BASELINE_WORLD)
    changed["routes"]["fx:r:public"]["values"]["quota"] += 1
    second = TwoContractAdapter(ProviderA(world=changed)).run()
    for cid in first["consumer_effects"]:
        assert first["consumer_effects"][cid]["output"] != second["consumer_effects"][cid]["output"]
    assert first["world_receipt"]["world"]["routes"]["fx:r:mutual"] == second["world_receipt"]["world"]["routes"]["fx:r:mutual"]


def test_08_an_unchecked_new_semantic_field_cannot_disappear_in_equivalence():
    class AExtra(ProviderA):
        def resolve_world_selection(self, demand):
            selection = super().resolve_world_selection(demand)
            selection["world"]["native_authority_scope_extension"] = "AUTH-A"
            return selection
    class BExtra(ProviderB):
        def resolve_world_selection(self, demand):
            selection = super().resolve_world_selection(demand)
            selection["world"]["native_authority_scope_extension"] = "AUTH-B"
            return selection
    a = TwoContractAdapter(AExtra()).run()
    b = TwoContractAdapter(BExtra()).run()
    assert not provider_equivalence_report(a,b)["equivalent_except_physical_lineage"]


def test_09_publication_successor_must_rebind_to_actual_changed_source_boundary():
    provider = ProviderA()
    first = TwoContractAdapter(provider).run()
    provider.refresh_publication_generation()
    newer = TwoContractAdapter(provider).run()
    # A fresh generation ID alone is not a changed publication/effective boundary.
    assert (newer["world_receipt"]["world"]["source_release_ref"] !=
            first["world_receipt"]["world"]["source_release_ref"] or
            newer["world_receipt"]["world"]["time_axes"]["published"] !=
            first["world_receipt"]["world"]["time_axes"]["published"])
