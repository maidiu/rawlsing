from __future__ import annotations

from copy import deepcopy

import pytest

from rawlsing_next.pre553_c11_ingest import C11IngestValidationError, validate_c11_source_release
from rawlsing_next.pre553_physical_decoder import (
    MAX_READ_ROWS,
    PhysicalCell,
    PhysicalMissingState,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    SourceConfigurationBindingError,
    build_governed_c11_projection,
    decode_fixture_config,
    project_c11_candidate_from_config,
    row_native_keys_from_transport,
    unjoined_r157_original_item_census,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    SourceBackedC11FacadeError,
)
from rawlsing_next.tests.test_pyat940_s1b_support import (
    build_scenario,
    make_config,
    write_fixture,
)


def _events_by_row(candidate, projection):
    row_by_respondent = {
        binding.respondent_ref.content_hash: binding.row_ordinal
        for binding in projection.row_bindings
    }
    return {
        row_by_respondent[event.scoped_respondent_ref["content_hash"]]: event
        for event in candidate.respondent_events
    }


def test_b05_physical_missing_dk_refusal_and_routing_unknown_are_distinct(tmp_path):
    scenario = build_scenario(
        tmp_path / "states",
        source_format="SAV",
        values=(1.0, 7.0, None, 8.0),
        config_kwargs={"missing_range": True},
    )
    incidence = scenario["incidence"]
    try:
        cells = {(cell.row_ordinal, cell.variable_name): cell for cell in scenario["cells"]}
        assert cells[(1, "q101")].missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
        assert cells[(2, "q101")].missing_state is PhysicalMissingState.FORMAT_USER_MISSING_VALUE
        assert cells[(2, "q101")].source_missing_declaration == {"kind": "discrete", "value": 7.0}
        assert cells[(3, "q101")].missing_state is PhysicalMissingState.SYSTEM_MISSING
        assert cells[(4, "q101")].missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE

        events = _events_by_row(scenario["candidate"], scenario["projection"])
        assert events[1].response_state == "SUBSTANTIVE_RESPONSE"
        assert events[2].response_state == "DK"
        assert events[3].response_state == "MISSING"
        assert events[4].response_state == "REFUSAL"
        assert len(set(events)) == 4
    finally:
        incidence.close()

    # A source label/missing declaration is not semantic authority.  The same
    # bytes decoded against a mapping that only knows observed 7.0 must refuse;
    # physical missingness cannot be promoted by the decoder or inferred away.
    path, source_sha, rows = write_fixture(
        tmp_path / "label-only", source_format="SAV", values=(7.0, 1.0), missing_range=True
    )
    document = make_config(
        source_format="SAV",
        active_source_sha256=source_sha,
        row_count=rows,
        values=(7.0, 1.0),
        user_missing_range=False,
    )
    config = SourceConfig(document)
    incidence = decode_fixture_config(config, path)
    try:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=4)
        projection = build_governed_c11_projection(config, row_native_keys=keys)
        with pytest.raises(SourceBackedC11FacadeError, match="unbound response value"):
            project_c11_candidate_from_config(
                config,
                projection,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=keys,
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b05_observed_zero_and_routing_unknown_do_not_collapse(tmp_path):
    scenario = build_scenario(
        tmp_path / "zero",
        source_format="SAV",
        values=(0.0, 1.0),
        config_kwargs={"routing_state": "ROUTING_UNKNOWN"},
    )
    incidence = scenario["incidence"]
    try:
        assert {fact.routing_state for fact in scenario["projection"].routing} == {"ROUTING_UNKNOWN"}
        assert {fact.typed_state for fact in scenario["projection"].routing} == {"ROUTING_UNKNOWN"}
        events = _events_by_row(scenario["candidate"], scenario["projection"])
        assert events[1].response_state == "SUBSTANTIVE_RESPONSE"
        assert events[1].canonical_response_value_if_authorized == "0.0"
        assert events[2].response_state == "SUBSTANTIVE_RESPONSE"
        assert len(scenario["candidate"].routing_eligibility_facts_or_exact_rules) == 2
        assert all(
            fact.typed_state == "ROUTING_UNKNOWN"
            for fact in scenario["candidate"].routing_eligibility_facts_or_exact_rules
        )
    finally:
        incidence.close()

    # An observed zero is not a free INAPPLICABLE/routing zero.  If it is not
    # explicitly bound, the actual first consumer must refuse the cell.
    path, source_sha, rows = write_fixture(
        tmp_path / "zero-unbound", source_format="SAV", values=(0.0, 1.0)
    )
    document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=rows, values=(1.0,)
    )
    config = SourceConfig(document)
    incidence = decode_fixture_config(config, path)
    try:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=4)
        projection = build_governed_c11_projection(config, row_native_keys=keys)
        with pytest.raises(SourceBackedC11FacadeError, match="unbound response value"):
            project_c11_candidate_from_config(
                config,
                projection,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=keys,
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b05_dta_extended_missing_token_is_preserved(tmp_path):
    scenario = build_scenario(
        tmp_path / "dta-missing",
        source_format="DTA",
        values=("a", 1.0, None),
        config_kwargs={"extended_missing": True},
    )
    incidence = scenario["incidence"]
    try:
        cells = {(cell.row_ordinal, cell.variable_name): cell for cell in scenario["cells"]}
        assert cells[(1, "q101")].missing_state is PhysicalMissingState.FORMAT_EXTENDED_MISSING
        assert cells[(1, "q101")].source_missing_declaration == {
            "kind": "extended", "reader_token": "a", "stata_token": ".a",
        }
        assert cells[(3, "q101")].missing_state is PhysicalMissingState.SYSTEM_MISSING
        events = _events_by_row(scenario["candidate"], scenario["projection"])
        assert events[1].response_state == "DK"
        assert events[2].response_state == "SUBSTANTIVE_RESPONSE"
        assert events[3].response_state == "MISSING"
    finally:
        incidence.close()


def test_b06_multiselect_occurrences_and_duplicate_identity_conservation(tmp_path):
    scenario = build_scenario(
        tmp_path / "multi",
        source_format="SAV",
        values=(1.0,),
        config_kwargs={"occurrences": 2},
    )
    incidence = scenario["incidence"]
    try:
        events = scenario["candidate"].respondent_events
        assert len(events) == 2
        assert len({event.ref for event in events}) == 2
        ranks = {
            event.multiplicity_order_rank_fields["index"] for event in events
        }
        assert ranks == {0, 1}
    finally:
        incidence.close()

    # Duplicate occurrence identity is a storage duplicate, not a new event.
    path, source_sha, rows = write_fixture(
        tmp_path / "multi-dup", source_format="SAV", values=(1.0,)
    )
    document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=rows,
        values=(1.0,), occurrences=2,
    )
    document["response_slots"][0]["values"][0]["occurrences"][1]["key"] = "0"
    config = SourceConfig(document)
    incidence = decode_fixture_config(config, path)
    try:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=4)
        projection = build_governed_c11_projection(config, row_native_keys=keys)
        candidate = project_c11_candidate_from_config(
            config,
            projection,
            cells=tuple(incidence.iter_cells(4)),
            row_native_keys=keys,
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        with pytest.raises(C11IngestValidationError, match="duplicate response occurrence identity"):
            validate_c11_source_release(candidate)
    finally:
        incidence.close()


def test_b06_slot_owner_absence_and_explicit_multiowner(tmp_path):
    path, source_sha, rows = write_fixture(
        tmp_path / "owner-missing", source_format="SAV", values=(1.0,)
    )
    missing_owner_document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=rows,
        values=(1.0,), duplicate_slot_owner=True, include_slot_owner_set=False,
    )
    missing_owner_config = SourceConfig(missing_owner_document)
    incidence = decode_fixture_config(missing_owner_config, path)
    try:
        keys = row_native_keys_from_transport(
            missing_owner_config, incidence=incidence, batch_size=4
        )
        with pytest.raises(SourceBackedC11FacadeError, match="implicit/unapproved second physical-slot owner"):
            build_governed_c11_projection(missing_owner_config, row_native_keys=keys)
    finally:
        incidence.close()

    explicit_document = make_config(
        source_format="SAV", active_source_sha256=source_sha, row_count=rows,
        values=(1.0,), duplicate_slot_owner=True, include_slot_owner_set=True,
    )
    explicit_config = SourceConfig(explicit_document)
    incidence = decode_fixture_config(explicit_config, path)
    try:
        keys = row_native_keys_from_transport(explicit_config, incidence=incidence, batch_size=4)
        projection = build_governed_c11_projection(explicit_config, row_native_keys=keys)
        assert len(projection.slot_owner_sets) == 1
        assert projection.slot_owner_sets[0].owner_families == (
            "EmpiricalCoordinateFact@1.0.0", "RespondentEvent@1.0.0",
        )
        candidate = project_c11_candidate_from_config(
            explicit_config,
            projection,
            cells=tuple(incidence.iter_cells(4)),
            row_native_keys=keys,
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        release = validate_c11_source_release(candidate)
        assert release.release_ref.content_hash
    finally:
        incidence.close()


def test_b06_unjoined_items_remain_preparation_and_never_invent_slots(tmp_path):
    census = unjoined_r157_original_item_census()
    ids = {implementation_id for _, implementation_id in census["items"]}
    assert len(ids) == 26

    scenario = build_scenario(tmp_path / "census", source_format="SAV")
    try:
        serialized_item_ids = {
            item["implementation_id"] for item in scenario["document"]["items"]
        }
        response_slot_ids = {
            slot["question_id"] for slot in scenario["document"]["response_slots"]
        }
        assert not (ids & serialized_item_ids)
        assert not (ids & response_slot_ids)
        assert census["status"] == "PREPARATION_HELD__NOT_SCIENCE"
        assert "not administered items" in census["claim_boundary"]
    finally:
        scenario["incidence"].close()

def test_b05_dta_extended_missing_outside_first_probe_chunk(tmp_path):
    values = [1.0] * (MAX_READ_ROWS + 2_000)
    values[MAX_READ_ROWS + 1_000] = "a"
    assert len(values) > MAX_READ_ROWS
    scenario = build_scenario(
        tmp_path / "dta-missing-late",
        source_format="DTA",
        values=values,
        config_kwargs={"extended_missing": True},
    )
    incidence = scenario["incidence"]
    try:
        declarations = incidence.variables[0].missing_declarations
        assert {
            "kind": "extended", "reader_token": "a", "stata_token": ".a",
        } in declarations
        late_row = MAX_READ_ROWS + 1_001
        late_cell = next(
            cell for cell in scenario["cells"]
            if cell.row_ordinal == late_row and cell.variable_name == "q101"
        )
        assert late_cell.missing_state is PhysicalMissingState.FORMAT_EXTENDED_MISSING
        events = _events_by_row(scenario["candidate"], scenario["projection"])
        assert events[late_row].response_state == "DK"
        assert len(scenario["candidate"].respondent_events) == len(values)
    finally:
        incidence.close()
