"""F0 conditional transport checks for S48's product CLI surface."""
from __future__ import annotations

from pathlib import Path

import pytest

from s48 import product
from s48.errors import ProductCallError


def test_missing_product_cli_is_typed_before_subprocess(monkeypatch, tmp_path):
    for name in (
        "S48_PRODUCT_CLI",
        "S48_PRODUCT_PROVIDER",
        "S48_PRODUCT_MODEL",
        "S48_PRODUCT_VARIANT",
        "S48_PRODUCT_ACCOUNT",
    ):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ProductCallError) as exc:
        product.run_product_cli(
            "prompt",
            workdir=tmp_path / "work",
            log_dir=tmp_path / "logs",
        )
    assert exc.value.code == "S48_PRODUCT_CLI_MISSING"
    assert not (tmp_path / "work").exists()
    assert not (tmp_path / "logs").exists()


def test_product_cli_is_not_a_fixed_user_path():
    source = (Path(__file__).resolve().parents[1] / "s48/product.py").read_text()
    assert "/Users/" not in source
    assert "S48_PRODUCT_CLI" in source
    assert "shutil.which" not in source
    assert "opencode-go/deepseek-v4.1-flash" not in source
