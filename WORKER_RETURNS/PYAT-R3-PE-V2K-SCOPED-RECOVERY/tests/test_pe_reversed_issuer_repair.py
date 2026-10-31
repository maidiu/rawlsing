"""Sourcefree regression for PE reversed-issuer competence.

Run with the exact branch rawlsing_next tree on PYTHONPATH and this candidate
module loaded by path. No production source is mutated.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef

CANDIDATE = Path(__file__).parents[1] / "candidate" / "pre553_postastra_pe_generic_world_possibility.py"
spec = importlib.util.spec_from_file_location("pe_candidate", CANDIDATE)
pe = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = pe
spec.loader.exec_module(pe)

VALID = AuthorityRef(
    authority_id="urn:test:postastra-pe:role-reversal-authority:valid",
    authority_version="1.0.0",
    authority_content_hash="a" * 64,
)
FORGED = AuthorityRef(
    authority_id="urn:test:unissued:reversal:WRONG_TOPOLOGY",
    authority_version="999.0.0",
    authority_content_hash="f" * 64,
)
TARGET = ExactRef("TARGET", "urn:test:target", "b" * 64)
DENOM = ExactRef("RISK_SET", "urn:test:risk", "c" * 64)


class Registry:
    def __init__(self) -> None:
        self.snapshot = SimpleNamespace(
            typed_state="ALLOW",
            decision_state="ALLOW",
            governed_operations=(pe.ROLE_REVERSE,),
            governed_object_families=(
                "POSTASTRA_PE_GENERIC_WORLD_SITATED_POSSIBILITY@1.0.0",
            ),
        )

    def require(self, ref, **kwargs):
        if ref.key != VALID.key:
            raise RuntimeError("UNISSUED_OR_FORGED_REVERSAL_AUTHORITY")
        return self.snapshot


def test_shape_auth_alone_is_not_competence():
    # _auth is only shape normalization; it returns a forged caller ref.
    assert pe._auth(FORGED, "role_reversal_authority_ref").key == FORGED.key
    assert pe._reversal_authority_competent(
        Registry(), FORGED, target_ref=TARGET, denominator_basis_ref=DENOM
    ) is False


def test_exact_issued_reversal_authority_is_competent():
    assert pe._reversal_authority_competent(
        Registry(), VALID, target_ref=TARGET, denominator_basis_ref=DENOM
    ) is True
