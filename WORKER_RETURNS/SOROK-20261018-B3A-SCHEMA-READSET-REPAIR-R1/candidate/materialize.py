"""Exact, bounded Git transport. Run from any cwd inside the commissioned worktree."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
ROOT=Path(__file__).resolve().parent
RUNTIME=ROOT/'.runtime'
PINS={
 'b2':('8f7966d6d0bbb1ea2e57359de9defbcf552268bd','SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'),
 'm2':('5c2fbe14ccfa5027becfabc682206a1e61aaf986','SOROK-V2-HQ328-M2-M1-SOURCE-TIME-REPAIR-R1'),
 'f2':('a24429906c93446f9d912e7054d48f9f51aee63d','SOROK-V2-HQ327-F2-HELDOUT-OTHERNESS-R1'),
 'tests_after/R1':('358fd1086eac0a4aa7791ca14abc25c45b935ddd','SOROK-V2-HQ327-R1-EVENT-IDENTITY-REPAIR-R1'),
 'tests_after/E2':('8983315b3aee130e9446d43bd983c4a91c6f0437','SOROK-V2-HQ328-E2-R1-INDEPENDENT-CUSTODY-R1'),
 'repair':('8f7966d6d0bbb1ea2e57359de9defbcf552268bd','SOROK-V2-USERDIRECT-B2-LEGACY-REENTRY-REPAIR-R1'),
 'm3':('49dfcb30971310756a12f659961600d9f2eb4a11','SOROK-V2-HQ329-M3-M2-INDEPENDENT-SCIENCE-R1'),
 'e3':('a16ba353f3bc471776d60ce198f267be4e9e5773','SOROK-V2-HQ329-E3-LEGACY-REENTRY-INDEPENDENT-R1'),
 's2':('7e6ac81e85aa2c8dca0cea53349ad61f10fb6665','SOROK-V2-HQ326-S2-B2-SCIENTIFIC-R1'),
 'i2':('19f1e86ad2eab7226b59f84288dbbe4f970de77c','SOROK-V2-HQ327-I2-M1-INDEPENDENT-SCIENCE-R1'),
}
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0','-c','maintenance.auto=false',*args],cwd=ROOT.parent.parent)
def dump(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
def transport(commit,path,dest,rows):
 data=git('show',commit+':'+path);blob=git('rev-parse',commit+':'+path).decode().strip()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert dest.read_bytes()==data,str(dest)
 else:dest.write_bytes(data)
 rows.append(dict(commit=commit,path=path,git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),local=str(dest.relative_to(ROOT))))
def unpack(archive,dest):
 with tarfile.open(archive) as t:
  for m in t.getmembers():
   target=dest/m.name
   assert target.resolve().is_relative_to(dest.resolve()) and not m.issym() and not m.islnk()
   if m.isfile():
    target.parent.mkdir(parents=True,exist_ok=True);data=t.extractfile(m).read()
    if target.exists():assert target.read_bytes()==data
    else:target.write_bytes(data)
def main():
 rows=[]
 for label,(commit,name) in PINS.items():
  prefix='WORKER_RETURNS/'+name+'/'
  for p in git('ls-tree','-r','--name-only',commit,prefix).decode().splitlines():
   rel=p.removeprefix(prefix)
   if any(x in rel.split('/') for x in ('evidence','execution','local_publication')):continue
   if not (p.endswith(('.py','.json','.md','.js','.gz')) or rel=='.gitignore'):continue
   transport(commit,p,RUNTIME/label/rel,rows)
 # The inherited materializer uses cwd ROOT.parent.parent; use explicit GIT_DIR
 # for its unchanged subprocesses while retaining the original source bytes.
 env=__import__('os').environ.copy();env['GIT_DIR']=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip()
 subprocess.run(['python3',str(RUNTIME/'b2/materialize.py')],cwd=ROOT,env=env,check=True)
 inherited=json.loads((RUNTIME/'b2/imported_sources.json').read_text())
 assert len(inherited)==69
 for r in inherited:
  p=RUNTIME/'b2'/r['materialized_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
  rows.append(dict(r,local=str(p.relative_to(ROOT))))
 for archive,dest in [(RUNTIME/'m2/frozen_inputs/M1_original_exact_7e91c198.tar.gz',RUNTIME/'m1_original'),(RUNTIME/'m2/frozen_inputs/I2_strict_exact_19f1e86a.tar.gz',RUNTIME/'i2_strict')]:unpack(archive,dest)
 gov=json.loads((RUNTIME/'b2/governing_sources.json').read_text())
 for i,r in enumerate(gov):transport(r['commit'],r['path'],RUNTIME/'governance'/f'{i:02d}_{Path(r["path"]).name}',rows)
 for p in git('ls-tree','-r','--name-only','7b091166ac31c0b538093007808cbbbdaccf8d6f','SOROK_PRODUCT_CONTROL_ROOM/PRE_A0_PSYCHIC_ARCHITECTURE_R1').decode().splitlines():
  if p.endswith('00_PRE_A0_ARCHITECTURAL_BANK_R1.md'):transport('7b091166ac31c0b538093007808cbbbdaccf8d6f',p,RUNTIME/'governance/PRE_A0.md',rows)
 transport('63f07960eb04cc856d94ed85f4c3c597f2f6bc9e','WORKER_COMMISSIONS/SOROK-V2-HQ329-B3-COUPLED-INTERPRETATION-PROTOTYPE-R1/00_COMMISSION.md',RUNTIME/'governance/B3_COMMISSION.md',rows)
 transport('794a0b192b125703c02a669ca918f1a8f20fe34e','SOROK_PRODUCT_CONTROL_ROOM/HQ329_E2_FIX_M2_FANIN_R1/00_VERIFIED_RETURNS_ACCEPTANCE_BOUNDARY_AND_PARALLEL_PLAN.md',RUNTIME/'governance/HQ329_INTAKE.md',rows)
 for name in ('README.md','bridge.py'):
  transport('950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883','WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1/'+name,RUNTIME/'original_b2'/name,rows)
 dump(ROOT/'source_manifest.json',rows)
 print('Exact staged entries:',len(rows))
if __name__=='__main__':main()
