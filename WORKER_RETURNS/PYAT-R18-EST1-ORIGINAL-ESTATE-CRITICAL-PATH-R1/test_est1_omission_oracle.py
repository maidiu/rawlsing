import copy
from est1_omission_oracle import judge, sha

BASE = dict(scope='SOURCEFREE_TEST_ONLY', issuer_kind='INDEPENDENT_PRECOMMITTED_TEST_FIXTURE', operations=[
    dict(op_id='W1:A:MARG', op_class='MARGINAL', target='A', conditioners=[], item_ids=['A'],source_id='SYN-A',wave='W1',release='REL-1',form='F1',unit='respondent',risk='R1',source_edition='edition-1',permission_scope='test-only:MARG',disposition='PRODUCED', disposition_reason='ELIGIBLE'),
    dict(op_id='W1:B|A:COND', op_class='CONDITIONAL',target='B',conditioners=['A'],item_ids=['B','A'],source_id='SYN-A',wave='W1',release='REL-1',form='F1',unit='respondent',risk='R1',source_edition='edition-1',permission_scope='test-only:COND',disposition='PRODUCED',disposition_reason='ELIGIBLE'),
    dict(op_id='W1:C:HELD', op_class='MARGINAL', target='C',conditioners=[],item_ids=['C'],source_id='SYN-A',wave='W1',release='REL-1',form='F2',unit='respondent',risk='UNKNOWN',source_edition='edition-1',permission_scope='test-only:HOLD',disposition='HELD',disposition_reason='ROUTING_NOT_PROVED'),
    dict(op_id='W2:D:NA',op_class='CONDITIONAL',target='D',conditioners=['B'],item_ids=['D','B'],source_id='SYN-B',wave='W2',release='REL-2',form='F3',unit='household',risk='R3',source_edition='edition-2',permission_scope='test-only:NA',disposition='INADMISSIBLE',disposition_reason='CROSS_UNIT'),
])

def fixture():
    exp = copy.deepcopy(BASE)
    actual = {'scope':'SOURCEFREE_TEST_ONLY','receipts':[]}
    for row in exp['operations']:
        r = copy.deepcopy(row)
        if r['disposition']=='PRODUCED':
            r.update(kind='EXECUTED_TEST_ONLY',native_owner_receipt_ref='mock-fixture:'+r['op_id'],native_owner_receipt_blob='mock-blobs-sourcefree',owner_execution_verified=True)
        else:
            r.update(kind='BLOCKED_ACCOUNTED')
        actual['receipts'].append(r)
    return exp,actual,sha(exp)

def kinds(result): return {x['kind'] for x in result['issues']}

def test_all_four_locally_reconcile():
    e,a,h=fixture(); assert judge(e,a,pinned_sha=h)['verdict']=='SOURCEFREE_TEST_ONLY_RECONCILED'

def test_missing_eligible():
    e,a,h=fixture(); a['receipts'].pop(0); assert 'OMITTED_ELIGIBLE_OPERATION' in kinds(judge(e,a,pinned_sha=h))

def test_swapped_same_cardinality():
    e,a,h=fixture(); a['receipts'][0]['op_id']='W1:Z:MARG'; result=judge(e,a,pinned_sha=h);assert {'OMITTED_ELIGIBLE_OPERATION','UNEXPECTED_OR_SUBSTITUTED_OPERATION'}<=kinds(result)

def test_held_miscount():
    e,a,h=fixture(); a['receipts'][2]['disposition']='PRODUCED'; assert 'EXACT_IDENTITY_OR_STATUS_MISMATCH' in kinds(judge(e,a,pinned_sha=h))

def test_held_silent_drop():
    e,a,h=fixture();a['receipts'].pop(2);assert 'MISSING_BLOCKED_ACCOUNTING' in kinds(judge(e,a,pinned_sha=h))

def test_duplicate_reissue():
    e,a,h=fixture();a['receipts'].append(copy.deepcopy(a['receipts'][0])); assert 'DUPLICATE_REISSUE' in kinds(judge(e,a,pinned_sha=h))

def test_forged_source_grant():
    e,a,h=fixture();a['receipts'][0]['source_grant']='ORIGINAL_SOURCE_LICENSED';assert 'FORGED_OR_UNAUTHORIZED_SOURCE_GRANT_CLAIM' in kinds(judge(e,a,pinned_sha=h))

def test_source_swap_without_count_change():
    e,a,h=fixture();a['receipts'][0]['source_id']='SYN-B';assert 'EXACT_IDENTITY_OR_STATUS_MISMATCH' in kinds(judge(e,a,pinned_sha=h))

def test_reason_swap_without_count_change():
    e,a,h=fixture();a['receipts'][2]['disposition_reason']='SOME_OTHER_REASON';assert 'EXACT_IDENTITY_OR_STATUS_MISMATCH' in kinds(judge(e,a,pinned_sha=h))

def test_changed_expectation_root_refused():
    e,a,h=fixture();e['operations'].pop();assert judge(e,a,pinned_sha=h)['verdict']=='INVALID_ORACLE_ROOT'

def test_unverified_native_owner_receipt_not_counted_as_real():
    e,a,h=fixture();a['receipts'][0]['owner_execution_verified']=False;assert 'NATIVE_OWNER_WITNESS_UNVERIFIED' in kinds(judge(e,a,pinned_sha=h))

def test_false_positive_for_inapplicable():
    e,a,h=fixture();a['receipts'][3]['kind']='EXECUTED_TEST_ONLY';assert 'HELD_OR_INADMISSIBLE_FALSE_POSITIVE' in kinds(judge(e,a,pinned_sha=h))

def test_wrong_edition():
    e,a,h=fixture();a['receipts'][1]['source_edition']='edition-2';assert 'EXACT_IDENTITY_OR_STATUS_MISMATCH' in kinds(judge(e,a,pinned_sha=h))

def test_no_production_claim():
    e,a,h=fixture();a['scope']='ACTUAL_ORIGINAL_SURVEY';assert 'ACTUAL_SOURCE_USE_NOT_GRANTED' in kinds(judge(e,a,pinned_sha=h))
