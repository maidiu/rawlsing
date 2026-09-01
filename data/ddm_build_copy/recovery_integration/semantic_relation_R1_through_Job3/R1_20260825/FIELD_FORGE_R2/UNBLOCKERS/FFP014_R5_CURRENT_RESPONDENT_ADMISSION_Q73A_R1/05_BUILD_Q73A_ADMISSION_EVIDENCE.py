#!/usr/bin/env python3
"""FFP014 bounded Q73A respondent-admission evidence builder.

Reuses the byte-validated FFP008 SPSS decoder and respondent identity rule, but does
NOT import or execute the unresolved Q73D paid-employment exposure mapping. Q73A
exposure is computed only from its exact C04 country predicate. Response facts are
serialized independently from exposure facts so response presence/missingness cannot
participate in the exposure result.
"""
from __future__ import annotations
import argparse, csv, gzip, hashlib, importlib.util, io, json, sys
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
SOURCE_BYTES = 49_689_458
SOURCE_ROWS = 51_587
BASE_MEMBER_SHA256 = "f55741a53a4caed3f74980afba2488233caa93dd4f1a2edcfde8d90e2fcce4be"
BASE_MEMBER_ROWS = 51_587
RECON_SCRIPT_SHA256 = "ca0afd16475d9cabfbcac8b09ad68612c8ced680a3bb3051f9b1ea8a828ce774"
QIMPL = "question_impl.phase0.cae005624221d7b00dd2"
MEASUREMENT = "Afrobarometer:R5:Q73A"
PREDICATE_ID = "C04P.b651b9af6671a2fe1166"
PREDICATE = "COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}"
CURRENT_CARRIER_ID = "sha256:6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5"
EXCLUDED = frozenset({"ALG", "EGY", "MRC", "SUD", "TUN"})
EXPECTED_EXCLUDED_COUNTRY_TOKEN = {31:"ALG", 32:"EGY", 33:"MRC", 34:"SUD", 35:"TUN"}


def sha256_file(path: Path):
    h=hashlib.sha256(); n=0
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''):
            h.update(b); n += len(b)
    return h.hexdigest(), n


def cjson(o):
    return json.dumps(o, sort_keys=True, separators=(",",":"), ensure_ascii=False)


def deterministic_gzip(path: Path, payload: bytes):
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as gz:
            gz.write(payload)


def load_recon(path: Path):
    got,_ = sha256_file(path)
    if got != RECON_SCRIPT_SHA256:
        raise RuntimeError(f"reconstruction script hash mismatch: {got}")
    spec=importlib.util.spec_from_file_location('ffp008_recon_exact', path)
    mod=importlib.util.module_from_spec(spec); sys.modules[spec.name]=mod; spec.loader.exec_module(mod)
    return mod


def evaluate_q73a(alpha, known_tokens):
    if alpha is None or alpha not in known_tokens:
        return 'UNRESOLVED', 'EXPOSURE__UNRESOLVED'
    pred = alpha not in EXCLUDED
    return ('TRUE' if pred else 'FALSE'), ('EXPOSED__PROVED' if pred else 'NONEXPOSURE__PROVED')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source', required=True, type=Path)
    ap.add_argument('--base-carrier', required=True, type=Path)
    ap.add_argument('--recon-script', required=True, type=Path)
    ap.add_argument('--out-dir', required=True, type=Path)
    a=ap.parse_args(); a.out_dir.mkdir(parents=True, exist_ok=True)

    sh,sb=sha256_file(a.source)
    if (sh,sb)!=(SOURCE_SHA256,SOURCE_BYTES): raise RuntimeError('source byte identity mismatch')
    bh,_=sha256_file(a.base_carrier)
    if bh != BASE_MEMBER_SHA256: raise RuntimeError('base carrier member hash mismatch')
    m=load_recon(a.recon_script)

    base={}
    with gzip.open(a.base_carrier,'rt',encoding='utf-8',newline='') as f:
        r=csv.DictReader(f,delimiter='\t')
        for x in r:
            k=(int(x['COUNTRY']),x['RESPNO'])
            if k in base: raise RuntimeError(f'duplicate carrier key {k}')
            base[k]=x
    if len(base)!=BASE_MEMBER_ROWS: raise RuntimeError('base carrier row count mismatch')

    reader=m.SavReader(a.source)
    if reader.header.ncases != SOURCE_ROWS: raise RuntimeError('source row count mismatch')
    rows=[]; source_keys=set(); prefixes=defaultdict(set); qcounts=Counter(); expcounts=Counter(); expq=Counter()
    for s in reader.rows(('COUNTRY','RESPNO','Q73A')):
        country=int(s['COUNTRY']); respno=str(s['RESPNO']); key=(country,respno)
        if key in source_keys: raise RuntimeError(f'duplicate source key {key}')
        source_keys.add(key)
        b=base.get(key)
        if b is None: raise RuntimeError(f'source key absent from admitted base member {key}')
        alpha=b['COUNTRY_ALPHA3']; prefix=respno[:3]
        if alpha != prefix: raise RuntimeError(f'COUNTRY_ALPHA3 != RESPNO source token for {key}')
        prefixes[country].add(prefix)
        local_id=m.respondent_local_id(country,respno)
        q=s['Q73A']
        if q is None: qtok='SYSTEM_MISSING'
        elif isinstance(q,float) and q.is_integer(): qtok=str(int(q))
        else: qtok=str(q)
        rows.append((country,respno,local_id,alpha,qtok))
    if source_keys != set(base): raise RuntimeError('source/carrier key set mismatch')
    if any(len(v)!=1 for v in prefixes.values()): raise RuntimeError('COUNTRY -> RESPNO alpha token not functional')
    for c,tok in EXPECTED_EXCLUDED_COUNTRY_TOKEN.items():
        if prefixes.get(c)!={tok}: raise RuntimeError(f'excluded COUNTRY token mismatch {c}: {prefixes.get(c)}')
    known_tokens={next(iter(v)) for v in prefixes.values()}
    evaluated=[]
    for country,respno,local_id,alpha,qtok in rows:
        pred_state, exposure=evaluate_q73a(alpha, known_tokens)
        pred = True if pred_state=='TRUE' else False if pred_state=='FALSE' else None
        qcounts[qtok]+=1; expcounts[exposure]+=1; expq[(exposure,qtok)]+=1
        evaluated.append((country,respno,local_id,alpha,qtok,pred,exposure))
    rows=sorted(evaluated,key=lambda z:(z[0],z[1]))
    hostile_unknown=evaluate_q73a(None, known_tokens)
    if hostile_unknown != ('UNRESOLVED','EXPOSURE__UNRESOLVED'):
        raise RuntimeError('hostile unresolved input coercion')

    # independent response facts: deliberately omit predicate/exposure fields
    rs=io.StringIO(newline=''); rw=csv.writer(rs,delimiter='\t',lineterminator='\n')
    rw.writerow(['respondent_carrier_identity','COUNTRY','RESPNO','respondent_local_id','empirical_measurement_id','Q73A_source_state'])
    # exposure execution: deliberately omit response state
    es=io.StringIO(newline=''); ew=csv.writer(es,delimiter='\t',lineterminator='\n')
    ew.writerow(['respondent_carrier_identity','COUNTRY','RESPNO','respondent_local_id','question_implementation_id','empirical_measurement_id','predicate_id','COUNTRY_ALPHA3','predicate_result','exposure_state'])
    response_root=hashlib.sha256(); exposure_root=hashlib.sha256()
    for country,respno,lid,alpha,q,pred,exp in rows:
        rw.writerow([CURRENT_CARRIER_ID,country,respno,lid,MEASUREMENT,q])
        ew.writerow([CURRENT_CARRIER_ID,country,respno,lid,QIMPL,MEASUREMENT,PREDICATE_ID,alpha,'TRUE' if pred else 'FALSE' if pred is False else 'UNRESOLVED',exp])
        response_root.update((cjson({'empirical_measurement_id':MEASUREMENT,'respondent_carrier_identity':CURRENT_CARRIER_ID,'respondent_local_id':lid,'source_key':{'COUNTRY':country,'RESPNO':respno},'response_state':q})+'\n').encode())
        exposure_root.update((cjson({'empirical_measurement_id':MEASUREMENT,'respondent_carrier_identity':CURRENT_CARRIER_ID,'exposure_state':exp,'predicate_id':PREDICATE_ID,'predicate_input':{'COUNTRY_ALPHA3':alpha},'predicate_result':pred,'question_implementation_id':QIMPL,'respondent_local_id':lid,'source_key':{'COUNTRY':country,'RESPNO':respno}})+'\n').encode())
    response_path=a.out_dir/'q73a_response_binding.tsv.gz'; deterministic_gzip(response_path,rs.getvalue().encode())
    exposure_path=a.out_dir/'q73a_exposure_execution.tsv.gz'; deterministic_gzip(exposure_path,es.getvalue().encode())
    rh,rb=sha256_file(response_path); eh,eb=sha256_file(exposure_path)

    first_sub=next(z for z in rows if z[5] and z[4] in ('0','1'))
    first_non=next(z for z in rows if not z[5])
    first_missing=next(z for z in rows if z[5] and z[4] not in ('0','1'))
    def witness(z):
        c,r,l,a,q,p,e=z
        return {'source_key':{'COUNTRY':c,'RESPNO':r},'respondent_local_id':l,'COUNTRY_ALPHA3':a,'Q73A_source_state':q,'predicate_result':p,'exposure_state':e}

    receipt={
      'status':'PASS__Q73A_BOUNDED_EXECUTION_EVIDENCE',
      'respondent_carrier_identity':CURRENT_CARRIER_ID,
      'source':{'sha256':sh,'bytes':sb,'rows':SOURCE_ROWS},
      'base_carrier_member':{'sha256':bh,'rows':len(base)},
      'reconstruction_code':{'sha256':RECON_SCRIPT_SHA256},
      'admission_evidence_builder':{'sha256':sha256_file(Path(__file__).resolve())[0]},
      'respondent_identity':{'key_fields':['COUNTRY','RESPNO'],'unique_keys':len(source_keys),'duplicate_keys':0,'row_order_is_identity':False,'local_id_rule':"sha256(canonical_json({source_family:'Afrobarometer',wave:'R5',COUNTRY:<int>,RESPNO:<exact source string>}))"},
      'qimpl_measurement_binding':{'qimpl':QIMPL,'empirical_measurement_id':MEASUREMENT,'source_variable':'Q73A'},
      'predicate':{'predicate_id':PREDICATE_ID,'compiled':PREDICATE,'only_input_symbol':'COUNTRY_ALPHA3'},
      'predicate_input_proof':{'derivation':'first 3 exact characters of governed source RESPNO; exhaustively functional against governed source COUNTRY over the complete source/carrier key set','observed_country_values':len(prefixes),'excluded_country_value_to_exact_source_token':EXPECTED_EXCLUDED_COUNTRY_TOKEN,'scope_ceiling':'Afrobarometer R5 Q73A routing only; not a global country ontology'},
      'execution_counts':dict(sorted(expcounts.items())),
      'response_state_counts':dict(sorted(qcounts.items())),
      'exposure_by_response_state':{f'{a}|{b}':v for (a,b),v in sorted(expq.items())},
      'independent_response_binding':{'path':response_path.name,'sha256':rh,'bytes':rb,'semantic_sorted_root_sha256':response_root.hexdigest(),'response_does_not_participate_in_exposure':True},
      'exposure_execution':{'path':exposure_path.name,'sha256':eh,'bytes':eb,'semantic_sorted_root_sha256':exposure_root.hexdigest(),'predicate_true_entails':'EXPOSED__PROVED','predicate_false_entails':'NONEXPOSURE__PROVED','basis':'Q73A C04 administration predicate is the exact source not-asked/asked condition'},
      'witnesses':{'first_exposed_substantive_after_nonidentity_sort':witness(first_sub),'first_nonexposed_after_nonidentity_sort':witness(first_non),'missing_response_but_exposed_hostile_witness':witness(first_missing)},
      'hostile_assertions':{'response_missingness_used_for_exposure':False,'source_and_carrier_key_sets_identical':True,'country_token_functional':True,'excluded_country_tokens_exact':True,'neighboring_wave_used':False,'row_order_identity_used':False,'q73d_exposure_consumed':False,'unresolved_predicate_input_yields_unresolved': hostile_unknown==('UNRESOLVED','EXPOSURE__UNRESOLVED')}
    }
    out=a.out_dir/'q73a_execution_receipt.json'; out.write_text(cjson(receipt)+'\n',encoding='utf-8')
    print(cjson(receipt))

if __name__=='__main__': main()
