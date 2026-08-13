#!/usr/bin/env python3
"""Deterministic preflight for the three M6 Track-B response-map scopes."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import pandas as pd
from data.ddm_build_copy.build_determinicity_wave_shard_v550 import _filter_response_map_for_wave

SCOPES=(
    ("EVS","1981","BE","evs_1981.json"),
    ("South Asia","W1","IN","southasia_w1.json"),
    ("WVS","W1","SE","wvs_w1.json"),
)
def sha(p):
    h=hashlib.sha256();
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--map',required=True); ap.add_argument('--input-dir',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    mp=Path(a.map); frame=pd.read_csv(mp,low_memory=False,dtype=object).fillna(''); rows=[]
    for source,wave,country,fn in SCOPES:
        payload=json.loads((Path(a.input_dir)/fn).read_text())
        selected={str(x).strip().lower() for x in payload.get('var_codes',[])}
        src=frame[frame.source_family.astype(str).map(str.lower).eq(source.lower()) | frame.source.astype(str).map(str.lower).eq(source.lower())]
        scoped=_filter_response_map_for_wave(frame,pd.DataFrame({'var_code':payload.get('var_codes',[]),'question_id':payload.get('question_ids',[])}),source=source,wave=wave,canonical_wave=wave)
        matched={str(x).strip().lower() for x in scoped.get('var_code',pd.Series(dtype=str)).tolist() if str(x).strip()}
        rows.append({'source_family':source,'incoming_wave':wave,'country_code':country,'canonical_source':source,'canonical_wave':wave,'selected_variable_count':len(selected),'selected_variables_json':json.dumps(sorted(selected)),'response_map_parent_path':str(mp),'response_map_parent_sha256':sha(mp),'response_map_rows_source_family':len(src),'response_map_rows_source_wave_before_variable_filter':len(scoped),'response_map_rows_after_exact_selected_variable_filter':len(scoped),'exact_matched_variable_codes_json':json.dumps(sorted(matched)),'exact_unmatched_variable_codes_json':json.dumps(sorted(selected-matched)),'aliases_or_canonicalization_applied':'source-family canonicalization; exact wave canonicalization; source-file-derived wave only where map metadata is blank','map_key_columns_used':'source_family/source; canonical_wave/wave/wave_id; question_id/item_id/var_code/var_name/variable_id/canonical_var_code','failure_stage':'after authority loading' if len(scoped) else 'during map filtering','family_only_fallback_used':False,'parent_sha_pinned':sha(mp)})
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame(rows).to_csv(out,index=False)
if __name__=='__main__': main()
