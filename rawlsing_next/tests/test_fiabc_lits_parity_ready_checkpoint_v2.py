from __future__ import annotations

import copy
import hashlib
from types import SimpleNamespace

import pytest

import rawlsing_next.fiabc_final_oracle_freeze_producers as producer
from rawlsing_next.pre553_c11_integrity import ReplayManifest
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    canonicalize,
    semantic_hash,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    digest = _h(label)
    return ExactRef(kind, f"urn:test:{label}", digest)


def _authority() -> AuthoritySnapshot:
    authority_material_hash = _h("authority-material")
    replay = _ref("ReplayRoot@1.0.0", "authority-replay")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=replay,
        authority_id="TEST-CANONICAL-CLOSURE",
        authority_version="1.0.0",
        authority_content_hash=authority_material_hash,
        authority_kind="TEST_EXACT_AUTHORITY",
        decision_state="ALLOW",
        governed_operations=("TEST",),
        governed_object_families=(
            "EmpiricalUniverse@1.0.0",
            "EmpiricalPredicate@1.0.0",
            "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
            "DiscoveryAuthority@1.0.0",
            "DiscoveryResultReceipt@1.0.0",
        ),
        scope_envelope={"scope": "TEST"},
        effective_time_or_interval={"kind": "TEST"},
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h("authority-semantics"),
        replay_protocol_ref=_ref("ReplayProtocol@1.0.0", "authority-protocol"),
    )


def _fixture():
    auth = _authority()
    source_artifact = _ref("SourceArtifact@1.0.0", "source-artifact")
    release_ref = _ref("C11LogicalRelease", "release")
    replay = ReplayManifest(
        frontier_version="TEST-FRONTIER",
        authority_snapshot_set_hash=_h("authority-set"),
        source_substrate_content_refs=(source_artifact,),
        semantic_projection_id="TEST-PROJECTION",
        semantic_projection_hash=_h("semantic-projection"),
        deterministic_tie_order_rules_ref=_ref("TieOrder@1.0.0", "tie-order"),
        replay_protocol_version="1.0.0",
        replay_protocol_authority_ref=auth.authority_ref,
        closure_refs=(),
    )
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("ReplayRoot@1.0.0", "universe-replay"),
        raw_source_identity={"sha256": _h("source")},
        source_family="TEST",
        study_product_release="TEST-RELEASE",
        instrument_release="TEST-INSTRUMENT",
        country_geography={"country": "TEST"},
        sampling_geography={"scope": "TEST"},
        raw_wave="I",
        canonical_wave_if_governed="I",
        field_or_reference_time={"year": 2006},
        target_population_and_sample_frame={"population": "TEST"},
        sampling_design_regime={"kind": "TEST"},
        respondent_namespace="urn:test:respondent",
        source_artifact_import_lineage={"source_artifact_ref": source_artifact.as_dict()},
        harmonization_authority_ref=auth.authority_ref,
        source_relation_refs=(),
    )
    target = _ref("QuestionValue@1.0.0", "target")
    risk = _ref("RiskSet@1.0.0", "risk")
    scope = _ref("Scope@1.0.0", "scope")
    measure = _ref("MeasureBasis@1.0.0", "measure")
    state_semantics = _ref("ResponseStateSemantics@1.0.0", "state-semantics")
    ast = {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_ref": target.as_dict(),
        "value": 1,
    }
    predicate = EmpiricalPredicate(
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("ReplayRoot@1.0.0", "predicate-replay"),
        predicate_ast=ast,
        predicate_hash=semantic_hash(ast),
        grammar_authority_ref=auth.authority_ref,
        coordinate_question_value_refs=(target,),
        risk_set_refs=(risk,),
        scope_refs=(scope,),
        same_respondent_binding_semantics="EXACT_SAME_RESPONDENT",
        operator_semantics_refs=(_ref("Operator@1.0.0", "operator"),),
    )
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(auth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("ReplayRoot@1.0.0", "query-replay"),
        target_refs=(target,),
        target_arity_and_topology={
            "arity": 1,
            "joint_order_semantics": "SCALAR",
            "target_domain_identity": _h("target-domain"),
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=risk,
        empirical_universe_refs=(universe.ref,),
        scope_refs=(scope,),
        measure_basis_ref=measure,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": "TEST",
            "response_state_semantics_ref": state_semantics.as_dict(),
        },
        query_authority_refs=(auth.authority_ref,),
    )
    grammar = {"schema": "TEST_GRAMMAR", "rules": []}
    discovery = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(auth.authority_ref,),
        dependency_refs=(query.ref, predicate.ref),
        producer_replay_locator_or_reference_root=_ref("ReplayRoot@1.0.0", "discovery-replay"),
        candidate_grammar_ref=ExactRef(
            "CandidateGrammar@1.0.0", "urn:test:grammar", semantic_hash(grammar)
        ),
        candidate_universe_definition=grammar,
        source_universe_scope=(universe.ref,),
        risk_set_scope=(risk,),
        topology_scope={"arity": 1},
        measure_scope={"kind": "RAW"},
        support_rules={"minimum_raw_denominator": 1},
        validation_rules={"kinds": ["TARGET_CELL_SUPPORTED"]},
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={"kind": "NONE_EXACT_EVALUATE_ALL"},
        algorithm_identity_if_semantically_required=None,
        tie_order_rules={"kind": "EXACT"},
        rng_policy_if_any="NONE",
        mode="EXACT_BOUNDED",
    )

    member_refs = (
        _ref("RespondentIdentity@1.0.0", "member-1"),
        _ref("RespondentIdentity@1.0.0", "member-2"),
    )
    facts = []
    for i in range(60):
        replay_ref = _ref("PRE553_I03_QUERY_REPLAY", f"fact-replay-{i:02d}")
        fact = EmpiricalFact(
            typed_state="SUPPORTED",
            authority_snapshot_refs=(auth.authority_ref,),
            dependency_refs=(query.ref, predicate.ref, replay_ref, release_ref, universe.ref),
            producer_replay_locator_or_reference_root=replay_ref,
            empirical_query_spec_ref=query.ref,
            empirical_universe_refs=(universe.ref,),
            target_topology={
                "arity": 1,
                "joint_order_semantics": "SCALAR",
                "target_domain_identity": _h("target-domain"),
                "complete_cell_semantic_projection": [
                    {
                        "cell": i,
                        "cell_state": "OBSERVED_POSITIVE",
                        "raw_numerator_support": i + 1,
                        "weighted_numerator_support_if_authorized": None,
                    }
                ],
            },
            condition_predicate_ref=predicate.ref,
            risk_set_ref=risk,
            raw_numerator_support=i + 1,
            raw_denominator_support=100 + i,
            weighted_numerator_support_if_authorized=None,
            weighted_denominator_support_if_authorized=None,
            measure_basis_ref=measure,
            response_state_semantics_ref=state_semantics,
            uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
            source_empirical_provenance_refs=(release_ref, universe.ref),
            replay_ref=replay_ref,
            query_execution_contract_id="PRE553_I03_EXACT_QUERY@TEST",
            execution_detail=f"fact-{i:02d}",
            source_scope_mode="SINGLE_UNIVERSE",
            measure_kind="RAW",
            risk_set_type="TEST",
            risk_set_member_refs=member_refs,
            denominator_member_refs=member_refs,
            target_domain_identity=_h("target-domain"),
            raw_resolved_target_support=i + 1,
        )
        facts.append(fact)

    receipts = []
    candidate_rows = []
    cursor = 0
    for i in range(50):
        fact_count = 2 if i < 10 else 1
        owned = facts[cursor:cursor + fact_count]
        cursor += fact_count
        role_count = 2 if i < 27 else 1
        roles = [
            {
                "role": f"ROLE_{j}",
                "predicate_ref": predicate.ref.as_dict(),
                "query_ref": query.ref.as_dict(),
            }
            for j in range(role_count)
        ]
        candidate_hash = _h(f"candidate-{i:02d}")
        candidate_identity = {
            "candidate_id": f"urn:test:candidate:{i:02d}",
            "candidate_hash": candidate_hash,
            "family": "TEST",
            "rule_id": f"TEST_RULE_{i:02d}",
            "validation": {"kind": "TARGET_CELL_SUPPORTED", "ordinal": i},
            "query_roles": roles,
        }
        coverage = "EVALUATED_VALID_EMPTY" if i == 49 else "EVALUATED_SUPPORTED"
        typed = "VALID_EMPTY" if i == 49 else "DISCOVERED_RESULT_SUPPORTED"
        receipt_replay = _ref("PRE553_I05_DISCOVERY_REPLAY", f"candidate-replay-{i:02d}")
        receipt = DiscoveryResultReceipt(
            typed_state=typed,
            authority_snapshot_refs=(auth.authority_ref,),
            dependency_refs=(discovery.ref, predicate.ref, *[fact.ref for fact in owned]),
            producer_replay_locator_or_reference_root=receipt_replay,
            discovery_authority_ref=discovery.ref,
            candidate_identity=candidate_identity,
            winning_predicate_ref=predicate.ref,
            empirical_fact_refs=tuple(fact.ref for fact in owned),
            validation_fact_refs=tuple(fact.ref for fact in owned),
            coverage_state=coverage,
            evaluated_frontier_ref=_ref("PRE553_I05_EVALUATED_FRONTIER", "frontier"),
            branch_or_parent_ancestry_refs=(),
            support_uncertainty_state={
                "fact_states": [fact.typed_state for fact in owned],
                "query_role_fact_refs": {
                    role["role"]: [owned[0].ref.as_dict()] for role in roles
                },
            },
            replay_ref=receipt_replay,
        )
        receipts.append(receipt)
        candidate_rows.append({
            "candidate_hash": candidate_hash,
            "typed_state": typed,
            "semantic_fields": {
                "candidate_identity": canonicalize(receipt.candidate_identity),
                "constituent_fact_manifest": [
                    {"ref": fact.ref.as_dict(), "typed_state": fact.typed_state}
                    for fact in sorted(owned, key=lambda item: item.ref.key)
                ],
                "coverage_state": coverage,
                "support_uncertainty_state": canonicalize(receipt.support_uncertainty_state),
                "replay_ref": canonicalize(receipt.replay_ref),
            },
        })

    release = SimpleNamespace(
        release_ref=release_ref,
        source_artifact_ref=source_artifact,
        source_release_manifest_hash=_h("source-release-manifest"),
        semantic_release_hash=release_ref.content_hash,
        replay_manifest=replay,
        public_objects=(auth, universe),
        m01_m18_coverage={},
    )
    catalog = SimpleNamespace(
        authorities=(auth,),
        predicates=(predicate,),
        queries=(query,),
        discovery_authorities=(discovery,),
    )
    result = SimpleNamespace(
        empirical_facts=tuple(facts),
        receipts=tuple(receipts),
    )
    closure = producer._build_lits_canonical_empirical_closure(
        catalog=catalog,
        result=result,
        release=release,
    )
    compact_facts = [
        {"ref": fact.ref.as_dict(), "typed_state": fact.typed_state}
        for fact in sorted(facts, key=lambda item: item.ref.key)
    ]
    projection = {
        "release_refs": [release_ref.as_dict()],
        "c11_release_identity": release_ref.content_hash,
        "c11_replay_identity": replay.ref.content_hash,
    }
    return closure, candidate_rows, compact_facts, projection, query, predicate


def _reseal(closure):
    body = {key: value for key, value in closure.items() if key != "closure_identity"}
    closure["closure_identity"] = semantic_hash(canonicalize(body))


def _doc(closure, schema_id):
    return next(
        doc for doc in closure["public_object_preimages"]
        if doc["schema_id"] == schema_id
    )


def test_complete_current_object_closure_round_trips_full_fact_query_and_predicate_preimages():
    closure, rows, compact, projection, query, predicate = _fixture()
    inventory = producer._validate_lits_canonical_empirical_closure(
        closure,
        candidate_rows=rows,
        compact_facts=compact,
        projection_and_release_refs=projection,
    )
    assert inventory["EmpiricalFact@1.0.0"] == 60
    assert inventory["DiscoveryResultReceipt@1.0.0"] == 50
    assert inventory["EmpiricalQuerySpec@1.0.0"] == 1
    assert inventory["EmpiricalPredicate@1.0.0"] == 1
    fact_doc = _doc(closure, "EmpiricalFact")
    assert fact_doc["semantic_fields"]["target_topology"]["complete_cell_semantic_projection"]
    assert fact_doc["semantic_fields"]["risk_set_member_refs"]
    assert fact_doc["semantic_fields"]["denominator_member_refs"]
    assert fact_doc["semantic_fields"]["raw_resolved_target_support"] > 0
    assert _doc(closure, "EmpiricalQuerySpec")["content_hash"] == query.content_hash
    assert _doc(closure, "EmpiricalPredicate")["content_hash"] == predicate.content_hash


@pytest.mark.parametrize(
    "mutator",
    [
        lambda doc: doc["semantic_fields"].__setitem__("raw_numerator_support", 99),
        lambda doc: doc["semantic_fields"]["target_topology"][
            "complete_cell_semantic_projection"
        ][0].__setitem__("raw_numerator_support", 99),
        lambda doc: doc["semantic_fields"].__setitem__(
            "risk_set_ref", _ref("RiskSet@1.0.0", "wrong-risk").as_dict()
        ),
    ],
)
def test_fact_hash_tampering_complete_cell_mutation_and_risk_drift_fail_closed(mutator):
    closure, rows, compact, projection, _query, _predicate = _fixture()
    mutated = copy.deepcopy(closure)
    mutator(_doc(mutated, "EmpiricalFact"))
    _reseal(mutated)
    with pytest.raises(producer.FinalOracleProducerError, match="re-materialization"):
        producer._validate_lits_canonical_empirical_closure(
            mutated,
            candidate_rows=rows,
            compact_facts=compact,
            projection_and_release_refs=projection,
        )


def test_query_preimage_tampering_fails_exact_round_trip():
    closure, rows, compact, projection, _query, _predicate = _fixture()
    mutated = copy.deepcopy(closure)
    _doc(mutated, "EmpiricalQuerySpec")["semantic_fields"]["target_refs"][0] = (
        _ref("QuestionValue@1.0.0", "wrong-target").as_dict()
    )
    _reseal(mutated)
    with pytest.raises(producer.FinalOracleProducerError, match="re-materialization"):
        producer._validate_lits_canonical_empirical_closure(
            mutated,
            candidate_rows=rows,
            compact_facts=compact,
            projection_and_release_refs=projection,
        )


def test_predicate_query_substitution_in_frontier_is_detected():
    closure, rows, compact, projection, _query, predicate = _fixture()
    mutated_rows = copy.deepcopy(rows)
    mutated_rows[0]["semantic_fields"]["candidate_identity"]["query_roles"][0][
        "query_ref"
    ] = predicate.ref.as_dict()
    with pytest.raises(
        producer.FinalOracleProducerError,
        match="compact frontier identity|predicate/query preimage substitution",
    ):
        producer._validate_lits_canonical_empirical_closure(
            closure,
            candidate_rows=mutated_rows,
            compact_facts=compact,
            projection_and_release_refs=projection,
        )


def test_release_drift_and_50_77_frontier_drift_fail_closed():
    closure, rows, compact, projection, _query, _predicate = _fixture()
    bad_projection = copy.deepcopy(projection)
    bad_projection["release_refs"][0] = _ref("C11LogicalRelease", "wrong-release").as_dict()
    with pytest.raises(producer.FinalOracleProducerError, match="release/replay identity drift"):
        producer._validate_lits_canonical_empirical_closure(
            closure,
            candidate_rows=rows,
            compact_facts=compact,
            projection_and_release_refs=bad_projection,
        )

    missing_role = copy.deepcopy(rows)
    missing_role[0]["semantic_fields"]["candidate_identity"]["query_roles"].pop()
    with pytest.raises(
        producer.FinalOracleProducerError,
        match="compact frontier identity|50/77 frontier",
    ):
        producer._validate_lits_canonical_empirical_closure(
            closure,
            candidate_rows=missing_role,
            compact_facts=compact,
            projection_and_release_refs=projection,
        )


def test_candidate_neutral_closure_contains_no_structural_admission_objects():
    closure, rows, compact, projection, _query, _predicate = _fixture()
    producer._validate_lits_canonical_empirical_closure(
        closure,
        candidate_rows=rows,
        compact_facts=compact,
        projection_and_release_refs=projection,
    )
    assert closure["structural_admission_object_count"] == 0
    assert "StructuralEmpiricalAdmission@1.0.0" not in closure["inventory"]


@pytest.mark.parametrize(
    "schema",
    [
        producer.LITS_LEGACY_MATERIALIZATION_CHECKPOINT_SCHEMA,
        producer.LITS_PARTIAL_MATERIALIZATION_CHECKPOINT_SCHEMA,
    ],
)
def test_v1_v2_checkpoints_fail_closed_for_missing_complete_current_object_preimages(schema):
    with pytest.raises(
        producer.FinalOracleProducerError,
        match="lacks complete canonical current empirical object preimages",
    ):
        producer._validate_lits_materialization_checkpoint_body({"schema": schema})


def test_zero_source_resume_starts_no_source_decoder_or_candidate_process(tmp_path, monkeypatch):
    execution = {"execution_identity": _h("execution")}
    material = {
        "astra_shaped_empirical_summary": {},
        "source_identity": {
            "source": "LITS_I",
            "sha256": producer.LITS_SOURCE_SHA256,
            "rows": producer.LITS_ROWS,
            "variables": producer.LITS_VARIABLES,
        },
        "court_constitution_refs": {},
        "semantic_authority_closure": [],
        "projection_and_release_refs": {},
        "frontier_manifest": {},
        "comparison_fact_manifest": [],
        "expected_learned_product": {},
        "replay_manifest": {"i05_replay_ref": {"content_hash": _h("replay")}},
        "exact_ref_manifest": [],
        "constituent_i03_fact_manifest": [],
        "constituent_i03_closure_identity": _h("closure"),
    }
    audit = {
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }

    def forbidden_source(**_kwargs):
        raise AssertionError("zero-source resume must not execute source-backed materialization")

    monkeypatch.setattr(producer, "_neutral_lits_material", forbidden_source)
    monkeypatch.setattr(
        producer,
        "_load_lits_materialization_checkpoint",
        lambda _path: (
            material,
            audit,
            execution,
            {"candidate_processes_started": 0},
            _h("checkpoint"),
            _h("checkpoint-document"),
        ),
    )
    monkeypatch.setattr(producer, "_git_json", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(producer, "_verified_astra_input_manifest", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(producer, "normalize_accepted_astra_summary", lambda **_kwargs: {})
    monkeypatch.setattr(
        producer,
        "assert_lits_astra_substantive_parity",
        lambda **_kwargs: {
            "parity_receipt_identity": _h("parity"),
            "expected_empirical_summary_identity": _h("summary"),
            "observed_empirical_summary_identity": _h("summary"),
        },
    )
    monkeypatch.setattr(producer, "build_lits_i_oracle", lambda **_kwargs: {"fake": True})
    monkeypatch.setattr(producer, "verify_frozen_oracle", lambda _doc: _h("oracle"))

    checkpoint = tmp_path / "checkpoint-v3.json"
    checkpoint.write_text("{}\n", encoding="utf-8")
    receipt = producer.produce_lits_local_oracle(
        repo_root=tmp_path,
        work_root=tmp_path / "work",
        output_path=tmp_path / "oracle.json",
        resume_checkpoint=checkpoint,
    )
    assert receipt["source_access"] == {
        "mode": "RESUME_VERIFIED_PARITY_READY_I05_CHECKPOINT",
        "source_hash_passes": 0,
        "decoder_calls": 0,
    }
    assert receipt["candidate_processes_started"] == 0
    assert receipt["candidate_outputs_seen"] == 0
    assert receipt["candidate_owned_roots_consulted"] == []
    assert receipt["candidate_owned_state_reused"] is False
