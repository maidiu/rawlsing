"""Build a disposable repo-shaped exact source closure from frozen preimages."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent
PREFIX='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
RUN=R/'runs/runtime';RUN.mkdir(parents=True,exist_ok=True)
for cache in RUN.rglob('__pycache__'):
 if cache.is_dir():shutil.rmtree(cache)
for source,dst in [(R/'frozen/c9p',RUN/PREFIX),(R/'frozen/native',RUN),(R/'review',RUN/'review')]:
 shutil.copytree(source,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
for row in json.loads((R/'custody/source_preimages.json').read_text()):
 p=R/row['staged'];b=p.read_bytes()
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
for row in json.loads((R/'custody/native_sources.json').read_text()):
 b=(RUN/row['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
(R/'runs/tmp').mkdir(parents=True,exist_ok=True)
(R/'runs/pytest').mkdir(parents=True,exist_ok=True)
(R/'evidence').mkdir(exist_ok=True)
print('Exact closure prepared; no candidate or author test edits')
