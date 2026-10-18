"""Carry the explicitly pinned P6 custody bootstrap into legacy cold children."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[6]/'bootstrap_p6/sitecustomize.py'))
