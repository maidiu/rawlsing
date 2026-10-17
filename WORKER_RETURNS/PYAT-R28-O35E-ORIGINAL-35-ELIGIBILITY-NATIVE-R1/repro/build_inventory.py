"""Metadata-only census through actual pinned V550 authority resolver.

Executed with the established pandas runtime. Never opens the raw locators.
"""
from pathlib import Path
from collections import Counter
import csv,hashlib,io,json,os,re,subprocess,sys
HERE=Path(__file__).resolve().parents[1]
REPO=HERE.parents[1]
PINNED=HERE/'runtime/pinned'
PIN='eede2b8bdb9fcdcc1d4187912f8e00773869c22c'
QRA='data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'
sys.path.insert(0,str(PINNED/'data/ddm_build_copy'))
os.environ['RAWLSING_QUESTION_RELATION_AUTHORITY_PATH']=str(PINNED/QRA)
import ddm_v550_question_relation_authority as native
import pandas

def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def sha(b):return hashlib.sha256(b).hexdigest()
def safe_ref(v):
 if not v:return None
 # Retain repository-relative authority pointers, never historical user roots.
 for token in ('data/','PYAT_CONTROL_ROOM/','WORKER_RETURNS/'):
  if token in v:return v[v.index(token):]
 return v if not v.startswith('/') else 'HISTORICAL_ABSOLUTE_LOCATOR_REDACTED'

def main():
 sourcepin=json.loads((HERE/'SOURCE_INPUTS.json').read_text())
 for p in (QRA,'data/ddm_build_copy/ddm_v550_question_relation_authority.py','data/ddm_build_copy/manifests/source_dataset_manifest.csv'):
  assert sha((PINNED/p).read_bytes())==sourcepin['files'][p]['sha256']
 closed=native.active_closed_35_waves()
 raw=list(csv.DictReader((PINNED/QRA).open()))
 atlaspath='PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/SOURCES.md'
 atlas=git('show',f'{PIN}:{atlaspath}')
 source_rows=re.findall(r'\| \[(SRC\d+)\][^|]*\| ([^|]+?) \| ([BP]) \| ([^|]+?) \|',atlas.decode())
 assert len(source_rows)==35
 manifests=list(csv.DictReader((PINNED/'data/ddm_build_copy/manifests/source_dataset_manifest.csv').open()))
 structurepath='data/ddm_build_copy/manifests/source_structure_validation_manifest.csv'
 structurebytes=git('show',f'{PIN}:{structurepath}')
 structures=list(csv.DictReader(io.StringIO(structurebytes.decode())))
 tree=set(git('ls-tree','-r','--name-only',PIN).decode().splitlines())
 rawgroup={}
 for i,r in enumerate(raw,2):
  if r['authority_status']=='EXCLUDED_INACTIVE_WAVE':continue
  pair=(native.canonical_source_family(r['canonical_source']),native.canonical_wave(r['canonical_source'],r['canonical_wave']))
  rawgroup.setdefault(pair,[]).append((i,r))
 families={x[0] for x in closed}
 operations={
  'I03_RAW_MARGINAL':'Source-grounded target/response/risk/denominator and scientific operation authority required.',
  'I03_GOVERNED_WEIGHTED':'Also explicit weight/design/estimand; not default weight=1.',
  'I03_DIRECTED_CONDITIONAL':'Also eligible condition role, directed predicate, shared subject carrier and risk-set binding.',
  'I05_EXACT_BOUNDED_DISCOVERY':'Also prospective finite grammar/frontier, support/validation and coverage authority.',
  'I04_STRUCTURAL_ADMISSION':'Relation-specific semantic authority and exact ingress required; empirical facts remain distinct.',
  'BATCH_EXPECTED_WORK':'Source issuer E_pre expected root independent of emitted manifest, exact result custody.',
  'OC01_SOURCE_LOCAL_CONSUMER':'Exact measured fact and current bounded evidence; no population or actor promotion.'}
 waves=[]
 for sid,label,census,residual in source_rows:
  family=next(f for f in sorted(families,key=len,reverse=True) if label.startswith(f))
  wave=native.canonical_wave(family,label[len(family):].strip())
  pair=(family,wave);assert pair in rawgroup,(sid,label,pair)
  group=rawgroup[pair]
  matches=[m for m in manifests if native.canonical_source_family(m['source_family'])==family and native.canonical_wave(family,m['wave'])==wave]
  assert len(matches)==1,(sid,matches)
  m=matches[0]
  structure=next(s for s in structures if s['dataset_id']==m['dataset_id'])
  items=[]
  for line,r in group:
   items.append({'csv_line':line,'legacy_source':r['source'],'legacy_wave':r['wave'],
    'question_id':r['question_id'],'var_code':r['var_code'],'country_code_scope_as_preserved':r['country_code_scope'],
    'qra_authority_status':r['authority_status'],'relation_use_status':r['relation_use_status_final'],
    'governed_row_payload_hash':r['governed_row_payload_hash'],'qsmv2_final_payload_hash':r['qsmv2_final_payload_hash'] or None,
    'topology_metadata':{'manual_response_topology':r['manual_response_topology'] or None,
      'p2_response_topology':r['p2_response_topology'] or None,'p2_response_binding_status':r['p2_response_binding_status'] or None},
    'preserved_authority_pointers':{k:safe_ref(r[k]) for k in ('manual_source_authority','manual_row_authority_path','p2_source_authority','p2_question_authority_artifact') if r[k]},
    'p2_exact_identity_sha256':r['p2_exact_identity_sha256'] or None,
    'original_administered_occurrence':'PARTIALLY_MAPPED_NOT_VERIFIED_EXHAUSTIVE',
    'original_item_operation_eligibility':'HOLD_SOURCE_SCIENTIFIC_E_PRE_UNISSUED',
    'operation_statuses_inherit':'original_operation_status_default'})
  waves.append({'atlas_id':sid,'atlas_label':label,'canonical_source_family':family,'canonical_wave':wave,
   'historical_representation':{'P_or_B':census,'residual':residual,'grade':'representation only'},
   'dataset_manifest_identity':{'dataset_id':m['dataset_id'],'legacy_wave':m['wave'],
     'recorded_basename':Path(m['relative_path']).name,'format':m['format'],'recorded_size_bytes':int(m['size_bytes']),
     'recorded_source_sha256':m['sha256'] or None,'classification_confidence':m['classification_confidence'],
     'physical_presence_or_bytes_checked':False,'actual_source_edition_hash':'UNBOUND'},
   'qra_row_count':len(items),'qra_status_counts':dict(Counter(r['authority_status'] for _,r in group)),
   'historical_header_and_instrument_audit':{
    'grade':'PRESERVED_HISTORICAL_METADATA_NOT_FRESH_SOURCE_READ',
    'recorded_rows':int(structure['raw_row_count']),'recorded_columns':int(structure['raw_column_count']),
    'header_minus_qra_row_count':int(structure['raw_column_count'])-len(items),
    'recorded_audit_status':structure['audit_status'],
    'recorded_raw_exists':structure['raw_exists'],'recorded_codebook_exists':structure['codebook_exists'],
    'source_structure_disagrees_count':structure['source_structure_disagrees_count'],
    'codebook_stale_count':structure['codebook_stale_count'],
    'kind_counts':json.loads(structure['kind_counts']),
    'problem_fields':structure['problem_fields'].split('|') if structure['problem_fields'] else [],
    'audit_preimages_tracked_at_pin':False,
    'interpretation':'Column-count mismatch is an unresolved inventory reconciliation, not eligible-item omission proof. Equality is not source-original completeness.'},
   'qra_distinct_question_ids':len({r['question_id'] for _,r in group}),
   'sample_risk_design_edition':'UNBOUND_TO_CURRENT_ORIGINAL_NATIVE_RELEASE',
   'permission_warrant_ref':None,'competent_original_U_ref':None,'competent_original_E_pre_ref':None,
   'source_use_status':'HOLD_NO_VERIFIED_CURRENT_SIGNED_ORIGINAL_RIGHT',
   'administered_U_status':'PARTIALLY_MAPPED_QRA_ONLY','eligible_original_count':None,
   'native_original_runs':0,'items':items})
 assert {(w['canonical_source_family'],w['canonical_wave'],'') for w in waves}==set(closed)
 scale='data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json'
 scales=json.loads((PINNED/scale).read_text())
 refs=[scales['selected_question_universe_path'],scales['inventory_path'],scales['ruling_ledger_path']]+[v['path'] for v in scales['response_authority_inputs']]
 statuses=Counter(r['authority_status'] for r in raw)
 out={'schema':'O35E_ORIGINAL35_METADATA_TO_OPERATION_INVENTORY@1','canonical_pin':PIN,
  'native_resolver':{'__file__':'$RETURN/runtime/pinned/'+native.__file__.split('/runtime/pinned/')[-1],
   'sha256':sha(Path(native.__file__).read_bytes()),'git_blob':sourcepin['files']['data/ddm_build_copy/ddm_v550_question_relation_authority.py']['git_blob'],
   'python':sys.version,'pandas':pandas.__version__,'function':'active_closed_35_waves','observed_pairs':[list(x) for x in closed]},
  'atlas':{'path':atlaspath,'git_blob':git('rev-parse',f'{PIN}:{atlaspath}').decode().strip(),'sha256':sha(atlas)},
  'historical_structure_manifest':{'path':structurepath,'git_blob':git('rev-parse',f'{PIN}:{structurepath}').decode().strip(),'sha256':sha(structurebytes),
   'recorded_canonical_rows':sum(s['canonical_intended']=='True' for s in structures),
   'total_recorded_header_columns_35':sum(w['historical_header_and_instrument_audit']['recorded_columns'] for w in waves),
   'unreconciled_header_minus_qra_columns':sum(w['historical_header_and_instrument_audit']['header_minus_qra_row_count'] for w in waves)},
  'census':{'wave_identity':'CENSUSED_35_EXACT_NATIVE_RESOLVER_EQUALS_ATLAS',
   'preserved_qra_metadata':'CENSUSED_WITHIN_PINNED_ARTIFACT','all_rows':len(raw),'active_rows':sum(w['qra_row_count'] for w in waves),
   'excluded_Asian_W6_rows':statuses['EXCLUDED_INACTIVE_WAVE'],'all_status_counts':dict(statuses),
   'administered_original_U':'PARTIALLY_MAPPED_NOT_EXHAUSTIVE','original_E_pre':'ABSENT_AS_VERIFIED_COMPETENT_CURRENT_ISSUANCE',
   'eligible_original_count':None,'original_measurement_products_this_return':0},
  'original_operation_status_default':{k:'HOLD_UNISSUED_ORIGINAL_SOURCE_ITEM_OP_BINDING' for k in operations},
  'operation_requirements':operations,
  'partial_response_registry':{'contracts':145,'selected_questions_declared':700,'active_authority_rows_declared':906,
   'grade':'partial scale metadata, not full18518 source-item authority or rights',
   'referenced_artifact_custody_at_pin':[{'path':p,'tracked_in_pin':p in tree} for p in refs]},
  'historical_narrow_source_version_witnesses':[
   {'atlas_id':'SRC02','source_sha256':'c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651',
    'C11_release':'R5_GT12_Q86A_Q86B_FROZEN','C11_release_hash':'8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295',
    'scope':'Historical GT12 Q86B CONDITIONER -> Q86A TARGET RAW CONTEXT; new original I03/I05/Batch and prospective E_pre are outside that permission.',
    'evidence_commit':'e894c8f5cb394b07d9c63ee702cfead23e9e81b5','source_freshly_checked_here':False},
   {'atlas_id':'SRC03','source_sha256':'3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8',
    'scope':'HQ272 historical metadata-only witness; no new row/temporal operation right.',
    'evidence_commit':PIN,'evidence_path':'PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/HQ272_M01_F01_SOURCE_NATIVE_TRIPLE_AND_FF02_SEMANTIC_INTAKE_R1.md','source_freshly_checked_here':False}],
  'waves':waves}
 (HERE/'01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'waves':len(waves),'active_qra_rows':out['census']['active_rows'],
  'native_resolver_import_verified':True,'manifest_source_hashes_bound':sum(bool(w['dataset_manifest_identity']['recorded_source_sha256']) for w in waves),
  'scale_references_present':sum(p in tree for p in refs),'scale_references':len(refs)}))

if __name__=='__main__':main()
