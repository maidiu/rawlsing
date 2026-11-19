"""Generated keyed sourcefree fixture; never original data."""
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
def make_keyed_fixture(root):
 root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=True)
 f=source_fixture(root,keyed=True,values=(1.,2.,0.,7.,None,-1.,1.,2.,None,-1.))
 return f["config"],f["path"]
