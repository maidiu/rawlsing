from __future__ import annotations

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
