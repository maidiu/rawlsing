"""W05/P03: physical respondent iteration on a verified saved C11 index.

Author candidate tests, NOT evidence that large sourcefree/native economics
or source/rights/G5 have been independently executed.  The independent #1036
physical-locality experiment is source-grounding, not production authority.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from rawlsing_next._pre553_query_eval import (
    _query_respondents,
    _respondent_root,
)
from rawlsing_next.pre553_empirical_objects import ExactRef


def _fake_index(*, physical: bool):
    # Intentionally NON-canonical insertion order, mimicking an authenticated
    # physical estate whose row-group order differs from a semantic ref sort.
    respondents = {
        "z": SimpleNamespace(ref=ExactRef(
            "RespondentIdentity@1.0.0", "urn:pyat:w05:z", "a" * 64,
        )),
        "a": SimpleNamespace(ref=ExactRef(
            "RespondentIdentity@1.0.0", "urn:pyat:w05:a", "b" * 64,
        )),
    }
    return SimpleNamespace(
        respondents=respondents,
        native_verified_physical_respondent_order=physical,
    )


def test_w05_legacy_index_remains_canonical_and_native_uses_physical_order():
    legacy = _fake_index(physical=False)
    physical = _fake_index(physical=True)
    native_iterated = [obj.ref.key for obj in _query_respondents(physical)]
    legacy_iterated = [obj.ref.key for obj in _query_respondents(legacy)]
    assert native_iterated == [obj.ref.key for obj in physical.respondents.values()]
    assert legacy_iterated == sorted(native_iterated)
    assert native_iterated != legacy_iterated
    # Output-root identity must be canonical even if the evaluator visits
    # respondents in native physical order.
    assert _respondent_root(legacy) == _respondent_root(physical)


def test_w05_real_saved_i03_uses_verified_physical_order_with_exact_native_parity(
    tmp_path, monkeypatch,
):
    pytest.importorskip("pyarrow")
    import rawlsing_next._pre553_query_eval as evaluator
    import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
    import rawlsing_next.tests.test_pre553_empirical_query as native

    source, candidate = s2c._source_with_candidate(
        monkeypatch, "W05-VERIFIED-PHYSICAL", 1,
    )
    qauth = native._query_authority("W05-VERIFIED-PHYSICAL")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(
        source, qauth, predicate, ("Y",),
        tag="W05-VERIFIED-PHYSICAL",
    )
    expected = native._run(source, qauth, predicate, query)
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref,
        "w05-verified-native",
    )
    executor = s2c._executor(
        root, receipt, source, qauth, predicate, query,
    )

    used_native = []
    normal = evaluator._query_respondents

    def recorded(index):
        used_native.append(index.native_verified_physical_respondent_order)
        return normal(index)

    with monkeypatch.context() as patch:
        patch.setattr(evaluator, "_query_respondents", recorded)
        actual = executor.execute_i03(
            query_ref=query.ref, predicate_ref=predicate.ref,
        )

    assert used_native and all(used_native)
    assert tuple(x.ref for x in actual.facts) == tuple(x.ref for x in expected.facts)
    assert s2c._fact_signature(actual) == s2c._fact_signature(expected)
    assert actual.release_refs == expected.release_refs


def test_w05_new_native_order_refuses_revoked_current(tmp_path, monkeypatch):
    pytest.importorskip("pyarrow")
    import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
    import rawlsing_next.tests.test_pre553_empirical_query as native
    from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError

    source, candidate = s2c._source_with_candidate(
        monkeypatch, "W05-VERIFIED-REVOKED", 1,
    )
    qauth = native._query_authority("W05-VERIFIED-REVOKED")
    predicate = native._branch_predicate(source, qauth)
    query = native._query(
        source, qauth, predicate, ("Y",),
        tag="W05-VERIFIED-REVOKED",
    )
    root, receipt = s2c._cold(
        tmp_path, candidate, source["universe"].ref, "w05-revoked",
    )
    grant = {"now": True}
    executor = s2c._executor(
        root, receipt, source, qauth, predicate, query,
        grant=lambda _: grant["now"],
    )
    grant["now"] = False
    with pytest.raises(DirectEstateError, match="current source/operation authority refused"):
        executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
