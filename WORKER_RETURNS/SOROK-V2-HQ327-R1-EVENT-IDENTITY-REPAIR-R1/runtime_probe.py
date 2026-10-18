"""Observed interpreter and imported-file identities, portable relative paths."""
import hashlib, json, os, platform, sqlite3, subprocess, sys
from pathlib import Path
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
root=Path(os.environ['B2_REVIEW_ROOT']).resolve()
modules={name:dict(path=str(Path(module.__file__).resolve().relative_to(root)),
    sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest())
    for name,module in [('bridge',m),('B1',m.b1),('P1',m.p1)]}
result=dict(python=platform.python_version(),sqlite=sqlite3.sqlite_version,
    pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),
    git=subprocess.check_output(['git','--version'],text=True).strip(),
    node=subprocess.check_output(['node','--version'],text=True).strip(),modules=modules)
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
