"""PYAT sourcefree executable S04/DHIKR -> FF01 -> PRE-V3 empirical handoff.

THIS IS A FIRST, REAL CONSUMER, NOT AN ACTOR OR A STRUCTURAL/CAUSAL CLAIM.
One already executed I03 result is read by the existing S04 receiver and the
existing FF01 receiver. DHIKR explores the SAME full-case sample joint.
A V3-facing request can then draw a whole observed joint configuration,
conditional on actual source states: no independent marginal sampling and no
re-decoding of survey respondents. Sourcefree only; original data and actor
ownership require separately issued rights.

The frozen FF->PRE-V3 structural relation admission and the Sorok actor
issuers are NEVER bypassed. This is an empirical candidate interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from random import Random
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, EmpiricalQuerySpec, canonical_json, canonicalize,
    exact_ref, semantic_hash,
)
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_s04_cold_custody import SOURCEFREE_ASSERTION
from rawlsing_next.pre553_s04_first_consumer import (
    S04OnePassResult, receive_s04_first_consumer,
)
from rawlsing_next.pre553_s04_dhikr_comparative import (
    DHIKRComparisonRequest, DHIKRComparisonReceipt,
)
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralJointWorkspace
from rawlsing_next.field_forge_generic_empirical_ingress import FF01ObservedJoint
from rawlsing_next.field_forge_observed_research import (
    ask_exact_descriptive_support,
)

CONTRACT = "PYAT_S04_DHIKR_FF01_PREV3_EMPIRICAL_HANDOFF@1"
OFFER_CONTRACT = "PYAT_PREV3_SOURCE_COHERENT_CASE_OFFER@1"
GRADE = "SOURCEFREE_RAW_COHERENT_JOINT__EMPIRICAL_PROPOSAL_ONLY"
NOT_ISSUED = (
    "ORIGINAL_SURVEY_USE_OR_DISCLOSURE_RIGHTS",
    "POPULATION_REPRESENTATIVE_PROBABILITIES",
    "COMPLEX_SURVEY_DESIGN_VARIANCE",
    "CAUSAL_OR_STRUCTURAL_FIELD_FORGE_RELATION",
    "V557_V558_WORLD_SELECTION_OR_M1_ADMISSION",
    "N10E_N10W_ACTOR_POSSIBILITY_ISSUER",
    "V3_OR_SOROK_PERSON_OR_RECRUITMENT_AUTHORITY",
)


class EmpiricalSeamError(ValueError):
    """Refuse handoff, forged replay, unsupported case or authority promotion."""


@dataclass(frozen=True)
class V3SeamExternalPin:
    """Independently held source/consumer identities; NOT included in archive."""
    query_ref: ExactRef
    fact_ref: ExactRef
    release_ref: ExactRef
    s04_ref: ExactRef
    ff01_ref: ExactRef
    dhikr_ref: ExactRef
    one_pass_ref: ExactRef

    def __post_init__(self) -> None:
        for field in self.__dataclass_fields__:
            if type(getattr(self, field)) is not ExactRef:
                raise EmpiricalSeamError("external pin must hold actual ExactRef objects")


@dataclass(frozen=True)
class V3SeamEnvelope:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            material = loads(self.payload_json)
            if (type(material) is not dict or material.get("contract") != CONTRACT
                    or canonical_json(material) != self.payload_json
                    or semantic_hash(material) != self.content_hash
                    or material.get("sourcefree_assertion") != SOURCEFREE_ASSERTION):
                raise EmpiricalSeamError("invalid sourcefree empirical handoff identity")
        except (TypeError, ValueError) as exc:
            raise EmpiricalSeamError("invalid empirical handoff payload") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT, "urn:rawlsing:pyat:ff-prev3:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class V3EmpiricalCaseOffer:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            material = loads(self.payload_json)
            if (type(material) is not dict
                    or material.get("contract") != OFFER_CONTRACT
                    or canonical_json(material) != self.payload_json
                    or semantic_hash(material) != self.content_hash):
                raise EmpiricalSeamError("V3 empirical offer is not content exact")
        except (TypeError, ValueError) as exc:
            raise EmpiricalSeamError("invalid V3 empirical offer") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            OFFER_CONTRACT,
            "urn:rawlsing:pyat:prev3-case-offer:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class V3EmpiricalBuild:
    first_consumer: S04OnePassResult
    comparison: DHIKRComparisonReceipt
    envelope: V3SeamEnvelope
    external_pin: V3SeamExternalPin


def _ref(value: Any, label: str) -> ExactRef:
    try:
        return exact_ref(value, label)
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        raise EmpiricalSeamError(label + " must be an exact ref") from exc


def _same(a: Any, b: Any, label: str) -> None:
    if canonical_json(a) != canonical_json(b):
        raise EmpiricalSeamError("SOURCE_CLOSURE_CONTRADICTION:" + label)


def _source_closure(
    material: Mapping[str, Any],
    ff: FF01ObservedJoint,
    dhikr: DHIKRComparisonReceipt,
    pin: V3SeamExternalPin | None,
) -> None:
    fm, dm = ff.semantic_projection(), dhikr.material()
    if (material["sourcefree_assertion"] != SOURCEFREE_ASSERTION
            or material["grade"] != GRADE
            or material["scope"] != "SINGLE_UNIVERSE_RAW_COMPLETE_CASE"
            or material["not_issued"] != list(NOT_ISSUED)):
        raise EmpiricalSeamError("source/grade boundary changed")
    expected = (
        ("query_ref", "producer_query_ref", "source_query_ref"),
        ("fact_ref", "producer_fact_ref", "source_fact_ref"),
        ("release_ref", "release_ref", "source_release_ref"),
        ("risk_set_ref", "risk_set_ref", "source_risk_set_ref"),
    )
    for name, ff_key, dhikr_key in expected:
        _same(material[name], fm[ff_key], name + "/ff01")
        _same(material[name], dm[dhikr_key], name + "/dhikr")
    _same(material["ff01_ref"], ff.ref.as_dict(), "ff01")
    _same(material["dhikr_ref"], dhikr.ref.as_dict(), "dhikr")
    _same(material["s04_ref"], dm["source_knowledge_ref"], "s04")
    if (fm["joint_arity"] != len(fm["target_refs"])
            or fm["joint_arity"] < 2
            or dm["target_axis"] >= fm["joint_arity"]
            or fm["producer_state"] == "SUPPORTED" and
            dm["state"] != "SOURCE_COHERENT_SAMPLE_COMPARISON"
            or fm["producer_state"] != "SUPPORTED" and
            dm["state"] == "SOURCE_COHERENT_SAMPLE_COMPARISON"):
        raise EmpiricalSeamError("FF01 and DHIKR semantic positive/held grade conflict")
    if fm["producer_state"] == "SUPPORTED":
        _same(
            fm["raw_fully_resolved_joint_n"],
            dm["raw_original_full_joint_n"],
            "same-case-full-joint-n",
        )
    else:
        if fm["complete_cells"]:
            raise EmpiricalSeamError("held producer smuggled full-case cells")
    if (type(material.get("min_branch_n")) is not int
            or material["min_branch_n"] < 2
            or material.get("target_index") != dm["target_axis"]):
        raise EmpiricalSeamError("DHIKR candidate target or minimum support changed")
    original_nodes = dm["nodes"]
    published_nodes = material.get("source_observed_contexts")
    if type(published_nodes) is not list or len(published_nodes) != len(original_nodes):
        raise EmpiricalSeamError("cold FF/DHIKR contextual receipt missing/augmented")
    for original, published in zip(original_nodes, published_nodes):
        _same(published["node"], original["node"], "context-node-id")
        _same(published["dhikr_source_context"], original["context"],
              "context-node-ancestry")
        _same(published["raw_same_case_n"], original["raw_same_case_n"],
              "context-observed-n")
        if original["raw_same_case_n"] < material["min_branch_n"]:
            if (published["state"] != "HELD_BELOW_MINIMUM_CONTEXT_N"
                    or published["observed_research_ref"] is not None):
                raise EmpiricalSeamError("small context laundered as research")
        else:
            context = {item["axis"]: item["value"] for item in original["context"]}
            answer = ask_exact_descriptive_support(
                received=ff, target_index=dm["target_axis"], conditions=context,
            )
            _same(published["state"], answer.material()["state"],
                  "context-research-state")
            _same(published["observed_research_ref"], answer.ref.as_dict(),
                  "context-research-ref")
            _same(
                answer.material()["condition_fully_resolved_n"],
                original["raw_same_case_n"],
                "context-research-n",
            )
    if pin is not None:
        if type(pin) is not V3SeamExternalPin:
            raise EmpiricalSeamError("external root must be independent typed pin")
        for field in pin.__dataclass_fields__:
            _same(material[field].copy() if field in material else None,
                  getattr(pin, field).as_dict(), "external/" + field)


def _restored(
    envelope: V3SeamEnvelope,
    pin: V3SeamExternalPin | None,
) -> tuple[dict[str, Any], FF01ObservedJoint, DHIKRComparisonReceipt]:
    if type(envelope) is not V3SeamEnvelope:
        raise EmpiricalSeamError("exact sourcefree envelope required")
    m = envelope.material()
    try:
        projection = m["ff01_projection_json"]
        ff_content = loads(projection)
        ff_digest = semantic_hash(ff_content)
        ff = FF01ObservedJoint(
            projection_json=projection,
            content_hash=ff_digest,
            object_id="urn:rawlsing:ff01:observed-joint:sha256:" + ff_digest,
        )
        payload = m["dhikr_payload_json"]
        dhikr_content = loads(payload)
        dhikr = DHIKRComparisonReceipt(payload, semantic_hash(dhikr_content))
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        raise EmpiricalSeamError("cannot rehydrate established FF01/DHIKR consumers") from exc
    _source_closure(m, ff, dhikr, pin)
    return m, ff, dhikr


def build_empirical_field_forge_v3_handoff(
    *,
    query: EmpiricalQuerySpec,
    execution: QueryExecutionResult,
    comparison_request: DHIKRComparisonRequest,
    conditioner_index: int,
    sourcefree_origin_assertion: str,
    producer_permission_ceiling: tuple[str, ...] = ("FF01_DESCRIPTIVE_SOURCEFREE",),
) -> V3EmpiricalBuild:
    """Reuse original I03 exactly once. S04, DHIKR, FF01 are existing owners.

    Only an explicitly asserted synthetic sourcefree fixture may be serialized
    into this candidate bridge. An original wave needs a separately designed
    issued disclosure/redaction grant; caller strings cannot supply one.
    """
    if sourcefree_origin_assertion != SOURCEFREE_ASSERTION:
        raise EmpiricalSeamError("ORIGINAL_SOURCE_SEAM_RIGHTS_NOT_ISSUED")
    if (type(query) is not EmpiricalQuerySpec
            or type(execution) is not QueryExecutionResult
            or type(comparison_request) is not DHIKRComparisonRequest):
        raise EmpiricalSeamError("original typed I03 and exact DHIKR request required")
    result = receive_s04_first_consumer(
        query=query,
        execution=execution,
        conditioner_index=conditioner_index,
        producer_permission_ceiling=producer_permission_ceiling,
    )
    if result.ff01 is None:
        raise EmpiricalSeamError("actual generic FF01 consumer is mandatory")
    workspace = S04GeneralJointWorkspace(
        knowledge=result.knowledge,
        expected_knowledge_ref=result.knowledge.ref,
    )
    dhikr = workspace.compare_dhikr(comparison_request)
    ff = result.ff01
    sm = result.knowledge.material()
    fm = ff.semantic_projection()
    dm = dhikr.material()
    nodes = []
    for node in dm["nodes"]:
        context = {item["axis"]: item["value"] for item in node["context"]}
        if node["raw_same_case_n"] < comparison_request.min_branch_n:
            nodes.append({
                "node": node["node"],
                "dhikr_source_context": node["context"],
                "state": "HELD_BELOW_MINIMUM_CONTEXT_N",
                "raw_same_case_n": node["raw_same_case_n"],
                "observed_research_ref": None,
            })
            continue
        answer = ask_exact_descriptive_support(
            received=ff, target_index=comparison_request.target_axis,
            conditions=context,
        )
        am = answer.material()
        _same(
            am["condition_fully_resolved_n"],
            node["raw_same_case_n"],
            "DHIKR/FF01 node sample conservation",
        )
        nodes.append({
            "node": node["node"],
            "dhikr_source_context": node["context"],
            "state": am["state"],
            "raw_same_case_n": node["raw_same_case_n"],
            "observed_research_ref": answer.ref.as_dict(),
        })
    payload = {
        "contract": CONTRACT,
        "sourcefree_assertion": SOURCEFREE_ASSERTION,
        "grade": GRADE,
        "scope": "SINGLE_UNIVERSE_RAW_COMPLETE_CASE",
        "not_issued": list(NOT_ISSUED),
        "query_ref": query.ref.as_dict(),
        "fact_ref": execution.facts[0].ref.as_dict(),
        "release_ref": execution.release_refs[0].as_dict(),
        "risk_set_ref": sm["risk_set_ref"],
        "s04_ref": result.knowledge.ref.as_dict(),
        "one_pass_ref": result.receipt.ref.as_dict(),
        "ff01_ref": ff.ref.as_dict(),
        "dhikr_ref": dhikr.ref.as_dict(),
        "ff01_projection_json": ff.projection_json,
        "dhikr_payload_json": dhikr.payload_json,
        "target_index": comparison_request.target_axis,
        "min_branch_n": comparison_request.min_branch_n,
        "source_observed_contexts": nodes,
        "execution_count": "ONE_ALREADY_EXECUTED_I03__NO_REQUERY",
        "cold_rights": "SOURCEFREE_INSPECTION_WITH_INDEPENDENT_EXACT_ROOT_PIN",
    }
    envelope = V3SeamEnvelope(canonical_json(payload), semantic_hash(payload))
    pin = V3SeamExternalPin(
        query.ref, execution.facts[0].ref, execution.release_refs[0],
        result.knowledge.ref, ff.ref, dhikr.ref, result.receipt.ref,
    )
    _restored(envelope, pin)
    return V3EmpiricalBuild(result, dhikr, envelope, pin)


def consume_v3_empirical_case_offer(
    *,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
    conditions: Mapping[int, Any],
    seed: int,
    min_context_n: int | None = None,
) -> V3EmpiricalCaseOffer:
    """PRE-V3 first consumer: a WHOLE source-coherent hypothetical case.

    Samples one complete k-way observed joint cell on the same actual common
    risk, optionally restricted to caller context. It does not sample targets
    independently, infer a real respondent, or construct a Sorok actor.
    """
    if type(external_pin) is not V3SeamExternalPin:
        raise EmpiricalSeamError("cold V3 research requires separately held source pin")
    if type(seed) is not int or seed < 0:
        raise EmpiricalSeamError("explicit finite nonnegative integer seed required")
    if min_context_n is not None and (
        type(min_context_n) is not int or min_context_n < 2
    ):
        raise EmpiricalSeamError("minimum context support must be >=2")
    m, ff, dhikr = _restored(envelope, external_pin)
    fm, dm = ff.semantic_projection(), dhikr.material()
    if not isinstance(conditions, Mapping):
        raise EmpiricalSeamError("exact caller context mapping required")
    context: dict[int, Any] = {}
    for axis, value in conditions.items():
        if type(axis) is not int or not 0 <= axis < fm["joint_arity"]:
            raise EmpiricalSeamError("context axis outside actual source joint")
        if axis in context:
            raise EmpiricalSeamError("duplicate context axis")
        context[axis] = canonicalize(value)
    required_n = max(m["min_branch_n"], min_context_n or 2)
    rows = fm["complete_cells"]
    # Supported/held is NOT equivalent to zero. A held I03 cannot produce
    # a generated case even if earlier per-target counts were nonzero.
    supported = (fm["producer_state"] == "SUPPORTED"
                 and dm["state"] == "SOURCE_COHERENT_SAMPLE_COMPARISON")
    if supported:
        for axis, value in context.items():
            domain = {canonical_json(cell["cell"][axis]) for cell in rows}
            if canonical_json(value) not in domain:
                raise EmpiricalSeamError("context value outside source-issued domain")
    matching = [
        row for row in rows
        if all(canonical_json(row["cell"][axis]) == canonical_json(value)
               for axis, value in context.items())
    ] if supported else []
    n = sum(row["raw_support"] for row in matching)
    if supported and sum(row["raw_support"] for row in rows) != fm["raw_fully_resolved_joint_n"]:
        raise EmpiricalSeamError("FF01 full joint sample changed")
    state = (
        "PRODUCER_TYPED_HELD__NO_CASE_OFFER" if not supported
        else "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY" if n == 0
        else "LOW_CONTEXT_SUPPORT__ABSTAIN" if n < required_n
        else "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
    )
    selected = None
    if state == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER":
        selector_seed = int(semantic_hash({
            "source": envelope.ref.as_dict(),
            "conditions": [[axis, context[axis]] for axis in sorted(context)],
            "user_seed": seed,
        }), 16)
        draw = Random(selector_seed).randrange(n)
        running = 0
        for row in sorted(matching, key=lambda x: canonical_json(x["cell"])):
            running += row["raw_support"]
            if draw < running:
                selected = row
                break
        if selected is None:
            raise EmpiricalSeamError("real joint draw failed conservation")
    # A single observed joint cell is coherent but is not an observed
    # respondent record: no respondent ids/strings or independent marginals.
    proposal = [
        {"source_dimension": axis, "target_ref": fm["target_refs"][axis],
         "candidate_state": canonicalize(value)}
        for axis, value in enumerate(selected["cell"])
    ] if selected is not None else []
    answer = None
    # The complete target distribution is a separately derived conditional
    # research receipt. A low/zero-N abstention must NOT publish even its
    # keyed digest: that would defeat the held target-disclosure boundary.
    # This remains an API guard over sourcefree material, NOT an independently
    # authorized privacy system for original-survey cohorts.
    if (state == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
            and m["target_index"] not in context):
        answer = ask_exact_descriptive_support(
            received=ff, target_index=m["target_index"],
            conditions=context,
        )
        _same(
            answer.material()["condition_fully_resolved_n"], n,
            "same-case V3 target denominator",
        )
    payload = {
        "contract": OFFER_CONTRACT,
        "grade": GRADE,
        "state": state,
        "source_handoff_ref": envelope.ref.as_dict(),
        "source_ff01_ref": ff.ref.as_dict(),
        "source_dhikr_ref": dhikr.ref.as_dict(),
        "source_query_ref": m["query_ref"],
        "source_fact_ref": m["fact_ref"],
        "external_pin_check": "MATCHED_EXACT_REFERENCES__ISSUER_RIGHTS_UNVERIFIED",
        "target_axis": m["target_index"],
        "constraints": [
            {"axis": axis, "state": context[axis]}
            for axis in sorted(context)
        ],
        "raw_conditioned_complete_case_n": n if supported else None,
        "minimum_required_context_n": required_n,
        "source_target_distribution_ref": answer.ref.as_dict() if answer else None,
        "selected_complete_joint_cell": proposal,
        "selected_cell_support_raw": selected["raw_support"] if selected else None,
        "sampled_unit": "ANONYMOUS_COMPLETE_JOINT_CONFIGURATION_NOT_RESPONDENT",
        "selection_rule": (
            "REPRODUCIBLE_COUNT_WEIGHTED_DRAW_WITHIN_SAME_SOURCE_JOINT"
            if selected else "NO_DRAW_BECAUSE_TYPED_HOLD_ZERO_OR_INADEQUATE_SUPPORT"
        ),
        "seed": seed,
        "sorok_v3_actor_mutation": None,
        "structural_relation_admission": None,
        "not_issued": list(NOT_ISSUED),
    }
    return V3EmpiricalCaseOffer(canonical_json(payload), semantic_hash(payload))



def _private_directory(directory):
    """Sourcefree cold archive is an owned, nonlinked 0700 directory."""
    import os
    from pathlib import Path
    root = Path(directory).absolute()
    if root.is_symlink() or not root.is_dir():
        raise EmpiricalSeamError("private seam storage directory absent or linked")
    st = root.stat()
    if st.st_uid != os.geteuid() or st.st_mode & 0o077:
        raise EmpiricalSeamError("private seam storage directory not restricted")
    return root


def write_sourcefree_v3_handoff_private(
    directory, envelope: V3SeamEnvelope,
):
    """Cold sourcefree archive, atomic no-clobber, original roots NEVER stored."""
    import os
    from pathlib import Path
    from secrets import token_hex
    if type(envelope) is not V3SeamEnvelope:
        raise EmpiricalSeamError("only typed sourcefree seam archive is writable")
    _restored(envelope, None)
    root = _private_directory(directory)
    path = root / ("pyat-ff-prev3-" + envelope.content_hash + ".json")
    if path.exists() or path.is_symlink():
        raise EmpiricalSeamError("immutable content-addressed seam archive exists")
    body = canonical_json({
        "schema": CONTRACT + ":COLD@1",
        "envelope_payload_json": envelope.payload_json,
        "envelope_hash": envelope.content_hash,
        "external_source_roots": "SEPARATELY_HELD__NEVER_IN_ARCHIVE",
    }).encode("utf-8")
    if len(body) > (64 << 20):
        raise EmpiricalSeamError("bounded cold archive size exceeded")
    temp = root / (".tmp-ff-prev3-" + token_hex(16))
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        # Atomic no-clobber publish: relink to stable content name only after
        # fully written/closed data; never replace an independently held file.
        os.link(temp, path)
    finally:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
    return path


def read_sourcefree_v3_handoff_private(
    path, *, external_pin: V3SeamExternalPin,
) -> V3SeamEnvelope:
    """Cold sourcefree first reader; independent exact pin is mandatory."""
    import os
    import stat
    from pathlib import Path
    if type(external_pin) is not V3SeamExternalPin:
        raise EmpiricalSeamError("external source/consumer root pin required")
    leaf = Path(path).absolute()
    _private_directory(leaf.parent)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(leaf, flags)
    try:
        st = os.fstat(fd)
        if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid()
                or st.st_mode & 0o077 or st.st_nlink != 1
                or st.st_size > (64 << 20)):
            raise EmpiricalSeamError("cold seam file not private, single-linked, bounded")
        with os.fdopen(fd, "rb") as handle:
            fd = -1
            data = handle.read((64 << 20) + 1)
    finally:
        if fd >= 0:
            os.close(fd)
    try:
        cold = loads(data.decode("utf-8"))
        if (type(cold) is not dict or set(cold) != {
                "schema", "envelope_payload_json", "envelope_hash", "external_source_roots"
        } or cold["schema"] != CONTRACT + ":COLD@1"
                or cold["external_source_roots"] != "SEPARATELY_HELD__NEVER_IN_ARCHIVE"
                or canonical_json(cold).encode("utf-8") != data):
            raise EmpiricalSeamError("cold seam manifest is not exact")
        envelope = V3SeamEnvelope(
            cold["envelope_payload_json"], cold["envelope_hash"],
        )
    except (UnicodeError, ValueError, TypeError, KeyError) as exc:
        raise EmpiricalSeamError("cold seam bytes invalid") from exc
    if leaf.name != "pyat-ff-prev3-" + envelope.content_hash + ".json":
        raise EmpiricalSeamError("cold path does not match content identity")
    _restored(envelope, external_pin)
    return envelope


__all__ = [
    "CONTRACT", "OFFER_CONTRACT", "GRADE", "EmpiricalSeamError",
    "V3SeamExternalPin", "V3SeamEnvelope", "V3EmpiricalCaseOffer",
    "V3EmpiricalBuild", "build_empirical_field_forge_v3_handoff",
    "consume_v3_empirical_case_offer",
    "write_sourcefree_v3_handoff_private",
    "read_sourcefree_v3_handoff_private",
]
