import pandas as pd,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; errs=[]
v=pd.read_csv(R/'ADJUDICATION/CENTRAL_13_RULE_VERDICTS_R8C.csv'); b=pd.read_csv(R/'ADJUDICATION/BLOCKER_4_RESOLUTION_R8C.csv'); p=pd.read_csv(R/'PROVENANCE/CENTRAL_13_PARENT_DENOMINATOR_R8.csv'); bp=pd.read_csv(R/'PROVENANCE/BLOCKER_4_PARENT_DENOMINATOR_R8.csv'); s=json.load(open(R/'CURRENT_STATUS_R8C.json'))
def ck(n,x):
  if not x: errs.append(n)
ck('13 central packet ids accounted',set(v.canonical_packet_id)==set(p.canonical_packet_id))
ck('no empty central verdicts',v.central_verdict.fillna('').str.len().gt(0).all())
ck('no empty rationales',v.decisive_rationale.fillna('').str.len().gt(0).all())
ck('4 blocker ids accounted',set(b.canonical_packet_id)==set(bp.canonical_packet_id))
ck('remaining blocker exactly one',sum(b.blocker_resolution.str.startswith('REMAINS_BLOCKED'))==1)
ck('Q550 T10 accepted',((b.canonical_packet_id=='S14R8-d48368fafb02')&(b.rule_ids=='T10')&b.blocker_resolution.str.contains('ACCEPT')).any())
ck('Q628 T09 rejected and T10 accepted',((b.canonical_packet_id=='S14R8-4e6063f8f97d')&(b.rule_ids=='T09')&b.blocker_resolution.str.contains('REJECT')).any() and ((b.canonical_packet_id=='S14R8-4e6063f8f97d')&(b.rule_ids=='T10')&b.blocker_resolution.str.contains('ACCEPT')).any())
ck('job3 false',s['job3_authorized'] is False); ck('s14 not frozen',s['s14_authority_frozen'] is False)
print(json.dumps({'status':'PASS' if not errs else 'FAIL','checks':9,'errors':errs},indent=2)); sys.exit(1 if errs else 0)
