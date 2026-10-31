from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import hashlib
import os

import pytest

from rawlsing_next.tests.test_postastra_pe_fixture import law_a_cases
import rawlsing_next.pre553_postastra_pe_generic_world_possibility as pe
import sc0_pe_overlay as overlay

PE_MODULE_GIT_BLOB = "58484f4c3d9aae148d4116dcf00420c432aefcbd"


def _git_blob(path: Path) -> str:
    buf = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(buf)).encode() + b"\0" + buf).hexdigest()


@pytest.fixture(scope="module")
def cases():
    return law_a_cases()


@pytest.fixture(scope="session", autouse=True)
def installed():
    overlay.install()


def _serve(case, *, request=None):
    return pe.serve_generic_world_situated_possibility(
        repository=case["repository"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        request=case["request"] if request is None else request,
        model_rule=case["model_rule"],
        condition_binding_witness=case["witness"],
    )


def test_pinned_pe_module_stays_byte_identical():
    root = Path(os.environ["HQ297_EXACT_PE_ROOT"]).resolve()
    assert _git_blob(root / "rawlsing_next/pre553_postastra_pe_generic_world_possibility.py") == PE_MODULE_GIT_BLOB


def test_positive_overlay_uses_pe_reverse_geometry_not_world_baseline(cases):
    result = _serve(cases["nonparent_reverse"])
    assert result.result_state == "EXACT_SUPPORTED"
    material = result.receipt.material()
    exact = material["n10e_values_read_receipt"]["exact_numerator_and_denominator"]
    assert exact["cell"] == "P1"
    assert exact["numerator"] == 48
    assert exact["denominator"] == 64
    assert material["n9_world"]["clocks"] == {
        "observation_effective": "2008",
        "publication_knowledge": "2010",
        "actor_event": None,
        "request_currentness": "2026-10-14",
    }
    assert material["sc0_overlay"]["grade"] == overlay.GRADE
    assert material["n9_values_read_receipt"]["consumer_id"] == "NONPARENT_APPRENTICESHIP_ENTRY"
    assert material["sc0_overlay_provenance"]["n10e_values_read"].startswith(
        "original PE receipt consumer_exact_geometry"
    )


def test_positive_overlay_keeps_conception_pe_denominator(cases):
    result = _serve(cases["conception_scenario"])
    assert result.result_state == "EXACT_SUPPORTED"
    exact = result.receipt.material()["n10e_values_read_receipt"]["exact_numerator_and_denominator"]
    assert exact["cell"] == "yes"
    assert exact["numerator"] == 21
    assert exact["denominator"] == 30
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in exact["cells"]} == {
        "no": 9,
        "yes": 21,
    }
    assert exact["denominator"] != 60
    assert result.receipt.material()["n9_values_read_receipt"]["consumer_id"] == "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY"


def test_wrong_issuer_refuses_before_enrichment(cases):
    case = cases["nonparent_reverse"]
    old = case["request"].role_reversal_authority_ref
    forged = type(old)(
        authority_id="urn:test:unissued:reversal:WRONG_TOPOLOGY",
        authority_version="999.0.0",
        authority_content_hash="f" * 64,
    )
    request = replace(case["request"], role_reversal_authority_ref=forged)
    result = _serve(case, request=request)
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == pe.REFUSAL_REVERSED_UNAUTHORIZED_ROLE
    assert result.receipt.consumer_exact_geometry is None
    assert "sc0_overlay" not in result.receipt.material()
    assert "n9_values_read_receipt" not in result.receipt.material()


def test_invalidated_snapshot_gets_no_stale_clock_or_value_enrichment(cases):
    case = cases["multi_binding_parent_context"]
    request = replace(
        case["request"],
        n9_world=replace(case["request"].n9_world, n9_snapshot_state="INVALIDATED"),
    )
    result = _serve(case, request=request)
    assert result.result_state == "TYPED_REFUSAL"
    assert result.receipt.refusal_state == pe.REFUSAL_INVALIDATED_CURRENT
    material = result.receipt.material()
    assert "sc0_overlay" not in material
    assert "clocks" not in material["n9_world"]
    assert "scoped_status_rows" not in material["n9_world"]


def test_missing_producer_fails_closed(cases):
    result = _serve(cases["nonparent_reverse"])
    bundle = overlay.fixture_bundle()
    bundle.pop("world_receipt")
    with pytest.raises(overlay.Sc0OverlayContractError, match="MISSING_WORLD_SELECTION_DIGEST"):
        overlay.enrich_material(result, cases["nonparent_reverse"]["request"], bundle)


def test_consumer_severance_fails_closed(cases):
    result = _serve(cases["nonparent_reverse"])
    bundle = overlay.fixture_bundle()
    bundle["consumer_effects"].pop("NONPARENT_APPRENTICESHIP_ENTRY")
    with pytest.raises(
        overlay.Sc0OverlayContractError,
        match="MISSING_CONSUMER_EFFECT:NONPARENT_APPRENTICESHIP_ENTRY",
    ):
        overlay.enrich_material(result, cases["nonparent_reverse"]["request"], bundle)


def test_generated_binding_echo_source_promotion_fails_closed(cases):
    result = _serve(cases["nonparent_reverse"])
    bundle = overlay.fixture_bundle()
    bundle["world_receipt"]["world"]["generated_binding_echo"]["upstream_authorship"] = True
    with pytest.raises(overlay.Sc0OverlayContractError, match="GENERATED_BINDING_ECHO_SOURCE_PROMOTION"):
        overlay.enrich_material(result, cases["nonparent_reverse"]["request"], bundle)


def test_missing_publication_clock_fails_closed(cases):
    result = _serve(cases["multi_binding_parent_context"])
    bundle = overlay.fixture_bundle()
    bundle["world_receipt"]["world"]["time_axes"].pop("published")
    with pytest.raises(overlay.Sc0OverlayContractError, match="MISSING_PUBLICATION_CLOCK"):
        overlay.enrich_material(result, cases["multi_binding_parent_context"]["request"], bundle)
