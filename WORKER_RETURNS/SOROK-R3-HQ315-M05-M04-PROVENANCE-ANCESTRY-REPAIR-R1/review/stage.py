"""Fresh Git-only reconstruction; never depends on another chat's live files."""
from pathlib import Path
import subprocess,shutil,sys,os
R=Path(__file__).resolve().parents[1];assert not (R/'runtime').exists(),'Move an existing runtime aside explicitly before fresh reconstruction'
bin=R/'toolbin';bin.mkdir(exist_ok=True);real=shutil.which('git');wrapper=bin/'git'
wrapper.write_text('#!'+sys.executable+'\nimport sys,os\na=sys.argv[1:]\nif "ls-tree" in a:a.insert(a.index("ls-tree")+1,"--full-tree")\nos.execv('+repr(real)+',['+repr(real)+']+a)\n');wrapper.chmod(0o755)
manifest=(R/'01_INPUT_SOURCE_IDENTITIES.json').read_bytes()
p=subprocess.run([sys.executable,str(R/'repro/stage.py')],cwd=R.parents[1],env=dict(os.environ,PATH=str(bin)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
(R/'evidence/reconstruction.stdout').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
(R/'01_INPUT_SOURCE_IDENTITIES.json').write_bytes(manifest)
original=R/'runtime/m03_original';original.mkdir()
for name in ['cell.py','claim_provenance.py']:
 path='WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1/candidate/'+name
 data=subprocess.check_output([real,'show','e1f7a74e51201b9614bcc578348b4e9db7be7bd3:'+path],cwd=R.parents[1]);(original/name).write_bytes(data);(R/'runtime/m02/runtime/m01/repro'/name).write_bytes(data)
print('Original M03 installed for baseline638; no candidate/oracle edits')
