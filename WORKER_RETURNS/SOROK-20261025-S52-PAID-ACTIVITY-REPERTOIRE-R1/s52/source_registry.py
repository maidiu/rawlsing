"""Fail-closed dependency verification for S52's accepted source seams.

S52 must not silently run against a different S49/S51/G18 revision.  The roots
come from the portable S51 bootstrap; this module verifies the exact accepted
file hashes before the session is allowed to import or execute.
"""
from __future__ import annotations

from pathlib import Path
from typing import Mapping

EXPECTED = {
    "s49": {
        "s49/actor.py": "c2a889c825807c174cdc91ce4ec08cde07c2e6e0575fadf9ee97185324c5eb95",
        "s49/session.py": "9932029c529a399ffedb24545ea5d0f6884a5fe8719ffc39c8af9fe1db0f3625",
    },
    "s51": {
        "s51/session.py": "6ef8e92eb3ea2d83cfdb5aba1121ed42f1706a0df9bc3f36aff2b91a47596a82",
    },
}

G18_EXPECTED = {
    "lab_sgi1/joint.py": "755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9",
    "lab_sgi1/history.py": "2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1",
}


def verify_dependencies(roots: Mapping[str, str]) -> bool:
    """Verify every required dependency; raise on missing or changed source."""
    from s51.source_binding import SourceBindingError, verify_expected

    required = {
        "s49_return": EXPECTED["s49"],
        "s51_return": EXPECTED["s51"],
        "g18_source": G18_EXPECTED,
    }
    for root_key, expected in required.items():
        raw_root = roots.get(root_key)
        if not raw_root:
            raise SourceBindingError("SOURCE_ROOT_MISSING", root_key)
        verify_expected(Path(raw_root), expected)
    return True


__all__ = ["EXPECTED", "G18_EXPECTED", "verify_dependencies"]
