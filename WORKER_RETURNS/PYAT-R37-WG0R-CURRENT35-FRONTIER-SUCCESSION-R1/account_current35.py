"""Lossless accounting projection of inherited authority, never new issuance."""
import base64
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P2_SHA = 'd38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6'
PACK_SHA = '64a43ba2d7564d7681770065b843273330dc368b8d01bf328a8af7b19878bd98'
ACTIVE_PACK = ROOT/'sources/recovered_disposition/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv'


def decode_dispositions(row_count=18276, *, pack_path=None):
    pack_path = ACTIVE_PACK if pack_path is None else Path(pack_path)
    packs = list(csv.DictReader(pack_path.open()))
    if len(packs)!=1: raise ValueError('DISPOSITION_PACK_CARDINALITY')
    pack = packs[0]
    if pack['p2_sha256']!=P2_SHA or int(pack['p2_row_count'])!=row_count:
        raise ValueError('PACK_NOT_BOUND_TO_EXACT_P2')
    payload = base64.b64decode(''.join(pack['payload_b64_'+str(i)] for i in range(4)),validate=True)
    if len(payload)!=row_count or hashlib.sha256(payload).hexdigest()!=PACK_SHA:
        raise ValueError('DISPOSITION_PAYLOAD_MISMATCH')
    codes = dict(x.split('=') for x in pack['use_code_map'].split(';'))
    if codes != {str(i):c for i,c in enumerate(['SEM','TOP','POS','END','CTX','SCX','ADM','REJ','CPC','BLK'])}:
        raise ValueError('DISPOSITION_CODE_MAP_MISMATCH')
    if pack['format_version']!='P2_ORDINAL_BYTEPACK_V1' or pack['payload_sha256']!=PACK_SHA or int(pack['payload_bytes'])!=row_count:
        raise ValueError('DISPOSITION_HEADER_MISMATCH')
    if any(b&0xc0 or str(b&15) not in codes for b in payload):
        raise ValueError('UNRECOGNIZED_PACK_BITS')
    return payload,codes


def pack_receipt():
    pack=next(csv.DictReader(ACTIVE_PACK.open()))
    payload=base64.b64decode(''.join(pack['payload_b64_'+str(i)] for i in range(4)),validate=True)
    try:
        decode_dispositions()
        state='EXACT_PACK_VERIFIED'
    except ValueError as exc: state=str(exc)
    return {'state':state,'claimed_bytes':int(pack['payload_bytes']),'observed_bytes':len(payload),
            'claimed_sha256':pack['payload_sha256'],'observed_sha256':hashlib.sha256(payload).hexdigest(),
            'reserved_bit_violations':sum(bool(b&192) for b in payload),
            'scope':'BYTE_EXACT_RECOVERY_OF_FROZEN_ACCEPTED_PAYLOAD__NO_NEW_SEMANTIC_ISSUANCE',
            'active_path':str(ACTIVE_PACK.relative_to(ROOT)),
            'historical_red_path':'sources/local_archive/CURRENT35_IMPLEMENTATION_DISPOSITION_LEDGER.csv'}


def load():
    p = ROOT/'sources/local_archive/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv'
    data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != P2_SHA:
        raise ValueError('EXACT_P2_IDENTITY_MISMATCH')
    rows = list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
    if len(rows)!=18276 or len({r['question_implementation_id'] for r in rows})!=18276:
        raise ValueError('P2_IDENTITY_OR_CARDINALITY_LOSS')
    try: payload,codes=decode_dispositions(len(rows))
    except ValueError: payload,codes=None,None
    registry = json.loads((ROOT/'sources/local_archive/source_wave_identity_registry_35wave_v1.json').read_text())
    waves = {(s['canonical_display_source'], w['canonical_display_wave']):w
             for s in registry['source_families'] for w in s['waves'] if w['closed_35_member']}
    actual = {(r['source_family'],r['wave']) for r in rows}
    if set(waves)!=actual or len(waves)!=35:
        raise ValueError('ALL35_WAVE_ANTI_JOIN_FAILED')
    ledger=[]
    for ordinal,row in enumerate(rows):
        byte=payload[ordinal] if payload is not None else None
        wave = waves[(row['source_family'],row['wave'])]
        ledger.append({
            'p2_ordinal':ordinal,'question_implementation_id':row['question_implementation_id'],
            'exact_identity_sha256':row['exact_identity_sha256'],
            'wave_uid':wave['wave_uid'],'source_family':row['source_family'],'wave':row['wave'],
            'source_variable_code':row['source_variable_code'],
            'governed_use':codes[str(byte&15)] if byte is not None else None,
            'hard_fail':bool(byte&16) if byte is not None else None,
            'route_predicate_required':bool(byte&32) if byte is not None else None,
            'execution_state':('DISPOSITION_CARRIER_REQUIRES_EXACT_REPUBLICATION' if byte is None else
                               'HELD_BY_EXISTING_AUTHORITY' if byte&16 else
                               'ORIGINAL_OPERATION_BINDING_AND_WARRANT_NOT_WITNESSED'),
        })
    return ledger, waves, registry


def main():
    rows,waves,registry=load()
    out=ROOT/'evidence'
    keys=list(rows[0])
    with (out/'current35_implementation_accounting.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,keys,lineterminator="\n");w.writeheader();w.writerows(rows)
    wave_rows=[]
    for (family,wave),data in sorted(waves.items()):
        members=[r for r in rows if r['wave_uid']==data['wave_uid']]
        wave_rows.append({'source_family':family,'wave':wave,'wave_uid':data['wave_uid'],
                          'implementations':len(members),
                          'hard_fail':None if any(r['hard_fail'] is None for r in members) else sum(r['hard_fail'] for r in members),
                          'route_predicate_required':None if any(r['route_predicate_required'] is None for r in members) else sum(r['route_predicate_required'] for r in members),
                          'operation_execution':'NOT_CLAIMED__METADATA_ACCOUNTING_ONLY'})
    with (out/'all35_wave_conservation.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,list(wave_rows[0]),lineterminator="\n");w.writeheader();w.writerows(wave_rows)
    census=next((ROOT/'sources/inheritance').rglob('03_P10_FINAL_AUTHORITY_FUNCTION_CENSUS.csv'))
    cs=list(csv.DictReader(census.open()))
    dispositions=Counter()
    for r in cs: dispositions[r['primary_disposition']]+=int(r['unit_count'])
    assert sum(dispositions.values())==65354
    assert dispositions['PRESERVED_AS_EXACT_UNRESOLVED/BLOCKED_AUTHORITY']==76
    # Re-key itinerary only through the retained explicit SWID aliases. Do not
    # default a manual gate or issue an EVS1999 gate from the missing old row.
    itinerary=next((ROOT/'sources/inheritance').rglob('question_wave_itinerary.csv'))
    prior=list(csv.DictReader(itinerary.open())); resolved=[]
    for r in prior:
        candidates=[(s,w) for s in registry['source_families'] for w in s['waves']
                    if r['source'] in s['aliases'] and r['wave'] in w['aliases']]
        if len(candidates)!=1:raise ValueError('ITINERARY_ALIAS_BINDING_NOT_UNIQUE')
        s,w=candidates[0];resolved.append(w['wave_uid'])
    expected_uid={w['wave_uid'] for w in waves.values()}
    receipt={
        'schema':'WG0R_AUTHORITY_CONSERVATION@1','p2_sha256':P2_SHA,'payload_sha256':PACK_SHA,
        'implementations':len(rows),'unique_ids':len({r['question_implementation_id'] for r in rows}),
        'active_waves':len(waves),'families':len({r['source_family'] for r in rows}),
        'missing_waves':[],'unexpected_waves':[],'duplicate_ids':[],
        'primary_use_counts':None if rows[0]['governed_use'] is None else dict(Counter(r['governed_use'] for r in rows)),
        'hard_fail_implementations':None if rows[0]['hard_fail'] is None else sum(r['hard_fail'] for r in rows),
        'route_predicate_required':None if rows[0]['route_predicate_required'] is None else sum(r['route_predicate_required'] for r in rows),
        'disposition_carrier':pack_receipt(),
        'p10_accounting_units':sum(dispositions.values()),'p10_census_rows':len(cs),
        'p10_dispositions':dict(dispositions),'p10_exact_held_states':76,
        'old_itinerary_only_uids':sorted(set(resolved)-expected_uid),
        'current35_without_old_itinerary_gate':sorted(expected_uid-set(resolved)),
        'all35_operation_execution':'UNVERIFIED__NO_RAW_READS_OR_SOURCE_WARRANT_ISSUED',
        'pending_edge':'EXACT_ACCEPTED_AUTHORITY_TO_OPERATION_CATALOG_BINDING_AND_FULL_FRONTIER_WITNESS',
    }
    (out/'current35_conservation.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))


if __name__=='__main__': main()
