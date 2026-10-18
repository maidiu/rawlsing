"""Explicit pytest plugin: run unchanged tests against the repair candidate."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'candidate'))
import recursive_court

assert Path(recursive_court.__file__).resolve()==ROOT/'candidate/recursive_court.py'

def pytest_report_header():
    return 'CLR3 repair candidate binding verified: repair_r1/candidate/recursive_court.py'
