import importlib.util
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
path = root / "programma_pyat_original35_constructor.py"
spec = importlib.util.spec_from_file_location("p1.programma_pyat_original35_constructor", path)
module = importlib.util.module_from_spec(spec)
sys.modules["p1.programma_pyat_original35_constructor"] = module
sys.modules["rawlsing_next.programma_pyat_original35_constructor"] = module
spec.loader.exec_module(module)
