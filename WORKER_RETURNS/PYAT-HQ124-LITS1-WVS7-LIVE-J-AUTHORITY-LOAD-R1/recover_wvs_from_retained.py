"""Recover post-decode receipt serialization; never opens the respondent source."""
from pathlib import Path
import sys,json,gzip,hashlib,datetime,importlib.util
from collections import Counter
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_physical_decoder import PhysicalVariable,classify_physical_value
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.pre553_carrier_execution import governed_projection_binding_receipt
OUT=Path(__file__).resolve().parent;E=OUT/'evidence';L=OUT/'local_intermediates'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(canonicalize(d),sort_keys=True,indent=2)+'\n')
f=E/'FROZEN_PREVALUE_SELECTION.json';assert sha(f)=='508838fc85e84d82b5a5a5f5f4799c214dee277fe69605bec79de13bc2437814'
spec=json.loads(f.read_text())['specimens'][1]
local=L/'WVS7_selected_physical_incidence.json.gz';raw=gzip.decompress(local.read_bytes());doc=json.loads(raw)
assert doc['source_sha256']=='2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d'
assert doc['columns']==spec['governed_native_component_order']+['B_COUNTRY'] and doc['row_count']==97220
assert [r['source_row_ordinal'] for r in doc['rows']]==list(range(1,97221))
metadata_path=E/'WVS7_METADATA.json';metadata=json.loads(metadata_path.read_text())
assert metadata['source_sha256']==doc['source_sha256'] and metadata['full_decodes']==0
p=ROOT/'rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py'
loader=importlib.util.spec_from_file_location('hq124_wvs_recovered',p);m=importlib.util.module_from_spec(loader);sys.modules[loader.name]=m;loader.loader.exec_module(m)
meta=SimpleNamespace(missing_ranges=metadata['missing_ranges'],missing_user_values=metadata['missing_user_values'])
variables=tuple(PhysicalVariable(i,n,None,metadata['column_names_to_labels'].get(n),{},m._sav_missing_declarations(meta,n),{},{}) for i,n in enumerate(metadata['column_names'],1))
by={v.name:v for v in variables}
def unpack(v):
 if v['kind']=='float64_hex':return float.fromhex(v['value'])
 if v['kind']=='none':return None
 return v['value']
rows=[tuple(unpack(v) for v in r['physical_values']) for r in doc['rows']]
counters={n:Counter() for n in spec['governed_native_component_order']};nonmissing=0
for row in rows:
 states=[]
 for n,v in zip(counters,row):
  state,_=classify_physical_value(v,by[n].missing_declarations);counters[n][state.value]+=1;states.append(state.value)
 nonmissing+=all(s!='SYSTEM_MISSING' for s in states)
country=tuple(row[-1] for row in rows)
structural=m.projection_structural_input(variables,country);dump(E/'WVS7_CURRENT_STRUCTURAL_INPUT.json',structural)
qualified=m.materialize_from_structural_input(structural)
assert tuple(s.slot.name for s in qualified.response_slots)==('Q291G5','Q291P5')
binding=governed_projection_binding_receipt(qualified);dump(E/'WVS7_CURRENT_PROJECTION_BINDING.json',binding)
recovery={'schema':'HQ124_POST_DECODE_SERIALIZATION_RECOVERY@1','failure':'canonicalize rejected float-valued physical missing-range declarations in metadata; full source read and exact selected incidence retention had already succeeded','source_full_decode_retries':0,'respondent_source_reopened':False,'retained_incidence_sha256':sha(local),'metadata_sha256':sha(metadata_path),'metadata_reconstruction_scope':'exact variable ordinal/name/missing declarations from retained metadata-only receipt; no claim of a complete current-decoder physical-metadata digest','recovery_method':'current materializer projection_structural_input + materialize_from_structural_input on retained country values and metadata','retained_incidence_used_without_changes':True}
dump(E/'WVS7_POST_DECODE_RECOVERY.json',recovery)
basis={'contract':'source SHA256 + source-local 1-based row ordinal, no cross-source linkage','source_row_count':97220,'all_required_slots_exact_unique':True,'native_component_order':spec['governed_native_component_order'],'raw_physical_non_system_same_row_count':nonmissing,'physical_nonmissing_is_not_applicability':True,'semantic_risk_set_membership':'UNRESOLVED_FOR_FULL_CURRENT_J_CANDIDATE','current_j_coadministration_semantics':'SOURCE_NATIVE_GROUPING_BOUND_BY_CURRENT_J01A__FULL_EXECUTION_APPLICABILITY_NOT_AUTHORIZED','qualified_projection_identity_ref':qualified.projection_identity_ref.as_dict(),'qualified_same_row_respondent_bindings':len(qualified.row_bindings),'qualified_routing_fact_count':len(qualified.routing),'qualified_routing_states':dict(Counter(r.routing_state for r in qualified.routing)),'qualified_whole_grid_coverage':False}
receipt={'schema':'HQ124_SELECTED_PHYSICAL_EXECUTION@1','source':'WVS7','source_path':metadata['source_path'],'source_sha256':doc['source_sha256'],'specimen_id':spec['candidate_row']['current_source_structure_id'],'freeze_sha256':sha(f),'freeze_commit':'6744e3e0','value_access_started_at_utc':json.loads((L/'WVS7_VALUE_ACCESS_STARTED.json').read_text())['started_at_utc'],'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'full_decodes':1,'additional_metadata_only_inspections':1,'decoder_configuration':{'reader':'pyreadstat','reader_version':'1.3.6','user_missing':True,'apply_value_formats':False,'encoding':None},'physical_shape':[97220,613],'decoder_columns_read':metadata['column_names'],'specimen_columns_consumed':doc['columns'],'physical_missing_state_counts':{n:dict(c) for n,c in counters.items()},'row_basis':basis,'retained_raw_intermediate':{'path':str(local.relative_to(OUT)),'bytes':local.stat().st_size,'sha256':sha(local),'uncompressed_payload_sha256':hashlib.sha256(raw).hexdigest(),'storage':'LOCAL_ONLY__NO_RESPONDENT_VALUE_UPLOAD'},'retry':'POST_DECODE_SERIALIZATION_RECOVERY_FROM_RETAINED_BYTES__ZERO_SOURCE_REREADS','semantic_empirical_fact_or_discovery_claim':'NONE__L1_L4_POSITIVE_PERMISSION_ABSENT'}
dump(E/'WVS7_PHYSICAL_EXECUTION.json',receipt)
print('WVS7 recovered from retained bytes; full decodes=1, source rereads=0; qualified routing:',basis['qualified_routing_states'])
