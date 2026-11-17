#!/usr/bin/env python3
"""Analytical pre-build elimination evidence guard.

A passing structural result is a reviewable candidate proof, not a theorem, a
comparator winner, a scientifically authorized result or an independent C decision.
No implementation of an eliminated competitor is required to prepare this proof.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys
from r7_decision import digest, sha, ishash, H40

BAD=('todo','tbd','placeholder','just assume','probably slower','not yet implemented',
     'missing rival benchmark','no B code','competitor has not been built')


def _substantive(value, min_length=48):
    return (isinstance(value,str) and len(value.strip())>=min_length
            and not any(term in value.lower() for term in BAD))


def check(proof, frozen, evidence_root, source_root):
    errors=[]
    if not isinstance(proof,dict) or not isinstance(frozen,dict):
        return {'status':'RED','errors':['ANALYTICAL_BAD_INPUT']}
    if proof.get('schema')!='ANVIL_R7_ANALYTICAL_ELIMINATION':errors.append('ANALYTICAL_BAD_SCHEMA')
    if proof.get('frozen_sha256')!=digest(frozen):errors.append('ANALYTICAL_NOT_FROZEN_SCOPE')
    if proof.get('source_cut')!=frozen.get('source_cut') or proof.get('scope')!=frozen.get('scope'):
        errors.append('ANALYTICAL_SOURCE_OR_SCOPE_DRIFT')
    candidate=proof.get('eliminated_candidate')
    if candidate not in ('A','B'):errors.append('ANALYTICAL_BAD_ELIMINATED_CANDIDATE')
    elif proof.get('candidate_code_head')!=frozen.get('candidate_code_heads',{}).get(candidate):
        errors.append('ANALYTICAL_CANDIDATE_CODE_UNPINNED')
    if proof.get('proof_type') not in {'CONTRACT_CONTRADICTION','PROVEN_RESOURCE_LOWER_BOUND',
                                      'SOURCE_SEMANTIC_IMPOSSIBILITY','EXISTING_ABI_IMPOSSIBILITY'}:
        errors.append('ANALYTICAL_UNQUALIFIED_PROOF_TYPE')
    for field in ('necessary_capability','unavoidable_contradiction', 'first_consumer_effect',
                  'source_semantic_negative_or_restoration', 'strongest_surviving_reverser',
                  'how_an_independent_reviewer_can_disprove'):
        if not _substantive(proof.get(field)):
            errors.append('ANALYTICAL_MISSING_SUBSTANTIVE_'+field)
    if proof.get('requires_competitor_implementation') is not False:
        errors.append('ANALYTICAL_COMPETITOR_BAKEOFF_NOT_ELIMINATION')
    if proof.get('proposes_unconditional_winner') is not False:
        errors.append('ANALYTICAL_SELF_AWARDED_WINNER')
    refs=proof.get('premises')
    if not isinstance(refs,list) or len(refs)<2:
        errors.append('ANALYTICAL_NEEDS_TWO_INDEPENDENT_PREMISES');refs=[]
    keys=set();classes=set()
    ev=pathlib.Path(evidence_root).resolve() if evidence_root else None
    src=pathlib.Path(source_root).resolve() if source_root else None
    if src is None or not (src/'.git').exists():
        errors.append('ANALYTICAL_REQUIRES_EXACT_REAL_CODE_CHECKOUT')
    else:
        try:
            actual=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL,timeout=5).strip()
            if actual!=proof.get('candidate_code_head'):
                errors.append('ANALYTICAL_CHECKOUT_NOT_FROZEN_CANDIDATE_HEAD')
        except (OSError,subprocess.SubprocessError):errors.append('ANALYTICAL_UNVERIFIED_GIT_HEAD')
    for item in refs:
        if not isinstance(item,dict):errors.append('ANALYTICAL_BAD_PREMISE');continue
        kind=item.get('kind');rel=item.get('path');expected=item.get('sha256');exact=item.get('exact_excerpt')
        if kind not in ('FROZEN_CONTRACT','CANDIDATE_CODE','CALCULATED_BOUND'):
            errors.append('ANALYTICAL_INVALID_PREMISE_KIND');continue
        if not isinstance(rel,str) or not rel or '\\' in rel or rel.startswith('/') or '..' in pathlib.PurePosixPath(rel).parts:
            errors.append('ANALYTICAL_UNSAFE_PREMISE_PATH');continue
        if (kind,rel) in keys:errors.append('ANALYTICAL_DUPLICATE_PREMISE')
        keys.add((kind,rel));classes.add(kind)
        if not ishash(expected):errors.append('ANALYTICAL_PREMISE_HASH_MISSING');continue
        base=src if kind=='CANDIDATE_CODE' else ev
        if base is None:errors.append('ANALYTICAL_MISSING_PREMISE_ROOT');continue
        fp=(base/rel).resolve()
        if not fp.is_relative_to(base) or not fp.is_file() or fp.is_symlink():
            errors.append('ANALYTICAL_PREMISE_FILE_MISSING_OR_ESCAPED');continue
        by=fp.read_bytes()
        if sha(by)!=expected:errors.append('ANALYTICAL_PREMISE_HASH_MISMATCH');continue
        if not _substantive(exact,20) or exact.encode('utf-8') not in by:
            errors.append('ANALYTICAL_PREMISE_EXCERPT_NOT_IN_PINNED_BYTES')
        if kind=='CANDIDATE_CODE':
            try:
                committed=subprocess.check_output(['git','-C',str(src),'show','HEAD:'+rel],stderr=subprocess.DEVNULL,timeout=5)
                if committed!=by:errors.append('ANALYTICAL_CANDIDATE_FILE_NOT_COMMITTED_AT_HEAD')
            except (OSError,subprocess.SubprocessError):errors.append('ANALYTICAL_CANDIDATE_FILE_NOT_AT_HEAD')
    if not {'FROZEN_CONTRACT','CANDIDATE_CODE'}<=classes:
        errors.append('ANALYTICAL_NO_INDEPENDENT_CONTRACT_AND_CODE_PREMISES')
    if proof.get('proof_type')=='PROVEN_RESOURCE_LOWER_BOUND':
        bound=proof.get('lower_bound')
        if not isinstance(bound,dict) or any(type(bound.get(x)) is not int or bound[x]<1 for x in ('minimum_items','minimum_bytes_per_item','ceiling_bytes')):
            errors.append('ANALYTICAL_LOWER_BOUND_INVALID')
        elif bound['minimum_items']*bound['minimum_bytes_per_item']<=bound['ceiling_bytes']:
            errors.append('ANALYTICAL_LOWER_BOUND_DOES_NOT_EXCEED_HARD_CEILING')
        elif bound['ceiling_bytes']!=6442450944:
            errors.append('ANALYTICAL_LOWER_BOUND_NOT_BOUND_TO_6GIB')
    return {'status':'RED' if errors else 'PROVISIONAL_ANALYTICAL_ELIMINATION__C_MUST_AUTHENTICATE_AND_ADJUDICATE',
            'errors':sorted(set(errors)), 'eliminated_candidate':candidate if not errors else None,
            'winner':None,'proof_grade':'EXACT_BYTES_AND_LOCAL_GIT_ONLY__NOT_AUTHENTICATED_OWNER_OR_C'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('proof');ap.add_argument('frozen')
    ap.add_argument('--evidence-root',required=True);ap.add_argument('--source-root',required=True)
    args=ap.parse_args()
    try:
        res=check(json.loads(pathlib.Path(args.proof).read_text()),json.loads(pathlib.Path(args.frozen).read_text()),
                  args.evidence_root,args.source_root)
    except (OSError,ValueError,TypeError,KeyError) as e:
        res={'status':'RED','errors':['ANALYTICAL_INVALID_INPUT:'+str(e)]}
    print(json.dumps(res,indent=2));return 2 if res['status']=='RED' else 0

if __name__=='__main__':sys.exit(main())
