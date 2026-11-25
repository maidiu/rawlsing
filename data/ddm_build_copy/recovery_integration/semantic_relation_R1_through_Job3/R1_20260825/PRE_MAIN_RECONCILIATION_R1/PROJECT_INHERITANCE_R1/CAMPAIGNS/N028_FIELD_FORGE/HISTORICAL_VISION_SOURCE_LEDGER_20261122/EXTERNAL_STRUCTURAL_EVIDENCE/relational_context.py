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


def _validate_social_roles(session, question, position_axes, repertoire_axes,
                           axis_meanings, active_ancestry):
    from rawlsing_next.pre553_s04_dynamic_research import (
        S04DynamicQuestion, S04DynamicResearchSession,
    )

    if type(session) is not S04DynamicResearchSession or type(question) is not S04DynamicQuestion:
        raise TypeError("actual sourcefree dynamic research session/question required")
    if (type(position_axes) is not tuple or type(repertoire_axes) is not tuple
            or len(position_axes) < 2 or len(repertoire_axes) < 2):
        raise ValueError("two independent position and repertoire axes required")
    axes = position_axes + repertoire_axes
    if (any(type(a) is not int or a < 0 for a in axes)
            or len(set(axes)) != len(axes) or question.conditioner_index not in position_axes):
        raise ValueError("distinct ordered position/disposition axes and FF01 anchor required")
    if (type(axis_meanings) is not dict or set(axis_meanings) != set(axes)
            or any(not isinstance(v, str) or not v.strip() for v in axis_meanings.values())):
        raise ValueError("explicit axis meanings required")
    if (type(active_ancestry) is not dict or set(active_ancestry) != set(axes)
            or any(type(v) is not tuple or not v or
                   any(not isinstance(x, str) or not x.strip() for x in v)
                   for v in active_ancestry.values())):
        raise ValueError("explicit caller-declared active measurement ancestry required")
    p_roots = {v for a in position_axes for v in active_ancestry[a]}
    d_roots = {v for a in repertoire_axes for v in active_ancestry[a]}
    if p_roots & d_roots:
        raise ValueError("shared active position/disposition ancestry")
    return axes


def _validate_social_result(result, question, axes, position_axes, repertoire_axes):
    original = result.original
    knowledge = original.knowledge.material()
    ff = original.ff01.semantic_projection()
    obs = result.observation_scope.material()
    if (ff["producer_fact_ref"] != knowledge["fact_ref"]
            or ff["conditioner_index"] != question.conditioner_index
            or obs["knowledge_ref"] != original.knowledge.ref.as_dict()
            or obs["fact_ref"] != knowledge["fact_ref"]):
        raise ValueError("inconsistent incumbent FF01/S04/observation identity")
    if set(axes) != set(range(knowledge["target_arity"])):
        raise ValueError("explicit roles required for every queried axis")
    # Even different axis indices may reference the same native measurement.
    targets = knowledge["target_refs"]
    if ({_json(targets[a]) for a in position_axes} &
            {_json(targets[a]) for a in repertoire_axes}):
        raise ValueError("shared actual target identity")

    return original, knowledge, obs


def inquire_social_field(session, question, *, position_axes, repertoire_axes,
                         axis_meanings, active_ancestry, contrasts, propose, revise):
    """Public R14 entry: one actual saved I03 question, selected contrasts."""
    return _inquire_social_field(session, question, position_axes=position_axes,
        repertoire_axes=repertoire_axes, axis_meanings=axis_meanings,
        active_ancestry=active_ancestry, contrasts=contrasts, propose=propose, revise=revise)


def _inquire_social_field(session, question, *, position_axes, repertoire_axes,
                         axis_meanings, active_ancestry, contrasts, propose, revise, _result=None):
    """R14: selected multidimensional correspondence over the incumbent S04 joint.

    Caller roles/ancestry and advantage directions are provisional SOURCEFREE
    declarations, not independently issued classifications. Each contrast is
    (label, left_conditions, right_conditions) on identical position axes.
    Preserve marginal and intersection contrasts, baseline and reverse
    composition; no Cartesian expansion beyond the existing S04 joint.
    No external pack, world assumption, new estimator or actor issuance.
    """
    from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
    axes = _validate_social_roles(session, question, position_axes, repertoire_axes,
                                  axis_meanings, active_ancestry)
    if not callable(propose) or not callable(revise):
        raise TypeError("proposal and revision callbacks required")
    contrasts = tuple(deepcopy(tuple(contrasts)))
    if not contrasts:
        raise ValueError("selected position contrasts required")
    labels = set()
    for label, left, right in contrasts:
        if (not isinstance(label, str) or not label.strip() or label in labels
                or type(left) is not dict or type(right) is not dict
                or not left or set(left) != set(right) or not set(left) <= set(position_axes)
                or _json(left) == _json(right)):
            raise ValueError("distinct named same-axis position contrasts required")
        labels.add(label)

    result = session.ask(question) if _result is None else _result
    original, knowledge, obs = _validate_social_result(
        result, question, axes, position_axes, repertoire_axes)

    def ask(output, conditions):
        answer = result.joint_workspace.query(S04Projection(output, conditions))
        export = _projection(answer)
        if export["material"]["knowledge_ref"] != original.knowledge.ref.as_dict():
            raise ValueError("projection escaped retained source knowledge")
        return answer, export

    def aggregate(export):
        m = export["material"]
        # No raw respondent IDs or authority references in interpretation view.
        return {"state": m["state"],
                "axes": [a["index"] for a in m["output_axes"]],
                "conditions": [{"axis": c["index"], "value": deepcopy(c["value"])}
                               for c in m["conditions"]],
                "selected_n": m["raw_selected_full_case_n"],
                "eligible_n": m["raw_source_eligible_n"],
                "resolved_n": m["raw_original_full_joint_resolved_n"],
                "cells": deepcopy(m["complete_output_cells"])}

    def fraction(cell):
        value = cell["raw_fraction_of_selected_full_cases"]
        return None if value is None else Fraction(*value["$exact_fraction"])

    def pair(v):
        return None if v is None else [v.numerator, v.denominator]

    def indexed(export):
        return {_json(c["output_states"]): c for c in export["material"]["complete_output_cells"]}

    _, base = ask(repertoire_axes, {})
    _, positions = ask(position_axes, {})
    # Full joint retains cross-position reach. Its cardinality is bounded by
    # the original admitted joint, not a new dense global social field.
    _, joint = ask(axes, {})
    packet = {"grade": "INTERNAL_SOURCEFREE_FF_SOCIAL_FIELD_NOT_POWER_OR_WORLD_ISSUANCE",
              "knowledge_ref": original.knowledge.ref.as_dict(),
              "observation_ref": result.observation_scope.ref.as_dict(),
              "role_grade": "CALLER_DECLARED_ANCESTRY_AND_MEANINGS_NOT_INDEPENDENT_ROLE_ISSUANCE",
              "position_axes": list(position_axes), "repertoire_axes": list(repertoire_axes),
              "axis_meanings": {str(k): v for k, v in axis_meanings.items()},
              "active_ancestry": {str(k): list(v) for k, v in active_ancestry.items()},
              "baseline": base, "positions": positions, "joint": joint,
              "contrasts": [], "proposal": None, "motifs": [], "revision": None,
              "observation_limits": {k: deepcopy(obs[k]) for k in (
                  "state", "source_frame_population_n", "survey_design_weight_or_variance",
                  "condition_membership_unknown_n", "observed_route_and_nonresponse_cause")},
              "external_context": "NOT_REQUIRED_FOR_DESCRIPTIVE_CORRESPONDENCE"}
    baseline = indexed(base)
    for label, left, right in contrasts:
        la, le = ask(repertoire_axes, left)
        ra, re = ask(repertoire_axes, right)
        delta = repertoire_contrast(la, ra)
        _, lp = ask((), left)
        _, rp = ask((), right)
        # Compare each conditional to its own baseline. Zero denominator
        # cannot be treated as zero prevalence or enrichment.
        def enrich(export):
            out = []
            for key, cell in indexed(export).items():
                p, b = fraction(cell), fraction(baseline[key])
                out.append({"states": cell["output_states"],
                            "enrichment": pair(p/b if p is not None and b else None)})
            return out
        packet["contrasts"].append({"label": label, "left": le, "right": re,
                                    "left_position_support": lp, "right_position_support": rp,
                                    "difference_state": delta["state"], "differences": delta["cells"],
                                    "left_enrichment": enrich(le), "right_enrichment": enrich(re)})
    if base["material"]["state"] != "OBSERVED_FULL_CASE_SUPPORT":
        return dict(packet, state="UPSTREAM_NONPOSITIVE_RETAINED")

    view = {"grade": "SYNTHETIC_SOURCEFREE_SAMPLE_ONLY",
            "position_axes": list(position_axes), "repertoire_axes": list(repertoire_axes),
            "axis_meanings": packet["axis_meanings"],
            "baseline": aggregate(base), "positions": aggregate(positions),
            "joint": aggregate(joint), "observation_limits": packet["observation_limits"],
            "contrasts": [{"label": c["label"], "left": aggregate(c["left"]),
                           "right": aggregate(c["right"]), "differences": c["differences"],
                           "difference_state": c["difference_state"],
                           "left_enrichment": c["left_enrichment"],
                           "right_enrichment": c["right_enrichment"]}
                          for c in packet["contrasts"]]}
    proposal = deepcopy(propose(deepcopy(view)))
    if (type(proposal) is not dict or set(proposal) != {"concept", "rival", "question", "motifs"}
            or any(not isinstance(proposal[k], str) or not proposal[k].strip()
                   for k in ("concept", "rival", "question"))
            or type(proposal["motifs"]) is not list or len(proposal["motifs"]) < 2
            or any(type(m) is not list or len(m) != len(repertoire_axes) for m in proposal["motifs"])
            or len({_json(m) for m in proposal["motifs"]}) != len(proposal["motifs"])):
        raise ValueError("concept, rival, question and distinct exact joint motifs required")
    packet["proposal"] = proposal
    for motif in proposal["motifs"]:
        cond = dict(zip(repertoire_axes, motif))
        _, reverse = ask(position_axes, cond)
        key = _json(motif)
        base_cell = baseline[key]  # S04 validates exact source-domain states.
        # For each selected position, distinguish P(D|C), P(C|D), and
        # P(D,C) using the original S04 support and full-case denominator.
        motif_rows = []
        for c in packet["contrasts"]:
            for side in ("left", "right"):
                e = c[side]
                poscond = {v["index"]: v["value"] for v in e["material"]["conditions"]}
                _, rev = ask((), {**cond, **poscond})
                hit = indexed(e).get(key)
                both = rev["material"]["raw_selected_full_case_n"]
                total = base["material"]["raw_selected_full_case_n"]
                motif_n = reverse["material"]["raw_selected_full_case_n"]
                if hit is not None and hit["raw_count"] != both:
                    raise ValueError("forward/reverse joint support mismatch")
                motif_rows.append({"label": c["label"], "side": side,
                                   "joint_support": rev,
                                   "prevalence": pair(fraction(hit) if hit else None),
                                   "composition": pair(Fraction(both, motif_n)
                                                       if motif_n and both is not None else None),
                                   "joint_mass": pair(Fraction(both, total)
                                                     if total and both is not None else None)})
        packet["motifs"].append({"motif": motif, "baseline_count": base_cell["raw_count"],
                                 "reverse": reverse, "selected_positions": motif_rows})
    public_motifs = [{"motif": m["motif"], "baseline_count": m["baseline_count"],
                      "reverse": aggregate(m["reverse"]),
                      "selected_positions": [{k: deepcopy(v) for k,v in r.items()
                                              if k != "joint_support"}
                                             for r in m["selected_positions"]]}
                     for m in packet["motifs"]]
    revision = deepcopy(revise(deepcopy(view), deepcopy(proposal), deepcopy(public_motifs)))
    if (type(revision) is not dict
            or set(revision) != {"interpretation", "remaining_question", "recipient_possibility"}
            or any(not isinstance(v, str) or not v.strip() for v in revision.values())):
        raise ValueError("explicit revised interpretation, question and recipient possibility required")
    # Existing workspace guard rechecks source CURRENT after semantic work.
    _, final_base = ask(repertoire_axes, {})
    if final_base != base:
        raise ValueError("source result changed during interpretation")
    return dict(packet, state="PROVISIONAL_SOCIAL_FIELD_REVISED_NOT_CERTIFIED",
                revision=revision, recipient_state="DESCRIPTIVE_POSSIBILITIES_ONLY__RECEIVING_HELD")


def discover_social_field(session, question, *, position_axes, repertoire_axes,
                          axis_meanings, active_ancestry, discovery_authority,
                          authority_registry, root_rule, child_rule, budget,
                          max_position_order, min_position_n, interpret, revise):
    """R15: productive discovery within one admitted sourcefree joint.

    Existing I05 adaptive scheduler owns scheduling, budget and coverage.
    Existing S04 DHIKR owns information/synergy diagnostics, not FF.
    FF discovers exact joint motif contrasts on position subsets and feeds
    positive findings back into the existing R14 inquiry and a semantic
    callback. No caller-selected motif, contrast, or universal power rank.
    This is an in-sample exploratory search, not source/science issuance.
    """
    from rawlsing_next.pre553_discovery_adaptive import (
        AdaptiveExplorationUnit, AdaptiveUnitOutcome, execute_adaptive_exploration,
    )
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
    from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
    from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest

    axes = _validate_social_roles(session, question, position_axes, repertoire_axes,
                                  axis_meanings, active_ancestry)
    if (type(budget) is not int or budget < 1
            or type(max_position_order) is not int
            or not 1 <= max_position_order <= len(position_axes)
            or type(min_position_n) is not int or min_position_n < 2
            or not callable(interpret) or not callable(revise)):
        raise ValueError("explicit positive search budget, position order, support and callbacks required")
    result = session.ask(question)
    original, knowledge, obs = _validate_social_result(
        result, question, axes, position_axes, repertoire_axes)
    workspace = result.joint_workspace

    def project(output, conditions):
        answer = workspace.query(S04Projection(output, conditions))
        export = _projection(answer)
        if export["material"]["knowledge_ref"] != original.knowledge.ref.as_dict():
            raise ValueError("projection escaped retained source knowledge")
        return answer, export

    def seal(kind, payload):
        digest = semantic_hash(payload)
        return ExactRef(kind, "urn:rawlsing:ff:r15:" + kind.lower() + ":" + digest, digest)

    def fraction(cell):
        v = cell["raw_fraction_of_selected_full_cases"]
        return None if v is None else Fraction(*v["$exact_fraction"])

    def pair(v):
        return [v.numerator, v.denominator]

    def public_projection(export):
        m = export["material"]
        return {"state": m["state"], "selected_n": m["raw_selected_full_case_n"],
                "cells": deepcopy(m["complete_output_cells"])}

    _, baseline = project(repertoire_axes, {})
    # Each target's existing DHIKR diagnostic can nominate interaction
    # questions even when every single position association is zero.
    # The incumbent has a documented 8-predictor bound; do not silently
    # truncate or claim a diagnostic for a larger universe.
    diagnostics = []
    for target in repertoire_axes:
        predictors = tuple(a for a in axes if a != target)
        if len(predictors) > 8:
            diagnostics.append({"target_axis": target,
                "state": "DHIKR_PREDICTOR_BOUND__NO_DIAGNOSTIC"})
            continue
        receipt = workspace.compare_dhikr(DHIKRComparisonRequest(
            target, predictors, min_branch_n=min_position_n,
            max_depth=0, max_nodes=1, max_interaction_order=min(3,len(predictors))))
        m = receipt.material()
        if m["source_knowledge_ref"] != original.knowledge.ref.as_dict():
            raise ValueError("DHIKR diagnostic escaped retained knowledge")
        diagnostics.append({"target_axis": target, "ref": receipt.ref.as_dict(), "material": m})

    determinant = seal("FF_SOCIAL_DISCOVERY_DETERMINANT", {
        "knowledge_ref": original.knowledge.ref.as_dict(),
        "observation_ref": result.observation_scope.ref.as_dict(),
        "position_axes": list(position_axes), "repertoire_axes": list(repertoire_axes),
        "axis_meanings": {str(k): v for k,v in axis_meanings.items()},
        "active_ancestry": {str(k): list(v) for k,v in active_ancestry.items()},
        "max_position_order": max_position_order, "min_position_n": min_position_n,
        "diagnostics": diagnostics, "policy": "R15_SELECTED_POSITION_SUBSETS_V1"})
    order = tuple(sorted(position_axes))
    specs, records = {}, {}
    priority_axes = set()
    for d in diagnostics:
        for node in d.get("material", {}).get("nodes", []):
            priority_axes.update(node["priority_group"])
    definition = discovery_authority.candidate_universe_definition
    frontier_cap = definition["maximum_frontier_size"]
    generation_cap = definition["maximum_generation"]

    def make_unit(subset, parent=None, sealed=None, rank=0):
        # Canonical increasing subsets have exactly one parent. The
        # scheduler still verifies parent result, determinant and rule.
        ref = seal("FF_SOCIAL_POSITION_UNIT", {
            "determinant": determinant.as_dict(), "axes": list(subset)})
        unit = AdaptiveExplorationUnit(
            unit_ref=ref, proposal_rule_ref=root_rule if parent is None else child_rule,
            generation=len(subset)-1, heuristic_rank=rank,
            determinant_refs=(determinant,) if parent is None else (determinant,sealed),
            parent_unit_ref=None if parent is None else parent.unit_ref)
        specs[ref.key] = subset
        return unit

    roots = tuple(make_unit((a,), rank=int(a in priority_axes)) for a in order)

    def evaluate(unit, history):
        subset = specs[unit.unit_ref.key]
        _, positions = project(subset, {})
        contexts, excluded = [], []
        for row in positions["material"]["complete_output_cells"]:
            conditions = dict(zip(subset, row["output_states"]))
            if row["raw_count"] < min_position_n:
                excluded.append({"conditions": [[a,v] for a,v in conditions.items()],
                    "raw_n": row["raw_count"], "state": "BELOW_SELECTED_SUPPORT__NOT_ABSENCE"})
                continue
            answer, export = project(repertoire_axes, conditions)
            contexts.append((conditions, answer, export))

        # Compare extrema of each actually observed joint motif, using
        # exact fractions already issued by S04. Keep all searched motifs,
        # including constant profiles and rare positive alternatives.
        candidates = []
        for b in baseline["material"]["complete_output_cells"]:
            if b["raw_count"] <= 0 or len(contexts) < 2:
                continue
            key = _json(b["output_states"])
            supported = []
            for cond, answer, exp in contexts:
                cell = next(c for c in exp["material"]["complete_output_cells"]
                            if _json(c["output_states"]) == key)
                supported.append((fraction(cell), cond, answer, exp))
            supported.sort(key=lambda x: (x[0], _json(x[1])))
            low, high = supported[0], supported[-1]
            gap = high[0] - low[0]
            candidates.append({"motif": deepcopy(b["output_states"]),
                "baseline_n": b["raw_count"], "gap": pair(gap),
                "low": [[a,v] for a,v in low[1].items()],
                "high": [[a,v] for a,v in high[1].items()],
                "low_prevalence": pair(low[0]), "high_prevalence": pair(high[0]),
                "low_ref": low[3]["ref"], "high_ref": high[3]["ref"]})
        candidates.sort(key=lambda x: (-Fraction(*x["gap"]), x["baseline_n"], _json(x["motif"])))
        top = candidates[0] if candidates else None
        view = {"grade": "SYNTHETIC_SOURCEFREE_SAMPLE_ONLY",
                "position_axes": list(subset), "repertoire_axes": list(repertoire_axes),
                "axis_meanings": {str(k): v for k,v in axis_meanings.items()},
                "baseline": public_projection(baseline),
                "contexts": [{"conditions": [[a,v] for a,v in cond.items()],
                              "repertoire": public_projection(exp)} for cond,_,exp in contexts],
                "excluded": excluded,
                "candidates": [{k: deepcopy(v) for k,v in x.items() if not k.endswith("_ref")}
                               for x in candidates],
                "earlier_questions": [records[v.unit.unit_ref.key]["interpretation"]["question"]
                                      for v in history],
                "eligible_extension_axes": [a for a in order if a > subset[-1]
                                             and len(subset) < max_position_order
                                             and unit.generation < generation_cap]}
        interpretation = deepcopy(interpret(deepcopy(view)))
        if (type(interpretation) is not dict
                or set(interpretation) != {"concept","rival","question","preferred_axis"}
                or any(not isinstance(interpretation[k], str) or not interpretation[k].strip()
                       for k in ("concept","rival","question"))
                or (interpretation["preferred_axis"] is not None
                    and (type(interpretation["preferred_axis"]) is not int
                         or interpretation["preferred_axis"] not in view["eligible_extension_axes"]))):
            raise ValueError("interpretation must nominate only an eligible next position axis")
        followthrough = None
        if top is not None and Fraction(*top["gap"]) > 0:
            left, right = dict(top["low"]), dict(top["high"])
            la, _ = project(repertoire_axes, left)
            ra, _ = project(repertoire_axes, right)
            delta = repertoire_contrast(la, ra)
            # A rival is selected from actual opposite redistribution on
            # these exact contexts, not invented by the callback.
            rivals = [v for v in delta["cells"] if
                      Fraction(*v["difference_right_minus_left"]) < 0]
            rivals.sort(key=lambda v: (Fraction(*v["difference_right_minus_left"]),
                                      _json(v["output_states"])))
            if not rivals:
                raise ValueError("positive redistribution without conserved counterweight")
            motif_pair = [top["motif"], rivals[0]["output_states"]]
            followthrough = _inquire_social_field(session, question,
                position_axes=position_axes, repertoire_axes=repertoire_axes,
                axis_meanings=axis_meanings, active_ancestry=active_ancestry,
                contrasts=(("discovered:" + ",".join(map(str,subset)), left, right),),
                propose=lambda _: {"concept": interpretation["concept"],
                    "rival": interpretation["rival"], "question": interpretation["question"],
                    "motifs": deepcopy(motif_pair)}, revise=revise, _result=result)
        # Recheck CURRENT after semantic callbacks even if all marginal
        # differences vanish. A null marginal must not prune intersections.
        project((), {})
        record = {"unit_ref": unit.unit_ref.as_dict(), "position_axes": list(subset),
                  "positions": positions, "conditional_repertoires": [e for _,_,e in contexts],
                  "excluded": excluded, "candidates": candidates,
                  "interpretation": interpretation, "followthrough": followthrough,
                  "not_proposed": []}
        eligible = view["eligible_extension_axes"]
        # Explicitly retain any known extension excluded by the finite
        # authority frontier; an unscheduled axis is never a negative.
        preference = interpretation["preferred_axis"]
        chosen = sorted(eligible, key=lambda a: (a != preference, a not in priority_axes, a))
        room = max(0, frontier_cap - len(specs))
        for a in chosen[room:]:
            record["not_proposed"].append({"axis": a, "state": "AUTHORITY_FRONTIER_LIMIT__UNKNOWN"})
        if len(subset) >= max_position_order or unit.generation >= generation_cap:
            record["not_proposed"].extend({"axis": a, "state": "POSITION_ORDER_OR_GENERATION_LIMIT__UNKNOWN"}
                                         for a in order if a > subset[-1])
        sealed = seal("FF_SOCIAL_DISCOVERY_UNIT_RESULT", record)
        proposals = []
        rank = int(1000 * Fraction(*top["gap"])) if top else 0
        for a in chosen[:room]:
            proposals.append(make_unit(subset+(a,), parent=unit, sealed=sealed,
                rank=rank + (1001 if a == preference else 0) + int(a in priority_axes)))
        records[unit.unit_ref.key] = record
        return AdaptiveUnitOutcome(unit_ref=unit.unit_ref, sealed_result_ref=sealed,
            proposal_basis_ref=seal("FF_SOCIAL_DISCOVERY_PROPOSAL_BASIS", {
                "sealed": sealed.as_dict(), "proposal_axes": [specs[u.unit_ref.key] for u in proposals],
                "heuristic_not_truth": True}),
            unit_result_state="SEALED_SOURCEFREE_POSITION_SUBSET_INQUIRY",
            proposal_units=tuple(proposals))

    search = execute_adaptive_exploration(discovery_authority=discovery_authority,
        authority_registry=authority_registry, determinant_state_ref=determinant,
        initial_units=roots, evaluate_unit=evaluate, budget=budget)
    project((), {})
    return {"grade": "INTERNAL_SOURCEFREE_FF_DISCOVERY_NOT_SOURCE_SCIENCE_OR_WORLD_ISSUANCE",
            "knowledge_ref": original.knowledge.ref.as_dict(),
            "observation_ref": result.observation_scope.ref.as_dict(),
            "diagnostics": diagnostics, "determinant_ref": determinant.as_dict(),
            "baseline": baseline, "records": [records[v.unit.unit_ref.key]
                                               for v in search.checkpoint.visits],
            "search_ref": search.result_ref.as_dict(), "checkpoint": search.checkpoint.as_dict(),
            "completeness_state": search.completeness_state,
            "unvisited": [{"unit_ref": u.as_dict(), "axes": list(specs[u.key]),
                           "state": "UNKNOWN_UNVISITED"} for u in search.unvisited_unit_refs],
            "global_negative_claim": False, "semantic_truth_effect": False,
            "actor_v3_effect": False}
