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


def direction_model_authority(direction: str) -> Any:
    """A distinct exact model authority per analytical direction.

    Direction-scoping the model authority means a single determinant mutation reaches
    exactly one registered product and leaves a genuine unaffected sibling.
    """

    from rawlsing_next.pre553_empirical_objects import AuthorityRef

    entry = _authority_entry("FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL")
    base = dict(entry["expected_authority_ref"])
    material = {"fixture_only": True, "direction": direction, "base_authority": base}
    return AuthorityRef(
        authority_id=f"{base['authority_id']}-{direction.upper()}",
        authority_version=base["authority_version"],
        authority_content_hash=semantic_hash(material),
    )


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
    """Exact retained determinants a fresh process needs to recompute the product.

    This is deliberately an *exact-ref* descriptor, not a stored output: it names the
    inputs and the expected authority/output identities, and carries no precomputed
    evidence or geometry.
    """

    composition = compose(case)
    return {
        "schema": "C1_03R_RETAINED_ANALYTICAL_DETERMINANTS@1",
        "direction": case["direction"],
        "producer_route": composition.producer_route,
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
        },
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
]
