from pathlib import Path
import sys,json,hashlib,subprocess,os
R=Path(__file__).resolve().parents[1];W=R/'runtime/candidate_checkout/WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1';F=R/'runtime/f6n/WORKER_RETURNS/PYAT-R29-F6N-INDEPENDENT-NATIVE-F6-COURT-R1';O=R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD'
sys.path.insert(0,str(W/'inherited/F6M/candidate'))
import rawlsing_next.pre553_heterogeneous_synthesis as M
assert hashlib.sha1(b'blob '+str(Path(M.__file__).stat().st_size).encode()+b'\0'+Path(M.__file__).read_bytes()).hexdigest()=='2df811d76db258d98d89ffb43c830cb221ff9a7d'
import pytest
which=sys.argv[1];p=F/({'diagnostics':'03_PHASE_B/test_phase_b_diagnostics.py','frozen_n8':'02_PHASE_A/04_TESTS/test_f6n_phase_a.py','frozen_l26':'01_INHERITED_F6L/02_PHASE_A/04_TESTS/test_f6l_phase_a.py'}[which]);print('ACTUAL_PRODUCER',M.__file__,flush=True)
raise SystemExit(pytest.main(['-q',str(p),'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/('independent_f6n_'+which+'.xml'))]))
