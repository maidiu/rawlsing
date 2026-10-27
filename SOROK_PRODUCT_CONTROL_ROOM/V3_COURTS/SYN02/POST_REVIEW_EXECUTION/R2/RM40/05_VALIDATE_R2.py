#!/usr/bin/env python3
"""Structural/source-identity validator for the RM40-R2 corrected 40x12 JSON."""
from __future__ import annotations
import argparse, hashlib, json, os, sys

TEN={(f'M{i:02d}',n) for i,n in [(9,'N01'),(10,'N01'),(11,'N01'),(13,'N01'),(14,'N02'),(18,'N01'),(19,'N01'),(24,'N01'),(36,'N01'),(39,'N01')]}
CARRIER={k for k in TEN if k not in {('M14','N02'),('M39','N01')}}
ALLOWED_KINDS={'callable','method','field','config','constant','callsite','prose_abstraction'}
FAKE=('create_gift_shard_from_event','create_disruption_shard_from_event')

def fail(msg: str) -> None:
    raise SystemExit('FAIL: '+msg)

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--json',default=os.path.join(os.path.dirname(__file__),'02_CORRECTED_SOURCE_GRADED_40X12.json'))
    ap.add_argument('--source-root',default='/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging')
    args=ap.parse_args()
    d=json.load(open(args.json))
    if d.get('schema')!='SOROK_SYN02_RM40_R2_CORRECTED_SOURCE_GRADED_40X12': fail('schema')
    rows=d.get('rows',[])
    if [r.get('m') for r in rows]!=[f'M{i:02d}' for i in range(1,41)]: fail('40 ordered M rows')
    cells=[c for r in rows for c in r['cells']]
    if len(cells)!=480: fail(f'cell count {len(cells)}')
    if any([c['n'] for c in r['cells']]!=[f'N{i:02d}' for i in range(1,13)] for r in rows): fail('N order')
    if len({(c['m'],c['n']) for c in cells})!=480: fail('cell uniqueness')
    base_x=sum(c['baseline_s05']=='X' for c in cells); base_d=sum(c['baseline_s05']=='—' for c in cells)
    x=sum(c['mark']=='X' for c in cells); dash=sum(c['mark']=='—' for c in cells)
    if (base_x,base_d,x,dash)!=(126,354,124,356): fail(f'counts {(base_x,base_d,x,dash)}')
    changed={(c['m'],c['n']) for c in cells if c.get('changed_from_s04_s05')}
    if changed!=TEN: fail(f'changed set {changed}')
    carrier={(c['m'],c['n']) for c in cells if c['relation']=='INDIRECT_CARRIER_ONLY'}
    unsupported={(c['m'],c['n']) for c in cells if c['relation']=='UNSUPPORTED'}
    if carrier!=CARRIER or unsupported!={('M14','N02'),('M39','N01')}: fail(f'carrier/unsupported {carrier} {unsupported}')
    if any(c['mark']!='X' for c in cells if c['relation']=='INDIRECT_CARRIER_ONLY'): fail('carrier mark')
    if any(c['mark']!='—' for c in cells if c['relation']=='UNSUPPORTED'): fail('unsupported mark')
    if sum(c['relation']=='DIRECT_CONDITIONAL' for c in cells)!=116: fail('direct relation count')
    if sum(c['relation']=='NONE' for c in cells)!=354: fail('none count')
    if d.get('mismatch_count')!=10 or len(d.get('changed_cells',[]))!=10: fail('ten records')
    if d['m17_correction'].get('actual_symbol')!='apply_gift_disruption_shards_from_events': fail('M17 actual symbol')
    for fake in FAKE:
        if fake in json.dumps(d['rows']) or fake in json.dumps(d['changed_cells']): fail('fake M17 symbol '+fake)
    if any(c.get('source_kind') not in ALLOWED_KINDS for c in cells): fail('cell source kind')
    if any(r.get('symbol_kind') not in ALLOWED_KINDS for r in rows): fail('row symbol kind')
    consumers={r['first_future_consumer'] for r in rows}
    if len(consumers)!=40: fail(f'consumer uniqueness {len(consumers)}')
    if len({r['test_id'] for r in rows})!=40: fail('test id uniqueness')
    if any(c.get('first_future_consumer_grade') not in {'LIVE','TEST_ONLY','IMPLEMENTED_UNWIRED','TO_BUILD','RULE_HELD','SOURCE_HELD'} for c in cells): fail('consumer grade')
    # source identity
    registry=d.get('source_registry',[])
    paths=[f['path'] for f in registry]
    if len(registry)!=59 or len(set(paths))!=59: fail('source registry count')
    files_used={f['path'] for r in rows for f in r['source_files']}
    if files_used != set(paths): fail('source files not equal registry')
    for f in registry:
        b=open(os.path.join(args.source_root,f['path']),'rb').read()
        if hashlib.sha256(b).hexdigest()!=f['sha256'] or len(b)!=f['bytes']: fail('source hash '+f['path'])
    s50=d.get('s50_selected_files',[])
    if len(s50)!=31: fail('s50 count')
    for f in s50:
        b=open(os.path.join(args.source_root,f['path']),'rb').read()
        if hashlib.sha256(b).hexdigest()!=f['sha256'] or len(b)!=f['bytes']: fail('s50 hash '+f['path'])
    # exact symbol names present in the row's selected source files (prose artifacts excluded)
    for r in rows:
        text='\n'.join(open(os.path.join(args.source_root,f['path']),errors='ignore').read() for f in r['source_files'])
        for sym in [s.strip() for s in r['symbols'].split(';') if s.strip()]:
            if sym not in text: fail(f"symbol absent {r['m']} {sym}")
    if len({r['m'] for r in rows})!=40: fail('unique M')
    print('PASS: 40 rows, 480 unique cells, 126/354 baseline, 124/356 final, 10 changed, 8 carrier, 2 unsupported')
    print('PASS: 59/59 source hashes, 31/31 S50 hashes, 40 unique consumers/test IDs, all exact symbols present')
    print('PASS: no fake M17 symbols; X remains scoped historical source, never permission')
if __name__=='__main__': main()
