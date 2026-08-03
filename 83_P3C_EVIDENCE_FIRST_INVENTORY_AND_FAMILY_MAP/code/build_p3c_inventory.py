#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, re
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any
import psycopg

SPECIAL_MERGES = [
    ({160, 241}, "DEMOCRACY_SATISFACTION_WORDING_CONVERGENCE"),
    ({161, 207}, "NATIONAL_GOVERNMENT_TRUST_CONVERGENCE"),
]
PRAYER_CANDIDATES = {203, 252, 264}
DIRECT_PRAYER = {
    "p2lineage_426d1a3925832d5372cd1f71",
    "p2lineage_54355f0f436fb8696b623ecc",
    "p2lineage_e6156ffbabedac638c4d1759",
}
DERIVED_PRAYER = {"p2lineage_f0f18e2e584bc04b1b301b41"}


def cjson(v: Any) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def sha(v: Any) -> str:
    return hashlib.sha256(cjson(v).encode()).hexdigest()

def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def num_from_id(value: str) -> int:
    m = re.search(r"-(\d{6})(?:-|$)", value)
    if not m: raise ValueError(value)
    return int(m.group(1))

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--dsn', required=True)
    ap.add_argument('--lineage-registry', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args=ap.parse_args(); out=args.output_dir; out.mkdir(parents=True,exist_ok=True)
    registry={r['lineage_id']:r for r in csv.DictReader(args.lineage_registry.open(encoding='utf-8'))}
    with psycopg.connect(args.dsn) as conn:
        cand_meta={r[0]:dict(candidate_family_id=r[1], origin_type=r[2], evidence_bundle_hash=r[3], classification=r[4]) for r in conn.execute('''
          SELECT cr.candidate_revision_id,cr.candidate_family_id,cr.candidate_origin_type,cr.evidence_bundle_hash,cr.candidate_classification
          FROM p3_candidate_revision cr WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R40'
          ORDER BY cr.candidate_revision_id''')}
        cand_members=defaultdict(list)
        for rid,m,source in conn.execute('''SELECT cm.candidate_revision_id,cm.member_object_id,u.source_family
          FROM p3_candidate_membership cm LEFT JOIN p3_upstream_object_reference u ON u.object_id=cm.member_object_id
          JOIN p3_candidate_revision cr ON cr.candidate_revision_id=cm.candidate_revision_id
          WHERE cm.membership_role='PROPOSED_MEMBER' AND cr.authority_release_id='P3-AUTHORITY-2026-08-01-R40'
          ORDER BY cm.candidate_revision_id,cm.member_object_id'''):
            cand_members[rid].append((m,source))
        pair_counts=defaultdict(Counter)
        for rid,state,n in conn.execute('''SELECT candidate_revision_id,pair_state,count(*) FROM p3_internal_pair_matrix GROUP BY candidate_revision_id,pair_state'''):
            pair_counts[rid][state]=n
        obligations=defaultdict(list)
        for row in conn.execute('''SELECT closure_obligation_id,candidate_revision_id,left_object_id,right_object_id,obligation_type,status
          FROM p3_closure_obligation ORDER BY candidate_revision_id,closure_obligation_id'''):
            obligations[row[1]].append(dict(closure_obligation_id=row[0],left_object_id=row[2],right_object_id=row[3],obligation_type=row[4],status=row[5]))
        collisions=defaultdict(list)
        for row in conn.execute('''SELECT c.candidate_revision_id,c.left_object_id,c.right_object_id,c.collision_id,r.collision_type FROM p3_internal_pair_collision c JOIN p3_collision_scope_registry r USING(collision_id) ORDER BY c.candidate_revision_id,c.left_object_id,c.right_object_id'''):
            collisions[row[0]].append(dict(left_object_id=row[1],right_object_id=row[2],collision_id=row[3],collision_type=row[4]))
        hierarchy=defaultdict(list)
        for row in conn.execute("SELECT candidate_revision_id,left_object_id,right_object_id,direct_pair_projection_id FROM p3_internal_pair_matrix WHERE pair_state='HIERARCHICAL_ONLY' ORDER BY candidate_revision_id,left_object_id,right_object_id"):
            hierarchy[row[0]].append(dict(left_object_id=row[1],right_object_id=row[2],projection_id=row[3],relation_type='HIERARCHICAL_ONLY'))
        redirects=defaultdict(list)
        for row in conn.execute('''SELECT candidate_revision_id,left_object_id,right_object_id,projection_id,redirect_scope FROM p3_internal_pair_redirect_boundary ORDER BY candidate_revision_id,left_object_id,right_object_id'''):
            redirects[row[0]].append(dict(left_object_id=row[1],right_object_id=row[2],projection_id=row[3],redirect_scope=row[4]))
        unresolved=defaultdict(list)
        for row in conn.execute('''SELECT candidate_revision_id,left_object_id,right_object_id,projection_id,unresolved_boundary_type FROM p3_internal_pair_unresolved_boundary ORDER BY candidate_revision_id,left_object_id,right_object_id'''):
            unresolved[row[0]].append(dict(left_object_id=row[1],right_object_id=row[2],projection_id=row[3],unresolved_boundary_type=row[4]))
        coordinate=defaultdict(list)
        for row in conn.execute('''SELECT candidate_revision_id,left_object_id,right_object_id,projection_id,coordinate_relation_type FROM p3_internal_pair_coordinate_constraint ORDER BY candidate_revision_id,left_object_id,right_object_id'''):
            coordinate[row[0]].append(dict(left_object_id=row[1],right_object_id=row[2],projection_id=row[3],coordinate_relation_type=row[4]))

    revisions=sorted(cand_meta,key=num_from_id)
    assert len(revisions)==141, len(revisions)
    # Shared-member candidate graph.
    member_to_candidates=defaultdict(set)
    for rid,rows in cand_members.items():
        for m,_ in rows: member_to_candidates[m].add(rid)
    adj={rid:set() for rid in revisions}
    for rids in member_to_candidates.values():
        for rid in rids: adj[rid].update(rids-{rid})
    components=[]; seen=set()
    for rid in revisions:
        if rid in seen: continue
        q=[rid]; seen.add(rid); comp=[]
        while q:
            x=q.pop(); comp.append(x)
            for y in sorted(adj[x]):
                if y not in seen: seen.add(y); q.append(y)
        components.append(sorted(comp,key=num_from_id))
    component_of={rid:i for i,c in enumerate(components,1) for rid in c}

    # Union components only for independently reviewed cross-component exact propositions.
    parent={i:i for i in range(1,len(components)+1)}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[max(ra,rb)]=min(ra,rb)
    merge_rows=[]
    for nums,reason in SPECIAL_MERGES:
        rids=[f'P3CANDREV-{n:06d}-R0002' for n in sorted(nums)]
        cids={component_of[r] for r in rids}
        assert len(cids)==2,(reason,cids)
        a,b=sorted(cids); union(a,b)
        merge_rows.append(dict(merge_reason=reason,left_candidate_revision_id=rids[0],right_candidate_revision_id=rids[1],left_component_id=a,right_component_id=b))
    grouped=defaultdict(list)
    for i,c in enumerate(components,1): grouped[find(i)].extend(c)

    family_members=defaultdict(set); family_candidates=defaultdict(set); candidate_member_family={}
    for _,group in sorted(grouped.items()):
        nums={num_from_id(r) for r in group}
        if nums & PRAYER_CANDIDATES:
            assert nums==PRAYER_CANDIDATES,nums
            for rid in group:
                for m,_ in cand_members[rid]:
                    fam='JFAM-000203' if m in DIRECT_PRAYER else 'JFAM-000425' if m in DERIVED_PRAYER else None
                    assert fam,m
                    candidate_member_family[(rid,m)]=fam; family_members[fam].add(m); family_candidates[fam].add(rid)
        else:
            seed=min(nums); fam=f'JFAM-{seed:06d}'
            for rid in group:
                family_candidates[fam].add(rid)
                for m,_ in cand_members[rid]:
                    candidate_member_family[(rid,m)]=fam; family_members[fam].add(m)

    # Exact family ownership must partition all unique members.
    member_families=defaultdict(set)
    for (rid,m),fam in candidate_member_family.items(): member_families[m].add(fam)
    overlaps={m:sorted(fs) for m,fs in member_families.items() if len(fs)!=1}
    if overlaps: raise RuntimeError(f'family overlap {overlaps}')

    candidate_rows=[]; member_rows=[]; detail=[]
    for rid in revisions:
        n=num_from_id(rid); members=cand_members[rid]; fams=sorted({candidate_member_family[(rid,m)] for m,_ in members})
        if n==252:
            plan='SPLIT_REQUIRED_TO_SUCCESSORS_424_425'; primary=''
        elif n==264:
            plan='DIRECT_FAMILY_CONFIRMATION_WITH_DERIVED_NAMED_EXCLUSION'; primary='JFAM-000203'
        elif len(fams)==1:
            plan='CANONICAL_ADMISSION_OR_EXTENSION'; primary=fams[0]
        else:
            raise RuntimeError((rid,fams))
        profiles=[]; texts=[]; semantic=set(); sources=set()
        for m,source in members:
            r=registry.get(m,{})
            topo=r.get('response_topologies_json','[]'); sig=r.get('response_signatures_json','[]')
            profile=sha({'topology':json.loads(topo or '[]'),'signature':json.loads(sig or '[]')})[:16]
            profiles.append(profile); texts.append(r.get('representative_text','')); sources.add(source or r.get('source_family','UNKNOWN'))
            try: semantic.update(json.loads(r.get('semantic_content_ids_json','[]') or '[]'))
            except json.JSONDecodeError: pass
            member_rows.append(dict(candidate_revision_id=rid,candidate_family_id=cand_meta[rid]['candidate_family_id'],member_object_id=m,source_family=source or r.get('source_family','UNKNOWN'),representative_text=r.get('representative_text',''),response_topologies_json=topo,response_signatures_json=sig,response_profile_id=profile,semantic_content_ids_json=r.get('semantic_content_ids_json','[]'),final_canonical_family_id=candidate_member_family[(rid,m)],planned_member_disposition=('EXCLUDE_NAMED_BOUNDARY' if n==264 and m in DERIVED_PRAYER else 'SPLIT' if n==252 else 'DETERMINE_ACCEPT_OR_ALREADY_CANONICAL_DURING_REPLAY')))
        row=dict(candidate_revision_id=rid,candidate_family_id=cand_meta[rid]['candidate_family_id'],candidate_number=n,origin_type=cand_meta[rid]['origin_type'],classification=cand_meta[rid]['classification'],evidence_bundle_hash=cand_meta[rid]['evidence_bundle_hash'],member_count=len(members),source_count=len(sources),sources=' | '.join(sorted(sources)),shared_member_component_id=component_of[rid],final_family_ids=' | '.join(fams),primary_family_id=primary,planned_decision=plan,distinct_response_profiles=len(set(profiles)),direct_positive_count=pair_counts[rid]['DIRECT_POSITIVE'],direct_collision_count=pair_counts[rid]['DIRECT_COLLISION'],direct_unresolved_count=pair_counts[rid]['DIRECT_UNRESOLVED'],hierarchical_only_count=pair_counts[rid]['HIERARCHICAL_ONLY'],unruled_count=pair_counts[rid]['UNRULED'],open_obligation_count=sum(o['status']=='OPEN' for o in obligations[rid]),collision_surface_count=len(collisions[rid]),hierarchy_surface_count=len(hierarchy[rid]),redirect_surface_count=len(redirects[rid]),unresolved_surface_count=len(unresolved[rid]),coordinate_surface_count=len(coordinate[rid]),semantic_content_ids=' | '.join(sorted(semantic)),representative_texts=' || '.join(texts))
        candidate_rows.append(row)
        detail.append(dict(**row,members=[dict(member_object_id=m,source_family=s,registry=registry.get(m,{}),final_canonical_family_id=candidate_member_family[(rid,m)]) for m,s in members],obligations=obligations[rid],collisions=collisions[rid],hierarchy=hierarchy[rid],redirects=redirects[rid],unresolved_boundaries=unresolved[rid],coordinate_constraints=coordinate[rid],pair_state_counts=dict(pair_counts[rid])))

    family_rows=[]
    for fam in sorted(family_members,key=num_from_id):
        members=sorted(family_members[fam]); cands=sorted(family_candidates[fam],key=num_from_id)
        profiles=set(); sources=set(); semantic=set(); texts=[]
        for m in members:
            r=registry.get(m,{})
            sources.add(r.get('source_family','UNKNOWN'))
            profiles.add(sha({'topology':json.loads(r.get('response_topologies_json','[]') or '[]'),'signature':json.loads(r.get('response_signatures_json','[]') or '[]')})[:16])
            try: semantic.update(json.loads(r.get('semantic_content_ids_json','[]') or '[]'))
            except json.JSONDecodeError: pass
            if r.get('representative_text') not in texts: texts.append(r.get('representative_text'))
        family_rows.append(dict(canonical_family_id=fam,seed_candidate_number=num_from_id(fam),member_count=len(members),candidate_count=len(cands),candidate_revision_ids=' | '.join(cands),source_count=len(sources),source_families=' | '.join(sorted(sources)),distinct_response_profiles=len(profiles),semantic_content_ids=' | '.join(sorted(semantic)),representative_texts=' || '.join(texts),family_member_set_hash=sha(members)))

    component_rows=[]
    for i,comp in enumerate(components,1):
        members=sorted({m for rid in comp for m,_ in cand_members[rid]})
        component_rows.append(dict(shared_member_component_id=i,candidate_count=len(comp),candidate_revision_ids=' | '.join(comp),unique_member_count=len(members),member_set_hash=sha(members),merged_group_id=find(i)))

    summary={
      'status':'PASS', 'authority_source':'P3A_V40_RECONSTRUCTED_DATABASE_PLUS_FROZEN_P2_LINEAGE_REGISTRY',
      'original_candidate_revisions':len(revisions),'candidate_membership_occurrences':sum(len(v) for v in cand_members.values()),
      'unique_member_lineages':len(member_families),'shared_member_components':len(components),
      'shared_component_size_distribution':dict(sorted(Counter(len(c) for c in components).items())),
      'cross_component_merges':len(SPECIAL_MERGES),'prayer_component_partition_count':2,
      'final_proposition_families':len(family_rows),'multi_family_original_candidates':sum(len({candidate_member_family[(rid,m)] for m,_ in cand_members[rid]})>1 for rid in revisions),
      'multi_family_candidate_revision_ids':[rid for rid in revisions if len({candidate_member_family[(rid,m)] for m,_ in cand_members[rid]})>1],
      'open_closure_obligations':sum(sum(o['status']=='OPEN' for o in obligations[rid]) for rid in revisions),
      'collision_surfaces':sum(map(len,collisions.values())),'hierarchy_surfaces':sum(map(len,hierarchy.values())),
      'redirect_surfaces':sum(map(len,redirects.values())),'unresolved_surfaces':sum(map(len,unresolved.values())),
      'coordinate_surfaces':sum(map(len,coordinate.values())),
      'family_map_hash':sha({f:sorted(ms) for f,ms in sorted(family_members.items())}),
      'candidate_partition_hash':sha({rid:{m:candidate_member_family[(rid,m)] for m,_ in cand_members[rid]} for rid in revisions}),
      'non_authoritative_recovery_records_used_as_decision_input':False,
      'special_merges':[{'candidate_numbers':sorted(s),'reason':r} for s,r in SPECIAL_MERGES],
      'special_split':{'candidate_numbers':sorted(PRAYER_CANDIDATES),'direct_family':'JFAM-000203','derived_family':'JFAM-000425','direct_members':sorted(DIRECT_PRAYER),'derived_members':sorted(DERIVED_PRAYER)},
    }
    assert summary['original_candidate_revisions']==141
    assert summary['candidate_membership_occurrences']==496
    assert summary['shared_member_components']==112
    assert summary['final_proposition_families']==111
    assert summary['multi_family_original_candidates']==2
    assert summary['open_closure_obligations']==345

    write_csv(out/'P3C_EVIDENCE_FIRST_CANDIDATE_INVENTORY.csv',candidate_rows)
    write_csv(out/'P3C_EVIDENCE_FIRST_MEMBER_MAP.csv',member_rows)
    write_csv(out/'P3C_SHARED_MEMBER_COMPONENTS.csv',component_rows)
    write_csv(out/'P3C_FINAL_PROPOSITION_FAMILY_MAP.csv',family_rows)
    write_csv(out/'P3C_CROSS_COMPONENT_MERGE_EVIDENCE.csv',merge_rows)
    (out/'P3C_EVIDENCE_FIRST_CANDIDATE_DETAIL.json').write_text(json.dumps(detail,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    (out/'P3C_EVIDENCE_FIRST_INVENTORY_RETURN.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
