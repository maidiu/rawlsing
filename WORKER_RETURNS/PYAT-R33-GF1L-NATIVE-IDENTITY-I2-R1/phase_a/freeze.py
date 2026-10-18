import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
refs={
 'GF1E':'eeb726357204653b22458dc267dd70ba0009bd77',
 'GF1G':'ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7',
 'GF1H':'cc41ad4553d189a3c4c8152179b3d1977327c07f',
 'GF1J':'f3f34bc1b7b9fd97a3ae8a9b24dd2201f42f38f5',
 'GF1K_startup_only':'d2169b3db2e364506a606adec2b6b7c508497307'}
obj={'commission_startup':'6346b8ed72cc1687d84c358f48cb88f042ade6fd',
 'phase':'A BEFORE GF1K repair inspection', 'pins':refs,
 'test_sha256':hashlib.sha256((R/'phase_a/test_gf1l_frozen.py').read_bytes()).hexdigest(),
 'expected':{'native_closure':74,'GF1L':'all pass; strict native type AND value identity',
 'original44':'44 pass unchanged','GF1G26':'26 pass unchanged','GF1H26':'26 pass unchanged',
 'GF1J_two':'two original strict red nodes plus native positive run unchanged',
 'GF1F100':'96 pass, 4 stale historical failures retained; never all green',
 'GF1I19':'17 pass, 2 historical consumer absence failures retained; never all green',
 'reverse_X_given_Y':'distinct granted relation; no implicit reversal',
 'F2':'no copied consumer outputs on producer',
 'denominator_risk':'exact nonnegative integers; support conserved',
 'zero_missing_empty':'distinct typed states; no fabricated downstream positive',
 'forged_rehash':'structural hash does not authenticate original signatory; TEST_ONLY, no owner grant',
 'cold':'two distinct OS processes; equal non-PID result and source receipts'},
 'gate':'No candidate inspection until this oracle and tests are remotely frozen. Actual returned repair required for Phase B.',
 'authority':'SOURCEFREE TEST_ONLY; no SAV/DTA or source/FF/actor/N11/N12/OC05/V3 issuance'}
(R/'01_INDEPENDENT_PHASE_A_FROZEN_SHA_AND_ORACLE.json').write_text(json.dumps(obj,indent=2)+'\n')
