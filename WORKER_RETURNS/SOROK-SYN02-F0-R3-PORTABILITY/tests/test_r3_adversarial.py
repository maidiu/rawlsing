"""R3 sourcefree adversarial acceptance tests.

They are intentionally run against the immutable R2 tree first (expected RED)
and, only in an isolated copy, against the proposed R3 patches (expected GREEN).
No provider, account entitlement, native C9/C12, survey, production, or source
owner edit is performed by these tests.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(os.environ.get(
    "F0R3_SOURCE_ROOT",
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/f0r3",
)).resolve()
S48 = ROOT / "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
S51 = ROOT / "WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"
S52 = ROOT / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
R3 = ROOT / "WORKER_RETURNS/SOROK-SYN02-F0-R3-PORTABILITY"


def _env(source_root: Path = ROOT) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = os.pathsep.join([str(source_root / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1")])
    env["F0R3_SOURCE_ROOT"] = str(source_root)
    return env


def _fake_cli(tmp_path: Path, *, marker: Path | None = None) -> Path:
    path = tmp_path / "fake-opencode"
    marker_line = "" if marker is None else f"print('CALLED'); Path({str(marker)!r}).write_text('called')"
    path.write_text(
        textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import json
            import sys
            from pathlib import Path
            {marker_line}
            print(json.dumps({{"type": "step_start", "sessionID": "fake"}}))
            print(json.dumps({{"type": "text", "part": {{"text": json.dumps({{"narrative": "x", "self_account": None, "prospective": []}})}}}}))
            print(json.dumps({{"type": "step_finish", "sessionID": "fake"}}))
            """
        ),
        encoding="utf8",
    )
    path.chmod(0o755)
    return path


def test_preloaded_fake_binding_is_refused_before_managed_imports():
    script = textwrap.dedent(
        f"""\
        import sys, types
        sys.path.insert(0, {str(S52)!r})
        fake = types.ModuleType("s51.source_binding")
        fake.source_roots = lambda *a, **k: {{}}
        fake.verify_sources = lambda *a, **k: True
        sys.modules["s51.source_binding"] = fake
        try:
            from s52.source_registry import verify_dependencies
            verify_dependencies()
        except Exception as exc:
            print("REFUSED", type(exc).__name__, getattr(exc, "code", ""))
            raise SystemExit(0)
        print("BYPASS")
        raise SystemExit(1)
        """
    )
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=str(ROOT), env=_env(), capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REFUSED" in result.stdout
    assert "BYPASS" not in result.stdout


def test_managed_no_file_cache_is_refused():
    script = textwrap.dedent(
        f"""\
        import importlib.util, sys, types
        path = {str(S51 / "s51/source_binding.py")!r}
        spec = importlib.util.spec_from_file_location("_r3_binding", path)
        binding = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(binding)
        sys.modules["s52"] = types.ModuleType("s52")
        try:
            binding.verify_sources(check_cache=True)
        except Exception as exc:
            print("REFUSED", getattr(exc, "code", type(exc).__name__))
            raise SystemExit(0)
        print("BYPASS")
        raise SystemExit(1)
        """
    )
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=str(ROOT), env=_env(), capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "REFUSED SOURCE_IMPORT_CACHE_UNBOUND" in result.stdout, result.stdout
    assert "BYPASS" not in result.stdout


def test_empty_manifest_is_refused(tmp_path):
    sys.path.insert(0, str(S51))
    try:
        import s51.source_binding as binding
    finally:
        if sys.path and sys.path[0] == str(S51):
            sys.path.pop(0)
    roots = binding.source_roots(S51, ROOT)
    manifest = json.loads(Path(roots["manifest"]).read_text(encoding="utf8"))
    manifest["sources"] = []
    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps(manifest), encoding="utf8")
    with pytest.raises(Exception) as exc:
        binding.verify_sources(manifest_path=empty, check_cache=False)
    assert getattr(exc.value, "code", "") in {"SOURCE_MANIFEST_TRUNCATED", "SOURCE_EXTERNAL_TRUST_MISSING"} or "SOURCE_MANIFEST_TRUNCATED" in str(exc.value)


def test_external_trust_covers_r30a_vendor_and_s39():
    sys.path.insert(0, str(S51))
    try:
        import s51.source_binding as binding
    finally:
        if sys.path and sys.path[0] == str(S51):
            sys.path.pop(0)
    trust = json.loads((R3 / "external_source_trust.json").read_text(encoding="utf8"))
    paths = {entry["path"] for entry in trust["sources"]}
    assert "vendor/r29p/candidate/stable_actor_binding.py" in paths
    assert "vendor/r29p/r29p/runner.py" in paths
    assert "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/sources.py" in paths
    result = binding.verify_sources(check_cache=False)
    assert result.get("external_verified") == len(trust["sources"])


def test_external_log_dir_refused_before_fake_subprocess(tmp_path, monkeypatch):
    from s48 import product
    marker = tmp_path / "fake-called.marker"
    cli = _fake_cli(tmp_path, marker=marker)
    return_root = tmp_path / "return"
    return_root.mkdir()
    monkeypatch.setattr(product, "RETURN", return_root)
    monkeypatch.setenv("S48_PRODUCT_CLI", str(cli))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-x/model-y")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "variant-z")
    monkeypatch.setenv("S48_PRODUCT_ACCOUNT", "account-alias")
    with pytest.raises(product.ProductCallError) as exc:
        product.run_product_cli(
            "hello", workdir=tmp_path / "work", log_dir=tmp_path / "external-logs"
        )
    assert exc.value.code == "S48_PRODUCT_LOG_DIR_OUTSIDE"
    assert not marker.exists()


def test_fake_cli_receipt_does_not_claim_actual_provider_call(tmp_path, monkeypatch):
    from s48 import product
    cli = _fake_cli(tmp_path)
    return_root = tmp_path / "return"
    return_root.mkdir()
    monkeypatch.setattr(product, "RETURN", return_root)
    monkeypatch.setenv("S48_PRODUCT_CLI", str(cli))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-x/model-y")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "variant-z")
    monkeypatch.setenv("S48_PRODUCT_ACCOUNT", "account-alias")
    result = product.run_product_cli(
        "hello", workdir=tmp_path / "work", log_dir=return_root / "logs"
    )
    receipt = result["call_receipt"]
    assert receipt["actual_provider_call"] is False
    assert receipt.get("account_transport") == "ALIAS_ONLY"
    assert receipt.get("subprocess_completed") is True
    assert receipt.get("provider_call_evidence") == "SOURCEFREE_SUBPROCESS_EVENTS_NOT_PROVIDER_PROOF"

def test_truncated_manifest_missing_required_path_is_refused(tmp_path):
    import hashlib
    sys.path.insert(0, str(S51))
    try:
        import s51.source_binding as binding
    finally:
        if sys.path and sys.path[0] == str(S51):
            sys.path.pop(0)
    roots = binding.source_roots(S51, ROOT)
    manifest = json.loads(Path(roots["manifest"]).read_text(encoding="utf8"))
    manifest["sources"] = manifest["sources"][:-1]
    extra = ROOT / "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py"
    manifest["sources"].append({
        "root": "repo",
        "path": "WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/tests/test_f0_product_portability.py",
        "sha256": hashlib.sha256(extra.read_bytes()).hexdigest(),
    })
    altered = tmp_path / "truncated.json"
    altered.write_text(json.dumps(manifest), encoding="utf8")
    with pytest.raises(Exception) as exc:
        binding.verify_sources(manifest_path=altered, check_cache=False)
    assert getattr(exc.value, "code", "") == "SOURCE_MANIFEST_REQUIRED_PATH_MISSING" or "SOURCE_MANIFEST_REQUIRED_PATH_MISSING" in str(exc.value)
