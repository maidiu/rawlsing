"""Construction-dependency DAG vs represented causal DAG validation.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Construction edges (RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON) live outside causal
parentship. Any endpoint->childhood edge in the CAUSAL graph is
CAUSAL_TEMPORAL_INVERSION. Both graphs must be acyclic.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .core import h_obj, typed, S

DAG_VERSION = "TWO_DAG_VALIDATION@1.0-LAB"


def _is_acyclic(nodes: List[str], edges: List[Dict[str, str]]) -> bool:
    import collections
    adj = collections.defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for e in edges:
        if e["from"] not in indeg or e["to"] not in indeg:
            continue
        adj[e["from"]].append(e["to"])
        indeg[e["to"]] += 1
    queue = [n for n in nodes if indeg[n] == 0]
    seen = 0
    while queue:
        n = queue.pop()
        seen += 1
        for m in adj[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    return seen == len(nodes)


def build_construction_graph(pipeline_nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """M -> T -> P -> Q -> S -> E -> H -> F -> C -> A with the typed E->H edge."""
    order = ["M_MOTHER_CHECKPOINT", "T_PENDING_TARGET", "P_PROPOSALS", "Q_QUALIFICATION",
             "S_SELECTION", "E_ENDPOINT_CONSTRAINTS", "H_PREHISTORY_CONSTRUCTION",
             "F_FORWARD_REPLAY", "C_RECONCILIATION", "A_ADMISSION"]
    edges = []
    for a, b in zip(order, order[1:]):
        etype = ("RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON"
                 if (a, b) == ("E_ENDPOINT_CONSTRAINTS", "H_PREHISTORY_CONSTRUCTION")
                 else "CONSTRUCTION_PIPELINE_FLOW")
        edges.append({
            "from": a, "to": b,
            "edge_type": etype,
            "algorithm_time": True,
            "causal_parent": False,
        })
    return {
        "graph_kind": "SOFTWARE_CONSTRUCTION_DEPENDENCY_DAG",
        "nodes": order,
        "edges": edges,
        "E_to_H_typed_only": True,
        "acyclic": _is_acyclic(order, edges),
    }


def build_causal_graph(mother_events: List[Dict[str, Any]],
                       dad_events: List[Dict[str, Any]],
                       continuation_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Represented in-world causal DAG from actual event chronology only."""
    nodes: List[str] = []
    edges: List[Dict[str, str]] = []
    all_events = []
    for e in mother_events:
        all_events.append(("M", e))
    for e in dad_events:
        all_events.append(("D", e))
    for e in continuation_events:
        all_events.append(("C", e))
    for _, e in all_events:
        nodes.append(e["event_id"])
    for _, e in all_events:
        for p in e.get("causal_parent_event_ids", []):
            edges.append({"from": p, "to": e["event_id"],
                          "edge_type": "CAUSAL_PARENT", "causal_parent": True})
    acyclic = _is_acyclic(nodes, edges) if nodes else True

    # Detect temporal inversion: any causal edge whose 'from' event has a strictly
    # later effective_index than the 'to' event (endpoint->childhood = inversion).
    index_by_id = {e["event_id"]: e.get("effective_index", 0) for _, e in all_events}
    inversions = []
    for e in edges:
        src = index_by_id.get(e["from"], 0)
        dst = index_by_id.get(e["to"], 0)
        if src > dst:
            inversions.append({"edge": e, "from_index": src, "to_index": dst})
    return {
        "graph_kind": "REPRESENTED_IN_WORLD_CAUSAL_DAG",
        "nodes": nodes,
        "edges": edges,
        "acyclic": acyclic,
        "causal_endpoint_to_childhood_edges": inversions,
        "zero_causal_endpoint_to_childhood_edges": len(inversions) == 0,
    }


def validate_two_dags(construction: Dict[str, Any], causal: Dict[str, Any]) -> Dict[str, Any]:
    ok = (
        construction.get("acyclic")
        and causal.get("acyclic")
        and construction.get("E_to_H_typed_only")
        and causal.get("zero_causal_endpoint_to_childhood_edges")
        and construction.get("nodes") is not None
    )
    return {
        "dag_version": DAG_VERSION,
        "construction_graph": construction,
        "causal_graph_summary": {
            "n_nodes": len(causal.get("nodes", [])),
            "n_edges": len(causal.get("edges", [])),
            "acyclic": causal.get("acyclic"),
            "causal_endpoint_to_childhood_edges": causal.get(
                "causal_endpoint_to_childhood_edges"
            ),
            "zero_causal_endpoint_to_childhood_edges": causal.get(
                "zero_causal_endpoint_to_childhood_edges"
            ),
        },
        "both_graphs_acyclic": construction.get("acyclic") and causal.get("acyclic"),
        "construction_E_to_H_edge_allowed_and_typed_only": construction.get(
            "E_to_H_typed_only"
        ),
        "causal_childhood_to_endpoint_chronology": causal.get(
            "zero_causal_endpoint_to_childhood_edges"
        ),
        "status": S.LAB_PASS if ok else S.CAUSAL_TEMPORAL_INVERSION,
    }
