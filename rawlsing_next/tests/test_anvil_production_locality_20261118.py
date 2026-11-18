"""Focused production locality regression: canonical order and CURRENT per yield."""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, VerifiedDirectEstate,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _estate(admission, grant):
    root = Path(admission.estate_path).parents[1]
    return VerifiedDirectEstate(
        root,
        exact_path=admission.estate_path,
        independently_held_manifest_sha256=admission.manifest_sha256,
        independently_held_i02=admission.i02,
        current_authorizer=lambda _roots: grant["ok"],
    )


def test_production_family_order_is_canonical_and_revocation_refuses(
    tmp_path, monkeypatch,
):
    grant = {"ok": True}
    _source, _qa, _predicate, _other, _queries, admission = _fixture(
        monkeypatch, tmp_path / "R5-PROD", "R5-PROD", grant=lambda _roots: grant["ok"],
    )
    estate = _estate(admission, grant)
    with DirectEstateI03Session(estate) as session:
        respondent = next(iter(session.respondents))
        family = None
        refs = []
        for candidate in (
            "RoutingEligibilityFact", "EmpiricalCoordinateFact", "WeightMeasureFact",
        ):
            rows = list(session._respondent_family(candidate, respondent))
            if len(rows) >= 2:
                family = candidate
                refs = [row.ref.key for row in rows]
                break
        assert family is not None, "fixture needs at least two family rows"
        assert refs == sorted(refs), "canonical ref order was not restored"

        # Fresh generator, consume one object, revoke, then require refusal.
        gen = session._respondent_family(family, respondent)
        first = next(gen)
        assert first.ref.key == refs[0]
        grant["ok"] = False
        with pytest.raises(
            DirectEstateError, match="current source/operation authority refused"
        ):
            next(gen)
        grant["ok"] = True


def test_production_selected_fact_matches_native_oracle(tmp_path, monkeypatch):
    source, qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "R5-PARITY", "R5-PARITY",
    )
    result = admission.execute_i03(
        query_ref=queries["selected"].ref, predicate_ref=predicate.ref,
    )
    oracle = native._run(source, qa, predicate, queries["selected"])
    assert tuple(f.ref for f in result.facts) == tuple(f.ref for f in oracle.facts)
    assert canonical_json(result.facts) == canonical_json(oracle.facts)
