from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import SimpleNamespace

import pytest

from rawlsing_next import pre553_carrier_execution


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "WORKER_RETURNS"
    / "EE-P2R6S"
    / "05_WVS7_PROJECTION_MATERIALIZER.py"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("ee_p2r6s_wvs7_projection_materializer", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_fields(module):
    coordinate = SimpleNamespace(
        slot=SimpleNamespace(name="B_COUNTRY"),
        source_semantic_authority_ref=module.COORDINATE_AUTH_REF,
    )
    return {
        "coordinate_slots": (coordinate,),
        "projection_authority_ref": module.PROJECTION_AUTH_REF,
        "replay_authority_ref": module.REPLAY_AUTH_REF,
        "tie_order_ref": module.TIE_ORDER_REF,
        "weight_slots": (),
    }


def test_public_wrapper_delegates_once_to_imported_p2r1_binder(monkeypatch):
    module = _load_module()
    assert module._bind_governed_c11_projection is pre553_carrier_execution.bind_governed_c11_projection
    assert "return bind_exact_projection_fields(fields)" not in inspect.getsource(
        module.bind_exact_projection_fields
    )

    calls = []
    sentinel = object()

    def fake_binder(fields):
        calls.append(fields)
        return sentinel

    monkeypatch.setattr(module, "_bind_governed_c11_projection", fake_binder)
    fields = _valid_fields(module)
    assert module.bind_exact_projection_fields(fields) is sentinel
    assert calls == [fields]


def test_frozen_r6s_identities_remain_exact():
    module = _load_module()
    assert module.PROJECTION_IDENTITY_REF.content_hash == (
        "838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d"
    )
    assert module.COORDINATE_SLOT_IDENTITY_REF.content_hash == (
        "4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6"
    )
    assert module.COORDINATE_AUTH_REF.authority_content_hash == (
        "9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
    )
    assert module.LOCK2 == "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
    assert module.TIE_ORDER_REF.content_hash == module.LOCK2

    receipt = module.authority_identity_receipt()
    assert receipt["projection_identity_ref"]["content_hash"] == module.PROJECTION_IDENTITY_REF.content_hash
    assert receipt["coordinate_slot_identity_ref"]["content_hash"] == module.COORDINATE_SLOT_IDENTITY_REF.content_hash
    assert receipt["coordinate_authority_ref"]["authority_content_hash"] == module.COORDINATE_AUTH_REF.authority_content_hash
    assert receipt["tie_order_ref"]["content_hash"] == module.LOCK2


@pytest.mark.parametrize(
    "mutation",
    [
        "coordinate_name",
        "coordinate_authority",
        "projection_authority",
        "replay_authority",
        "tie_order",
        "weight_slots",
    ],
)
def test_authority_substitution_and_mutation_negatives_fail_closed(monkeypatch, mutation):
    module = _load_module()
    fields = _valid_fields(module)

    coordinate = fields["coordinate_slots"][0]
    if mutation == "coordinate_name":
        fields["coordinate_slots"] = (
            SimpleNamespace(
                slot=SimpleNamespace(name="NOT_B_COUNTRY"),
                source_semantic_authority_ref=module.COORDINATE_AUTH_REF,
            ),
        )
    elif mutation == "coordinate_authority":
        fields["coordinate_slots"] = (
            SimpleNamespace(
                slot=coordinate.slot,
                source_semantic_authority_ref=None,
            ),
        )
    elif mutation == "projection_authority":
        fields["projection_authority_ref"] = None
    elif mutation == "replay_authority":
        fields["replay_authority_ref"] = None
    elif mutation == "tie_order":
        fields["tie_order_ref"] = None
    elif mutation == "weight_slots":
        fields["weight_slots"] = (object(),)

    def forbidden_delegate(_fields):
        raise AssertionError("invalid frozen authority reached imported binder")

    monkeypatch.setattr(module, "_bind_governed_c11_projection", forbidden_delegate)
    with pytest.raises(ValueError):
        module.bind_exact_projection_fields(fields)
