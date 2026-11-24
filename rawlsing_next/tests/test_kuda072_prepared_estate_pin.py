"""KUDA-072: actual exported prepared-session admission/estate provenance guard.

Sourcefree only. Two independently pinned physical S2-C estates are individually
valid, but cross-pairing A's admission with B's native session must never mint
A's public receipt or compute under A's source claim.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_prepared_saved_i03 import (
    PreparedI03Session,
    PreparedSavedI03Error,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def test_public_prepared_A_admission_B_native_session_refuses_before_receipt(
    tmp_path, monkeypatch,
):
    _, _, predicate_a, _, queries_a, a = _fixture(
        monkeypatch, tmp_path / "admission-A", "SPASITYEL-072-A"
    )
    _, _, _, _, _, b = _fixture(
        monkeypatch, tmp_path / "admission-B", "SPASITYEL-072-B"
    )
    assert a._estate is not b._estate
    assert a.estate_path != b.estate_path

    with DirectEstateI03Session(b._estate) as session_b:
        # Two genuinely valid separately admitted roots are not interchangeable.
        assert session_b.estate is b._estate
        with pytest.raises(
            PreparedSavedI03Error, match="admission/session estate mismatch",
        ):
            PreparedI03Session(a, session_b)
        with a.prepared_i03() as paired:
            receipt = paired.receipt()
            assert receipt.estate_path == a.estate_path
            assert receipt.manifest_sha256 == a.manifest_sha256
            assert receipt.release_ref == a.release_ref
            assert receipt.operations == 0

            with pytest.raises(
                PreparedSavedI03Error, match="binding is immutable",
            ):
                paired._admission = b
            with pytest.raises(
                PreparedSavedI03Error, match="binding is immutable",
            ):
                paired._session = session_b

            ordinary = a.execute_i03(
                query_ref=queries_a["selected"].ref,
                predicate_ref=predicate_a.ref,
            )
            positive = paired.execute_i03(
                query_ref=queries_a["selected"].ref,
                predicate_ref=predicate_a.ref,
            )
            assert positive.facts[0].ref == ordinary.facts[0].ref
            assert paired.receipt().operations == 1

            # The underlying direct-session object is currently mutable.
            # A malicious external retarget cannot make the existing wrapper
            # attest B's physical data as A, even after correct construction.
            saved = paired._session.estate
            paired._session.estate = b._estate
            try:
                with pytest.raises(
                    PreparedSavedI03Error, match="admission/session estate mismatch",
                ):
                    paired.receipt()
                with pytest.raises(
                    PreparedSavedI03Error, match="admission/session estate mismatch",
                ):
                    paired.execute_i03(
                        query_ref=queries_a["selected"].ref,
                        predicate_ref=predicate_a.ref,
                    )
            finally:
                paired._session.estate = saved

            restored = paired.execute_i03(
                query_ref=queries_a["selected"].ref,
                predicate_ref=predicate_a.ref,
            )
            assert restored.facts[0].ref == positive.facts[0].ref
            assert paired.receipt().operations == 2

    # Both contexts must have cleaned up their ephemeral indexes.
    assert not list(Path(a.estate_path).parents[1].glob(".s2c-native-i03-*"))
    assert not list(Path(b.estate_path).parents[1].glob(".s2c-native-i03-*"))


def test_prepared_receipt_after_current_revocation_does_not_claim_current(
    tmp_path, monkeypatch,
):
    from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError

    grant = {"live": True}
    _, _, _, _, _, admission = _fixture(
        monkeypatch, tmp_path / "revocation", "SPASITYEL-072-REV",
        grant=lambda _roots: grant["live"],
    )
    with admission.prepared_i03() as session:
        assert session.receipt().operations == 0
        grant["live"] = False
        with pytest.raises(
            DirectEstateError, match="current source/operation authority refused",
        ):
            session.receipt()
        grant["live"] = True
        assert session.receipt().manifest_sha256 == admission.manifest_sha256


def test_current_revocation_between_open_and_wrapper_bind_cleanup(
    tmp_path, monkeypatch,
):
    """An opened SQLite session must be closed even if the new pin guard fails."""
    from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError

    grant = {"allowed": True}
    _, _, _, _, _, admission = _fixture(
        monkeypatch, tmp_path / "late-revoke", "SPASITYEL-072-LATE-REV",
        grant=lambda _roots: grant["allowed"],
    )
    original_enter = DirectEstateI03Session.__enter__

    def revoke_just_after_successful_open(session):
        result = original_enter(session)
        grant["allowed"] = False
        return result

    monkeypatch.setattr(
        DirectEstateI03Session, "__enter__", revoke_just_after_successful_open,
    )
    with pytest.raises(
        DirectEstateError, match="current source/operation authority refused",
    ):
        with admission.prepared_i03():
            pytest.fail("revoked prepared wrapper must not yield")

    assert not list(Path(admission.estate_path).parents[1].glob(
        ".s2c-native-i03-*",
    ))

    grant["allowed"] = True
    monkeypatch.setattr(DirectEstateI03Session, "__enter__", original_enter)
    with admission.prepared_i03() as restored:
        assert restored.receipt().manifest_sha256 == admission.manifest_sha256
    assert not list(Path(admission.estate_path).parents[1].glob(
        ".s2c-native-i03-*",
    ))
