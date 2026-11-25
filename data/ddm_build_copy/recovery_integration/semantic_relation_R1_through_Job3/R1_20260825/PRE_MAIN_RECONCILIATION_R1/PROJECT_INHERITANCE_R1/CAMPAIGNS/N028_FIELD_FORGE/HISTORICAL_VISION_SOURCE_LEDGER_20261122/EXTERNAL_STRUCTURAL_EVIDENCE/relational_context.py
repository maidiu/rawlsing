"""Provisional FIELD FORGE relational reader; consumes R6 and S04 exports.
Native contrasts are descriptive; modeled correspondences are not survey joins.
No new empirical query, source authorization, sampler, or world/actor writer.
"""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json

from native_priority_readers import JOIN_STATUS, WBL_QUESTIONS, FINDEX_MARGINS

S04_CONTRACT = "S04_GENERAL_SOURCE_EXACT_JOINT_PROJECTION@1.0.0"
S04_GRADE = "SINGLE_ACTUAL_I03_FULL_JOINT__RAW_SAMPLE_ONLY__NO_NEW_ISSUER"


def field_changes(a, b, fields):
    """Compare literal native values, not a rank or inferred causal effect."""
    result = {}
    for field in fields:
        x, y = a.get(field), b.get(field)
        result[field] = {"left": x, "right": y, "state": (
            "UNRESOLVED" if x is None or y is None else
            "UNCHANGED" if x == y else "DIFFERENT")}
    return result


def unique_contrast(left, right, fields):
    """Never select an arbitrary survey or silently turn an absent row into zero."""
    out = {"left": deepcopy(left), "right": deepcopy(right), "changes": {}}
    if left["source"] != right["source"] or left["sha256"] != right["sha256"]:
        out["state"] = "DIFFERENT_SOURCE_OR_RELEASE"
    elif len(left["rows"]) != 1 or len(right["rows"]) != 1:
        out["state"] = "NO_MATCH" if not left["rows"] or not right["rows"] else "MULTIPLE_NATIVE_ROWS"
    else:
        out["state"] = "DESCRIPTIVE_NATIVE_CONTRAST"
        out["changes"] = field_changes(left["rows"][0]["values"], right["rows"][0]["values"], fields)
    return out


def formation_changes(pack, gwid, left_year, right_year):
    """Same-release, same-polity native group identities, not identity of persons."""
    a = pack.select("EPR", {"gwid": gwid}, year=left_year)
    b = pack.select("EPR", {"gwid": gwid}, year=right_year)
    def grouped(r):
        result = {}
        for row in r["rows"]:
            result.setdefault(row["values"]["gwgroupid"], []).append(row)
        return result
    x, y = grouped(a), grouped(b)
    contrasts = []
    for group in sorted(x.keys() | y.keys()):
        l = dict(a, rows=x.get(group, []), keys={"gwid": gwid, "gwgroupid": group})
        r = dict(b, rows=y.get(group, []), keys={"gwid": gwid, "gwgroupid": group})
        l["status"] = "ROWS" if l["rows"] else "NO_MATCH"
        r["status"] = "ROWS" if r["rows"] else "NO_MATCH"
        contrasts.append({"gwgroupid": group, **unique_contrast(l, r, ("status", "size", "reg_aut", "umbrella", "group"))})
    return {"grade": "NATIVE_EPR_REFERENCE_YEAR_CONTRAST_NOT_ADMITTED",
            "gwid": gwid, "left_year": left_year, "right_year": right_year,
            "left": a, "right": b, "formations": contrasts,
            "limits": "No rank of statuses, group disappearance claim, population partition, person membership or continuous-time event."}


def context_contrast(pack, left, right):
    """Read two explicit R6 contexts; do not imply a synchronized historical world."""
    a, b = pack.context(**left), pack.context(**right)
    out = {"grade": "RETROSPECTIVE_DESCRIPTIVE_NOT_ADMITTED", "left": a, "right": b,
           "alignment": "CALLER_SELECTED_CONTEXTS_NOT_QUALIFIED_CROSSWALK"}
    out["epr"] = (formation_changes(pack, left["gwid"], left["epr_year"], right["epr_year"])
                  if left["gwid"] == right["gwid"] else {"state": "DISTINCT_POLITIES_NO_GROUP_MATCH"})
    out["wbl"] = unique_contrast(a["wbl"], b["wbl"], WBL_QUESTIONS)
    if left["subsample"] == right["subsample"]:
        out["join"] = unique_contrast(a["join"], b["join"], (*JOIN_STATUS, "Share of work contract",
            "Share of health insurance", "Share of social security", "Average weekly working hours"))
    else:
        out["join"] = {"state": "DIFFERENT_SUBSAMPLES_NO_CELL_CONTRAST"}
    if (left["fin_group"], left["fin_group2"]) == (right["fin_group"], right["fin_group2"]):
        out["findex"] = unique_contrast(a["findex"], b["findex"], FINDEX_MARGINS)
    else:
        out["findex"] = {"state": "DIFFERENT_PUBLISHED_SUBGROUPS_NO_CELL_CONTRAST"}
    out["next_questions"] = []
    for relation, question in (("wbl", "Which actual role, rule, counterparty and resource conditions make the legal difference operative?"),
                               ("join", "Which already measured employment positions and source-local repertoires coexist with these livelihood differences?"),
                               ("findex", "Which actual household or institutional resource channels reproduce these different material capacities?")):
        if any(v["state"] == "DIFFERENT" for v in out[relation].get("changes", {}).values()):
            out["next_questions"].append({"relation": relation, "question": question})
    if any(f["changes"].get("status", {}).get("state") == "DIFFERENT" for f in out["epr"].get("formations", [])):
        out["next_questions"].append({"relation": "epr", "question": "Is a comparable source-local repertoire differently aligned with group executive position?"})
    out["limits"] = "Literal published values, not harmonized estimates, actual legal applicability, causal effects or person endowments."
    return out


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def _projection(answer):
    """Consume the S04 export contract, not reissue it. Integrity is not authority."""
    m = deepcopy(answer.material())
    ref = deepcopy(answer.ref.as_dict())
    digest = hashlib.sha256(_json(m).encode()).hexdigest()
    if (m.get("contract") != S04_CONTRACT or m.get("grade") != S04_GRADE or
            ref != {"kind": S04_CONTRACT, "object_id": "urn:rawlsing:s04:general-projection:sha256:" + digest,
                    "content_hash": digest}):
        raise ValueError("not an intact S04 projection export")
    return {"ref": ref, "material": m}


def repertoire_contrast(left_answer, right_answer):
    """Reuse S04's existing output fractions; compare only a shared source fact/domain."""
    a, b = _projection(left_answer), _projection(right_answer)
    x, y = a["material"], b["material"]
    out = {"left": a, "right": b, "grade": "EXPORTED_S04_COMPARISON_NOT_SOURCE_ISSUANCE", "cells": []}
    required = ("source_fact_ref", "source_release_ref", "source_universe_ref", "source_risk_set_ref",
                "source_measure_basis_ref", "source_response_semantics_ref", "output_axes",
                "raw_original_full_joint_resolved_n", "raw_source_eligible_n")
    if any(k not in x or k not in y or x[k] is None or x[k] != y[k] for k in required):
        return dict(out, state="SEPARATE_SCOPES_NO_NUMERICAL_COMPARISON")
    if any(m.get("state") != "OBSERVED_FULL_CASE_SUPPORT" for m in (x, y)):
        return dict(out, state="UPSTREAM_NONPOSITIVE_RETAINED")
    def cells(m):
        n = m["raw_selected_full_case_n"]
        if type(n) is not int or n <= 0:
            raise ValueError("invalid selected full-case support")
        result, total = {}, 0
        for cell in m["complete_output_cells"]:
            key = _json(cell["output_states"])
            count = cell["raw_count"]
            if key in result or type(count) is not int or count < 0:
                raise ValueError("invalid or duplicated S04 cell")
            f = Fraction(*cell["raw_fraction_of_selected_full_cases"]["$exact_fraction"])
            if f != Fraction(count, n):
                raise ValueError("S04 fraction disagrees with count and scope")
            total += count
            result[key] = f
        if total != n:
            raise ValueError("S04 output support not conserved")
        return result
    l, r = cells(x), cells(y)
    if l.keys() != r.keys():
        return dict(out, state="DISTINCT_OUTPUT_DOMAINS")
    out["cells"] = [{"output_states": json.loads(k), "difference_right_minus_left":
                     [ (r[k]-l[k]).numerator, (r[k]-l[k]).denominator ]} for k in sorted(l)]
    return dict(out, state="SAME_FACT_DESCRIPTIVE_FULL_CASE_CONTRAST")


def formation_repertoire_contrast(pack, left, right, left_answer, right_answer):
    """Two independently selected EPR group/year keys plus two S04 exports.

    A caller's association is an explicitly modeled juxtaposition, never a
    qualified identity crosswalk or empirical assertion of group alignment.
    """
    def get(key):
        gwid, group, year = key
        return pack.select("EPR", {"gwid": gwid, "gwgroupid": group}, year=year)
    material = unique_contrast(get(left), get(right), ("status", "size", "reg_aut"))
    empirical = repertoire_contrast(left_answer, right_answer)
    return {"grade": "PROVISIONAL_MODELED_JUXTAPOSITION_NOT_GROUP_CROSSWALK",
            "material": material, "empirical": empirical,
            "state": "ALIGNED_HISTORICAL_CLAIM_HELD",
            "question": "Does independent group position distinguish the practical force of comparable repertoires?",
            "unresolved": ["qualified source-position to EPR correspondence", "public recognition and practice",
                           "actual resource/control relation", "world rule and applicable reader"]}


def inquire_repertoire_fracture(session, question, *, position_states, repertoire_axes,
                                response_act_meanings, modeled_context, propose, revise,
                                pack=None, context_requests=()):
    """R11 internal, sourcefree inquiry through the actual #1292 dynamic owner.

    One existing catalog query, then three forward projections and one proposed
    reverse inquiry on its live workspace. No new I03 execution for followups.
    Interpretation callbacks are proposal machinery, never source/science/world
    issuers. Their input is aggregate only and explicitly SOURCEFREE. This is
    not an original-source disclosure surface or a downstream person packet.
    """
    from rawlsing_next.pre553_s04_dynamic_research import (
        S04DynamicQuestion, S04DynamicResearchSession,
    )
    from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
    from authored_world_handoff import select_world_evidence

    if type(session) is not S04DynamicResearchSession or type(question) is not S04DynamicQuestion:
        raise TypeError("actual sourcefree dynamic research session/question required")
    position = question.conditioner_index
    if (type(position) is not int or position < 0 or type(repertoire_axes) is not tuple
            or len(repertoire_axes) < 2 or any(type(a) is not int or a < 0 for a in repertoire_axes)
            or len(set(repertoire_axes)) != len(repertoire_axes) or position in repertoire_axes):
        raise ValueError("distinct position and at least two repertoire axes required")
    if (type(position_states) is not tuple or len(position_states) != 2
            or _json(position_states[0]) == _json(position_states[1])):
        raise ValueError("two distinct explicitly selected reported positions required")
    if (type(response_act_meanings) is not dict
            or set(response_act_meanings) != {position, *repertoire_axes}
            or any(not isinstance(v, str) or not v.strip() for v in response_act_meanings.values())):
        raise ValueError("explicit caller-proposed meanings for each selected axis required")
    if not isinstance(modeled_context, str) or not modeled_context.strip():
        raise ValueError("explicit fictional institutional context required")
    if not callable(propose) or not callable(revise):
        raise TypeError("proposal and revision callbacks required")
    requests = tuple(context_requests)
    if requests and pack is None:
        raise ValueError("native context selection requires a pack")
    # Do not send native context values to the sourcefree proposal callbacks.
    # The separate read remains internal, without a crosswalk or use grant.
    native_context = (select_world_evidence(pack, requests) if requests else
                      {"grade": "HELD_NO_SELECTED_NATIVE_CONTEXT", "observations": []})
    result = session.ask(question)
    original = result.original
    knowledge = original.knowledge.material()
    ff = original.ff01.semantic_projection()
    obs = result.observation_scope.material()
    if (ff["producer_fact_ref"] != knowledge["fact_ref"]
            or ff["conditioner_index"] != position
            or obs["knowledge_ref"] != original.knowledge.ref.as_dict()
            or obs["fact_ref"] != knowledge["fact_ref"]):
        raise ValueError("inconsistent incumbent FF01/S04/observation identity")
    axes = (position, *repertoire_axes)
    if any(a >= knowledge["target_arity"] for a in axes):
        raise ValueError("selected role outside source target domain")

    def ask(output_axes, conditions):
        answer = result.joint_workspace.query(S04Projection(output_axes, conditions))
        exported = _projection(answer)
        if exported["material"]["knowledge_ref"] != original.knowledge.ref.as_dict():
            raise ValueError("workspace escaped retained source knowledge")
        return answer, exported

    _, baseline = ask(repertoire_axes, {})
    left, _ = ask(repertoire_axes, {position: position_states[0]})
    right, _ = ask(repertoire_axes, {position: position_states[1]})
    contrast = repertoire_contrast(left, right)
    # Full receipt is local only. In particular do not pass the observation
    # cohort fingerprint, respondent refs or authority chain to a callback.
    obs_public = {k: deepcopy(v) for k, v in obs.items()
                  if k not in ("verified_eligible_member_set_sha256",
                               "source_asked_eligible_raw_summary")}
    packet = {
        "grade": "INTERNAL_SOURCEFREE_FF_INQUIRY_NOT_SOURCE_OR_WORLD_ISSUANCE",
        "ff01_ref": original.ff01.ref.as_dict(),
        "knowledge_ref": original.knowledge.ref.as_dict(),
        "observation_ref": result.observation_scope.ref.as_dict(),
        "observation": obs_public,
        "baseline": baseline,
        "contrast": contrast,
        "independent_native_context": native_context,
        "context_alignment": "NO_SURVEY_TO_MATERIAL_CROSSWALK",
        "modeled_context": {"grade": "EXPLICIT_FICTIONAL_PREMISE", "description": modeled_context},
        "response_act_meanings": {str(k): v for k, v in response_act_meanings.items()},
        "meaning_grade": "CALLER_PROPOSED_NOT_SOURCE_SEMANTIC_ISSUANCE",
        "proposal": None, "reverse": None, "revision": None,
    }
    if contrast["state"] != "SAME_FACT_DESCRIPTIVE_FULL_CASE_CONTRAST":
        return dict(packet, state="NO_POSITIVE_CONTRAST__OBSERVATION_LIMIT_RETAINED")

    def aggregate(export):
        m = export["material"]
        return {k: deepcopy(m[k]) for k in (
            "state", "output_axes", "conditions", "raw_selected_full_case_n",
            "raw_source_eligible_n", "raw_original_full_joint_resolved_n",
            "complete_output_cells",
        )}

    view = {
        "grade": "SYNTHETIC_SOURCEFREE_SAMPLE_ONLY",
        "axis_meanings": packet["response_act_meanings"],
        "position_axis": position,
        "repertoire_axes": list(repertoire_axes),
        "baseline": aggregate(baseline),
        "left": aggregate(contrast["left"]),
        "right": aggregate(contrast["right"]),
        "differences": deepcopy(contrast["cells"]),
        "observation_limits": {
            k: deepcopy(obs[k]) for k in (
                "state", "source_frame_population_n", "survey_design_weight_or_variance",
                "condition_membership_unknown_n", "observed_route_and_nonresponse_cause",
            )
        },
        "fictional_institution": modeled_context,
        "native_context": "SEPARATE_INTERNAL_READ_NOT_AVAILABLE_FOR_ALIGNMENT",
    }
    proposal = deepcopy(propose(deepcopy(view)))
    if (type(proposal) is not dict or set(proposal) != {"concept", "rival", "question", "motif"}
            or any(not isinstance(proposal[k], str) or not proposal[k].strip()
                   for k in ("concept", "rival", "question"))
            or type(proposal["motif"]) is not list or len(proposal["motif"]) != len(repertoire_axes)):
        raise ValueError("concept, rival, question and exact joint motif required")
    # Reverse conditioning is a genuine subsequent existing S04 operation;
    # invalid native response states are rejected by its own typed algebra.
    _, reverse = ask((position,), dict(zip(repertoire_axes, proposal["motif"])))
    revision = deepcopy(revise(deepcopy(view), deepcopy(proposal), aggregate(reverse)))
    if (type(revision) is not dict or set(revision) != {"interpretation", "remaining_question", "recipient_possibility"}
            or any(not isinstance(v, str) or not v.strip() for v in revision.values())):
        raise ValueError("explicit provisional interpretation, residual question and recipient possibility required")
    # Check CURRENT once more after the external interpretation callback,
    # including when the callback returns normally after source revocation.
    _, final_reverse = ask((position,), dict(zip(repertoire_axes, proposal["motif"])))
    if final_reverse != reverse:
        raise ValueError("reverse source result changed during interpretation")
    return dict(packet, state="PROVISIONAL_CONCEPT_REVISED_NOT_CERTIFIED",
                proposal=proposal, reverse=reverse, revision=revision,
                revision_grade="ABDUCTIVE_PROPOSAL_NOT_EMPIRICAL_ADJUDICATION",
                recipient_state="POSSIBILITY_ONLY__C6_AND_WORLD_OWNER_RECEIVING_HELD")
