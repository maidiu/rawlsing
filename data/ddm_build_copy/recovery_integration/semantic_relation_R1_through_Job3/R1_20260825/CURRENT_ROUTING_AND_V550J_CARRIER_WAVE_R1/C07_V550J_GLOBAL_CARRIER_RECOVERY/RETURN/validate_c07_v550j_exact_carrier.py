#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, tarfile, hashlib, io, json
import pandas as pd
CARRIER_SHA='1687b4fea789aabf90e3906f104250f4d7bfa0055586a71066598fd9541f0286'; CARRIER_SIZE=506528
REG_NAME='Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv'; MEM_NAME='Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv'
REG_SHA='d75d6e30373d1fd45d29ffb34fc14d135c6addf0bbb7aa64d7aed57cf45cd8dd'; MEM_SHA='52f10099ce98f9fe9bcf161b80d50b05dfd2f584bb78c3bed007d5055f38980c'; REG_SIZE=2595849; MEM_SIZE=2752901
EXPECTED_FAMILY={'Afrobarometer':(230,1264),'Arab Barometer':(159,856),'Asian Barometer':(71,479),'EVS':(182,1237),'GSS':(722,2823),'Latinobarómetro':(123,680),'LiTS':(882,7878),'South Asia':(15,76),'WVS':(115,697)}
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(description='Validate C07 exact recovered 2,499/15,990 carrier. Materialize the Library carrier first, then pass its path.')
 ap.add_argument('carrier',help='Path to C07_EXACT_P2_SOURCE_STRUCTURE_CARRIER.tar.xz')
 carrier=Path(ap.parse_args().carrier).read_bytes(); assert len(carrier)==CARRIER_SIZE and sha(carrier)==CARRIER_SHA
 with tarfile.open(fileobj=io.BytesIO(carrier),mode='r:xz') as tf:
  names={m.name for m in tf.getmembers() if m.isfile()}; assert names=={REG_NAME,MEM_NAME},names
  rb=tf.extractfile(REG_NAME).read(); mb=tf.extractfile(MEM_NAME).read()
 assert len(rb)==REG_SIZE and sha(rb)==REG_SHA; assert len(mb)==MEM_SIZE and sha(mb)==MEM_SHA
 r=pd.read_csv(io.BytesIO(rb),dtype=str,keep_default_na=False); m=pd.read_csv(io.BytesIO(mb),dtype=str,keep_default_na=False)
 assert len(r)==2499 and len(m)==15990 and r.source_structure_id.nunique()==2499
 rids=set(r.source_structure_id); assert set(m.source_structure_id)==rids
 rr=r.set_index('source_structure_id'); actual=m.groupby('source_structure_id').size(); declared=rr.declared_member_count.astype(int); recovered=rr.recovered_member_count.astype(int)
 assert (declared.reindex(actual.index)==actual).all() and (recovered.reindex(actual.index)==actual).all(); assert declared.sum()==15990 and recovered.sum()==15990
 j=m.join(rr[['source_family','wave']],on='source_structure_id',rsuffix='_registry'); assert (j.source_family==j.source_family_registry).all() and (j.wave==j.wave_registry).all()
 for sid,g in m.groupby('source_structure_id',sort=False):
  vals=[int(x) for x in g.member_order]; assert len(vals)==len(set(vals)) and set(vals)==set(range(1,len(vals)+1)),sid
 for c in ['source_variable_code','question_implementation_id','lineage_id']: assert (m[c]!='').all(),c
 assert not r.duplicated().any() and not m.duplicated().any() and not m.duplicated(['source_structure_id','member_order']).any()
 assert set(r.membership_recovery_status)=={'COMPLETE'} and set(r.cross_source_use_status)=={'DISCOVERY_STRUCTURE_ONLY_NOT_J_FAMILY_AUTHORITY'}
 rf=r.source_family.value_counts().to_dict(); mf=m.source_family.value_counts().to_dict(); observed={k:(int(rf.get(k,0)),int(mf.get(k,0))) for k in EXPECTED_FAMILY}; assert observed==EXPECTED_FAMILY
 print(json.dumps({'status':'PASS','carrier_sha256':sha(carrier),'source_structures':len(r),'structure_memberships':len(m),'registry_sha256':sha(rb),'memberships_sha256':sha(mb),'source_family_partitions':{k:{'structures':v[0],'memberships':v[1]} for k,v in observed.items()},'authority_ceiling':'RECOVERY_CARRIER_ONLY__NOT_J_FAMILY_AUTHORITY'},indent=2,ensure_ascii=False))
if __name__=='__main__':main()
