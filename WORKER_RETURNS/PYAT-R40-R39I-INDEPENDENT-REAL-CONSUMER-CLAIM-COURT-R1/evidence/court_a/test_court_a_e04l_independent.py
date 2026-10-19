"""Independent I2 Court A (E04L) claim-edge test module.

Authored by the independent reviewer (DeepSeek Harness / DeepSeek V4.1 Flash),
NOT by the E04L author and NOT a copy of the author test module. It imports the
author's *unchanged* fixture/readthrough harness and the *unchanged* original
E04 consumer, but every expectation below is independently recomputed from the
frozen synthetic source or is a reviewer-chosen counterfactual. The two named
fault-witness positives are:

  test_original_consumer_refuses_when_selected_release_removed_source_fixed
  test_stale_b5_current_selection_is_load_bearing
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import replace as _replace
from pathlib import Path
from unittest.mock import patch
import sys

import pytest


def _repo_root() -> Path:
    p = Path(__file__).resolve()
    for cand in p.parents:
        if (cand / "rawlsing_next").is_dir() and (cand / "WORKER_RETURNS").is_dir():
            return cand
    raise RuntimeError("repo root not found")


ROOT = _repo_root()
E04L = ROOT / "WORKER_RETURNS/PYAT-R39-E04L-RELEASE-READTHROUGH-CONSUMER-R1"
for _p in (str(E04L), str(ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import bootstrap  # noqa: E402,F401
from fixture import prepare, ref, CONDITIONS  # noqa: E402
from readthrough import ReadThroughService, ReadThroughError  # noqa: E402
from product.nonparent import consume  # noqa: E402
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash  # noqa: E402
from rawlsing_next import pre553_learned_product_release as m2  # noqa: E402
from rawlsing_next import pre553_learned_world_composition as i4  # noqa: E402
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03  # noqa: E402
import rawlsing_next.pre553_empirical_query as pq  # noqa: E402

PREFIXES = tuple(tuple(("ABC"[i], 1) for i in range(n)) for n in (1, 2, 3))


def _flip_same_marginals(rows):
    rows = [{**r, "responses": dict(r["responses"])} for r in rows]
    next(r for r in rows if all(r["responses"][q] == 1 for q in ("A", "B", "C"))
         and r["responses"]["Y"] == 0)["responses"]["Y"] = 1
    next(r for r in rows if all(r["responses"][q] == 0 for q in ("A", "B", "C"))
         and r["responses"]["Y"] == 1)["responses"]["Y"] = 0
    return rows


def _prefix_oracle(rows):
    out = []
    for conds in PREFIXES:
        sel = [r for r in rows if all(r["responses"][q] == v for q, v in conds)]
        y1 = sum(1 for r in sel if r["responses"]["Y"] == 1)
        out.append({"denominator": len(sel), "cells": {"0": len(sel) - y1, "1": y1}})
    return out


def _served(receipt):
    return [{"denominator": s["denominator"],
             "cells": {c["cell"]: c["raw_numerator_support"] for c in s["cells"]}}
            for s in receipt["material"]["empirical"]["steps"]]


def _empirical_reads(receipt):
    return [x for x in receipt["material"]["values_read"] if x["channel"] == "empirical"]


def test_independent_source_derived_oracle_matches_consumer_reads():
    rows = e03.synthetic_world_rows()
    base_expected = _prefix_oracle(rows)
    p = prepare()
    r = consume(ReadThroughService(p), p.snapshot)
    assert _served(r) == base_expected
    # Native reverse role independently recomputed: A|Y=1 denominator 29.
    sel = [x for x in rows if x["responses"]["Y"] == 1]
    assert len(sel) == 29
    assert sum(1 for x in sel if x["responses"]["A"] == 1) == 18

    sm_rows = _flip_same_marginals(rows)
    assert Counter(x["responses"]["Y"] for x in sm_rows) == Counter(
        x["responses"]["Y"] for x in rows)
    sm_expected = _prefix_oracle(sm_rows)
    assert sm_expected == [{"denominator": 32, "cells": {"0": 13, "1": 19}},
                           {"denominator": 16, "cells": {"0": 5, "1": 11}},
                           {"denominator": 8, "cells": {"0": 1, "1": 7}}]
    p2 = prepare(same_marginals=True)
    r2 = consume(ReadThroughService(p2), p2.snapshot)
    assert _served(r2) == sm_expected
    assert _served(r) != _served(r2)
    assert r["receipt_hash"] != r2["receipt_hash"]
    assert r["material"]["route_probability"] is None
    assert r2["material"]["route_probability"] is None
    assert r["material"]["structural_routes"] == r2["material"]["structural_routes"]


def test_served_values_are_exact_release_bound_producer_objects():
    p = prepare()
    service = ReadThroughService(p)
    receipt = consume(service, p.snapshot)

    b5 = p.composition.b5_selection_receipt
    current = p.lifecycle.resolve_selection_exact(b5.selection_key_ref, b5.ref)
    assert current.state == "CURRENT_SELECTED"
    res = m2.resolve_release_exact(p.repository, current.selected_release_ref)
    subject = res.subject
    disposition = service.provider.catalog.get(subject.ref)
    closure = p.repository.closure_exact(res.release_core.dependency_closure_ref)

    assert service.provider.expected_release == current.selected_release_ref
    assert service.provider.expected_subject == subject.ref
    assert subject.ref == p.composition.m1_disposition.ref
    assert disposition.ref == subject.ref

    reads = _empirical_reads(receipt)
    assert len(reads) == 3
    for step, read in zip(receipt["material"]["empirical"]["steps"], reads):
        key = (step["target"], tuple(tuple(c) for c in step["conditioners"]))
        rec = service.provider.records[key]
        fact = service.provider.catalog.get(rec["fact_ref"])
        query = service.provider.catalog.get(rec["query_ref"])
        pred = service.provider.catalog.get(rec["predicate_ref"])
        assert fact.ref in disposition.empirical_fact_refs
        assert query.ref in disposition.empirical_query_spec_refs
        assert pred.ref in disposition.empirical_predicate_refs
        for obj in (fact, query, pred):
            assert obj.ref in closure.member_refs
        topology = {c["cell"]: c["raw_numerator_support"]
                    for c in canonicalize(fact.target_topology)["complete_cell_semantic_projection"]}
        assert {c["cell"]: c["raw_numerator_support"] for c in step["cells"]} == topology
        assert step["denominator"] == fact.raw_denominator_support
        binding = read["learned_release_binding"]
        assert binding["learned_release_ref"] == current.selected_release_ref.as_dict()
        assert binding["m1_subject_ref"] == subject.ref.as_dict()
        assert binding["m2_resolution_ref"] == res.receipt.ref.as_dict()

    checked = i4.compose_learned_world(_replace(p.contract, lifecycle_actions=()),
                                       m2_repository=p.repository,
                                       lifecycle_executor=p.lifecycle,
                                       m1_disposition=disposition)
    assert checked.receipt.terminal_state == "RULE_SATISFIED"
    assert checked.m2_artifacts.release.ref == current.selected_release_ref


def test_original_consumer_refuses_when_selected_release_removed_source_fixed():
    p = prepare()
    service = ReadThroughService(p)
    first = consume(service, p.snapshot)
    release = p.composition.m2_artifacts.release
    rows_hash = p.native_provider.world["rows_hash"]
    trace_before = list(p.native_provider.trace)
    assert release.ref.key in p.repository._releases
    del p.repository._releases[release.ref.key]
    try:
        refused = False
        try:
            consume(service, p.snapshot)
        except ValueError:
            refused = True
        assert refused, "SEVERED_SELECTED_RELEASE_BUT_ORIGINAL_CONSUMER_STILL_PRODUCTIVE"
        assert p.native_provider.world["rows_hash"] == rows_hash
        assert p.native_provider.trace == trace_before
    finally:
        p.repository.register_release(release)
    assert consume(service, p.snapshot) == first


def test_stale_b5_current_selection_is_load_bearing():
    p = prepare()
    service = ReadThroughService(p)
    first = consume(service, p.snapshot)
    b5 = p.composition.b5_selection_receipt
    p.lifecycle.declare_no_current(
        b5.selection_key_ref,
        expected_previous_receipt_ref=b5.ref,
        event_authority_ref=ref("LifecycleAuthority", "none"),
        event_rule_ref=ref("LifecycleRule", "none"),
        reason_ref=ref("Reason", "none"),
        selection_attestation_ref=ref("SelectionAttestation", "none"),
    )
    refused = False
    try:
        consume(service, p.snapshot)
    except ValueError:
        refused = True
    assert refused, "STALE_B5_SELECTION_SERVED_WITHOUT_CURRENT_SELECTION"
    assert service.historical_receipt(first["receipt_hash"])["archival_only"] is True


def test_substituted_producer_fact_object_for_deepest_query_refuses():
    p = prepare()
    service = ReadThroughService(p)
    deep = service.provider.records[("Y", CONDITIONS)]
    shallow = service.provider.records[("Y", CONDITIONS[:1])]["fact_ref"]
    deep["fact_ref"] = shallow
    with pytest.raises(ValueError):
        consume(service, p.snapshot)


def test_deep_query_cannot_be_served_with_shallower_predicate():
    p = prepare()
    service = ReadThroughService(p)
    deep = service.provider.records[("Y", CONDITIONS)]
    deep["predicate_ref"] = service.provider.records[("Y", CONDITIONS[:1])]["predicate_ref"]
    with pytest.raises(ValueError):
        consume(service, p.snapshot)


def test_forged_source_universe_ref_binding_refuses():
    p = prepare()
    service = ReadThroughService(p)
    record = service.provider.records[("Y", CONDITIONS)]
    record["template"]["source_universe_ref"] = ref(
        "EmpiricalUniverse", "independent-forged-source").as_dict()
    record["template_hash"] = semantic_hash(record["template"])
    with pytest.raises(ValueError):
        consume(service, p.snapshot)


def test_missing_release_dependency_predicate_refuses():
    p = prepare()
    service = ReadThroughService(p)
    record = service.provider.records[("Y", CONDITIONS)]
    del service.provider.catalog.objects[record["predicate_ref"].key]
    with pytest.raises(ValueError, match="PRODUCER_OBJECT_UNAVAILABLE"):
        consume(service, p.snapshot)


def test_only_released_forward_query_is_served():
    p = prepare()
    service = ReadThroughService(p)
    consume(service, p.snapshot)
    with pytest.raises(ValueError, match="RELEASE_QUERY_NOT_INCLUDED"):
        service.provider.progressive("A", (("Y", 1),))
    with pytest.raises(ValueError):
        service.provider.progressive("Y", CONDITIONS + (("D", 1),))


def test_consumer_does_not_recompute_from_original_source_provider():
    p = prepare()
    service = ReadThroughService(p)
    trace_before = list(p.native_provider.trace)
    with patch.object(p.native_provider, "step", side_effect=AssertionError("SOURCE_STEP")), \
         patch.object(p.native_provider, "progressive", side_effect=AssertionError("SOURCE_PROGRESSIVE")), \
         patch.object(pq, "execute_empirical_query", side_effect=AssertionError("SOURCE_QUERY")):
        receipt = consume(service, p.snapshot)
    assert _served(receipt) == _prefix_oracle(e03.synthetic_world_rows())
    assert p.native_provider.trace == trace_before
