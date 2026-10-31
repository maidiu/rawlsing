"""Sourcefree severance tests for V2K's exact historical dependency.

These tests do not claim V2K current integration. They prove:
1. the current pre553_issued_workload.py has a different ABI; and
2. the V2K successor cannot import when its exact historical dependency is
   removed, so a missing dependency cannot become a silent green.
"""
from __future__ import annotations

import importlib
import importlib.abc
import sys

import pytest

DEP = "rawlsing_next.pre553_original_workload_contract_v2_candidate"
V2K = "rawlsing_next.pre553_original_identity_v2k_successor_candidate"


def test_current_issued_workload_is_not_v2k_abi():
    current = importlib.import_module("rawlsing_next.pre553_issued_workload")
    for symbol in ("V2ExpectedWorkDeclaration", "v2_bind_semantic_to_dispatch", "V2_SCHEMA_VERSION"):
        assert not hasattr(current, symbol), f"unexpected current ABI {symbol}"


class _BlockHistoricalDependency(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == DEP:
            raise ModuleNotFoundError(f"severed exact dependency: {DEP}")
        return None


def test_v2k_import_fails_when_exact_dependency_severed():
    sys.modules.pop(V2K, None)
    sys.modules.pop(DEP, None)
    blocker = _BlockHistoricalDependency()
    sys.meta_path.insert(0, blocker)
    try:
        with pytest.raises(ModuleNotFoundError, match="severed exact dependency"):
            importlib.import_module(V2K)
    finally:
        sys.meta_path.remove(blocker)
        sys.modules.pop(V2K, None)
        sys.modules.pop(DEP, None)
