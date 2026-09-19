from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from rawlsing_next.pre553_physical_decoder import PhysicalVariable
from rawlsing_next.pre553_carrier_execution import bind_governed_c11_projection

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "WORKER_RETURNS/EE-P2R6Q/08_WVS7_FROZEN_P2_PROJECTION_MATERIALIZER.py"

spec = importlib.util.spec_from_file_location("ee_p2r6q_materializer", PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def _variables():
    special = tuple({"kind": "discrete", "value": v} for v in (-5, -4, -2, -1))
    return (
        PhysicalVariable(301, "Q291G5", "double", None, {}, special, {}, {}),
        PhysicalVariable(302, "Q291P5", "double", None, {}, special, {}, {}),
        PhysicalVariable(7, "B_COUNTRY", "double", "ISO 3166-1 numeric country code", {}, (), {}, {}),
    )


def test_complete_projection_binds_through_exact_existing_p2r1_contract():
    projection = m.materialize_and_bind(
        physical_variables=_variables(),
        row_country_values=(231, 840, 404),
        enforce_frozen_dimensions=False,
    )
    assert projection.projection_identity_ref == m.PROJECTION_IDENTITY_REF
    assert projection.expected_source_sha256 == m.SOURCE_SHA256
    assert len(projection.universes) == 1
    assert len(projection.respondents) == 3
    assert len(projection.row_bindings) == 3
    assert len(projection.questions) == 2
    assert len(projection.response_slots) == 2
    assert len(projection.coordinate_slots) == 1
    assert len(projection.routing) == 6
    assert len(projection.weight_slots) == 0
    assert bind_governed_c11_projection(m.build_projection_fields(
        physical_variables=_variables(),
        row_country_values=(231, 840, 404),
        enforce_frozen_dimensions=False,
    )) == projection


def test_coordinate_and_routing_law_is_exact_and_not_missingness_inferred():
    projection = m.materialize_and_bind(
        physical_variables=_variables(),
        row_country_values=(231, 840, 404),
        enforce_frozen_dimensions=False,
    )
    slot = projection.coordinate_slots[0]
    assert slot.slot.name == "B_COUNTRY"
    assert slot.copy_observed_raw is True
    assert slot.native_coordinate_ref == m.NATIVE_COUNTRY_COORDINATE_REF
    by_row = {}
    respondent_row = {b.respondent_ref.object_id: b.row_ordinal for b in projection.row_bindings}
    for fact in projection.routing:
        by_row.setdefault(respondent_row[fact.scoped_respondent_ref["object_id"]], set()).add(fact.routing_state)
    assert by_row == {
        1: {"ELIGIBLE_APPLICABLE"},
        2: {"NOT_ELIGIBLE"},
        3: {"ELIGIBLE_APPLICABLE"},
    }


def test_missing_country_is_unknown_not_inferred_not_eligible():
    projection = m.materialize_and_bind(
        physical_variables=_variables(),
        row_country_values=(None,),
        enforce_frozen_dimensions=False,
    )
    assert {x.routing_state for x in projection.routing} == {"ROUTING_UNKNOWN"}
    assert projection.coordinate_slots[0].values
    assert {x.coordinate_state for x in projection.coordinate_slots[0].values} == {"MISSING"}


def test_exact_unique_source_variable_identity_is_fail_closed():
    bad = _variables() + (PhysicalVariable(700, "B_COUNTRY", "double", None, {}, (), {}, {}),)
    with pytest.raises(ValueError, match="must resolve uniquely"):
        m.build_projection_fields(
            physical_variables=bad,
            row_country_values=(231,),
            enforce_frozen_dimensions=False,
        )
    alias = tuple(
        PhysicalVariable(v.ordinal, "COUNTRY" if v.name == "B_COUNTRY" else v.name,
                         v.storage_type, v.variable_label, v.value_labels,
                         v.missing_declarations, v.display_metadata, v.topology_metadata)
        for v in _variables()
    )
    with pytest.raises(ValueError, match="B_COUNTRY"):
        m.build_projection_fields(
            physical_variables=alias,
            row_country_values=(231,),
            enforce_frozen_dimensions=False,
        )


def test_frozen_dimensions_and_authority_identity_are_explicit():
    with pytest.raises(ValueError, match="613"):
        m.build_projection_fields(
            physical_variables=_variables(),
            row_country_values=(231,),
            enforce_frozen_dimensions=True,
        )
    receipt = m.authority_identity_receipt()
    assert receipt["coordinate_authority_ref"]["authority_id"] == "EE-P2R6Q-WVS7-B-COUNTRY-COORDINATE-SEMANTICS"
    assert receipt["projection_authority_ref"]["authority_id"] == "EE-P2R6Q-WVS7-FROZEN-P2-C11-PROJECTION"
    assert receipt["tie_order_ref"]["content_hash"] == m.LOCK2
    assert m.REQUIRED_COUNTRY_CODES == frozenset({104, 231, 364, 404, 417, 434, 504, 558, 608, 704, 716, 762, 862})
