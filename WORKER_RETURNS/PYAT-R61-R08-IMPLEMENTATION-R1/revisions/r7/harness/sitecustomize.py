"""Sparse-checkout fixture path adaptation only; no candidate/evaluator patching."""
from pathlib import Path
import rawlsing_next.tests.n10e_empirical_slice_fixture as native_fixture
import rawlsing_next.tests.test_pre553_analytical_composition as composition_tests
fixture_root = Path(__file__).resolve().parents[1] / "fixtures"
for module in (native_fixture, composition_tests):
    for name in ("R2_RELATION", "R2_AUTHORITIES", "R2_SLICE", "R3_AUTHORITY", "R8_SPINE"):
        if hasattr(module, name):
            original = getattr(module, name)
            setattr(module, name, fixture_root / original.relative_to(module.ROOT))
