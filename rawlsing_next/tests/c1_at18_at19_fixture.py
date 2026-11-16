"""C1-03R source-free fixture for AT18 (replay grade) and AT19 (selective invalidation).

Builds one exact accepted C1-01 analytical case from the frozen C1-00 AT07 synthetic
law, runs the accepted composition owner, and exposes the exact retained determinants
so a *fresh process* can recompute the same composition from them.

Nothing here is raw survey material: the source law is a synthetic 100-respondent
response table, and the authority snapshots are the frozen synthetic C1-00 freezes.

Boundary: this module owns no maintenance/invalidation semantics. It only constructs
accepted inputs and exposes exact refs for the AT18/AT19 courts.
"""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_authority_maintenance import SemanticDeterminantGraph
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalQuerySpec,
    ExactRef,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
)
from rawlsing_next.pre553_analytical_composition import (
    ConditionValueBindingWitness,
    compose_positioned_subject_possibility,
)

import rawlsing_next.tests.test_pre553_empirical_query as i03

ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R2"
R3 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R3"
R8 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R8"
R2_RELATION = R2 / "02_VALUE_RELATION_ORACLE.json"
R2_AUTHORITIES = R2 / "03_SYNTHETIC_AUTHORITY_FREEZE.json"
R3_AUTHORITY = R3 / "02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"
R8_SPINE = R8 / "04_CURRENT_AT07_IDENTITY_SPINE.json"

#: Independently derived expected truth for the canonical forward grain.
#: An authority kind the accepted maintenance owner recognizes. The analytical model
#: authority is carried under it; the adapter invents no new authority kind.
MODEL_AUTHORITY_KIND = "SOURCE_SEMANTICS_TOPOLOGY"

FROZEN_AT07_FORWARD = {
    "denominator": 60,
    "cells": {"yes": 54, "no": 6},
    "exact_fraction_yes": {"$exact_fraction": [9, 10]},
    "consumer_state": "EXACT_SUPPORTED",
}


def load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def frozen_spine() -> Any:
    return load_json(R8_SPINE)["identity_spine"]


def at07_rows() -> list[dict[str, Any]]:
    """The exact synthetic AT07 source law: 54/6 P1 and 8/32 P2."""

    rows: list[dict[str, Any]] = []
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


def _authority_entry(authority_class: str) -> Any:
    data = load_json(R2_AUTHORITIES)
    return next(
        x for x in data["authorities"] if x["authority_class"] == authority_class
    )


def _snapshot(authority_class: str) -> AuthoritySnapshot:
    entry = _authority_entry(authority_class)
    material = dict(entry["canonical_material"])
    material.pop("schema", None)
    material.pop("purpose", None)
    material["authority_content_hash"] = entry["expected_authority_ref"][
        "authority_content_hash"
    ]
    return AuthoritySnapshot(**material)


def _query_snapshot() -> AuthoritySnapshot:
    entry = load_json(R3_AUTHORITY)["repaired_query_authority"]
    material = dict(entry["canonical_material"])
    material.pop("schema", None)
    material.pop("purpose", None)
    material["authority_content_hash"] = entry["expected_authority_ref"][
        "authority_content_hash"
    ]
    return AuthoritySnapshot(**material)


def fixture_authority(authority_class: str) -> Any:
    from rawlsing_next.pre553_empirical_objects import AuthorityRef

    return AuthorityRef(**_authority_entry(authority_class)["expected_authority_ref"])


def _relation(role: str, family: str) -> Any:
    data = load_json(R2_RELATION)
    return next(x for x in data[family] if x["material"]["role"] == role)


@contextmanager
def frozen_at07_source():
    """Yield the exact AT07 synthetic source with frozen C1-00 authority snapshots."""

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

    i03._auth = frozen_auth
    try:
        rows = at07_rows()
        source = i03._build_source(
            "c1-at07",
            rows,
            question_namespace="c1-at07",
            risk_sets={
                "R_ALL_100": {
                    "POSITION": {r["id"] for r in rows},
                    "ANSWER": {r["id"] for r in rows},
                }
            },
            risk_namespace="c1-at07",
        )
    finally:
        i03._auth = original_auth

    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL_100"]
    registry = AuthorityRegistry((*source["authorities"], query_auth))
    yield source, query_auth, registry


def build_producer(source: Any, query_auth: Any, direction: str = "forward") -> Any:
    """Exact accepted AT07 producer inputs (predicate + empirical query)."""

    if direction == "forward":
        leaf = i03._response_leaf(source, query_auth, "POSITION", "P1")
        predicate = i03._predicate(
            source, query_auth, leaf, tag="c1-at07-forward-position-p1"
        )
        query = i03._query(
            source,
            query_auth,
            predicate,
            ("ANSWER",),
            risk="R",
            tag="c1-at07-forward-position-p1-to-answer",
        )
    else:
        leaf = i03._response_leaf(source, query_auth, "ANSWER", "yes")
        predicate = i03._predicate(
            source, query_auth, leaf, tag="c1-at07-reverse-answer-yes"
        )
        query = i03._query(
            source,
            query_auth,
            predicate,
            ("POSITION",),
            risk="R",
            tag="c1-at07-reverse-answer-yes-to-position",
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
    return predicate, query


def build_consumer(
    source: Any, direction: str = "forward", *, pairing: Any = None
) -> tuple[PositionedSubjectPossibilityQuery, ConditionerBinding]:
    """Exact accepted AT07 governed consumer inputs (query + conditioner binding)."""

    if pairing is None:
        pairing = fixture_authority("FIXTURE_ONLY_CONDITION_VALUE_PAIRING")
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
            "position",
            ExactRef(**relation["ref"]),
            source["qrefs"]["POSITION"],
            pairing,
            source["universe"].ref,
            source["release_ref"],
            None,
        )
        query = PositionedSubjectPossibilityQuery(
            "c1-at07-forward-position-p1-to-answer",
            subject,
            source["qrefs"]["ANSWER"],
            source["universe"].ref,
            source["release_ref"],
            (binding,),
            {
                "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION",
                "direction": "POSITION_P1_TO_ANSWER",
                "target_role": "ANSWER",
            },
        )
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
            "answer",
            ExactRef(**relation["ref"]),
            source["qrefs"]["ANSWER"],
            pairing,
            source["universe"].ref,
            source["release_ref"],
            None,
        )
        query = PositionedSubjectPossibilityQuery(
            "c1-at07-reverse-answer-yes-to-position",
            subject,
            source["qrefs"]["POSITION"],
            source["universe"].ref,
            source["release_ref"],
            (binding,),
            {
                "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION",
                "direction": "ANSWER_YES_TO_POSITION",
                "target_role": "POSITION",
            },
        )
    return query, binding


def build_witness(
    source: Any,
    direction: str,
    consumer_query: PositionedSubjectPossibilityQuery,
    binding: ConditionerBinding,
    producer_query: EmpiricalQuerySpec,
    predicate: Any,
) -> ConditionValueBindingWitness:
    """Exact accepted AT07 custody witness (closed 16-key identity map)."""

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


def model_authority_snapshot(direction: str) -> AuthoritySnapshot:
    """The direction-scoped consumer model authority as a proper governed snapshot.

    The model authority is a first-class authority in its own right, so it is defined as
    an exact AuthoritySnapshot rather than an opaque ref. Its ``authority_ref`` is then a
    genuinely governed identity the accepted lifecycle owner can lawfully bind.
    """

    base = _snapshot("PRE553_AUTHORITY_SNAPSHOT::SOURCE_SEMANTICS_TOPOLOGY")
    material = dict(base.semantic_fields)
    material["authority_content_hash"] = base.authority_content_hash
    material["typed_state"] = "ALLOW"
    material["decision_state"] = "ALLOW"
    material["authority_id"] = f"C1-AT07-MODEL-{direction.upper()}"
    material["authority_version"] = "1.0.0"
    material["authority_kind"] = MODEL_AUTHORITY_KIND
    material["governed_operations"] = ("MODEL_LAW",)
    material["governed_object_families"] = ("ReplayReceipt@1.0.0",)
    material["parent_authority_refs"] = ()
    material["supersession_refs"] = ()
    material["producer_replay_locator_or_reference_root"] = (
        base.producer_replay_locator_or_reference_root
    )
    material["authority_snapshot_refs"] = tuple(base.authority_snapshot_refs)
    material["dependency_refs"] = tuple(base.dependency_refs)
    return AuthoritySnapshot(**material)


def direction_model_authority(direction: str) -> Any:
    """The exact governed model authority ref for a direction."""

    return model_authority_snapshot(direction).authority_ref


def revised_model_authority_snapshot(direction: str) -> AuthoritySnapshot:
    """A distinct governed revision of the direction's model authority."""

    base = model_authority_snapshot(direction)
    material = dict(base.semantic_fields)
    material["authority_content_hash"] = base.authority_content_hash
    material["typed_state"] = base.typed_state
    material["producer_replay_locator_or_reference_root"] = (
        base.producer_replay_locator_or_reference_root
    )
    material["authority_snapshot_refs"] = tuple(base.authority_snapshot_refs)
    material["dependency_refs"] = tuple(base.dependency_refs)
    material["authority_version"] = "2.0.0"
    material["parent_authority_refs"] = (base.authority_ref,)
    material["supersession_refs"] = (base.authority_ref,)
    material["interpretation_semantics_fingerprint"] = semantic_hash(
        {"revised": direction, "generation": 2}
    )
    return AuthoritySnapshot(**material)


def revised_model_authority(direction: str) -> Any:
    return revised_model_authority_snapshot(direction).authority_ref


def build_model_rule(
    source: Any, direction: str = "forward", *, model_authority: Any = None
) -> PositionedSubjectPossibilityModelRule:
    if model_authority is None:
        model_authority = direction_model_authority(direction)
    return PositionedSubjectPossibilityModelRule(
        model_authority,
        fixture_authority("FIXTURE_ONLY_WALKBACK_POLICY"),
        (source["universe"].ref,),
        (),
        (),
    )


def build_case(direction: str = "forward") -> dict[str, Any]:
    """Assemble the complete frozen analytical case for ``direction``."""

    with frozen_at07_source() as (source, query_auth, registry):
        predicate, producer_query = build_producer(source, query_auth, direction)
        consumer_query, binding = build_consumer(source, direction)
        witness = build_witness(
            source, direction, consumer_query, binding, producer_query, predicate
        )
        model_rule = build_model_rule(source, direction)
        return {
            "direction": direction,
            "source": source,
            "query_authority": query_auth,
            "registry": registry,
            "predicate": predicate,
            "empirical_query": producer_query,
            "consumer_query": consumer_query,
            "conditioner_binding": binding,
            "condition_binding_witness": witness,
            "model_rule": model_rule,
            "release_refs": (source["release_ref"],),
        }


def compose(case: dict[str, Any]) -> Any:
    """Run the accepted C1 analytical composition owner on a frozen case."""

    return compose_positioned_subject_possibility(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )


def replay_protocol_ref(case: dict[str, Any]) -> ExactRef:
    """The exact replay-protocol reference the accepted producer path actually uses."""

    root = case["empirical_query"].producer_replay_locator_or_reference_root
    if isinstance(root, ExactRef):
        return root
    from rawlsing_next.pre553_empirical_objects import _replay_root

    return _replay_root(root)


def deterministic_order_ref(case: dict[str, Any]) -> ExactRef:
    """The exact deterministic-order reference the accepted predicate path uses."""

    root = case["predicate"].producer_replay_locator_or_reference_root
    if isinstance(root, ExactRef):
        return root
    from rawlsing_next.pre553_empirical_objects import _replay_root

    return _replay_root(root)


def retained_determinants(case: dict[str, Any]) -> dict[str, Any]:
    """HQ-BLOCK-RETAINED-ANSWER-004: runner *input* carries only retained determinants.

    This describes exactly the inputs needed to reconstruct and re-execute the accepted
    producer/composition path. It deliberately contains **no** expected output, no
    result/evidence/fact ref, no denominator support and no geometry, so a fresh process
    reading it cannot obtain the answer.
    """

    return {
        "schema": "C1_03R_RETAINED_DETERMINANTS_INPUT@2",
        "direction": case["direction"],
        "empirical_query_ref": case["empirical_query"].ref.as_dict(),
        "predicate_ref": case["predicate"].ref.as_dict(),
        "predicate_hash": case["predicate"].predicate_hash,
        "condition_binding_witness_ref": case["condition_binding_witness"].witness_ref.as_dict(),
        "consumer_query_ref": case["consumer_query"].ref.as_dict(),
        "model_rule_hash": case["model_rule"].rule_hash,
        "release_refs": [x.as_dict() for x in case["release_refs"]],
        "source_universe_ref": case["source"]["universe"].ref.as_dict(),
        "authority_snapshot_refs": [
            x.as_dict() for x in case["empirical_query"].authority_snapshot_refs
        ],
        "conditioner_binding_refs": [
            x.empirical_coordinate_ref.as_dict()
            for x in case["consumer_query"].conditioner_bindings
        ],
    }


def oracle_expected_output(case: dict[str, Any]) -> dict[str, Any]:
    """The *oracle* side: expected output identity and support.

    This is asserted by the parent court and is never handed to the fresh runner.
    """

    composition = compose(case)
    return {
        "schema": "C1_03R_AT18_EXPECTED_OUTPUT_ORACLE@1",
        "direction": case["direction"],
        "expected_output_identity": {
            "composed_result_identity_hash": composition.composed_result_identity_hash,
            "producer_fact_ref": composition.producer_fact_ref.as_dict(),
            "evidence_ref_or_null": (
                None
                if composition.possibility_slice_evidence_or_null is None
                else composition.possibility_slice_evidence_or_null.evidence_ref.as_dict()
            ),
            "consumer_result_hash_or_null": (
                None
                if composition.consumer_result_or_null is None
                else composition.consumer_result_or_null.result_hash
            ),
            "raw_denominator_support": composition.raw_denominator_support,
            "cell_numerators": {
                cell["cell"]: cell["raw_numerator_support"]
                for cell in composition.complete_cell_geometry
            },
        },
    }


# --------------------------------------------------------------------------
# AT19 owner-ceremony helpers (accepted lifecycle owner drives the transition)
# --------------------------------------------------------------------------
def _model_candidate(
    model_authority: Any,
    *,
    version: str,
    evidence_ref: ExactRef,
    parent: Any = None,
    supersession: Any = None,
    semantics: str,
) -> Any:
    from rawlsing_next.pre553_authority_maintenance import AuthorityCandidate

    return AuthorityCandidate(
        candidate_id=f"CAND-{model_authority.authority_id}-{version}-{semantics}",
        candidate_revision=1,
        authority_id=model_authority.authority_id,
        authority_version=version,
        authority_kind=MODEL_AUTHORITY_KIND,
        proposed_decision_state="ALLOW",
        governed_operations=("MODEL_LAW",),
        governed_object_families=("ReplayReceipt@1.0.0",),
        scope_envelope={
            "source_universe_refs": (),
            "target_use_refs": ("ANALYTICAL_PRODUCT",),
        },
        effective_time_or_interval="ALL_TIME",
        evidence_receipt_refs=(evidence_ref,),
        proposed_parent_authority_refs=parent or (),
        proposed_negative_limit_refs=(),
        proposed_supersession_refs=supersession or (),
        interpretation_semantics={"model_law": semantics},
        replay_protocol_ref=_ref_for("REPLAY_PROTOCOL", f"model-{semantics}"),
        correction_kind="NONE",
        correction_target_refs=(),
        correction_scope_ref=None,
        source_onboarding_refs=(),
    )


def _ref_for(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:hq149:{kind.lower()}:{tag}", semantic_hash(f"hq149:{kind}:{tag}"))


def build_model_authority_transition(direction: str):
    """Drive a governed revision of a direction's model authority through the owner.

    The accepted owner's exact semantics are used:

    * the *baseline* selection is supplied as ``initial_current_selection`` (it is an
      already-accepted current authority, so no promotion ceremony is needed for it);
    * one governed *revision* is then produced through candidate -> APPROVED
      adjudication -> seal -> ``promote_current``, which is the owner's own transition.

    The determinant graph contains ONLY the authority the analytical product actually
    consumed. The revision enters solely through the promotion transition.
    """

    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityEvidenceReceipt,
        AuthorityMaintenanceExecutor,
    )

    case = build_case(direction)
    composition = compose(case)
    old_model = case["model_rule"].model_authority_ref
    product_ref = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        f"urn:test:c1-03r:composed:{direction}",
        composition.composed_result_identity_hash,
    )

    # The graph contains exactly the determinants the products actually consumed.
    # The sibling product is bound to its own (different) model authority identity.
    sibling_case = build_case("reverse") if direction == "forward" else build_case("forward")
    sibling_direction = "reverse" if direction == "forward" else "forward"
    sibling_ref = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        f"urn:test:c1-03r:composed:{sibling_direction}",
        compose(sibling_case).composed_result_identity_hash,
    )
    sibling_authority = direction_model_authority(sibling_direction)
    graph = SemanticDeterminantGraph(
        authority_edges=((old_model, product_ref), (sibling_authority, sibling_ref)),
        dependency_edges=(),
        known_dependent_refs=(product_ref, sibling_ref),
    )
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(model_authority_snapshot(direction),),
        initial_current_selection={old_model.authority_id: old_model},
        determinant_graph=graph,
    )
    evidence = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(_ref_for("EVIDENCE", f"{direction}-model"),),
        provenance_refs=(_ref_for("PROVENANCE", f"{direction}-model"),),
        source_release_refs=(),
    )
    executor.intake_evidence(evidence)

    revised_model = revised_model_authority(direction)
    revision = _model_candidate(
        revised_model,
        version="2.0.0",
        evidence_ref=evidence.ref,
        parent=(old_model,),
        supersession=(old_model,),
        semantics=f"{direction}-v2",
    )
    executor.intake_candidate(revision)
    adjudication = executor.adjudicate_candidate(
        revision.ref,
        decision="APPROVED",
        adjudicator_ref=_ref_for("ADJUDICATOR", f"{direction}-v2"),
        adjudication_authority_ref=_ref_for("GOVERNING_AUTHORITY", "HQ149"),
        findings_ref=_ref_for("FINDINGS", f"{direction}-v2"),
    )
    seal = executor.seal_revision(
        revision.ref,
        adjudication.ref,
        seal_attestation_ref=_ref_for("SEAL_ATTESTATION", f"{direction}-v2"),
    )
    return {
        "direction": direction,
        "case": case,
        "composition": composition,
        "product_ref": product_ref,
        "executor": executor,
        "old_model": old_model,
        # The DECOY. ``revised_model_authority_snapshot`` reuses the base snapshot's
        # authority_content_hash and only changes version/fingerprint/parentage, so
        # this ref carries the SAME content hash as the consumed v1 authority. It is
        # NOT the successor and must never be used as one.
        "unsealed_decoy_model_ref": revised_model,
        # The candidate-derived ref that was actually adjudicated, sealed and is
        # eligible for release. This is the only lawful successor.
        "sealed_successor_ref": revision.proposed_authority_ref,
        # Kept for compatibility with earlier courts, but equal to the sealed
        # successor, not to the decoy.
        "revised_model_snapshot_ref": revision.proposed_authority_ref,
        "seal_ref": seal.ref,
        "product_ref_key": product_ref.key,
        "sibling_ref": sibling_ref,
        "sibling_authority": sibling_authority,
        "sibling_direction": sibling_direction,
    }


def sealed_successor_of(transition: dict[str, Any]) -> Any:
    """The exact sealed authority ref a governed transition may recompose under.

    This resolves the successor through the OWNER (the sealed snapshot the candidate
    produced), never through the separately synthesized decoy snapshot and never by
    version label. The decoy shares the consumed prior's content hash, so choosing it
    would silently recompute the product under the authority it already consumed.
    """
    successor = transition["sealed_successor_ref"]
    decoy = transition["unsealed_decoy_model_ref"]
    consumed = transition["old_model"]
    if successor.authority_content_hash == consumed.authority_content_hash:
        raise AssertionError("sealed successor must differ from the consumed prior")
    if decoy.authority_content_hash == consumed.authority_content_hash:
        # Documented hazard, not an error: this is exactly why the decoy is unusable.
        pass
    return successor


def build_model_rule_from_sealed_successor(
    case: dict[str, Any], transition: dict[str, Any]
) -> Any:
    """Build the consumer model rule bound to the exact governed successor.

    ``PositionedSubjectPossibilityModelRule.material`` binds the complete model
    authority ref, so ``rule_hash`` cryptographically commits the rule to this exact
    successor. A court can therefore prove the rule binds the successor rather than
    the decoy.
    """
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule,
    )

    successor = sealed_successor_of(transition)
    base = case["model_rule"]
    return PositionedSubjectPossibilityModelRule(
        successor,
        base.walkback_authority_ref,
        base.source_universe_refs,
        base.walkback_steps,
        base.positive_proxy_authority_refs,
    )


def recompose_product_under_model_authority(direction: str):
    """A real recomposition path: re-runs the accepted composition owner.

    Returns ``(affected_product_ref, successor_authority_ref) -> new_exact_ref``. The new
    identity preserves the affected product's object id and carries the composition
    identity the accepted owner actually recomputes under the successor authority.
    """

    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule,
    )

    case = build_case(direction)
    rule = case["model_rule"]

    def recompose(affected_ref: ExactRef, authority: Any) -> ExactRef:
        mutated_rule = PositionedSubjectPossibilityModelRule(
            authority,
            rule.walkback_authority_ref,
            rule.source_universe_refs,
            rule.walkback_steps,
            rule.positive_proxy_authority_refs,
        )
        composition = compose_positioned_subject_possibility(
            repository=case["source"]["repo"],
            empirical_query=case["empirical_query"],
            predicate=case["predicate"],
            authority_registry=case["registry"],
            release_refs=case["release_refs"],
            consumer_query=case["consumer_query"],
            model_rule=mutated_rule,
            condition_binding_witness=case["condition_binding_witness"],
        )
        # The product keeps its stable exact identity (kind + object id); only the
        # semantic content identity changes, and it is exactly the accepted composition
        # identity recomputed under the supplied successor authority.
        return ExactRef(
            affected_ref.kind,
            affected_ref.object_id,
            composition.composed_result_identity_hash,
        )

    return recompose


def drive_owner_contract_without_recompiler():
    """Counterexample path A: an affected dependent with no recompiler declared.

    Requires that the owner has an affected dependent, then asks it to promote with
    ``recompiler=None``. The owner refuses (it cannot represent "no replacement").
    """

    transition = build_model_authority_transition("forward")
    return transition["executor"].promote_current(
        transition["seal_ref"],
        selection_rule_ref=_ref_for("SELECTION_RULE", "counterexample-a"),
        selection_attestation_ref=_ref_for("SELECTION_ATTESTATION", "counterexample-a"),
        recompiler=None,
    )


def drive_owner_contract_with_identity_recompiler():
    """Counterexample path B: the honest "nothing changed" recompiler.

    If the affected product genuinely has no lawful replacement, the only truthful
    recompilation is identity, which the owner rejects because the receipt demands a
    *new* exact ref for every affected dependent.
    """

    transition = build_model_authority_transition("forward")
    return transition["executor"].promote_current(
        transition["seal_ref"],
        selection_rule_ref=_ref_for("SELECTION_RULE", "counterexample-b"),
        selection_attestation_ref=_ref_for("SELECTION_ATTESTATION", "counterexample-b"),
        recompiler=lambda old_ref, changed: old_ref,
    )
def build_mixed_outcome_rollback_transition(direction: str = "forward"):
    """A THREE-state sequence whose final step is a genuine mixed-outcome ROLLBACK.

    Sequence, all driven through the owner's own ``promote_current`` /
    ``rollback_current``:

    1. promotion  v1 -> v2   (mixed R/N/U);
    2. promotion  v2 -> v3   (mixed R/N/U);
    3. rollback   v3 -> v2   (mixed R/N/U, citing the step-1 release).

    The determinant graph binds each analytical product to the exact model-authority
    revisions that own it, so every one of those three governed transitions genuinely
    reaches the products rather than silently producing an empty affected set. The
    sibling stays bound to the other direction's model authority and is unaffected
    throughout.

    Purpose: prove the promotion and rollback paths share ONE owner law, so the
    HQ155 fail-closed repairs (duplicate-row rejection, serialized negative-field and
    schema enforcement, owner-unknown currentness, checkpoint U re-derivation) apply
    identically on both paths and neither path invents an outcome.

    The caller drives the three transitions and supplies the recomposition callback;
    this fixture only stages the governed revisions, seals and declarations.
    """
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityEvidenceReceipt,
        AuthorityMaintenanceExecutor,
        NoncurrentDependentOutcome,
        NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    )

    case = build_case(direction)
    compose(case)
    old_model = case["model_rule"].model_authority_ref
    v2_base_ref = revised_model_authority(direction)
    sibling_direction = "reverse" if direction == "forward" else "forward"
    sibling_authority = direction_model_authority(sibling_direction)
    sibling_ref = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        f"urn:test:c1-03r:composed:{sibling_direction}",
        compose(build_case(sibling_direction)).composed_result_identity_hash,
    )

    def _product(kind_tag: str) -> ExactRef:
        return ExactRef(
            "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
            f"urn:test:c1-03r:rb:{direction}:{kind_tag}",
            semantic_hash({"rb": kind_tag, "direction": direction}),
        )

    replaced_product = _product("replaced")
    noncurrent_product = _product("noncurrent")
    downstream_product = _product("downstream")

    # Evidence first, then the candidates that cite it. Both revisions are minted here
    # so their exact proposed authority refs can be named in the determinant graph; the
    # executor then seals these very candidates, and derives the sealed snapshot itself.
    evidence_v2 = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(_ref_for("EVIDENCE", f"{direction}-rb-v2"),),
        provenance_refs=(_ref_for("PROVENANCE", f"{direction}-rb-v2"),),
        source_release_refs=(),
    )
    evidence_v3 = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(_ref_for("EVIDENCE", f"{direction}-rb-v3"),),
        provenance_refs=(_ref_for("PROVENANCE", f"{direction}-rb-v3"),),
        source_release_refs=(),
    )
    v2_candidate = _model_candidate(
        v2_base_ref, version="2.0.0", evidence_ref=evidence_v2.ref,
        parent=(old_model,), supersession=(old_model,), semantics=f"{direction}-rb-v2",
    )
    v2_ref = v2_candidate.proposed_authority_ref
    v3_candidate = _model_candidate(
        v2_base_ref, version="3.0.0", evidence_ref=evidence_v3.ref,
        parent=(v2_ref,), supersession=(v2_ref,), semantics=f"{direction}-rb-v3",
    )
    v3_ref = v3_candidate.proposed_authority_ref

    model_revisions = (old_model, v2_ref, v3_ref)
    graph = SemanticDeterminantGraph(
        authority_edges=tuple(
            (revision, product)
            for revision in model_revisions
            for product in (replaced_product, noncurrent_product, downstream_product)
        ) + ((sibling_authority, sibling_ref),),
        dependency_edges=((noncurrent_product, downstream_product),),
        known_dependent_refs=(
            replaced_product, noncurrent_product, downstream_product, sibling_ref,
        ),
    )
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(model_authority_snapshot(direction),),
        initial_current_selection={old_model.authority_id: old_model},
        determinant_graph=graph,
    )

    def _stage(evidence, candidate, *, tag):
        executor.intake_evidence(evidence)
        executor.intake_candidate(candidate)
        adjudication = executor.adjudicate_candidate(
            candidate.ref, decision="APPROVED",
            adjudicator_ref=_ref_for("ADJUDICATOR", f"{direction}-rb-{tag}"),
            adjudication_authority_ref=_ref_for("GOVERNING_AUTHORITY", "HQ155"),
            findings_ref=_ref_for("FINDINGS", f"{direction}-rb-{tag}"),
        )
        return executor.seal_revision(
            candidate.ref, adjudication.ref,
            seal_attestation_ref=_ref_for("SEAL_ATTESTATION", f"{direction}-rb-{tag}"),
        )

    seal_v2 = _stage(evidence_v2, v2_candidate, tag="v2")
    seal_v3 = _stage(evidence_v3, v3_candidate, tag="v3")

    policy_ref = _ref_for("REPLACEMENT_POLICY", f"{direction}-rollback-no-source")
    noncurrent_declarations = {
        noncurrent_product.key: NoncurrentDependentOutcome(
            old_ref=noncurrent_product,
            disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
            reason_code="NO_LAWFUL_REPLACEMENT_SOURCE",
            supporting_refs=(policy_ref,),
        ),
        downstream_product.key: NoncurrentDependentOutcome(
            old_ref=downstream_product,
            disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
            reason_code="REQUIRED_INPUT_NONCURRENT",
            supporting_refs=(policy_ref, noncurrent_product),
        ),
    }
    return {
        "direction": direction,
        "executor": executor,
        "seal_v2_ref": seal_v2.ref,
        "seal_v3_ref": seal_v3.ref,
        "v2_ref": v2_ref,
        "v3_ref": v3_ref,
        "old_model": old_model,
        "sibling_authority": sibling_authority,
        "replaced_product": replaced_product,
        "noncurrent_product": noncurrent_product,
        "downstream_product": downstream_product,
        "sibling_ref": sibling_ref,
        "noncurrent_declarations": noncurrent_declarations,
        "no_replacement_policy_ref": policy_ref,
        "graph": graph,
    }


__all__ = [

    "ROOT",
    "R2",
    "R3",
    "R8",
    "R2_RELATION",
    "R2_AUTHORITIES",
    "R3_AUTHORITY",
    "R8_SPINE",
    "FROZEN_AT07_FORWARD",
    "load_json",
    "frozen_spine",
    "at07_rows",
    "fixture_authority",
    "frozen_at07_source",
    "build_producer",
    "build_consumer",
    "build_witness",
    "build_model_rule",
    "direction_model_authority",
    "build_case",
    "compose",
    "replay_protocol_ref",
    "deterministic_order_ref",
    "retained_determinants",
    "oracle_expected_output",
    "MODEL_AUTHORITY_KIND",
    "model_authority_snapshot",
    "revised_model_authority_snapshot",
    "revised_model_authority",
    "model_authority_snapshot",
    "build_model_authority_transition",
    "recompose_product_under_model_authority",
    "drive_owner_contract_without_recompiler",
    "drive_owner_contract_with_identity_recompiler",
]


# --------------------------------------------------------------------------
# AT19 mixed-outcome release (Astra option-A)
# --------------------------------------------------------------------------
def build_mixed_outcome_transition(
    direction: str = "forward", *, include_downstream_edge: bool = True
):
    """ONE governed source-free release with all three dependent outcomes.

    Registered dependents of the single changed model authority:

    * ``replaced_product``   -- affected, has a real recomposition path;
    * ``noncurrent_product`` -- affected, the domain explicitly declares that no
      lawful replacement exists, with grounds;
    * ``downstream_product`` -- affected transitively through ``noncurrent_product``.
      It must NOT receive a replacement built from a noncurrent required input, so
      the domain declares its absence with the upstream noncurrent row as ground.
    * ``sibling_ref``        -- bound to a different, unchanged authority, so it is
      unaffected and must stay identity-stable and current.
    """
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityEvidenceReceipt,
        AuthorityMaintenanceExecutor,
        NoncurrentDependentOutcome,
        NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    )

    case = build_case(direction)
    composition = compose(case)
    old_model = case["model_rule"].model_authority_ref
    sibling_direction = "reverse" if direction == "forward" else "forward"
    sibling_authority = direction_model_authority(sibling_direction)

    def _product(kind_tag: str):
        return ExactRef(
            "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
            f"urn:test:c1-03r:composed:{direction}:{kind_tag}",
            semantic_hash({"mixed": kind_tag, "direction": direction}),
        )

    replaced_product = _product("replaced")
    noncurrent_product = _product("noncurrent")
    downstream_product = _product("downstream")
    sibling_ref = ExactRef(
        "C1_ANALYTICAL_COMPOSED_PRODUCT@1",
        f"urn:test:c1-03r:composed:{sibling_direction}",
        compose(build_case(sibling_direction)).composed_result_identity_hash,
    )

    graph = SemanticDeterminantGraph(
        authority_edges=(
            (old_model, replaced_product),
            (old_model, noncurrent_product),
            (sibling_authority, sibling_ref),
        ),
        dependency_edges=(
            ((noncurrent_product, downstream_product),)
            if include_downstream_edge else ()
        ),
        known_dependent_refs=(
            replaced_product, noncurrent_product, downstream_product, sibling_ref,
        ),
    )
    executor = AuthorityMaintenanceExecutor(
        initial_snapshots=(model_authority_snapshot(direction),),
        initial_current_selection={old_model.authority_id: old_model},
        determinant_graph=graph,
    )
    evidence = AuthorityEvidenceReceipt(
        evidence_role="SEMANTIC_AUTHORITY_EVIDENCE",
        evidence_refs=(_ref_for("EVIDENCE", f"{direction}-mixed"),),
        provenance_refs=(_ref_for("PROVENANCE", f"{direction}-mixed"),),
        source_release_refs=(),
    )
    executor.intake_evidence(evidence)
    revision = _model_candidate(
        revised_model_authority(direction),
        version="2.0.0",
        evidence_ref=evidence.ref,
        parent=(old_model,),
        supersession=(old_model,),
        semantics=f"{direction}-mixed-v2",
    )
    executor.intake_candidate(revision)
    adjudication = executor.adjudicate_candidate(
        revision.ref,
        decision="APPROVED",
        adjudicator_ref=_ref_for("ADJUDICATOR", f"{direction}-mixed"),
        adjudication_authority_ref=_ref_for("GOVERNING_AUTHORITY", "HQ151"),
        findings_ref=_ref_for("FINDINGS", f"{direction}-mixed"),
    )
    seal = executor.seal_revision(
        revision.ref,
        adjudication.ref,
        seal_attestation_ref=_ref_for("SEAL_ATTESTATION", f"{direction}-mixed"),
    )

    policy_ref = _ref_for("REPLACEMENT_POLICY", f"{direction}-no-source")
    no_source_row = NoncurrentDependentOutcome(
        old_ref=noncurrent_product,
        disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
        reason_code="NO_LAWFUL_REPLACEMENT_SOURCE",
        supporting_refs=(policy_ref,),
    )
    downstream_row = NoncurrentDependentOutcome(
        old_ref=downstream_product,
        disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
        reason_code="REQUIRED_INPUT_NONCURRENT",
        supporting_refs=(policy_ref, noncurrent_product),
    )
    return {
        "direction": direction,
        "case": case,
        "executor": executor,
        "seal_ref": seal.ref,
        "old_model": old_model,
        "sealed_successor_ref": revision.proposed_authority_ref,
        "replaced_product": replaced_product,
        "noncurrent_product": noncurrent_product,
        "downstream_product": downstream_product,
        "sibling_ref": sibling_ref,
        "sibling_authority": sibling_authority,
        "noncurrent_declarations": {
            noncurrent_product.key: no_source_row,
            downstream_product.key: downstream_row,
        },
        "no_replacement_policy_ref": policy_ref,
        "graph": graph,
    }
