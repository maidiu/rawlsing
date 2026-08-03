#!/usr/bin/env python3
"""Build Rawlsing P2 global cross-source reconciliation tranche 1.

Read-only over a v11/v12 cumulative handoff root. Produces a governed exact-
and-structural foundation, not J-family authority or respondent-level output.
"""
from __future__ import annotations
import argparse, collections, csv, hashlib, itertools, json, math, os, pathlib, re, shutil, sys, zipfile, io
from difflib import SequenceMatcher
from typing import Iterable
import pandas as pd
import yaml

SOURCES = ['GSS','WVS','EVS','Arab Barometer','Afrobarometer','Asian Barometer','Latinobarómetro','South Asia','LiTS']
CATALOGS = {
'GSS':'09_P2_GSS_PASS1/Rawlsing_P2_GSS_Deep_Question_Node_Catalog_v1.csv',
'WVS':'10_P2_WVS_PASS1/Rawlsing_P2_WVS_Deep_Question_Node_Catalog_v1.csv',
'EVS':'12_P2_EVS_PASS1/Rawlsing_P2_EVS_Deep_Question_Node_Catalog_v1.csv',
'Arab Barometer':'15_P2_ARAB_BAROMETER_PASS1/Rawlsing_P2_Arab_Barometer_Deep_Question_Node_Catalog_v1.csv',
'Afrobarometer':'19_P2_AFROBAROMETER_PASS1/Rawlsing_P2_Afrobarometer_Deep_Question_Node_Catalog_v1.csv',
'Asian Barometer':'24_P2_ASIAN_BAROMETER_PASS1/PACKAGE_CONTENTS/01_DEEP_NODE_CATALOG/Rawlsing_P2_Asian_Barometer_Deep_Question_Node_Catalog_v2.csv',
'Latinobarómetro':'25_P2_LATINOBAROMETRO_PASS1/PACKAGE_CONTENTS/01_DEEP_NODE_CATALOG/Rawlsing_P2_Latinobarometro_Deep_Question_Node_Catalog_v2.csv',
'South Asia':'26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/01_DEEP_NODE_CATALOG/Rawlsing_P2_South_Asia_Deep_Question_Node_Catalog_v2.csv',
'LiTS':'27_P2_LITS_PASS1/PACKAGE_CONTENTS/01_DEEP_NODE_CATALOG/Rawlsing_P2_LiTS_Deep_Question_Node_Catalog_v2.csv'}
EDGES = {
'GSS':'09_P2_GSS_PASS1/Rawlsing_P2_GSS_Accepted_Longitudinal_Continuity_Edges_v1.csv',
'WVS':'10_P2_WVS_PASS1/Rawlsing_P2_WVS_Accepted_Longitudinal_Continuity_Edges_v1.csv',
'EVS':'12_P2_EVS_PASS1/Rawlsing_P2_EVS_Accepted_Longitudinal_Continuity_Edges_v1.csv',
'Arab Barometer':'15_P2_ARAB_BAROMETER_PASS1/Rawlsing_P2_Arab_Barometer_Accepted_Longitudinal_Continuity_Edges_v1.csv',
'Afrobarometer':'19_P2_AFROBAROMETER_PASS1/Rawlsing_P2_Afrobarometer_Accepted_Longitudinal_Continuity_Edges_v1.csv',
'Asian Barometer':'24_P2_ASIAN_BAROMETER_PASS1/PACKAGE_CONTENTS/02_WITHIN_SOURCE_CONTINUITY/Rawlsing_P2_Asian_Barometer_Accepted_Longitudinal_Continuity_Edges_v2.csv',
'Latinobarómetro':'25_P2_LATINOBAROMETRO_PASS1/PACKAGE_CONTENTS/02_WITHIN_SOURCE_CONTINUITY/Rawlsing_P2_Latinobarometro_Accepted_Longitudinal_Continuity_Edges_v2.csv',
'South Asia':'26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/02_WITHIN_SOURCE_CONTINUITY/Rawlsing_P2_South_Asia_Accepted_Longitudinal_Continuity_Edges_v2.csv',
'LiTS':'27_P2_LITS_PASS1/PACKAGE_CONTENTS/02_WITHIN_SOURCE_CONTINUITY/Rawlsing_P2_LiTS_Accepted_Longitudinal_Continuity_Edges_v2.csv'}
STRUCT_INV = {
'GSS':'09_P2_GSS_PASS1/Rawlsing_P2_GSS_Source_Structure_Inventory_v1.csv',
'WVS':'10_P2_WVS_PASS1/Rawlsing_P2_WVS_Source_Structure_Inventory_v1.csv',
'EVS':'12_P2_EVS_PASS1/Rawlsing_P2_EVS_Source_Structure_Inventory_v1.csv',
'Arab Barometer':'15_P2_ARAB_BAROMETER_PASS1/Rawlsing_P2_Arab_Barometer_Source_Structure_Inventory_v1.csv',
'Afrobarometer':'19_P2_AFROBAROMETER_PASS1/Rawlsing_P2_Afrobarometer_Source_Structure_Inventory_v1.csv',
'Asian Barometer':'24_P2_ASIAN_BAROMETER_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_Asian_Barometer_Source_Structure_Inventory_v2.csv',
'Latinobarómetro':'25_P2_LATINOBAROMETRO_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_Latinobarometro_Source_Structure_Inventory_v2.csv',
'South Asia':'26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_South_Asia_Source_Structure_Inventory_v2.csv',
'LiTS':'27_P2_LITS_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_LiTS_Source_Structure_Inventory_v2.csv'}
STRUCT_MEM = {
'Afrobarometer':'19_P2_AFROBAROMETER_PASS1/Rawlsing_P2_Afrobarometer_Source_Structure_Memberships_v1.csv',
'Asian Barometer':'24_P2_ASIAN_BAROMETER_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_Asian_Barometer_Source_Structure_Memberships_v2.csv',
'Latinobarómetro':'25_P2_LATINOBAROMETRO_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_Latinobarometro_Source_Structure_Memberships_v2.csv',
'South Asia':'26_P2_SOUTH_ASIA_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_South_Asia_Source_Structure_Memberships_v2.csv',
'LiTS':'27_P2_LITS_PASS1/PACKAGE_CONTENTS/03_SOURCE_STRUCTURES/Rawlsing_P2_LiTS_Source_Structure_Memberships_v2.csv'}

STRUCT_MEM_ZIP = {
'GSS':('09_P2_GSS_PASS1/Rawlsing_P2_GSS_AllWave_Deep_Pass_v1_20260731.zip','Source_Structure_Membership'),
'WVS':('10_P2_WVS_PASS1/Rawlsing_P2_WVS_AllWave_Deep_Pass_v1_20260731.zip','Source_Structure_Membership'),
'EVS':('12_P2_EVS_PASS1/Rawlsing_P2_EVS_AllWave_Deep_Pass_v1_20260731.zip','Source_Structure_Membership'),
'Arab Barometer':('15_P2_ARAB_BAROMETER_PASS1/Rawlsing_P2_Arab_Barometer_AllWave_Deep_Pass_v1_20260731.zip','Source_Structure_Membership')}


def stable_id(prefix: str, *parts: object, n: int=24) -> str:
    return f"{prefix}_{hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:n]}"

def norm_text(s: object) -> str:
    s=str(s or '').strip().lower().replace('’',"'").replace('“','"').replace('”','"')
    s=re.sub(r'^\s*(?:q|v|p|gb|gbc|ir|s)?\s*\d+[a-z0-9_.\-]*\s*[:.\-]\s*','',s,flags=re.I)
    s=re.sub(r'\([^)]*\bq\d+[a-z0-9_]*[^)]*\)$','',s,flags=re.I)
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()

def json_set(s: object) -> set[str]:
    try: return set(json.loads(str(s)))
    except Exception: return set()

def wave_semantic(src: str,w: object) -> str:
    return {('Arab Barometer','I'):'W1',('Arab Barometer','II'):'W2',('Arab Barometer','V'):'W5',('Arab Barometer','VIII'):'W8',('EVS','1981'):'W1',('EVS','1999'):'W3'}.get((src,str(w)),str(w))

def token_jaccard(a: str,b: str) -> float:
    A,B=set(a.split()),set(b.split()); return len(A&B)/len(A|B) if A|B else 0.0

def sha256_file(p: pathlib.Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

class UF:
    def __init__(self, items: Iterable[str]): self.p={x:x for x in items}; self.r={x:0 for x in items}
    def find(self,x):
        if self.p[x]!=x:self.p[x]=self.find(self.p[x])
        return self.p[x]
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a==b:return
        if self.r[a]<self.r[b]:a,b=b,a
        self.p[b]=a
        if self.r[a]==self.r[b]:self.r[a]+=1


def load_nodes(root: pathlib.Path) -> pd.DataFrame:
    frames=[]
    for src,rel in CATALOGS.items():
        d=pd.read_csv(root/rel,dtype=str).fillna('')
        assert len(d)>0 and set(d.source_family)=={src}
        def col(n): return d[n] if n in d.columns else pd.Series(['']*len(d),index=d.index)
        out=pd.DataFrame({
          'question_implementation_id':d.question_implementation_id,'source_family':d.source_family,'wave':d.wave,
          'source_variable_code':d.source_variable_code,'source_row_index':d.source_row_index,'question_id':d.question_id,
          'exact_question_text':d.exact_question_text,'normalized_proposition_source':col('normalized_proposition'),
          'comparison_proposition_source':col('comparison_proposition'),'semantic_lane':d.semantic_lane,
          'semantic_role':d.semantic_role,'semantic_subrole':d.semantic_subrole,'response_topology':d.response_topology,
          'substantive_response_signature':col('substantive_response_signature'),'response_contract_hashes':d.response_contract_hashes,
          'response_options_substantive':d.response_options_substantive,'response_family_expectation':d.response_family_expectation,
          'respondent_universe_status':d.respondent_universe_status,'routing_signal_status':d.routing_signal_status,
          'country_scope':d.country_scope,'instrument_scope':d.instrument_scope,'position_conditioning':d.position_conditioning,
          'position_modifiers':col('position_modifiers'),'conditional_strata_weights':col('conditional_strata_weights'),
          'horizon_affordance':col('horizon_affordance'),'module_guess':d.module_guess,'source_authority':d.source_authority,
          'rationale':d.rationale,'exact_identity_sha256':d.exact_identity_sha256})
        out['comparison_text']=out.comparison_proposition_source
        out.loc[out.comparison_text=='','comparison_text']=out.loc[out.comparison_text=='','normalized_proposition_source']
        out.loc[out.comparison_text=='','comparison_text']=out.loc[out.comparison_text=='','exact_question_text']
        out['normalized_comparison_text']=out.comparison_text.map(norm_text)
        out['semantic_wave']=out.wave.map(lambda w:wave_semantic(src,w))
        frames.append(out)
    n=pd.concat(frames,ignore_index=True)
    assert len(n)==18276 and n.question_implementation_id.nunique()==18276
    # semantic reference join; casefold fallback only when unique
    q=pd.read_csv(root/'03_SEMANTIC_REFERENCE/questions_master_semantic(2).csv',dtype=str).fillna('')
    q=q[q.source!=''].copy()
    semcols=['exact_content_id','semantic_content_id','semantic_cluster_id','semantic_content_domain','semantic_content_description',
             'semantic_match_method','semantic_match_score','semantic_match_confidence','semantic_shared_driver','semantic_regional_driver',
             'semantic_primary_driver','semantic_secondary_driver','semantic_scope','semantic_notes','item_id']
    exact={ (r.source,r.wave,r.var_name):r for _,r in q.iterrows() }
    cf=collections.defaultdict(list)
    for _,r in q.iterrows():cf[(r.source,r.wave,r.var_name.casefold())].append(r)
    recs=[]
    for _,r in n.iterrows():
        x=exact.get((r.source_family,r.semantic_wave,r.source_variable_code)); status='EXACT_SOURCE_WAVE_VARIABLE'
        if x is None:
            xs=cf.get((r.source_family,r.semantic_wave,r.source_variable_code.casefold()),[])
            if len(xs)==1:x=xs[0];status='UNIQUE_CASEFOLD_FALLBACK_DIAGNOSTIC'
        if x is None: rec={c:'' for c in semcols};status='NO_SEMANTIC_REFERENCE_MATCH'
        else: rec={c:str(x[c]) for c in semcols}
        rec['semantic_reference_join_status']=status;recs.append(rec)
    return pd.concat([n.reset_index(drop=True),pd.DataFrame(recs)],axis=1)


def build_lineages(root: pathlib.Path,nodes: pd.DataFrame) -> tuple[pd.DataFrame,dict[str,str]]:
    ids=set(nodes.question_implementation_id);uf=UF(ids)
    for src,rel in EDGES.items():
        d=pd.read_csv(root/rel,dtype=str).fillna('')
        for _,r in d.iterrows():
            a,b=r.left_question_implementation_id,r.right_question_implementation_id
            assert a in ids and b in ids;uf.union(a,b)
    qsrc=dict(zip(nodes.question_implementation_id,nodes.source_family)); comps=collections.defaultdict(list)
    for q in ids:comps[(qsrc[q],uf.find(q))].append(q)
    nix=nodes.set_index('question_implementation_id');records=[];q2l={}
    for (src,_),members in sorted(comps.items()):
        members=sorted(members); lid=stable_id('p2lineage',src,*members)
        for m in members:q2l[m]=lid
        s=nix.loc[members].reset_index().sort_values(['wave','source_row_index','source_variable_code']);rep=s.iloc[-1]
        js=lambda col:json.dumps(sorted({str(x) for x in s[col] if str(x)}),ensure_ascii=False)
        records.append({'lineage_id':lid,'source_family':src,'member_count':len(members),
          'member_question_implementation_ids_json':json.dumps(members,ensure_ascii=False),'waves_json':js('wave'),'variables_json':js('source_variable_code'),
          'representative_question_implementation_id':rep.question_implementation_id,'representative_wave':rep.wave,
          'representative_variable':rep.source_variable_code,'representative_text':rep.exact_question_text,
          'normalized_comparison_texts_json':js('normalized_comparison_text'),'semantic_lanes_json':js('semantic_lane'),
          'semantic_roles_json':js('semantic_role'),'semantic_subroles_json':js('semantic_subrole'),
          'response_topologies_json':js('response_topology'),'response_signatures_json':js('substantive_response_signature'),
          'semantic_content_ids_json':js('semantic_content_id'),'exact_content_ids_json':js('exact_content_id'),
          'semantic_primary_drivers_json':js('semantic_primary_driver'),'semantic_secondary_drivers_json':js('semantic_secondary_driver'),
          'position_conditioning_json':js('position_conditioning'),'position_modifiers_json':js('position_modifiers'),
          'conditional_strata_weights_json':js('conditional_strata_weights'),'horizon_affordance_json':js('horizon_affordance'),
          'semantic_reference_statuses_json':js('semantic_reference_join_status'),
          'source_local_authority_status':'ACCEPTED_SOURCE_LOCAL_LINEAGE_COMPONENT' if len(members)>1 else 'SOURCE_LOCAL_SINGLETON_IMPLEMENTATION'})
    l=pd.DataFrame(records).sort_values(['source_family','lineage_id']).reset_index(drop=True)
    nodes['lineage_id']=nodes.question_implementation_id.map(q2l)
    return l,q2l

# Exact proposition group policies. Pair-level gates still prevent role/category leakage.
GENERIC_SHELL={
'do you strongly agree or just agree with the chosen statement','which of the following statements comes closest to your own opinion',
'don t know','none of these'}
GENERIC_ID_WEIGHT={'id','weight','calibration weights','population size weight'}
DEMOGRAPHIC_COORD={
'age','age group','age of respondent','age recoded 3 intervals','age recoded 6 intervals','how old are you','year of birth',
'gender','sex','religion','what is your religion','ethnicity','ethnic group','nationality','education','what is your highest level of education',
'occupation','what is your main occupation','employment status','marital status','sexual orientation','household size','monthly household income',
'number of children in household','how many children do you have','have you had any children','ideal number of children','what is your mother tongue',
'language','language in which interview was conducted','urban rural','father born in country','mother born in country',
'mothers country of birth iso 3166 1 3 alpha code','respondents country of birth iso 3166 1 3 alpha code','are you looking for a job',
'do you live with your parents','how many employees do you have'}
ADMIN_COORD={
'country','country code','country year','region','survey year','interview date','date of interview','interviewer id','interviewer number',
'interviewer s number','interviewer s age','interviewer s gender','respondent number','original respondent number','unified respondent number',
'primary sampling unit','mode of data collection','digital object identifier','year month of start fieldwork','year month of end fieldwork'}
ASSET_COORD={'bicycle','fridge','telephone','mobile phone','tractor','cows buffalo','pumping set','radio transistor','electric fan cooler','scooter motorcycle moped'}
TARGET_ONLY={'abortion','air pollution','parliament','television','local government','regional government','political parties','political party','social security','the courts','the government','the police','radio news','tv news'}
DERIVED_INDEX={'post materialist index 12 item','post materialist index 4 item'}


def group_policy(text: str) -> tuple[str,str,str]:
    if text in GENERIC_SHELL:return ('GENERIC_RESPONSE_OR_PROMPT_SHELL','REJECT','Shared shell/response fragment omits the identity-bearing target or proposition.')
    if text in GENERIC_ID_WEIGHT:return ('GENERIC_IDENTIFIER_OR_WEIGHT','REJECT_EQUIVALENCE','Generic IDs and weights are source-specific processing objects, not portable constructs or values.')
    if text in DEMOGRAPHIC_COORD:return ('DEMOGRAPHIC_OR_POSITION_COORDINATE','CONDITIONAL_ACCEPT','Portable only as a coordinate concept; coding, routing, coverage, and value semantics remain source-versioned.')
    if text in ADMIN_COORD:return ('ADMINISTRATIVE_OR_FIELDWORK_COORDINATE','CONDITIONAL_ACCEPT','Portable only as metadata function; codes and values remain source-versioned.')
    if text in ASSET_COORD:return ('MATERIAL_ASSET_TARGET','CONDITIONAL_ACCEPT','Portable only as an asset/household-context target when both source records confirm that function.')
    if text in TARGET_ONLY:return ('TARGET_LABEL_WITHOUT_RELATION_AXIS','UNRESOLVED','The exact target label does not specify trust, confidence, importance, exposure, behavior, or another relation axis.')
    if text in DERIVED_INDEX:return ('DERIVED_INDEX_LABEL','CONDITIONAL_ACCEPT','Comparable only when derivation contract is corroborated; raw value portability is not presumed.')
    if len(text.split())<=2:return ('SHORT_CONSTRUCT_LABEL','CONDITIONAL_ACCEPT','Short construct labels require semantic-role, target, and response corroboration from both deep-reviewed records.')
    return ('FULL_OR_SUBSTANTIVE_PROPOSITION','CONDITIONAL_ACCEPT','Exact normalized proposition is strong evidence; response and implementation differences set the ceiling.')


def exact_groups_and_pairs(root,nodes,lineages,q2l):
    lix=lineages.set_index('lineage_id'); signals=collections.defaultdict(lambda:collections.defaultdict(set))
    group_rows=[]
    for txt,sub in nodes[nodes.normalized_comparison_text!=''].groupby('normalized_comparison_text'):
        by={src:sorted(set(g.lineage_id)) for src,g in sub.groupby('source_family')}
        if len(by)<2:continue
        pair_count=sum(len(by[a])*len(by[b]) for a,b in itertools.combinations(sorted(by),2))
        cat,default,rat=group_policy(txt)
        group_rows.append({'exact_proposition_group_id':stable_id('p2exactgroup',txt),'normalized_comparison_text':txt,
          'token_count':len(txt.split()),'source_count':len(by),'lineage_count':sum(map(len,by.values())),'pair_count':pair_count,
          'sources_json':json.dumps(sorted(by),ensure_ascii=False),'lineages_by_source_json':json.dumps(by,ensure_ascii=False,sort_keys=True),
          'adjudication_rule_class':cat,'default_disposition':default,'group_rationale':rat,
          'authority_status':'GOVERNING_GROUP_POLICY_PAIR_LEVEL_EVIDENCE_REQUIRED'})
        for a,b in itertools.combinations(sorted(by),2):
            for x in by[a]:
                for y in by[b]:signals[tuple(sorted((x,y)))]['EXACT_NORMALIZED_COMPARISON_TEXT'].add(txt)
    # inherited exact-content discovery only
    for cid,sub in nodes[nodes.exact_content_id!=''].groupby('exact_content_id'):
        by={src:sorted(set(g.lineage_id)) for src,g in sub.groupby('source_family')}
        if len(by)<2:continue
        for a,b in itertools.combinations(sorted(by),2):
            for x in by[a]:
                for y in by[b]:signals[tuple(sorted((x,y)))]['INHERITED_EXACT_CONTENT_ID_DIAGNOSTIC'].add(cid)
    seed=pd.read_csv(root/'29_P2_ALL_NINE_CROSS_SOURCE_SEED_REFRESH/Rawlsing_P2_All_Nine_Source_Comparison_Proposition_Seed_Refresh_v1.csv',dtype=str).fillna('')
    for _,r in seed.iterrows():signals[tuple(sorted((q2l[r.left_question_implementation_id],q2l[r.right_question_implementation_id])))]['SECTION29_SEED'].add(r.candidate_id)

    rows=[]
    context_roles={'POSITION_COORDINATE','STRUCTURAL_CONTEXT','ADMINISTRATIVE_METADATA','admin','administrative_metadata','behavioral_or_demographic_context','demographic_material_or_behavioral_context','demographic_material_or_identity_context','position_context','interview_and_fieldwork_context'}
    material_markers={'demographic_material_or_identity_context','POSITION_COORDINATE','STRUCTURAL_CONTEXT','behavioral_or_demographic_context'}
    for (a,b),sigs in signals.items():
        A,B=lix.loc[a],lix.loc[b]
        if (A.source_family,a)>(B.source_family,b):a,b=b,a;A,B=B,A
        ta,tb=json_set(A.normalized_comparison_texts_json),json_set(B.normalized_comparison_texts_json)
        common=sorted(ta&tb); ex=sorted(json_set(A.exact_content_ids_json)&json_set(B.exact_content_ids_json)); sem=sorted(json_set(A.semantic_content_ids_json)&json_set(B.semantic_content_ids_json))
        ra,rb=json_set(A.semantic_roles_json),json_set(B.semantic_roles_json); sa,sb=json_set(A.semantic_subroles_json),json_set(B.semantic_subroles_json)
        topa,topb=json_set(A.response_topologies_json),json_set(B.response_topologies_json); rsa,rsb=json_set(A.response_signatures_json),json_set(B.response_signatures_json)
        role_overlap=bool(ra&rb); subrole_overlap=bool(sa&sb); top_overlap=bool(topa&topb); resp_overlap=bool(rsa and rsb and rsa&rsb)
        sim=max([SequenceMatcher(None,x,y).ratio() for x in ta for y in tb] or [0]); jac=max([token_jaccard(x,y) for x in ta for y in tb] or [0])
        relation='UNRESOLVED';authority='UNRESOLVED_REQUIRES_ADJUDICATION';ceiling='NONE';confidence='LOW';rule='INHERITED_DIAGNOSTIC_ONLY';rationale='Inherited content or seed evidence identifies a review candidate, not cross-source authority.'
        if common:
            text=common[0];cat,default,_=group_policy(text);rule=cat
            if cat=='GENERIC_RESPONSE_OR_PROMPT_SHELL':
                relation='SHARED_PROPOSITION_DIFFERENT_TARGET';authority='REJECTED_CROSS_SOURCE_EQUIVALENCE';ceiling='ANTI_JOIN_ONLY';confidence='HIGH';rationale='Shared shell or response fragment omits the identity-bearing target/proposition.'
            elif cat=='GENERIC_IDENTIFIER_OR_WEIGHT':
                relation='ANALOGOUS_NOT_EQUIVALENT';authority='REJECTED_CROSS_SOURCE_EQUIVALENCE';ceiling='METADATA_FUNCTION_ONLY';confidence='HIGH';rationale='Both records are generic processing objects; source-specific construction and values prohibit equivalence.'
            elif cat in {'DEMOGRAPHIC_OR_POSITION_COORDINATE','ADMINISTRATIVE_OR_FIELDWORK_COORDINATE'}:
                coordinate_topologies={'administrative','ordinal_context','nominal_choice','continuous_context','continuous_numeric','open_or_continuous','binary_contrast','interview_context'}
                prohibited_coordinate_subroles={'multi_response_dummy','uncollapsed_substantive_topology','religious_or_spiritual_orientation','national_belonging_or_pride'}
                typed_a=bool(topa) and topa.issubset(coordinate_topologies); typed_b=bool(topb) and topb.issubset(coordinate_topologies)
                subrole_conflict=bool((sa|sb)&prohibited_coordinate_subroles)
                ambiguous_coordinate_ok=(text!='language') or subrole_overlap or bool(sem)
                if (ra&context_roles) and (rb&context_roles) and typed_a and typed_b and not subrole_conflict and ambiguous_coordinate_ok:
                    relation='FUNCTIONALLY_COMPARABLE';authority='ACCEPTED_CROSS_SOURCE_CONTINUITY';ceiling='CONTEXT_OR_POSITION_COORDINATE_ONLY';confidence='HIGH';rationale='Both deep-reviewed records identify the same coordinate function; codes, categories, coverage, routing, and values remain source-versioned.'
                else:
                    relation='SHARED_PROPOSITION_DIFFERENT_TARGET';authority='UNRESOLVED_ROLE_OR_CONTEXT_CONFLICT';ceiling='NONE';confidence='MEDIUM';rationale='The shared label spans a coordinate/metadata use and a substantive, multiselect, scalar, or differently typed use; referent/value portability is not authorized.'
            elif cat=='MATERIAL_ASSET_TARGET':
                if (ra&material_markers) and (rb&material_markers):
                    relation='FUNCTIONALLY_COMPARABLE';authority='ACCEPTED_CROSS_SOURCE_CONTINUITY';ceiling='TARGET_AND_CONTEXT_FUNCTION_ONLY';confidence='HIGH';rationale='Both records encode the same material asset target; ownership coding, household universe, and response semantics remain source-versioned.'
                else:
                    relation='UNRESOLVED';authority='UNRESOLVED_TARGET_OR_ROLE_CONFLICT';ceiling='NONE';confidence='MEDIUM';rationale='The shared asset label is not corroborated as the same material-context function on both sides.'
            elif cat=='TARGET_LABEL_WITHOUT_RELATION_AXIS':
                relation='SHARED_TARGET_DIFFERENT_PROPOSITION';authority='UNRESOLVED_RELATION_AXIS_REQUIRED';ceiling='TARGET_NEIGHBORHOOD_ONLY';confidence='MEDIUM';rationale='Exact target recurrence is real, but the relation axis must be recovered from source parent/structure evidence before portability.'
            elif cat=='DERIVED_INDEX_LABEL':
                if role_overlap or sem:
                    relation='FUNCTIONALLY_COMPARABLE';authority='ACCEPTED_CROSS_SOURCE_CONTINUITY';ceiling='DERIVED_INDEX_CONSTRUCT_ONLY';confidence='MEDIUM';rationale='The named derived construct recurs and semantic function aligns; derivation formulas and values remain versioned.'
                else:
                    relation='UNRESOLVED';authority='UNRESOLVED_DERIVATION_CONTRACT_REQUIRED';ceiling='NONE';confidence='MEDIUM';rationale='Exact index label without corroborated derivation/semantic function cannot authorize equivalence.'
            elif cat=='SHORT_CONSTRUCT_LABEL':
                if role_overlap and (subrole_overlap or sem) and top_overlap:
                    relation='FUNCTIONALLY_COMPARABLE';authority='ACCEPTED_CROSS_SOURCE_CONTINUITY';ceiling='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY';confidence='MEDIUM';rationale='Short construct label is corroborated by matching semantic role/subrole and response topology; implementation details remain versioned.'
                else:
                    relation='UNRESOLVED';authority='UNRESOLVED_TARGET_OR_PROPOSITION_DIFFERENCE';ceiling='CONCEPT_NEIGHBORHOOD_ONLY';confidence='MEDIUM';rationale='Short shared label lacks sufficient two-sided role/target/response corroboration.'
            else: # full proposition
                if resp_overlap:relation='EXACT_PORTABLE_EQUIVALENT';ceiling='QUESTION_AND_RESPONSE_CONTRACT'
                elif top_overlap:relation='FUNCTIONALLY_COMPARABLE';ceiling='QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY'
                else:relation='FUNCTIONALLY_COMPARABLE';ceiling='QUESTION_PROPOSITION_ONLY'
                authority='ACCEPTED_CROSS_SOURCE_CONTINUITY';confidence='HIGH' if (role_overlap or sem) else 'MEDIUM'
                rationale='The full exact normalized proposition recurs in two deep-reviewed source records. Response and implementation differences set the ceiling; any source-local semantic-role conflict remains visible and is not used to widen portability.'
        rows.append({'cross_source_candidate_id':stable_id('p2xsrc',a,b),'left_source_family':A.source_family,'right_source_family':B.source_family,
          'left_lineage_id':a,'right_lineage_id':b,'left_representative_question_implementation_id':A.representative_question_implementation_id,
          'right_representative_question_implementation_id':B.representative_question_implementation_id,'left_waves_json':A.waves_json,'right_waves_json':B.waves_json,
          'left_variables_json':A.variables_json,'right_variables_json':B.variables_json,'left_texts_json':A.normalized_comparison_texts_json,'right_texts_json':B.normalized_comparison_texts_json,
          'common_exact_texts_json':json.dumps(common,ensure_ascii=False),'shared_exact_content_ids_json':json.dumps(ex,ensure_ascii=False),
          'shared_semantic_content_ids_json':json.dumps(sem,ensure_ascii=False),'discovery_signals_json':json.dumps({k:sorted(v) for k,v in sorted(sigs.items())},ensure_ascii=False,sort_keys=True),
          'left_semantic_roles_json':A.semantic_roles_json,'right_semantic_roles_json':B.semantic_roles_json,'left_semantic_subroles_json':A.semantic_subroles_json,
          'right_semantic_subroles_json':B.semantic_subroles_json,'left_response_topologies_json':A.response_topologies_json,'right_response_topologies_json':B.response_topologies_json,
          'semantic_role_overlap':str(role_overlap).lower(),'semantic_subrole_overlap':str(subrole_overlap).lower(),'response_topology_overlap':str(top_overlap).lower(),
          'response_signature_exact_overlap':str(resp_overlap).lower(),'max_text_sequence_similarity':f'{sim:.6f}','max_text_token_jaccard':f'{jac:.6f}',
          'adjudication_rule_class':rule,'relation_type':relation,'authority_status':authority,'portability_ceiling':ceiling,'adjudication_confidence':confidence,
          'two_sided_evidence_status':'COMPLETE_DEEP_REVIEWED_SOURCE_RECORDS_BOTH_SIDES','rationale':rationale,
          'prohibited_use':'No J-family membership, respondent join, registry installation, or runtime authority.'})
    return pd.DataFrame(group_rows).sort_values('normalized_comparison_text'),pd.DataFrame(rows).sort_values(['left_source_family','right_source_family','cross_source_candidate_id'])


def semantic_neighborhoods(lineages: pd.DataFrame):
    """Build cross-source semantic neighborhoods and a bounded priority queue.

    The inherited semantic IDs are discovery coordinates, not authority. Counts
    cover the complete Cartesian surface; the materialized queue keeps the top
    25 pairs per semantic-ID/source-pair cell so review is finite and useful.
    """
    cache={}; by_sem=collections.defaultdict(lambda:collections.defaultdict(list))
    for r in lineages.itertuples(index=False):
        texts=sorted(json_set(r.normalized_comparison_texts_json),key=lambda x:(-len(x),x))
        text=texts[0] if texts else norm_text(r.representative_text)
        cache[r.lineage_id]={'source':r.source_family,'rep':r.representative_text,'text':text,'tokens':set(text.split()),
          'roles':json_set(r.semantic_roles_json),'subs':json_set(r.semantic_subroles_json),'tops':json_set(r.response_topologies_json)}
        for sid in json_set(r.semantic_content_ids_json):by_sem[sid][r.source_family].append(r.lineage_id)
    cross=[];queue=[]
    for sid,by0 in by_sem.items():
        by={s:sorted(set(ids)) for s,ids in by0.items()}
        srcs=sorted(by)
        if len(srcs)<2:continue
        total=sum(len(by[a])*len(by[b]) for a,b in itertools.combinations(srcs,2))
        cross.append({'semantic_neighborhood_id':stable_id('p2semnbhd',sid),'semantic_content_id':sid,'source_count':len(srcs),
          'lineage_count':sum(len(x) for x in by.values()),'candidate_pair_count':total,'sources_json':json.dumps(srcs,ensure_ascii=False),
          'lineages_by_source_json':json.dumps(by,ensure_ascii=False,sort_keys=True),'authority_status':'DISCOVERY_NEIGHBORHOOD_REQUIRES_TWO_SIDED_ADJUDICATION',
          'prohibited_use':'Inherited semantic cluster is not equivalence, family membership, or respondent-level authority.'})
        for a,b in itertools.combinations(srcs,2):
            scored=[]
            for x in by[a]:
                A=cache[x]
                for y in by[b]:
                    B=cache[y]; union=A['tokens']|B['tokens'];jac=len(A['tokens']&B['tokens'])/len(union) if union else 0
                    exact=bool(A['text'] and A['text']==B['text']);roles=bool(A['roles']&B['roles']);subs=bool(A['subs']&B['subs']);tops=bool(A['tops']&B['tops'])
                    score=100*exact+55*jac+15*roles+10*subs+5*tops
                    scored.append((score,x,y,jac,exact,roles,subs,tops))
            scored.sort(key=lambda z:(-z[0],z[1],z[2]))
            for rank,z in enumerate(scored[:25],1):
                score,x,y,jac,exact,roles,subs,tops=z;A=cache[x];B=cache[y]
                queue.append({'semantic_pair_candidate_id':stable_id('p2sempair',sid,x,y),'semantic_content_id':sid,
                  'left_source_family':a,'right_source_family':b,'left_lineage_id':x,'right_lineage_id':y,
                  'left_representative_text':A['rep'],'right_representative_text':B['rep'],'cell_candidate_count':len(scored),'cell_priority_rank':rank,
                  'exact_normalized_text_match':str(exact).lower(),'semantic_role_overlap':str(roles).lower(),'semantic_subrole_overlap':str(subs).lower(),
                  'response_topology_overlap':str(tops).lower(),'max_text_token_jaccard':f'{jac:.6f}','review_priority_score':f'{score:.6f}',
                  'authority_status':'PROVISIONAL_DISCOVERY_PAIR_NOT_ADJUDICATED','prohibited_use':'No equivalence or J-family authority.'})
    c=pd.DataFrame(cross).sort_values(['source_count','lineage_count','semantic_content_id'],ascending=[False,False,True])
    q=pd.DataFrame(queue)
    if len(q):q=q.sort_values(['review_priority_score','semantic_pair_candidate_id'],ascending=[False,True])
    return c,q


def build_structures(root: pathlib.Path,nodes: pd.DataFrame,lineages: pd.DataFrame):
    inv_rows=[];mem_rows=[];nix=nodes.set_index('question_implementation_id'); lookup={(r.source_family,r.wave,r.source_variable_code):r.question_implementation_id for _,r in nodes.iterrows()}
    cf=collections.defaultdict(list)
    for _,r in nodes.iterrows():cf[(r.source_family,r.wave,r.source_variable_code.casefold())].append(r.question_implementation_id)
    # inventories
    for src,rel in STRUCT_INV.items():
        d=pd.read_csv(root/rel,dtype=str).fillna('')
        for _,r in d.iterrows():
            sid=r.get('source_structure_id',r.get('structure_id',''))
            inv_rows.append({'source_structure_id':sid,'source_family':src,'wave':r.get('wave',''),'structure_type':r.get('structure_basis',r.get('structure_type','')),
              'structure_label':r.get('common_text_stem',r.get('common_proposition_stem',r.get('source_structure_label',r.get('structure_label',r.get('common_variable_prefix',''))))),
              'declared_member_count':r.get('member_count',''),'source_authority_status':r.get('source_structure_status',r.get('authority_status','')),
              'source_rationale':r.get('source_rationale',r.get('source_basis',r.get('source_evidence',''))),
              'first_source_row_index':r.get('first_source_row_index',''),'last_source_row_index':r.get('last_source_row_index','')})
    inv=pd.DataFrame(inv_rows)
    print(f'  structures: inventories {len(inv)}',flush=True)
    # Exact membership files: exposed for five sources and recovered from the
    # governing nested source packages for GSS/WVS/EVS/Arab Barometer.
    membership_frames=[]
    for src,rel in STRUCT_MEM.items():
        membership_frames.append((src,pd.read_csv(root/rel,dtype=str).fillna(''),'EXPOSED_GOVERNING_MEMBERSHIP_FILE'))
    for src,(ziprel,needle) in STRUCT_MEM_ZIP.items():
        with zipfile.ZipFile(root/ziprel) as z:
            names=[n for n in z.namelist() if needle in n and n.lower().endswith('.csv')]
            assert len(names)==1,(src,names)
            membership_frames.append((src,pd.read_csv(io.BytesIO(z.read(names[0])),dtype=str).fillna(''),'NESTED_GOVERNING_SOURCE_PACKAGE_MEMBERSHIP_FILE'))
    for src,d,origin in membership_frames:
        for _,r in d.iterrows():
            sid=r.get('source_structure_id',r.get('structure_id',''));qid=r.get('question_implementation_id','');wave=r.get('wave','');var=r.get('source_variable_code','')
            status=origin
            if not qid:
                qid=lookup.get((src,wave,var),'');status=origin+'::EXACT_SOURCE_WAVE_VARIABLE_LOOKUP'
                if not qid:
                    xs=cf.get((src,wave,var.casefold()),[])
                    if len(xs)==1:qid=xs[0];status=origin+'::UNIQUE_CASEFOLD_SOURCE_WAVE_VARIABLE_LOOKUP'
            mem_rows.append({'source_structure_id':sid,'source_family':src,'wave':wave,'source_variable_code':var,'question_implementation_id':qid,
              'lineage_id':nix.loc[qid].lineage_id if qid in nix.index else '','member_order':r.get('member_order',''),
              'membership_recovery_status':status if qid else origin+'::UNRESOLVED_MEMBER'})
    print(f'  structures: governing membership rows {len(mem_rows)}',flush=True)
    mem=pd.DataFrame(mem_rows).drop_duplicates(['source_structure_id','question_implementation_id']).sort_values(['source_family','source_structure_id','member_order'])
    print(f'  structures: recovered membership rows {len(mem)}',flush=True)
    # signatures and recovery status
    sigrows=[]
    mem_by={k:g for k,g in mem.groupby('source_structure_id',sort=False)}
    for _,r in inv.iterrows():
        g=mem_by.get(r.source_structure_id,pd.DataFrame(columns=mem.columns));q=nix.loc[list(g.question_implementation_id)].reset_index() if len(g) else pd.DataFrame()
        def vals(c):return sorted({str(x) for x in q[c] if str(x)}) if len(q) else []
        sem=vals('semantic_content_id');ex=vals('exact_content_id');roles=vals('semantic_role');subs=vals('semantic_subrole');tops=vals('response_topology');lins=sorted(set(g.lineage_id)-{''})
        declared=int(r.declared_member_count) if str(r.declared_member_count).isdigit() else None
        recovered=len(g);status='COMPLETE' if declared==recovered else ('PARTIAL_OR_OVERLAPPING_REGISTRY_VERSION' if recovered else 'UNRECOVERED')
        sigrows.append({**r.to_dict(),'recovered_member_count':recovered,'membership_recovery_status':status,
          'member_lineage_count':len(lins),'member_lineages_json':json.dumps(lins,ensure_ascii=False),'semantic_content_ids_json':json.dumps(sem,ensure_ascii=False),
          'exact_content_ids_json':json.dumps(ex,ensure_ascii=False),'semantic_roles_json':json.dumps(roles,ensure_ascii=False),
          'semantic_subroles_json':json.dumps(subs,ensure_ascii=False),'response_topologies_json':json.dumps(tops,ensure_ascii=False),
          'cross_source_use_status':'DISCOVERY_STRUCTURE_ONLY_NOT_J_FAMILY_AUTHORITY'})
    sig=pd.DataFrame(sigrows)
    print(f'  structures: signatures {len(sig)}',flush=True)
    # High-precision provisional structure analogies only: exact normalized
    # source-structure labels, conservatively capped. Broad semantic structure
    # matching remains the next tranche because overlap alone is not authority.
    six=sig.set_index('source_structure_id');cand=[]
    label_groups=collections.defaultdict(list)
    for _,r in sig.iterrows():
        lab=norm_text(r.structure_label)
        if lab and len(lab.split())>=2:label_groups[lab].append(r.source_structure_id)
    for lab,ids in sorted(label_groups.items()):
        if len(ids)<2 or len(ids)>20:continue
        for a,b in itertools.combinations(sorted(ids),2):
            A,B=six.loc[a],six.loc[b]
            if A.source_family==B.source_family:continue
            sa=json_set(A.semantic_content_ids_json);sb=json_set(B.semantic_content_ids_json);shared=sa&sb
            role=bool(json_set(A.semantic_roles_json)&json_set(B.semantic_roles_json));top=bool(json_set(A.response_topologies_json)&json_set(B.response_topologies_json))
            jac=len(shared)/len(sa|sb) if sa|sb else 0
            cand.append({'structure_analogy_candidate_id':stable_id('p2structpair',a,b),'left_source_family':A.source_family,'right_source_family':B.source_family,
              'left_source_structure_id':a,'right_source_structure_id':b,'left_structure_label':A.structure_label,'right_structure_label':B.structure_label,
              'discovery_signals_json':json.dumps(['EXACT_NORMALIZED_STRUCTURE_LABEL'],ensure_ascii=False),'shared_semantic_content_count':len(shared),
              'shared_semantic_content_ids_json':json.dumps(sorted(shared),ensure_ascii=False),'semantic_set_jaccard':f'{jac:.6f}',
              'semantic_role_overlap':str(role).lower(),'response_topology_overlap':str(top).lower(),'review_priority_score':f'{20+10*role+5*top+20*jac:.6f}',
              'authority_status':'PROVISIONAL_HIGH_PRECISION_STRUCTURE_ANALOGY_REQUIRES_MEMBER_BY_MEMBER_ADJUDICATION',
              'prohibited_use':'Structure-label recurrence does not authorize family identity, hyperedges, or respondent composition.'})
    c=pd.DataFrame(cand)
    if len(c):c=c.sort_values(['review_priority_score','structure_analogy_candidate_id'],ascending=[False,True])
    print(f'  structures: exact-label provisional analogies {len(c)}',flush=True)
    return sig,mem,c


def driver_strata_bridge(lineages: pd.DataFrame,nodes: pd.DataFrame,nine_ledger_path: pathlib.Path):
    rows=[]
    for _,r in lineages.iterrows():
        rows.append({'lineage_id':r.lineage_id,'source_family':r.source_family,'member_count':r.member_count,
          'semantic_content_ids_json':r.semantic_content_ids_json,'semantic_primary_drivers_json':r.semantic_primary_drivers_json,
          'semantic_secondary_drivers_json':r.semantic_secondary_drivers_json,'position_conditioning_json':r.position_conditioning_json,
          'position_modifiers_json':r.position_modifiers_json,'conditional_strata_weights_json':r.conditional_strata_weights_json,
          'horizon_affordance_json':r.horizon_affordance_json,
          'bridge_authority_status':'INHERITED_DIAGNOSTIC_COORDINATES_REQUIRE_GLOBAL_P2_ADJUDICATION',
          'prohibited_use':'No direct driver, strata, horizon, or J-family installation authority.'})
    bridge=pd.DataFrame(rows)
    ledger=json.load(open(nine_ledger_path))
    gap_rows=[]
    for f in ledger.get('field_families',ledger.get('field_lineage_ledger',ledger.get('fields',[]))):
        if not isinstance(f,dict):continue
        gap_rows.append({k:(json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(dict,list)) else v) for k,v in f.items()})
    gaps=pd.DataFrame(gap_rows)
    return bridge,gaps,ledger


def coverage_matrix(exact_pairs,semantic_pairs,struct_pairs):
    rows=[]
    for a,b in itertools.combinations(SOURCES,2):
        e=exact_pairs[((exact_pairs.left_source_family==a)&(exact_pairs.right_source_family==b))|((exact_pairs.left_source_family==b)&(exact_pairs.right_source_family==a))]
        s=semantic_pairs[((semantic_pairs.left_source_family==a)&(semantic_pairs.right_source_family==b))|((semantic_pairs.left_source_family==b)&(semantic_pairs.right_source_family==a))]
        t=struct_pairs[((struct_pairs.left_source_family==a)&(struct_pairs.right_source_family==b))|((struct_pairs.left_source_family==b)&(struct_pairs.right_source_family==a))] if len(struct_pairs) else pd.DataFrame()
        rows.append({'left_source_family':a,'right_source_family':b,'exact_foundation_candidates':len(e),
          'exact_accepted':int(e.authority_status.str.startswith('ACCEPTED').sum()),'exact_rejected':int(e.authority_status.str.startswith('REJECTED').sum()),
          'exact_unresolved':int((~e.authority_status.str.startswith('ACCEPTED')&~e.authority_status.str.startswith('REJECTED')).sum()),
          'semantic_neighborhood_candidate_pairs':len(s),'provisional_structure_analogy_candidates':len(t),
          'coverage_status':'PRESENT' if len(e)+len(s)+len(t)>0 else 'NO_DISCOVERY_CANDIDATES_NOT_A_CLOSURE_FAILURE'})
    return pd.DataFrame(rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--handoff-root',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--nine-strata-ledger',required=True);args=ap.parse_args()
    root=pathlib.Path(args.handoff_root);out=pathlib.Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    print('stage: load nodes',flush=True); nodes=load_nodes(root)
    print('stage: build lineages',flush=True); lineages,q2l=build_lineages(root,nodes)
    print('stage: exact groups and pairs',flush=True); groups,exact_pairs=exact_groups_and_pairs(root,nodes,lineages,q2l)
    print('stage: semantic neighborhoods',flush=True); sem_groups,sem_pairs=semantic_neighborhoods(lineages)
    print('stage: structures',flush=True); structures,memberships,struct_pairs=build_structures(root,nodes,lineages)
    print('stage: driver strata',flush=True); bridge,strata_gaps,strata_raw=driver_strata_bridge(lineages,nodes,pathlib.Path(args.nine_strata_ledger))
    coverage=coverage_matrix(exact_pairs,sem_pairs,struct_pairs)
    files={
      'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv':nodes,
      'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv':lineages,
      'Rawlsing_P2_Exact_Proposition_Group_Adjudication_v1.csv':groups,
      'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v1.csv':exact_pairs,
      'Rawlsing_P2_Semantic_Neighborhood_Registry_v1.csv':sem_groups,
      'Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv':sem_pairs,
      'Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv':structures,
      'Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv':memberships,
      'Rawlsing_P2_Provisional_Structure_Analogy_Queue_v1.csv':struct_pairs,
      'Rawlsing_P2_Semantic_Driver_Strata_Bridge_v1.csv':bridge,
      'Rawlsing_P2_Nine_Strata_Field_Lineage_Gap_Ledger_v1.csv':strata_gaps,
      'Rawlsing_P2_Source_Pair_Coverage_Matrix_v1.csv':coverage}
    for name,df in files.items():df.to_csv(out/name,index=False)
    shutil.copy2(args.nine_strata_ledger,out/'SOURCE_nine_strata_field_lineage_ledger.json')
    raw_declared=strata_raw.get('summary',{}).get('field_families_traced')
    normalized_strata_summary={
      'normalized_field_family_rows':len(strata_gaps),
      'lineage_status_counts':strata_gaps.lineage_status.value_counts().to_dict() if len(strata_gaps) else {},
      'authority_status_counts':strata_gaps.authority_status.value_counts().to_dict() if len(strata_gaps) else {},
      'raw_summary_declared_field_families_traced':raw_declared,
      'raw_summary_status_count_sum':sum(v for k,v in strata_raw.get('summary',{}).items() if k in ['preserved_authoritative','present_upstream_dropped_at_v552j','present_but_empty','missing_generated_artifact'] and isinstance(v,int)),
      'raw_summary_consistent_with_rows':raw_declared==len(strata_gaps),
      'disposition':'RAW_SUMMARY_METADATA_STALE_OR_INTERNALLY_INCONSISTENT; GOVERN BY FIELD_FAMILY ROWS AND THIS NORMALIZED SUMMARY',
      'critical_finding':strata_raw.get('summary',{}).get('critical_finding','')}
    json.dump(normalized_strata_summary,open(out/'Rawlsing_P2_Nine_Strata_Field_Lineage_Normalized_Summary_v1.json','w'),indent=2,ensure_ascii=False)
    # validation
    validations=[]
    def ck(name,ok,observed,expected):validations.append({'check':name,'status':'PASS' if ok else 'FAIL','observed':observed,'expected':expected})
    ck('node_count',len(nodes)==18276,len(nodes),18276);ck('node_identity_unique',nodes.question_implementation_id.nunique()==18276,nodes.question_implementation_id.nunique(),18276)
    ck('lineage_partition_count',sum(pd.to_numeric(lineages.member_count))==18276,int(sum(pd.to_numeric(lineages.member_count))),18276)
    ck('lineage_count',len(lineages)==13526,len(lineages),13526)
    ck('semantic_reference_joined',int((nodes.semantic_reference_join_status!='NO_SEMANTIC_REFERENCE_MATCH').sum())==18249,int((nodes.semantic_reference_join_status!='NO_SEMANTIC_REFERENCE_MATCH').sum()),18249)
    ck('semantic_reference_unmatched_preserved',int((nodes.semantic_reference_join_status=='NO_SEMANTIC_REFERENCE_MATCH').sum())==27,int((nodes.semantic_reference_join_status=='NO_SEMANTIC_REFERENCE_MATCH').sum()),27)
    ck('exact_cross_source_groups',len(groups)==146,len(groups),146)
    ck('all_exact_groups_governed',groups.authority_status.str.startswith('GOVERNING').all(),int(groups.authority_status.str.startswith('GOVERNING').sum()),len(groups))
    ck('exact_pair_endpoints_valid',set(exact_pairs.left_lineage_id).union(set(exact_pairs.right_lineage_id)).issubset(set(lineages.lineage_id)),len(exact_pairs),'all valid')
    ck('exact_pair_ids_unique',exact_pairs.cross_source_candidate_id.nunique()==len(exact_pairs),exact_pairs.cross_source_candidate_id.nunique(),len(exact_pairs))
    ck('semantic_neighborhoods_cross_source',len(sem_groups)==200,len(sem_groups),200)
    ck('semantic_pair_ids_unique',sem_pairs.semantic_pair_candidate_id.nunique()==len(sem_pairs),sem_pairs.semantic_pair_candidate_id.nunique(),len(sem_pairs))
    ck('source_structure_inventory_count',len(structures)==2499,len(structures),2499)
    ck('structure_member_endpoints_resolved',(memberships.question_implementation_id!='').all(),int((memberships.question_implementation_id!='').sum()),len(memberships))
    ck('all_structure_memberships_match_declared',(structures.membership_recovery_status=='COMPLETE').all(),int((structures.membership_recovery_status=='COMPLETE').sum()),2499)
    ck('semantic_full_candidate_surface_count',int(pd.to_numeric(sem_groups.candidate_pair_count).sum())==136329,int(pd.to_numeric(sem_groups.candidate_pair_count).sum()),136329)
    ck('semantic_queue_bounded_per_cell',int(pd.to_numeric(sem_pairs.cell_priority_rank).max())<=25,int(pd.to_numeric(sem_pairs.cell_priority_rank).max()),25)
    ck('source_pair_matrix_complete',len(coverage)==36,len(coverage),36)
    ck('nine_strata_gap_source_preserved',(out/'SOURCE_nine_strata_field_lineage_ledger.json').exists(),1,1)
    ck('nine_strata_raw_summary_inconsistency_detected_and_disclosed',normalized_strata_summary['raw_summary_consistent_with_rows'] is False,normalized_strata_summary['raw_summary_consistent_with_rows'],False)
    vdf=pd.DataFrame(validations);vdf.to_csv(out/'VALIDATION_CHECKS.csv',index=False)
    status='PASS' if (vdf.status=='PASS').all() else 'FAIL'
    summary={
      'status':status,'stage':'P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1_EXACT_AND_STRUCTURAL_FOUNDATION',
      'authority_boundary':'No J-family membership, respondent join, registry installation, or runtime execution authorized.',
      'counts':{'nodes':len(nodes),'source_local_lineages':len(lineages),'exact_proposition_groups':len(groups),'exact_foundation_pairs':len(exact_pairs),
        'exact_accepted':int(exact_pairs.authority_status.str.startswith('ACCEPTED').sum()),'exact_rejected':int(exact_pairs.authority_status.str.startswith('REJECTED').sum()),
        'exact_unresolved':int((~exact_pairs.authority_status.str.startswith('ACCEPTED')&~exact_pairs.authority_status.str.startswith('REJECTED')).sum()),
        'semantic_neighborhoods':len(sem_groups),'semantic_pair_queue':len(sem_pairs),'source_structures':len(structures),
        'structure_memberships':len(memberships),'provisional_structure_analogy_candidates':len(struct_pairs),'source_pairs_covered':len(coverage),'nine_strata_field_family_rows':len(strata_gaps),'nine_strata_raw_summary_declared':raw_declared},
      'semantic_reference':nodes.semantic_reference_join_status.value_counts().to_dict(),
      'nine_strata_lineage_limitation':'Full nine-strata authority is not present across the P2 surface; authoritative fields exist upstream for a limited GSS subset and are dropped at V552→V552J. No strata labels were invented.',
      'next_pass':'P2_GLOBAL_REWORDED_TRANSLATION_TARGET_RELATION_AXIS_AND_STRUCTURE_ADJUDICATION',
      'validation_checks':validations}
    json.dump(summary,open(out/'VALIDATION.json','w'),indent=2,ensure_ascii=False)
    # deterministic file manifest
    manifest=[]
    for p in sorted(out.iterdir()):
        if p.is_file():manifest.append({'relative_path':p.name,'size_bytes':p.stat().st_size,'sha256':sha256_file(p)})
    pd.DataFrame(manifest).to_csv(out/'SECTION_MANIFEST.csv',index=False)
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    if status!='PASS':sys.exit(1)

if __name__=='__main__':main()
