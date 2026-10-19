"""Exact original retained P1 Facts reach native M1's typed authority boundary.

This is not the commissioned new I03/Batch execution positive. Facts are retained
original results, and no M1 rule authority is supplied or synthesized.
"""
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parents[1]))
from retained_p1_consumer import run_consumer


def test_original_p1_native_consumer_receives_exact_facts_and_preserves_rule_hold():
    frozen=json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    expected={s['hash'] for s in frozen['facts'].values()}
    result=run_consumer()
    assert result['state']=='BLOCKED__MISSING_FAMILY_VALIDATION_RULE_AUTHORITY'
    assert result['M1_run'] is True
    assert result['adjudication_outcome']=='BLOCKED'
    assert {r['content_hash'] for r in result['bundle_fact_refs']}==expected
    assert {r['content_hash'] for r in result['consumed_fact_refs']}==expected
    assert len(result['bundle_fact_refs'])==3
    assert result['raw_denominators']=={role:s['raw_denominator'] for role,s in frozen['facts'].items()}
    assert result['raw_reads']==0
    assert result['new_I03_Batch_executions']==0
