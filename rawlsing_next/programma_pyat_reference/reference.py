"""Deterministic standard-library evidence graph over seven immutable W1 returns.

All input assertions retain their author and raw scope. Navigation is association,
not proof inheritance. A source pin verifies bytes, never scientific correctness.
"""
import argparse
import collections
import hashlib
from functools import lru_cache
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CANONICAL = '9809203fd915a84bae056a67210e9213879840db'
HEX = re.compile(r'^[0-9a-f]{40}$')
TABLES = dict(zip('ABCDEFG', ['PLAN_CROSSWALK', 'CURRENT_REALIZATION', 'SEAMS',
    'SOURCE35_COVERAGE', 'WORK_AND_AUTHORITY_STATE', 'INGEST_SOURCE_MAP', 'HISTORICAL_REALIZATIONS']))
EXPECTED = dict(zip('ABCDEFG', [656, 28, 37, 35, 22, 28, 29]))
AXES = ['plan_state', 'science_state', 'engineering_state', 'code_location',
        'integration_state', 'first_consumer_state', 'review_state', 'authority_state',
        'theory_ontology_state','architecture_state','native_source_state','terminal_receiving_state']
BOUNDARY = {'scope': 'SOURCEFREE_DERIVED_REFERENCE_ONLY',
    'source_native_empirical_pilot': 'HOLD', 'adoption': 'RETURNED_UNADOPTED',
    'authority': 'NO_SOURCE_N11_N12_ACTOR_OR_CANONICAL_WRITE_GRANT',
    'navigation': 'ASSOCIATION_IS_NOT_PROOF_OR_UNCONDITIONAL_DEPENDENCY'}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


@lru_cache(maxsize=None)
def git(*args, binary=False):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    if p.returncode:
        raise ValueError(p.stderr.decode().strip())
    return p.stdout if binary else p.stdout.decode().strip()


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def validate_inputs(root=ROOT, git_check=True):
    locks = load(root / 'input_lock.json')
    if len(locks) != 39 or len({x['local'] for x in locks}) != 39:
        raise ValueError('INPUT_MANIFEST_CARDINALITY_OR_DUPLICATE')
    for x in locks:
        if not HEX.fullmatch(x['cut']) or not HEX.fullmatch(x['blob']):
            raise ValueError('MALFORMED_CONTENT_PIN')
        data = (root / x['local']).read_bytes()
        blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
        if blob != x['blob'] or hashlib.sha256(data).hexdigest() != x['sha256']:
            raise ValueError('INPUT_EVIDENCE_TAMPER: ' + x['local'])
        if git_check and (git('rev-parse', x['cut'] + ':' + x['path']) != blob or
                          git('show', x['cut'] + ':' + x['path'], binary=True) != data):
            raise ValueError('GIT_CONTENT_PIN_MISMATCH: ' + x['path'])
    return locks


def identity(label, lane='A'):
    """Only demonstrable stable namespaces join. Other lane labels stay provisional."""
    if label.startswith('PYAT:') or label.startswith('CODE:') or label.startswith('ROW:'):
        return label
    if label in ['PROGRAMMA_PYAT', 'PROGRAMMA_RAWLSING', 'PRE-V3', 'V3']:
        return 'PYAT:PROGRAM:' + label
    if re.fullmatch(r'N(?:[0-9]|1[0-3])(?:E|W|S)?', label):
        return 'PYAT:ASTRA:' + label
    if re.fullmatch(r'F[1-8]', label):
        return 'PYAT:FUNCTION:' + label
    if re.fullmatch(r'SRC\d{2}', label):
        return 'PYAT:SOURCE:' + label
    if re.fullmatch(r'(EE|AT)\d{2}|WG[0-4]', label):
        return 'PYAT:' + label
    if label.startswith(('WHOLE151:', 'WHOLE101:', 'ESTATE_AXIS:', 'ASTRA:')):
        return 'PYAT:' + label
    if lane == 'A':
        return 'PYAT:PLAN:' + label
    return f'PYAT:UNMAPPED_OR_AMBIGUOUS:{lane}:' + label


def maturity_for(lane,row):
    axes={k:row.get(k,'UNKNOWN_NOT_ASSERTED') for k in AXES}
    if lane=='B' and 'requirement_id' in row:
        axes.update(engineering_state=row['status'],code_location={'cut':row['ref'],'path':row.get('path'),'symbol':row.get('symbol'),'blob':row.get('blob')},
            integration_state={'location':row['main_or_premain_or_pending'],'limit':'Code presence at that cut; no receiver/adoption scope inferred'},
            first_consumer_state={'located':row.get('first_consumer'),'limit':'Returned static/caller claim; no H native invocation'},
            review_state={'returned_grade':row.get('reviewer_grade'),'tests':row.get('test_status'),'scope':'Inherited receipt, not H independent runtime acceptance'},
            science_state='NO_SOURCE_SCIENCE_ISSUED_BY_THIS_REFERENCE',authority_state='SOURCEFREE_CODE_IS_NOT_NATIVE_GRANT')
    elif lane=='D' and 'source_id' in row:
        axes.update(science_state=row['science_issued_eligible_operations'],
            native_source_state=row['original_per_operation_permission'],
            first_consumer_state=row['actual_measured_product'],authority_state=row['producer_hold'])
    elif lane=='G' and 'exact_source' in row:
        axes.update(engineering_state={'supported_returned_behavior':row['supported_behavior'],'limit':row['limits']},
            code_location=row['exact_source'],integration_state=row['modern_equivalent'],
            first_consumer_state=row['test_consumer_evidence'],authority_state=row['negative_owner'])
    elif lane=='F':
        axes.update(plan_state='PROPOSED_REFERENCE_DESIGN',engineering_state='NOT_OPERATIVE_IN_W1_F',authority_state='NO_ISSUANCE')
    # Unknown theory/ontology/terminal axes remain unknown; architecture never completes a child.
    return axes


def pins_for(lane, row):
    """Extract only explicit owning-cut/path pairs, never infer from a display label."""
    pins = []
    def add(cut, path, expected=None, role='source'):
        if isinstance(path, list):
            for p in path: add(cut, p, None, role)
        elif isinstance(path, str) and path:
            pins.append({'cut': cut, 'path': path, 'expected_blob': expected if isinstance(expected,str) and HEX.fullmatch(expected) else None, 'role': role})
    add(row.get('source_cut'), row.get('source_path'), row.get('source_blob_sha') or row.get('blob_sha'))
    if lane == 'B' and 'requirement_id' in row:
        add(row['ref'], row.get('path'), row.get('blob'), 'implementation')
        add(row['ref'], row.get('first_consumer', {}).get('path'), role='static_consumer')
        for p in row.get('test_files', []): add(row['ref'], p, role='reported_test')
    if lane == 'C':
        for x in row.get('source_evidence', []): add(x.get('git_sha'), x.get('path'), x.get('blob_sha'), 'exact_seam_source')
    if lane == 'D' and 'historical_snapshot' in row:
        h = row['historical_snapshot']
        for x in h.get('config_blob_paths', []): add(h.get('documentary_release_cut'), x.get('path'), x.get('blob_sha'), 'historical_configuration')
        for x in row.get('evidence', []): add(x.get('cut'), x.get('path'))
    if lane == 'F' and isinstance(row.get('source'), dict):
        x = row['source'];add(x.get('source_cut'),x.get('source_path'),x.get('blob_sha'),'proposed_ingest_source')
    if lane == 'G' and 'exact_source' in row:
        sources=[(row.get('exact_source',{}),'historical_variant'),(row.get('modern_equivalent',{}),'current_comparison')]
        sources.extend((x,'historical_alternative') for x in row.get('related_sources',[]))
        sources.extend((x,'historical_alternative') for x in row.get('exact_source',{}).get('related_refs',[]))
        for x,role in sources:
            for p in x.get('paths',[]):add(x.get('tip') or x.get('current_cut'),p.get('path'),p.get('blob'),role)
    return pins


def check_pin(pin):
    result = dict(pin)
    result['id'] = 'PIN:' + digest(pin)[:24]
    if not isinstance(pin['cut'], str) or not HEX.fullmatch(pin['cut']):
        result.update(status='UNRESOLVED_NONIMMUTABLE_REFERENCE', observed_blob=None)
        return result
    try:
        git('cat-file','-e',pin['cut']+'^{commit}')
    except ValueError:
        result.update(status='COMMIT_OBJECT_UNAVAILABLE',observed_blob=None)
        return result
    try:
        blob = git('rev-parse', pin['cut'] + ':' + pin['path'])
        data = git('show', pin['cut'] + ':' + pin['path'], binary=True)
        result.update(observed_blob=blob, content_sha256=hashlib.sha256(data).hexdigest(),
            status='VERIFIED' if not pin['expected_blob'] or pin['expected_blob'] == blob else 'BLOB_MISMATCH')
    except ValueError:
        result.update(status='UNAVAILABLE_AT_DECLARED_CUT', observed_blob=None)
    return result


def build(cut=CANONICAL, root=ROOT, git_check=True):
    if not HEX.fullmatch(cut): raise ValueError('CUT_MUST_BE_EXACT_40HEX')
    if git_check: git('cat-file','-e',cut+'^{commit}')
    locks = validate_inputs(root,git_check)
    records, entities, edges, pin_cache = {}, {}, {}, {}
    alias = collections.defaultdict(set)
    def entity(label, lane='A', kind='component'):
        eid = identity(label,lane)
        entities.setdefault(eid, {'id':eid,'label':label,'kind':kind,'definition':'REFERENCED_ONLY','records':[]})
        alias[label].add(eid)
        return eid
    def edge(a,b,kind,rid,condition=None):
        obj={'from':a,'to':b,'type':kind,'record':rid,'condition':condition}
        obj['id']='EDGE:'+digest(obj)[:24];edges[obj['id']]=obj
    def code(path, symbol, at, rid, kind):
        if not path: return None
        eid='CODE:'+str(at)+':'+path+'::'+str(symbol or '')
        entities.setdefault(eid,{'id':eid,'label':path+'::'+str(symbol or ''),'kind':'code_symbol','cut':at,'records':[],'definition':'EXPLICIT_SOURCE_POINTER'})
        entities[eid]['records'].append(rid)
        edge(rid,eid,kind,rid)
        return eid
    for lane,table in TABLES.items():
        for table_name in [table,'ATOMIC_FINDINGS']:
            item=next(x for x in locks if x['lane']==lane and x['path'].endswith('/'+table_name+'.jsonl'))
            rows=[json.loads(s) for s in (root/item['local']).read_text().splitlines()]
            if table_name==table and len(rows)!=EXPECTED[lane]: raise ValueError('ROW_COUNT:'+lane)
            for number,row in enumerate(rows,1):
                oid=row.get('record_id') or row.get('requirement_id') or row.get('work_id') or row.get('id')
                if not oid: raise ValueError('MISSING_ORIGINAL_RECORD_ID')
                rid=f'ROW:{lane}:{table_name}:{oid}'
                if rid in records: raise ValueError('DUPLICATE_RECORD_ID:'+rid)
                pins=[]
                for p in pins_for(lane,row):
                    k=canonical(p)
                    if k not in pin_cache: pin_cache[k]=check_pin(p) if git_check else dict(p,id='PIN:'+digest(p)[:24],status='NOT_CHECKED')
                    pins.append(pin_cache[k]['id'])
                records[rid]={'id':rid,'original_id':oid,'lane':lane,'table':table_name,'raw':row,
                    'evidence':{'cut':item['cut'],'path':item['path'],'blob':item['blob'],'line':number},
                    'support_pins':sorted(set(pins)), 'maturity':maturity_for(lane,row),
                    'scope':'ENGINEER_RETURN_NOT_H_INDEPENDENT_ACCEPTANCE',
                    'currentness':row.get('currentness','UNKNOWN'),
                    'negative':row.get('limit_or_counterevidence') or row.get('limits') or row.get('missing_subrequirements') or row.get('next_dependency') or 'UNKNOWN_NOT_ASSERTED'}
                alias[str(oid)].add(rid)
                labels=row.get('stable_ids') or row.get('stable_component_ids') or row.get('related_ids') or []
                if lane=='A' and table_name==table: labels=[row['stable_component_id']]
                if lane=='D' and table_name==table: labels=[row['source_id']]
                for label in labels:
                    if not isinstance(label,str):continue
                    eid=entity(label,lane)
                    entities[eid]['records'].append(rid)
                    edge(eid,rid,'HAS_ASSERTION',rid)
                    if lane=='A' and table_name==table:
                        entities[eid]['definition']='DOCUMENTED_PLAN_ID'
                if lane=='A' and table_name==table:
                    current=entity(row['stable_component_id'])
                    prerequisite=row['edge_type'] in ['UNCONDITIONAL_PREREQUISITE','CONDITIONAL_PREREQUISITE']
                    for parent in row['parent_ids']:
                        edge(entity(parent),current,row['edge_type'] if prerequisite else 'DECOMPOSES_TO',rid,row.get('edge_condition') if prerequisite else None)
                    if not prerequisite:
                        for child in row['child_ids']:edge(current,entity(child),'DECOMPOSES_TO',rid)
                    for member in row['cross_membership_ids']:edge(entity(member),current,'CROSS_MEMBERSHIP_NOT_IDENTITY',rid)
                    for alt in row['alternative_ids']:edge(current,entity(alt),'ALTERNATIVE_DECOMPOSITION_NOT_EQUIVALENCE',rid)
                elif lane=='B' and table_name==table:
                    producer=code(row.get('path'),row.get('symbol'),row['ref'],rid,'REALIZATION_LOCATION')
                    c=row.get('first_consumer',{})
                    caller=code(c.get('path'),c.get('symbol'),row['ref'],rid,'LOCATED_STATIC_CONSUMER')
                    if producer and caller:edge(caller,producer,'AUTHOR_REPORTED_STATIC_CALL_NOT_RUNTIME',rid,c.get('grade'))
                elif lane=='C' and table_name==table:
                    for field in ['producer_code','receiver_code']:
                        s=row.get(field)
                        if not isinstance(s,str) or '::' not in s:continue
                        path,symbol=s.split('::',1)
                        cut_key='producer_cut' if field=='producer_code' else 'receiver_cut'
                        at=row.get('currentness',{}).get(cut_key)
                        code(path,symbol,at,rid,field.upper())
                elif lane=='G' and table_name==table:
                    sources=[(row.get('exact_source',{}),'HISTORICAL_VARIANT'),(row.get('modern_equivalent',{}),'CURRENT_COMPARISON')]
                    sources.extend((x,'HISTORICAL_ALTERNATIVE') for x in row.get('related_sources',[]))
                    sources.extend((x,'HISTORICAL_ALTERNATIVE') for x in row.get('exact_source',{}).get('related_refs',[]))
                    for x,kind in sources:
                        for p in x.get('paths',[]):code(p['path'],None,x.get('tip') or x.get('current_cut'),rid,kind)
    # H reconciliation binds exact retained rows; it is not another authority layer.
    for line in (root/'adjudication.jsonl').read_text().splitlines():
        raw=json.loads(line);rid='ROW:H:ADJUDICATION:'+raw['id']
        related=raw['related_records']
        if any(x not in records for x in related):raise ValueError('ADJUDICATION_REF_MISMATCH:'+rid)
        records[rid]={'id':rid,'original_id':raw['id'],'lane':'H','table':'ADJUDICATION','raw':raw,
            'evidence':{'derived_from':related},'support_pins':sorted({p for x in related for p in records[x]['support_pins']}),
            'maturity':{k:raw.get(k,'UNKNOWN_NOT_ASSERTED') for k in AXES},
            'scope':'SOURCEFREE_CROSS_LANE_ADJUDICATION_NOT_ACCEPTANCE','currentness':raw['currentness'],
            'negative':raw['limit_or_counterevidence']}
        alias[raw['id']].add(rid)
        for label in raw['stable_ids']:
            eid=entity(label);entities[eid]['records'].append(rid);edge(eid,rid,'HAS_ASSERTION',rid)
        for target in related:edge(rid,target,'RECONCILES_WITHOUT_PROMOTION',rid)
    for line in (root/'navigation_links.jsonl').read_text().splitlines():
        link=json.loads(line);rid=link['support']
        if rid not in records:raise ValueError('LINK_REF_MISMATCH')
        edge(link['source'] if link['source'] in records else entity(link['source']),
             link['target'] if link['target'] in records else entity(link['target']),link['type'],rid,
            {'scope':link['condition'],'negative':link['negative']})
    # Every unmatched record stays navigable without claiming a semantic join.
    linked_records={e['to'] for e in edges.values() if e['type']=='HAS_ASSERTION'}
    for rid,r in records.items():
        if rid not in linked_records:
            eid=entity(r['original_id'],r['lane'],kind='unmapped_record_anchor')
            entities[eid]['records'].append(rid)
            edge(eid,rid,'UNMAPPED_OR_AMBIGUOUS',rid,'No source-grounded stable component join supplied')
    # Explicitly different meanings of M2. Bare M2 is always ambiguous.
    for label in ['M2_LOCAL_RELEASE','M2_V555_STRUCTURAL']:
        eid=entity(label,kind='disambiguated_namespace')
        alias['M2'].add(eid)
    for e in entities.values():e['records']=sorted(set(e['records']))
    pin_by_id={x['id']:x for x in pin_cache.values()}
    cut_comparison={}
    path_cache={}
    for pid,pin in sorted(pin_by_id.items()):
        path=pin['path']
        if path not in path_cache:
            try: path_cache[path]=git('rev-parse',cut+':'+path) if git_check else None
            except ValueError:path_cache[path]=None
        blob=path_cache[path]
        cut_comparison[pid]={'selected_cut':cut,'path':path,'selected_blob':blob,
            'declared_cut':pin['cut'],'declared_blob':pin.get('observed_blob'),
            'state':'ABSENT_AT_SELECTED_CUT' if blob is None else
                'SAME_BYTES' if blob==pin.get('observed_blob') else 'DIFFERENT_BYTES',
            'limit':'Byte comparison only; no adoption, authority or behavior equivalence inferred.'}

    for r in records.values():
        r['evidence_state']='PINNED_RETURN_AND_SOURCE_CHECKED' if all(pin_by_id[x]['status']=='VERIFIED' for x in r['support_pins']) and r['support_pins'] else 'RETURN_PINNED__SOURCE_PARTIAL_OR_UNKNOWN'
    coverage={lane:{'primary_table':TABLES[lane],'rows':sum(r['lane']==lane and r['table']==TABLES[lane] for r in records.values()),
        'atomic_findings':sum(r['lane']==lane and r['table']=='ATOMIC_FINDINGS' for r in records.values())} for lane in TABLES}
    linked={e['to'] for e in edges.values() if e['type']=='HAS_ASSERTION'}
    orphans=sorted(set(records)-linked)
    coverage.update(raw_rows_total=sum(r['lane']!='H' for r in records.values()),h_adjudications=sum(r['lane']=='H' for r in records.values()),assertion_unlinked_records=orphans,
        assertion_unlinked_count=len(orphans), typed_entity_count=len(entities),
        a_distinct_component_ids=len({r['raw']['stable_component_id'] for r in records.values() if r['table']=='PLAN_CROSSWALK'}),
        provisional_entities=sorted(e for e in entities if ':UNMAPPED_OR_AMBIGUOUS:' in e),
        source_pin_status=dict(collections.Counter(x['status'] for x in pin_cache.values())),
        counting_rule='ROWS_ARE_NOT_UNIQUE_COMPONENTS; FINDINGS_NOT_TEST_COUNTS; NO_COMPLETION_PERCENT')
    result={'schema':'PROGRAMMA_PYAT_REFERENCE@1','cut':cut,'frozen_canonical':CANONICAL,
        'boundary':BOUNDARY,'input_lock':locks,'records':records,'entities':entities,
        'edges':edges,'aliases':{k:sorted(v) for k,v in sorted(alias.items())},
        'source_pins':pin_by_id,'read_cut_comparison':cut_comparison,'coverage':coverage,
        'proposed_f_contract':load(root/'inputs/F/GRAPH_REFERENCE_CONTRACT.json'),
        'h_normalization_hash':digest({'adjudication':(root/'adjudication.jsonl').read_text(),'navigation':(root/'navigation_links.jsonl').read_text()})}
    result['snapshot_hash']=digest(result)
    return result


def resolve(s, token):
    if token in s['records'] or token in s['entities']:return [token]
    candidates=s['aliases'].get(token,[])
    entities=[x for x in candidates if x in s['entities']]
    # Stable entity shorthand wins over same-spelled original row ID (SRCxx).
    # Multiple entity meanings remain ambiguous; raw rows use ROW:lane:table:id.
    return entities if entities else candidates


def regrade(s, unavailable=()):
    """Read-only evidence withdrawal. No source permission or native grade is issued."""
    unknown=set(unavailable)-set(s['source_pins'])
    if unknown:raise ValueError('UNKNOWN_PIN:'+','.join(sorted(unknown)))
    # The same immutable pointer can be declared in multiple roles. Withdraw all
    # roles of that pointer together, including each derived H dependent claim.
    pointers={(s['source_pins'][p]['cut'],s['source_pins'][p]['path']) for p in unavailable}
    affected={p for p,x in s['source_pins'].items() if (x['cut'],x['path']) in pointers}
    return {rid:('HELD_EVIDENCE_UNAVAILABLE' if set(r['support_pins']) & affected else r['evidence_state']) for rid,r in s['records'].items()}


def permit_promotion(*, author, reviewer, appointed, source_scope, target_scope):
    # This reference has no issuing or adoption endpoint, even for distinct reviewers.
    if author==reviewer:raise ValueError('SELF_REVIEW_FORBIDDEN')
    if not appointed:raise ValueError('REVIEWER_APPOINTMENT_UNVERIFIED')
    if source_scope=='SYNTHETIC' and target_scope=='NATIVE':raise ValueError('SYNTHETIC_NATIVE_PROMOTION_FORBIDDEN')
    raise ValueError('REFERENCE_IS_NONISSUING')


def select_edges(s, ids, direction='both', depth=1, unconditional=False):
    selected={};front=set(ids);seen=set(ids)
    for _ in range(depth):
        nxt=set()
        for eid,e in s['edges'].items():
            if unconditional and e['type']=='CONDITIONAL_PREREQUISITE':continue
            match=(direction in ['both','forward'] and e['from'] in front) or (direction in ['both','reverse'] and e['to'] in front)
            if match:
                selected[eid]=e;nxt.update([e['from'],e['to']])
        front=nxt-seen;seen.update(nxt)
    return [selected[k] for k in sorted(selected)]


def query(s, command, token=None, depth=1, unconditional=False, brief=False):
    base={'command':command,'snapshot_hash':s['snapshot_hash'],'cut':s['cut'],'boundary':s['boundary']}
    if command=='whole':
        base.update(coverage=s['coverage'],terminal_nodes=[s['entities'][identity(n)] for n in ['PROGRAMMA_PYAT','N9','N10E','N10W','N11','N12']],
                    structural_gaps=[r for r in s['records'] if r.startswith('ROW:C:SEAMS:') and s['records'][r]['raw']['missing_adapter'] not in ['NONE','None',None,'']],
                    note='Read gaps for exact missing edges/owners; no row-count priority or percentage.',
                    high_impact_missing_edges=[{'id':r['id'],'upstream':r['raw']['upstream'],'downstream':r['raw']['downstream'],
                        'missing':r['raw']['missing_adapter'],'authority':r['raw']['authority'],
                        'qualified_input':r['raw']['qualified_input'],'source':r['evidence'],
                        'source_pins':r['support_pins'],'currentness':r['currentness'],'negative':r['negative']}
                        for r in s['records'].values() if r['original_id'] in
                        ['W1C-S02','W1C-S03','W1C-S04','W1C-S26','W1C-S27','W1C-S29','W1C-S32','W1C-S35','W1C-S36']])
        return base
    if command=='work-now':
        base.update(records=[r for r in s['records'].values() if r['table']==TABLES['E']],
                    next_action='Read exact held source/config-to-eligible-frontier seam W1C-S02/S03/S04; reuse governed lowering. Any native step still requires its issued source/host/purpose/operation grant.',
                    process_state='UNKNOWN; frozen issue/branch is not a local process lease')
        return base
    ids=resolve(s,token) if token else []
    if token and not ids:return dict(base,status='UNKNOWN_ID',token=token)
    if len(ids)>1:return dict(base,status='AMBIGUOUS_ID',token=token,candidates=ids)
    related=set(ids)
    edges=select_edges(s,ids,'reverse' if command=='reverse' else 'both',depth,unconditional)
    for e in edges:related.update([e['from'],e['to'],e['record']])
    for eid in list(related):
        if eid in s['entities']:related.update(s['entities'][eid]['records'])
    rows=[s['records'][r] for r in sorted(related) if r in s['records']]
    if command=='gaps':
        rows=rows if token else list(s['records'].values())
        rows=[r for r in rows if r['negative']!='UNKNOWN_NOT_ASSERTED']
    elif command=='seams':rows=[r for r in rows if r['table']=='SEAMS']
    elif command=='alternatives':rows=[r for r in rows if r['table']=='HISTORICAL_REALIZATIONS' or r['table']=='CURRENT_REALIZATION' or r['table']=='PLAN_CROSSWALK' and r['raw']['alternative_ids']]
    elif command=='code':rows=[r for r in rows if r['lane'] in ['B','C','G'] and r['table']!='ATOMIC_FINDINGS']
    # Include exact-code edges of selected records in code view, without proof rollup.
    if command=='code':
        known={e['id'] for e in edges}
        row_ids={r['id'] for r in rows}
        edges.extend(e for e in s['edges'].values() if e['record'] in row_ids and e['id'] not in known)
    if brief:
        rows=[{k:r[k] for k in ['id','evidence','support_pins','currentness','negative','maturity','evidence_state']} for r in rows]
    base.update(status='OK',ids=ids,records=rows,edges=edges,
                source_pins={p:s['source_pins'][p] for r in rows for p in r['support_pins']},
                read_cut_comparison={p:s['read_cut_comparison'][p] for r in rows for p in r['support_pins']})
    return base


def trace(s,tokens):
    ids=[]
    for token in tokens:
        resolved=resolve(s,token)
        if len(resolved)!=1:raise ValueError('TRACE_ID_UNKNOWN_OR_AMBIGUOUS:'+token)
        ids.append(resolved[0])
    hops=[]
    for a,b in zip(ids,ids[1:]):
        matches=[e for e in s['edges'].values() if {e['from'],e['to']}=={a,b}]
        if not matches:raise ValueError('NO_SOURCE_GROUNDED_EDGE:'+a+' -> '+b)
        hops.append({'from':a,'to':b,'edges':sorted(matches,key=lambda e:e['id']),
            'proof_scope':'NAVIGATION_ONLY; read each edge type/condition, including missing edges'})
    return {'ids':ids,'hops':hops,'reverse_uses_same_edge_ids':True}


def verify(s,root=ROOT):
    expected=s.get('snapshot_hash');copy=dict(s);copy.pop('snapshot_hash',None)
    if digest(copy)!=expected:raise ValueError('SNAPSHOT_CONTENT_TAMPER')
    validate_inputs(root)
    rebuilt=build(s['cut'],root)
    if rebuilt!=s:raise ValueError('SNAPSHOT_REPLAY_MISMATCH')
    for e in s['edges'].values():
        if e['from'] not in s['entities'] and e['from'] not in s['records']:raise ValueError('REF_MISMATCH')
        if e['to'] not in s['entities'] and e['to'] not in s['records']:raise ValueError('REF_MISMATCH')
    return {'status':'SOURCEFREE_MAP_STRUCTURE_AND_IMMUTABLE_REPLAY_PASS','snapshot_hash':expected,
            'source_pins':s['coverage']['source_pin_status'],'boundary':BOUNDARY}


def changes(old,new):
    result={'old_cut':old['cut'],'new_cut':new['cut'],'old_hash':old['snapshot_hash'],'new_hash':new['snapshot_hash']}
    for field in ['records','edges','entities','source_pins','read_cut_comparison']:
        a,b=old[field],new[field]
        changed=[]
        for k in set(a)&set(b):
            if field=='read_cut_comparison':
                differs=(a[k].get('selected_blob'),a[k].get('state'))!=(b[k].get('selected_blob'),b[k].get('state'))
            else:differs=a[k]!=b[k]
            if differs:changed.append(k)
        result[field]={'added':sorted(set(b)-set(a)),'removed':sorted(set(a)-set(b)),'changed':sorted(changed)}
    result['interpretation']='PINNED_SEVEN_LANES_RETAIN_THEIR_OWN_CUTS; selected cut is a read context, not a new source census'
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store',type=Path,default=Path('/tmp/programma-pyat-reference'))
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('ingest');p.add_argument('--cut',required=True)
    sub.add_parser('verify')
    sub.add_parser('whole');sub.add_parser('work-now')
    for command in ['focus','reverse','code','seams','gaps','alternatives','source']:
        p=sub.add_parser(command);p.add_argument('id',nargs='?' if command=='gaps' else None)
        p.add_argument('--route',nargs='+');p.add_argument('--depth',type=int,default=1);p.add_argument('--unconditional',action='store_true');p.add_argument('--brief',action='store_true')
    p=sub.add_parser('changes');p.add_argument('oldCut');p.add_argument('newCut')
    args=parser.parse_args(argv)
    try:
        if args.command=='ingest':
            s=build(args.cut);write(args.store/(args.cut+'.json'),s);write(args.store/'latest.json',{'cut':args.cut})
            result={'status':'INGESTED','snapshot_hash':s['snapshot_hash'],'coverage':s['coverage'],'boundary':BOUNDARY}
        elif args.command=='changes':result=changes(load(args.store/(args.oldCut+'.json')),load(args.store/(args.newCut+'.json')))
        else:
            s=load(args.store/(load(args.store/'latest.json')['cut']+'.json'))
            # Fail closed on accidental or malicious persisted-view modification.
            check=dict(s);h=check.pop('snapshot_hash',None)
            if digest(check)!=h:raise ValueError('SNAPSHOT_CONTENT_TAMPER')
            if args.command=='verify':result=verify(s)
            else:
                result=query(s,args.command,getattr(args,'id',None),getattr(args,'depth',1),getattr(args,'unconditional',False),getattr(args,'brief',False))
                if getattr(args,'route',None):result['actual_route']=trace(s,[args.id]+args.route)
        print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    except (ValueError,KeyError,OSError) as error:
        print(json.dumps({'status':'ERROR','error':str(error),'boundary':BOUNDARY}),file=sys.stderr);return 2
    return 0

if __name__=='__main__':sys.exit(main())
