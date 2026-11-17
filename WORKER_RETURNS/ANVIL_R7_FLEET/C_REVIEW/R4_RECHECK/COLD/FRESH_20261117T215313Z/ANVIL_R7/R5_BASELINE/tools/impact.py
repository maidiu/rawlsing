#!/usr/bin/env python3
"""Conservative transitive scope of any changed selected architectural node/decision.
Recorded-graph scope only: an independent reviewer must investigate unrecorded semantic dependencies.
"""
import argparse,collections,json,pathlib

def calculate(s, changed_nodes, changed_decisions):
    a=s['architecture'];nodes={n['id']:n for n in a['nodes']};h={v['id']:v for v in s['handoffs']}
    children=collections.defaultdict(set)
    for edge in a['edges']:children[edge['from']].add(edge['to'])
    starts=set(changed_nodes)|{n for n,v in nodes.items() if v.get('decision_id') in changed_decisions}
    if not starts.issubset(nodes):return {'status':'RED_UNKNOWN_ARCHITECTURE_NODE','unknown':sorted(starts-set(nodes))}
    q=collections.deque(starts);closure=set(starts)
    while q:
        for new in children[q.popleft()]:
            if new not in closure:closure.add(new);q.append(new)
    dec=sorted({nodes[n].get('decision_id') for n in closure if nodes[n].get('decision_id')})
    boundaries=sorted({e['boundary'] for e in a['edges'] if e['from'] in closure or e['to'] in closure})
    affected={hid for hid,v in h.items() if v['boundary'] in boundaries or any(z in closure or z in dec for z in v.get('dependencies',[]))}
    # propagate build dependency closure as well
    changed=True
    while changed:
        before=len(affected);affected|={hid for hid,v in h.items() if set(v.get('dependencies',[]))&affected};changed=len(affected)>before
    return {'status':'GRAPH_BASED_ADVISORY_NOT_SEMANTIC_CERTIFICATE','nodes':sorted(closure),'decisions':dec,'boundaries':boundaries,'handoffs':sorted(affected),'recheck':'Independently challenge omitted source/claim/temporal/first-consumer edges and reread affected exact code; graph cannot discover missing dependencies.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('spine');p.add_argument('--node',action='append',default=[]);p.add_argument('--decision',action='append',default=[]);args=p.parse_args()
    result=calculate(json.loads(pathlib.Path(args.spine).read_text()),args.node,args.decision)
    print(json.dumps(result,indent=2))
    raise SystemExit(2 if result['status'].startswith('RED') else 0)
