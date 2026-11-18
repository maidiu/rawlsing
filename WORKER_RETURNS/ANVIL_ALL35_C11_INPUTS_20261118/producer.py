#!/usr/bin/env python3
"""One shared all-35 metadata/C11-input producer.

Metadata only: no original source body is opened, read, decoded or hashed.
Codebooks are descriptions, not source permission or scientific eligibility.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile
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
CONFIG_INDEX_COMMIT='ad3386b718fd9ace234a00dab3b32ee51039b77f'
CONFIG_INDEX_PATH='WORKER_RETURNS/ANVIL_ALL35_R157_CONFIG_MATERIALIZATION_20261118/CONFIG_INDEX.json'
CONFIG_INDEX_SHA256='d6741f8e7d084f031d0b762f4f8b6465dc35eb73d7ab6ffc64598123174a1f27'
SRC04_REPAIR_COMMIT='da23c65d1e211cb7e8ce416e98757f321b78d25e'
SRC04_REPAIR_PATH='rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json'
SRC04_STALE_COMMIT='1924499ef52403a0f331b8aff9b7c7eff99bf1e2'
SRC04_STALE_PATH='rawlsing_next/source_configuration/data/SRC04/source.config.json'
SRC04_STALE_FILE_SHA='eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900'

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

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_bytes(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT/"IMPLEMENTER"), "show", f"{commit}:{path}"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise ProducerRefusal(f"CONFIG_GIT_MATERIALIZATION_FAILED:{commit}:{path}") from exc

def load_config_index(matrix):
    raw=git_bytes(CONFIG_INDEX_COMMIT, CONFIG_INDEX_PATH)
    if sha_bytes(raw)!=CONFIG_INDEX_SHA256:
        raise ProducerRefusal("CONFIG_INDEX_HASH_DRIFT")
    index=json.loads(raw)
    if index.get("schema")!="ANVIL_ALL35_R157_CONFIG_INDEX@1":
        raise ProducerRefusal("CONFIG_INDEX_SCHEMA_DRIFT")
    rows=index.get("rows",[])
    ids=[r.get("source_id") for r in rows]
    expected=[s["source_id"] for s in matrix["sources"]]
    if ids!=expected or len(rows)!=35 or len(set(ids))!=35:
        raise ProducerRefusal("CONFIG_INDEX_IDENTITY_ORDER_OR_CARDINALITY_DRIFT")
    refs=[(r["source_config"].get("revision_commit"),r["source_config"].get("revision_path")) for r in rows]
    if len(set(refs))!=35 or len({r["source_config"].get("file_sha256") for r in rows})!=35:
        raise ProducerRefusal("CONFIG_INDEX_REVISIONS_NOT_DISTINCT")
    if index.get("counts",{}).get("qualified_metadata")!=35 or index.get("counts",{}).get("authorized_executable_q2")!=0:
        raise ProducerRefusal("CONFIG_INDEX_COUNTS_DRIFT")
    return index

def expected_config_shape(bundle):
    c=bundle["counts"]
    return {"rows":bundle["declared_rows"],"columns":bundle["declared_columns"],
            "original_items":c["original_items"],"physical_slots":c["physical_slots"],
            "questions":c["questions"],"response_slots":c["response_slots"],
            "coordinate_slots":c["coordinate_slots"],"weight_slots":c["weight_slots"],
            "routing_rules":c["routing_rules"]}

def actual_config_shape(config):
    d=config.document
    return {"rows":d["identity"]["source_row_count"],
            "columns":d["identity"]["source_column_count"],
            "original_items":d["identity"]["original_item_count"],
            "physical_slots":len(d["physical_slots"]),
            "questions":len(d["questions"]),
            "response_slots":len(d["response_slots"]),
            "coordinate_slots":len(d["coordinate_slots"]),
            "weight_slots":len(d["weight_slots"]),
            "routing_rules":len(d["routing"])}

def bind_one_config(row, bundle, matrix_source, stage_dir):
    sid=row["source_id"]
    loc=row["source_config"]
    if bundle["source_id"]!=sid or matrix_source["source_id"]!=sid:
        raise ProducerRefusal(f"CONFIG_SOURCE_ROW_MISMATCH:{sid}")
    if row.get("q2_input_status")!="HELD" or row.get("authorized_executable_q2") is not False:
        raise ProducerRefusal(f"CONFIG_Q2_STATUS_DRIFT:{sid}")
    if sid=="SRC04":
        expected=(SRC04_REPAIR_COMMIT,SRC04_REPAIR_PATH)
        if (loc.get("revision_commit"),loc.get("revision_path"))!=expected:
            raise ProducerRefusal("STALE_SRC04_CONFIG_REFUSED")
        if loc.get("file_sha256")!=SRC04_CONFIG_SHA or loc.get("canonical_sha256")!=SRC04_CANONICAL:
            raise ProducerRefusal("STALE_SRC04_CONFIG_REFUSED")
    raw=git_bytes(loc["revision_commit"],loc["revision_path"])
    file_sha=sha_bytes(raw)
    if file_sha!=loc.get("file_sha256"):
        raise ProducerRefusal(f"CONFIG_FILE_SHA_MISMATCH:{sid}")
    staged=Path(stage_dir)/f"{sid}.config.json"; staged.write_bytes(raw)
    from rawlsing_next.pre553_r157_projection_adapter import canonical_config_hash, load_source_config
    config=load_source_config(staged)
    canonical=canonical_config_hash(config)
    d=config.document
    checks={
        "source_id":config.source_id==sid==bundle["source_id"]==matrix_source["source_id"],
        "identity_class":config.identity_class=="ORIGINAL_SOURCE",
        "active_source_sha":config.active_source_sha256==bundle["source_sha256"]==matrix_source["declared_source_sha256"],
        "expected_source_sha":d["identity"]["expected_source_sha256"]==bundle["source_sha256"],
        "binding_source_sha":d["binding"]["source_sha256"]==bundle["source_sha256"],
        "source_row_count":d["identity"]["source_row_count"]==bundle["declared_rows"],
        "source_column_count":d["identity"]["source_column_count"]==bundle["declared_columns"],
        "binding_row_count":d["binding"]["row_count"]==bundle["declared_rows"],
        "wave":d["identity"]["wave"]==bundle["wave"],
        "declared_shape":actual_config_shape(config)==expected_config_shape(bundle),
        "config_purpose":config.config_purpose=="SOURCE_PREPARATION",
        "config_schema":d.get("schema")=="PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "canonical_sha":canonical==loc.get("canonical_sha256"),
    }
    if not all(checks.values()):
        raise ProducerRefusal(f"CONFIG_BINDING_MISMATCH:{sid}:{json.dumps(checks,sort_keys=True)}")
    return {"revision_commit":loc["revision_commit"],"revision_path":loc["revision_path"],
            "revision_ref":f'{loc["revision_commit"]}:{loc["revision_path"]}',
            "file_sha256":file_sha,"canonical_sha256":canonical,
            "revision_basis":loc.get("revision_basis"),"wave":d["identity"]["wave"],
            "declared_shape":actual_config_shape(config),"checks":checks}

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
    matrix=load_matrix(Path(a.matrix)); index=load_config_index(matrix)
    cbm=codebook_map(); bundles=Path(a.bundles);bundles.mkdir(parents=True,exist_ok=True)
    rows=[]; produced=0; held=0
    stage=Path(tempfile.mkdtemp(prefix='anvil-all35-configs-'))
    for s, idx_row in zip(matrix['sources'],index['rows']):
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
        binding=bind_one_config(idx_row, {'source_id':sid,'source_sha256':s['declared_source_sha256'],'declared_rows':s['declared_rows'],'declared_columns':s['declared_columns'],'counts':s['counts'],'wave':s['wave']}, s, stage)
        config_loaded=True
        config_sha=binding['file_sha256']; config_canonical=binding['canonical_sha256']
        status=('METADATA_WITNESS_VALIDATED__Q2_INPUTS_MISSING' if sid=='SRC04' else
                'SOURCE_READ_C11_AUTHORIZED__I03_I05_EXCLUDED__Q2_INPUTS_MISSING' if sid=='SRC17' else
                'SOURCEFREE_TRANSFER_PINNED__Q2_INPUTS_MISSING' if sid=='SRC01' else
                'HELD__CURRENT_SOURCE_RIGHTS_AND_Q2_INPUTS_MISSING')
        missing=list(Q2_REQUIRED)
        if s['rights_decision']!='AUTHORIZED_FOR_THIS_HOST_PURPOSE': missing.insert(0,'current source-use grant')
        if sid=='SRC17': missing.append('I03/I05 scientific issuer (source-read/C11 grant excludes I03/I05)')
        missing=[x for x in missing if x!='current materialized SourceConfig']
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
          'source_config':{'path':binding['revision_path'],'revision_path':binding['revision_path'],'revision_commit':binding['revision_commit'],'revision_ref':binding['revision_ref'],'file_sha256':config_sha,'canonical_sha256':config_canonical,'revision_basis':binding['revision_basis'],'config_wave':binding['wave'],'binding_status':'BOUND_EXACT_CONFIG_REVISION','binding_checks':binding['checks'],'config_index':{'commit':CONFIG_INDEX_COMMIT,'path':CONFIG_INDEX_PATH,'sha256':CONFIG_INDEX_SHA256},'materialized':True},
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
        rows.append({'source_id':sid,'family':s['family'],'wave':s['wave'],'bundle':f'bundles/{sid}.json','status':status,'questions':s['counts']['questions'],'physical_slots':s['counts']['physical_slots'],'response_slots':s['counts']['response_slots'],'coordinate_slots':s['counts']['coordinate_slots'],'weight_slots':s['counts']['weight_slots'],'config_binding':{'revision_ref':binding['revision_ref'],'file_sha256':binding['file_sha256'],'canonical_sha256':binding['canonical_sha256'],'wave':binding['wave'],'status':'BOUND_EXACT'},'missing_q2_inputs':missing})
        produced+=1
    result={'schema':'ANVIL_ALL35_C11_INPUT_RESULT@1','canonical_commit':'d4f0a6499432aa3186c0d92174fa228211759e44','accepted_code':'aee95429609c372564e996c2d3d3eb30e9253cbf','matrix_sha256':sha(Path(a.matrix)),'source_count':35,'metadata_bundles_produced':produced,'metadata_bundles_validated':produced,'config_binding_count':35,'config_binding_failures':0,'config_index':{'schema':index['schema'],'commit':CONFIG_INDEX_COMMIT,'path':CONFIG_INDEX_PATH,'sha256':CONFIG_INDEX_SHA256,'accepted_by_immutable_ref':True},'q2_executable_bundles':0,'q2_held_bundles':35,'source_rights_held_bundles':sum(1 for s in matrix['sources'] if s['rights_decision']!='AUTHORIZED_FOR_THIS_HOST_PURPOSE'),'typed_held_bundles':35,'witness_config_loaded':'SRC04','sourcefree_transfer_example':'SRC01','rows':rows,'limits':['metadata only; no original bodies','codebook is description not authorization','no Q2 frontier/census/resolver provided; all Q2 status HELD','no new source/science/rights']}
    shutil.rmtree(stage,ignore_errors=True)
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('source_count','metadata_bundles_produced','metadata_bundles_validated','config_binding_count','config_binding_failures','q2_executable_bundles','q2_held_bundles','source_rights_held_bundles','typed_held_bundles','witness_config_loaded','sourcefree_transfer_example')},sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
