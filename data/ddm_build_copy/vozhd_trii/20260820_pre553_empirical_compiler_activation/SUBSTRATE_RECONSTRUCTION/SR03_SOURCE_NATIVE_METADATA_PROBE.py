#!/usr/bin/env python3
"""Read-only physical metadata census for Rawlsing SAV/DTA source files.

No semantic normalization. No database writes. No C11 writes.
Requires pyreadstat + pandas. Uses user_missing=True deliberately.

Source-specific reader compatibility overrides are explicit, hash-bound by the
checked-in inventory, and emitted into each physical manifest. They are never
silent fallbacks and they do not establish authoritative source text encoding.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math
from collections import Counter
from pathlib import Path
from typing import Any
import pandas as pd
import pyreadstat

COMPAT_STATUS = "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY"

# Explicit reader-compatibility rulings. These do NOT alter source bytes and do
# not normalize values. They only control decoding for this physical census.
# The checked-in inventory independently binds every filename to an exact SHA.
SOURCE_READER_OVERRIDES = {
    "EVS 1999.sav": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Default pyreadstat metadata decoding fails with invalid byte sequence; "
            "the exact frozen EVS 1999 SAV reads successfully under Latin-1. "
            "Override is explicit and recorded for deterministic replay."
        ),
    },
    "EVS 2008.sav": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Default pyreadstat metadata decoding fails with invalid byte sequence; "
            "the exact frozen EVS 2008 SAV reads successfully under Latin-1. "
            "Override is explicit for this physical compatibility execution."
        ),
    },
    "LiTS_II.dta": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Default pyreadstat DTA decoding fails with invalid byte sequence; "
            "the exact frozen LiTS II DTA reads successfully under Latin-1. "
            "Override is explicit for this physical compatibility execution."
        ),
    },
    "LiTS_I.dta": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Frozen pyreadstat compatibility execution path for the exact LiTS I DTA. "
            "This is not a ruling that Latin-1 is the source's intended text encoding."
        ),
    },
    "LiTS_III.dta": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Default chunked pyreadstat execution fails; the exact frozen LiTS III DTA "
            "completes under the Latin-1 full-read compatibility path."
        ),
    },
    "LiTS_IV.dta": {
        "encoding": "latin1",
        "authority_status": COMPAT_STATUS,
        "reason": (
            "Frozen pyreadstat compatibility execution path for the exact LiTS IV DTA. "
            "This is not a ruling that Latin-1 is the source's intended text encoding."
        ),
    },
}


def h256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def j(v: Any):
    if isinstance(v, dict): return {str(k):j(x) for k,x in v.items()}
    if isinstance(v, (list,tuple,set)): return [j(x) for x in v]
    if isinstance(v, Path): return str(v)
    if isinstance(v, pd.Timestamp): return v.isoformat()
    if hasattr(v,'item'):
        try: return j(v.item())
        except Exception: pass
    if isinstance(v,float) and math.isnan(v): return None
    if isinstance(v,(str,int,float,bool)) or v is None: return v
    return str(v)

def find_exact(root: Path, name: str, expected_sha: str) -> Path:
    hits=[p for p in root.rglob(name) if p.is_file() and not p.name.startswith('._')]
    exact=[p for p in hits if h256(p)==expected_sha]
    if len(exact)!=1:
        raise RuntimeError(f'{name}: expected exactly one hash-matched file, got {len(exact)}; candidates={hits}')
    return exact[0]

def meta_dict(meta) -> dict[str,Any]:
    attrs=[
      'number_rows','number_columns','column_names','column_labels','column_names_to_labels',
      'file_encoding','file_label','table_name','notes','creation_time','modification_time',
      'original_variable_types','readstat_variable_types','variable_alignment','variable_storage_width',
      'variable_display_width','variable_measure','variable_value_labels','value_labels',
      'missing_ranges','missing_user_values','mr_sets'
    ]
    return {a:j(getattr(meta,a,None)) for a in attrs}

def in_spss_missing(value: Any, ranges: list[dict[str,Any]]) -> str|None:
    if value is None: return None
    for r in ranges or []:
        lo,hi=r.get('lo'),r.get('hi')
        try:
            if lo <= value <= hi: return json.dumps({'lo':j(lo),'hi':j(hi)},sort_keys=True)
        except TypeError:
            if value==lo==hi: return json.dumps({'lo':j(lo),'hi':j(hi)},sort_keys=True)
    return None

def scan(path: Path, fmt: str, chunksize: int, reader_override: dict[str,Any]|None = None) -> tuple[dict[str,Any],dict[str,dict[str,Any]]]:
    reader_fn=pyreadstat.read_sav if fmt=='sav' else pyreadstat.read_dta
    read_kwargs=dict(user_missing=True,apply_value_formats=False)
    if reader_override and reader_override.get('encoding'):
        read_kwargs['encoding']=reader_override['encoding']
    _, meta=reader_fn(str(path), metadataonly=True, **read_kwargs)
    md=meta_dict(meta)
    cols=list(getattr(meta,'column_names',[]) or [])
    stats={c:{'rows_seen':0,'system_missing_count':0,'user_missing_count':0,'user_missing_by_native_code':Counter()} for c in cols}
    if reader_override and reader_override.get('encoding'):
        # For frozen compatibility-override sources, use the same explicit
        # reader configuration for one full read. This avoids pyreadstat
        # chunk-reader decoding failures observed on legacy SAV/DTA inputs.
        frames=[reader_fn(str(path), **read_kwargs)]
    else:
        frames=pyreadstat.read_file_in_chunks(reader_fn,str(path),chunksize=chunksize,**read_kwargs)
    for df,_ in frames:
        for c in df.columns:
            s=df[c]
            st=stats[c]; st['rows_seen'] += len(s)
            na=s.isna(); st['system_missing_count'] += int(na.sum())
            if fmt=='sav':
                ranges=(getattr(meta,'missing_ranges',{}) or {}).get(c,[])
                if ranges:
                    vc=s[~na].value_counts(dropna=False)
                    for value,count in vc.items():
                        key=in_spss_missing(value,ranges)
                        if key is not None:
                            st['user_missing_count'] += int(count)
                            st['user_missing_by_native_code'][str(j(value))] += int(count)
            else:
                miss=(getattr(meta,'missing_user_values',{}) or {}).get(c,[])
                if miss:
                    vc=s[~na].value_counts(dropna=False)
                    miss_strings=set(map(str,miss))
                    for value,count in vc.items():
                        if str(value) in miss_strings:
                            st['user_missing_count'] += int(count)
                            st['user_missing_by_native_code'][str(value)] += int(count)
    for st in stats.values():
        st['ordinary_present_count']=st['rows_seen']-st['system_missing_count']-st['user_missing_count']
        st['user_missing_by_native_code']=dict(sorted(st['user_missing_by_native_code'].items()))
    return md,stats

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inventory',required=True)
    ap.add_argument('--source-root',required=True)
    ap.add_argument('--output-dir',required=True)
    ap.add_argument('--chunksize',type=int,default=10000)
    args=ap.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    inv=list(csv.DictReader(open(args.inventory,encoding='utf-8')))
    summary=[]
    for i,row in enumerate(inv,1):
        name,fmt,expected=row['source_file'],row['format'].lower(),row['sha256']
        p=find_exact(Path(args.source_root),name,expected)
        override=SOURCE_READER_OVERRIDES.get(name)
        enc=(override or {}).get('encoding')
        print(f'[{i}/{len(inv)}] {name}' + (f' [encoding={enc}]' if enc else ''),flush=True)
        md,stats=scan(p,fmt,args.chunksize,override)
        payload={
          'source_file':name,'format':fmt,'path':str(p),'size_bytes':p.stat().st_size,
          'sha256':expected,
          'reader_compatibility_override':j(override),
          'metadata':md,'variable_physical_counts':stats
        }
        op=out/(name.replace('/','_')+'.physical_manifest.json')
        op.write_text(json.dumps(j(payload),indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
        summary.append({
          'source_file':name,'format':fmt,'sha256':expected,'size_bytes':p.stat().st_size,
          'reader_encoding_override':enc or '',
          'reader_override_authority_status':(override or {}).get('authority_status',''),
          'number_rows':md.get('number_rows'),'number_columns':md.get('number_columns'),
          'variables_with_spss_missing_ranges':len((md.get('missing_ranges') or {})),
          'variables_with_stata_extended_missing':len((md.get('missing_user_values') or {})),
          'multiple_response_sets':len((md.get('mr_sets') or {})),
          'manifest':op.name
        })
    with (out/'SOURCE_PHYSICAL_MANIFEST_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=summary[0].keys());w.writeheader();w.writerows(summary)
    receipt={
      'status':'COMPLETE','source_count':len(summary),'inventory_sha256':h256(Path(args.inventory)),
      'reader_overrides':SOURCE_READER_OVERRIDES,
      'reader_override_authority_status':COMPAT_STATUS,
      'completion_token':'PRE553_SR03_35_SOURCE_NATIVE_METADATA_RECEIPT_COMPLETE'
    }
    (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(receipt['completion_token'])

if __name__=='__main__': main()
