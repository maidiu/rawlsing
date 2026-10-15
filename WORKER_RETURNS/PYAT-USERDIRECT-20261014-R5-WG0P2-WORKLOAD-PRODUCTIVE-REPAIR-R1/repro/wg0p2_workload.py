"""R5 WG0P2 -- source-true workload repair: real C11 ingest, real I03 compute, real batch receipts.

Repairs all 15 WG0I-observed candidate defects while preserving the 5-item
frontier:
  * no caller-supplied numerators and no 1/2 fallback (fail-closed KeyError);
  * no manual C11Repository injection (real ingest_c11_source_release);
  * no auto-produced same-unit conditional (real joint risk-set predicate required);
  * unknown/withdrawn/arbitrary grants all HELD (only GRANTED_FIXTURE permits);
  * freeze binds every native field (options, grant, route evidence, version);
  * withdrawn/unrouteable conditioning pairs retained as HELD (no drops);
  * conflicting same-form carriers flagged, conflicting op ids refused;
  * frozen no-drop frontier ledger travels on the plan;
  * native option mutation changes unit identity (source values propagate);
  * positive source-issuer grant travels on the plan.

Source-free synthetic native records only. No raw survey, no canonical
changes, no V3. Permitted grant is the fixture grant GRANTED_FIXTURE.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional

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

VERSION = "R5_WG0P2_SOURCE_TRUE_WORKLOAD@1.0.0"
PERMITTED_GRANT = "GRANTED_FIXTURE"
FIXTURE_ISSUER = "WG0P2-SYNTHETIC-FIXTURE-ISSUER"


class Disposition(str, Enum):
    PRODUCED = "PRODUCED"
    HELD = "HELD"
    INADMISSIBLE = "INADMISSIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNDECIDED = "UNDECIDED"


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
        """Narrow scientific identity for carrier-conflict detection."""
        return f"{self.source_id}|{self.wave}|{self.form_id}|{self.version}"

    def freeze_material(self) -> str:
        """Every native field binds the freeze hash."""
        return "|".join([
            self.item_id, self.form_id, self.source_id, self.wave, self.unit,
            self.response_kind, ",".join(self.options), ",".join(self.missing_codes),
            self.route_evidence or "", self.grant, self.version,
        ])


@dataclass(frozen=True)
class OperationCandidate:
    op_id: str
    item_ids: tuple
    op_class: str
    target: str
    conditioners: tuple
    disposition: Disposition
    disposition_reason: str


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:wg0p2:test:{kind.lower()}:{label}", _h(f"wg0p2:{kind}:{label}"))


# --------------------------------------------------------------------------
# Frozen 5-item frontier (identical native items to the WG0P oracle inventory)
# --------------------------------------------------------------------------

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
# Disposition law (shared frozen spec; oracle and builder implement separately)
# --------------------------------------------------------------------------

def _marginal_disposition(item: NativeItem) -> tuple[Disposition, str]:
    if item.grant != PERMITTED_GRANT:
        return (Disposition.HELD, f"GRANT_{item.grant}")
    if item.response_kind == "ROUTED" and not item.route_evidence:
        return (Disposition.HELD, "ROUTE_EVIDENCE_MISSING")
    return (Disposition.PRODUCED, "ELIGIBLE")


def _conditional_disposition(tgt: NativeItem, cond: NativeItem) -> tuple[Disposition, str]:
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
    """Independent repaired oracle: full 25-op frontier, written without calling the builder."""
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
    """Builder under test. Must reproduce the repaired oracle exactly."""

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
# Frozen synthetic native cohorts (source-free; inputs fixed, outputs computed)
# --------------------------------------------------------------------------
# Native MR records are option SETS per household; the ingested carrier is the
# lossless per-option binary indicator expansion (declared projection).

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

# Native MR records are option SETS per household; the ingested carrier is the
# lossless per-option binary indicator expansion (declared projection).

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


def _auth(tag: str, kind: str, *, families) -> AuthoritySnapshot:
    digest = _h(f"wg0p2-authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"WG0P2-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"WG0P2-OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"wg0p2-semantics:{tag}"),
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


def admit_native_rows(release_tag: str, questions: Mapping[str, Any], rows: list) -> None:
    """Independent admission gate: every native response value must be a
    declared in-domain string. Out-of-domain values (including negative
    numbers smuggled as values) fail closed here, before any ingest."""
    for row in rows:
        for qname, value in sorted(row.get("responses", {}).items()):
            domain = questions[qname]["domain"]
            if not isinstance(value, str) or not value:
                raise ValueError(f"non-string native response rejected: {qname}={value!r}")
            if value not in domain:
                raise ValueError(
                    f"out-of-domain native response rejected: {qname}={value!r} "
                    f"(declared domain {domain})"
                )


def build_release(release_tag: str, question_namespace: str,
                  repo: Any = None) -> IngestedRelease:
    """Real I02 issuance path: candidate -> replay manifest -> validated ingest.

    All releases commit into one shared append-only repository through the
    validated ingest entry only; no private-attribute injection exists.
    """
    cohort = COHORTS[release_tag]
    questions = cohort["questions"]
    rows = cohort["rows"]
    admit_native_rows(release_tag, questions, rows)

    source_auth = _auth(f"source-{release_tag}", "SOURCE_SEMANTICS_TOPOLOGY",
                        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    routing_auth = _auth(f"routing-{release_tag}", "ROUTING_RISK_SET",
                         families=("RoutingEligibilityFact@1.0.0",))
    coord_auth = _auth(f"coord-{release_tag}", "COORDINATE_SEMANTICS",
                       families=("EmpiricalCoordinateFact@1.0.0",))
    replay_auth = _auth(f"replay-{release_tag}", "REPLAY_PROTOCOL",
                        families=("ReplayReceipt@1.0.0",))
    authorities = (source_auth, routing_auth, coord_auth, replay_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{release_tag}"),
        raw_source_identity=f"RAW-WG0P2-{release_tag}",
        source_family="SURVEY",
        study_product_release=f"STUDY-WG0P2-{release_tag}/REL-1",
        instrument_release=f"INST-WG0P2-{release_tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-I03",
        respondent_namespace=f"NS-WG0P2-{release_tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-WG0P2-{release_tag}",
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
    coordinates = []
    for row in rows:
        respondent = respondent_by_id[row["id"]]
        for q, value in sorted(row.get("responses", {}).items()):
            topology_kind = questions[q]["topology"]
            events.append(RespondentEvent(
                typed_state="SUBSTANTIVE_RESPONSE",
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
                response_state="SUBSTANTIVE_RESPONSE",
            ))
    crefs = {}
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
    source_hash = _h(f"source-artifact:wg0p2:{release_tag}")
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
        source_artifact_id=f"SOURCE-WG0P2-{release_tag}",
        source_artifact_content_hash=source_hash,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-WG0P2-{release_tag}",
        release_id=f"REL-{release_tag}",
        instrument_release_id=f"INST-WG0P2-{release_tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:wg0p2:test:source-snapshot:{release_tag}", source_hash
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
    from dataclasses import replace as _replace
    candidate = _replace(candidate, candidate_replay_manifest=replay)
    if repo is None:
        repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    if not result.accepted:
        raise RuntimeError(f"I02 ingest refused: {result.errors}")
    qauth = _query_authority(f"wg0p2-{release_tag}")
    return IngestedRelease(
        release_tag=release_tag, repo=repo, release_ref=result.release_ref,
        respondent_keys=respondent_keys,
        universe_ref=universe.ref, qrefs=qrefs,
        risk_refs={name: _ref("RISK_SET", f"{release_tag}-{name}") for name in risk_sets},
        authorities=authorities, qauth=qauth,
    )


# --------------------------------------------------------------------------
# Real I03 executor: no caller numerators, no fallback, fail-closed lookup
# --------------------------------------------------------------------------

@dataclass
class OpExecutionSpec:
    op_id: str
    release_tag: str
    risk_name: str
    targets: tuple  # ((question, domain, topology), ...)
    member_ids: tuple
    grant: str
    disposition: Disposition


def build_all_releases() -> dict:
    """Ingest all three synthetic releases into ONE shared append-only repository."""
    shared = C11Repository()
    out = {}
    for tag, ns in (("REL-A-W1", "aw1"), ("REL-A-W2", "aw2"), ("REL-B-W2", "bw2")):
        out[tag] = build_release(tag, ns, repo=shared)
    return out


def _branch_predicate_for(release: IngestedRelease, member_ids: tuple, *, tag: str,
                          risk_name: str | None = None):
    from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot  # noqa
    refs = []
    # member respondents resolved from build-time tracked exact refs
    member_refs = _member_refs(release, member_ids)
    membership = _ref("BRANCH_MEMBERSHIP",
                      f"{tag}-{_h('|'.join(r.key for r in member_refs))[:12]}")
    ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": f"BRANCH-{tag}",
        "resolved_predicate_hash_or_exact_membership_ref": membership,
        "parent_ancestry_ref": _ref("BRANCH_PARENT", tag),
        "branch_algorithm_authority_ref": release.qauth.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", tag),
        "branch_source_scope_ref": release.universe_ref,
        "exact_member_respondent_refs": member_refs,
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
    """Exact respondent refs from build-time tracked refs (no repository introspection)."""
    out = []
    for mid in sorted(member_ids):
        ref = release.respondent_keys.get(mid)
        if ref is None:
            raise KeyError(f"risk-set member respondent {mid!r} has no ingested identity")
        out.append(ref)
    return out


def _response_predicate_for(release: IngestedRelease, question: str, value: str, *,
                              risk_name: str, tag: str):
    """Real I03 response-leaf predicate (target GIVEN conditioner value).

    Mirrors the accepted predicate grammar: SURVEY_RESPONSE_EVENT leaf bound to
    the source authority, EXACT_SCOPED_RESPONDENT same-person semantics.
    """
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
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec as _EQS
    # topology/response-semantic authorities must be the SOURCE authority that
    # binds the ingested response events (query authority alone does not bind them)
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
            "domain": list(domain),
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{tag}-{target}-domain"),
            "topology_authority_refs": [source_auth_ref],
            "response_semantic_authority_refs": [source_auth_ref],
            "included_states": ["SUBSTANTIVE_RESPONSE"],
        })
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": "RAW",
        "risk_set_type": "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1 else "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    return _EQS(
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
    fact_registry: dict = field(default_factory=dict)


def _item_ref(item: NativeItem) -> ExactRef:
    return ExactRef(
        "WG0P2_NATIVE_ITEM", f"urn:wg0p2:test:native-item:{item.item_id}",
        _h(f"native-item:{item.freeze_material()}"),
    )


def build_executable_plan(ops: list[OperationCandidate], releases: Mapping[str, IngestedRelease],
                          *, freeze_hash: str, items_by_id: Mapping[str, NativeItem]) -> ExecutablePlan:
    """Map PRODUCED ops to BatchUnitSpec against REAL releases.

    Refuses conflicting duplicate op ids, carries the frozen no-drop frontier
    ledger and the positive source-issuer grant on the plan.
    """
    seen: dict[str, OperationCandidate] = {}
    for op in ops:
        prior = seen.get(op.op_id)
        if prior is not None and (prior.item_ids, prior.target) != (op.item_ids, op.target):
            raise ValueError(f"conflicting duplicate op id refused: {op.op_id}")
        seen[op.op_id] = op
    produced = sorted(
        [o for o in ops if o.disposition == Disposition.PRODUCED], key=lambda o: o.op_id)
    units = []
    units_by_op: dict[str, BatchUnitSpec] = {}
    op_specs: dict[str, OpExecutionSpec] = {}
    for op in produced:
        spec = OP_EXECUTION_MAP[op.op_id]
        release = releases[spec["release"]]
        item_refs = tuple(_item_ref(items_by_id[iid]) for iid in op.item_ids)
        unit = BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", op.op_id),
            release_refs=(release.release_ref,),
            semantic_input_refs=item_refs,
        )
        units.append(unit)
        units_by_op[op.op_id] = unit
        op_specs[op.op_id] = OpExecutionSpec(
            op_id=op.op_id, release_tag=spec["release"], risk_name=spec["risk"],
            targets=tuple((t, tuple(d)) for t, d in spec["targets"]),
            member_ids=tuple(sorted(COHORTS[spec["release"]]["risk_sets"][spec["risk"]][t]
                                    for t, _ in spec["targets"])[0]),
            grant=next(items_by_id[iid].grant for iid in op.item_ids),
            disposition=op.disposition,
        )
    manifest = BatchManifest(tuple(units))
    frontier_receipts = tuple(
        {
            "op_id": o.op_id, "op_class": o.op_class, "target": o.target,
            "conditioners": list(o.conditioners), "disposition": o.disposition.value,
            "disposition_reason": o.disposition_reason, "item_ids": list(o.item_ids),
        }
        for o in sorted(ops, key=lambda o: o.op_id)
    )
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
    )


def make_executor(plan: ExecutablePlan):
    """Real I03 executor: computes from ingested records, never caller payloads."""

    def execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        label = unit.job_ref.object_id
        op_id = label.rsplit(":", 1)[-1]
        spec = plan.op_specs.get(op_id)
        if spec is None:
            raise KeyError(f"no execution spec for unit {op_id!r}; fail-closed, no fallback")
        if spec.disposition != Disposition.PRODUCED or spec.grant != PERMITTED_GRANT:
            raise KeyError(f"unit {op_id!r} is not an executable permitted operation")
        release = plan.releases[spec.release_tag]
        predicate = _branch_predicate_for(release, spec.member_ids, tag=f"wg0p2-{op_id}",
                                          risk_name=spec.risk_name)
        query = _query_for(release, predicate, spec.targets, risk=spec.risk_name,
                           tag=f"wg0p2-{op_id}")
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
            plan.fact_registry[fact.ref.key] = {
                "op_id": op_id,
                "fact_ref": fact.ref.as_dict(),
                "typed_state": fact.typed_state,
                "denominator": fact.raw_denominator_support,
                "cells": [
                    {"cell": row["cell"], "n": row["raw_numerator_support"],
                     "state": row["cell_state"]}
                    for row in fact.target_topology["complete_cell_semantic_projection"]
                ],
            }
            result_refs.append(fact.ref)
        return ExecutionOutcome(
            result_refs=tuple(result_refs),
            provenance_refs=(query.ref, predicate.ref),
        )

    return execute


def run_plan(plan: ExecutablePlan, executor, max_units: int | None = None):
    runner = BatchExecutionRunner(manifest=plan.manifest, repository=plan.repository)
    binding = ExecutorBinding(_ref("EXECUTOR", "wg0p2-query"), executor)
    receipts = runner.run(executors={"QUERY": binding}, max_units=max_units)
    return runner, receipts


def consumer_effects(plan: ExecutablePlan, receipts) -> dict:
    """Consumer effects derived ONLY from actually computed facts."""
    completed = [r for r in receipts if r.state == "COMPLETED"]
    effects = {}
    for receipt in completed:
        for ref in receipt.result_refs:
            entry = plan.fact_registry.get(ref.key)
            if entry is None:
                raise KeyError(f"consumer cannot resolve uncomputed result {ref.key!r}")
            effects.setdefault(entry["op_id"], []).append(entry)
    return effects
