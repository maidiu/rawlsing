from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from rawlsing_next import pre553_discovery_exact as i05
from rawlsing_next.fiabc_lm2_r1l_validation_authority_successor import (
    ACTIVATION_SCHEMA,
    CANDIDATE_GRAMMAR_HASH,
    CANONICAL_VALIDATION_KINDS,
    PREDECESSOR_DISCOVERY_HASH,
    PREDECESSOR_LOCK2,
    SUCCESSION_SCHEMA,
    ValidationAuthorityRepairError,
    build_conditional_discovery_successor,
    prepare_lock2_successor,
    prepare_runtime_package_successor,
    validate_conditional_discovery_successor,
    validate_frozen_p2f2_package,
    validate_provenance_activation,
    validate_requested_validation_kinds,
    validate_succession_activation,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_PATH = ROOT / "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json"


def _package():
    return json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))


def _context():
    return validate_frozen_p2f2_package(_package())


def _eref(kind: str, tag: str) -> dict[str, str]:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return {
        "kind": kind,
        "object_id": f"urn:test:fiabc-r1l:{tag}:sha256:{digest}",
        "content_hash": digest,
    }


def _provenance(ctx=None):
    if ctx is None:
        ctx = _context()
    parent = next(
        ref for ref in ctx.predecessor.authority_snapshot_refs
        if ref.authority_id == "EE-P2F2-WVS7-LOCK1-DISCOVERY-FRONTIER"
    )
    return {
        "schema": ACTIVATION_SCHEMA,
        "status": "PASS",
        "independently_authorized": True,
        "authority_basis": "INDEPENDENT_PREOUTCOME_AUTHORITY",
        "preoutcome": True,
        "empirical_outcomes_consulted": 0,
        "candidate_outputs_consulted": 0,
        "candidate_owned_parent_refs": [],
        "authorized_validation_kinds": list(CANONICAL_VALIDATION_KINDS),
        "authority_parent_refs": [parent.as_dict()],
        "provenance_receipt_ref": _eref("FIABC_R1L_A_PROVENANCE_COURT@1.0.0", "provenance"),
    }


def _succession(candidate_hashes="MAY_REMAIN_EXACT"):
    return {
        "schema": SUCCESSION_SCHEMA,
        "status": "PASS",
        "predecessor_lock2": PREDECESSOR_LOCK2,
        "classifications": {
            "DiscoveryAuthority": "MUST_CHANGE",
            "Lock2": "MUST_CHANGE",
            "candidate_grammar": "MAY_REMAIN_EXACT",
            "candidate_hashes": candidate_hashes,
            "predicates": "OUTSIDE_INVALIDATION",
            "query_templates": "OUTSIDE_INVALIDATION",
            "universe": "OUTSIDE_INVALIDATION",
            "risk_set": "OUTSIDE_INVALIDATION",
            "measure_basis": "OUTSIDE_INVALIDATION",
        },
        "candidate_pruning_allowed": False,
        "candidate_addition_allowed": False,
        "succession_court_ref": _eref("FIABC_R1L_B_SUCCESSION_COURT@1.0.0", "succession"),
    }


def _successor(ctx=None, provenance=None):
    if ctx is None:
        ctx = _context()
    if provenance is None:
        provenance = _provenance(ctx)
    return build_conditional_discovery_successor(ctx.predecessor, provenance)


def test_01_exact_three_kind_envelope_passes_in_canonical_order():
    out = validate_requested_validation_kinds(
        reversed(CANONICAL_VALIDATION_KINDS),
        independently_authorized=CANONICAL_VALIDATION_KINDS,
    )
    assert out == CANONICAL_VALIDATION_KINDS


def test_02_missing_one_kind_fails():
    with pytest.raises(ValidationAuthorityRepairError, match="must equal exact frozen grammar use"):
        validate_requested_validation_kinds(
            CANONICAL_VALIDATION_KINDS[:-1],
            independently_authorized=CANONICAL_VALIDATION_KINDS,
        )


def test_03_extra_fourth_kind_fails_without_independent_authority_and_minimal_scope_stays_exact():
    requested = (*CANONICAL_VALIDATION_KINDS, "FUTURE_FOURTH_VALIDATOR")
    with pytest.raises(ValidationAuthorityRepairError):
        validate_requested_validation_kinds(
            requested,
            independently_authorized=CANONICAL_VALIDATION_KINDS,
        )
    # Even a separately authorized future kind is not silently imported into this
    # exact three-kind repair. A later court would need a separate successor.
    with pytest.raises(ValidationAuthorityRepairError, match="must equal exact frozen grammar use"):
        validate_requested_validation_kinds(
            requested,
            independently_authorized=requested,
        )


def test_04_wildcard_and_all_fail():
    for token in ("*", "ALL"):
        requested = tuple(CANONICAL_VALIDATION_KINDS[:-1]) + (token,)
        with pytest.raises(ValidationAuthorityRepairError):
            validate_requested_validation_kinds(
                requested,
                independently_authorized=(*CANONICAL_VALIDATION_KINDS, token),
            )


def test_05_candidate_grammar_mutation_fails_closed():
    doc = _package()
    discovery = doc["discovery_authority_documents"][0]
    discovery["semantic_fields"]["candidate_universe_definition"]["rules"][0]["rule_id"] = "MUTATED"
    with pytest.raises(Exception):
        validate_frozen_p2f2_package(doc)


def test_06_candidate_pruning_mutation_fails_closed():
    doc = _package()
    discovery = doc["discovery_authority_documents"][0]
    discovery["semantic_fields"]["pruning_contract"] = {"kind": "TOP_K", "k": 1}
    with pytest.raises(Exception):
        validate_frozen_p2f2_package(doc)


def test_07_predicate_mutation_fails_closed():
    doc = _package()
    doc["predicate_documents"][0]["content_hash"] = "0" * 64
    with pytest.raises(Exception):
        validate_frozen_p2f2_package(doc)


def test_08_query_mutation_fails_closed():
    doc = _package()
    doc["query_documents"][0]["content_hash"] = "0" * 64
    with pytest.raises(Exception):
        validate_frozen_p2f2_package(doc)


def test_09_outcome_derived_authority_fails():
    evidence = _provenance()
    evidence["empirical_outcomes_consulted"] = 1
    with pytest.raises(ValidationAuthorityRepairError, match="empirical outcomes"):
        validate_provenance_activation(evidence)

    evidence = _provenance()
    evidence["authority_basis"] = "EMPIRICAL_OUTCOME_DERIVED"
    with pytest.raises(ValidationAuthorityRepairError, match="outcome-derived"):
        validate_provenance_activation(evidence)


def test_10_candidate_output_cannot_parent_authority():
    evidence = _provenance()
    evidence["candidate_outputs_consulted"] = 1
    with pytest.raises(ValidationAuthorityRepairError, match="candidate output"):
        validate_provenance_activation(evidence)

    evidence = _provenance()
    evidence["candidate_owned_parent_refs"] = [_eref("CandidateOutput@1.0.0", "bad-parent")]
    with pytest.raises(ValidationAuthorityRepairError, match="candidate-owned"):
        validate_provenance_activation(evidence)


def test_11_old_defective_authority_still_fails_unchanged_generic_i05_guard():
    ctx = _context()
    with pytest.raises(
        Pre553AuthorityError,
        match="candidate validation rule exceeds exact discovery validation authority",
    ):
        i05.execute_exact_bounded_discovery(
            repository=object(),
            discovery_authority=ctx.predecessor,
            authority_registry=ctx.catalog.authority_registry,
            release_refs=(ExactRef("DummyRelease@1.0.0", "urn:test:release", "1" * 64),),
            predicate_catalog=ctx.catalog.predicates,
            query_template_catalog=ctx.catalog.queries,
        )


def test_12_successor_crosses_unchanged_generic_i05_validation_admission(monkeypatch):
    ctx = _context()
    successor = _successor(ctx)
    sentinel = RuntimeError("R1L_C_ADMISSION_REACHED_AFTER_GENERIC_VALIDATION_GUARD")

    def stop_before_any_empirical_evaluation(*args, **kwargs):
        raise sentinel

    monkeypatch.setattr(i05, "_evaluate_candidate", stop_before_any_empirical_evaluation)
    with pytest.raises(RuntimeError, match="R1L_C_ADMISSION_REACHED"):
        i05.execute_exact_bounded_discovery(
            repository=object(),
            discovery_authority=successor,
            authority_registry=ctx.catalog.authority_registry,
            release_refs=(ExactRef("DummyRelease@1.0.0", "urn:test:release", "1" * 64),),
            predicate_catalog=ctx.catalog.predicates,
            query_template_catalog=ctx.catalog.queries,
        )


def test_13_successor_changes_only_validation_envelope_plus_authorized_replay_parentage():
    ctx = _context()
    provenance = _provenance(ctx)
    successor = _successor(ctx, provenance)
    validate_conditional_discovery_successor(ctx.predecessor, successor, provenance)

    old = ctx.predecessor.semantic_projection()
    new = successor.semantic_projection()
    assert successor.content_hash != PREDECESSOR_DISCOVERY_HASH
    assert new["semantic_fields"]["candidate_grammar_ref"]["content_hash"] == CANDIDATE_GRAMMAR_HASH
    assert new["semantic_fields"]["candidate_universe_definition"] == old["semantic_fields"]["candidate_universe_definition"]
    assert new["semantic_fields"]["predicates"] if "predicates" in new["semantic_fields"] else True
    for key in old["semantic_fields"]:
        if key != "validation_rules":
            assert canonical_json(old["semantic_fields"][key]) == canonical_json(new["semantic_fields"][key])
    new_rules = dict(new["semantic_fields"]["validation_rules"])
    assert tuple(new_rules["kinds"]) == CANONICAL_VALIDATION_KINDS
    assert {k: v for k, v in new_rules.items() if k != "kinds"} == dict(old["semantic_fields"]["validation_rules"])


def test_14_lock2_successor_seam_changes_transitive_identities_not_frontier_semantics():
    ctx = _context()
    provenance = _provenance(ctx)
    successor = _successor(ctx, provenance)
    packet = prepare_lock2_successor(
        ctx,
        successor,
        provenance,
        _succession(),
    )
    assert packet["activated"] is False
    assert packet["predecessor_lock2"] == PREDECESSOR_LOCK2
    assert packet["successor_lock2_hash"] != PREDECESSOR_LOCK2
    assert packet["successor_discovery_authority_ref"] == successor.ref.as_dict()
    assert tuple(packet["candidate_hashes"]) == ctx.candidate_hashes
    assert packet["candidate_grammar_ref"]["content_hash"] == CANDIDATE_GRAMMAR_HASH
    assert packet["empirical_outcomes_consulted"] == 0
    assert packet["candidate_outputs_consulted"] == 0


def test_15_replay_required_by_succession_must_replay_exact_same_frontier():
    ctx = _context()
    provenance = _provenance(ctx)
    successor = _successor(ctx, provenance)
    with pytest.raises(ValidationAuthorityRepairError, match="requires source-free candidate replay"):
        prepare_lock2_successor(
            ctx, successor, provenance, _succession("MUST_REPLAY_BUT_EXPECTED_SAME")
        )
    with pytest.raises(ValidationAuthorityRepairError, match="candidate replay differs"):
        prepare_lock2_successor(
            ctx,
            successor,
            provenance,
            _succession("MUST_REPLAY_BUT_EXPECTED_SAME"),
            replayed_candidate_hashes=ctx.candidate_hashes[:-1] + ("0" * 64,),
        )
    packet = prepare_lock2_successor(
        ctx,
        successor,
        provenance,
        _succession("MUST_REPLAY_BUT_EXPECTED_SAME"),
        replayed_candidate_hashes=ctx.candidate_hashes,
    )
    assert tuple(packet["candidate_hashes"]) == ctx.candidate_hashes


def test_16_succession_court_cannot_authorize_workload_redesign():
    evidence = _succession()
    evidence["classifications"]["candidate_grammar"] = "MUST_CHANGE"
    with pytest.raises(ValidationAuthorityRepairError, match="cannot activate"):
        validate_succession_activation(evidence)

    evidence = _succession()
    evidence["candidate_pruning_allowed"] = True
    with pytest.raises(ValidationAuthorityRepairError, match="pruning"):
        validate_succession_activation(evidence)


def test_17_conditional_runtime_package_preserves_predicates_queries_and_generic_i05():
    ctx = _context()
    provenance = _provenance(ctx)
    successor = _successor(ctx, provenance)
    lock2 = prepare_lock2_successor(ctx, successor, provenance, _succession())
    package = prepare_runtime_package_successor(ctx, successor, lock2)

    assert package["status"] == "CONDITIONAL_R1L_SUCCESSOR_PREPARED__NOT_ADOPTED"
    assert package["predicate_documents"] == ctx.package["predicate_documents"]
    assert package["query_documents"] == ctx.package["query_documents"]
    assert package["discovery_authority_documents"] == [successor.as_dict()]
    assert package["counts"]["candidates"] == 46

    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=package["authority_documents"],
        predicate_documents=package["predicate_documents"],
        query_documents=package["query_documents"],
        discovery_authority_documents=package["discovery_authority_documents"],
    )
    assert catalog.discovery_authorities[0].ref == successor.ref
