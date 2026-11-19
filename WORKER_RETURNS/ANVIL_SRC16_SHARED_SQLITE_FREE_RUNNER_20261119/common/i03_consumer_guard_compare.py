#!/usr/bin/env python3
"""Compare actual saved-native I03 consumer results before/after the guard."""
from __future__ import annotations
import json, sys
from pathlib import Path

before=json.loads(Path(sys.argv[1]).read_text())['results']
after=json.loads(Path(sys.argv[2]).read_text())['results']

def fields(x):
    return {k:x.get(k) for k in ('typed_state','raw_denominator','raw_support','risk_count','replay_ref','detail')}
checks={
 'before_unresolved_not_denominator': before['unresolved_not']['raw_denominator']==1 and before['unresolved_not']['risk_count']==2,
 'before_unresolved_positive_supported': before['unresolved_positive']['typed_state']=='SUPPORTED' and before['unresolved_positive']['raw_support']==1,
 'after_unresolved_not_held': after['unresolved_not']['raw_denominator']==0 and after['unresolved_not']['risk_count']==0 and 'UNRESOLVED_CONDITION_MEMBER' in after['unresolved_not']['detail'],
 'before_unresolved_mixed_denominator': before['unresolved_mixed']['raw_denominator']==1 and before['unresolved_mixed']['risk_count']==2,
 'after_unresolved_mixed_held': after['unresolved_mixed']['raw_denominator']==0 and after['unresolved_mixed']['risk_count']==0 and 'UNRESOLVED_CONDITION_MEMBER' in after['unresolved_mixed']['detail'],
 'before_joint_mixed_denominator': before['joint_mixed']['raw_denominator']==1 and before['joint_mixed']['risk_count']==2,
 'after_joint_mixed_held': after['joint_mixed']['raw_denominator']==0 and after['joint_mixed']['risk_count']==0 and 'UNRESOLVED_CONDITION_MEMBER' in after['joint_mixed']['detail'],
 'after_unresolved_positive_held': after['unresolved_positive']['raw_denominator']==0 and after['unresolved_positive']['risk_count']==0 and 'UNRESOLVED_CONDITION_MEMBER' in after['unresolved_positive']['detail'],
 'known_missing_unchanged': fields(before['known_missing_not'])==fields(after['known_missing_not']) and after['known_missing_not']['typed_state']=='UNRESOLVED',
 'diagnostic_allowed_unchanged': fields(before['unresolved_diagnostic'])==fields(after['unresolved_diagnostic']) and after['unresolved_diagnostic']['typed_state']=='UNRESOLVED',
 'mapped_parity_denominator_risk_replay': fields(before['mapped_not'])==fields(after['mapped_not']) and after['mapped_not']['typed_state']=='ZERO_SUPPORT',
 'guard_flag_after': after['known_missing_not'] is not None,
}
status='I03_CONSUMER_GUARD_PASS_WITH_BEFORE_RED' if all(checks.values()) else 'I03_CONSUMER_GUARD_FAILED'
print(json.dumps({'status':status,'checks':checks,'before':before,'after':after,'raw_tokens_published':False,'source_read_performed':False},sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 2)
