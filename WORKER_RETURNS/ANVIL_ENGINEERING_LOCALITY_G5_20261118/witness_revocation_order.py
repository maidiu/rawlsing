#!/usr/bin/env python3
"""Frozen-60e767 production revocation-after-yield and canonical 600 order."""
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path
OWNER=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER')
SNAP=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/tmp/snapshot'
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
sys.path[:0]=[str(SNAP),str(MP),str(MP/'vendor')]
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session, DirectEstateError
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
CONTRACT=MP/'R2_PILOT/fixture_contract_pilot.json'
R4=MP/'R4_LOCALITY_EXPERIMENT/locality_adapter.py'

def load(path):
    spec=importlib.util.spec_from_file_location('r4_adapter',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def estate(contract,grant):
    e=contract['estate']
    return VerifiedDirectEstate(e['root'],exact_path=e['exact_path'],
        independently_held_manifest_sha256=e['manifest_sha256'],
        independently_held_i02=ExternalI02Roots(**e['i02']),
        current_authorizer=lambda _r:grant['ok'])

def case(adapter,contract,grant):
    orig=adapter.install() if adapter else None
    second_ref=None; err=None; first_ref=None
    try:
        with DirectEstateI03Session(estate(contract,grant)) as s:
            r=next(iter(s.respondents)); g=s._respondent_family('RoutingEligibilityFact',r)
            first=next(g); first_ref=first.ref.key; grant['ok']=False
            try:
                second=next(g); second_ref=second.ref.key
            except Exception as exc:
                err=f'{type(exc).__name__}: {exc}'
    finally:
        if adapter is not None: adapter.restore(orig)
        restored = adapter is None or DirectEstateI03Session._respondent_family is orig
    return {'first_ref':first_ref,'second_ref':second_ref,'second_error':err,
            'bypassed':err is None and second_ref is not None,'restored':restored}

def order(contract,grant):
    grant['ok']=True
    with DirectEstateI03Session(estate(contract,grant)) as s:
        r=next(iter(s.respondents))
        refs=[o.ref.key for o in s._respondent_family('RoutingEligibilityFact',r)]
    return {'count':len(refs),'sorted':refs==sorted(refs),
            'first':refs[0] if refs else None,'last':refs[-1] if refs else None}

contract=json.loads(CONTRACT.read_text()); grant={'ok':True}; r4=load(R4)
red=case(r4,contract,grant); grant['ok']=True
green=case(None,contract,grant); grant['ok']=True
valid=order(contract,grant)
product=SNAP/'rawlsing_next/pre553_direct_estate_i03.py'
out={'schema':'ANVIL_ENGINEERING_LOCALITY_G5_REVOCATION_ORDER@1',
 'product_file':str(product),'product_sha256':hashlib.sha256(product.read_bytes()).hexdigest(),
 'estate_manifest':contract['estate']['manifest_sha256'],
 'r4_red':red,'production_green':green,'valid_iteration':valid,
 'red_expected':red['bypassed'] is True,
 'green_expected':green['bypassed'] is False and 'current source/operation authority refused' in (green['second_error'] or ''),
 'order_expected':valid['sorted'] and valid['count']>0,
 'all_expected':False}
out['all_expected']=all((out['red_expected'],out['green_expected'],out['order_expected'],red['restored'],green['restored']))
OUT=OWNER/'WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/revocation-order.json'
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_expected'] else 2)
