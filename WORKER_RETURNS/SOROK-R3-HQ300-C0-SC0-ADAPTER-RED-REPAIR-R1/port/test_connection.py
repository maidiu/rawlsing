"""Connection oracle: the adapter's empirical lane must come from pinned PE/C1/N10E.

A static TEST_ONLY empirical hint can never satisfy this oracle: the probe
requires (a) real call events into the pinned modules while ``TwoContractAdapter
.run()`` executes, and (b) the served support to equal the producer-computed
geometry.  Both providers are exercised.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from port.adapter import TwoContractAdapter
from port.pinned_producer import (
    PINNED_MODULES,
    ProducerCallCounter,
    compute_pinned_empirical_lane,
    pinned_provenance,
)
from port.provider_a import ProviderA
from port.provider_b import ProviderB

OUT = Path(__file__).resolve().parents[1] / "outputs"


@pytest.mark.parametrize("provider", [ProviderA, ProviderB])
def test_adapter_run_calls_pinned_pe_c1_n10e(provider):
    counter = ProducerCallCounter()
    with counter:
        bundle = TwoContractAdapter(provider()).run()
    modules = set(counter.modules_touched())
    fns = {(c["module"], c["function"]) for c in counter.summary()}
    assert modules == {"PE", "C1", "N10E"}, modules
    assert ("N10E", "provide_empirical_possibility_slice") in fns
    assert ("C1", "compose_positioned_subject_possibility") in fns
    assert ("PE", "serve_generic_world_situated_possibility") in fns
    assert counter.total() > 0
    lane = bundle["empirical_lane"]
    assert lane["connected"] is True
    assert lane["call_total"] > 0
    OUT.mkdir(exist_ok=True)
    (OUT / f"connection_trace_{provider.__name__}.json").write_text(json.dumps({
        "provider": provider.__name__,
        "modules_touched": sorted(modules),
        "call_total": counter.total(),
        "calls": counter.summary(),
        "lane_support": lane["support"],
        "n10e_state": lane["n10e_result_state"],
        "pe_state": lane["pe_result_state"],
        "pinned_provenance": pinned_provenance(),
    }, indent=2, sort_keys=True) + "\n")


@pytest.mark.parametrize("provider", [ProviderA, ProviderB])
def test_served_support_is_producer_derived_not_static_hint(provider):
    counter = ProducerCallCounter()
    with counter:
        bundle = TwoContractAdapter(provider()).run()
    lane = bundle["empirical_lane"]
    # the reported support is the computed lane's, cross-checked against the
    # declared fixture; a static hint would show zero producer calls
    assert counter.total() > 0, "static empirical hint cannot satisfy the connection oracle"
    support = bundle["possibility_receipt"]["support"]
    assert support == lane["support"]
    assert support["target_yes"] == 54 and support["target_no"] == 6
    assert support["denominator"] == 60
    cells = {c["value"]: c for c in lane["cells"]}
    assert cells["yes"]["n"] == 54 and cells["no"]["n"] == 6
    assert cells["yes"]["fraction"] == [9, 10] and cells["no"]["fraction"] == [1, 10]


def test_lane_cannot_be_satisfied_by_declared_hint_alone(monkeypatch):
    """Adversarial: if the producer call is removed the connection must fail closed."""

    import port.adapter as adapter_mod

    def fake_lane(*, counter=None):
        return {
            "connected": False,
            "producer": "STATIC_HINT_ONLY",
            "cells": [],
            "support": {"target_yes": 54, "target_no": 6, "denominator": 60,
                        "base_ratio": "54/60", "minority_ratio": "6/60",
                        "risk_set": "fx:risk:asked_eligible", "routing": "fx:routing:asked",
                        "weight": "fx:design_weight:unit",
                        "uncertainty": "fx:u:fixture_no_real_inference"},
            "denominator": 60,
            "evidence_digest": None,
            "lane_digest": "static",
            "calls": [],
            "call_total": 0,
            "modules_touched": [],
        }

    monkeypatch.setattr(adapter_mod, "compute_pinned_empirical_lane", fake_lane)
    from port.contracts import PortContractError

    with pytest.raises(PortContractError) as exc:
        TwoContractAdapter(ProviderA()).run()
    assert exc.value.code == "INTEGRITY_FAILURE"


def test_pinned_module_blobs_match_manifest():
    man = json.loads(
        (Path(__file__).resolve().parents[1] / "staging" / "staging_manifest.json").read_text()
    )
    by_path = {e["staged_path"]: e for e in man["entries"]}
    prov = pinned_provenance()
    expected = {
        "PE": "58484f4c3d9aae148d4116dcf00420c432aefcbd",
        "C1": "604c8d591d4cc2b646e9b149cdb233fc9d69cf6b",
        "N10E": "23167aa25291fb148b1e3cf210ac33fe7769b783",
    }
    for name, want in expected.items():
        assert prov[name]["git_blob_sha1"] == want, (name, prov[name])
        staged = by_path[f"ns/rawlsing_next/{Path(prov[name]['file']).name}"]
        assert staged["git_blob_sha1"] == want
