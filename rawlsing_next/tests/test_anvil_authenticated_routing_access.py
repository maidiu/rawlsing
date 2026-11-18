"""Focused regression for the session-local authenticated routing locator.

The locator is derivative of the admitted C11 estate.  It never supplies
predicate, risk, weight, fact or replay semantics; those remain native.
"""
from __future__ import annotations

from dataclasses import replace
import json

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_query_common import (
    _parse_target_plan, _profile, _ref_field,
)
from rawlsing_next._pre553_query_eval import _build_fact, _evaluate_index_group
from rawlsing_next._pre553_query_predicate import (
    _question_matches, _validate_public_object_authorities,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _ref_from_key(key: str) -> ExactRef:
    kind, rest = key.split("|", 1)
    object_id, digest = rest.rsplit("|", 1)
    return ExactRef(kind, object_id, digest)


def _eval(index, query, predicate, registry):
    plan = _parse_target_plan(query, registry)
    profile = _profile(query)
    evaluation = _evaluate_index_group(
        (index,), query=query, predicate=predicate, plan=plan,
        profile=profile, registry=registry, group_scope=None,
    )
    fact = _build_fact(
        (index,), query=query, predicate=predicate, plan=plan,
        profile=profile, evaluation=evaluation, registry=registry,
    )
    return evaluation, fact


def test_routing_locator_parity_and_exact_key_axes(tmp_path, monkeypatch):
    source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "routing", "ROUTING",
    )
    with admission.prepared_i03() as prepared:
        candidate_index = prepared._session.indices_for(
            query=queries["f4"], release_refs=(admission.release_ref,),
        )[0][1]
        baseline_index = replace(candidate_index, routing_lookup=None)
        assert candidate_index.routing_lookup is not None
        assert baseline_index.routing_lookup is None

        calls = []
        original_lookup = prepared._session._routing_lookup.lookup

        def counted_lookup(*, respondent, target, risk_set):
            calls.append((respondent, target, risk_set))
            yield from original_lookup(
                respondent=respondent, target=target, risk_set=risk_set,
            )

        monkeypatch.setattr(
            prepared._session._routing_lookup, "lookup", counted_lookup,
        )
        registry = admission._runtime_catalog.authority_registry
        for name in ("f4", "f2"):
            candidate_eval, candidate_fact = _eval(
                candidate_index, queries[name], predicate, registry,
            )
            baseline_eval, baseline_fact = _eval(
                baseline_index, queries[name], predicate, registry,
            )
            assert candidate_fact.ref == baseline_fact.ref
            assert canonical_json(candidate_fact) == canonical_json(baseline_fact)
            assert candidate_eval.risk_members == baseline_eval.risk_members
            assert candidate_eval.denominator_members == baseline_eval.denominator_members
            assert candidate_eval.used_authority_refs == baseline_eval.used_authority_refs
            assert [o.ref.key for o in candidate_eval.used_objects] == [
                o.ref.key for o in baseline_eval.used_objects
            ]
            public = prepared.execute_i03(
                query_ref=queries[name].ref, predicate_ref=predicate.ref,
            )
            assert public.facts[0].ref == candidate_fact.ref
            assert canonical_json(public.facts[0]) == canonical_json(candidate_fact)

        assert calls
        assert all(len(call) == 3 for call in calls)
        stored = prepared._session._db.execute(
            "SELECT COUNT(*) FROM routing_locator"
        ).fetchone()[0]
        assert stored > 0


def test_locator_equals_full_authoritative_family_with_authority_inputs(
    tmp_path, monkeypatch,
):
    _source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "routing-full-family", "ROUTING-FULL",
    )
    registry = admission._runtime_catalog.authority_registry
    with admission.prepared_i03() as prepared:
        index = prepared._session.indices_for(
            query=queries["f4"], release_refs=(admission.release_ref,),
        )[0][1]
        row = prepared._session._db.execute(
            "SELECT respondent,target,risk_set FROM routing_locator LIMIT 1"
        ).fetchone()
        assert row is not None
        respondent_key, target_key, risk_key = row
        full = list(prepared._session._respondent_family(
            "RoutingEligibilityFact", respondent_key,
        ))
        expected = []
        for fact in full:
            if (_question_matches(fact, _ref_from_key(target_key))
                    and _ref_field(fact, "risk_set_ref").key == risk_key):
                expected.append((
                    fact.ref.key,
                    fact.routing_state,
                    fact.applicability_state,
                    _ref_field(fact, "member_set_replay_ref").key,
                    tuple(sorted(
                        ref.key for ref in (
                            _validate_public_object_authorities(fact, registry)
                        )
                    )),
                ))
        actual = []
        for fact in index.routing_lookup.lookup(
            respondent=respondent_key, target=target_key, risk_set=risk_key,
        ):
            actual.append((
                fact.ref.key, fact.routing_state, fact.applicability_state,
                _ref_field(fact, "member_set_replay_ref").key,
                tuple(sorted(
                    ref.key for ref in _validate_public_object_authorities(
                        fact, registry
                    )
                )),
            ))
        assert actual == sorted(expected, key=lambda item: item[0])
        assert len(actual) == len(expected)
        assert [item[0] for item in actual] == sorted(item[0] for item in actual)


def test_locator_multiple_yields_and_current_between_yields(tmp_path, monkeypatch):
    grant = {"ok": True}
    _source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "routing-multi", "ROUTING-MULTI",
        grant=lambda _roots: grant["ok"],
    )
    with admission.prepared_i03() as prepared:
        index = prepared._session.indices_for(
            query=queries["f4"], release_refs=(admission.release_ref,),
        )[0][1]
        row = prepared._session._db.execute(
            "SELECT respondent,target,risk_set FROM routing_locator LIMIT 1"
        ).fetchone()
        assert row is not None
        respondent, target, risk = row
        db = prepared._session._db
        # Controlled test-only duplicate table: the fixture has one exact
        # routing candidate per key. This tests multiple new-path yields and
        # CURRENT between yields without inventing a conflicting scientific row.
        db.execute("ALTER TABLE routing_locator RENAME TO routing_locator_one")
        db.execute(
            "CREATE TABLE routing_locator(respondent TEXT NOT NULL, "
            "target TEXT NOT NULL, risk_set TEXT NOT NULL, "
            "fact_ref TEXT NOT NULL, member_set TEXT NOT NULL, "
            "gid INTEGER NOT NULL, off INTEGER NOT NULL)"
        )
        db.execute("INSERT INTO routing_locator SELECT * FROM routing_locator_one")
        db.execute(
            "INSERT INTO routing_locator SELECT * FROM routing_locator_one "
            "WHERE respondent=? AND target=? AND risk_set=?",
            (respondent, target, risk),
        )
        db.execute("DROP TABLE routing_locator_one")
        db.commit()
        gen = index.routing_lookup.lookup(
            respondent=respondent, target=target, risk_set=risk,
        )
        assert next(gen).ref is not None
        grant["ok"] = False
        with pytest.raises(Exception, match="current source/operation authority refused"):
            next(gen)
        grant["ok"] = True


def test_filtered_missing_routing_and_corrupt_locator_fail_closed(tmp_path, monkeypatch):
    _source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "routing-negative", "ROUTING-NEG",
    )
    with admission.prepared_i03() as prepared:
        index = prepared._session.indices_for(
            query=queries["f4"], release_refs=(admission.release_ref,),
        )[0][1]
        registry = admission._runtime_catalog.authority_registry
        row = prepared._session._db.execute(
            "SELECT respondent,target,risk_set,fact_ref FROM routing_locator "
            "LIMIT 1"
        ).fetchone()
        assert row is not None
        respondent_key, target_key, risk_key, _fact_ref = row
        respondent = prepared._session.respondents[respondent_key]
        target = _ref_from_key(target_key)
        risk = _ref_from_key(risk_key)
        prepared._session._db.execute(
            "DELETE FROM routing_locator WHERE respondent=? AND target=? AND risk_set=?",
            (respondent_key, target_key, risk_key),
        )
        prepared._session._db.commit()
        with pytest.raises(
            Exception, match="routing/risk-set membership fact is unavailable"
        ):
            from rawlsing_next._pre553_query_eval import _routing_fact_for

            _routing_fact_for(
                respondent, index,
                target_ref=target, risk_set_ref=risk, registry=registry,
                used=[], used_auth=[],
            )

        # Reinstate a locator but point it at a different physical ref.
        prepared._session._db.execute(
            "INSERT INTO routing_locator VALUES(?,?,?,?,?,?,?)",
            (
                respondent_key, target_key, risk_key, "not|a|ref",
                "not|a|member", 0, 0,
            ),
        )
        prepared._session._db.commit()
        with pytest.raises(Exception, match="routing locator"):
            list(index.routing_lookup.lookup(
                respondent=respondent_key, target=target_key, risk_set=risk_key,
            ))


def test_routing_locator_revocation_and_cleanup(tmp_path, monkeypatch):
    grant = {"ok": True}
    _source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "routing-current", "ROUTING-CURRENT",
        grant=lambda _roots: grant["ok"],
    )
    with admission.prepared_i03() as prepared:
        prepared.execute_i03(
            query_ref=queries["f4"].ref, predicate_ref=predicate.ref,
        )
        grant["ok"] = False
        with pytest.raises(Exception, match="current source/operation authority refused"):
            prepared.execute_i03(
                query_ref=queries["f2"].ref, predicate_ref=predicate.ref,
            )
        grant["ok"] = True
        prepared.execute_i03(
            query_ref=queries["f2"].ref, predicate_ref=predicate.ref,
        )
    assert prepared._session._db is None
