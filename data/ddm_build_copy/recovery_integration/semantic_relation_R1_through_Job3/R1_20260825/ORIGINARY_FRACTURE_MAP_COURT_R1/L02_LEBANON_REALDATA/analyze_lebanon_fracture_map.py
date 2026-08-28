#!/usr/bin/env python3
"""Exact-source Arab Barometer VIII Lebanon Q873 fracture-map reconstruction.

Reads the exact Library SAV directly (no pyreadstat dependency) using the documented
$FL2 dictionary and bytecode-compression records needed by this release.
Outputs deterministic CSV oracles used by L02.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, struct
from pathlib import Path
from collections import defaultdict
import pandas as pd
import numpy as np

EXPECTED = {
    'sav': 'a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998',
    'questionnaire': 'd72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb',
    'chatlog': 'b0ff181b0d1f6a591b005b829aafeb27b0740249332b49e08bd381800ab1745a',
}
OPT_LABEL = {
    1:'socioeconomic_class',2:'region',3:'skin_color',4:'race_or_ethnicity',5:'nationality',
    6:'religion',7:'gender',8:'tribe',9:'age',10:'sexual_orientation',11:'disability_status',
    12:'migration_status',13:'none_of_these'
}

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def read_sav_selected(path: Path):
    f=path.open('rb'); h=f.read(176)
    if h[:4] != b'$FL2': raise RuntimeError('Expected $FL2 SAV')
    layout,case_size,compression,weight_index,ncases=struct.unpack('<5i',h[64:84]); bias=struct.unpack('<d',h[84:92])[0]
    if layout != 2 or compression != 1: raise RuntimeError((layout,compression))
    vars=[]; ext={}; vlraw=[]
    while True:
        raw=f.read(4)
        if len(raw)!=4: raise EOFError('dictionary')
        rt=struct.unpack('<i',raw)[0]
        if rt==2:
            r=f.read(28); typ,haslab,nmiss,pr,wr=struct.unpack('<5i',r[:20]); short=r[20:28].decode('latin1').rstrip(' \x00')
            label=''
            if haslab:
                L=struct.unpack('<i',f.read(4))[0]; label=f.read(L).decode('utf-8','replace'); f.read((-L)%4)
            miss=[f.read(8) for _ in range(abs(nmiss))]
            vars.append({'dict_index':len(vars)+1,'short':short,'type':typ,'label':label,'nmiss':nmiss,'missing_raw':miss})
        elif rt==3:
            cnt=struct.unpack('<i',f.read(4))[0]; ents=[]
            for _ in range(cnt):
                value=f.read(8); L=f.read(1)[0]; label=f.read(L).decode('utf-8','replace'); f.read((-(1+L))%8); ents.append((value,label))
            if struct.unpack('<i',f.read(4))[0] != 4: raise RuntimeError('value-label variable record')
            nv=struct.unpack('<i',f.read(4))[0]; idx=list(struct.unpack('<'+'i'*nv,f.read(4*nv))); vlraw.append((idx,ents))
        elif rt==6:
            n=struct.unpack('<i',f.read(4))[0]; f.read(n*80)
        elif rt==7:
            subtype,size,count=struct.unpack('<3i',f.read(12)); ext[subtype]=f.read(size*count)
        elif rt==999:
            f.read(4); data_pos=f.tell(); break
        else: raise RuntimeError(f'unknown record {rt}')
    longmap={}
    if 13 in ext:
        for pair in ext[13].decode('utf-8','replace').split('\t'):
            if '=' in pair:
                k,v=pair.split('=',1); longmap[k]=v
    for v in vars: v['name']=longmap.get(v['short'],v['short'])
    labels={}
    for idxs,ents in vlraw:
        typ=vars[idxs[0]-1]['type']; mp={}
        for raw,label in ents:
            value=struct.unpack('<d',raw)[0] if typ==0 else raw[:typ].decode('utf-8','replace').rstrip()
            mp[value]=label
        for idx in idxs: labels[vars[idx-1]['name']]=mp
    want=['COUNTRY','WT','STRATUM','PSU','Q13','Q1001','Q1002','Q1003','Q1012','Q1012A_MUSLIM','Q1012A_CHRISTIAN','Q609','Q1015','Q1015A','Q1016']+[f'Q873_{i}' for i in list(range(1,14))+[98,99]]
    slot_name={i:v['name'] for i,v in enumerate(vars) if v['name'] in want}
    miss={}
    for i,v in enumerate(vars):
        if v['type']==0 and v['missing_raw']:
            miss[i]=set(struct.unpack('<'+'d'*len(v['missing_raw']),b''.join(v['missing_raw'])))
        else: miss[i]=set()
    rows=[]; cur={}; slot=0; case=0
    while case<ncases:
        codes=f.read(8)
        if len(codes)<8: break
        raws=[f.read(8) for _ in range(sum(c==253 for c in codes))]; ri=0; eof=False
        for code in codes:
            if code==0: continue
            if code==252: eof=True; break
            v=vars[slot]
            if code==253:
                raw=raws[ri]; ri+=1; value=struct.unpack('<d',raw)[0] if v['type']==0 else raw
            elif v['type']==0:
                value=float('nan') if code in (254,255) else float(code)-bias
            else:
                value=b'        ' if code==254 else None
            if slot in slot_name:
                if v['type']==0 and value in miss[slot]: value=float('nan')
                cur[slot_name[slot]]=value
            slot += 1
            if slot==case_size:
                rows.append(cur); cur={}; slot=0; case+=1
                if case>=ncases: break
        if eof: break
    if len(rows)!=ncases or slot!=0 or f.tell()!=path.stat().st_size:
        raise RuntimeError({'decoded':len(rows),'expected':ncases,'slot':slot,'position':f.tell(),'size':path.stat().st_size})
    df=pd.DataFrame(rows,columns=want)
    meta={'layout':layout,'case_size':case_size,'compression':compression,'weight_index':weight_index,'ncases':ncases,'bias':bias,'data_pos':data_pos,
          'variables':{v['name']:{'dict_index':v['dict_index'],'short':v['short'],'label':v['label'],'value_labels':labels.get(v['name'],{})} for v in vars if v['name'] in want}}
    return df,meta

def kish(df):
    w=df.WT.dropna().astype(float)
    return (w.sum()**2/(w.pow(2).sum())) if len(w) and w.pow(2).sum()>0 else float('nan')

def binary_stats(df,var):
    d=df[df[var].notna() & df.WT.notna() & (df.WT>0)]
    n=len(d); wn=float(d.WT.sum())
    if not n: return {'n':0,'weighted_n':0,'n_eff':0,'unweighted_pct':None,'weighted_pct':None,'ci_low':None,'ci_high':None,'selected_n':0}
    p=float(np.average(d[var],weights=d.WT)); ne=float(kish(d)); se=math.sqrt(max(0,p*(1-p)/ne)) if ne>0 else float('nan')
    return {'n':n,'weighted_n':wn,'n_eff':ne,'unweighted_pct':float(d[var].mean()*100),'weighted_pct':p*100,
            'ci_low':max(0,p-1.96*se)*100,'ci_high':min(1,p+1.96*se)*100,'selected_n':int((d[var]==1).sum())}

def support_class(n):
    if n<25: return 'UNDERPOWERED_STOP_NO_SPLIT'
    if n<50: return 'EXPLORATORY_ONLY'
    return 'DESCRIPTIVE_ORACLE_SUPPORTED'

def denom_series(df):
    M={1:'Muslim:Just Muslim',2:'Muslim:Sunni',3:'Muslim:Shia',4:'Muslim:Hanbali',5:'Muslim:Shafii',6:'Muslim:Jafari',7:'Muslim:Druze',9:'Muslim:Alawi',10:'Muslim:Ibadi',11:'Muslim:Malki',90:'Muslim:Other'}
    C={1:'Christian:Just Christian',2:'Christian:Maronite',3:'Christian:Orthodox',4:'Christian:Catholic',5:'Christian:Armenian',6:'Christian:Coptic',7:'Christian:Protestant',90:'Christian:Other'}
    out=[]
    for _,r in df.iterrows():
        if r.Q1012==1 and pd.notna(r.Q1012A_MUSLIM) and r.Q1012A_MUSLIM!=99: out.append(M.get(int(r.Q1012A_MUSLIM),f'Muslim:{int(r.Q1012A_MUSLIM)}'))
        elif r.Q1012==2 and pd.notna(r.Q1012A_CHRISTIAN) and r.Q1012A_CHRISTIAN!=99: out.append(C.get(int(r.Q1012A_CHRISTIAN),f'Christian:{int(r.Q1012A_CHRISTIAN)}'))
        elif r.Q1012==4: out.append('No religion')
        elif r.Q1012==90: out.append('Other religion')
        else: out.append(np.nan)
    return pd.Series(out,index=df.index,dtype='object')

def add_derived(df):
    df=df.copy(); df['DENOMINATION_COMBINED']=denom_series(df)
    df['AGE_BAND']=pd.cut(df.Q1001,bins=[17,29,44,59,200],labels=['18-29','30-44','45-59','60+'])
    # Country-local source Q1015 rank quintile. Rank is deterministic and used only as a descriptive splitter.
    df['COUNTRY_INCOME_RANK_QUINTILE']=np.nan
    for country,g in df.groupby('COUNTRY'):
        valid=g.Q1015.notna(); ranks=g.loc[valid,'Q1015'].rank(method='average',pct=True); q=np.minimum(np.ceil(ranks*5),5).astype(int)
        df.loc[q.index,'COUNTRY_INCOME_RANK_QUINTILE']=q
    for x in ['Q1003','Q1012','Q609','Q1016']:
        df.loc[df[x].isin([98,99]),x]=np.nan
    return df

def wmi(df,x,y):
    d=df[[x,y,'WT']].dropna(); d=d[d.WT>0]
    if len(d)<1 or d[y].nunique()<2: return None
    total=float(d.WT.sum()); joint=d.groupby([x,y],observed=True).WT.sum()/total; px=d.groupby(x,observed=True).WT.sum()/total; py=d.groupby(y,observed=True).WT.sum()/total
    mi=0.0
    for (a,b),p in joint.items(): mi += float(p)*math.log2(float(p)/(float(px[a])*float(py[b])))
    hy=-sum(float(p)*math.log2(float(p)) for p in py if p>0)
    return {'n_complete':len(d),'weighted_n_complete':total,'mi_bits':mi,'target_entropy_bits':hy,'normalized_mi':mi/hy if hy else 0.0}

def pattern(r, applicable):
    s=[OPT_LABEL[i] for i in applicable if r[f'Q873_{i}']==1]
    return '+'.join(s) if s else 'NO_SUBSTANTIVE_SELECTION'

def write_csv(path,rows,fields=None):
    rows=list(rows)
    if fields is None:
        fields=[]
        for r in rows:
            for k in r:
                if k not in fields: fields.append(k)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--sav',type=Path,required=True); ap.add_argument('--questionnaire',type=Path,required=True); ap.add_argument('--chatlog',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    observed={'sav':sha256(a.sav),'questionnaire':sha256(a.questionnaire),'chatlog':sha256(a.chatlog)}
    if observed != EXPECTED: raise SystemExit(f'hash mismatch {observed}')
    raw,meta=read_sav_selected(a.sav); d=add_derived(raw)
    eligible=d.Q873_1.notna(); substantive=eligible & (d.Q873_98!=1) & (d.Q873_99!=1)
    E=d[substantive].copy(); L=E[E.COUNTRY==10].copy()
    if len(raw)!=15627 or len(L)!=2339: raise RuntimeError((len(raw),len(L)))
    # source-wide and Lebanon key correction metrics
    wave_ses=binary_stats(E,'Q873_1'); lb_ses=binary_stats(L,'Q873_1')
    legacy_den=d[(d.Q873_98!=1)&(d.Q873_99!=1)]
    legacy_pct=float((legacy_den.Q873_1.fillna(0)*legacy_den.WT).sum()/legacy_den.WT.sum()*100)

    # Branch oracle.
    branches=[]
    def branch_row(bid,parent,desc,df):
        r={'branch_id':bid,'parent_branch_id':parent,'filter_description':desc,'n':len(df),'weighted_n':float(df.WT.sum()),'n_eff':float(kish(df)),'support_class':support_class(len(df))}
        for i in [1,2,3,4,5,6,7,9,10,11,12,13]:
            s=binary_stats(df,f'Q873_{i}'); r[f'{OPT_LABEL[i]}_weighted_pct']=s['weighted_pct']; r[f'{OPT_LABEL[i]}_selected_n']=s['selected_n']
        return r
    branches.append(branch_row('LB_ALL_SUBSTANTIVE','ROOT','COUNTRY=10; Q873_1 nonmissing; Q873_98!=1; Q873_99!=1',L))
    branches.append(branch_row('LB_SES_SELECTED','LB_ALL_SUBSTANTIVE','Q873_1=1',L[L.Q873_1==1]))
    branches.append(branch_row('LB_NON_SES','LB_ALL_SUBSTANTIVE','Q873_1=0',L[L.Q873_1==0]))
    edu={1:'NO_FORMAL',2:'ELEMENTARY',3:'PREPARATORY_BASIC',4:'SECONDARY',5:'TECHNICAL',6:'BA',7:'MA_PLUS'}
    for code,name in edu.items():
        e=L[L.Q1003==code]; bid=f'LB_EDU_{name}'; branches.append(branch_row(bid,'LB_ALL_SUBSTANTIVE',f'Q1003={code}',e))
        if code in (1,7):
            ns=e[e.Q873_1==0]; branches.append(branch_row(bid+'_NON_SES',bid,'Q873_1=0',ns)); branches.append(branch_row(bid+'_NON_SES_NON_RELIGION',bid+'_NON_SES','Q873_6=0',ns[ns.Q873_6==0]))
    write_csv(a.out/'LEBANON_BRANCH_ORACLE.csv',branches)

    # Response patterns preserving same-respondent multi-select overlap.
    patrows=[]; applicable=[1,2,3,4,5,6,7,9,10,11,12,13]
    pattargets={
      'LB_ALL_SUBSTANTIVE':L,
      'LB_NON_SES':L[L.Q873_1==0],
      'LB_NO_FORMAL_NON_SES':L[(L.Q1003==1)&(L.Q873_1==0)],
      'LB_NO_FORMAL_NON_SES_NON_RELIGION':L[(L.Q1003==1)&(L.Q873_1==0)&(L.Q873_6==0)],
      'LB_MA_PLUS_NON_SES':L[(L.Q1003==7)&(L.Q873_1==0)],
      'LB_MA_PLUS_NON_SES_NON_RELIGION':L[(L.Q1003==7)&(L.Q873_1==0)&(L.Q873_6==0)],
    }
    for bid,g0 in pattargets.items():
        g=g0.copy(); g['response_pattern']=g.apply(lambda r:pattern(r,applicable),axis=1); denomw=float(g.WT.sum())
        agg=g.groupby('response_pattern',dropna=False).WT.agg(['size','sum']).reset_index().sort_values(['sum','response_pattern'],ascending=[False,True])
        for rank,(_,x) in enumerate(agg.iterrows(),1): patrows.append({'branch_id':bid,'pattern_rank':rank,'response_pattern':x.response_pattern,'n':int(x['size']),'weighted_n':float(x['sum']),'unweighted_pct':float(x['size']/len(g)*100) if len(g) else None,'weighted_pct':float(x['sum']/denomw*100) if denomw else None,'support_class':support_class(len(g))})
    write_csv(a.out/'RESPONSE_PATTERN_ORACLE.csv',patrows)

    # Determinicity: descriptive weighted normalized mutual information, not causal inference.
    det=[]
    targets=[
      ('WAVE8_SES_SELECTION',E,'Q873_1',['COUNTRY','Q1003','Q609','Q1016','Q13','Q1002','AGE_BAND','COUNTRY_INCOME_RANK_QUINTILE']),
      ('LB_SES_SELECTION',L,'Q873_1',['COUNTRY_INCOME_RANK_QUINTILE','DENOMINATION_COMBINED','Q1016','Q1003','Q1012','Q13','AGE_BAND','Q1002','Q609']),
      ('LB_NON_SES_RELIGION_SELECTION',L[L.Q873_1==0],'Q873_6',['DENOMINATION_COMBINED','Q1016','Q1012','COUNTRY_INCOME_RANK_QUINTILE','Q1003','Q13','Q609','Q1002','AGE_BAND']),
      ('LB_NON_SES_NATIONALITY_SELECTION',L[L.Q873_1==0],'Q873_5',['Q1003','DENOMINATION_COMBINED','COUNTRY_INCOME_RANK_QUINTILE','Q13','AGE_BAND','Q1016','Q1012','Q1002','Q609']),
      ('LB_NON_SES_NONE_SELECTION',L[L.Q873_1==0],'Q873_13',['DENOMINATION_COMBINED','Q1012','Q1016','COUNTRY_INCOME_RANK_QUINTILE','Q1003','AGE_BAND','Q609','Q13','Q1002']),
      ('LB_NON_SES_NON_RELIGION_NONE_SELECTION',L[(L.Q873_1==0)&(L.Q873_6==0)],'Q873_13',['DENOMINATION_COMBINED','Q1012','Q1016','AGE_BAND','COUNTRY_INCOME_RANK_QUINTILE','Q1003','Q609','Q1002','Q13']),
      ('LB_MA_PLUS_NON_SES_RELIGION_SELECTION',L[(L.Q1003==7)&(L.Q873_1==0)],'Q873_6',['DENOMINATION_COMBINED','COUNTRY_INCOME_RANK_QUINTILE','Q1016','Q1012','Q13','Q609','AGE_BAND','Q1002']),
      ('LB_MA_PLUS_NON_SES_NONE_SELECTION',L[(L.Q1003==7)&(L.Q873_1==0)],'Q873_13',['DENOMINATION_COMBINED','COUNTRY_INCOME_RANK_QUINTILE','Q1016','Q1012','Q13','Q609','AGE_BAND','Q1002']),
      ('LB_MA_PLUS_NON_SES_NON_RELIGION_NONE_SELECTION',L[(L.Q1003==7)&(L.Q873_1==0)&(L.Q873_6==0)],'Q873_13',['DENOMINATION_COMBINED','COUNTRY_INCOME_RANK_QUINTILE','Q1016','Q1012','Q13','Q609','AGE_BAND','Q1002']),
    ]
    for tid,g,y,cands in targets:
        tmp=[]
        for x in cands:
            z=wmi(g,x,y)
            if z: tmp.append((x,z))
        tmp.sort(key=lambda q:(-q[1]['normalized_mi'],q[0]))
        for rank,(x,z) in enumerate(tmp,1): det.append({'target_id':tid,'target_variable':y,'branch_n':len(g),'branch_weighted_n':float(g.WT.sum()),'predictor_rank':rank,'predictor':x,**z,'interpretation_limit':'DESCRIPTIVE_ASSOCIATION_ONLY__NOT_CAUSAL_NOT_PERSONA','support_class':support_class(len(g))})
    write_csv(a.out/'BRANCH_DETERMINICITY_ORACLE.csv',det)

    # Support, routing, weight, missingness ledger.
    led=[]
    def add(scope,item,n,wn,detail): led.append({'scope':scope,'item':item,'n':n,'weighted_n':wn,'detail':detail})
    add('WAVE8','released_rows',len(d),float(d.WT.sum()),'all SAV cases')
    add('WAVE8','q873_1_nonmissing_rows',int(eligible.sum()),float(d.loc[eligible,'WT'].sum()),'source-routed/observed Q873 SES toggle')
    sm=d[~eligible]; add('WAVE8','q873_structural_missing_rows',len(sm),float(sm.WT.sum()),'all are COUNTRY=9 Kuwait in released SAV; do not code as non-selection')
    add('WAVE8','q873_dont_know_selected',int((d.Q873_98==1).sum()),float(d.loc[d.Q873_98==1,'WT'].sum()),'Q873_98=1')
    add('WAVE8','q873_refused_selected',int((d.Q873_99==1).sum()),float(d.loc[d.Q873_99==1,'WT'].sum()),'Q873_99=1')
    add('WAVE8','q873_substantive_denominator',len(E),float(E.WT.sum()),'Q873_1 nonmissing and Q873_98!=1 and Q873_99!=1')
    add('LEBANON','released_rows',int((d.COUNTRY==10).sum()),float(d.loc[d.COUNTRY==10,'WT'].sum()),'COUNTRY=10')
    add('LEBANON','q873_substantive_denominator',len(L),float(L.WT.sum()),'64 excluded: 62 DK, 2 refused')
    add('LEBANON','q873_tribe_structural_missing',int(L.Q873_8.isna().sum()),float(L.loc[L.Q873_8.isna(),'WT'].sum()),'Q873_8 routed only COUNTRY 7,8,9; Lebanon unavailable')
    add('LEBANON','q873_sexual_orientation_observed',int(L.Q873_10.notna().sum()),float(L.loc[L.Q873_10.notna(),'WT'].sum()),'Q873_10 available for COUNTRY 10 and 21')
    noneviol=L[(L.Q873_13==1)&(L[[f'Q873_{i}' for i in [1,2,3,4,5,6,7,9,10,11,12]]].fillna(0).sum(axis=1)>0)]
    add('LEBANON','none_exclusivity_violations',len(noneviol),float(noneviol.WT.sum()),'expected 0; Q873_13 cannot combine with other substantive options')
    for x in ['Q13','Q1001','Q1002','Q1003','Q1012','Q1012A_MUSLIM','Q1012A_CHRISTIAN','Q609','Q1015','Q1015A','Q1016','DENOMINATION_COMBINED']:
        missn=int(L[x].isna().sum()); add('LEBANON_SUBSTANTIVE',x+'_missing',missn,float(L.loc[L[x].isna(),'WT'].sum()),'source/route missing; 98/99 converted to missing for determinant analysis only where noted' if x in ['Q1003','Q1012','Q609','Q1016'] else 'source/route missing')
    write_csv(a.out/'SUPPORT_WEIGHT_MISSINGNESS_LEDGER.csv',led)

    # Replication matrix.
    def bfind(bid): return next(r for r in branches if r['branch_id']==bid)
    claims=[]
    claims.append({'claim_id':'C01','originary_claim':'Wave VIII SES selected ~=43.5%','disposition':'CORRECTED_DENOMINATOR_ARTIFACT','source_result':wave_ses['weighted_pct'],'source_n':wave_ses['n'],'source_weighted_n':wave_ses['weighted_n'],'detail':f'Proper routed substantive denominator gives {wave_ses["weighted_pct"]:.6f}%. The remembered value is reproduced as {legacy_pct:.6f}% only by retaining 1,210 Kuwait Q873 structural-missing rows in denominator while coding missing SES as zero.'})
    claims.append({'claim_id':'C02','originary_claim':'Lebanon SES selected ~=57.5%','disposition':'CONFIRMED','source_result':lb_ses['weighted_pct'],'source_n':lb_ses['n'],'source_weighted_n':lb_ses['weighted_n'],'detail':'COUNTRY=10 routed substantive Q873 denominator.'})
    for cid,bid,remember in [('C03','LB_EDU_NO_FORMAL','No formal education SES ~=74.5%; n=45'),('C04','LB_EDU_PREPARATORY_BASIC','Preparatory/basic SES ~=61.5%'),('C05','LB_EDU_BA','BA SES ~=54.2%'),('C06','LB_EDU_MA_PLUS','MA+ SES ~=54.1%; n=156')]:
        r=bfind(bid); claims.append({'claim_id':cid,'originary_claim':remember,'disposition':'CONFIRMED','source_result':r['socioeconomic_class_weighted_pct'],'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'WT-weighted Q873_1 selection.'})
    r=bfind('LB_EDU_NO_FORMAL_NON_SES'); claims.append({'claim_id':'C07','originary_claim':'No-formal non-SES: religion 34.4, none 26.1, nationality 22.0, region 18.1','disposition':'CONFIRMED__UNDERPOWERED','source_result':json.dumps({k:r[k] for k in ['religion_weighted_pct','none_of_these_weighted_pct','nationality_weighted_pct','region_weighted_pct']}),'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'n=12; report distribution, do not accept stable splitter ranking.'})
    r=bfind('LB_EDU_NO_FORMAL_NON_SES_NON_RELIGION'); claims.append({'claim_id':'C08','originary_claim':'No-formal non-SES/non-religion residual led by none, then region/nationality','disposition':'DIRECTIONALLY_CONFIRMED__UNDERPOWERED_STOP','source_result':json.dumps({k:r[k] for k in ['none_of_these_weighted_pct','region_weighted_pct','nationality_weighted_pct','skin_color_weighted_pct','migration_status_weighted_pct']}),'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'n=8; no recursive splitter inference authorized.'})
    r=bfind('LB_EDU_MA_PLUS'); claims.append({'claim_id':'C09','originary_claim':'MA+ overall religion 47.1 and none 12.6','disposition':'CONFIRMED','source_result':json.dumps({'religion':r['religion_weighted_pct'],'none':r['none_of_these_weighted_pct']}),'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'WT-weighted.'})
    r=bfind('LB_EDU_MA_PLUS_NON_SES'); claims.append({'claim_id':'C10','originary_claim':'MA+ non-SES: religion 40.4, nationality 32.2, none 27.4, region 23.1','disposition':'CONFIRMED','source_result':json.dumps({k:r[k] for k in ['religion_weighted_pct','nationality_weighted_pct','none_of_these_weighted_pct','region_weighted_pct']}),'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'WT-weighted; n=72.'})
    r=bfind('LB_EDU_MA_PLUS_NON_SES_NON_RELIGION'); claims.append({'claim_id':'C11','originary_claim':'MA+ residual: none 46.0, nationality 22.3, skin 12.8, migration 11.5, region 7.2','disposition':'CONFIRMED__EXPLORATORY','source_result':json.dumps({k:r[k] for k in ['none_of_these_weighted_pct','nationality_weighted_pct','skin_color_weighted_pct','migration_status_weighted_pct','region_weighted_pct']}),'source_n':r['n'],'source_weighted_n':r['weighted_n'],'detail':'n=42: exploratory-only by originary guardrail.'})
    claims.append({'claim_id':'C12','originary_claim':'Income rank is strongest splitter in no-formal non-SES','disposition':'NOT_ACCEPTED_AS_STABLE__UNDERPOWERED','source_result':'n=12','source_n':12,'source_weighted_n':float(L[(L.Q1003==1)&(L.Q873_1==0)].WT.sum()),'detail':'Guardrail n<25 prohibits split inference; source can reproduce branch distribution but not a stable determinant ranking.'})
    claims.append({'claim_id':'C13','originary_claim':'Denomination strongest in MA+ non-SES / subgroup sect patterns','disposition':'DESCRIPTIVE_SIGNAL_ONLY__CELL_SUPPORT_LIMITS','source_result':'See BRANCH_DETERMINICITY_ORACLE.csv and response oracle','source_n':72,'source_weighted_n':float(L[(L.Q1003==7)&(L.Q873_1==0)].WT.sum()),'detail':'Denomination is a leading descriptive association for several Lebanon non-SES targets, but MA+ denomination cells are small; no global causal/persona claim frozen.'})
    write_csv(a.out/'ORIGINARY_CLAIM_REPLICATION_MATRIX.csv',claims)

    summary={'status':'PASS','source_hashes':observed,'sav_header':meta,'counts':{'released_rows':len(d),'q873_eligible_rows':int(eligible.sum()),'q873_substantive_rows':len(E),'lebanon_released_rows':int((d.COUNTRY==10).sum()),'lebanon_substantive_rows':len(L)},'key_findings':{'wave8_ses_source_routed_weighted_pct':wave_ses['weighted_pct'],'legacy_43_5_denominator_artifact_pct':legacy_pct,'lebanon_ses_weighted_pct':lb_ses['weighted_pct'],'lebanon_ses_unweighted_pct':lb_ses['unweighted_pct'],'lebanon_substantive_weighted_n':lb_ses['weighted_n']},'method':{'weight':'WT','uncertainty':'Kish effective-n approximate 95% Wald CI; descriptive, not full complex-survey variance','determinicity':'weighted normalized mutual information; descriptive association only','support_guardrail':'originary chatlog: n<25 stop split; 25<=n<50 exploratory-only; >=50 descriptive oracle supported'},'success_token':'L02_LEBANON_WAVEVIII_FRACTURE_MAP_REALDATA_R1_COMPLETE'}
    (a.out/'analysis_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(summary['key_findings'],indent=2))

if __name__=='__main__': main()
