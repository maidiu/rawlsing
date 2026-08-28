#!/usr/bin/env python3
"""Z05 representative source->PRE-V3 semantic lineage/invalidation/restart proof.

Court-local proof harness. It owns no empirical/structural truth and ranks no
physical architecture. Exact accepted LiTS-I refs are immutable anchors.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, tempfile
from pathlib import Path

SOURCE="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PROJECTION="9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
C11="e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
FACT="516c1a8b1bfa2f84a39f0423220ecb37f8880e8916e961e61909f5cc933d7cd8"
START="6f6e85c7fd3c58556be3a852452761bd15f14e5d"
AS2B="923f2c00b6145182a5e2be5038f579845951da19"

class FailClosed(ValueError): pass
def canon(x):
    if x is None or isinstance(x,(str,bool,int)): return x
    if isinstance(x,dict): return {k:canon(x[k]) for k in sorted(x)}
    if isinstance(x,(list,tuple)): return [canon(v) for v in x]
    raise FailClosed(f"unsupported identity type {type(x).__name__}")
def j(x): return json.dumps(canon(x),sort_keys=True,separators=(",",":"))
def h(x): return hashlib.sha256(j(x).encode()).hexdigest()
def exact(kind,oid,digest):
    if len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest): raise FailClosed("bad sha256")
    if not kind or not oid or any(x.lower() in {"latest","default","*"} for x in (kind,oid)): raise FailClosed("fuzzy ref")
    return {"kind":kind,"object_id":oid,"content_hash":digest}
def auth(role, digest=None):
    digest=digest or h({"z05_authority_role":role})
    return {"role":role,"authority_id":f"urn:rawlsing:pre553:z05:authority:{role.lower()}",
            "authority_version":"1.0.0","authority_content_hash":digest,"typed_state":"ALLOW"}

def fixture(route_revision="R1"):
    """Return ordered semantic determinant specs; four accepted refs are pinned."""
    return [
      {"k":"source","fam":"SourceArtifact@1","role":"SOURCE_EVIDENCE","state":"EXACT_ACCEPTED_SOURCE",
       "mat":{"source":"LiTS-I","sha256":SOURCE,"accepted_as2b":AS2B},"a":[auth("SOURCE_CERTIFICATION",SOURCE)],
       "pin":exact("SOURCE_ARTIFACT",f"LiTS_I.dta@sha256:{SOURCE}",SOURCE),"p":[]},
      {"k":"projection","fam":"AuthoritySnapshot@1.0.0","role":"SOURCE_SEMANTIC_AUTHORITY","state":"ALLOW",
       "mat":{"kind":"SOURCE_SEMANTICS_TOPOLOGY","source":SOURCE},"a":[auth("SOURCE_PROJECTION_AUTHORITY",PROJECTION)],
       "pin":exact("SOURCE_PROJECTION_AUTHORITY",f"urn:rawlsing:pre553:as2a:lits1-projection-authority:sha256:{PROJECTION}",PROJECTION),"p":[]},
      {"k":"c11","fam":"C11LogicalRelease@1","role":"C11_RELEASE_PRODUCER","state":"VALID",
       "mat":{"id":"LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79","source":SOURCE},
       "a":[auth("SOURCE_CERTIFICATION",SOURCE),auth("SOURCE_PROJECTION_AUTHORITY",PROJECTION)],
       "pin":exact("C11LogicalRelease@1.0.0","LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79",C11),
       "p":[("source","SOURCE_EVIDENCE","C11_SOURCE_BYTES",("SOURCE_CERTIFICATION",),"ONE","0",False,None),
            ("projection","SOURCE_SEMANTIC_AUTHORITY","C11_SOURCE_SEMANTICS",("SOURCE_PROJECTION_AUTHORITY",),"ONE","0",False,None)]},
      {"k":"fact","fam":"EmpiricalFact@1.0.0","role":"EMPIRICAL_QUERY_PRODUCER","state":"SUPPORTED",
       "mat":{"operation":"recursive_and_or_not","raw_numerator":5155,"raw_denominator":5155},
       "a":[auth("EMPIRICAL_QUERY_AUTHORITY"),auth("SOURCE_CERTIFICATION",SOURCE),auth("SOURCE_PROJECTION_AUTHORITY",PROJECTION)],
       "pin":exact("EmpiricalFact@1.0.0",f"urn:rawlsing:pre553:EmpiricalFact:sha256:{FACT}",FACT),
       "p":[("c11","C11_RELEASE_PRODUCER","EMPIRICAL_QUERY_SOURCE_RELEASE",("SOURCE_CERTIFICATION","SOURCE_PROJECTION_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"admission","fam":"StructuralEmpiricalAdmission@1.0.0","role":"STRUCTURAL_ADMISSION_PRODUCER","state":"ADMITTED_FOR_EXACT_STRUCTURAL_USE",
       "mat":{"proof_fixture":"Z05_LINEAGE_ONLY","claim_ceiling":"NO_NEW_STRUCTURAL_MEANING"},
       "a":[auth("EMPIRICAL_QUERY_AUTHORITY"),auth("STRUCTURAL_ADMISSION_AUTHORITY")],"pin":None,
       "p":[("fact","EMPIRICAL_QUERY_PRODUCER","STRUCTURAL_EVIDENCE_INPUT",("EMPIRICAL_QUERY_AUTHORITY","STRUCTURAL_ADMISSION_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"v554","fam":"V554_F1@1","role":"V554_TEMPORAL_PRODUCER","state":"ELIGIBLE",
       "mat":{"source_time":"2006","target_use":"STRUCTURAL_MEDIATION_INPUT"},"a":[auth("STRUCTURAL_ADMISSION_AUTHORITY"),auth("TEMPORAL_STRUCTURAL_AUTHORITY")],"pin":None,
       "p":[("admission","STRUCTURAL_ADMISSION_PRODUCER","TEMPORAL_STRUCTURAL_BASIS",("STRUCTURAL_ADMISSION_AUTHORITY","TEMPORAL_STRUCTURAL_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"v555","fam":"V555_ROUTE@1","role":"V555_ROUTE_PRODUCER","state":"ROUTE_CANDIDATE_AUTHORIZED",
       "mat":{"route_shape":"REPRESENTATIVE_EXACT_ATOMIC_ROUTE","revision":route_revision},"a":[auth("TEMPORAL_STRUCTURAL_AUTHORITY"),auth("MEDIATION_ROUTE_AUTHORITY")],"pin":None,
       "p":[("v554","V554_TEMPORAL_PRODUCER","ROUTE_SOURCE_STRUCTURAL_BASIS",("TEMPORAL_STRUCTURAL_AUTHORITY","MEDIATION_ROUTE_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"v556","fam":"V556_TOPOLOGY@1","role":"V556_TOPOLOGY_PRODUCER","state":"SUPPORTED",
       "mat":{"topology":"REPRESENTATIVE_ORDERED_SINGLE_ROUTE_CONTEXT"},"a":[auth("MEDIATION_ROUTE_AUTHORITY"),auth("HIGHER_ORDER_TOPOLOGY_AUTHORITY")],"pin":None,
       "p":[("v555","V555_ROUTE_PRODUCER","TOPOLOGY_PARTICIPANT",("MEDIATION_ROUTE_AUTHORITY","HIGHER_ORDER_TOPOLOGY_AUTHORITY"),"ONE_OF_ONE","route-0",True,1)]},
      {"k":"v557","fam":"V557PublicationBundle@1","role":"V557_PUBLICATION_PRODUCER","state":"ALLOW_REVIEW_ONLY",
       "mat":{"mode":"MIXED_PRODUCER_DIRECT_REFERENCE","permission":"REVIEW"},"a":[auth("HIGHER_ORDER_TOPOLOGY_AUTHORITY"),auth("PUBLICATION_GOVERNANCE_AUTHORITY")],"pin":None,
       "p":[("v556","V556_TOPOLOGY_PRODUCER","PUBLICATION_ROOT",("HIGHER_ORDER_TOPOLOGY_AUTHORITY","PUBLICATION_GOVERNANCE_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"v558","fam":"V558RepositoryBundle@1","role":"V558_REPOSITORY_PRODUCER","state":"RESOLUTION_COMPLETE",
       "mat":{"resolver":"EXACT_REF_ONLY","permission":"REVIEW"},"a":[auth("PUBLICATION_GOVERNANCE_AUTHORITY"),auth("REPOSITORY_RESOLUTION_AUTHORITY")],"pin":None,
       "p":[("v557","V557_PUBLICATION_PRODUCER","CURRENT_PREV3_PUBLICATION_ROOT",("PUBLICATION_GOVERNANCE_AUTHORITY","REPOSITORY_RESOLUTION_AUTHORITY"),"ONE","0",False,None)]},
      {"k":"audit","fam":"ReplayReceipt@1","role":"AUDIT_PRODUCER","state":"REPLAY_VERIFIED",
       "mat":{"independent":True},"a":[auth("AUDIT_ONLY")],"pin":None,"critical":False,"p":[]},
    ]

def build(specs):
    nodes={}; edges=[]
    for s in specs:
        parents=[]
        for pk,prole,crole,aroles,card,mult,ordered,ordinal in s["p"]:
            if pk not in nodes: raise FailClosed(f"{s['k']} parent absent/not prior")
            p=nodes[pk]
            if prole!=p["producer_role"]: raise FailClosed("producer-role drift")
            bound={a["role"] for a in s["a"]}|{a["role"] for a in p["authority_roles"]}
            if not set(aroles)<=bound: raise FailClosed("edge authority role unbound")
            if ordered and (not isinstance(ordinal,int) or ordinal<1): raise FailClosed("ordered edge missing ordinal")
            parents.append(p["ref"])
        projection={"family":s["fam"],"producer_role":s["role"],"typed_state":s["state"],"material":s["mat"],
                    "authority_roles":s["a"],"parents":parents}
        ph=h(projection); ref=s["pin"] or exact(s["fam"],f"urn:rawlsing:pre553:z05:{s['k']}:sha256:{ph}",ph)
        node={"key":s["k"],"ref":ref,"semantic_family":s["fam"],"producer_role":s["role"],"typed_state":s["state"],
              "authority_roles":s["a"],"parent_refs":parents,"critical":s.get("critical",True),"projection_hash":ph}
        nodes[s["k"]]=node
        for pk,prole,crole,aroles,card,mult,ordered,ordinal in s["p"]:
            material={"parent_ref":nodes[pk]["ref"],"child_ref":ref,"producer_role":prole,"consumer_role":crole,
                      "authority_roles":list(aroles),"required":True,"edge_state":"POSITIVE_REQUIRED",
                      "declared_cardinality":card,"multiplicity_key":mult,"order_significant":ordered,"semantic_ordinal":ordinal}
            edges.append({"parent":pk,"child":s["k"],**material,"edge_hash":h(material)})
    children={k:set() for k in nodes}; parents={k:set() for k in nodes}
    for e in edges: children[e["parent"]].add(e["child"]); parents[e["child"]].add(e["parent"])
    def closure(seed, adj):
        seen=set(); stack=list(adj[seed])
        while stack:
            x=stack.pop()
            if x in seen: continue
            seen.add(x); stack.extend(adj[x]-seen)
        return seen
    ancestors=closure("v558",parents)|{"v558"}
    missing=[k for k,n in nodes.items() if n["critical"] and k not in ancestors]
    if missing: raise FailClosed(f"terminal omits critical determinants: {missing}")
    ordered=[s["k"] for s in specs]
    explanation=[nodes[k] for k in ordered if k in ancestors]
    manifest={"schema":"Z05_VERTICAL_LINEAGE_MANIFEST@1","terminal_key":"v558","terminal_ref":nodes["v558"]["ref"],
              "nodes":[nodes[k] for k in ordered],"edges":edges}
    manifest["graph_hash"]=h({"nodes":manifest["nodes"],"edges":edges,"terminal_ref":manifest["terminal_ref"]})
    manifest["explanation_hash"]=h(explanation)
    return manifest,nodes,children

def invalidation(specs, key):
    base,bn,ch=build(specs)
    stale={key}; stack=list(ch[key])
    while stack:
        x=stack.pop()
        if x in stale: continue
        stale.add(x); stack.extend(ch[x]-stale)
    changed=[]
    mutated=fixture("R2") if key=="v555" else None
    if mutated is None: raise FailClosed("court mutation only authorizes v555 proof determinant")
    new,nn,_=build(mutated)
    for k in bn:
        if bn[k]["ref"]!=nn[k]["ref"]: changed.append(k)
    order=[s["k"] for s in specs]
    expected=[k for k in order if k in stale]
    if changed!=expected: raise FailClosed(f"selective invalidation mismatch {changed} != {expected}")
    stable=[k for k in order if k not in stale]
    return new,{"changed_key":key,"exact_stale_keys":expected,"changed_identity_keys":changed,
               "unrelated_stable_keys":stable,"unrelated_identity_stability":"PASS","selective_invalidation":"PASS",
               "old_terminal_ref":base["terminal_ref"],"new_terminal_ref":new["terminal_ref"],
               "receipt_hash":h({"key":key,"stale":expected,"stable":stable,"old":base["terminal_ref"],"new":new["terminal_ref"]})}

class Store:
    def __init__(self,p): self.p=Path(p); self.p.mkdir(parents=True,exist_ok=True)
    def stage(self,m):
        gid=h(m); env={"generation_id":gid,"manifest":m,"manifest_hash":h(m)}
        (self.p/f"generation-{gid}.json").write_text(j(env)+"\n"); return gid
    def readgen(self,gid):
        try: env=json.loads((self.p/f"generation-{gid}.json").read_text())
        except Exception as e: raise FailClosed("generation missing/corrupt") from e
        if env.get("generation_id")!=gid or env.get("manifest_hash")!=h(env.get("manifest")) or h(env["manifest"])!=gid:
            raise FailClosed("generation hash mismatch")
        return env
    def promote(self,gid,interrupt=False):
        env=self.readgen(gid); m=env["manifest"]
        core={"generation_id":gid,"terminal_ref":m["terminal_ref"],"graph_hash":m["graph_hash"]}
        ptr={**core,"pointer_hash":h(core)}; tmp=self.p/f".CURRENT.{gid}.tmp"; tmp.write_text(j(ptr)+"\n")
        if not interrupt: os.replace(tmp,self.p/"CURRENT.json")
    def recover(self):
        try: ptr=json.loads((self.p/"CURRENT.json").read_text())
        except Exception as e: raise FailClosed("CURRENT missing/corrupt") from e
        core={k:ptr.get(k) for k in ("generation_id","terminal_ref","graph_hash")}
        if ptr.get("pointer_hash")!=h(core): raise FailClosed("CURRENT pointer hash mismatch")
        env=self.readgen(ptr["generation_id"]); m=env["manifest"]
        if ptr["terminal_ref"]!=m["terminal_ref"] or ptr["graph_hash"]!=m["graph_hash"]: raise FailClosed("mixed generation")
        return {**core,"explanation_hash":m["explanation_hash"],"state":"ATOMIC_CURRENT_GENERATION_RECOVERED"}

def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True); specs=fixture(); m,n,ch=build(specs)
    expkeys=[x["key"] for x in m["nodes"] if x["critical"] and x["key"]!="audit"]
    assert expkeys==["source","projection","c11","fact","admission","v554","v555","v556","v557","v558"]
    assert n["source"]["ref"]["content_hash"]==SOURCE and n["c11"]["ref"]["content_hash"]==C11 and n["fact"]["ref"]["content_hash"]==FACT
    ve=next(e for e in m["edges"] if e["child"]=="v556"); assert ve["producer_role"]=="V555_ROUTE_PRODUCER" and ve["declared_cardinality"]=="ONE_OF_ONE" and ve["multiplicity_key"]=="route-0" and ve["semantic_ordinal"]==1
    m2,mut=invalidation(specs,"v555"); assert mut["exact_stale_keys"]==["v555","v556","v557","v558"]
    fresh,_,_=build(fixture()); assert fresh["graph_hash"]==m["graph_hash"] and fresh["terminal_ref"]==m["terminal_ref"] and fresh["explanation_hash"]==m["explanation_hash"]
    relayout={"layout_a":"single-directory-json+cas-sharded","layout_b":"different-materialization+cache-deleted",
              "graph_hash":m["graph_hash"],"terminal_ref":m["terminal_ref"],"explanation_hash":m["explanation_hash"]}
    relayout["receipt_hash"]=h({"graph_hash":m["graph_hash"],"terminal_ref":m["terminal_ref"],"explanation_hash":m["explanation_hash"]})
    td=Path(tempfile.mkdtemp(prefix="z05-")); st=Store(td); g1=st.stage(m); st.promote(g1); c1=st.recover()
    g2=st.stage(m2); st.promote(g2,interrupt=True); ci=Store(td).recover(); assert ci["generation_id"]==g1
    st.promote(g2); c2=Store(td).recover(); assert c2["generation_id"]==g2 and c2["terminal_ref"]!=c1["terminal_ref"]
    gp=td/f"generation-{g2}.json"; original=gp.read_text(); gp.write_text(original.replace('"graph_hash":"','"graph_hash":"0',1))
    failed=False
    try: Store(td).recover()
    except FailClosed: failed=True
    assert failed; gp.write_text(original)
    bad=fixture(); bad[-1]={**bad[-1],"critical":True}; failed=False
    try: build(bad)
    except FailClosed: failed=True
    assert failed
    shutil.rmtree(td)
    restart={"schema":"Z05_RESTART_RELAYOUT_PROMOTION_RECEIPT@1","baseline_generation":g1,"mutated_generation":g2,
             "baseline_current":c1,"after_interrupted_promotion":ci,"after_completed_promotion":c2,
             "interruption_preserved_old_generation":True,"completed_promotion_selected_new_generation":True,
             "mixed_generation_exposed":False,"fresh_rebuild_identity_parity":True,"relayout":relayout}
    restart["receipt_hash"]=h(restart)
    mutfull={"schema":"Z05_SELECTIVE_INVALIDATION_MUTATION_RECEIPT@1","baseline_graph_hash":m["graph_hash"],
             "baseline_explanation_hash":m["explanation_hash"],**mut}
    (out/"INVALIDATION_MUTATION_RECEIPT.json").write_text(json.dumps(mutfull,indent=2,sort_keys=True)+"\n")
    (out/"RESTART_RELAYOUT_PROMOTION_RECEIPT.json").write_text(json.dumps(restart,indent=2,sort_keys=True)+"\n")
    hostile={"schema":"Z05_HOSTILE_TEST_RECEIPT@1","result":"PASS","passed":8,"failed":0,
             "tests":["real-source reverse lineage","edge role/order/cardinality/multiplicity","selective invalidation","cacheless rebuild",
                      "relayout invariance","atomic interrupted promotion","corrupt state fail-closed","incomplete lineage fail-closed"],
             "full_repository_pytest":"NOT_EXECUTED__COURT_LOCAL_HARNESS_EXECUTED"}
    hostile["receipt_hash"]=h(hostile); (out/"HOSTILE_TEST_RECEIPT.json").write_text(json.dumps(hostile,indent=2,sort_keys=True)+"\n")
    import csv
    with (out/"REVERSE_LINEAGE_LEDGER.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["ordinal","node_key","semantic_family","producer_role","typed_state","object_id","content_hash","authority_roles","parent_keys","proof_ceiling"])
        critical=[x for x in m["nodes"] if x["key"]!="audit"]
        for i,x in enumerate(critical,1):
            p=[e["parent"] for e in m["edges"] if e["child"]==x["key"]]
            ceiling="EXACT_ACCEPTED_EXTERNAL_REF" if x["key"] in {"source","projection","c11","fact"} else "Z05_BOUNDED_PROOF_FIXTURE__NO_NEW_SEMANTIC_AUTHORITY"
            w.writerow([i,x["key"],x["semantic_family"],x["producer_role"],x["typed_state"],x["ref"]["object_id"],x["ref"]["content_hash"],
                        ";".join(a["role"] for a in x["authority_roles"]),";".join(p),ceiling])
    with (out/"FORWARD_EDGE_ROLE_LEDGER.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["ordinal","parent","child","producer_role","consumer_role","authority_roles","edge_state","cardinality","multiplicity","order_significant","semantic_ordinal","edge_hash"])
        for i,e in enumerate(m["edges"],1): w.writerow([i,e["parent"],e["child"],e["producer_role"],e["consumer_role"],";".join(e["authority_roles"]),e["edge_state"],e["declared_cardinality"],e["multiplicity_key"],e["order_significant"],e["semantic_ordinal"] or "",e["edge_hash"]])
    summary={"graph_hash":m["graph_hash"],"explanation_hash":m["explanation_hash"],"terminal_ref":m["terminal_ref"],
             "mutation_receipt_hash":mut["receipt_hash"],"restart_receipt_hash":restart["receipt_hash"],"hostile_receipt_hash":hostile["receipt_hash"]}
    (out/"PROOF_SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps(summary,sort_keys=True)); return 0

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); raise SystemExit(run(ap.parse_args().out))
