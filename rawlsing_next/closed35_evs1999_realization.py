"""Governed source-specific realization law for CLOSED_35 EVS 1999.

This module never reads the SAV. It freezes the candidate-neutral semantic law
that later A/B/C realizations must share after physical extraction.

Compatibility-decoded text is deliberately excluded from semantic authority.
Only the exact ZA3811 v3.0.0 producer documentary surfaces admitted by
CLOSED35-L2-EVS1999 may provide text or routing semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import COMPATIBILITY_ONLY


CONTRACT_ID = "CLOSED35_R1_EVS1999_SOURCE_REALIZATION@1.0.0"
CANONICAL_FILENAME = "EVS 1999.sav"
CANONICAL_SHA256 = "6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a"
SOURCE_FORMAT = "SAV"
PRODUCER_RELEASE_ID = "ZA3811_v3.0.0"
PRODUCER_RELEASE_DATE = "2011-11-20"
PRODUCER_DOI = "10.4232/1.10789"
SOURCE_DECLARED_ENCODING = "UTF-8"
SOURCE_DECLARED_CHARACTER_CODE = 65001
PHYSICAL_COMPATIBILITY_MODE = "SAV_LATIN1_COMPAT_PHYSICAL_ONLY__SOURCE_DECLARES_UTF8"
COMPATIBILITY_ENCODING = "latin1"
COMPATIBILITY_SEMANTIC_SCOPE = "PHYSICAL_EXTRACTION_ONLY__NO_SOURCE_TEXT_OR_SEMANTIC_AUTHORITY"
DOCUMENTARY_ALIGNMENT_UNKNOWN = "DOCUMENTARY_ALIGNMENT_UNKNOWN"

# R35-I01/I02/I03 live on accepted implementation branches but are not present
# in the L2-HQ base. Freeze their exact integration schemas here rather than
# pretending those implementations have already been merged.
R35_PHYSICAL_METADATA_SCHEMA = "PRE553_PHYSICAL_METADATA@1.0.0"
R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"
R35_PHYSICAL_SCOPE_SCHEMA = "FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0"
R35_PHYSICAL_EXPECTATION_SCHEMA = "FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0"
R35_PHYSICAL_REALIZATION_SCHEMA = "FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0"
R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA = "FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0"

APPLICABLE_EDGE_CLASSES = ("EC01", "EC02", "EC03", "EC10", "EC14")
R35_REQUIRED_PHYSICAL_DIMENSIONS = (
    "physical_metadata",
    "variable_inventory_order",
    "raw_storage_values",
    "row_replay_identity",
    "reader_configuration_digest",
    "compatibility_decode_evidence",
    "form_module_skip_routing_carriers",
)

EXACT_READER_CONFIGURATION: Mapping[str, Any] = {
    "decoder_implementation": "rawlsing_next/pre553_physical_decoder.py",
    "decoder_version": "pyreadstat/1.3.6",
    "decoder_mode": PHYSICAL_COMPATIBILITY_MODE,
    "config": {
        "reader": "pyreadstat.read_sav",
        "encoding": COMPATIBILITY_ENCODING,
        "user_missing": True,
        "apply_value_formats": False,
        "automatic_encoding_guessing": False,
    },
    "compatibility_mode": PHYSICAL_COMPATIBILITY_MODE,
    "compatibility_semantic_scope": COMPATIBILITY_SEMANTIC_SCOPE,
    "semantic_authority": False,
    "source_declared_encoding": SOURCE_DECLARED_ENCODING,
    "source_declared_character_code": SOURCE_DECLARED_CHARACTER_CODE,
}

DOCUMENTARY_AUTHORITY_CHAIN = (
    {
        "tier": 1,
        "authority_id": "ZA3811_V3_0_0_VARIABLE_REPORT",
        "scope": "exact integrated data-file variable semantics, value dictionaries, construction/country notes",
        "locator": "https://access.gesis.org/dbk/50677",
    },
    {
        "tier": 2,
        "authority_id": "EVS1999_NATIONAL_DOCUMENT",
        "scope": "exact country-specific wording/deviation after country+variable/question alignment",
        "locator": "EVS/GESIS national field questionnaire or bilingual/national variable report",
    },
    {
        "tier": 3,
        "authority_id": "EVS1999_MASTER_QUESTIONNAIRE",
        "scope": "default instrument wording and flow where no release-specific/national override applies",
        "locator": "https://access.gesis.org/dbk/9782",
    },
)
_ALLOWED_DOCUMENT_AUTHORITY_IDS = frozenset(x["authority_id"] for x in DOCUMENTARY_AUTHORITY_CHAIN)
_AUTHORITY_PRECEDENCE = {x["authority_id"]: x["tier"] for x in DOCUMENTARY_AUTHORITY_CHAIN}


class EVS1999RealizationError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise EVS1999RealizationError(f"non-canonical realization material: {type(value).__name__}")


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require_nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EVS1999RealizationError(f"{name} must be a non-empty string")
    return value


@dataclass(frozen=True)
class DocumentaryVariableEntry:
    variable_name: str
    authority_id: str
    producer_label: str | None
    value_labels: Mapping[str, Any]
    question_or_construct_ref: str | None = None
    country_scope: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty(self.variable_name, "variable_name")
        if self.authority_id not in _ALLOWED_DOCUMENT_AUTHORITY_IDS:
            raise EVS1999RealizationError("unadmitted documentary authority")
        if self.producer_label is not None:
            _require_nonempty(self.producer_label, "producer_label")


@dataclass(frozen=True)
class DocumentaryAlignment:
    variable_name: str
    status: str
    authority_id: str | None
    semantic_label: str | None
    value_status: str
    documentary_value_label: Any = None

    @property
    def semantic_authority_present(self) -> bool:
        return self.status == "DOCUMENTARY_ALIGNMENT_RESOLVED"


def align_documentary_semantics(
    variable_name: str,
    *,
    entries: Iterable[DocumentaryVariableEntry],
    raw_value: Any = None,
    compatibility_rendered_text: str | None = None,
) -> DocumentaryAlignment:
    """Resolve semantics only through an exact producer-documentary join."""

    _require_nonempty(variable_name, "variable_name")
    del compatibility_rendered_text

    exact = [entry for entry in entries if entry.variable_name == variable_name]
    if not exact:
        return DocumentaryAlignment(
            variable_name,
            DOCUMENTARY_ALIGNMENT_UNKNOWN,
            None,
            None,
            DOCUMENTARY_ALIGNMENT_UNKNOWN,
            None,
        )

    exact.sort(key=lambda entry: _AUTHORITY_PRECEDENCE[entry.authority_id])
    chosen = exact[0]
    if chosen.producer_label is None:
        return DocumentaryAlignment(
            variable_name,
            DOCUMENTARY_ALIGNMENT_UNKNOWN,
            chosen.authority_id,
            None,
            DOCUMENTARY_ALIGNMENT_UNKNOWN,
            None,
        )

    if raw_value is None:
        value_status = "DOCUMENTARY_VALUE_NOT_REQUESTED"
        value_label = None
    else:
        normalized = {str(key): value for key, value in chosen.value_labels.items()}
        raw_key = str(raw_value)
        if raw_key in normalized:
            value_status = "DOCUMENTARY_VALUE_ALIGNMENT_RESOLVED"
            value_label = normalized[raw_key]
        else:
            value_status = DOCUMENTARY_ALIGNMENT_UNKNOWN
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
class DocumentaryRoutingRule:
    route_id: str
    variable_or_question: str
    authority_id: str
    producer_rule: str
    country_scope: tuple[str, ...] = ()
    status: str = "AUTHORITATIVE_DOCUMENTARY_ROUTING"

    def __post_init__(self) -> None:
        _require_nonempty(self.route_id, "route_id")
        _require_nonempty(self.variable_or_question, "variable_or_question")
        _require_nonempty(self.producer_rule, "producer_rule")
        if self.authority_id not in _ALLOWED_DOCUMENT_AUTHORITY_IDS:
            raise EVS1999RealizationError("routing rule uses unadmitted documentary authority")


@dataclass(frozen=True)
class RoutingResolution:
    variable_or_question: str
    status: str
    route_id: str | None
    authority_id: str | None
    producer_rule: str | None


def resolve_documentary_routing(
    variable_or_question: str,
    *,
    rules: Sequence[DocumentaryRoutingRule],
    country: str | None = None,
    observed_missing_state: str | None = None,
) -> RoutingResolution:
    """Resolve routing through documentary authority, never missingness."""

    _require_nonempty(variable_or_question, "variable_or_question")
    del observed_missing_state

    candidates = []
    for rule in rules:
        if rule.variable_or_question != variable_or_question:
            continue
        if rule.country_scope and country not in rule.country_scope:
            continue
        candidates.append(rule)

    if not candidates:
        return RoutingResolution(
            variable_or_question,
            DOCUMENTARY_ALIGNMENT_UNKNOWN,
            None,
            None,
            None,
        )

    candidates.sort(key=lambda rule: (_AUTHORITY_PRECEDENCE[rule.authority_id], rule.route_id))
    chosen = candidates[0]
    return RoutingResolution(
        variable_or_question,
        "DOCUMENTARY_ROUTING_RESOLVED",
        chosen.route_id,
        chosen.authority_id,
        chosen.producer_rule,
    )


ROUTING_RULES = (
    DocumentaryRoutingRule(
        "RT002",
        "v49_filt",
        "ZA3811_V3_0_0_VARIABLE_REPORT",
        "Reconstruct category -3 NAP using the producer-documented v87/v306 rule and named country handling.",
    ),
    DocumentaryRoutingRule(
        "RT003",
        "v50_filt",
        "ZA3811_V3_0_0_VARIABLE_REPORT",
        "Use the producer v13/v101 construction; named countries use documented reconstruction and Turkey is not asked/coded -4.",
    ),
    DocumentaryRoutingRule(
        "RT004",
        "v51_filt",
        "ZA3811_V3_0_0_VARIABLE_REPORT",
        "Preserve the producer expression ANY(0,v27,v45) verbatim for the documented reconstruction.",
    ),
    DocumentaryRoutingRule(
        "RT005",
        "v290_hu",
        "ZA3811_V3_0_0_VARIABLE_REPORT",
        "Hungary-only Q83E_HU eligibility follows the producer-documented preceding-Q81d condition.",
        ("HU", "Hungary"),
    ),
    DocumentaryRoutingRule(
        "RT006",
        "v87",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q14 employed -> Q15; not employed -> Q17 unless an exact higher-precedence producer note overrides.",
    ),
    DocumentaryRoutingRule(
        "RT007",
        "v101",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q22 denomination-membership no -> Q24a unless an exact higher-precedence producer note overrides.",
    ),
    DocumentaryRoutingRule(
        "RT008",
        "v103",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q24a prior-membership no -> Q25 unless an exact higher-precedence producer note overrides.",
    ),
    DocumentaryRoutingRule(
        "RT009",
        "v293",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q86 stable-relationship no -> Q88 unless an exact higher-precedence producer note overrides.",
    ),
    DocumentaryRoutingRule(
        "RT010",
        "v296",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q89 divorced/never-married -> Q91; other documented statuses continue Q90.",
    ),
    DocumentaryRoutingRule(
        "RT011",
        "v306",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q96 employment categories route to Q100/Q101/Q104/Q105; paid employment continues Q97.",
    ),
    DocumentaryRoutingRule(
        "RT012",
        "v307",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q97 supervisory-status no -> Q101.",
    ),
    DocumentaryRoutingRule(
        "RT013",
        "v309",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "After Q99 proceed to Q101.",
    ),
    DocumentaryRoutingRule(
        "RT014",
        "v315",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "Q105 chief-wage-earner yes -> Q110; no -> Q106; Q110 resumes all-respondent flow.",
    ),
)


def _normalized_runtime_reader_configuration(reader_configuration: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "decoder_implementation": reader_configuration.get(
            "decoder_implementation", "rawlsing_next/pre553_physical_decoder.py"
        ),
        "decoder_version": (
            f"pyreadstat/{reader_configuration.get('reader_version')}"
            if reader_configuration.get("reader_version")
            else reader_configuration.get("decoder_version")
        ),
        "decoder_mode": reader_configuration.get("decoder_mode", PHYSICAL_COMPATIBILITY_MODE),
        "config": {
            "reader": (
                "pyreadstat.read_sav"
                if reader_configuration.get("reader") == "pyreadstat"
                else reader_configuration.get("reader")
            ),
            "encoding": reader_configuration.get("encoding"),
            "user_missing": reader_configuration.get("user_missing"),
            "apply_value_formats": reader_configuration.get("apply_value_formats"),
            "automatic_encoding_guessing": reader_configuration.get(
                "automatic_encoding_guessing", False
            ),
        },
        "compatibility_mode": reader_configuration.get(
            "compatibility_mode", PHYSICAL_COMPATIBILITY_MODE
        ),
        "compatibility_semantic_scope": reader_configuration.get(
            "compatibility_semantic_scope", COMPATIBILITY_SEMANTIC_SCOPE
        ),
        "semantic_authority": reader_configuration.get("semantic_authority", False),
        "source_declared_encoding": reader_configuration.get(
            "source_declared_encoding", SOURCE_DECLARED_ENCODING
        ),
        "source_declared_character_code": reader_configuration.get(
            "source_declared_character_code", SOURCE_DECLARED_CHARACTER_CODE
        ),
    }


@dataclass(frozen=True)
class PhysicalAdmission:
    source_sha256: str
    reader_configuration_digest: str
    compatibility_semantic_authority: bool = False


def admit_physical_incidence(incidence: Any) -> PhysicalAdmission:
    """Bind a synthetic or future physical incidence to exact EVS1999 law."""

    if getattr(incidence, "source_sha256", None) != CANONICAL_SHA256:
        raise EVS1999RealizationError("canonical EVS1999 source root mismatch")
    reader_configuration = getattr(incidence, "reader_configuration", None)
    if not isinstance(reader_configuration, Mapping):
        raise EVS1999RealizationError("reader configuration missing")

    normalized = _normalized_runtime_reader_configuration(reader_configuration)
    if _canonical(normalized) != _canonical(EXACT_READER_CONFIGURATION):
        raise EVS1999RealizationError("EVS1999 reader/config drift")

    authority_status = reader_configuration.get("authority_status")
    if authority_status not in (None, COMPATIBILITY_ONLY):
        raise EVS1999RealizationError("compatibility authority-status drift")
    if authority_status is None and reader_configuration.get("compatibility_mode") is None:
        raise EVS1999RealizationError("physical-only compatibility witness missing")

    return PhysicalAdmission(
        CANONICAL_SHA256,
        canonical_digest(EXACT_READER_CONFIGURATION),
        False,
    )


R35_HOOK_BINDING: Mapping[str, Any] = {
    "i01_physical_metadata": {
        "schema": R35_PHYSICAL_METADATA_SCHEMA,
        "required": True,
        "semantic_authority": False,
    },
    "i02_derivative_parentage": {
        "schema": R35_DERIVATIVE_PARENTAGE_BUNDLE_SCHEMA,
        "required_for_non_direct_raw": True,
        "semantic_authority": False,
    },
    "i03_source_scope": {
        "scope_schema": R35_PHYSICAL_SCOPE_SCHEMA,
        "expectation_schema": R35_PHYSICAL_EXPECTATION_SCHEMA,
        "candidate_realization_schema": R35_PHYSICAL_REALIZATION_SCHEMA,
        "receipt_schema": R35_PHYSICAL_EQUIVALENCE_RECEIPT_SCHEMA,
        "applicable_edge_classes": APPLICABLE_EDGE_CLASSES,
        "required_physical_dimensions": R35_REQUIRED_PHYSICAL_DIMENSIONS,
        "semantic_authority": False,
    },
}


def source_specific_realization_payload() -> Mapping[str, Any]:
    return {
        "contract": CONTRACT_ID,
        "source": {
            "canonical_filename": CANONICAL_FILENAME,
            "canonical_sha256": CANONICAL_SHA256,
            "format": SOURCE_FORMAT,
            "replay_identity": "SOURCE_SHA256+ROW_ORDINAL",
        },
        "reader_configuration": EXACT_READER_CONFIGURATION,
        "producer_release": {
            "id": PRODUCER_RELEASE_ID,
            "release_date": PRODUCER_RELEASE_DATE,
            "doi": PRODUCER_DOI,
        },
        "documentary_alignment": {
            "variable_join": "EXACT_SOURCE_VARIABLE_IDENTIFIER_ONLY",
            "compatibility_rendered_text_semantic_authority": False,
            "failed_join_state": DOCUMENTARY_ALIGNMENT_UNKNOWN,
            "authority_chain": DOCUMENTARY_AUTHORITY_CHAIN,
        },
        "routing": {
            "authority_source": "DOCUMENTARY_ONLY",
            "missingness_is_authority": False,
            "precedence": [
                "ZA3811_V3_0_0_VARIABLE_REPORT",
                "EVS1999_NATIONAL_DOCUMENT",
                "EVS1999_MASTER_QUESTIONNAIRE",
                DOCUMENTARY_ALIGNMENT_UNKNOWN,
            ],
        },
        "semantic_owner_surface": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0",
        "r35_hooks": R35_HOOK_BINDING,
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
            raise EVS1999RealizationError("candidate must be A, B or C")
        if self.source_sha256 != CANONICAL_SHA256:
            raise EVS1999RealizationError("candidate source root divergence")
        if self.source_specific_realization_identity != SOURCE_SPECIFIC_REALIZATION_IDENTITY:
            raise EVS1999RealizationError("candidate semantic realization divergence")


def require_common_abc_semantic_law(
    bindings: Sequence[CandidateSemanticBinding],
) -> str:
    if tuple(sorted(binding.candidate_id for binding in bindings)) != ("A", "B", "C"):
        raise EVS1999RealizationError("exact A/B/C candidate set required")
    if len({binding.source_sha256 for binding in bindings}) != 1:
        raise EVS1999RealizationError("A/B/C source root divergence")
    if len({binding.source_specific_realization_identity for binding in bindings}) != 1:
        raise EVS1999RealizationError("A/B/C semantic realization divergence")
    return SOURCE_SPECIFIC_REALIZATION_IDENTITY


__all__ = [
    "APPLICABLE_EDGE_CLASSES",
    "CANONICAL_FILENAME",
    "CANONICAL_SHA256",
    "COMPATIBILITY_SEMANTIC_SCOPE",
    "CONTRACT_ID",
    "CandidateSemanticBinding",
    "DOCUMENTARY_ALIGNMENT_UNKNOWN",
    "DOCUMENTARY_AUTHORITY_CHAIN",
    "DocumentaryAlignment",
    "DocumentaryRoutingRule",
    "DocumentaryVariableEntry",
    "EVS1999RealizationError",
    "EXACT_READER_CONFIGURATION",
    "PHYSICAL_COMPATIBILITY_MODE",
    "PRODUCER_RELEASE_ID",
    "R35_HOOK_BINDING",
    "R35_REQUIRED_PHYSICAL_DIMENSIONS",
    "ROUTING_RULES",
    "SOURCE_SPECIFIC_REALIZATION_IDENTITY",
    "admit_physical_incidence",
    "align_documentary_semantics",
    "canonical_digest",
    "require_common_abc_semantic_law",
    "resolve_documentary_routing",
    "source_specific_realization_payload",
]
