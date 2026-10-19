"""Bounded read-only recovery of the exact HQ261 P1 retained public objects.

Full identity-bearing arrays stay in ignored local runtime. No raw survey,
native query execution, semantic decision or source permission is created.
"""
import argparse
import gzip
import hashlib
import json
import mmap
from pathlib import Path
import resource
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path.insert(0,str(REPO))
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.fiabc_final_oracle_freeze_producers import _hydrate_lits_canonical_preimage


def hash_span(mm,start,end):
    h=hashlib.sha256()
    for i in range(start,end,8*1024*1024):h.update(mm[i:min(end,i+8*1024*1024)])
    return h.hexdigest()


def verify_document(checkpoint,freeze):
    h=hashlib.sha256();size=0
    with checkpoint.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk);size+=len(chunk)
    if size!=3404445161 or h.hexdigest()!=freeze['document_sha256']:
        raise ValueError('retained checkpoint identity mismatch')
    return size,h.hexdigest()


def public_document(mm,array_start,digest,family):
    end_limit=mm.find(b',"comparison_fact_manifest":',array_start)
    if end_limit<0:raise ValueError('selected public closure boundary missing')
    needle=b'"content_hash":"'+digest.encode()+b'"'
    pos=array_start
    while True:
        found=mm.find(needle,pos,end_limit)
        if found<0:raise ValueError('expected selected public preimage missing')
        start=mm.rfind(b'{"authority_snapshot_refs":',array_start,found)
        if start<0:raise ValueError('selected public preimage header missing')
        # A fact ref inside another object's body is not its public identity.
        if mm.find(b'"content_hash":',start,found)>=0:
            pos=found+len(needle)
            continue
        end=mm.find(b',"typed_state":',found,end_limit)
        if end<0:raise ValueError('selected public preimage terminal missing')
        end=mm.find(b'}',end)+1
        if end-start>256*1024*1024:raise ValueError('selected preimage exceeds bounded read budget')
        doc=json.loads(mm[start:end])
        if doc.get('content_hash')==digest and doc.get('schema_id')==family:return doc
        pos=found+len(needle)


def recover(checkpoint):
    freeze=json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    size,digest=verify_document(checkpoint,freeze)
    out=HERE/'.runtime/continuation/p1';out.mkdir(parents=True,exist_ok=True)
    receipt={'scope':'EXACT_HQ261_RETAINED_P1_ONLY__NO_NEW_SOURCE_EXECUTION',
             'document_sha256':digest,'document_bytes':size,'facts':[]}
    with checkpoint.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
        marker=b'"canonical_empirical_object_closure":'
        start=mm.find(marker)+len(marker)
        if start<len(marker):raise ValueError('canonical closure missing')
        end=mm.find(b',"comparison_fact_manifest":',start)
        if end<0:raise ValueError('canonical closure boundary missing')
        omit=b',"closure_identity":"'+freeze['closure_sha256'].encode()+b'"'
        cut=mm.find(omit,start,end)
        if cut<0:raise ValueError('canonical closure identity field missing')
        closure_h=hashlib.sha256()
        for lo,hi in [(start,cut),(cut+len(omit),end)]:
            for i in range(lo,hi,8*1024*1024):closure_h.update(mm[i:min(hi,i+8*1024*1024)])
        if closure_h.hexdigest()!=freeze['closure_sha256']:
            raise ValueError('canonical closure content identity mismatch')
        receipt['closure_identity_recomputed']=closure_h.hexdigest()
        array_start=mm.find(b'"public_object_preimages":[',start,end)
        if array_start<0:raise ValueError('public preimage array missing')
        for role,spec in freeze['facts'].items():
            packed=public_document(mm,array_start,spec['hash'],'EmpiricalFact')
            needed=set()
            def collect(v):
                if isinstance(v,dict):
                    if set(v)=={'$canonical_preimage_fragment'}:needed.add(v['$canonical_preimage_fragment'])
                    else:
                        for x in v.values():collect(x)
                elif isinstance(v,list):
                    for x in v:collect(x)
            collect(packed);fragments={}
            for digest in sorted(needed):
                prefix=b'{"fragment_hash":"'+digest.encode()+b'","value":'
                lo=mm.find(prefix,start,array_start)
                if lo<0:raise ValueError('selected fragment missing')
                lo+=len(prefix)
                tail=mm.find(b'},{"fragment_hash":',lo,array_start)
                if tail<0:tail=mm.rfind(b'}],"public_object_preimages":',lo,array_start+64)
                if tail<0 or tail-lo>256*1024*1024:raise ValueError('fragment boundary or budget refusal')
                raw=mm[lo:tail]
                if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('exact selected fragment bytes mismatch')
                fragments[digest]=json.loads(raw)
            doc=_hydrate_lits_canonical_preimage(packed,fragments)
            obj=materialize_public_object(doc)
            if obj.ref.content_hash!=spec['hash']:raise ValueError('native selected Fact identity mismatch')
            if obj.raw_denominator_support!=spec['raw_denominator']:raise ValueError('selected original support mismatch')
            with gzip.open(out/(role+'.json.gz'),'wt',encoding='utf-8') as target:
                json.dump(doc,target,ensure_ascii=False,separators=(',',':'),sort_keys=True)
            receipt['facts'].append({'role':role,'fact_ref':obj.ref.as_dict(),
                                     'typed_state':obj.typed_state,'raw_denominator_support':obj.raw_denominator_support,
                                     'query_ref':canonicalize(obj.empirical_query_spec_ref),
                                     'selected_fragment_hashes':sorted(needed),
                                     'native_materialization':'EXACT_IDENTITY_VERIFIED'})
            del doc,obj,packed,fragments
        receipt['max_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (HERE/'evidence/continuation_p1_native_objects.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def recover_support(checkpoint):
    """Recover only P1's required retained receipt/authority, not other results."""
    import re
    freeze=json.loads((HERE/'evidence/CONTINUATION_P1_FREEZE.json').read_text())
    verify_document(checkpoint,freeze)
    with checkpoint.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
        closure=mm.find(b'"canonical_empirical_object_closure":')
        end=mm.find(b',"comparison_fact_manifest":',closure)
        if closure<0 or end<0:raise ValueError('selected canonical closure missing')
        array=mm.find(b'"public_object_preimages":[',closure,end)
        if array<0:raise ValueError('selected public preimage array missing')
        at=mm.find(b'"candidate_hash":"'+freeze['candidate_hash'].encode()+b'"',array,end)
        if at<0:raise ValueError('exact P1 receipt candidate identity missing')
        start=mm.rfind(b'{"authority_snapshot_refs":',array,at)
        match=re.search(b'"content_hash":"([0-9a-f]{64})"',mm[start:start+8192])
        if match is None:raise ValueError('exact P1 receipt public identity missing')
        receipt=public_document(mm,array,match.group(1).decode(),'DiscoveryResultReceipt')
        obj=materialize_public_object(receipt)
        if obj.candidate_identity.get('candidate_hash')!=freeze['candidate_hash']:
            raise ValueError('selected receipt candidate substitution')
        refs={r['content_hash'] for r in [*obj.empirical_fact_refs,*obj.validation_fact_refs]}
        if refs!={r['hash'] for r in freeze['facts'].values()}:
            raise ValueError('selected receipt fact closure mismatch')
        authority=public_document(mm,array,obj.discovery_authority_ref['content_hash'],'DiscoveryAuthority')
        materialize_public_object(authority)
    result={'receipt':receipt,'discovery_authority':authority}
    (HERE/'evidence/continuation_p1_support_preimages.json').write_text(json.dumps(result,indent=2)+'\n')
    return {'receipt_ref':obj.ref.as_dict(),'expected_facts':sorted(refs)}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--checkpoint',type=Path,required=True)
    parser.add_argument('--support-only',action='store_true');args=parser.parse_args()
    if args.support_only:print(json.dumps(recover_support(args.checkpoint)))
    else:
        result=recover(args.checkpoint)
        print(json.dumps({'exact_native_facts':len(result['facts']),'closure_identity':result['closure_identity_recomputed'],
                          'max_rss_bytes':result['max_rss_bytes'],'raw_reads':0}))
