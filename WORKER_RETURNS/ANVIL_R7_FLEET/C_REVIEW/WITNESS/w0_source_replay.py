#!/usr/bin/env python3
"""Independent replay of the 118 identity source universe from exact Git bytes and
the original supplied ZIP. No candidate inventory is trusted for existence/counts;
candidate inventory is compared after independent extraction."""
import hashlib, json, pathlib, re, subprocess, zipfile

REPO = '/Users/matthewsmith/s2b-work/rawlsing'
K3 = '7fc00289dd801d2d0a8ce159986c7595fc27a4d9'
ZIP = '/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT = ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
OUT = ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W0_SOURCE_REPLAY'
OUT.mkdir(parents=True, exist_ok=True)

def sh(*args):
    return subprocess.run(args, capture_output=True, check=True).stdout

def git_show(commit, path):
    return sh('git','-C',REPO,'show',f'{commit}:{path}')

def sha(b): return hashlib.sha256(b).hexdigest()

files = {
 'K3_CAP_29.tsv': (K3, 'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv'),
 'K3_PC_26.tsv': (K3, 'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/K3_R15_26_OWNER_DECISIONS.tsv'),
 'K3_P4R_14.tsv': (K3, 'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/K3_P4R_14_OBLIGATION_ROUTES.tsv'),
 'SEAM_25.md': ('596f1230258ff50f98d8543dec42a80e696720f4','SEAM/25_RETURN_TO_BOUNDARY_TRANSFORMATIONS_AND_OPEN_REGISTER_R1.md'),
 'SEAM_26.md': ('796452b8cb788fa5a02f37a7ce86eafce8312dfe','SEAM/26_CONDITIONED_SOCIAL_FIELD_IDENTIFICATION_AND_GENERATIVE_PERSON_REVERSE_CONTRACT_R1.md'),
 'ANVIL_15.md': ('3cc09bba3d0e26c226da0ddca4b64c43dd74e493','PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ANVIL/15_SEAM_REVERSE_CONSUMER_SOCIAL_FIELD_AND_C11_DESIGN_IMPLICATIONS_R1.md'),
}
bodies = {}
meta = {}
for name,(commit,path) in files.items():
    b = git_show(commit,path)
    blob = sh('git','-C',REPO,'rev-parse',f'{commit}:{path}').decode().strip()
    bodies[name]=b
    meta[name]={'commit':commit,'git_path':path,'git_blob':blob,'sha256':sha(b),'bytes':len(b)}

def tsv(name):
    text = bodies[name].decode('utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    header = lines[0].split('\t')
    rows = [dict(zip(header,l.split('\t'))) for l in lines[1:]]
    return header, rows, lines

cap_h, cap, cap_lines = tsv('K3_CAP_29.tsv')
pc_h, pc, pc_lines = tsv('K3_PC_26.tsv')
p4_h, p4, p4_lines = tsv('K3_P4R_14.tsv')

md25 = bodies['SEAM_25.md'].decode('utf-8')
md26 = bodies['SEAM_26.md'].decode('utf-8')
md15 = bodies['ANVIL_15.md'].decode('utf-8')
b_lines = [l.strip() for l in md25.splitlines() if l.strip().startswith('| **B-') or l.strip().startswith('|**B-')]
s_lines = [l.strip() for l in md26.splitlines() if l.strip().startswith('| **S-') or l.strip().startswith('|**S-')]
l_lines = [l.strip() for l in md15.splitlines() if l.strip().startswith('| **L-') or l.strip().startswith('|**L-')]

with zipfile.ZipFile(ZIP) as z:
    bc = json.loads(z.read('ANVIL_R7/02_BOUNDARY_CONTRACTS.json'))
    fc = json.loads(z.read('ANVIL_R7/03_FROZEN_SOURCE_CUTS.json'))
T = [b['id'] for b in bc['boundaries']]
TERM = fc['mandatory']['TERMINAL']

inv = json.loads((INT/'EVIDENCE/SOURCE_IDENTITY_INVENTORY.json').read_text())
inv_ids = {e['id']:e for e in inv['entries']}
true_ids = set(cap[0].get('capability_id') for cap in [cap][0]) if False else set()
# actual IDs
ids_cap = [r['capability_id'] for r in cap]
ids_pc = [r['proposal_id'] for r in pc]
ids_p4 = [r['P4R_id'] for r in p4]
ids_b = [re.search(r'\*\*(B-\d\d)',l).group(1) for l in b_lines]
ids_s = [re.search(r'\*\*(S-\d\d)',l).group(1) for l in s_lines]
ids_l = [re.search(r'\*\*(L-\d\d)',l).group(1) for l in l_lines]
all_ids = ids_cap+ids_pc+ids_p4+ids_b+ids_s+ids_l+T+TERM

# Candidate source excerpts vs exact true lines. K3 excerpt should be one raw line; B/S/L exact line; T quote fragment.
replay = {}
for group, ids, source, lines in (
    ('K1_CAP',ids_cap,'K3_CAP_29.tsv',cap_lines[1:]),
    ('PYAT_PC',ids_pc,'K3_PC_26.tsv',pc_lines[1:]),
    ('P4R',ids_p4,'K3_P4R_14.tsv',p4_lines[1:])):
    line_by_id = {}
    for l in lines:
        line_by_id[l.split('\t',1)[0]] = l
    for rid in ids:
        e = inv_ids.get(rid)
        assert e is not None, rid
        exact = e['source_excerpt']
        ok = exact == line_by_id[rid]
        replay[rid] = {'group':group,'source_file':source,'source_excerpt_exact_raw_row':ok,'origin_sha256_matches_excerpt':sha(exact.encode())==e['origin_sha256']}
for group, ids, source, lines in (
    ('SEAM_B',ids_b,'SEAM_25.md',b_lines),
    ('SEAM_S',ids_s,'SEAM_26.md',s_lines),
    ('ANVIL_L',ids_l,'ANVIL_15.md',l_lines)):
    line_by_id = {re.search(r'\*\*([BSL]-\d\d)',l).group(1):l for l in lines}
    for rid in ids:
        e = inv_ids.get(rid); assert e is not None, rid
        exact = e['source_excerpt']
        ok = exact == line_by_id[rid]
        replay[rid] = {'group':group,'source_file':source,'source_excerpt_exact_raw_row':ok,'origin_sha256_matches_excerpt':sha(exact.encode())==e['origin_sha256']}
for rid in T:
    e=inv_ids.get(rid); assert e is not None, rid
    replay[rid]={'group':'BOUNDARY','source_file':'02_BOUNDARY_CONTRACTS.json','source_excerpt_in_member':e['source_excerpt'].encode() in zipfile.ZipFile(ZIP).read('ANVIL_R7/02_BOUNDARY_CONTRACTS.json')}
for rid in TERM:
    e=inv_ids.get(rid); assert e is not None, rid
    replay[rid]={'group':'TERMINAL','source_file':'03_FROZEN_SOURCE_CUTS.json','source_excerpt_in_member':e['source_excerpt'].encode() in zipfile.ZipFile(ZIP).read('ANVIL_R7/03_FROZEN_SOURCE_CUTS.json')}

report = {
 'schema':'C_REVIEW_SOURCE_REPLAY_W0',
 'original_zip_sha256':sha(pathlib.Path(ZIP).read_bytes()),
 'git_files':meta,
 'counts_actual':{
   'K1_CAP':len(ids_cap),'PYAT_PC':len(ids_pc),'P4R':len(ids_p4),
   'SEAM_B':len(ids_b),'SEAM_S':len(ids_s),'ANVIL_L':len(ids_l),
   'BOUNDARY':len(T),'TERMINAL':len(TERM),'TOTAL':len(all_ids)},
 'ids':{'K1_CAP':ids_cap,'PYAT_PC':ids_pc,'P4R':ids_p4,'SEAM_B':ids_b,'SEAM_S':ids_s,'ANVIL_L':ids_l,'BOUNDARY':T,'TERMINAL':TERM},
 'candidate_inventory_counts':inv.get('counts'),
 'candidate_total':inv.get('total'),
 'sets_equal':set(all_ids)==set(inv_ids) and len(all_ids)==len(inv_ids)==118,
 'unique_ids':len(set(all_ids)),
 'candidate_excerpt_exact_rows':{k:v for k,v in replay.items()},
 'exact_rows_ok':sum(1 for v in replay.values() if any(v.get(k) for k in ('source_excerpt_exact_raw_row','source_excerpt_in_member'))),
 'P4R_closed_flags_all_false':all(str(r.get('status','') or '').upper().startswith('HELD') for r in p4),
 'PYAT_PC_not_adopted_rows':sum(1 for r in pc if 'NOT_ADOPTED' in json.dumps(r).upper()),
 'K1_first_cap':cap[0].get('capability_id'),'K1_last_cap':cap[-1].get('capability_id'),
 'K3_CAP_header':cap_h,'K3_PC_header':pc_h,'K3_P4R_header':p4_h,
 'B10_line':next((l for l in b_lines if 'B-10' in l),None),
 'S08_line':next((l for l in s_lines if 'S-08' in l),None),
 'L08_line':next((l for l in l_lines if 'L-08' in l),None),
}
(OUT/'source_replay.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:report[k] for k in ('counts_actual','candidate_inventory_counts','candidate_total','sets_equal','unique_ids','exact_rows_ok','PYAT_PC_not_adopted_rows','K1_first_cap','K1_last_cap')},indent=2))
print('bad exact rows:',[k for k,v in replay.items() if not any(v.get(x) for x in ('source_excerpt_exact_raw_row','source_excerpt_in_member'))])
