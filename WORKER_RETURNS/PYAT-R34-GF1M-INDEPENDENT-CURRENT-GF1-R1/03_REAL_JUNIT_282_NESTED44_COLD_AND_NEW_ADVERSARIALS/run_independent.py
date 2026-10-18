import os,sys,subprocess,json,hashlib,xml.etree.ElementTree as ET
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parent
V=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';S=V/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
seat=E/'court/runtime_root/gf1_pair_support_consumer.py';data=seat.read_bytes();candidate=V/'repair/gf1_pair_support_consumer.py'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'),GF1M_HISTORICAL_HELPER=str(V/'phase_a/test_gf1l_executable_v2.py'))
try:
 seat.write_bytes(candidate.read_bytes())
 args=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',str(O/'test_independent_domains.py'),'--junitxml='+str(O/'independent_domains.xml')]
 p=subprocess.run(args,cwd=E/'court/repro',env=env,capture_output=True,text=True)
 (O/'independent_domains.log').write_text(p.stdout+p.stderr)
 (O/'independent_execution.json').write_text(json.dumps(dict(command=args,cwd=str(E/'court/repro'),exit=p.returncode,consumer_sha256=hashlib.sha256(seat.read_bytes()).hexdigest()),indent=2)+'\n')
 print(p.stdout[-7000:])
finally:seat.write_bytes(data)
