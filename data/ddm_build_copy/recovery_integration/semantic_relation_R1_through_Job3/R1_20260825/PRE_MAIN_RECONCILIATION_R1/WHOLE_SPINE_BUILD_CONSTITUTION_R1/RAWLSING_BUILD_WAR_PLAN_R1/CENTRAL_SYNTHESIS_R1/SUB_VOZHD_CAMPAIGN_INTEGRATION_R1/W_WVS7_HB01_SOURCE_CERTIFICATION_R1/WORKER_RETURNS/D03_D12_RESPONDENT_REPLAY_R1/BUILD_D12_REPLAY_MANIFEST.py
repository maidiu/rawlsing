#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, sys
from pathlib import Path

SOURCE_SHA='2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d'
IDENTITY_PROTOCOL='SOURCE_SHA256_PLUS_SOURCE_ROW_ORDINAL'
RESP_CONTRACT='PRE553_WVS7_SCOPED_RESPONDENT@1.0.0'
SCOPE_CONTRACT='PRE553_WVS7_SOURCE_SCOPE_MEMBER_SET@1.0.0'
REPLAY_CONTRACT='PRE553_WVS7_D12_SCOPED_RESPONDENT_REPLAY@1.0.0'
EXPECTED_ROWS=97220
EXPECTED_SCOPES=66
REQUIRED_COLUMNS=['source_row_ordinal','A_YEAR','B_COUNTR','D_INTERV','S007','S025']

def cj(v):
    return json.dumps(v, sort_keys=True, separators=(',',':'), ensure_ascii=False, allow_nan=False)
def sh(v):
    return hashlib.sha256(cj(v).encode('utf-8')).hexdigest()
def exact_ref(kind, ns, material):
    h=sh(material)
    return {'kind':kind,'object_id':f'urn:rawlsing:pre553:gsr07:wvs7:{ns}:sha256:{h}','content_hash':h}
def line_digest_update(h, material):
    b=cj(material).encode('utf-8')
    h.update(len(b).to_bytes(8,'big'))
    h.update(b)

def main(inp, outdir):
    inp=Path(inp); out=Path(outdir); out.mkdir(parents=True,exist_ok=True)
    selected_sha=hashlib.sha256(inp.read_bytes()).hexdigest()
    global_h=hashlib.sha256()
    scopes=[]; cur=None
    row_count=0
    s007_seen=set(); d_seen=set(); d_dupes={}
    with inp.open(newline='',encoding='utf-8') as f:
        r=csv.DictReader(f)
        missing=[x for x in REQUIRED_COLUMNS if x not in (r.fieldnames or [])]
        if missing: raise SystemExit(f'missing columns: {missing}')
        for row in r:
            row_count += 1
            ordinal=int(row['source_row_ordinal'])
            if ordinal != row_count: raise SystemExit(f'ordinal mismatch {ordinal} != {row_count}')
            year=int(float(row['A_YEAR'])); country=int(float(row['B_COUNTR'])); s025=int(float(row['S025']))
            key=(s025,country,year)
            identity_material={
                'contract':RESP_CONTRACT,
                'identity_protocol':IDENTITY_PROTOCOL,
                'source_row_ordinal':ordinal,
                'source_sha256':SOURCE_SHA,
            }
            rr=exact_ref('SCOPED_RESPONDENT','scoped-respondent',identity_material)
            binding={
                'source_row_ordinal':ordinal,
                'scoped_respondent_ref':rr,
                'source_scope':{'S025':s025,'B_COUNTR':country,'A_YEAR':year},
            }
            line_digest_update(global_h,binding)
            if cur is None or cur['key'] != key:
                if cur is not None: scopes.append(cur)
                cur={'key':key,'first':ordinal,'last':ordinal,'count':1,'h':hashlib.sha256()}
            else:
                cur['last']=ordinal; cur['count']+=1
            line_digest_update(cur['h'],binding)
            s=row['S007']; d=row['D_INTERV']
            if s in s007_seen: raise SystemExit(f'S007 duplicate unexpectedly encountered: {s}')
            s007_seen.add(s)
            if d in d_seen: d_dupes[d]=d_dupes.get(d,1)+1
            else: d_seen.add(d)
    if cur is not None: scopes.append(cur)
    if row_count != EXPECTED_ROWS: raise SystemExit(f'row_count {row_count}')
    if len(scopes) != EXPECTED_SCOPES: raise SystemExit(f'scope count {len(scopes)}')
    if len({x['key'] for x in scopes}) != EXPECTED_SCOPES: raise SystemExit('noncontiguous/repeated source scope')

    scope_rows=[]; scope_refs=[]
    for x in scopes:
        s025,country,year=x['key']
        ordered_digest=x['h'].hexdigest()
        material={
            'contract':SCOPE_CONTRACT,
            'identity_protocol':IDENTITY_PROTOCOL,
            'source_sha256':SOURCE_SHA,
            'source_scope':{'S025':s025,'B_COUNTR':country,'A_YEAR':year},
            'source_row_ordinal_first':x['first'],
            'source_row_ordinal_last':x['last'],
            'member_count':x['count'],
            'ordered_member_binding_digest':ordered_digest,
            'ordered_member_binding_digest_protocol':'SHA256_LENGTH_PREFIXED_CANONICAL_JSON_BINDINGS@1.0.0',
        }
        ref=exact_ref('SOURCE_SCOPE_MEMBER_SET','source-scope-member-set',material)
        scope_refs.append(ref)
        scope_rows.append({
            'S025':s025,'B_COUNTR':country,'A_YEAR':year,
            'source_row_ordinal_first':x['first'],'source_row_ordinal_last':x['last'],
            'member_count':x['count'],'ordered_member_binding_digest':ordered_digest,
            'source_scope_member_set_ref':ref['object_id'],'source_scope_member_set_hash':ref['content_hash']
        })

    duplicate_summary=sorted(((k,v) for k,v in d_dupes.items()), key=lambda kv:(-kv[1],kv[0]))
    replay_material={
        'contract':REPLAY_CONTRACT,
        'source_sha256':SOURCE_SHA,
        'source_rows':row_count,
        'source_scopes':len(scope_rows),
        'identity_protocol':IDENTITY_PROTOCOL,
        'scoped_respondent_ref_contract':RESP_CONTRACT,
        'ordered_row_binding_digest':global_h.hexdigest(),
        'ordered_row_binding_digest_protocol':'SHA256_LENGTH_PREFIXED_CANONICAL_JSON_BINDINGS@1.0.0',
        'source_scope_member_set_refs':sorted(scope_refs,key=lambda z:z['object_id']),
        'source_scope_partition':{
            'partition_field':'S025_PLUS_B_COUNTR_PLUS_A_YEAR',
            'contiguous_blocks':True,
            'coverage':'EXACTLY_ALL_SOURCE_ROWS_ONCE',
        },
        'source_native_identity_inputs':{
            'D_INTERVIEW':{'canonical_identity':False,'distinct_count':len(d_seen),'row_count':row_count},
            'S007':{'canonical_identity':False,'distinct_count':len(s007_seen),'row_count':row_count},
        },
        'anti_promotion_law':['D_INTERVIEW_NOT_CANONICAL','S007_NOT_CANONICAL'],
    }
    replay_ref=exact_ref('SCOPED_RESPONDENT_REPLAY','d12-scoped-respondent-replay',replay_material)
    manifest={
        'schema':'pre553-wvs7-d12-scoped-respondent-replay-manifest-v1',
        'source_sha256':SOURCE_SHA,
        'selected_raw_projection_sha256':selected_sha,
        'identity_protocol':IDENTITY_PROTOCOL,
        'row_count':row_count,
        'source_scope_count':len(scope_rows),
        'ordered_row_binding_digest':global_h.hexdigest(),
        'replay_material':replay_material,
        'replay_ref':replay_ref,
        'D_INTERVIEW':{
            'distinct_count':len(d_seen),
            'duplicate_row_excess':row_count-len(d_seen),
            'largest_duplicate_groups':[{'value':k,'count':v} for k,v in duplicate_summary[:10]],
            'canonical_identity':False,
        },
        'S007':{'distinct_count':len(s007_seen),'canonical_identity':False},
    }
    (out/'SCOPED_RESPONDENT_REPLAY_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    with (out/'COUNTRY_SOURCE_SCOPE_ROW_RANGES.csv').open('w',newline='') as f:
        field=list(scope_rows[0]); w=csv.DictWriter(f,fieldnames=field); w.writeheader(); w.writerows(scope_rows)
    receipt={
        'input_selected_projection_sha256':selected_sha,
        'source_sha256':SOURCE_SHA,
        'row_count':row_count,
        'scope_count':len(scope_rows),
        'ordered_row_binding_digest':global_h.hexdigest(),
        'replay_ref':replay_ref,
        'country_scope_ledger_sha256':hashlib.sha256((out/'COUNTRY_SOURCE_SCOPE_ROW_RANGES.csv').read_bytes()).hexdigest(),
    }
    (out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: build_d12_replay.py selected.csv outdir')
    main(sys.argv[1],sys.argv[2])
