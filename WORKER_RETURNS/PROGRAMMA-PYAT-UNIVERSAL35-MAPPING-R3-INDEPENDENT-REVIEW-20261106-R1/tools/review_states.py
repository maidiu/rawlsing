"""Independent source-metadata and projection-state review for A R2."""
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, classify_physical_value, decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
from rawlsing_next.source_configuration.factory import build_governed_c11_projection
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import reader_configuration_from_config

SOURCES=('SRC31','SRC32','SRC04','SRC16','SRC24','SRC25','SRC33','SRC26')

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("--projection-sources",default=""); args=ap.parse_args(); projection_sources=set(filter(None,args.projection_sources.split(",")))
    binding=json.loads((ROOT/'.local-logs/pyat-universal35/source-runtime-binding.local.json').read_text())
    root=binding['USER_ORIGINAL35_DATA_ROOT']
    lib=SourceConfigLibrary(source_root=root)
    registry=json.loads((ROOT/'rawlsing_next/source_configuration/corrections/SOURCE_CONFIGURATION_CORRECTIONS.json').read_text())
    entries={e['source_id']:e for e in registry['entries']}
    rows=[]
    for sid in SOURCES:
        cfg=lib.load_original(sid); doc=cfg.document; rc=reader_configuration_from_config(cfg); res=lib.resolve_source_path(sid)
        inc=decode_sav(res['resolved_source_path'],encoding=rc.encoding,expected_source_sha256=cfg.original_source_sha256)
        variables={v.name:v for v in inc.variables}
        checks=Counter(); state_counts=Counter(); mismatches=[]
        for ch in entries[sid]['response_value_changes']:
            name=ch['slot']['name']; var=variables.get(name)
            if var is None:
                mismatches.append({'slot':name,'kind':'SLOT_ABSENT'}); continue
            checks['changes']+=1
            state=classify_physical_value(ch['raw_value'],var.missing_declarations)[0]
            expected=ch.get('missing_state')
            if state.value!=expected:
                mismatches.append({'slot':name,'kind':'MISSING_STATE_MISMATCH','expected':expected,'actual':state.value}); continue
            declaration=classify_physical_value(ch['raw_value'],var.missing_declarations)[1]
            if declaration!=ch.get('source_missing_declaration'):
                mismatches.append({'slot':name,'kind':'MISSING_DECLARATION_MISMATCH'}); continue
            label=ch.get('source_label')
            if label is not None and var.value_labels.get(str(ch['raw_value']))!=label:
                mismatches.append({'slot':name,'kind':'LABEL_MISMATCH'}); continue
            if ch.get('response_state')=='SUBSTANTIVE_RESPONSE':
                checks['substantive_added']+=1
            elif ch.get('canonical_value') is not None:
                mismatches.append({'slot':name,'kind':'NONSUBSTANTIVE_CANONICAL_VALUE'}); continue
            state_counts[ch.get('response_state')]+=1
        projection_checked=projection_missing=0; projection_skipped=True
        if sid in projection_sources:
            projection_skipped=False
            if (doc.get('respondents') or {}).get('source_native_key_slot') is None:
                proj=build_governed_c11_projection(cfg,source_sha256=inc.source_sha256,row_count=inc.row_count)
            else:
                from rawlsing_next.source_configuration.factory import row_native_keys_from_transport
                keys=row_native_keys_from_transport(cfg,incidence=inc)
                proj=build_governed_c11_projection(cfg,source_sha256=inc.source_sha256,row_count=inc.row_count,row_native_keys=keys)
            rules={}
            for slot in proj.response_slots:
                rules[(slot.slot.ordinal,slot.slot.name)]={v.physical_key:v for v in slot.values}
            for ch in entries[sid]['response_value_changes']:
                key=(ch['slot']['ordinal'],ch['slot']['name']); table=rules.get(key,{})
                pk=physical_value_binding_key(ch['raw_value'],ch['missing_state'],ch.get('source_missing_declaration'))
                rule=table.get(pk)
                if rule is None:
                    projection_missing+=1; continue
                projection_checked+=1
                if rule.response_state!=ch.get('response_state'):
                    mismatches.append({'slot':ch['slot']['name'],'kind':'PROJECTION_STATE_MISMATCH','expected':ch.get('response_state'),'actual':rule.response_state})
        inc.close()
        rows.append({'source_id':sid,'source_sha256':cfg.original_source_sha256,'corrections':len(entries[sid]['response_value_changes']),'checks':dict(checks),'state_counts':dict(state_counts),'projection_checked':projection_checked,'projection_missing':projection_missing,'projection_skipped':projection_skipped,'mismatches':mismatches})
    payload={'schema':'PYAT_UNIVERSAL35_MAPPING_R2_STATE_REVIEW@1','rows':rows,'all_mismatch_free':all(not r['mismatches'] for r in rows),'no_substantive_added':all(r['checks'].get('substantive_added',0)==0 for r in rows)}
    out=ROOT/'WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-MAPPING-R3-INDEPENDENT-REVIEW-20261106-R1/results/state_probe.json'
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:payload[k] for k in ('all_mismatch_free','no_substantive_added')},sort_keys=True))
    for r in rows: print(r['source_id'],r['corrections'],r['checks'],r['state_counts'],'proj',r['projection_checked'],r['projection_missing'],'skip',r['projection_skipped'],'mism',len(r['mismatches']))

if __name__=='__main__': main()
