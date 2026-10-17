"""Synthetic fixtures for C1-02 higher-order / joint / recursive analytical composition (AT08-AT13).

These helpers deliberately reuse the I03/I05/MX01R2 owners; they only build the
witness/query material needed to drive the C1 composition seam.
"""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_analytical_composition import ConditionValueBindingWitness
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
)


WITNESS_KIND = "C1_CONDITION_VALUE_BINDING_WITNESS@2"
BINDING_MODE = "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE"


def _ref(kind: str, namespace: str, material: object) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:c1-02:{namespace}:sha256:{digest}", digest)


def make_pairing_authority(tag: str = "c1-02") -> AuthorityRef:
    material = {
        "schema": "C1_SYNTHETIC_PAIRING_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_CONDITION_VALUE_PAIRING",
    }
    digest = semantic_hash(material)
    return AuthorityRef(
        authority_id=f"urn:test:c1-02:pairing-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
    )


def make_model_rule(source_universe_ref: ExactRef, tag: str = "c1-02") -> PositionedSubjectPossibilityModelRule:
    model_material = {
        "schema": "C1_SYNTHETIC_MODEL_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL",
    }
    walkback_material = {
        "schema": "C1_SYNTHETIC_WALKBACK_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_WALKBACK_POLICY",
    }
    model_digest = semantic_hash(model_material)
    walkback_digest = semantic_hash(walkback_material)
    model = AuthorityRef(
        authority_id=f"urn:test:c1-02:model-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=model_digest,
    )
    walkback = AuthorityRef(
        authority_id=f"urn:test:c1-02:walkback-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=walkback_digest,
    )
    return PositionedSubjectPossibilityModelRule(
        model_authority_ref=model,
        walkback_authority_ref=walkback,
        source_universe_refs=(source_universe_ref,),
        walkback_steps=(),
        positive_proxy_authority_refs=(),
    )


def make_multi_conditioner_consumer_query(
    *,
    query_id: str,
    subject_ref: ExactRef,
    target_ref: ExactRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    bindings: list[ConditionerBinding],
    projection_kind: str,
    projection_payload: dict | None = None,
) -> PositionedSubjectPossibilityQuery:
    if projection_payload is None:
        projection_payload = {}
    return PositionedSubjectPossibilityQuery(
        query_id=query_id,
        subject_ref=subject_ref,
        target_ref=target_ref,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        conditioner_bindings=tuple(bindings),
        requested_projection={"kind": projection_kind, **projection_payload},
    )


def make_conditioner_binding(
    *,
    binding_id: str,
    subject_fact_ref: ExactRef,
    empirical_coordinate_ref: ExactRef,
    comparability_authority_ref: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    effective_time_or_interval: object = None,
) -> ConditionerBinding:
    return ConditionerBinding(
        binding_id=binding_id,
        subject_fact_ref=subject_fact_ref,
        empirical_coordinate_ref=empirical_coordinate_ref,
        comparability_authority_ref=comparability_authority_ref,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        effective_time_or_interval=effective_time_or_interval,
    )


def _subject_material(binding_id: str, coordinate_ref: ExactRef, exact_value: object) -> dict:
    # Keep material minimal and stable; binding_id is intentionally not part of the
    # preimage so callers can construct matching subject_fact_refs independently.
    return {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "empirical_semantic_ref": coordinate_ref.as_dict(),
        "exact_value": str(exact_value),
    }


def _leaf_projection(leaf_id: str, coordinate_ref: ExactRef, exact_value: object, *, leaf_type: str = "SURVEY_RESPONSE_EVENT") -> dict:
    projection = {
        "schema": "C1_CONDITION_VALUE_LEAF_PROJECTION@1",
        "leaf_id": leaf_id,
        "leaf_type": leaf_type,
        "operator": "EQ",
        "exact_value": str(exact_value),
    }
    # Governed empirical-position coordinates key their semantic ref differently
    # from survey-response leaves; the owner matches on the per-leaf-type key.
    if leaf_type == "EMPIRICAL_POSITION_COORDINATE":
        projection["coordinate_semantic_ref"] = coordinate_ref.as_dict()
    else:
        projection["question_semantic_ref"] = coordinate_ref.as_dict()
    return projection


def _pairing_material(
    subject_ref: ExactRef,
    leaf_ref: ExactRef,
    coordinate_ref: ExactRef,
    exact_value: object,
) -> dict:
    return {
        "schema": "C1_CONDITION_VALUE_PAIRING_GROUND_TRUTH@1",
        "subject_preimage_ref": subject_ref.as_dict(),
        "predicate_leaf_preimage_ref": leaf_ref.as_dict(),
        "required_semantic_ref": coordinate_ref.as_dict(),
        "required_exact_value": str(exact_value),
    }


def make_multi_conditioner_witness(
    *,
    witness_object_id: str,
    consumer_query: PositionedSubjectPossibilityQuery,
    producer_query: EmpiricalQuerySpec,
    producer_predicate: EmpiricalPredicate,
    bindings: list[ConditionerBinding],
    subject_materials: list[dict],
    leaf_projections: list[dict],
    pairing_materials: list[dict],
    pairing_authority: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    subject_preimage_refs: list[ExactRef] | None = None,
) -> ConditionValueBindingWitness:
    """Build a C1-02 multi-conditioner witness.

    The caller must supply one subject material, leaf projection and pairing
    material per binding, in the same order as ``bindings``.
    """
    if not (len(bindings) == len(subject_materials) == len(leaf_projections) == len(pairing_materials)):
        raise ValueError("binding and witness material counts must match")

    if subject_preimage_refs is None:
        subject_preimage_refs = []
        for i, subject in enumerate(subject_materials):
            subject_preimage_refs.append(_ref("C1_SYNTHETIC_POSITIONED_SUBJECT@1", f"subject-{i}", subject))
    producer_leaf_refs = []
    pairing_refs = []
    for i, (leaf, pair) in enumerate(zip(leaf_projections, pairing_materials)):
        producer_leaf_refs.append(_ref("C1_CONDITION_VALUE_LEAF_PROJECTION@1", f"leaf-{i}", leaf))
        pairing_refs.append(_ref("C1_CONDITION_VALUE_PAIRING_GROUND_TRUTH@1", f"pair-{i}", pair))

    identity_material = {
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_binding_materials": [b.material() for b in bindings],
        "consumer_binding_fingerprint": semantic_hash([b.material() for b in bindings]),
        "producer_query_ref": producer_query.ref.as_dict(),
        "producer_predicate_ref": producer_predicate.ref.as_dict(),
        "producer_predicate_hash": producer_predicate.predicate_hash,
        "producer_predicate_leaf_refs": [ref.as_dict() for ref in producer_leaf_refs],
        "producer_predicate_leaf_projections": leaf_projections,
        "pairing_ground_truth_refs": [ref.as_dict() for ref in pairing_refs],
        "pairing_ground_truth_materials": pairing_materials,
        "pairing_authority_refs": [pairing_authority.as_dict()] * len(bindings),
        "source_universe_ref": source_universe_ref.as_dict(),
        "release_ref": release_ref.as_dict(),
        "effective_time_or_intervals": [b.effective_time_or_interval for b in bindings],
        "binding_mode": BINDING_MODE,
    }
    witness_ref = ExactRef(WITNESS_KIND, witness_object_id, semantic_hash(identity_material))
    return ConditionValueBindingWitness(
        witness_ref=witness_ref,
        identity_material=identity_material,
        subject_condition_preimage_refs=tuple(subject_preimage_refs),
        subject_condition_preimage_materials=tuple(subject_materials),
        producer_predicate_leaf_refs=tuple(producer_leaf_refs),
        producer_predicate_leaf_projections=tuple(leaf_projections),
        pairing_ground_truth_refs=tuple(pairing_refs),
        pairing_ground_truth_materials=tuple(pairing_materials),
        pairing_authority_refs=tuple([pairing_authority] * len(bindings)),
    )


def build_witness_for_binding(
    *,
    witness_object_id: str,
    consumer_query: PositionedSubjectPossibilityQuery,
    producer_query: EmpiricalQuerySpec,
    producer_predicate: EmpiricalPredicate,
    bindings: list[ConditionerBinding],
    coordinate_value_pairs: list[tuple[ExactRef, object]],
    pairing_authority: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    leaf_type: str = "SURVEY_RESPONSE_EVENT",
) -> ConditionValueBindingWitness:
    """Convenience builder when each binding is a simple EQ value.

    Uses each binding's own ``subject_fact_ref`` as the frozen subject preimage,
    so the witness matches the consumer query exactly. ``leaf_type`` selects the
    owner-native leaf kind of the producer condition (``SURVEY_RESPONSE_EVENT``
    for response conditioners, ``EMPIRICAL_POSITION_COORDINATE`` for governed
    position-coordinate conditioners).
    """
    subject_materials = []
    leaf_projections = []
    pairing_materials = []
    subject_preimage_refs = []
    for i, (binding, (coordinate_ref, value)) in enumerate(zip(bindings, coordinate_value_pairs)):
        subject = _subject_material(binding.binding_id, coordinate_ref, value)
        leaf = _leaf_projection(binding.binding_id, coordinate_ref, value, leaf_type=leaf_type)
        leaf_ref = _ref("C1_CONDITION_VALUE_LEAF_PROJECTION@1", f"leaf-{i}", leaf)
        pair = _pairing_material(
            binding.subject_fact_ref,
            leaf_ref,
            coordinate_ref,
            value,
        )
        subject_materials.append(subject)
        leaf_projections.append(leaf)
        pairing_materials.append(pair)
        subject_preimage_refs.append(binding.subject_fact_ref)
    return make_multi_conditioner_witness(
        witness_object_id=witness_object_id,
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=producer_predicate,
        bindings=bindings,
        subject_materials=subject_materials,
        leaf_projections=leaf_projections,
        pairing_materials=pairing_materials,
        pairing_authority=pairing_authority,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        subject_preimage_refs=subject_preimage_refs,
    )


def readdress_witness_with_false_pairing(
    witness,
    *,
    conditioner_index: int = 0,
    false_semantic_ref=None,
    false_exact_value=None,
    witness_object_id: str | None = None,
):
    """Return a fully self-consistent witness whose pairing relation is a LIE.

    This is the hostile constructor for the witness pairing-ground-truth law. It
    deliberately does NOT corrupt any hash or ref. Instead it mutates only the
    *semantics* of one pairing-ground-truth relation -- naming a different
    required semantic ref and/or a different required exact value than the real
    relation -- and then re-content-addresses everything that depends on that
    mutation:

      * the mutated pairing material's own ref is recomputed as
        sha256(canonical_json(mutated_material));
      * the witness identity material is rebuilt with the new pairing ref and
        material;
      * the witness ref is recomputed as sha256(canonical_json(new_identity)).

    The result therefore satisfies every structural, count and hash-integrity
    check the owner performs, while still contradicting the unchanged consumer
    binding, subject preimage and producer-leaf truth. Only a genuine semantic
    comparison can reject it.
    """
    if (false_semantic_ref is None) == (false_exact_value is None):
        raise ValueError("supply exactly one of false_semantic_ref / false_exact_value")

    pairing_materials = [dict(m) for m in witness.pairing_ground_truth_materials]
    pairing_refs = list(witness.pairing_ground_truth_refs)

    mutated = dict(pairing_materials[conditioner_index])
    if false_semantic_ref is not None:
        mutated["required_semantic_ref"] = (
            false_semantic_ref.as_dict()
            if isinstance(false_semantic_ref, ExactRef)
            else false_semantic_ref
        )
    if false_exact_value is not None:
        mutated["required_exact_value"] = str(false_exact_value)
    pairing_materials[conditioner_index] = mutated

    # Re-content-address the mutated pairing preimage.
    pairing_refs[conditioner_index] = ExactRef(
        pairing_refs[conditioner_index].kind,
        pairing_refs[conditioner_index].object_id,
        semantic_hash(mutated),
    )

    identity_material = dict(witness.identity_material)
    identity_material["pairing_ground_truth_refs"] = [ref.as_dict() for ref in pairing_refs]
    identity_material["pairing_ground_truth_materials"] = pairing_materials

    witness_ref = ExactRef(
        witness.witness_ref.kind,
        witness_object_id or witness.witness_ref.object_id,
        semantic_hash(identity_material),
    )
    return ConditionValueBindingWitness(
        witness_ref=witness_ref,
        identity_material=identity_material,
        subject_condition_preimage_refs=witness.subject_condition_preimage_refs,
        subject_condition_preimage_materials=witness.subject_condition_preimage_materials,
        producer_predicate_leaf_refs=witness.producer_predicate_leaf_refs,
        producer_predicate_leaf_projections=witness.producer_predicate_leaf_projections,
        pairing_ground_truth_refs=tuple(pairing_refs),
        pairing_ground_truth_materials=tuple(pairing_materials),
        pairing_authority_refs=witness.pairing_authority_refs,
    )


__all__ = [
    "make_pairing_authority",
    "make_model_rule",
    "make_multi_conditioner_consumer_query",
    "make_conditioner_binding",
    "make_multi_conditioner_witness",
    "build_witness_for_binding",
    "subject_fact_ref",
    "attitude_fixture",
    "ATTITUDE_ORACLE",
    "xor_fixture",
    "XOR_ORACLE",
    "equal_marginals_fixtures",
    "EQUAL_MARGINALS_ORACLE",
    "minority_fixture",
    "MINORITY_ORACLE",
    "cotravel_fixture",
    "COTRAVEL_ORACLE",
    "ranked_fixture",
    "RANKED_ORACLE",
    "with_target_domains",
    "readdress_witness_with_false_pairing",
    "direct_condition_composition",
    "WITNESS_KIND",
    "BINDING_MODE",
]


# ---------------------------------------------------------------------------
# Subject-fact helper
# ---------------------------------------------------------------------------


def subject_fact_ref(source, question, value) -> dict:
    """Frozen synthetic subject-condition preimage ref for one exact coordinate value."""
    refs = source.get("crefs", {})
    semantic_ref = source["qrefs"].get(question) or refs.get(question)
    if semantic_ref is None:
        raise KeyError(f"unknown coordinate {question!r}")
    material = {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "empirical_semantic_ref": semantic_ref.as_dict(),
        "exact_value": str(value),
    }
    return ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:c1-02:subject-fact:{question}:{value}",
        semantic_hash(material),
    ).as_dict()


# ---------------------------------------------------------------------------
# AT08 - attitude/value conditioning onto a different attitude target
# ---------------------------------------------------------------------------

# Frozen 100-respondent table. Hand-derived before any candidate output.
#
#                ATT2=support  ATT2=oppose   row total
#   ATT1=agree           54            6           60
#   ATT1=disagree         8           32           40
#   column total         62           38          100
ATTITUDE_ORACLE = {
    "denominator_when_agree": 60,
    "denominator_when_disagree": 40,
    "P(support | agree)": (54, 60),
    "P(oppose | agree)": (6, 60),
    "P(support | disagree)": (8, 40),
    "P(oppose | disagree)": (32, 40),
    "marginal_support": 62,
    "marginal_oppose": 38,
}


def attitude_fixture(tag: str = "c1-at08-attitude"):
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    rows = (
        [{"id": f"AG{i:03d}", "responses": {"ATT1": "agree", "ATT2": "support"}} for i in range(54)]
        + [{"id": f"AO{i:03d}", "responses": {"ATT1": "agree", "ATT2": "oppose"}} for i in range(6)]
        + [{"id": f"DS{i:03d}", "responses": {"ATT1": "disagree", "ATT2": "support"}} for i in range(8)]
        + [{"id": f"DO{i:03d}", "responses": {"ATT1": "disagree", "ATT2": "oppose"}} for i in range(32)]
    )
    return _build_source(tag, rows)


# ---------------------------------------------------------------------------
# AT09 - XOR: unary marginals flat, joint configuration decisive
# ---------------------------------------------------------------------------

# Frozen 4-respondent table with C = A xor B. Hand-derived before any output.
#
#   A  B  C
#   0  0  0
#   0  1  1
#   1  0  1
#   1  1  0
#
# Unary marginals:  P(C=1) = 1/2
#                   P(C=1|A=0) = 1/2   <-- flat
#                   P(C=1|A=1) = 1/2   <-- flat
#                   P(C=1|B=0) = 1/2   <-- flat
#                   P(C=1|B=1) = 1/2   <-- flat
# Joint:            P(C=1|A=0,B=0) = 0
#                   P(C=1|A=0,B=1) = 1
#                   P(C=1|A=1,B=0) = 1
#                   P(C=1|A=1,B=1) = 0
XOR_ORACLE = {
    "denominator": 4,
    "unary_marginal_flat": {
        "P(C=1)": (2, 4),
        "P(C=1|A=0)": (1, 2),
        "P(C=1|A=1)": (1, 2),
        "P(C=1|B=0)": (1, 2),
        "P(C=1|B=1)": (1, 2),
    },
    "joint_decisive": {
        "P(C=1|A=0,B=0)": (0, 1),
        "P(C=1|A=0,B=1)": (1, 1),
        "P(C=1|A=1,B=0)": (1, 1),
        "P(C=1|A=1,B=1)": (0, 1),
    },
    "joint_support": {"0,1": 1, "1,0": 1},
    "joint_zero_support": {"0,0": 1, "1,1": 1},
}


def xor_fixture(tag: str = "c1-at09-xor"):
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    rows = [
        {"id": f"R{a}{b}", "responses": {"A": a, "B": b, "C": a ^ b}}
        for a in (0, 1)
        for b in (0, 1)
    ]
    return _build_source(tag, rows)


# Equal univariate marginals over A and B (each 2/4 ones), different joint pairing.
EQUAL_MARGINALS_ORACLE = {
    "denominator": 4,
    "shared_marginals": {"P(A=1)": (2, 4), "P(B=1)": (2, 4)},
    "left_joint": {"0,0": 2, "1,1": 2, "0,1": 0, "1,0": 0},
    "right_joint": {"0,1": 2, "1,0": 2, "0,0": 0, "1,1": 0},
    "left_member_ids": ("L1", "L2", "L3", "L4"),
    "right_member_ids": ("M1", "M2", "M3", "M4"),
}


def equal_marginals_fixtures(question_namespace: str = "c1-at09-shared"):
    """Two single-universe sources with identical A/B marginals but different joint.

    Each source is independently composable (one universe / one release each), so
    the equal-marginal/different-joint distinction does not require multi-universe
    consumption authority.
    """
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    left = _build_source(
        "c1-at09-joint-left",
        [
            {"id": "L1", "responses": {"A": 0, "B": 0}},
            {"id": "L2", "responses": {"A": 0, "B": 0}},
            {"id": "L3", "responses": {"A": 1, "B": 1}},
            {"id": "L4", "responses": {"A": 1, "B": 1}},
        ],
        question_namespace=question_namespace,
        risk_namespace=question_namespace,
    )
    right = _build_source(
        "c1-at09-joint-right",
        [
            {"id": "M1", "responses": {"A": 0, "B": 1}},
            {"id": "M2", "responses": {"A": 0, "B": 1}},
            {"id": "M3", "responses": {"A": 1, "B": 0}},
            {"id": "M4", "responses": {"A": 1, "B": 0}},
        ],
        question_namespace=question_namespace,
        risk_namespace=question_namespace,
    )
    return left, right


# ---------------------------------------------------------------------------
# AT10 - modal majority plus a supported minority/counterpattern branch
# ---------------------------------------------------------------------------

# Frozen table. G=A is modal (10), G=B is minority (8), G=C is counterpattern (2).
# Every group has Y=1 support at a distinct rate, so all three are supported and
# none is the product of the pooled marginal.
MINORITY_ORACLE = {
    "group_sizes": {"A": 10, "B": 8, "C": 2},
    "total": 20,
    "support_counts": {"A": 3, "B": 8, "C": 2},
    "counterpattern_supported": True,
    "minority_supported": True,
    "modal_supported": True,
}


def minority_fixture(tag: str = "c1-at10-minority"):
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    rows = []
    for i in range(3):
        rows.append({"id": f"MA{i}", "responses": {"Y": 1}, "coords": {"G": "A"}})
    for i in range(7):
        rows.append({"id": f"NA{i}", "responses": {"Y": 0}, "coords": {"G": "A"}})
    for i in range(8):
        rows.append({"id": f"MB{i}", "responses": {"Y": 1}, "coords": {"G": "B"}})
    for i in range(2):
        rows.append({"id": f"CB{i}", "responses": {"Y": 1}, "coords": {"G": "C"}})
    return _build_source(tag, rows)


# ---------------------------------------------------------------------------
# AT12 - empirical co-travel with no semantic-relation authority present
# ---------------------------------------------------------------------------

# R1,R2 travel with X=1 and Y=1; R3 travels with X=1 and Y=0; R4 has X=0,Y=1.
# Conditioning on X=1 therefore yields an exact same-respondent co-travel cohort
# of 3 with Y=1 for 2 and Y=0 for 1.
COTRAVEL_ORACLE = {
    "denominator_when_x1": 3,
    "member_ids": ("R1", "R2", "R3"),
    "Y1": 2,
    "Y0": 1,
    "P(Y=1|X=1)": (2, 3),
    "excluded_by_cohort": ("R4",),
}


def cotravel_fixture(tag: str = "c1-at12-cotravel"):
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    rows = [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "Y": 1}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}},
        {"id": "R4", "responses": {"X": 0, "Y": 1}},
    ]
    return _build_source(tag, rows)


# ---------------------------------------------------------------------------
# AT13 - genuinely non-scalar RANKED_RESPONSE target
# ---------------------------------------------------------------------------

# Each respondent holds one scalar ATT conditioner event and two ranked events.
# Rank is carried by the source-native "rank" order field, so the ordered value
# vector is ["HIGH","LOW"] for the modal cohort and ["LOW","HIGH"] for the
# re-identified cohort. Arity is 1 but the cell value is a non-scalar vector.
RANKED_ORACLE = {
    "topology": "RANKED_RESPONSE",
    "arity": 1,
    "denominator": 3,
    "source_native_order_must_survive": True,
    "modal_value_vector": ["HIGH", "LOW"],
    "reidentified_value_vector": ["LOW", "HIGH"],
    "scalarization_forbidden": True,
}


def ranked_fixture(tag: str = "c1-at13-ranked", reverse_rank: bool = False):
    """Non-scalar RANKED_RESPONSE source with a scalar conditioner question."""
    from rawlsing_next.tests.pre553_query_frontier_fixtures import _build_event_source

    first, second = ("HIGH", "LOW") if not reverse_rank else ("LOW", "HIGH")
    rows = [
        {
            "id": f"S{i}",
            "events": {
                # _build_event_source stores raw_response_value verbatim, and the
                # shared leaf builder canonicalizes the exact value to str, so the
                # conditioner value is declared as a string here.
                "ATT": ({"value": "1", "event_id": f"ATT-{i}", "order_fields": {"semantic_ordinal": 0}},),
                "RANK": (
                    {"value": first, "event_id": f"R1-{i}", "order_fields": {"rank": 1}},
                    {"value": second, "event_id": f"R2-{i}", "order_fields": {"rank": 2}},
                ),
            },
        }
        for i in range(3)
    ]
    return _build_event_source(tag, rows, {"ATT": "SCALAR_SINGULAR", "RANK": "RANKED_RESPONSE"})


def with_target_domains(query, domains):
    """Rebuild an EmpiricalQuerySpec with explicit per-target declared domains.

    The shared test helper ``_query`` hard-codes a ``["0", "1"]`` domain, which is
    correct for binary integer fixtures but wrong for string-valued attitude
    questions and for ordered value vectors.
    """
    from rawlsing_next.tests.test_pre553_empirical_query import _ref

    if isinstance(domains[0], str):
        domains = [domains]
    components = [dict(component) for component in query.target_arity_and_topology["components"]]
    for component, domain in zip(components, domains):
        component["domain"] = list(domain)
        component["target_domain_replay_ref"] = _ref(
            "TARGET_DOMAIN", "-".join(str(value) for value in domain)
        )
    return EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        target_refs=query.target_refs,
        target_arity_and_topology={
            "arity": query.target_arity_and_topology["arity"],
            "joint_order_semantics": query.target_arity_and_topology["joint_order_semantics"],
            "components": components,
        },
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=query.scope_refs,
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=query.requested_output_grain,
        query_authority_refs=query.query_authority_refs,
    )


def with_components(query, components):
    """Rebuild an EmpiricalQuerySpec with caller-supplied component material.

    ``EmpiricalQuerySpec`` is an immutable semantic object rather than a dataclass,
    so hostile component mutations must be expressed as an explicit rebuild.
    """
    return EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        target_refs=query.target_refs,
        target_arity_and_topology={
            "arity": query.target_arity_and_topology["arity"],
            "joint_order_semantics": query.target_arity_and_topology["joint_order_semantics"],
            "components": [dict(component) for component in components],
        },
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=query.scope_refs,
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=query.requested_output_grain,
        query_authority_refs=query.query_authority_refs,
    )


# ---------------------------------------------------------------------------
# Shared direct-composition driver
# ---------------------------------------------------------------------------


def direct_condition_composition(
    *,
    source,
    qauth,
    registry,
    conditions,
    target_question,
    tag,
    binding_ids=None,
    target_domain=None,
    measure="RAW",
    risk="R",
    producer_query=None,
    release_refs=None,
    consumer_universe_ref=None,
    consumer_release_ref=None,
):
    """Drive one DIRECT_I03 composition from an explicit condition list.

    ``conditions`` is a sequence of ``(kind, question, value)`` where kind is
    ``"RESPONSE"`` or ``"COORDINATE"``. The AND of those atoms is the producer
    predicate, and each atom becomes one consumer conditioner binding carrying
    its exact value.

    The producer query is always built from the predicate this helper constructs,
    so ``query.condition_predicate_ref`` cannot drift from the supplied predicate.
    ``target_domain`` declares the exact cell domain when the target is not
    ``["0", "1"]``.
    """
    from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _branch_predicate,
        _coordinate_leaf,
        _predicate,
        _query,
        _response_leaf,
    )

    leaves = []
    for kind, question, value in conditions:
        if kind == "RESPONSE":
            leaves.append(_response_leaf(source, qauth, question, value))
        elif kind == "COORDINATE":
            leaves.append(_coordinate_leaf(source, question, value))
        else:
            raise ValueError(f"unsupported condition kind {kind!r}")

    if not conditions:
        predicate = _branch_predicate(source, qauth, tag=f"{tag}-branch")
    elif len(leaves) == 1:
        predicate = _predicate(source, qauth, leaves[0], tag=f"{tag}-predicate")
    else:
        predicate = _predicate(
            source, qauth, {"op": "AND", "children": list(leaves)}, tag=f"{tag}-predicate"
        )

    if producer_query is None:
        producer_query = _query(
            source,
            qauth,
            predicate,
            (target_question,),
            risk=risk,
            measure=measure,
            tag=f"{tag}-query",
        )
        if target_domain is not None:
            producer_query = with_target_domains(producer_query, target_domain)

    pairing = make_pairing_authority(tag)
    leaf_types = {
        "RESPONSE": "SURVEY_RESPONSE_EVENT",
        "COORDINATE": "EMPIRICAL_POSITION_COORDINATE",
    }
    if len({leaf_types[kind] for kind, _, _ in conditions}) > 1:
        raise ValueError("direct_condition_composition requires one uniform conditioner leaf kind")
    leaf_type = leaf_types[conditions[0][0]] if conditions else "SURVEY_RESPONSE_EVENT"
    ids = list(binding_ids) if binding_ids else [f"c{i}" for i in range(len(conditions))]
    bindings = []
    pairs = []
    for binding_id, (kind, question, value) in zip(ids, conditions):
        coordinate_ref = source["qrefs"][question] if kind == "RESPONSE" else source["crefs"][question]
        bindings.append(
            make_conditioner_binding(
                binding_id=binding_id,
                subject_fact_ref=ExactRef(**subject_fact_ref(source, question, value)),
                empirical_coordinate_ref=coordinate_ref,
                comparability_authority_ref=pairing,
                source_universe_ref=source["universe"].ref,
                release_ref=source["release_ref"],
            )
        )
        pairs.append((coordinate_ref, value))

    consumer_query = make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:c1-02:{tag}:subject",
            semantic_hash({"fixture_id": tag}),
        ),
        target_ref=source["qrefs"][target_question],
        source_universe_ref=consumer_universe_ref or source["universe"].ref,
        release_ref=consumer_release_ref or source["release_ref"],
        bindings=bindings,
        projection_kind=f"C1_{tag}_CONDITIONAL_DISTRIBUTION",
    )
    witness = build_witness_for_binding(
        witness_object_id=f"urn:test:c1-02:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=bindings,
        coordinate_value_pairs=pairs,
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        leaf_type=leaf_type,
    )
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=release_refs if release_refs is not None else (source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=make_model_rule(source["universe"].ref, tag),
        condition_binding_witness=witness,
    )
    return result, consumer_query, witness, producer_query, predicate