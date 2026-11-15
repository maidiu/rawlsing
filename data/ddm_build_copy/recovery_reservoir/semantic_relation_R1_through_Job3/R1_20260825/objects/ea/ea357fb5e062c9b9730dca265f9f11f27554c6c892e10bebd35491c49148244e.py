from pathlib import Path
import shutil
B=Path(__file__).resolve().parents[1]
R=B/'RETURN'; R.mkdir(exist_ok=True)
for p in (B/'TEMPLATES').glob('*.csv'): shutil.copy(p,R/p.name)
print('initialized',R)
