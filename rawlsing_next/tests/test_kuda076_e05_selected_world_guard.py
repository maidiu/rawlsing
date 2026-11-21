"""KUDA-076: missing original E05 checks through the real R112 first consumer."""
from copy import deepcopy

import pytest

import rawlsing_next.pre553_universal_world_binding as world
from rawlsing_next.pre553_world_conditioned_progressive_service import (
    WorldConditionedPrefix, WorldConditionedProgressiveError,
    consume_world_conditioned_prefixes,
)
from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_fixture


def _actual():
    handle = _progressive_fixture()
    view = world.progressive_world_view(
        world.ProgressiveWorldRequest(handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL")
    )
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    ctx = world._PROGRESSIVE_CONTEXTS[handle]
    source_prefix = ctx.prefixes[0]
    prefix = WorldConditionedPrefix(
        source_prefix.prefix_id, ctx.target_ref.object_id,
        tuple((ref.object_id, value) for ref, value in source_prefix.conditions),
        view.n10e_steps[0],
    )
    return ctx, ctx.snapshots["T0"], prefix


def test_real_selected_world_and_native_prefix_remain_productive():
    ctx, snapshot, prefix = _actual()
    result = consume_world_conditioned_prefixes(
        snapshot=snapshot, catalog=ctx.catalog, prefixes=(prefix,),
    )
    assert result[0].native_material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    assert result[0].native_material["structural_routes"]
    assert result[0].world_snapshot_hash == snapshot.snapshot_hash


@pytest.mark.parametrize("field,forgery,expected", (
    ("source_root", "OTHER_ROOT", "E05_FIELD_PERMISSION_ROOT_MISMATCH"),
    ("effective_to", "2026-01-01", "E05_FIELD_EFFECTIVE_CLOCK_OUTSIDE_SELECTION"),
    ("publication", "2031-01-01", "E05_FIELD_PUBLICATION_AFTER_SELECTION"),
    ("key", "OTHER_FIELD", "E05_FIELD_PRODUCER_BINDING_MISMATCH"),
))
def test_postread_structural_spoof_rejected(monkeypatch, field, forgery, expected):
    ctx, snapshot, prefix = _actual()
    native_read = ctx.catalog.read

    def forged(s, key):
        item = native_read(s, key)
        if key == "training_access" and item["state"] == "SUPPORTED_TEST_ONLY":
            item = deepcopy(item)
            item["payload"][field] = forgery
        return item

    monkeypatch.setattr(ctx.catalog, "read", forged)
    with pytest.raises(WorldConditionedProgressiveError, match=expected):
        consume_world_conditioned_prefixes(
            snapshot=snapshot, catalog=ctx.catalog, prefixes=(prefix,),
        )


def test_payload_hash_tampering_rejected(monkeypatch):
    ctx, snapshot, prefix = _actual()
    native_read = ctx.catalog.read

    def forged(s, key):
        item = native_read(s, key)
        if key == "training_access" and item["state"] == "SUPPORTED_TEST_ONLY":
            item = deepcopy(item)
            item["payload"]["value"] = not item["payload"]["value"]
        return item

    monkeypatch.setattr(ctx.catalog, "read", forged)
    with pytest.raises(WorldConditionedProgressiveError, match="E05_FIELD_PAYLOAD_HASH_MISMATCH"):
        consume_world_conditioned_prefixes(
            snapshot=snapshot, catalog=ctx.catalog, prefixes=(prefix,),
        )


def test_empirical_permission_root_spoof_rejected(monkeypatch):
    ctx, snapshot, prefix = _actual()
    native_read = ctx.catalog.read

    def forged(s, key):
        item = native_read(s, key)
        if key == "empirical":
            item = deepcopy(item)
            item["permission_root"] = "OTHER_ROOT"
        return item

    monkeypatch.setattr(ctx.catalog, "read", forged)
    with pytest.raises(WorldConditionedProgressiveError, match="E05_EMPIRICAL_PERMISSION_ROOT_MISMATCH"):
        consume_world_conditioned_prefixes(
            snapshot=snapshot, catalog=ctx.catalog, prefixes=(prefix,),
        )
