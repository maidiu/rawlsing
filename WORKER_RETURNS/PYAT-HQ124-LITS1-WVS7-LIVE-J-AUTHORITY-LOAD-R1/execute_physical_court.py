"""One full decode per frozen source; retain selected physical incidence only.

This court does not interpret numeric missingness as applicability, extend
selected-B authority, or execute empirical queries without L1-L4 permission.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import json,hashlib,datetime,gzip,importlib.util,subprocess
from dataclasses import replace
from collections import Counter
import pyreadstat
from rawlsing_next.pre553_physical_decoder import decode_dta,decode_sav,classify_physical_value,build_physical_metadata_payload
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.fiabc_lits_i_d03_risk_set_authority import decode_membership_payload,ROOTS,RESPONDENT_KEY_PREFIX,UNIVERSE_REF,RISK_SET_REF
OUT=Path(__file__).resolve().parent; E=OUT/'evidence'; LOCAL=OUT/'local_intermediates'; LOCAL.mkdir(exist_ok=True)
F=E/'FROZEN_PREVALUE_SELECTION.json'; FREEZE_SHA='508838fc85e84d82b5a5a5f5f4799c214dee277fe69605bec79de13bc2437814'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,d):p.write_text(json.dumps(canonicalize(d),sort_keys=True,indent=2)+'\n')
def physical_metadata_pack(v):
 if isinstance(v,float):return {'physical_float64_hex':v.hex()}
 if isinstance(v,dict):return {k:physical_metadata_pack(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [physical_metadata_pack(x) for x in v]
 return v
def pack(v):
 if v is None:return {'kind':'none'}
 if isinstance(v,str):return {'kind':'str','value':v}
 if isinstance(v,bool):return {'kind':'bool','value':v}
 if isinstance(v,int):return {'kind':'int','value':v}
 if isinstance(v,float):return {'kind':'float64_hex','value':v.hex()}
 raise TypeError(type(v).__name__)
assert sha(F)==FREEZE_SHA
frozen=json.loads(F.read_text());assert not frozen['respondent_outcome_values_accessed_before_freeze']
for spec in frozen['specimens']:
 source=spec['source']; receipt_path=E/(source+'_PHYSICAL_EXECUTION.json'); marker=LOCAL/(source+'_VALUE_ACCESS_STARTED.json')
 if receipt_path.exists():
  receipt=json.loads(receipt_path.read_text());assert sha(OUT/receipt['retained_raw_intermediate']['path'])==receipt['retained_raw_intermediate']['sha256'];print(source,'retained execution verified; no source reread');continue
 if marker.exists():raise SystemExit('Interrupted decode requires an exact documented retry; refusing automatic reread: '+source)
 path=Path('/Users/matthewsmith/Desktop/Rawlsing')/('LiTS_I.dta' if source=='LiTS_I' else 'WVS Wave 7.sav')
 expected='7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09' if source=='LiTS_I' else '2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d'
 assert sha(path)==expected
 dump(marker,{'source':source,'freeze_sha256':FREEZE_SHA,'started_at_utc':now(),'full_decode_attempt':1,'source_sha256':expected})
 print(source,'decoding exact source once after committed specimen freeze',flush=True)
 if source=='LiTS_I': incidence=decode_dta(path,encoding='latin1',expected_source_sha256=expected); frame=incidence._frame
 else:
  incidence=decode_sav(path,expected_source_sha256=expected)
  frame,meta=pyreadstat.read_sav(str(path),apply_value_formats=False,user_missing=True)
  assert len(frame)==incidence.row_count and tuple(frame.columns)==tuple(v.name for v in incidence.variables)
  incidence=replace(incidence,_frame=frame)
 assert frame is not None
 assert (len(frame),len(frame.columns))==((29002,1198) if source=='LiTS_I' else (97220,613))
 names=spec['governed_native_component_order'];extras=[] if source=='LiTS_I' else ['B_COUNTRY'];cols=names+extras
 variables={v.name:v for v in incidence.variables};assert all(n in variables for n in cols)
 counters={n:Counter() for n in names};same_row_non_system=0;retained=[]
 for row_ordinal,row in enumerate(frame[cols].itertuples(index=False,name=None),1):
  states=[]
  for n,v in zip(names,row):
   st,_=classify_physical_value(v,variables[n].missing_declarations);counters[n][st.value]+=1;states.append(st.value)
  if all(s!='SYSTEM_MISSING' for s in states):same_row_non_system+=1
  retained.append({'source_row_ordinal':row_ordinal,'physical_values':[pack(v) for v in row]})
 payload={'schema':'HQ124_RETAINED_SELECTED_PHYSICAL_INCIDENCE@1','source_sha256':expected,'freeze_sha256':FREEZE_SHA,'columns':cols,'row_count':len(frame),'rows':retained}
 payload_bytes=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
 local=LOCAL/(source+'_selected_physical_incidence.json.gz');local.write_bytes(gzip.compress(payload_bytes,mtime=0))
 metadata=build_physical_metadata_payload(source_sha256=incidence.source_sha256,source_format=incidence.source_format,reader_configuration=incidence.reader_configuration,file_metadata=incidence.file_metadata,variables=incidence.variables)
 # Physical missing-range floats are not semantic identity values. Preserve
 # them explicitly instead of applying the semantic canonicalizer to metadata.
 dump(E/(source+'_CURRENT_DECODER_METADATA.json'),physical_metadata_pack(metadata))
 basis={'contract':'source SHA256 + source-local 1-based row ordinal, no cross-source linkage','source_row_count':len(frame),'all_required_slots_exact_unique':True,'native_component_order':names,'raw_physical_non_system_same_row_count':same_row_non_system,'semantic_risk_set_membership':'UNRESOLVED_FOR_FULL_CURRENT_J_CANDIDATE','physical_nonmissing_is_not_applicability':True,'current_j_coadministration_semantics':'SOURCE_NATIVE_GROUPING_BOUND_BY_CURRENT_J01A__FULL_EXECUTION_APPLICABILITY_NOT_AUTHORIZED'}
 if source=='LiTS_I':
  roots=decode_membership_payload();assert all(len(roots[k])==ROOTS[k]['member_count'] for k in roots)
  rootdoc={'source_sha256':expected,'respondent_key_prefix':RESPONDENT_KEY_PREFIX,'source_universe_ref':UNIVERSE_REF.as_dict(),'risk_set_ref':RISK_SET_REF.as_dict(),'roots':{k:sorted(v) for k,v in roots.items()},'authority_scope':'q301_2/q301_7 only; no other target or generic missingness extension'}
  dump(E/'LiTS_I_QUALIFIED_D03_ROOTS.json',rootdoc)
  basis['qualified_subscope_risk_sets']={k:len(v) for k,v in roots.items()};basis['full_grid_risk_set_extension']='NOT_AUTHORIZED'
 else:
  p=ROOT/'rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py';loader=importlib.util.spec_from_file_location('hq124_wvs_projection',p);module=importlib.util.module_from_spec(loader);sys.modules[loader.name]=module;loader.loader.exec_module(module)
  country=tuple(frame['B_COUNTRY'].tolist())
  structural=module.projection_structural_input(incidence.variables,country)
  dump(E/'WVS7_CURRENT_STRUCTURAL_INPUT.json',structural)
  fields=module.build_projection_fields(physical_variables=incidence.variables,row_country_values=country,enforce_frozen_dimensions=True)
  qualified=module.bind_exact_projection_fields(fields)
  from rawlsing_next.pre553_carrier_execution import governed_projection_binding_receipt
  dump(E/'WVS7_CURRENT_PROJECTION_BINDING.json',governed_projection_binding_receipt(qualified))
  assert tuple(s.slot.name for s in qualified.response_slots)==('Q291G5','Q291P5')
  basis['qualified_projection_identity_ref']=qualified.projection_identity_ref.as_dict()
  basis['qualified_same_row_respondent_bindings']=len(qualified.row_bindings)
  basis['qualified_routing_fact_count']=len(qualified.routing)
  basis['qualified_whole_grid_coverage']=False
  del fields,qualified,country,structural
 receipt={'schema':'HQ124_SELECTED_PHYSICAL_EXECUTION@1','source':source,'source_path':str(path),'source_sha256':expected,'specimen_id':spec['candidate_row']['current_source_structure_id'],'freeze_sha256':FREEZE_SHA,'freeze_commit':'6744e3e0','value_access_started_at_utc':json.loads(marker.read_text())['started_at_utc'],'completed_at_utc':now(),'full_decodes':1,'additional_metadata_only_inspections':1,'decoder_configuration':incidence.reader_configuration,'physical_shape':[len(frame),len(frame.columns)],'decoder_columns_read':list(frame.columns),'specimen_columns_consumed':cols,'physical_missing_state_counts':{n:dict(c) for n,c in counters.items()},'row_basis':basis,'retained_raw_intermediate':{'path':str(local.relative_to(OUT)),'bytes':local.stat().st_size,'sha256':sha(local),'uncompressed_payload_sha256':hashlib.sha256(payload_bytes).hexdigest(),'storage':'LOCAL_ONLY__NO_RESPONDENT_VALUE_UPLOAD'},'retry':'NONE','semantic_empirical_fact_or_discovery_claim':'NONE__L1_L4_POSITIVE_PERMISSION_ABSENT'}
 dump(receipt_path,receipt);print(source,'physical source execution retained; full-grid denominator remains typed unresolved',flush=True)
 del frame,incidence,retained,payload,payload_bytes
