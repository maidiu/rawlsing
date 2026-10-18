"""Verify custody, produce portable native/Node JUnit and final byte manifest."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,uuid,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
B2=REPO/'WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
BASE='950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883'
X2='931aec3497c60114444806c375d1bb51ec7c0e7d'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def portable(s):
    s=s.replace(str(ROOT),'<R1>').replace(str(Path.home()),'<HOME>')
    return re.sub(r"/(?:private/)?var/folders/[^\s'\"<>]*",'<TEMP>',s)
def main():
    frozen=git('show',X2+':WORKER_RETURNS/SOROK-V2-HQ326-X2-B2-INDEPENDENT-EXECUTABLE-R1/test_hostile_x2.py')
    assert (ROOT/'frozen/test_hostile_x2.py').read_bytes()==frozen
    sources=json.loads((B2/'imported_sources.json').read_text())
    assert len(sources)==69
    for row in sources:assert digest(B2/row['materialized_path'])==row['sha256']
    # The only tracked prior artifact changed is the commissioned candidate bridge.
    assert git('diff',BASE,'--name-only','--',str(B2.relative_to(REPO))).decode().splitlines()==[str((B2/'bridge.py').relative_to(REPO))]
    runtime=json.loads((ROOT/'evidence/after/runtime.json').read_text())
    assert runtime['modules']['bridge']['sha256']==digest(B2/'bridge.py')
    for phase in ('before','after'):
        out=ROOT/'evidence'/phase
        receipt=json.loads((out/'b2_execution_receipt.json').read_text())
        assert receipt['f1']['raw_native_failures']==17
        assert receipt['f1']['boundary_negative_deferral_pass']==19
        assert receipt['f1']['not_applicable']==17
        for label,n in [('b1',39),('p1',74),('f1',97),('integration',81)]:
            suite=ET.parse(out/'b2'/(label+'.xml')).find('testsuite')
            assert int(suite.get('tests'))==n and int(suite.get('failures'))==0 and int(suite.get('errors'))==0
        native=json.loads((out/'b2/f1_native_gate.log').read_text())
        rows=json.loads((out/'b2/f1_applicability.json').read_text())
        failures={r['case_id']:r for r in native['failures']}
        assert len(failures)==17 and len(rows)==36
        suite=ET.Element('testsuite',name='unchanged_native_F1',tests='36',failures='17',errors='0',skipped='0')
        for row in rows:
            case=ET.SubElement(suite,'testcase',name=row['case_id'],classname='F1.native')
            if row['case_id'] in failures:
                ET.SubElement(case,'failure',message='Inherited native RED').text=json.dumps(failures[row['case_id']])
        ET.ElementTree(suite).write(out/'f1_native.xml',encoding='utf-8',xml_declaration=True)
        for label,n in [('d1_original',22),('d1_corrected',17)]:
            lines=(out/'b2'/(label+'.log')).read_text().splitlines()
            cases=[s for s in lines if s.startswith('PASS ')]
            assert len(cases)==n
            suite=ET.Element('testsuite',name=label,tests=str(n),failures='0',errors='0',skipped='0')
            for i,line in enumerate(cases):ET.SubElement(suite,'testcase',name=line[5:],classname=label)
            ET.ElementTree(suite).write(out/(label+'.xml'),encoding='utf-8',xml_declaration=True)
    # Portable evidence copies only. Never touch frozen X2 or imported source.
    for p in (ROOT/'evidence').rglob('*'):
        if not p.is_file() or p.suffix not in ('.json','.xml','.log'):continue
        if p.suffix=='.xml':
            tree=ET.parse(p)
            for node in tree.iter():
                node.attrib.pop('hostname',None)
                for k,v in node.attrib.items():node.set(k,portable(v))
                if node.text:node.text=portable(node.text)
                if node.tail:node.tail=portable(node.tail)
            tree.write(p,encoding='utf-8',xml_declaration=True)
        else:p.write_text(portable(p.read_text()))
    actual=json.loads((ROOT/'evidence/after/source_runtime.json').read_text())
    for path,sha in actual['test_sources'].items():assert digest(ROOT/path)==sha,path
    (ROOT/'source_diff.patch').write_bytes(git('diff',BASE,'--',str((B2/'bridge.py').relative_to(REPO))))
    files=git('ls-files','--cached','--others','--exclude-standard','--',str(ROOT.relative_to(REPO))).decode().splitlines()
    inventory=[]
    for name in sorted(set(files+[str((B2/'bridge.py').relative_to(REPO))])):
        p=REPO/name
        if p.name=='source_manifest.json':continue
        data=p.read_bytes()
        inventory.append(dict(path=name,sha256=hashlib.sha256(data).hexdigest(),
            git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),bytes=len(data)))
    (ROOT/'source_manifest.json').write_text(json.dumps(dict(base=BASE,frozen_x2=X2,
        inherited_sources=sources,files=inventory),indent=2)+'\n')
    print(json.dumps(dict(status='CUSTODY_AND_EVIDENCE_VERIFIED',inherited_files=len(sources),manifest_files=len(inventory))))
if __name__=='__main__':main()
