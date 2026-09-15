"""Repo-native Q69B exact-source transport and bounded PRE553/C11 candidate.

N2 closes the source-byte transport seam without committing the accepted raw SAV.
The fixed committed transport contains only source row ordinal, exact respondent
binding, Q69B native/typed state, DATEINTR temporal-anchor material, and frozen
provenance.  No caller-selected path, source reacquisition, comparator, PSEPF,
actor mutation, or adoption occurs here.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import gzip
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Final, Iterable, Mapping

from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    RespondentEvent,
    RoutingEligibilityFact,
    canonical_json,
    semantic_hash,
)
import rawlsing_next.pre553_repo_native_current_payload as current_gt2
import rawlsing_next.wave1_r5_q86_c11_projection as q86


class R5Q69BProjectionError(Pre553IntegrityError):
    """The fixed Q69B transport or candidate release failed closed."""


TRANSPORT_SCHEMA: Final[str] = "GT34_N2_R5_Q69B_EXACT_SOURCE_TRANSPORT@1.0.0"
TRANSPORT_SEMANTIC_SHA256: Final[str] = (
    "c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5"
)
TRANSPORT_GZIP_SHA256: Final[str] = (
    "bbf256e01beef96d29a0a00517348d983ebfa718a320acc16787a9a3c59ab719"
)
TRANSPORT_GZIP_BYTES: Final[int] = 332_746
TRANSPORT_CANONICAL_BYTES: Final[int] = 5_275_419
SOURCE_SHA256: Final[str] = (
    "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
)
SOURCE_BYTES: Final[int] = 49_689_458
SOURCE_ROWS: Final[int] = 51_587
SOURCE_ARTIFACT_ID: Final[str] = "Data/Afro Barometer Round 5.sav"
CODEBOOK_SHA256: Final[str] = (
    "7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735"
)
QUESTION_TEXT_SHA256: Final[str] = (
    "d235a464e0b36db851134fe2ced54f9ccade94370c719ebdafe89cc14ab4ff9d"
)
ROUTING_NOTE_SHA256: Final[str] = (
    "62823c05f73b724d96fba327511bf1e82b4c3afd17ad0ad54dd36fe0e4c4cb20"
)
RESPONDENT_CARRIER_ID: Final[str] = "FFP014_R5_CURRENT_RESPONDENT_CARRIER@1"
RESPONDENT_CARRIER_SHA256: Final[str] = (
    "6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5"
)
SOURCE_STRUCTURE_ID: Final[str] = "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4"
SOURCE_STRUCTURE_SHA256: Final[str] = (
    "ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99"
)
ACCEPTED_UNIVERSE_SHA256: Final[str] = (
    "4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1"
)
PREDECESSOR_RELEASE_ID: Final[str] = "R5_GT12_Q86A_Q86B_FROZEN"
PREDECESSOR_RELEASE_SHA256: Final[str] = (
    "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295"
)
CANDIDATE_RELEASE_ID: Final[str] = "R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1"

REPAIRED_COORDINATE_AUTHORITY_ID: Final[str] = (
    "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY"
)
REPAIRED_COORDINATE_AUTHORITY_VERSION: Final[str] = "1.0.0"
REPAIRED_COORDINATE_AUTHORITY_SHA256: Final[str] = (
    "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
)
REJECTED_OVERBROAD_AUTHORITY_SHA256: Final[str] = (
    "3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a"
)
COORDINATE_SHA256: Final[str] = (
    "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937"
)
CROSSWALK_ID: Final[str] = "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK"
CROSSWALK_VERSION: Final[str] = "1.0.0"
CROSSWALK_SHA256: Final[str] = (
    "fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095"
)
TIME_RULE_ID: Final[str] = "R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR"
TIME_RULE_VERSION: Final[str] = "1.0.0"
TIME_RULE_SHA256: Final[str] = (
    "4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2"
)
MEASURE_BASIS_SHA256: Final[str] = (
    "f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3"
)
CURRENTNESS_REF: Final[ExactRef] = q86.CURRENTNESS_REF
SOURCE_REF: Final[ExactRef] = q86.FROZEN_BINDINGS.source_ref
RESPONDENT_CARRIER_REF: Final[ExactRef] = q86.FROZEN_BINDINGS.respondent_ref
SOURCE_STRUCTURE_REF: Final[ExactRef] = q86.FROZEN_BINDINGS.structure_ref
PREDECESSOR_RELEASE_REF: Final[ExactRef] = ExactRef(
    "C11LogicalRelease", PREDECESSOR_RELEASE_ID, PREDECESSOR_RELEASE_SHA256
)
CODEBOOK_REF: Final[ExactRef] = ExactRef(
    "INSTRUMENT_RELEASE",
    "merged_r5_codebook_2.pdf",
    CODEBOOK_SHA256,
)
CANONICAL_COORDINATE_REF: Final[ExactRef] = ExactRef(
    "COORDINATE_NATIVE",
    "Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS",
    COORDINATE_SHA256,
)
TRANSPORT_REF: Final[ExactRef] = ExactRef(
    "GT34_N2_Q69B_TRANSPORT",
    TRANSPORT_SCHEMA,
    TRANSPORT_SEMANTIC_SHA256,
)
MEASURE_BASIS_REF: Final[ExactRef] = ExactRef(
    "MEASURE_BASIS",
    "R5_Q69B_RAW_CONDITIONER_MEMBERSHIP_BASIS@1.0.0",
    MEASURE_BASIS_SHA256,
)

_TRANSPORT_RELATIVE: Final[Path] = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_Q69B_TRANSPORT_METABOLISM_TARGET_AUDIT_WAVE_R1/"
    "N2_Q69B_SOURCE_TRANSPORT_MATERIALIZATION_R1/transport/"
    "q69b_exact_source_transport.json.gz"
)

_Q69B_PHYSICAL_LABELS: Final[dict[str, str]] = {
    "-1": "Missing",
    "0": "Never",
    "1": "Once or Twice",
    "2": "A Few Times",
    "3": "Often",
    "7": "No experience with public clinics in past year",
    "9": "Don't Know",
    "998": "Refused",
}
_Q69B_TYPED_COUNTS: Final[dict[str, int]] = {
    "PUBLIC_CLINIC_EXPERIENCE_PRESENT": 42_656,
    "PUBLIC_CLINIC_EXPERIENCE_ABSENT": 8_554,
    "UNKNOWN": 298,
    "REFUSAL_NOT_LAWFULLY_CONDITIONABLE": 0,
    "MISSING": 79,
    "PHYSICAL_SYSTEM_MISSING": 0,
}
_Q69B_NATIVE_COUNTS: Final[dict[str, int]] = {
    "-1": 79, "0": 12_951, "1": 8_213, "2": 10_822, "3": 10_670,
    "7": 8_554, "9": 298, "998": 0, "SYSTEM_MISSING": 0,
}
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _fixed_transport_path() -> Path:
    return _repo_root() / _TRANSPORT_RELATIVE


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _eref(kind: str, object_id: str, material: Any) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


@dataclass(frozen=True)
class Q69BTransportRow:
    row_ordinal: int
    respondent_key: str
    q69b_native_code: int
    q69b_typed_state: str
    dateintr_raw_exact_token: str
    dateintr_iso: str
    dateintr_state: str

    @classmethod
    def from_wire(cls, wire: Any) -> "Q69BTransportRow":
        if not isinstance(wire, list) or len(wire) != 7:
            raise R5Q69BProjectionError("Q69B transport row schema mismatch")
        row, respondent, code, state, date_raw, date_iso, date_state = wire
        if not isinstance(row, int) or isinstance(row, bool) or row < 1:
            raise R5Q69BProjectionError("Q69B row ordinal invalid")
        if not isinstance(respondent, str) or respondent.count("|") != 1:
            raise R5Q69BProjectionError("respondent binding must be exact COUNTRY|RESPNO")
        if code is None:
            raise R5Q69BProjectionError(
                "N2 accepted transport has no physical-system-missing Q69B cells")
        if not isinstance(code, int) or isinstance(code, bool) or str(code) not in _Q69B_PHYSICAL_LABELS:
            raise R5Q69BProjectionError("undocumented Q69B native code")
        expected_state = {
            -1: "MISSING",
            0: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
            1: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
            2: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
            3: "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
            7: "PUBLIC_CLINIC_EXPERIENCE_ABSENT",
            9: "UNKNOWN",
            998: "REFUSAL_NOT_LAWFULLY_CONDITIONABLE",
        }[code]
        if state != expected_state:
            raise R5Q69BProjectionError("Q69B typed state does not match frozen code")
        if not isinstance(date_raw, str) or not date_raw:
            raise R5Q69BProjectionError("DATEINTR exact raw token missing")
        if not isinstance(date_iso, str) or not _DATE_RE.fullmatch(date_iso):
            raise R5Q69BProjectionError("DATEINTR ISO anchor invalid")
        if date_state != "VALID":
            raise R5Q69BProjectionError("N2 accepted transport requires valid DATEINTR")
        return cls(row, respondent, code, state, date_raw, date_iso, date_state)


@dataclass(frozen=True)
class Q69BTransport:
    raw: Mapping[str, Any]
    rows: tuple[Q69BTransportRow, ...]

    @property
    def semantic_hash(self) -> str:
        return TRANSPORT_SEMANTIC_SHA256


def _verify_transport_material(material: Any) -> Q69BTransport:
    if not isinstance(material, Mapping):
        raise R5Q69BProjectionError("transport root must be mapping")
    if material.get("schema_id") != TRANSPORT_SCHEMA:
        raise R5Q69BProjectionError("transport schema drift")
    source = material.get("source")
    if not isinstance(source, Mapping) or dict(source) != {
        "object_id": SOURCE_ARTIFACT_ID,
        "byte_count": SOURCE_BYTES,
        "sha256": SOURCE_SHA256,
        "rows": SOURCE_ROWS,
        "route": "OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION",
    }:
        raise R5Q69BProjectionError("transport source identity drift")
    provenance = material.get("provenance")
    expected_provenance = {
        "codebook_sha256": CODEBOOK_SHA256,
        "respondent_carrier_id": RESPONDENT_CARRIER_ID,
        "respondent_carrier_sha256": RESPONDENT_CARRIER_SHA256,
        "source_structure_id": SOURCE_STRUCTURE_ID,
        "source_structure_sha256": SOURCE_STRUCTURE_SHA256,
        "repaired_coordinate_authority_sha256": REPAIRED_COORDINATE_AUTHORITY_SHA256,
        "coordinate_sha256": COORDINATE_SHA256,
        "crosswalk_sha256": CROSSWALK_SHA256,
        "time_rule_sha256": TIME_RULE_SHA256,
        "measure_basis_sha256": MEASURE_BASIS_SHA256,
    }
    if not isinstance(provenance, Mapping) or dict(provenance) != expected_provenance:
        raise R5Q69BProjectionError("transport provenance drift")
    metadata = material.get("metadata")
    if not isinstance(metadata, Mapping):
        raise R5Q69BProjectionError("transport metadata missing")
    if metadata.get("q69b_physical_variable_label") != (
        "Q69b. Problems with public clinic: lack of medicine/supplies"
    ):
        raise R5Q69BProjectionError("Q69B physical variable label drift")
    if dict(metadata.get("q69b_physical_value_labels", {})) != _Q69B_PHYSICAL_LABELS:
        raise R5Q69BProjectionError("Q69B physical value dictionary drift")
    if metadata.get("q69b_original_variable_type") != "F3.0":
        raise R5Q69BProjectionError("Q69B physical type drift")
    if metadata.get("dateintr_variable_label") != "Date of interview":
        raise R5Q69BProjectionError("DATEINTR variable label drift")
    if metadata.get("dateintr_original_variable_type") != "EDATE8":
        raise R5Q69BProjectionError("DATEINTR physical type drift")
    if metadata.get("q69b_missing_ranges") != [] or metadata.get("dateintr_missing_ranges") != []:
        raise R5Q69BProjectionError("unexpected SPSS user-missing declaration")
    counts = material.get("counts")
    if not isinstance(counts, Mapping):
        raise R5Q69BProjectionError("transport counts missing")
    if dict(counts.get("q69b_native", {})) != _Q69B_NATIVE_COUNTS:
        raise R5Q69BProjectionError("Q69B native counts drift")
    if dict(counts.get("q69b_typed", {})) != _Q69B_TYPED_COUNTS:
        raise R5Q69BProjectionError("Q69B typed counts drift")
    if dict(counts.get("dateintr", {})) != {"VALID": SOURCE_ROWS, "MISSING": 0, "INVALID": 0}:
        raise R5Q69BProjectionError("DATEINTR counts drift")
    if counts.get("dateintr_min_iso") != "2011-10-20" or counts.get("dateintr_max_iso") != "2013-06-04":
        raise R5Q69BProjectionError("DATEINTR range drift")
    binding = material.get("respondent_binding")
    if not isinstance(binding, Mapping) or dict(binding) != {
        "law": "COUNTRY_TEXT_PIPE_RESPNO_TEXT",
        "current_q86_contract_compatible": True,
        "unique_keys": SOURCE_ROWS,
        "rows": SOURCE_ROWS,
    }:
        raise R5Q69BProjectionError("respondent binding law drift")
    wires = material.get("rows")
    if not isinstance(wires, list) or len(wires) != SOURCE_ROWS:
        raise R5Q69BProjectionError("transport row count drift")
    rows = tuple(Q69BTransportRow.from_wire(wire) for wire in wires)
    if tuple(row.row_ordinal for row in rows) != tuple(range(1, SOURCE_ROWS + 1)):
        raise R5Q69BProjectionError("transport row ordinals do not cover source exactly")
    if len({row.respondent_key for row in rows}) != SOURCE_ROWS:
        raise R5Q69BProjectionError("transport respondent key collision")
    return Q69BTransport(material, rows)


def _rehydrate_verified_transport(compressed: bytes) -> Q69BTransport:
    if len(compressed) != TRANSPORT_GZIP_BYTES or _sha256(compressed) != TRANSPORT_GZIP_SHA256:
        raise R5Q69BProjectionError("Q69B committed gzip identity mismatch")
    canonical = gzip.decompress(compressed)
    if len(canonical) != TRANSPORT_CANONICAL_BYTES or _sha256(canonical) != TRANSPORT_SEMANTIC_SHA256:
        raise R5Q69BProjectionError("Q69B transport semantic identity mismatch")
    material = json.loads(canonical)
    if canonical_json(material).encode("utf-8") != canonical:
        raise R5Q69BProjectionError("Q69B transport bytes are not canonical semantic JSON")
    return _verify_transport_material(material)


def load_q69b_transport() -> Q69BTransport:
    """Load only the fixed repo-native N2 transport; no caller-selected source/path."""
    return _rehydrate_verified_transport(_fixed_transport_path().read_bytes())


def _accepted_universe() -> tuple[EmpiricalUniverse, AuthoritySnapshot]:
    source_auth = q86._authorities(q86.FROZEN_BINDINGS)[0]
    b = q86.FROZEN_BINDINGS
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(b.source_ref, b.respondent_ref, b.structure_ref, CURRENTNESS_REF),
        producer_replay_locator_or_reference_root=_eref(
            "REPLAY_ROOT",
            "GT12:R5:Q86:UNIVERSE",
            {
                "source": b.source_ref.as_dict(),
                "respondents": b.respondent_ref.as_dict(),
                "currentness": CURRENTNESS_REF.as_dict(),
            },
        ),
        raw_source_identity=b.source_artifact_id,
        source_family="Afrobarometer",
        study_product_release="Afrobarometer/R5",
        instrument_release=f"merged_r5_codebook_2.pdf@sha256:{b.codebook_sha256}",
        country_geography="AFROBAROMETER_R5_SOURCE_NATIVE_MULTI_COUNTRY",
        sampling_geography="AFROBAROMETER_R5_SOURCE_NATIVE_SAMPLE_SCOPE",
        raw_wave="R5",
        canonical_wave_if_governed="R5",
        field_or_reference_time="AFROBAROMETER_ROUND_5_SOURCE_NATIVE",
        target_population_and_sample_frame="SOURCE_NATIVE_R5_SAMPLE_FRAME__NO_POPULATION_GENERALIZATION_BY_GT12",
        sampling_design_regime="SOURCE_NATIVE_R5__RAW_UNWEIGHTED_GT12_USE",
        respondent_namespace=b.respondent_carrier_id,
        source_artifact_import_lineage=(
            f"source:{b.source_sha256}|respondents:{b.respondent_carrier_sha256}|"
            f"responses:{b.response_fact_carrier_sha256}|exposure:{b.exposure_fact_carrier_sha256}"
        ),
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    if universe.content_hash != ACCEPTED_UNIVERSE_SHA256:
        raise R5Q69BProjectionError("accepted R5 empirical universe reconstruction drift")
    return universe, source_auth


def _candidate_authority(
    *,
    authority_id: str,
    kind: str,
    operations: Iterable[str],
    families: Iterable[str],
    scope: Mapping[str, Any],
    dependencies: Iterable[ExactRef],
    fixed_content_hash: str | None = None,
) -> AuthoritySnapshot:
    operations = tuple(sorted(set(operations)))
    families = tuple(sorted(set(families)))
    deps = tuple(sorted(set(dependencies), key=lambda ref: ref.key))
    material = {
        "contract": "GT34_N2_Q69B_BOUNDED_C11_MATERIALIZATION@1.0.0",
        "id": authority_id,
        "version": "1.0.0",
        "kind": kind,
        "operations": operations,
        "families": families,
        "scope": scope,
        "dependencies": [ref.as_dict() for ref in deps],
    }
    authority_hash = fixed_content_hash or semantic_hash(material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=_eref(
            "AUTHORITY_REPLAY_ROOT", f"{authority_id}:N2", material
        ),
        authority_id=authority_id,
        authority_version="1.0.0",
        authority_content_hash=authority_hash,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=operations,
        governed_object_families=families,
        scope_envelope=scope,
        effective_time_or_interval="GT34_N2_Q69B_CANDIDATE_ONLY__NO_ADOPTION",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(
            {"material": material, "candidate_only": True, "no_widening": True}
        ),
        replay_protocol_ref=q86.REPLAY_PROTOCOL_REF,
    )


def _respondents(transport: Q69BTransport, universe: EmpiricalUniverse) -> tuple[RespondentIdentity, ...]:
    respondents = []
    for row in transport.rows:
        country, respno = row.respondent_key.split("|", 1)
        source_native_ref = _eref(
            "SOURCE_RESPONDENT",
            f"{RESPONDENT_CARRIER_ID}:{row.respondent_key}",
            {
                "carrier": RESPONDENT_CARRIER_REF.as_dict(),
                "COUNTRY": country,
                "RESPNO": respno,
            },
        )
        respondents.append(
            RespondentIdentity(
                empirical_universe_ref=universe.ref,
                respondent_key=row.respondent_key,
                source_native_respondent_key_ref_or_typed_absence=source_native_ref,
                identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            )
        )
    return tuple(respondents)


def current_gt2_respondent_subset_match_count(respondents: tuple[RespondentIdentity, ...]) -> int:
    """Prove exact compatibility with all 19,210 current GT2 respondent refs."""
    _, payloads = current_gt2._read_committed_transport()
    current_refs = current_gt2._decode_exact_ref_hashes(
        "respondent_refs", payloads["respondent_refs"]
    )
    candidate_hashes = {respondent.content_hash for respondent in respondents}
    matched = sum(ref.content_hash in candidate_hashes for ref in current_refs)
    if matched != len(current_refs):
        raise R5Q69BProjectionError(
            f"current GT2 respondent exact-ref subset mismatch {matched}/{len(current_refs)}"
        )
    return matched


def _authority_bundle(
    transport: Q69BTransport,
    universe: EmpiricalUniverse,
    accepted_source_auth: AuthoritySnapshot,
) -> tuple[AuthoritySnapshot, ...]:
    metadata = transport.raw["metadata"]
    physical_domain_ref = _eref(
        "SOURCE_NATIVE_VALUE_DOMAIN",
        "Afrobarometer/R5:Q69B:PHYSICAL_VALUE_LABEL_DICTIONARY",
        {
            "physical_variable_label": metadata["q69b_physical_variable_label"],
            "physical_variable_label_sha256": metadata["q69b_physical_variable_label_sha256"],
            "physical_value_labels": metadata["q69b_physical_value_labels"],
            "physical_value_label_hashes": metadata["q69b_physical_value_label_hashes"],
            "original_variable_type": metadata["q69b_original_variable_type"],
        },
    )
    native_question_ref = _eref(
        "QUESTION_IMPLEMENTATION",
        "Afrobarometer/R5:Q69B",
        {
            "source": SOURCE_REF.as_dict(),
            "physical_domain": physical_domain_ref.as_dict(),
            "codebook_sha256": CODEBOOK_SHA256,
        },
    )
    common_deps = (
        SOURCE_REF, RESPONDENT_CARRIER_REF, SOURCE_STRUCTURE_REF, CURRENTNESS_REF,
        TRANSPORT_REF, native_question_ref, physical_domain_ref,
    )
    source_auth = _candidate_authority(
        authority_id="GT34-N2-R5-Q69B-SOURCE-SEMANTICS",
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        operations=("R5_Q69B_SOURCE_NATIVE_RESPONSE_SEMANTICS_REEXPRESSION",),
        families=("RespondentEvent@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "question_ref": native_question_ref,
            "physical_domain_ref": physical_domain_ref,
            "frequency_order_is_metric_authority": False,
            "currentness_ref": CURRENTNESS_REF,
        },
        dependencies=common_deps,
    )
    routing_auth = _candidate_authority(
        authority_id="GT34-N2-R5-Q69B-ROUTING",
        kind="ROUTING_RISK_SET",
        operations=("R5_Q69B_ALL_SOURCE_ROWS_INSTRUMENT_APPLICABILITY",),
        families=("RoutingEligibilityFact@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "question_ref": native_question_ref,
            "rule": "ALL_51587_SOURCE_ROWS_HAVE_Q69B_PHYSICAL_CELL__MISSING_IS_TYPED_VALUE_NOT_NOT_ASKED",
            "currentness_ref": CURRENTNESS_REF,
        },
        dependencies=common_deps,
    )
    coordinate_auth = _candidate_authority(
        authority_id=REPAIRED_COORDINATE_AUTHORITY_ID,
        kind="COORDINATE_SEMANTICS",
        operations=("R5_Q69B_SOURCE_NATIVE_PUBLIC_CLINIC_EXPERIENCE_D08_CONDITIONER",),
        families=("EmpiricalCoordinateFact@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "source_family": "Afrobarometer",
            "study_product_release": "Afrobarometer/R5",
            "instrument_release": f"merged_r5_codebook_2.pdf@sha256:{CODEBOOK_SHA256}",
            "empirical_universe_ref": universe.ref,
            "respondent_ref": RESPONDENT_CARRIER_REF,
            "coordinate_ref": CANONICAL_COORDINATE_REF,
            "currentness_ref": CURRENTNESS_REF,
            "logical_release_predecessor": PREDECESSOR_RELEASE_REF,
            "logical_release_law": (
                "Q69B_NOT_IN_Q86_PREDECESSOR__NEW_BOUNDED_RELEASE_REQUIRED__"
                "PREDECESSOR_IMMUTABLE"
            ),
            "d08_use": "CONDITIONER_ONLY__NO_STRUCTURAL_POSITION__NO_ACTOR_FACT_PROMOTION",
            "portability": "NONE",
        },
        dependencies=(
            SOURCE_REF, RESPONDENT_CARRIER_REF, CURRENTNESS_REF, TRANSPORT_REF,
            CANONICAL_COORDINATE_REF, PREDECESSOR_RELEASE_REF,
        ),
        fixed_content_hash=REPAIRED_COORDINATE_AUTHORITY_SHA256,
    )
    crosswalk_auth = _candidate_authority(
        authority_id=CROSSWALK_ID,
        kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        operations=("R5_Q69B_NATIVE_CODE_TO_PUBLIC_CLINIC_EXPERIENCE_STATUS",),
        families=("EmpiricalCoordinateFact@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "coordinate_ref": CANONICAL_COORDINATE_REF,
            "native_variable": "Q69B",
            "question_text_sha256": QUESTION_TEXT_SHA256,
            "routing_note_sha256": ROUTING_NOTE_SHA256,
            "codebook_sha256": CODEBOOK_SHA256,
            "codebook_normalized_variable_label_sha256":
                metadata["q69b_codebook_normalized_variable_label_sha256"],
            "codebook_normalized_value_label_hashes":
                metadata["q69b_codebook_normalized_value_label_hashes"],
            "map": {
                "0": "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
                "1": "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
                "2": "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
                "3": "PUBLIC_CLINIC_EXPERIENCE_PRESENT",
                "7": "PUBLIC_CLINIC_EXPERIENCE_ABSENT",
                "9": "UNKNOWN",
                "998": "REFUSAL_NOT_LAWFULLY_CONDITIONABLE",
                "-1": "MISSING",
            },
            "frequency_order_discarded": True,
            "source_specific_law_only": True,
            "named_problem_occurrence_not_promoted_to_actor_history": True,
            "portability": "NONE",
        },
        dependencies=(SOURCE_REF, TRANSPORT_REF, CANONICAL_COORDINATE_REF),
        fixed_content_hash=CROSSWALK_SHA256,
    )
    temporal_auth = _candidate_authority(
        authority_id=TIME_RULE_ID,
        kind="TEMPORAL_EVIDENCE",
        operations=("R5_Q69B_DATEINTR_PAST_12_MONTHS_ANCHOR",),
        families=("EmpiricalCoordinateFact@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "anchor_variable": "DATEINTR",
            "source_native_interval": "PAST_12_MONTHS",
            "query_time_substitution": "FORBIDDEN",
            "wall_clock_substitution": "FORBIDDEN",
            "actor_current_time_substitution": "FORBIDDEN",
            "invented_edge_inclusion": "FORBIDDEN",
            "edge_inclusion_if_disputed": "NONCOMPARABLE_UNTIL_SEPARATE_AUTHORITY",
        },
        dependencies=(SOURCE_REF, TRANSPORT_REF),
        fixed_content_hash=TIME_RULE_SHA256,
    )
    projection_auth = _candidate_authority(
        authority_id="GT34-N2-R5-Q69B-C11-REEXPRESSION",
        kind="SOURCE_SEMANTICS_TOPOLOGY",
        operations=("R5_Q69B_EXACT_REPO_NATIVE_TRANSPORT_TO_C11_CANDIDATE",),
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"),
        scope={
            "source_ref": SOURCE_REF,
            "transport_ref": TRANSPORT_REF,
            "predecessor_release_ref": PREDECESSOR_RELEASE_REF,
            "predecessor_mutated": False,
            "currentness_ref": CURRENTNESS_REF,
        },
        dependencies=(SOURCE_REF, TRANSPORT_REF, PREDECESSOR_RELEASE_REF, CURRENTNESS_REF),
    )
    replay_auth = _candidate_authority(
        authority_id="GT34-N2-R5-Q69B-C11-REPLAY",
        kind="REPLAY_PROTOCOL",
        operations=("R5_Q69B_REPO_NATIVE_TRANSPORT_DETERMINISTIC_C11_REPLAY",),
        families=("ReplayReceipt@1.0.0",),
        scope={
            "source_ref": SOURCE_REF,
            "transport_ref": TRANSPORT_REF,
            "transport_semantic_sha256": TRANSPORT_SEMANTIC_SHA256,
            "transport_gzip_sha256": TRANSPORT_GZIP_SHA256,
            "currentness_ref": CURRENTNESS_REF,
        },
        dependencies=(SOURCE_REF, TRANSPORT_REF, CURRENTNESS_REF),
    )
    return (
        accepted_source_auth,
        source_auth, routing_auth, coordinate_auth, crosswalk_auth,
        temporal_auth, projection_auth, replay_auth,
    )


def _source_response_state(row: Q69BTransportRow) -> str:
    if row.q69b_native_code in {0, 1, 2, 3, 7}:
        return "SUBSTANTIVE_RESPONSE"
    if row.q69b_native_code == 9:
        return "DK"
    if row.q69b_native_code == 998:
        return "REFUSAL"
    if row.q69b_native_code == -1:
        return "MISSING"
    raise R5Q69BProjectionError("unreachable Q69B response code")


def _candidate_from_transport(transport: Q69BTransport) -> C11SourceReleaseCandidate:
    universe, accepted_source_auth = _accepted_universe()
    respondents = _respondents(transport, universe)
    current_gt2_respondent_subset_match_count(respondents)
    by_key = {respondent.respondent_key: respondent for respondent in respondents}
    authorities = _authority_bundle(transport, universe, accepted_source_auth)
    (
        _accepted_source_auth, source_auth, routing_auth, coordinate_auth,
        crosswalk_auth, temporal_auth, projection_auth, replay_auth,
    ) = authorities

    metadata = transport.raw["metadata"]
    physical_domain_ref = _eref(
        "SOURCE_NATIVE_VALUE_DOMAIN",
        "Afrobarometer/R5:Q69B:PHYSICAL_VALUE_LABEL_DICTIONARY",
        {
            "physical_variable_label": metadata["q69b_physical_variable_label"],
            "physical_variable_label_sha256": metadata["q69b_physical_variable_label_sha256"],
            "physical_value_labels": metadata["q69b_physical_value_labels"],
            "physical_value_label_hashes": metadata["q69b_physical_value_label_hashes"],
            "original_variable_type": metadata["q69b_original_variable_type"],
        },
    )
    native_question_ref = _eref(
        "QUESTION_IMPLEMENTATION",
        "Afrobarometer/R5:Q69B",
        {"source": SOURCE_REF.as_dict(), "physical_domain": physical_domain_ref.as_dict(),
         "codebook_sha256": CODEBOOK_SHA256},
    )
    topology_ref = _eref(
        "RESPONSE_TOPOLOGY",
        "Afrobarometer:R5:Q69B:SCALAR_SINGULAR",
        {"variable": "Q69B", "kind": "SCALAR_SINGULAR", "numeric_order_authorized": False},
    )
    native_coordinate_ref = _eref(
        "COORDINATE_NATIVE",
        "Afrobarometer/R5:Q69B:SOURCE_NATIVE",
        {"question_ref": native_question_ref.as_dict(), "physical_domain_ref": physical_domain_ref.as_dict()},
    )
    unit_ref = _eref(
        "UNIT_TAXONOMY",
        "SOURCE_NATIVE_Q69B_PUBLIC_CLINIC_EXPERIENCE_CODE_DOMAIN",
        {"physical_domain_ref": physical_domain_ref.as_dict(), "categorical": True, "metric": False},
    )

    question_binding = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=native_question_ref,
        instrument_question_version="Afrobarometer_R5",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )

    risk_set_ref = _eref(
        "RISK_SET",
        "GT34_N2_R5_Q69B_ALL_SOURCE_RESPONDENTS@1",
        {
            "source": SOURCE_REF.as_dict(),
            "respondent_refs": [respondent.ref.as_dict() for respondent in respondents],
            "rule": "ALL_SOURCE_ROWS_Q69B_PHYSICAL_CELL_PRESENT",
        },
    )
    routing_rule_ref = _eref(
        "ROUTING_RULE",
        "GT34_N2:R5:Q69B:ALL_SOURCE_ROWS",
        {"risk_set_ref": risk_set_ref.as_dict(), "authority_ref": routing_auth.authority_ref.as_dict()},
    )
    member_replay_ref = _eref(
        "MEMBER_SET_REPLAY",
        "GT34_N2_R5_Q69B_ALL_SOURCE_RESPONDENTS@1:REPLAY",
        {"risk_set_ref": risk_set_ref.as_dict(), "transport_ref": TRANSPORT_REF.as_dict()},
    )

    events = []
    routing = []
    coordinates = []
    for row in transport.rows:
        respondent = by_key[row.respondent_key]
        event_material = {
            "transport_ref": TRANSPORT_REF.as_dict(),
            "row_ordinal": row.row_ordinal,
            "respondent_ref": respondent.ref.as_dict(),
            "question_ref": native_question_ref.as_dict(),
            "q69b_native_code": row.q69b_native_code,
        }
        group_hash = semantic_hash({**event_material, "role": "GROUP"})
        event_hash = semantic_hash({**event_material, "role": "EVENT"})
        events.append(
            RespondentEvent(
                typed_state=_source_response_state(row),
                authority_snapshot_refs=(projection_auth.authority_ref, source_auth.authority_ref),
                dependency_refs=(SOURCE_REF, TRANSPORT_REF, respondent.ref, native_question_ref),
                producer_replay_locator_or_reference_root=_eref(
                    "REPLAY_ROOT", f"GT34:N2:R5:Q69B:EVENT:{row.row_ordinal}", event_material
                ),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_question_ref=native_question_ref,
                canonical_question_ref_if_authorized=None,
                component_or_subitem_ref=None,
                event_group_id=f"urn:rawlsing:pre553:n2:q69b:event-group:sha256:{group_hash}",
                response_event_id_or_deterministic_index=(
                    f"urn:rawlsing:pre553:n2:q69b:event:sha256:{event_hash}"
                ),
                raw_response_value=row.q69b_native_code,
                canonical_response_value_if_authorized=None,
                value_transform_authority_ref=None,
                response_topology_ref=topology_ref,
                multiplicity_order_rank_fields={"kind": "SCALAR_SINGULAR", "index": 0},
                response_state=_source_response_state(row),
            )
        )
        routing.append(
            RoutingEligibilityFact(
                typed_state="ELIGIBLE_APPLICABLE",
                authority_snapshot_refs=(projection_auth.authority_ref, routing_auth.authority_ref),
                dependency_refs=(SOURCE_REF, TRANSPORT_REF, respondent.ref, native_question_ref),
                producer_replay_locator_or_reference_root=_eref(
                    "REPLAY_ROOT",
                    f"GT34:N2:R5:Q69B:ROUTING:{row.row_ordinal}",
                    {"row": row.row_ordinal, "respondent": respondent.ref.as_dict(),
                     "risk_set": risk_set_ref.as_dict()},
                ),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=native_question_ref,
                risk_set_ref=risk_set_ref,
                routing_rule_ref=routing_rule_ref,
                applicability_state="ELIGIBLE_APPLICABLE",
                routing_state="ELIGIBLE_APPLICABLE",
                parent_predicate_refs=(),
                member_set_replay_ref=member_replay_ref,
            )
        )

        observed = row.q69b_typed_state in {
            "PUBLIC_CLINIC_EXPERIENCE_PRESENT", "PUBLIC_CLINIC_EXPERIENCE_ABSENT"
        }
        if observed:
            coord_state = "OBSERVED_COORDINATE"
            canonical_value: str | None = row.q69b_typed_state
        elif row.q69b_typed_state == "UNKNOWN":
            coord_state = "UNKNOWN"
            canonical_value = None
        elif row.q69b_typed_state == "REFUSAL_NOT_LAWFULLY_CONDITIONABLE":
            coord_state = "NOT_LAWFULLY_CONDITIONABLE"
            canonical_value = None
        elif row.q69b_typed_state == "MISSING":
            coord_state = "MISSING"
            canonical_value = None
        else:
            raise R5Q69BProjectionError("unsupported typed Q69B transport state")

        coordinate_material = {
            "transport_ref": TRANSPORT_REF.as_dict(),
            "row_ordinal": row.row_ordinal,
            "respondent_ref": respondent.ref.as_dict(),
            "native_code": row.q69b_native_code,
            "typed_state": row.q69b_typed_state,
            "dateintr_raw": row.dateintr_raw_exact_token,
            "dateintr_iso": row.dateintr_iso,
            "codebook_ref": CODEBOOK_REF.as_dict(),
            "crosswalk_ref": crosswalk_auth.authority_ref.as_dict(),
            "time_rule_ref": temporal_auth.authority_ref.as_dict(),
            "coordinate_authority_ref": coordinate_auth.authority_ref.as_dict(),
            "currentness_ref": CURRENTNESS_REF.as_dict(),
            "measure_basis_ref": MEASURE_BASIS_REF.as_dict(),
        }
        coordinates.append(
            EmpiricalCoordinateFact(
                typed_state=coord_state,
                authority_snapshot_refs=(
                    projection_auth.authority_ref,
                    coordinate_auth.authority_ref,
                    crosswalk_auth.authority_ref,
                    temporal_auth.authority_ref,
                ),
                dependency_refs=(
                    SOURCE_REF,
                    CODEBOOK_REF,
                    TRANSPORT_REF,
                    CURRENTNESS_REF,
                    MEASURE_BASIS_REF,
                    CANONICAL_COORDINATE_REF,
                    respondent.ref,
                    native_question_ref,
                ),
                producer_replay_locator_or_reference_root=_eref(
                    "REPLAY_ROOT",
                    f"GT34:N2:R5:Q69B:COORDINATE:{row.row_ordinal}",
                    coordinate_material,
                ),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_coordinate_ref=native_coordinate_ref,
                canonical_coordinate_ref_if_authorized=CANONICAL_COORDINATE_REF,
                raw_coordinate_value=row.q69b_native_code,
                canonical_coordinate_value_if_authorized=canonical_value,
                unit_category_taxonomy_ref=unit_ref,
                effective_or_reference_time=row.dateintr_iso,
                coordinate_state=coord_state,
                normalization_crosswalk_authority_ref=crosswalk_auth.authority_ref,
                source_semantic_authority_ref=coordinate_auth.authority_ref,
            )
        )

    events = tuple(events)
    routing = tuple(routing)
    coordinates = tuple(coordinates)
    counts = {
        "EmpiricalUniverse": 1,
        "RespondentIdentity": len(respondents),
        "QuestionVariableBinding": 1,
        "RespondentEvent": len(events),
        "RoutingEligibilityFact": len(routing),
        "EmpiricalCoordinateFact": len(coordinates),
        "AuthoritySnapshot": len(authorities),
    }
    source_manifest = SourceReleaseManifest(
        source_artifact_id=SOURCE_ARTIFACT_ID,
        source_artifact_content_hash=SOURCE_SHA256,
        source_family_id="Afrobarometer",
        study_product_id="Afrobarometer",
        release_id=CANDIDATE_RELEASE_ID,
        instrument_release_id=f"merged_r5_codebook_2.pdf@sha256:{CODEBOOK_SHA256}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(
            sorted((authority.authority_ref for authority in authorities), key=lambda ref: ref.key)
        ),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=SOURCE_REF,
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=source_manifest,
        empirical_universes=(universe,),
        respondent_identities=respondents,
        question_variable_bindings=(question_binding,),
        respondent_events=events,
        routing_eligibility_facts_or_exact_rules=routing,
        empirical_coordinate_facts=coordinates,
        weight_measure_facts_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        authority_snapshots=authorities,
        source_universe_relations_or_explicit_distinct_default=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence("NOT_APPLICABLE"),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=replay_auth.authority_ref,
        deterministic_tie_order_rules_ref=q86.TIE_ORDER_REF,
        replay_protocol_version="1.0.0",
    )
    return replace(candidate, candidate_replay_manifest=replay)


def build_q69b_bounded_c11_candidate_release():
    """Materialize and completely validate one new immutable candidate release."""
    candidate = _candidate_from_transport(load_q69b_transport())
    release = validate_c11_source_release(candidate)
    if release.release_id != CANDIDATE_RELEASE_ID:
        raise R5Q69BProjectionError("candidate release ID drift")
    if release.source_artifact_ref.content_hash != SOURCE_SHA256:
        raise R5Q69BProjectionError("candidate release source identity drift")
    return release


def q69b_candidate_identity_report() -> Mapping[str, Any]:
    transport = load_q69b_transport()
    release = build_q69b_bounded_c11_candidate_release()
    coordinate_facts = tuple(
        obj for obj in release.public_objects if isinstance(obj, EmpiricalCoordinateFact)
    )
    coordinate_states: dict[str, int] = {}
    canonical_values: dict[str, int] = {}
    for fact in coordinate_facts:
        coordinate_states[fact.coordinate_state] = coordinate_states.get(fact.coordinate_state, 0) + 1
        value = fact.canonical_coordinate_value_if_authorized
        key = "NONE" if value is None else str(value)
        canonical_values[key] = canonical_values.get(key, 0) + 1
    respondents = tuple(
        record for record in release.internal_records if isinstance(record, RespondentIdentity)
    )
    return {
        "transport_semantic_sha256": TRANSPORT_SEMANTIC_SHA256,
        "transport_gzip_sha256": TRANSPORT_GZIP_SHA256,
        "transport_rows": len(transport.rows),
        "source_sha256": SOURCE_SHA256,
        "respondent_count": len(respondents),
        "current_gt2_exact_respondent_subset_matches":
            current_gt2_respondent_subset_match_count(respondents),
        "coordinate_fact_count": len(coordinate_facts),
        "coordinate_states": dict(sorted(coordinate_states.items())),
        "canonical_values": dict(sorted(canonical_values.items())),
        "release_id": release.release_id,
        "release_semantic_sha256": release.semantic_release_hash,
        "release_manifest_sha256": release.source_release_manifest_hash,
        "release_replay_ref": release.replay_manifest.ref.as_dict(),
        "repaired_coordinate_authority_sha256": REPAIRED_COORDINATE_AUTHORITY_SHA256,
        "rejected_overbroad_authority_present": any(
            isinstance(obj, AuthoritySnapshot)
            and obj.authority_content_hash == REJECTED_OVERBROAD_AUTHORITY_SHA256
            for obj in release.public_objects
        ),
        "predecessor_release_ref": PREDECESSOR_RELEASE_REF.as_dict(),
        "measure_basis_ref": MEASURE_BASIS_REF.as_dict(),
    }


__all__ = [
    "R5Q69BProjectionError",
    "TRANSPORT_SCHEMA", "TRANSPORT_SEMANTIC_SHA256", "TRANSPORT_GZIP_SHA256",
    "SOURCE_SHA256", "SOURCE_ROWS", "CANDIDATE_RELEASE_ID",
    "REPAIRED_COORDINATE_AUTHORITY_SHA256", "REJECTED_OVERBROAD_AUTHORITY_SHA256",
    "Q69BTransportRow", "Q69BTransport", "load_q69b_transport",
    "current_gt2_respondent_subset_match_count",
    "build_q69b_bounded_c11_candidate_release", "q69b_candidate_identity_report",
]
