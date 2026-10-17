import copy
import hashlib

import pytest

import rawlsing_next.pre553_independent_parity_oracle as oracle_mod
from rawlsing_next.pre553_independent_parity_oracle import (
    FreezeContext,
    LITS_C11_RELEASE_IDENTITY,
    LITS_C11_REPLAY_IDENTITY,
    LITS_FRONTIER_SEAL,
    LITS_LEARNED_PRODUCT_IDENTITY,
    LITS_PROJECTION_IDENTITY,
    LITS_SEMANTIC_REPLAY_IDENTITY,
    LITS_SOURCE_SHA256,
    NEGATIVE_STATE_LAW,
    OracleIndependenceError,
    OracleMismatchError,
    ParityOracleError,
    WVS7_DISCOVERY_AUTHORITY,
    WVS7_EMPIRICAL_UNIVERSE,
    WVS7_FAMILY_COUNTS,
    WVS7_LOCK2_IDENTITY,
    WVS7_LOCK2_REPLAY_IDENTITY,
    WVS7_MEASURE_BASIS,
    WVS7_ORDERED_CANDIDATE_HASHES,
    WVS7_RISK_SET,
    WVS7_SOURCE_SHA256,
    WVS_MATERIALIZER_CONTRACT,
    build_lits_i_oracle,
    freeze_wvs7_oracle_from_common_material,
    materialize_wvs7_oracle,
    validate_candidate_observation,
    validate_three_way_parity,
    verify_frozen_oracle,
)


def _h(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _lits_inputs(*, freeze=None, dependency_owner="ACCEPTED_AUTHORITY"):
    candidate_hashes = [_h(f"lits-candidate-{i:02d}") for i in range(50)]
    facts = [
        {
            "candidate_hash": candidate_hash,
            "typed_state": "EVALUATED_VALID_EMPTY" if i == 49 else "EVALUATED_SUPPORTED",
            "semantic_fields": {"support": i, "denominator": 100 + i},
        }
        for i, candidate_hash in enumerate(candidate_hashes)
    ]
    return {
        "prior_product": {
            "schema": "ASTRA_D04_R2_TYPED_LEARNED_EMPIRICAL_PRODUCT@1.0.0",
            "full_execution_product_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
            "semantic_replay_hash": LITS_SEMANTIC_REPLAY_IDENTITY,
            "terminal_counts": {
                "EVALUATED_SUPPORTED": 49,
                "EVALUATED_VALID_EMPTY": 1,
            },
            "frontier": {
                "candidate_count": 50,
                "query_role_count": 77,
                "preexecution_seal": LITS_FRONTIER_SEAL,
            },
        },
        "prior_replay_receipt": {
            "source": {"sha256": LITS_SOURCE_SHA256},
            "execution": {
                "byte_identical": True,
                "run_1_output_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
                "run_2_output_sha256": LITS_LEARNED_PRODUCT_IDENTITY,
            },
            "preoutcome": {
                "candidate_count": 50,
                "query_role_count": 77,
                "frontier_seal": LITS_FRONTIER_SEAL,
            },
        },
        "source_identity": {
            "source": "LITS_I",
            "sha256": LITS_SOURCE_SHA256,
            "rows": 29002,
            "variables": 1198,
        },
        "court_constitution_refs": {
            "lock1_ref": {"kind": "COURT_CONSTITUTION", "content_hash": _h("lock1")},
        },
        "semantic_authority_closure": [
            {
                "kind": "AuthoritySnapshot@1.0.0",
                "object_id": "urn:test:lits:authority",
                "content_hash": _h("lits-authority"),
            }
        ],
        "projection_and_release_refs": {
            "projection_identity": LITS_PROJECTION_IDENTITY,
            "c11_release_identity": LITS_C11_RELEASE_IDENTITY,
            "c11_replay_identity": LITS_C11_REPLAY_IDENTITY,
        },
        "frontier_manifest": {
            "candidate_count": 50,
            "query_role_count": 77,
            "frontier_seal": LITS_FRONTIER_SEAL,
            "ordered_candidate_hashes": candidate_hashes,
        },
        "comparison_fact_manifest": facts,
        "expected_learned_product": {
            "product_identity": LITS_LEARNED_PRODUCT_IDENTITY,
            "semantic_identity": LITS_SEMANTIC_REPLAY_IDENTITY,
            "replay_identity": _h("lits-current-replay"),
            "exact_output_identity": _h("lits-current-output"),
            "coverage": {
                "candidate_count": 50,
                "query_role_count": 77,
                "typed_terminal_counts": {
                    "EVALUATED_SUPPORTED": 49,
                    "EVALUATED_VALID_EMPTY": 1,
                },
            },
        },
        "replay_manifest": {
            "semantic_replay_identity": LITS_SEMANTIC_REPLAY_IDENTITY,
            "dependency_root": _h("lits-dependency-root"),
        },
        "exact_ref_manifest": [
            {
                "kind": "EmpiricalQuerySpec@1.0.0",
                "object_id": "urn:test:lits:query",
                "content_hash": _h("lits-query"),
            },
            {
                "kind": "DiscoveryAuthority@1.0.0",
                "object_id": "urn:test:lits:discovery",
                "content_hash": _h("lits-discovery"),
            },
        ],
        "oracle_build_provenance": {
            "builder": "FIABC-W3-I05",
            "dependencies": [
                {
                    "owner_class": "ACCEPTED_IMMUTABLE_PRIOR_EMPIRICAL_PRODUCT",
                    "identity": LITS_LEARNED_PRODUCT_IDENTITY,
                },
                {
                    "owner_class": dependency_owner,
                    "identity": _h("current-authority"),
                },
            ],
            "candidate_outputs_used": [],
            "pairwise_candidate_vote": False,
            "first_successful_candidate_as_golden": False,
        },
        "freeze": freeze or FreezeContext(freeze_sequence=10),
    }


def _lits_oracle(**kwargs):
    return build_lits_i_oracle(**_lits_inputs(**kwargs))


def _observation(oracle, candidate):
    return {
        "candidate": candidate,
        "oracle_identity_sha256": oracle["oracle_identity_sha256"],
        "source_identity": copy.deepcopy(oracle["source_identity"]),
        "court_constitution_refs": copy.deepcopy(oracle["court_constitution_refs"]),
        "semantic_authority_closure": copy.deepcopy(oracle["semantic_authority_closure"]),
        "projection_and_release_refs": copy.deepcopy(oracle["projection_and_release_refs"]),
        "frontier_manifest": copy.deepcopy(oracle["frontier_manifest"]),
        "fact_manifest": copy.deepcopy(oracle["expected_fact_manifest"]),
        "learned_product": copy.deepcopy(oracle["expected_learned_product"]),
        "replay_manifest": copy.deepcopy(oracle["replay_manifest"]),
        "exact_ref_manifest": copy.deepcopy(oracle["exact_ref_manifest"]),
        "negative_state_manifest": copy.deepcopy(oracle["negative_state_manifest"]),
        "authority_closure_digest": oracle["authority_closure_digest"],
        "frontier_digest": oracle["frontier_digest"],
        "self_replay_ok": True,
    }


def _wvs_materializer_result(*, candidate_owner=False, hashes=None):
    ordered = list(hashes or WVS7_ORDERED_CANDIDATE_HASHES)
    return {
        "contract": WVS_MATERIALIZER_CONTRACT,
        "source_identity": {
            "source": "WVS7",
            "sha256": WVS7_SOURCE_SHA256,
            "rows": 97220,
            "variables": 613,
        },
        "court_constitution_refs": {
            "lock2_hash": WVS7_LOCK2_IDENTITY,
            "lock2_replay_hash": WVS7_LOCK2_REPLAY_IDENTITY,
            "discovery_authority": WVS7_DISCOVERY_AUTHORITY,
            "empirical_universe": WVS7_EMPIRICAL_UNIVERSE,
            "risk_set": WVS7_RISK_SET,
            "measure_basis": WVS7_MEASURE_BASIS,
        },
        "semantic_authority_closure": [
            {
                "kind": "AuthoritySnapshot@1.0.0",
                "object_id": "urn:test:wvs:authority",
                "content_hash": _h("wvs-authority"),
            }
        ],
        "projection_and_release_refs": {
            "projection_identity": _h("wvs-projection"),
            "c11_release_identity": _h("wvs-c11"),
            "c11_replay_identity": _h("wvs-c11-replay"),
        },
        "frontier_manifest": {
            "candidate_count": 46,
            "ordered_candidate_hashes": ordered,
            "family_counts": dict(WVS7_FAMILY_COUNTS),
        },
        "expected_fact_manifest": [
            {
                "candidate_hash": candidate_hash,
                "typed_state": "EVALUATED_SUPPORTED",
                "semantic_fields": {"support": i, "denominator": 1000},
            }
            for i, candidate_hash in enumerate(ordered)
        ],
        "expected_learned_product": {
            "product_identity": _h("wvs-product"),
            "semantic_identity": _h("wvs-semantic"),
            "replay_identity": _h("wvs-replay"),
            "exact_output_identity": _h("wvs-output"),
            "coverage": {"candidate_count": 46},
        },
        "replay_manifest": {"lock2_replay_identity": WVS7_LOCK2_REPLAY_IDENTITY},
        "exact_ref_manifest": [
            {
                "kind": "EmpiricalQuerySpec@1.0.0",
                "object_id": "urn:test:wvs:query",
                "content_hash": _h("wvs-query"),
            }
        ],
        "oracle_build_provenance": {
            "builder": "WVS7_NEUTRAL_MATERIALIZER",
            "dependencies": [
                {
                    "owner_class": "CANDIDATE_B" if candidate_owner else "EXACT_SOURCE",
                    "identity": WVS7_SOURCE_SHA256,
                },
                {
                    "owner_class": "ACCEPTED_AUTHORITY",
                    "identity": WVS7_LOCK2_IDENTITY,
                },
                {
                    "owner_class": "COMMON_SEMANTIC_PRODUCER",
                    "identity": _h("common-pre553-i03-i05"),
                },
            ],
            "candidate_outputs_used": [],
            "pairwise_candidate_vote": False,
            "first_successful_candidate_as_golden": False,
        },
    }


def test_positive_three_way_requires_each_candidate_to_match_same_frozen_oracle():
    oracle = _lits_oracle()
    observations = {candidate: _observation(oracle, candidate) for candidate in ("A", "B", "C")}

    receipt = validate_three_way_parity(oracle, observations)

    assert receipt["status"] == "PASS__A_B_C_MATCH_ONE_FROZEN_CANDIDATE_NEUTRAL_ORACLE"
    assert receipt["pairwise_agreement_used_as_truth"] is False
    assert receipt["self_replay_used_as_truth"] is False
    assert {r["candidate"] for r in receipt["candidate_match_receipts"]} == {"A", "B", "C"}


def test_self_replay_pass_cannot_substitute_for_oracle_fact_match():
    oracle = _lits_oracle()
    observation = _observation(oracle, "A")
    observation["self_replay_ok"] = True
    observation["fact_manifest"][0]["semantic_fields"]["support"] += 1

    with pytest.raises(OracleMismatchError) as exc:
        validate_candidate_observation(oracle, observation)

    assert exc.value.disposition == "FAIL_CLOSED__SEMANTIC_FACT_MISMATCH"


def test_a_agreeing_with_itself_cannot_masquerade_as_three_way_parity():
    oracle = _lits_oracle()
    a = _observation(oracle, "A")
    observations = {"A": copy.deepcopy(a), "B": copy.deepcopy(a), "C": copy.deepcopy(a)}

    with pytest.raises(OracleMismatchError) as exc:
        validate_three_way_parity(oracle, observations)

    assert exc.value.disposition == "FAIL_CLOSED__CANDIDATE_IDENTITY_SUBSTITUTION"


def test_a_b_pairwise_agreement_cannot_substitute_for_missing_c():
    oracle = _lits_oracle()
    observations = {
        "A": _observation(oracle, "A"),
        "B": _observation(oracle, "B"),
    }

    with pytest.raises(OracleMismatchError) as exc:
        validate_three_way_parity(oracle, observations)

    assert exc.value.disposition == "NO_THREE_WAY_PASS__CANDIDATE_MISSING_OR_FAILED"


def test_partial_frontier_cannot_pass_even_if_remaining_facts_match():
    oracle = _lits_oracle()
    observation = _observation(oracle, "A")
    observation["frontier_manifest"]["ordered_candidate_hashes"].pop()
    observation["frontier_manifest"]["candidate_count"] = 49
    observation["fact_manifest"].pop()

    with pytest.raises(OracleMismatchError) as exc:
        validate_candidate_observation(oracle, observation)

    assert exc.value.disposition == "FAIL_CLOSED__FRONTIER_INCOMPLETE_OR_DRIFT"


def test_collapsed_negative_state_law_cannot_pass():
    oracle = _lits_oracle()
    observation = _observation(oracle, "A")
    observation["negative_state_manifest"]["valid_empty_distinction"] = "VALID_EMPTY_EQUALS_EMPTY"

    with pytest.raises(OracleMismatchError) as exc:
        validate_candidate_observation(oracle, observation)

    assert exc.value.disposition == "FAIL_CLOSED__TYPED_ABSENCE_COLLAPSE"


def test_stale_authority_closure_cannot_pass_on_equal_values():
    oracle = _lits_oracle()
    observation = _observation(oracle, "A")
    observation["semantic_authority_closure"][0]["content_hash"] = _h("stale-authority")

    with pytest.raises(OracleMismatchError) as exc:
        validate_candidate_observation(oracle, observation)

    assert exc.value.disposition == "FAIL_CLOSED__AUTHORITY_CLOSURE_MISMATCH"


def test_stale_replay_root_cannot_pass_on_equal_semantics():
    oracle = _lits_oracle()
    observation = _observation(oracle, "A")
    observation["replay_manifest"]["dependency_root"] = _h("stale-replay-root")

    with pytest.raises(OracleMismatchError) as exc:
        validate_candidate_observation(oracle, observation)

    assert exc.value.disposition == "FAIL_CLOSED__PROVENANCE_MISMATCH"


def test_candidate_owned_oracle_dependency_is_rejected():
    with pytest.raises(OracleIndependenceError):
        _lits_oracle(dependency_owner="CANDIDATE_A")


def test_bounded_physical_representation_authority_is_explicit_neutral_dependency():
    oracle = _lits_oracle(
        dependency_owner="BOUNDED_PHYSICAL_REPRESENTATION_AUTHORITY"
    )
    dependency_classes = {
        item["owner_class"]
        for item in oracle["oracle_build_provenance"]["dependencies"]
    }
    assert "BOUNDED_PHYSICAL_REPRESENTATION_AUTHORITY" in dependency_classes
    assert verify_frozen_oracle(oracle) == oracle["oracle_identity_sha256"]


def test_unrecognized_oracle_dependency_owner_still_fails_closed():
    with pytest.raises(OracleIndependenceError, match="unrecognized dependency owner class"):
        _lits_oracle(dependency_owner="UNAUTHORIZED_DEPENDENCY_OWNER")


def test_oracle_cannot_freeze_after_candidate_output_exists():
    freeze = FreezeContext(
        freeze_sequence=20,
        candidate_outputs_seen=1,
        candidate_output_first_sequence=19,
    )

    with pytest.raises(OracleIndependenceError):
        _lits_oracle(freeze=freeze)


def test_frozen_oracle_mutation_is_detected():
    oracle = _lits_oracle()
    oracle["expected_fact_manifest"][0]["semantic_fields"]["support"] += 1

    with pytest.raises(OracleIndependenceError):
        verify_frozen_oracle(oracle)


def test_current_wvs_constitution_is_successor_only_and_rejects_predecessor():
    assert WVS7_LOCK2_IDENTITY == "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
    assert WVS7_LOCK2_REPLAY_IDENTITY == "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"
    assert WVS7_DISCOVERY_AUTHORITY == "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"

    material = _wvs_materializer_result()
    material["court_constitution_refs"].update({
        "lock2_hash": "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188",
        "lock2_replay_hash": "b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490",
        "discovery_authority": "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab",
    })
    with pytest.raises(ParityOracleError, match="WVS7 constitution drift"):
        freeze_wvs7_oracle_from_common_material(
            material=material,
            freeze=FreezeContext(freeze_sequence=1),
        )


def test_wvs_source_free_freeze_accepts_exact_candidate_neutral_common_material():
    oracle = freeze_wvs7_oracle_from_common_material(
        material=_wvs_materializer_result(),
        freeze=FreezeContext(freeze_sequence=1),
    )
    assert oracle["source_identity"]["sha256"] == WVS7_SOURCE_SHA256
    assert oracle["frontier_manifest"]["candidate_count"] == 46
    assert oracle["freeze_receipt"]["candidate_outputs_seen"] == 0
    verify_frozen_oracle(oracle)


def test_wvs_source_free_freeze_rejects_candidate_owned_material():
    with pytest.raises(OracleIndependenceError):
        freeze_wvs7_oracle_from_common_material(
            material=_wvs_materializer_result(candidate_owner=True),
            freeze=FreezeContext(freeze_sequence=1),
        )


def test_wvs_materialization_rejects_wrong_source_bytes_before_semantic_execution(tmp_path):
    source = tmp_path / "WVS Wave 7.sav"
    source.write_bytes(b"not the accepted source")
    called = False

    def neutral_materializer(path, authority):
        nonlocal called
        called = True
        return _wvs_materializer_result()

    with pytest.raises(ParityOracleError, match="source sha256 drift"):
        materialize_wvs7_oracle(
            source_path=source,
            frozen_authority={"source": "WVS7"},
            neutral_materializer=neutral_materializer,
            freeze=FreezeContext(freeze_sequence=1),
        )

    assert called is False


def test_wvs_materializer_cannot_consult_candidate_owned_state(tmp_path, monkeypatch):
    source = tmp_path / "WVS Wave 7.sav"
    source.write_bytes(b"fixture bytes; sha verification monkeypatched only for contract test")
    monkeypatch.setattr(oracle_mod, "_sha256_file", lambda path: WVS7_SOURCE_SHA256)

    with pytest.raises(OracleIndependenceError):
        materialize_wvs7_oracle(
            source_path=source,
            frozen_authority={"source": "WVS7"},
            neutral_materializer=lambda path, authority: _wvs_materializer_result(
                candidate_owner=True
            ),
            freeze=FreezeContext(freeze_sequence=1),
        )


def test_wvs_exact_lock2_frontier_cannot_be_substituted_at_same_cardinality(
    tmp_path, monkeypatch
):
    source = tmp_path / "WVS Wave 7.sav"
    source.write_bytes(b"fixture bytes; sha verification monkeypatched only for contract test")
    monkeypatch.setattr(oracle_mod, "_sha256_file", lambda path: WVS7_SOURCE_SHA256)
    substituted = list(WVS7_ORDERED_CANDIDATE_HASHES)
    substituted[-1] = _h("post-outcome-substitute")

    with pytest.raises(ParityOracleError, match="exact ordered Lock2 frontier drift"):
        materialize_wvs7_oracle(
            source_path=source,
            frozen_authority={"source": "WVS7"},
            neutral_materializer=lambda path, authority: _wvs_materializer_result(
                hashes=substituted
            ),
            freeze=FreezeContext(freeze_sequence=1),
        )


def test_negative_state_contract_keeps_blocked_and_valid_empty_out_of_scalar_truth():
    assert (
        NEGATIVE_STATE_LAW["governance_blocked_state"]
        == "BLOCKED_OR_MANUAL_REVIEW_IS_GOVERNANCE_NOT_EMPIRICAL_DATA"
    )
    assert (
        NEGATIVE_STATE_LAW["valid_empty_distinction"]
        == "VALID_EMPTY_IS_NOT_UNAVAILABLE_UNRESOLVED_OR_INTEGRITY_FAILURE"
    )
