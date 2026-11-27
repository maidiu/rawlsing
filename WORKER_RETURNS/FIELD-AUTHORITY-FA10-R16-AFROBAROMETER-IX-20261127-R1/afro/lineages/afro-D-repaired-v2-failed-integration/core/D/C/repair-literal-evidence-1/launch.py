import subprocess,sys
from pathlib import Path
root=Path('$HOME/.local/state/rawlsing-controller/fa10-r16-20261127')
d=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,str(root/'opencode_provider_sequential.py'),'--cap','1800','--effort','none'],input=(d/'input.json').read_text(),text=True,capture_output=True,timeout=820)
(d/'provider_stderr.txt').write_text(p.stderr)
(d/'stdout.json').write_text(p.stdout)
raise SystemExit(p.returncode)
