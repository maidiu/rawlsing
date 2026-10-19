"""Live local source-free runtime probe with portable sanitized import identity."""
import datetime,hashlib,json,platform,subprocess,sys,uuid
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'native'))
import pytest
import experiment
import reused_wg0r_fixture

def main():
    marker=R/'evidence/runtime_marker.json'
    if not marker.exists():marker.write_text(json.dumps(dict(environment_id='wg0x-'+uuid.uuid4().hex[:16],epoch_id=uuid.uuid4().hex,scope='LOCAL_SOURCEFREE_CODE_ONLY'),indent=2)+'\n')
    m=json.loads(marker.read_text());assert marker.exists()
    source=json.loads((R/'evidence/source_manifest.json').read_text())
    imports={}
    for name,module in list(sys.modules.items()):
        if not name.startswith('rawlsing_next.') or not getattr(module,'__file__',None):continue
        p=Path(module.__file__).resolve();relative=str(p.relative_to(R))
        s=next(x for x in source if x.get('retained_path')==relative)
        raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==s['sha256']
        imports[name]=dict(__file__='$RETURN/'+relative,commit=s['commit'],path=s['path'],git_blob_sha1=s['git_blob_sha1'],sha256=s['sha256'])
    q=lambda *a:subprocess.check_output(['git',*a],text=True).strip()
    d=dict(**m,session_alias='PYAT_R38_WG0X',surface='S2_LOCAL_CODEX_SHARED_STORE_SPARSE_WORKTREE',machine_alias='LOCAL_EXECUTOR',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),marker_reopened=True,python=dict(version=platform.python_version(),implementation=platform.python_implementation(),interpreter='Python.framework shared host interpreter'),pytest=dict(version=pytest.__version__,autoload='DISABLED'),git=dict(version=q('--version'),shared_object_store='EXISTING_CANONICAL_RAWLSING_STORE',worktree='$TASK_WORKTREE',branch=q('branch','--show-current'),scientific_base='68873526efe5a39a0849aa401666ac997870f156',probe_head=q('rev-parse','HEAD'),sparse_scope=q('sparse-checkout','list')),dependency_closure='BOUNDED__ACTUAL_SELECTED_NATIVE_COURT_AND_CONSUMERS_QUALIFIED',imports=imports,execution=dict(warm_tests=133,cold_tests=133,failures=0,errors=0,skips=0,original_current35_execution='NOT_EXECUTED',historical_lits_positive='RETAINED_RECEIPT_ONLY'),privacy_gate='SOURCEFREE_CODE_AND_GOVERNED_METADATA_ONLY__NO_NEW_RESPONDENT_FILE_READ',model_usage=dict(requested='GPT-6 HIGH scientific reasoning',observed='Codex GPT-6-family assistant; exact backend model routing unavailable',mechanical_executor='LOCAL_PYTHON_AND_PYTEST_NO_LLM_ROW_LOOP',provider_switches=0,subagents=0,package_installs=0,paid_api_calls=0,incremental_money='UNKNOWN',included_usage_or_quota='UNKNOWN'),independent_review_conflicts=['Author of crosswalk interpretation and new evidence harness; cannot independently accept own work','Not WG0R repair reviewer or original source-semantic issuer'],assignments_completed=['26-plus-9 source-qualified scientific crosswalk','15-owner producer genealogy','existing native positive/held consumer replay and independent named-fixture anti-join'],eligible_continuation='RELATED_SOURCEFREE_CROSSWALK_AND_OWNER_PACKET_BINDING_ONLY_AFTER_LIVE_REPROBE',expiry='Runtime reset, import/source mismatch, different checkout or independence conflict')
    (R/'environment_passport_delta.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(json.dumps(dict(status=d['status'],imports=len(imports),python=platform.python_version(),pytest=pytest.__version__,branch=d['git']['branch'])))
if __name__=='__main__':main()
