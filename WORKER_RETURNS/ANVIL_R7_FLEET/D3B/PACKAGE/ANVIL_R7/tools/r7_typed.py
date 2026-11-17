#!/usr/bin/env python3
"""Use mainMAC R6's stricter claim/graph contracts as an additive R7 check.
Preserves the original independent artifact unmodified and makes its useful rules
operative; it cannot issue new source, structural or actor truth.
"""
from __future__ import annotations
import importlib.util,json,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
MODULE=ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6/tools/r6.py'
def load_mainmac():
    spec=importlib.util.spec_from_file_location('anvil_mainmac_r6_strict_claim_graph',MODULE)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def validate(packet,canonical_spine=None):
    e=[]
    if not isinstance(packet,dict) or packet.get('schema')!='ANVIL_R7_TYPED_BOUNDARY_WITNESS':return ['R7_TYPED_BAD_SCHEMA']
    mod=load_mainmac()
    if not isinstance(packet.get('source_cut'),str) or len(packet['source_cut'])!=40 or any(ch not in '0123456789abcdef' for ch in packet['source_cut']):e.append('R7_TYPED_SOURCE_CUT_UNPINNED')
    if packet.get('mainmac_policy_sha256')!=hashlib.sha256((ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6/contracts/policy.json').read_bytes()).hexdigest():e.append('R7_TYPED_POLICY_NOT_PINNED')
    claims=packet.get('claims')
    if not isinstance(claims,list) or not claims:e.append('R7_TYPED_NO_SOURCE_CLAIMS');claims=[]
    for i,c in enumerate(claims):e.extend('R7_TYPED_CLAIM_'+str(i)+':'+x for x in mod.validate_source_claim(c))
    graph=packet.get('graph')
    if not isinstance(graph,dict):e.append('R7_TYPED_NO_WHOLE_MACHINE_GRAPH')
    else:e.extend('R7_TYPED_GRAPH:'+x for x in mod.validate_graph(graph))
    if canonical_spine is not None:
        if packet.get('R5_R6_spine_sha256')!=hashlib.sha256(json.dumps(canonical_spine,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest():
            e.append('R7_TYPED_WITNESS_NOT_BOUND_TO_FULL_SPINE')
        if packet.get('source_cut')!=canonical_spine.get('baseline_sha'):
            e.append('R7_TYPED_SOURCE_CUT_NOT_CANONICAL_C11_CUT')
    return sorted(set(e))
