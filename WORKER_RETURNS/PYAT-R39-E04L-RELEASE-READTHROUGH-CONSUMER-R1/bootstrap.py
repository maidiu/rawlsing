"""Load exact retained E03/E04 sourcefree modules; no production install."""
from pathlib import Path
import importlib.util
import sys

ROOT=Path(__file__).resolve().parent
for path in (ROOT,ROOT/'vendor',ROOT.parents[1]):
    if str(path) not in sys.path:sys.path.insert(0,str(path))
import rawlsing_next
name='rawlsing_next.pre553_n9_n10w_progressive_candidate'
if name not in sys.modules:
    spec=importlib.util.spec_from_file_location(name,ROOT/'vendor/aux/pre553_n9_n10w_progressive_candidate.py')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    setattr(rawlsing_next,'pre553_n9_n10w_progressive_candidate',module)
