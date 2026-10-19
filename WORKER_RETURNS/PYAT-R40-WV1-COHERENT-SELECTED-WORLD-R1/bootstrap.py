"""Isolated exact sourcefree owner closure. No production package installation."""
import importlib.util
import json
from pathlib import Path
import sys
RETURN = Path(__file__).resolve().parent
SEALED = '1150e836ef58553255abc0f588e66c1327db4932'
REPO = RETURN.parents[1]
for p in (RETURN, RETURN/'vendor', REPO, REPO/'rawlsing_next/tests'):
    if str(p) not in sys.path: sys.path.insert(0, str(p))
def install():
    import rawlsing_next
    for leaf in ('pre553_n9_n10w_progressive_candidate', 'pre553_hq297_n9c_two_field_reader'):
        name = 'rawlsing_next.' + leaf
        if name not in sys.modules:
            spec = importlib.util.spec_from_file_location(name, RETURN/'vendor/aux'/ (leaf+'.py'))
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
            setattr(rawlsing_next, leaf, mod)
def fixture_rows():
    return json.loads((RETURN/'vendor/fields.json').read_text())['fields']
install()
