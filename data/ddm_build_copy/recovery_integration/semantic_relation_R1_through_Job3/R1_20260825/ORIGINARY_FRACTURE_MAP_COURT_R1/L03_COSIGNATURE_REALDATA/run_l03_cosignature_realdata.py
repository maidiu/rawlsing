#!/usr/bin/env python3
"""Exact L03 Wave-VIII Lebanon branch/co-signature replay. Descriptive, non-causal."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,struct
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency,chi2

SAV_SHA='a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998'
CB_SHA='328bbbbfa6cb8a78eacad52847b1432a56a81ec9ecfcd4f18754e05532afd4fc'
HEADER=(2,692,1,15627,100.0,176848)
VALID={
 'Q511':list(range(11)),'Q512':list(range(11)),'Q533_4':[1,2,3,4],
 'Q601_3':[1,2,3,4],'Q601_4':[1,2,3,4],'Q605':[1,2,3,4,5],
 'Q606_2':[1,2,3,4],'Q606_4':[1,2,3,4],'Q885':[1,2,3,97],
 'Q201A_1':[1,2,3,4],'Q201A_3':[1,2,3,4],'Q606_8':[1,2,3,4],'Q631':[1,2,3,4],'Q867B':[1,2,3]}
SCREEN=['Q885','Q605','Q533_4','Q511','Q601_3','Q512','Q601_4','Q606_2','Q606_4']
PAIRS=[('P001','Q201A_1','Q601_4'),('P002','Q511','Q601_4'),('P003','Q606_4','Q867B'),('P004','Q512','Q631'),('P005','Q606_4','Q606_8')]
TRIPLES=[('H01',('Q201A_3','Q606_2','Q606_8')),('H02',('Q606_2','Q606_4','Q601_4')),('H03',('Q533_4','Q606_8','Q631'))]
LABEL={
 'Q885':'government action on discrimination','Q605':"laws based on sharia versus people's will",
 'Q533_4':'leader may bend rules to get things done','Q511':'extent country is democratic',
 'Q601_3':'men better at political leadership','Q512':'democracy appropriate for country',
 'Q601_4':'male university education more important','Q606_2':'better off with religious people in public positions',
 'Q606_4':'religious practice private/separate from socio-economic life',
 'Q201A_3':'trust elected council/parliament','Q606_8':'religious leaders as likely corrupt as non-religious leaders',
 'Q201A_1':'trust government','Q631':"women political leaders advance women's rights agenda",'Q867B':"children's lives better/same/worse than respondent's life"}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dictionary(b):
 if b[:4]!=b'$FL2': raise ValueError('not SPSS $FL2')
 layout,case_size,compression,weight,ncases=struct.unpack_from('<5i',b,64); bias=struct.unpack_from('<d',b,84)[0]
 off=176; slots=[]
 while True:
  t=struct.unpack_from('<i',b,off)[0]
  if t==2:
   _,vtype,has_label,missing,_,_=struct.unpack_from('<6i',b,off); name=b[off+24:off+32].decode('latin1').rstrip(' \0'); off+=32
   if has_label:
    n=struct.unpack_from('<i',b,off)[0]; off+=4+((n+3)//4)*4
   off+=8*(abs(missing) if missing else 0); slots.append(name if vtype==0 else None)
  elif t==3:
   n=struct.unpack_from('<i',b,off+4)[0]; off+=8
   for _ in range(n):
    off+=8; z=b[off]; off+=1+z; off+=(-(1+z))%8
   if struct.unpack_from('<i',b,off)[0]!=4: raise ValueError('bad value-label linkage')
   nv=struct.unpack_from('<i',b,off+4)[0]; off+=8+4*nv
  elif t==6: off+=8+80*struct.unpack_from('<i',b,off+4)[0]
  elif t==7:
   _,size,count=struct.unpack_from('<3i',b,off+4); off+=16+size*count
  elif t==999: return dict(layout=layout,case_size=case_size,compression=compression,weight=weight,ncases=ncases,bias=bias,slots=slots,data_offset=off+8)
  else: raise ValueError(f'unsupported dictionary record {t} at {off}')

def decode(b,m):
 names=[x for x in m['slots'] if x is not None]; out=np.full((m['ncases'],len(names)),np.nan); pos=m['data_offset']; ci=si=ni=0; cmds=b''; j=8
 while ci<m['ncases']:
  if j>=8:
   cmds=b[pos:pos+8]; pos+=8; j=0
   if len(cmds)!=8: raise EOFError('truncated command block')
  c=cmds[j]; j+=1
  if c==0: continue
  if c==252: raise EOFError('premature EOF command')
  numeric=m['slots'][si] is not None; v=np.nan
  if c==253:
   raw=b[pos:pos+8]; pos+=8
   if len(raw)!=8: raise EOFError('truncated raw value')
   if numeric: v=struct.unpack('<d',raw)[0]
  elif c not in (254,255) and numeric: v=float(c)-m['bias']
  if numeric: out[ci,ni]=v; ni+=1
  si+=1
  if si==len(m['slots']):
   if ni!=len(names): raise ValueError('slot drift')
   ci+=1; si=ni=0
 if pos!=len(b): raise ValueError(f'decoder ended {pos}, source ends {len(b)}')
 return pd.DataFrame(out,columns=names),dict(decoded_cases=ci,retained_numeric_variables=len(names),final_offset=pos)

def eligible(df,v,mask): return mask & df[v].isin(VALID[v])
def dist(df,v,mask):
 x=df.loc[eligible(df,v,mask),[v,'WT']]; g=x.groupby(v).WT.sum().reindex(VALID[v],fill_value=0.0); return g/g.sum(),len(x),float(g.sum())
def js(s): return json.dumps({str(int(k)):round(float(v),12) for k,v in s.items()},sort_keys=True,separators=(',',':'))
def tv(a,b): return float(.5*np.abs(a-b).sum())
def digest(df,mask):
 ids=sorted(int(x) for x in df.loc[mask,'ID']); payload=''.join(f'{x}\n' for x in ids).encode(); return hashlib.sha256(payload).hexdigest()
def cramers(df,a,b,mask):
 e=eligible(df,a,mask)&df[b].isin(VALID[b]); t=pd.crosstab(df.loc[e,a],df.loc[e,b]); n=int(t.values.sum()); x=float(chi2_contingency(t,correction=False)[0]); return math.sqrt(x/n/min(t.shape[0]-1,t.shape[1]-1)),n

def triple(df,vars,mask):
 a,b,c=vars; e=eligible(df,a,mask)&df[b].isin(VALID[b])&df[c].isin(VALID[c]); cats=[VALID[a],VALID[b],VALID[c]]; maps=[{v:i for i,v in enumerate(q)} for q in cats]; obs=np.zeros(tuple(map(len,cats)))
 for x in df.loc[e,[a,b,c]].itertuples(index=False,name=None): obs[maps[0][x[0]],maps[1][x[1]],maps[2][x[2]]]+=1
 ab,ac,bc=obs.sum(2),obs.sum(1),obs.sum(0); exp=np.ones_like(obs)*obs.sum()/obs.size
 for _ in range(10000):
  old=exp.copy()
  for axes,target in [((0,1),ab),((0,2),ac),((1,2),bc)]:
   summed=exp.sum(axis=tuple(i for i in range(3) if i not in axes)); ratio=np.divide(target,summed,out=np.ones_like(target),where=summed>0)
   if axes==(0,1): exp*=ratio[:,:,None]
   elif axes==(0,2): exp*=ratio[:,None,:]
   else: exp*=ratio[None,:,:]
  if np.max(np.abs(exp-old))<1e-12: break
 err=max(np.abs(exp.sum(2)-ab).max(),np.abs(exp.sum(1)-ac).max(),np.abs(exp.sum(0)-bc).max()); nz=obs>0; g2=float(2*np.sum(obs[nz]*np.log(obs[nz]/exp[nz]))); dfree=(obs.shape[0]-1)*(obs.shape[1]-1)*(obs.shape[2]-1); n=int(obs.sum()); resid=obs-exp; ix=np.unravel_index(np.argmax(np.abs(resid)),obs.shape); cell='|'.join(str(cats[d][ix[d]]) for d in range(3))
 return dict(n=n,g2=g2,df=dfree,p=float(chi2.sf(g2,dfree)),joint_tv=float(.5*np.abs(obs/n-exp/n).sum()),margin_error=float(err),cell=cell,observed=float(obs[ix]),expected=float(exp[ix]),residual=float(resid[ix]))

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--sav',type=Path,required=True); ap.add_argument('--codebook',type=Path,required=True); ap.add_argument('--out-dir',type=Path,required=True); a=ap.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True)
 if sha(a.sav)!=SAV_SHA or sha(a.codebook)!=CB_SHA: raise ValueError('source hash mismatch')
 b=a.sav.read_bytes(); m=dictionary(b)
 got=(m['layout'],m['case_size'],m['compression'],m['ncases'],m['bias'],m['data_offset'])
 if got!=HEADER: raise ValueError(f'header mismatch {got}')
 df,receipt=decode(b,m); lb=df[df.COUNTRY.eq(10)].copy(); branch=lb.Q873_1.eq(1); comp=lb.Q873_1.eq(0); overall=branch|comp
 if (len(lb),lb.ID.nunique(),int(branch.sum()),int(comp.sum()))!=(2403,2403,1334,1069): raise ValueError('Lebanon/branch identity mismatch')
 rows=[]
 rows.append(dict(kind='BRANCH',variable='Q873_1',label='selected socioeconomic class as one perceived basis of discrimination',branch_n=1334,comparison_n=1069,tv_branch_complement='',tv_branch_overall='',branch_distribution=digest(lb,branch),comparison_distribution=digest(lb,comp),holding='EXACT_RESPONSE_BRANCH_MEMBERSHIP'))
 for v in SCREEN:
  pb,nb,_=dist(lb,v,branch); pc,nc,_=dist(lb,v,comp); po,no,_=dist(lb,v,overall)
  rows.append(dict(kind='MARGINAL',variable=v,label=LABEL[v],branch_n=nb,comparison_n=nc,tv_branch_complement=tv(pb,pc),tv_branch_overall=tv(pb,po),branch_distribution=js(pb),comparison_distribution=js(pc),holding='BRANCH_CONDITIONED_EMPIRICAL_MORPHOLOGY'))
 demos={'FEMALE_Q1002_EQ_2':lb.Q1002.eq(2),'AGE_18_29_Q1001':lb.Q1001.between(18,29),'NO_FORMAL_EDUCATION_Q1003_EQ_1':lb.Q1003.eq(1),'MA_PLUS_Q1003_EQ_7':lb.Q1003.eq(7)}
 for name,mask in demos.items():
  rows.append(dict(kind='PREDICTOR',variable=name,label='demographic conditioner; not attitude node',branch_n=int(mask.sum()),comparison_n='',tv_branch_complement='',tv_branch_overall='',branch_distribution=float((branch&mask).sum()/mask.sum()),comparison_distribution='',holding='PREDICTOR_REMAINS_OUTSIDE_ATTITUDE_ONTOLOGY'))
  for v in ('Q605','Q601_4','Q606_4'):
   pb,nb,_=dist(lb,v,branch); pdemo,nd,_=dist(lb,v,mask)
   rows.append(dict(kind='PREDICTOR_RESPONSE_CONTRAST',variable=f'{name}|{v}',label=f'demographic conditioner contrast on {LABEL[v]}',branch_n=nb,comparison_n=nd,tv_branch_complement=tv(pb,pdemo),tv_branch_overall='',branch_distribution=js(pb),comparison_distribution=js(pdemo),holding='PREDICTOR_COHORT_DOES_NOT_DEFINE_RESPONSE_BRANCH'))
 with (a.out_dir/'REALDATA_BRANCH_COSIGNATURE_ORACLE.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n'); w.writeheader(); w.writerows(rows)
 scopes={'SES_DISCRIMINATION_BRANCH_Q873_1_EQ_1':branch,'COMPLEMENT_Q873_1_EQ_0':comp,'LEBANON_OVERALL':overall}; out=[]
 for case_id,x,y in PAIRS:
  for scope,mask in scopes.items():
   v,n=cramers(lb,x,y,mask); out.append(dict(case_id=case_id,case_type='PAIRWISE',variables=f'{x}|{y}',scope=scope,n=n,metric='CRAMERS_V',value=v,df='',p='',joint_tv='',pairwise_margin_error='',largest_cell='',observed='',expected='',residual='',holding='PAIR_RELATION_IS_BRANCH_CONDITIONED'))
 for case_id,vars in TRIPLES:
  for scope,mask in scopes.items():
   r=triple(lb,vars,mask); out.append(dict(case_id=case_id,case_type='THREE_WAY_PAIRWISE_INFORMATION_LOSS',variables='|'.join(vars),scope=scope,n=r['n'],metric='G2_NO_THREEWAY_INTERACTION',value=r['g2'],df=r['df'],p=r['p'],joint_tv=r['joint_tv'],pairwise_margin_error=r['margin_error'],largest_cell=r['cell'],observed=r['observed'],expected=r['expected'],residual=r['residual'],holding='ALL_PAIRWISE_MARGINS_MATCH_BUT_THREEWAY_JOINT_DIFFERS'))
 with (a.out_dir/'PAIRWISE_VS_BRANCH_CONDITIONED_MATRIX.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n'); w.writeheader(); w.writerows(out)
 print(json.dumps({'sav_sha256':SAV_SHA,'codebook_sha256':CB_SHA,'decode':receipt,'lebanon_n':len(lb),'branch_n':int(branch.sum()),'complement_n':int(comp.sum()),'branch_id_sha256':digest(lb,branch),'complement_id_sha256':digest(lb,comp)},sort_keys=True))
if __name__=='__main__': main()
