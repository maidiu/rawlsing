#!/usr/bin/env python3
"""One shared all-35 metadata/C11-input producer.

Metadata only: no original source body is opened, read, decoded or hashed.
Codebooks are descriptions, not source permission or scientific eligibility.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117')
REPO=Path('/Users/matthewsmith/Desktop/Rawlsing')
sys.path.insert(0, str(ROOT/'IMPLEMENTER'))
DATA=REPO/'data'/'Data'
CODEBOOKS=REPO/'data'/'FINAL CODEBOOKS'/'FINAL FINAL CODEBOOKS'
MATRIX=HERE/'evidence'/'35_row_source_rights_matrix.json'
SRC04_CONFIG=HERE/'inputs'/'SRC04'/'source.config.repaired.v2.json'
SRC04_CONFIG_SHA='5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5'
SRC04_CANONICAL='28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d'
SRC04_ACCEPTED={
  'commit':'ba41253681212be14a0cde009afb99d77e14935e',
  'release_object_id':'SRC04_ARAB_BAROMETER_I_PREPARATION',
  'semantic_release_hash':'9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1',
  'rows':7337,'selected_responses':177,'selected_coordinates':3,
  'response_positions':1298649,'q217_held_unbound_cells':38,
  'initial_target':'163_RESPONSES_PLUS_2_COORDINATES',
  'repaired_target':'178_RESPONSES_PLUS_3_COORDINATES_WHERE_SOURCE_QUALIFIED',
}
Q2_REQUIRED=['FrozenInputCensus','SourceInventory','GrammarPolicy','ScientificFrontier','current SourceReadDecisionResolver adapter']

class ProducerRefusal(ValueError): pass

def sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def codebook_map():
    out={}
    for p in CODEBOOKS.iterdir():
        if p.is_file() and p.suffix.lower()=='.csv':
            out[sha(p)] = p
    return out

def load_matrix(path: Path):
    d=json.loads(path.read_text())
    ids=[s['source_id'] for s in d['sources']]
    if ids!=d['historical_ledger']['source_ids'] or len(ids)!=35 or len(set(ids))!=35:
        raise ProducerRefusal('ALL35_IDENTITY_ORDER_OR_CARDINALITY_DRIFT')
    return d

def main() -> int:
    global SRC04_CONFIG
    ap=argparse.ArgumentParser();ap.add_argument('--matrix',default=str(MATRIX));ap.add_argument('--out',default=str(HERE/'ALL35_RESULT.json'));ap.add_argument('--bundles',default=str(HERE/'bundles'));ap.add_argument('--src04-config',default=str(SRC04_CONFIG));a=ap.parse_args()
    SRC04_CONFIG=Path(a.src04_config)
    matrix=load_matrix(Path(a.matrix)); cbm=codebook_map(); bundles=Path(a.bundles);bundles.mkdir(parents=True,exist_ok=True)
    rows=[]; produced=0; held=0
    for s in matrix['sources']:
        sid=s['source_id']; cr=s.get('custody_refs',{}); code_hash=cr.get('codebook_sha256')
        codebook=cbm.get(code_hash)
        if codebook is None: raise ProducerRefusal(f'CODEBOOK_HASH_NOT_FOUND:{sid}:{code_hash}')
        rel=s.get('host_custody',{}).get('artifact_relpath')
        data_path=DATA/Path(rel).name if rel else None
        if data_path is None or not data_path.is_file():
            raise ProducerRefusal(f'DATA_PATH_MISSING:{sid}')
        observed=data_path.stat().st_size; declared=s.get('host_custody',{}).get('observed_size_bytes')
        if declared is not None and observed!=declared: raise ProducerRefusal(f'DATA_SIZE_DRIFT:{sid}:{observed}!={declared}')
        config_loaded=False; config_sha=None; config_canonical=None
        if sid=='SRC04':
            if not SRC04_CONFIG.is_file() or sha(SRC04_CONFIG)!=SRC04_CONFIG_SHA:
                raise ProducerRefusal('SRC04_CONFIG_FILE_DRIFT')
            # Current accepted adapter must load the exact historical config.
            from rawlsing_next.pre553_r157_projection_adapter import load_source_config, canonical_config_hash
            cfg=load_source_config(SRC04_CONFIG)
            config_sha=sha(SRC04_CONFIG); config_canonical=canonical_config_hash(cfg)
            if config_canonical!=SRC04_CANONICAL or cfg.source_id!=sid or cfg.active_source_sha256!=s['declared_source_sha256']:
                raise ProducerRefusal('SRC04_CONFIG_IDENTITY_DRIFT')
            if (len(cfg.document['physical_slots']),len(cfg.document['response_slots']),len(cfg.document['coordinate_slots']))!=(181,178,3):
                raise ProducerRefusal('SRC04_CONFIG_SCOPE_DRIFT')
            config_loaded=True
        status=('METADATA_WITNESS_VALIDATED__Q2_INPUTS_MISSING' if sid=='SRC04' else
                'SOURCE_READ_C11_AUTHORIZED__I03_I05_EXCLUDED__Q2_INPUTS_MISSING' if sid=='SRC17' else
                'SOURCEFREE_TRANSFER_PINNED__Q2_INPUTS_MISSING' if sid=='SRC01' else
                'HELD__CURRENT_SOURCE_RIGHTS_AND_Q2_INPUTS_MISSING')
        missing=list(Q2_REQUIRED)
        if s['rights_decision']!='AUTHORIZED_FOR_THIS_HOST_PURPOSE': missing.insert(0,'current source-use grant')
        if sid=='SRC17': missing.append('I03/I05 scientific issuer (source-read/C11 grant excludes I03/I05)')
        if not config_loaded: missing.insert(0,'current materialized SourceConfig')
        bundle={
          'schema':'ANVIL_ALL35_C11_INPUT_BUNDLE@1','source_id':sid,
          'family':s['family'],'wave':s['wave'],'source_format':s['source_format'],
          'source_artifact_id':s['source_artifact_id'],
          'source_sha256':s['declared_source_sha256'],
          'declared_rows':s['declared_rows'],'declared_columns':s['declared_columns'],
          'counts':s['counts'],
          'rights_decision':s['rights_decision'],'current_permission':s.get('current_permission'),
          'data_metadata_only':{'path':str(data_path),'present':True,'size':observed,'size_matches':declared is None or observed==declared},
          'codebook':{'path':str(codebook),'sha256':code_hash,'status':'METADATA_DESCRIPTION_ONLY_NOT_AUTHORIZATION'},
          'source_config':{'path':cr.get('source_config_path'),'file_sha256':config_sha or cr.get('source_config_file_sha256'),'canonical_sha256':config_canonical or cr.get('source_config_canonical_sha256'),'materialized':config_loaded},
          'sourcefree_fixture':{'file_sha256':cr.get('fixture_file_sha256'),'config_file_sha256':cr.get('fixture_config_file_sha256'),'status':'SOURCEFREE_FIXTURE_PIN_ONLY__NOT_ORIGINAL_READ'},
          'metadata_bundle_status':status,
          'q2_input_status':'HELD',
          'missing_q2_inputs':missing,
          'original_source_bodies_read':False,
        }
        if sid=='SRC04':
            bundle['accepted_c11_reference']=SRC04_ACCEPTED
            bundle['accepted_grant']={'path':'campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json','commit':'303a57851785557fff8229e29a5554717168cbd1','sha256':'d8f13c67af276175266168e9af1a91e28fd543fcecadc1e79112a9854b4a8139'}
        (bundles/(sid+'.json')).write_text(json.dumps(bundle,indent=2,sort_keys=True)+'\n')
        rows.append({'source_id':sid,'family':s['family'],'wave':s['wave'],'bundle':f'bundles/{sid}.json','status':status,'questions':s['counts']['questions'],'physical_slots':s['counts']['physical_slots'],'response_slots':s['counts']['response_slots'],'coordinate_slots':s['counts']['coordinate_slots'],'weight_slots':s['counts']['weight_slots'],'missing_q2_inputs':missing})
        produced+=1
    result={'schema':'ANVIL_ALL35_C11_INPUT_RESULT@1','canonical_commit':'d4f0a6499432aa3186c0d92174fa228211759e44','accepted_code':'aee95429609c372564e996c2d3d3eb30e9253cbf','matrix_sha256':sha(Path(a.matrix)),'source_count':35,'metadata_bundles_produced':produced,'metadata_bundles_validated':produced,'q2_executable_bundles':0,'q2_held_bundles':35,'source_rights_held_bundles':sum(1 for s in matrix['sources'] if s['rights_decision']!='AUTHORIZED_FOR_THIS_HOST_PURPOSE'),'typed_held_bundles':35,'witness_config_loaded':'SRC04','sourcefree_transfer_example':'SRC01','rows':rows,'limits':['metadata only; no original bodies','codebook is description not authorization','no Q2 frontier/census/resolver provided; all Q2 status HELD','no new source/science/rights']}
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('source_count','metadata_bundles_produced','metadata_bundles_validated','q2_executable_bundles','q2_held_bundles','source_rights_held_bundles','typed_held_bundles','witness_config_loaded','sourcefree_transfer_example')},sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
