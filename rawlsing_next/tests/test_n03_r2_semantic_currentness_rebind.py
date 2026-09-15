from __future__ import annotations
import importlib.util, json, pathlib

BASE = pathlib.Path('data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N03-R2')

def load_replay():
    spec=importlib.util.spec_from_file_location('n03r2_replay', BASE/'replay_n03_r2.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_n03_r2_exact_current_18276_semantic_currentness_rebind():
    mod=load_replay(); ledger, vec, vb64, summary=mod.build(); manifest=json.loads((BASE/'01_AUTHORITY_JURISDICTION_MANIFEST.json').read_text())
    expected=manifest.get('expected_output')
    if expected is None:
        raise AssertionError('N03R2_DISCOVERY_JSON='+json.dumps(summary,sort_keys=True,separators=(',',':'))+'\nN03R2_VECTOR_B64='+vb64.decode())
    assert summary == expected
    assert (BASE/'03_CURRENT_18276_SEMANTIC_CURRENTNESS_VECTOR.zlib.b64').read_bytes().strip() == vb64
    remainder=json.loads((BASE/'04_UNRESOLVED_REMAINDER_MANIFEST.json').read_text())
    assert remainder['count']==summary['unresolved_count']
    assert remainder['sorted_id_stream_sha256']==summary['unresolved_sorted_id_stream_sha256']
    receipt=json.loads((BASE/'05_VALIDATION_RECEIPT.json').read_text())
    assert receipt['terminal']=='PASS'
    assert receipt['grain']==manifest['grain']
    assert receipt['summary']==summary
    assert len(ledger)==18276 and len({r['question_implementation_id'] for r in ledger})==18276
    assert all(r['top_level_authority_refs'] for r in ledger if r['top_level_disposition']!='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS')
    assert all(r['unresolved_basis'] for r in ledger if r['top_level_disposition']=='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS')
