import pathlib,subprocess,sys
runner=pathlib.Path(__file__).with_name('run.py')
for stage in ['k9','k10','n10e_c1','pe','hq297']:
 print('RC0_REQUIRED_SUITE',stage,flush=True)
 subprocess.run([sys.executable,str(runner),stage],check=True)
