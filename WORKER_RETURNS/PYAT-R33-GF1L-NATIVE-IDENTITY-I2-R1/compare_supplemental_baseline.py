"""Same postinspection test bytes against exact GF1H; restore GF1K in finally."""
import os,subprocess,sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
H=S/'WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1'
K=S/'WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1'
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'))
target=E/'court/runtime_root/gf1_pair_support_consumer.py';repaired=(K/'gf1_pair_support_consumer.py').read_bytes();baseline=(H/'gf1_pair_support_consumer.py').read_bytes()
assert target.read_bytes()==repaired
assert hashlib.sha256(baseline).hexdigest()=='a4915b845853e70f9430190aebde298346ea5ad4472de8380e26182113f97c8a'
args=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(R/'postinspection/test_gf1l_typed_domain_conservation.py'),'--import-mode=importlib','--junitxml='+str(OUT/'gf1h_postinspection_typed_domains.xml')]
try:
    target.write_bytes(baseline)
    p=subprocess.run(args,cwd=E/'court/repro',env=env,capture_output=True,text=True)
    (OUT/'gf1h_postinspection_typed_domains.log').write_text(p.stdout+p.stderr)
    (R/'postinspection/baseline_comparison_run.json').write_text(json.dumps(dict(command=args,exit=p.returncode,consumer_sha256=hashlib.sha256(baseline).hexdigest(),restored_consumer_sha256=hashlib.sha256(repaired).hexdigest()),indent=2)+'\n')
    print(p.returncode,p.stdout[-1500:])
finally:
    target.write_bytes(repaired)
    assert target.read_bytes()==repaired
