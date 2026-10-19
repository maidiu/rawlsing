"""Cold selected native owner/client regression command, sourcefree only."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
SUITES=[str(ROOT.relative_to(REPO)/'test_world_consumer.py'),
        str(ROOT.relative_to(REPO)/'native_courts/test_product.py')]
SUITES += ['rawlsing_next/tests/test_'+n+'.py' for n in (
    'm4_v557_v558_publication_repository','m5_runtime_rsc_peer_prior',
    'pre553_empirical_query','pre553_learned_empirical_adjudication',
    'pre553_learned_product_release','pre553_learned_product_lifecycle',
    'pre553_learned_world_composition')]
if __name__=='__main__':
    args=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',*SUITES,
          '--junitxml='+str(ROOT/'evidence/final_native.xml')]
    output=subprocess.run(args,cwd=REPO,capture_output=True,text=True)
    (ROOT/'evidence/final_native.log').write_text((output.stdout+output.stderr).replace(str(REPO),'<ISOLATED_WORKTREE>'))
    print(output.stdout.replace(str(REPO),'<ISOLATED_WORKTREE>'))
    raise SystemExit(output.returncode)
