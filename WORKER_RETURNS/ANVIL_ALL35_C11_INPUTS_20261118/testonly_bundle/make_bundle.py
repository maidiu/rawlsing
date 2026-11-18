#!/usr/bin/env python3
"""Emit actual typed TEST_ONLY sourcefree Q2 inputs and pickled reload bundle."""
from __future__ import annotations
import hashlib, json, os, pickle, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'))
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
HERE=Path(os.environ.get('ANVIL_TESTONLY_ROOT', str(Path(__file__).resolve().parent))).resolve()
(HERE/'inputs').mkdir(parents=True,exist_ok=True)
fixture_root=HERE/'inputs'/'sourcefree_fixture'
fixture=source_fixture(fixture_root,source_format='SAV',values=(0.,1.,2.,0.,1.),original=False)
inputs={
 'config':fixture['config'],'inventory':fixture['inventory'],
 'policy':fixture['policy'],'frontier':fixture['frontier'],
 'census':fixture['census'],'source_path':str(Path('inputs')/'sourcefree_fixture'/'src-SAV'/'s1b_fixture.sav'),
 'source_sha256':fixture['source_sha'],'rows':fixture['rows'],
}
pickle_path=HERE/'inputs'/'typed_inputs.pkl'
pickle_path.write_bytes(pickle.dumps(inputs,protocol=5))
manifest={
 'schema':'ANVIL_TESTONLY_Q2_TYPED_INPUTS@1',
 'sourcefree_test_only':True,'original_source_bodies_read':False,
 'source_path':str(Path('inputs')/'sourcefree_fixture'/'src-SAV'/'s1b_fixture.sav'),'source_sha256':fixture['source_sha'],
 'rows':fixture['rows'],'typed_objects':['SourceConfig','SourceInventory','GrammarPolicy','ScientificFrontier','FrozenInputCensus'],
 'pickle_sha256':hashlib.sha256(pickle_path.read_bytes()).hexdigest(),
 'pickle_relpath':'inputs/typed_inputs.pkl',
 'q2_interfaces':'aee95429609c372564e996c2d3d3eb30e9253cbf',
}
(HERE/'inputs'/'typed_inputs_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps(manifest,sort_keys=True))
