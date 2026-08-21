"""Post-freeze blind I05 court for PRE553 R5.

The candidate implementation was frozen at d03b25c65519c6c4ab3c89dbe517dba79212b3a4.
Only after that commit existed was the nonce below generated.  The workload is
selected as sha256(nonce + ':' + freeze_sha) mod 4 over the fixed hostile set
(xor, simpson, minority, recursive).  This file contains no candidate tuning.
"""
from __future__ import annotations

import hashlib

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests import test_pre553_empirical_query as qf
from rawlsing_next.tests import test_pre553_discovery_exact as df
from rawlsing_next.test_pre553_r5_frozen_integration import _r5_source

FREEZE_SHA = "d03b25c65519c6c4ab3c89dbe517dba79212b3a4"
NONCE = "65af86b0c241af2f2cd8fec508dd334fd57dadaae4e8ecf6dddeae1acb38b36d"
WORKLOADS = ("xor", "simpson", "minority", "recursive")
SELECTOR_DIGEST = hashlib.sha256(f"{NONCE}:{FREEZE_SHA}".encode("ascii")).hexdigest()
SELECTED = WORKLOADS[int(SELECTOR_DIGEST, 16) % len(WORKLOADS)]


def test_g7_blind_i05_recursive_subgroup_exact_parity(tmp_path):
    assert SELECTOR_DIGEST == "f8b2eb05c519b489e1c6d25ab3c8eeefe2dd3b7bfdd18e2ee992e6007c422dcf"
    assert SELECTED == "recursive"

    source = qf._build_source("r5-blind-recursive", [
        {"id": "R1", "responses": {"Y": 1}, "coords": {"H": 1}},
        {"id": "R2", "responses": {"Y": 0}, "coords": {"H": 0}},
        {"id": "R3", "responses": {"Y": 0}, "coords": {"H": 0}},
        {"id": "R4", "responses": {"Y": 0}, "coords": {"H": 1}},
    ])
    qauth = qf._query_authority("r5-blind-recursive")
    dauth = df._d_auth("r5-blind-recursive-discovery")
    parent = qf._branch_predicate(
        source,
        qauth,
        members=(
            source["respondents"]["R1"],
            source["respondents"]["R2"],
            source["respondents"]["R3"],
        ),
        tag="parent",
    )
    h1 = qf._predicate(source, qauth, qf._coordinate_leaf(source, "H", 1), tag="h1")
    yq = qf._query(source, qauth, parent, ("Y",), tag="y")
    ancestry = ExactRef(
        "DISCOVERY_BRANCH_ANCESTRY",
        "urn:test:r5:blind:i05:parent",
        qf._h("r5-blind-i05-parent-ancestry"),
    )
    grammar = df._grammar(
        operation="I03-OP-r5-blind-recursive-discovery",
        atoms=[
            df._atom("PARENT", parent, "BRANCH", ancestry=(ancestry,)),
            df._atom("H1", h1, "COORDINATE"),
        ],
        templates=[df._qt("Y", yq)],
        rules=[df._rule(
            "child",
            "RECURSIVE_SUBGROUP_FORK",
            "SINGLE_ATOM",
            atom_ids=("H1",),
            baseline_atom_id="PARENT",
            query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )

    reference = df._execute(source, qauth, dauth, grammar, (parent, h1), (yq,))
    rebuilt = _r5_source(source, tmp_path)
    observed = df._execute(rebuilt, qauth, dauth, grammar, (parent, h1), (yq,))

    assert reference.candidate_count == reference.covered_candidate_count == 1
    assert observed.candidate_count == observed.covered_candidate_count == 1
    assert observed.evaluated_frontier_ref == reference.evaluated_frontier_ref
    assert observed.empirical_fact_refs == reference.empirical_fact_refs
    assert observed.replay_ref == reference.replay_ref
    assert [r.ref for r in observed.receipts] == [r.ref for r in reference.receipts]
    assert [r.semantic_projection() for r in observed.receipts] == [r.semantic_projection() for r in reference.receipts]
    assert observed.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert ancestry.as_dict() in observed.receipts[0].branch_or_parent_ancestry_refs
