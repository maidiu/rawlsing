#!/usr/bin/env python3
"""One-command pinned baseline + frozen R2 tests/mocks. No external model calls."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent

def stage():
 rows=json.loads((R/'source_manifest.json').read_text())
 for row in rows:
  p=(R/row['local_relative_path']).resolve()
  if not p.is_relative_to((R/'imports').resolve()):raise ValueError('IMPORT_PATH_ESCAPE')
  data=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=R.parents[1])
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest()==row['git_blob_sha1']
  assert hashlib.sha256(data).hexdigest()==row['sha256']
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 print('Verified pinned staging:',len(rows),'files',flush=True)

def sanitize_xml(p):
 tree=ET.parse(p)
 for el in tree.iter():
  el.attrib.pop('hostname',None)
  if el.text:el.text=el.text.replace(str(R.parents[1]),'<WORKTREE>')
 tree.write(p,encoding='unicode')

def main():
 parser=argparse.ArgumentParser();parser.add_argument('run_id');parser.add_argument('--without-baseline',action='store_true');args=parser.parse_args()
 if not re.fullmatch('[a-zA-Z0-9_-]{1,64}',args.run_id):raise ValueError('Single safe run ID required')
 if (R/'receipts'/args.run_id).exists():raise FileExistsError('Preserved receipts must not be overwritten')
 stage()
 if not args.without_baseline:
  import baseline
  baseline.main()
 from assay.transport import Frozen
 Frozen(R,R/(R/'CURRENT_FREEZE').read_text().strip()).verify()
 xml=R/'receipts'/f'{args.run_id}_tests.xml'
 command=[sys.executable,'-m','pytest','test_r2.py','-q','--tb=short',f'--junitxml={xml.relative_to(R)}']
 p=subprocess.run(command,cwd=R,text=True,capture_output=True)
 (R/'receipts'/f'{args.run_id}_tests.txt').write_text(' '.join(command)+'\nexit='+str(p.returncode)+'\n'+(p.stdout+p.stderr).replace(str(R.parents[1]),'<WORKTREE>'))
 sanitize_xml(xml);print(p.stdout,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
 subprocess.run([sys.executable,'-u','run_experiments.py',args.run_id],cwd=R,check=True)
 subprocess.run([sys.executable,'audit_outputs.py',args.run_id],cwd=R,check=True)
if __name__=='__main__':main()
