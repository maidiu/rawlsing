from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next import pre553_physical_decoder as decoder


DECLARED = {
    "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2": "BIG5",
    "5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2": "WINDOWS-1252",
    "66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec": "WINDOWS-1252",
}


def test_declared_encoding_allowlist_is_exact_and_distinct_from_compatibility_lane():
    assert dict(decoder.DECLARED_ENCODING_ALLOWLIST) == DECLARED
    assert not (set(decoder.DECLARED_ENCODING_ALLOWLIST) & set(decoder.COMPATIBILITY_ALLOWLIST))
    for sha, encoding in DECLARED.items():
        config = decoder._compatibility_config(sha, encoding)
        assert config == {
            "encoding": encoding,
            "authority_status": decoder.SOURCE_DECLARED_ENCODING_ONLY,
        }


def test_declared_encoding_admission_is_sha_and_encoding_exact():
    for sha, encoding in DECLARED.items():
        hostile_encoding = "WINDOWS-1252" if encoding == "BIG5" else "BIG5"
        with pytest.raises(decoder.DecoderError, match="exact SHA/config"):
            decoder._compatibility_config(sha, hostile_encoding)
        with pytest.raises(decoder.DecoderError, match="exact SHA/config"):
            decoder._compatibility_config("0" * 64, encoding)


def test_fault_wrong_hash_and_wrong_encoding_remain_closed():
    big5_sha = next(sha for sha, encoding in DECLARED.items() if encoding == "BIG5")
    win1252_sha = next(sha for sha, encoding in DECLARED.items() if encoding == "WINDOWS-1252")
    with pytest.raises(decoder.DecoderError, match="exact SHA/config representation allowlist"):
        decoder._compatibility_config(big5_sha, "WINDOWS-1252")
    with pytest.raises(decoder.DecoderError, match="exact SHA/config representation allowlist"):
        decoder._compatibility_config(win1252_sha, "BIG5")
    with pytest.raises(decoder.DecoderError, match="exact SHA/config representation allowlist"):
        decoder._compatibility_config("f" * 64, "BIG5")
    with pytest.raises(decoder.DecoderError, match="exact SHA/config representation allowlist"):
        decoder._compatibility_config("f" * 64, "WINDOWS-1252")


@pytest.mark.parametrize("guess", ["auto", "guess", "fallback"])
def test_automatic_encoding_guessing_remains_forbidden(guess):
    with pytest.raises(decoder.DecoderError, match="automatic encoding guessing/fallback is forbidden"):
        decoder._compatibility_config(next(iter(DECLARED)), guess)


def test_no_encoding_override_remains_unprivileged():
    assert decoder._compatibility_config(next(iter(DECLARED)), None) == {
        "encoding": None,
        "authority_status": None,
    }


def test_existing_exact_sha_compatibility_lane_is_conserved():
    sha, encoding = next(iter(decoder.COMPATIBILITY_ALLOWLIST.items()))
    config = decoder._compatibility_config(sha, encoding)
    assert config == {"encoding": encoding, "authority_status": decoder.COMPATIBILITY_ONLY}


def test_declared_lane_does_not_authorize_text_semantics_or_cross_source_inheritance():
    assert "PHYSICAL_DECODING_ONLY" in decoder.SOURCE_DECLARED_ENCODING_ONLY
    first_sha, first_encoding = next(iter(DECLARED.items()))
    other_sha = next(sha for sha in DECLARED if sha != first_sha)
    if DECLARED[other_sha] != first_encoding:
        with pytest.raises(decoder.DecoderError):
            decoder._compatibility_config(other_sha, first_encoding)
    with pytest.raises(decoder.DecoderError):
        decoder._compatibility_config("f" * 64, first_encoding)


def test_fault_synthetic_source_is_refused_by_declared_lane_end_to_end(tmp_path: Path):
    path = tmp_path / "synthetic-not-declared.sav"
    pyreadstat.write_sav(pd.DataFrame({"score": [1.0, 2.0]}), str(path))
    source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(decoder.DecoderError, match="exact SHA/config representation allowlist"):
        decoder.decode_sav(path, encoding="BIG5", expected_source_sha256=source_sha)
    with pytest.raises(decoder.DecoderError, match="automatic encoding guessing/fallback is forbidden"):
        decoder.decode_sav(path, encoding="auto", expected_source_sha256=source_sha)


def test_declared_lane_decodes_end_to_end_with_test_only_synthetic_binding(tmp_path: Path, monkeypatch):
    path = tmp_path / "synthetic-test-bound.sav"
    pyreadstat.write_sav(pd.DataFrame({"score": [1.0, 2.0]}), str(path))
    source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    monkeypatch.setitem(decoder.DECLARED_ENCODING_ALLOWLIST, source_sha, "BIG5")
    incidence = decoder.decode_sav(path, encoding="BIG5", expected_source_sha256=source_sha)
    try:
        assert incidence.reader_configuration["encoding"] == "BIG5"
        assert incidence.reader_configuration["authority_status"] == decoder.SOURCE_DECLARED_ENCODING_ONLY
        assert incidence.reader_configuration["authority_status"] != decoder.COMPATIBILITY_ONLY
        assert [cell.raw_value for cell in incidence.iter_cells(1)] == [1.0, 2.0]
        assert incidence.verify_source_identity() == source_sha
    finally:
        incidence.close()
