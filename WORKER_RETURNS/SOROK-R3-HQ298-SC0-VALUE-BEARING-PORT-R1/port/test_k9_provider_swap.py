"""K9 provider-swap court — the 8 frozen SC0 cases, executed against the port.

Statuses are assigned by execution only (PASS / RED / NOT_REACHED).  Frozen
expected classes come from the SC0 oracle blob 9ccb66f9b08a4aa8b96582295bb2966d250fd72d
and are never edited here.
"""
from __future__ import annotations

import copy

import pytest

from port.adapter import TwoContractAdapter, provider_equivalence_report
from port.contracts import PortContractError
from port.provider_a import ProviderA, build_provider_a
from port.provider_b import ProviderB, build_provider_b
from port.world_baseline import (
    BASELINE_WORLD,
    CONSUMER_SPECS,
    EMPIRICAL,
    REVERSAL_GRANT_FORGED,
    REVERSAL_GRANT_SCOPED,
)

FROZEN = {
    "K9_01_TWO_PROVIDERS_SAME_MEANING": "EQUIVALENT_EXCEPT_DECLARED_PHYSICAL_LINEAGE",
    "K9_02_INDEPENDENT_NONPARENT": "GENERIC_API_CONSUMED_WITHOUT_GENEALOGY",
    "K9_03_ID_REORDER_AND_STAGE_RENAME": "EQUIVALENT",
    "K9_04_NOT_EQUIVALENT_CONTRAST": "FAIL_NON_EQUIVALENT_PROVIDER_NOT_PERMITTED_NORMALIZATION",
    "K9_05_MODELLED_VS_OBSERVED": "REFUSE_GRADE_PROMOTION",
    "K9_06_FORWARD_REVERSE": "HELD_AUTHORITY_REVERSE_ROLE",
    "K9_07_PERMISSIONS": "DENIED_USE",
    "K9_08_TWO_CHANNEL_REFRESH": "TWO_INDEPENDENT_SUCCESSORS",
}


def test_k9_01_two_providers_same_meaning():
    """K9_01 — A and B equivalent except declared physical lineage."""

    bundle_a = TwoContractAdapter(build_provider_a()).run()
    bundle_b = TwoContractAdapter(build_provider_b()).run()
    report = provider_equivalence_report(bundle_a, bundle_b)
    assert report["world_projection_diffs"] == []
    assert report["possibility_projection_diffs"] == []
    assert report["consumer_effect_diffs"] == []
    assert report["physical_provider_ids_differ"] is True
    assert report["equivalent_except_physical_lineage"] is True
    assert TwoContractAdapter.round_trip_two_contracts(bundle_a)["state"] == "LOSSLESS_TWO_CONTRACT_ROUNDTRIP"
    assert TwoContractAdapter.round_trip_two_contracts(bundle_b)["state"] == "LOSSLESS_TWO_CONTRACT_ROUNDTRIP"


def test_k9_02_independent_nonparent_consumer():
    """K9_02 — generic API consumed without genealogy; no person generation."""

    bundle = TwoContractAdapter(build_provider_a()).run(
        consumer_ids=("NONPARENT_APPRENTICESHIP_ENTRY",)
    )
    effect = bundle["consumer_effects"]["NONPARENT_APPRENTICESHIP_ENTRY"]
    assert effect["person_generation"] == "NONE"
    assert "no parent or coparent tag" in effect["restrictions"]
    read_keys = effect["values_read"]["keys"]
    assert "fx:rule:public_access_2008" in read_keys and "fx:rule:mutual_aid" in read_keys
    # selected apprenticeship routes equal across A and B
    bundle_b = TwoContractAdapter(build_provider_b()).run(
        consumer_ids=("NONPARENT_APPRENTICESHIP_ENTRY",)
    )
    assert (
        effect["output"]["apprenticeship_access_routes"]
        == bundle_b["consumer_effects"]["NONPARENT_APPRENTICESHIP_ENTRY"]["output"][
            "apprenticeship_access_routes"
        ]
    )


def test_k9_03_id_reorder_and_stage_rename_equivalent():
    """K9_03 — shuffled record order + renamed stage files change nothing."""

    bundle_a = TwoContractAdapter(build_provider_a()).run()
    # B physically shuffles rows and renames stage_one/stage_two -> renamed_data/join_index
    provider_b = build_provider_b()
    assert provider_b.physical_lineage["stage_names"] == ["renamed_data", "join_index"]
    bundle_b = TwoContractAdapter(provider_b).run()
    report = provider_equivalence_report(bundle_a, bundle_b)
    assert report["equivalent_except_physical_lineage"] is True
    assert report["world_projection_diffs"] == []
    # no stage-name dependency anywhere in the semantic projection
    proj = bundle_b["world_receipt"]["world"]
    assert "stage_one" not in repr(proj) and "stage_two" not in repr(proj)


def test_k9_04_not_equivalent_contrast_rejected():
    """K9_04 — dropped sponsor participant / dyadized triad must be rejected."""

    mutated = copy.deepcopy(BASELINE_WORLD)
    mutated["nary"]["participants"] = mutated["nary"]["participants"][:2]
    mutated["nary"]["cardinality"] = 2
    with pytest.raises(PortContractError) as exc:
        TwoContractAdapter(ProviderA(world=mutated)).run()
    assert exc.value.code == "REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS"

    mutated2 = copy.deepcopy(BASELINE_WORLD)
    mutated2["nary"]["participants"] = [
        p for p in mutated2["nary"]["participants"] if p["role"] != "third-party"
    ]
    mutated2["nary"]["cardinality"] = 2
    with pytest.raises(PortContractError) as exc2:
        TwoContractAdapter(ProviderB(world=mutated2)).run()
    assert exc2.value.code == "REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS"


def test_k9_05_modelled_vs_observed_refuses_grade_promotion():
    """K9_05 — marking a fixture route as observed must refuse promotion."""

    mutated = copy.deepcopy(BASELINE_WORLD)
    mutated["epistemic_grade"] = "OBSERVED_SOURCE_FACT"
    with pytest.raises(PortContractError) as exc:
        TwoContractAdapter(ProviderA(world=mutated)).run()
    assert exc.value.code == "REJECT_EPISTEMIC_PROMOTION"


def test_k9_06_forward_reverse_held_without_scoped_issuer():
    """K9_06 — reversal held without competent scoped grant; permitted with one."""

    adapter = TwoContractAdapter(build_provider_a())
    bundle = adapter.run()
    selection = bundle["world_receipt"]
    possibility = bundle["possibility_receipt"]

    provider = adapter.provider
    with pytest.raises(PortContractError) as held:
        provider.request_role_reversal(selection, possibility, None)
    assert held.value.code == "HELD_AUTHORITY"

    with pytest.raises(PortContractError) as forged:
        provider.request_role_reversal(selection, possibility, REVERSAL_GRANT_FORGED)
    assert forged.value.code == "HELD_AUTHORITY"

    permitted = provider.request_role_reversal(
        selection, possibility, REVERSAL_GRANT_SCOPED
    )
    assert permitted["state"] == "REVERSAL_PERMITTED_UNDER_SCOPED_GRANT"
    assert permitted["computed_from_forward"] is False
    # forward legal slice preserved untouched
    assert possibility["support"]["base_ratio"] == "54/60"


def test_k9_07_permissions_denied_use_no_cached_bypass():
    """K9_07 — dropping the dependency use atom denies the slice; no A bypass."""

    provider_a = build_provider_a()
    bundle_a = TwoContractAdapter(provider_a).run()
    permitted = provider_a.revoked_use(bundle_a["world_receipt"], "WORLD_READ")
    assert permitted["state"] == "PERMITTED"

    mutated = copy.deepcopy(BASELINE_WORLD)
    mutated["permission_ceiling"]["revoked_atoms"] = ["WORLD_READ"]
    mutated["permission_ceiling"]["use_atoms"] = ["POSSIBILITY_QUERY"]
    provider_b = ProviderB(world=mutated)
    bundle_b = TwoContractAdapter(provider_b).run()
    with pytest.raises(PortContractError) as denied:
        provider_b.revoked_use(bundle_b["world_receipt"], "WORLD_READ")
    assert denied.value.code == "DENIED_USE"
    # cached A result must not satisfy B's denied request
    with pytest.raises(PortContractError):
        provider_b.revoked_use(bundle_a["world_receipt"], "WORLD_READ")


def test_k9_08_two_channel_refresh_two_independent_successors():
    """K9_08 — binding and publication refresh are independent; prior immutable."""

    provider = build_provider_a()
    adapter = TwoContractAdapter(provider)
    first = adapter.run()
    first_digest = first["world_receipt"]["selection_digest"]

    binding_refresh = provider.refresh_binding_generation()
    assert binding_refresh["channel"] == "H2_GENERATED_BINDING_REFRESH"
    after_binding = adapter.run()
    publication_refresh = provider.refresh_publication_generation()
    assert publication_refresh["channel"] == "H2_PUBLICATION_BOUNDARY_REFRESH"
    after_publication = adapter.run()

    assert after_binding["world_receipt"]["binding_generation"] == 1
    assert after_binding["world_receipt"]["publication_generation"] == 0
    assert after_publication["world_receipt"]["binding_generation"] == 1
    assert after_publication["world_receipt"]["publication_generation"] == 1
    # two independent successors
    assert (
        after_binding["world_receipt"]["selection_digest"]
        != after_publication["world_receipt"]["selection_digest"]
    )
    # prior receipts immutable
    assert first["world_receipt"]["selection_digest"] == first_digest
    assert first_digest != after_binding["world_receipt"]["selection_digest"]
