"""KUDA-082 actual R157 synthetic fixture -> current facade/direct I02 parity.

No original35 file, source read, native scientific issuance or new C11 engine.
"""
from copy import deepcopy

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
from rawlsing_next.pre553_r157_universal_c11_parity import (
    UniversalC11ReceiptError,
    receive_r157_fixture_c11_parity,
)
from rawlsing_next.tests.test_pyat940_s1b_support import build_scenario


@pytest.mark.parametrize("source_format,values", [
    ("SAV", (1.0, 2.0, 0.0, 7.0, 8.0, -1.0, None)),
    ("DTA", (1.0, 1.0, 0.0, None)),
])
def test_actual_current_r157_two_ingress_parity_and_existing_release(
    tmp_path, source_format, values
):
    case = build_scenario(tmp_path / source_format, source_format=source_format, values=values)
    try:
        receipt = receive_r157_fixture_c11_parity(
            config=case["config"], incidence=case["incidence"],
            expected_release_ref=case["release"].release_ref,
            batch_size=3,
        )
        assert receipt.release_ref == case["release"].release_ref
        assert receipt.facade_release_ref == receipt.release_ref
        assert receipt.repository_release_refs == (receipt.release_ref,)
        assert receipt.semantic_release_hash == receipt.release_ref.content_hash
        assert receipt.original_execution == "NOT_RUN"
        assert receipt.source_sha256 == case["source_sha"]
        assert receipt.source_rows == case["rows"]
        assert receipt.family_counts
        assert receipt.m01_m18_coverage
    finally:
        case["incidence"].close()


def test_original_source_config_refused_before_any_physical_iteration(tmp_path, monkeypatch):
    case = build_scenario(tmp_path / "orig", source_format="SAV")
    try:
        document = deepcopy(case["document"])
        document["binding"]["identity_class"] = "ORIGINAL_SOURCE"
        # The raw closed config may independently refuse the forged original
        # claim. If a correct original config is constructible, the receiver
        # must still refuse it without physical access.
        try:
            original = SourceConfig(document)
        except Exception:
            return
        with monkeypatch.context() as m:
            m.setattr(case["incidence"], "iter_cells",
                      lambda *_a, **_k: (_ for _ in ()).throw(
                          AssertionError("ORIGINAL CONFIG MUST NOT TOUCH CELLS")))
            with pytest.raises(UniversalC11ReceiptError,
                               match="EXACT_NONRESPONDENT_FIXTURE_CONFIG_REQUIRED"):
                receive_r157_fixture_c11_parity(
                    config=original, incidence=case["incidence"])
    finally:
        case["incidence"].close()


def test_wrong_pinned_expected_release_ref_is_not_silently_admitted(tmp_path):
    case = build_scenario(tmp_path / "wrong", source_format="SAV")
    try:
        previous = case["release"].release_ref
        false = ExactRef(previous.kind, previous.object_id, "0" * 64)
        with pytest.raises(UniversalC11ReceiptError,
                           match="PINNED_EXPECTED_C11_REF_MISMATCH"):
            receive_r157_fixture_c11_parity(
                config=case["config"], incidence=case["incidence"],
                expected_release_ref=false,
            )
    finally:
        case["incidence"].close()


def test_uncertified_sourcefree_inputs_refused_without_ingress():
    with pytest.raises(UniversalC11ReceiptError, match="EXACT_NONRESPONDENT_FIXTURE"):
        receive_r157_fixture_c11_parity(config=None, incidence=None)
