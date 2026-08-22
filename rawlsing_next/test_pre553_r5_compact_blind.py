"""Post-freeze blind I05 court for compact LONG_SHARDED V2.

Candidate implementation was frozen at b643ea6ea08a6ed29e31453135ac9113286d581d.
The nonce below was generated only after that freeze. Workload selection is
sha256(nonce + ':' + freeze_sha) mod 4 over the same pre-frozen hostile set.
"""
from __future__ import annotations

import hashlib

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests import test_pre553_empirical_query as qf
from rawlsing_next.tests import test_pre553_discovery_exact as df
from rawlsing_next.test_pre553_r5_compact_frozen_integration import _r5_source

FREEZE_SHA = "b643ea6ea08a6ed29e31453135ac9113286d581d"
NONCE = "adae6b9e1fac3daa7e06f3ecd333d48127d802324f13d99614bf387fe8315522"
WORKLOADS = ("xor", "simpson", "minority", "recursive")
SELECTOR_DIGEST = hashlib.sha256(
    f"{NONCE}:{FREEZE_SHA}".encode("ascii")
).hexdigest()
SELECTED = WORKLOADS[int(SELECTOR_DIGEST, 16) % len(WORKLOADS)]


def test_compact_g7_blind_i05_recursive_subgroup_exact_parity(tmp_path):
    assert SELECTOR_DIGEST == "ae37ca91e20e16886852408f244d5c45adcc3edb8adba44aeea4a782b41d6953"
    assert SELECTED == "recursive"

    source = qf._build_source(
        "r5-compact-blind-recursive",
        [
            {"id": "R1", "responses": {"Y": 1}, "coords": {"H": 1}},
            {"id": "R2", "responses": {"Y": 0}, "coords": {"H": 0}},
            {"id": "R3", "responses": {"Y": 0}, "coords": {"H": 0}},
            {"id": "R4", "responses": {"Y": 0}, "coords": {"H": 1}},
        ],
    )
    qauth = qf._query_authority("r5-compact-blind-recursive")
    dauth = df._d_auth("r5-compact-blind-recursive-discovery")
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
    h1 = qf._predicate(
        source, qauth, qf._coordinate_leaf(source, "H", 1), tag="h1"
    )
    yq = qf._query(source, qauth, parent, ("Y",), tag="y")
    ancestry = ExactRef(
        "DISCOVERY_BRANCH_ANCESTRY",
        "urn:test:r5:compact:blind:i05:parent",
        qf._h("r5-compact-blind-i05-parent-ancestry"),
    )
    grammar = df._grammar(
        operation="I03-OP-r5-compact-blind-recursive-discovery",
        atoms=[
            df._atom("PARENT", parent, "BRANCH", ancestry=(ancestry,)),
            df._atom("H1", h1, "COORDINATE"),
        ],
        templates=[df._qt("Y", yq)],
        rules=[
            df._rule(
                "child",
                "RECURSIVE_SUBGROUP_FORK",
                "SINGLE_ATOM",
                atom_ids=("H1",),
                baseline_atom_id="PARENT",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
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
    assert [r.semantic_projection() for r in observed.receipts] == [
        r.semantic_projection() for r in reference.receipts
    ]
    assert observed.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert ancestry.as_dict() in observed.receipts[0].branch_or_parent_ancestry_refs
