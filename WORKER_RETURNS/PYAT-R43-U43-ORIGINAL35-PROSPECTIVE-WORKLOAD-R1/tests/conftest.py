import sys
import os
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R.parents[1]))
sys.path.insert(0, str(R / "repro"))
review = Path(os.environ.get("U43_REVIEW_ROOT", str(R.parents[1] / "LOCAL_COURTS/u43-repaired")))
if (review / "repro").is_dir():
    sys.path.append(str(review / "repro"))
