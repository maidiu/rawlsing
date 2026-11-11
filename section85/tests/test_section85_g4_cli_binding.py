from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "section85/code"
DIAGNOSTIC = CODE / "run_section85_diagnostic_smoke_matrix.py"


def load_diagnostic():
    if str(CODE) not in sys.path:
        sys.path.insert(0, str(CODE))
    spec = importlib.util.spec_from_file_location("section85_diag_g4_cli", DIAGNOSTIC)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_diagnostic_patches_exact_g4_v551j_and_v552j_clis() -> None:
    diagnostic = load_diagnostic()
    calls: list[list[str]] = []

    def invoke(cmd, timeout_sec, config):
        calls.append(cmd)
        return {"exit_code": 0}

    impl = SimpleNamespace(
        _abs=lambda path, config: f"/repo/{path}",
        _invoke_run=invoke,
        DEFAULT_JOINT_REGISTRY=Path("/repo/default_registry.yaml"),
        run_v551=lambda *args, **kwargs: {},
        run_v551j=lambda *args, **kwargs: {},
        run_v552j=lambda *args, **kwargs: {},
        summarize_v551_functional_gate=lambda path: {},
        summarize_v551j_functional_gate=lambda path: {},
        summarize_v552j_functional_gate=lambda path: {},
    )
    base = SimpleNamespace(_impl=impl, run_wave=lambda *args, **kwargs: {"passed": True})
    diagnostic._patch_base_module(base)

    impl.run_v551j(
        "GSS_2010_US",
        "/tmp/v551/relation_evidence_atoms.parquet",
        "/tmp/v550j/joint_response_pattern_index.parquet",
        "/tmp/v550j/joint_pattern_meaning_summary.parquet",
        "/tmp/v551j",
        "/tmp/v552/structural",
        object(),
        "/tmp/registry.yaml",
    )
    impl.run_v552j(
        "GSS_2010_US",
        "/tmp/v551j/GSS_2010_US",
        "/tmp/v552j",
        "/tmp/v552/structural",
        object(),
    )

    v551j, v552j = calls
    assert v551j[1].endswith("compile_v551j_joint_evidence_packets.py")
    assert v551j[v551j.index("--v551-manifest-path") + 1] == "/tmp/v551/manifest.json"
    assert not any(flag.startswith("--v552-") for flag in v551j)

    assert v552j[1].endswith("compile_v552j_structural_handoff.py")
    assert v552j[v552j.index("--v551j-manifest-path") + 1].endswith("/manifest/manifest.json")
    assert v552j[v552j.index("--v552-manifest-path") + 1] == "/tmp/v552/manifest.json"
    assert "--v551j-run-root" not in v552j
    assert "--strict" not in v552j
