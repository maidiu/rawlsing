"""Run frozen assertions against E04R product using its original import names."""
import sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
import product.service, product.empirical, product.world, product.nonparent, product.scenario
import pytest
raise SystemExit(pytest.main(sys.argv[1:]))
