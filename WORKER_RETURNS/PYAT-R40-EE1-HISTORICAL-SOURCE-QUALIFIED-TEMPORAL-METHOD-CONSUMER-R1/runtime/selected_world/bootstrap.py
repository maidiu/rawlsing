"""Pinned import bootstrap for the R35 T35 two-epoch native world court.

Only staged non-sealed owner modules are loaded by path; every other
``rawlsing_next`` module is the exact sealed-HEAD byte image.  No network, no
original source, no wall clock, no actor.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
RETURN = RUNTIME.parent
REPO = RETURN.parents[1]
SELECTED = RUNTIME / "selected"
FIXTURE = SELECTED / "fixtures" / "02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"
FREEZE = RETURN / "01_FROZEN_CLOCK_AND_N8E_METHOD_EXPECTATIONS.json"
SEALED = "5064d76b3c58a8225693055a8ec6bb07e216d9b1"
R10_PRODUCT = ("9c96f201f3530d2dae321201e9a913bb7a61800f",
               "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1/product/")
R10_COURT = ("9c96f201f3530d2dae321201e9a913bb7a61800f",
             "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1/repro/test_product.py")
R13_ADAPTER = ("84485d32c0088995f8dc664dc0517b2d27f2563d",
               "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R13-E05R-SELECTED-WORLD-REPAIR-R1/candidate/e05r_selected_world_adapter.py")
HQ297_READER = ("9ab4a0192b7c951bb0b387637e6c74333246766c",
                "rawlsing_next/pre553_hq297_n9c_two_field_reader.py")
HQ297_FIXTURE = ("9ab4a0192b7c951bb0b387637e6c74333246766c",
                 "WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json")
E03 = ("0e0ed50dbce2dd1434d3a3c84b937b9a956adba9",
       "rawlsing_next/pre553_n9_n10w_progressive_candidate.py")

_EXTRA = {
    "rawlsing_next.pre553_hq297_n9c_two_field_reader":
        SELECTED / "native_extra" / "pre553_hq297_n9c_two_field_reader.py",
    "rawlsing_next.pre553_n9_n10w_progressive_candidate":
        SELECTED / "native_extra" / "pre553_n9_n10w_progressive_candidate.py",
}
_INSTALLED = False
_FREEZE_CACHE = None


def _load_native(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError("NO_SPEC:" + name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    import rawlsing_next
    setattr(rawlsing_next, name.rsplit(".", 1)[-1], module)
    return module


def install() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    for path in (str(SELECTED), str(REPO), str(REPO / "rawlsing_next"),
                 str(REPO / "rawlsing_next" / "tests")):
        if path not in sys.path:
            sys.path.insert(0, path)
    import rawlsing_next  # noqa: F401
    for name, path in _EXTRA.items():
        _load_native(name, path)
    _INSTALLED = True


def fixture_rows() -> list:
    return json.loads(FIXTURE.read_text())["fields"]


def freeze() -> dict:
    global _FREEZE_CACHE
    if _FREEZE_CACHE is None:
        _FREEZE_CACHE = json.loads(FREEZE.read_text())
    return _FREEZE_CACHE


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def staged_source_path(path: Path):
    """Return (commit, source_path) for a staged file, or None."""
    try:
        rel = path.resolve().relative_to(RETURN).as_posix()
    except ValueError:
        return None
    if rel.startswith("runtime/selected/product/"):
        return R10_PRODUCT[0], R10_PRODUCT[1] + path.name
    if rel == "runtime/selected/e05_n9_selected_world_adapter.py":
        return R13_ADAPTER
    if rel == "runtime/selected/native_extra/pre553_hq297_n9c_two_field_reader.py":
        return HQ297_READER
    if rel == "runtime/selected/native_extra/pre553_n9_n10w_progressive_candidate.py":
        return E03
    if rel == "runtime/selected/fixtures/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json":
        return HQ297_FIXTURE
    if rel == "runtime/author_courts/test_product_r10.py":
        return R10_COURT
    return None


def frozen_pin(source_path: str):
    for pin in freeze()["pinned_closure"]:
        if pin["path"] == source_path:
            return pin
    return None
