"""Governed source-specific realization law for CLOSED_35 EVS 2008.

This module never opens EVS 2008.sav. It freezes the candidate-neutral
semantic realization that later A/B/C executions must share after governed
physical extraction.

The accepted latin1 compatibility path is physical extraction only. Producer
semantics come from the admitted ZA4800 v5.0.0 documentary estate, never from
compatibility-rendered malformed text.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import COMPATIBILITY_ONLY


CONTRACT_ID = "CLOSED35_R2_EVS2008_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "EVS 2008.sav"
CANONICAL_SHA256 = "5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379"
SOURCE_FORMAT = "SAV"
REPLAY_IDENTITY = "SOURCE_SHA256+ROW_ORDINAL"

PRODUCER_RELEASE_ID = "ZA4800_v5.0.0"
PRODUCER_RELEASE_DATE = "2022-06-08"
PRODUCER_DOI = "10.4232/1.13841"
PRODUCER_DOCUMENTED_CASES = 66280
PRODUCER_DOCUMENTED_VARIABLES = 477
PRODUCER_CHECKSUM_AVAILABLE = False

SOURCE_DECLARED_ENCODING = "UTF-8"
PHYSICAL_COMPATIBILITY_MODE = "SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8"
COMPATIBILITY_ENCODING = "latin1"
COMPATIBILITY_SEMANTIC_SCOPE = "PHYSICAL_EXTRACTION_ONLY__NO_SOURCE_TEXT_OR_SEMANTIC_AUTHORITY"
UNKNOWN_PRODUCER_TEXT = "UNKNOWN_PRODUCER_TEXT"
BOUNDED_UNKNOWN = "BOUNDED_UNKNOWN"

V372_VARIABLE = "v372"
V372_PRODUCER_QUESTION = "Q137"
V372_PRODUCER_SEMANTICS = "date of interview"
V372_RENDERED_SENTINEL = "1582-10-13"
V372_MISSING_STATE = "EVS_STANDARDIZED_MISSING__NEGATIVE_SUBCODE_NOT_RECOVERABLE_FROM_DATE_RENDERING"
V372_MISSING_DETAIL = "UNKNOWN_WITHIN_PRODUCER_NEGATIVE_MISSING_DOMAIN"
V372_ACCEPTED_USER_MISSING_COUNT = 1917
V372_ACCEPTED_PRESENT_COUNT = 64363
V372_SOURCE_VARIABLE_ORDINAL = 466

EVS_NEGATIVE_MISSING_DOMAIN: Mapping[int, str] = {
    -1: "DONT_KNOW",
    -2: "NO_ANSWER",
    -3: "NOT_APPLICABLE",
    -4: "QUESTION_NOT_ASKED_OR_NOT_PROVIDED",
    -5: "OTHER_MISSING_INCLUDING_SYSTEM_WILD_OR_ILLOGICAL",
}

APPLICABLE_EDGE_CLASSES = ("EC01", "EC02", "EC03", "EC08", "EC14")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "typed_missingness",
    "row_replay_identity",
    "reader_configuration_digest",
    "compatibility_decode_evidence",
    "mr_topology",
)

R35_HOOK_BINDING: Mapping[str, Any] = {
    "i01_physical_metadata": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i01-raw-layout-metadata-r1",
        "schema": "PRE553_PHYSICAL_METADATA@1.0.0",
        "required": True,
        "semantic_authority": False,
    },
    "i02_derivative_parentage": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i02-derivative-parentage-r1",
        "source_receipt_schema": "FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0",
        "derivative_receipt_schema": "FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0",
        "bundle_schema": "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0",
        "required_for_non_direct_raw": True,
        "semantic_authority": False,
    },
    "i03_whole_source_physical_equivalence": {
        "worker_branch": "agent/rabochii-premain-fiabc-r35-i03-physical-equivalence-r1",
        "scope_schema": "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0",
        "expectation_schema": "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0",
        "candidate_realization_schema": "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0",
        "receipt_schema": "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0",
        "pass_state": "PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS",
        "applicable_edge_classes": APPLICABLE_EDGE_CLASSES,
        "required_physical_dimensions": R35_REQUIRED_PHYSICAL_DIMENSIONS,
        "semantic_authority": False,
    },
}

DOCUMENTARY_AUTHORITY_CHAIN = (
    {
        "tier": 1,
        "authority_id": "ZA4800_V5_VARIABLE_REPORT",
        "scope": "integrated variable semantics, standardized missing vocabulary, recodes and country notes",
    },
    {
        "tier": 2,
        "authority_id": "EVS2008_MASTER_QUESTIONNAIRE",
        "scope": "question wording, response design and routing",
    },
    {
        "tier": 3,
        "authority_id": "EVS2008_METHOD_NATIONAL_TRANSLATION_ERRATA",
        "scope": "country-specific deviations and producer correction context",
    },
)
_ALLOWED_DOCUMENT_AUTHORITY_IDS = frozenset(x["authority_id"] for x in DOCUMENTARY_AUTHORITY_CHAIN)
_AUTHORITY_PRECEDENCE = {x["authority_id"]: x["tier"] for x in DOCUMENTARY_AUTHORITY_CHAIN}


class EVS2008RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise EVS2008RealizationError(f"non-canonical realization material: {type(value).__name__}")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class DocumentaryVariableEntry:
    variable_name: str
    authority_id: str
    producer_label: str | None
    value_labels: Mapping[str, Any]
    question_or_construct_ref: str | None = None
    country_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.variable_name:
            raise EVS2008RealizationError("variable_name must be non-empty")
        if self.authority_id not in _ALLOWED_DOCUMENT_AUTHORITY_IDS:
            raise EVS2008RealizationError("unadmitted documentary authority")


@dataclass(frozen=True)
class DocumentaryAlignment:
    variable_name: str
    status: str
    authority_id: str | None
    semantic_label: str | None
    value_status: str
    documentary_value_label: Any = None


def align_documentary_semantics(
    variable_name: str,
    *,
    entries: Iterable[DocumentaryVariableEntry],
    raw_value: Any = None,
    country: str | None = None,
    compatibility_rendered_text: str | None = None,
) -> DocumentaryAlignment:
    """Resolve semantics only through exact producer documentary identity."""

    del compatibility_rendered_text
    exact = []
    for entry in entries:
        if entry.variable_name != variable_name:
            continue
        if entry.country_scope and country not in entry.country_scope:
            continue
        exact.append(entry)

    if not exact:
        return DocumentaryAlignment(
            variable_name,
            UNKNOWN_PRODUCER_TEXT,
            None,
            None,
            UNKNOWN_PRODUCER_TEXT,
            None,
        )

    exact.sort(key=lambda entry: _AUTHORITY_PRECEDENCE[entry.authority_id])
    chosen = exact[0]
    if chosen.producer_label is None:
        return DocumentaryAlignment(
            variable_name,
            UNKNOWN_PRODUCER_TEXT,
            chosen.authority_id,
            None,
            UNKNOWN_PRODUCER_TEXT,
            None,
        )

    if raw_value is None:
        value_status = "DOCUMENTARY_VALUE_NOT_REQUESTED"
        value_label = None
    else:
        labels = {str(key): value for key, value in chosen.value_labels.items()}
        key = str(raw_value)
        if key in labels:
            value_status = "DOCUMENTARY_VALUE_ALIGNMENT_RESOLVED"
            value_label = labels[key]
        else:
            value_status = UNKNOWN_PRODUCER_TEXT
            value_label = None

    return DocumentaryAlignment(
        variable_name,
        "DOCUMENTARY_ALIGNMENT_RESOLVED",
        chosen.authority_id,
        chosen.producer_label,
        value_status,
        value_label,
    )


@dataclass(frozen=True)
class MRSetLaw:
    set_name: str
    members: tuple[str, ...]
    producer_question: str
    producer_semantics: str
    rank_law: str = "NO_RANK_SIGNIFICANCE__CATEGORY_ORDER_ONLY"
    selection_cap: int | None = None
    alias_of: str | None = None
    overlap_of: str | None = None
    omitted_members: tuple[str, ...] = ()
    distinct_nonmember_roles: tuple[str, ...] = ()
    distinct_nonmember_role_semantics: str | None = None
    type_code: str = "D"
    counted_value: int = 1

    def __post_init__(self) -> None:
        if not self.set_name or not self.members:
            raise EVS2008RealizationError("MR set identity and members are required")
        if len(set(self.members)) != len(self.members):
            raise EVS2008RealizationError(f"duplicate member inside MR set {self.set_name}")
        if self.type_code != "D" or self.counted_value != 1:
            raise EVS2008RealizationError("EVS2008 native MR law requires type D counted_value=1")
        if self.selection_cap is not None and self.selection_cap < 1:
            raise EVS2008RealizationError("selection cap must be positive")


MR_SETS: tuple[MRSetLaw, ...] = (
    MRSetLaw(
        "q5a",
        tuple(f"v{i}" for i in range(10, 26)),
        "Q5a",
        "voluntary-organisation membership",
        alias_of="evs_q5a",
    ),
    MRSetLaw(
        "evs_q5a",
        tuple(f"v{i}" for i in range(10, 26)),
        "Q5a",
        "voluntary-organisation membership",
        alias_of="q5a",
    ),
    MRSetLaw(
        "vv25",
        tuple(f"v{i}" for i in range(10, 25)),
        "Q5a substantive body",
        "voluntary-organisation substantive categories excluding v25=None",
        overlap_of="q5a",
        omitted_members=("v25",),
    ),
    MRSetLaw(
        "q5b",
        tuple(f"v{i}" for i in range(28, 44)),
        "Q5b",
        "unpaid voluntary work",
        alias_of="evs_q5b",
    ),
    MRSetLaw(
        "evs_q5b",
        tuple(f"v{i}" for i in range(28, 44)),
        "Q5b",
        "unpaid voluntary work",
        alias_of="q5b",
    ),
    MRSetLaw(
        "vv43",
        tuple(f"v{i}" for i in range(28, 43)),
        "Q5b substantive body",
        "unpaid-work substantive categories excluding v43=None",
        overlap_of="q5b",
        omitted_members=("v43",),
    ),
    MRSetLaw(
        "evs_q6",
        tuple(f"v{i}" for i in range(46, 61)),
        "Q6",
        "groups not wanted as neighbours",
    ),
    MRSetLaw(
        "q14",
        tuple(f"v{i}" for i in range(69, 87)),
        "Q14",
        "job aspects personally important",
        alias_of="evs_q14",
    ),
    MRSetLaw(
        "evs_q14",
        tuple(f"v{i}" for i in range(69, 87)),
        "Q14",
        "job aspects personally important",
        alias_of="q14",
    ),
    MRSetLaw(
        "q52",
        tuple(f"v{i}" for i in range(170, 182)),
        "Q52",
        "qualities children should be encouraged to learn at home",
        rank_law="SELECTION_CAP_5__NO_RANK_SIGNIFICANCE",
        selection_cap=5,
        alias_of="evs_q52",
    ),
    MRSetLaw(
        "evs_q52",
        tuple(f"v{i}" for i in range(170, 182)),
        "Q52",
        "qualities children should be encouraged to learn at home",
        rank_law="SELECTION_CAP_5__NO_RANK_SIGNIFICANCE",
        selection_cap=5,
        alias_of="q52",
    ),
    MRSetLaw(
        "evs_q107",
        ("v323", "v324a", "v325a", "v326a", "v327a", "v328a"),
        "Q107",
        "household-member category presence",
        distinct_nonmember_roles=("v324b", "v325b", "v326b", "v327b", "v328b"),
        distinct_nonmember_role_semantics="counts of household members in corresponding categories",
    ),
    MRSetLaw(
        "evs_q108",
        ("v329a", "v330a", "v331a", "v332a", "v333a", "v334a"),
        "Q108",
        "family events ever experienced",
        distinct_nonmember_roles=("v329b", "v330b", "v331b", "v332b", "v333b", "v334b"),
        distinct_nonmember_role_semantics="age at first experience",
    ),
)

MR_SET_BY_NAME: Mapping[str, MRSetLaw] = {rule.set_name: rule for rule in MR_SETS}
if len(MR_SET_BY_NAME) != 13:
    raise EVS2008RealizationError("EVS2008 realization must contain exactly 13 native MR identities")


def mr_topology_payload() -> tuple[Mapping[str, Any], ...]:
    return tuple(
        {
            "set_name": rule.set_name,
            "members": rule.members,
            "producer_question": rule.producer_question,
            "producer_semantics": rule.producer_semantics,
            "rank_law": rule.rank_law,
            "selection_cap": rule.selection_cap,
            "alias_of": rule.alias_of,
            "overlap_of": rule.overlap_of,
            "omitted_members": rule.omitted_members,
            "distinct_nonmember_roles": rule.distinct_nonmember_roles,
            "distinct_nonmember_role_semantics": rule.distinct_nonmember_role_semantics,
            "type_code": rule.type_code,
            "counted_value": rule.counted_value,
        }
        for rule in MR_SETS
    )


MR_TOPOLOGY_IDENTITY = canonical_digest(mr_topology_payload())


def require_exact_mr_topology(observed_sets: Mapping[str, Sequence[str]]) -> str:
    """Require exact native set identities and exact ordered membership."""

    if set(observed_sets) != set(MR_SET_BY_NAME):
        raise EVS2008RealizationError("MR set identity collapse or invention")
    for name, law in MR_SET_BY_NAME.items():
        if tuple(observed_sets[name]) != law.members:
            raise EVS2008RealizationError(f"MR membership/order drift for {name}")
    return MR_TOPOLOGY_IDENTITY


@dataclass(frozen=True)
class MRMissingState:
    raw_code: int
    semantic_state: str
    is_missing: bool


def realize_mr_item_code(raw_code: int) -> MRMissingState:
    if raw_code == 1:
        return MRMissingState(1, "MENTIONED_OR_YES", False)
    if raw_code == 0:
        return MRMissingState(0, "NOT_MENTIONED_OR_NO", False)
    if raw_code in EVS_NEGATIVE_MISSING_DOMAIN:
        return MRMissingState(raw_code, EVS_NEGATIVE_MISSING_DOMAIN[raw_code], True)
    return MRMissingState(raw_code, BOUNDED_UNKNOWN, False)


@dataclass(frozen=True)
class MRRoutingRule:
    rule_id: str
    set_names: tuple[str, ...]
    country_scope: tuple[str, ...]
    producer_rule: str
    authority_id: str = "ZA4800_V5_VARIABLE_REPORT"

    def __post_init__(self) -> None:
        if self.authority_id not in _ALLOWED_DOCUMENT_AUTHORITY_IDS:
            raise EVS2008RealizationError("routing rule uses unadmitted authority")
        if any(name not in MR_SET_BY_NAME for name in self.set_names):
            raise EVS2008RealizationError("routing rule references unknown MR set")


MR_ROUTING_RULES = (
    MRRoutingRule(
        "MRR_Q5B_DK",
        ("q5b", "evs_q5b", "vv43"),
        ("DK", "Denmark"),
        "Q5b not implemented in Denmark; integrated producer state is -4 question not asked.",
    ),
    MRRoutingRule(
        "MRR_Q6_NOT_IMPLEMENTED",
        ("evs_q6",),
        ("AT", "Austria", "BY", "Belarus", "DK", "Denmark", "FR", "France", "IT", "Italy", "NO", "Norway", "SI", "Slovenia"),
        "Q6 not implemented in the named country; integrated producer state is -4 question not asked.",
    ),
    MRRoutingRule(
        "MRR_Q6_FI",
        ("evs_q6",),
        ("FI", "Finland"),
        "Finland auxiliary no-such-groups maps to 0 and cannot-say maps to -1 under producer documentation.",
    ),
    MRRoutingRule(
        "MRR_Q107_FI",
        ("evs_q107",),
        ("FI", "Finland"),
        "Finland none-above auxiliary maps Q107 presence indicators to 0.",
    ),
    MRRoutingRule(
        "MRR_Q108_FI",
        ("evs_q108",),
        ("FI", "Finland"),
        "Finland none-above maps Q108 a-variables to 0 and cannot-say maps to -1.",
    ),
)


@dataclass(frozen=True)
class RoutingResolution:
    set_name: str
    country: str | None
    status: str
    rule_id: str | None
    producer_rule: str | None


def resolve_mr_routing(
    set_name: str,
    *,
    country: str | None,
    observed_missing_state: str | None = None,
) -> RoutingResolution:
    """Resolve only explicit documentary country/question routing.

    Missingness is deliberately discarded as an authority input.
    """

    del observed_missing_state
    if set_name not in MR_SET_BY_NAME:
        raise EVS2008RealizationError("unknown native MR set")

    candidates = [
        rule
        for rule in MR_ROUTING_RULES
        if set_name in rule.set_names and country in rule.country_scope
    ]
    if not candidates:
        return RoutingResolution(set_name, country, BOUNDED_UNKNOWN, None, None)
    candidates.sort(key=lambda rule: rule.rule_id)
    chosen = candidates[0]
    return RoutingResolution(
        set_name,
        country,
        "DOCUMENTARY_ROUTING_RESOLVED",
        chosen.rule_id,
        chosen.producer_rule,
    )


@dataclass(frozen=True)
class V372MissingRealization:
    variable: str
    rendered_witness: str
    semantic_state: str
    semantic_reason_detail: str
    producer_missing_domain: tuple[int, ...]


def realize_v372_rendered_missing(
    rendered_witness: str,
    *,
    claimed_negative_subcode: int | None = None,
) -> V372MissingRealization:
    if rendered_witness != V372_RENDERED_SENTINEL:
        raise EVS2008RealizationError("unsupported V372 rendered witness")
    if claimed_negative_subcode is not None:
        raise EVS2008RealizationError(
            "V372 negative subcode is not recoverable from date rendering"
        )
    return V372MissingRealization(
        V372_VARIABLE,
        rendered_witness,
        V372_MISSING_STATE,
        V372_MISSING_DETAIL,
        tuple(EVS_NEGATIVE_MISSING_DOMAIN),
    )


FLAG_RELATIONS: Mapping[str, Mapping[str, Any]] = {
    "f201": {
        "scope": ("v201", "v202"),
        "rule": "if v201 == v202 then f201=1",
        "values": {0: "consistent", 1: "inconsistent"},
    },
    "f25": {"scope": tuple(f"v{i}" for i in range(10, 26)), "role": "Q5a body-versus-None consistency"},
    "f43": {"scope": tuple(f"v{i}" for i in range(28, 44)), "role": "Q5b body-versus-None consistency"},
    "f86": {"scope": tuple(f"v{i}" for i in range(69, 87)), "role": "Q14 body-versus-None consistency"},
    "f180": {"scope": tuple(f"v{i}" for i in range(170, 181)), "role": "Q52 more-than-five-selection flag"},
}


def assert_no_producer_checksum_claim(claimed_digest: str | None) -> None:
    if claimed_digest is not None:
        raise EVS2008RealizationError(
            "documentary release alignment cannot mint a producer checksum claim"
        )


def _normalized_reader_configuration(reader_configuration: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "reader": reader_configuration.get("reader"),
        "reader_version": reader_configuration.get("reader_version"),
        "user_missing": reader_configuration.get("user_missing"),
        "apply_value_formats": reader_configuration.get("apply_value_formats"),
        "encoding": reader_configuration.get("encoding"),
        "authority_status": reader_configuration.get("authority_status"),
        "compatibility_mode": reader_configuration.get(
            "compatibility_mode", PHYSICAL_COMPATIBILITY_MODE
        ),
        "compatibility_semantic_scope": reader_configuration.get(
            "compatibility_semantic_scope", COMPATIBILITY_SEMANTIC_SCOPE
        ),
        "semantic_authority": reader_configuration.get("semantic_authority", False),
    }


@dataclass(frozen=True)
class PhysicalAdmission:
    source_sha256: str
    reader_configuration_digest: str
    compatibility_semantic_authority: bool


def admit_physical_incidence(incidence: Any) -> PhysicalAdmission:
    if getattr(incidence, "source_sha256", None) != CANONICAL_SHA256:
        raise EVS2008RealizationError("canonical EVS2008 source root mismatch")

    reader_configuration = getattr(incidence, "reader_configuration", None)
    if not isinstance(reader_configuration, Mapping):
        raise EVS2008RealizationError("reader configuration missing")

    normalized = _normalized_reader_configuration(reader_configuration)
    expected = {
        "reader": "pyreadstat",
        "reader_version": reader_configuration.get("reader_version"),
        "user_missing": True,
        "apply_value_formats": False,
        "encoding": COMPATIBILITY_ENCODING,
        "authority_status": COMPATIBILITY_ONLY,
        "compatibility_mode": PHYSICAL_COMPATIBILITY_MODE,
        "compatibility_semantic_scope": COMPATIBILITY_SEMANTIC_SCOPE,
        "semantic_authority": False,
    }
    if normalized != expected:
        raise EVS2008RealizationError("EVS2008 reader/config drift")

    return PhysicalAdmission(
        CANONICAL_SHA256,
        canonical_digest(normalized),
        False,
    )


def source_specific_realization_payload() -> Mapping[str, Any]:
    return {
        "contract": CONTRACT_ID,
        "source": {
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "replay_identity": REPLAY_IDENTITY,
            "physical_compatibility_mode": PHYSICAL_COMPATIBILITY_MODE,
            "compatibility_semantic_scope": COMPATIBILITY_SEMANTIC_SCOPE,
        },
        "producer_release": {
            "id": PRODUCER_RELEASE_ID,
            "release_date": PRODUCER_RELEASE_DATE,
            "doi": PRODUCER_DOI,
            "documented_cases": PRODUCER_DOCUMENTED_CASES,
            "documented_variables": PRODUCER_DOCUMENTED_VARIABLES,
            "public_producer_checksum_available": PRODUCER_CHECKSUM_AVAILABLE,
        },
        "documentary_alignment": {
            "join": "EXACT_SOURCE_VARIABLE_OR_PRODUCER_QUESTION_IDENTITY",
            "compatibility_rendered_text_semantic_authority": False,
            "unmatched_text_state": UNKNOWN_PRODUCER_TEXT,
            "authority_chain": DOCUMENTARY_AUTHORITY_CHAIN,
        },
        "native_mr": {
            "set_count": 13,
            "topology_identity": MR_TOPOLOGY_IDENTITY,
            "sets": mr_topology_payload(),
            "alias_law": "PRESERVE_NATIVE_IDENTITIES__ONE_PRODUCER_BATTERY__NO_DOUBLE_COUNT",
            "overlap_law": "PRESERVE_SUBSET_IDENTITY__NO_MEMBER_VECTOR_COLLAPSE",
            "missing_domain": EVS_NEGATIVE_MISSING_DOMAIN,
            "routing_from_missingness": False,
        },
        "v372": {
            "semantic_state": V372_MISSING_STATE,
            "semantic_reason_detail": V372_MISSING_DETAIL,
            "rendered_witness": V372_RENDERED_SENTINEL,
            "producer_missing_domain": tuple(EVS_NEGATIVE_MISSING_DOMAIN),
        },
        "flag_relations": FLAG_RELATIONS,
        "s35_edge_classes": APPLICABLE_EDGE_CLASSES,
        "r35_hooks": R35_HOOK_BINDING,
        "semantic_owner_surface": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0",
        "candidate_law": "A_B_C_SHARE_ONE_SOURCE_SPECIFIC_SEMANTIC_REALIZATION_IDENTITY",
    }


SOURCE_SPECIFIC_REALIZATION_IDENTITY = canonical_digest(source_specific_realization_payload())


@dataclass(frozen=True)
class CandidateSemanticBinding:
    candidate_id: str
    source_sha256: str = CANONICAL_SHA256
    source_specific_realization_identity: str = SOURCE_SPECIFIC_REALIZATION_IDENTITY

    def __post_init__(self) -> None:
        if self.candidate_id not in {"A", "B", "C"}:
            raise EVS2008RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise EVS2008RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise EVS2008RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise EVS2008RealizationError("exact A/B/C candidate set required")
    if any(binding.source_sha256 != CANONICAL_SHA256 for binding in bindings):
        raise EVS2008RealizationError("candidate source root divergence")
    identities = {binding.source_specific_realization_identity for binding in bindings}
    if identities != {SOURCE_SPECIFIC_REALIZATION_IDENTITY}:
        raise EVS2008RealizationError("candidate semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "BOUNDED_UNKNOWN",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "CandidateSemanticBinding",
    "COMPATIBILITY_SEMANTIC_SCOPE",
    "CONTRACT_ID",
    "DocumentaryAlignment",
    "DocumentaryVariableEntry",
    "EVS2008RealizationError",
    "EVS_NEGATIVE_MISSING_DOMAIN",
    "FLAG_RELATIONS",
    "MR_ROUTING_RULES",
    "MR_SETS",
    "MR_SET_BY_NAME",
    "MR_TOPOLOGY_IDENTITY",
    "PHYSICAL_COMPATIBILITY_MODE",
    "PRODUCER_RELEASE_ID",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "REPLAY_IDENTITY",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "UNKNOWN_PRODUCER_TEXT",
    "V372_MISSING_DETAIL",
    "V372_MISSING_STATE",
    "V372_RENDERED_SENTINEL",
    "admit_physical_incidence",
    "align_documentary_semantics",
    "assert_no_producer_checksum_claim",
    "canonical_digest",
    "mr_topology_payload",
    "realize_mr_item_code",
    "realize_v372_rendered_missing",
    "require_common_abc_semantic_law",
    "require_exact_mr_topology",
    "resolve_mr_routing",
]
