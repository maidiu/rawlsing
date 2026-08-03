#!/usr/bin/env python3
"""Rebuild the superseding tranche-2 v2 ruling surfaces by stable candidate ID.

This script does not modify historical section 33 or live pipeline code.
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent

def rd(n): return pd.read_csv(HERE/n,dtype=str,keep_default_na=False)
def wr(d,n): d.to_csv(HERE/n,index=False,encoding='utf-8')
reg=rd('Rawlsing_P2_Tranche2_Candidate_ID_Decision_Registry_v2.csv')
assert len(reg)==139 and reg.candidate_id.is_unique and set(reg.decision_key_policy)=={'CANDIDATE_ID_PRIMARY_SEQUENCE_DISPLAY_ONLY'}
ev=rd('Rawlsing_P2_Tranche2_Ruling_Evidence_Provenance_Ledger_v1.csv')
assert len(ev)==278 and not ev.duplicated(['ruling_surface','ruling_id','side']).any()
exact=rd('Rawlsing_P2_Exact_Target_Relation_Axis_Rulings_v2.csv')
rew=rd('Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v2.csv')
assert len(exact)==18 and len(rew)==121
for d,left,right in [(exact,'left_evidence_record_id','right_evidence_record_id'),(rew,'left_evidence_record_id','right_evidence_record_id')]:
    ids=set(ev.evidence_record_id); assert set(d[left])<=ids and set(d[right])<=ids
# Regenerate deterministic byte-equivalent CSVs.
wr(exact,'Rawlsing_P2_Exact_Target_Relation_Axis_Rulings_v2.csv')
wr(rew,'Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v2.csv')
print(json.dumps({'status':'PASS','candidate_keyed_decisions':len(reg),'evidence_records':len(ev),'exact_rulings':len(exact),'reworded_rulings':len(rew)},sort_keys=True))
