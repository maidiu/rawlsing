"""Verify independent evidence, retain actual REDs, and build portable custody receipts."""
from pathlib import Path
import datetime, hashlib, json, os, re, sys, uuid
import xml.etree.ElementTree as ET
import run_e2 as r

ROOT=r.ROOT
E=r.EVIDENCE

def read(path):return json.loads(path.read_text())

def suite(path,n,failures=0):
    root=ET.parse(path).getroot()
    s=root if root.tag=='testsuite' else root.find('testsuite')
    assert int(s.get('tests'))==n and int(s.get('failures'))==failures and int(s.get('errors'))==0
    assert int(s.get('skipped','0'))==0
    return s

def main():
    phase_totals={}
    for phase in ('original','repaired'):
        out=E/phase
        receipt=read(out/'execution_receipt.json')
        for label,n in [('b1',39),('p1',74),('f1',97),('integration',81)]:suite(out/'inherited'/(label+'.xml'),n)
        assert receipt['f1']['boundary_negative_deferral_pass']==19
        assert receipt['f1']['not_applicable']==17 and receipt['f1']['raw_native_exit']==1
        native=read(out/'inherited/f1_native_gate.log')
        native_ids=sorted(c['case_id'] for c in native['failures'])
        assert native_ids==['F01','F02','F03','F04','F05','F06','F07','F08','F10','F11','F13','F15','F16','F17','F18','F19','F21']
        rows=read(out/'inherited/f1_applicability.json')
        assert len(rows)==36 and sum(c['result']=='NOT_APPLICABLE_TO_THIS_LAB' for c in rows)==17
        native_junit=ET.Element('testsuite',name='supplemental_unchanged_F1_native',tests='36',failures='17',errors='0')
        for row in rows:
            case=ET.SubElement(native_junit,'testcase',name=row['case_id'])
            if row['case_id'] in native_ids:ET.SubElement(case,'failure',message='Actual inherited native RED').text=json.dumps(next(c for c in native['failures'] if c['case_id']==row['case_id']))
        ET.ElementTree(native_junit).write(out/'f1_native_supplemental.xml',encoding='utf-8',xml_declaration=True)
        for label,n in [('d1_original',22),('d1_corrected',17)]:
            lines=(out/'inherited'/(label+'.log')).read_text().splitlines()
            passed=[line[5:] for line in lines if line.startswith('PASS ')]
            assert len(passed)==n
            s=ET.Element('testsuite',name='supplemental_'+label,tests=str(n),failures='0',errors='0')
            for name in passed:ET.SubElement(s,'testcase',name=name)
            ET.ElementTree(s).write(out/(label+'_supplemental.xml'),encoding='utf-8',xml_declaration=True)
        x2=suite(out/'x2.xml',17,0 if phase=='original' else 1)
        failed=[c.get('name') for c in x2.findall('testcase') if c.find('failure') is not None]
        assert failed==([] if phase=='original' else ['test_same_event_id_accepts_distinct_objective_payload_hashes'])
        source=read(out/'source_manifest.json')
        for row in source:
            if '/evidence/' in row['staged_path'] or row['staged_path'].endswith('/execution_receipt.json'):continue
            assert r.sha((ROOT/row['staged_path']).read_bytes())==row['sha256']
        runtime=read(out/'runtime.json')
        for module in runtime['modules'].values():
            expected=next(row for row in source if row['staged_path']=='.runtime/'+phase+'/'+module['path'])
            assert module['sha256']==expected['sha256']
        collision=read(out/'collision.json')
        assert len(collision['after']['occurrence'])==(2 if phase=='original' else 1)
        assert collision['after']['checkpoint']==collision['before']['checkpoint']
        if phase=='repaired':
            assert collision['middle']==collision['after']
            assert collision['second']['reason']=='EVENT_IDENTITY_CONFLICT'
            # Actual trace: lock -> state/identity reads -> all inserts -> admission COMMIT.
            trace=collision['sql_trace']
            begin=trace.index('BEGIN IMMEDIATE')
            occurrence=next(i for i,s in enumerate(trace) if s.startswith('INSERT OR IGNORE INTO occurrence'))
            ingress=next(i for i,s in enumerate(trace) if s.startswith('INSERT OR IGNORE INTO b2_ingress'))
            identity=next(i for i,s in enumerate(trace) if s.startswith('INSERT INTO b2_event_identity'))
            commit=trace.index('COMMIT')
            assert begin<occurrence<ingress<identity<commit
        phase_totals[phase]=dict(unchanged=330,x2_pass=17-len(failed),x2_fail=len(failed),native_red=native_ids)
    suite(E/'repaired/r1.xml',45)
    strict=suite(E/'repaired/e2.xml',44,2)
    failures=[c.get('name') for c in strict.findall('testcase') if c.find('failure') is not None]
    assert failures==['test_legacy_after_mapping_must_fail_closed_at_b2_reentry[False]','test_legacy_after_mapping_must_fail_closed_at_b2_reentry[True]']
    sql=E/'repaired/sql'
    for committed in (False,True):
        row=read(sql/('strict_legacy_after_'+str(committed)+'.json'))
        assert row['before']==row['after'] and len(row['before']['occurrence'])==2
        assert isinstance(row['receipt']['event_admission'],dict)
    processes={}
    for mode in ('same','conflicting','distinct','commit'):
        row=read(sql/('processes_'+mode+'.json'))
        assert len(set(row['process_ids']))==6
        processes[mode]=dict(distinct_os_processes=6,occurrences=len(row['tables']['occurrence']),joint_receipts=len(row['tables']['joint_receipt']))
    for boundary in ('occurrence','ingress','identity'):
        row=read(sql/('sigkill_'+boundary+'.json'))
        assert row['returncode']==-9 and row['external_before']==row['recovered']
        assert row['retry']['status']=='COMMITTED'
    # The source and bytes of frozen X2 and author R1 tests are exact Git objects.
    executed=[]
    for commit,prefix,stage in [(r.R1,r.R1_PATH,'.runtime/R1'),(r.X2,r.X2_PATH,'.runtime/frozen')]:
        for path,data,record in r.tree(commit,prefix):
            rel=Path(path).relative_to(prefix)
            target=ROOT/stage/rel
            if target.is_file():
                assert target.read_bytes()==data
                executed.append(dict(record,staged_path=str(target.relative_to(ROOT))))
    for p in ROOT.glob('*.py'):
        data=p.read_bytes();executed.append(dict(e2_source=p.name,sha256=r.sha(data),git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()))
    r.dump(E/'executed_test_sources.json',executed)
    r.dump(ROOT/'verification_receipt.json',dict(verdict='REVIEW_REVISE',original=r.BASE,repair=r.R1,phases=phase_totals,r1=dict(tests=45,pass_count=45),independent_e2=dict(tests=44,pass_count=42,fail_count=2,strict_failures=failures),concurrent_processes=processes,killed_writer='SIGKILL at three uncommitted insert boundaries; not power loss',cold_replay='exact receipts/state and persisted two-event mediator verified',revision_scope='B2 reentry integrity after conflicting legacy B1 write; no B1 producer lockdown requested'))
    # Sanitize only evidence copies, preserving every test status and raw SQL value.
    for p in E.rglob('*'):
        if not p.is_file():continue
        r.sanitize(p)
        def portable(s):
            return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',r.portable(s))
        if p.suffix=='.xml':
            tree=ET.parse(p)
            for node in tree.iter():
                for k,v in node.attrib.items():node.set(k,portable(v))
                if node.text:node.text=portable(node.text)
                if node.tail:node.tail=portable(node.tail)
            tree.write(p,encoding='utf-8',xml_declaration=True)
        elif p.suffix in ('.json','.log'):p.write_text(portable(p.read_text()))
    inventory=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(x in rel.parts for x in ('.runtime','__pycache__','.pytest_cache')) or rel.as_posix()=='artifact_manifest.json':continue
        data=p.read_bytes()
        inventory.append(dict(path=rel.as_posix(),bytes=len(data),sha256=r.sha(data),git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()))
    r.dump(ROOT/'artifact_manifest.json',dict(files=inventory,manifest_self_excluded=True))
    print(json.dumps(dict(status='E2_EVIDENCE_AUDITED',verdict='REVIEW_REVISE',e2_pass=42,e2_red=2,inherited=330,r1=45,native_f1_red=17,artifact_files=len(inventory))))

if __name__=='__main__':main()
