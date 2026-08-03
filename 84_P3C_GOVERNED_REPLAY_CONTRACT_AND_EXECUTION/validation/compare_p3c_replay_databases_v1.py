#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,datetime,decimal,hashlib,json,uuid
from pathlib import Path
from typing import Any
import psycopg


def norm(v:Any)->Any:
    if v is None or isinstance(v,(str,int,bool)): return v
    if isinstance(v,float): return format(v,'.17g')
    if isinstance(v,decimal.Decimal): return str(v)
    if isinstance(v,(datetime.datetime,datetime.date,datetime.time)): return v.isoformat()
    if isinstance(v,(bytes,bytearray,memoryview)): return bytes(v).hex()
    if isinstance(v,uuid.UUID): return str(v)
    if isinstance(v,dict): return {str(k):norm(x) for k,x in sorted(v.items(),key=lambda z:str(z[0]))}
    if isinstance(v,(list,tuple)): return [norm(x) for x in v]
    return str(v)

def cjson(v:Any)->str:return json.dumps(norm(v),sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha_lines(lines:list[str])->str:
    h=hashlib.sha256()
    for line in sorted(lines): h.update(line.encode());h.update(b'\n')
    return h.hexdigest()

def snapshot(dsn:str)->dict[str,dict[str,Any]]:
    out={}
    with psycopg.connect(dsn) as conn:
        tables=[r[0] for r in conn.execute("""select table_name from information_schema.tables where table_schema='public' and table_type='BASE TABLE' order by table_name""")]
        for table in tables:
            cols=[r[0] for r in conn.execute("""select column_name from information_schema.columns where table_schema='public' and table_name=%s order by ordinal_position""",(table,))]
            q='select '+','.join('"'+c.replace('"','""')+'"' for c in cols)+' from "'+table.replace('"','""')+'"'
            lines=[cjson(dict(zip(cols,row))) for row in conn.execute(q)]
            out[table]={'columns':cols,'row_count':len(lines),'row_set_hash':sha_lines(lines)}
        seq=[]
        for row in conn.execute("select schemaname,sequencename,start_value,min_value,max_value,increment_by,cycle,cache_size,last_value from pg_sequences where schemaname='public' order by sequencename"):
            seq.append(cjson(row))
        out['__SEQUENCES__']={'columns':['pg_sequences'],'row_count':len(seq),'row_set_hash':sha_lines(seq)}
    return out

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--left-dsn',required=True);ap.add_argument('--right-dsn',required=True);ap.add_argument('--section',type=Path,required=True);args=ap.parse_args()
    left=snapshot(args.left_dsn);right=snapshot(args.right_dsn)
    names=sorted(set(left)|set(right));rows=[]
    for n in names:
        l=left.get(n);r=right.get(n);ok=l==r
        rows.append({'table':n,'status':'PASS' if ok else 'FAIL','left_count':None if l is None else l['row_count'],'right_count':None if r is None else r['row_count'],'left_hash':None if l is None else l['row_set_hash'],'right_hash':None if r is None else r['row_set_hash']})
    out={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','table_count':len(rows),'matched_tables':sum(r['status']=='PASS' for r in rows),'mismatched_tables':sum(r['status']=='FAIL' for r in rows),'tables':rows}
    v=args.section/'validation';v.mkdir(parents=True,exist_ok=True)
    (v/'P3C_INDEPENDENT_DATABASE_COMPARISON_RETURN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    with (v/'P3C_INDEPENDENT_DATABASE_COMPARISON_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({k:v for k,v in out.items() if k!='tables'},indent=2,sort_keys=True))
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
