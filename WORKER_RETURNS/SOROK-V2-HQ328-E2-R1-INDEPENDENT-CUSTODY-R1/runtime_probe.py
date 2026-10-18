from pathlib import Path
import hashlib,json,os,platform,sqlite3,subprocess,sys
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
import pytest
root=Path(os.environ['B2_REVIEW_ROOT']).resolve()
def version(args):return subprocess.check_output(args,text=True).strip()
modules={name:dict(path=str(Path(module.__file__).relative_to(root)),sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()) for name,module in [('bridge',m),('B1',m.b1),('P1',m.p1)]}
Path(sys.argv[1]).write_text(json.dumps(dict(python=platform.python_version(),pytest=pytest.__version__,sqlite=sqlite3.sqlite_version,node=version(['node','--version']),git=version(['git','--version']),modules=modules),indent=2)+'\n')
