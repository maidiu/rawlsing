#!/usr/bin/env python3
"""Stdlib-only Rawlsing control-plane verifier and operator helper."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CP = ROOT / "control_plane"
def load(name):
    with (CP / name).open("r", encoding="utf-8") as fh: return json.load(fh)
def by_id(items): return {x["id"]: x for x in items}
def execution_edges(graph): return [e for e in graph["edges"] if e["type"] == "EXECUTION_PRECEDES"]
def validate_dag(graph, errors):
    nodes=by_id(graph["nodes"])
    for e in graph["edges"]:
        if e["from"] not in nodes or e["to"] not in nodes: errors.append(f"edge references unknown node: {e}")
    adj={n:[] for n in nodes}; indeg={n:0 for n in nodes}
    for e in execution_edges(graph): adj[e["from"]].append(e["to"]); indeg[e["to"]]+=1
    q=[n for n,d in indeg.items() if d==0]; seen=0
    while q:
        n=q.pop(); seen+=1
        for m in adj[n]:
            indeg[m]-=1
            if indeg[m]==0: q.append(m)
    if seen != len(nodes): errors.append("EXECUTION_PRECEDES graph contains a cycle")
def validate_repo():
    errors=[]; warnings=[]
    auth=load("authority_registry.json"); current=load("current.json"); graph=load("pipeline_graph.json"); courts=load("courts.json"); policy=load("change_policy.json"); regressions=load("regression_catalog.json"); repair=load("repair_stack.json"); obligations=load("obligations.json")
    auth_ids={e["id"] for e in auth["entries"]}
    for a in current["foundation_authority"]:
        if a not in auth_ids: errors.append(f"current foundation authority missing: {a}")
    node_ids={n["id"] for n in graph["nodes"]}
    if current["active_frontier"] not in node_ids: errors.append("active_frontier not present in pipeline graph")
    receipt_path=CP/"receipts"/f'{current["latest_accepted_receipt"]}.json'
    if not receipt_path.exists(): errors.append(f"latest accepted receipt missing: {receipt_path}")
    else:
        receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
        if not receipt.get("immutable"): errors.append("latest accepted receipt is not marked immutable")
        if not receipt.get("accepted"): errors.append("latest accepted receipt is not accepted")
        if receipt["receipt_id"] != current["latest_accepted_receipt"]: errors.append("receipt id disagrees with current pointer")
    validate_dag(graph, errors)
    court_ids={c["id"] for c in courts["courts"]}
    for n in graph["nodes"]:
        if n.get("court") and n["court"] not in court_ids: errors.append(f'{n["id"]} references missing court {n["court"]}')
    for c in courts["courts"]:
        if not c.get("allowed_claims") or not c.get("forbidden_claims"): errors.append(f'court {c["id"]} lacks explicit claim ceiling')
    required={"C0_IMPLEMENTATION","C1_INTERFACE","C2_AUTHORITY","C3_ARCHITECTURE","C4_DATA_EXECUTION"}
    if set(policy["classes"]) != required: errors.append("change policy classes differ from canonical C0-C4 set")
    reg_ids=[r["id"] for r in regressions["regressions"]]
    if len(reg_ids)!=len(set(reg_ids)): errors.append("duplicate regression ids")
    done=repair["done"]; partial=repair["partial_not_closed"]; active=repair["in_progress"]
    if len(done)!=repair["done_count"] or repair["done_count"]!=16: errors.append("repair-stack DONE accounting mismatch")
    if set(done)&set(partial) or set(done)&set(active) or set(partial)&set(active): errors.append("repair-stack status sets overlap")
    if sorted(set(done+partial+active)) != list(range(1,26)): errors.append("repair-stack does not disposition exactly items 1..25")
    if 25 not in active: errors.append("repair-stack item 25 must remain IN_PROGRESS at R1")
    obligation_ids=[x["id"] for x in obligations["items"]]
    if len(obligation_ids)!=len(set(obligation_ids)): errors.append("duplicate obligation ids")
    phase=next((n for n in graph["nodes"] if n["id"]=="PHASE_D"),None)
    if not phase or phase.get("terminal")!="PHASE_D_GATE_CLOSED": errors.append("Phase-D accepted terminal missing")
    app=next((n for n in graph["nodes"] if n["id"]=="APP_GATE_35"),None)
    if not app or app.get("status")!="LOCKED": errors.append("APP_GATE_35 must be locked at R1")
    return errors,warnings
def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def validate_trusted(artifact_dir):
    errors=[]; auth=load("authority_registry.json"); base=Path(artifact_dir)
    for entry in auth["entries"]:
        if entry.get("kind")!="LIBRARY_ARCHIVE": continue
        matches=list(base.rglob(entry["artifact_basename"]))
        if len(matches)!=1:
            errors.append(f'{entry["id"]}: expected exactly one {entry["artifact_basename"]} under {base}, found {len(matches)}'); continue
        actual=sha256(matches[0])
        if actual!=entry["sha256"]: errors.append(f'{entry["id"]}: SHA-256 mismatch {actual} != {entry["sha256"]}')
    return errors
def cmd_verify(args):
    errors,warnings=validate_repo()
    if args.tier=="trusted":
        if not args.artifact_dir: errors.append("--tier trusted requires --artifact-dir")
        else: errors += validate_trusted(args.artifact_dir)
    for w in warnings: print(f"WARN: {w}")
    if errors:
        for e in errors: print(f"ERROR: {e}")
        print(f"CONTROL_PLANE_INVALID errors={len(errors)}"); return 1
    print(f"CONTROL_PLANE_VALID tier={args.tier}"); return 0
def get_node(stage):
    nodes=by_id(load("pipeline_graph.json")["nodes"])
    if stage not in nodes: raise SystemExit(f"unknown stage: {stage}")
    return nodes[stage]
def cmd_status(_args):
    current=load("current.json"); repair=load("repair_stack.json"); receipt=json.loads((CP/"receipts"/f'{current["latest_accepted_receipt"]}.json').read_text(encoding="utf-8")); node=get_node(current["active_frontier"])
    print(f'foundation={" + ".join(current["foundation_authority"])}'); print(f'latest_accepted_receipt={receipt["receipt_id"]}'); print(f'latest_terminal={receipt["terminal"]}'); print(f'frontier={node["id"]}'); print(f'frontier_status={node["status"]}'); print(f'entry_gate={node.get("entry_gate","")}'); print(f'court={node.get("court","")}'); print(f'repair_stack_done={repair["done_count"]}/25'); print(f'repair_stack_partial={",".join(map(str,repair["partial_not_closed"]))}'); print(f'repair_stack_in_progress={",".join(map(str,repair["in_progress"]))}'); return 0
def cmd_next(_args):
    current=load("current.json"); print(json.dumps(get_node(current["active_frontier"]),indent=2)); return 0
def cmd_court(args):
    courts=by_id(load("courts.json")["courts"])
    if args.id not in courts: raise SystemExit(f"unknown court: {args.id}")
    print(json.dumps(courts[args.id],indent=2)); return 0
def descendants(graph,start):
    adj={}
    for e in execution_edges(graph): adj.setdefault(e["from"],[]).append(e["to"])
    out=[]; seen=set(); stack=[start]
    while stack:
        n=stack.pop()
        for m in adj.get(n,[]):
            if m not in seen: seen.add(m); out.append(m); stack.append(m)
    return out
def cmd_impact(args):
    graph=load("pipeline_graph.json"); policy=load("change_policy.json"); nodes=by_id(graph["nodes"])
    if args.node not in nodes: raise SystemExit(f"unknown node: {args.node}")
    if args.change_class not in policy["classes"]: raise SystemExit(f"unknown change class: {args.change_class}")
    rule=policy["classes"][args.change_class]
    print(json.dumps({"node":args.node,"change_class":args.change_class,"requires_vozhd":rule["requires_vozhd"],"policy":rule,"execution_descendants":descendants(graph,args.node),"law":"Descendants are candidates for revalidation, not automatic invalidation. Upstream authority is never reopened solely by descendant inconvenience."},indent=2)); return 0
def cmd_task(args):
    node=get_node(args.stage)
    if node.get("kind") not in {"EXECUTION_STAGE","SCALE_RELEASE_STAGE","INTEGRATION_STAGE","CLOSURE_STAGE"}: raise SystemExit(f"{args.stage} is not an executable frontier stage")
    print(f"STAGE: {node['id']}"); print(f"ENTRY GATE: {node.get('entry_gate','')}"); print(f"COURT: {node.get('court','')}"); print(f"OWNER: {node.get('owner','')}"); print(f"STATUS: {node.get('status','')}"); print("MANDATORY: read control_plane/worker_task_contract.md and the exact governing authority/receipts before mutation."); print("RETURN: one consolidated immutable receipt or one exact governance blocker."); return 0
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    s=sub.add_parser("verify"); s.add_argument("--tier",choices=["repo","trusted"],default="repo"); s.add_argument("--artifact-dir"); s.set_defaults(func=cmd_verify)
    s=sub.add_parser("status"); s.set_defaults(func=cmd_status)
    s=sub.add_parser("next"); s.set_defaults(func=cmd_next)
    s=sub.add_parser("court"); s.add_argument("--id",required=True); s.set_defaults(func=cmd_court)
    s=sub.add_parser("impact"); s.add_argument("--node",required=True); s.add_argument("--class",dest="change_class",required=True); s.set_defaults(func=cmd_impact)
    s=sub.add_parser("task"); s.add_argument("--stage",required=True); s.set_defaults(func=cmd_task)
    args=p.parse_args(); return args.func(args)
if __name__=="__main__": sys.exit(main())
