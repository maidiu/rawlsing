"""PYAT HQ292 I01K — typed selection-key restore repair tests.

Tests for the typed selection-key identity validation in restore_product.
No raw survey access, no external issuer, no protected CURRENT.
"""
from __future__ import annotations

import json
import pytest

import rawlsing_next.pre553_i01_sourcefree_world_lifecycle_candidate as I


def _build_and_get_root(tmp_path):
    p, _ = I.build_product(tmp_path)
    return tmp_path, p


def test_hq292_i01k_correct_saved_key_restores(tmp_path):
    """A correct saved selection key still restores successfully."""
    root, p = _build_and_get_root(tmp_path)
    restored = I.restore_product(root)
    assert restored is not None
    assert restored.selection_key.ref == p.selection_key.ref


def test_hq292_i01k_missing_key_returns_typed_i01error(tmp_path):
    """A missing selection_key_ref returns typed I01Error, not StopIteration."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    del data['selection_key_ref']
    I.save_json(path, data)
    with pytest.raises(I.I01Error) as excinfo:
        I.restore_product(root)
    assert 'SAVED_SELECTION_KEY_IDENTITY_MISMATCH' in str(excinfo.value)


def test_hq292_i01k_forged_key_returns_typed_i01error(tmp_path):
    """A forged selection_key_ref returns typed I01Error, not StopIteration."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    data['selection_key_ref'] = p.subject_ref.as_dict()
    I.save_json(path, data)
    with pytest.raises(I.I01Error) as excinfo:
        I.restore_product(root)
    assert 'SAVED_SELECTION_KEY_IDENTITY_MISMATCH' in str(excinfo.value)


def test_hq292_i01k_foreign_key_returns_typed_i01error(tmp_path):
    """A foreign selection_key_ref returns typed I01Error."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    data['selection_key_ref'] = {
        'kind': 'B5Lifecycle:SELECTION_KEY',
        'object_id': 'urn:foreign:key:sha256:' + '0' * 64,
        'content_hash': '0' * 64,
    }
    I.save_json(path, data)
    with pytest.raises(I.I01Error) as excinfo:
        I.restore_product(root)
    assert 'SAVED_SELECTION_KEY_IDENTITY_MISMATCH' in str(excinfo.value)


def test_hq292_i01k_malformed_key_returns_typed_i01error(tmp_path):
    """A malformed selection_key_ref returns typed I01Error."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    data['selection_key_ref'] = 'not_a_dict'
    I.save_json(path, data)
    with pytest.raises(I.I01Error) as excinfo:
        I.restore_product(root)
    assert 'SAVED_SELECTION_KEY_IDENTITY_MISMATCH' in str(excinfo.value)


def test_hq292_i01k_invalid_type_key_returns_typed_i01error(tmp_path):
    """An invalid-type selection_key_ref returns typed I01Error."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    data['selection_key_ref'] = 12345
    I.save_json(path, data)
    with pytest.raises(I.I01Error) as excinfo:
        I.restore_product(root)
    assert 'SAVED_SELECTION_KEY_IDENTITY_MISMATCH' in str(excinfo.value)


def test_hq292_i01k_no_product_constructed_on_negative(tmp_path):
    """A forged key must NOT construct a Product."""
    root, p = _build_and_get_root(tmp_path)
    path = root / 'product_index.json'
    data = json.loads(path.read_text())
    data['selection_key_ref'] = p.subject_ref.as_dict()
    I.save_json(path, data)
    with pytest.raises(I.I01Error):
        I.restore_product(root)
    # No Product was returned; restore_product raised before constructing one
