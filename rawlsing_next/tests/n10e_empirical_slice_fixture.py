"""N10E independent source-free fixture and frozen oracle material.

This module is deliberately separate from the candidate provider: it freezes the
exact AT07 synthetic source law, the accepted-authority bindings and the expected
canonical results *before* any provider output is used as expected truth.

Independence argument:

* the source law is an exact synthetic response table (100 respondents) defined
  here, not read back from the provider;
* the expected canonical results are exact arithmetic on that table
  (54/60 = 9/10 forward, 54/62 = 27/31 reverse), plus the frozen R8 identity spine
  refs that the accepted C1-00/C1-01 courts already bind to;
* the authority snapshots are the frozen synthetic C1-00 freezes, not provider
  internals.

Everything here is source-free: synthetic fixture rows, no raw survey file, no
real-source C11 execution, no measured P2X, no Candidate A/B/C.
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
from rawlsing_next.pre553_analytical_composition import ConditionValueBindingWitness

import rawlsing_next.tests.test_pre553_empirical_query as i03

ROOT = Path(__file__).resolve().parents[2]
R2 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R2"
R3 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R3"
R8 = ROOT / "WORKER_RETURNS" / "PYAT-C1-00-CONTRACT-CORRECTION-R8"
R2_RELATION = R2 / "02_VALUE_RELATION_ORACLE.json"
R2_AUTHORITIES = R2 / "03_SYNTHETIC_AUTHORITY_FREEZE.json"
R8_SPINE = R8 / "04_CURRENT_AT07_IDENTITY_SPINE.json"
R3_AUTHORITY = R3 / "02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json"

#: Independently derived expected truth. Forward: 54 yes / 60 denominator = 9/10.
#: Reverse: 54 P1 / 62 denominator = 27/31.
FROZEN_ORACLE = {
    "fixture_id": "AT07_BIDIRECTIONAL_100",
    "fixture_rows": 100,
    "forward": {
        "direction": "POSITION_P1_TO_ANSWER",
        "denominator": 60,
        "cells": {"yes": 54, "no": 6},
        "expected_fraction": {"$exact_fraction": [9, 10]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "reverse": {
        "direction": "ANSWER_YES_TO_POSITION",
        "denominator": 62,
        "cells": {"P1": 54, "P2": 8},
        "expected_fraction": {"$exact_fraction": [27, 31]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
}

N10E_EXACT_ALLOWED_CONSUMER_STATES = frozenset({"EXACT_SUPPORTED"})

#: Second, genuinely different source-free empirical law used by the corrected P6
#: changed-source proof. It appends 10 extra ``POSITION=P1, ANSWER=no`` respondents,
#: which keeps both target domains ({no,yes} and {P1,P2}), the risk-set construction
#: and the conditioner grain identical while changing the empirical counts. The
#: P1-positive cohort stays at 60, so the forward denominator is the *complement*
#: count that moves: 60 -> 70.
CHANGED_SOURCE_VARIANT = "CHANGED_SOURCE_LAW"
CHANGED_SOURCE_EXTRA_ROWS = 10

FROZEN_CHANGED_ORACLE = {
    "fixture_id": "AT07_BIDIRECTIONAL_110_CHANGED_SOURCE_LAW",
    "fixture_rows": 110,
    "forward": {
        "direction": "POSITION_P1_TO_ANSWER",
        "denominator": 70,
        "cells": {"yes": 54, "no": 16},
        "expected_fraction_yes": {"$exact_fraction": [27, 35]},
        "expected_fraction_no": {"$exact_fraction": [8, 35]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "reverse": {
        "direction": "ANSWER_YES_TO_POSITION",
        "denominator": 62,
        "cells": {"P1": 54, "P2": 8},
        "expected_fraction_P1": {"$exact_fraction": [27, 31]},
        "expected_consumer_state": "EXACT_SUPPORTED",
    },
    "expected_relation_to_canonical": {
        "forward_denominator_differs": True,
        "forward_cells_differ": True,
        "forward_yes_cell_unchanged": True,
        "reverse_denominator_unchanged": True,
        "source_universe_ref_differs": True,
        "source_release_ref_differs": True,
    },
}


def load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def frozen_spine() -> Any:
    return load_json(R8_SPINE)["identity_spine"]


def at07_rows() -> list[dict[str, Any]]:
    """The exact synthetic source law: 54/6 P1 and 8/32 P2."""

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


def changed_source_rows() -> list[dict[str, Any]]:
    """The canonical AT07 law plus 10 extra ``POSITION=P1, ANSWER=no`` respondents.

    Independent arithmetic on this law: the conditioner cohort is still the 60
    ``POSITION=P1`` respondents, but the target denominator follows the changed
    cohort composition, giving 54/70 = 27/35 for "yes" and 16/70 = 8/35 for "no".
    """

    extra = [
        {"id": f"P1X{n:03d}", "responses": {"POSITION": "P1", "ANSWER": "no"}}
        for n in range(1, CHANGED_SOURCE_EXTRA_ROWS + 1)
    ]
    return at07_rows() + extra


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


def frozen_changed_source_query_authority(universe_ref: Any) -> AuthoritySnapshot:
    """A source-free query authority whose explicit scope names ``universe_ref``.

    The canonical AT07 query authority is *explicitly* scoped to the single canonical
    universe. The changed-source law lives in a different universe, so it requires an
    authority that explicitly names that universe — no implicit scope widening and no
    "latest"/"default" fallback. This copies the canonical snapshot's governed
    semantics, replaces only the explicit universe scope, and rebinds the authority
    content hash to the new semantic material (the hash is validated as sha256 and is
    the exact-identity binding of that material).
    """

    base = _query_snapshot()
    material = dict(base.semantic_fields)
    material["typed_state"] = base.typed_state
    material["producer_replay_locator_or_reference_root"] = (
        base.producer_replay_locator_or_reference_root
    )
    material["authority_snapshot_refs"] = tuple(base.authority_snapshot_refs)
    material["dependency_refs"] = tuple(base.dependency_refs)
    scope = dict(material["scope_envelope"])
    scope["source_universe_refs"] = [canonicalize(universe_ref)]
    material["scope_envelope"] = scope
    material["authority_id"] = "C1-AT07-CHANGED-SOURCE-QUERY"
    material["authority_content_hash"] = semantic_hash(canonicalize(material))
    return AuthoritySnapshot(**material)


@contextmanager
def frozen_at07_source(
    *,
    tag: str = "c1-at07",
    rows: list[dict[str, Any]] | None = None,
    question_namespace: str = "c1-at07",
    risk_namespace: str = "c1-at07",
    scope_query_authority_to_universe: bool = False,
):
    """Yield a source-free synthetic source with the frozen C1-00 authority snapshots.

    Defaults reproduce the canonical AT07 law exactly. Passing ``rows`` (and a distinct
    ``tag``) yields a *different empirical source law* built the same way, while the
    authority snapshots, question/risk namespaces and consumer fixture semantics stay
    identical — so a changed-source case exercises the real producer/consumer seam
    rather than a different fixture procedure.
    """

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

    def frozen_auth(tag_, kind, *, families):
        if kind in exact_by_kind:
            return exact_by_kind[kind]
        return original_auth(tag_, kind, families=families)

    i03._auth = frozen_auth
    try:
        active_rows = at07_rows() if rows is None else rows
        source = i03._build_source(
            tag,
            active_rows,
            question_namespace=question_namespace,
            risk_sets={
                "R_ALL_100": {
                    "POSITION": {r["id"] for r in active_rows},
                    "ANSWER": {r["id"] for r in active_rows},
                }
            },
            risk_namespace=risk_namespace,
        )
    finally:
        i03._auth = original_auth

    source["risk_refs"]["R"] = source["risk_refs"]["R_ALL_100"]
    if scope_query_authority_to_universe:
        query_auth = frozen_changed_source_query_authority(source["universe"].ref)
    registry = AuthorityRegistry((*source["authorities"], query_auth))
    yield source, query_auth, registry


def build_producer(source: Any, query_auth: Any, direction: str) -> Any:
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
    source: Any, direction: str, *, pairing: Any = None
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
    """Exact accepted AT07 custody witness (16-key closed identity map)."""

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


def build_model_rule(source: Any) -> PositionedSubjectPossibilityModelRule:
    return PositionedSubjectPossibilityModelRule(
        fixture_authority("FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL"),
        fixture_authority("FIXTURE_ONLY_WALKBACK_POLICY"),
        (source["universe"].ref,),
        (),
        (),
    )


def build_provider_case(direction: str, *, variant: str | None = None) -> dict[str, Any]:
    """Assemble one complete frozen provider case for ``direction``.

    ``variant=None`` (default) builds the canonical AT07 case that the frozen R8
    identity spine binds. ``variant="CHANGED_SOURCE_LAW"`` builds a *different
    empirical source law* through the same fixture procedure, keeping the accepted
    authority snapshots, question/risk namespaces and consumer fixture semantics
    identical so the only difference is the empirical response law itself.
    """

    if variant is None:
        source_kwargs: dict[str, Any] = {}
    elif variant == CHANGED_SOURCE_VARIANT:
        source_kwargs = {
            "tag": "c1-at07-changed",
            "rows": changed_source_rows(),
            "scope_query_authority_to_universe": True,
        }
    else:
        raise ValueError(f"unknown N10E fixture variant: {variant!r}")

    with frozen_at07_source(**source_kwargs) as (source, query_auth, registry):
        predicate, producer_query = build_producer(source, query_auth, direction)
        consumer_query, binding = build_consumer(source, direction)
        witness = build_witness(
            source, direction, consumer_query, binding, producer_query, predicate
        )
        model_rule = build_model_rule(source)
        return {
            "direction": direction,
            "variant": variant,
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


__all__ = [
    "ROOT",
    "R2",
    "R3",
    "R8",
    "R2_RELATION",
    "R2_AUTHORITIES",
    "R3_AUTHORITY",
    "R8_SPINE",
    "FROZEN_ORACLE",
    "FROZEN_CHANGED_ORACLE",
    "CHANGED_SOURCE_VARIANT",
    "CHANGED_SOURCE_EXTRA_ROWS",
    "changed_source_rows",
    "N10E_EXACT_ALLOWED_CONSUMER_STATES",
    "load_json",
    "frozen_spine",
    "at07_rows",
    "fixture_authority",
    "frozen_at07_source",
    "frozen_changed_source_query_authority",
    "build_producer",
    "build_consumer",
    "build_witness",
    "build_model_rule",
    "build_provider_case",
]
