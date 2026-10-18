import json,os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'))
args=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(R/'postinspection/test_gf1l_typed_domain_conservation.py'),'--import-mode=importlib','--junitxml='+str(OUT/'gf1k_postinspection_typed_domains.xml')]
p=subprocess.run(args,cwd=E/'court/repro',env=env,capture_output=True,text=True)
(OUT/'gf1k_postinspection_typed_domains.log').write_text(p.stdout+p.stderr)
(R/'supplemental_run.json').write_text(json.dumps(dict(command=args,exit=p.returncode,cwd=str(E/'court/repro')),indent=2)+'\n')
print(p.returncode,p.stdout[-3200:])
