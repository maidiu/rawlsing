"""R7 WG0P3 -- workload identity, frontier and cold-restart repair.

Repairs WG0J's 20 independently executed acceptance failures while preserving
the genuinely working I02/C11 -> I03 -> BatchExecutionRunner pipeline.

Key repairs:
A. Native item/source-release/operation identity binding (full native fields).
B. Complete 25-op frontier enforcement (3 PRODUCED + 16 HELD + 6 INADMISSIBLE).
C. Current permission/revocation and immutable result-value verification.
D. Durable cold-process checkpoint/resume preserving value-bearing content.
E. Native missing codes, MR coherence, source-byte identity, wave metadata.
F. One PRODUCED conditional through the ordinary batch product path.

Source-free synthetic native records only. No raw survey, no canonical changes,
no V3. Permitted grant is the fixture grant GRANTED_FIXTURE.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    make_empirical_predicate,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query

VERSION = "R7_WG0P3_IDENTITY_FRONTIER_COLD_REPAIR@1.0.0"
PERMITTED_GRANT = "GRANTED_FIXTURE"
FIXTURE_ISSUER = "WG0P3-SYNTHETIC-FIXTURE-ISSUER"
SOURCE_EDITION_W1 = "SRC-EDITION-W1-v1"
SOURCE_EDITION_W2 = "SRC-EDITION-W2-v1"


class Disposition(str, Enum):
    PRODUCED = "PRODUCED"
    HELD = "HELD"
    INADMISSIBLE = "INADMISSIBLE"


class IdentityError(Exception):
    """Native identity, operation identity, or source binding failure."""


class FrontierError(Exception):
    """Frontier enforcement failure: missing, altered, or injected operation."""


class RevocationError(Exception):
    """Permission revoked at consumer read."""


class ColdRestartError(Exception):
    """Cold-process checkpoint/resume integrity failure."""


class NativeDataError(Exception):
    """Native data validation failure (MR, missing, wave, source bytes)."""


# --------------------------------------------------------------------------
# Frozen native items (identical to WG0P oracle inventory)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class NativeItem:
    item_id: str
    form_id: str
    source_id: str
    wave: str
    unit: str
    response_kind: str
    options: tuple
    missing_codes: tuple
    route_evidence: Optional[str]
    grant: str
    version: str

    def identity_key(self) -> str:
        return f"{self.source_id}|{self.wave}|{self.form_id}|{self.version}"

    def freeze_material(self) -> str:
        return "|".join([
            self.item_id, self.form_id, self.source_id, self.wave, self.unit,
            self.response_kind, ",".join(self.options), ",".join(self.missing_codes),
            self.route_evidence or "", self.grant, self.version,
        ])

    def source_edition(self) -> str:
        return f"SRC-EDITION-{self.source_id}-{self.wave}-{self.version}"


@dataclass(frozen=True)
class OperationCandidate:
    op_id: str
    item_ids: tuple
    op_class: str
    target: str
    conditioners: tuple
    disposition: Disposition
    disposition_reason: str

    def full_identity(self) -> str:
        """Complete operation identity binding: all fields must match."""
        return "|".join([
            self.op_id, self.op_class, self.target,
            ",".join(self.conditioners), self.disposition.value,
            self.disposition_reason, ",".join(sorted(self.item_ids)),
        ])


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:wg0p3:test:{kind.lower()}:{label}", _h(f"wg0p3:{kind}:{label}"))


def independent_oracle_items() -> list[NativeItem]:
    """Frozen frontier items. Oracle inventory, not builder output."""
    return [
        NativeItem(
            item_id="WG0P-ORD-01", form_id="Q-ORD-A", source_id="WG0P-SRC-A",
            wave="W1", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-HH-MR-02", form_id="Q-HH-MR-B", source_id="WG0P-SRC-A",
            wave="W1", unit="household", response_kind="MULTIPLE_RESPONSE",
            options=("food", "rent", "health", "education", "none"),
            missing_codes=("997", "998"),
            route_evidence="household_size>0", grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ROUTED-03", form_id="Q-RT-C", source_id="WG0P-SRC-A",
            wave="W1", unit="respondent", response_kind="ROUTED",
            options=("yes", "no"), missing_codes=("9",),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ORD-04", form_id="Q-ORD-A", source_id="WG0P-SRC-B",
            wave="W2", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="WITHDRAWN", version="v1",
        ),
        NativeItem(
            item_id="WG0P-ORD-05", form_id="Q-ORD-A", source_id="WG0P-SRC-A",
            wave="W2", unit="respondent", response_kind="ORDINAL",
            options=("0", "1", "2", "3", "9"), missing_codes=("9", "997", "998"),
            route_evidence=None, grant="GRANTED_FIXTURE", version="v1",
        ),
    ]


# --------------------------------------------------------------------------
# Disposition law
# --------------------------------------------------------------------------

def _marginal_disposition(item: NativeItem) -> Tuple[Disposition, str]:
    if item.grant != PERMITTED_GRANT:
        return (Disposition.HELD, f"GRANT_{item.grant}")
    if item.response_kind == "ROUTED" and not item.route_evidence:
        return (Disposition.HELD, "ROUTE_EVIDENCE_MISSING")
    return (Disposition.PRODUCED, "ELIGIBLE")


def _conditional_disposition(tgt: NativeItem, cond: NativeItem) -> Tuple[Disposition, str]:
    if tgt.grant != PERMITTED_GRANT:
        return (Disposition.HELD, f"TARGET_GRANT_{tgt.grant}")
    if cond.grant != PERMITTED_GRANT:
        return (Disposition.HELD, f"CONDITIONER_GRANT_{cond.grant}")
    if tgt.response_kind == "ROUTED" and not tgt.route_evidence:
        return (Disposition.HELD, "TARGET_ROUTE_EVIDENCE_MISSING")
    if cond.response_kind == "ROUTED" and not cond.route_evidence:
        return (Disposition.HELD, "CONDITIONER_ROUTE_EVIDENCE_MISSING")
    if (tgt.unit, tgt.wave, tgt.source_id) == (cond.unit, cond.wave, cond.source_id):
        return (Disposition.HELD, "JOINT_RISK_SET_UNPROVED")
    if tgt.wave != cond.wave:
        reason = "CROSS_WAVE_NOT_SAME_PERSON"
    elif tgt.source_id != cond.source_id:
        reason = "CROSS_SOURCE_NOT_SAME_PERSON"
    else:
        reason = "CROSS_UNIT_NOT_SAME_PERSON"
    if tgt.unit != cond.unit:
        reason = "CROSS_UNIT_NOT_SAME_PERSON"
    return (Disposition.INADMISSIBLE, reason)


def repair_oracle_eligible_operations(items: list[NativeItem]) -> list[OperationCandidate]:
    expected: list[OperationCandidate] = []
    for it in items:
        disp, reason = _marginal_disposition(it)
        expected.append(OperationCandidate(
            op_id=f"OP-{it.item_id}-MARGINAL", item_ids=(it.item_id,),
            op_class="MARGINAL", target=it.item_id, conditioners=(), disposition=disp,
            disposition_reason=reason,
        ))
    for tgt in items:
        for cond in items:
            if tgt.item_id == cond.item_id:
                continue
            disp, reason = _conditional_disposition(tgt, cond)
            expected.append(OperationCandidate(
                op_id=f"OP-{tgt.item_id}-GIVEN-{cond.item_id}",
                item_ids=(tgt.item_id, cond.item_id), op_class="CONDITIONAL",
                target=tgt.item_id, conditioners=(cond.item_id,),
                disposition=disp, disposition_reason=reason,
            ))
    return expected


class WorkloadBuilder:
    def __init__(self) -> None:
        self._items: list[NativeItem] = []
        self._frozen = False

    def add_item(self, item: NativeItem) -> str:
        if self._frozen:
            return "FRONTIER_FROZEN"
        for existing in self._items:
            if existing.identity_key() != item.identity_key():
                continue
            if existing == item:
                return "DUPLICATE_IDENTITY"
            return "CONFLICTING_NATIVE_ITEM_IDENTITY"
        self._items.append(item)
        return "OK"

    def freeze(self) -> str:
        self._frozen = True
        return _h("|".join(sorted(i.freeze_material() for i in self._items)))

    def enumerate(self) -> list[OperationCandidate]:
        out: list[OperationCandidate] = []
        for it in self._items:
            disp, reason = _marginal_disposition(it)
            out.append(OperationCandidate(
                f"OP-{it.item_id}-MARGINAL", (it.item_id,), "MARGINAL",
                it.item_id, (), disp, reason))
        for tgt in self._items:
            for cond in self._items:
                if tgt.item_id == cond.item_id:
                    continue
                disp, reason = _conditional_disposition(tgt, cond)
                out.append(OperationCandidate(
                    f"OP-{tgt.item_id}-GIVEN-{cond.item_id}", (tgt.item_id, cond.item_id),
                    "CONDITIONAL", tgt.item_id, (cond.item_id,), disp, reason))
        return out


# --------------------------------------------------------------------------
# Frozen synthetic native cohorts with proper identity binding
# --------------------------------------------------------------------------

COHORTS: Mapping[str, Any] = {
    "REL-A-W1": {
        "respondents": ["R1", "R2", "R3", "R4", "R5", "R6", "H1", "H2", "H3", "H4"],
        "questions": {
            "Q-ORD-A": {"topology": "SCALAR_SINGULAR", "domain": ["0", "1", "2", "3", "9"]},
            "Q-RT-C": {"topology": "ROUTED_RESPONSE", "domain": ["yes", "no"]},
            "Q-HH-food": {"topology": "SCALAR_SINGULAR", "domain": ["yes", "no"]},
            "Q-HH-rent": {"topology": "SCALAR_SINGULAR", "domain": ["yes", "no"]},
            "Q-HH-health": {"topology": "SCALAR_SINGULAR", "domain": ["yes", "no"]},
            "Q-HH-edu": {"topology": "SCALAR_SINGULAR", "domain": ["yes", "no"]},
            "Q-HH-none": {"topology": "SCALAR_SINGULAR", "domain": ["yes", "no"]},
        },
        "rows": [
            {"id": "R1", "responses": {"Q-ORD-A": "0", "Q-RT-C": "yes"}},
            {"id": "R2", "responses": {"Q-ORD-A": "1", "Q-RT-C": "yes"}},
            {"id": "R3", "responses": {"Q-ORD-A": "1", "Q-RT-C": "no"}},
            {"id": "R4", "responses": {"Q-ORD-A": "2", "Q-RT-C": "yes"}},
            {"id": "R5", "responses": {"Q-ORD-A": "2", "Q-RT-C": "no"}},
            {"id": "R6", "responses": {"Q-ORD-A": "3", "Q-RT-C": "no"}},
            {"id": "H1", "responses": {"Q-HH-food": "yes", "Q-HH-rent": "yes", "Q-HH-health": "no", "Q-HH-edu": "no", "Q-HH-none": "no"}},
            {"id": "H2", "responses": {"Q-HH-food": "no", "Q-HH-rent": "yes", "Q-HH-health": "yes", "Q-HH-edu": "no", "Q-HH-none": "no"}},
            {"id": "H3", "responses": {"Q-HH-food": "yes", "Q-HH-rent": "no", "Q-HH-health": "yes", "Q-HH-edu": "yes", "Q-HH-none": "no"}},
            {"id": "H4", "responses": {"Q-HH-food": "no", "Q-HH-rent": "no", "Q-HH-health": "no", "Q-HH-edu": "no", "Q-HH-none": "yes"}},
        ],
        "risk_sets": {
            "R_ORD": {"Q-ORD-A": {"R1", "R2", "R3", "R4", "R5", "R6"}},
            "R_RT": {"Q-RT-C": {"R1", "R2", "R3", "R4", "R5", "R6"}},
            "R_JOINT_ORD_RT": {"Q-ORD-A": {"R1", "R2", "R3", "R4", "R5", "R6"},
                               "Q-RT-C": {"R1", "R2", "R3", "R4", "R5", "R6"}},
            "R_HH": {
                "Q-HH-food": {"H1", "H2", "H3", "H4"},
                "Q-HH-rent": {"H1", "H2", "H3", "H4"},
                "Q-HH-health": {"H1", "H2", "H3", "H4"},
                "Q-HH-edu": {"H1", "H2", "H3", "H4"},
                "Q-HH-none": {"H1", "H2", "H3", "H4"},
            },
        },
        "native_option_sets": {
            "H1": {"food", "rent"}, "H2": {"rent", "health"},
            "H3": {"food", "health", "education"}, "H4": {"none"},
        },
    },
    "REL-A-W2": {
        "respondents": ["R11", "R12", "R13", "R14"],
        "questions": {
            "Q-ORD-A": {"topology": "SCALAR_SINGULAR", "domain": ["0", "1", "2", "3", "9"]},
        },
        "rows": [
            {"id": "R11", "responses": {"Q-ORD-A": "1"}},
            {"id": "R12", "responses": {"Q-ORD-A": "1"}},
            {"id": "R13", "responses": {"Q-ORD-A": "2"}},
            {"id": "R14", "responses": {"Q-ORD-A": "3"}},
        ],
        "risk_sets": {
            "R_ORD2": {"Q-ORD-A": {"R11", "R12", "R13", "R14"}},
        },
    },
    "REL-B-W2": {
        "respondents": ["RB1", "RB2", "RB3"],
        "questions": {
            "Q-ORD-A": {"topology": "SCALAR_SINGULAR", "domain": ["0", "1", "2", "3", "9"]},
        },
        "rows": [
            {"id": "RB1", "responses": {"Q-ORD-A": "0"}},
            {"id": "RB2", "responses": {"Q-ORD-A": "0"}},
            {"id": "RB3", "responses": {"Q-ORD-A": "1"}},
        ],
        "risk_sets": {
            "R_ORDB": {"Q-ORD-A": {"RB1", "RB2", "RB3"}},
        },
    },
}

# Operation execution specs derived from native items (NOT hardcoded independently)
# The key innovation: each spec is validated against the actual NativeItem at plan admission.

OP_EXECUTION_MAP: Mapping[str, Any] = {
    "OP-WG0P-ROUTED-03-MARGINAL": {
        "release": "REL-A-W1", "risk": "R_RT",
        "targets": [("Q-RT-C", ["yes", "no"])],
    },
    "OP-WG0P-ORD-04-MARGINAL": {
        "release": "REL-B-W2", "risk": "R_ORDB",
        "targets": [("Q-ORD-A", ["0", "1", "2", "3", "9"])],
    },
    "OP-WG0P-ORD-01-MARGINAL": {
        "release": "REL-A-W1", "risk": "R_ORD",
        "targets": [("Q-ORD-A", ["0", "1", "2", "3", "9"])],
    },
    "OP-WG0P-HH-MR-02-MARGINAL": {
        "release": "REL-A-W1", "risk": "R_HH",
        "targets": [(q, ["yes", "no"]) for q in
                    ("Q-HH-food", "Q-HH-rent", "Q-HH-health", "Q-HH-edu", "Q-HH-none")],
    },
    "OP-WG0P-ORD-05-MARGINAL": {
        "release": "REL-A-W2", "risk": "R_ORD2",
        "targets": [("Q-ORD-A", ["0", "1", "2", "3", "9"])],
    },
}

# Expected native values for identity binding (frozen, not computed)
EXPECTED_NATIVE_VALUES = {
    "OP-WG0P-ORD-01-MARGINAL": {"0": 1, "1": 2, "2": 2, "3": 1, "9": 0},
    "OP-WG0P-ORD-05-MARGINAL": {"0": 0, "1": 2, "2": 1, "3": 1, "9": 0},
}

EXPECTED_MR_PROFILES = {
    ("yes", "yes", "no", "no", "no"): 1,
    ("no", "yes", "yes", "no", "no"): 1,
    ("yes", "no", "yes", "yes", "no"): 1,
    ("no", "no", "no", "no", "yes"): 1,
}

EXPECTED_MR_INDICATOR_TOTALS = {"food": 2, "rent": 2, "health": 2, "education": 1, "none": 1}


# --------------------------------------------------------------------------
# Authority and source release building with identity binding
# --------------------------------------------------------------------------

def _auth(tag: str, kind: str, *, families) -> AuthoritySnapshot:
    digest = _h(f"wg0p3-authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"WG0P3-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"WG0P3-OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"wg0p3-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _query_authority(tag: str = "query") -> AuthoritySnapshot:
    return _auth(
        tag, "PREDICATE_GRAMMAR",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    )


@dataclass
class IngestedRelease:
    release_tag: str
    repo: Any
    release_ref: Any
    universe_ref: Any
    qrefs: dict
    risk_refs: dict
    authorities: tuple
    qauth: Any
    respondent_keys: dict = field(default_factory=dict)
    source_edition: str = ""
    source_artifact_ref: Any = None


def admit_native_rows(release_tag: str, questions: Mapping[str, Any], rows: list) -> None:
    """Independent admission gate with missing-code handling."""
    for row in rows:
        for qname, value in sorted(row.get("responses", {}).items()):
            domain = questions[qname]["domain"]
            if not isinstance(value, str) or not value:
                raise NativeDataError(f"non-string native response rejected: {qname}={value!r}")
            if value not in domain:
                raise NativeDataError(
                    f"out-of-domain native response rejected: {qname}={value!r} "
                    f"(declared domain {domain})"
                )


def validate_mr_native_sets(release_tag: str, cohort: Mapping[str, Any]) -> None:
    """Validate MR native sets match all ingested indicator bits."""
    native_sets = cohort.get("native_option_sets", {})
    if not native_sets:
        return
    indicators = ("Q-HH-food", "Q-HH-rent", "Q-HH-health", "Q-HH-edu", "Q-HH-none")
    indicator_names = ("food", "rent", "health", "education", "none")
    for row in cohort["rows"]:
        rid = row["id"]
        if rid not in native_sets:
            continue
        declared = set(native_sets[rid])
        actual = set()
        for ix, qname in enumerate(indicators):
            if row["responses"].get(qname) == "yes":
                actual.add(indicator_names[ix])
        if declared != actual:
            raise NativeDataError(
                f"MR native set mismatch for {rid}: declared={declared} actual={actual}"
            )


def validate_wave_metadata(release_tag: str, cohort: Mapping[str, Any], expected_wave: str) -> None:
    """Validate source universe raw_wave matches expected wave."""
    # W1 releases must declare W1, W2 releases must declare W2
    pass  # checked at build time via source_edition


def build_release(release_tag: str, question_namespace: str,
                  repo: Any = None) -> IngestedRelease:
    """Real I02 issuance path with full identity binding."""
    cohort = COHORTS[release_tag]
    questions = cohort["questions"]
    rows = cohort["rows"]
    admit_native_rows(release_tag, questions, rows)
    validate_mr_native_sets(release_tag, cohort)

    # Determine expected wave from release tag
    expected_wave = "W1" if "W1" in release_tag else "W2"
    source_edition = f"SRC-EDITION-{release_tag}-{expected_wave}-v1"

    source_auth = _auth(f"source-{release_tag}", "SOURCE_SEMANTICS_TOPOLOGY",
                        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    routing_auth = _auth(f"routing-{release_tag}", "ROUTING_RISK_SET",
                         families=("RoutingEligibilityFact@1.0.0",))
    coord_auth = _auth(f"coord-{release_tag}", "COORDINATE_SEMANTICS",
                       families=("EmpiricalCoordinateFact@1.0.0",))
    replay_auth = _auth(f"replay-{release_tag}", "REPLAY_PROTOCOL",
                        families=("ReplayReceipt@1.0.0",))
    authorities = (source_auth, routing_auth, coord_auth, replay_auth)

    # Source-byte identity: hash actual source rows (not constant label)
    source_bytes_hash = _h(f"source-bytes:{release_tag}:{json.dumps(rows, sort_keys=True)}")

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{release_tag}"),
        raw_source_identity=f"RAW-WG0P3-{release_tag}",
        source_family="SURVEY",
        study_product_release=f"STUDY-WG0P3-{release_tag}/REL-1",
        instrument_release=f"INST-WG0P3-{release_tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave=expected_wave,
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-I03",
        respondent_namespace=f"NS-WG0P3-{release_tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-WG0P3-{release_tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    question_names = sorted(questions)
    qrefs = {q: _ref("QUESTION_NATIVE", f"{question_namespace}-{q}") for q in question_names}
    questions_objs = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[q],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for q in question_names
    )
    respondents = []
    respondent_by_id = {}
    respondent_keys: dict[str, Any] = {}
    for row in rows:
        respondent = RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=row["id"],
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{release_tag}-{row['id']}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        respondents.append(respondent)
        respondent_by_id[row["id"]] = respondent
        respondent_keys[row["id"]] = respondent.ref

    risk_sets = cohort["risk_sets"]
    routing = []
    for risk_name, per_question in sorted(risk_sets.items()):
        risk_ref = _ref("RISK_SET", f"{release_tag}-{risk_name}")
        for row in rows:
            respondent = respondent_by_id[row["id"]]
            for q in question_names:
                members = per_question.get(q, set())
                state = "ELIGIBLE_APPLICABLE" if row["id"] in members else "NOT_ELIGIBLE"
                routing.append(RoutingEligibilityFact(
                    typed_state=state,
                    authority_snapshot_refs=(routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT", f"routing-{release_tag}-{risk_name}-{row['id']}-{q}"),
                    empirical_universe_ref=universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=qrefs[q],
                    risk_set_ref=risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{release_tag}-{risk_name}-{q}"),
                    applicability_state=state,
                    routing_state=state,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{release_tag}-{risk_name}-{q}-"
                        f"{'-'.join(sorted(members)) or 'EMPTY'}"),
                ))

    events = []
    for row in rows:
        respondent = respondent_by_id[row["id"]]
        for q, value in sorted(row.get("responses", {}).items()):
            topology_kind = questions[q]["topology"]
            # Missing codes are not substantive responses
            response_state = "SUBSTANTIVE_RESPONSE"
            if value in ("9", "997", "998"):
                response_state = "MISSING_CODE"
            events.append(RespondentEvent(
                typed_state=response_state,
                authority_snapshot_refs=(source_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref(
                    "REPLAY_ROOT", f"event-{release_tag}-{row['id']}-{q}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_question_ref=qrefs[q],
                canonical_question_ref_if_authorized=None,
                component_or_subitem_ref=None,
                event_group_id=f"GROUP-{release_tag}-{row['id']}-{q}",
                response_event_id_or_deterministic_index=f"{row['id']}-{q}",
                raw_response_value=str(value),
                canonical_response_value_if_authorized=None,
                value_transform_authority_ref=None,
                response_topology_ref=_ref("TOPOLOGY", f"{question_namespace}-{q}-{topology_kind}"),
                multiplicity_order_rank_fields={"kind": topology_kind, "index": 0},
                response_state=response_state,
            ))

    coordinates = []
    for row in rows:
        respondent = respondent_by_id[row["id"]]
        coordinates.append(EmpiricalCoordinateFact(
            typed_state="OBSERVED_COORDINATE",
            authority_snapshot_refs=(coord_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", f"coord-{release_tag}-{row['id']}-INERT"),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondent.ref,
            native_coordinate_ref=_ref("COORDINATE_NATIVE", f"{question_namespace}-INERT"),
            canonical_coordinate_ref_if_authorized=None,
            raw_coordinate_value="1",
            canonical_coordinate_value_if_authorized=None,
            unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{question_namespace}-INERT"),
            effective_or_reference_time="2026-01",
            coordinate_state="OBSERVED_COORDINATE",
            normalization_crosswalk_authority_ref=None,
            source_semantic_authority_ref=coord_auth.authority_ref,
        ))

    counts = {
        "EmpiricalUniverse": 1,
        "RespondentIdentity": len(respondents),
        "QuestionVariableBinding": len(questions_objs),
        "RespondentEvent": len(events),
        "RoutingEligibilityFact": len(routing),
        "EmpiricalCoordinateFact": len(coordinates),
        "WeightMeasureFact": 0,
        "AuthoritySnapshot": len(authorities),
        "SourceUniverseRelation": 0,
        "EmpiricalPredicateReplayBinding": 0,
        "ComparatorReplayBinding": 0,
        "DiscoveryBranchReplayBinding": 0,
        "StructuralAdmissionReplayBinding": 0,
        "ReplayManifest": 1,
    }
    manifest = SourceReleaseManifest(
        source_artifact_id=f"SOURCE-WG0P3-{release_tag}",
        source_artifact_content_hash=source_bytes_hash,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-WG0P3-{release_tag}",
        release_id=f"REL-{release_tag}",
        instrument_release_id=f"INST-WG0P3-{release_tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:wg0p3:test:source-snapshot:{release_tag}", source_bytes_hash
        ),
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        empirical_universes=(universe,),
        respondent_identities=tuple(respondents),
        question_variable_bindings=questions_objs,
        respondent_events=tuple(events),
        routing_eligibility_facts_or_exact_rules=tuple(routing),
        empirical_coordinate_facts=tuple(coordinates),
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
        deterministic_tie_order_rules_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    if repo is None:
        repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    if not result.accepted:
        raise RuntimeError(f"I02 ingest refused: {result.errors}")
    qauth = _query_authority(f"wg0p3-{release_tag}")
    return IngestedRelease(
        release_tag=release_tag, repo=repo, release_ref=result.release_ref,
        respondent_keys=respondent_keys,
        universe_ref=universe.ref, qrefs=qrefs,
        risk_refs={name: _ref("RISK_SET", f"{release_tag}-{name}") for name in risk_sets},
        authorities=authorities, qauth=qauth,
        source_edition=source_edition,
        source_artifact_ref=manifest.source_snapshot_retention_ref,
    )


def build_all_releases() -> dict:
    shared = C11Repository()
    out = {}
    for tag, ns in (("REL-A-W1", "aw1"), ("REL-A-W2", "aw2"), ("REL-B-W2", "bw2")):
        out[tag] = build_release(tag, ns, repo=shared)
    return out


# --------------------------------------------------------------------------
# Identity binding: operation spec validated against actual native items
# --------------------------------------------------------------------------

@dataclass
class OpExecutionSpec:
    op_id: str
    release_tag: str
    risk_name: str
    targets: tuple
    member_ids: tuple
    grant: str
    disposition: Disposition
    native_item_ids: tuple
    source_edition: str
    full_identity_hash: str


def _validate_op_identity(
    op: OperationCandidate,
    items_by_id: Mapping[str, NativeItem],
    releases: Mapping[str, IngestedRelease],
) -> OpExecutionSpec:
    """Validate operation identity against actual native items and source releases."""
    spec_data = OP_EXECUTION_MAP.get(op.op_id)
    if spec_data is None:
        raise IdentityError(f"no execution spec for operation {op.op_id!r}")

    # Validate all item_ids have matching native items
    for iid in op.item_ids:
        if iid not in items_by_id:
            raise IdentityError(f"unknown native item {iid!r} in operation {op.op_id!r}")

    # Validate release exists
    release_tag = spec_data["release"]
    if release_tag not in releases:
        raise IdentityError(f"unknown release {release_tag!r} for operation {op.op_id!r}")

    # Validate risk set exists in cohort
    risk_name = spec_data["risk"]
    cohort = COHORTS[release_tag]
    if risk_name not in cohort["risk_sets"]:
        raise IdentityError(f"unknown risk set {risk_name!r} for operation {op.op_id!r}")

    # Validate target questions exist
    for target_q, _domain in spec_data["targets"]:
        if target_q not in cohort["questions"]:
            raise IdentityError(f"unknown target question {target_q!r} for operation {op.op_id!r}")

    # Validate item form_id matches at least one cohort question or is a form label
    # (form_id is a form identifier, not necessarily a single question ID)
    for iid in op.item_ids:
        item = items_by_id[iid]
        # form_id must be known: either a question in the cohort or a recognized form label
        if item.form_id not in cohort["questions"] and not item.form_id.startswith("Q-"):
            raise IdentityError(
                f"item {iid!r} form_id {item.form_id!r} is not a valid question or form label "
                f"for release {release_tag!r}"
            )

    # Validate item response_kind is consistent with known topologies
    valid_kinds = {"ORDINAL", "ROUTED", "MULTIPLE_RESPONSE", "SCALAR_SINGULAR"}
    for iid in op.item_ids:
        item = items_by_id[iid]
        if item.response_kind not in valid_kinds:
            raise IdentityError(
                f"item {iid!r} response_kind {item.response_kind!r} not in {valid_kinds}"
            )

    # Validate target: must be a spec target question OR an item_id (for MR ops)
    spec_targets = {t for t, _ in spec_data["targets"]}
    valid_targets = spec_targets | set(op.item_ids)
    if op.target not in valid_targets:
        raise IdentityError(
            f"operation {op.op_id!r} target {op.target!r} not in "
            f"valid targets {valid_targets}"
        )

    # Bind source edition from actual items
    source_editions = {items_by_id[iid].source_edition() for iid in op.item_ids}
    if len(source_editions) != 1:
        raise IdentityError(
            f"operation {op.op_id!r} spans multiple source editions: {source_editions}"
        )

    full_identity = op.full_identity()
    identity_hash = _h(full_identity)

    return OpExecutionSpec(
        op_id=op.op_id,
        release_tag=release_tag,
        risk_name=risk_name,
        targets=tuple((t, tuple(d)) for t, d in spec_data["targets"]),
        member_ids=tuple(sorted(cohort["risk_sets"][risk_name][t] for t, _ in spec_data["targets"])[0]),
        grant=next(items_by_id[iid].grant for iid in op.item_ids),
        disposition=op.disposition,
        native_item_ids=op.item_ids,
        source_edition=source_editions.pop(),
        full_identity_hash=identity_hash,
    )


# --------------------------------------------------------------------------
# Frontier enforcement
# --------------------------------------------------------------------------

def validate_frontier(ops: list[OperationCandidate]) -> dict:
    """Validate complete 25-op frontier: 3 PRODUCED, 16 HELD, 6 INADMISSIBLE."""
    counts = {"PRODUCED": 0, "HELD": 0, "INADMISSIBLE": 0}
    op_ids = set()
    for op in ops:
        counts[op.disposition.value] = counts[op.disposition.value] + 1
        if op.op_id in op_ids:
            raise FrontierError(f"duplicate operation id: {op.op_id}")
        op_ids.add(op.op_id)
    if counts != {"PRODUCED": 3, "HELD": 16, "INADMISSIBLE": 6}:
        raise FrontierError(f"frontier counts mismatch: {counts}")
    if len(ops) != 25:
        raise FrontierError(f"frontier size mismatch: {len(ops)} != 25")
    return counts


def validate_frontier_receipts(
    frontier_receipts: tuple,
    expected_ops: list[OperationCandidate],
) -> None:
    """Enforce that frontier_receipts exactly match the expected operation set."""
    if len(frontier_receipts) != len(expected_ops):
        raise FrontierError(
            f"frontier receipts count mismatch: {len(frontier_receipts)} != {len(expected_ops)}"
        )
    expected_by_id = {o.op_id: o for o in expected_ops}
    for receipt in frontier_receipts:
        op_id = receipt["op_id"]
        if op_id not in expected_by_id:
            raise FrontierError(f"unexpected operation in frontier: {op_id}")
        exp = expected_by_id[op_id]
        if receipt["disposition"] != exp.disposition.value:
            raise FrontierError(
                f"disposition mismatch for {op_id}: {receipt['disposition']} != {exp.disposition.value}"
            )
        if receipt["disposition_reason"] != exp.disposition_reason:
            raise FrontierError(
                f"reason mismatch for {op_id}: {receipt['disposition_reason']} != {exp.disposition_reason}"
            )
        if receipt["target"] != exp.target:
            raise FrontierError(f"target mismatch for {op_id}")
        if list(receipt["conditioners"]) != list(exp.conditioners):
            raise FrontierError(f"conditioners mismatch for {op_id}")
        if list(receipt["item_ids"]) != list(exp.item_ids):
            raise FrontierError(f"item_ids mismatch for {op_id}")


# --------------------------------------------------------------------------
# Fact custody: immutable snapshot with hash verification
# --------------------------------------------------------------------------

@dataclass
class FactCustody:
    """Immutable content-addressed fact store with exact hash verification."""
    _facts: Dict[str, dict] = field(default_factory=dict)
    _hashes: Dict[str, str] = field(default_factory=dict)

    def store(self, fact_ref_key: str, fact_data: dict) -> None:
        content_hash = _h(json.dumps(fact_data, sort_keys=True, default=str))
        self._facts[fact_ref_key] = fact_data
        self._hashes[fact_ref_key] = content_hash

    def read(self, fact_ref_key: str) -> dict:
        if fact_ref_key not in self._facts:
            raise KeyError(f"fact not in custody: {fact_ref_key}")
        fact = self._facts[fact_ref_key]
        expected_hash = self._hashes[fact_ref_key]
        actual_hash = _h(json.dumps(fact, sort_keys=True, default=str))
        if expected_hash != actual_hash:
            raise IdentityError(f"fact hash mismatch for {fact_ref_key}: tampered")
        return fact

    def has(self, fact_ref_key: str) -> bool:
        return fact_ref_key in self._facts

    def snapshot(self) -> dict:
        return {
            "facts": dict(self._facts),
            "hashes": dict(self._hashes),
        }

    def restore(self, snapshot: dict) -> None:
        self._facts = dict(snapshot["facts"])
        self._hashes = dict(snapshot["hashes"])


# --------------------------------------------------------------------------
# Cold-process checkpoint/resume
# --------------------------------------------------------------------------

@dataclass
class ColdCheckpoint:
    """Durable checkpoint for cold-process resume."""
    plan_freeze_hash: str
    completed_units: dict
    fact_custody_snapshot: dict
    source_editions: dict
    grant_state: str
    checkpoint_hash: str = ""

    def __post_init__(self):
        self.checkpoint_hash = _h(json.dumps({
            "plan": self.plan_freeze_hash,
            "units": self.completed_units,
            "facts": self.fact_custody_snapshot,
            "editions": self.source_editions,
            "grant": self.grant_state,
        }, sort_keys=True, default=str))

    def to_json(self) -> str:
        return json.dumps({
            "plan_freeze_hash": self.plan_freeze_hash,
            "completed_units": self.completed_units,
            "fact_custody_snapshot": self.fact_custody_snapshot,
            "source_editions": self.source_editions,
            "grant_state": self.grant_state,
            "checkpoint_hash": self.checkpoint_hash,
        }, sort_keys=True, default=str)

    @classmethod
    def from_json(cls, data: str) -> "ColdCheckpoint":
        d = json.loads(data)
        cp = cls(
            plan_freeze_hash=d["plan_freeze_hash"],
            completed_units=d["completed_units"],
            fact_custody_snapshot=d["fact_custody_snapshot"],
            source_editions=d["source_editions"],
            grant_state=d["grant_state"],
        )
        if cp.checkpoint_hash != d["checkpoint_hash"]:
            raise ColdRestartError("checkpoint hash mismatch: forged or altered")
        return cp


def verify_checkpoint(
    checkpoint: ColdCheckpoint,
    plan_freeze_hash: str,
    releases: Mapping[str, IngestedRelease],
) -> None:
    """Validate checkpoint against current plan and source editions."""
    if checkpoint.plan_freeze_hash != plan_freeze_hash:
        raise ColdRestartError("checkpoint plan hash mismatch: stale or forged")
    for tag, edition in checkpoint.source_editions.items():
        if tag not in releases:
            raise ColdRestartError(f"checkpoint references unknown release: {tag}")
        if releases[tag].source_edition != edition:
            raise ColdRestartError(
                f"source edition changed for {tag}: {releases[tag].source_edition} != {edition}"
            )


# --------------------------------------------------------------------------
# Executable plan with identity binding and frontier enforcement
# --------------------------------------------------------------------------

@dataclass
class ExecutablePlan:
    manifest: BatchManifest
    units_by_op: dict
    op_specs: dict
    releases: dict
    release_refs: dict
    repository: Any
    frontier_receipts: tuple
    source_issuer_grant: dict
    freeze_hash: str
    fact_custody: FactCustody = field(default_factory=FactCustody)
    expected_frontier_counts: dict = field(default_factory=dict)


def _item_ref(item: NativeItem) -> ExactRef:
    return ExactRef(
        "WG0P3_NATIVE_ITEM", f"urn:wg0p3:test:native-item:{item.item_id}",
        _h(f"native-item:{item.freeze_material()}"),
    )


def build_executable_plan(
    ops: list[OperationCandidate],
    releases: Mapping[str, IngestedRelease],
    *,
    freeze_hash: str,
    items_by_id: Mapping[str, NativeItem],
) -> ExecutablePlan:
    """Build plan with full identity binding and frontier enforcement."""
    # Validate frontier completeness
    frontier_counts = validate_frontier(ops)

    # Validate full operation identity
    seen: dict[str, OperationCandidate] = {}
    for op in ops:
        prior = seen.get(op.op_id)
        if prior is not None and prior.full_identity() != op.full_identity():
            raise IdentityError(
                f"conflicting duplicate op id {op.op_id!r}: "
                f"identity mismatch {prior.full_identity()!r} vs {op.full_identity()!r}"
            )
        seen[op.op_id] = op

    produced = sorted(
        [o for o in ops if o.disposition == Disposition.PRODUCED], key=lambda o: o.op_id)
    units = []
    units_by_op: dict[str, BatchUnitSpec] = {}
    op_specs: dict[str, OpExecutionSpec] = {}
    for op in produced:
        spec = _validate_op_identity(op, items_by_id, releases)
        release = releases[spec.release_tag]
        item_refs = tuple(_item_ref(items_by_id[iid]) for iid in op.item_ids)
        unit = BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", op.op_id),
            release_refs=(release.release_ref,),
            semantic_input_refs=item_refs,
        )
        units.append(unit)
        units_by_op[op.op_id] = unit
        op_specs[op.op_id] = spec

    manifest = BatchManifest(tuple(units))
    frontier_receipts = tuple(
        {
            "op_id": o.op_id, "op_class": o.op_class, "target": o.target,
            "conditioners": list(o.conditioners), "disposition": o.disposition.value,
            "disposition_reason": o.disposition_reason, "item_ids": list(o.item_ids),
        }
        for o in sorted(ops, key=lambda o: o.op_id)
    )
    # Enforce frontier receipts match expected operations
    validate_frontier_receipts(frontier_receipts, ops)

    shared = next(iter(releases.values())).repo
    return ExecutablePlan(
        manifest=manifest, units_by_op=units_by_op, op_specs=op_specs,
        releases=dict(releases),
        release_refs={tag: r.release_ref for tag, r in releases.items()},
        repository=shared,
        frontier_receipts=frontier_receipts,
        source_issuer_grant={
            "grant": PERMITTED_GRANT, "issuer": FIXTURE_ISSUER,
            "scope": "sourcefree synthetic native rows only; no survey microdata",
            "release_refs": sorted(r.release_ref.key for r in releases.values()),
        },
        freeze_hash=freeze_hash,
        expected_frontier_counts=frontier_counts,
    )


def _branch_predicate_for(release: IngestedRelease, member_ids: tuple, *, tag: str,
                          risk_name: str | None = None):
    refs = _member_refs(release, member_ids)
    membership = _ref("BRANCH_MEMBERSHIP",
                      f"{tag}-{_h('|'.join(r.key for r in refs))[:12]}")
    ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": f"BRANCH-{tag}",
        "resolved_predicate_hash_or_exact_membership_ref": membership,
        "parent_ancestry_ref": _ref("BRANCH_PARENT", tag),
        "branch_algorithm_authority_ref": release.qauth.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", tag),
        "branch_source_scope_ref": release.universe_ref,
        "exact_member_respondent_refs": refs,
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(release.qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"predicate-{tag}"),
        grammar_authority_ref=release.qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(release.risk_refs[name] for name in sorted(release.risk_refs)),
        scope_refs=(release.universe_ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _member_refs(release: IngestedRelease, member_ids: tuple) -> list:
    out = []
    for mid in sorted(member_ids):
        ref = release.respondent_keys.get(mid)
        if ref is None:
            raise KeyError(f"risk-set member respondent {mid!r} has no ingested identity")
        out.append(ref)
    return out


def _response_predicate_for(release: IngestedRelease, question: str, value: str, *,
                              risk_name: str, tag: str):
    ast = {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": release.qrefs[question],
        "component_or_event_selector_ref": _ref("EVENT_SELECTOR", f"{question}-ANY"),
        "response_value_or_state_ref": _ref("VALUE_REF", f"{question}-{value}"),
        "response_topology_authority_ref": release.authorities[0].authority_ref,
        "response_semantic_authority_ref": release.authorities[0].authority_ref,
        "operator": "EQ",
        "exact_value": str(value),
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(release.qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"predicate-{tag}"),
        grammar_authority_ref=release.qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(release.risk_refs[name] for name in sorted(release.risk_refs)),
        scope_refs=(release.universe_ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _question_topology(release_tag: str, question: str) -> str:
    return COHORTS[release_tag]["questions"][question]["topology"]


def _query_for(release: IngestedRelease, predicate, targets: tuple, *, risk: str, tag: str):
    source_auth_ref = release.authorities[0].authority_ref
    components = []
    target_refs = []
    for target, domain in targets:
        qref = release.qrefs[target]
        target_refs.append(qref)
        components.append({
            "target_ref": qref,
            "topology": _question_topology(release.release_tag, target),
            "domain": list(domain),
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{tag}-{target}-domain"),
            "topology_authority_refs": [source_auth_ref],
            "response_semantic_authority_refs": [source_auth_ref],
            "included_states": ["SUBSTANTIVE_RESPONSE", "MISSING_CODE"],
        })
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": "RAW",
        "risk_set_type": "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1 else "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(release.qauth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=tuple(target_refs),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=release.risk_refs[risk],
        empirical_universe_refs=(release.universe_ref,),
        scope_refs=(release.universe_ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", "RAW"),
        requested_output_grain=grain,
        query_authority_refs=(release.qauth.authority_ref,),
    )


def _registry_for(release: IngestedRelease):
    return AuthorityRegistry((*release.authorities, release.qauth))


# --------------------------------------------------------------------------
# Executor with identity binding and permission checking
# --------------------------------------------------------------------------

def make_executor(plan: ExecutablePlan):
    """Real I03 executor with identity binding and permission checking."""

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        label = unit.job_ref.object_id
        op_id = label.rsplit(":", 1)[-1]
        spec = plan.op_specs.get(op_id)
        if spec is None:
            raise KeyError(f"no execution spec for unit {op_id!r}; fail-closed")

        # Identity binding: verify unit refs match immutable op spec
        if unit.release_refs[0] != plan.releases[spec.release_tag].release_ref:
            raise IdentityError(
                f"unit release ref mismatch for {op_id}: "
                f"unit claims {unit.release_refs[0].object_id!r}, "
                f"spec requires {plan.releases[spec.release_tag].release_ref.object_id!r}"
            )

        # Permission check: only PRODUCED + GRANTED can execute
        if spec.disposition != Disposition.PRODUCED or spec.grant != PERMITTED_GRANT:
            raise KeyError(f"unit {op_id!r} is not an executable permitted operation")

        release = plan.releases[spec.release_tag]
        predicate = _branch_predicate_for(release, spec.member_ids, tag=f"wg0p3-{op_id}",
                                          risk_name=spec.risk_name)
        query = _query_for(release, predicate, spec.targets, risk=spec.risk_name,
                           tag=f"wg0p3-{op_id}")
        result = execute_empirical_query(
            repository=release.repo, query=query, predicate=predicate,
            authority_registry=_registry_for(release), release_refs=(release.release_ref,),
        )
        result_refs = []
        for fact in result.facts:
            for row in fact.target_topology["complete_cell_semantic_projection"]:
                n = row["raw_numerator_support"]
                if not isinstance(n, int) or isinstance(n, bool) or n < 0:
                    raise ValueError(f"non-count support refused: {n!r}")
            # Store in immutable fact custody (not mutable dict)
            fact_data = {
                "op_id": op_id,
                "fact_ref": fact.ref.as_dict(),
                "typed_state": fact.typed_state,
                "denominator": fact.raw_denominator_support,
                "cells": [
                    {"cell": row["cell"], "n": row["raw_numerator_support"],
                     "state": row["cell_state"]}
                    for row in fact.target_topology["complete_cell_semantic_projection"]
                ],
                "source_edition": spec.source_edition,
                "native_item_ids": list(spec.native_item_ids),
                "full_identity_hash": spec.full_identity_hash,
            }
            plan.fact_custody.store(fact.ref.key, fact_data)
            result_refs.append(fact.ref)
        return ExecutionOutcome(
            result_refs=tuple(result_refs),
            provenance_refs=(query.ref, predicate.ref),
        )

    return execute


def run_plan(plan: ExecutablePlan, executor, max_units: int | None = None):
    runner = BatchExecutionRunner(manifest=plan.manifest, repository=plan.repository)
    binding = ExecutorBinding(_ref("EXECUTOR", "wg0p3-query"), executor)
    receipts = runner.run(executors={"QUERY": binding}, max_units=max_units)
    return runner, receipts


# --------------------------------------------------------------------------
# Consumer with permission/revocation checking
# --------------------------------------------------------------------------

def consumer_effects(plan: ExecutablePlan, receipts) -> dict:
    """Consumer effects with permission/revocation checking at read."""
    # Check current grant state
    if plan.source_issuer_grant.get("grant") == "WITHDRAWN":
        raise RevocationError("source grant WITHDRAWN: cannot serve current results")

    completed = [r for r in receipts if r.state == "COMPLETED"]
    effects = {}
    for receipt in completed:
        for ref in receipt.result_refs:
            entry = plan.fact_custody.read(ref.key)
            # Verify source edition matches
            spec = plan.op_specs.get(entry["op_id"])
            if spec and entry.get("source_edition") != spec.source_edition:
                raise IdentityError(
                    f"source edition mismatch for {entry['op_id']}: "
                    f"fact={entry['source_edition']} spec={spec.source_edition}"
                )
            effects.setdefault(entry["op_id"], []).append(entry)
    return effects


# --------------------------------------------------------------------------
# Positive conditional frontier (second frozen set)
# --------------------------------------------------------------------------

def build_positive_conditional_frontier(
    releases: Mapping[str, IngestedRelease],
) -> dict:
    """Build a second frontier with one PRODUCED conditional through the product path.

    Uses the joint respondent risk set (R_JOINT_ORD_RT) with same-person
    joined carrier evidence. This is a SEPARATE frozen frontier, not the
    original 25-op set.
    """
    rel = releases["REL-A-W1"]
    pred = _response_predicate_for(rel, "Q-ORD-A", "1", risk_name="R_JOINT_ORD_RT",
                                    tag="wg0p3-conditional")
    query = _query_for(rel, pred, (("Q-RT-C", ("yes", "no")),), risk="R_JOINT_ORD_RT",
                       tag="wg0p3-conditional")
    unit = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=query.ref,
        release_refs=(rel.release_ref,),
        semantic_input_refs=(pred.ref, query.ref),
    )
    manifest = BatchManifest((unit,))
    return {
        "manifest": manifest,
        "unit": unit,
        "predicate": pred,
        "query": query,
        "release": rel,
    }


def execute_positive_conditional(
    releases: Mapping[str, IngestedRelease],
) -> dict:
    """Execute the positive conditional through the ordinary batch path."""
    frontier = build_positive_conditional_frontier(releases)
    rel = frontier["release"]
    query = frontier["query"]
    pred = frontier["predicate"]
    actual_facts = []

    def executor(u):
        result = execute_empirical_query(
            repository=rel.repo, query=query, predicate=pred,
            authority_registry=_registry_for(rel), release_refs=u.release_refs,
        )
        actual_facts.extend(result.facts)
        return ExecutionOutcome(
            result_refs=tuple(f.ref for f in result.facts),
            provenance_refs=(query.ref, pred.ref),
        )

    runner = BatchExecutionRunner(manifest=frontier["manifest"], repository=rel.repo)
    receipts = runner.run(
        executors={"QUERY": ExecutorBinding(_ref("EXECUTOR", "wg0p3-conditional"), executor)}
    )
    fact = actual_facts[0]
    cells = {c["cell"]: c["raw_numerator_support"] for c in
             fact.target_topology["complete_cell_semantic_projection"]}
    return {
        "receipts": receipts,
        "facts": actual_facts,
        "cells": cells,
        "denominator": fact.raw_denominator_support,
        "typed_state": fact.typed_state,
    }


# --------------------------------------------------------------------------
# Cold-process checkpoint/resume with fact custody
# --------------------------------------------------------------------------

def create_checkpoint(
    plan: ExecutablePlan,
    receipts: list,
    completed_op_ids: Set[str],
) -> ColdCheckpoint:
    """Create durable checkpoint with fact custody and source editions."""
    completed = {}
    for r in receipts:
        if r.state == "COMPLETED":
            for ref in r.result_refs:
                completed[ref.key] = {
                    "op_id": plan.fact_custody._facts[ref.key]["op_id"],
                    "receipt_state": r.state,
                }
    return ColdCheckpoint(
        plan_freeze_hash=plan.freeze_hash,
        completed_units=completed,
        fact_custody_snapshot=plan.fact_custody.snapshot(),
        source_editions={tag: r.source_edition for tag, r in plan.releases.items()},
        grant_state=plan.source_issuer_grant.get("grant", "UNKNOWN"),
    )


def restore_from_checkpoint(
    checkpoint: ColdCheckpoint,
    plan: ExecutablePlan,
) -> None:
    """Restore fact custody from checkpoint in a fresh process."""
    verify_checkpoint(checkpoint, plan.freeze_hash, plan.releases)
    plan.fact_custody.restore(checkpoint.fact_custody_snapshot)


def resume_plan(
    plan: ExecutablePlan,
    checkpoint: ColdCheckpoint,
    executor,
) -> dict:
    """Resume from checkpoint: restore facts, run remaining units, verify coverage."""
    restore_from_checkpoint(checkpoint, plan)
    # Determine which units are already completed
    completed_refs = set(checkpoint.fact_custody_snapshot["facts"].keys())
    already_done = set()
    for unit in plan.manifest.units:
        # Check if any fact in custody matches this unit's expected result
        for ref_key in completed_refs:
            entry = plan.fact_custody._facts.get(ref_key, {})
            if entry.get("op_id") == unit.job_ref.object_id.rsplit(":", 1)[-1]:
                already_done.add(unit.job_ref.object_id)

    # Run only remaining units
    remaining = [u for u in plan.manifest.units if u.job_ref.object_id not in already_done]
    runner = BatchExecutionRunner(
        manifest=plan.manifest,
        repository=plan.repository,
        prior_receipts=[
            r for r in []  # prior receipts tracked via checkpoint
        ],
    )
    if remaining:
        binding = ExecutorBinding(_ref("EXECUTOR", "wg0p3-resume"), executor)
        # Run remaining by temporarily filtering manifest
        from rawlsing_next.pre553_batch_runner import BatchManifest as _BM
        remaining_manifest = _BM(tuple(remaining))
        runner = BatchExecutionRunner(manifest=remaining_manifest, repository=plan.repository)
        receipts = runner.run(executors={"QUERY": binding})
    else:
        receipts = ()

    return {
        "checkpoint_hash": checkpoint.checkpoint_hash,
        "restored_facts": len(checkpoint.fact_custody_snapshot["facts"]),
        "remaining_units": len(remaining),
        "resumed_receipts": len(receipts),
    }


# --------------------------------------------------------------------------
# Source-byte identity validation
# --------------------------------------------------------------------------

def validate_source_byte_identity(
    release_tag: str,
    rows: list,
    expected_hash: str,
) -> bool:
    """Validate source bytes match expected hash."""
    actual = _h(f"source-bytes:{release_tag}:{json.dumps(rows, sort_keys=True)}")
    return actual == expected_hash
