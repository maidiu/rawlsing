"""Read exact Git objects, audit entire copied tree, stage a static import closure.

No candidate executable is run by this script. Reproduction requires local pinned
Git objects; source snapshots are byte-preserving and confined to this return.
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

RET = Path(__file__).resolve().parent
WT = RET.parents[1]
CAND = 'edf3494b1b11cb71a78540aba950aa15da900c8a'
BASE = '646ac11ab8f1d49d56464c484ec5e0f4eba8f34e'
PREFIX = 'WORKER_RETURNS/PYAT-R18-T9B-TEMPORAL-HISTORY-CONSUMER-R1/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(WT), *args])

def tree(rev, prefix):
    out = {}
    for row in git('ls-tree', '-r', '-l', '-z', rev, '--', prefix).split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, kind, oid, size = meta.decode().split()
        out[path.decode()] = {'mode': mode, 'kind': kind, 'oid': oid, 'size': int(size)}
    return out

def read_blobs(entries):
    unique = list(dict.fromkeys(x['oid'] for x in entries.values()))
    raw = git('cat-file', '--batch') if not unique else subprocess.check_output(
        ['git', '-C', str(WT), 'cat-file', '--batch'], input=('\n'.join(unique)+'\n').encode())
    out, offset = {}, 0
    for oid in unique:
        end = raw.index(b'\n', offset)
        header = raw[offset:end].decode().split()
        assert header[0] == oid and header[1] == 'blob', header
        size = int(header[2]); start = end+1
        out[oid] = raw[start:start+size]; offset = start+size+1
    return out

def main():
    entries = tree(CAND, PREFIX)
    blobs = read_blobs(entries)
    original = tree(BASE, 'data/ddm_build_copy/')
    ledger = json.loads(blobs[entries[PREFIX+'evidence/native_source_ledger.json']['oid']])
    rows = []
    by_path = {r['path']:r for r in ledger}
    native = {p.removeprefix(PREFIX+'native/'):m for p,m in entries.items() if p.startswith(PREFIX+'native/')}
    assert len(native) == len(ledger) == 1259
    assert set(native) == set(by_path)
    findings = []
    json_shapes=[]
    for path, m in native.items():
        b = blobs[m['oid']]
        oid = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert oid == m['oid'] == by_path[path]['git_blob_sha1']
        assert len(b) == m['size'] == by_path[path]['bytes']
        text = b.decode('utf-8', errors='replace')
        risks = []
        if b'\0' in b: risks.append('binary_NUL')
        if Path(path).suffix.lower() in {'.sav','.dta','.csv','.tsv','.parquet','.sqlite','.db','.pkl','.pickle','.xlsx','.zip'}:
            risks.append('data_or_container_extension')
        if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}', text):
            risks.append('credential_pattern')
        if re.search(r'(?:postgres(?:ql)?|mysql)://[^\s:/]+:[^\s@/]+@',text):
            risks.append('embedded_database_credential_shape')
        if re.search(r'(?i)\b(?:ssn|social_security_number|email_address|phone_number)\b\s*[=:]\s*[\"\'][0-9a-zA-Z@.+ -]{6,}', text):
            risks.append('potential_identifier_literal')
        if m['mode'] != '100644': risks.append('nonregular_or_executable_git_mode')
        if path.endswith('.json'):
            try:
                parsed_json=json.loads(text)
                identifiers={'respondent_id','respondentid','caseid','respid','social_security_number','email_address','phone_number'}
                suspicious_records=0;pending=[parsed_json]
                while pending:
                    node=pending.pop()
                    if isinstance(node,dict):
                        keys={str(k).lower() for k in node}
                        if keys & identifiers and len(keys)>=3:
                            if any(isinstance(v,(int,float)) or (isinstance(v,str) and v and not any(c in v for c in '{}[]'))
                                   for k,v in node.items() if str(k).lower() in identifiers):
                                suspicious_records+=1
                        pending.extend(node.values())
                    elif isinstance(node,list): pending.extend(node)
                if suspicious_records: risks.append('possible_row_level_identifier_record')
                json_shapes.append({'path':path,'root_type':type(parsed_json).__name__,
                                    'root_length':len(parsed_json) if isinstance(parsed_json,(dict,list)) else None,
                                    'identifier_record_candidates':suspicious_records})
            except (ValueError,TypeError): risks.append('json_parse_failure')
        if risks: findings.append({'path':path,'flags':risks})
        rows.append({'path':path,'bytes':len(b),'git_blob_sha1':oid,'sha256':hashlib.sha256(b).hexdigest(),
                     'pre_main_original_blob':original.get(path,{}).get('oid'),
                     'matches_pre_main_original':original.get(path,{}).get('oid')==oid,'risk_flags':risks})
    # Resolve project-local imports without importing or executing anything.
    seeds = ['data/ddm_build_copy/ddm_v553_temporal_pressure.py',
             'data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py',
             'data/ddm_build_copy/compile_v553_wave_harmonization.py',
             'data/ddm_build_copy/compile_v553_wave_harmonization_from_repo.py']
    selected, queue = set(), list(seeds)
    def add_module(module):
        p = module.replace('.', '/')
        for candidate in (p+'.py',p+'/__init__.py'):
            if candidate in native and candidate not in selected: queue.append(candidate)
    while queue:
        p = queue.pop()
        if p in selected: continue
        selected.add(p)
        for parent in Path(p).parents:
            init = str(parent/'__init__.py')
            if init in native and init not in selected: queue.append(init)
        parsed = ast.parse(blobs[native[p]['oid']].decode())
        for n in ast.walk(parsed):
            if isinstance(n, ast.Import):
                for alias in n.names: add_module(alias.name)
            elif isinstance(n, ast.ImportFrom) and n.module:
                add_module(n.module)
                for alias in n.names: add_module(n.module+'.'+alias.name)
    stage = RET/'pinned_candidate'
    snapshots = ['t9b_temporal.py','test_t9b_temporal.py','run_pinned_v553_suite.py',
                 '01_PREDECLARED_SERIES_CLOCK_ORACLE.json','evidence/native_source_ledger.json',
                 'evidence/02_real_temporal_to_selected_world_two_times.json']
    source_map = []
    for relative in snapshots + ['native/'+p for p in sorted(selected)]:
        entry = entries[PREFIX+relative]
        b = blobs[entry['oid']]
        dest = stage/relative
        dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
        source_map.append({'relative':relative,'candidate_git_path':PREFIX+relative,'git_blob_sha1':entry['oid'],
                           'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
    (RET/'evidence').mkdir(exist_ok=True)
    (RET/'evidence/immutable_copied_source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    (RET/'evidence/json_structure_privacy_scan.json').write_text(json.dumps(json_shapes,indent=2)+'\n')
    (RET/'evidence/staged_source_manifest.json').write_text(json.dumps(source_map,indent=2)+'\n')
    summary = {'candidate':CAND,'independent_base':BASE,'full_copied_count':len(rows),
        'total_bytes':sum(r['bytes'] for r in rows),'all_sha1_NUL_preimages_and_ledger_lengths_verified':True,
        'pre_main_identical_count':sum(r['matches_pre_main_original'] for r in rows),
        'extensions':dict(Counter(Path(r['path']).suffix for r in rows)),
        'risk_findings':findings,'static_minimal_stage_native_files':len(selected),
        'json_structures_inspected':len(json_shapes),
        'unneeded_copied_files_not_materialized':1259-len(selected),
        'limits':'Static name/content-pattern audit is not exhaustive DLP or permission certification. No raw binary/data containers staged. Unrelated executable cargo retained only as Git evidence, not run.',
        'source_map_sha256':hashlib.sha256((RET/'evidence/staged_source_manifest.json').read_bytes()).hexdigest()}
    (RET/'evidence/source_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__': main()
