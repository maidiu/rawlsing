"""C5 — PRE-V3 SOURCEFREE contextual possibility navigation over actual FF01.

C4 already hands PRE-V3 an exact, pinned, source-coherent hypothetical
k-dimensional joint case. This module adds a substantive *continuing*
scenario interface: ask which additional source states are observed together,
follow a sequence of admissible constraints, preserve low-N/zero/tied
branches, and obtain/replay a final coherent C4 offer.

The candidate navigator is NOT psychological recruitment, actor genesis,
world/position materialization, nor a new survey estimator. "Possibility"
below means only raw complete-case support in ONE actual I03/S04/FF01 joint.
No C11 or I03 reread; no source/actor permission is granted.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_s04_field_forge_v3_bridge import (
    EmpiricalSeamError, V3SeamEnvelope, V3SeamExternalPin,
    _restored, consume_v3_empirical_case_offer,
)
from rawlsing_next.field_forge_observed_research import (
    ask_exact_descriptive_support,
)

PLAN_CONTRACT = "PYAT_FF01_PREV3_CONTEXT_POSSIBILITY_MAP@1"
PATH_CONTRACT = "PYAT_FF01_PREV3_REPLAYABLE_CONTEXT_PATH@1"
GRADE = "SOURCEFREE_OBSERVED_FULL_CASE_POSSIBILITY_NOT_PERSON_OR_POPULATION"
MAX_DIMENSIONS = 24
MAX_STATES_PER_MAP = 256
MAX_PATH_LENGTH = 16

class V3ContextNavigationError(ValueError):
    """A scenario attempted to exceed the exact source evidence or rights."""


@dataclass(frozen=True)
class V3ContextPossibilityMap:
    payload_json: str
    digest: str

    def __post_init__(self) -> None:
        try:
            obj = loads(self.payload_json)
            if (type(obj) is not dict or obj.get("contract") != PLAN_CONTRACT
                    or canonical_json(obj) != self.payload_json
                    or semantic_hash(obj) != self.digest):
                raise V3ContextNavigationError("invalid exact contextual map identity")
        except (ValueError, TypeError) as exc:
            raise V3ContextNavigationError("invalid contextual map payload") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(PLAN_CONTRACT,
                        "urn:rawlsing:ff-prev3:context-map:sha256:" + self.digest,
                        self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


@dataclass(frozen=True)
class V3ContextPath:
    payload_json: str
    digest: str

    def __post_init__(self) -> None:
        try:
            obj = loads(self.payload_json)
            if (type(obj) is not dict or obj.get("contract") != PATH_CONTRACT
                    or canonical_json(obj) != self.payload_json
                    or semantic_hash(obj) != self.digest):
                raise V3ContextNavigationError("invalid exact contextual path identity")
        except (ValueError, TypeError) as exc:
            raise V3ContextNavigationError("invalid contextual path payload") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(PATH_CONTRACT,
                        "urn:rawlsing:ff-prev3:context-path:sha256:" + self.digest,
                        self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _seal(material: dict[str, Any], cls):
    return cls(canonical_json(material), semantic_hash(material))


def _source(envelope: V3SeamEnvelope, external_pin: V3SeamExternalPin):
    if type(external_pin) is not V3SeamExternalPin:
        raise V3ContextNavigationError("independent actual C4 external pin required")
    # C4 is the established exact source authority boundary. Do NOT build
    # another FF01 type from arbitrary JSON or accept a self-signed archive.
    original, ff, dhikr = _restored(envelope, external_pin)
    f, d = ff.semantic_projection(), dhikr.material()
    if f["joint_arity"] != len(f["target_refs"]):
        raise V3ContextNavigationError("joint dimension/ref mismatch")
    if original["target_index"] != d["target_axis"]:
        raise V3ContextNavigationError("C4/DHIKR target contradiction")
    if f["producer_state"] == "SUPPORTED":
        rows = f["complete_cells"]
        if sum(row["raw_support"] for row in rows) != f["raw_fully_resolved_joint_n"]:
            raise V3ContextNavigationError("C4 source full-case n changed")
    elif f["complete_cells"]:
        raise V3ContextNavigationError("upstream-held source leaked observed cells")
    return original, ff, f, d


def _source_domains(f: Mapping[str, Any]):
    if f["producer_state"] != "SUPPORTED":
        return {}
    domains = {}
    for axis in range(f["joint_arity"]):
        values = {
            canonical_json(row["cell"][axis]): row["cell"][axis]
            for row in f["complete_cells"]
        }
        domains[axis] = {k: values[k] for k in sorted(values)}
    return domains


def _condition(
    conditions: Mapping[int, Any],
    *,
    f: Mapping[str, Any],
    domains: Mapping[int, Mapping[str, Any]],
) -> dict[int, Any]:
    if not isinstance(conditions, Mapping):
        raise V3ContextNavigationError("exact source-axis context mapping required")
    if len(conditions) > MAX_DIMENSIONS:
        raise V3ContextNavigationError("context exceeds bounded dimensions")
    bound = {}
    for axis, value in conditions.items():
        if type(axis) is not int or not 0 <= axis < f["joint_arity"]:
            raise V3ContextNavigationError("context axis does not exist in source")
        try:
            state = canonicalize(value)
            key = canonical_json(state)
        except (ValueError, TypeError) as exc:
            raise V3ContextNavigationError("noncanonical source condition") from exc
        if domains and key not in domains[axis]:
            raise V3ContextNavigationError("context value outside actual source joint domain")
        bound[axis] = state
    return dict(sorted(bound.items()))


def _context_rows(f: Mapping[str, Any], context: Mapping[int, Any]) -> list[dict[str, Any]]:
    if f["producer_state"] != "SUPPORTED":
        return []
    return [
        row for row in f["complete_cells"]
        if all(canonical_json(row["cell"][axis]) == canonical_json(state)
               for axis, state in context.items())
    ]


def _total(rows: Sequence[dict[str, Any]]) -> int:
    return sum(row["raw_support"] for row in rows)


def _branch_status(n: int | None, min_n: int) -> str:
    if n is None:
        return "UPSTREAM_TYPED_HELD__NO_INFERRED_ZERO"
    if n == 0:
        return "OBSERVED_ZERO_IN_COMPLETE_CASE__NOT_IMPOSSIBLE"
    if n < min_n:
        return "LOW_COMPLETE_CASE_N__NO_CANDIDATE_OFFER"
    return "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER"


def _exact_context(context: Mapping[int, Any], f: Mapping[str, Any]):
    return [
        {"axis": axis, "target_ref": f["target_refs"][axis],
         "exact_state": context[axis]}
        for axis in sorted(context)
    ]


def plan_v3_sourcefree_context_branches(
    *,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
    conditions: Mapping[int, Any],
    candidate_axes: Sequence[int] | None = None,
    min_context_n: int | None = None,
) -> V3ContextPossibilityMap:
    """Ask what source states can follow a given scenario on this SAME joint.

    No statistical inference: for each unbound source axis, ALL source-domain
    states (including zero cells) form a conserving partition of the same
    conditioned full-case sample n. There is no per-wave/source pooling.
    """
    m, ff, f, d = _source(envelope, external_pin)
    if min_context_n is not None and (
            type(min_context_n) is not int or min_context_n < 2):
        raise V3ContextNavigationError("minimum contextual n must be integer >= 2")
    required = max(m["min_branch_n"], min_context_n or 2)
    domains = _source_domains(f)
    context = _condition(conditions, f=f, domains=domains)
    if candidate_axes is None:
        axes = tuple(a for a in range(f["joint_arity"]) if a not in context)
    else:
        if (isinstance(candidate_axes, (str, bytes))
                or not isinstance(candidate_axes, Sequence)):
            raise V3ContextNavigationError("candidate axes must be explicit sequence")
        axes = tuple(candidate_axes)
        if (len(axes) != len(set(axes))
                or any(type(a) is not int or a in context
                       or not 0 <= a < f["joint_arity"] for a in axes)):
            raise V3ContextNavigationError("duplicate, conditioned or foreign candidate axis")
        axes = tuple(sorted(axes))
    if len(axes) > MAX_DIMENSIONS:
        raise V3ContextNavigationError("unbounded candidate axis request")
    if domains and sum(len(domains[a]) for a in axes) > MAX_STATES_PER_MAP:
        raise V3ContextNavigationError("explicit branch budget exceeded; request fewer axes")

    supported = f["producer_state"] == "SUPPORTED" and d["state"] == "SOURCE_COHERENT_SAMPLE_COMPARISON"
    base_rows = _context_rows(f, context) if supported else []
    base_n = _total(base_rows) if supported else None
    axis_products = []
    for axis in axes:
        branches = []
        if supported:
            for key, value in domains[axis].items():
                selected = _context_rows(f, {**context, axis: value})
                n = _total(selected)
                state = _branch_status(n, required)
                target_read_ref = None
                target_alternatives = []
                # Actual FF01 first reader, not a recreated estimator. Never
                # ask target conditional evidence when target itself is bound.
                if n >= required and m["target_index"] not in context and axis != m["target_index"]:
                    read = ask_exact_descriptive_support(
                        received=ff, target_index=m["target_index"],
                        conditions={**context, axis: value},
                    )
                    if read.material()["condition_fully_resolved_n"] != n:
                        raise V3ContextNavigationError("FF01 candidate n diverged from same joint")
                    target_read_ref = read.ref.as_dict()
                    observed = read.material()["complete_case_cells"]
                    if sum(cell["raw_count"] for cell in observed) != n:
                        raise V3ContextNavigationError("FF01 target-state partition changed joint n")
                    maximum = max(cell["raw_count"] for cell in observed)
                    tied = sum(1 for cell in observed
                               if cell["raw_count"] == maximum) != 1
                    target_alternatives = [
                        {
                            "source_target_state": cell["target_state"],
                            "raw_target_n": cell["raw_count"],
                            "observed_sample_status": (
                                "OBSERVED_ZERO_NOT_IMPOSSIBILITY"
                                if cell["raw_count"] == 0
                                else "TIED_SAMPLE_MODAL_NO_SINGLE_MAJORITY"
                                if tied and cell["raw_count"] == maximum
                                else "SAMPLE_UNIQUE_MODAL"
                                if cell["raw_count"] == maximum
                                else "SAMPLE_NONMODAL_NOT_TRAIT_OR_COHORT"
                            ),
                        }
                        for cell in observed
                    ]
                branches.append({
                    "exact_state": value,
                    "raw_complete_case_n": n,
                    "status": state,
                    "source_target_conditional_support_ref": target_read_ref,
                    "source_target_alternatives": target_alternatives,
                    "target_alternative_grade": (
                        "OBSERVED_RAW_SAMPLE_MODALITY__NOT_PERSONAL_TRAIT"
                        if target_read_ref else "WITHHELD_OR_TARGET_ALREADY_CONDITIONED"
                    ),
                    "not_a_population_probability": True,
                })
            if sum(b["raw_complete_case_n"] for b in branches) != base_n:
                raise V3ContextNavigationError("candidate axis partition changed same-case n")
        axis_products.append({
            "axis": axis,
            "target_ref": f["target_refs"][axis],
            "state": "SOURCE_OBSERVED_PARTITION" if supported else "UPSTREAM_TYPED_HELD",
            "branches": branches,
            "partition_sum_conserves_base_full_cases": True if supported else None,
        })
    result = {
        "contract": PLAN_CONTRACT, "grade": GRADE,
        "source_handoff_ref": envelope.ref.as_dict(),
        "source_ff01_ref": ff.ref.as_dict(),
        "source_dhikr_ref": m["dhikr_ref"],
        "external_source_pin_grade": "MATCHED_EXACT_ROOTS__NO_RIGHTS_ISSUED",
        "target_index": m["target_index"],
        "context": _exact_context(context, f),
        "candidate_axes": list(axes),
        "min_context_n": required,
        "state": _branch_status(base_n, required),
        "base_raw_complete_case_n": base_n,
        "source_observed_axes": axis_products,
        "full_joint_arity": f["joint_arity"],
        "not_issued": m["not_issued"],
        "new_i03_queries": 0,
        "semantic_limit": "OBSERVED_SOURCEFREE_RAW_JOINT_ONLY__NO_NATIVE_SCIENCE_OR_ACTOR",
    }
    return _seal(result, V3ContextPossibilityMap)


def run_v3_sourcefree_context_path(
    *,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
    starting_conditions: Mapping[int, Any],
    steps: Sequence[tuple[int, Any]],
    seed: int,
    min_context_n: int | None = None,
) -> V3ContextPath:
    """A replayable multi-step scenario narrowing one existing I03 joint.

    A step may be explored even if it turns out unsupported, but once it
    reaches a low/zero/producer-held branch it cannot be used to infer a
    subsequent supported context. This is a decision *proposal*, not life.
    """
    if (type(seed) is not int or seed < 0):
        raise V3ContextNavigationError("nonnegative integer seed required")
    if (not isinstance(steps, Sequence) or isinstance(steps, (str, bytes))
            or len(steps) > MAX_PATH_LENGTH):
        raise V3ContextNavigationError("path must be bounded source-axis sequence")
    m, _, f, _ = _source(envelope, external_pin)
    context = _condition(starting_conditions, f=f, domains=_source_domains(f))
    start = _exact_context(context, f)
    requested_steps = []
    history = []
    for step in steps:
        if (not isinstance(step, (list, tuple)) or len(step) != 2
                or type(step[0]) is not int):
            raise V3ContextNavigationError("path step must bind exact integer source axis")
        axis, value = step
        if axis in context:
            raise V3ContextNavigationError("source axis already conditioned; explicit fork required")
        try:
            requested = canonicalize(value)
        except (ValueError, TypeError) as exc:
            raise V3ContextNavigationError("noncanonical path source state") from exc
        # A focused one-axis map conserves the exact same baseline full cases.
        preview = plan_v3_sourcefree_context_branches(
            envelope=envelope, external_pin=external_pin, conditions=context,
            candidate_axes=(axis,), min_context_n=min_context_n,
        )
        p = preview.material()
        matched = [
            branch for branch in p["source_observed_axes"][0]["branches"]
            if canonical_json(branch["exact_state"]) == canonical_json(requested)
        ]
        if f["producer_state"] == "SUPPORTED":
            if len(matched) != 1:
                raise V3ContextNavigationError("requested path state outside actual domain")
            chosen = matched[0]
            status = chosen["status"]
            n = chosen["raw_complete_case_n"]
        else:
            status = "UPSTREAM_TYPED_HELD__NO_INFERRED_ZERO"
            n = None
        context[axis] = requested
        context = dict(sorted(context.items()))
        entry = {
            "step": len(history), "axis": axis, "target_ref": f["target_refs"][axis],
            "exact_state": context[axis],
            "from_context_map_ref": preview.ref.as_dict(),
            "base_complete_case_n": p["base_raw_complete_case_n"],
            "next_complete_case_n": n,
            "disposition": status,
        }
        history.append(entry)
        requested_steps.append({"axis": axis, "state": context[axis]})
        if status != "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER":
            # Preserve the attempt and its failure as an actual branch
            # result, but do not pretend additional selections can follow.
            if len(history) != len(steps):
                raise V3ContextNavigationError("cannot extend a held/zero path")
            break

    offer = consume_v3_empirical_case_offer(
        envelope=envelope, external_pin=external_pin,
        conditions=context, seed=seed, min_context_n=min_context_n,
    )
    o = offer.material()
    assert_status = _branch_status(
        o["raw_conditioned_complete_case_n"],
        o["minimum_required_context_n"],
    )
    c4_states = {
        "UPSTREAM_TYPED_HELD__NO_INFERRED_ZERO": "PRODUCER_TYPED_HELD__NO_CASE_OFFER",
        "OBSERVED_ZERO_IN_COMPLETE_CASE__NOT_IMPOSSIBLE": "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY",
        "LOW_COMPLETE_CASE_N__NO_CANDIDATE_OFFER": "LOW_CONTEXT_SUPPORT__ABSTAIN",
        "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER": "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER",
    }
    if o["state"] != c4_states[assert_status]:
        raise V3ContextNavigationError("C4 offer contradicts source-observed navigation support")
    if (o["state"] != "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
            and o["selected_complete_joint_cell"]):
        raise V3ContextNavigationError("C4 held context leaked hypothetical case")
    result = {
        "contract": PATH_CONTRACT, "grade": GRADE,
        "source_handoff_ref": envelope.ref.as_dict(),
        "source_ff01_ref": m["ff01_ref"],
        "source_dhikr_ref": m["dhikr_ref"],
        "external_source_pin_grade": "MATCHED_EXACT_ROOTS__NO_RIGHTS_ISSUED",
        "starting_context": start,
        "requested_steps": requested_steps,
        "history": history,
        "final_context": _exact_context(context, f),
        "status": o["state"],
        "final_raw_complete_case_n": o["raw_conditioned_complete_case_n"],
        "final_case_offer_ref": offer.ref.as_dict(),
        "final_case_offer_payload": o,
        "min_context_n": max(m["min_branch_n"], min_context_n or 2),
        "seed": seed,
        "new_i03_queries": 0,
        "object_scope": "HYPOTHETICAL_WHOLE_JOINT_CONFIGURATION_NOT_ACTOR",
        "not_issued": m["not_issued"],
    }
    return _seal(result, V3ContextPath)


def replay_v3_sourcefree_context_path(
    *,
    path: V3ContextPath,
    envelope: V3SeamEnvelope,
    external_pin: V3SeamExternalPin,
) -> V3ContextPath:
    """Cold replay with actual C4 source pins, not a self-rehashed fiction."""
    if type(path) is not V3ContextPath:
        raise V3ContextNavigationError("typed path receipt required")
    p = path.material()
    if p["source_handoff_ref"] != envelope.ref.as_dict():
        raise V3ContextNavigationError("path source envelope swapped")
    context = {x["axis"]: x["exact_state"] for x in p["starting_context"]}
    steps = [(x["axis"], x["state"]) for x in p["requested_steps"]]
    rebuilt = run_v3_sourcefree_context_path(
        envelope=envelope, external_pin=external_pin,
        starting_conditions=context, steps=steps,
        seed=p["seed"], min_context_n=p["min_context_n"],
    )
    if rebuilt.ref != path.ref:
        raise V3ContextNavigationError("context path failed independently pinned replay")
    return rebuilt


__all__ = [
    "PLAN_CONTRACT", "PATH_CONTRACT", "GRADE", "V3ContextNavigationError",
    "V3ContextPossibilityMap", "V3ContextPath",
    "plan_v3_sourcefree_context_branches",
    "run_v3_sourcefree_context_path",
    "replay_v3_sourcefree_context_path",
]
