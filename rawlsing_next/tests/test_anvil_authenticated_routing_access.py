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
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next._pre553_query_predicate import _build_release_index
from rawlsing_next.tests.test_pre553_empirical_query import _registry, _ref
from rawlsing_next.tests.test_pre553_i03_scale_equivalence_repair import _joint_fixture
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
from rawlsing_next._pre553_query_eval import _build_fact, _evaluate_index_group
from rawlsing_next._pre553_query_predicate import (
    _question_matches, _validate_public_object_authorities,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, RoutingEligibilityFact, canonical_json,
)
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
        original_lookup = DirectEstateI03Session._routing_facts

        def counted_lookup(self, *, respondent, target, risk_set):
            calls.append((respondent, target, risk_set))
            yield from original_lookup(
                self, respondent=respondent, target=target, risk_set=risk_set,
            )

        monkeypatch.setattr(DirectEstateI03Session, "_routing_facts", counted_lookup)
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
        for fact in index.routing_lookup(
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
            "fact_ref TEXT NOT NULL, gid INTEGER NOT NULL, "
            "off INTEGER NOT NULL)"
        )
        db.execute("INSERT INTO routing_locator SELECT * FROM routing_locator_one")
        db.execute(
            "INSERT INTO routing_locator SELECT * FROM routing_locator_one "
            "WHERE respondent=? AND target=? AND risk_set=?",
            (respondent, target, risk),
        )
        db.execute("DROP TABLE routing_locator_one")
        db.commit()
        gen = index.routing_lookup(
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
            "INSERT INTO routing_locator VALUES(?,?,?,?,?,?)",
            (
                respondent_key, target_key, risk_key, "not|a|ref",
                0, 0,
            ),
        )
        prepared._session._db.commit()
        with pytest.raises(Exception, match="routing locator"):
            list(index.routing_lookup(
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

def test_two_distinct_canonical_locator_matches_and_used_authority(tmp_path, monkeypatch):
    source, qa, _predicate, _query_spec = _joint_fixture("repair-conflict")
    release = source["repo"].resolve_release_exact(source["release_ref"])
    index = _build_release_index(release, source["universe"].ref)
    respondent = source["respondents"]["R1"]
    base = next(
        fact for fact in index.routing_by_respondent[respondent.ref.key]
        if fact.question_or_target_ref in (
            source["qrefs"]["X"], source["qrefs"]["X"].as_dict(),
        )
    )
    conflict = RoutingEligibilityFact(
        typed_state="NOT_ELIGIBLE",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "repair-conflict-second",
        ),
        empirical_universe_ref=base.empirical_universe_ref,
        scoped_respondent_ref=base.scoped_respondent_ref,
        question_or_target_ref=base.question_or_target_ref,
        risk_set_ref=base.risk_set_ref,
        routing_rule_ref=base.routing_rule_ref,
        applicability_state="NOT_ELIGIBLE",
        routing_state="NOT_ELIGIBLE",
        parent_predicate_refs=base.parent_predicate_refs,
        member_set_replay_ref=base.member_set_replay_ref,
    )
    registry = _registry(source, qa)
    target = _ref_field(base, "question_or_target_ref")
    risk = _ref_field(base, "risk_set_ref")
    adapter_index = replace(
        index, routing_lookup=lambda **_kwargs: iter((conflict, base)),
    )
    both = list(adapter_index.routing_lookup(
        respondent=respondent.ref.key, target=target.key, risk_set=risk.key,
    ))
    assert [f.ref.key for f in both] == sorted(
        [base.ref.key, conflict.ref.key]
    )
    with pytest.raises(Exception, match="conflicting exact routing/risk-set facts"):
        from rawlsing_next._pre553_query_eval import _routing_fact_for
        _routing_fact_for(
            respondent, adapter_index, target_ref=target, risk_set_ref=risk,
            registry=registry, used=[], used_auth=[],
        )
    # Same state/member-set but distinct canonical refs must both enter
    # used and authority validation without changing the conflict guard.
    twin = RoutingEligibilityFact(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "repair-conflict-twin",
        ),
        empirical_universe_ref=base.empirical_universe_ref,
        scoped_respondent_ref=base.scoped_respondent_ref,
        question_or_target_ref=base.question_or_target_ref,
        risk_set_ref=base.risk_set_ref,
        routing_rule_ref=base.routing_rule_ref,
        applicability_state=base.applicability_state,
        routing_state=base.routing_state,
        parent_predicate_refs=base.parent_predicate_refs,
        member_set_replay_ref=base.member_set_replay_ref,
    )
    twin_index = replace(
        index, routing_lookup=lambda **_kwargs: iter((twin, base)),
    )
    used, used_auth = [], []
    from rawlsing_next._pre553_query_eval import _routing_fact_for
    returned = _routing_fact_for(
        respondent, twin_index, target_ref=target, risk_set_ref=risk,
        registry=registry, used=used, used_auth=used_auth,
    )
    assert {fact.ref.key for fact in used} == {base.ref.key, twin.ref.key}
    assert returned.ref.key in {base.ref.key, twin.ref.key}
    assert used_auth


def test_malformed_routing_projection_refuses_at_preparation(tmp_path, monkeypatch):
    import rawlsing_next.pre553_direct_estate_i03 as direct
    _source, _qa, _predicate, _other, _queries, admission = _fixture(
        monkeypatch, tmp_path / "routing-malformed", "ROUTING-MALFORMED",
    )
    original = direct._object_from_row

    def corrupt(row):
        obj = original(row)
        if isinstance(obj, direct.RoutingEligibilityFact):
            return object()
        return obj

    monkeypatch.setattr(direct, "_object_from_row", corrupt)
    with pytest.raises(Exception, match="routing body/ref"):
        with admission.prepared_i03():
            pass

def test_physical_canonical_conflict_is_returned_and_refused(tmp_path, monkeypatch):
    import rawlsing_next.tests.test_pre553_empirical_query as native
    holder = {}
    original_ingest = native.ingest_c11_source_release

    def mutate(candidate, repo):
        base = next(iter(
            candidate.routing_eligibility_facts_or_exact_rules
        ))
        conflict = RoutingEligibilityFact(
            typed_state="NOT_ELIGIBLE",
            authority_snapshot_refs=base.authority_snapshot_refs,
            dependency_refs=base.dependency_refs,
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", "physical-conflict-second",
            ),
            empirical_universe_ref=base.empirical_universe_ref,
            scoped_respondent_ref=base.scoped_respondent_ref,
            question_or_target_ref=base.question_or_target_ref,
            risk_set_ref=base.risk_set_ref,
            routing_rule_ref=base.routing_rule_ref,
            applicability_state="NOT_ELIGIBLE",
            routing_state="NOT_ELIGIBLE",
            parent_predicate_refs=base.parent_predicate_refs,
            member_set_replay_ref=base.member_set_replay_ref,
        )
        counts = dict(
            candidate.source_release_manifest.declared_record_counts_by_logical_family
        )
        counts["RoutingEligibilityFact"] += 1
        manifest = replace(
            candidate.source_release_manifest,
            declared_record_counts_by_logical_family=counts,
        )
        old = candidate.candidate_replay_manifest
        candidate = replace(
            candidate,
            source_release_manifest=manifest,
            routing_eligibility_facts_or_exact_rules=(
                *candidate.routing_eligibility_facts_or_exact_rules, conflict,
            ),
            candidate_replay_manifest=None,
        )
        replay = build_candidate_replay_manifest(
            candidate,
            replay_protocol_authority_ref=old.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=old.deterministic_tie_order_rules_ref,
            replay_protocol_version=old.replay_protocol_version,
        )
        candidate = replace(candidate, candidate_replay_manifest=replay)
        holder["candidate"] = candidate
        holder["base"] = base
        return original_ingest(candidate, repo)

    monkeypatch.setattr(native, "ingest_c11_source_release", mutate)
    source, _qa, predicate, _other, queries, _admission = _fixture(
        monkeypatch, tmp_path / "physical-source", "PHYSICAL-CONFLICT",
    )
    candidate = holder["candidate"]
    base = holder["base"]
    (tmp_path / "physical-estate").mkdir()
    root, receipt = s2c._cold(
        tmp_path / "physical-estate", candidate, source["universe"].ref,
        "PHYSICAL-CONFLICT",
    )
    estate = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    with DirectEstateI03Session(estate) as session:
        index = session.indices_for(
            query=queries["f4"], release_refs=(source["release_ref"],),
        )[0][1]
        respondent = session.respondents[_ref_field(base, "scoped_respondent_ref").key]
        target = _ref_field(base, "question_or_target_ref")
        risk = _ref_field(base, "risk_set_ref")
        facts = list(index.routing_lookup(
            respondent=respondent.ref.key, target=target.key,
            risk_set=risk.key,
        ))
        assert len(facts) == 2
        assert [f.ref.key for f in facts] == sorted(f.ref.key for f in facts)
        assert {f.routing_state for f in facts} == {"ELIGIBLE_APPLICABLE", "NOT_ELIGIBLE"}
        with pytest.raises(Exception, match="conflicting exact routing/risk-set facts"):
            from rawlsing_next._pre553_query_eval import _routing_fact_for
            _routing_fact_for(
                respondent, index, target_ref=target, risk_set_ref=risk,
                registry=_registry(source, _qa), used=[], used_auth=[],
            )
