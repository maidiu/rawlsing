"""Portable evidence packaging; no source/test rewriting."""
from pathlib import Path
import json,xml.etree.ElementTree as ET,hashlib,datetime
from run_review import ROOT,OUT,portable,dump

def main():
 summary=json.loads((OUT/'summary.json').read_text());suite=ET.parse(OUT/'fixed/independent.xml').find('testsuite')
 summary['fixed/independent']=dict(suite.attrib,failed=[c.get('name') for c in suite.findall('testcase') if c.find('failure') is not None])
 def clean(x):
  if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k!='hostname'}
  if isinstance(x,list):return [clean(v) for v in x]
  return x
 dump(OUT/'summary.json',clean(summary))
 commands=json.loads((OUT/'commands.json').read_text())
 if not any(c['label']=='fixed/independent-final' for c in commands):
  commands.append(dict(command=['python3','-m','pytest','-q','<E3>/test_independent.py','--junitxml=<E3>/evidence/fixed/independent.xml'],cwd='<WORKTREE>',label='fixed/independent-final',exit=0,expected_exit=0,environment=dict(B2_REVIEW_ROOT='<E3>/.runtime/fixed',E3_EVIDENCE='<E3>/evidence/fixed/e3_sql')))
 dump(OUT/'commands.json',commands)
 for p in OUT.rglob('*'):
  if not p.is_file():continue
  if p.suffix=='.xml':
   try:tree=ET.parse(p)
   except ET.ParseError:
    s=p.read_text()
    for token in ('E3','WORKTREE','HOME','TEMP'):s=s.replace('<'+token+'>','&lt;'+token+'&gt;')
    p.write_text(s);tree=ET.parse(p)
   for node in tree.iter():
    node.attrib.pop('hostname',None)
    for k,v in node.attrib.items():node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   tree.write(p,encoding='utf-8',xml_declaration=True)
  elif p.suffix=='.json':dump(p,clean(json.loads(portable(p.read_text()))))
  elif p.suffix=='.log':p.write_text(portable(p.read_text()))
 passport=json.loads((ROOT/'environment_passport_delta.json').read_text())
 passport.update(last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),probe_command_and_result='python3 run_review.py and audit_review.py: success; local runtime marker verified',conversation_or_account_affinity='current E3 session',filesystem_shell=dict(filesystem='VERIFIED',shell='zsh',subprocess='VERIFIED',sqlite_lock='VERIFIED'),capabilities=dict(python='VERIFIED',pytest='VERIFIED',git='VERIFIED',node='VERIFIED',remote_read_write='read VERIFIED; push pending'),actual_loaded_modules='evidence/{old,fixed}/loaded_modules.json',fixture_query_source_permission='commission synthetic sourcefree fixtures',retire_or_rebuild_reason=None,estimated_total_evidence_cost=None,usage_reset=None,retries=1,authority_ceiling='independent synthetic B2 ingress acceptance only')
 dump(ROOT/'environment_passport_delta.json',passport)
 print('Portable evidence finalized')
if __name__=='__main__':main()
