from pathlib import Path
import json
import pandas as pd
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from compile_positioned_relational_evidence import compile_scope

def test_positive_and_empirical_only(tmp_path):
    scope=tmp_path/'scope'; scope.mkdir()
    pd.DataFrame([
        {'pattern_id':'p1','member_ids':'question_impl.a question_impl.b','n_unweighted':'50'},
        {'pattern_id':'p2','member_ids':'question_impl.x question_impl.y','n_unweighted':'40'},
    ]).to_csv(scope/'joint_patterns.csv',index=False)
    (scope/'manifest.json').write_text(json.dumps({'v550j_substrate_mode':'prepared_required','forbid_database_access':True}))
    top=pd.DataFrame([{'authority_id':'A1','source_family':'GSS','wave':'2010','rule_id':'S14-T01','relation_type':'T','member_implementation_ids_json':json.dumps(['question_impl.a','question_impl.b'])}])
    blk=pd.DataFrame(columns=['source_family','active_wave','implementation_ids','candidate_id','rule_id'])
    ev,scan=compile_scope(scope,top,blk,'GSS','2010','US')
    assert scan['fused_manifest_verified']
    assert ((ev.semantic_relation_posture=='GOVERNED_POSITIVE') & (ev.empirical_cotravel_posture=='OBSERVED')).any()
    assert ((ev.semantic_relation_posture=='NO_GOVERNED_TYPED_RELATION') & (ev.empirical_cotravel_posture=='OBSERVED')).any()

def test_blocked_semantic_does_not_erase_empirical_and_partial_does_not_promote(tmp_path):
    scope=tmp_path/'scope'; scope.mkdir()
    pd.DataFrame([
        {'pattern_id':'blocked_obs','member_ids':'question_impl.c question_impl.d','n_unweighted':'30'},
        {'pattern_id':'partial','member_ids':'question_impl.a question_impl.z','n_unweighted':'20'},
    ]).to_csv(scope/'joint_patterns.csv',index=False)
    (scope/'manifest.json').write_text(json.dumps({'v550j_substrate_mode':'prepared_required','forbid_database_access':True}))
    top=pd.DataFrame([{'authority_id':'A1','source_family':'GSS','wave':'2010','rule_id':'S14-T01','relation_type':'T','member_implementation_ids_json':json.dumps(['question_impl.a','question_impl.b'])}])
    blk=pd.DataFrame([{'source_family':'GSS','active_wave':'2010','implementation_ids':json.dumps(['question_impl.c','question_impl.d']),'candidate_id':'B1','rule_id':'S14-T01'}])
    ev,_=compile_scope(scope,top,blk,'GSS','2010','US')
    assert ((ev.semantic_relation_posture=='BLOCKED_TYPED_RELATION') & (ev.empirical_cotravel_posture=='OBSERVED')).any()
    positive=ev[ev.semantic_relation_posture=='GOVERNED_POSITIVE'].iloc[0]
    assert positive.empirical_cotravel_posture=='NOT_TESTED'
