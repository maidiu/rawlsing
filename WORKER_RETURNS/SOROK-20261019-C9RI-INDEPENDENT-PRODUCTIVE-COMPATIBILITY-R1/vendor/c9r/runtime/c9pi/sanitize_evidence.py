"""Remove personal host prefixes from generated receipts; never alters frozen sources."""
from pathlib import Path
R=Path(__file__).resolve().parent;REPO=R.parents[1]
for p in (R/'evidence').rglob('*'):
 if p.is_file() and p.suffix in ('.json','.xml','.log'):
  text=p.read_text();text=text.replace(str(R),'<RETURN_ROOT>').replace(str(REPO),'<REPO_ROOT>')
  p.write_text(text)
