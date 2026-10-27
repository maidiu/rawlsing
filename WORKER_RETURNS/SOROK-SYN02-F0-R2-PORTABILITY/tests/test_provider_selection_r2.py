"""R2 explicit paid-transport selection tests; no provider is invoked."""
from __future__ import annotations

import os
import stat

import pytest

from s48 import product
from s48.errors import ProductCallError

_ENV = (
    "S48_PRODUCT_CLI",
    "S48_PRODUCT_PROVIDER",
    "S48_PRODUCT_MODEL",
    "S48_PRODUCT_VARIANT",
    "S48_PRODUCT_ACCOUNT",
)


def _clear(monkeypatch):
    for name in _ENV:
        monkeypatch.delenv(name, raising=False)


def _fake_cli(tmp_path, name="opencode"):
    path = tmp_path / name
    path.write_text(
        "#!/bin/sh\n"
        "printf invoked > \"$(dirname \"$0\")/invoked\"\n"
        "exit 0\n",
        encoding="utf8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def test_path_opencode_is_not_a_cli_selection(monkeypatch, tmp_path):
    _clear(monkeypatch)
    fake = _fake_cli(tmp_path)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ.get('PATH', '')}")
    with pytest.raises(ProductCallError) as exc:
        product.run_product_cli(
            "prompt", workdir=tmp_path / "work", log_dir=tmp_path / "logs"
        )
    assert exc.value.code == "S48_PRODUCT_CLI_MISSING"
    assert not (tmp_path / "work").exists()
    assert not (tmp_path / "logs").exists()
    assert not (tmp_path / "invoked").exists()


def test_explicit_selection_and_provider_config(monkeypatch, tmp_path):
    _clear(monkeypatch)
    cli = _fake_cli(tmp_path)
    monkeypatch.setenv("S48_PRODUCT_CLI", str(cli))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-x/model-y")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "high")
    monkeypatch.setenv("S48_PRODUCT_ACCOUNT", "account-alias")
    selection = product.select_product()
    assert selection.cli == str(cli)
    assert selection.provider == "provider-x"
    assert selection.model == "provider-x/model-y"
    assert selection.variant == "high"
    config = product.product_config(selection)
    assert config["model"] == "provider-x/model-y"
    assert config["small_model"] == "provider-x/model-y"
    assert config["enabled_providers"] == ["provider-x"]


def test_provider_model_mismatch_fails_before_directories(monkeypatch, tmp_path):
    _clear(monkeypatch)
    cli = _fake_cli(tmp_path)
    monkeypatch.setenv("S48_PRODUCT_CLI", str(cli))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-y/model-y")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "high")
    monkeypatch.setenv("S48_PRODUCT_ACCOUNT", "account-alias")
    with pytest.raises(ProductCallError) as exc:
        product.run_product_cli(
            "prompt", workdir=tmp_path / "work", log_dir=tmp_path / "logs"
        )
    assert exc.value.code == "S48_PRODUCT_PROVIDER_MODEL_MISMATCH"
    assert not (tmp_path / "work").exists()
    assert not (tmp_path / "logs").exists()
    assert not (tmp_path / "invoked").exists()


def test_missing_model_and_account_fail_typed(monkeypatch, tmp_path):
    _clear(monkeypatch)
    cli = _fake_cli(tmp_path)
    monkeypatch.setenv("S48_PRODUCT_CLI", str(cli))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "high")
    with pytest.raises(ProductCallError) as exc:
        product.select_product()
    assert exc.value.code == "S48_PRODUCT_MODEL_MISSING"
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-x/model-y")
    with pytest.raises(ProductCallError) as exc:
        product.select_product()
    assert exc.value.code == "S48_PRODUCT_ACCOUNT_MISSING"


def test_relative_or_non_executable_cli_is_rejected(monkeypatch, tmp_path):
    _clear(monkeypatch)
    relative = tmp_path / "relative-cli"
    relative.write_text("#!/bin/sh\nexit 0\n", encoding="utf8")
    monkeypatch.setenv("S48_PRODUCT_CLI", str(relative))
    monkeypatch.setenv("S48_PRODUCT_PROVIDER", "provider-x")
    monkeypatch.setenv("S48_PRODUCT_MODEL", "provider-x/model-y")
    monkeypatch.setenv("S48_PRODUCT_VARIANT", "high")
    monkeypatch.setenv("S48_PRODUCT_ACCOUNT", "account-alias")
    with pytest.raises(ProductCallError) as exc:
        product.select_product()
    assert exc.value.code in {
        "S48_PRODUCT_CLI_INVALID",
        "S48_PRODUCT_CLI_NOT_ABSOLUTE",
    }
