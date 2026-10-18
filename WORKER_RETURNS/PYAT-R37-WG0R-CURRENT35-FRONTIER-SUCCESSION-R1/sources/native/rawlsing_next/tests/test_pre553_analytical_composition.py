import copy
import inspect
import json
from pathlib import Path

import pytest

import rawlsing_next.tests.test_pre553_empirical_query as i03
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    EmpiricalQuerySpec,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_analytical_composition import (
    ConditionValueBindingWitness,
    ConditionValueRelationMismatch,
    EVIDENCE_CONTRACT_ID,
    EVIDENCE_PREIMAGE_SCHEMA,
    SLICE_PROJECTION_SCHEMA_HASH,
    compose_positioned_subject_possibility,
    _build_evidence,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
)

ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R2"
R3 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R3"
R8 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R8"
R2_RELATION = R2 / "02_VALUE_RELATION_ORACLE.json"
R2_AUTHORITIES = R2 / "03_SYNTHETIC_AUTHORITY_FREEZE.json"
R2_SLICE = R2 / "04_SLICE_PROJECTION.json"
R3_AUTHORITY = R3 / "02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"
R8_SPINE = R8 / "04_CURRENT_AT07_IDENTITY_SPINE.json"

OLD = {
    "forward_query": "83727ca59eaf43085324ee7dc7db5ce4ecf4e4bf1f1284692cd3ad3f192df027",
    "reverse_query": "cb2d085675c137848bb40f191ba8992100513eaa904a09cd54064f6ef51d3d8a",
    "forward_witness": "c93e840c06da9ab8de9ca237863d52858fe6765d5bfd7c7efb42b879440663c9",
    "reverse_witness": "e81c4e19144a749877a6f6e7e48a213e869bfe5d04ba81372ca5384b7cf5e700",
}
R6_FORWARD_QUERY_HASH = "8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9"
R6_REVERSE_QUERY_HASH = "2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e"


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _authority_entry(authority_class):
    data = _load(R2_AUTHORITIES)
    return next(x for x in data["authorities"] if x["authority_class"] == authority_class)


def _snapshot(authority_class):
    entry = _authority_entry(authority_class)
    material = dict(entry["canonical_material"])
    material.pop("schema", None)
    material.pop("purpose", None)
    expected = entry["expected_authority_ref"]
    material["authority_content_hash"] = expected["authority_content_hash"]
    return AuthoritySnapshot(**material)


def _query_snapshot():
    entry = _load(R3_AUTHORITY)["repaired_query_authority"]
    material = dict(entry["canonical_material"])
    material.pop("schema", None)
    material.pop("purpose", None)
    material["authority_content_hash"] = entry["expected_authority_ref"]["authority_content_hash"]
    return AuthoritySnapshot(**material)


def _fixture_authority(authority_class):
    ref = _authority_entry(authority_class)["expected_authority_ref"]
    return AuthorityRef(**ref)


def _relation(role, family):
    data = _load(R2_RELATION)
    return next(x for x in data[family] if x["material"]["role"] == role)


def _rows():
    rows = []
    for position, answer, count, prefix in (
        ("P1", "yes", 54, "P1Y"),
        ("P1", "no", 6, "P1N"),
        ("P2", "yes", 8, "P2Y"),
        ("P2", "no", 32, "P2N"),
    ):
        rows.extend(
            {"id": f"{prefix}{n:03d}", "responses": {"POSITION": position, "ANSWER": answer}}
            for n in range(1, count + 1)
        )
    return rows


@pytest.fixture
def at07(monkeypatch):
    source_auth = _snapshot("PRE553_AUTHORITY_SNAPSHOT::SOURCE_SEMANTICS_TOPOLOGY")
    routing_auth = _snapshot("PRE553_AUTHORITY_SNAPSHOT::ROUTING_RISK_SET")
    coord_auth = _snapshot("PRE553_AUTHORITY_SNAPSHOT::COORDINATE_SEMANTICS")
    replay_auth = _snapshot("PRE553_AUTHORITY_SNAPSHOT::REPLAY_PROTOCOL")
    query_auth = _query_snapshot()

    original_auth = i03._auth
    exact_by_kind = {
        "SOURCE_SEMANTICS_TOPOLOGY": source_auth,
        "ROUTING_RISK_SET": routing_auth,
        "COORDINATE_SEMANTICS": coord_auth,
        "REPLAY_PROTOCOL": replay_auth,
    }

    def frozen_auth(tag, kind, *, families):
        if kind in exact_by_kind:
            return exact_by_kind[kind]
        return original_auth(tag, kind, families=families)

    monkeypatch.setattr(i03, "_auth", frozen_auth)
    source = i03._build_source(
        "c1-at07",
        _rows(),
        question_namespace="c1-at07",
        risk_sets={"R_ALL_100": {"POSITION": {r["id"] for r in _rows()}, "ANSWER": {r["id"] for r in _rows()}}},
        risk_namespace="c1-at07",
    )
    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL_100"]

    spine = _load(R8_SPINE)["identity_spine"]
    assert source["universe"].ref.as_dict() == spine["universe_ref"]
    assert source["release_ref"].as_dict() == spine["release_ref"]
    assert query_auth.authority_ref.as_dict() == spine["query_authority_ref"]

    registry = AuthorityRegistry((*source["authorities"], query_auth))
    return source, query_auth, registry


def _producer(source, query_auth, direction):
    if direction == "forward":
        leaf = i03._response_leaf(source, query_auth, "POSITION", "P1")
        predicate = i03._predicate(source, query_auth, leaf, tag="c1-at07-forward-position-p1")
        query = i03._query(
            source, query_auth, predicate, ("ANSWER",),
            risk="R", tag="c1-at07-forward-position-p1-to-answer",
        )
    else:
        leaf = i03._response_leaf(source, query_auth, "ANSWER", "yes")
        predicate = i03._predicate(source, query_auth, leaf, tag="c1-at07-reverse-answer-yes")
        query = i03._query(
            source, query_auth, predicate, ("POSITION",),
            risk="R", tag="c1-at07-reverse-answer-yes-to-position",
        )
    domain = ["no", "yes"] if direction == "forward" else ["P1", "P2"]
    target = "ANSWER" if direction == "forward" else "POSITION"
    component = dict(query.target_arity_and_topology["components"][0])
    component["domain"] = domain
    component["target_domain_replay_ref"] = i03._ref(
        "TARGET_DOMAIN", f"{target}-{'-'.join(domain)}"
    )
    query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        target_refs=query.target_refs,
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [component],
        },
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=query.scope_refs,
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=query.requested_output_grain,
        query_authority_refs=query.query_authority_refs,
    )
    frozen = _load(R8_SPINE)["identity_spine"][direction]
    assert predicate.ref.as_dict() == frozen["producer_predicate_ref"]
    assert predicate.predicate_hash == frozen["producer_predicate_hash"]
    assert query.ref.as_dict() == frozen["producer_query_ref"]
    return predicate, query


def _consumer(source, direction, *, pairing=None):
    if pairing is None:
        pairing = _fixture_authority("FIXTURE_ONLY_CONDITION_VALUE_PAIRING")
    if direction == "forward":
        subject_material = {
            "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "fixture_id": "AT07_BIDIRECTIONAL_100",
            "role": "FORWARD_POSITION_P1",
            "real_subject": False,
        }
        subject = ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:c1:at07:positioned-subject:forward-position-p1",
            semantic_hash(subject_material),
        )
        relation = _relation("POSITION_P1", "subject_condition_preimages")
        binding = ConditionerBinding(
            "position", ExactRef(**relation["ref"]), source["qrefs"]["POSITION"], pairing,
            source["universe"].ref, source["release_ref"], None,
        )
        query = PositionedSubjectPossibilityQuery(
            "c1-at07-forward-position-p1-to-answer", subject, source["qrefs"]["ANSWER"],
            source["universe"].ref, source["release_ref"], (binding,),
            {"kind": "C1_AT07_CONDITIONAL_DISTRIBUTION", "direction": "POSITION_P1_TO_ANSWER", "target_role": "ANSWER"},
        )
        assert query.ref.as_dict() == _load(R8_SPINE)["identity_spine"][direction]["consumer_query_ref"]
    else:
        subject_material = {
            "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "fixture_id": "AT07_BIDIRECTIONAL_100",
            "role": "REVERSE_ANSWER_YES",
            "real_subject": False,
        }
        subject = ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:c1:at07:positioned-subject:reverse-answer-yes",
            semantic_hash(subject_material),
        )
        relation = _relation("ANSWER_YES", "subject_condition_preimages")
        binding = ConditionerBinding(
            "answer", ExactRef(**relation["ref"]), source["qrefs"]["ANSWER"], pairing,
            source["universe"].ref, source["release_ref"], None,
        )
        query = PositionedSubjectPossibilityQuery(
            "c1-at07-reverse-answer-yes-to-position", subject, source["qrefs"]["POSITION"],
            source["universe"].ref, source["release_ref"], (binding,),
            {"kind": "C1_AT07_CONDITIONAL_DISTRIBUTION", "direction": "ANSWER_YES_TO_POSITION", "target_role": "POSITION"},
        )
        assert query.ref.as_dict() == _load(R8_SPINE)["identity_spine"][direction]["consumer_query_ref"]
    return query, binding


def _witness(source, direction, consumer_query, binding, producer_query, predicate):
    if direction == "forward":
        subject = _relation("POSITION_P1", "subject_condition_preimages")
        leaf = _relation("POSITION_EQ_P1", "predicate_leaf_preimages")
        pair = _relation("POSITION_P1__POSITION_EQ_P1", "pairing_ground_truth")
        object_id = "urn:test:c1:at07:condition-value-witness:r6-forward-p1"
    else:
        subject = _relation("ANSWER_YES", "subject_condition_preimages")
        leaf = _relation("ANSWER_EQ_YES", "predicate_leaf_preimages")
        pair = _relation("ANSWER_YES__ANSWER_EQ_YES", "pairing_ground_truth")
        object_id = "urn:test:c1:at07:condition-value-witness:r6-reverse-yes"
    pairing = binding.comparability_authority_ref
    material = {
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_binding_material": canonicalize(binding.material()),
        "consumer_binding_fingerprint": semantic_hash(binding.material()),
        "subject_condition_preimage_ref": subject["ref"],
        "subject_condition_preimage_material": canonicalize(subject["material"]),
        "producer_query_ref": producer_query.ref.as_dict(),
        "producer_predicate_ref": predicate.ref.as_dict(),
        "producer_predicate_hash": predicate.predicate_hash,
        "producer_predicate_leaf_ref": leaf["ref"],
        "producer_predicate_leaf_projection": canonicalize(leaf["material"]),
        "pairing_ground_truth_ref": pair["ref"],
        "pairing_authority_ref": pairing.as_dict(),
        "source_universe_ref": source["universe"].ref.as_dict(),
        "release_ref": source["release_ref"].as_dict(),
        "effective_time_or_interval": canonicalize(binding.effective_time_or_interval),
        "binding_mode": "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE",
    }
    assert set(material) == {
        "consumer_query_ref", "consumer_binding_material", "consumer_binding_fingerprint",
        "subject_condition_preimage_ref", "subject_condition_preimage_material",
        "producer_query_ref", "producer_predicate_ref", "producer_predicate_hash",
        "producer_predicate_leaf_ref", "producer_predicate_leaf_projection",
        "pairing_ground_truth_ref", "pairing_authority_ref", "source_universe_ref",
        "release_ref", "effective_time_or_interval", "binding_mode",
    }
    digest = semantic_hash(material)
    return ConditionValueBindingWitness(
        witness_ref=ExactRef("C1_CONDITION_VALUE_BINDING_WITNESS@2", object_id, digest),
        identity_material=material,
        subject_condition_preimage_ref=ExactRef(**subject["ref"]),
        subject_condition_preimage_material=subject["material"],
        producer_predicate_leaf_ref=ExactRef(**leaf["ref"]),
        producer_predicate_leaf_projection=leaf["material"],
        pairing_ground_truth_ref=ExactRef(**pair["ref"]),
        pairing_ground_truth_material=pair["material"],
        pairing_authority_ref=pairing,
    )


def _model(source):
    return PositionedSubjectPossibilityModelRule(
        _fixture_authority("FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL"),
        _fixture_authority("FIXTURE_ONLY_WALKBACK_POLICY"),
        (source["universe"].ref,), (), (),
    )


def _execute(at07, direction):
    source, query_auth, registry = at07
    predicate, producer_query = _producer(source, query_auth, direction)
    consumer_query, binding = _consumer(source, direction)
    witness = _witness(source, direction, consumer_query, binding, producer_query, predicate)
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=_model(source),
        condition_binding_witness=witness,
    )
    return result, witness, consumer_query, binding, predicate, producer_query


def _query_with_binding(query, binding):
    return PositionedSubjectPossibilityQuery(
        query.query_id,
        query.subject_ref,
        query.target_ref,
        query.source_universe_ref,
        query.release_ref,
        (binding,),
        query.requested_projection,
        purpose=query.purpose,
    )


def _evidence_preimage(evidence):
    return {
        "schema": EVIDENCE_PREIMAGE_SCHEMA,
        "contract_id": EVIDENCE_CONTRACT_ID,
        "source_universe_ref": evidence.source_universe_ref.as_dict(),
        "release_ref": evidence.release_ref.as_dict(),
        "target_ref": evidence.target_ref.as_dict(),
        "retained_conditioner_ids": list(evidence.retained_conditioner_ids),
        "evidence_state": evidence.evidence_state,
        "geometry": canonicalize(evidence.geometry),
        "raw_support": evidence.raw_support,
        "uncertainty_state": evidence.uncertainty_state,
        "provenance_refs": [x.as_dict() for x in evidence.provenance_refs],
        "authority_refs": [x.as_dict() for x in evidence.authority_refs],
    }


def _assert_unrelated_direct_determinants_unchanged(baseline, mutated):
    for name in (
        "producer_query_ref",
        "producer_predicate_ref",
        "producer_fact_ref",
        "source_universe_refs",
        "release_refs",
        "ordered_target_refs",
        "target_arity_and_topology",
        "target_domain_identity",
        "risk_set_ref",
        "risk_set_member_refs",
        "denominator_member_refs",
        "raw_denominator_support",
        "measure_kind",
        "measure_basis_ref",
        "weight_basis_id_or_null",
        "consumer_model_rule_hash",
    ):
        assert getattr(mutated, name) == getattr(baseline, name), name


def test_r8_queries_supersede_documentary_r6_hashes(at07):
    source, _, _ = at07
    forward, _ = _consumer(source, "forward")
    reverse, _ = _consumer(source, "reverse")
    assert forward.ref.content_hash not in {R6_FORWARD_QUERY_HASH, OLD["forward_query"]}
    assert reverse.ref.content_hash not in {R6_REVERSE_QUERY_HASH, OLD["reverse_query"]}


@pytest.mark.parametrize(("direction", "denominator", "numerators"), (
    ("forward", 60, {"yes": 54, "no": 6}),
    ("reverse", 62, {"P1": 54, "P2": 8}),
))
def test_at07_r6_executes_public_producer_adapter_consumer(at07, direction, denominator, numerators):
    result, witness, consumer_query, _, _, _ = _execute(at07, direction)
    assert witness.witness_ref.content_hash not in OLD.values()
    assert result.producer_result.query_ref == result.producer_query_ref
    assert result.raw_denominator_support == denominator
    assert result.possibility_slice_evidence_or_null.raw_support == denominator
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert result.consumer_result_or_null.exact_evidence_ref == result.possibility_slice_evidence_or_null.evidence_ref
    cells = {x["cell"]: x["raw_numerator_support"] for x in result.complete_cell_geometry}
    assert cells == numerators
    expected = _load(R8_SPINE)["identity_spine"][direction]
    assert witness.witness_ref.content_hash == expected["witness_ref"]["content_hash"]
    assert consumer_query.ref.content_hash == expected["consumer_query_ref"]["content_hash"]
    assert result.possibility_slice_evidence_or_null.evidence_ref.as_dict() == expected["evidence_ref"]


def test_r6_witness_mutation_reidentifies_and_stale_ref_fails_closed(at07):
    result, witness, consumer_query, binding, predicate, producer_query = _execute(at07, "forward")
    mutated = dict(witness.identity_material)
    mutated["binding_mode"] = "MUTATED_FIXTURE_ONLY"
    assert semantic_hash(mutated) != witness.witness_ref.content_hash
    stale = ConditionValueBindingWitness(
        witness_ref=witness.witness_ref,
        identity_material=mutated,
        subject_condition_preimage_ref=witness.subject_condition_preimage_ref,
        subject_condition_preimage_material=witness.subject_condition_preimage_material,
        producer_predicate_leaf_ref=witness.producer_predicate_leaf_ref,
        producer_predicate_leaf_projection=witness.producer_predicate_leaf_projection,
        pairing_ground_truth_ref=witness.pairing_ground_truth_ref,
        pairing_ground_truth_material=witness.pairing_ground_truth_material,
        pairing_authority_ref=witness.pairing_authority_ref,
    )
    source, _, registry = at07
    with pytest.raises(ConditionValueRelationMismatch, match="preimage hash mismatch"):
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query, predicate=predicate,
            authority_registry=registry, release_refs=(source["release_ref"],),
            consumer_query=consumer_query, model_rule=_model(source),
            condition_binding_witness=stale,
        )


def test_r7_closed_16_key_witness_rejects_matching_hash_with_extra_field(at07):
    source, _, registry = at07
    _, witness, consumer_query, _, predicate, producer_query = _execute(at07, "forward")
    mutated = dict(witness.identity_material)
    mutated["extra_fixture_identity_key"] = "R7-CLOSED-MAP-COUNTEREXAMPLE"
    hostile = ConditionValueBindingWitness(
        witness_ref=ExactRef(
            witness.witness_ref.kind,
            witness.witness_ref.object_id,
            semantic_hash(mutated),
        ),
        identity_material=mutated,
        subject_condition_preimage_ref=witness.subject_condition_preimage_ref,
        subject_condition_preimage_material=witness.subject_condition_preimage_material,
        producer_predicate_leaf_ref=witness.producer_predicate_leaf_ref,
        producer_predicate_leaf_projection=witness.producer_predicate_leaf_projection,
        pairing_ground_truth_ref=witness.pairing_ground_truth_ref,
        pairing_ground_truth_material=witness.pairing_ground_truth_material,
        pairing_authority_ref=witness.pairing_authority_ref,
    )
    hostile.verify_identity()
    assert len(hostile.identity_material) == 17
    with pytest.raises(
        ConditionValueRelationMismatch,
        match="witness identity field set mismatch",
    ):
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query, predicate=predicate,
            authority_registry=registry, release_refs=(source["release_ref"],),
            consumer_query=consumer_query, model_rule=_model(source),
            condition_binding_witness=hostile,
        )


def test_at19_valid_relation_determinant_reidentifies_composed_result(at07):
    source, _, registry = at07
    baseline, baseline_witness, consumer_query, binding, predicate, producer_query = _execute(
        at07, "forward"
    )
    mutated_binding = ConditionerBinding(
        binding.binding_id,
        binding.subject_fact_ref,
        binding.empirical_coordinate_ref,
        binding.comparability_authority_ref,
        binding.source_universe_ref,
        binding.release_ref,
        "AT19_FIXTURE_ONLY_TIME_MUTATION",
    )
    mutated_query = _query_with_binding(consumer_query, mutated_binding)
    mutated_witness = _witness(
        source, "forward", mutated_query, mutated_binding, producer_query, predicate
    )
    assert mutated_witness.witness_ref != baseline_witness.witness_ref
    mutated_witness.verify_identity()
    mutated = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=registry, release_refs=(source["release_ref"],),
        consumer_query=mutated_query, model_rule=_model(source),
        condition_binding_witness=mutated_witness,
    )
    assert mutated.composed_result_identity_hash != baseline.composed_result_identity_hash
    assert mutated.consumer_query_ref != baseline.consumer_query_ref
    assert (
        mutated.condition_binding_witness_ref_or_hash
        != baseline.condition_binding_witness_ref_or_hash
    )
    assert mutated.raw_denominator_support == baseline.raw_denominator_support == 60
    assert mutated.complete_cell_geometry == baseline.complete_cell_geometry
    _assert_unrelated_direct_determinants_unchanged(baseline, mutated)


def test_r7_denominator_member_identity_hostile_preserves_visible_54_over_60(at07):
    result, _, _, _, _, _ = _execute(at07, "forward")
    evidence = result.possibility_slice_evidence_or_null
    baseline = _evidence_preimage(evidence)
    assert semantic_hash(baseline) == evidence.evidence_ref.content_hash
    assert baseline["raw_support"] == 60
    assert {x["cell"]: x["raw_numerator_support"] for x in baseline["geometry"]["cells"]} == {
        "yes": 54,
        "no": 6,
    }

    mutated = copy.deepcopy(baseline)
    hostile_hash = semantic_hash({"fixture_only": "H3_DENOMINATOR_MEMBER_MUTATION"})
    hostile_member = ExactRef(
        "C11Internal:RespondentIdentity",
        f"urn:test:c1:hostile:denominator-member:sha256:{hostile_hash}",
        hostile_hash,
    )
    mutated["geometry"]["denominator"]["denominator_member_refs"][0] = hostile_member.as_dict()

    assert mutated["raw_support"] == baseline["raw_support"] == 60
    assert mutated["geometry"]["cells"] == baseline["geometry"]["cells"]
    assert semantic_hash(mutated) != evidence.evidence_ref.content_hash


def test_r7_geometry_cell_identity_hostile_reidentifies_evidence(at07):
    result, _, _, _, _, _ = _execute(at07, "forward")
    evidence = result.possibility_slice_evidence_or_null
    baseline = _evidence_preimage(evidence)
    assert semantic_hash(baseline) == evidence.evidence_ref.content_hash

    mutated = copy.deepcopy(baseline)
    no_cell = next(x for x in mutated["geometry"]["cells"] if x["cell"] == "no")
    assert no_cell["raw_numerator_support"] == 6
    no_cell["raw_numerator_support"] = 5
    no_cell["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 12]}

    assert mutated["geometry"]["denominator"]["raw_denominator_support"] == 60
    assert semantic_hash(mutated) != evidence.evidence_ref.content_hash


def test_r7_fixture_pairing_authority_reidentifies_witness_evidence_and_composed_result(at07):
    source, _, registry = at07
    baseline, baseline_witness, consumer_query, binding, predicate, producer_query = _execute(
        at07, "forward"
    )
    hostile_authority = AuthorityRef(
        authority_id="C1-AT07-COMPARABILITY-H5-FIXTURE",
        authority_version="1.0.0",
        authority_content_hash=semantic_hash(
            {
                "fixture_only": True,
                "hostile_court": "H5_RELATION_PAIRING_AUTHORITY",
                "real_source_effect": False,
            }
        ),
    )
    mutated_binding = ConditionerBinding(
        binding.binding_id,
        binding.subject_fact_ref,
        binding.empirical_coordinate_ref,
        hostile_authority,
        binding.source_universe_ref,
        binding.release_ref,
        binding.effective_time_or_interval,
    )
    mutated_query = _query_with_binding(consumer_query, mutated_binding)
    mutated_witness = _witness(
        source, "forward", mutated_query, mutated_binding, producer_query, predicate
    )
    mutated_witness.verify_identity()
    mutated = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=registry, release_refs=(source["release_ref"],),
        consumer_query=mutated_query, model_rule=_model(source),
        condition_binding_witness=mutated_witness,
    )

    assert mutated_witness.witness_ref != baseline_witness.witness_ref
    assert (
        mutated.possibility_slice_evidence_or_null.evidence_ref
        != baseline.possibility_slice_evidence_or_null.evidence_ref
    )
    assert mutated.composed_result_identity_hash != baseline.composed_result_identity_hash
    assert hostile_authority in mutated.possibility_slice_evidence_or_null.authority_refs
    assert hostile_authority in mutated.authority_refs
    _assert_unrelated_direct_determinants_unchanged(baseline, mutated)


def test_relation_mismatch_fails_before_evidence_and_consumer(monkeypatch, at07):
    source, query_auth, registry = at07
    predicate, producer_query = _producer(source, query_auth, "forward")
    consumer_query, binding = _consumer(source, "forward")
    witness = _witness(source, "forward", consumer_query, binding, producer_query, predicate)
    hostile_leaf = _relation("POSITION_EQ_P2", "predicate_leaf_preimages")
    hostile = ConditionValueBindingWitness(
        witness_ref=witness.witness_ref,
        identity_material=witness.identity_material,
        subject_condition_preimage_ref=witness.subject_condition_preimage_ref,
        subject_condition_preimage_material=witness.subject_condition_preimage_material,
        producer_predicate_leaf_ref=ExactRef(**hostile_leaf["ref"]),
        producer_predicate_leaf_projection=hostile_leaf["material"],
        pairing_ground_truth_ref=witness.pairing_ground_truth_ref,
        pairing_ground_truth_material=witness.pairing_ground_truth_material,
        pairing_authority_ref=witness.pairing_authority_ref,
    )
    import rawlsing_next.pre553_analytical_composition as c1
    built = called = False
    def forbidden_build(*args, **kwargs):
        nonlocal built
        built = True
        raise AssertionError("evidence construction reached")
    def forbidden_consumer(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("consumer reached")
    monkeypatch.setattr(c1, "_build_evidence", forbidden_build)
    monkeypatch.setattr(c1, "evaluate_positioned_subject_possibility", forbidden_consumer)
    with pytest.raises(ConditionValueRelationMismatch):
        compose_positioned_subject_possibility(
            repository=source["repo"], empirical_query=producer_query, predicate=predicate,
            authority_registry=registry, release_refs=(source["release_ref"],),
            consumer_query=consumer_query, model_rule=_model(source),
            condition_binding_witness=hostile,
        )
    assert not built and not called


def test_composer_has_no_preconstructed_possibility_slice_input():
    sig = inspect.signature(compose_positioned_subject_possibility)
    assert "evidence" not in sig.parameters
    assert "possibility_slice_evidence" not in sig.parameters
    # C1-01 core parameters + C1-02 optional extensions
    assert set(sig.parameters) == {
        "repository", "empirical_query", "predicate", "authority_registry", "release_refs",
        "consumer_query", "model_rule", "condition_binding_witness",
        "discovery_result", "discovery_receipt_ref", "recursive_handoff",
    }


def test_relation_guard_is_before_evidence_construction_and_consumer_invocation():
    source = inspect.getsource(compose_positioned_subject_possibility)
    assert source.index("_verify_witness(") < source.index("_build_evidence(") < source.index("evaluate_positioned_subject_possibility(")


def test_supported_evidence_uses_raw_denominator_not_target_numerator():
    source = inspect.getsource(_build_evidence)
    assert "raw_support=fact.raw_denominator_support" in source
    assert "raw_support=fact.raw_numerator_support" not in source
    assert "float(" not in source
    assert _load(R2_SLICE)["projection_schema_hash"] == SLICE_PROJECTION_SCHEMA_HASH
