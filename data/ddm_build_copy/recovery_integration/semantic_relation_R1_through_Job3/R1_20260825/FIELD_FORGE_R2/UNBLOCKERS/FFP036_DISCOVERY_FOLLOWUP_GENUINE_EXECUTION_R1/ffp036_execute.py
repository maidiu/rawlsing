#!/usr/bin/env python3
import csv,gzip,hashlib,json,os,sys,collections,shutil
from pathlib import Path
V=['Q76A','Q76B','Q86A','Q86B','Q86C','Q86D','Q86E','Q86F']; C=['BFO','BOT','CVE','KEN','LES','MAU','MLW','MOZ','NAM','SAF','UGA']
H={'risk':'c5281c564c1cafdcbe6769013b46834bc4da9bb481e56a172a581fee745cb8dc','responses':'98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709','exposures':'0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce','roster':'4968bb74fc733cbbd3dd4db4d3aa4dfe7439b172d3fcdf62ee0ee2bc2f01319c','roster_raw':'5bf42464f3ff93e97d80f8ce178d670aa7fee98d13144f9c2d29d4f59032bced'}
TH=['predicate_id','subset_size','subset_mask','variables','state_pairs_json','original_support','COUNTRY_ALPHA3','country_support','status']
def die(s): raise SystemExit(s)
def hf(p,op=open):
 h=hashlib.sha256()
 with op(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def line(a):return ('\t'.join(map(str,a))+'\n').encode()
def dg(src,dst):
 with open(src,'rb') as i,open(dst,'wb') as o:
  with gzip.GzipFile(filename='',mode='wb',fileobj=o,mtime=0,compresslevel=9) as z:shutil.copyfileobj(i,z,1<<20)
def roster(p):
 R=[]; by=collections.OrderedDict(); n=collections.Counter()
 with gzip.open(p,'rt',newline='') as f:
  rd=csv.DictReader(f,delimiter='\t')
  if rd.fieldnames!=['predicate_id','subset_size','subset_mask','variables','state_pairs_json','support']:die('BLOCKED__DISCOVERY_PREDICATE_IDENTITY_UNRESOLVED')
  for r in rd:
   m=int(r['subset_mask']); s=int(r['subset_size']); q=int(r['support']); pairs=json.loads(r['state_pairs_json']); vv=[V[i] for i in range(8) if m>>i&1]
   if s!=len(vv) or [x[0] for x in pairs]!=vv or r['variables']!='|'.join(vv) or hashlib.sha256(r['state_pairs_json'].encode()).hexdigest()!=r['predicate_id']:die('BLOCKED__DISCOVERY_PREDICATE_IDENTITY_UNRESOLVED')
   x=(r['predicate_id'],s,m,r['variables'],r['state_pairs_json'],q,tuple(str(y[1]) for y in pairs));R.append(x);by.setdefault(m,[]).append(x);n[s]+=1
 if len(R)!=62609 or dict(n)!={1:34,2:469,3:2861,4:9736,5:18865,6:19218,7:9570,8:1856}:die('BLOCKED__DISCOVERY_PREDICATE_IDENTITY_UNRESOLVED')
 return R,by
def risk(p):
 d={}
 with gzip.open(p,'rt',newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
   if r['respondent_local_id'] in d:die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
   d[r['respondent_local_id']]=r['COUNTRY_ALPHA3']
 if len(d)!=19210 or sorted(set(d.values()))!=C:die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
 return d,sorted(d)
def wide(p,c,rids):
 ix={v:i for i,v in enumerate(V)};d={r:[None]*8 for r in rids};n=bad=0
 with gzip.open(p,'rt',newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
   rid=r['respondent_local_id'];v=r['source_variable']
   if rid not in d or v not in ix:continue
   i=ix[v]
   if d[rid][i] is not None:die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
   d[rid][i]=r['source_response_state'];n+=1;bad+=r['COUNTRY_ALPHA3']!=c[rid]
 if n!=153680 or bad or any(None in d[r] for r in rids):die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
 return d
def exposure(p,c):
 M={'Afrobarometer:R5:'+v for v in V};seen=set();bad=0
 with gzip.open(p,'rt',newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
   rid=r['respondent_local_id'];m=r['empirical_measurement_id']
   if rid not in c or m not in M:continue
   k=(rid,m)
   if k in seen:die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
   seen.add(k);bad+=r['exposure_state']!='EXPOSED__PROVED' or r['COUNTRY_ALPHA3']!=c[rid] or r['predicate_input_symbol']!='COUNTRY_ALPHA3' or r['predicate_input_value']!=c[rid]
 if len(seen)!=153680 or bad:die('BLOCKED__SAME_UNIT_OR_EXPOSURE_UNRESOLVED')
def w1(path,by,S,c,rids):
 h=hashlib.sha256();rows=pos=zero=bad=0
 with open(path,'wb') as o:
  b=line(TH);o.write(b);h.update(b)
  for m,ps in by.items():
   ii=[i for i in range(8) if m>>i&1];a=collections.Counter((tuple(S[r][i] for i in ii),c[r]) for r in rids)
   for p in ps:
    sm=0
    for cc in C:
     n=a.get((p[6],cc),0);sm+=n;st='OBSERVED_POSITIVE' if n else 'OBSERVED_ZERO';pos+=n>0;zero+=n==0;b=line([*p[:6],cc,n,st]);o.write(b);h.update(b);rows+=1
    bad+=sm!=p[5]
 if rows!=688699 or bad:die('INVALID__COMMON_INPUT_OR_RISK_SET_DIVERGENCE')
 return h.hexdigest(),pos,zero
def hash_from_counts(R,cnt):
 h=hashlib.sha256();h.update(line(TH));rows=bad=0
 for p in R:
  sm=0
  for cc in C:
   n=cnt.get((p[2],p[6],cc),0);sm+=n;st='OBSERVED_POSITIVE' if n else 'OBSERVED_ZERO';h.update(line([*p[:6],cc,n,st]));rows+=1
  bad+=sm!=p[5]
 if rows!=688699 or bad:die('INVALID__REPLAY_OR_INTEGRITY_FAILURE')
 return h.hexdigest()
def main(I,O):
 I=Path(I);O=Path(O);O.mkdir(parents=True,exist_ok=True);P={'roster':I/'ffif014_frozen_discovery_predicate_roster.tsv.gz','risk':I/'core_claim_common_risk_set.tsv.gz','responses':I/'selected_response_facts.tsv.gz','exposures':I/'selected_exposure_facts.tsv.gz'}
 for k,p in P.items():
  if hf(p)!=H[k]:die('INVALID__REPLAY_OR_INTEGRITY_FAILURE')
 if hf(P['roster'],gzip.open)!=H['roster_raw']:die('BLOCKED__DISCOVERY_PREDICATE_IDENTITY_UNRESOLVED')
 R,by=roster(P['roster']);c,rids=risk(P['risk']);exposure(P['exposures'],c);S=wide(P['responses'],c,rids)
 a=O/'a.tsv';b=O/'b.tsv';ha,pos,zero=w1(a,by,S,c,rids);S2=wide(P['responses'],c,rids);hb,_,_=w1(b,by,S2,c,rids)
 if ha!=hb or open(a,'rb').read()!=open(b,'rb').read():die('INVALID__REPLAY_OR_INTEGRITY_FAILURE')
 # W5: full-profile-country collapse then all 255 subset marginalizations.
 pc=collections.Counter((tuple(S[r]),c[r]) for r in rids);cnt=collections.Counter();idx={m:[i for i in range(8) if m>>i&1] for m in range(1,256)}
 for (f,cc),n in pc.items():
  for m,ii in idx.items():cnt[(m,tuple(f[i] for i in ii),cc)]+=n
 h5=hash_from_counts(R,cnt)
 # W4: explicit membership lists, then country join.
 c4=collections.Counter();members=0
 for m,ps in by.items():
  ii=idx[m];M=collections.defaultdict(list)
  for rid in rids:M[tuple(S[rid][i] for i in ii)].append(rid)
  for p in ps:
   rr=M[p[6]];members+=len(rr)
   if len(rr)!=p[5]:die('INVALID__REPLAY_OR_INTEGRITY_FAILURE')
   for rid in rr:c4[(m,p[6],c[rid])]+=1
 h4=hash_from_counts(R,c4)
 # W3: exact Q1 sufficient statistic after target, then reconstruct target from summary counts.
 q=O/'ffp036_w3_q1_sufficient_statistic.tsv';qcnt={}
 with open(a,'rt',newline='') as f,open(q,'w',newline='\n') as o:
  rd=csv.DictReader(f,delimiter='\t');o.write('predicate_id\tCOUNTRY_ALPHA3\tcountry_support\tstatus\n')
  for r in rd:o.write(f"{r['predicate_id']}\t{r['COUNTRY_ALPHA3']}\t{r['country_support']}\t{r['status']}\n");qcnt[(r['predicate_id'],r['COUNTRY_ALPHA3'])]=int(r['country_support'])
 h=hashlib.sha256();h.update(line(TH))
 for p in R:
  for cc in C:
   n=qcnt[(p[0],cc)];h.update(line([*p[:6],cc,n,'OBSERVED_POSITIVE' if n else 'OBSERVED_ZERO']))
 h3=h.hexdigest()
 if len({ha,h3,h4,h5})!=1:die('INVALID__REPLAY_OR_INTEGRITY_FAILURE')
 dg(a,O/'ffp036_canonical_oracle_target.tsv.gz');dg(q,O/'ffp036_w3_q1_sufficient_statistic.tsv.gz')
 # W5 bankable wide state surface.
 w=O/'w5.tsv'
 with open(w,'w',newline='\n') as o:
  o.write('\t'.join(['respondent_local_id','COUNTRY_ALPHA3']+V)+'\n')
  for rid in rids:o.write('\t'.join([rid,c[rid]]+S[rid])+'\n')
 dg(w,O/'ffp036_w5_full_state_surface.tsv.gz')
 print(json.dumps({'terminal':'PASS__DISCOVERY_FOLLOWUP_GENUINE_EXECUTION_COMPLETE__FROZEN_W0_W5_EVIDENCE_BANKED__NO_ARCHITECTURE_VERDICT','oracle_sha256':ha,'positive_cells':pos,'zero_cells':zero,'W3':h3,'W4':h4,'W5':h5,'W4_membership_rows':members,'W2_AS06':'UNDEFINED_FOR_OBJECT','W0_AS07':'INCOMPLETE__CANNOT_INDEPENDENTLY_REGENERATE_AS07','W6':'EXCLUDED__NO_PREOUTPUT_FUSION_TRIGGER'},sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=3:die('usage: ffp036_execute.py INPUT_DIR OUTPUT_DIR')
 main(sys.argv[1],sys.argv[2])
