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
    """Complete source-free event closure, with strict causal clocks."""
    from .core import h_obj
    events={};errors=[]
    for e in mother_events+dad_events+continuation_events:
        eid=e['event_id']
        if eid in events and events[eid]!=e:
            errors.append(dict(code='CONFLICTING_EVENT_ID',event_id=eid))
        else:events[eid]=e
    edges=[];inversions=[]
    for eid,e in events.items():
        for parent in e.get('causal_parent_event_ids',[]):
            edge=dict(from_=parent,to=eid,edge_type='CAUSAL_PARENT',causal_parent=True)
            edge['from']=edge.pop('from_');edges.append(edge)
            if parent not in events:
                errors.append(dict(code='UNRESOLVED_CAUSAL_PARENT',event_id=eid,parent=parent))
            elif events[parent]['effective_index']>=e['effective_index']:
                inversions.append(dict(edge=edge,from_index=events[parent]['effective_index'],to_index=e['effective_index']))
    if inversions:errors.append(dict(code='NONFORWARD_CAUSAL_CLOCK',edges=inversions))
    acyclic=_is_acyclic(list(events),edges)
    if not acyclic:errors.append(dict(code='CAUSAL_CYCLE'))
    return dict(graph_kind='REPRESENTED_IN_WORLD_CAUSAL_DAG',nodes=sorted(events),events=events,
        edges=edges,acyclic=acyclic,causal_endpoint_to_childhood_edges=inversions,
        zero_causal_endpoint_to_childhood_edges=not inversions,complete_parent_closure=not errors,
        errors=errors,event_closure_hash=h_obj(events))


def validate_two_dags(construction: Dict[str, Any], causal: Dict[str, Any]) -> Dict[str, Any]:
    ok = (
        construction.get("acyclic")
        and causal.get("acyclic")
        and causal.get("complete_parent_closure")
        and construction.get("E_to_H_typed_only")
        and causal.get("zero_causal_endpoint_to_childhood_edges")
        and construction.get("nodes") is not None
    )
    return {
        "dag_version": DAG_VERSION,
        "construction_graph": construction,
        "complete_event_closure": causal,
        "causal_graph_summary": {
            "complete_parent_closure": causal.get("complete_parent_closure"),
            "errors": causal.get("errors"),
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
