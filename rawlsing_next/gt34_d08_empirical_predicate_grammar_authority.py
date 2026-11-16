"""OBL057 candidate: exact D08 EmpiricalPredicate grammar authority binding only.

This module constitutes one candidate authority identity.  It does not adopt that
identity as project-current and it does not create coordinates, respondents,
actors, events, comparators, PSEPF, V3 effects, or topology.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

AUTHORITY_ID = "GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_AUTHORITY"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_KIND = "PREDICATE_GRAMMAR"
GOVERNED_OBJECT_FAMILY = "EmpiricalPredicate@1.0.0"
GOVERNED_OPERATION = "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE"
PREDICATE_LEAF_TYPE = "EMPIRICAL_POSITION_COORDINATE"
COMPARISON_OPERATOR = "EQ"
CANDIDATE_NOT_ADOPTED = "CANDIDATE_NOT_ADOPTED"
CURRENT_ACCEPTED = "CURRENT_ACCEPTED"

AUTHORITY_CEILING = (
    "NO_Q69B_COORDINATE_SEMANTICS",
    "NO_RESPONDENT_INCIDENCE",
    "NO_ACTOR_SEMANTICS",
    "NO_OBL048_SUBJECT_CLASSIFICATION",
    "NO_ADP010_EVENT_SEMANTICS",
    "NO_COMPARATOR_MAPPING_SEMANTICS",
    "NO_SOURCE_PORTABILITY_OR_POOLING",
    "NO_PSEPF",
    "NO_V3_MUTATION",
    "NO_ARCHITECTURE_OR_TOPOLOGY",
)

_COORDINATE_SEMANTICS_MATERIAL = {
    "semantic_id": "D08_EMPIRICAL_POSITION_COORDINATE@1.0.0",
    "predicate_atom": PREDICATE_LEAF_TYPE,
    "ontology": "EMPIRICAL_SURVEY_COORDINATE",
    "meaning": (
        "A typed predicate leaf over one separately authorized respondent-linked empirical "
        "coordinate; it does not create coordinate semantics, actor position, actor identity, "
        "actor state, or structural interpretation."
    ),
    "operand_requirement": "EXACT_SEPARATELY_AUTHORIZED_EMPIRICAL_COORDINATE_AND_CANONICAL_VALUE",
}
COORDINATE_SEMANTICS_REF = ExactRef(
    "PREDICATE_OPERATOR_SEMANTICS",
    "D08_EMPIRICAL_POSITION_COORDINATE@1.0.0",
    semantic_hash(_COORDINATE_SEMANTICS_MATERIAL),
)

_EQ_SEMANTICS_MATERIAL = {
    "semantic_id": "D08_EMPIRICAL_POSITION_COORDINATE_EQ@1.0.0",
    "operator": COMPARISON_OPERATOR,
    "lhs_type": PREDICATE_LEAF_TYPE,
    "rhs_type": "CANONICAL_COORDINATE_VALUE",
    "meaning": (
        "True exactly when the governed empirical coordinate value equals the separately "
        "governed canonical value under the exact coordinate authority; no fuzzy, label, "
        "nearest, embedding, narrative, or cross-ontology equivalence."
    ),
    "ast_contract": {
        "op": "LEAF",
        "leaf_type": PREDICATE_LEAF_TYPE,
        "comparison_operator": COMPARISON_OPERATOR,
    },
}
EQ_SEMANTICS_REF = ExactRef(
    "PREDICATE_OPERATOR_SEMANTICS",
    "D08_EMPIRICAL_POSITION_COORDINATE_EQ@1.0.0",
    semantic_hash(_EQ_SEMANTICS_MATERIAL),
)
OPERATOR_SEMANTICS_REFS = (COORDINATE_SEMANTICS_REF, EQ_SEMANTICS_REF)

_OWNER_JURISDICTION_MATERIAL = {
    "owner": "VOZHD_HQ_PRE_MAIN",
    "jurisdiction": "GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_ONLY",
    "authority_to_adopt": "PROJECT_CURRENT_EFFECT_RESERVED_TO_VOZHD_HQ",
}
OWNER_JURISDICTION_REF = ExactRef(
    "OWNER_JURISDICTION",
    "VOZHD_HQ_PRE_MAIN:GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_ONLY",
    semantic_hash(_OWNER_JURISDICTION_MATERIAL),
)

HISTORICAL_D08_REF = ExactRef(
    "GIT_COMMIT",
    "maidiu/rawlsing@db03fcbcb5e34c28b486070628377ead0408e13a",
    semantic_hash({
        "repository": "maidiu/rawlsing",
        "commit": "db03fcbcb5e34c28b486070628377ead0408e13a",
    }),
)
PRE553_RUNTIME_CONTRACT_REF = ExactRef(
    "GIT_PATH_AT_COMMIT",
    (
        "maidiu/rawlsing@eba17fadb00492a08bfcf6163b60d09158fbb583:"
        "rawlsing_next/pre553_empirical_objects.py"
    ),
    semantic_hash({
        "repository": "maidiu/rawlsing",
        "commit": "eba17fadb00492a08bfcf6163b60d09158fbb583",
        "path": "rawlsing_next/pre553_empirical_objects.py",
    }),
)
HQ_OBL057_COMMISSION_REF = ExactRef(
    "GIT_PATH_AT_COMMIT",
    (
        "maidiu/rawlsing@72825f7086c6c397b6c16df6666b2a426aab9295:"
        "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
        "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
        "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
        "GT34_POST_TRANSFER_DUAL_LANE_HQ_ADJUDICATION_R1/"
        "01_SUB_VOZHD_A_OBL057_CONTINUATION.md"
    ),
    semantic_hash({
        "repository": "maidiu/rawlsing",
        "commit": "72825f7086c6c397b6c16df6666b2a426aab9295",
        "path": (
            "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
            "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
            "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
            "GT34_POST_TRANSFER_DUAL_LANE_HQ_ADJUDICATION_R1/"
            "01_SUB_VOZHD_A_OBL057_CONTINUATION.md"
        ),
    }),
)
IMMUTABLE_PROVENANCE_REFS = (
    HISTORICAL_D08_REF,
    PRE553_RUNTIME_CONTRACT_REF,
    HQ_OBL057_COMMISSION_REF,
)

AUTHORITY_MATERIAL = {
    "authority_id": AUTHORITY_ID,
    "authority_version": AUTHORITY_VERSION,
    "authority_kind": AUTHORITY_KIND,
    "governed_object_families": [GOVERNED_OBJECT_FAMILY],
    "governed_operations": [GOVERNED_OPERATION],
    "predicate_leaf_type": PREDICATE_LEAF_TYPE,
    "comparison_operator": COMPARISON_OPERATOR,
    "operator_semantics_refs": [ref.as_dict() for ref in OPERATOR_SEMANTICS_REFS],
    "owner_jurisdiction_ref": OWNER_JURISDICTION_REF.as_dict(),
    "historical_semantic_court_commit": "db03fcbcb5e34c28b486070628377ead0408e13a",
    "runtime_contract": "PRE553_EXACT_AUTHORITY_REF_ID_VERSION_CONTENT_HASH",
    "adoption_contract": (
        "NO_RUNTIME_CURRENTNESS_UNTIL_EXPLICIT_VOZHD_HQ_ADOPTION_OF_THIS_EXACT_TUPLE"
    ),
    "resolution_contract": "EXACT_TUPLE_ONLY__NO_LATEST_DEFAULT_FUZZY_FALLBACK",
    "status": CANDIDATE_NOT_ADOPTED,
    "authority_ceiling": list(AUTHORITY_CEILING),
    "immutable_provenance_refs": [ref.as_dict() for ref in IMMUTABLE_PROVENANCE_REFS],
}
AUTHORITY_CONTENT_HASH = semantic_hash(AUTHORITY_MATERIAL)
AUTHORITY_REF = AuthorityRef(AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH)


class GrammarAuthorityError(ValueError):
    """Base OBL057 exact-authority failure."""


class GrammarAuthorityIntegrityError(GrammarAuthorityError):
    """The supplied authority tuple or semantic refs drifted."""


class GrammarAuthorityNotCurrent(GrammarAuthorityError):
    """No exact HQ-adopted current selection was supplied."""


@dataclass(frozen=True, slots=True)
class RuntimeGrammarBinding:
    authority_ref: AuthorityRef
    authority_kind: str
    governed_operation: str
    governed_object_family: str
    operator_semantics_refs: tuple[ExactRef, ...]
    owner_jurisdiction_ref: ExactRef
    currentness: str
    adoption_current_selection_evidence_refs: tuple[ExactRef, ...]
    immutable_provenance_refs: tuple[ExactRef, ...]


def candidate_definition() -> dict:
    """Return detached exact candidate material; never a current-selection claim."""
    return {
        **AUTHORITY_MATERIAL,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "authority_ref": AUTHORITY_REF.as_dict(),
    }


def validate_predicate_ast_shape(predicate_ast: dict) -> None:
    """Validate only the D08 leaf/operator grammar owned by this authority."""
    if not isinstance(predicate_ast, dict):
        raise GrammarAuthorityIntegrityError("predicate_ast must be a dict")
    required = {"op", "leaf_type", "coordinate_ref", "comparison_operator", "canonical_value"}
    if not required.issubset(predicate_ast):
        raise GrammarAuthorityIntegrityError("predicate_ast missing exact D08 leaf fields")
    if predicate_ast["op"] != "LEAF":
        raise GrammarAuthorityIntegrityError("only D08 LEAF is governed")
    if predicate_ast["leaf_type"] != PREDICATE_LEAF_TYPE:
        raise GrammarAuthorityIntegrityError("wrong empirical predicate leaf type")
    if predicate_ast["comparison_operator"] != COMPARISON_OPERATOR:
        raise GrammarAuthorityIntegrityError("only exact EQ is governed")
    if not isinstance(predicate_ast["coordinate_ref"], str) or not predicate_ast["coordinate_ref"]:
        raise GrammarAuthorityIntegrityError("coordinate_ref must be exact nonempty external coordinate identity")
    if predicate_ast["canonical_value"] is None:
        raise GrammarAuthorityIntegrityError("canonical_value is required")
    forbidden = {
        "actor_id", "actor_state", "actor_semantics", "respondent_incidence",
        "subject_classification", "event_semantics", "comparator_mapping",
        "source_pooling", "psepf", "v3_mutation",
    }
    if forbidden.intersection(predicate_ast):
        raise GrammarAuthorityIntegrityError("predicate AST attempts to import out-of-jurisdiction semantics")


def validate_runtime_binding(
    binding: RuntimeGrammarBinding,
    *,
    expected_adoption_current_selection_evidence_refs: Iterable[ExactRef],
) -> RuntimeGrammarBinding:
    """Validate one explicitly HQ-pinned adopted tuple; there is no resolver or fallback.

    The caller must pin the exact immutable HQ adoption/current-selection evidence
    after HQ acts.  This candidate does not issue that evidence and therefore
    cannot self-adopt.
    """
    expected_selection = tuple(expected_adoption_current_selection_evidence_refs)
    if not expected_selection:
        raise GrammarAuthorityNotCurrent("explicit HQ adoption/current-selection evidence is required")
    if binding.authority_ref != AUTHORITY_REF:
        raise GrammarAuthorityIntegrityError("authority id/version/content hash mismatch")
    if binding.authority_kind != AUTHORITY_KIND:
        raise GrammarAuthorityIntegrityError("authority kind mismatch")
    if binding.governed_operation != GOVERNED_OPERATION:
        raise GrammarAuthorityIntegrityError("governed operation mismatch")
    if binding.governed_object_family != GOVERNED_OBJECT_FAMILY:
        raise GrammarAuthorityIntegrityError("governed object family mismatch")
    if binding.operator_semantics_refs != OPERATOR_SEMANTICS_REFS:
        raise GrammarAuthorityIntegrityError("operator semantics refs mismatch")
    if binding.owner_jurisdiction_ref != OWNER_JURISDICTION_REF:
        raise GrammarAuthorityIntegrityError("owner/jurisdiction mismatch")
    if binding.currentness != CURRENT_ACCEPTED:
        raise GrammarAuthorityNotCurrent("binding is not CURRENT_ACCEPTED")
    if binding.adoption_current_selection_evidence_refs != expected_selection:
        raise GrammarAuthorityIntegrityError("adoption/current-selection evidence mismatch")
    required_provenance = set(IMMUTABLE_PROVENANCE_REFS) | set(expected_selection)
    if not required_provenance.issubset(set(binding.immutable_provenance_refs)):
        raise GrammarAuthorityIntegrityError("immutable provenance closure incomplete")
    return binding


def exact_runtime_binding(
    *,
    adoption_current_selection_evidence_refs: Iterable[ExactRef],
    immutable_provenance_refs: Iterable[ExactRef],
) -> RuntimeGrammarBinding:
    """Mechanical constructor for a post-HQ-adoption pinned binding.

    It does not issue adoption evidence.  Supplying evidence here is not itself
    an adoption; consumers must pin the exact HQ-issued refs when calling
    validate_runtime_binding().
    """
    return RuntimeGrammarBinding(
        authority_ref=AUTHORITY_REF,
        authority_kind=AUTHORITY_KIND,
        governed_operation=GOVERNED_OPERATION,
        governed_object_family=GOVERNED_OBJECT_FAMILY,
        operator_semantics_refs=OPERATOR_SEMANTICS_REFS,
        owner_jurisdiction_ref=OWNER_JURISDICTION_REF,
        currentness=CURRENT_ACCEPTED,
        adoption_current_selection_evidence_refs=tuple(adoption_current_selection_evidence_refs),
        immutable_provenance_refs=tuple(immutable_provenance_refs),
    )
