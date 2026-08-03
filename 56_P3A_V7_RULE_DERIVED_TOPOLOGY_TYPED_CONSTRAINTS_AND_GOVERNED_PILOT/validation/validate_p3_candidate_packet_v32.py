from __future__ import annotations
from pathlib import Path
import copy,itertools,json,sys
from referencing import Registry,Resource
from jsonschema import Draft202012Validator,FormatChecker
from p3_canonical_json_v7 import canonical_sha256

def loadj(p): return json.loads(Path(p).read_text())
def schema_registry(sec):
    pairs=[]
    for p in sorted((sec/'schemas').glob('*.json')):
        o=loadj(p); pairs.append((o['$id'],Resource.from_contents(o)))
    return Registry().with_resources(pairs)
def fail(msg): raise ValueError(msg)
def validate_schema(sec,name,obj,reg):
    Draft202012Validator(loadj(sec/'schemas'/name),registry=reg,format_checker=FormatChecker()).validate(obj)

def _sort_objects(values):
    return sorted(values,key=canonical_sha256)

def evidence_surface(packet):
    candidate=copy.deepcopy(packet['candidate_family'])
    candidate.pop('evidence_bundle_hash',None); candidate.pop('ranking',None)
    return {
      'serialization_contract':'P3_CANONICAL_JSON_V7',
      'candidate_family':candidate,
      'origin_components':_sort_objects(packet['origin_components']),
      'members_by_source':packet['members_by_source'],
      'proposition_signature_matrix':_sort_objects(packet['proposition_signature_matrix']),
      'response_contract_matrix':_sort_objects(packet['response_contract_matrix']),
      'pair_projections':_sort_objects(packet['pair_projections']),
      'internal_pair_matrix':_sort_objects(packet['internal_pair_matrix']),
      'hard_collisions':_sort_objects(packet['hard_collisions']),
      'unresolved_pairs':_sort_objects(packet['unresolved_pairs']),
      'unruled_pairs':_sort_objects(packet['unruled_pairs']),
      'closure_obligations':_sort_objects(packet['closure_obligations']),
      'likely_split_points':_sort_objects(packet['likely_split_points']),
      'proposed_variants':_sort_objects(packet['proposed_variants']),
      'explicit_exclusions':_sort_objects(packet['explicit_exclusions']),
      'hyperedge_context':_sort_objects(packet['hyperedge_context']),
      'strata_horizon_context':_sort_objects(packet['strata_horizon_context']),
      'exact_evidence_links':packet['exact_evidence_links'],
    }

def _release_ids(obj):
    out=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=='authority_release_id': out.append(v)
            out.extend(_release_ids(v))
    elif isinstance(obj,list):
        for v in obj: out.extend(_release_ids(v))
    return out

def _exact_object_index(values,key):
    out={}
    for v in values:
        k=v[key]
        if k in out: fail(f'duplicate {key}: {k}')
        out[k]=v
    return out

def validate_packet(packet_path,decision_path=None):
    packet_path=Path(packet_path); sec=Path(__file__).resolve().parents[1]; p=loadj(packet_path); reg=schema_registry(sec)
    validate_schema(sec,'candidate_packet.schema.json',p,reg)
    c=p['candidate_family']; members=set(c['member_ids']); release=c['authority_release_id']
    bad_releases={x for x in _release_ids({k:v for k,v in p.items() if k!='decision_form'}) if x!=release}
    if bad_releases: fail(f'packet authority-release mismatch: {sorted(bad_releases)}')
    computed_hash=canonical_sha256(evidence_surface(p))
    if computed_hash!=p['evidence_bundle_hash']: fail('evidence bundle hash does not recompute from full delivered evidence')
    if c['evidence_bundle_hash']!=p['evidence_bundle_hash']: fail('candidate and packet evidence hashes differ')
    source_members=[x for xs in p['members_by_source'].values() for x in xs]
    if len(source_members)!=len(set(source_members)) or set(source_members)!=members: fail('members_by_source must partition candidate members exactly')
    sigs=_exact_object_index(p['proposition_signature_matrix'],'subject_id')
    rcs=_exact_object_index(p['response_contract_matrix'],'subject_id')
    if set(sigs)!=members: fail('exactly one signature per member')
    if set(rcs)!=members: fail('exactly one response contract reference per member')
    expected={tuple(sorted(x)) for x in itertools.combinations(members,2)}
    projections=_exact_object_index(p['pair_projections'],'projection_id')
    rows=p['internal_pair_matrix']
    direct_states={'DIRECT_POSITIVE','DIRECT_COLLISION','DIRECT_UNRESOLVED','HIERARCHICAL_ONLY'}
    for row in rows:
        if row['pair_state'] in direct_states:
            proj=projections.get(row['pair_projection_id'])
            if not proj: fail('direct internal pair lacks delivered projection')
            if {proj['left_subject_id'],proj['right_subject_id']}!={row['left_id'],row['right_id']}: fail('projection endpoints do not match internal pair subjects')
            if proj['pair_fact_id']!=row['pair_fact_id']: fail('projection pair fact mismatch')
    direct_used={x['pair_projection_id'] for x in rows if x.get('pair_projection_id')}
    attachment_used=set(c['attachment_projection_ids'])
    if direct_used|attachment_used != set(projections): fail('delivered projection surface must equal direct-pair plus attachment-origin projections')
    actual=[tuple(sorted((x['left_id'],x['right_id']))) for x in rows]
    if len(actual)!=len(set(actual)) or set(actual)!=expected: fail('internal pair matrix must equal n choose 2 member pairs exactly')
    counts={'DIRECT_POSITIVE':'direct_positive','DIRECT_COLLISION':'direct_collision','DIRECT_UNRESOLVED':'direct_unresolved','HIERARCHICAL_ONLY':'hierarchical_only','UNRULED':'unruled','SIGNATURE_CONFLICT':'signature_conflict','SIGNATURE_COMPATIBLE':'signature_compatible'}
    calc={v:0 for v in counts.values()}
    for x in rows: calc[counts[x['pair_state']]]+=1
    calc['expected_pairs']=len(expected)
    if calc!=c['internal_pair_counts']: fail('internal pair counts do not reconcile')
    def keys(xs): return {tuple(sorted((x['left_id'],x['right_id']))) for x in xs}
    row_by_key={tuple(sorted((x['left_id'],x['right_id']))):x for x in rows}
    if keys(p['unresolved_pairs'])!={k for k,x in row_by_key.items() if x['pair_state']=='DIRECT_UNRESOLVED'}: fail('unresolved summary mismatch')
    if keys(p['unruled_pairs'])!={k for k,x in row_by_key.items() if x['pair_state']=='UNRULED'}: fail('unruled summary mismatch')
    collisions=_exact_object_index(p['hard_collisions'],'collision_id'); obligations=_exact_object_index(p['closure_obligations'],'closure_obligation_id')
    linked_coll={z for x in rows for z in x['collision_ids']}; linked_obl={z for x in rows for z in x['closure_obligation_ids']}
    if linked_coll!=set(collisions): fail('collision links do not reconcile')
    if linked_obl!=set(obligations) or set(c['closure_obligation_ids'])!=set(obligations): fail('closure links do not reconcile')
    link_count={}
    for row in rows:
        key=tuple(sorted((row['left_id'],row['right_id'])))
        if row['pair_state'].startswith('DIRECT_') or row['pair_state']=='HIERARCHICAL_ONLY':
            if not row.get('pair_fact_id') or not row.get('pair_projection_id'):
                fail('direct candidate pair must deliver pair fact and projection')
        if row['pair_state']=='DIRECT_COLLISION' and not row.get('collision_ids'):
            fail('DIRECT_COLLISION row requires typed collision link')
        if row['pair_state']=='UNRULED' and (row.get('pair_fact_id') or row.get('pair_projection_id')):
            fail('UNRULED candidate pair cannot carry direct pair fact or projection')
        if row['pair_state']=='UNRULED':
            unr_obligations=[oid for oid in row['closure_obligation_ids'] if obligations[oid]['obligation_type']=='UNRULED_INTERNAL_PAIR']
            if len(unr_obligations)!=1:
                fail('every UNRULED internal pair must link exactly one UNRULED_INTERNAL_PAIR closure obligation')
            oid=unr_obligations[0]
            obl=obligations[oid]
            if obl['candidate_revision_id']!=c['revision_id'] or obl['authority_release_id']!=release:
                fail('closure obligation candidate or release mismatch')
            if tuple(sorted((obl['left_id'],obl['right_id'])))!=key:
                fail('closure obligation endpoints do not match linked internal pair')
            if obl['obligation_type']!='UNRULED_INTERNAL_PAIR' or obl['status']!='OPEN':
                fail('UNRULED pair requires OPEN UNRULED_INTERNAL_PAIR obligation')
        elif row['pair_state']=='SIGNATURE_COMPATIBLE' and row['closure_obligation_ids']:
            fail('SIGNATURE_COMPATIBLE row cannot carry closure obligations')
        elif row['pair_state']!='UNRULED':
            for oid in row['closure_obligation_ids']:
                obl=obligations[oid]
                if obl['status']!='OPEN':
                    fail('direct-risk closure obligation must remain OPEN in P3A packet')
                if row['pair_state']=='DIRECT_UNRESOLVED' and obl['obligation_type'] not in {'UNRESOLVED_PAIR','INCOMPLETE_SIGNATURE'}:
                    fail('DIRECT_UNRESOLVED row has incompatible closure obligation')
                if row['pair_state']=='DIRECT_COLLISION' and obl['obligation_type'] not in {'DIRECT_COLLISION','INCOMPLETE_SIGNATURE','VALUE_PORTABILITY_BOUNDARY'}:
                    fail('DIRECT_COLLISION row has incompatible closure obligation')
                if row['pair_state']=='HIERARCHICAL_ONLY' and obl['obligation_type'] not in {'MERGE_OR_SIBLING_REVIEW','INCOMPLETE_SIGNATURE','ATTACHMENT_REVIEW'}:
                    fail('HIERARCHICAL_ONLY row has incompatible closure obligation')
        for oid in row['closure_obligation_ids']:
            if oid not in obligations:
                fail('internal pair links undelivered closure obligation')
            link_count[oid]=link_count.get(oid,0)+1
    for oid,count in link_count.items():
        if count!=1:
            fail('closure obligation linked more than once')
    if set(link_count)!=set(obligations):
        fail('delivered closure obligation has no linked internal pair')
    endpoint_type_seen=set()
    for obl in obligations.values():
        key=(obl['candidate_revision_id'],tuple(sorted((obl['left_id'],obl['right_id']))),obl['obligation_type'])
        if key in endpoint_type_seen:
            fail('duplicate closure obligation for candidate/endpoints/type')
        endpoint_type_seen.add(key)
    rank=c['ranking']
    if rank['candidate_revision_id']!=c['revision_id'] or rank['authority_release_id']!=release or rank['lineage_count']!=len(members) or rank['source_count']!=len(p['members_by_source']): fail('ranking counts, revision, or release mismatch')
    density=calc['direct_positive']/len(expected) if expected else 0
    if abs(rank['direct_positive_density']-density)>1e-12: fail('ranking density mismatch')
    if not any(x['exclusion_type']=='RULE_BASED' for x in p['explicit_exclusions']): fail('rule-based exclusion required')
    variant_ids={x['variant_id'] for x in p['proposed_variants']}
    exclusion_ids={x['exclusion_id'] for x in p['explicit_exclusions']}
    if set(c['variant_ids'])!=variant_ids: fail('candidate variant_ids do not equal delivered proposed variants')
    if set(c['exclusion_ids'])!=exclusion_ids: fail('candidate exclusion_ids do not equal delivered exclusions')
    for x in p['proposed_variants']:
        if x['owner_object_id']!=c['revision_id'] or not set(x['member_ids'])<=members: fail('candidate variant owner or members mismatch')
    for x in p['explicit_exclusions']:
        if x['owner_object_id']!=c['candidate_family_id']: fail('candidate exclusion owner mismatch')
        if x['exclusion_type']=='NAMED_MEMBER' and not set(x.get('excluded_object_ids',[]))<=members: fail('named candidate exclusion references nonmember')
    components=_exact_object_index(p['origin_components'],'component_id')
    if set(c['component_ids'])!=set(components): fail('candidate component_ids do not equal delivered origin components')
    origin=c['candidate_origin_type']
    component_members=set().union(*(set(x['member_ids']) for x in components.values())) if components else set()
    for comp in components.values():
        if not set(comp['connectivity_projection_ids'])<=set(projections): fail('origin component cites undelivered projection')
    if origin in ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED'):
        expected_type='STRICT_RESPONSE_COMPONENT' if origin=='STRICT_RESPONSE_COMPONENT' else 'PROPOSITION_ONLY_COMPONENT'
        if len(components)!=1 or c['attachment_projection_ids'] or next(iter(components.values()))['component_type']!=expected_type or component_members!=members: fail('base candidate origin does not reconstruct exactly')
    elif origin=='ATTACHMENT_REVIEW':
        if not c['attachment_projection_ids']: fail('attachment candidate requires projections')
        endpoints={s for pid in c['attachment_projection_ids'] for s in (projections[pid]['left_subject_id'],projections[pid]['right_subject_id'])}
        if component_members|endpoints != members: fail('attachment candidate origin does not reconstruct exactly')
    elif origin=='NONCONNECTIVE_DIAGNOSTIC_CASE':
        if components or c['attachment_projection_ids']: fail('diagnostic origin cannot borrow connectivity')
    d=loadj(decision_path) if decision_path else p['decision_form']
    schema='adjudication_decision.schema.json' if d.get('decision_status') else 'adjudication_decision_draft.schema.json'
    validate_schema(sec,schema,d,reg)
    if d['candidate_family_id']!=c['candidate_family_id'] or d['candidate_revision_id']!=c['revision_id']: fail('decision candidate mismatch')
    if d['evidence_bundle_hash']!=p['evidence_bundle_hash'] or d['authority_release_id']!=release: fail('decision evidence/release mismatch')
    if d.get('decision_status'):
        status=d['decision_status']
        cats={
          'ACCEPT':set(d['accepted_members']),
          'EXCLUDE':set(d['excluded_members']),
          'HIERARCHICAL':{z for x in d['hierarchical_relations'] for z in (x['broader_object_id'],x['narrower_object_id']) if z in members},
          'UNRESOLVED':{z for x in d['unresolved_boundaries'] for z in (x['left_id'],x['right_id']) if z in members},
          'SPLIT':{z for x in d['split_results'] for z in x['member_ids']},
        }
        active={k:v for k,v in cats.items() if v}
        seen=set()
        for k,v in active.items():
            overlap=seen&v
            if overlap: fail(f'members assigned to multiple terminal disposition categories: {sorted(overlap)}')
            seen|=v
        if seen!=members: fail('completed decision must disposition every candidate member exactly once')
        if status=='SPLIT_REQUIRED':
            groups=[set(x['member_ids']) for x in d['split_results']]
            if len(groups)<2 or set().union(*groups)!=members or sum(map(len,groups))!=len(members): fail('split results must be disjoint and cover all members')
            ords=[x['result_ordinal'] for x in d['split_results']]
            if sorted(ords)!=list(range(1,len(ords)+1)): fail('split result ordinals must be contiguous')
            if len({x['successor_candidate_family_id'] for x in d['split_results']})!=len(groups) or len({x['successor_origin_key'] for x in d['split_results']})!=len(groups): fail('split successors and origin keys must be unique')
        if status=='HIERARCHICAL_RELATION_ONLY' and cats['HIERARCHICAL']!=members: fail('hierarchy-only decision must cover all members through hierarchy endpoints')
        if status in ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS'):
            accepted=cats['ACCEPT']; excluded=cats['EXCLUDE']
            variants_by_rev={x['variant_revision_id']:x for x in p['proposed_variants']}
            promotions={x['candidate_variant_revision_id']:x for x in d['variant_promotions']}
            if status=='ACCEPTED_WITH_VARIANTS':
                if set(promotions)!=set(variants_by_rev): fail('variant promotions must map every and only delivered candidate variant revision')
                promoted=set()
                for vr,promo in promotions.items():
                    if set(promo['member_ids'])!=set(variants_by_rev[vr]['member_ids']): fail('variant promotion members differ from candidate variant revision')
                    if promoted & set(promo['member_ids']): fail('variant promotions overlap')
                    promoted|=set(promo['member_ids'])
                if promoted!=accepted: fail('canonical variant promotions must partition accepted members')
            elif d['variant_promotions']: fail('plain canonical acceptance cannot promote candidate variants')
            ex_by_id={x['exclusion_id']:x for x in p['explicit_exclusions']}
            ex_prom={x['candidate_exclusion_id']:x for x in d['exclusion_promotions']}
            if set(ex_prom)!=set(ex_by_id): fail('exclusion promotions must map every and only delivered candidate exclusion')
            named=set()
            for eid,promo in ex_prom.items():
                source=ex_by_id[eid]
                expected_ids=set(source.get('excluded_object_ids',[]))
                if source['exclusion_type']=='RULE_BASED' and promo['excluded_member_ids']: fail('rule-based exclusion promotion cannot fabricate named members')
                if source['exclusion_type']=='NAMED_MEMBER' and set(promo['excluded_member_ids'])!=expected_ids: fail('named exclusion promotion members differ from candidate exclusion')
                named|=set(promo['excluded_member_ids'])
            if named!=excluded: fail('named exclusion promotions must cover excluded members exactly')
    return {'status':'PASS','members':len(members),'internal_pairs':len(expected),'decision_status':d.get('decision_status'),'evidence_bundle_hash':computed_hash}

if __name__=='__main__':
    try: print(json.dumps(validate_packet(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None),indent=2))
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e)},indent=2)); raise
