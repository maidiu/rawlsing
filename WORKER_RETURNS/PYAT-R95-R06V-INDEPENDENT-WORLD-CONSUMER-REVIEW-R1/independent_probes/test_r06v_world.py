"""R95-R06V independent world/consumer probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_universal_world_binding import (
    R05WorldField, R05WorldConsumerRequest, select_r05_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import (
    P41_COMMIT, P41_PACKET, _build_r05_learned_inprocess,
    _r05_request, _run_r05_p41,
)

REPO_ROOT = Path.cwd()


def _runtime():
    base = Path(tempfile.mkdtemp(prefix="r06v-p41-"))
    archive = base / "p41.tar"
    subprocess.run(
        ["git", "archive", P41_COMMIT, P41_PACKET, "-o", str(archive)],
        cwd=str(REPO_ROOT), check=True, capture_output=True, timeout=180,
    )
    with tarfile.open(archive) as handle:
        handle.extractall(base)
    return base


def _fixture():
    base = _runtime()
    try:
        receipts = _run_r05_p41(str(base / P41_PACKET / "runtime"))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    return _build_r05_learned_inprocess(), receipts


def test_P1_actual_r05_to_p41_positive():
    data, receipts = _fixture()
    view = select_r05_world_view(_r05_request(data, receipts))
    assert view.state == "R05_WORLD_SELECTED_VIEW", view.reason_code
    values = view.consumer_values_read
    assert view.temporal_changed is True
    assert values["t0_routes"]["training"] == "ELIGIBLE"
    assert values["t1_routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert values["t0_n10e_steps"][0]["content_hash"] == values["consumer_result_hash"]
    assert values["t1_n10e_steps"][0]["content_hash"] == values["consumer_result_hash"]
    assert values["coordinator_original_ref"] is not None


def test_H1_hash_clock_only_temporal_mutation_must_refuse():
    data, receipts = _fixture()
    mutated = deepcopy(receipts)
    # Keep the pair clocks/hashes distinct, but make the actual consumer
    # routes and N10W state identical. A hash/clock-only temporal change must
    # not count as consumed pair state.
    mutated["T1"]["structural"]["routes"] = deepcopy(
        mutated["T0"]["structural"]["routes"])
    mutated["T1"]["n10w"] = deepcopy(mutated["T0"]["n10w"])
    mutated["T1"].pop("content_hash", None)
    mutated["T1"]["content_hash"] = semantic_hash(mutated["T1"])
    view = select_r05_world_view(_r05_request(data, mutated))
    assert view.state == "REFUSED" or view.temporal_changed is False, (
        "identical actual consumer routes were accepted as a temporal pair change"
    )
    if view.state == "R05_WORLD_SELECTED_VIEW":
        assert view.consumer_values_read["t0_routes"] != (
            view.consumer_values_read["t1_routes"]
        )


def test_H2_transport_label_without_linked_index_must_refuse():
    data, receipts = _fixture()
    fields = _r05_request(data, receipts).fields
    relation = ExactRef(
        "R06V_TRANSPORT_RELATION", "urn:test:r06v:transport", "e" * 64)
    linked_claim = (
        replace(fields[0], unit="person", relation_ref=relation),
        replace(fields[1], unit="household", relation_ref=relation),
    )
    request = _r05_request(
        data, receipts, fields=linked_claim,
        relation_transport_authorized=True, relation_transport_ref=relation,
    )
    view = select_r05_world_view(request)
    assert view.state == "REFUSED", (
        "person/household pooling accepted from a transport label without a linked indexed query"
    )


def test_H3_context_promotion_with_bogus_ff_authority_must_refuse():
    data, receipts = _fixture()
    fields = _r05_request(data, receipts).fields
    promoted = (
        fields[0],
        replace(fields[1], role="CONTEXT"),
    )
    bogus_ff = ExactRef(
        "R06V_BOGUS_FF_AUTHORITY", "urn:test:r06v:bogus-ff", "f" * 64)
    request = _r05_request(
        data, receipts, fields=promoted, ff_structural_authority_ref=bogus_ff)
    view = select_r05_world_view(request)
    assert view.state == "REFUSED", (
        "context field promoted to structural with an unvalidated FF ref"
    )


def test_H4_actual_consumer_receipt_is_not_a_canned_callback():
    data, receipts = _fixture()
    canned = deepcopy(receipts)
    # The wrapper must not accept an arbitrary caller callback returning a
    # self-consistent receipt; this callback is not actual P41/E04 execution.
    calls = []
    def consumer(label):
        calls.append(label)
        return canned[label]
    request = _r05_request(data, canned, consumer=consumer)
    view = select_r05_world_view(request)
    assert view.state == "REFUSED", (
        "a canned caller callback returning a receipt was accepted as actual P41/E04"
    )
