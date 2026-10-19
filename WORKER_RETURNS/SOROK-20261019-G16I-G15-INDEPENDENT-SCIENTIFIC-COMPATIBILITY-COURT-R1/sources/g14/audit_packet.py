"""Recompute custody and per-case matrices after the independent execution.

The exact source staging remains local and is reproducible with review_runner.py;
only new evidence is published. All provenance paths are repository-relative.
"""
from pathlib import Path
import ast, collections, hashlib, json, os, re, shutil, subprocess, sys
import xml.etree.ElementTree as ET
from review_runner import ROOT, REPO, TARGET, G13, dump, git

START='f4e0d218997777d7975db9f35e7cfde9825f3b5f'
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def read(p): return json.loads((ROOT/p).read_text())
def counts(cases): return dict(collections.Counter(c['status'] for c in cases))

def main():
    obj=read('custody/staged_objects.json')
    mismatches=[]
    for row in obj:
        p=ROOT/row['staged']
        if not p.exists() or blob(p.read_bytes())!=row['blob_sha1']: mismatches.append(row['staged'])
    assert not mismatches,mismatches
    imported=read('execution/g14_observations.json')['imports']
    authoritative=json.loads(git('show',TARGET+':'+G13+'06_CUSTODY/imported_blob_manifest.json'))['repaired_lab_modules']
    modules=[]
    source_manifest=read('reproduction/03_POSTREPAIR_COURT/source_manifest.json')
    for row in authoritative:
        module=row['module']
        p=G13+'02_REPAIRED_LAB/'+module
        b=git('show',TARGET+':'+p)
        imp=next(x for x in imported if x['module_file'].endswith('/'+module))
        orig=next(x for x in source_manifest if x['staged_path'].endswith('/'+module))
        original=git('show',orig['commit']+':'+orig['path'])
        assert blob(b)==row['repaired_blob_sha1']==imp['git_blob_sha1']
        assert blob(original)==row['original_blob_sha1']==orig['git_blob_sha1']
        # Compare actual imported bytes, target canonical repaired bytes, original source.
        modules.append(dict(module=module,target_commit=TARGET,target_path=p,target_blob_sha1=blob(b),
            original_commit=orig['commit'],original_path=orig['path'],original_blob_sha1=blob(original),
            changed=b!=original,actual_import=imp['module_file'],actual_import_blob_sha1=imp['git_blob_sha1']))
    assert len(modules)==14 and sum(m['changed'] for m in modules)==6
    # Independently check EVERY pinned original source/native preimage, not the old
    # test's first-failure shortcut, which stops at the first repaired lab module.
    native=read('reproduction/03_POSTREPAIR_COURT/native_source_manifest.json')
    originals=[]
    for row in source_manifest+native:
        if row.get('commit') and row.get('path'):
            commit,path=row['commit'],row['path']
        else:
            # Old manifests contain five blob-only authority pins. Verify the
            # actual object and its target-commit custody, preserving that limit.
            commit,path=TARGET,G13+'03_POSTREPAIR_COURT/'+row['staged_path']
            assert blob(git('cat-file','blob',row['git_blob_sha1']))==row['git_blob_sha1']
        b=git('show',commit+':'+path)
        assert blob(b)==row['git_blob_sha1']
        originals.append(dict(commit=commit,path=path,blob_sha1=blob(b),original_issuer_commit=row.get('commit'),original_issuer_path=row.get('path')))
    dump(ROOT/'custody/module_preimages_and_imports.json',dict(modules=modules,original_manifest_preimages=originals,
         staged_object_count=len(obj),staged_object_mismatches=mismatches,closure='FULL_SOURCEFREE_LAB__NOT_FULL_V3_RUNTIME'))
    # Exact unchanged frozen tests and all matrices remain distinct from findings.
    rows=read('execution/reproduction.json')
    g14=[]
    test_source=(ROOT/'test_g14_science.py').read_text()
    functions={n.name:n for n in ast.parse(test_source).body if isinstance(n,ast.FunctionDef)}
    for c in ET.parse(ROOT/'execution/g14_science.xml').iter('testcase'):
        status='RED' if c.find('failure') is not None else 'ERROR' if c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
        name=c.get('name');family=next((f'F{i}' for i in range(1,8) if name.startswith(f'test_f{i}_')),'CEILINGS')
        fn=functions[name.split('[')[0]]
        checks=[ast.get_source_segment(test_source,n) for n in ast.walk(fn) if isinstance(n,ast.Assert)]
        raises=[ast.get_source_segment(test_source,n) for n in ast.walk(fn) if isinstance(n,ast.With)]
        g14.append(dict(name=name,classname=c.get('classname'),family=family,status=status,
                        scientific_question=name.split('[')[0].replace('test_','').replace('_',' '),
                        source_file='test_g14_science.py',source_line=fn.lineno,
                        expected_assertions=checks,expected_exception_controls=raises,
                        evidence='execution/g14_observations.json; execution/g14_science.xml',
                        interpretation='Tested dependency/guard holds' if status=='PASS' else 'Stronger scientific or custody claim falsified at tested helper boundary; see seven-family adjudication',
                        assertion=(c.find('failure').get('message') if c.find('failure') is not None else None)))
    inherited=[r for r in rows if r['suite']!='sgi1_historical']
    cases=[dict(suite=r['suite'],**c) for r in inherited for c in r['tests']]
    assert len(cases)==181 and counts(cases)=={'PASS':164,'RED':17}
    # Compare original literal RED test IDs to the G13 committed execution evidence.
    originals_red=[]
    for label,path in [('sgi1_target','sgi1_junit.xml'),('g12_controls','g12_controls_junit.xml'),('g12_literal','g12_literal_contract_junit.xml')]:
        old=git('show',TARGET+':'+G13+'03_POSTREPAIR_COURT/evidence/'+path)
        for c in ET.fromstring(old).iter('testcase'):
            if c.find('failure') is not None: originals_red.append((label,c.get('name')))
    actual_red=[(c['suite'],c['name']) for c in cases if c['status']=='RED']
    assert sorted(originals_red)==sorted(actual_red)
    classified=[]
    for suite,name in actual_red:
        if suite=='sgi1_target': verdict='FINGERPRINT_REBASE__EXPECTED_IDENTITY_CHANGE__ORIGINAL_RED_RETAINED'
        elif name=='test_original_source_bytes_and_actual_imports': verdict='G12_ORIGINAL_SOURCE_PIN_STALE__REPinned_BY_INDEPENDENT_G14_CUSTODY'
        elif suite=='g12_literal': verdict='FROZEN_LITERAL_VS_LITERAL_HARNESS_DEFECT__NOT_A_LIVE_SAMPLER_TEST'
        else: verdict='OLD_DEFECT_CHARACTERIZATION_INVERTED_BY_REAL_REPAIR'
        classified.append(dict(suite=suite,name=name,classification=verdict,literal_status='RED',waived=False))
    dump(ROOT/'01_CASE_MATRIX.json',dict(target_181=cases,target_counts=counts(cases),
        historical_control=[r for r in rows if r['suite']=='sgi1_historical'],
        independent_g14=g14,independent_counts=counts(g14),
        denominators=dict(inherited_original_tests=94,g13_author_tests=87,target_total=181,
            historical_sgi1_separate=25,independent_g14=len(g14),
            original_k11_cases=24,original_k11_atomic_predicates=98,
            warning='98 predicates are nested in 24 cases; 28 author checks repeat those cases. Do not add predicates, cases, fingerprints and pytest rows as independent evidence.')))
    dump(ROOT/'02_ORIGINAL_17_REDS.json',dict(count=len(classified),same_literal_failure_ids_as_target=True,cases=classified))
    # Rerun forensic audits in each source epoch; retain exact exits and output.
    audits=[]
    for label,stage in [('target','reproduction'),('historical','historical')]:
        cwd=ROOT/stage/'03_POSTREPAIR_COURT'
        cmd=[sys.executable,'-B','audit_replay.py']
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
        (ROOT/'execution'/('audit_'+label+'.txt')).write_text(p.stdout+p.stderr)
        assert p.returncode==0
        audits.append(dict(cwd=stage+'/03_POSTREPAIR_COURT',command=['python3','-B','audit_replay.py'],exit_status=p.returncode,stdout='execution/audit_'+label+'.txt'))
        dst=ROOT/'execution'/('generated_'+label)
        shutil.copytree(cwd/'evidence',dst,dirs_exist_ok=True)
    dump(ROOT/'execution/audit_commands.json',audits)
    # Portable logs: retain exactly the test output except local checkout prefix.
    for p in (ROOT/'execution').rglob('*'):
        if p.is_file() and p.suffix in {'.json','.txt','.xml'}:
            content=p.read_text().replace(str(REPO),'$WORKTREE')
            if p.suffix=='.xml': content=re.sub(r'hostname="[^"]*"','hostname="local-runner"',content)
            p.write_text(content)
    print(json.dumps(dict(custody_modules=len(modules),changed_modules=sum(m['changed'] for m in modules),
        source_preimages=len(originals),target_181=counts(cases),independent_g14=counts(g14),
        original_reds_retained=len(classified))))

if __name__=='__main__': main()
