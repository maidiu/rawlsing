from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "section85/code/run_section85_diagnostic_smoke_matrix.py"


def load_module():
    spec = importlib.util.spec_from_file_location("section85_diagnostic_smoke", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_section85_diagnostic_uses_proven_public_qsm_default() -> None:
    module = load_module()
    assert module.DEFAULT_QSM_RELATION == "question_structural_mapping"
    assert module.DEFAULT_CANONICAL_REGISTRY_RELATION.endswith(".canonical_question_registry")


def test_section85_diagnostic_does_not_hardcode_missing_reconcile_qsm() -> None:
    module = load_module()
    source = inspect.getsource(module.main)
    assert "rawlsing_authority_reconcile_ar_20260719t213835z.question_structural_mapping" not in source
    assert "qsm_relation=args.qsm_relation" in source
    assert "canonical_registry_relation=args.canonical_registry_relation" in source
    assert "DATABASE_RELATION_BINDING.json" in source
    assert "database_relation_preflight_failed" in source


def test_section85_diagnostic_has_no_obsolete_package_or_desktop_roots() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert "85_V550J_BOUNDED_NINE_FAMILY_AUTHORITY_ADAPTER_AND_CANARY" not in source
    assert "/Users/matthewsmith/Desktop" not in source
    assert 'SECTION = Path("section85")' in source
    assert 'BASE_MODULE_DIR = Path("data/ddm_build_copy")' in source
