"""ZAK03S sourcefree positive / two-source / permission / restoration court.

Runs the *real* Route-B C11 builder, I03 and I05.  Only the 700-row historical
calibration registry is copied into temporary synthetic test resources; no
original35 production data or scientific/source authority is inferred.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_v550_question_relation_authority import (
    CALIBRATION_AUTHORITY_PATH,
    _recompute_row_hash,
    load_question_relation_authority,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalQuerySpec
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_zak03s_selected_qsm_reader import (
    SelectedQsmRequest,
    SelectedQsmRouteError,
    execute_selected_qsm_route_b,
)
from rawlsing_next.tests.test_pre553_empirical_query import _h, _ref
from rawlsing_next.tests.test_pre553_route_b_production import _fixture


def _synthetic_qsm(path: Path, *, variant: str, status="GOVERNED_NEUTRAL_COVERAGE"):
    registry = pd.read_csv(CALIBRATION_AUTHORITY_PATH, dtype=str, keep_default_na=False)
    columns = list(registry.columns)
    k = 0
    row = registry.iloc[k].to_dict()
    row.update({
        "source_family": "SURVEY", "canonical_wave": "W1",
        "country_code_scope": "US", "question_id": "Y", "var_code": "Y",
        "authority_rule_id": "SYNTH-QSM-Y",
        "relation_use_status": status,
        "authority_status": (
            "BLOCKED_SOURCE_AUTHORITY" if status.startswith("BLOCKED_")
            else "GOVERNED_NON_DIRECTIONAL_DISPOSITION"
        ),
        "review_notes": f"synthetic independently selected {variant}",
        "current_directional_atom_eligible": "false",
        "driver_id": "", "driver_facet_id": "",
        "question_block_id": "", "structural_domain_id": "",
        "relation_axis_id": "", "target_entity_id": "",
        "relation_projection_polarity": "", "item_reversal": "false",
        "source_response_polarity": "",
    })
    row["row_payload_hash"] = _recompute_row_hash(row, columns)
    registry.loc[k, columns] = [row[c] for c in columns]
    registry.to_csv(path, index=False)
    index = load_question_relation_authority(path)
    assert len(index.rows) == 700
    return index.file_sha256, row["row_payload_hash"], row["authority_version"]


def _use_authority(universe, use_ref, *, decision="ALLOW"):
    return AuthoritySnapshot(
        typed_state=decision,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "zak03s-use"),
        authority_id="ZAK03S-SOURCEFREE-USE",
        authority_version="1.0.0",
        authority_content_hash=_h("zak03s-current-use-content"),
        authority_kind="TARGET_USE_PERMISSION",
        decision_state=decision,
        governed_operations=("ZAK03S-RAW-I03-USE",),
        governed_object_families=("EmpiricalFact@1.0.0",),
        scope_envelope={
            "source_universe_refs": (universe.ref.as_dict(),),
            "target_use_refs": (use_ref.as_dict(),),
        },
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h("zak03s-use-meaning"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "zak03s-use"),
    )


def _authorized_query(original, use_ref, authority):
    fields = dict(original.semantic_fields)
    fields["requested_output_grain"] = {
        **dict(original.requested_output_grain),
        "target_use_ref": use_ref.as_dict(),
        "target_use_authority_ref": authority.authority_ref.as_dict(),
        "target_use_operation": "ZAK03S-RAW-I03-USE",
    }
    return EmpiricalQuerySpec(
        typed_state=original.typed_state,
        authority_snapshot_refs=(
            *original.authority_snapshot_refs, authority.authority_ref
        ),
        dependency_refs=(*original.dependency_refs, use_ref),
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **fields,
    )


def _setup(fx, path, sha, row_sha, version, *, deny=False):
    universe = fx["projection"].universes[0]
    use_ref = _ref("TARGET_USE", "zak03s-raw-i03")
    authority = _use_authority(universe, use_ref, decision="DENY" if deny else "ALLOW")
    query = _authorized_query(fx["raw_query"], use_ref, authority)
    catalog = RuntimeObjectCatalog(
        authorities=fx["catalog"].authorities + (authority,),
        predicates=fx["catalog"].predicates,
        # Preserve original raw/weighted templates consumed by genuine I05.
        queries=fx["catalog"].queries + (query,),
        discovery_authorities=fx["catalog"].discovery_authorities,
    )
    selection = SelectedQsmRequest(
        authority_path=path,
        expected_file_sha256=sha,
        expected_row_hash=row_sha,
        expected_authority_version=version,
        expected_rule_id="SYNTH-QSM-Y",
        source_family="SURVEY", canonical_wave="W1", country_code="US",
        var_code="Y", native_question_ref=fx["qrefs"]["Y"],
        target_use_ref=use_ref, target_use_authority_ref=authority.authority_ref,
        target_use_operation="ZAK03S-RAW-I03-USE",
    )
    return selection, catalog, (I03ExecutionRequest(query.ref, fx["all_p"].ref),)


def _run(fx, selection, catalog, requests):
    return execute_selected_qsm_route_b(
        selection=selection,
        source=fx["stream"],
        projection=fx["projection"],
        runtime_catalog=catalog,
        i03_requests=requests,
        discovery_authority_ref=fx["discovery_authority"].ref,
    )


def test_two_independent_selected_qsm_files_actual_i03_i05_and_restore(tmp_path):
    fx = _fixture()
    a_path = tmp_path / "qsm_selected_A.csv"
    b_path = tmp_path / "qsm_selected_B.csv"
    a_sha, a_row, a_ver = _synthetic_qsm(a_path, variant="A")
    b_sha, b_row, b_ver = _synthetic_qsm(
        b_path, variant="B", status="GOVERNED_CONTEXT_ONLY"
    )
    assert (a_sha, a_row) != (b_sha, b_row)
    a, catalog, requests = _setup(fx, a_path, a_sha, a_row, a_ver)
    valid = _run(fx, a, catalog, requests)
    assert valid.route.c11_release.release_ref
    assert valid.route.i03_results[0].facts[0].raw_denominator_support == 2
    assert valid.route.i05_result.receipts
    assert valid.binding_receipt["qsm_artifact_sha256"] == a_sha
    assert valid.binding_receipt["qsm_row_sha256"] == a_row
    assert valid.binding_receipt["i05_historical_qsm_authority_established"] is False
    assert valid.binding_receipt["original35_native_or_historical_production"] is False

    # Same modern authority objects, but the wrong actual historical source.
    wrong_file = replace(a, authority_path=b_path)
    with pytest.raises(SelectedQsmRouteError, match="file SHA mismatch"):
        _run(fx, wrong_file, catalog, requests)
    # An explicitly selected and separately qualified B *is* distinguishable
    # in the result's historical binding, even though I03 facts remain equal.
    b = replace(
        a, authority_path=b_path, expected_file_sha256=b_sha,
        expected_row_hash=b_row, expected_authority_version=b_ver,
    )
    other = _run(fx, b, catalog, requests)
    assert other.route.i03_results[0].facts[0].ref == valid.route.i03_results[0].facts[0].ref
    assert other.binding_receipt["binding_root"] != valid.binding_receipt["binding_root"]
    assert other.binding_receipt["qsm_resolution"] != valid.binding_receipt["qsm_resolution"]

    restored = _run(fx, a, catalog, requests)
    assert restored.binding_receipt == valid.binding_receipt
    assert restored.route.replay_receipt == valid.route.replay_receipt


def test_wrong_row_and_version_fail_before_actual_reader(tmp_path):
    fx = _fixture()
    path = tmp_path / "qsm_selected.csv"
    sha, row, version = _synthetic_qsm(path, variant="A")
    selection, catalog, requests = _setup(fx, path, sha, row, version)
    for bad, reason in (
        (replace(selection, expected_row_hash="0"*64), "row hash"),
        (replace(selection, expected_authority_version="wrong"), "version"),
        (replace(selection, expected_rule_id="other"), "rule identity"),
        (replace(selection, var_code="X"), "unavailable"),
        (replace(selection, native_question_ref=fx["qrefs"]["X"]), "not an I03 query target"),
    ):
        with pytest.raises(SelectedQsmRouteError, match=reason):
            _run(fx, bad, catalog, requests)


def test_historical_block_and_modern_permission_revocation_and_restore(tmp_path):
    fx = _fixture()
    a_path = tmp_path / "qsm_allow.csv"
    held_path = tmp_path / "qsm_block.csv"
    a_sha, a_row, a_ver = _synthetic_qsm(a_path, variant="ALLOW")
    held_sha, held_row, held_ver = _synthetic_qsm(
        held_path, variant="BLOCK", status="BLOCKED_SOURCE_AUTHORITY"
    )
    a, catalog, requests = _setup(fx, a_path, a_sha, a_row, a_ver)
    first = _run(fx, a, catalog, requests)

    blocked = replace(
        a, authority_path=held_path, expected_file_sha256=held_sha,
        expected_row_hash=held_row, expected_authority_version=held_ver,
    )
    with pytest.raises(SelectedQsmRouteError, match="does not allow"):
        _run(fx, blocked, catalog, requests)

    deny_sel, deny_catalog, deny_requests = _setup(
        fx, a_path, a_sha, a_row, a_ver, deny=True
    )
    with pytest.raises(Exception, match="positive authority required"):
        _run(fx, deny_sel, deny_catalog, deny_requests)

    restored = _run(fx, a, catalog, requests)
    assert restored.binding_receipt == first.binding_receipt


def test_unbound_current_reader_refused_even_with_good_qsm(tmp_path):
    fx = _fixture()
    path = tmp_path / "qsm_selected.csv"
    sha, row, version = _synthetic_qsm(path, variant="A")
    selection, catalog, requests = _setup(fx, path, sha, row, version)
    # The historical file does not grant unqualified I03 execution.
    with pytest.raises(SelectedQsmRouteError, match="target-use permission triple"):
        _run(fx, selection, catalog, fx["requests"][:1])
    with pytest.raises(SelectedQsmRouteError, match="not an I03 query target"):
        _run(
            fx, replace(selection, native_question_ref=fx["qrefs"]["X"]),
            catalog, requests,
        )
