"""Adapted frozen seven-case acceptance for the D2P3 single producer registry.

These target the new code, not the preserved original D2P/N9C RED modules.
TEST_ONLY synthetic GSS/NCA fixture; no original PDF bytes/rights/science.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from new.d2p.single_registry import (
    D2P3Error, GSS, NCA, ROLES, ProducerRegistry, field_content_ref,
    produce_field, produce_registry, read_exact, read_produced_registry,
    FAMILY, PUBLISHER, FIELD_VERSION, NATIVE_UNIT, PERMISSION,
)

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / "repro" / "n9c_fields.json").read_text())["fields"]


def rows():
    return deepcopy(ROWS)


def registry_and_refs(changed=None):
    source = rows() if changed is None else deepcopy(changed)
    registry = produce_registry(source)
    return registry, registry.refs_by_role()


def test_new_01_exact_producer_refs_are_dereferenced_and_native_numbers_read():
    registry, refs = registry_and_refs()
    receipt = read_produced_registry(registry, as_of="2022-07-08")
    assert receipt["state"] == "TWO_VALUES_READ_TEST_ONLY"
    assert receipt["selected_refs"] == [refs[GSS], refs[NCA]]
    assert receipt["values_read"][0]["field_ref"] == refs[GSS]
    assert receipt["values_read"][0]["values"]["numerator"] == 2388192
    assert receipt["values_read"][1]["values"]["active_subscriptions"] == 23414527


def test_new_02_reader_dependency_readset_is_exact_produced_refs_only():
    registry, refs = registry_and_refs()
    receipt = read_produced_registry(registry, as_of="2022-07-08")
    assert receipt["dependency_readset"] == [refs[GSS], refs[NCA]]
    assert all(ref.startswith("D2P_TESTONLY_FIELD:") for ref in receipt["dependency_readset"])
    assert registry.dereference(refs[GSS])["role"] == GSS
    assert registry.dereference(refs[NCA])["role"] == NCA


def test_new_03_mutated_exported_field_ref_is_denied_not_self_rehashed():
    registry, refs = registry_and_refs()
    field = registry.dereference(refs[GSS])
    old_ref = field["field_ref"]
    field["values"]["numerator"] += 1
    with pytest.raises(D2P3Error) as exc:
        field_content_ref(field)
    assert exc.value.code == "FIELD_CONTENT_REF_MISMATCH"
    assert old_ref == refs[GSS]
    # A new registry containing a mutated field cannot silently pass.
    with pytest.raises(D2P3Error):
        ProducerRegistry((field, registry.dereference(refs[NCA])))


def test_new_04_forged_issuer_signature_cannot_pass_producer_or_reader():
    source = rows()
    source[0]["issuer_signature"] = "FORGED"
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "ISSUER_FORGERY"


def test_new_05_wind_cannot_be_renamed_hydro_turbine_at_same_totals():
    source = rows()
    parts = source[0]["values"]["electricity_subtypes"]
    parts["hydro_turbine"] = parts.pop("wind")
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "GSS_ELECTRICITY_SUBTYPE_IDENTITY_MISMATCH"


def test_new_06_producer_refuses_wrong_person_mobile_unit_before_emission():
    source = rows()
    source[1]["native_unit"] = "PERSON_WITH_MOBILE_DATA"
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "NATIVE_UNIT_OR_MEASURE_MISMATCH"


def test_new_07_publisher_and_source_family_identity_are_verified():
    source = rows()
    source[0]["publisher"] = "Invented Census Foundation"
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "OFFICIAL_PUBLISHER_IDENTITY_MISMATCH"
    source = rows()
    source[1]["family"] = "GH_FAKE_FAMILY"
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "SOURCE_FAMILY_IDENTITY_MISMATCH"


def test_new_08_gss_minus_one_moves_only_gss_ref_value_readset_and_snapshot():
    base_registry, base_refs = registry_and_refs()
    base = read_produced_registry(base_registry, as_of="2022-07-08")
    changed = rows()
    changed[0]["values"]["numerator"] -= 1
    changed[0]["values"]["electricity_subtypes"]["mains"] -= 1
    changed_registry, changed_refs = registry_and_refs(changed)
    changed_read = read_produced_registry(changed_registry, as_of="2022-07-08")
    assert changed_refs[GSS] != base_refs[GSS]
    assert changed_refs[NCA] == base_refs[NCA]
    assert changed_read["values_read"][0]["values"]["numerator"] == 2388191
    assert changed_read["values_read"][1] == base["values_read"][1]
    assert changed_read["test_snapshot_ref"] != base["test_snapshot_ref"]


def test_new_09_nca_plus_one_inverse_isolation():
    base_registry, base_refs = registry_and_refs()
    base = read_produced_registry(base_registry, as_of="2022-07-08")
    changed = rows()
    changed[1]["values"]["active_subscriptions"] += 1
    changed[1]["values"]["prepaid"] += 1
    changed_registry, changed_refs = registry_and_refs(changed)
    changed_read = read_produced_registry(changed_registry, as_of="2022-07-08")
    assert changed_refs[NCA] != base_refs[NCA]
    assert changed_refs[GSS] == base_refs[GSS]
    assert changed_read["values_read"][1]["values"]["active_subscriptions"] == 23414528
    assert changed_read["values_read"][0] == base["values_read"][0]


def test_new_10_revocation_invalidates_dependent_read_without_orphan():
    registry, refs = registry_and_refs()
    registry.revoke(refs[NCA])
    out = read_produced_registry(registry, as_of="2022-07-08", partial_allowed=True)
    assert out["state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert out["dependency_readset"] == [refs[GSS], refs[NCA]]
    assert out["values_read"][0]["role"] == GSS
    assert any(row["role"] == NCA and row["reason"] == "FIELD_REGISTRY_REVOKED"
               for row in out["refusals"])


def test_new_11_publication_cutoff_cold_replay_and_partial_nonpositive():
    registry, _ = registry_and_refs()
    before = read_produced_registry(registry, as_of="2022-03-01", partial_allowed=True)
    at_nca = read_produced_registry(registry, as_of="2022-07-08")
    replay = read_produced_registry(registry, as_of="2022-07-08")
    early = read_produced_registry(registry, as_of="2022-02-23", partial_allowed=True)
    assert before["state"] == "PARTIAL_TEST_ONLY_NOT_POSITIVE"
    assert [row["role"] for row in before["values_read"]] == [GSS]
    assert early["state"] == "REFUSED_REQUIRED_FIELD_TEST_ONLY"
    assert at_nca == replay


def test_new_12_version_permission_and_person_inference_are_refused():
    source = rows()
    source[0]["permission"] = "GRANTED"
    with pytest.raises(D2P3Error) as exc:
        produce_registry(source)
    assert exc.value.code == "REAL_USE_PERMISSION_NOT_ISSUED"
    registry, refs = registry_and_refs()
    for flag in ("requested_person_exposure", "requested_pooling", "requested_model_use"):
        with pytest.raises(D2P3Error) as exc:
            read_produced_registry(registry, as_of="2022-07-08", **{flag: True})
        assert exc.value.code == "PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN"
    assert NATIVE_UNIT[GSS] != NATIVE_UNIT[NCA]
    assert FAMILY[GSS] != FAMILY[NCA]
    assert PUBLISHER[GSS] != PUBLISHER[NCA]


def test_new_13_long_term_identity_and_changed_exported_version_are_exact():
    a = registry_and_refs()[0]
    b = registry_and_refs()[0]
    assert a.refs_by_role() == b.refs_by_role()
    assert a.snapshot_ref() == b.snapshot_ref()
    registry, refs = registry_and_refs()
    field = registry.dereference(refs[GSS])
    field["field_version"] = "MUTATED_VERSION"
    with pytest.raises(D2P3Error) as exc:
        field_content_ref(field)
    assert exc.value.code == "FIELD_CONTENT_REF_MISMATCH"
