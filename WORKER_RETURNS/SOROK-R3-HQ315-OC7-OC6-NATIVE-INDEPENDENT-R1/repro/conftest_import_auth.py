"""OC7 reviewer import-authentication conftest.

Independent of the frozen suites. Asserts that the `custody_protocol` module
actually imported by pytest is the reviewer-staged pinned module, by absolute
path, SHA-256 and Git blob SHA-1. Fails the whole session if the import
identity is not the pinned one, so no reported tally can come from a shadowing
or stale module. Writes the observed import ledger for the evidence return.
"""
import hashlib
import json
import os

import pytest

_EXPECTED_SHA256 = os.environ["OC7_EXPECT_MODULE_SHA256"]
_EXPECTED_BLOB = os.environ["OC7_EXPECT_MODULE_BLOB"]
_EXPECT_BASENAME = os.environ["OC7_EXPECT_MODULE_BASENAME"]  # staged file name
_VARIANT = os.environ["OC7_VARIANT"]

_LEDGER_PATH = os.environ["OC7_IMPORT_LEDGER"]


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def pytest_sessionstart(session):
    import custody_protocol as CP

    abs_file = os.path.realpath(CP.__file__)
    src_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    expect_path = os.path.realpath(os.path.join(src_dir, _EXPECT_BASENAME))

    if abs_file != expect_path:
        raise pytest.UsageError(
            f"OC7 IMPORT AUTHENTICATION FAILURE [{_VARIANT}]: imported "
            f"custody_protocol from {abs_file!r}, expected {expect_path!r}"
        )
    with open(abs_file, "rb") as fh:
        data = fh.read()
    sha = hashlib.sha256(data).hexdigest()
    blob = _git_blob_sha1(data)
    if sha != _EXPECTED_SHA256:
        raise pytest.UsageError(
            f"OC7 IMPORT AUTHENTICATION FAILURE [{_VARIANT}]: module sha256 "
            f"{sha} != pinned {_EXPECTED_SHA256}"
        )
    if blob != _EXPECTED_BLOB:
        raise pytest.UsageError(
            f"OC7 IMPORT AUTHENTICATION FAILURE [{_VARIANT}]: module git blob "
            f"{blob} != pinned {_EXPECTED_BLOB}"
        )

    ledger = {
        "variant": _VARIANT,
        "authenticated": True,
        "module_file_abs": abs_file,
        "module_expected_path": expect_path,
        "module_sha256_observed": sha,
        "module_sha256_pinned": _EXPECTED_SHA256,
        "module_git_blob_sha1_observed": blob,
        "module_git_blob_sha1_pinned": _EXPECTED_BLOB,
        "bytes": len(data),
        "python": os.sys.version.split()[0],
        "public_names_sample": sorted(
            n for n in dir(CP) if not n.startswith("_")
        )[:40],
    }
    with open(_LEDGER_PATH, "a") as fh:
        fh.write(json.dumps(ledger) + "\n")
    print(
        f"\n[OC7 IMPORT AUTHENTICATED] variant={_VARIANT} "
        f"file={abs_file}\n[OC7 IMPORT AUTHENTICATED] sha256={sha} "
        f"git_blob={blob} bytes={len(data)}"
    )
