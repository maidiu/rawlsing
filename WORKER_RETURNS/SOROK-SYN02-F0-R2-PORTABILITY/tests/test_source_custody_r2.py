"""R2 source custody, containment, manifest and import-order adversaries."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from s52.bootstrap import REPO, install
from s52.source_registry import source_roots, verify_dependencies

install()

import s51.source_binding as binding  # noqa: E402
from s51.source_binding import SourceBindingError  # noqa: E402


def _accepted_g18() -> Path:
    return Path(source_roots()["g18"])


def _s52_path() -> Path:
    return REPO / "WORKER_RETURNS/SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"


def _copy_g18(target: Path) -> Path:
    target.mkdir(parents=True)
    shutil.copytree(_accepted_g18() / "lab_sgi1", target / "lab_sgi1")
    return target


def test_manifest_verifies_bounded_closure():
    result = binding.verify_sources()
    assert result["verified"] == 31
    assert Path(result["roots"]["g18"]).is_dir()
    assert Path(result["roots"]["r30a"]).is_dir()
    assert verify_dependencies() is True


def test_symlink_g18_root_is_refused(monkeypatch, tmp_path):
    outside = _copy_g18(tmp_path / "outside")
    fake = tmp_path / "fake-root"
    fake.mkdir()
    link = fake / "g18"
    os.symlink(outside, link)
    monkeypatch.setenv("S52_G18_SOURCE", str(link))
    monkeypatch.setenv("S52_ALLOWED_ROOTS", str(tmp_path))
    with pytest.raises(SourceBindingError) as exc:
        source_roots()
    assert exc.value.code == "G18_SOURCE_SYMLINK"


def test_conflicting_g18_environment_is_refused(monkeypatch, tmp_path):
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.mkdir()
    two.mkdir()
    monkeypatch.setenv("S52_G18_SOURCE", str(one))
    monkeypatch.setenv("S51_G18_SOURCE", str(two))
    monkeypatch.setenv("S52_ALLOWED_ROOTS", str(tmp_path))
    with pytest.raises(SourceBindingError) as exc:
        source_roots()
    assert exc.value.code == "G18_SOURCE_ENV_CONFLICT"


def test_changed_unlisted_g18_module_fails_before_import(monkeypatch, tmp_path):
    changed = _copy_g18(tmp_path / "changed")
    marker = tmp_path / "imported.marker"
    init = changed / "lab_sgi1" / "__init__.py"
    init.write_text(
        init.read_text(encoding="utf8")
        + f"\nopen({str(marker)!r}, 'w', encoding='utf8').write('executed')\n",
        encoding="utf8",
    )
    monkeypatch.setenv("S52_G18_SOURCE", str(changed))
    monkeypatch.setenv("S52_ALLOWED_ROOTS", str(tmp_path))
    with pytest.raises(SourceBindingError) as exc:
        binding.verify_sources(check_cache=False)
    assert exc.value.code == "SOURCE_HASH_MISMATCH"
    assert not marker.exists()


def test_wrong_manifest_role_is_refused(tmp_path):
    source_manifest = Path(source_roots()["manifest"])
    value = json.loads(source_manifest.read_text(encoding="utf8"))
    value["roots"]["repo"]["role"] = "WRONG_ROLE"
    altered = tmp_path / "altered.json"
    altered.write_text(json.dumps(value), encoding="utf8")
    with pytest.raises(SourceBindingError) as exc:
        binding.verify_sources(manifest_path=altered, check_cache=False)
    assert exc.value.code == "SOURCE_PROVENANCE_INVALID"


def test_bootstrap_fails_before_s49_import_and_without_side_effect(monkeypatch, tmp_path):
    changed = _copy_g18(tmp_path / "changed")
    marker = tmp_path / "imported.marker"
    init = changed / "lab_sgi1" / "__init__.py"
    init.write_text(
        init.read_text(encoding="utf8")
        + f"\nopen({str(marker)!r}, 'w', encoding='utf8').write('executed')\n",
        encoding="utf8",
    )
    env = dict(os.environ)
    for key in ("S52_G18_SOURCE", "S51_G18_SOURCE", "G18_SOURCE", "M35_G18_SOURCE"):
        env.pop(key, None)
    env.update(
        {
            "S52_G18_SOURCE": str(changed),
            "S52_ALLOWED_ROOTS": str(tmp_path),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    script = f"""
import sys
sys.path.insert(0, {str(_s52_path())!r})
try:
    from s52.bootstrap import install
    install()
except Exception as exc:
    print(type(exc).__name__, getattr(exc, 'code', ''))
    print('s49_loaded', 's49' in sys.modules)
    print('lab_loaded', 'lab_sgi1' in sys.modules)
    raise SystemExit(0 if getattr(exc, 'code', '') == 'SOURCE_HASH_MISMATCH' else 2)
raise SystemExit(3)
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "s49_loaded False" in result.stdout
    assert "lab_loaded False" in result.stdout
    assert not marker.exists()


def test_poison_preloaded_g18_is_refused_before_s49_import(monkeypatch, tmp_path):
    poison = _copy_g18(tmp_path / "poison")
    env = dict(os.environ)
    for key in ("S52_G18_SOURCE", "S51_G18_SOURCE", "G18_SOURCE", "M35_G18_SOURCE"):
        env.pop(key, None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    script = f"""
import sys
sys.path.insert(0, {str(poison)!r})
import lab_sgi1.history
sys.path.insert(0, {str(_s52_path())!r})
try:
    from s52.bootstrap import install
    install()
except Exception as exc:
    print(type(exc).__name__, getattr(exc, 'code', ''))
    print('s49_loaded', 's49' in sys.modules)
    raise SystemExit(0 if getattr(exc, 'code', '') == 'SOURCE_IMPORT_CACHE_FOREIGN' else 2)
raise SystemExit(3)
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", script],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "s49_loaded False" in result.stdout


def test_manifest_covers_all_g18_package_files():
    manifest = json.loads(Path(source_roots()["manifest"]).read_text(encoding="utf8"))
    paths = {
        entry["path"] for entry in manifest["sources"] if entry["root"] == "g18"
    }
    assert paths == {
        "lab_sgi1/__init__.py",
        "lab_sgi1/core.py",
        "lab_sgi1/proposal.py",
        "lab_sgi1/joint.py",
        "lab_sgi1/history.py",
    }


def test_traversal_and_absolute_paths_are_refused(tmp_path):
    for relpath in ("../outside.py", "/etc/hosts"):
        with pytest.raises(SourceBindingError) as exc:
            binding.verify_expected(tmp_path, {relpath: "0" * 64})
        assert exc.value.code == "SOURCE_PATH_INVALID"


def test_symlinked_file_inside_root_is_refused(tmp_path):
    root = _copy_g18(tmp_path / "linked")
    outside = tmp_path / "outside-joint.py"
    outside.write_text("outside", encoding="utf8")
    target = root / "lab_sgi1" / "joint.py"
    target.unlink()
    os.symlink(outside, target)
    with pytest.raises(SourceBindingError) as exc:
        binding.verify_expected(root, {"lab_sgi1/joint.py": "0" * 64})
    assert exc.value.code == "SOURCE_PATH_SYMLINK"


def test_changed_g18_core_before_import_is_refused(monkeypatch, tmp_path):
    changed = _copy_g18(tmp_path / "changed-core")
    core = changed / "lab_sgi1" / "core.py"
    core.write_text(core.read_text(encoding="utf8") + "\nCHANGED = True\n", encoding="utf8")
    monkeypatch.setenv("S52_G18_SOURCE", str(changed))
    monkeypatch.setenv("S52_ALLOWED_ROOTS", str(tmp_path))
    with pytest.raises(SourceBindingError) as exc:
        binding.verify_sources(check_cache=False)
    assert exc.value.code == "SOURCE_HASH_MISMATCH"
